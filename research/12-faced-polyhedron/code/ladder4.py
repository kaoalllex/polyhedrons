"""Ladder rung 8b: closed polyhedra with 8 mutually adjacent faces on genus 2 WITHOUT doubled
adjacencies: the dual K8 embedding has 16 triangles + 2 quadrilaterals, i.e. the polyhedron has 16
three-valent vertices and 2 FOUR-valent vertices (4 concurrent face planes; each pair of faces shares
exactly one edge, like the 12-face problem).

Concurrency is built in: for each quadrilateral (A, B, C, D) one "dependent" plane D gets its offset
from the point A cap B cap C (e_D = -n_D . P_ABC). Energy = numba pair energy (as ladder.pair_energy)
with the 4-valent point of a quadrilateral allowed as an isolated common point of its two opposite faces.
Exact verification: ladder4_exact.py.
Usage: python3 -I ladder4.py N_MAPS MINUTES SEED OUT_JSON [ENGINE=anneal|cma]"""
import json, sys, time
import numpy as np
import numba
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ladder import trace_faces, _solve3


def random_map4(n, genus, rng, steps=200000):
    """K_n rotation system of the given genus whose faces are triangles and exactly two quadrilaterals."""
    target = (n * (n - 1) // 2) - n + 2 - 2 * genus
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
    faces = trace_faces(rot)
    sizes = sorted(len(f) for f in faces)
    if sizes.count(4) != 2 or sizes.count(3) != len(sizes) - 2:
        return None
    quads = [tuple(d[0] for d in f) for f in faces if len(f) == 4]
    tris = [frozenset(d[0] for d in f) for f in faces if len(f) == 3]
    if any(len(set(q)) != 4 for q in quads) or len(set(tris)) != len(tris) or any(len(t) != 3 for t in tris):
        return None
    if any(t <= frozenset(q) for t in tris for q in quads) or len(set(quads[0]) & set(quads[1])) > 2:
        return None                                    # a triangle inside a quad = two vertices at one point
    links = {X: [d[1] for d in rot[X]] for X in range(n)}
    # dependent planes: a private plane of each quadrilateral
    d0 = [x for x in quads[0] if x not in quads[1]][0]
    d1 = [x for x in quads[1] if x not in quads[0]][0]
    return {'links': links, 'quads': [list(quads[0]), list(quads[1])], 'dep': [d0, d1]}


def pack4(m):
    links = {int(k): v for k, v in m['links'].items()}
    n = len(links); mmax = max(len(v) for v in links.values())
    LK = -np.ones((n, mmax), np.int64); M = np.zeros(n, np.int64)
    for X, L in links.items():
        M[X] = len(L); LK[X, :len(L)] = L
    QD = np.zeros((2, 4), np.int64)                    # three determining planes, then the dependent one
    OPP = np.zeros((2, 2, 2), np.int64)                # per quad: its two opposite pairs
    for qi, (q, d) in enumerate(zip(m['quads'], m['dep'])):
        QD[qi, :3] = [x for x in q if x != d]; QD[qi, 3] = d
        OPP[qi, 0] = sorted((q[0], q[2])); OPP[qi, 1] = sorted((q[1], q[3]))
    return LK, M, QD, OPP


@numba.njit(cache=True)
def constrain(H, QD):
    H2 = H.copy()
    for qi in range(QD.shape[0]):
        p = _solve3(H2, QD[qi, 0], QD[qi, 1], QD[qi, 2])
        d = QD[qi, 3]
        H2[d, 3] = -(H2[d, 0] * p[0] + H2[d, 1] * p[1] + H2[d, 2] * p[2])
    return H2


@numba.njit(cache=True)
def pair_energy4(H0, LK, M, QD, OPP):
    H = constrain(H0, QD)
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
    lo3 = np.full(3, 1e300); hi3 = np.full(3, -1e300)
    for X in range(n):
        for i in range(M[X]):
            for q in range(3):
                lo3[q] = min(lo3[q], P3[X, i, q]); hi3[q] = max(hi3[q], P3[X, i, q])
    diam = np.sqrt(((hi3 - lo3) ** 2).sum()); cmax = max(np.abs(lo3).max(), np.abs(hi3).max())
    if diam < 1e-3 * (1.0 + cmax):
        return 99, 0.0
    cross = 0; short = 0
    for X in range(n):
        m = M[X]
        for i in range(m):
            dv = P3[X, i] - P3[X, i - 1 if i > 0 else m - 1]
            if np.sqrt((dv ** 2).sum()) < 1e-6 * diam:
                short += 1
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
    QP = np.zeros((QD.shape[0], 3))
    for qi in range(QD.shape[0]):
        QP[qi] = _solve3(H, QD[qi, 0], QD[qi, 1], QD[qi, 2])
    bad = short; over = 0.0
    crit = np.zeros(4 * mmax + 4); sh0 = np.zeros(mmax); sh1 = np.zeros(mmax)
    for X in range(n):
        for Y in range(X + 1, n):
            d = np.cross(H[X, :3], H[Y, :3]); dd = (d ** 2).sum()
            A = np.empty((3, 3)); A[0] = H[X, :3]; A[1] = H[Y, :3]; A[2] = d
            p0 = np.linalg.solve(A, np.array([-H[X, 3], -H[Y, 3], 0.0]))
            nc = 0; ns = 0
            for qi in range(QD.shape[0]):              # opposite faces of a quad touch at its point
                for k in range(2):
                    if OPP[qi, k, 0] == X and OPP[qi, k, 1] == Y:
                        crit[nc] = ((QP[qi] - p0) @ d) / dd; nc += 1
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
            # the 4-valent point must not lie on the shared edge of two opposite faces of its quad
            # (lesson of the first run: the annealer routed that edge through the point)
            isbad = False
            for qi in range(QD.shape[0]):
                for k in range(2):
                    if OPP[qi, k, 0] == X and OPP[qi, k, 1] == Y:
                        tq = ((QP[qi] - p0) @ d) / dd
                        for s in range(ns):
                            if sh0[s] - 1e-9 * (sh1[s] - sh0[s] + 1e-12) <= tq <= sh1[s] + 1e-9 * (sh1[s] - sh0[s] + 1e-12):
                                isbad = True
            cs = np.sort(crit[:nc])
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
    return cross + bad, over


def energy(H, pk):
    try:
        e, o = pair_energy4(H, *pk)
    except Exception:
        return 1e9
    return e + 0.01 * np.tanh(o)


def anneal(pk, n, rng, minutes, steps=40000):
    best = (1e9, None); t0 = time.monotonic()
    while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
        H = rng.standard_normal((n, 4)); H[:, :3] /= np.linalg.norm(H[:, :3], axis=1)[:, None]
        cur = energy(H, pk); bl = (cur, H.copy()); T = 1.5
        for _ in range(steps):
            H2 = H.copy(); k = int(rng.integers(n)); sig = float(rng.choice([0.01, 0.05, 0.2]))
            H2[k] += sig * rng.standard_normal(4); H2[k, :3] /= np.linalg.norm(H2[k, :3])
            c2 = energy(H2, pk)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                H, cur = H2, c2
                if cur < bl[0]:
                    bl = (cur, H.copy())
            T = max(0.03, T * 0.9998)
            if bl[0] < 0.5 or time.monotonic() - t0 > 60 * minutes:
                break
        if bl[0] < best[0]:
            best = bl
    return best


def cma_search(pk, n, rng, minutes):
    if not hasattr(np, 'Inf'):
        np.Inf = np.inf
    import cma
    best = (1e9, None); t0 = time.monotonic(); runs = 0
    def f(x):
        H = np.asarray(x, float).reshape(n, 4).copy(); nr = np.linalg.norm(H[:, :3], axis=1)
        if np.any(nr < 1e-6):
            return 1e6
        H[:, :3] /= nr[:, None]; H[:, 3] /= nr
        return energy(H, pk)
    while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
        runs += 1
        es = cma.CMAEvolutionStrategy(rng.standard_normal(4 * n), 0.5, {'seed': int(rng.integers(1 << 30)), 'verbose': -9,
                                      'popsize': int(4 + 3 * np.log(4 * n)) * (2 ** (runs % 4)), 'tolflatfitness': 50})
        while not es.stop() and time.monotonic() - t0 < 60 * minutes:
            X = es.ask(); F = [f(x) for x in X]; es.tell(X, F)
            i = int(np.argmin(F))
            if F[i] < best[0]:
                H = np.array(X[i]).reshape(n, 4); nr = np.linalg.norm(H[:, :3], axis=1); H[:, :3] /= nr[:, None]; H[:, 3] /= nr
                best = (F[i], H)
            if best[0] < 0.5:
                break
    return best


if __name__ == '__main__':
    nmaps, minutes, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    engine = sys.argv[5] if len(sys.argv) > 5 else 'anneal'
    rng = np.random.default_rng(seed); results = []
    for mi in range(nmaps):
        m = None; tries = 0
        while m is None:
            m = random_map4(8, 2, rng); tries += 1
        pk = pack4(m)
        b, H = (anneal if engine == 'anneal' else cma_search)(pk, 8, rng, minutes)
        Hc = constrain(H, pk[2]) if H is not None else None
        print('map %d (%d tries, quads %s): %s best %.3f' % (mi, tries, m['quads'], engine, b), flush=True)
        results.append({'links': {str(k): v for k, v in m['links'].items()}, 'quads': m['quads'], 'dep': m['dep'],
                        'planes': Hc.tolist() if Hc is not None else None, 'best_fast': float(b)})
        json.dump(results, open(out, 'w'))
        if b < 0.5:
            print('!!! ZERO (float) on map', mi, flush=True)
