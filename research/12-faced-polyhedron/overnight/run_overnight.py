#!/usr/bin/env python3
"""Autonomous, resumable long runs for the 12-face polyhedron research.

Jobs (run one job per invocation; re-running the same command resumes where it stopped):

  normals  E1. For a near-miss seed, keep its 12 face NORMALS (rounded to integers) and decide
           exactly, with z3 (linear real arithmetic), whether ANY choice of the 12 plane offsets
           gives an embedded polyhedron. SAT answers are re-checked by an independent exact
           rational checker. Then the same for randomly perturbed normals of the best seeds.
  sym      Certified UNSAT for every symmetric case (every conjugacy class of half-turn C2 and
           3-fold C3 subgroups of Aut of all 59 maps). With CaDiCaL + drat-trim on PATH (or given
           by --cadical / --drat-trim) every UNSAT gets a checked DRAT proof; otherwise PySAT
           is used and results are marked unverified.
  cube     Cube-and-conquer on the full ASYMMETRIC OM-SAT instance of the chosen maps (Lutz
           numbering). Timed-out cubes are split further. Reports the refuted fraction.
  ils      Iterated local search from the seeds: exact single-plane relocation + random kicks.
  gate     Night 5: Gauss gate T1 for every realized polyhedron x next handle; test 2.2 on night-3 chains.
  n5       Night 5: normals-first ladder (nfirst), k-targeted drift (kdrift), genus-6 normals first (g6).

Progress is appended after every finished task to results/<job>/results.jsonl (fsync'ed), so a
power cut loses at most the tasks that were running. With --git the results directory is
committed every --commit-minutes (and immediately when a candidate is found); --push also pushes.

Examples:
  python3 run_overnight.py normals --hours 8 --workers 4 --git
  python3 run_overnight.py sym --hours 3 --workers 4 --git
  python3 run_overnight.py cube --maps 1 --hours 8 --workers 4 --git
  python3 run_overnight.py ils --hours 4 --workers 4 --git
  python3 run_overnight.py status
"""
import argparse
import hashlib
import itertools
import json
import multiprocessing as mp
import os
import random
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.normpath(os.path.join(HERE, '..', 'code'))
RES = os.environ.get('POLY_RESULTS_DIR') or os.path.join(HERE, 'results')   # env: seen by spawned workers too
WORK = os.path.join(HERE, 'work')            # big scratch files (CNFs, proofs); not committed
SEEDS = os.path.join(HERE, 'data', 'seeds.json')
sys.path.insert(0, CODE)


# ----------------------------------------------------------------------------- bookkeeping

def jobdir(job):
    d = os.path.join(RES, job)
    os.makedirs(d, exist_ok=True)
    return d


def load_results(job):
    p = os.path.join(jobdir(job), 'results.jsonl')
    out = []
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:      # torn last line after a crash
                    pass
    return out


def append_result(job, rec):
    p = os.path.join(jobdir(job), 'results.jsonl')
    with open(p, 'a') as f:
        f.write(json.dumps(rec, separators=(',', ':')) + '\n')
        f.flush()
        os.fsync(f.fileno())


def write_json_atomic(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def save_candidate(job, rec):
    d = os.path.join(jobdir(job), 'CANDIDATES')
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, '%s_%d.json' % (str(rec.get('task', 'x')).replace('/', '_'), int(time.time())))
    write_json_atomic(path, rec)
    return path


class Committer:
    def __init__(self, args):
        self.on = args.git
        self.push = args.push
        self.every = args.commit_minutes * 60
        self.last = time.monotonic()
        self.root = None
        if self.on:
            try:
                self.root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=HERE,
                                                    text=True).strip()
            except Exception as e:                  # noqa: BLE001
                print('git not available, --git ignored:', e)
                self.on = False

    def maybe(self, msg, force=False):
        if not self.on or (not force and time.monotonic() - self.last < self.every):
            return
        self.last = time.monotonic()
        try:
            subprocess.run(['git', 'add', '-A', RES], cwd=self.root, check=True)
            r = subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=self.root)
            if r.returncode == 0 and self.push:
                subprocess.run(['git', 'push', '-q'], cwd=self.root)
        except Exception as e:                      # noqa: BLE001
            print('git commit failed (continuing):', e)


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


def run_pool(job, tasks, worker, args, committer, init=None, initargs=()):
    """Run tasks (list of (task_id, payload)) in a pool; record each result; respect --hours."""
    deadline = time.monotonic() + args.hours * 3600
    done = {r['task'] for r in load_results(job)}
    todo = [(t, p) for t, p in tasks if t not in done and (not args.only or args.only in t)]
    log('%s: %d tasks total, %d already done, %d to do' % (job, len(tasks), len(done), len(todo)))
    if not todo:
        return
    ctx = mp.get_context('spawn')
    pool = ctx.Pool(args.workers, initializer=init, initargs=initargs, maxtasksperchild=50)
    try:
        it = pool.imap_unordered(worker, todo, chunksize=1)
        while True:
            try:
                rec = it.next(timeout=30)
            except mp.TimeoutError:
                if time.monotonic() > deadline:
                    log('time budget reached; stopping (resume by re-running the same command)')
                    break
                continue
            except StopIteration:
                break
            rec['finished_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
            append_result(job, rec)
            flag = rec.get('candidate')
            log(job, rec['task'], rec.get('status'), rec.get('summary', ''))
            if flag:
                p = save_candidate(job, rec)
                log('!!! CANDIDATE saved to', p)
                committer.maybe('overnight %s: CANDIDATE %s' % (job, rec['task']), force=True)
            elif rec.get('important'):
                committer.maybe('overnight %s: %s %s' % (job, rec.get('status'), rec['task']), force=True)
            else:
                committer.maybe('overnight %s: progress' % job)
            if time.monotonic() > deadline:
                log('time budget reached; stopping (resume by re-running the same command)')
                break
    finally:
        pool.terminate()
        pool.join()
        committer.maybe('overnight %s: stop' % job, force=True)


# ----------------------------------------------------------------------------- job: normals

def _gp_ok(N):
    for a, b, c in itertools.combinations(range(len(N)), 3):
        from fixed_normals import det3
        if det3(N[a], N[b], N[c]) == 0:
            return False
    return True


def normals_worker(item):
    task, p = item
    import numpy as np
    from fixed_normals import solve, integer_normals, exact_check
    t0 = time.monotonic()
    H = np.array(p['planes'], dtype=float)
    rng = np.random.default_rng(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16))
    Nf = H[:, :3] / np.linalg.norm(H[:, :3], axis=1)[:, None]
    if p['sigma'] > 0:
        Nf = Nf + p['sigma'] * rng.standard_normal(Nf.shape)
    N = integer_normals(Nf)
    k = 0
    while not _gp_ok(N) and k < 20:               # break accidental degeneracy by tiny integer noise
        N = [[x + int(rng.integers(-1, 2)) for x in v] for v in N]
        k += 1
    from gauss_degree import coherent_triangles, admissible_gauges
    if not admissible_gauges(N, coherent_triangles(p['triangles']), -5):
        return {'task': task, 'seed_id': p['seed_id'], 'source': p['source'], 'seed_count': p['ours'],
                'sigma': p['sigma'], 'status': 'UNSAT-GAUSS', 'seconds': round(time.monotonic() - t0, 1),
                'summary': 'no gauge with Gauss degree -5 and convex covering (exact)'}
    try:
        status, planes = solve(N, p['triangles'], timeout_s=p['timeout'])
    except Exception as e:                          # noqa: BLE001
        return {'task': task, 'status': 'ERROR', 'error': repr(e)[:300], 'seconds': round(time.monotonic() - t0, 1)}
    rec = {'task': task, 'seed_id': p['seed_id'], 'source': p['source'], 'seed_count': p['ours'],
           'sigma': p['sigma'], 'status': status, 'seconds': round(time.monotonic() - t0, 1), 'normals': N}
    if status == 'SAT':
        ok, nv, nb = exact_check(planes, p['triangles'])
        rec.update({'planes': [[int(x) for x in h] for h in planes], 'triangles': p['triangles'],
                    'exact_embedded': ok, 'exact_violated_triples': nv, 'exact_bad_pairs': nb})
        rec['candidate'] = bool(ok)
        rec['summary'] = 'SAT exact=%s' % ok
    else:
        rec['summary'] = '%.0fs' % rec['seconds']
    return rec


