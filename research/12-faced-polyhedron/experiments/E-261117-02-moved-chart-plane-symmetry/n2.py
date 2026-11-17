"""E-261117-02 (N2): plane-only symmetry in a moved chart.

  controls OUT                 stage A: the Szilassi control chain K1-K5 and the negative controls (exact, minutes)
  sample SHARD SHARDS N CAP DEADLINE OUT
                               stage B: units i = SHARD, SHARD + SHARDS, ... < N of both arms (c2: C2 3 x 2 + 1 about
                               the z-axis; asym: seven independent planes; integer box [-8, 8] without 0), frozen
                               engine of E-261103-05 at seven planes, E = 21, a far plane as infinity; one JSON line
                               per unit and arm in OUT/results.jsonl
  summary OUT                  stage B tally over OUT/<shard>/results.jsonl, every hit re-checked by verify_candidate

The chart move: for an integer plane h = (a, b, c, d) (h . (x, y, z, 1) = 0) and the far plane H' = (-n, R),
R > n . p for every finite triple point p, the new coordinates X' = (x, y, z, R - n . x) give the integer plane
(aR + d n1, bR + d n2, cR + d n3, d) (a positive multiple of h M^-1, so coorientations are kept). The new chirotope
with infinity is that of the eight planes {h_i, H'}; plane-only signs are unchanged (det M = R > 0)."""
from fractions import Fraction
import importlib.util
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
from omsat import CNF, build, chirotope_from_planes, det4, perm_parity
from omsat_sym import build_sym, orbfix_quads
from omsat_validate import ALL_OPTS, szilassi
from ladder_exact import solve3, verify
from solid_fast import Tables
from solid_cpsat import best_solid
from pysat.solvers import Solver

_spec = importlib.util.spec_from_file_location(
    'frozen_engine', ROOT / 'experiments/E-261103-05-s5-symmetric-solid-first/pilot.py')
ENGINE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ENGINE)

NORMALS = [(2, 3, 5), (3, -5, 7), (-4, 7, 3), (5, 2, -9), (7, -3, 4), (-6, -5, 8), (9, 4, 1), (1, -8, -6)]
G_SZ = (1, 0, 3, 2, 6, 5, 4)          # Szilassi's half-turn about the z-axis: (a, b, c, d) -> (-a, -b, c, d)
NZ = [v for v in range(-8, 9) if v]
E7 = 21
ARMS = ('c2', 'asym')


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def sgn(x):
    return (x > 0) - (x < 0)


def plane_only(h):
    return {S: sgn(det4([h[i] for i in S])) for S in itertools.combinations(range(len(h)), 4)}


def finite_triple_points(h):
    pts = {}
    for t in itertools.combinations(range(len(h)), 3):
        m = [h[i][:3] for i in t]
        if det4([list(r) + [0] for r in m] + [[0, 0, 0, 1]]) != 0:
            pts[t] = solve3([h[i] for i in t])
    return pts


def far_plane(h, nrm):
    R = max(1, math.floor(max(sum(Fraction(a) * b for a, b in zip(nrm, p)) for p in finite_triple_points(h).values())) + 1)
    return [-nrm[0], -nrm[1], -nrm[2], R]


