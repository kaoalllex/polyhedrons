"""PLAN.md part (a): Lutz #15 with its rotation group T, decided exactly; no solver.

Planes: the cube x, y, z = +-1 and the four planes n . p = t (n the even tetrahedron normals). With the map fixed, the
planes fix the polyhedron (vertex XYZ = the point of planes X, Y, Z), so every unit (t, labelling) is decided by the
exact verifier `ladder_exact.verify`. Labellings: bijections faces -> planes whose pulled-back rotations of T are
orientation-preserving map automorphisms. Units: two points inside each interval between consecutive roots of the
4 x 4 determinants (linear in t), two beyond each end, and every root. Planes are integer rows, so the verifier's
1e-9 rounding is exact.

Controls: the convex cube cut at four alternate corners (map built from the hull at t = 2): EMBEDDED only inside
(1, 3) and its point reflection (-3, -1), at t = 2 and at t = -2 (the other labellings), never at t = 4, -4, 1/2,
and never for a non-equivariant labelling at t = 2.
Usage: python3 tetra.py OUT_DIR"""
from fractions import Fraction as Fr
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
from ladder_exact import verify  # noqa: E402
from omsat_sym import automorphisms  # noqa: E402

MAPS = ROOT / 'experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json'
CUBE = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]   # planes n . p = 1
TET = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]                       # planes n . p = t
NORMALS = CUBE + TET


def rows(t):
    """Plane rows (a, b, c, d) of a x + b y + c z + d = 0 at t (Fraction), scaled to integers."""
    t = Fr(t)
    return [[*n, -1] for n in CUBE] + [[t.denominator * a, t.denominator * b, t.denominator * c, -t.numerator]
                                       for a, b, c in TET]


def rotations():
    """The 12 rotations of T as permutations of the 10 planes (signed permutation matrices, det +1, TET kept)."""
    out = set()
    for p in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            M = [[s[i] if j == p[i] else 0 for j in range(3)] for i in range(3)]
            det = round(_det3(M))
            image = [tuple(sum(M[i][k] * n[k] for k in range(3)) for i in range(3)) for n in NORMALS]
            if det == 1 and set(image[6:]) == set(TET):
                out.add(tuple(NORMALS.index(v) for v in image))
    assert len(out) == 12
    return sorted(out)


