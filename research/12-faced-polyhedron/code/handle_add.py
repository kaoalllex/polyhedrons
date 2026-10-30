"""'Frankenstein' handle attaching: from an embedded n-face polyhedron (solid-first result) take its
dual triangulation, list every way to attach a TUBE between two vertex-disjoint triangles abc, def
(remove both, add a 6-triangle annulus; new edges = 6 of the 9 cross pairs) such that all 6 new pairs
of faces are currently NOT adjacent (so adjacency grows by exactly 6 = one genus) and the result is an
orientable surface; then search each new map with the map-based engine (annealing + CMA-ES on the
honest pair energy) seeded from the current planes; every float zero is re-checked exactly.
Usage: python3 -I handle_add.py SOLID_JSON MINUTES_PER_CANDIDATE MAX_CANDIDATES SEED OUT_JSON"""
import json, sys, itertools, random
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from gauss_degree import coherent_triangles, links_from
from genus_ladder import search
from ladder_exact import verify


def annuli(t1, t2):
    """All 6-triangle annuli without interior vertices between triangles t1 and t2: walk around the
    annulus, each step advancing on cycle A (triangle a_i a_{i+1} b_j) or on cycle B (a_i b_j b_{j+1});
    3 steps of each kind, every alignment, both relative orientations."""
    a = list(t1); out = []
    for bb in (list(t2), list(t2)[::-1]):
        for j0 in range(3):
            b = bb[j0:] + bb[:j0]
            for steps in itertools.combinations(range(6), 3):        # positions of the A-steps
                i = j = 0; tri = []; cross = {frozenset((a[0], b[0]))}
                for k in range(6):
                    if k in steps:
                        tri.append((a[i % 3], a[(i + 1) % 3], b[j % 3])); i += 1
                    else:
                        tri.append((a[i % 3], b[j % 3], b[(j + 1) % 3])); j += 1
                    cross.add(frozenset((a[i % 3], b[j % 3])))
                out.append((tri, cross))
    return out


def candidates(tris, n):
    T = [tuple(sorted(t)) for t in tris]
    edges = {frozenset(e) for t in T for e in itertools.combinations(t, 2)}
    out = []; seen = set()
    for t1, t2 in itertools.combinations(T, 2):
        if set(t1) & set(t2):
            continue
        for tri, cross in annuli(t1, t2):
            if len(cross) != 6 or cross & edges:
                continue
            R = [t for t in T if t != t1 and t != t2] + [tuple(sorted(t)) for t in tri]
            key = frozenset(R)
            if key in seen:
                continue
            try:
                L = links_from(coherent_triangles(R), n)
            except AssertionError:
                continue
            seen.add(key)
            out.append((t1, t2, R, L))
    return out


if __name__ == '__main__':
    src, minutes, maxc, seed, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    r = json.load(open(src)); H = np.array(r['planes'], float); n = len(H)
    A = SF.Arrangement(H); S = {tuple(x) for x in r['solid']}
    tris = SF.extract_map(A, S)
    C = candidates(tris, n)
    print('%d triangles, %d handle candidates' % (len(tris), len(C)), flush=True)
    random.Random(seed).shuffle(C); rng = np.random.default_rng(seed); res = []
    for i, (t1, t2, R, L) in enumerate(C[:maxc]):
        (b, Hb), runs = search(L, n, minutes, rng, A.H.tolist())
        rec = {'tube': [list(t1), list(t2)], 'best': float(b), 'planes': Hb.tolist(), 'triangles': [list(t) for t in R]}
        if b < 0.5:
            ex = verify(Hb.tolist(), L, require_all_pairs=False); rec['exact'] = ex['EMBEDDED']
        print('candidate %d tube %s-%s: best %.3f %s' % (i, t1, t2, b, 'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
        res.append(rec); json.dump(res, open(out, 'w'))
        if rec.get('exact'):
            print('!!! genus +1 realized', flush=True)
            break


def reach(tris, n, target_edges=None, node_limit=20000):
    """Highest number of edges reachable from this triangulation by attaching tubes whose six new
    edges are all new (DFS with memo; stops early when all n(n-1)/2 pairs are reached). Returns
    (max_edges, exhausted_search)."""
    full = n * (n - 1) // 2 if target_edges is None else target_edges
    seen = set(); best = [0]; nodes = [0]
    def ne(T):
        return len({frozenset(e) for t in T for e in itertools.combinations(t, 2)})
    def dfs(T):
        key = frozenset(tuple(sorted(t)) for t in T)
        if key in seen or nodes[0] > node_limit:
            return
        seen.add(key); nodes[0] += 1
        e = ne(T); best[0] = max(best[0], e)
        if best[0] >= full:
            return
        for t1, t2, R, L in candidates(T, n):
            dfs(R)
            if best[0] >= full:
                return
    dfs([tuple(t) for t in tris])
    return best[0], nodes[0] <= node_limit
