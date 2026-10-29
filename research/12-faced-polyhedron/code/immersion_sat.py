"""Q12: does a type admit a polyhedral IMMERSION with planar faces (OM level)?
Clauses: uniform rank-4 GP, every face polygon simple (no two non-adjacent edges cross),
at most one reflex corner per vertex (= vertex stars embedded), polygon-orientation consistency,
optional Gauss degree/cover (implied by immersion via Hopf). No global embedding clauses.
SAT -> candidate immersion chirotope (to be realized); UNSAT -> no immersion -> no embedding.
Usage: python3 -I immersion_sat.py TYPES_JSON TYPE_ID GAUSS_K OUT_PREFIX"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from omsat import CNF, build, Triangulation
from omsat_gauss import add_gauss
from gauss_degree import coherent_triangles, links_from
from pysat.solvers import Solver
types = json.load(open(sys.argv[1])); tid = int(sys.argv[2]); k = int(sys.argv[3]); out = sys.argv[4]
tri = next(e for e in types if e['id'] == tid)['triangles']
ot = coherent_triangles(tri); T = Triangulation(12, ot, links_from(ot, 12))
C = CNF(12)
P = build(C, T, dict(gp=True, triples=False, reflex=True, poc=True, symbreak=True, mirror=True))
ns = 0
for X in range(12):
    L = T.link[X]
    for i in range(11):
        for j in range(i + 2, 11):
            if i == 0 and j == 10:
                continue
            W1, W2 = L[i], L[j]
            C.clause([-P.E(X, W1, W2), -P.E(X, W2, W1)], 'SIMPLE'); ns += 1
if k:
    add_gauss(C, P, T, k=k)
print('type', tid, 'gauss k', k, 'vars', C.nv, 'clauses', len(C.clauses), 'simplicity clauses', ns, flush=True)
t0 = time.time()
with Solver(name='cadical195', bootstrap_with=C.clauses) as s:
    r = s.solve()
    print('RESULT', 'SAT' if r else 'UNSAT', '%.1fs' % (time.time() - t0), flush=True)
    if r:
        m = set(l for l in s.get_model() if l > 0)
        chi = {''.join('%x' % e for e in S): (1 if v in m else -1) for S, v in C.qvar.items()}
        json.dump({'type': tid, 'chi': chi}, open(out + '_chi.json', 'w'))
