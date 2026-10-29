"""C2 (half-turn) symmetric IMMERSION instance at OM level: uniform GP + SYM + orbit/mirror normalisation +
simple faces + <=1 reflex corner per vertex + polygon-orientation consistency; NO forbidden-triple clauses.
SAT => the asymmetric immersion instance of this map is SAT too (local route cannot refute this map)."""
import sys, time, threading
sys.path.insert(0, '/home/user/polyhedrons/research/12-faced-polyhedron/code')
import omsat_sym as S
from omsat import CNF, build, Triangulation
from pysat.solvers import Solver
mp, which, tmo = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
maps = S.parse_lutz(); otris = S.orient(maps[mp]); links, succ = S.links_from_oriented(otris)
T = Triangulation(12, otris, links); auts = S.automorphisms(otris); eps = dict(auts)
subs = [H for H in S.subgroups(auts) if S.classify(H) == 'C2']
classes = []
for H in sorted(subs, key=lambda H: sorted(H)):
    if not any(frozenset(S.compose(S.compose(a, h), tuple(sorted(range(12), key=lambda i: a[i]))) for h in H) == K
               for K in classes for a, _ in auts):
        classes.append(H)
print('map #%d |Aut|=%d C2 classes %d' % (mp, len(auts), len(classes)), flush=True)
H = classes[which]
C = CNF(12)
sym = [(g, eps[g]) for g in H if g != tuple(range(12))]
P = build(C, T, dict(gp=True, triples=False, reflex=True, poc=True, symbreak=False, mirror=False), sym=sym)
for X in (range(12) if 'nosimple' not in sys.argv else []):
    L = T.link[X]
    for i in range(11):
        for j in range(i + 2, 11):
            if i == 0 and j == 10: continue
            C.clause([-P.E(X, L[i], L[j]), -P.E(X, L[j], L[i])], 'SIMPLE')
basis, orbs = S.orbfix_quads(H)
for Sq in basis: C.clause([C.chi_pos_lit(Sq)], 'SB_ORBFLIP')
C.clause([C.chi_pos_lit((0, 1, 2, 3))], 'SB_MIRROR')
print('vars %d clauses %d' % (C.nv, len(C.clauses)), flush=True)
s = Solver(name='cadical195', bootstrap_with=C.clauses)
tm = threading.Timer(tmo, lambda: s.interrupt()); tm.start(); t0 = time.time()
r = s.solve_limited(expect_interrupt=True); tm.cancel()
print('RESULT map #%d C2 class %d %s: %s in %.1fs'
      % (mp, which, 'reflex+poc only (no simple, no triples)' if 'nosimple' in sys.argv else 'immersion(simple+reflex+poc, no triples)', {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[r], time.time() - t0), flush=True)
