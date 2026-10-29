"""'Beauty' = robustness / shape quality of a face-plane configuration (user's idea, 2026-10-29).
All measures are dimensionless (divided by the diameter D of the vertex set):
  margin   = min distance of a triple point P_abc from a fourth plane w (all a, b, c, w), / D:
             how far the configuration is from a degenerate one (4 planes through a point). The
             realization space is open, so a true solution can be moved to have a positive margin;
             tiny margins are where float exploits and 'spiky' shapes live;
  edge     = shortest polygon edge / D;
  fat      = min over faces of the isoperimetric quotient 4 pi |area| / perimeter^2 (1 = disk);
  beauty   = geometric mean of margin, edge, fat (a single number to rank or to cut).
Usage: python3 -I beauty.py RESULTS_JSON [...]   (entries with 'planes' and 'links' or 'triangles')"""
import json, sys
from itertools import combinations
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])


def polygons(H, links):
    P = {}
    for X, L in links.items():
        m = len(L)
        P[X] = np.array([np.linalg.solve(H[[X, L[i], L[(i + 1) % m]], :3], -H[[X, L[i], L[(i + 1) % m]], 3]) for i in range(m)])
    return P


def beauty(H, links):
    H = np.asarray(H, float); n = len(H)
    H = H / np.linalg.norm(H[:, :3], axis=1)[:, None]
    P = polygons(H, links)
    V = np.vstack(list(P.values())); D = np.linalg.norm(V.max(0) - V.min(0))
    margin = min(abs(H[w, :3] @ np.linalg.solve(H[[a, b, c], :3], -H[[a, b, c], 3]) + H[w, 3])
                 for a, b, c in combinations(range(n), 3) for w in range(n) if w not in (a, b, c)) / D
    edge = min(np.linalg.norm(q - np.roll(q, 1, axis=0), axis=1).min() for q in P.values()) / D
    fat = 1.0
    for X, q in P.items():
        nx = H[X, :3]; u = np.cross(nx, [1, 0, 0] if abs(nx[0]) < 0.9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(nx, u)
        Q = np.c_[q @ u, q @ w]; area = 0.5 * abs(np.sum(Q[:, 0] * np.roll(Q[:, 1], -1) - np.roll(Q[:, 0], -1) * Q[:, 1]))
        per = np.linalg.norm(Q - np.roll(Q, 1, axis=0), axis=1).sum()
        fat = min(fat, 4 * np.pi * area / per ** 2)
    return {'margin': margin, 'edge': edge, 'fat': fat, 'beauty': float((margin * edge * fat) ** (1 / 3))}


def links_of(r):
    if 'links' in r:
        return {int(k): v for k, v in r['links'].items()}
    from gauss_degree import coherent_triangles, links_from
    tri = json.loads(r['triangles']) if isinstance(r['triangles'], str) else r['triangles']
    return links_from(coherent_triangles(tri), len(r['planes']))


if __name__ == '__main__':
    for f in sys.argv[1:]:
        R = json.load(open(f)); R = R if isinstance(R, list) else [R]
        vals = []
        for r in R:
            if r.get('planes') is None:
                continue
            try:
                vals.append(beauty(r['planes'], links_of(r)))
            except np.linalg.LinAlgError:
                pass
        if not vals:
            continue
        b = np.array([v['beauty'] for v in vals])
        print('%-28s n=%4d  beauty median %.2e (min %.2e, max %.2e) | margin med %.1e  edge med %.1e  fat med %.2f'
              % (f.split('/')[-1][:28], len(vals), np.median(b), b.min(), b.max(), np.median([v['margin'] for v in vals]),
                 np.median([v['edge'] for v in vals]), np.median([v['fat'] for v in vals])))
