"""Realization archive + bandit climb (2026-10-30; user's brainstorms: MAP-Elites-style archive, bandit
scheduler instead of a fixed chain). What worked by hand on type 0 is automated here:
  * ARCHIVE: every exactly embedded polyhedron found (genus >= 2) with its map (dual triangles);
    several different realizations of the same map are kept (diversity gave the best genus-4 starts);
  * ARMS: (realization, next handle) for every handle after which all n(n-1)/2 pairs stay reachable
    (handle_add.reach); an arm's estimate = its best degeneracy-adjusted violation count so far (+1 for
    a shortest edge < 1e-4, +1 for a margin < 1e-5 of the diameter; start energy / 3 before the first try); priority = higher target genus first, then low estimate + exploration bonus;
  * DIVERSITY tasks (a quarter of the time): search an archived map again from a failed attempt or
    or from a strongly perturbed realization, to find a DIFFERENT realization (oriented matroid differs
    in >= 30 of the 495 signs, up to reorientation);
  * every task: annealing + CMA-ES with a degeneracy floor (edge < 3e-5, margin < 1e-6 of the diameter
    count as violations; near-solutions tend to hug the floor, so the log shows edge and margin), seeded
    from the arm's best attempt or from the realization; every float zero re-checked exactly.
A realization of the full map (genus 6, all 66 pairs) is a solution.
Gauss gate (review 2026-10-30; code/gauss_gate.py): every arm records T1 at its realization (degree of the
next map in the realized polyhedron's orientation, k_tau, number of admissible gauges for 1 - g'); every
task logs the class data of its best attempt (own degree vs 1 - g, faces with turning != +1). With
gate=True (run_overnight.py arch --gauss-gate) arms without an admissible gauge are never picked, so the
climb only spends time on arms in the right normal class and on diversity tasks (new realizations,
whose arms may pass).
State: OUT_DIR/archive.json (atomic) + OUT_DIR/results.jsonl (one line per task); resumable.
Usage: python3 -I archive_climb.py OUT_DIR HOURS WORKERS MINUTES_PER_TASK SEED_FILES... [--gauss-gate]"""
import json, os, sys, time, random
import multiprocessing as mp
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

N = 12
FULL_GENUS = (N - 3) * (N - 4) // 12
DIFFERENT = 30           # a realization is new if its oriented matroid differs in >= this many of the 495 signs
_Q = None; _P = None
FLOOR_EDGE, FLOOR_MARGIN = 3e-5, 1e-6   # degeneracy floor of the search energy (near-solutions tend to hug it)


def chirotope(H):
    """Signs of det of every 4 planes (the oriented matroid of the arrangement, 495 signs)."""
    import itertools
    global _Q
    if _Q is None:
        _Q = list(itertools.combinations(range(N), 4))
    H = np.array(H, float)
    return np.sign([np.linalg.det(H[list(q)]) for q in _Q]).astype(np.int8)


def om_distance(c1, c2):
    """Number of differing signs, minimized over reorientations (sign flips of single planes)."""
    global _P
    if _P is None:
        import itertools
        Q = list(itertools.combinations(range(N), 4))
        S = np.array([[1 if (m >> i) & 1 else -1 for i in range(N)] for m in range(1 << N)], np.int8)
        _P = np.stack([S[:, a] * S[:, b] * S[:, c] * S[:, d] for a, b, c, d in Q], 1)
    return int((_P * np.asarray(c1, np.int8)[None, :] != np.asarray(c2, np.int8)[None, :]).sum(1).min())


def mapkey(tris):
    return ';'.join('%d,%d,%d' % t for t in sorted(tuple(sorted(int(x) for x in t)) for t in tris))


def norm_planes(H):
    H = np.array(H, float); nr = np.linalg.norm(H[:, :3], axis=1)
    return H / nr[:, None]


def genus_of(tris):
    E = len({frozenset(e) for t in tris for e in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2]))})
    return (2 - (N - E + len(tris))) // 2


