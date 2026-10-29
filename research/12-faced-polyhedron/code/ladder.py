"""Ladder of smaller analogues (cross-field-ideas.md, Y1): closed polyhedra with n faces, every two
faces sharing at least one edge, 3 faces per vertex, generic face planes.

n = 7: K7 on the torus (Szilassi; calibration).  n = 8: K8 on genus 2 needs F = 18 faces of the dual
embedding; with 16 triangles + 2 quadrilaterals (or 17 + 1 pentagon) the extra diagonals become
DOUBLED adjacencies (two faces share two edges on the same line), giving a cubic map with 20 vertices.

Pipeline (all our own, no external seeds):
  1. random_map(n, genus): annealing over rotation systems of K_n to reach the target number of faces,
     then random diagonals -> 'links' (for each face X the cyclic list of neighbouring faces, with
     repetitions for doubled adjacencies). Validity: all corner triples distinct.
  2. energy(H, links): face self-crossings + pairs of faces whose intersection on their common line is
     more than their shared edge(s)  (= exact embedding criterion 'simple faces and every pair of faces
     meets exactly in its common edges'), plus a small continuous overlap term.
  3. anneal(links): plane-space annealing with restarts.
Usage: python3 -I ladder.py fast N GENUS N_MAPS MINUTES_PER_MAP SEED OUT_JSON   (fast = numba triple energy)
"""
import json, sys, time
from itertools import combinations
import numpy as np


# ----------------------------------------------------------------------------- maps

def trace_faces(rot):
    """rot[v] = list of darts (v, w, k) in cyclic order; dart twin = (w, v, k). Faces as dart lists."""
    pos = {}
    for v, lst in rot.items():
        for i, d in enumerate(lst):
            pos[d] = (v, i)
    seen, faces = set(), []
    for v in rot:
        for d in rot[v]:
            if d in seen:
                continue
            f, x = [], d
            while x not in seen:
                seen.add(x); f.append(x)
                t = (x[1], x[0], x[2])                 # twin, outgoing at head
                h, i = pos[t]
                x = rot[h][(i + 1) % len(rot[h])]      # successor of the twin
            faces.append(f)
    return faces


