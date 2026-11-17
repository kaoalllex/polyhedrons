"""P4 (E-261117-03): coherent patchwork chirotopes in a weight box [0, K].

Elements as in omsat: rows 0..F-1 are planes, row F = INF; chi(S) = sign det of the four rows of S (S sorted).
A patchwork matrix is H (n x 4), H_ij = s_ij t^(w_ij), integer w_ij in [0, K]. If every 4 x 4 minor has a unique
minimum-weight matching pi, the minor's sign for small t is sgn(pi) prod s_(a, pi(a)); at t = 1/q, q >= 24, the other
at most 23 terms sum to less than the leading one (review dialogue-2026-11-16-strategy, Appendix A2).

Certificate per 4-subset (CP-SAT): one matching selector per permutation (exactly one), x_aj the induced permutation
matrix, potentials u_a + v_j = 4 w_aj on the matching and <= 4 w_aj - 1 off it, u_0 = 0, |u|, |v| <= 4 (4K + 1).
Sound: another matching has at least two off edges, so its scaled weight exceeds the selected one. Complete
(PROVED-1): a unique minimum gives every alternating cycle a weight gap >= 1, at most four off edges, so 4 * gap
covers the -1 margins; shortest-path potentials from u_0 stay within 3 (4K + 1) for u and 4K + 3 (4K + 1) for v.
C0 tests both directions against brute force on all 24 costs.

Normalisation (search only, lossless): every row and every column has a zero weight (subtract row minima, then
column minima; both stay in the box and leave every minor's argmin and sign unchanged). All sign bits stay free,
plus one global sign eps (redundant with a column flip; kept as registered).

Usage: p4.py c0 OUT | p4.py c1 OUT | p4.py c2 OUT | p4.py all OUT
"""
import hashlib
import itertools
import json
import multiprocessing as mp
import os
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path
import platform
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'verification'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder'))

from ortools.sat.python import cp_model  # noqa: E402
from omsat import CNF, build, chirotope_from_planes, det4, perm_parity  # noqa: E402

PERMS = list(itertools.permutations(range(4)))
K_LADDER = (2, 4, 8, 16, 32)
C1_CAP = float(os.environ.get('P4_C1_CAP', '12'))
C2_CAP = float(os.environ.get('P4_C2_CAP', '120'))
SZ = ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/results/pilot/szilassi.input.json'
K13 = ROOT / 'reviews/dialogue-2026-11-16-strategy-checks/d2_rate.json'
K13_SHA = 'b7b5ff8438acf7ea1e7526c936604abd3407013f67ebb1cab6b797e0f7f8aafa'
S6_CONTROLS = ROOT / 'witnesses/s6_10_2_controls'


# ----------------------------------------------------------------------------- CP-SAT model

