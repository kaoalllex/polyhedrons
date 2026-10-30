"""Branching genus ladder: instead of one fixed chain M0 -> M6, grow from a REALIZED level by every
possible next handle. From an exactly embedded polyhedron (planes + dual triangles) list all tubes
whose six new edges are new (handle_add.candidates), keep those after which all n(n-1)/2 pairs are
still reachable (handle_add.reach), order them by the pair energy of the new map at the current
planes, and search each (annealing + CMA-ES, seeded from the current planes; float zeros re-checked
exactly). Every realized next level is saved and climbed further (depth first).
Gauss gate (review 2026-10-30, code/gauss_gate.py): every handle gets T1 at the current planes (degree of
the next map in the realized polyhedron's orientation, k_tau, admissible gauges for 1 - g'); arms that pass
are searched first, and with --gauss-gate (climb_seq: gate=True) arms that fail are skipped. Every attempt
records the class data of its best configuration (own degree, faces with turning != +1).
Usage: python3 -I beam_ladder.py LEVEL_JSON MINUTES_PER_CANDIDATE SEED OUT_DIR [WORKERS] [--floor] [--gauss-gate]"""
import json, os, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from handle_add import candidates, reach
from ladder import pack, pair_energy
from genus_ladder import search
from ladder_exact import verify

FLOOR = '--floor' in sys.argv          # degeneracy floor in the search energy (genus_ladder.use_floor)
GATE = '--gauss-gate' in sys.argv      # skip handles that fail the Gauss gate T1


def gauss_t1(planes, tris, R, t1, t2):
    """T1 summary of one handle at the current planes (None on error)."""
    from gauss_gate import arm_report
    try:
        r = arm_report(planes, tris, R, (t1, t2))
        return {k: r.get(k) for k in ('own_degree', 'target_degree', 'k_tau', 'hemisphere_margin', 'n_admissible',
                                      'min_reversed', 'n_tube_only')}
    except Exception:                       # noqa: BLE001
        return None


def class_data(H, R):
    """Own degree and faces with turning != +1 of a (failed) attempt for its own map."""
    from gauss_gate import config_report
    try:
        c = config_report(np.asarray(H).tolist(), R, gauges=False)
        return {'degree': c.get('own_degree'), 'target_degree': c['target_degree'], 'bad_turning': c.get('bad_turning_faces')}
    except Exception:                       # noqa: BLE001
        return {}


def genus_of(tris, n):
    E = len({frozenset(e) for t in tris for e in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2]))})
    return (2 - (n - E + len(tris))) // 2


def extendable(tris, n):
    full = n * (n - 1) // 2
    out = []
    for t1, t2, R, L in candidates(tris, n):
        r, _ = reach(R, n, node_limit=3000)
        if r == full:
            out.append((t1, t2, R, L))
    return out


def work(args):
    planes, R, L, minutes, seed = args
    if FLOOR:
        import genus_ladder
        genus_ladder.use_floor()
    rng = np.random.default_rng(seed)
    (b, H), runs = search(L, len(planes), minutes, rng, planes)
    rec = {'best': float(b), 'planes': H.tolist(), 'triangles': [list(t) for t in R]}
    rec.update(class_data(H, R))
    if b < 0.5:
        rec['exact'] = bool(verify(H.tolist(), L, require_all_pairs=False)['EMBEDDED'])
    return rec


