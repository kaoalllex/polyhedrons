"""Fixed-normals SMT (fixed_normals.py) with the polygon orientation gauge imposed.

The normals g_X are given WITH signs (gauge normals: each face polygon, traversed in the coherent
link order, must be counter-clockwise about g_X). This is imposed as RTURN xor REFLEX = 0 at
every corner (omsat F6 literals: convex corners turn left, reflex corners right, seen from g_X).
Use with normals that pass the Gauss-degree prefilter (gauss_degree.py / gauss_search.py).
Works for sub-maps too (some pairs of faces not adjacent, e.g. a genus-ladder level; omsat.Triangulation
with submap=True): the gauge normals then need degree 1 - g, not -5 (gauss_gate.py).
"""
import os
import sys

import z3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omsat import CNF, build, Triangulation, Predicates
from gauss_degree import coherent_triangles, links_from
from fixed_normals import det3


def solve_gauge(G, tris, timeout_s=600, margin=1, bound=10 ** 9, orient_sign=0):
    """G: integer gauge normals. orient_sign: required value of RTURN xor REFLEX (0 = ccw)."""
    from fractions import Fraction
    from math import lcm
    n = len(G)
    ot = coherent_triangles(tris)
    T = Triangulation(n, ot, links_from(ot, n), submap=True)
    C = CNF(n)
    P = build(C, T, dict(gp=False, triples=True, reflex=True, poc=True))
    for X in range(n):
        for A, B in T.corners(X):
            w = C.xor([P.RTURN(X, A, B), P.REFLEX(X, A, B)])
            C.clause([w if orient_sign else -w], 'GAUGE')
    s = z3.Solver()
    s.set('timeout', int(timeout_s * 1000))
    Bv = [None] + [z3.Bool('b%d' % i) for i in range(1, C.nv + 1)]
    lit = lambda l: Bv[l] if l > 0 else z3.Not(Bv[-l])
    for cl in C.clauses:
        s.add(z3.Or([lit(l) for l in cl]) if len(cl) > 1 else lit(cl[0]))
    E = [z3.Real('e%d' % i) for i in range(n)]
    for x in E:
        s.add(x <= bound, x >= -bound)
    for S, v in C.qvar.items():
        if S[-1] == n:
            d = det3(G[S[0]], G[S[1]], G[S[2]])
            if d == 0:
                raise ValueError('degenerate normals')
            s.add(Bv[v] if d > 0 else z3.Not(Bv[v]))
        else:
            terms = []
            for i in range(4):
                rest = [G[S[j]] for j in range(4) if j != i]
                terms.append(z3.IntVal((-1) ** (i + 3) * det3(*rest)) * E[S[i]])
            s.add(z3.If(Bv[v], z3.Sum(terms) >= margin, z3.Sum(terms) <= -margin))
    r = s.check()
    if r == z3.sat:
        m = s.model()
        ef = [m.eval(x, model_completion=True).as_fraction() for x in E]
        L = 1
        for f in ef:
            L = lcm(L, f.denominator)
        return 'SAT', [[a * L, b * L, c * L, int(f * L)] for (a, b, c), f in zip(G, ef)]
    return ('UNSAT' if r == z3.unsat else 'UNKNOWN'), None
