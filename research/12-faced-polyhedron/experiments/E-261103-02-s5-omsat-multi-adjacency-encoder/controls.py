"""Reproducible, bounded encoder controls; never solve a target map."""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import threading
import time

from test_encoder import ROOT, controls, from_links, perturb, EncoderTests
from omsat import CNF, Eval, build, chirotope_from_planes, load_types, perm_parity
from omsat_sym import build_sym, closure, sym_consistency, orient, automorphisms
from omsat_validate import ALL_OPTS, compare_direct, uniform, cnf_check
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def unit_refutes(clauses):
    """Independent unit propagation, sufficient for these fixed-chi negative controls."""
    assigned = set()
    pending = [set(c) for c in clauses]
    while True:
        changed = False
        for clause in pending:
            if clause & assigned:
                continue
            rest = {v for v in clause if -v not in assigned}
            if not rest:
                return True
            if len(rest) == 1:
                assigned.update(rest)
                changed = True
        if not changed:
            return False


def solve(c, out, name, chi=None, expected=True):
    if chi is not None:
        assert all(v in (-1, 1) for v in chi.values())
        c.clauses.extend([[c.qvar[s] if v > 0 else -c.qvar[s]] for s, v in chi.items()])
    path = out / (name + '.cnf')
    c.dimacs(path, [name, 'control only; pinned chi or symmetry-only, no target decision'])
    started = time.monotonic()
    with Solver(name='cadical195', bootstrap_with=c.clauses, with_proof=True) as solver:
        timer = threading.Timer(60, solver.interrupt)
        timer.start()
        try:
            sat = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        assert sat is expected, (name, sat, expected)
        if sat:
            model = set(solver.get_model())
            assert all(any(lit in model for lit in cl) for cl in c.clauses)
            if chi is not None:
                assert all((c.qvar[s] in model) == (v > 0) for s, v in chi.items())
            dump(out / (name + '.model.json'), sorted(model, key=abs))
        else:
            proof = solver.get_proof()
            (out / (name + '.drat')).write_text('\n'.join(proof) + '\n')
            # Re-check the actual stored DIMACS, not an Eval verdict or solver core.
            stored = [[int(x) for x in line.split()[:-1]] for line in path.read_text().splitlines()
                      if line and line[0] not in 'cp']
            assert unit_refutes(stored), 'negative control is not independently unit-refutable'
            (out / (name + '.rup')).write_text('0\n')
    packed = path.with_suffix('.cnf.gz')
    with gzip.GzipFile(filename=str(packed), mode='wb', mtime=0) as dst:
        dst.write(path.read_bytes())
    path.unlink()
    elapsed = time.monotonic() - started
    return dict(status='SAT' if sat else 'UNSAT', cnf_sha256=sha(packed), variables=c.nv,
                clauses=len(c.clauses), seconds=elapsed, budget_fraction=elapsed / 60,
                ended_by='completed', independently_unit_refuted=not sat)


def census(f, g):
    return json.loads((ROOT / f'experiments/E-261103-01-s5-map-census/results/maps_{f}_{g}.json').read_text())


def symmetric_planes(perm, order, seed):
    """Exact proper C2 or C3 rotation; assign a generic plane to each free orbit."""
    rng = random.Random(seed)
    planes = [None] * len(perm)
    for v in range(len(perm)):
        if planes[v] is not None:
            continue
        h = [rng.randint(-100, 100) for _ in range(4)]
        w = v
        for _ in range(order):
            assert planes[w] is None
            planes[w] = h
            h = ([-h[0], -h[1], h[2], h[3]] if order == 2 else [h[1], h[2], h[0], h[3]])
            w = perm[w]
        assert w == v
    return planes


def symmetry_controls(out):
    t8 = from_links(census(8, 2)['maps'][0]['links'])
    t9 = from_links(census(9, 3)['maps'][0]['links'])
    c2free = (1, 0, 3, 2, 6, 7, 4, 5)
    c3free = (3, 4, 1, 6, 2, 8, 0, 5, 7)
    c2fixed = (1, 0, 3, 2, 6, 7, 4, 5, 8)
    result = {}
    for name, t, p, order in [('C2_free', t8, c2free, 2), ('C3_free', t9, c3free, 3)]:
        group = closure([p], t.n)
        eps = {g: 1 for g in group}
        assert not sym_consistency(group, eps, t.n)
        for seed in range(100):
            h = symmetric_planes(p, order, seed)
            chi = chirotope_from_planes(h)
            if uniform(chi):
                break
        else:
            raise AssertionError('no uniform symmetric control')
        c, _, _ = build_sym(t, group, eps, dict(gp=True, triples=False), mirror=False, orbfix=False)
        result[name] = solve(c, out, name, chi)
        dump(out / (name + '.planes.json'), dict(planes=h, permutation=p, seed=seed))
    for name, generators in [('C2_fixed', [c2fixed]), ('D3', [c3free, c2fixed])]:
        group = closure(generators, 9)
        eps = {g: 1 for g in group}
        bad = sym_consistency(group, eps, 9)
        assert bad
        c, _, _ = build_sym(t9, group, eps, dict(gp=False, triples=False), mirror=False, orbfix=False)
        result[name] = solve(c, out, name, expected=False)
        result[name].update(group_order=len(group), forced_zero_quadruples=len(bad),
                            example=bad[0], scope='uniform cooriented symmetry only; no geometric exclusion')
    assert result['D3']['group_order'] == 6
    return result


