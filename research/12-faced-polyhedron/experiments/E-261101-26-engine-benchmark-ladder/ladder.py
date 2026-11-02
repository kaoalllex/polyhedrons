"""Engine benchmark ladder (E-261101-26): tasks with known answers, an engine runner, an exact judge, scores.

  python3 ladder.py build
      writes tasks.json; every task's judge must accept its reference realization, the reference chirotope must
      satisfy the task's CNF (the answer is in the engine's search space), and the judge must reject random planes
  python3 ladder.py run --shard S --shards N --out DIR [--only TASK ...] [--seeds K] [--minutes M] [--alt A] [--timeout S]
      the chirotope-first engine (E-261101-25, E-261102-02 configuration) on the shard's (task, seed) units; one record
      per unit in DIR/results.jsonl, recorded units are skipped on restart; each unit runs in its own process group
      with a hard cap of (budget + 15) minutes (HARD-CAP)
  python3 ladder.py score DIR ... --to FILE [--cutoffs M ...]
      per task: successes / seeds, median minutes to an exact success, the budget; with cutoffs, the successes within
      each M minutes (the engine's budget is only a deadline, so a long unit truncated at M scores an M-minute unit),
      the limit that ended each failure, the fraction of the budget used and the highest k realized

The judge is exact: `ladder_exact.verify` for a full map (all pairs adjacent required only for a neighborly map); for
a k-face task, integer planes in general position whose normalised chirotope satisfies the task's CNF.
"""
import argparse
import collections
import glob
import json
import multiprocessing as mp
import os
import signal
import statistics
import sys
import time
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'experiments', 'E-261101-25-chirotope-first'))
import chirotope_first as CF                                     # noqa: E402  (also puts code/ on sys.path)
import ladder_exact                                              # noqa: E402
from omsat import CNF, Triangulation, chirotope_from_planes     # noqa: E402

TASKS = os.path.join(HERE, 'tasks.json')
ARCH = os.path.join(ROOT, 'experiments/E-261030-10-realization-archive-climb/results/arch/archive.json')
TYPE0 = os.path.join(ROOT, 'experiments/E-261030-03-genus-ladder-type0-genus3/results/type0_genus3_extendable.json')
SZILASSI = os.path.join(ROOT, 'experiments/E-261101-25-chirotope-first/szilassi_control.json')
# the configuration E-261102-02 will run on the target (its run.sh), so the score is the score of that run
ENGINE = dict(alt=20, timeout=60.0, rounds=40, readd=1000, realize_restarts=6, block=1, realizer='two-stage',
              simple=1, fp=1, assume='all', solver='core')
CAP_MARGIN_MIN = 15   # hard cap of a unit = its budget + this margin
log = lambda *a: print(time.strftime('%H:%M:%S'), *a, flush=True)


def tri_list(s):
    return [list(map(int, t.split(','))) for t in s.split(';')]


def make_T(task):
    return Triangulation(task['n'], [tuple(t) for t in task['triangles']], submap=True)


def task_cnf(task, T):
    C = CNF(task['n'])
    CF.build_faces(C, T, task['faces'], simple=bool(ENGINE['simple']))
    return C


def satisfies_cnf(task, T, planes_int, C=None):
    """The normalised chirotope of planes_int is non-degenerate and satisfies the task's CNF (all 715 signs assumed)."""
    try:
        planes_n, _ = CF.normalise(planes_int, task['n'])
    except ValueError as e:
        return False, str(e)
    chi = chirotope_from_planes(planes_n)
    if any(v == 0 for v in chi.values()):
        return False, 'degenerate'
    C = C or task_cnf(task, T)
    r = CF.solve(C.clauses, CF.lits_from_chi(C, chi, list(chi)), C.nv, 300)
    return r['status'] == 'SAT', r['status']


