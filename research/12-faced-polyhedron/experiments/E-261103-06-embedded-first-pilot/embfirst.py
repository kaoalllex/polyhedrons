"""Embedded first, planar later: flatten the 7 regions of a K7 torus mesh without leaving embedding (R1 pilot)."""
import argparse
import itertools
import json
import math
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(HERE.parent / 'E-261103-05-s5-symmetric-solid-first'))
ENERGY_STOP = 1e-12
DAMP = 0.05  # Tikhonov damping of the vertex correction (near-parallel planes make the plain solve explode)


def lattice_metric(j):
    """Linear map sending the lattice {(k/7, jk/7)} + Z^2 to a triangular lattice (hexagonal Voronoi cells)."""
    pts = [np.array([k / 7 + a, j * k / 7 + b]) for k in range(7) for a in (-1, 0, 1) for b in (-1, 0, 1)]
    pts = [p for p in pts if np.linalg.norm(p) > 1e-9]
    b1 = min(pts, key=np.linalg.norm)
    b2 = min((p for p in pts if abs(b1[0] * p[1] - b1[1] * p[0]) > 1e-9), key=np.linalg.norm)
    if np.dot(b1, b2) < 0:
        b2 = -b2
    # reduce so that b1, b2, b2 - b1 are the three shortest directions
    if np.linalg.norm(b2 - b1) < np.linalg.norm(b2):
        b2 = b2 - b1
    return np.array([[1, .5], [0, math.sqrt(3) / 2]]) @ np.linalg.inv(np.column_stack([b1, b2]))


def build_mesh(N, R, r, j):
    """N x N grid on R^2/Z^2 mapped to a torus; triangle -> region (0..6) by hexagonal Voronoi cell."""
    idx = lambda i, k: (i % N) * N + (k % N)
    uv = np.array([(i / N, k / N) for i in range(N) for k in range(N)])
    th, ph = 2 * np.pi * uv[:, 0], 2 * np.pi * uv[:, 1]
    X = np.column_stack([(R + r * np.cos(ph)) * np.cos(th), (R + r * np.cos(ph)) * np.sin(th), r * np.sin(ph)])
    tris = []
    for i in range(N):
        for k in range(N):
            a, b, c, d = idx(i, k), idx(i + 1, k), idx(i + 1, k + 1), idx(i, k + 1)
            tris += [(a, b, c), (a, c, d)]
    tris = np.array(tris)
    M = lattice_metric(j)
    cen = uv[tris].mean(axis=1)
    # centroids of triangles straddling the seam: recompute from unwrapped coordinates
    base = uv[tris[:, 0]]
    delta = (uv[tris] - base[:, None, :] + .5) % 1 - .5
    cen = base + delta.mean(axis=1)
    best = np.full(len(tris), np.inf); region = np.zeros(len(tris), int)
    for k in range(7):
        for a in (-2, -1, 0, 1, 2):
            for b in (-2, -1, 0, 1, 2):
                c = np.array([k / 7 + a, (j * k / 7) + b])
                dist = np.linalg.norm((cen - c) @ M.T, axis=1)
                better = dist < best
                best[better] = dist[better]; region[better] = k
    return X, tris, region


def region_vertices(tris, region):
    return [np.unique(tris[region == k]) for k in range(7)]


def adjacency_ok(rv):
    return all(set(rv[a]) & set(rv[b]) for a, b in itertools.combinations(range(7), 2))


def fit_planes(X, rv):
    """Best-fit planes (n, d) with |n| = 1 and the energy sum of squared distances."""
    planes, energy = [], 0.0
    for v in rv:
        P = X[v]; c = P.mean(axis=0)
        w, U = np.linalg.eigh((P - c).T @ (P - c))
        planes.append((U[:, 0], U[:, 0] @ c)); energy += max(w[0], 0.0)
    return planes, energy


def planarity_energy(P):
    P = np.asarray(P, float); c = P.mean(axis=0)
    return max(np.linalg.eigvalsh((P - c).T @ (P - c))[0], 0.0)


def pair_hits(X, A, B):
    """Boolean per triangle pair (rows of A and B): some edge of one pierces the other (edges at shared vertices skipped)."""
    hit = np.zeros(len(A), bool)
    for S, T in ((A, B), (B, A)):
        tv = X[T]
        for e0, e1 in ((0, 1), (1, 2), (2, 0)):
            free = ~(((S[:, e0][:, None] == T).any(axis=1)) | ((S[:, e1][:, None] == T).any(axis=1)))
            if not free.any():
                continue
            p, q, t0, t1, t2 = X[S[free, e0]], X[S[free, e1]], tv[free, 0], tv[free, 1], tv[free, 2]
            dvec = q - p; e1v, e2v = t1 - t0, t2 - t0
            h = np.cross(dvec, e2v); a = np.einsum('ij,ij->i', e1v, h)
            ok = np.abs(a) > 1e-14
            f = np.where(ok, 1 / np.where(ok, a, 1), 0); s = p - t0
            u = f * np.einsum('ij,ij->i', s, h); qv = np.cross(s, e1v)
            v = f * np.einsum('ij,ij->i', dvec, qv); t = f * np.einsum('ij,ij->i', e2v, qv)
            hit[np.flatnonzero(free)[ok & (u > 0) & (v > 0) & (u + v < 1) & (t > 0) & (t < 1)]] = True
    return hit


