"""Validation of the sub-map extension of the OM predicates (omsat.Triangulation(submap=True)) and of
the exact fixed-normal offset solver on sub-maps (fixed_normals_gauge.solve_gauge).

  E. Eval backend on the exact chirotope of every saved realization (forbidden triples, at most one
     reflex corner per vertex, polygon-orientation consistency, Grassmann-Pluecker): no violation
     allowed; the GAUGE literal (RTURN xor REFLEX) must equal 0 on every corner in the own gauge.
     Negative control: the non-embedded genus-4 attempts must violate something.
  S. solve_gauge at the realization's own gauge normals (integer, scale 1e6): must be SAT, and the
     returned rational planes must pass ladder_exact.verify.
  U. soundness control (optional, --unsat): solve_gauge for the NEXT map M + tau (genus 4) at the
     genus-3 normals in the realized polyhedron's gauge, which has Gauss degree -2 != -3: must not be SAT.
Usage: python3 -I submap_validate.py OUT_JSON [--unsat] [--timeout S] FILES..."""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omsat import Triangulation, Eval, build, chirotope_from_planes
from gauss_degree import coherent_triangles, links_from
import gauss_gate as GG
from ladder_exact import verify


def eval_check(planes, tris, scale=10 ** 9):
    n = len(planes)
    ot = coherent_triangles([tuple(t) for t in tris])
    L = links_from(ot, n)
    eps = GG.own_gauge(planes, L)
    Hn = GG.unit_planes(planes)
    Hi = [[int(round(eps[X] * v * scale)) for v in Hn[X]] for X in range(n)]   # gauge-oriented planes
    chi = chirotope_from_planes(Hi)
    if any(v == 0 for v in chi.values()):
        return {'degenerate_chirotope': True}
    T = Triangulation(n, ot, L, submap=True)
    B = Eval(n, chi)
    P = build(B, T, dict(gp=True, triples=True, reflex=True, poc=True))
    gauge_bad = [(X, A, Bv) for X in range(n) for A, Bv in T.corners(X)
                 if B.xor([P.RTURN(X, A, Bv), P.REFLEX(X, A, Bv)])]
    viol = {}
    for v in B.violations:
        viol[v] = viol.get(v, 0) + 1
    return {'violations': viol, 'gauge_violations': len(gauge_bad), 'clauses': B.tags}


def main():
    args = sys.argv[1:]
    out = args.pop(0)
    unsat = '--unsat' in args
    timeout = 900
    if '--timeout' in args:
        i = args.index('--timeout'); timeout = float(args[i + 1]); del args[i:i + 2]
    files = [a for a in args if not a.startswith('--')]
    from fixed_normals_gauge import solve_gauge
    res = []
    for f in files:
        d = json.load(open(f))
        planes, tris = d['planes'], [tuple(t) for t in d['triangles']]
        n = len(planes)
        L = links_from(coherent_triangles(tris), n)
        emb = bool(verify(planes, L, require_all_pairs=False)['EMBEDDED'])
        rec = {'file': os.path.basename(f), 'embedded': emb, 'genus': GG.genus(tris, n)}
        rec['eval'] = eval_check(planes, tris)
        ok_e = (not rec['eval'].get('degenerate_chirotope') and not rec['eval']['violations']
                and rec['eval']['gauge_violations'] == 0)
        rec['eval_clean'] = ok_e
        print('%s genus %d embedded %s: Eval %s' % (rec['file'], rec['genus'], emb,
              'clean' if ok_e else rec['eval']), flush=True)
        if emb:
            ot = coherent_triangles(tris)
            eps = GG.own_gauge(planes, links_from(ot, n))
            N = GG.int_normals(planes)
            G = [[e * v for v in x] for e, x in zip(eps, N)]
            t0 = time.time()
            st, Hs = solve_gauge(G, tris, timeout_s=timeout)
            rec['solve_own'] = st; rec['solve_own_s'] = round(time.time() - t0, 1)
            if st == 'SAT':
                rec['solve_own_verified'] = bool(verify(Hs, links_from(ot, n), require_all_pairs=False)['EMBEDDED'])
            print('  solve_gauge at own normals: %s in %.1f s, exact verify %s' % (
                st, rec['solve_own_s'], rec.get('solve_own_verified')), flush=True)
            if unsat:
                rec['next'] = []
                for t1, t2, R in GG.arms_of(planes, tris, n):
                    oM, oR = GG.aligned_orientations(tris, R, n)
                    epsM = GG.own_gauge(planes, links_from(oM, n))
                    GM = [[e * v for v in x] for e, x in zip(epsM, N)]
                    D = GG.degree(N, oR, epsM)
                    t0 = time.time()
                    st2, H2 = solve_gauge(GM, R, timeout_s=timeout)
                    r2 = {'tube': [list(t1), list(t2)], 'degree': D, 'target': GG.euler_target(R, n), 'status': st2,
                          'seconds': round(time.time() - t0, 1)}
                    if st2 == 'SAT':
                        r2['verified'] = bool(verify(H2, links_from(oR, n), require_all_pairs=False)['EMBEDDED'])
                    rec['next'].append(r2)
                    print('  next map %s-%s (degree %d, target %d) at genus-3 normals: %s in %.1f s%s' % (
                        t1, t2, D, r2['target'], st2, r2['seconds'],
                        ' !!! SAT contradicts the degree theorem (verified %s)' % r2.get('verified') if st2 == 'SAT' else ''), flush=True)
        res.append(rec)
        json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
