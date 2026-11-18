"""E-261110-04 (amended 2026-11-17): the owner night, three symmetric-family arms on the frozen engine of E-261103-05.

  controls OUT                    stage A: positive and negative controls of the engine, the chart and the draws
  sample SHARD SHARDS DEADLINE OUT
                                  units i = SHARD, SHARD + SHARDS, ...; per i every arm in ARMS (c3 and c2 at nine
                                  planes, each at E = 45 and 51; geo2 / geo3 D2 2 x 4 at eight planes, E = 36, while
                                  i < N_GEO); one JSON line per (arm, E, i) in OUT/results.jsonl; stops at DEADLINE s
                                  (monotonic) or when results/stop.requested exists (a verified nine-face hit sets it)
  summary OUT                     tally over OUT/<shard>/results.jsonl; every hit re-checked by verify_candidate

Arms: c3 = C3 3+3+3, the rotation (x, y, z) -> (y, z, x), K14's integer box (coefficients in [-8, 8] without 0,
d in [-8, -1]), standard chart. c2 = C2 4 x 2 + 1 about the z-axis (one plane z-perpendicular, four pairs
(a, b, c, d), (-a, -b, c, d); coefficients in [-8, 8] without 0), a far plane as infinity (n2.chart). geoQ = K13's D2
2 x 4 sampler with every coefficient s * Q^w, s = +-1 and w in {0, ..., K} uniform, d = -Q^w. The solid need not be
invariant; the engine searches every solid of the drawn arrangement."""
import json
import math
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'experiments/E-261117-02-moved-chart-plane-symmetry'))
import n2  # noqa: E402  (loads the frozen engine of E-261103-05 as n2.ENGINE and adds ROOT/code to sys.path)
from omsat import chirotope_from_planes  # noqa: E402

ENGINE = n2.ENGINE
NZ = n2.NZ
CAP = {'c3': 20.0, 'c2': 20.0, 'geo2': 15.0, 'geo3': 15.0}
EDGES = {'c3': (45, 51), 'c2': (45, 51), 'geo2': (36,), 'geo3': (36,)}
GEO = {'geo2': (2, 3), 'geo3': (3, 3)}             # (q, K): magnitudes q^0 .. q^K
N_GEO = 3000
ARMS = ('c3', 'c2', 'geo2', 'geo3')
STOP = HERE / 'results' / 'stop.requested'
K13_BASELINE = (17, 240)                            # archived K13: 17 SOLID in 240 D2 2 x 4 draws, box [-8, 8]


def rot3(r):
    a, b, c, d = r
    return [c, a, b, d]


def uniform_standard(rows):
    try:
        ENGINE.arrangement(rows)
        return True
    except ValueError:
        return False


