"""Exact Stage A list: the generic near-copy ninth-plane cells of a fixed eight-plane source, their orbits under the
source's signed coordinate permutations, and one exactly verified rational representative per orbit.

Ported and reviewed from the dialogue prototypes cells9.py / cells_exact.py / stage_a_reps.py (2026-11-10 thread).
A ninth plane p is generic iff det(p, x, y, z) != 0 for every triple of the source planes and the plane at infinity
INF; its cell is the projective sign vector over those 84 dual vectors D. For a source plane A, the near-copy cells
A + eps * b are the regions of the central rank-3 arrangement W = {cross4(A, x, y)} acting on b modulo A.

Certificate (all exact; floats only propose directions, every sign used is recomputed in integers / Fractions):
  * per plane, the distinct local regions found, each with a verified b (sign(W . b) == key, no zero), number
    exactly 2 (1 + sum over rank-2 flats (|flat| - 1)) (Zaslavsky, rank 3, W essential and pairwise independent);
  * every near-copy plane has 84 nonzero signs; the union is deduplicated by its projective 84-key;
  * every symmetry permutes the source planes and the dual vectors; every key's orbit, computed from its own
    representative, equals its orbit leader's orbit, and every orbit lies in the union (exact partition).
The representative of a cell comes from representative(): a max-margin LP over the 84 normalised duals, rounded
to 1e-9 and checked exactly; if the check fails, the exact witness is used and the method says so.
Usage: python3 cells.py OUT_DIR   (writes units.json and certificate.json)"""
import hashlib
import itertools
import json
import math
from fractions import Fraction as Fr
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'E-261103-05-s5-symmetric-solid-first'))
import pilot as base  # noqa: E402

INF = [0, 0, 0, 1]
SOURCES = ('roest_vigh', 'mizhaev')


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sgn(x):
    return (x > 0) - (x < 0)


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def cross4(a, b, c):
    """w with w . p = det(p, a, b, c)."""
    return [(-1) ** k * det3([[r[j] for j in range(4) if j != k] for r in (a, b, c)]) for k in range(4)]


def canon(v):
    """Primitive integer vector with a positive first nonzero entry (projective class of a nonzero vector)."""
    den = math.lcm(*(Fr(x).denominator for x in v))
    v = [int(Fr(x) * den) for x in v]
    g = math.gcd(*v)
    if not g:
        raise ValueError('zero vector')
    v = [x // g for x in v]
    s = next(x for x in v if x)
    return tuple(x if s > 0 else -x for x in v)


def rank(vs):
    m = [[Fr(x) for x in v] for v in vs]; r = 0
    for c in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c] / m[r][c]; m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def zaslavsky_rank3(W):
    """Number of regions of the central arrangement of W (rank 3, pairwise independent): 2 (1 + c2)."""
    assert rank(W) == 3, 'local arrangement is not essential'
    assert len({canon(w) for w in W}) == len(W), 'local vectors not pairwise independent'
    seen = set(); c2 = 0
    for i, j in itertools.combinations(range(len(W)), 2):
        if (i, j) in seen:
            continue
        flat = [k for k in range(len(W)) if rank([W[i], W[j], W[k]]) == 2]
        c2 += len(flat) - 1; seen.update(itertools.combinations(flat, 2))
    return 2 * (1 + c2)


def duals(h):
    return sorted({canon(cross4(*t)) for t in itertools.combinations([list(r) for r in h] + [INF], 3)})


def key_of(D, p):
    s = tuple(sgn(dot(w, p)) for w in D)
    if 0 in s:
        raise ArithmeticError('plane on a dual hyperplane (not generic)')
    return max(s, tuple(-v for v in s))                  # projective: p and -p are the same plane


def key_str(k):
    return ''.join('+' if v > 0 else '-' for v in k)


