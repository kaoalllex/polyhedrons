"""Normals-first ladder step (review 2026-10-30, test T3 / direction 1): for an ARM (an exactly embedded
polyhedron H of the map M and a next map M + tau, one handle more) anneal the face normals, staying within
a radius of the seed normals, until the gauge normals pass the exact Gauss gate of M + tau
(degree 1 - g', positive covering, at least 2 g' + 1 saddles), then decide the plane offsets EXACTLY with
fixed_normals_gauge.solve_gauge (z3, sub-map encoding). SAT = an exact genus g' polyhedron (re-checked with
ladder_exact); UNSAT = these normals with this gauge admit no embedding. Every decided normal set is logged.

Gauge (face orientation) modes:
  tube    faces outside the handle keep the seed polyhedron's orientation, the six handle faces are free
          (default: no polygon outside the tube has to reverse);
  free    all twelve are free, each reversal of a face outside the tube costs `--rev-cost`;
  fixed   one given gauge (`--gauge +1,-1,...`), e.g. an admissible gauge listed by gauss_gate.py T1.
The seed gauge is the realized polyhedron's own orientation; at all saved type-0 genus-3 seeds the
next-map degree in it is 1 - g (k_tau = 0, review 2.1), so the normals must move.

Usage (one arm):  python3 -I normals_first.py LEVEL_JSON ARM_INDEX MINUTES SEED OUT_JSONL
        [--radius R1,R2,...] [--mode tube|free|fixed] [--gauge ...] [--timeout S] [--anneal-minutes M]
  ARM_INDEX: index into gauss_gate.arms_of(LEVEL) (extendable next handles), or 'all' (round robin).
A free (seedless) map, e.g. a full genus-6 type: `--map TRIANGLES_JSON TYPE_ID` instead of LEVEL_JSON ARM_INDEX
uses radius infinity and random start normals (direction 5 of the review).
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import coherent_triangles, links_from
import gauss_gate as GG


# ----------------------------------------------------------------------------- float class energy

class ClassEnergy:
    """Float energy of gauge normals for the Gauss gate of one oriented map (annealing only; every
    zero is re-checked exactly by gauss_gate)."""

    def __init__(self, otris, target, min_saddles, n_samples, rng):
        self.T = np.array(otris, np.int64)
        self.target = target
        self.min_saddles = min_saddles
        U = rng.standard_normal((n_samples, 3))
        self.U = U / np.linalg.norm(U, axis=1)[:, None]

    def __call__(self, G):
        T, U = self.T, self.U
        A, B, C = G[T[:, 0]], G[T[:, 1]], G[T[:, 2]]
        d = np.einsum('ij,ij->i', A, np.cross(B, C))
        s = np.sign(d)
        inside = ((U @ np.cross(B, C).T) * s > 0) & ((U @ np.cross(C, A).T) * s > 0) & ((U @ np.cross(A, B).T) * s > 0)
        pos = (inside & (s > 0)).sum(axis=1)
        neg = (inside & (s < 0)).sum(axis=1)
        deg = pos - neg
        dmed = int(np.median(deg))
        sad = int((s < 0).sum())
        # conditioning: tiny |det| of a triangle's normals = vertex near infinity; keep away from it
        weak = int((np.abs(d) < 1e-3).sum())
        e = (10 * abs(dmed - self.target) + int((pos == 0).sum()) + int((deg != dmed).sum())
             + 3 * max(0, self.min_saddles - sad) + weak)
        return e, dmed, sad


# ----------------------------------------------------------------------------- one normal set

def anneal_normals(Nseed, eps0, free, rev_cost, energy, rng, radius, minutes, start=None):
    """Anneal unit normals (each within `radius` radians of its seed) and the gauge signs of the
    `free` faces. Returns (normals, gauge, energy) of the best state."""
    n = len(Nseed)
    Nc = (Nseed.copy() if start is None else start[0].copy())
    eps = (np.array(eps0) if start is None else np.array(start[1]))

    def cost(Nx, ex):
        e, d, s = energy(ex[:, None] * Nx)
        return e + rev_cost * int(sum(1 for X in range(n) if ex[X] != eps0[X] and X not in free))

    E = cost(Nc, eps); best = (E, Nc.copy(), eps.copy())
    Tmp = 2.0; t0 = time.monotonic(); it = 0
    while best[0] > 0 and time.monotonic() - t0 < 60 * minutes:
        it += 1
        N2 = Nc.copy(); e2 = eps.copy()
        k = int(rng.integers(n))
        if free and rng.random() < 0.08:
            k = list(free)[int(rng.integers(len(free)))]
            e2[k] = -e2[k]
        else:
            N2[k] += float(rng.choice([0.003, 0.01, 0.03, 0.1])) * rng.standard_normal(3)
            N2[k] /= np.linalg.norm(N2[k])
            if radius is not None and np.arccos(np.clip(N2[k] @ Nseed[k], -1, 1)) > radius:
                continue
        E2 = cost(N2, e2)
        if E2 <= E or rng.random() < np.exp((E - E2) / Tmp):
            Nc, eps, E = N2, e2, E2
            if E < best[0]:
                best = (E, Nc.copy(), eps.copy())
        Tmp = max(0.05, Tmp * 0.9995)
    return best[1], [int(x) for x in best[2]], best[0], it


def exact_gate(Nf, eps, otris, target, min_saddles, n_cover=256, seed=0):
    """Integer normals (scale 1e6) and the exact gate: degree, covering, saddles, no coplanar triple."""
    N = [[int(round(v * GG.SCALE)) for v in x] for x in Nf]
    try:
        adm, _ = GG.admissible(N, otris, target, n_cover=n_cover, seed=seed, eps=[eps])
    except ValueError:
        return N, False, 'degenerate'
    if not adm:
        return N, False, 'gauss'
    if GG.saddles(N, otris, eps) < min_saddles:
        return N, False, 'saddles'
    return N, True, 'ok'


# ----------------------------------------------------------------------------- arm loop

def run_arm(Hseed, tris_M, tris_R, tube, minutes, rng, out, radii=(0.1, 0.2, 0.4, 0.8), mode='tube',
            fixed_gauge=None, rev_cost=2, timeout=600, anneal_minutes=2.0, tag='', log=print):
    from fixed_normals_gauge import solve_gauge
    from ladder_exact import verify
    n = len(tris_R) and max(max(t) for t in tris_R) + 1
    gR = GG.genus(tris_R, n); target = 1 - gR; min_sad = 2 * gR + 1
    six = set(tube[0]) | set(tube[1]) if tube else set(range(n))
    if Hseed is not None:
        oM, oR = GG.aligned_orientations(tris_M, tris_R, n)
        eps_seed = GG.own_gauge(Hseed, links_from(oM, n))
        Nseed = GG.unit_planes(Hseed)[:, :3]
    else:
        oR = coherent_triangles([tuple(t) for t in tris_R])
        eps_seed = [1] * n
        Nseed = rng.standard_normal((n, 3)); Nseed /= np.linalg.norm(Nseed, axis=1)[:, None]
        radii = (None,)
    if mode == 'fixed':
        eps0, free = list(fixed_gauge), set()
    elif mode == 'free':
        eps0, free = list(eps_seed), set(range(n))
    else:
        eps0, free = list(eps_seed), set(six)
    LR = links_from(oR, n)
    energy = ClassEnergy(oR, target, min_sad, 2000, rng)
    t0 = time.monotonic(); k = 0; stats = {}
    while time.monotonic() - t0 < 60 * minutes:
        radius = radii[k % len(radii)]; k += 1
        start = None
        if Hseed is None:
            S = rng.standard_normal((n, 3)); S /= np.linalg.norm(S, axis=1)[:, None]
            start = (S, eps0); Nbase = S
        else:
            Nbase = Nseed
        Nf, eps, e, it = anneal_normals(Nbase, eps0, free if mode != 'free' else set(range(n)),
                                        rev_cost if mode == 'free' else 0, energy, rng,
                                        radius if Hseed is not None else None, anneal_minutes, start)
        rec = {'tag': tag, 'tube': [list(t) for t in tube] if tube else None, 'genus': gR, 'radius': radius,
               'mode': mode, 'anneal_energy': int(e), 'anneal_iterations': it, 'gauge': eps,
               'reversed_outside_tube': [X for X in range(n) if eps[X] != eps_seed[X] and X not in six]}
        if Hseed is not None:
            rec['max_angle'] = float(np.max(np.arccos(np.clip(np.einsum('ij,ij->i', Nf, Nseed), -1, 1))))
        if e > 0:
            rec['status'] = 'NO_ADMISSIBLE_NORMALS'
        else:
            N, ok, why = exact_gate(Nf, eps, oR, target, min_sad)
            rec['normals'] = N
            if not ok:
                rec['status'] = 'EXACT_GATE_FAILED_' + why
            else:
                G = [[g * v for v in x] for g, x in zip(eps, N)]
                ts = time.monotonic()
                try:
                    st, Hs = solve_gauge(G, tris_R, timeout_s=timeout)
                except ValueError as ex:
                    st, Hs = 'DEGENERATE', None
                rec['status'] = st; rec['smt_seconds'] = round(time.monotonic() - ts, 1)
                if st == 'SAT':
                    ex = verify(Hs, LR, require_all_pairs=(gR == (n - 3) * (n - 4) // 12))
                    rec['exact'] = bool(ex['EMBEDDED']); rec['planes'] = [[int(v) for v in h] for h in Hs]
                    rec['triangles'] = [list(t) for t in tris_R]
        stats[rec['status']] = stats.get(rec['status'], 0) + 1
        with open(out, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        log('%s r=%s: %s%s (anneal E %d, %d it%s)' % (
            tag, radius, rec['status'], ' smt %.0fs' % rec['smt_seconds'] if 'smt_seconds' in rec else '',
            rec['anneal_energy'], it, ', max angle %.2f' % rec['max_angle'] if 'max_angle' in rec else ''))
        if rec.get('exact'):
            log('!!! %s: genus %d REALIZED EXACTLY (normals first)' % (tag, gR))
            return rec, stats
    return None, stats


def main():
    a = sys.argv[1:]

    def opt(name, default, conv=str):
        if name in a:
            i = a.index(name); v = a[i + 1]; del a[i:i + 2]; return conv(v)
        return default
    radii = tuple(float(x) for x in opt('--radius', '0.1,0.2,0.4,0.8').split(','))
    mode = opt('--mode', 'tube'); timeout = opt('--timeout', 600.0, float)
    am = opt('--anneal-minutes', 2.0, float); gauge = opt('--gauge', None)
    rev_cost = opt('--rev-cost', 2, int)
    fixed = [int(x) for x in gauge.split(',')] if gauge else None
    if a[0] == '--map':
        types = json.load(open(a[1])); tid = int(a[2]); minutes, seed, out = float(a[3]), int(a[4]), a[5]
        ent = next(e for e in types if e['id'] == tid)
        rng = np.random.default_rng(seed)
        run_arm(None, None, [tuple(t) for t in ent['triangles']], None, minutes, rng, out, mode='free',
                rev_cost=0, timeout=timeout, anneal_minutes=am, tag='type%d' % tid,
                log=lambda *x: print(time.strftime('%H:%M:%S'), *x, flush=True))
        return
    lv = json.load(open(a[0])); idx = a[1]; minutes, seed, out = float(a[2]), int(a[3]), a[4]
    rng = np.random.default_rng(seed)
    H = lv['planes']; tris = [tuple(t) for t in lv['triangles']]; n = len(H)
    arms = GG.arms_of(H, tris, n)
    sel = range(len(arms)) if idx == 'all' else [int(idx)]
    per = minutes / len(sel)
    for i in sel:
        t1, t2, R = arms[i]
        rec, stats = run_arm(H, tris, R, (t1, t2), per, rng, out, radii, mode, fixed, rev_cost, timeout, am,
                             tag='%s arm %d %s-%s' % (os.path.basename(a[0]), i, t1, t2),
                             log=lambda *x: print(time.strftime('%H:%M:%S'), *x, flush=True))
        print('arm %d: %s' % (i, stats), flush=True)
        if rec:
            json.dump(rec, open(out.rsplit('.', 1)[0] + '_REALIZED_arm%d.json' % i, 'w'))
            break


if __name__ == '__main__':
    main()
