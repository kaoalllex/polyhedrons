"""Gauss-map gate for the genus ladder (review 2026-10-30, test T1; theory: gauss_degree.py).

For a polyhedron with n faces and genus g (any sub-map, not only the neighborly genus-6 map) the
Gauss-map degree in the gauge of its own face orientations is chi/2 = 1 - g, and every direction is
covered by a POSITIVE triangle. Seeding level g+1 from the planes of level g starts with degree
D_M + k_tau (D_M = 1 - g at a realization; k_tau = degree of the octahedral sphere tube - A - B of the
six handle faces), so a handle needs k_tau = -1 and the review found k_tau = 0 at every saved type-0
seed (six handle normals in an open hemisphere). This module computes, for a configuration H (planes)
and a map (dual triangles):

  own_gauge     eps_X = sign of the area of face X's polygon (coherent link order) about n_X
  own_degree    the degree in that gauge (exact: integer normals, rounded at scale 1e6)
  turning       turning number of every face polygon about its own gauge normal (+1 for a simple
                face; 0 = figure-eight, the signature of the genus-4 plateau)
  gauges        all eps in {+-1}^n with degree == 1 - g (or a given target) and positive covering at
                n_cover sample directions (exact sign tables, vectorised over the 2^n gauges)
  k_tau, hemisphere margin of the six handle faces (for an arm: realization of M -> next map M + tau)

Counter names (review problem 1): this module counts CLASS defects (|degree - (1 - g)|, number of faces
with turning != +1); ladder.pair_energy counts violation EVENTS; ladder_exact counts exact defects.

Usage: python3 -I gauss_gate.py T1 OUT_JSON FILES...   (realization / attempt JSON files with 'planes'
       + 'triangles', or night-3 glad results.jsonl: every level, realized or not, and every arm
       (realization, extendable next handle) of the realized ones)
       python3 -I gauss_gate.py T22 OUT_JSON GLAD_RESULTS.jsonl...   (review test 2.2 per chain)
"""
import itertools
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import coherent_triangles, links_from, det3

SCALE = 10 ** 6


# ----------------------------------------------------------------------------- basic invariants

def euler_target(tris, n):
    """chi/2 = 1 - g of the closed surface with these dual triangles (n faces)."""
    E = len({frozenset(e) for t in tris for e in itertools.combinations(t, 2)})
    chi = n - E + len(tris)
    assert chi % 2 == 0
    return chi // 2


def genus(tris, n):
    return 1 - euler_target(tris, n)


def unit_planes(H):
    H = np.array(H, float)
    nr = np.linalg.norm(H[:, :3], axis=1)
    return H / nr[:, None]


def int_normals(H, scale=SCALE):
    """Integer normals of the planes (unit normals scaled and rounded)."""
    Hn = unit_planes(H)
    return [[int(round(v * scale)) for v in h[:3]] for h in Hn]


def face_polygons(H, links):
    """Corner points of every face polygon in link order (float). Corner i = P(X, L[i], L[i+1])."""
    H = unit_planes(H)
    out = {}
    for X, cyc in links.items():
        pts = []
        for i in range(len(cyc)):
            A, B = cyc[i], cyc[(i + 1) % len(cyc)]
            M = np.array([H[X][:3], H[A][:3], H[B][:3]])
            pts.append(np.linalg.solve(M, -np.array([H[X][3], H[A][3], H[B][3]])))
        out[X] = np.array(pts)
    return out


def own_gauge(H, links, polys=None):
    """eps_X = +1 iff the polygon of face X (link order) has positive signed area about n_X."""
    H = unit_planes(H)
    polys = face_polygons(H, links) if polys is None else polys
    eps = []
    for X in range(len(H)):
        P = polys[X]
        area = np.cross(P, np.roll(P, -1, axis=0)).sum(axis=0)
        eps.append(1 if area @ H[X][:3] > 0 else -1)
    return eps