def job_normals(args, committer):
    seeds = json.load(open(SEEDS))
    tasks = []
    for s in seeds:
        if s['ours'] <= args.max_seed_count:
            tasks.append(('s%d' % s['seed_id'], dict(s, sigma=0.0, timeout=args.timeout)))
    best = [s for s in seeds if s['ours'] <= args.perturb_max_count]
    for sigma in (0.003, 0.01, 0.03, 0.1):
        for rep in range(args.perturb_reps):
            for s in best:
                tasks.append(('p%d_%g_%d' % (s['seed_id'], sigma, rep), dict(s, sigma=sigma, timeout=args.timeout)))
    run_pool('normals', tasks, normals_worker, args, committer)


# ----------------------------------------------------------------------------- job: gnormals

def gnormals_worker(item):
    task, p = item
    import numpy as np
    from gauss_degree import coherent_triangles, admissible_gauges
    from gauss_search import find_admissible
    from fixed_normals import integer_normals, exact_check
    from fixed_normals_gauge import solve_gauge
    t0 = time.monotonic()
    rng = np.random.default_rng(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16))
    ot = coherent_triangles(p['triangles'])
    G, it = find_admissible(ot, rng, minutes=p['anneal_minutes'])
    rec = {'task': task, 'type_id': p['type_id'], 'anneal_iterations': it}
    if G is None:
        rec.update(status='NO_ADMISSIBLE_NORMALS', seconds=round(time.monotonic() - t0, 1), summary='anneal failed')
        return rec
    N = integer_normals(G)
    if tuple([1] * 12) not in admissible_gauges(N, ot, -5, n_cover=500):
        rec.update(status='ROUNDING_FAILED', seconds=round(time.monotonic() - t0, 1), summary='exact recheck failed')
        return rec
    ta = time.monotonic()
    try:
        status, planes = solve_gauge(N, p['triangles'], timeout_s=p['timeout'])
    except Exception as e:                          # noqa: BLE001
        rec.update(status='ERROR', error=repr(e)[:300], seconds=round(time.monotonic() - t0, 1))
        return rec
    rec.update(status=status, normals=N, smt_seconds=round(time.monotonic() - ta, 1), seconds=round(time.monotonic() - t0, 1))
    if status == 'SAT':
        ok, nv, nb = exact_check(planes, p['triangles'])
        rec.update(planes=[[int(x) for x in h] for h in planes], triangles=p['triangles'], exact_embedded=ok,
                   exact_violated_triples=nv, exact_bad_pairs=nb, candidate=bool(ok))
        rec['summary'] = 'SAT exact=%s' % ok
    else:
        rec['summary'] = 'type %d %s smt %.0fs' % (p['type_id'], status, rec['smt_seconds'])
    return rec


def job_gnormals(args, committer):
    types = json.load(open(os.path.join(HERE, '..', 'data', 'k12_triangulations.json')))
    tasks = [('g%d_%d' % (t['id'], r), dict(type_id=t['id'], triangles=t['triangles'], timeout=args.timeout,
                                             anneal_minutes=args.anneal_minutes))
             for r in range(args.reps) for t in types]
    run_pool('gnormals', tasks, gnormals_worker, args, committer)


# ----------------------------------------------------------------------------- job: pdefect