def _det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def det4(A):
    A = [list(map(Fr, r)) for r in A]
    d = Fr(1)
    for c in range(4):
        piv = next((r for r in range(c, 4) if A[r][c] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            d = -d
        d *= A[c][c]
        for r in range(c + 1, 4):
            f = A[r][c] / A[c][c]
            A[r] = [A[r][k] - f * A[c][k] for k in range(4)]
    return d


def roots():
    """Roots of every 4-subset determinant (linear in t, checked at a third point), and the same list by sympy."""
    out = set()
    unscaled = lambda t: [[*n, -1] for n in CUBE] + [[*n, -Fr(t)] for n in TET]  # noqa: E731
    for S in itertools.combinations(range(10), 4):
        a = det4([unscaled(0)[i] for i in S])
        b = det4([unscaled(1)[i] for i in S]) - a
        assert det4([unscaled(7)[i] for i in S]) == a + 7 * b, 'determinant not linear in t'
        if b != 0:
            out.add(-a / b)
    import sympy
    t = sympy.Symbol('t')
    sym = [[*n, -1] for n in CUBE] + [[*n, -t] for n in TET]
    check = set()
    for S in itertools.combinations(range(10), 4):
        p = sympy.Poly(sympy.Matrix([sym[i] for i in S]).det(), t)
        if p.degree() >= 1:
            check |= {Fr(int(sympy.fraction(r)[0]), int(sympy.fraction(r)[1])) for r in sympy.solve(p.as_expr(), t)}
    assert check == out, ('root lists differ', sorted(out), sorted(check))
    return sorted(out)


def units(rs):
    """(t, kind, interval id) - two interior points per interval, two beyond each end, every root."""
    out = [(rs[0] - 2, 'end', 'below'), (rs[0] - 1, 'end', 'below'), (rs[-1] + 1, 'end', 'above'),
           (rs[-1] + 2, 'end', 'above')]
    for i, (a, b) in enumerate(zip(rs, rs[1:])):
        out += [(a + (b - a) / 3, 'interior', i), (a + 2 * (b - a) / 3, 'interior', i)]
    out += [(r, 'wall', f'root{j}') for j, r in enumerate(rs)]
    return out


def oriented_triangles(links):
    tris, seen = [], set()
    for X, L in links.items():
        for a, b in zip(L, L[1:] + L[:1]):
            if frozenset((X, a, b)) not in seen:
                seen.add(frozenset((X, a, b)))
                tris.append((X, a, b))
    return tris


def labellings(links):
    """Bijections phi (face -> plane) with phi^-1 T phi inside Aut+ of the map; faces of the six-orbit to cube planes."""
    n = len(links)
    aut_plus = {p for p, eps in automorphisms(oriented_triangles(links), n) if eps == 1}
    rot = rotations()
    degree = {X: len(L) for X, L in links.items()}
    classes = sorted({d for d in degree.values()}, key=lambda d: -sum(1 for v in degree.values() if v == d))
    six = [X for X in range(n) if degree[X] == classes[0]]
    four = [X for X in range(n) if degree[X] != classes[0]]
    assert len(six) == 6 and len(four) == 4 and len({degree[X] for X in four}) == 1
    out = []
    for c in itertools.permutations(range(6)):
        for d in itertools.permutations(range(6, 10)):
            phi = [None] * n
            for X, P in zip(six, c):
                phi[X] = P
            for X, P in zip(four, d):
                phi[X] = P
            inv = {P: X for X, P in enumerate(phi)}
            if all(tuple(inv[g[phi[X]]] for X in range(n)) in aut_plus for g in rot):
                out.append(tuple(phi))
    return out, len(aut_plus)


def decide(links, t, phi):
    R = rows(t)
    H = [R[phi[X]] for X in range(len(links))]
    try:
        rep = verify(H, links, require_all_pairs=False)
    except Exception as exc:  # degenerate wall geometry; recorded, counts as not embedded
        return dict(EMBEDDED=False, error=f'{type(exc).__name__}: {exc}')
    return dict(EMBEDDED=bool(rep['EMBEDDED']), nonsimple=len(rep.get('nonsimple_faces', [])),
                bad_pairs=len(rep.get('bad_pairs', [])), points_distinct=rep.get('points_distinct'),
                V_E_F_chi=list(rep['V_E_F_chi']))


def sweep(links, out, name, target=None):
    rs = roots()
    phis, aut = labellings(links)
    table = []
    for t, kind, interval in units(rs):
        reps = [decide(links, t, phi) for phi in phis]
        table.append(dict(t=str(t), kind=kind, interval=str(interval), reports=reps,
                          embedded=[i for i, r in enumerate(reps) if r['EMBEDDED']]))
    constancy = True
    for interval in {u['interval'] for u in table if u['kind'] != 'wall'}:
        pair = [u['reports'] for u in table if u['interval'] == interval and u['kind'] != 'wall']
        constancy &= all(r == pair[0] for r in pair)
    candidates = []
    for u in table:
        for i in u['embedded']:
            path = out / f'{name}_t{u["t"].replace("/", "_")}_phi{i}.candidate.json'
            path.write_text(json.dumps(dict(planes=[rows(Fr(u['t']))[phis[i][X]] for X in range(len(links))],
                                            links={str(k): v for k, v in links.items()})) + '\n')
            rc = None
            if target:
                rc = subprocess.run([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(path),
                                     '--target', target], capture_output=True, text=True).returncode
            candidates.append(dict(file=path.name, verify_target=target, rc=rc))
    return dict(roots=[str(r) for r in rs], labellings=len(phis), aut_plus=aut, units=len(table) * len(phis),
                interval_constancy=constancy, embedded_units=sum(len(u['embedded']) for u in table),
                embedded_t=sorted({u['t'] for u in table if u['embedded']}, key=Fr), candidates=candidates,
                table=table), phis


def convex_links():
    """Map of {|x|, |y|, |z| <= 1, n . p <= 2}: vertices are the simple triple points inside, faces ordered CCW."""
    R = [[*n, -1] for n in CUBE] + [[*n, -2] for n in TET]
    verts = []
    for S in itertools.combinations(range(10), 3):
        M = [R[i][:3] for i in S]
        if _det3(M) == 0:
            continue
        p = _solve3(M, [-R[i][3] for i in S])
        tight = [i for i in range(10) if sum(R[i][k] * p[k] for k in range(3)) + R[i][3] == 0]
        if all(sum(R[i][k] * p[k] for k in range(3)) + R[i][3] <= 0 for i in range(10)) and p not in [v for v, _ in verts]:
            assert len(tight) == 3, 'convex control is not simple'
            verts.append((p, frozenset(tight)))
    links = {}
    for X in range(10):
        on = [(p, s) for p, s in verts if X in s]
        n = R[X][:3]
        u = [1, 0, 0] if abs(n[0]) != max(map(abs, n)) else [0, 1, 0]
        u = _cross(n, u)
        v = _cross(n, u)
        c = [sum(float(p[k]) for p, _ in on) / len(on) for k in range(3)]
        on.sort(key=lambda ps: math.atan2(sum((float(ps[0][k]) - c[k]) * v[k] for k in range(3)),
                                           sum((float(ps[0][k]) - c[k]) * u[k] for k in range(3))))
        links[X] = [next(iter((a & b) - {X})) for (_, a), (_, b) in zip(on, on[1:] + on[:1])]
    return links


def _solve3(M, b):
    d = Fr(_det3(M))
    out = []
    for c in range(3):
        Mc = [[b[r] if k == c else M[r][k] for k in range(3)] for r in range(3)]
        out.append(Fr(_det3(Mc)) / d)
    return tuple(out)


def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    report = dict(maps_sha256=hashlib.sha256(MAPS.read_bytes()).hexdigest(),
                  sources={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [Path(__file__), ROOT / 'code/ladder_exact.py', ROOT / 'code/omsat_sym.py']})
    # controls
    cl = convex_links()
    control, cphis = sweep(cl, out, 'control')
    inside = all(1 < abs(Fr(t)) < 3 for t in control['embedded_t'])
    at2 = [decide(cl, Fr(2), phi)['EMBEDDED'] for phi in cphis]
    atm2 = [decide(cl, Fr(-2), phi)['EMBEDDED'] for phi in cphis]
    neg_t = [decide(cl, Fr(t), phi)['EMBEDDED'] for t in (4, -4, Fr(1, 2)) for phi in cphis]
    rng = random.Random(261113)
    wrong = []
    while len(wrong) < 200:
        phi = tuple(rng.sample(range(10), 10))
        if phi not in cphis:
            wrong.append(decide(cl, Fr(2), phi)['EMBEDDED'])
    report['controls'] = dict(
        convex_links={str(k): v for k, v in cl.items()}, labellings=control['labellings'], aut_plus=control['aut_plus'],
        roots=control['roots'], embedded_t=control['embedded_t'], interval_constancy=control['interval_constancy'],
        positive_t2=sum(at2), positive_tm2=sum(atm2), negative_t4_tm4_thalf=sum(neg_t), negative_wrong_labelling=sum(wrong), wrong_tried=len(wrong))
    report['controls']['PASS'] = (bool(control['embedded_t']) and inside and any(at2) and any(atm2) and not any(neg_t)
                                  and not any(wrong) and control['interval_constancy'])
    for f in out.glob('control_*.candidate.json'):
        f.unlink()  # positive-control objects (convex, genus 0) are not candidates
    if not report['controls']['PASS']:
        (out / 'tetra.json').write_text(json.dumps(report, indent=1) + '\n')
        print('CONTROLS FAIL', json.dumps(report['controls']))
        return 1
    # Lutz #15
    rec = json.loads(MAPS.read_text())['maps'][14]
    assert rec['lutz'] == 15 and rec['aut_plus'] == 12
    links = dict(enumerate(rec['links']))
    result, phis = sweep(links, out, 'lutz15', target='S6')
    report['lutz15'] = dict(result, labellings_list=phis, canonical_sha256=rec['canonical_sha256'])
    report['wall_seconds'] = time.monotonic() - started
    (out / 'tetra.json').write_text(json.dumps(report, indent=1) + '\n')
    summary = {k: report['lutz15'][k] for k in ('roots', 'labellings', 'units', 'interval_constancy',
                                                 'embedded_units', 'embedded_t', 'candidates')}
    print('controls PASS', json.dumps({k: v for k, v in report['controls'].items() if k != 'convex_links'}))
    print('lutz15', json.dumps(summary))
    return 0 if result['interval_constancy'] else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