def turning_numbers(H, links, eps=None, polys=None):
    """Turning number of each face polygon about its gauge normal eps_X n_X (+1 = once
    counter-clockwise; a simple polygon has +1 in its own gauge, a figure-eight 0). None if an
    edge has (numerically) zero length."""
    H = unit_planes(H)
    polys = face_polygons(H, links) if polys is None else polys
    eps = own_gauge(H, links, polys) if eps is None else eps
    out = []
    for X in range(len(H)):
        nrm = eps[X] * H[X][:3]
        a = np.cross(nrm, [1.0, 0, 0] if abs(nrm[0]) < 0.9 else [0, 1.0, 0]); a /= np.linalg.norm(a)
        b = np.cross(nrm, a)                                    # (a, b, nrm) right-handed
        P = polys[X]
        d = np.roll(P, -1, axis=0) - P
        if np.min(np.linalg.norm(d, axis=1)) < 1e-12:
            out.append(None); continue
        ang = np.arctan2(d @ b, d @ a)
        turn = np.diff(np.concatenate([ang, ang[:1]]))
        turn = (turn + np.pi) % (2 * np.pi) - np.pi
        out.append(int(round(turn.sum() / (2 * np.pi))))
    return out


# ----------------------------------------------------------------------------- exact degree tables

def _directions(n_cover, seed):
    rng = random.Random(seed)
    U = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(3)] for _ in range(n_cover + 1)]
    return U                                              # U[0] = the degree direction


def sign_tables(N, otris, U):
    """Exact sign tables (independent of the gauge). For a triangle t = (a,b,c) with d0 = sign det
    (n_a,n_b,n_c) and d1, d2, d3 = sign det(u,n_b,n_c), det(n_a,u,n_c), det(n_a,n_b,u): u lies in the cone
    of the GAUGE normals (e_a n_a, e_b n_b, e_c n_c) iff (e_a, e_b, e_c) = d0 (d1, d2, d3), and then the
    triangle contributes sign d1 d2 d3 to the degree. Returns (req (m,T,3) int8, contrib (m,T) int8,
    d0 (T,))."""
    T = len(otris)
    d0 = np.array([np.sign(det3(N[a], N[b], N[c])) for a, b, c in otris], np.int8)
    if (d0 == 0).any():
        raise ValueError('degenerate normals (three coplanar)')
    req = np.zeros((len(U), T, 3), np.int8)
    con = np.zeros((len(U), T), np.int8)
    for i, u in enumerate(U):
        for j, (a, b, c) in enumerate(otris):
            d1 = det3(u, N[b], N[c]); d2 = det3(N[a], u, N[c]); d3 = det3(N[a], N[b], u)
            if d1 == 0 or d2 == 0 or d3 == 0:
                raise ValueError('sample direction not generic')
            s1, s2, s3 = (1 if d1 > 0 else -1), (1 if d2 > 0 else -1), (1 if d3 > 0 else -1)
            req[i, j] = (d0[j] * s1, d0[j] * s2, d0[j] * s3)
            con[i, j] = s1 * s2 * s3
    return req, con, d0


def degrees_and_cover(eps, otris, req, con):
    """eps (G, n) of +-1. Returns degree at U[0] (G,) and positive covering at all U[1:] (G,) bool."""
    eps = np.asarray(eps, np.int8)
    if eps.ndim == 1:
        eps = eps[None, :]
    ia = np.array([t[0] for t in otris]); ib = np.array([t[1] for t in otris]); ic = np.array([t[2] for t in otris])
    Ea, Eb, Ec = eps[:, ia], eps[:, ib], eps[:, ic]                      # (G, T)
    inside = ((Ea[:, None, :] == req[None, :, :, 0]) & (Eb[:, None, :] == req[None, :, :, 1])
              & (Ec[:, None, :] == req[None, :, :, 2]))                  # (G, m, T)
    deg = (inside[:, 0, :] * con[0][None, :]).sum(axis=1)
    cover = (inside[:, 1:, :] & (con[None, 1:, :] > 0)).any(axis=2).all(axis=1)
    return deg, cover


def degree(N, otris, eps, seed=0):
    U = _directions(0, seed)
    req, con, _ = sign_tables(N, otris, U)
    return int(degrees_and_cover(eps, otris, req, con)[0][0])


def all_gauges(n):
    return np.array([[1 if (m >> i) & 1 == 0 else -1 for i in range(n)] for m in range(1 << n)], np.int8)


