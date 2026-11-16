"""Polar transfer (E-261116-04): the polar planes of a vertex realization in every affine chart.

A vertex realization has points v_i and faces (triangles, or quads for the cube control). The polar objects are the
planes h_i = (v_i, 1) (plane vectors of P^3*). A chart is a plane at infinity l (a vector of R^4); the dual vertices
are the points x_F spanned by the planes of a face F, so the charts fall into the cells of the central arrangement
{l : x_F . l = 0}. One interior point per cell (mod l -> -l) is found by LPs; the planes in that chart are
h M^-1 with M = [e_a, e_b, e_c, l]. Every chart's planes and links go to verification/verify_candidate.py.

Usage (python from the research venv):
  python3 polar_transfer.py control OUT_DIR
  python3 polar_transfer.py map OBJ OUT_DIR [--sample N]     # one realization, all charts
"""
import itertools
import json
import os
import subprocess
import sys
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'code'))
MIN_MARGIN = 1e-7      # cells whose Chebyshev margin (unit x_F, |l|_inf <= 1) is below this are not enumerated


def read_obj(path):
    pts, faces = [], []
    for line in open(path):
        t = line.split()
        if t and t[0] == 'v':
            pts.append(tuple(int(float(x)) if float(x) == int(float(x)) else float(x) for x in t[1:4]))
        elif t and t[0] == 'f':
            faces.append(tuple(int(x.split('/')[0]) - 1 for x in t[1:]))
    return pts, faces


def minor_vec(rows):
    """Integer null vector of three integer rows in Z^4 (signed 3x3 minors); exact."""
    out = []
    for j in range(4):
        cols = [c for c in range(4) if c != j]
        m = [[r[c] for c in cols] for r in rows]
        d = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
             + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        out.append((-1) ** j * d)
    return tuple(out)


def dual_vertices(pts, faces):
    """x_F for every face (integer vectors); every other plane of the face must contain it."""
    H = [tuple(p) + (1,) for p in pts]
    X = []
    for f in faces:
        x = minor_vec([H[i] for i in f[:3]])
        if not any(x):
            raise ValueError('degenerate face %s' % (f,))
        for i in f[3:]:
            if sum(a * b for a, b in zip(H[i], x)):
                raise ValueError('face %s not planar-dual' % (f,))
        X.append(x)
    return H, X


def cells(X):
    """Sign vectors (first sign fixed +1) of the cells of {l : x.l = 0} with an interior point; [(signs, l)]."""
    A = np.array([np.array(x, float) / np.linalg.norm(np.array(x, float)) for x in X])
    n = len(A)

    def cheb(signs):
        k = len(signs)
        S = np.array(signs, float)[:, None] * A[:k]
        res = linprog(c=[0, 0, 0, 0, -1], A_ub=np.hstack([-S, np.ones((k, 1))]), b_ub=np.zeros(k),
                      bounds=[(-1, 1)] * 4 + [(None, 1)], method='highs')
        return (res.x[:4], res.x[4]) if res.status == 0 and res.x[4] > MIN_MARGIN else (None, 0.0)

    live = []
    l0, t0 = cheb([1])
    live.append(([1], l0))
    for k in range(1, n):
        nxt = []
        for signs, l in live:
            s = 1 if A[k] @ l > 0 else -1
            ok_same = abs(A[k] @ l) > MIN_MARGIN
            if ok_same:
                nxt.append((signs + [s], l))
            if not ok_same:
                l3, _ = cheb(signs + [s])
                if l3 is not None:
                    nxt.append((signs + [s], l3))
            l2, _ = cheb(signs + [-s])
            if l2 is not None:
                nxt.append((signs + [-s], l2))
        live = nxt
    return A, live


def chart_planes(H, l):
    d = int(np.argmax(np.abs(l)))
    rows = [np.eye(4)[j] for j in range(4) if j != d] + [l]
    M = np.array(rows)
    P = np.array(H, float) @ np.linalg.inv(M)
    P /= np.linalg.norm(P[:, :3], axis=1)[:, None]
    return P