def random_map(n, genus, rng, steps=200000):
    target = (n * (n - 1) // 2) - n + 2 - 2 * genus     # faces of a K_n embedding of this genus
    rot = {v: [(v, w, 0) for w in rng.permutation([u for u in range(n) if u != v]).tolist()] for v in range(n)}
    cur = len(trace_faces(rot)); T = 1.0
    for _ in range(steps):
        if cur == target:
            break
        v = int(rng.integers(n)); i, j = rng.choice(n - 1, 2, replace=False)
        r2 = dict(rot); l = list(rot[v]); l[i], l[j] = l[j], l[i]; r2[v] = l
        f = len(trace_faces(r2))
        if f >= cur or rng.random() < np.exp((f - cur) / T):
            rot, cur = r2, f
        T = max(0.05, T * 0.9995)
    if cur != target:
        return None
    # triangulate: add diagonals (doubled adjacencies) inside non-triangular faces
    k = 1
    for f in trace_faces(rot):
        while len(f) > 3:
            m = len(f)
            s = int(rng.integers(m))
            f = f[s:] + f[:s]                         # f[0]: a->b, f[1]: b->c, ..., f[-1]: z->a
            a, c = f[0][0], f[1][1]
            # insert dart a->c at a between twin(f[-1]) and f[0]; c->a at c between twin(f[1]) and f[2]
            n0, n1 = (a, c, k), (c, a, k); k += 1
            la = rot[a]; ia = la.index(f[0]); rot[a] = la[:ia] + [n0] + la[ia:]
            lc = rot[c]; ic = lc.index(f[2]); rot[c] = lc[:ic] + [n1] + lc[ic:]
            f = [n0] + f[2:]
    faces = trace_faces(rot)
    if any(len(f) != 3 for f in faces):
        return None
    triples = [frozenset(d[0] for d in f) for f in faces]
    if any(len(t) != 3 for t in triples) or len(set(triples)) != len(triples):
        return None
    return {X: [d[1] for d in rot[X]] for X in range(n)}


# ----------------------------------------------------------------------------- geometry

def _basis(nrm):
    u = np.cross(nrm, [1.0, 0, 0] if abs(nrm[0]) < 0.9 else [0, 1.0, 0]); u /= np.linalg.norm(u)
    return u, np.cross(nrm, u)


def polygons(H, links):
    P = {}
    for X, L in links.items():
        m = len(L); pts = []
        for i in range(m):
            A, B = L[i], L[(i + 1) % m]
            pts.append(np.linalg.solve(H[[X, A, B], :3], -H[[X, A, B], 3]))
        P[X] = np.array(pts)                           # vertex i = corner (X, L[i], L[i+1])
    return P


def _cr(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _pip(Q, q):
    c = False; m = len(Q)
    for i in range(m):
        a, b = Q[i], Q[(i + 1) % m]
        if (a[1] > q[1]) != (b[1] > q[1]):
            x = a[0] + (q[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > q[0]:
                c = not c
    return c


def line_cover(H, links, P, X, Y):
    """Intervals (in the parameter of line X cap Y) covered by the closed face X, and its shared edges."""
    nX = H[X, :3] / np.linalg.norm(H[X, :3]); u, w = _basis(nX)
    d = np.cross(H[X, :3], H[Y, :3]); d /= np.linalg.norm(d)
    p0 = np.linalg.lstsq(H[[X, Y], :3], -H[[X, Y], 3], rcond=None)[0]
    Q = np.array([[(p - p0) @ u, (p - p0) @ w] for p in P[X]])
    dd = np.array([d @ u, d @ w]); nn = np.array([-dd[1], dd[0]])
    L = links[X]; m = len(L)
    shared, cuts = [], []
    for i in range(m):                                  # edge i of face X joins vertex i-1 and vertex i
        a, b = Q[i - 1], Q[i]
        if L[i] == Y:
            ta, tb = a @ dd, b @ dd; shared.append((min(ta, tb), max(ta, tb))); cuts += [ta, tb]
            continue
        sa, sb = a @ nn, b @ nn
        if sa * sb < 0:
            t = (a + (b - a) * (sa / (sa - sb))) @ dd; cuts.append(t)
        elif sa == 0:
            cuts.append(a @ dd)
    cuts = sorted(cuts)
    span = (max(cuts) - min(cuts)) if cuts else 1.0
    delta = 1e-7 * (span + 1.0)
    cover = []
    for t0, t1 in zip(cuts[:-1], cuts[1:]):
        if t1 - t0 < 1e-12:
            continue
        q = dd * (0.5 * (t0 + t1))
        if _pip(Q, q + delta * nn) or _pip(Q, q - delta * nn):
            cover.append((t0, t1))
    return cover, shared


def _inter_len(A, B):
    s = 0.0
    for a0, a1 in A:
        for b0, b1 in B:
            s += max(0.0, min(a1, b1) - max(a0, b0))
    return s


def energy(H, links, detail=False):
    try:
        P = polygons(H, links)
    except np.linalg.LinAlgError:
        return 10 ** 6, 0.0
    cross = 0
    for X, pts in P.items():
        nX = H[X, :3]; u, w = _basis(nX / np.linalg.norm(nX))
        Q = np.array([[p @ u, p @ w] for p in pts]); m = len(Q)
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                a, b, c, e = Q[i], Q[(i + 1) % m], Q[j], Q[(j + 1) % m]
                if _cr(a, b, c) * _cr(a, b, e) < 0 and _cr(c, e, a) * _cr(c, e, b) < 0:
                    cross += 1
    bad, extra = 0, 0.0
    n = len(H)
    for X, Y in combinations(range(n), 2):
        cX, sX = line_cover(H, links, P, X, Y)
        cY, sY = line_cover(H, links, P, Y, X)
        # align parameterisations: both use d = n_X x n_Y up to sign and the same base point p0
        ov = _inter_len(cX, [(-b, -a) for a, b in cY])   # Y's parameter runs along -d
        sh = sum(b - a for a, b in sX)
        e = ov - sh
        if e > 1e-9 * (1 + sh):
            bad += 1; extra += e / (sh + 1e-9)
    if detail:
        return cross, bad, extra
    return cross + bad, extra


def anneal(links, rng, minutes, steps=20000):
    n = len(links); best = (10 ** 9, None); t0 = time.monotonic(); restarts = 0
    while time.monotonic() - t0 < 60 * minutes:
        restarts += 1
        H = rng.standard_normal((n, 4)); H[:, :3] /= np.linalg.norm(H[:, :3], axis=1)[:, None]
        e, x = energy(H, links); cur = e + 0.01 * np.tanh(x); bl = (cur, H.copy()); T = 1.5
        for _ in range(steps):
            H2 = H.copy(); k = int(rng.integers(n)); sig = float(rng.choice([0.01, 0.05, 0.2]))
            H2[k] += sig * rng.standard_normal(4); H2[k, :3] /= np.linalg.norm(H2[k, :3])
            e2, x2 = energy(H2, links); c2 = e2 + 0.01 * np.tanh(x2)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                H, cur = H2, c2
                if cur < bl[0]:
                    bl = (cur, H.copy())
            T = max(0.02, T * 0.9996)
            if bl[0] < 0.5 or time.monotonic() - t0 > 60 * minutes:
                break
        if bl[0] < best[0]:
            best = bl
        if best[0] < 0.5:
            break
    return best, restarts


def main_slow():
    n, genus, nmaps, minutes, seed, out = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]),
                                            float(sys.argv[4]), int(sys.argv[5]), sys.argv[6])
    rng = np.random.default_rng(seed); results = []
    for mi in range(nmaps):
        links = None
        while links is None:
            links = random_map(n, genus, rng)
        (b, H), rs = anneal(links, rng, minutes)
        det = energy(H, links, detail=True)
        print('map %d: best %.3f (crossings %d, bad pairs %d) restarts %d links %s' % (mi, b, det[0], det[1], rs,
              {k: v for k, v in links.items()}), flush=True)
        results.append({'n': n, 'genus': genus, 'links': {str(k): v for k, v in links.items()},
                        'best': float(b), 'crossings': det[0], 'bad_pairs': det[1], 'planes': H.tolist()})
        json.dump(results, open(out, 'w'))
        if b < 0.5:
            print('!!! ZERO-VIOLATION CONFIGURATION (float) for map', mi, flush=True)


# ----------------------------------------------------------------------------- fast energy (numba)
# Triple criterion (Lemma 5.1 analogue): violation = a triple point P_XYZ that is NOT a corner and lies
# in all three closed faces (even-odd), plus face self-crossings.  Used for annealing; the pair-based
# energy() above is the independent final check.
import numba


def pack(links):
    n = len(links); mmax = max(len(v) for v in links.values())
    LK = -np.ones((n, mmax), np.int64); M = np.zeros(n, np.int64)
    corners = set()
    for X, L in links.items():
        M[X] = len(L); LK[X, :len(L)] = L
        for i in range(len(L)):
            corners.add(frozenset((X, L[i], L[(i + 1) % len(L)])))
    forb = np.array([t for t in combinations(range(n), 3) if frozenset(t) not in corners], np.int64)
    return LK, M, forb


@numba.njit(cache=True)
def _solve3(H, a, b, c):
    m = np.empty((3, 3)); r = np.empty(3)
    for k, x in enumerate((a, b, c)):
        m[k, 0] = H[x, 0]; m[k, 1] = H[x, 1]; m[k, 2] = H[x, 2]; r[k] = -H[x, 3]
    return np.linalg.solve(m, r)


@numba.njit(cache=True)
def fast_energy(H, LK, M, forb):
    n = H.shape[0]; mmax = LK.shape[1]
    Q = np.zeros((n, mmax, 2)); U = np.zeros((n, 2, 3))
    for X in range(n):
        nx = H[X, :3] / np.sqrt((H[X, :3] ** 2).sum())
        if abs(nx[0]) < 0.9:
            t = np.array([1.0, 0.0, 0.0])
        else:
            t = np.array([0.0, 1.0, 0.0])
        u = np.cross(nx, t); u /= np.sqrt((u ** 2).sum()); w = np.cross(nx, u)
        U[X, 0] = u; U[X, 1] = w
        m = M[X]
        for i in range(m):
            p = _solve3(H, X, LK[X, i], LK[X, (i + 1) % m])
            Q[X, i, 0] = p @ u; Q[X, i, 1] = p @ w
    cross = 0
    for X in range(n):
        m = M[X]
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                a = Q[X, i]; b = Q[X, (i + 1) % m]; c = Q[X, j]; e = Q[X, (j + 1) % m]
                d1 = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
                d2 = (b[0] - a[0]) * (e[1] - a[1]) - (b[1] - a[1]) * (e[0] - a[0])
                d3 = (e[0] - c[0]) * (a[1] - c[1]) - (e[1] - c[1]) * (a[0] - c[0])
                d4 = (e[0] - c[0]) * (b[1] - c[1]) - (e[1] - c[1]) * (b[0] - c[0])
                if d1 * d2 < 0 and d3 * d4 < 0:
                    cross += 1
    # doubled adjacencies: the edges of face X lying on the same line X cap Y must be disjoint segments
    # (lesson of the first n = 8 run: otherwise the annealer merges them; the triple criterion is blind to it)
    dbl = 0
    for X in range(n):
        m = M[X]
        for i in range(m):
            for j in range(i + 1, m):
                if LK[X, i] != LK[X, j]:
                    continue
                a0 = Q[X, i - 1 if i > 0 else m - 1]; a1 = Q[X, i]; b0 = Q[X, j - 1]; b1 = Q[X, j]
                dx = a1[0] - a0[0]; dy = a1[1] - a0[1]
                ta1 = dx * dx + dy * dy
                tb0 = (b0[0] - a0[0]) * dx + (b0[1] - a0[1]) * dy; tb1 = (b1[0] - a0[0]) * dx + (b1[1] - a0[1]) * dy
                lo = max(0.0, min(tb0, tb1)); hi = min(ta1, max(tb0, tb1))
                if hi >= lo - 1e-9 * ta1:
                    dbl += 1
    viol = dbl
    for k in range(forb.shape[0]):
        a, b, c = forb[k, 0], forb[k, 1], forb[k, 2]
        p = _solve3(H, a, b, c)
        ok = True
        for X in (a, b, c):
            qx = p @ U[X, 0]; qy = p @ U[X, 1]; m = M[X]; inside = False
            # p lies on the lines X cap Y and X cap Z, i.e. on the supporting lines of edges of face X:
            # if it lies ON such an edge segment it belongs to the closed face (edge pierces a face)
            onb = False
            for i in range(m):
                Bn = LK[X, i]
                if Bn == a or Bn == b or Bn == c:
                    ax, ay = Q[X, i - 1 if i > 0 else m - 1, 0], Q[X, i - 1 if i > 0 else m - 1, 1]
                    bx, by = Q[X, i, 0], Q[X, i, 1]
                    ll = (bx - ax) ** 2 + (by - ay) ** 2
                    t = ((qx - ax) * (bx - ax) + (qy - ay) * (by - ay)) / ll
                    if 0.0 <= t <= 1.0:
                        onb = True
            if onb:
                continue
            for i in range(m):
                ax, ay = Q[X, i, 0], Q[X, i, 1]; bx, by = Q[X, (i + 1) % m, 0], Q[X, (i + 1) % m, 1]
                if (ay > qy) != (by > qy):
                    xx = ax + (qy - ay) * (bx - ax) / (by - ay)
                    if xx > qx:
                        inside = not inside
            if not inside:
                ok = False
                break
        if ok:
            viol += 1
    return cross + viol


def anneal_fast(links, rng, minutes, steps=40000):
    LK, M, forb = pack(links); n = len(links); best = (10 ** 9, None); t0 = time.monotonic(); restarts = 0
    while time.monotonic() - t0 < 60 * minutes:
        restarts += 1
        H = rng.standard_normal((n, 4)); H[:, :3] /= np.linalg.norm(H[:, :3], axis=1)[:, None]
        try:
            e0, o0 = pair_energy(H, LK, M); cur = e0 + 0.01 * np.tanh(o0)
        except Exception as ex:
            if restarts < 3:
                print('energy evaluation failed:', repr(ex)[:300], flush=True)
            continue
        bl = (cur, H.copy()); T = 1.5
        for _ in range(steps):
            H2 = H.copy(); k = int(rng.integers(n)); sig = float(rng.choice([0.01, 0.05, 0.2]))
            H2[k] += sig * rng.standard_normal(4); H2[k, :3] /= np.linalg.norm(H2[k, :3])
            try:
                e2, o2 = pair_energy(H2, LK, M); c2 = e2 + 0.01 * np.tanh(o2)
            except Exception:
                continue
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                H, cur = H2, c2
                if cur < bl[0]:
                    bl = (cur, H.copy())
            T = max(0.03, T * 0.9998)
            if bl[0] < 0.5:
                break
        if bl[0] < best[0]:
            best = bl
        if best[0] < 0.5:
            break
    return best, restarts


def main_fast():
    n, genus, nmaps, minutes, seed, out = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                                            float(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
    rng = np.random.default_rng(seed); results = []
    for mi in range(nmaps):
        links = None
        while links is None:
            links = random_map(n, genus, rng)
        (b, H), rs = anneal_fast(links, rng, minutes)
        if H is None:
            print('map %d: no evaluation succeeded' % mi, flush=True); continue
        det = energy(H, links, detail=True)
        print('map %d: fast best %.3f | pair check: crossings %d, bad pairs %d | restarts %d' % (mi, b, det[0], det[1], rs), flush=True)
        results.append({'n': n, 'genus': genus, 'links': {str(k): v for k, v in links.items()},
                        'best_fast': float(b), 'crossings': det[0], 'bad_pairs': det[1], 'planes': H.tolist()})
        json.dump(results, open(out, 'w'))
        if b < 0.5:
            print('!!! ZERO-VIOLATION CONFIGURATION (float) for map', mi, flush=True)



# ----------------------------------------------------------------------------- pair energy (numba)
# The triple criterion is blind to doubled adjacencies (an overlap in the gap between the two shared
# edges starts and ends at CORNERS). This energy is the float twin of ladder_exact.verify: for every
# pair of faces, decide on the line X cap Y which open intervals lie in both faces outside the shared
# edges. Energy = self-crossings + overlapping collinear (doubled) edges + bad pairs (+ overlap length).

@numba.njit(cache=True)
def pair_energy(H, LK, M):
    n = H.shape[0]; mmax = LK.shape[1]
    P3 = np.zeros((n, mmax, 3)); Q = np.zeros((n, mmax, 2)); U = np.zeros((n, 2, 3))
    for X in range(n):
        nx = H[X, :3] / np.sqrt((H[X, :3] ** 2).sum())
        t = np.array([1.0, 0.0, 0.0]) if abs(nx[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        u = np.cross(nx, t); u /= np.sqrt((u ** 2).sum()); w = np.cross(nx, u)
        U[X, 0] = u; U[X, 1] = w
        m = M[X]
        for i in range(m):
            p = _solve3(H, X, LK[X, i], LK[X, (i + 1) % m])
            P3[X, i] = p; Q[X, i, 0] = p @ u; Q[X, i, 1] = p @ w
    cross = 0; dbl = 0
    for X in range(n):
        m = M[X]
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                a = Q[X, i]; b = Q[X, (i + 1) % m]; c = Q[X, j]; e = Q[X, (j + 1) % m]
                d1 = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
                d2 = (b[0] - a[0]) * (e[1] - a[1]) - (b[1] - a[1]) * (e[0] - a[0])
                d3 = (e[0] - c[0]) * (a[1] - c[1]) - (e[1] - c[1]) * (a[0] - c[0])
                d4 = (e[0] - c[0]) * (b[1] - c[1]) - (e[1] - c[1]) * (b[0] - c[0])
                if d1 * d2 < 0 and d3 * d4 < 0:
                    cross += 1
            for j in range(i + 1, m):
                if LK[X, i] != LK[X, j]:
                    continue
                a0 = Q[X, i - 1 if i > 0 else m - 1]; a1 = Q[X, i]; b0 = Q[X, j - 1]; b1 = Q[X, j]
                dx = a1[0] - a0[0]; dy = a1[1] - a0[1]; ta1 = dx * dx + dy * dy
                tb0 = (b0[0] - a0[0]) * dx + (b0[1] - a0[1]) * dy; tb1 = (b1[0] - a0[0]) * dx + (b1[1] - a0[1]) * dy
                if min(ta1, max(tb0, tb1)) >= max(0.0, min(tb0, tb1)) - 1e-9 * ta1:
                    dbl += 1
    # degeneracy guard (lesson of the CMA-ES run: the optimizer collapsed features below the float
    # thresholds and scored 0 on configurations that change under 1e-9 perturbations): every polygon
    # edge must be at least 1e-6 of the diameter of the vertex set (1e-3 rejected genuine Szilassi
    # realizations with short edges); shorter edges count as violations
    lo3 = np.full(3, 1e300); hi3 = np.full(3, -1e300)
    for X in range(n):
        for i in range(M[X]):
            for q in range(3):
                lo3[q] = min(lo3[q], P3[X, i, q]); hi3[q] = max(hi3[q], P3[X, i, q])
    diam = np.sqrt(((hi3 - lo3) ** 2).sum())
    # scale-collapse guard: the problem is scale invariant, so a configuration whose vertices shrink
    # towards one point (all planes nearly concurrent) only feeds float noise to the predicates
    cmax = max(np.abs(lo3).max(), np.abs(hi3).max())
    if diam < 1e-3 * (1.0 + cmax):
        return 99, 0.0
    short = 0
    for X in range(n):
        m = M[X]
        for i in range(m):
            dv = P3[X, i] - P3[X, i - 1 if i > 0 else m - 1]
            if np.sqrt((dv ** 2).sum()) < 1e-6 * diam:
                short += 1
    bad = short; over = 0.0
    crit = np.zeros(4 * mmax); sh0 = np.zeros(mmax); sh1 = np.zeros(mmax)
    for X in range(n):
        for Y in range(X + 1, n):
            d = np.cross(H[X, :3], H[Y, :3]); dd = (d ** 2).sum()
            A = np.empty((3, 3)); A[0] = H[X, :3]; A[1] = H[Y, :3]; A[2] = d
            rhs = np.array([-H[X, 3], -H[Y, 3], 0.0])
            p0 = np.linalg.solve(A, rhs)
            nc = 0; ns = 0
            for side in range(2):
                Z = X if side == 0 else Y
                W = Y if side == 0 else X
                m = M[Z]
                for i in range(m):
                    a = P3[Z, i - 1 if i > 0 else m - 1]; b = P3[Z, i]
                    if LK[Z, i] == W:
                        ta = ((a - p0) @ d) / dd; tb = ((b - p0) @ d) / dd
                        crit[nc] = ta; crit[nc + 1] = tb; nc += 2
                        if side == 0:
                            sh0[ns] = min(ta, tb); sh1[ns] = max(ta, tb); ns += 1
                        continue
                    fa = H[W, :3] @ a + H[W, 3]; fb = H[W, :3] @ b + H[W, 3]
                    if fa * fb < 0:
                        q = a + (b - a) * (fa / (fa - fb))
                        crit[nc] = ((q - p0) @ d) / dd; nc += 1
            cs = np.sort(crit[:nc])
            isbad = False
            for k in range(nc - 1):
                t0 = cs[k]; t1 = cs[k + 1]
                if t1 - t0 < 1e-12:
                    continue
                tm = 0.5 * (t0 + t1)
                insh = False
                for s in range(ns):
                    if sh0[s] - 1e-12 <= tm <= sh1[s] + 1e-12:
                        insh = True
                if insh:
                    continue
                q = p0 + tm * d
                inb = True
                for side in range(2):
                    Z = X if side == 0 else Y
                    qx = q @ U[Z, 0]; qy = q @ U[Z, 1]; m = M[Z]; inside = False
                    for i in range(m):
                        ax, ay = Q[Z, i, 0], Q[Z, i, 1]; bx, by = Q[Z, (i + 1) % m, 0], Q[Z, (i + 1) % m, 1]
                        if (ay > qy) != (by > qy):
                            if ax + (qy - ay) * (bx - ax) / (by - ay) > qx:
                                inside = not inside
                    if not inside:
                        inb = False
                        break
                if inb:
                    isbad = True; over += (t1 - t0) * np.sqrt(dd)
            if isbad:
                bad += 1
    return cross + dbl + bad, over


if __name__ == '__main__':
    if sys.argv[1] == 'fast':
        main_fast()
    else:
        main_slow()
