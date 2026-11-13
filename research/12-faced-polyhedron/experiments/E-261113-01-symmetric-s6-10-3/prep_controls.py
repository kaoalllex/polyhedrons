"""Prep controls c1-c7 of PLAN.md part (b), through the night's code (`tranche.submap_formula`, `pilot.solve`,
`tranche.bridge`); kissat at $SAT_SOLVER (default ~/bin/kissat), no proofs.

c1  the 25 FD5 symmetric S0 CNFs rebuilt by `run_overnight.sym_build` hash as recorded (encoder regression);
c2  the (10, 2) witness, trivial group through `build_sym` (orbit-flip and mirror normalisation on a sub-map with
    non-adjacent pairs), its normalised chirotope pinned: SAT;
c3  Roest-Vigh with its free C2 (rotation about z), the night's symmetric formula, normalised chirotope pinned: SAT;
c4  negatives on c3: (a) det sign -1 for the involution: UNSAT; (b) the pinned chirotope with one sign flipped on a
    quadruple the involution moves: UNSAT;
c5  Roest-Vigh unpinned symmetric formula: SAT, the model through `tranche.bridge`, the saved file
    `verify_candidate.py --all-pairs` PASS with (V, E, F, chi) = (24, 36, 8, -4);
c6  per formula of maps/sym_formulas.json: no forced-zero quadruple; a random rho-symmetric integer configuration is
    uniform, satisfies the SYM relation, and its normalised chirotope is SAT on the gp-only symmetric formula;
c7  (amendment 2) C3 with one fixed face on an embedded object: the convex cube cut at four alternate corners
    (part (a), t = 2) with the rotation (x, y, z) -> (z, x, y), made uniform by a small C3-symmetric integer
    perturbation (still EMBEDDED by the exact verifier), the night's symmetric formula: pinned normalised SAT,
    unpinned SAT, the model through `tranche.bridge` EMBEDDED with (V, E, F, chi) = (16, 24, 10, 2).
Usage: python3 prep_controls.py OUT_DIR [c1 c2 ...]   (default: all)"""
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
os.environ.setdefault('SAT_SOLVER', str(Path.home() / 'bin/kissat'))
os.environ['NO_PROOF'] = '1'
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
sys.path.insert(0, str(ROOT / 'overnight'))
sys.path.insert(0, str(ROOT / "code"))
import pilot  # noqa: E402
import tranche  # noqa: E402
from omsat import Eval  # noqa: E402
from omsat_sym import orbfix_quads, sym_consistency  # noqa: E402
from ladder_exact import verify  # noqa: E402
import control_rost_vigh  # noqa: E402

FD5 = ROOT / 'experiments/E-261029-13-symmetric-embedding-certificates/results/sym/results.jsonl'
WITNESS = ROOT / 'witnesses/s6_10_2.json'
FORMULAS = HERE / 'maps/sym_formulas.json'


def pin(c, chi):
    c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()])


def normalised(planes, group, n):
    """Orbit flips making every orbit-flip basis quadruple positive, then the mirror if chi(0,1,2,3) < 0, as
    `omsat_sym.build_sym` normalises; returns the chirotope of a real configuration (mirror = reflection + flip all)."""
    basis, orbs = orbfix_quads(group, n)
    oid = {v: k for k, o in enumerate(orbs) for v in o}
    for f in itertools.product((1, -1), repeat=len(orbs)):
        chi = pilot.chirotope_from_planes([[f[oid[X]] * x for x in planes[X]] for X in range(n)])
        if all(chi[S] > 0 for S in basis):
            break
    else:
        raise AssertionError('no orbit flip satisfies the basis')
    if chi[(0, 1, 2, 3)] < 0:
        chi = {S: (-v if n not in S else v) for S, v in chi.items()}
    return chi


def c1(out):
    import run_overnight
    rows = [json.loads(line) for line in FD5.read_text().splitlines()]
    bad = []
    for r in rows:
        opts = dict(gp=True, triples=True, **{k: True for k in r['opts']})
        C, _ = run_overnight.sym_build(r['map_lutz'], r['group'], r['class'], opts)
        cnf = out / 'c1.cnf'
        C.dimacs(str(cnf), comments=['12-face polyhedron, symmetric OM-SAT, Lutz map #%d group %s class %d opts %s'
                                     % (r['map_lutz'], r['group'], r['class'], r['opts'])])
        if pilot.sha(cnf) != r['cnf_sha256']:
            bad.append(r['task'])
        cnf.unlink()
    return dict(PASS=not bad and len(rows) == 25, checked=len(rows), mismatched=bad)