def climb(level, minutes, seed, out_dir, workers, path=()):
    H = np.array(level['planes'], float); n = len(H); tris = [tuple(t) for t in level['triangles']]
    g = genus_of(tris, n)
    C = extendable(tris, n)
    order = []; t1s = {}
    for i, (t1, t2, R, L) in enumerate(C):
        LK, M, _ = pack(L); e, o = pair_energy(H, LK, M)
        t1s[i] = gauss_t1(level['planes'], tris, R, t1, t2)
        ok = bool(t1s[i] and t1s[i]['n_admissible'])
        if GATE and not ok:
            continue
        order.append((not ok, e, o, i))
    order.sort(); order = [(e, o, i) for _, e, o, i in order]
    print('genus %d %s: %d extendable handles, start energies %s; Gauss T1 (degree, k_tau, admissible) %s%s' % (
        g, path, len(C), [(int(e), i) for e, o, i in order],
        {i: (r['own_degree'], r['k_tau'], r['n_admissible']) if r else None for i, r in t1s.items()},
        ' (gate ON: %d kept)' % len(order) if GATE else ''), flush=True)
    jobs = [(level['planes'], C[i][2], C[i][3], minutes, seed * 1000 + i) for e, o, i in order]
    with Pool(workers) as P:
        recs = P.map(work, jobs)
    log = []
    for (e, o, i), rec in zip(order, recs):
        rec['tube'] = [list(C[i][0]), list(C[i][1])]; rec['genus'] = g + 1; rec['start_energy'] = float(e)
        rec['gauss_t1'] = t1s[i]
        log.append(dict(rec, exact=rec.get('exact', False)))            # with planes: failed attempts seed later runs
        print('  genus %d via tube %s-%s: best %.3f (degree %s/%s, turning!=1 %s) %s' % (
            g + 1, C[i][0], C[i][1], rec['best'], rec.get('degree'), rec.get('target_degree'), rec.get('bad_turning'),
            'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
    json.dump(log, open(os.path.join(out_dir, 'genus%d_%s.json' % (g + 1, '_'.join(map(str, path)) or 'root')), 'w'))
    for (e, o, i), rec in zip(order, recs):
        if rec.get('exact'):
            name = os.path.join(out_dir, 'realized_genus%d_%s.json' % (g + 1, '_'.join(map(str, path + (i,)))))
            json.dump(rec, open(name, 'w'))
            if g + 1 == (n - 3) * (n - 4) // 12:
                print('!!! FULL GENUS REALIZED:', name, flush=True)
                return True
            if climb(rec, minutes, seed, out_dir, workers, path + (i,)):
                return True
    return False


def climb_seq(level, minutes, rng, deadline, path=(), gate=False):
    """Sequential depth-first branching climb (for the overnight job): returns (highest exactly
    realized genus, its record, the list of attempts). Handles passing the Gauss gate T1 first;
    gate=True skips the others."""
    H = np.array(level['planes'], float); n = len(H); tris = [tuple(t) for t in level['triangles']]
    g = genus_of(tris, n); top = (g, level); tried = []
    C = extendable(tris, n); order = []; t1s = {}
    for i, (t1, t2, R, L) in enumerate(C):
        LK, M, _ = pack(L); e, o = pair_energy(H, LK, M)
        t1s[i] = gauss_t1(level['planes'], tris, R, t1, t2)
        ok = bool(t1s[i] and t1s[i]['n_admissible'])
        if gate and not ok:
            tried.append({'genus': g + 1, 'tube': [list(t1), list(t2)], 'path': list(path + (i,)), 'skipped': 'gauss_gate',
                          'gauss_t1': t1s[i]})
            continue
        order.append((not ok, e, i))
    order.sort(); order = [(e, i) for _, e, i in order]
    for e, i in order:
        if time.monotonic() > deadline:
            break
        t1, t2, R, L = C[i]
        (b, Hb), runs = search(L, n, minutes, rng, level['planes'])
        rec = {'genus': g + 1, 'tube': [list(t1), list(t2)], 'path': list(path + (i,)), 'best': float(b),
               'start_energy': float(e), 'planes': Hb.tolist(), 'triangles': [list(t) for t in R], 'gauss_t1': t1s[i]}
        rec.update(class_data(Hb, R))
        if b < 0.5:
            rec['exact'] = bool(verify(Hb.tolist(), L, require_all_pairs=(g + 1 == (n - 3) * (n - 4) // 12))['EMBEDDED'])
        tried.append({k: rec.get(k) for k in ('genus', 'tube', 'path', 'best', 'start_energy', 'planes', 'triangles',
                                               'gauss_t1', 'degree', 'target_degree', 'bad_turning')} | {'exact': rec.get('exact', False)})
        if rec.get('exact'):
            sub_top, sub_rec, sub_tried = climb_seq(rec, minutes, rng, deadline, path + (i,), gate)
            tried += sub_tried
            if sub_top > top[0]:
                top = (sub_top, sub_rec)
            if top[0] == (n - 3) * (n - 4) // 12:
                break
    return top[0], top[1], tried


if __name__ == '__main__':
    lv = json.load(open(sys.argv[1])); minutes = float(sys.argv[2]); seed = int(sys.argv[3]); out_dir = sys.argv[4]
    workers = int(sys.argv[5]) if len(sys.argv) > 5 and not sys.argv[5].startswith('--') else 1
    os.makedirs(out_dir, exist_ok=True)
    climb(lv, minutes, seed, out_dir, workers)