class P4:
    """Patchwork variables on n rows and the per-minor certificate."""

    def __init__(self, model, n, K, normalise=True, fixed_w=None):
        self.m, self.n, self.K = model, n, K
        self.B = 4 * (4 * K + 1)
        if fixed_w is not None:
            self.w = [[model.NewConstant(int(x)) for x in row] for row in fixed_w]
        else:
            self.w = [[model.NewIntVar(0, K, 'w%d_%d' % (i, j)) for j in range(4)] for i in range(n)]
        self.sig = [[model.NewBoolVar('s%d_%d' % (i, j)) for j in range(4)] for i in range(n)]
        self.eps = model.NewBoolVar('eps')
        self.true = model.NewConstant(1)
        self.sel = {}
        if normalise and fixed_w is None:
            for cells in ([(i, j) for j in range(4)] for i in range(n)):
                self._has_zero(cells)
            for cells in ([(i, j) for i in range(n)] for j in range(4)):
                self._has_zero(cells)

    def _has_zero(self, cells):
        zs = []
        for i, j in cells:
            z = self.m.NewBoolVar('')
            self.m.Add(self.w[i][j] == 0).OnlyEnforceIf(z)
            zs.append(z)
        self.m.AddBoolOr(zs)

    def minor(self, S, neg=None):
        """Certificate for rows S (sorted). neg: None (no sign), 0/1 constant or a literal TRUE iff chi(S) = -1."""
        m = self.m
        z = [m.NewBoolVar('') for _ in PERMS]
        m.AddExactlyOne(z)
        self.sel[S] = z
        u = [m.NewIntVar(-self.B, self.B, '') for _ in range(4)]
        v = [m.NewIntVar(-self.B, self.B, '') for _ in range(4)]
        m.Add(u[0] == 0)
        for a in range(4):
            for j in range(4):
                x = m.NewBoolVar('')
                m.Add(x == sum(z[p] for p, pi in enumerate(PERMS) if pi[a] == j))
                w4 = 4 * self.w[S[a]][j]
                m.Add(u[a] + v[j] == w4).OnlyEnforceIf(x)
                m.Add(u[a] + v[j] <= w4 - 1).OnlyEnforceIf(x.Not())
        if neg is None:
            return z
        for p, pi in enumerate(PERMS):
            lits = [self.sig[S[a]][pi[a]] for a in range(4)] + [self.eps]
            if isinstance(neg, int):
                odd = neg ^ perm_parity(pi)
            else:
                lits.append(neg)
                odd = perm_parity(pi)
            # parity(sig on the matching) + eps + neg + parity(pi) = 0 (mod 2)
            m.AddBoolXOr(lits if odd else lits + [self.true]).OnlyEnforceIf(z[p])
        return z

    def values(self, solver):
        w = [[solver.Value(x) for x in row] for row in self.w]
        s = [[-1 if solver.Value(x) else 1 for x in row] for row in self.sig]
        return w, s, -1 if solver.Value(self.eps) else 1


def solve(model, cap, workers=1, seed=0):
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = cap
    sv.parameters.num_workers = workers
    sv.parameters.random_seed = seed
    t0 = time.monotonic()
    st = sv.Solve(model)
    return sv, sv.StatusName(st), time.monotonic() - t0


# ----------------------------------------------------------------------------- independent exact side (no CP-SAT)

def brute(W, rows):
    """Sorted (weight, perm) of the 24 matchings of the minor on rows."""
    return sorted((sum(W[rows[a]][pi[a]] for a in range(4)), pi) for pi in PERMS)


def leading_chi(W, Sg):
    """Combinatorial chirotope of a patchwork matrix, or None if some minor's minimum is tied."""
    n = len(W)
    chi = {}
    for S in itertools.combinations(range(n), 4):
        c = brute(W, S)
        if c[0][0] == c[1][0]:
            return None
        pi = c[0][1]
        sgn = -1 if perm_parity(pi) else 1
        for a in range(4):
            sgn *= Sg[S[a]][pi[a]]
        chi[S] = sgn
    return chi


def exact_matrix(W, Sg, q):
    """Integer matrix q^K H(1/q) = s_ij q^(K - w_ij)."""
    K = max(max(r) for r in W)
    return [[Sg[i][j] * q ** (K - W[i][j]) for j in range(4)] for i in range(len(W))]


def exact_chi(H):
    return {S: (lambda d: (d > 0) - (d < 0))(det4([H[i] for i in S])) for S in itertools.combinations(range(len(H)), 4)}