def admissible(N, otris, target, n_cover=64, seed=0, eps=None, n_confirm=1000):
    """All gauges (or the given ones) with degree == target and positive covering at n_cover samples,
    confirmed at n_confirm further samples (64 alone let a gauge with an uncovered region through).
    Also returns the degrees of all tested gauges (for statistics)."""
    U = _directions(n_cover, seed)
    req, con, _ = sign_tables(N, otris, U)
    E = all_gauges(len(N)) if eps is None else np.asarray(eps, np.int8)
    out = []; degs = []
    for k in range(0, len(E), 512):
        d, c = degrees_and_cover(E[k:k + 512], otris, req, con)
        degs.append(d)
        for i in np.nonzero((d == target) & c)[0]:
            out.append([int(x) for x in E[k + i]])
    if out and n_confirm:
        U2 = _directions(n_confirm, seed + 1)
        req2, con2, _ = sign_tables(N, otris, U2)
        _, c2 = degrees_and_cover(out, otris, req2, con2)
        out = [g for g, ok in zip(out, c2) if ok]
    return out, np.concatenate(degs)


def saddles(N, otris, eps):
    """Number of negatively oriented triangles in the gauge (= saddle vertices; >= 2g+1 needed)."""
    s = 0
    for a, b, c in otris:
        d = eps[a] * eps[b] * eps[c] * det3(N[a], N[b], N[c])
        s += d < 0
    return int(s)


# ----------------------------------------------------------------------------- handles

def aligned_orientations(tris_M, tris_R, n):
    """Coherent orientations of M and of M + tau that agree on their common triangles."""
    oM = coherent_triangles([tuple(t) for t in tris_M])
    oR = coherent_triangles([tuple(t) for t in tris_R])
    dM = {frozenset(t): t for t in oM}
    for t in oR:
        s = dM.get(frozenset(t))
        if s is not None:
            same = any(t == s[i:] + s[:i] for i in range(3))
            if not same:
                oR = [(b, a, c) for a, b, c in oR]
            break
    return oM, oR


def hemisphere_margin(vectors):
    """max_w min_i <w, v_i/|v_i|> over |w| <= 1 (LP with the box |w_j| <= 1, then normalised).
    > 0 iff the vectors lie in an open hemisphere."""
    from scipy.optimize import linprog
    V = np.array(vectors, float); V /= np.linalg.norm(V, axis=1)[:, None]
    # variables w (3), t; maximize t s.t. t - V w <= 0, -1 <= w <= 1
    A = np.hstack([-V, np.ones((len(V), 1))])
    r = linprog([0, 0, 0, -1], A_ub=A, b_ub=np.zeros(len(V)), bounds=[(-1, 1)] * 3 + [(None, None)], method='highs')
    w = r.x[:3]; nw = np.linalg.norm(w)
    if nw < 1e-12:
        return float(r.x[3])
    return float(np.min(V @ (w / nw)))


def k_tau(N, eps, oM, oR, seed=0):
    """Degree of the handle sphere (tube minus the two removed triangles) = D_{M+tau} - D_M (same gauge)."""
    return degree(N, oR, eps, seed) - degree(N, oM, eps, seed)


# ----------------------------------------------------------------------------- reports

def config_report(H, tris, n_cover=64, seed=0, gauges=True):
    """Class data of a configuration H for its own map: own degree vs 1 - g, turning numbers,
    saddles, number of admissible gauges (and whether the own gauge is one of them)."""
    n = len(H)
    ot = coherent_triangles([tuple(t) for t in tris])
    L = links_from(ot, n)
    target = euler_target(tris, n)
    N = int_normals(H)
    polys = face_polygons(H, L)
    eps = own_gauge(H, L, polys)
    rep = {'genus': 1 - target, 'target_degree': target, 'own_gauge': eps}
    try:
        rep['own_degree'] = degree(N, ot, eps, seed)
    except ValueError as e:
        rep['own_degree'] = None; rep['error'] = str(e)
        return rep
    rep['turning'] = turning_numbers(H, L, eps, polys)
    rep['bad_turning_faces'] = [X for X, t in enumerate(rep['turning']) if t != 1]
    rep['saddles'] = saddles(N, ot, eps)
    rep['class_defect'] = abs(rep['own_degree'] - target) + len(rep['bad_turning_faces'])
    if gauges:
        adm, _ = admissible(N, ot, target, n_cover, seed)
        rep['n_admissible'] = len(adm)
        rep['own_admissible'] = eps in adm
        rep['admissible'] = adm[:64]
    return rep