def s0_regression():
    expected = json.loads((HERE / 's0_baseline.json').read_text())
    result = {}
    for i, t, _ in load_types(ROOT / 'data/k12_triangulations.json'):
        if i not in (0, 15, 58):
            continue
        for mode in (('plain', 'symmetric', 'full_group') if i == 58 else ('plain', 'symmetric')):
            if mode == 'plain':
                c = CNF(t.n)
                build(c, t, ALL_OPTS)
            elif mode == 'symmetric':
                identity = tuple(range(12))
                c, _, _ = build_sym(t, [identity], {identity: 1}, ALL_OPTS)
            else:
                autos = automorphisms(orient(t.tris))
                c, _, _ = build_sym(t, [g for g, ds in autos], dict(autos), ALL_OPTS)
            key = f'{i}_{mode}'
            digest = hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest()
            assert digest == expected[key]['sha256'], key
            result[key] = expected[key]
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--trials', type=int, default=1000, choices=(1, 1000))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 600
    assert unit_refutes([[1], [-1]]) and not unit_refutes([[1, 2]])
    report = dict(trials_per_object=args.trials, status='RUNNING', controls={})
    try:
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(EncoderTests)
        assert unittest.TextTestRunner().run(suite).wasSuccessful()
        report['s0_regression'] = s0_regression()
        fixtures = controls()
        for name, h, t in fixtures:
            chi = chirotope_from_planes(h)
            zero = [s for s, v in chi.items() if v == 0]
            hp = h if not zero else perturb(h)
            dump(args.out / (name + '.input.json'), dict(raw_planes=h, planes=hp, links=t.link, raw_zero_quads=zero))
            ev = Eval(t.n, chirotope_from_planes(hp))
            build(ev, t, ALL_OPTS)
            assert not ev.violations
            c = CNF(t.n)
            build(c, t, ALL_OPTS)
            r = solve(c, args.out, name, chirotope_from_planes(hp))
            r['backend_check'] = cnf_check(hp, t)
            assert r['backend_check']['agree'] and r['backend_check']['named_mismatch'] == 0
            report['controls'][name] = r
        # Both negatives must pass before any target CNF is built.
        h, t = fixtures[0][1], fixtures[1][2]
        ev = Eval(t.n, chirotope_from_planes(h))
        build(ev, t, ALL_OPTS)
        assert ev.violations
        c = CNF(t.n)
        build(c, t, ALL_OPTS)
        report['negative_cross_map'] = solve(c, args.out, 'roest_vigh_on_mizhaev', chirotope_from_planes(h), False)
        report['negative_cross_map']['violations'] = dict(Counter(ev.violations))
        EncoderTests('test_one_sided_parallel_pairing_is_rejected').test_one_sided_parallel_pairing_is_rejected()
        report['negative_pairing'] = 'REJECTED'
        report['symmetry'] = symmetry_controls(args.out)
        # Preserve all accepted inputs so every mismatch count is exactly replayable.
        for index, (name, h, t) in enumerate(fixtures):
            started = time.monotonic()
            rng = random.Random(261103020 + index)
            stats, degenerate, embedded, count = {}, 0, 0, 0
            with gzip.open(args.out / (name + '.perturbations.jsonl.gz'), 'wt') as samples:
                for attempt in range(args.trials * 20):
                    assert time.monotonic() < deadline, '600-second control budget exhausted'
                    radius = [1, 10, 300, 3000, 10000, 40000][count % 6]
                    pl = [[1000 * v + rng.randint(-radius, radius) for v in row] for row in h]
                    chi = chirotope_from_planes(pl)
                    if not uniform(chi):
                        degenerate += 1
                        continue
                    ev = Eval(t.n, chi)
                    build(ev, t, ALL_OPTS)
                    mism, emb, _ = compare_direct(pl, t, ev, stats)
                    samples.write(json.dumps(dict(attempt=attempt, radius=radius, planes=pl,
                                                  embedded=emb, mismatches=mism, violations=dict(Counter(ev.violations)))) + '\n')
                    assert not mism, (name, count, mism[:10])
                    assert not emb or not ev.violations, (name, count, ev.violations)
                    embedded += emb
                    count += 1
                    if count % 100 == 0 or count == args.trials:
                        print(name, count, 'mismatches 0', flush=True)
                    if count == args.trials:
                        break
            assert count == args.trials
            for kind in ('IN', 'RF', 'RT', 'E', 'lt', 'side'):
                assert 0 < stats[kind + '_true'] < stats[kind], (name, kind, stats)
            r = dict(accepted=count, rejected_degenerate=degenerate, mismatches=0, embedded=embedded,
                     defective=count - embedded, predicate_counts=stats, ended_by='completed',
                     seconds=time.monotonic() - started)
            report['controls'][name]['perturbations'] = r
            dump(args.out / 'summary.json', report)
        # Build only: target decisions belong to E-261103-03.
        rec = census(8, 2)['maps'][0]
        t = from_links(rec['links'])
        c = CNF(t.n)
        build(c, t, ALL_OPTS)
        path = args.out / 'first_8_2.cnf'
        c.dimacs(path, ['first saved (8,2) census map; build only; NOT SOLVED'])
        with gzip.GzipFile(filename=str(path) + '.gz', mode='wb', mtime=0) as dst:
            dst.write(path.read_bytes())
        path.unlink()
        dump(args.out / 'first_8_2.map.json', rec)
        report['first_8_2'] = dict(variables=c.nv, chirotope_variables=len(c.qvar), clauses=len(c.clauses),
                                  tags=c.tags, solved=False)
        report['status'] = 'PASS'
    except BaseException as exc:
        report.update(status='ERROR', error=repr(exc))
        raise
    finally:
        dump(args.out / 'summary.json', report)
    print('ALL CONTROLS PASS; first (8,2) CNF built, not solved', flush=True)


if __name__ == '__main__':
    main()