def judge(task, T, planes_int):
    if planes_int is None:
        return False, 'no planes'
    if task['faces'] is None:
        links = {X: list(T.link[X]) for X in range(task['n'])}
        r = ladder_exact.verify(planes_int, links, require_all_pairs=T.neighborly)
        return bool(r['EMBEDDED']), {k: r[k] for k in ('all_pairs_adjacent', 'points_distinct', 'corner_triples_distinct',
                                                        'nonsimple_faces') if k in r}
    return satisfies_cnf(task, T, planes_int)


def genus(n, tris):
    return (2 - (n - 3 * len(tris) // 2 + len(tris))) // 2


# ----------------------------------------------------------------------------- build

def build():
    arch = json.load(open(ARCH))['real']
    by_id = {r['id']: r for r in arch}
    g3 = [r for r in arch if r['genus'] == 3 and r['type_id'] == 15]
    ref15 = g3[0]
    tris15 = tri_list(ref15['map'])
    assert all(r['map'] == ref15['map'] for r in g3), 'type-15 genus-3 realizations on more than one map'
    s15 = set(ref15['map'].split(';'))
    parents = [r['id'] for r in arch if r['genus'] == 2 and len(set(r['map'].split(';')) & s15) == len(s15) - 6]   # one handle less
    t0 = json.load(open(TYPE0))
    sz = json.load(open(SZILASSI))
    rnd = lambda k: [{'random': i} for i in range(k)]
    tasks = [
        dict(id='R1-szilassi', rung='R1', n=7, triangles=sz['triangles'], faces=None, kmax=0, minutes=5,
             seeds=rnd(20), reference={'file': os.path.relpath(SZILASSI, ROOT)}),
        dict(id='R4-type15-genus3', rung='R4', n=12, triangles=tris15, faces=None, kmax=0, minutes=40,
             seeds=rnd(10), reference={'archive': ref15['id']}),
        dict(id='R4-type0-genus3', rung='R4', n=12, triangles=t0['triangles'], faces=None, kmax=0, minutes=40,
             seeds=rnd(10), reference={'file': os.path.relpath(TYPE0, ROOT)}),
        dict(id='R5-type15-genus3-from-parent', rung='R5', n=12, triangles=tris15, faces=None, kmax=0, minutes=40,
             seeds=[{'parent': parents[i % len(parents)], 'noise': 0.0 if i < len(parents) else 0.01} for i in range(10)],
             reference={'archive': ref15['id']}),
    ]
    for k in (7, 8, 9):
        tasks.append(dict(id='R6k-type15-genus3-k%d' % k, rung='R6k', n=12, triangles=tris15, faces=None, kmax=k,
                          minutes=20, seeds=rnd(10), reference={'archive': ref15['id']}))
    rng = np.random.default_rng(12345)
    for t in tasks:
        T = make_T(t)
        t['genus'] = genus(t['n'], t['triangles'])
        t['face_order'] = CF.greedy_face_order(T)
        t['ladder'] = t['kmax'] or 7
        if t['kmax']:
            t['faces'] = t['face_order'][:t['kmax']]
        ref = t['reference']
        planes = by_id[ref['archive']]['planes'] if 'archive' in ref else json.load(open(os.path.join(ROOT, ref['file'])))['planes']
        P = np.array(planes, float)
        C = task_cnf(t, T)
        # a symmetric reference (Szilassi) is not in general position; the realization space is open (FD1), so a
        # small perturbation that the exact judge still accepts is a reference in general position
        for trial in range(10):
            ref_int = CF.to_int(P + rng.normal(scale=1e-5 * trial * np.abs(P).max(), size=P.shape))
            ok_ref, d_ref = judge(t, T, ref_int)
            ok_cnf, d_cnf = (ok_ref, d_ref) if t['faces'] else satisfies_cnf(t, T, ref_int, C)
            if ok_ref and ok_cnf:
                break
        ref['perturbation_trial'] = trial
        ok_rnd, d_rnd = judge(t, T, CF.to_int(CF.random_planes(t['n'], rng)))
        t['controls'] = {'reference_judged': [ok_ref, str(d_ref)], 'reference_in_cnf': [ok_cnf, str(d_cnf)],
                         'random_judged': [ok_rnd, str(d_rnd)], 'cnf': [C.nv, len(C.clauses)]}
        log(t['id'], 'genus', t['genus'], 'faces', t['faces'], t['controls'])
        if not (ok_ref and ok_cnf) or ok_rnd:
            raise SystemExit('control failed on %s: the task has no known answer for this judge / encoder' % t['id'])
    json.dump(tasks, open(TASKS, 'w'), indent=1)
    log('wrote %s: %d tasks, %d units' % (TASKS, len(tasks), sum(len(t['seeds']) for t in tasks)))


# ----------------------------------------------------------------------------- run

def seed_planes(task, i):
    s = task['seeds'][i]
    rng = np.random.default_rng([zlib.crc32(task['id'].encode()), i])
    if 'random' in s:
        return CF.random_planes(task['n'], rng).tolist()
    by_id = {r['id']: r for r in json.load(open(ARCH))['real']}
    P = np.array(by_id[s['parent']]['planes'], float)
    return (P + rng.normal(scale=s['noise'], size=P.shape)).tolist()


def unit(task, i, out):
    os.setpgrp()                                   # the parent can kill this unit with every solver child it forked
    T = make_T(task)
    tag = '%s-seed%d' % (task['id'], i)
    args = argparse.Namespace(**ENGINE, ladder=task['ladder'], kmax=task['kmax'], seed_minutes=task['minutes'],
                              progress=os.path.join(out, 'progress.jsonl'))
    t0 = time.monotonic()
    rec = CF.one_run(T, seed_planes(task, i), args, log, tag, faces_order=task['face_order'])
    seconds = time.monotonic() - t0
    k = task['kmax'] or task['n']
    planes = rec.get('planes') or rec.get('planes_k%d' % k) or rec.get('planes_best')
    ok, detail = judge(task, T, planes)
    keep = ('k', 'iteration', 'status', 'released', 'rounds', 'sat_seconds', 'realized_wrong_signs', 'EMBEDDED')
    steps = [{**{a: s[a] for a in keep if a in s}, 'fp': s.get('final_polynomial', {}).get('status')} for s in rec['steps']]
    out_rec = {'task': task['id'], 'rung': task['rung'], 'seed': i, 'tag': tag, 'minutes': task['minutes'], 'alt': ENGINE['alt'], 'timeout': ENGINE['timeout'],
               'engine_result': rec.get('result'), 'success': ok, 'judge': str(detail), 'seconds': round(seconds, 1),
               'steps': steps, 'planes': planes if ok else None}
    with open(os.path.join(out, 'results.jsonl'), 'a') as f:
        f.write(json.dumps(out_rec) + '\n')
    log('RESULT %s: engine %s, success %s (%s), %.0fs' % (tag, rec.get('result'), ok, detail, seconds))


def run(a):
    if a.alt:
        ENGINE['alt'] = a.alt                      # before the fork, so every unit inherits it
    if a.timeout:
        ENGINE['timeout'] = a.timeout
    tasks = json.load(open(TASKS))
    if a.only:
        tasks = [t for t in tasks if t['id'] in a.only]
    for t in tasks:
        if a.seeds:
            t['seeds'] = t['seeds'][:a.seeds]
        if a.minutes:
            t['minutes'] = a.minutes
    units = [(t, i) for t in tasks for i in range(len(t['seeds']))][a.shard::a.shards]
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, 'results.jsonl')
    # every sibling shard directory counts, so a restart with another shard count does not repeat a unit
    done = {(r['task'], r['seed']) for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(a.out)), '*', 'results.jsonl'))
            for r in map(json.loads, open(f))}
    ctx = mp.get_context('fork')
    for t, i in units:
        if (t['id'], i) in done:
            log('skip %s seed %d: recorded' % (t['id'], i))
            continue
        log('%s seed %d: start (budget %g min)' % (t['id'], i, t['minutes']))
        p = ctx.Process(target=unit, args=(t, i, a.out))
        t0 = time.monotonic()
        p.start()
        p.join(60 * (t['minutes'] + CAP_MARGIN_MIN))
        if p.is_alive():
            os.killpg(p.pid, signal.SIGKILL)
            p.join()
        if p.exitcode != 0:
            status = 'HARD-CAP' if time.monotonic() - t0 >= 60 * (t['minutes'] + CAP_MARGIN_MIN) else 'CRASH %s' % p.exitcode
            with open(path, 'a') as f:
                f.write(json.dumps({'task': t['id'], 'rung': t['rung'], 'seed': i, 'minutes': t['minutes'], 'alt': ENGINE['alt'], 'timeout': ENGINE['timeout'],
                                    'engine_result': status, 'success': False, 'seconds': round(time.monotonic() - t0, 1)}) + '\n')
            log('%s seed %d: %s' % (t['id'], i, status))