def arm_report(H, tris_M, tris_R, tube, n_cover=64, seed=0):
    """T1 for an arm (realization H of M, next map M + tau). The seed gauge is the face orientation of
    the realized polyhedron M (its polygons, coherent order of M aligned with M + tau): in it
    D_{M+tau} = D_M + k_tau = (1 - g) + k_tau. ('new_polygon_*': the gauge of the next map's polygons at
    the same planes; the six handle faces' new polygons are not meaningful there, for information only.)"""
    n = len(H)
    oM, oR = aligned_orientations(tris_M, tris_R, n)
    LM, LR = links_from(oM, n), links_from(oR, n)
    target = euler_target(tris_R, n)
    N = int_normals(H)
    eps = own_gauge(H, LM)                            # the realized polyhedron's own face orientation
    polys = face_polygons(H, LR)
    eps_new = own_gauge(H, LR, polys)
    six = sorted(set(tube[0]) | set(tube[1]))
    rep = {'tube': [list(tube[0]), list(tube[1])], 'target_degree': target, 'seed_gauge': eps}
    try:
        rep['own_degree'] = degree(N, oR, eps, seed)
        rep['k_tau'] = k_tau(N, eps, oM, oR, seed)
        rep['new_polygon_degree'] = degree(N, oR, eps_new, seed)
    except ValueError as e:
        rep['error'] = str(e); return rep
    rep['hemisphere_margin'] = hemisphere_margin([[eps[X] * v for v in N[X]] for X in six])
    rep['turning'] = turning_numbers(H, LR, eps_new, polys)
    rep['bad_turning_faces'] = [X for X, t in enumerate(rep['turning']) if t != 1]
    adm, degs = admissible(N, oR, target, n_cover, seed)
    rep['n_admissible'] = len(adm)
    rep['degree_range'] = [int(degs.min()), int(degs.max())]
    rep['admissible'] = adm[:64]
    # admissible gauges that differ from the own gauge only on the six handle faces (no reversal of a
    # polygon outside the tube is needed); reversed faces per admissible gauge
    rev = [[X for X in range(n) if g[X] != eps[X]] for g in adm]
    rep['min_reversed'] = min((len(r) for r in rev), default=None)
    rep['n_tube_only'] = sum(1 for r in rev if set(r) <= set(six))
    rep['pass'] = len(adm) > 0
    return rep


def arms_of(H, tris, n, extendable_only=True):
    """(t1, t2, R) for every next handle (all six new pairs new); extendable ones only by default."""
    from handle_add import candidates, reach
    full = n * (n - 1) // 2
    out = []
    for t1, t2, R, L in candidates([tuple(t) for t in tris], n):
        if extendable_only:
            r, _ = reach(R, n, node_limit=3000)
            if r != full:
                continue
        out.append((t1, t2, R))
    return out


def iter_inputs(files):
    """Yield (name, planes, triangles, realized_flag or None, type_id)."""
    for f in files:
        if f.endswith('.jsonl'):
            for line in open(f):
                if not line.strip():
                    continue
                r = json.loads(line)
                for lv in r.get('levels', []):
                    yield ('%s level %d' % (r.get('task'), lv.get('genus', -1)), lv['planes'], lv['triangles'],
                           lv.get('best', 99) < 0.5, r.get('type_id', -1))
                br = (r.get('branch') or {}).get('realized')
                if br:
                    yield ('%s branch' % r.get('task'), br['planes'], br['triangles'], True, r.get('type_id', -1))
        else:
            d = json.load(open(f))
            recs = d if isinstance(d, list) else [d]
            for i, r in enumerate(recs):
                if 'planes' in r and 'triangles' in r:
                    yield ('%s[%d]' % (os.path.basename(f), i), r['planes'], r['triangles'],
                           r.get('exact', r.get('best', 99) < 0.5), r.get('type_id', -1))