def chart(H):
    """Planes h_i A with h_INF A = (0, 0, 0, 1), det A > 0, rows scaled to primitive integers (positive factors)."""
    inf = [Fraction(x) for x in H[-1]]
    for drop in range(4):
        basis = [[Fraction(int(k == e)) for k in range(4)] for e in range(4) if e != drop]
        B = basis + [inf]
        d = det4(B)
        if d != 0:
            break
    if d < 0:
        B[0] = [-x for x in B[0]]
    A = invert(B)
    out = []
    for h in H[:-1]:
        r = [sum(Fraction(h[k]) * A[k][j] for k in range(4)) for j in range(4)]
        den = lcm(*[x.denominator for x in r])
        r = [int(x * den) for x in r]
        g = gcd(*r)
        out.append([x // g for x in r])
    assert [sum(inf[k] * A[k][j] for k in range(4)) for j in range(4)] == [0, 0, 0, 1]
    return out


def invert(M):
    n = len(M)
    a = [list(map(Fraction, row)) + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        a[c] = [x / a[c][c] for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def realize(W, Sg, eps, target, links=None, target_check=None):
    """Exact end-to-end check of a model: combinatorial chi, exact chi at the smallest working q <= 25, chart, and
    the standard verifier when links are given. target: chi on rows (INF last)."""
    from verify_candidate import _verify, passes
    rec = dict(w=W, s=Sg, eps=eps)
    comb = leading_chi(W, Sg)
    rec['unique_minima'] = comb is not None
    rec['combinatorial_match'] = comb is not None and all(comb[S] * eps == target[S] for S in target)
    for q in range(2, 26):
        H = exact_matrix(W, Sg, q)
        if all(v * eps == target[S] for S, v in exact_chi(H).items()):
            break
    else:
        rec['q'] = None
        return rec
    rec['q'] = q
    planes = chart(H)
    rec['planes'] = planes
    rec['charted_chi_match'] = all(chirotope_from_planes(planes)[S] * eps == target[S] for S in target)
    if links is not None:
        rep = _verify(dict(planes=planes, links={str(k): v for k, v in links.items()}))
        rec['verify'] = dict(EMBEDDED=bool(rep.get('EMBEDDED')), V_E_F_chi=list(rep.get('V_E_F_chi', [])),
                             all_pairs_adjacent=bool(rep.get('all_pairs_adjacent')))
        rec['target_check'] = target_check
        rec['PASS'] = bool(passes(rep, target_check))
    return rec


# ----------------------------------------------------------------------------- C0

def c0_case(W):
    """Certificate on one fixed 4 x 4 matrix vs brute force: returns (expected perm or None, agree, detail)."""
    c = brute(W, (0, 1, 2, 3))
    want = c[0][1] if c[0][0] != c[1][0] else None
    K = max(max(r) for r in W)
    m = cp_model.CpModel()
    P = P4(m, 4, max(K, 1), normalise=False, fixed_w=W)
    z = P.minor((0, 1, 2, 3))
    sv, st, _ = solve(m, 30)
    if st == 'INFEASIBLE':
        return want, want is None, 'infeasible'
    if st not in ('OPTIMAL', 'FEASIBLE'):
        return want, False, st
    got = PERMS[[sv.Value(x) for x in z].index(1)]
    if got != want:
        return want, False, 'selected %s' % (got,)
    m.Add(z[PERMS.index(got)] == 0)
    sv, st, _ = solve(m, 30)
    return want, st == 'INFEASIBLE', 'second ' + st


def c0_chunk(args):
    kind, K, seed, count = args
    rng = random.Random(seed)
    rows = []
    if kind == 'exhaustive':
        mats = (list(map(list, zip(*[iter(bits)] * 4))) for bits in itertools.product(range(K + 1), repeat=16))
        mats = itertools.islice(mats, seed, None, count)        # stride: chunk seed of count chunks
    elif kind == 'random':
        mats = ([[rng.randint(0, K) for _ in range(4)] for _ in range(4)] for _ in range(count))
    else:                                                       # planted ties: two matchings forced equal
        def tied_matrix():
            while True:
                W = [[rng.randint(0, K) for _ in range(4)] for _ in range(4)]
                c = brute(W, (0, 1, 2, 3))
                if c[0][0] == c[1][0]:
                    return W
        mats = (tied_matrix() for _ in range(count))
    unique = tied = bad = 0
    examples = []
    for W in mats:
        want, ok, detail = c0_case(W)
        unique += want is not None
        tied += want is None
        if not ok:
            bad += 1
            examples.append(dict(W=W, detail=detail))
    return dict(kind=kind, K=K, seed=seed, unique=unique, tied=tied, bad=bad, examples=examples[:5])


def c0(out, workers):
    t0 = time.monotonic()
    jobs = [('exhaustive', 1, i, 64) for i in range(64)]
    jobs += [('random', K, 26111703 + 100 * K + i, 250) for K in (2, 3, 8) for i in range(8)]
    jobs += [('tied', K, 26111704 + 100 * K + i, 125) for K in (2, 3, 8) for i in range(8)]
    with mp.Pool(workers) as pool:
        rows = pool.map(c0_chunk, jobs, chunksize=1)
    embedded = [[0, 0, 9, 9], [0, 1, 9, 9], [9, 9, 0, 9], [9, 9, 9, 0]]   # the [[0, 0], [0, 1]] case
    e_want, e_ok, e_detail = c0_case(embedded)
    rep = dict(rows=rows, embedded=dict(W=embedded, want=e_want, ok=e_ok, detail=e_detail),
               unique=sum(r['unique'] for r in rows), tied=sum(r['tied'] for r in rows),
               bad=sum(r['bad'] for r in rows), seconds=time.monotonic() - t0)
    rep['PASS'] = bool(rep['bad'] == 0 and e_ok and e_want is not None and rep['unique'] > 0 and rep['tied'] > 0)
    dump(out / 'c0.json', rep)
    return rep


# ----------------------------------------------------------------------------- C1

def c1_controls():
    """(name, planes, links or None, verifier target) of the registered controls; INF is appended by omsat."""
    sz = json.loads(SZ.read_text())
    import importlib.util
    spec = importlib.util.spec_from_file_location('pilot05', ROOT / 'experiments/E-261103-05-s5-symmetric-solid-first/pilot.py')
    p05 = importlib.util.module_from_spec(spec); sys.modules['pilot05'] = p05; spec.loader.exec_module(p05)
    out = [('szilassi_perturbed', sz['planes'], sz['links'], 'S5')]
    out += [(name, h, links, 'all-pairs') for name, h, links in p05.fixtures()]
    assert sha(K13) == K13_SHA, 'K13 archive hash changed'
    out += [('k13_%d' % r['seed'], r['planes'], None, None) for r in json.loads(K13.read_text())['rows']
            if r['status'] == 'OPTIMAL']
    for p in sorted(S6_CONTROLS.glob('**/*.json')):
        d = json.loads(p.read_text())
        out.append(('s6_' + p.stem[len('s6_10_2_'):], d['planes'], d['links'], 'S6'))
    return out


def planted(seed, n=8):
    """Tropical Vandermonde w_ij = a_i b_j (a, b random permutations of 0..n-1 and 0..3) with random signs: every
    minimum is unique by the strict rearrangement inequality, K = 3 (n - 1) (C1 positive control)."""
    rng = random.Random(seed)
    a, b = rng.sample(range(n), n), rng.sample(range(4), 4)
    W = [[a[i] * b[j] for j in range(4)] for i in range(n)]
    Sg = [[rng.choice((1, -1)) for _ in range(4)] for _ in range(n)]
    chi = leading_chi(W, Sg)
    assert chi is not None
    return W, Sg, chi


def capacity_unit(args):
    """Does the box hold any n x 4 matrix with every minimum unique (no signs)? Calibrates C1's negatives."""
    n, K, cap = args
    m = cp_model.CpModel()
    P = P4(m, n, K)
    for S in itertools.combinations(range(n), 4):
        P.minor(S)
    sv, st, sec = solve(m, cap)
    rec = dict(n=n, K=K, status=st, seconds=round(sec, 3))
    if st in ('OPTIMAL', 'FEASIBLE'):
        W = P.values(sv)[0]
        rec['W'] = W
        rec['brute_unique'] = leading_chi(W, [[1] * 4 for _ in W]) is not None
    return rec


def flipped(chi):
    """chi with the first sign whose flip violates three-term Grassmann-Pluecker (C1 negative control)."""
    n = 1 + max(max(S) for S in chi)
    for S in sorted(chi):
        bad = dict(chi)
        bad[S] = -bad[S]
        if not gp_ok(bad, n):
            return S, bad
    raise AssertionError('no GP-breaking flip')


def gp_ok(chi, n):
    def c(t):
        return (-1 if perm_parity(t) else 1) * chi[tuple(sorted(t))]
    for a, b in itertools.combinations(range(n), 2):
        rest = [e for e in range(n) if e not in (a, b)]
        for p, q, r, s in itertools.combinations(rest, 4):
            t1 = c((a, b, p, q)) * c((a, b, r, s))
            t2 = -c((a, b, p, r)) * c((a, b, q, s))
            t3 = c((a, b, p, s)) * c((a, b, q, r))
            if t1 == t2 == t3:
                return False
    return True


def c1_unit(args):
    name, chi, links, target_check, ks, cap = args
    n = 1 + max(max(S) for S in chi)
    rec = dict(name=name, n=n, ladder=[])
    for K in ks:
        m = cp_model.CpModel()
        P = P4(m, n, K)
        for S in itertools.combinations(range(n), 4):
            P.minor(S, int(chi[S] < 0))
        sv, st, sec = solve(m, cap)
        step = dict(K=K, status=st, seconds=round(sec, 3))
        rec['ladder'].append(step)
        if st in ('OPTIMAL', 'FEASIBLE'):
            w, s, eps = P.values(sv)
            step['realize'] = realize(w, s, eps, chi, links, target_check)
            break
    return rec


def c1(out, workers):
    t0 = time.monotonic()
    units = []
    for name, planes, links, tc in c1_controls():
        chi = chirotope_from_planes(planes)
        assert all(chi.values()), name + ' not uniform'
        units.append((name, chi, {int(k): v for k, v in links.items()} if isinstance(links, dict) else
                      (dict(enumerate(links)) if links is not None else None), tc, K_LADDER, C1_CAP))
    planted_rows = {}
    for n in (8, 11):
        pw, ps, pchi = planted(26111705 + n, n)
        planted_rows['planted_positive_n%d' % n] = dict(W=pw, s=ps, K=max(map(max, pw)))
        units.append(('planted_positive_n%d' % n, pchi, None, None, K_LADDER, C1_CAP))
    cap_units = [(n, K, C1_CAP) for n in (8, 9, 11) for K in K_LADDER]
    sz_chi = chirotope_from_planes(json.loads(SZ.read_text())['planes'])
    fS, fchi = flipped(sz_chi)
    units.append(('negative_szilassi_gp_flip', fchi, None, None, K_LADDER, C1_CAP))
    with mp.Pool(workers) as pool:
        capacity = pool.map(capacity_unit, cap_units, chunksize=1)
        rows = pool.map(c1_unit, units, chunksize=1)
    by = {r['name']: r for r in rows}
    known = [r for r in rows if not r['name'].startswith(('planted', 'negative'))]

    def hit(r):
        last = r['ladder'][-1]
        return last['status'] in ('OPTIMAL', 'FEASIBLE') and last['K']

    def sound(r):
        rz = r['ladder'][-1].get('realize')
        return rz is None or (rz['unique_minima'] and rz['combinatorial_match'] and rz['q'] is not None
                              and rz['charted_chi_match'] and rz.get('PASS', True))
    coverage = {K: sum(1 for r in known if hit(r) and hit(r) <= K) for K in K_LADDER}
    neg = by['negative_szilassi_gp_flip']
    rep = dict(rows=rows, coverage_per_K=coverage, controls=len(known), flipped_quad=list(fS),
               planted=planted_rows, capacity=capacity, seconds=time.monotonic() - t0)
    rep['checks'] = dict(planted_found=all(hit(by[k]) for k in planted_rows),
                         capacity_models_exact=all(r.get('brute_unique', True) for r in capacity),
                         negative_not_sat=not hit(neg), every_model_exact=all(sound(r) for r in rows))
    rep['PASS'] = all(rep['checks'].values())
    dump(out / 'c1.json', rep)
    return rep


# ----------------------------------------------------------------------------- C2

def c2_unit(args):
    K, cap = args
    from test_encoder import from_links
    from omsat_validate import ALL_OPTS
    sz = json.loads(SZ.read_text())
    T = from_links(sz['links'])
    c = CNF(T.n)
    build(c, T, ALL_OPTS)
    m = cp_model.CpModel()
    x = [None] + [m.NewBoolVar('c%d' % i) for i in range(1, c.nv + 1)]
    lit = lambda l: x[l] if l > 0 else x[-l].Not()
    for cl in c.clauses:
        m.AddBoolOr([lit(l) for l in cl])
    n = T.n + 1
    P = P4(m, n, K)
    for S in itertools.combinations(range(n), 4):
        P.minor(S, x[c.qvar[S]])
    sv, st, sec = solve(m, cap)
    rec = dict(K=K, status=st, seconds=round(sec, 3), cnf_vars=c.nv, cnf_clauses=len(c.clauses))
    if st in ('OPTIMAL', 'FEASIBLE'):
        chi = {S: -1 if sv.Value(x[v]) else 1 for S, v in c.qvar.items()}
        w, s, eps = P.values(sv)
        links = {int(k): v for k, v in sz['links'].items()} if isinstance(sz['links'], dict) else dict(enumerate(sz['links']))
        rec['realize'] = realize(w, s, eps, chi, links, 'S5')
    return rec


def c2(out, workers, c1_rep=None):
    t0 = time.monotonic()
    with mp.Pool(min(workers, len(K_LADDER))) as pool:
        rows = pool.map(c2_unit, [(K, C2_CAP) for K in K_LADDER], chunksize=1)
    rep = dict(rows=rows, seconds=time.monotonic() - t0)
    sz_k = None
    if c1_rep:
        r = next(r for r in c1_rep['rows'] if r['name'] == 'szilassi_perturbed')
        last = r['ladder'][-1]
        sz_k = last['K'] if last['status'] in ('OPTIMAL', 'FEASIBLE') else None
    rep['szilassi_c1_K'] = sz_k
    contradiction = [r['K'] for r in rows if r['status'] == 'INFEASIBLE' and sz_k is not None and r['K'] >= sz_k]
    bad_model = [r['K'] for r in rows if 'realize' in r and not (r['realize']['combinatorial_match']
                 and r['realize']['charted_chi_match'] and r['realize'].get('PASS'))]
    rep['checks'] = dict(no_contradiction_with_c1=not contradiction, every_model_realized_s5=not bad_model)
    rep['PASS'] = all(rep['checks'].values())
    dump(out / 'c2.json', rep)
    return rep


# ----------------------------------------------------------------------------- driver

def dump(path, value):
    path.write_text(json.dumps(value, indent=1, default=str) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def manifest(out, t0):
    git = lambda *a: subprocess.check_output(['git', '-C', str(ROOT), *a], text=True).strip()
    dump(out / 'manifest.json', dict(commit=git('rev-parse', 'HEAD'), dirty=git('status', '--porcelain'),
                                     python=sys.version, host=platform.platform(),
                                     ortools=__import__('ortools').__version__, wall_seconds=time.monotonic() - t0,
                                     caps=dict(c1=C1_CAP, c2=C2_CAP), K_ladder=K_LADDER,
                                     sources_sha256={str(p.relative_to(ROOT)): sha(p)
                                                     for p in (Path(__file__).resolve(), SZ, K13)}))


def main():
    stage, out = sys.argv[1], Path(sys.argv[2])
    workers = int(os.environ.get('WORKERS', '8'))
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic()
    summary = {}
    if stage in ('c0', 'all'):
        summary['C0'] = c0(out, workers)['PASS']
    c1_rep = None
    if stage in ('c1', 'all'):
        c1_rep = c1(out, workers)
        summary['C1'] = c1_rep['PASS']
        summary['C1_coverage'] = c1_rep['coverage_per_K']
    if stage in ('c2', 'all'):
        summary['C2'] = c2(out, workers, c1_rep)['PASS']
    manifest(out, t0)
    dump(out / 'summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