def candidate_pairs(X, tris):
    cen = X[tris].mean(axis=1)
    rad = np.linalg.norm(X[tris] - cen[:, None, :], axis=2).max()
    return cKDTree(cen).query_pairs(2 * rad, output_type='ndarray')


def intersects(X, tris):
    """True if two non-adjacent triangles cross."""
    pairs = candidate_pairs(X, tris)
    return bool(len(pairs) and pair_hits(X, tris[pairs[:, 0]], tris[pairs[:, 1]]).any())


def vertex_scale(X, tris):
    """Per-vertex 0.25 x distance to the nearest vertex outside its 2-ring."""
    n = len(X); nb = [set() for _ in range(n)]
    for t in tris:
        for a in t:
            nb[a].update(t)
    ring2 = [set(s).union(*(nb[u] for u in s)) for s in nb]
    tree = cKDTree(X); out = np.empty(n)
    for i in range(n):
        for k in (24, 64, n):
            dist, ind = tree.query(X[i], k=min(k, n))
            far = [d for d, j in zip(dist, ind) if j not in ring2[i]]
            if far:
                out[i] = .25 * far[0]; break
    return out


def run_start(name, N, R, r, j, wall, max_steps, log):
    X, tris, region = build_mesh(N, R, r, j)
    rv = region_vertices(tris, region)
    vreg = [[k for k in range(7) if i in set(rv[k])] for i in range(len(X))]
    rec = dict(name=name, N=N, R=R, r=r, j=j, regions_nonempty=[len(v) for v in rv], k7=adjacency_ok(rv),
               start_embedded=not intersects(X, tris))
    planes, e0 = fit_planes(X, rv); rec['energy_start'] = e0
    trace = []; stats = dict(cap=0, barrier=0, accepted=0, rejected_all=0); t_end = time.monotonic() + wall
    if not (rec['k7'] and rec['start_embedded']):
        rec.update(status='BAD-START'); return rec, X, planes
    step = 0; status = 'MAX-STEPS'
    while step < max_steps and time.monotonic() < t_end:
        planes, e = fit_planes(X, rv)
        if step % 25 == 0:
            trace.append((step, e)); log(f'{name} step {step} energy {e:.3e}')
        if e < ENERGY_STOP:
            status = 'CONVERGED'; break
        if len(trace) > 12 and e > .999 * trace[-12][1] and step % 25 == 0:
            status = 'PLATEAU'; break
        D = np.zeros_like(X)
        for i, regs in enumerate(vreg):
            A = np.array([planes[k][0] for k in regs]); d = np.array([planes[k][1] for k in regs])
            D[i] = A.T @ np.linalg.solve(A @ A.T + DAMP * np.eye(len(A)), d - A @ X[i])
        cap = vertex_scale(X, tris); mag = np.linalg.norm(D, axis=1)
        clip = np.minimum(1.0, cap / np.maximum(mag, 1e-300)); capped = bool((clip < 1.0).any())
        D = D * clip[:, None]; t = 1.0; moved = False
        for _ in range(8):
            if not intersects(X + t * D, tris):
                X = X + t * D; moved = True; break
            stats['barrier'] += 1; t /= 2
        if not moved:
            stats['rejected_all'] += 1; status = 'BLOCKED'; break
        stats['accepted'] += 1; stats['cap'] += capped; step += 1
    planes, e = fit_planes(X, rv)
    rec.update(status=status, energy_end=e, steps=step, stats=stats, trace=trace,
               end_embedded=not intersects(X, tris), seconds=time.monotonic() - (t_end - wall))
    return rec, X, planes