# ----------------------------------------------------------------------------- score

def score(a):
    recs = [json.loads(line) for d in a.dirs for line in open(os.path.join(d, 'results.jsonl'))]
    out = {}
    for t in json.load(open(TASKS)):
        rs = [r for r in recs if r['task'] == t['id']]
        if not rs:
            continue
        won = [r['seconds'] / 60 for r in rs if r['success']]
        out[t['id']] = {'rung': t['rung'], 'seeds': len(rs), 'successes': len(won), 'budget_minutes': sorted({r['minutes'] for r in rs}),
                        'median_minutes_to_success': round(statistics.median(won), 2) if won else None,
                        'engine_results': dict(collections.Counter(r['engine_result'] for r in rs))}
        if a.cutoffs:
            out[t['id']]['successes_within_minutes'] = {m: sum(r['success'] and r['seconds'] <= 60 * m for r in rs) for m in a.cutoffs}
            out[t['id']]['units'] = [{'seed': r['seed'], 'result': r['engine_result'], 'success': r['success'],
                                      'budget_fraction': round(r['seconds'] / (60 * r['minutes']), 2),
                                      'alternations': len(r.get('steps', [])),
                                      'k_realized': max([s['k'] for s in r.get('steps', []) if s.get('realized_wrong_signs') == 0], default=None)}
                                     for r in sorted(rs, key=lambda r: r['seed'])]
    seen = lambda key: (lambda v: v if len(v) > 1 else v[0])(sorted({r.get(key, ENGINE[key]) for r in recs}))
    json.dump({'engine': 'chirotope-first (E-261101-25)', 'config': {**ENGINE, 'alt': seen('alt'), 'timeout': seen('timeout')}, 'judge': 'exact (ladder.py)', 'tasks': out},
              open(a.to, 'w'), indent=1)
    for k, v in out.items():
        log(k, '%d/%d' % (v['successes'], v['seeds']), v['median_minutes_to_success'], v['engine_results'])


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('build')
    r = sub.add_parser('run')
    r.add_argument('--shard', type=int, default=0)
    r.add_argument('--shards', type=int, default=1)
    r.add_argument('--out', required=True)
    r.add_argument('--only', nargs='*', default=[])
    r.add_argument('--seeds', type=int, default=0, help='at most this many seeds per task (pilot)')
    r.add_argument('--minutes', type=float, default=0, help='override every budget (pilot)')
    r.add_argument('--alt', type=int, default=0, help='override ENGINE alt, the alternations per face-ladder step')
    r.add_argument('--timeout', type=float, default=0, help='override ENGINE timeout, seconds per SAT call')
    s = sub.add_parser('score')
    s.add_argument('dirs', nargs='+')
    s.add_argument('--to', required=True)
    s.add_argument('--cutoffs', type=int, nargs='*', default=[])
    a = ap.parse_args()
    build() if a.cmd == 'build' else run(a) if a.cmd == 'run' else score(a)


if __name__ == '__main__':
    main()