def draw(arm, i):
    """(source planes, far plane or None, planes given to the engine, rejected draws); deterministic in (arm, i)."""
    rng = random.Random('E-261110-04/%s/%d' % (arm, i))
    for rejected in range(200):
        if arm == 'c3':
            rows = []
            for _ in range(3):
                r = [rng.choice(NZ) for _ in range(3)] + [-rng.randint(1, 8)]
                rows += [r, rot3(r), rot3(rot3(r))]
            if uniform_standard(rows):
                return rows, None, rows, rejected
        elif arm == 'c2':
            rows = [[0, 0, rng.choice((-1, 1)), rng.choice(NZ)]]
            for _ in range(4):
                a, b, c, d = (rng.choice(NZ) for _ in range(4))
                rows += [[a, b, c, d], [-a, -b, c, d]]
            if all(v != 0 for v in n2.plane_only(rows).values()):
                ch = n2.chart(rows)
                if ch is not None:
                    return rows, ch[0], ch[1], rejected
        else:
            q, k = GEO[arm]
            mag = lambda: q ** rng.randint(0, k)
            rows = []
            for _ in range(2):
                abc = [rng.choice((-1, 1)) * mag() for _ in range(3)]; d = -mag()
                rows += [[s * a for s, a in zip(sg, abc)] + [d]
                         for sg in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
            if uniform_standard(rows):
                return rows, None, rows, rejected
    raise ValueError('no admissible draw in 200 attempts')


def decide(planes, edges, cap):
    """One frozen-engine call; ENGINE_ERROR records an exact/model disagreement instead of killing the shard."""
    rec = {}
    try:
        r = n2.engine(planes, cap, edges=edges)
        rec.update(status=r['solver']['status'], bounded_cells=r['bounded_cells'])
        if 'links' in r:
            g = r['geometry']
            rec.update(engine_planes=r['planes'], links=r['links'], EMBEDDED=g.get('EMBEDDED'),
                       all_pairs=g.get('all_pairs_adjacent'), V_E_F_chi=g.get('V_E_F_chi'))
    except ValueError as exc:
        rec.update(status='REJECTED_BY_ENGINE', error=str(exc))
    except (ArithmeticError, AssertionError, RuntimeError) as exc:
        rec.update(status='ENGINE_ERROR', error='%s: %s' % (type(exc).__name__, exc))
    return rec


def save_hit(path, rec):
    n2.dump(path, dict(planes=rec['engine_planes'], links=rec['links'], source_planes=rec['planes'],
                       far_plane=rec['far_plane'], arm=rec['arm'], edges=rec['edges'], i=rec['i']))
    return n2.verify_candidate(path)


def controls(out):
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic(); rep = dict(target='controls only; no target decided')

    # P1: planted moved Szilassi (E-261117-02 K3), E = 21 -> a solid, EMBEDDED, all pairs, verify_candidate PASS.
    sz = json.loads((ROOT / 'experiments/E-261117-02-moved-chart-plane-symmetry/results/controls/szilassi_moved.json')
                    .read_text())
    r = decide(sz['planes'], 21, 20)
    p1 = dict(status=r['status'], V_E_F_chi=r.get('V_E_F_chi'))
    if 'links' in r:
        p = out / 'p1_szilassi.json'; n2.dump(p, dict(planes=r['engine_planes'], links=r['links']))
        p1['verify_candidate'] = n2.verify_candidate(p)
    p1['PASS'] = r.get('EMBEDDED') is True and r.get('all_pairs') is True and \
        p1.get('verify_candidate', {}).get('returncode') == 0
    rep['P1_planted_szilassi'] = p1

    # P2: K13 seed 4 (D2 2 x 4, E = 36) -> SOLID (24, 36, 8, -4); N4 its links with two entries swapped must fail.
    h4, _ = ENGINE.random_d2(4)
    r = decide(h4, 36, 15)
    p2 = dict(status=r['status'], V_E_F_chi=r.get('V_E_F_chi'))
    if 'links' in r:
        p = out / 'p2_k13_seed4.json'; n2.dump(p, dict(planes=r['engine_planes'], links=r['links']))
        p2['verify_candidate'] = n2.verify_candidate(p)
        bad = {k: list(v) for k, v in r['links'].items()}; bad[0][0], bad[0][1] = bad[0][1], bad[0][0]
        q = out / 'n4_swapped.json'; n2.dump(q, dict(planes=r['engine_planes'], links=bad))
        rep['N4_swapped_links'] = dict(verify_candidate=n2.verify_candidate(q))
        rep['N4_swapped_links']['PASS'] = rep['N4_swapped_links']['verify_candidate']['returncode'] != 0
    p2['PASS'] = r.get('EMBEDDED') is True and tuple(r.get('V_E_F_chi') or ()) == (24, 36, 8, -4) and \
        p2.get('verify_candidate', {}).get('returncode') == 0
    rep['P2_k13_seed4'] = p2

    # N1: K13 seeds 0-3 INFEASIBLE at E = 36; N2: tetrahedron at E = 7 INFEASIBLE (E = 6 is the positive twin).
    neg = dict(k13_seeds_0_3=[decide(ENGINE.random_d2(s)[0], 36, 15)['status'] for s in range(4)])
    tetra = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]]
    neg['tetra_E7'] = decide(tetra, 7, 5)['status']; neg['tetra_E6'] = decide(tetra, 6, 5)['status']
    # N3: the unmoved C2 draw is rejected by the engine (the fixed plane's normal and a pair's are dependent).
    neg['c2_unmoved'] = decide(draw('c2', 0)[0], 45, 5)
    neg['PASS'] = (neg['k13_seeds_0_3'] == ['INFEASIBLE'] * 4 and neg['tetra_E7'] == 'INFEASIBLE'
                   and neg['tetra_E6'] == 'OPTIMAL' and neg['c2_unmoved']['status'] == 'REJECTED_BY_ENGINE'
                   and neg['c2_unmoved']['error'].startswith('nonuniform triple'))
    rep['N1_N3_negatives'] = neg

    # D: exact checks of the draws on units 0-9 of each arm.
    d = {}
    for i in range(10):
        s, Hp, hm, _ = draw('c3', i)
        d.setdefault('c3_orbits_exact', []).append(all(rot3(s[3 * k + j]) == s[3 * k + (j + 1) % 3]
                                                       for k in range(3) for j in range(3)))
        s, Hp, hm, _ = draw('c2', i)
        po = n2.plane_only(s); chi = chirotope_from_planes(hm)
        d.setdefault('c2_halfturn_exact', []).append(s[0][:2] == [0, 0] and all(
            s[k + 1] == [-s[k][0], -s[k][1], s[k][2], s[k][3]] for k in (1, 3, 5, 7)))
        d.setdefault('c2_moved_uniform', []).append(all(v != 0 for v in chi.values()) and len(chi) == 210)
        d.setdefault('c2_plane_only_kept', []).append(all(chi[S] == po[S] for S in po))
        d.setdefault('c2_far_plane_misses_triples', []).append(all(
            Hp[3] - sum(-a * b for a, b in zip(Hp[:3], v)) > 0 for v in n2.finite_triple_points(s).values()))
        for arm in ('geo2', 'geo3'):
            q, k = GEO[arm]; s = draw(arm, i)[0]
            d.setdefault(arm + '_box_exact', []).append(all(abs(x) in {q ** w for w in range(k + 1)}
                                                            for r in s for x in r) and len(s) == 8)
    rep['D_draws'] = {k: all(v) for k, v in d.items()}
    rep['D_draws']['PASS'] = all(rep['D_draws'].values())

    rep['PASS'] = all(rep[k]['PASS'] for k in rep if isinstance(rep[k], dict) and 'PASS' in rep[k])
    rep['seconds'] = round(time.monotonic() - t0, 3)
    n2.dump(out / 'controls.json', rep)
    print(json.dumps(dict(PASS=rep['PASS'], **{k: v.get('PASS') for k, v in rep.items() if isinstance(v, dict)})))
    return rep