def tail(planes, name, out):
    """Exact tail: round planes, solid-first (E = 21, one run per pair), verify_candidate --target S5."""
    import pilot as base
    from solid_cpsat import best_solid
    from solid_fast import Tables
    from ladder_exact import verify
    res = dict(name=name)
    for scale in (10 ** 3, 10 ** 4, 10 ** 6):
        try:
            h = base.integer_planes([[int(round(scale * x)) for x in (*n, -d)] for n, d in planes])
            a = base.arrangement(h); T = Tables(a)
            cells, info = best_solid(a, T, time_limit=60, max_runs=1, target_edges=21)
        except (ValueError, ArithmeticError) as exc:
            res[f'scale_{scale}'] = 'ERROR ' + repr(exc); continue
        res[f'scale_{scale}'] = info
        if cells is None:
            continue
        solid = {T.cells[i] for i, v in enumerate(cells) if v}
        links = base.extract_links(a, solid)
        path = out / f'{name}.candidate.json'; path.write_text(json.dumps(dict(planes=h, links=links)))
        p = subprocess.run([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(path), '--target', 'S5'],
                           capture_output=True, text=True)
        res.update(scale=scale, verify_stdout=p.stdout.strip(), PASS=p.returncode == 0)
        return res
    res['PASS'] = False
    return res


def controls(out, log):
    c = {}
    rng = np.random.default_rng(0)
    flat = np.column_stack([rng.normal(size=(40, 2)), np.zeros(40)]) @ np.linalg.qr(rng.normal(size=(3, 3)))[0]
    c['energy_coplanar'] = planarity_energy(flat)
    c['energy_random'] = planarity_energy(rng.normal(size=(40, 3)))
    X, tris, region = build_mesh(28, 2.0, 0.7, 2)
    c['energy_round_torus_start'] = fit_planes(X, region_vertices(tris, region))[1]
    Xs, trs, _ = build_mesh(28, .5, 1.0, 2)
    c['detector_spindle_torus_intersects'] = bool(intersects(Xs, trs))
    c['detector_round_torus_intersects'] = bool(intersects(X, tris))
    d = json.loads((ROOT / 'experiments/E-261101-25-chirotope-first/szilassi_control.json').read_text())
    prng = random.Random(1)
    h = [[100 * int(x) + prng.randint(-3, 3) for x in p] for p in d['planes']]
    pl = lambda rows: [(np.array(r[:3], float) / np.linalg.norm(r[:3]), -r[3] / np.linalg.norm(r[:3])) for r in rows]
    c['tail_szilassi_perturbed'] = tail([(n, d_) for n, d_ in pl(h)], 'ctrl_szilassi', out)
    bad = [r[:] for r in h]; bad[0][3] += 400; bad[3][0] += 900
    c['tail_szilassi_one_plane_moved'] = tail(pl(bad), 'ctrl_szilassi_bad', out)
    c['PASS'] = (c['energy_coplanar'] < 1e-20 and c['energy_random'] > 1e-3 and c['energy_round_torus_start'] > 1e-3
                 and c['detector_spindle_torus_intersects'] and not c['detector_round_torus_intersects']
                 and c['tail_szilassi_perturbed'].get('PASS') and not c['tail_szilassi_one_plane_moved'].get('PASS'))
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True); ap.add_argument('--wall', type=float, default=600)
    ap.add_argument('--steps', type=int, default=5000); ap.add_argument('--N', type=int, default=28)
    ap.add_argument('--starts', type=int, default=6); ap.add_argument('--controls-only', action='store_true')
    ap.add_argument('--workers', type=int, default=1)
    args = ap.parse_args(); out = args.out; out.mkdir(parents=True, exist_ok=False)
    log = lambda s: print(s, flush=True)
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
                    started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), args={k: str(v) for k, v in vars(args).items()})
    t0 = time.monotonic()
    ctrl = controls(out, log); (out / 'controls.json').write_text(json.dumps(ctrl, indent=1, default=str))
    log('controls PASS' if ctrl['PASS'] else 'CONTROLS FAILED: ' + json.dumps(ctrl, default=str))
    result = dict(controls_pass=ctrl['PASS'], starts={})
    if ctrl['PASS'] and not args.controls_only:
        starts = list(itertools.product((2.0, 3.0), (2, 3, 4)))[:args.starts]
        for Rr, j in starts:
            name = f'R{Rr:g}_j{j}'
            rec, X, planes = run_start(name, args.N, Rr, 1.0, j, args.wall, args.steps, log)
            if rec['status'] == 'CONVERGED':
                rec['tail'] = tail(planes, name, out)
            (out / f'{name}.json').write_text(json.dumps(rec, indent=1, default=str)); np.save(out / f'{name}.X.npy', X)
            result['starts'][name] = {k: rec.get(k) for k in ('status', 'energy_start', 'energy_end', 'steps', 'stats', 'end_embedded', 'seconds')}
            result['starts'][name]['PASS'] = rec.get('tail', {}).get('PASS')
            (out / 'summary.json').write_text(json.dumps(result, indent=1, default=str))
    manifest.update(ended_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), wall_seconds=time.monotonic() - t0,
                    core_hours=(time.monotonic() - t0) / 3600)
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1)); (out / 'summary.json').write_text(json.dumps(result, indent=1, default=str))


if __name__ == '__main__':
    main()
