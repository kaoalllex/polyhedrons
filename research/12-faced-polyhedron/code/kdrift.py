"""k-targeted drift (review 2026-10-30, test T2 / direction 2): random plane moves that keep the CURRENT
map realized (float pair energy 0 = an embedded polyhedron at every step, as in drift_search.py) while
driving the handle degree k_tau of the next map M + tau from 0 to -1 (D_{M+tau} = (1 - g) + k_tau must be
1 - g - 1). k_tau depends only on the six handle faces' gauge normals; while they lie in an open hemisphere
k_tau = 0, so the energy is the Gauss-class energy of M + tau in the realized polyhedron's orientation
(normals_first.ClassEnergy parts: 10 |degree - (1 - g')| + 30 x fraction of directions without a robust
positive triangle + saddle shortfall + near-coplanar triples; degree = (1 - g) + k_tau) plus
20 max(0, hemisphere margin + HM_TARGET) (spread the six normals, then wander until the octahedral sphere wraps
negatively and the sphere is covered). Robustness (the first tests reached the class only on its
boundary, margin -0.000, with uncovered slivers): covering is counted with an angular margin
(COVER_MARGIN) and the hemisphere term 20 max(0, margin + HM_TARGET) stays on after k_tau = -1. The six tube vertices are not vertices of the genus-g polyhedron,
so they may pass through infinity freely. (k_tau = -1 alone is not enough: the first test reached it with
an uncovered region and the exact offsets were UNSAT.)
Success = an exactly embedded genus-g polyhedron (re-checked with ladder_exact) at which the arm passes the
Gauss gate T1 (gauss_gate.arm_report): a seed in the right class for normals_first.run_arm.
Usage: python3 -I kdrift.py LEVEL_JSON ARM_INDEX MINUTES SEED OUT_JSON"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import links_from, det3
from ladder import pack, pair_energy
import gauss_gate as GG


COVER_MARGIN = 0.01      # robust positive covering (unit-normal determinants), see ClassEnergy
HM_TARGET = 0.05         # push the six handle normals this far beyond any open hemisphere


def handle_degree(G, sphere):
    """Degree of the oriented triangles `sphere` under gauge normals G (float, generic direction)."""
    u = np.array([0.3141592653, -0.2718281828, 0.9238795325])
    D = 0
    for a, b, c in sphere:
        A, B, C = G[a], G[b], G[c]
        s = np.sign(np.dot(A, np.cross(B, C)))
        if (np.dot(u, np.cross(B, C)) * s > 0 and np.dot(A, np.cross(u, C)) * s > 0 and np.dot(A, np.cross(B, u)) * s > 0):
            D += s
    return int(D)


def drift(H, tris_M, tris_R, tube, minutes, rng, log=print):
    """Returns (record, best planes). record['status']: T1_PASS (exactly embedded, and the realized
    polyhedron's own gauge is admissible for M + tau: degree 1 - g', covering confirmed exactly), K_REACHED
    (k = -1 but T1 fails), or NOT_REACHED."""
    from ladder_exact import verify
    n = len(H)
    H = GG.unit_planes(H)
    oM, oR = GG.aligned_orientations(tris_M, tris_R, n)
    LM = links_from(oM, n)
    K0, M0, _ = pack(LM)
    assert pair_energy(H, K0, M0)[0] == 0, 'the start is not a realization of the current map'
    sM = {frozenset(t) for t in oM}
    sR = {frozenset(t) for t in oR}
    sphere = [t for t in oR if frozenset(t) not in sM] + [(b, a, c) for a, b, c in oM if frozenset((a, b, c)) not in sR]
    six = sorted(set(tube[0]) | set(tube[1]))
    from normals_first import ClassEnergy
    gR = GG.genus(tris_R, n)
    cls = ClassEnergy(oR, 1 - gR, 2 * gR + 1, 3000, rng, cover_margin=COVER_MARGIN)

    def state(Hx):
        eps = GG.own_gauge(Hx, LM)
        G = np.array(eps)[:, None] * Hx[:, :3]
        k = handle_degree(G, sphere)
        hm = GG.hemisphere_margin(G[six])
        cls(G); c = cls.last
        e = (10 * abs(c['degree'] - cls.target) + 30.0 * (c['uncovered'] + c['inconsistent']) / c['samples']
             + 3 * max(0, cls.min_saddles - c['saddles']) + c['weak'] + 20 * max(0.0, hm + HM_TARGET))
        return e, k, hm

    E, k, hm = state(H)
    best = (E, H.copy(), k, hm)
    log('start: k_tau %d, hemisphere margin %.3f, class energy %.2f' % (k, hm, E))
    T = 1.0; t0 = time.monotonic(); steps = acc = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] > 0:
        steps += 1
        H2 = H.copy(); j = int(rng.integers(n))
        if rng.random() < 0.7:
            j = six[int(rng.integers(6))]                   # mostly move the handle faces
        H2[j] += float(rng.choice([0.002, 0.01, 0.04, 0.15])) * rng.standard_normal(4)
        H2[j] /= np.linalg.norm(H2[j, :3])
        try:
            if pair_energy(H2, K0, M0)[0] != 0:
                continue
            E2, k2, hm2 = state(H2)
        except Exception:                                    # noqa: BLE001
            continue
        if E2 <= E or rng.random() < np.exp((E - E2) / T):
            H, E, k, hm = H2, E2, k2, hm2; acc += 1
            if E < best[0]:
                best = (E, H.copy(), k, hm)
                log('  energy %.2f, k_tau %d, margin %.3f at %.0fs (step %d)' % (E, k, hm, time.monotonic() - t0, steps))
        T = max(0.05, T * 0.9998)
    rec = {'tube': [list(t) for t in tube], 'steps': steps, 'accepted': acc, 'k_tau': best[2], 'energy': float(best[0]),
           'hemisphere_margin': best[3], 'planes': best[1].tolist(), 'triangles': [list(t) for t in tris_M]}
    rec['status'] = 'NOT_REACHED'
    if best[2] == -1:
        ex = verify(best[1].tolist(), LM, require_all_pairs=False)
        rec['exact_embedded'] = bool(ex['EMBEDDED'])
        if ex['EMBEDDED']:
            t1 = GG.arm_report(best[1].tolist(), tris_M, tris_R, tube)
            rec['t1'] = {k_: t1.get(k_) for k_ in ('own_degree', 'target_degree', 'k_tau', 'n_admissible', 'min_reversed',
                                                    'n_tube_only', 'hemisphere_margin')}
            rec['status'] = 'T1_PASS' if t1.get('min_reversed') == 0 else 'K_REACHED'
    return rec, best[1]


if __name__ == '__main__':
    lv = json.load(open(sys.argv[1])); idx = int(sys.argv[2])
    minutes, rng, out = float(sys.argv[3]), np.random.default_rng(int(sys.argv[4])), sys.argv[5]
    tris = [tuple(t) for t in lv['triangles']]
    t1, t2, R = GG.arms_of(lv['planes'], tris, len(lv['planes']))[idx]
    rec, _ = drift(lv['planes'], tris, R, (t1, t2), minutes, rng,
                   log=lambda *a: print(time.strftime('%H:%M:%S'), *a, flush=True))
    rec['next_triangles'] = [list(t) for t in R]
    json.dump(rec, open(out, 'w'))
    print('FINAL', rec['status'], 'k_tau', rec['k_tau'], 'margin %.3f' % rec['hemisphere_margin'], rec.get('t1'), flush=True)