def done_units(results):
    """(arm, edges, i) recorded in any shard, so a restart with another SHARDS skips them."""
    return {(r['arm'], r['edges'], r['i']) for p in results.glob('[0-9]*/results.jsonl') for r in n2.records(p)}


def sample(shard, shards, deadline, out, n_max=10 ** 6):
    out.mkdir(parents=True, exist_ok=True)
    path = out / 'results.jsonl'
    done = done_units(out.parent)
    stop = time.monotonic() + deadline
    (out / 'hits').mkdir(exist_ok=True)
    with path.open('a') as f:
        if path.stat().st_size and not path.read_bytes().endswith(b'\n'):
            f.write('\n')
        for i in range(shard, n_max, shards):
            for arm in ARMS:
                if arm.startswith('geo') and i >= N_GEO:
                    continue
                todo = [e for e in EDGES[arm] if (arm, e, i) not in done]
                if not todo:
                    continue
                if time.monotonic() > stop or STOP.exists():
                    print('stop: %s' % ('deadline' if time.monotonic() > stop else STOP.name), flush=True)
                    return
                rows, Hp, hm, rej = draw(arm, i)
                for e in todo:
                    print('unit %s E=%d i=%d' % (arm, e, i), flush=True)
                    t0 = time.monotonic()
                    rec = dict(i=i, arm=arm, edges=e, planes=rows, far_plane=Hp, rejected=rej, cap=CAP[arm])
                    rec.update(decide(hm, e, CAP[arm]))
                    rec['seconds'] = round(time.monotonic() - t0, 3)
                    if rec.get('EMBEDDED') and rec.get('all_pairs') and len(rows) == 9:
                        vc = save_hit(out / 'hits' / ('%s_%d_%d.json' % (arm, e, i)), rec)
                        rec['verify_candidate'] = vc
                        print('CANDIDATE %s E=%d i=%d verify_candidate rc=%d' % (arm, e, i, vc['returncode']), flush=True)
                        if vc['returncode'] == 0:
                            STOP.touch()
                    if rec['status'] == 'ENGINE_ERROR':
                        print('ENGINE_ERROR %s E=%d i=%d: %s' % (arm, e, i, rec['error']), flush=True)
                    f.write(json.dumps(rec) + '\n'); f.flush()


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; w = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(max(0.0, c - w), 5), round(min(1.0, c + w), 5)]


