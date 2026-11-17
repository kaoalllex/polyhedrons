"""Stage B: plain (10 elements) and uniform free-C3 formulas of the admissible Cayley (9, 4) maps. No proofs:
an UNSAT is UNSAT-SOLVER (formula scope only); a TIMEOUT decides nothing; a SAT model is saved and clause-checked."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
os.environ.setdefault('NO_PROOF', '1')
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
import pilot  # noqa: E402
from pilot import ALL_OPTS, CNF, build, build_sym, chirotope_from_planes, closure, from_links, solve  # noqa: E402

assert pilot.NO_PROOF, 'no proofs in this experiment (PLAN.md)'
MAPS = HERE / 'results/census/maps_9_4.json'


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def link_automorphisms(links):
    """Face permutations preserving every cyclic link (orientation-preserving); face 0's link fixes the rest."""
    n = len(links); out = set()
    for image, link in enumerate(links):
        if len(link) != len(links[0]):
            continue
        for shift in range(len(link)):
            p = {0: image}
            if any(p.setdefault(a, b) != b for a, b in zip(links[0], link[shift:] + link[:shift])):
                continue
            if len(p) != n or len(set(p.values())) != n:
                continue
            q = tuple(p[k] for k in range(n))
            if all(any([q[v] for v in a] == links[q[k]][j:] + links[q[k]][:j] for j in range(len(a)))
                   for k, a in enumerate(links)):
                out.add(q)
    return sorted(out)


def free_c3_classes(links):
    """One generator per Aut+-conjugacy class of subgroups of order 3 acting without fixed faces."""
    auts = link_automorphisms(links); n = len(links)
    inv = {g: tuple(sorted(range(n), key=lambda i: g[i])) for g in auts}
    subgroups = {frozenset((p, compose(p, p))) for p in auts
                 if compose(p, compose(p, p)) == tuple(range(n)) and all(p[i] != i for i in range(n))}
    reps = {}
    for s in subgroups:
        orbit = {frozenset(compose(compose(g, p), inv[g]) for p in s) for g in auts}
        reps.setdefault(min(min(o) for o in orbit), min(s))
    return len(auts), [reps[k] for k in sorted(reps)]


def units():
    maps = [m for m in json.loads(MAPS.read_text())['maps'] if m['admissible']]
    c3, plain = [], []
    for i, m in enumerate(maps):
        aut, gens = free_c3_classes(m['links'])
        assert aut == m['aut_plus'], (i, aut, m['aut_plus'])
        assert gens, f'map {i}: a Cayley map of Z9 or Z3 x Z3 has a free C3'
        c3 += [dict(unit=f'map{i}_C3_{j}', map=i, generator=list(p)) for j, p in enumerate(gens)]
        plain.append(dict(unit=f'map{i}_plain', map=i, generator=None))
    return maps, c3 + plain


def formula(links, generator):
    t = from_links(links)
    if generator is None:
        c = CNF(t.n); build(c, t, ALL_OPTS)
        return c
    group = sorted(closure([tuple(generator)], t.n))
    return build_sym(t, group, {g: 1 for g in group}, ALL_OPTS)[0]


def pinned(c, chi):
    c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()])
    return c


def controls(out, cap):
    """Formula-side controls; each must give its expected status before any target formula."""
    report = {}
    fixtures = pilot.controls()
    (rv_name, rv_planes, rv_t), (_, _, mz_t) = fixtures[:2]
    c = CNF(rv_t.n); build(c, rv_t, ALL_OPTS)
    report['roest_vigh_pinned'] = solve(pinned(c, chirotope_from_planes(rv_planes)), out, 'roest_vigh_pinned', cap)
    c = CNF(mz_t.n); build(c, mz_t, ALL_OPTS)
    report['cross_map_pinned'] = solve(pinned(c, chirotope_from_planes(rv_planes)), out, 'cross_map_pinned', cap)
    maps, todo = units()
    if not maps:
        report['PASS'] = report['roest_vigh_pinned']['status'] == 'SAT' and report['cross_map_pinned']['status'] == 'UNSAT-SOLVER'
        report['note'] = 'no admissible (9, 4) map: the target-side controls have no input'
        return report
    rng = random.Random(261117)
    while True:
        h = [[rng.randint(-100, 100) for _ in range(4)] for _ in range(9)]
        chi = chirotope_from_planes(h)
        if all(chi.values()):
            break
    c = CNF(9); c.defs_only = True; build(c, from_links(maps[0]['links']), ALL_OPTS); c.gp()
    report['nine_plane_gp'] = solve(pinned(c, chi), out, 'nine_plane_gp', cap)
    u = todo[0]
    from controls import symmetric_planes
    for seed in range(100):
        h = symmetric_planes(tuple(u['generator']), 3, seed)
        chi = chirotope_from_planes(h)
        if all(chi.values()):
            break
    else:
        raise AssertionError('no uniform C3 control')
    group = sorted(closure([tuple(u['generator'])], 9))
    c, _, _ = build_sym(from_links(maps[u['map']]['links']), group, {g: 1 for g in group},
                        dict(gp=True, triples=False), mirror=False, orbfix=False)
    report['c3_symmetric_gp'] = solve(pinned(c, chi), out, 'c3_symmetric_gp', cap)
    expected = dict(roest_vigh_pinned='SAT', cross_map_pinned='UNSAT-SOLVER', nine_plane_gp='SAT', c3_symmetric_gp='SAT')
    report['PASS'] = all(report[k]['status'] == v for k, v in expected.items())
    return report


def done(results):
    return {json.loads(line)['unit'] for p in results.glob('*/results.jsonl') for line in p.read_text().splitlines()}


def shard(out, k, shards, budget, cap):
    out.mkdir(parents=True, exist_ok=True)
    maps, todo = units()
    mine = [u for i, u in enumerate(todo) if i % shards == k]
    skip = done(out.parent)
    end = time.monotonic() + budget
    with (out / 'results.jsonl').open('a') as log:
        for u in mine:
            if u['unit'] in skip:
                continue
            left = end - time.monotonic()
            if left < 5:
                break
            if (out / 'STOP').exists():
                break
            c = formula(maps[u['map']]['links'], u['generator'])
            r = solve(c, out, u['unit'], min(cap, left))
            r.update(u, scope='uniform free-C3 ansatz' if u['generator'] else 'plain formula, 10 elements',
                     cap_seconds=cap, map_code_sha256=hashlib.sha256(json.dumps(maps[u['map']]['code']).encode()).hexdigest())
            log.write(json.dumps(r) + '\n'); log.flush()
            print(u['unit'], r['status'], round(r['seconds'], 1), flush=True)
            if r['status'] == 'ERROR':
                raise RuntimeError(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=10)
    ap.add_argument('--budget', type=float, default=280)
    ap.add_argument('--cap', type=float, default=120)
    a = ap.parse_args()
    if a.controls:
        a.out.mkdir(parents=True, exist_ok=True)
        report = controls(a.out, 60)
        (a.out / 'formula_controls.json').write_text(json.dumps(report, indent=1) + '\n')
        print(json.dumps({k: v if k == 'PASS' else v['status'] for k, v in report.items()}))
        sys.exit(0 if report['PASS'] else 1)
    shard(a.out, a.shard, a.shards, a.budget, a.cap)


if __name__ == '__main__':
    main()
