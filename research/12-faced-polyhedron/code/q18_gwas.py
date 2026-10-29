"""Idea from genetics (genome-wide association studies): across all near-miss seeds of one type,
map every seed to a canonical labeling and ask whether the defects (vertices with >= 2 reflex
corners, i.e. where the immersion fails) sit at the SAME combinatorial positions (orbits of vertices
under the automorphism group). A position that fails in ~100% of seeds is a candidate local lemma.
Usage: SEEDS_JSON [MIN_SEEDS_PER_TYPE]"""
import json, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles, links_from
from local_viol import local_violations


def canon(tris):
    """Canonical relabeling by BFS from every flag (oriented triangle, both orientations).
    Returns (key, list of relabeling maps achieving the minimal key)."""
    ot = coherent_triangles(tris)
    succ = defaultdict(dict)
    for a, b, c in ot:
        succ[a][b] = c; succ[b][c] = a; succ[c][a] = b
    best, maps = None, []
    for a, b, c in ot:
        for flip in (False, True):
            start = (a, c, b) if flip else (a, b, c)
            lab = {}; order = []
            queue = [start]
            while queue:
                x, y, z = queue.pop(0)
                for v in (x, y, z):
                    if v not in lab:
                        lab[v] = len(lab)
                # rotate around x starting from y in the chosen orientation
                for u in (x, y, z):
                    pass
                for (p, q) in ((x, y), (y, z), (z, x)):
                    r = succ[q][p] if not flip else succ[p][q]
                    tri = (q, p, r)
                    key3 = frozenset(tri)
                    if key3 not in order:
                        order.append(key3); queue.append(tri)
            key = tuple(sorted(tuple(sorted(lab[v] for v in t)) for t in map(tuple, tris)))
            if best is None or key < best:
                best, maps = key, [dict(lab)]
            elif key == best:
                maps.append(dict(lab))
    return best, maps


if __name__ == '__main__':
    seeds = json.load(open(sys.argv[1])); mn = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    bytype = defaultdict(list)
    for s in seeds:
        bytype[s['our_id']].append(s)
    for tid, group in sorted(bytype.items(), key=lambda kv: -len(kv[1])):
        if len(group) < mn:
            continue
        key0 = None; freq = defaultdict(float); nseeds = 0; orbits = None
        for s in group:
            tris = json.loads(s['triangles']) if isinstance(s['triangles'], str) else s['triangles']
            key, maps = canon(tris)
            if key0 is None:
                key0 = key
                # automorphism orbits of canonical triangles: images of each canonical triangle under all min maps
                m0 = maps[0]; inv0 = {v: k for k, v in m0.items()}
                orb = {}
                for m in maps:
                    for t in tris:
                        ct0 = frozenset(m0[v] for v in t); ct = frozenset(m[v] for v in t)
                        orb.setdefault(ct0, set()).add(ct)
                # union-find into orbits
                orbits = {}
                for t, imgs in orb.items():
                    rep = min(tuple(sorted(x)) for x in imgs)
                    for x in imgs:
                        orbits[x] = min(orbits.get(x, rep), rep)
            if key != key0:
                continue
            H = np.array(s['planes'], float); L = links_from(coherent_triangles(tris), 12)
            try:
                _, _, refl = local_violations(H, L)
            except np.linalg.LinAlgError:
                continue
            nseeds += 1; m = maps[0]
            for t, r in refl.items():
                if r >= 2:
                    freq[orbits[frozenset(m[v] for v in t)]] += 1
        sizes = defaultdict(int)
        for x, rep in orbits.items():
            sizes[rep] += 1
        rows = sorted(((freq[rep] / (nseeds * sizes[rep]), rep, sizes[rep]) for rep in sizes), reverse=True)
        print('type %d: %d seeds, %d vertex orbits; multi-reflex rate per vertex in orbit: top %s ... bottom %s'
              % (tid, nseeds, len(sizes), [(round(f, 2), sz) for f, _, sz in rows[:5]],
                 [(round(f, 2), sz) for f, _, sz in rows[-3:]]), flush=True)