def c2(out):
    data = json.loads(WITNESS.read_text())
    links = {int(k): v for k, v in data['links'].items()}
    e = tuple(range(10))
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
    c = pilot.build_sym(pilot.Triangulation(10, tris, links=links, submap=True), [e], {e: 1}, pilot.ALL_OPTS)[0]
    pin(c, normalised(data['planes'], [e], 10))
    r = pilot.solve(c, out, 'c2_witness_trivial_group', 600)
    return dict(PASS=r['status'] == 'SAT', result=r)


def roest_vigh():
    H, links = control_rost_vigh.build()
    image = [[-h[0], -h[1], h[2], h[3]] for h in H]           # rotation by pi about the z axis
    g = tuple(H.index(v) for v in image)
    assert sorted(g) == list(range(8)) and all(g[i] != i for i in range(8)) and all(g[g[i]] == i for i in range(8))
    return H, links, g


def c3_c4(out):
    H, links, g = roest_vigh()
    e = tuple(range(8))
    group = sorted([e, g])
    chi = normalised(H, group, 8)
    res = {}
    c = tranche.submap_formula(8, links, g)
    pin(c, chi)
    res['c3'] = pilot.solve(c, out, 'c3_rv_c2_pinned', 600)
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
    c = pilot.build_sym(pilot.Triangulation(8, tris, links=links, submap=True), group, {e: 1, g: -1}, pilot.ALL_OPTS)[0]
    pin(c, chi)
    res['c4a'] = pilot.solve(c, out, 'c4a_rv_det_minus', 600)
    S = next(S for S in itertools.combinations(range(9), 4)
             if 8 not in S and tuple(sorted(g[x] for x in S)) != S)
    flipped = dict(chi); flipped[S] = -chi[S]
    c = tranche.submap_formula(8, links, g)
    pin(c, flipped)
    res['c4b'] = pilot.solve(c, out, 'c4b_rv_one_sign_flipped', 600)
    res['c4b_quadruple'] = S
    ok = (res['c3']['status'] == 'SAT' and res['c4a']['status'] == 'UNSAT-SOLVER'
          and res['c4b']['status'] == 'UNSAT-SOLVER')
    return dict(PASS=ok, generator=g, **res)


def c5(out):
    H, links, g = roest_vigh()
    c = tranche.submap_formula(8, links, g)
    r = pilot.solve(c, out, 'c5_rv_c2_unpinned', 3600)
    res = dict(result=r)
    if r['status'] == 'SAT':
        res.update(tranche.bridge(out, 'c5_rv_c2_unpinned', c, links, 'S6'))
        cand = out / 'c5_rv_c2_unpinned.candidate.json'
        if cand.exists():
            p = subprocess.run([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(cand),
                                '--all-pairs'], capture_output=True, text=True)
            (out / 'c5_all_pairs.log').write_text(p.stdout + p.stderr)
            line = p.stdout.strip().splitlines()[0] if p.stdout.strip() else ''
            res['all_pairs_rc'] = p.returncode
            res['V_E_F_chi'] = json.loads(line.split(' ', 1)[1])['V_E_F_chi'] if line.startswith('0 ') else None
    res['PASS'] = res.get('all_pairs_rc') == 0 and res.get('V_E_F_chi') == [24, 36, 8, -4]
    return res