def worker(item):
    """One search task: (task_id, {'tris', 'seed_planes', 'minutes', 'seed'}) -> result record."""
    task, p = item
    import genus_ladder
    from gauss_degree import coherent_triangles, links_from
    from ladder_exact import verify
    genus_ladder.use_floor(edge=FLOOR_EDGE, margin=FLOOR_MARGIN)
    from ladder import pack, degeneracy
    t0 = time.monotonic()
    tris = [tuple(t) for t in p['tris']]
    L = links_from(coherent_triangles(tris), N)
    (b, H), _ = genus_ladder.search(L, N, p['minutes'], np.random.default_rng(p['seed']), p['seed_planes'])
    rec = {'task': task, 'kind': p['kind'], 'arm': p.get('arm'), 'map': p['map'], 'genus': genus_of(tris),
           'best': float(b), 'seconds': round(time.monotonic() - t0, 1)}
    Hn = np.array(H, float); nr = np.linalg.norm(Hn[:, :3], axis=1); Hn[:, :3] /= nr[:, None]; Hn[:, 3] /= nr
    e_rel, m_rel = degeneracy(Hn, *pack(L)[:2])
    rec['edge'] = float(e_rel); rec['margin'] = float(m_rel)
    try:
        from gauss_gate import config_report
        cr = config_report(H.tolist(), tris, gauges=False)
        rec['degree'] = cr.get('own_degree'); rec['target_degree'] = cr['target_degree']
        rec['bad_turning'] = cr.get('bad_turning_faces')
    except Exception as e:                           # noqa: BLE001
        rec['degree_error'] = repr(e)[:200]
    if b < 4.5:
        rec['planes'] = H.tolist()
    if b < 0.5:
        ex = verify(H.tolist(), L, require_all_pairs=(genus_of(tris) == FULL_GENUS))
        rec['exact'] = bool(ex['EMBEDDED'])
    return rec


class Archive:
    def __init__(self, path):
        self.path = path
        self.real = []; self.arms = {}; self.attempts = {}; self.maps = {}; self.done = 0
        if os.path.exists(path):
            d = json.load(open(path))
            self.real, self.arms, self.attempts, self.maps, self.done = d['real'], d['arms'], d['attempts'], d['maps'], d['done']

    def save(self):
        tmp = self.path + '.tmp'
        json.dump({'real': self.real, 'arms': self.arms, 'attempts': self.attempts, 'maps': self.maps, 'done': self.done},
                  open(tmp, 'w'))
        os.replace(tmp, self.path)

    def add_attempt(self, mk, best, planes):
        lst = self.attempts.setdefault(mk, [])
        lst.append([best, planes]); lst.sort(key=lambda x: x[0]); del lst[6:]

    def add_realization(self, tris, planes, type_id, origin):
        """Add if new (different from the realizations of the same map); create its arms. Returns the id or None."""
        from beam_ladder import extendable
        from ladder import pack, pair_energy
        mk = mapkey(tris); ch = chirotope(planes)
        for r in self.real:
            if r['map'] == mk and om_distance(r['chi'], ch) < DIFFERENT:
                return None
        g = genus_of(tris)
        rid = len(self.real)
        self.real.append({'id': rid, 'map': mk, 'genus': g, 'type_id': type_id, 'planes': [list(map(float, h)) for h in planes],
                          'origin': origin, 'chi': [int(x) for x in ch]})
        self.maps[mk] = [list(map(int, t)) for t in tris]
        if g < FULL_GENUS:
            H2 = np.array(planes, float); nr = np.linalg.norm(H2[:, :3], axis=1)
            H2[:, :3] /= nr[:, None]; H2[:, 3] /= nr
            from gauss_gate import arm_report
            cached = GATE_CACHE.get(gate_key(planes, tris))       # job `gate` already did reach + T1
            if cached is not None:
                from handle_add import candidates
                from gauss_degree import coherent_triangles, links_from
                keep = {json.dumps(a['tube']): a for a in cached['arms']}
                arms = [(t1, t2, R, links_from(coherent_triangles(R), N)) for t1, t2, R, _ in
                        candidates([tuple(t) for t in tris], N) if json.dumps([list(t1), list(t2)]) in keep]
            else:
                arms = extendable([tuple(t) for t in tris], N)
            for t1, t2, R, L in arms:
                LK, M, _ = pack(L)
                try:
                    e = float(pair_energy(H2, LK, M)[0])
                except Exception:
                    e = 99.0
                tk = mapkey(R); self.maps[tk] = [list(map(int, t)) for t in R]
                try:
                    t1r = keep[json.dumps([list(t1), list(t2)])] if cached is not None else arm_report(planes, tris, R, (t1, t2))
                    gauss = {k: t1r.get(k) for k in ('own_degree', 'target_degree', 'k_tau', 'hemisphere_margin',
                                                      'n_admissible', 'min_reversed', 'n_tube_only')}
                except Exception as ex:              # noqa: BLE001
                    gauss = {'error': repr(ex)[:200]}
                self.arms['%d:%s' % (rid, tk)] = {'real': rid, 'target': tk, 'genus': g + 1, 'tube': [list(t1), list(t2)],
                                                  'start': e, 'tries': 0, 'best': None, 'running': 0, 'gauss': gauss}
        return rid


def gauss_pass(a):
    """T1 verdict of an arm: True / False, None if unknown (arm created before the gate existed)."""
    g = a.get('gauss') or {}
    if g.get('n_admissible') is None:
        return None
    return g['n_admissible'] > 0