def summary(out):
    rows = [r for p in sorted(out.glob('[0-9]*/results.jsonl')) for r in n2.records(p)]
    hits_dir = out / 'hits'; hits_dir.mkdir(exist_ok=True)
    rep = dict(k13_baseline=dict(hits=K13_BASELINE[0], units=K13_BASELINE[1], wilson=wilson(*K13_BASELINE)))
    for arm, e in sorted({(r['arm'], r['edges']) for r in rows}):
        rs = [r for r in rows if r['arm'] == arm and r['edges'] == e]
        st = {}
        for r in rs:
            st[r['status']] = st.get(r['status'], 0) + 1
        hits = [r for r in rs if r.get('EMBEDDED') and r.get('all_pairs')]
        checked = []
        for r in hits:
            p = hits_dir / ('%s_%d_%d.json' % (arm, e, r['i']))
            checked.append(dict(i=r['i'], V_E_F_chi=r['V_E_F_chi'], verify_candidate=save_hit(p, r)))
        decided = st.get('INFEASIBLE', 0) + len(hits)
        secs = sorted(r['seconds'] for r in rs)
        rep['%s_E%d' % (arm, e)] = dict(
            units=len(rs), distinct_units=len({r['i'] for r in rs}), status=st, decided=decided, hits=len(hits),
            hits_verified=sum(c['verify_candidate']['returncode'] == 0 for c in checked), checked=checked,
            rate_wilson=wilson(len(hits), decided),
            zero_hit_rejects_p_at_least=round(-math.log(0.05) / decided, 6) if decided and not hits else None,
            unknown_fraction=round(st.get('UNKNOWN', 0) / len(rs), 4), core_seconds=round(sum(secs), 1),
            median_seconds=secs[len(secs) // 2], max_seconds=secs[-1], rejected_draws=sum(r['rejected'] for r in rs))
    rep['engine_errors'] = sum(r['status'] == 'ENGINE_ERROR' for r in rows)
    rep['core_hours'] = round(sum(r['seconds'] for r in rows) / 3600, 3)
    n2.dump(out / 'summary.json', rep)
    print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk != 'checked'} if isinstance(v, dict) else v)
                      for k, v in rep.items()}, indent=1))
    return rep


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'controls':
        sys.exit(0 if controls(Path(sys.argv[2]))['PASS'] else 1)
    elif cmd == 'sample':
        shard, shards, deadline, out = sys.argv[2:6]
        sample(int(shard), int(shards), float(deadline), Path(out))
    elif cmd == 'summary':
        summary(Path(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
