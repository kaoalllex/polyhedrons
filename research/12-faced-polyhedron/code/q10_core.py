"""Q10: unsat cores (in forbidden triples) of the gauge-fixed offset SMT for admissible normals."""
import sys, json, time, numpy as np, itertools, z3
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from omsat import CNF, build, Triangulation
from gauss_degree import coherent_triangles, links_from
from gauss_search import find_admissible
from fixed_normals import det3, integer_normals
types = json.load(open(sys.argv[1])); tid = int(sys.argv[2]); seed = int(sys.argv[3])
tri = next(e for e in types if e['id'] == tid)['triangles']
ot = coherent_triangles(tri); T = Triangulation(12, ot, links_from(ot, 12))
G, _ = find_admissible(ot, np.random.default_rng(seed), minutes=2); G = integer_normals(G)
C = CNF(12); P = build(C, T, dict(gp=False, triples=False, reflex=True, poc=True))
for X in range(12):
    for A, B in T.corners(X):
        C.clause([-C.xor([P.RTURN(X, A, B), P.REFLEX(X, A, B)])], 'GAUGE')
trip = []
for X, Y, Z in T.nontriangles():
    trip.append(((X, Y, Z), [-P.IN(X, Y, Z), -P.IN(Y, Z, X), -P.IN(Z, X, Y)]))
z3.set_param('smt.core.minimize', True)
s = z3.Solver(); s.set('timeout', 600000)
Bv = [None] + [z3.Bool('b%d' % i) for i in range(1, C.nv + 1)]
lit = lambda l: Bv[l] if l > 0 else z3.Not(Bv[-l])
for cl in C.clauses:
    s.add(z3.Or([lit(l) for l in cl]) if len(cl) > 1 else lit(cl[0]))
E = [z3.Real('e%d' % i) for i in range(12)]
for x in E: s.add(x <= 10 ** 9, x >= -10 ** 9)
for S, v in C.qvar.items():
    if S[-1] == 12:
        s.add(Bv[v] if det3(G[S[0]], G[S[1]], G[S[2]]) > 0 else z3.Not(Bv[v]))
    else:
        terms = [z3.IntVal((-1) ** (i + 3) * det3(*[G[S[j]] for j in range(4) if j != i])) * E[S[i]] for i in range(4)]
        s.add(z3.If(Bv[v], z3.Sum(terms) >= 1, z3.Sum(terms) <= -1))
sel = []
for k, (t, cl) in enumerate(trip):
    a = z3.Bool('sel%d' % k); sel.append(a)
    s.add(z3.Implies(a, z3.Or([lit(l) for l in cl])))
t0 = time.time(); r = s.check(sel)
print('type', tid, 'result', r, '%.0fs' % (time.time() - t0))
if r == z3.unsat:
    core = [trip[int(str(c)[3:])][0] for c in s.unsat_core()]
    faces = sorted(set(x for t in core for x in t))
    print('core size', len(core), 'of', len(trip), 'faces involved', len(faces), core)