def move(h, Hp):
    R = Hp[3]; nrm = [-x for x in Hp[:3]]
    out = []
    for a, b, c, d in h:
        row = [a * R + d * nrm[0], b * R + d * nrm[1], c * R + d * nrm[2], d]
        g = math.gcd(*row)
        out.append([x // g for x in row])
    return out


def chart(h):
    """First far plane from NORMALS whose moved seven/eight-plane chirotope is uniform; None if there is none."""
    for nrm in NORMALS:
        Hp = far_plane(h, nrm); hm = move(h, Hp)
        if all(v != 0 for v in chirotope_from_planes(hm).values()):
            return Hp, hm
    return None


def links_of(faces):
    links = {}
    for k, f in enumerate(faces):
        links[k] = [next(j for j, g in enumerate(faces) if j != k and a in g and b in g)
                    for a, b in zip(f, f[1:] + f[:1])]
    return links


def sat(clauses, seconds=60):
    t0 = time.monotonic()
    with Solver(name='cadical195', bootstrap_with=clauses) as s:
        timer = threading.Timer(seconds, s.interrupt); timer.start()
        try:
            r = s.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
    return dict(status={True: 'SAT', False: 'UNSAT', None: 'UNKNOWN'}[r], seconds=round(time.monotonic() - t0, 3))


def pin(c, chi):
    return c.clauses + [[c.qvar[S] if v > 0 else -c.qvar[S]] for S, v in chi.items()]


def gauge(chi, G, n):
    """Equivariant gauge of build_sym: orbit flips making the orbfix quads positive, then mirror o flip-all
    (negates exactly the plane-only quads) if chi(0,1,2,3) < 0."""
    basis, orbs = orbfix_quads(G, n)
    for f in itertools.product((0, 1), repeat=len(orbs)):
        flip = {v for o, b in zip(orbs, f) if b for v in o}
        c = {S: v * (-1) ** len(flip & set(S)) for S, v in chi.items()}
        if all(c[S] > 0 for S in basis):
            if c[(0, 1, 2, 3)] < 0:
                c = {S: (-v if n not in S else v) for S, v in c.items()}
            return c, sorted(flip)
    raise AssertionError('orbfix basis is not a gauge')


def symbreak_reachable(chi, orbs, n):
    """Is the symbreak normal form reachable from chi by an equivariant gauge (orbit flips, mirror)?"""
    fixed = [(0, 1, k, n) for k in range(2, n)] + [(0, 2, 3, n), (1, 2, 3, n)]
    for f in itertools.product((0, 1), repeat=len(orbs)):
        flip = {v for o, b in zip(orbs, f) if b for v in o}
        for m in (1, -1):
            if all(m * chi[S] * (-1) ** len(flip & set(S)) > 0 for S in fixed):
                return True
    return False


def engine(h, cap, edges=E7):
    """Frozen engine of E-261103-05 (arrangement, Tables, hard disk CP-SAT model, exact verify), unchanged."""
    a = ENGINE.arrangement(h); tables = Tables(a)
    cells, info = best_solid(a, tables, time_limit=cap, target_edges=edges, max_runs=3)
    r = dict(solver=info, bounded_cells=len(tables.cells))
    if cells is not None:
        assert info['valid'], 'hard disk model disagrees with boundary diagnostics'
        solid = {tables.cells[i] for i, v in enumerate(cells) if v}
        links = ENGINE.extract_links(a, solid)
        r.update(planes=ENGINE.integer_planes(h), links=links, geometry=verify(ENGINE.integer_planes(h), links,
                                                                                require_all_pairs=True))
    ENGINE.validate_result(r, dict(edges=edges, planes=h))
    return r


def verify_candidate(path):
    p = subprocess.run([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(path), '--all-pairs'],
                       capture_output=True, text=True)
    return dict(returncode=p.returncode, stdout=p.stdout.strip().splitlines()[-1:] if p.stdout else [])


def controls(out):
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic(); rep = dict(target='S1 control chain at seven faces; no target decided')
    h, T, verts, faces = szilassi(); n = 7; links = links_of(faces)
    G = [tuple(range(n)), G_SZ]

    # K1: exact plane-only determinants and the half-turn on plane vectors.
    k1 = dict(image_is_plane=all([-r[0], -r[1], r[2], r[3]] == list(h[G_SZ[i]]) for i, r in enumerate(h)))
    po = plane_only(h)
    k1['plane_only_nonzero'] = sum(v != 0 for v in po.values()); k1['plane_only_total'] = len(po)
    k1['plane_only_symmetric'] = all(
        po[tuple(sorted(G_SZ[i] for i in S))] * (-1) ** perm_parity([G_SZ[i] for i in S]) == po[S] for S in po)
    std = chirotope_from_planes(h)
    k1['standard_chart_zeros'] = sorted(S[:3] for S, v in std.items() if v == 0)
    k1['PASS'] = (k1['image_is_plane'] and k1['plane_only_nonzero'] == 35 and k1['plane_only_symmetric']
                  and k1['standard_chart_zeros'] == [(0, 1, 5), (2, 3, 5), (4, 5, 6)])
    rep['K1_plane_only_determinants'] = k1

    # K2: a rational far plane missing the whole solid, generic with respect to all 35 triples.
    Hp, hm = chart(h)
    side = [Hp[3] - sum(-a * b for a, b in zip(Hp[:3], v)) for v in verts]
    trip = [sgn(det4([h[i] for i in t] + [Hp])) for t in itertools.combinations(range(n), 3)]
    k2 = dict(far_plane=Hp, vertices_positive=all(s > 0 for s in side), min_vertex_value=str(min(side)),
              triples_nonzero=sum(t != 0 for t in trip))
    k2['PASS'] = k2['vertices_positive'] and k2['triples_nonzero'] == 35
    rep['K2_far_plane'] = k2

    # K3: exact transformed signs and embedding.
    chi_m = chirotope_from_planes(hm)
    R = Hp[3]; nrm = [-x for x in Hp[:3]]
    vm = [tuple(x / (R - sum(a * b for a, b in zip(nrm, v))) for x in v) for v in verts]
    incid = all(sum(Fraction(a) * b for a, b in zip(hm[k][:3], vm[v])) + hm[k][3] == 0 for k, f in enumerate(faces)
                for v in f)
    geo = verify(hm, links, require_all_pairs=True)
    cand = out / 'szilassi_moved.json'; dump(cand, dict(planes=hm, links=links, far_plane=Hp))
    vc = verify_candidate(cand)
    k3 = dict(planes=hm, uniform=all(v != 0 for v in chi_m.values()), signs=len(chi_m),
              plane_only_unchanged=all(chi_m[S] == po[S] for S in po), incidence=incid,
              EMBEDDED=geo.get('EMBEDDED'), all_pairs=geo.get('all_pairs_adjacent'),
              V_E_F_chi=geo.get('V_E_F_chi'), verify_candidate=vc)
    k3['PASS'] = (k3['uniform'] and k3['plane_only_unchanged'] and incid and geo.get('EMBEDDED') is True
                  and geo.get('all_pairs_adjacent') is True and vc['returncode'] == 0)
    rep['K3_moved_chart'] = k3

    # K4: SAT controls, Szilassi's map, ALL_OPTS, plane-only half-turn clauses in the moved chart.
    o = dict(ALL_OPTS, sym_planes_only=True)
    eps = {g: 1 for g in G}
    k4 = {}
    c = CNF(n); build(c, T, o, sym=[(G_SZ, 1)])
    k4['pinned_no_gauge'] = sat(pin(c, chi_m))
    cg, basis, orbs = build_sym(T, G, eps, o)
    chi_g, flip = gauge(chi_m, G, n)
    k4['gauge'] = dict(orbits=orbs, orbfix_quads=basis, flipped=flip)
    k4['pinned_gauge'] = sat(pin(cg, chi_g))
    k4['free_gauge'] = sat(cg.clauses)
    k4['symbreak_reachable_equivariantly'] = symbreak_reachable(chi_m, orbs, n)
    cs = CNF(n); build(cs, T, dict(o, symbreak=True, mirror=True), sym=[(G_SZ, 1)])
    k4['free_symbreak'] = sat(cs.clauses)
    k4['PASS'] = all(k4[k]['status'] == 'SAT' for k in ('pinned_no_gauge', 'pinned_gauge', 'free_gauge'))
    rep['K4_sat_controls'] = k4

    # Negative controls (must fail).
    neg = {}
    c = CNF(n); build(c, T, ALL_OPTS, sym=[(G_SZ, 1)])          # INF fixed by the half-turn: forced zeros
    neg['standard_chart_symmetry_uniform'] = sat(c.clauses)
    auts = [p for p in itertools.permutations(range(n))
            if {frozenset(p[x] for x in t) for t in T.tris} == T.triset]
    invol = [p for p in auts if p != tuple(range(n)) and all(p[p[i]] == i for i in range(n)) and p != G_SZ]
    other = invol[0]
    c = CNF(n); build(c, T, o, sym=[(other, 1)])
    neg['pinned_wrong_involution'] = dict(sat(pin(c, chi_m)), involution=other, map_automorphisms=len(auts),
                                          involutions=len(invol) + 1)
    try:
        ENGINE.arrangement(h); neg['engine_standard_chart'] = 'ACCEPTED'
    except ValueError as exc:
        neg['engine_standard_chart'] = 'REJECTED: %s' % exc
    tetra = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]]
    neg['engine_tetra_E7'] = engine(tetra, 5, edges=7)['solver']['status']
    neg['PASS'] = (neg['standard_chart_symmetry_uniform']['status'] == 'UNSAT'
                   and neg['pinned_wrong_involution']['status'] == 'UNSAT'
                   and neg['engine_standard_chart'].startswith('REJECTED: nonuniform triple')
                   and neg['engine_tetra_E7'] == 'INFEASIBLE')
    rep['negative_controls'] = neg

    # K5: planted recovery on the frozen engine in the moved chart.
    t1 = time.monotonic(); r = engine(hm, 20)
    k5 = dict(status=r['solver']['status'], seconds=round(time.monotonic() - t1, 3),
              bounded_cells=r['bounded_cells'])
    if 'links' in r:
        k5['EMBEDDED'] = r['geometry'].get('EMBEDDED'); k5['V_E_F_chi'] = r['geometry'].get('V_E_F_chi')
        k5['all_pairs'] = r['geometry'].get('all_pairs_adjacent')
        k5['same_links_as_szilassi'] = all(ENGINE.cyclic_equal(r['links'][i], links[i]) for i in range(n))
        p = out / 'planted_solid.json'; dump(p, dict(planes=r['planes'], links=r['links'])); k5['verify_candidate'] = \
            verify_candidate(p)
    k5['PASS'] = k5['status'] in ('OPTIMAL', 'FEASIBLE') and k5.get('EMBEDDED') is True and \
        k5.get('all_pairs') is True and k5.get('verify_candidate', {}).get('returncode') == 0
    rep['K5_planted_engine'] = k5

    rep['PASS'] = all(rep[k]['PASS'] for k in rep if isinstance(rep[k], dict) and 'PASS' in rep[k])
    rep['seconds'] = round(time.monotonic() - t0, 3)
    dump(out / 'controls.json', rep)
    print(json.dumps(dict(PASS=rep['PASS'], **{k: v.get('PASS') for k, v in rep.items() if isinstance(v, dict)})))
    return rep


