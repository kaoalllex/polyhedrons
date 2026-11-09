"""E-261109-04: boundary of the union of two projectively matched exact solids (see PLAN.md).
Usage: python3 union.py SHARD SHARDS OUT_DIR   (controls first, then this shard's slice of the frozen samples)."""
import hashlib, itertools, json, random, sys, time
from fractions import Fraction as Fr
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
import numpy as np
from szilassi import load_szilassi
from planes import planes_from_polyhedron
from solid_first import Arrangement, evaluate, boundary_euler, cell_graph
from q17_winding import winding

T1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [Fr(1, 20), Fr(1, 30), Fr(1, 40), 1]]
MAGS = [Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 2), Fr(2), Fr(3), Fr(4)]
N_WANT, MAX_CORR, MAX_DRAW_B = 128, 4000, 2000


# ---------------------------------------------------------------- exact helpers
def det(M):
    M = [[Fr(x) for x in r] for r in M]; n = len(M); d = Fr(1)
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i] != 0), None)
        if p is None:
            return Fr(0)
        if p != i:
            M[i], M[p] = M[p], M[i]; d = -d
        d *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] -= f * M[i][c]
    return d


def inv(M):
    n = len(M); A = [[Fr(x) for x in r] + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for i in range(n):
        p = next(r for r in range(i, n) if A[r][i] != 0)
        A[i], A[p] = A[p], A[i]
        A[i] = [x / A[i][i] for x in A[i]]
        for r in range(n):
            if r != i and A[r][i] != 0:
                f = A[r][i]; A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    return [r[n:] for r in A]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def tr(A):
    return [list(r) for r in zip(*A)]


def apply(M, verts):
    """Homogeneous map of points; returns the points and 'all w of one sign'."""
    out, ws = [], []
    for v in verts:
        h = [sum(M[i][j] * x for j, x in enumerate((*v, 1))) for i in range(4)]
        ws.append(h[3]); out.append(tuple(h[i] / h[3] if h[3] != 0 else None for i in range(3)))
    ok = all(w > 0 for w in ws) or all(w < 0 for w in ws)
    return out, ok


def prim(h):
    """Canonical integer representative of a projective plane vector."""
    from math import gcd, lcm
    den = lcm(*(Fr(x).denominator for x in h))
    h = [int(Fr(x) * den) for x in h]
    g = 0
    for x in h:
        g = gcd(g, abs(x))
    h = [x // g for x in h]
    return tuple(h) if next(x for x in h if x != 0) > 0 else tuple(-x for x in h)


def orient_faces(faces):
    faces = [list(f) for f in faces]
    de = lambda f: {(f[i], f[(i + 1) % len(f)]) for i in range(len(f))}
    done, stack = {0}, [0]
    while stack:
        a = stack.pop(); ea = de(faces[a])
        for b in range(len(faces)):
            if b in done:
                continue
            eb = de(faces[b])
            if any((y, x) in ea for x, y in eb):
                pass
            elif any(e in ea for e in eb):
                faces[b] = faces[b][::-1]
            else:
                continue
            done.add(b); stack.append(b)
    assert len(done) == len(faces)
    return faces


def base_solid():
    verts, faces = load_szilassi()
    faces = orient_faces(faces)
    vb, ok = apply(T1, verts)
    assert ok, 'T1: pole meets the Szilassi vertices'
    H = [prim(h) for h in planes_from_polyhedron(vb, faces)]
    for X, Y, Z in itertools.combinations(range(7), 3):
        assert det([H[X][:3], H[Y][:3], H[Z][:3]]) != 0, 'base planes without a triple point'
    return vb, faces, H


def proportional(h, g):
    return all(h[i] * g[j] == h[j] * g[i] for i in range(4) for j in range(4))


# ---------------------------------------------------------------- the union
def general(H):
    n = len(H)
    return (all(det([H[a][:3], H[b][:3], H[c][:3]]) != 0 for a, b, c in itertools.combinations(range(n), 3))
            and all(det([H[a], H[b], H[c], H[d]]) != 0 for a, b, c, d in itertools.combinations(range(n), 4)))


def solid_cells(A, polys):
    keys = list(A.bounded)
    cen = np.array([np.mean(A.cells[k], axis=0) for k in keys])
    w = winding(polys, cen)
    wi = np.rint(w).astype(int)
    if wi.sum() < 0:
        wi = -wi
    return {k for k, x in zip(keys, wi) if x == 1}, float(np.max(np.abs(w - np.rint(w))))


def union_metrics(copies):
    """copies: list of (verts, oriented faces, plane list). Returns the counters of the union boundary."""
    planes = []
    for _, _, H in copies:
        for h in H:
            h = prim(h)
            if h not in planes:
                planes.append(h)
    if not general(planes):
        return dict(valid=False, reason='arrangement not general')
    A = Arrangement(np.array(planes, float))
    S, dev = set(), 0.0
    for verts, faces, _ in copies:
        polys = [np.array([[float(c) for c in verts[i]] for i in f]) for f in faces]
        s, d = solid_cells(A, polys)
        S |= s; dev = max(dev, d)
    _, d = evaluate(A, S, detail=True)
    nb = cell_graph(A); seen, comps = set(), 0
    for k in S:
        if k in seen:
            continue
        comps += 1; stack = [k]; seen.add(k)
        while stack:
            for x in nb[stack.pop()]:
                if x in S and x not in seen:
                    seen.add(x); stack.append(x)
    n = len(planes); chi = boundary_euler(A, S)
    m = dict(valid=dev < 1e-3, reason='' if dev < 1e-3 else 'winding deviation', planes=n, cells=len(S), s_components=comps, chi=chi,
             face_bad=d['faces'], disk_bad=d['disks'], diag=d['diagonal_edges'], bad_vertices=d['bad_vertices'],
             missing=d['missing'], adj_bad=d['adjacency'], pairs=n * (n - 1) // 2 - d['missing'], winding_dev=dev)
    m['target_like'] = bool(m['valid'] and n == 10 and not (m['face_bad'] or m['disk_bad'] or m['diag'] or m['bad_vertices'])
                            and chi == -6 and comps == 1)
    m['all_pairs'] = bool(m['target_like'] and m['missing'] == 0 and m['adj_bad'] == 0)
    return m


# ---------------------------------------------------------------- copies
def copy_by_map(base, tau, sigma, lam):
    vb, faces, H = base
    Bt = tr([H[i] for i in tau]); Ls = tr([[l * x for x in H[s]] for l, s in zip(lam, sigma)])
    if det(Bt) == 0 or det(tr([H[i] for i in sigma])) == 0:
        return None, 'dependent plane set'
    G = mm(Ls, inv(Bt)); M = tr(inv(G))
    v2, ok = apply(M, vb)
    if not ok:
        return None, 'pole meets copy 2'
    H2 = [prim(h) for h in planes_from_polyhedron(v2, faces)]
    for t, s in zip(tau, sigma):
        assert proportional(H2[t], H[s]), 'matched planes differ'
    return (v2, faces, H2), ''


def tetra(h4):
    """Tetrahedron from 4 planes (integer vectors); None unless bounded."""
    if det(h4) == 0:
        return None
    V = []
    for k in range(4):
        r = [h4[i] for i in range(4) if i != k]
        if det([x[:3] for x in r]) == 0:
            return None
        Mx = inv([x[:3] for x in r]); V.append(tuple(-sum(Mx[i][j] * r[j][3] for j in range(3)) for i in range(3)))
    faces = []
    for i in range(4):
        a, b, c = [k for k in range(4) if k != i]
        u = [V[b][m] - V[a][m] for m in range(3)]; w = [V[c][m] - V[a][m] for m in range(3)]
        nrm = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        out = sum(nrm[m] * (V[i][m] - V[a][m]) for m in range(3))
        faces.append([a, b, c] if out < 0 else [a, c, b])
    return V, faces, [prim(h) for h in h4]


def samples_A(base):
    rng = random.Random(2611090401); out, draws, bad = [], 0, {}
    for _ in range(MAX_CORR):
        tau, sigma = rng.sample(range(7), 4), rng.sample(range(7), 4)
        ratios = [[Fr(1)] + [rng.choice((1, -1)) * rng.choice(MAGS) for _ in range(3)] for _ in range(8)]
        for lam in ratios:
            draws += 1
            c2, why = copy_by_map(base, tau, sigma, lam)
            if c2 is None or not general(list({prim(h) for h in base[2]} | {prim(h) for h in c2[2]})):
                bad[why or 'arrangement not general'] = bad.get(why or 'arrangement not general', 0) + 1
                continue
            out.append(dict(source='A', tau=tau, sigma=sigma, lam=[str(x) for x in lam]))
            if len(out) == N_WANT:
                return out, draws, bad
    return out, draws, bad


def samples_B(base):
    rng = random.Random(2611090402); out, draws, bad = [], 0, {}
    xs = [[float(v[m]) for v in base[0]] for m in range(3)]
    lo, hi = [min(x) for x in xs], [max(x) for x in xs]
    while len(out) < N_WANT and draws < MAX_DRAW_B:
        j = len(out) * 7 // N_WANT; draws += 1
        h = [base[2][j]]
        for _ in range(3):
            n = [rng.randint(-9, 9) for _ in range(3)]
            if not any(n):
                n = [1, 0, 0]
            p = [Fr(round(rng.uniform(lo[m], hi[m]) * 10), 10) for m in range(3)]
            h.append((n[0], n[1], n[2], -sum(n[m] * p[m] for m in range(3))))
        h = [prim(v) for v in h]
        t = tetra(h)
        if t is None or not general(list({prim(x) for x in base[2]} | {prim(x) for x in t[2]})):
            bad['degenerate'] = bad.get('degenerate', 0) + 1
            continue
        out.append(dict(source='B', j=j, planes=[list(x) for x in h]))
    return out, draws, bad


def run_sample(base, s):
    if s['source'] == 'A':
        c2, why = copy_by_map(base, s['tau'], s['sigma'], [Fr(x) for x in s['lam']])
    else:
        c2 = tetra([tuple(x) for x in s['planes']])
    return union_metrics([base, c2])


# ---------------------------------------------------------------- controls
def controls(base):
    res = {}
    one = union_metrics([base])
    res['single'] = one
    for name, idx in (('identical_a', (0, 1, 2, 3)), ('identical_b', (3, 5, 0, 2))):
        c2, _ = copy_by_map(base, idx, idx, [Fr(1)] * 4)
        res[name] = union_metrics([base, c2])
    # negative: copy 2 moved far away by a generic affine map
    vb, faces, H = base
    shift = [[1, Fr(1, 7), 0, 10], [0, 1, Fr(1, 5), 0], [Fr(1, 9), 0, 1, 0], [0, 0, 0, 1]]
    v2, _ = apply(shift, vb)
    res['disjoint'] = union_metrics([base, (v2, faces, [prim(h) for h in planes_from_polyhedron(v2, faces)])])
    key = ('planes', 'face_bad', 'disk_bad', 'diag', 'bad_vertices', 'chi', 's_components', 'pairs', 'missing')
    pos = [tuple(res[k][x] for x in key) for k in ('single', 'identical_a', 'identical_b')]
    ok_pos = all(p == (7, 0, 0, 0, 0, 0, 1, 21, 0) for p in pos) and all(res[k]['winding_dev'] < 1e-6 for k in ('single', 'identical_a', 'identical_b'))
    d = res['disjoint']
    ok_neg = d.get('missing', 0) > 0 and d.get('s_components') == 2
    return ok_pos and ok_neg, res


def main():
    shard, shards, out = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); base = base_solid()
    ok, res = controls(base)
    (out / 'controls.json').write_text(json.dumps(dict(ok=ok, results=res), indent=1, default=str))
    print('controls', 'PASS' if ok else 'FAIL', flush=True)
    if not ok:
        sys.exit(2)
    allsamples = {}
    for name, f in (('A', samples_A), ('B', samples_B)):
        s, draws, bad = f(base); allsamples[name] = (s, draws, bad)
    frozen = json.dumps({k: v[0] for k, v in allsamples.items()}, sort_keys=True)
    (out / 'frozen.json').write_text(json.dumps(dict(sha256=hashlib.sha256(frozen.encode()).hexdigest(),
                                                     counts={k: len(v[0]) for k, v in allsamples.items()},
                                                     draws={k: v[1] for k, v in allsamples.items()},
                                                     rejected={k: v[2] for k, v in allsamples.items()}), indent=1))
    done = set()
    rp = out / 'samples.jsonl'
    if rp.exists():
        done = {(r['source'], r['index']) for r in map(json.loads, rp.read_text().splitlines())}
    with open(rp, 'a') as fh:
        for name, (s, _, _) in allsamples.items():
            for i, smp in enumerate(s):
                if i % shards != shard or (name, i) in done:
                    continue
                try:
                    m = run_sample(base, smp)
                except Exception as e:                       # recorded, never dropped
                    m = dict(valid=False, reason=f'{type(e).__name__}: {e}')
                fh.write(json.dumps(dict(source=name, index=i, sample=smp, **m), default=str) + '\n'); fh.flush()
    print('shard done', round(time.time() - t0, 1), 's')


if __name__ == '__main__':
    main()