GATE_CACHE = {}          # gate_key -> results/gate record (set by run(gate_records=...))


def gate_key(planes, tris):
    """= run_overnight._rkey"""
    import hashlib
    h = hashlib.sha256(json.dumps([[round(float(v), 9) for v in p] for p in planes]).encode()
                       + json.dumps(sorted(sorted(int(x) for x in t) for t in tris)).encode())
    return h.hexdigest()[:10]


def pick(arc, rng, minutes, gate=False):
    """Next task: a diversity task (25 %; always when the gate leaves no arm) or the arm with the
    highest priority (with gate: only arms passing T1)."""
    reals = arc.real
    arms = {k: a for k, a in arc.arms.items() if not gate or gauss_pass(a) is not False}
    if reals and (rng.random() < 0.25 or not arms):
        top = max(r['genus'] for r in reals)
        pool = [r for r in reals if r['genus'] >= top - 1]
        r = pool[int(rng.integers(len(pool)))]
        att = arc.attempts.get(r['map'], [])
        if att and rng.random() < 0.7:
            seed = att[int(rng.integers(len(att)))][1]
        else:
            seed = (norm_planes(r['planes']) + 0.15 * rng.standard_normal((N, 4))).tolist()
        return {'kind': 'diversity', 'map': r['map'], 'tris': arc.maps[r['map']], 'seed_planes': seed,
                'type_id': r['type_id'], 'minutes': minutes}
    if not arms:
        return None
    total = sum(a['tries'] for a in arms.values()) + 1
    def prio(a):
        est = a['best'] if a['best'] is not None else a['start'] / 3.0
        return 2 * a['genus'] - est + 2.0 * np.sqrt(np.log(total + 1) / (a['tries'] + a['running'] + 1))
    key = max(arms, key=lambda k: prio(arms[k]))
    a = arc.arms[key]; r = arc.real[a['real']]
    att = arc.attempts.get(a['target'], [])
    seed = att[0][1] if (att and rng.random() < 0.5) else r['planes']
    return {'kind': 'arm', 'arm': key, 'map': a['target'], 'tris': arc.maps[a['target']], 'seed_planes': seed,
            'type_id': r['type_id'], 'minutes': minutes}


def load_seeds(arc, files, log):
    """Exact realizations (genus >= 2) and failed attempts from glad results (.jsonl) and JSON files
    with 'planes' + 'triangles'; every realization is re-checked exactly before it enters."""
    from gauss_degree import coherent_triangles, links_from
    from ladder_exact import verify
    cand = []
    for f in files:
        if f.endswith('.jsonl'):
            for line in open(f):
                if not line.strip():
                    continue
                r = json.loads(line)
                for lv in r.get('levels', []):
                    cand.append((lv['triangles'], lv['planes'], r.get('type_id', -1), '%s level %d' % (r['task'], lv['genus']), lv.get('best', 99)))
                br = (r.get('branch') or {}).get('realized')
                if br:
                    cand.append((br['triangles'], br['planes'], r.get('type_id', -1), '%s branch' % r['task'], 0.0))
        else:
            d = json.load(open(f))
            if 'planes' in d and 'triangles' in d:
                cand.append((d['triangles'], d['planes'], d.get('type_id', -1), os.path.basename(f), d.get('best', 0.0)))
    n_real = n_att = 0
    for tris, planes, tid, origin, best in cand:
        if genus_of(tris) < 2:
            continue
        tris = [tuple(t) for t in tris]
        if best < 0.5:
            L = links_from(coherent_triangles(tris), N)
            if verify(planes, L, require_all_pairs=(genus_of(tris) == FULL_GENUS))['EMBEDDED']:
                if arc.add_realization(tris, planes, tid, origin) is not None:
                    n_real += 1
                continue
        if best < 4.5:                                   # degeneracy-adjusted, as for the task results
            from ladder import pack, degeneracy
            H = np.array(planes, float); nr = np.linalg.norm(H[:, :3], axis=1); H[:, :3] /= nr[:, None]; H[:, 3] /= nr
            e_rel, m_rel = degeneracy(H, *pack(links_from(coherent_triangles(tris), N))[:2])
            score = float(best) + (1.0 if e_rel < 1e-4 else 0.0) + (1.0 if m_rel < 1e-5 else 0.0)
            arc.add_attempt(mapkey(tris), score, planes); n_att += 1
    log('archive seeds: %d realizations (genus >= 2), %d attempts; %d arms' % (n_real, n_att, len(arc.arms)))