def pdefect_worker(item):
    task, p = item
    import numpy as np
    from gauss_degree import coherent_triangles
    from gauss_search import find_admissible, cover_counts, tri_index
    from period_defect import period_defect
    rng = np.random.default_rng(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16))
    tri = p['triangles']; ot = coherent_triangles(tri); T = tri_index(ot)
    U = rng.standard_normal((1500, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
    def adm(G):
        pos, neg = cover_counts(G, T, U)
        return bool(np.all(pos - neg == -5) and np.all(pos > 0))
    t0 = time.monotonic()
    G, _ = find_admissible(ot, rng, minutes=2)
    if G is None:
        return {'task': task, 'type_id': p['type_id'], 'status': 'NO_ADMISSIBLE_NORMALS', 'seconds': round(time.monotonic() - t0, 1)}
    cur = period_defect(G, tri, time_limit=15)[0]
    start = cur; best = (cur, G.copy()); Tmp = 2.0; it = 0
    while cur is not None and time.monotonic() - t0 < 60 * p['minutes'] and best[0] > 1e-6:
        it += 1
        G2 = G.copy(); k = int(rng.integers(12))
        v = G2[k] + float(rng.choice([0.02, 0.05, 0.15])) * rng.standard_normal(3); G2[k] = v / np.linalg.norm(v)
        if not adm(G2):
            continue
        d2 = period_defect(G2, tri, time_limit=15)[0]
        if d2 is None:
            continue
        if d2 <= cur or rng.random() < np.exp((cur - d2) / Tmp):
            G, cur = G2, d2
            if cur < best[0]:
                best = (cur, G.copy())
        Tmp = max(0.05, Tmp * 0.97)
    rec = {'task': task, 'type_id': p['type_id'], 'start_defect': start, 'best_defect': best[0], 'iterations': it,
           'normals': best[1].tolist(), 'seconds': round(time.monotonic() - t0, 1)}
    rec['status'] = 'ZERO_DEFECT' if best[0] is not None and best[0] <= 1e-6 else 'POSITIVE'
    if rec['status'] == 'ZERO_DEFECT':
        # zero closure defect is only necessary (night 2: pd10_0 had 11 non-simple faces); a candidate
        # must also close up with SIMPLE faces (exact closure + simplicity MILP, phi = 0 = R^3)
        from period_defect import torus_simple, surface_edges
        edges, _, _ = surface_edges(best[1], tri)
        st, _ = torus_simple(best[1], tri, {k: (0, 0, 0) for k in edges}, time_limit=300, general=False)
        rec['simple_milp_status'] = int(st)        # 0 feasible, 1 time limit, 2 infeasible
        if st == 2:
            rec['status'] = 'ZERO_DEFECT_NOT_SIMPLE'
        elif st == 1:
            rec['status'] = 'ZERO_DEFECT_SIMPLE_UNKNOWN'
    rec['candidate'] = rec['status'] in ('ZERO_DEFECT', 'ZERO_DEFECT_SIMPLE_UNKNOWN')
    rec['summary'] = 'type %d defect %.3f -> %.3f (%d its)' % (p['type_id'], start or -1, best[0] or -1, it)
    return rec


def job_pdefect(args, committer):
    types = json.load(open(os.path.join(HERE, '..', 'data', 'k12_triangulations.json')))
    tasks = [('pd%d_%d' % (t['id'], r), dict(type_id=t['id'], triangles=t['triangles'], minutes=args.minutes_per_seed))
             for r in range(args.reps) for t in types]
    run_pool('pdefect', tasks, pdefect_worker, args, committer)


# ----------------------------------------------------------------------------- job: ladder
# Own path (cross-field-ideas.md Y1): closed polyhedra with n mutually adjacent faces, n < 12, maps
# generated from scratch (no external seeds), genetic algorithm on the honest pair energy, every float
# zero re-checked in exact rational arithmetic (code/ladder_exact.py). n = 7 (Szilassi) is found in
# seconds; n = 8 (genus 2, two doubled adjacencies) plateaued at 1-2 violations in the cloud runs.

def ladder_worker(item):
    task, p = item
    import numpy as np
    from ladder import random_map
    from ladder_ga import run as ga_run
    from ladder_exact import verify
    rng = np.random.default_rng(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16))
    t0 = time.monotonic()
    links, tries = None, 0
    while links is None and tries < 20:
        links = random_map(p['n'], p['genus'], rng); tries += 1
    if links is None:
        return {'task': task, 'n': p['n'], 'status': 'NO_MAP', 'seconds': round(time.monotonic() - t0, 1)}
    (b, H), gen, _ = ga_run(links, p['minutes'], rng)
    rec = {'task': task, 'n': p['n'], 'genus': p['genus'], 'best': float(b), 'generations': gen,
           'links': {str(k): v for k, v in links.items()}, 'planes': H.tolist(), 'seconds': round(time.monotonic() - t0, 1)}
    rec['status'] = 'POSITIVE'
    if b < 0.5:
        ex = verify(H.tolist(), links)
        rec['exact'] = {k: (v if not isinstance(v, list) else len(v)) for k, v in ex.items()}
        rec['status'] = 'EMBEDDED' if ex['EMBEDDED'] else 'ZERO_FLOAT_NOT_EXACT'
    rec['candidate'] = rec['status'] == 'EMBEDDED'
    rec['summary'] = 'n=%d genus %d best %.3f (%d generations) %s' % (p['n'], p['genus'], b, gen, rec['status'])
    return rec


def job_ladder(args, committer):
    ns = [int(x) for x in args.ladder_n.split(',')]
    tasks = [('lad%d_%d' % (n, r), dict(n=n, genus=-(-(n - 3) * (n - 4) // 12), minutes=args.minutes_per_seed))
             for r in range(args.reps) for n in ns]
    run_pool('ladder', tasks, ladder_worker, args, committer)


# ----------------------------------------------------------------------------- job: sdefect
# "Simple faces first" for the 12-face problem: anneal admissible normals (Gauss degree -5) on the
# simple defect = minimum number of faces that must be NON-simple for an exact closed, locally
# consistent surface with these normals (MILP, period_defect.torus_simple(relax_faces=True)).
# 0 = closed surface with all faces simple -> planes reconstructed and checked exactly.

def sdefect_worker(item):
    task, p = item
    import numpy as np
    from gauss_degree import coherent_triangles
    from gauss_search import find_admissible, cover_counts, tri_index
    from period_defect import torus_simple, surface_edges
    rng = np.random.default_rng(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16))
    tri = p['triangles']; ot = coherent_triangles(tri); T = tri_index(ot)
    U = rng.standard_normal((1500, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
    def adm(G):
        pos, neg = cover_counts(G, T, U)
        return bool(np.all(pos - neg == -5) and np.all(pos > 0))
    from period_defect import period_defect
    def f(G):
        # lexicographic: while the closure (period) defect is positive the simple-defect MILP is infeasible,
        # so the objective is 12 + defect; at zero defect it is the number of faces that must be non-simple
        d = period_defect(G, tri, time_limit=15)[0]
        if d is None:
            return 99.0, None
        if d > 1e-6:
            return 12.0 + d, None
        edges, _, _ = surface_edges(G, tri)
        st, sol = torus_simple(G, tri, {k: (0, 0, 0) for k in edges}, time_limit=p['milp_s'], general=False,
                               relax_faces=True)
        return (float(sol['nonsimple']), sol) if sol is not None else (12.0, None)
    t0 = time.monotonic()
    G, _ = find_admissible(ot, rng, minutes=2)
    if G is None:
        return {'task': task, 'type_id': p['type_id'], 'status': 'NO_ADMISSIBLE_NORMALS', 'seconds': round(time.monotonic() - t0, 1)}
    cur, sol = f(G); start = cur; best = (cur, G.copy(), sol); it = 0; Tmp = 2.0
    while time.monotonic() - t0 < 60 * p['minutes'] and best[0] > 0.5:
        it += 1
        G2 = G.copy(); k = int(rng.integers(12))
        v = G2[k] + float(rng.choice([0.02, 0.05, 0.15])) * rng.standard_normal(3); G2[k] = v / np.linalg.norm(v)
        if not adm(G2):
            continue
        c2, s2 = f(G2)
        if c2 <= cur or rng.random() < np.exp((cur - c2) / Tmp):
            G, cur = G2, c2
            if cur < best[0]:
                best = (cur, G.copy(), s2)
        Tmp = max(0.05, Tmp * 0.97)
    rec = {'task': task, 'type_id': p['type_id'], 'start_nonsimple': start, 'best_nonsimple': best[0], 'iterations': it,
           'normals': best[1].tolist(), 'seconds': round(time.monotonic() - t0, 1)}
    rec['status'] = 'POSITIVE'
    if best[0] < 0.5 and best[2] is not None:
        from planes import Arrangement, check_embedding
        Gn = best[1] / np.linalg.norm(best[1], axis=1)[:, None]; P = best[2]['p']
        off = [float(np.mean([-Gn[X] @ P[i] for i, t in enumerate(ot) if X in t])) for X in range(12)]
        H = np.hstack([Gn, np.array(off)[:, None]]); rec['planes'] = H.tolist()
        try:
            e = check_embedding(Arrangement([[int(round(v * 10 ** 8)) for v in h] for h in H]), tri)
            rec['simple_faces'] = int(sum(e['simple'])); rec['viol_triples'] = len(e['viol_triples']); rec['bad_pairs'] = len(e['bad_pairs'])
            rec['status'] = 'EMBEDDED' if (e['ok_triples'] and e['ok_pairs']) else 'SIMPLE_CLOSED'
        except Exception as ex:                       # noqa: BLE001
            rec['status'] = 'SIMPLE_CLOSED'; rec['check_error'] = repr(ex)[:200]
    rec['candidate'] = rec['status'] in ('SIMPLE_CLOSED', 'EMBEDDED')
    rec['summary'] = 'type %d objective %.3f -> %.3f (12+defect while not closed; else non-simple faces; %d its) %s' % (
        p['type_id'], start, best[0], it, rec['status'])
    return rec


def job_sdefect(args, committer):
    types = json.load(open(os.path.join(HERE, '..', 'data', 'k12_triangulations.json')))
    tasks = [('sd%d_%d' % (t['id'], r), dict(type_id=t['id'], triangles=t['triangles'], minutes=args.minutes_per_seed,
                                             milp_s=args.milp_seconds))
             for r in range(args.reps) for t in types]
    run_pool('sdefect', tasks, sdefect_worker, args, committer)


# ----------------------------------------------------------------------------- job: glad
# Genus ladder (2026-10-30 night): every neighbourly 12-face map = simple 12-faced polyhedron + 6 handles.
# Remove tubes down to the sphere (code/genus_ladder.chain), then climb: realize M0, M1, ... with
# one-plane annealing + CMA-ES on the honest pair energy, each level seeded from the level below;
# every zero re-checked exactly. A realized genus-6 level IS a solution (CANDIDATE). Maps on these
# chains are extendable by construction (the free-type solid search drifts into dead-end maps).

def glad_worker(item):
    task, p = item
    import random
    import numpy as np
    from genus_ladder import chain, search
    from gauss_degree import coherent_triangles, links_from
    from ladder_exact import verify
    seed = int(hashlib.sha256(task.encode()).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed); t0 = time.monotonic()
    ch = chain(p['triangles'], 12, random.Random(seed))
    levels = []; seed_planes = None; top = -1
    for lvl, T in enumerate(ch):
        g = 6 - (len(ch) - 1 - lvl)
        L = links_from(coherent_triangles(T), 12)
        (b, H), runs = search(L, 12, p['minutes'], rng, seed_planes)
        rec = {'genus': g, 'best': float(b), 'planes': H.tolist(), 'triangles': [list(t) for t in T]}
        if b < 0.5:
            ex = verify(H.tolist(), L, require_all_pairs=(g == 6))
            rec['exact'] = bool(ex['EMBEDDED'])
            if ex['EMBEDDED']:
                top = g
        levels.append(rec)
        seed_planes = H.tolist()
        if not rec.get('exact') and lvl >= 1 and b > 6:          # hopeless above this level: stop early
            break
    out = {'task': task, 'type_id': p['type_id'], 'top_exact_genus': top, 'levels': levels}
    if 2 <= top < 6 and p.get('branch_minutes', 0) > 0:
        # branching: from the highest realized level try every extendable next handle (depth first)
        from beam_ladder import climb_seq
        base = next(lv for lv in levels if lv['genus'] == top and lv.get('exact'))
        btop, brec, tried = climb_seq(base, p['minutes'], rng, time.monotonic() + 60 * p['branch_minutes'])
        out['branch'] = {'from_genus': top, 'top': btop, 'tried': tried}
        if btop > top:
            top = btop; out['top_exact_genus'] = top; out['branch']['realized'] = brec
    out['seconds'] = round(time.monotonic() - t0, 1)
    out['status'] = 'SOLUTION' if top == 6 else 'TOP_GENUS_%d' % top
    out['candidate'] = top == 6
    out['summary'] = 'type %d: highest exactly realized genus %d; per level %s' % (
        p['type_id'], top, [(lv['genus'], round(lv['best'], 2)) for lv in levels])
    return out


def job_glad(args, committer):
    types = json.load(open(os.path.join(HERE, '..', 'data', 'k12_triangulations.json')))
    tasks = [('gl%d_%d' % (t['id'], r), dict(type_id=t['id'], triangles=t['triangles'], minutes=args.minutes_per_seed,
                                            branch_minutes=args.branch_minutes))
             for r in range(args.reps) for t in types]
    run_pool('glad', tasks, glad_worker, args, committer)


def job_arch(args, committer):
    """Realization archive + bandit climb (code/archive_climb.py): seeded from the glad results and the
    realized polyhedra in experiments/genus_ladder/; every exactly embedded genus >= 2 polyhedron is a
    root, every extendable next handle an arm; a quarter of the time goes to new realizations."""
    from archive_climb import run
    ex = os.path.normpath(os.path.join(HERE, '..', 'experiments', 'genus_ladder'))
    seeds = [os.path.join(RES, 'glad', 'results.jsonl')]
    if os.path.isdir(ex):
        seeds += [os.path.join(ex, f) for f in sorted(os.listdir(ex)) if f.endswith('.json')]
    seeds = [f for f in seeds if os.path.exists(f)]
    run(jobdir('arch'), args.hours, args.workers, args.minutes_per_seed, seeds, log=log, committer=committer,
        gate=args.gauss_gate)


# ----------------------------------------------------------------------------- night 5: Gauss gate + normals first
# Review 2026-10-30 (reviews/review-2026-10-30.md): the type-0 genus-4 plateau is a Gauss-degree (normal-class)
# obstruction. Job `gate` = test T1 for every realized polyhedron x every extendable next handle (+ test 2.2 on
# the night-3 chains); job `n5` = the gated ladder: `nfirst` (normals first, exact offsets: normals_first.py),
# `kdrift` (drift inside the realization space until the handle degree k_tau = -1 and the next map's class is
# reached, then normals first from there: kdrift.py) and `g6` (genus-6 normals first from random normals).

def _rkey(planes, tris):
    h = hashlib.sha256(json.dumps([[round(float(v), 9) for v in p] for p in planes]).encode()
                       + json.dumps(sorted(sorted(int(x) for x in t) for t in tris)).encode())
    return h.hexdigest()[:10]


def gate_realizations():
    """Every exactly embedded polyhedron of genus >= 2 known on disk: experiments/genus_ladder, night-3 glad
    levels and branches, night-4 arch archive, night-5 realizations. Returns [(key, record)]."""
    from gauss_gate import genus
    out = {}

    def add(planes, tris, tid, origin):
        tris = [list(map(int, t)) for t in tris]
        if genus(tris, len(planes)) < 2:
            return
        k = _rkey(planes, tris)
        out.setdefault(k, {'planes': planes, 'triangles': tris, 'type_id': tid, 'origin': origin})
    ex = os.path.normpath(os.path.join(HERE, '..', 'experiments', 'genus_ladder'))
    if os.path.isdir(ex):
        for f in sorted(os.listdir(ex)):
            if f.endswith('.json'):
                d = json.load(open(os.path.join(ex, f)))
                if 'attempt' not in f and 'planes' in d:
                    add(d['planes'], d['triangles'], d.get('type_id', 0), f)
    for r in load_results('glad'):
        for lv in r.get('levels', []):
            if lv.get('exact'):
                add(lv['planes'], lv['triangles'], r.get('type_id', -1), '%s level %d' % (r['task'], lv['genus']))
        br = (r.get('branch') or {}).get('realized')
        if br:
            add(br['planes'], br['triangles'], r.get('type_id', -1), '%s branch' % r['task'])
    ap = os.path.join(RES, 'arch', 'archive.json')
    if os.path.exists(ap):
        a = json.load(open(ap))
        for r in a.get('real', []):
            add(r['planes'], a['maps'][r['map']], r.get('type_id', -1), 'arch %s' % r.get('origin'))
    rd = os.path.join(RES, 'n5', 'realized')
    if os.path.isdir(rd):
        for f in sorted(os.listdir(rd)):
            d = json.load(open(os.path.join(rd, f)))
            add(d['planes'], d['triangles'], d.get('type_id', -1), 'n5 %s' % f)
    return sorted(out.items())


def gate_worker(item):
    task, p = item
    t0 = time.monotonic()
    if p.get('chains'):
        from gauss_gate import t22_main
        out = os.path.join(jobdir('gate'), 'chains_2_2.json')
        st = t22_main(out, [p['chains']])
        return {'task': task, 'status': 'CHAINS', 'summary': '2.2: %s' % st, 'stats': st,
                'seconds': round(time.monotonic() - t0, 1)}
    from gauss_gate import config_report, arms_of, arm_report
    planes, tris = p['planes'], [tuple(t) for t in p['triangles']]
    rec = {'task': task, 'type_id': p['type_id'], 'origin': p['origin'], 'planes': planes,
           'triangles': p['triangles']}
    c = config_report(planes, tris, gauges=False)
    rec.update(genus=c['genus'], own_degree=c.get('own_degree'), bad_turning=c.get('bad_turning_faces'))
    arms = []
    if c['genus'] < 6:
        for t1, t2, R in arms_of(planes, tris, len(planes)):
            a = arm_report(planes, tris, R, (t1, t2))
            arms.append({k: a.get(k) for k in ('tube', 'own_degree', 'target_degree', 'k_tau', 'hemisphere_margin',
                                               'n_admissible', 'min_reversed', 'n_tube_only', 'pass', 'error')})
    rec['arms'] = arms
    rec['status'] = 'GATE'
    rec['seconds'] = round(time.monotonic() - t0, 1)
    rec['summary'] = 'type %s genus %d (degree %s): %d arms, T1 pass %d, k_tau %s' % (
        p['type_id'], c['genus'], c.get('own_degree'), len(arms), sum(1 for a in arms if a.get('pass')),
        sorted(set(a.get('k_tau') for a in arms), key=str))
    return rec


def job_gate(args, committer):
    tasks = [('r_%s' % k, r) for k, r in gate_realizations()]
    gl = os.path.join(RES, 'glad', 'results.jsonl')
    if os.path.exists(gl):
        tasks.append(('chains', {'chains': gl}))
    run_pool('gate', tasks, gate_worker, args, committer)


def _n5_climb(planes, tris, type_id, minutes, rng, task, log_path, depth=0):
    """Normals-first from one realization over all its extendable arms (equal shares); recursive on success.
    Returns the highest realized record or None."""
    from gauss_gate import arms_of, genus
    from normals_first import run_arm
    arms = arms_of(planes, [tuple(t) for t in tris], len(planes))
    if not arms or minutes <= 0:
        return None
    best = None
    t_end = time.monotonic() + 60 * minutes
    for i, (t1, t2, R) in enumerate(arms):
        left = (t_end - time.monotonic()) / 60
        if left <= 0.5:
            break
        rec, _ = run_arm(planes, tris, R, (t1, t2), left / (len(arms) - i), rng, log_path,
                         tag='%s climb%d arm %d' % (task, depth, i), log=lambda *a: None)
        if rec and rec.get('exact'):
            rec['type_id'] = type_id
            _save_realized(task + '_c%d_%d' % (depth, i), rec)
            best = rec
            if genus(rec['triangles'], len(planes)) < 6:
                up = _n5_climb(rec['planes'], rec['triangles'], type_id, (t_end - time.monotonic()) / 60, rng, task,
                               log_path, depth + 1)
                if up:
                    best = up
            break
    return best


def _save_realized(name, rec):
    d = os.path.join(jobdir('n5'), 'realized')
    os.makedirs(d, exist_ok=True)
    write_json_atomic(os.path.join(d, name + '.json'), {k: rec[k] for k in ('planes', 'triangles', 'type_id', 'genus', 'tube')
                                                        if k in rec})


def n5_worker(item):
    task, p = item
    import numpy as np
    from gauss_gate import arms_of, genus
    from normals_first import run_arm
    t0 = time.monotonic()
    rng = np.random.default_rng(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16))
    att = os.path.join(jobdir('n5'), 'attempts')
    os.makedirs(att, exist_ok=True)
    log_path = os.path.join(att, task + '.jsonl')
    out = {'task': task, 'kind': p['kind'], 'type_id': p.get('type_id')}
    realized = None
    if p['kind'] == 'g6':
        rec, stats = run_arm(None, None, [tuple(t) for t in p['triangles']], None, p['minutes'], rng, log_path,
                             mode='free', rev_cost=0, timeout=p['timeout'], tag=task, log=lambda *a: None)
        out['stats'] = stats; realized = rec
    else:
        planes, tris = p['planes'], [tuple(t) for t in p['triangles']]
        arm = next(a for a in arms_of(planes, tris, len(planes)) if [list(a[0]), list(a[1])] == p['tube'])
        t1, t2, R = arm
        seed_planes = planes; seed_tris = tris; minutes = p['minutes']
        if p['kind'] == 'kdrift':
            from kdrift import drift
            dr, Hd = drift(planes, tris, R, (t1, t2), minutes / 2, rng, log=lambda *a: None)
            out['drift'] = {k: dr.get(k) for k in ('status', 'k_tau', 'energy', 'hemisphere_margin', 't1', 'steps')}
            if dr['status'] in ('T1_PASS', 'K_REACHED'):
                seed_planes = Hd.tolist()
                sd = os.path.join(jobdir('n5'), 'class_seeds'); os.makedirs(sd, exist_ok=True)
                write_json_atomic(os.path.join(sd, task + '.json'), dict(dr, next_triangles=[list(t) for t in R],
                                                                         type_id=p.get('type_id')))
            minutes = max(0.5, minutes - (time.monotonic() - t0) / 60)
            if dr['status'] != 'T1_PASS':
                minutes = min(minutes, p['minutes'] / 4)       # out of class: only a short normals-first try
        rec, stats = run_arm(seed_planes, seed_tris, R, (t1, t2), minutes, rng, log_path, timeout=p['timeout'],
                             tag=task, log=lambda *a: None)
        out['stats'] = stats; realized = rec
        if realized and realized.get('exact') and genus(realized['triangles'], 12) < 6:
            realized['type_id'] = p.get('type_id')
            _save_realized(task, realized)
            up = _n5_climb(realized['planes'], realized['triangles'], p.get('type_id'), p['minutes'], rng, task, log_path)
            if up:
                realized = up
    out['seconds'] = round(time.monotonic() - t0, 1)
    if realized and realized.get('exact'):
        g = genus(realized['triangles'], 12)
        realized['type_id'] = p.get('type_id')
        _save_realized(task + '_top', realized)
        out.update(status='REALIZED_GENUS_%d' % g, genus=g, planes=realized['planes'], triangles=realized['triangles'],
                   important=True, candidate=(g == 6))
    else:
        out['status'] = 'NOT_REALIZED'
    out['summary'] = '%s %s %s' % (p['kind'], out.get('stats'), out.get('drift', {}).get('status', ''))
    return out


def job_n5(args, committer):
    """Tasks interleaved by --mix (nfirst, kdrift, g6) from the gate results (run `gate` first)."""
    gate = [r for r in load_results('gate') if r.get('status') == 'GATE']
    arms = []
    for r in gate:
        for a in r.get('arms', []):
            if a.get('error'):
                continue
            arms.append((r, a))
    # rank: higher genus first, T1 pass first, then small hemisphere margin (closest to k_tau changing);
    # round robin over types so that one type with many archived realizations does not take the night
    arms.sort(key=lambda ra: (-ra[0]['genus'], not ra[1].get('pass'), ra[1].get('hemisphere_margin') or 0))
    by_type = {}
    for ra in arms:
        by_type.setdefault(ra[0]['type_id'], []).append(ra)
    rr = []
    while any(by_type.values()):
        for t in sorted(by_type, key=str):
            if by_type[t]:
                rr.append(by_type[t].pop(0))
    nf, kd = [], []
    for r, a in rr:
        base = dict(planes=r['planes'], triangles=r['triangles'], type_id=r['type_id'], tube=a['tube'],
                    minutes=args.minutes_per_seed, timeout=args.timeout)
        tid = '%s_%s' % (r['task'][2:], '_'.join(str(x) for t in a['tube'] for x in t))
        nf.append(('nf_%s' % tid, dict(base, kind='nfirst')))
        if a.get('k_tau') == 0 or not a.get('pass'):
            kd.append(('kd_%s' % tid, dict(base, kind='kdrift')))
    types = json.load(open(os.path.join(HERE, '..', 'data', 'k12_triangulations.json')))
    g6 = []
    for rep in range(args.reps):
        for t in types:
            if str(t['id']) in args.g6_types.split(','):
                g6.append(('g6_%d_%d' % (t['id'], rep), dict(kind='g6', type_id=t['id'], triangles=t['triangles'],
                                                            minutes=args.minutes_per_seed, timeout=args.timeout)))
    mix = [int(x) for x in args.mix.split(',')]
    queues = [nf, kd, g6]
    tasks = []
    while any(queues):
        for q, m in zip(queues, mix):
            for _ in range(m):
                if q:
                    tasks.append(q.pop(0))
    log('n5: %d gated arms from %d realizations; %d tasks (mix nfirst:kdrift:g6 = %s)' % (len(arms), len(gate), len(tasks), args.mix))
    run_pool('n5', tasks, n5_worker, args, committer)


# ----------------------------------------------------------------------------- job: sym

def sym_cases():
    from omsat_sym import parse_lutz, orient, automorphisms, subgroups, classify, compose
    maps = parse_lutz()
    cases = []
    for m in sorted(maps):
        otris = orient(maps[m])
        auts = automorphisms(otris)
        if len(auts) == 1:
            continue
        for grp in ('C2', 'C3'):
            subs = [H for H in subgroups(auts) if classify(H) == grp]
            classes = []
            for H in sorted(subs, key=lambda H: sorted(H)):
                conj = False
                for K in classes:
                    for a, _ in auts:
                        ainv = tuple(sorted(range(12), key=lambda i: a[i]))
                        if frozenset(compose(compose(a, h), ainv) for h in H) == K:
                            conj = True
                            break
                    if conj:
                        break
                if not conj:
                    classes.append(H)
            for w in range(len(classes)):
                cases.append((m, grp, w))
    return cases


def sym_build_immersion(m, grp, which):
    """Symmetric IMMERSION instance: no global triple clauses; faces simple; <= 1 reflex corner per
    vertex; orientation consistency."""
    from omsat_sym import (parse_lutz, orient, links_from_oriented, automorphisms, subgroups, classify,
                           compose, orbfix_quads)
    from omsat import Triangulation, CNF, build
    maps = parse_lutz()
    otris = orient(maps[m])
    links, _ = links_from_oriented(otris)
    T = Triangulation(12, otris, links)
    auts = automorphisms(otris)
    eps = dict(auts)
    subs = [H for H in subgroups(auts) if classify(H) == grp]
    classes = []
    for H in sorted(subs, key=lambda H: sorted(H)):
        conj = False
        for K in classes:
            for a, _ in auts:
                ainv = tuple(sorted(range(12), key=lambda i: a[i]))
                if frozenset(compose(compose(a, h), ainv) for h in H) == K:
                    conj = True
                    break
            if conj:
                break
        if not conj:
            classes.append(H)
    H = classes[which]
    sym = [(g, eps[g]) for g in H if g != tuple(range(12))]
    def make(local):
        C = CNF(12)
        P = build(C, T, dict(gp=True, triples=False, reflex=local, poc=local), sym=sym)
        basis, _ = orbfix_quads(H)
        for S in basis:
            C.clause([C.chi_pos_lit(S)], 'SB_ORBFLIP')
        C.clause([C.chi_pos_lit((0, 1, 2, 3))], 'SB_MIRROR')
        if local:
            for X in range(12):
                L = T.link[X]
                for i in range(11):
                    for j in range(i + 2, 11):
                        if not (i == 0 and j == 10):
                            C.clause([-P.E(X, L[i], L[j]), -P.E(X, L[j], L[i])], 'SIMPLE')
        return C
    return make(True), make(False)


def sym_build(m, grp, which, opts):
    from omsat_sym import (parse_lutz, orient, links_from_oriented, automorphisms, subgroups, classify,
                           compose, build_sym)
    from omsat import Triangulation
    maps = parse_lutz()
    otris = orient(maps[m])
    links, _ = links_from_oriented(otris)
    T = Triangulation(12, otris, links)
    auts = automorphisms(otris)
    eps = dict(auts)
    subs = [H for H in subgroups(auts) if classify(H) == grp]
    classes = []
    for H in sorted(subs, key=lambda H: sorted(H)):
        conj = False
        for K in classes:
            for a, _ in auts:
                ainv = tuple(sorted(range(12), key=lambda i: a[i]))
                if frozenset(compose(compose(a, h), ainv) for h in H) == K:
                    conj = True
                    break
            if conj:
                break
        if not conj:
            classes.append(H)
    H = classes[which]
    C, _, _ = build_sym(T, H, eps, opts)
    C0, _, _ = build_sym(T, H, eps, dict(gp=True, triples=False))
    return C, C0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sym_worker(item):
    task, p = item
    from pysat.solvers import Solver
    import threading
    t0 = time.monotonic()
    m, grp, which = p['case']
    opts = dict(gp=True, triples=True)
    for k in p['opts']:
        opts[k] = True
    C, C0 = sym_build_immersion(m, grp, which) if p.get('immersion') else sym_build(m, grp, which, opts)
    with Solver(name='cadical195', bootstrap_with=C0.clauses) as s0:
        ctl_timer = threading.Timer(p['timeout'], lambda: s0.interrupt())
        ctl_timer.start()
        control = s0.solve_limited(expect_interrupt=True)       # None if it hit the timeout
        ctl_timer.cancel()
    rec = {'task': task, 'map_lutz': m, 'group': grp, 'class': which, 'opts': p['opts'],
           'vars': C.nv, 'clauses': len(C.clauses), 'control_no_triples_SAT': control}
    os.makedirs(WORK, exist_ok=True)
    cnf = os.path.join(WORK, task + '.cnf')
    C.dimacs(cnf, comments=['12-face polyhedron, symmetric OM-SAT, Lutz map #%d group %s class %d opts %s'
                            % (m, grp, which, p['opts'])])
    rec['cnf_sha256'] = sha256_file(cnf)
    if p['cadical'] and p['drat_trim']:
        proof = os.path.join(WORK, task + '.drat')
        ts = time.monotonic()
        r = subprocess.run([p['cadical'], '-q', '-t', str(int(p['timeout'])), cnf, proof],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        rec['solve_seconds'] = round(time.monotonic() - ts, 1)
        status = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'TIMEOUT')
        rec['solver'] = 'cadical-binary'
        if status == 'UNSAT':
            rec['proof_bytes'] = os.path.getsize(proof)
            rec['proof_sha256'] = sha256_file(proof)
            tv = time.monotonic()
            v = subprocess.run([p['drat_trim'], cnf, proof, '-t', str(int(p['check_timeout']))],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            rec['drat_trim_seconds'] = round(time.monotonic() - tv, 1)
            rec['drat_trim'] = 'VERIFIED' if 's VERIFIED' in v.stdout else 'NOT VERIFIED'
            rec['drat_trim_tail'] = v.stdout[-300:]
            status = 'UNSAT-VERIFIED' if rec['drat_trim'] == 'VERIFIED' else 'UNSAT-PROOF-FAILED'
        if not p['keep_proofs'] and os.path.exists(proof):
            os.remove(proof)
    else:
        s = Solver(name='cadical195', bootstrap_with=C.clauses)
        timer = threading.Timer(p['timeout'], lambda: s.interrupt())
        timer.start()
        r = s.solve_limited(expect_interrupt=True)
        timer.cancel()
        rec['solve_seconds'] = round(time.monotonic() - t0, 1)
        rec['solver'] = 'pysat-cadical195 (no proof)'
        status = {True: 'SAT', False: 'UNSAT-UNVERIFIED', None: 'TIMEOUT'}[r]
        if r is True:
            mdl = set(l for l in s.get_model() if l > 0)
            rec['chi_plus'] = [''.join('%x' % e for e in S) for S, v in C.qvar.items() if v in mdl]
        s.delete()
    if not p['keep_cnf']:
        os.remove(cnf)
    rec['status'] = status
    rec['candidate'] = status == 'SAT'           # would contradict the claimed symmetric theorem
    rec['summary'] = '#%d %s/%d %s %.0fs' % (m, grp, which, status, rec['solve_seconds'])
    return rec


def job_sym(args, committer):
    cases = sym_cases()
    log('symmetric cases (map, group, class):', len(cases))
    cad = args.cadical or shutil.which('cadical')
    drat = args.drat_trim or shutil.which('drat-trim')
    if not (cad and drat):
        log('WARNING: cadical/drat-trim not found; results will be UNVERIFIED (see README for setup)')
    tasks = [('sym_%d_%s_%d' % c, dict(case=c, opts=args.sym_opts.split(',') if args.sym_opts else [],
                                        cadical=cad, drat_trim=drat, timeout=args.timeout,
                                        check_timeout=args.check_timeout, keep_proofs=args.keep_proofs,
                                        keep_cnf=args.keep_cnf))
             for c in sorted(cases, key=lambda c: c[1] != 'C2')]      # hard C2 cases first, quick C3 fill the tail
    job = 'symimm' if args.sym_immersion else 'sym'
    for t, p in tasks:
        p['immersion'] = args.sym_immersion
    run_pool(job, tasks, sym_worker, args, committer)


# ----------------------------------------------------------------------------- job: cube

def cube_child(m, opts, cube, nchi, q):
    """Solve one cube in a separate process (killed by the parent on timeout)."""
    from pysat.solvers import Solver
    C = cube_build(m, opts)
    with Solver(name='cadical195', bootstrap_with=C.clauses) as s:
        r = s.solve(assumptions=cube)
        out = {'status': 'SAT' if r else 'UNSAT'}
        if r:
            out['model_chi_true'] = [l for l in s.get_model()[:nchi + 1] if l > 0]
    q.put(out)


def cube_build(m, opts):
    from omsat_sym import parse_lutz, orient, links_from_oriented
    from omsat import Triangulation, CNF, build
    maps = parse_lutz()
    otris = orient(maps[m])
    links, _ = links_from_oriented(otris)
    T = Triangulation(12, otris, links)
    C = CNF(12)
    build(C, T, opts)
    return C


def job_cube(args, committer):
    import collections
    opts = dict(gp=True, triples=True, reflex=True, poc=True, symbreak=True, mirror=True)
    for m in [int(x) for x in args.maps.split(',')]:
        job = 'cube_map%d' % m
        d = jobdir(job)
        os.makedirs(WORK, exist_ok=True)
        cnf = os.path.join(WORK, 'full_map%d.cnf' % m)
        stp = os.path.join(d, 'state.json')
        if not os.path.exists(stp) or not os.path.exists(cnf):
            log('building full CNF for Lutz map #%d ...' % m)
            C = cube_build(m, opts)
            C.dimacs(cnf, comments=['12-face polyhedron, full asymmetric OM-SAT, Lutz map #%d opts %s' % (m, opts)])
            nchi = len(C.qvar)
            occ = collections.Counter(abs(l) for cl in C.clauses for l in cl if 2 <= abs(l) <= nchi + 1)
            units = {abs(cl[0]) for cl in C.clauses if len(cl) == 1}
            order = [v for v, _ in occ.most_common() if v not in units]
            del C
        if os.path.exists(stp):
            st = json.load(open(stp))
        else:
            st = {'map': m, 'opts': opts, 'cnf_sha256': sha256_file(cnf), 'order': order, 'nchi': nchi,
                  'open': [[]], 'refuted_fraction': 0.0, 'sat': []}
            write_json_atomic(stp, st)
        if sha256_file(cnf) != st['cnf_sha256']:
            raise SystemExit('CNF changed since the run started; delete results/%s to restart' % job)
        deadline = time.monotonic() + args.hours * 3600
        ctx = mp.get_context('spawn')
        log('%s: open cubes %d, refuted fraction %.6f' % (job, len(st['open']), st['refuted_fraction']))
        running = {}                                    # key -> (cube, process, queue, start)
        try:
            while (st['open'] or running) and time.monotonic() < deadline:
                for cube in st['open']:                    # cubes stay in 'open' until finished
                    if len(running) >= args.workers:
                        break
                    k = ','.join(map(str, cube)) or 'root'
                    if k not in running:
                        q = ctx.Queue()
                        pr = ctx.Process(target=cube_child, args=(m, opts, cube, st['nchi'], q), daemon=True)
                        pr.start()
                        running[k] = (cube, pr, q, time.monotonic())
                time.sleep(1)
                for k in list(running):
                    cube, pr, q, t0 = running[k]
                    res = None
                    if not q.empty():
                        res = q.get()
                    elif time.monotonic() - t0 > args.timeout or not pr.is_alive():
                        res = {'status': 'TIMEOUT' if pr.is_alive() else 'ERROR'}
                    if res is None:
                        continue
                    pr.terminate()
                    pr.join()
                    del running[k]
                    rec = dict(res, task=k, cube=cube, seconds=round(time.monotonic() - t0, 1))
                    st['open'] = [c for c in st['open'] if c != cube]
                    if rec['status'] == 'UNSAT':
                        st['refuted_fraction'] += 2.0 ** (-len(cube))
                    elif rec['status'] == 'SAT':
                        st['sat'].append(cube)
                        rec['candidate'] = True
                        save_candidate(job, rec)
                    else:                                       # TIMEOUT/ERROR: split on next variable
                        used = {abs(l) for l in cube}
                        v = next(x for x in st['order'] if x not in used)
                        st['open'] += [cube + [v], cube + [-v]]
                        rec['split_on'] = v
                    rec['refuted_fraction'] = st['refuted_fraction']
                    rec['open'] = len(st['open'])
                    append_result(job, rec)
                    write_json_atomic(stp, st)
                    log(job, rec['task'][:60], rec['status'], '%.0fs' % rec['seconds'],
                        'refuted %.6f open %d' % (st['refuted_fraction'], len(st['open'])))
                    committer.maybe('overnight %s: refuted %.6f' % (job, st['refuted_fraction']),
                                    force=rec['status'] == 'SAT')
            if not st['open'] and not running:
                log('%s FINISHED: %s' % (job, 'SAT cube(s) found' if st['sat'] else 'all cubes UNSAT (instance UNSAT)'))
        finally:
            for k, (cube, pr, q, t0) in running.items():
                pr.terminate()
            write_json_atomic(stp, st)
            committer.maybe('overnight %s: stop, refuted %.6f' % (job, st['refuted_fraction']), force=True)


# ----------------------------------------------------------------------------- job: immersion

def immersion_child(tid, triangles, gauss_k, q):
    """OM-SAT for a polyhedral IMMERSION of type tid (no global embedding clauses)."""
    from omsat import CNF, build, Triangulation
    from omsat_gauss import add_gauss
    from gauss_degree import coherent_triangles, links_from
    from pysat.solvers import Solver
    ot = coherent_triangles(triangles)
    T = Triangulation(12, ot, links_from(ot, 12))
    C = CNF(12)
    P = build(C, T, dict(gp=True, triples=False, reflex=True, poc=True, symbreak=True, mirror=True))
    for X in range(12):
        L = T.link[X]
        for i in range(11):
            for j in range(i + 2, 11):
                if not (i == 0 and j == 10):
                    C.clause([-P.E(X, L[i], L[j]), -P.E(X, L[j], L[i])], 'SIMPLE')
    if gauss_k:
        add_gauss(C, P, T, k=gauss_k)
    with Solver(name='cadical195', bootstrap_with=C.clauses) as s:
        r = s.solve()
        out = {'status': 'SAT' if r else 'UNSAT', 'vars': C.nv, 'clauses': len(C.clauses)}
        if r:
            mdl = set(l for l in s.get_model() if l > 0)
            out['chi_plus'] = [''.join('%x' % e for e in S) for S, v in C.qvar.items() if v in mdl]
    q.put(out)


def job_immersion(args, committer):
    job = 'immersion'
    types = json.load(open(os.path.join(HERE, '..', 'data', 'k12_triangulations.json')))
    done = {r['task'] for r in load_results(job)}
    todo = [t for t in types if 'imm%d_k%d' % (t['id'], args.gauss) not in done
            and (not args.only or args.only in 'imm%d_k%d' % (t['id'], args.gauss))]
    log('%s: %d types to do (%d done)' % (job, len(todo), len(done)))
    deadline = time.monotonic() + args.hours * 3600
    ctx = mp.get_context('spawn')
    running = {}
    try:
        while (todo or running) and time.monotonic() < deadline:
            while todo and len(running) < args.workers:
                t = todo.pop(0)
                q = ctx.Queue()
                pr = ctx.Process(target=immersion_child, args=(t['id'], t['triangles'], args.gauss, q), daemon=True)
                pr.start()
                running['imm%d_k%d' % (t['id'], args.gauss)] = (t, pr, q, time.monotonic())
            time.sleep(2)
            for k in list(running):
                t, pr, q, t0 = running[k]
                res = q.get() if not q.empty() else None
                if res is None and (time.monotonic() - t0 > args.timeout or not pr.is_alive()):
                    res = {'status': 'TIMEOUT' if pr.is_alive() else 'ERROR'}
                if res is None:
                    continue
                pr.terminate(); pr.join(); del running[k]
                rec = dict(res, task=k, type_id=t['id'], gauss_k=args.gauss, seconds=round(time.monotonic() - t0, 1),
                           finished_at=time.strftime('%Y-%m-%d %H:%M:%S'))
                rec['candidate'] = rec['status'] == 'UNSAT'      # UNSAT = no immersion = no embedding: important
                append_result(job, rec)
                log(job, k, rec['status'], '%.0fs' % rec['seconds'])
                if rec['candidate']:
                    save_candidate(job, rec)
                committer.maybe('overnight %s: %s %s' % (job, k, rec['status']), force=rec['status'] == 'UNSAT')
    finally:
        for k, (t, pr, q, t0) in running.items():
            pr.terminate()
        committer.maybe('overnight %s: stop' % job, force=True)


# ----------------------------------------------------------------------------- job: ils

def ils_worker(item):
    task, p = item
    import numpy as np
    import numba
    numba.set_num_threads(1)
    from fastviol import triangulation_tables, violations
    from relocate import relocate
    rng = np.random.default_rng(int(hashlib.sha256(task.encode()).hexdigest()[:8], 16))
    H = np.array(p['planes'], dtype=float)
    H = H / np.linalg.norm(H[:, :3], axis=1)[:, None]
    pa, it = triangulation_tables(12, p['triangles'])
    cur = int(violations(H, pa, it))
    start = cur
    best, bestH = cur, H.copy()
    t0 = time.monotonic()
    steps = kicks = stall = 0
    spread = float(np.std(H[:, 3])) or 1.0
    while time.monotonic() - t0 < 60 * p['minutes'] and best > 0:
        k = int(rng.integers(12))
        c, h, hc, m = relocate(H, pa, it, k, stride=p['stride'], offset=int(rng.integers(p['stride'])), cap=cur + 1)
        H2 = H.copy(); H2[k] = hc
        vc = int(violations(H2, pa, it))
        if vc > c:
            H2[k] = h; vc = int(violations(H2, pa, it))
        steps += 1
        if vc <= cur:
            stall = stall + 1 if vc == cur else 0
            H, cur = H2, vc
        else:
            stall += 1
        if cur < best:
            best, bestH = cur, H.copy()
        if stall >= p['stall']:                     # kick 1-2 planes
            H = bestH.copy() if rng.random() < 0.5 else H
            sig = float(rng.choice([0.003, 0.01, 0.03]))
            for q in rng.choice(12, size=int(rng.integers(1, 3)), replace=False):
                H[q, :3] += sig * rng.standard_normal(3)
                H[q, 3] += sig * spread * rng.standard_normal()
            cur = int(violations(H, pa, it))
            kicks += 1
            stall = 0
    rec = {'task': task, 'seed_id': p['seed_id'], 'source': p['source'], 'start_count': start,
           'best_count': best, 'steps': steps, 'kicks': kicks, 'seconds': round(time.monotonic() - t0, 1)}
    rec['status'] = 'IMPROVED' if best < start else 'NO_IMPROVEMENT'
    if best < start:
        rec['planes'] = bestH.tolist()
        rec['triangles'] = p['triangles']
    if best == 0:
        from fixed_normals import exact_check
        Hi = [[int(round(x * 10 ** 9)) for x in h] for h in bestH]
        ok, nv, nb = exact_check(Hi, p['triangles'])
        rec.update({'exact_embedded': ok, 'exact_violated_triples': nv, 'exact_bad_pairs': nb,
                    'planes_int': Hi, 'candidate': bool(ok)})
    rec['summary'] = '%d -> %d (%d steps, %d kicks)' % (start, best, steps, kicks)
    return rec


def job_ils(args, committer):
    seeds = json.load(open(SEEDS))
    tasks = [('ils%d_r%d' % (s['seed_id'], r), dict(s, minutes=args.minutes_per_seed, stride=args.stride,
                                                     stall=args.stall))
             for r in range(args.rounds) for s in seeds if s['ours'] <= args.max_seed_count]
    run_pool('ils', tasks, ils_worker, args, committer)


# ----------------------------------------------------------------------------- status

def job_status(args, committer):
    if not os.path.isdir(RES):
        print('no results yet')
        return
    for job in sorted(os.listdir(RES)):
        recs = load_results(job)
        import collections
        c = collections.Counter(r.get('status') for r in recs)
        print('%-14s %5d records  %s' % (job, len(recs), dict(c)))
        cd = os.path.join(RES, job, 'CANDIDATES')
        if os.path.isdir(cd) and os.listdir(cd):
            print('   CANDIDATES:', os.listdir(cd))
        st = os.path.join(RES, job, 'state.json')
        if os.path.exists(st):
            s = json.load(open(st))
            print('   refuted fraction %.6f, open cubes %d, SAT cubes %d' % (s['refuted_fraction'], len(s['open']), len(s['sat'])))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('job', choices=['gnormals', 'pdefect', 'immersion', 'normals', 'sym', 'cube', 'ils', 'ladder', 'sdefect', 'glad', 'arch', 'gate', 'n5', 'status'])
    ap.add_argument('--hours', type=float, default=8.0, help='wall-clock budget of this invocation')
    ap.add_argument('--workers', type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument('--timeout', type=float, default=None, help='per-task solver timeout in seconds')
    ap.add_argument('--git', action='store_true', help='commit results/ periodically')
    ap.add_argument('--push', action='store_true', help='also git push after each commit')
    ap.add_argument('--commit-minutes', type=float, default=30)
    ap.add_argument('--only', default='', help='run only tasks whose id contains this substring')
    ap.add_argument('--results-dir', default=None, help='override results directory (testing)')
    # normals
    ap.add_argument('--max-seed-count', type=int, default=10)
    ap.add_argument('--perturb-max-count', type=int, default=6)
    ap.add_argument('--perturb-reps', type=int, default=3)
    # gnormals
    ap.add_argument('--reps', type=int, default=1000, help='gnormals: samples per type (round robin over 59 types)')
    ap.add_argument('--anneal-minutes', type=float, default=3.0)
    # immersion
    ap.add_argument('--gauss', type=int, default=0, help='immersion: number of Gauss-degree directions (0 = off)')
    # sym
    ap.add_argument('--cadical', default=None)
    ap.add_argument('--drat-trim', default=None)
    ap.add_argument('--sym-opts', default='reflex,poc')
    ap.add_argument('--sym-immersion', action='store_true',
                    help='sym: certify that no symmetric IMMERSION exists (results in results/symimm)')
    ap.add_argument('--check-timeout', type=float, default=40000)
    ap.add_argument('--keep-proofs', action='store_true')
    ap.add_argument('--keep-cnf', action='store_true')
    # cube
    ap.add_argument('--maps', default='1', help='comma-separated Lutz map numbers')
    # ils
    ap.add_argument('--minutes-per-seed', type=float, default=20)
    ap.add_argument('--stride', type=int, default=4)
    ap.add_argument('--stall', type=int, default=24)
    ap.add_argument('--rounds', type=int, default=1)
    ap.add_argument('--ladder-n', default='8', help='ladder: comma-separated face counts (8 = genus 2)')
    ap.add_argument('--milp-seconds', type=float, default=45, help='sdefect: time limit per simple-defect MILP')
    ap.add_argument('--mix', default='4,3,1', help='n5: tasks per round for nfirst, kdrift, g6')
    ap.add_argument('--g6-types', default='0,11,58', help='n5: types for genus-6 normals-first tasks')
    ap.add_argument('--gauss-gate', action='store_true', help='arch: never pick arms that fail the Gauss gate T1')
    ap.add_argument('--branch-minutes', type=float, default=0,
                    help='glad: budget for branching from the highest realized level (genus >= 2) over every extendable handle')
    args = ap.parse_args()
    if args.results_dir:
        global RES
        RES = os.path.abspath(args.results_dir)
        os.environ['POLY_RESULTS_DIR'] = RES            # spawned pool workers re-import this module
    if args.timeout is None:
        args.timeout = {'gnormals': 900, 'pdefect': 0, 'immersion': 3600, 'normals': 1800, 'sym': 4 * 3600, 'cube': 900, 'ils': 0, 'ladder': 0, 'sdefect': 0, 'glad': 0, 'arch': 0, 'gate': 0, 'n5': 600, 'status': 0}[args.job]
    committer = Committer(args)
    {'gnormals': job_gnormals, 'pdefect': job_pdefect, 'immersion': job_immersion, 'normals': job_normals, 'sym': job_sym, 'cube': job_cube, 'ils': job_ils, 'ladder': job_ladder, 'sdefect': job_sdefect, 'glad': job_glad, 'arch': job_arch, 'gate': job_gate, 'n5': job_n5, 'status': job_status}[args.job](
        args, committer)


if __name__ == '__main__':
    main()
