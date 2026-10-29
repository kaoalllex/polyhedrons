"""Idea from computer graphics (generalized winding numbers, Jacobson et al. 2013): the winding number
w(x) of the closed polyhedral 2-cycle is constant on every cell of the 12-plane arrangement; an
embedding has w in {0,1} everywhere, while any transverse self-intersection creates w outside {0,1}.
'Excess' = vol(w not in {0,1}) / vol(w != 0) is a continuous, volume-based distance to an embedding.
Monte Carlo diagnostic on the near-miss seeds. Usage: SEEDS_JSON N_POINTS [MAX_SEEDS]"""
import json, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles, links_from
from local_viol import polygons, local_violations


def winding(polys, P):
    """Generalized winding number of the oriented polygons at points P (n x 3)."""
    tot = np.zeros(len(P))
    for Q in polys:
        for i in range(1, len(Q) - 1):        # fan triangles (Q0, Qi, Qi+1): fine for any closed polygon
            a, b, c = Q[0] - P, Q[i] - P, Q[i + 1] - P
            la, lb, lc = (np.linalg.norm(v, axis=1) for v in (a, b, c))
            num = np.einsum('ij,ij->i', a, np.cross(b, c))
            den = la * lb * lc + np.einsum('ij,ij->i', a, b) * lc + np.einsum('ij,ij->i', a, c) * lb \
                + np.einsum('ij,ij->i', b, c) * la
            tot += 2 * np.arctan2(num, den)
    return tot / (4 * np.pi)


def excess(H, L, n, rng):
    polys = polygons(H, L)
    V = np.vstack(polys)
    lo, hi = V.min(0), V.max(0)
    P = lo + (hi - lo) * rng.random((n, 3))
    w = winding(polys, P)
    wi = np.rint(w)
    bad_int = float(np.mean(np.abs(w - wi) > 1e-6))   # must be ~0 (coherent orientation check)
    wi = wi.astype(int)
    if wi.sum() < 0:
        wi = -wi
    nz = np.count_nonzero(wi)
    ex = np.count_nonzero((wi != 0) & (wi != 1))
    vals, cnt = np.unique(wi, return_counts=True)
    return ex / max(nz, 1), dict(zip(vals.tolist(), cnt.tolist())), bad_int


if __name__ == '__main__':
    seeds = json.load(open(sys.argv[1])); n = int(sys.argv[2])
    m = int(sys.argv[3]) if len(sys.argv) > 3 else len(seeds)
    rng = np.random.default_rng(0); rows = []
    for s in seeds[:m]:
        H = np.array(s['planes'], float); L = links_from(coherent_triangles(s['triangles']), 12)
        try:
            ex, hist, bad = excess(H, L, n, rng)
            cr, mr, _ = local_violations(H, L)
        except np.linalg.LinAlgError:
            continue
        rows.append((ex, cr + mr, s.get('hp_intersections'), hist, bad, s['seed_id']))
    rows.sort(key=lambda r: r[0])
    print('seeds', len(rows), 'max non-integer fraction', max(r[4] for r in rows))
    print('excess quantiles (0,10,50,90,100%%):', np.quantile([r[0] for r in rows], [0, .1, .5, .9, 1]).round(4))
    allv = {}
    for r in rows:
        for k, c in r[3].items():
            allv[k] = allv.get(k, 0) + 1
    print('winding values occurring (number of seeds):', dict(sorted(allv.items())))
    ex = np.array([r[0] for r in rows]); loc = np.array([r[1] for r in rows], float)
    hpv = np.array([r[2] if r[2] is not None else np.nan for r in rows], float)
    print('Spearman-like corr(excess, local viol) = %.3f' % np.corrcoef(np.argsort(np.argsort(ex)), np.argsort(np.argsort(loc)))[0, 1])
    ok = ~np.isnan(hpv)
    if ok.sum() > 10:
        print('corr(excess, hp_intersections) = %.3f' % np.corrcoef(np.argsort(np.argsort(ex[ok])), np.argsort(np.argsort(hpv[ok])))[0, 1])
    for r in rows[:8]:
        print('best: excess %.4f local %d hp_int %s hist %s %s' % (r[0], r[1], r[2], r[3], r[5]))


def octant_winding(H, L, eps=1e-7):
    """Exact-in-principle cell test: w at the 8 octant points next to every triple point (every bounded
    cell of the arrangement has a triple point on its boundary). Returns (bad samples, distinct w values)."""
    from itertools import combinations, product
    polys = polygons(H, L)
    scale = np.ptp(np.vstack(polys), axis=0).max()
    pts = []
    for a, b, c in combinations(range(len(H)), 3):
        M = H[[a, b, c], :3]
        p = np.linalg.solve(M, -H[[a, b, c], 3])
        Minv = np.linalg.inv(M)
        for s in product((-1.0, 1.0), repeat=3):
            d = Minv @ np.array(s)
            pts.append(p + eps * scale * d / np.linalg.norm(d))
    w = np.rint(winding(polys, np.array(pts))).astype(int)
    if w.sum() < 0:
        w = -w
    return int(np.count_nonzero((w != 0) & (w != 1))), sorted(set(w.tolist()))