def draw(arm, i):
    rng = random.Random('E-261117-02/%s/%d' % (arm, i))
    for rejected in range(200):
        if arm == 'c2':
            rows = [[0, 0, rng.choice((-1, 1)), rng.choice(NZ)]]
            for _ in range(3):
                a, b, c, d = (rng.choice(NZ) for _ in range(4))
                rows += [[a, b, c, d], [-a, -b, c, d]]
        else:
            rows = [[rng.choice(NZ) for _ in range(4)] for _ in range(7)]
        if any(v == 0 for v in plane_only(rows).values()):
            continue
        ch = chart(rows)
        if ch is not None:
            return rows, ch[0], ch[1], rejected
    raise ValueError('no admissible draw in 200 attempts')


def sample(shard, shards, n_units, cap, deadline, out):
    """Units i = shard, shard + shards, ... < n_units; both arms per i, so a deadline cut leaves them balanced."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / 'results.jsonl'
    done = {(r['arm'], r['i']) for r in records(path)}
    stop = time.monotonic() + deadline
    with path.open('a') as f:
        if path.stat().st_size and not path.read_bytes().endswith(b'\n'):
            f.write('\n')
        for i in range(shard, n_units, shards):
            for arm in ARMS:
                if (arm, i) in done or time.monotonic() > stop:
                    continue
                t0 = time.monotonic()
                rows, Hp, hm, rej = draw(arm, i)
                rec = dict(i=i, arm=arm, planes=rows, far_plane=Hp, rejected=rej)
                try:
                    r = engine(hm, cap)
                    rec.update(status=r['solver']['status'], bounded_cells=r['bounded_cells'])
                    if 'links' in r:
                        g = r['geometry']
                        rec.update(moved_planes=r['planes'], links=r['links'], EMBEDDED=g.get('EMBEDDED'),
                                   all_pairs=g.get('all_pairs_adjacent'), V_E_F_chi=g.get('V_E_F_chi'))
                except ValueError as exc:
                    rec.update(status='REJECTED_BY_ENGINE', error=str(exc))
                rec['seconds'] = round(time.monotonic() - t0, 3)
                f.write(json.dumps(rec) + '\n'); f.flush()


def records(path):
    """Complete JSON lines of a results file; a line cut by a kill is dropped and its unit reruns."""
    out = []
    for line in (path.read_text().splitlines() if path.exists() else []):
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def summary(out):
    rows = [r for p in sorted(out.glob('[0-9]*/results.jsonl')) for r in records(p)]
    rep = {}
    hits_dir = out / 'hits'; hits_dir.mkdir(exist_ok=True)
    for arm in sorted({r['arm'] for r in rows}):
        rs = [r for r in rows if r['arm'] == arm]
        st = {}
        for r in rs:
            st[r['status']] = st.get(r['status'], 0) + 1
        hits = [r for r in rs if r.get('EMBEDDED') and r.get('all_pairs')]
        checked = []
        for r in hits:
            p = hits_dir / ('%s_%d.json' % (arm, r['i']))
            dump(p, dict(planes=r['moved_planes'], links=r['links'], source_planes=r['planes'], far_plane=r['far_plane']))
            checked.append(dict(i=r['i'], V_E_F_chi=r['V_E_F_chi'], verify_candidate=verify_candidate(p)))
        secs = sorted(r['seconds'] for r in rs)
        rep[arm] = dict(units=len(rs), distinct_units=len({r['i'] for r in rs}), status=st, hits=len(hits),
                        hits_verified=sum(c['verify_candidate']['returncode'] == 0 for c in checked), checked=checked,
                        core_seconds=round(sum(secs), 1), median_seconds=secs[len(secs) // 2] if secs else None,
                        max_seconds=secs[-1] if secs else None, rejected_draws=sum(r['rejected'] for r in rs))
    dump(out / 'summary.json', rep)
    print(json.dumps({a: {k: v for k, v in r.items() if k != 'checked'} for a, r in rep.items()}))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'controls':
        sys.exit(0 if controls(Path(sys.argv[2]))['PASS'] else 1)
    elif cmd == 'sample':
        shard, shards, n_units, cap, deadline, out = sys.argv[2:8]
        sample(int(shard), int(shards), int(n_units), float(cap), float(deadline), Path(out))
    elif cmd == 'summary':
        summary(Path(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
