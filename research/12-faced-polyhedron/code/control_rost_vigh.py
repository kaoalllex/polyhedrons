"""POSITIVE CONTROL from the literature: the Röst-Vígh eight-faced genus-3 polyhedron (arXiv:2609.32998,
Table 1): 8 planes, 24 vertices, 36 edges; 20 pairs of faces share one edge, 8 pairs two collinear edges.
Rebuilt from the published planes and face cycles only (vertices = intersections of the three face planes),
then checked with our exact verifier (code/ladder_exact.py, links with repetitions = doubled adjacencies)
and with the Gauss gate (code/gauss_gate.py; corners taken from the links, since the dual has doubled
edges): expected EMBEDDED, own degree chi/2 = -2, every face turning +1, own gauge admissible.
Usage: python3 -I control_rost_vigh.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gauss_gate as GG
from ladder_exact import verify

NAMES = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']
PLANES = [(3, -4, -2, 5), (-3, 4, -2, 5), (3, 4, 2, 5), (-3, -4, 2, 5),       # a x + b y + c z = rhs
          (-2, 5, -5, 3), (2, -5, -5, 3), (-2, -5, 5, 3), (2, 5, 5, 3)]
CYCLES = {'A1': [1, 2, 5, 7, 17, 13, 21, 12, 9], 'A2': [6, 8, 18, 14, 22, 11, 10, 2, 1],
          'A3': [7, 5, 19, 15, 23, 10, 11, 3, 4], 'A4': [4, 3, 8, 6, 20, 16, 24, 9, 12],
          'B1': [1, 9, 24, 23, 15, 14, 18, 20, 6], 'B2': [13, 17, 19, 5, 2, 10, 23, 24, 16],
          'B3': [21, 13, 16, 20, 18, 8, 3, 11, 22], 'B4': [4, 12, 21, 22, 14, 15, 19, 17, 7]}


def build():
    H = [[a, b, c, -r] for a, b, c, r in PLANES]
    idx = {nm: i for i, nm in enumerate(NAMES)}
    vf = {}
    for nm, cyc in CYCLES.items():
        for v in cyc:
            vf.setdefault(v, set()).add(idx[nm])
    assert len(vf) == 24 and all(len(s) == 3 for s in vf.values()), 'every vertex in exactly three faces'
    links = {}
    for nm, cyc in CYCLES.items():
        X = idx[nm]; m = len(cyc)
        # edge v_k -> v_{k+1} lies on X and on the other common face; corner i of `links` = vertex v_{i+1}
        links[X] = [(vf[cyc[k]] & vf[cyc[(k + 1) % m]] - {X}).pop() for k in range(m)]
    return H, links


def main():
    H, links = build()
    ex = verify(H, links, require_all_pairs=True)
    print('exact verifier:', {k: ex[k] for k in ('EMBEDDED', 'V_E_F_chi', 'all_pairs_adjacent', 'simple_faces',
                                                  'edges_consistent', 'bad_pairs')})
    mult = {}
    for X, L in links.items():
        for Y in L:
            mult[frozenset((X, Y))] = mult.get(frozenset((X, Y)), 0) + 1
    print('edge multiplicities (pairs):', sorted(v // 2 for v in mult.values()).count(1), 'single,',
          sorted(v // 2 for v in mult.values()).count(2), 'double')
    # oriented corner triangles from the links; coherent iff the three corners at every vertex agree cyclically
    corners = {}
    for X, L in links.items():
        for i in range(len(L)):
            corners.setdefault(frozenset((X, L[i], L[(i + 1) % len(L)])), []).append((X, L[i], L[(i + 1) % len(L)]))
    def rot(t):
        return min(t[i:] + t[:i] for i in range(3))
    coherent = all(len({rot(t) for t in ts}) == 1 for ts in corners.values())
    otris = [ts[0] for ts in corners.values()]
    V, E, F = ex['V_E_F_chi'][:3]
    target = (V - E + F) // 2
    N = GG.int_normals(H)
    eps = GG.own_gauge(H, links)
    deg = GG.degree(N, otris, eps)
    turn = GG.turning_numbers(H, links, eps)
    adm, _ = GG.admissible(N, otris, target, n_cover=256, eps=[eps], n_confirm=2000)
    print('corners coherent:', coherent, '| own degree', deg, 'target', target, '| turning', turn,
          '| own gauge admissible (2256 directions):', bool(adm), '| saddles', GG.saddles(N, otris, eps),
          '(need >= %d)' % (2 * (1 - target) + 1))


if __name__ == '__main__':
    main()