def near_copy_cells(h, a):
    """Local regions of plane a: {key: b} with b exactly verified; floats only propose the wedge directions."""
    el = [r for i, r in enumerate(h) if i != a] + [INF]
    W = sorted({canon(cross4(h[a], x, y)) for x, y in itertools.combinations(el, 2)})
    return W, local_cells(h[a], W)


def local_cells(A, W):
    """Regions of the central rank-3 arrangement W (all orthogonal to A) acting on b modulo A: {key: b}, exact."""
    out = {}
    for i, j in itertools.combinations(range(len(W)), 2):
        r0 = cross4(A, W[i], W[j])
        if not any(r0):
            continue
        for r in (r0, [-v for v in r0]):
            on = [m for m in range(len(W)) if dot(W[m], r) == 0]
            e1 = W[on[0]]; e2 = cross4(A, r, e1)
            n1, n2 = math.sqrt(dot(e1, e1)), math.sqrt(dot(e2, e2))
            ang = sorted({round(math.atan2(dot(W[m], e2) / n2, dot(W[m], e1) / n1) % math.pi, 12) for m in on})
            ang = ang + [t + math.pi for t in ang]; ang.append(ang[0] + 2 * math.pi)
            for t0, t1 in zip(ang, ang[1:]):
                phi = (t0 + t1) / 2 + math.pi / 2          # a direction strictly between two consecutive lines
                d = [Fr(round(1e9 * (math.cos(phi) * x / n1 + math.sin(phi) * y / n2)), 10 ** 9) for x, y in zip(e1, e2)]
                loc = {m: sgn(dot(W[m], d)) for m in on}
                if 0 in loc.values():
                    raise ArithmeticError('wedge direction on a local plane')
                key = tuple(sgn(dot(w, r)) or loc[m] for m, w in enumerate(W))
                if key in out:
                    continue
                off = [abs(dot(w, r)) for m, w in enumerate(W) if m not in on]
                delta = min(off) / (2 * max(abs(dot(w, d)) for w in W) + 1) if off else Fr(1)
                b = [Fr(x) + delta * y for x, y in zip(r, d)]
                if tuple(sgn(dot(w, b)) for w in W) != key:
                    raise ArithmeticError('local representative misses its cell')
                out[key] = b
    return out


def ninth_plane(h, a, b):
    """A + eps * b; every determinant without A keeps the sign it has with A (exact)."""
    el = [r for i, r in enumerate(h) if i != a] + [INF]
    da = [dot(cross4(*t), h[a]) for t in itertools.combinations(el, 3)]
    db = [dot(cross4(*t), b) for t in itertools.combinations(el, 3)]
    assert all(da)
    eps = min(abs(x) for x in da) / (2 * max(abs(x) for x in db) + 1)
    return [Fr(x) + eps * y for x, y in zip(h[a], b)]


def representative(D, key, witness):
    """A rational plane in the cell `key` of D: a max-margin LP point if it verifies exactly, else the witness."""
    s = np.array(key, float); Dn = np.array(D, float); Dn /= np.linalg.norm(Dn, axis=1)[:, None]
    res = linprog([0, 0, 0, 0, -1], A_ub=np.hstack([-(s[:, None] * Dn), np.ones((len(D), 1))]), b_ub=np.zeros(len(D)),
                  bounds=[(-1, 1)] * 4 + [(0, None)], method='highs')
    if res.status == 0 and res.x[4] > 0:
        p = [Fr(round(float(v) * 10 ** 9), 10 ** 9) for v in res.x[:4]]
        if any(p[:3]) and tuple(sgn(dot(w, p)) for w in D) == tuple(key):
            return p, 'lp', float(res.x[4])
    if key_of(D, witness) != tuple(key):
        raise ArithmeticError('witness is not in its cell')
    return [Fr(v) for v in witness], 'witness', None


def symmetries(h):
    S = {canon(r) for r in h}; out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            g = lambda r, perm=perm, sg=sg: [sg[k] * r[perm[k]] for k in range(3)] + [r[3]]
            if {canon(g(r)) for r in h} == S:
                out.append(((perm, sg), g))
    return out


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def source_planes(name):
    return next([list(map(int, r)) for r in base.integer_planes(hh)] for n, hh, _ in base.fixtures() if n == name)


