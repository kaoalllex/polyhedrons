"""shared helpers for Track 4 scripts"""
import json, os, random, itertools
from itertools import combinations, permutations
from fractions import Fraction
from planes import *
import geomsat
from pysat.solvers import Solver

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
SCRATCH = "/tmp/claude-0/-home-user-polyhedrons/960178c5-7659-5869-80e8-5eb8e302e35d/scratchpad"

TORUS7 = sorted(tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)) + \
         sorted(tuple(sorted((i % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7))


def load_k12():
    return json.load(open(os.path.join(DATA, "k12_triangulations.json")))


def relabel(tris, perm):
    return sorted(tuple(sorted(perm[v] for v in t)) for t in tris)


def labelings_torus7():
    seen = set()
    for p in permutations(range(7)):
        seen.add(tuple(relabel(TORUS7, p)))
    return [list(t) for t in sorted(seen)]


def eval_IN_with_fixed_t(arr, tris, ray="min", rev=False, solver="glucose4"):
    """evaluate the encoded IN predicates for the fixed triangulation by solving the definitional CNF with the t
    variables fixed by assumptions.  returns {(X,(Y,Z)): bool}"""
    enc = geomsat.GeomEncoding(arr, hard_triples=False, ray=ray, rev=rev)
    tset = set(tuple(sorted(t)) for t in tris)
    assum = [v if T in tset else -v for T, v in enc.tv.items()]
    S = Solver(name=solver, bootstrap_with=enc.clauses)
    ok = S.solve(assumptions=assum)
    assert ok, "definitional CNF + valid triangulation unsat?!"
    m = S.get_model()
    val = {abs(l): (l > 0) for l in m}
    S.delete()

    def lv(l):
        return val[abs(l)] if l > 0 else not val[abs(l)]

    out = {}
    for (x, y, z), lit in enc.IN.items():
        out[(x, (y, z))] = lv(lit)
    viol = {T: lv(v) for T, v in enc.viol.items()}
    return out, viol