def links_for(faces):
    """Cyclic neighbour list of every polyhedron-face (= original vertex), from coherently oriented faces."""
    from collections import defaultdict
    n = 1 + max(max(f) for f in faces)
    if all(len(f) == 3 for f in faces):
        import lutz_import
        faces = lutz_import.orient([tuple(f) for f in faces])
    succ = defaultdict(dict)
    for f in faces:
        m = len(f)
        for i in range(m):
            succ[f[i]][f[(i + 1) % m]] = f[i - 1]
    links = {}
    for v in range(n):
        s = min(succ[v]); cyc = [s]
        while succ[v][cyc[-1]] != s:
            cyc.append(succ[v][cyc[-1]])
        if len(cyc) != len(succ[v]):
            raise ValueError('vertex %d link not one cycle' % v)
        links[v] = cyc
    return links


def verify(planes, links, out_dir, name, target):
    path = os.path.join(out_dir, name + '.json')
    json.dump({'planes': planes.tolist(), 'links': {str(k): v for k, v in links.items()}}, open(path, 'w'))
    cmd = [sys.executable, os.path.join(ROOT, 'verification', 'verify_candidate.py'), path]
    if target:
        cmd += ['--target', target]
    p = subprocess.run(cmd, capture_output=True, text=True)
    lines = p.stdout.strip().splitlines()
    try:
        rep = json.loads(lines[0].split(' ', 1)[1])
    except (IndexError, ValueError):
        rep = {'error': (p.stderr or p.stdout).strip()[-300:]}
    return p.returncode == 0, rep, path


def run(pts, faces, out_dir, target, sample=None, keep='failed-none'):
    os.makedirs(out_dir, exist_ok=True)
    H, X = dual_vertices(pts, faces)
    A, live = cells(X)
    links = links_for(faces)
    rng = np.random.default_rng(0)
    # consistency: every sign pattern of random l (normalised to first sign +) must be an enumerated cell
    L = rng.standard_normal((200000, 4))
    sg = np.sign(L @ A.T)
    sg *= sg[:, :1]
    found = {tuple(int(v) for v in r) for r in sg}
    enum = {tuple(s) for s, _ in live}
    missing = len(found - enum)
    todo = live if sample is None else live[:sample]
    res = {'cells': len(live), 'random_patterns': len(found), 'random_not_enumerated': missing, 'tested': 0,
           'embedded': 0, 'pass': 0, 'min_margin': MIN_MARGIN, 'passing_files': []}
    rows = []
    for i, (signs, l) in enumerate(todo):
        planes = chart_planes(H, l)
        ok, line, path = verify(planes, links, out_dir, 'chart', target)
        emb = bool(line.get('EMBEDDED'))
        res['tested'] += 1
        res['embedded'] += emb
        res['pass'] += ok
        rows.append((i, emb, ok))
        if ok:
            keepp = os.path.join(out_dir, 'PASS_chart_%d.json' % i)
            os.replace(path, keepp)
            res['passing_files'].append(keepp)
    chart = os.path.join(out_dir, 'chart.json')
    if os.path.exists(chart):
        os.remove(chart)
    return res, rows


def main():
    a = sys.argv[1:]
    if a[0] == 'control':
        # octahedron -> cube (the verifier needs cubic vertices, so the cube -> octahedron direction is not checkable)
        pts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        faces = []
        for sx, sy, sz in itertools.product((0, 1), repeat=3):
            f = [(0 if sx else 1), (2 if sy else 3), (4 if sz else 5)]
            if sx ^ sy ^ sz ^ 1:
                f.reverse()
            faces.append(tuple(f))
        res, rows = run(pts, faces, a[1], None)
        print(json.dumps(res))
        print('embedded charts %d of %d' % (res['embedded'], res['tested']))
    else:
        pts, faces = read_obj(a[1])
        sample = int(a[a.index('--sample') + 1]) if '--sample' in a else None
        res, rows = run(pts, faces, a[2], 'S6', sample)
        res['obj'] = os.path.basename(a[1])
        json.dump(res, open(os.path.join(a[2], 'result.json'), 'w'))
        print(json.dumps(res))


if __name__ == '__main__':
    main()