def build(name):
    h = source_planes(name); D = duals(h); G = symmetries(h)
    assert len(D) == 84, len(D)
    for _, g in G:                                       # the action permutes the dual vectors (INF is fixed)
        assert sorted(canon(g(w)) for w in D) == D, 'symmetry does not permute D'
    full = {}; per = []
    for a in range(len(h)):
        W, cells = near_copy_cells(h, a)
        z = zaslavsky_rank3(W)
        per.append(dict(plane=a, local_vectors=len(W), found=len(cells), zaslavsky=z))
        if len(cells) != z:
            raise ArithmeticError(f'{name} plane {a}: {len(cells)} local cells found, Zaslavsky count {z}')
        for b in cells.values():
            p = ninth_plane(h, a, b)
            full.setdefault(key_of(D, p), (a, p))
    reps = {}
    for k, (a, p) in sorted(full.items()):
        q, method, margin = representative(D, k, p)
        reps[k] = dict(plane=a, p=q, method=method, margin=margin)
    orbit_of = {}; orbits = []
    for k in sorted(full):
        orb = frozenset(key_of(D, g(reps[k]['p'])) for _, g in G)
        if not orb <= set(full):
            raise ArithmeticError('symmetry leaves the near-copy union')
        if k in orbit_of:
            if orbits[orbit_of[k]] != orb:
                raise ArithmeticError('orbits do not partition the union')
            continue
        for m in orb:
            orbit_of[m] = len(orbits)
        orbits.append(orb)
    assert sum(map(len, orbits)) == len(full) == len(orbit_of)
    units = []
    for i, orb in enumerate(orbits):
        k = min(orb); r = reps[k]
        units.append(dict(source=name, orbit=i, orbit_size=len(orb), plane=r['plane'], key=key_str(k),
                          method=r['method'], margin=r['margin'], ninth=[str(v) for v in r['p']]))
    sizes = {}
    for orb in orbits:
        sizes[str(len(orb))] = sizes.get(str(len(orb)), 0) + 1
    cert = dict(source=name, planes=h, duals=len(D), symmetries=[[list(p), list(s)] for (p, s), _ in G],
                per_plane=per, union=len(full), orbits=len(orbits), orbit_sizes=sizes,
                methods={m: sum(u['method'] == m for u in units) for m in ('lp', 'witness')},
                keys_sha256=sha(sorted(key_str(k) for k in full)),
                orbits_sha256=sha(sorted(sorted(key_str(k) for k in orb) for orb in orbits)),
                reps_sha256=sha([(u['key'], u['ninth']) for u in units]))
    return units, cert


def queue(by_source):
    """Stable source-interleaved queue in blocks of 10: ordinal modulo 10 gives every shard both sources."""
    out = []; lists = [list(by_source[s]) for s in SOURCES]
    while any(lists):
        for lst in lists:
            out += lst[:10]; del lst[:10]
    for i, u in enumerate(out):
        u['ordinal'] = i; u['unit'] = f"{'rv' if u['source'] == 'roest_vigh' else 'mz'}_o{u['orbit']:04d}"
    return out


if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    by_source = {}; certs = []
    for name in SOURCES:
        by_source[name], cert = build(name); certs.append(cert)
        print(name, json.dumps({k: cert[k] for k in ('union', 'orbits', 'orbit_sizes', 'methods')}), flush=True)
    units = queue(by_source)
    (out / 'units.json').write_text(json.dumps(units, indent=0) + '\n')
    for c in certs:
        c['units_file_sha256'] = base.sha(out / 'units.json')
    (out / 'certificate.json').write_text(json.dumps(certs, indent=1) + '\n')
    print('units', len(units), 'units.json sha256', base.sha(out / 'units.json'))
