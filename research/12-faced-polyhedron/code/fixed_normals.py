"""Exact search over plane offsets with the face normals fixed (experiment E1, Track 6 idea).

With the normals n_X fixed, chi(a,b,c,inf) = sign det3(n_a,n_b,n_c) is constant and every
other chirotope sign chi(a,b,c,d) is the sign of a LINEAR form in the offsets e (plane
n_X . x + e_X = 0). So "is there an embedded realization with these normals?" is an SMT problem
over linear real arithmetic: the Lemma 5.1 circuit of omsat.build (Grassmann-Pluecker clauses are
not needed: every offset vector gives a realizable chirotope) plus one linear atom per quadruple.
SAT gives explicit offsets, hence explicit planes; UNSAT proves that no offsets work for these
normals (exact, modulo z3 and the encoder).
"""
import itertools, sys, os
import numpy as np
import z3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omsat import CNF, build, Triangulation


def det3(a, b, c):
    """exact for integer input"""
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def integer_normals(normals, scale=10 ** 4):
    """Round unit-normalized normals to integers (exact arithmetic from here on)."""
    N = np.asarray(normals, dtype=float)
    N = N / np.linalg.norm(N, axis=1)[:, None]
    return [[int(round(x * scale)) for x in v] for v in N]


def build_instance(normals, tris, opts=None, margin=1, bound=10 ** 9):
    """normals: (n,3) INTEGER normals (see integer_normals). tris: triangles.
    All linear forms have exact integer coefficients. Offsets are bounded by |e| <= bound.
    Returns (solver, e_vars, cnf)."""
    n = len(normals)
    T = Triangulation(n, [tuple(t) for t in tris], None) if not isinstance(tris, Triangulation) else tris
    C = CNF(n)
    o = dict(gp=False, triples=True, reflex=True, poc=True, symbreak=False, mirror=False)
    if opts:
        o.update(opts)
    build(C, T, o)
    s = z3.Solver()
    B = [None] + [z3.Bool('b%d' % i) for i in range(1, C.nv + 1)]
    lit = lambda l: B[l] if l > 0 else z3.Not(B[-l])
    for cl in C.clauses:
        s.add(z3.Or([lit(l) for l in cl]) if len(cl) > 1 else lit(cl[0]))
    E = [z3.Real('e%d' % i) for i in range(n)]
    N = [[int(x) for x in v] for v in normals]
    for x in E:
        s.add(x <= bound, x >= -bound)
    for S, v in C.qvar.items():
        if S[-1] == n:                                   # contains infinity: constant
            d = det3(N[S[0]], N[S[1]], N[S[2]])
            if d == 0:
                raise ValueError('degenerate normals %s' % (S,))
            s.add(B[v] if d > 0 else z3.Not(B[v]))
        else:
            terms = []
            for i in range(4):
                rest = [N[S[j]] for j in range(4) if j != i]
                cof = (-1) ** (i + 3) * det3(*rest)
                terms.append(z3.IntVal(cof) * E[S[i]])
            L = z3.Sum(terms)
            s.add(z3.If(B[v], L >= margin, L <= -margin))
    return s, E, C


def solve(normals_int, tris, timeout_s=600, opts=None):
    """Returns (status, integer planes or None). SAT planes are integer 4-vectors (a,b,c,e)."""
    from fractions import Fraction
    from math import lcm
    s, E, C = build_instance(normals_int, tris, opts)
    s.set('timeout', int(timeout_s * 1000))
    r = s.check()
    if r == z3.sat:
        m = s.model()
        ef = [m.eval(x, model_completion=True).as_fraction() for x in E]
        L = 1
        for f in ef:
            L = lcm(L, f.denominator)
        planes = [[a * L, b * L, c * L, int(f * L)] for (a, b, c), f in zip(normals_int, ef)]
        return 'SAT', planes
    return ('UNSAT' if r == z3.unsat else 'UNKNOWN'), None


def exact_check(planes, tris):
    """Independent exact embedding check (Track 4 checker, planes.py)."""
    from planes import Arrangement, check_embedding
    res = check_embedding(Arrangement(planes), [tuple(t) for t in tris])
    return bool(res['ok_triples'] and res['ok_pairs']), len(res['viol_triples']), len(res['bad_pairs'])