def run(out_dir, hours, workers, minutes, files, log=print, committer=None, seed=0, gate=False, gate_records=()):
    deadline = time.monotonic() + 3600 * hours          # the budget includes loading the seeds
    for r in gate_records:
        GATE_CACHE[r['task'][2:]] = r
    os.makedirs(out_dir, exist_ok=True)
    arc = Archive(os.path.join(out_dir, 'archive.json'))
    if not arc.real:
        load_seeds(arc, files, log); arc.save()
    if not arc.arms and not arc.real:
        log('archive: nothing to climb from (no realized genus >= 2)'); return
    np_ = sum(1 for a in arc.arms.values() if gauss_pass(a)); nf = sum(1 for a in arc.arms.values() if gauss_pass(a) is False)
    log('archive: %d realizations, %d arms; Gauss gate T1: %d pass, %d fail, %d unknown%s' % (
        len(arc.real), len(arc.arms), np_, nf, len(arc.arms) - np_ - nf, ' (gate ON)' if gate else ''))
    rng = np.random.default_rng(seed + arc.done)
    res_path = os.path.join(out_dir, 'results.jsonl')
    pool = mp.get_context('spawn').Pool(workers, maxtasksperchild=20)
    running = {}; issued = 0
    try:
        while True:
            while len(running) < workers and time.monotonic() < deadline:
                p = pick(arc, rng, minutes, gate)
                if p is None:
                    break
                issued += 1; tid = 'a%d_%d' % (arc.done, issued)
                p['seed'] = int(rng.integers(1 << 30))
                if p.get('arm'):
                    arc.arms[p['arm']]['running'] += 1
                running[tid] = (p, pool.apply_async(worker, ((tid, p),)))
            if not running:
                break
            time.sleep(5)
            for tid in [t for t, (p, h) in running.items() if h.ready()]:
                p, h = running.pop(tid)
                try:
                    rec = h.get()
                except Exception as e:                       # noqa: BLE001
                    log('task %s failed: %r' % (tid, e)); continue
                arc.done += 1
                # degeneracy-adjusted value: near-solutions hugging the floor (tiny edge / margin) are degenerate
                # limits, not progress; they must not attract the bandit or seed later tasks
                score = rec['best'] + (1.0 if rec.get('edge', 1.0) < 1e-4 else 0.0) + (1.0 if rec.get('margin', 1.0) < 1e-5 else 0.0)
                rec['score'] = score
                if p.get('arm'):
                    a = arc.arms[p['arm']]; a['running'] = max(0, a['running'] - 1); a['tries'] += 1
                    a['best'] = score if a['best'] is None else min(a['best'], score)
                if 'planes' in rec and not rec.get('exact'):
                    arc.add_attempt(rec['map'], score, rec['planes'])
                new = None
                if rec.get('exact'):
                    new = arc.add_realization([tuple(t) for t in arc.maps[rec['map']]], rec['planes'], p['type_id'],
                                              '%s %s' % (p['kind'], tid))
                rec['new_realization'] = new
                rec['type_id'] = p['type_id']
                with open(res_path, 'a') as f:
                    f.write(json.dumps({k: v for k, v in rec.items() if k != 'planes'} | ({'planes': rec['planes']} if rec.get('exact') else {})) + '\n')
                arc.save()
                top = max(r['genus'] for r in arc.real) if arc.real else -1
                log('arch %s %s type %d genus %d: best %.2f (edge %.0e, margin %.0e, degree %s/%s, turning!=1 %s)%s (archive: %d realizations, top genus %d)' % (
                    tid, p['kind'], p['type_id'], rec['genus'], rec['best'], rec.get('edge', 0), rec.get('margin', 0),
                    rec.get('degree'), rec.get('target_degree'), rec.get('bad_turning'),
                    ' NEW REALIZATION #%d' % new if new is not None else (' (exact, same as known)' if rec.get('exact') else ''),
                    len(arc.real), top))
                if new is not None and rec['genus'] == FULL_GENUS:
                    log('!!! CANDIDATE: genus %d realized exactly (all pairs adjacent)' % FULL_GENUS)
                    if committer:
                        committer.maybe('overnight arch: CANDIDATE', force=True)
                elif committer:
                    committer.maybe('overnight arch: progress', force=new is not None)
            if time.monotonic() > deadline and not running:
                break
            if time.monotonic() > deadline:
                log('time budget reached; stopping (resume by re-running the same command)')
                break
    finally:
        pool.terminate(); pool.join(); arc.save()
        if committer:
            committer.maybe('overnight arch: stop', force=True)


if __name__ == '__main__':
    gate = '--gauss-gate' in sys.argv
    argv = [a for a in sys.argv if a != '--gauss-gate']
    out_dir, hours, workers, minutes = argv[1], float(argv[2]), int(argv[3]), float(argv[4])
    run(out_dir, hours, workers, minutes, argv[5:],
        log=lambda *a: print(time.strftime('%H:%M:%S'), *a, flush=True), gate=gate)