def c7(out):
    import tetra
    links = tetra.convex_links()
    H = tetra.rows(2)
    image = [act(ROT['C3'], h) for h in H]
    g = tuple(H.index(v) for v in image)
    e = tuple(range(10))
    assert sorted(g) == list(e) and sum(g[i] == i for i in e) == 1
    group = sorted(pilot.closure([g], 10))
    rng = random.Random(261113)
    for seed in range(100):
        delta = symmetric_planes(g, 'C3', 10, rng)
        planes = [[1000 * a + b // 50 for a, b in zip(h, d)] for h, d in zip(H, delta)]
        assert all(act(ROT['C3'], planes[X]) == planes[g[X]] for X in e)
        if all(pilot.chirotope_from_planes(planes).values()) and verify(planes, links, require_all_pairs=False)['EMBEDDED']:
            break
    else:
        return dict(PASS=False, note='no uniform embedded C3-symmetric perturbation')
    res = dict(generator=g, planes=planes, perturbation_seeds=seed + 1)
    c = tranche.submap_formula(10, links, g)
    pin(c, normalised(planes, group, 10))
    res['pinned'] = pilot.solve(c, out, 'c7_convex_c3_pinned', 600)
    c = tranche.submap_formula(10, links, g)
    res['unpinned'] = r = pilot.solve(c, out, 'c7_convex_c3_unpinned', 1200)
    if r['status'] == 'SAT':
        res.update(tranche.bridge(out, 'c7_convex_c3_unpinned', c, links, 'S6'))
        geo = [v.get('geometry', {}) for v in res['processing'].values()]
        res['V_E_F_chi'] = next((x['V_E_F_chi'] for x in geo if x.get('EMBEDDED')), None)
    res['PASS'] = (res['pinned']['status'] == 'SAT' and r['status'] == 'SAT' and res.get('candidate') is not None
                   and res.get('V_E_F_chi') == [16, 24, 10, 2])
    return res


ROT = {'C3': ((0, 0, 1), (1, 0, 0), (0, 1, 0)), 'C2': ((-1, 0, 0), (0, -1, 0), (0, 0, 1))}


def act(M, h):
    return [sum(M[i][k] * h[k] for k in range(3)) for i in range(3)] + [h[3]]


def symmetric_planes(gen, kind, n, rng):
    """h_{g X} = diag(rho(g), 1) h_X; a face fixed by the C3 gets a plane perpendicular to the axis (1, 1, 1)."""
    planes = [None] * n
    for r in range(n):
        if planes[r] is not None:
            continue
        if gen[r] == r:
            a = rng.choice([-1, 1]) * rng.randint(1, 50)
            planes[r] = [a, a, a, rng.randint(-1000, 1000)]
            continue
        h = [rng.randint(-1000, 1000) for _ in range(4)]
        x = r
        while planes[x] is None:
            planes[x] = h
            x, h = gen[x], act(ROT[kind], h)
        assert planes[x] == h, 'orbit does not close'
    return planes


def c6(out):
    recs = json.loads(FORMULAS.read_text())['maps']
    rows = []
    for i, rec in enumerate(recs):
        n = len(rec['links'])
        gen = tuple(rec['sym_generator'])
        group = sorted(pilot.closure([gen], n))
        eps = {g: 1 for g in group}
        forced = sym_consistency(group, eps, n)
        rng = random.Random(261113 + i)
        for seed in range(100):
            planes = symmetric_planes(gen, rec['sym_group'], n, rng)
            chi = pilot.chirotope_from_planes(planes)
            if all(chi.values()):
                break
        else:
            rows.append(dict(index=i, lutz=rec['lutz'], uniform=False)); continue
        ev = Eval(n, chi)
        sym_ok = all(ev.chi_neg(tuple(g[x] if x < n else n for x in S)) == ev.chi_neg(S)
                     for g in group for S in itertools.combinations(range(n + 1), 4))
        links = dict(enumerate(rec['links']))
        tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
        c = pilot.build_sym(pilot.Triangulation(n, tris, links=links, submap=True), group, eps,
                            dict(gp=True, triples=False))[0]
        pin(c, normalised(planes, group, n))
        r = pilot.solve(c, out, f'c6_formula{i}', 120)
        rows.append(dict(index=i, lutz=rec['lutz'], group=rec['sym_group'], forced_zero=len(forced), uniform=True,
                         seeds=seed + 1, sym_relation=sym_ok, status=r['status'], seconds=r['seconds']))
    ok = len(rows) == 10 and all(r.get('uniform') and r['forced_zero'] == 0 and r['sym_relation']
                                 and r['status'] == 'SAT' for r in rows)
    return dict(PASS=ok, formulas=rows)


def main(out, which):
    out.mkdir(parents=True, exist_ok=True)
    report = dict(solver_sha256=pilot.sha(Path(pilot.CADICAL)), formulas_sha256=pilot.sha(FORMULAS), controls={})
    path = out / 'controls.json'
    if path.exists():
        report = json.loads(path.read_text())
    for name, f in [('c1', c1), ('c2', c2), ('c3_c4', c3_c4), ('c5', c5), ('c6', c6), ('c7', c7)]:
        if which and not any(name.startswith(w) or w in name for w in which):
            continue
        started = time.monotonic()
        report['controls'][name] = r = f(out)
        r['wall_seconds'] = time.monotonic() - started
        path.write_text(json.dumps(report, indent=1, default=list) + '\n')
        print(name, 'PASS' if r['PASS'] else 'FAIL', round(r['wall_seconds'], 1), flush=True)
    return 0 if all(r['PASS'] for r in report['controls'].values()) else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve(), sys.argv[2:]))