def t1_main(out, files, verify_exact=True):
    from ladder_exact import verify
    res = []
    for name, planes, tris, realized, tid in iter_inputs(files):
        n = len(planes)
        tris = [tuple(t) for t in tris]
        L = links_from(coherent_triangles(tris), n)
        if verify_exact:
            realized = bool(verify(planes, L, require_all_pairs=False)['EMBEDDED'])
        rec = {'name': name, 'type_id': tid, 'realized': realized}
        rec.update(config_report(planes, tris))
        if realized and rec['genus'] < (n - 3) * (n - 4) // 12:
            arms = []
            for t1, t2, R in arms_of(planes, tris, n):
                a = arm_report(planes, tris, R, (t1, t2))
                a.pop('admissible', None)
                arms.append(a)
            rec['arms'] = arms
            rec['arms_passing'] = sum(1 for a in arms if a.get('pass'))
        rec.pop('admissible', None)
        res.append(rec)
        print('%s type %s genus %d %s: own degree %s (target %d), bad turning %s, admissible %s%s' % (
            name, tid, rec['genus'], 'REALIZED' if realized else 'attempt', rec.get('own_degree'), rec['target_degree'],
            rec.get('bad_turning_faces'), rec.get('n_admissible'),
            '' if 'arms' not in rec else '; arms %d, passing T1 %d, own degree %s, k_tau %s' % (
                len(rec['arms']), rec['arms_passing'], [a.get('own_degree') for a in rec['arms']],
                [a.get('k_tau') for a in rec['arms']])), flush=True)
        json.dump(res, open(out, 'w'))
    return res


def chain_report(levels, n=12):
    """Review test 2.2 on one genus-ladder chain (glad record 'levels', each seeded from the planes of
    the level below): per level the own-orientation degree of its best attempt (vs 1 - g), the faces
    with turning != +1, and the degree of the NEXT level's map at the same planes in the same orientation
    (vs 1 - g - 1). Prediction: failed levels have degree != 1 - g; a failed level followed by a
    realized one already sits at 1 - (g + 1)."""
    out = []
    for i, lv in enumerate(levels):
        tris = [tuple(t) for t in lv['triangles']]
        r = {'genus': lv.get('genus'), 'best': lv.get('best'), 'exact': bool(lv.get('exact'))}
        try:
            c = config_report(lv['planes'], tris, gauges=False)
            r.update(own_degree=c.get('own_degree'), target=c['target_degree'], bad_turning=c.get('bad_turning_faces'))
            if i + 1 < len(levels):
                R = [tuple(t) for t in levels[i + 1]['triangles']]
                oM, oR = aligned_orientations(tris, R, n)
                eps = own_gauge(lv['planes'], links_from(oM, n))
                r['next_degree'] = degree(int_normals(lv['planes']), oR, eps)
                r['next_target'] = euler_target(R, n)
        except Exception as e:                       # noqa: BLE001
            r['error'] = repr(e)[:200]
        out.append(r)
    return out


def t22_main(out, files):
    """Chain reports for every glad record; summary of the 2.2 prediction."""
    res = []; stats = {'failed_in_class': 0, 'failed_out_of_class': 0, 'skip_next_in_class': 0, 'skip_next_out': 0}
    for f in files:
        for line in open(f):
            if not line.strip():
                continue
            r = json.loads(line)
            ch = chain_report(r.get('levels', []))
            for i, lv in enumerate(ch):
                if lv.get('own_degree') is None:
                    continue
                if not lv['exact']:
                    stats['failed_in_class' if lv['own_degree'] == lv['target'] else 'failed_out_of_class'] += 1
                    if i + 1 < len(ch) and ch[i + 1]['exact'] and 'next_degree' in lv:
                        stats['skip_next_in_class' if lv['next_degree'] == lv['next_target'] else 'skip_next_out'] += 1
            res.append({'task': r.get('task'), 'type_id': r.get('type_id'), 'levels': ch})
            print(r.get('task'), 'type', r.get('type_id'), [(l.get('genus'), round(l.get('best') or 0, 2), l.get('own_degree'),
                                                            l.get('target'), l.get('next_degree')) for l in ch], flush=True)
    print('2.2 summary:', stats, flush=True)
    json.dump({'chains': res, 'summary': stats}, open(out, 'w'))
    return stats


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'T1':
        t1_main(sys.argv[2], sys.argv[3:])
    elif len(sys.argv) > 2 and sys.argv[1] == 'T22':
        t22_main(sys.argv[2], sys.argv[3:])
    else:
        print(__doc__)
