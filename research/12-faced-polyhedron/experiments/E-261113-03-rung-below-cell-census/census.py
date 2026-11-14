"""E-261113-03 rung-below cell census: every generic cell of an eighth plane over seven planes of Roest-Vigh (one
plane deleted per symmetry class), decided by the frozen Stage A model at eight faces (stage_a.worker: 28 pairs,
<= 3 runs per pair, connected disk faces, edge runs >= 30, genus free); SOLID cells classed by canonical map and genus.

List (exact, `python3 census.py --list OUT`): D = the 56 dual vectors of the triples of the seven planes and INF.
Every projective cell of D has a vertex X (a rank-3 flat of D), so the cells are the union over X of X + eps * b,
b a region of the local rank-3 arrangement {w in D : w . X = 0} (cells.local_cells, the Stage A algorithm). Checks:
per vertex, found local regions = 2 (1 + c2) (Zaslavsky, rank 3); the deduplicated union = m + c3, the projective
region count of D (Zaslavsky, rank 4; central r = 2 (m + c3) since chi(1) = 0), from the flats directly; random
integer planes all land in the union; the deleted plane's own cell (planted) is in the union. Representatives:
cells.representative (max-margin LP rounded to 1e-9, checked exactly). The stabiliser of the deleted plane is trivial
(checked), so every cell is one unit.
Runner (`run.sh` -> --out DIR --shard S --shards N): controls first on every start (C0 Roest-Vigh unseeded, C2
tetrahedron INFEASIBLE, P<d> the planted cell's list unit SOLID with all pairs at eight faces), then the shard's units
under the budget (total / SHARDS core-s). A SOLID does not stop the census. INFEASIBLE is UNSAT-SOLVER for the exact
model; UNKNOWN / HARD-TIMEOUT leave the unit open. --summary prints counts, timing, the price and the map classes.
"""
import argparse
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'E-261112-01-ninth-plane-stage-a'))
import cells  # noqa: E402
import stage_a  # noqa: E402
base = cells.base
from cells import Fr, canon, cross4, dot, rank  # noqa: E402

SOURCE = 'roest_vigh'
UNITS = HERE / 'list' / 'units.json.gz'                # gzip of the compact JSON; the hash is of the JSON
UNITS_SHA256 = '9cda089c7171aa8e6141d3e6002a679239b46c7f02718393307424292a7315da'
TOTAL_CORE_SECONDS = 20 * 3600                       # ROADMAP row: owner day run <= 20 core-h
PILOT_UNITS, PILOT_CORE_SECONDS = 5, 0.5 * 3600      # 10 shards x 5 = the 50 timed cells
EDGES_MIN = 30
MC_SAMPLES = 5000


# ---- exact list ----

def deletions(h):
    """The smallest plane index of every orbit of the source's symmetries on its planes."""
    S = [canon(r) for r in h]; G = cells.symmetries(h); out = set()
    for r in h:
        out.add(min(S.index(canon(g(r))) for _, g in G))
    return sorted(out)


def vertices(D):
    """Rank-3 flats of D as projective points X (primitive integer vectors)."""
    return sorted({canon(v) for t in itertools.combinations(D, 3) if any(v := cross4(*t))})


def perturb(D, X, b):
    """X + eps * b; every w in D with w . X != 0 keeps that sign (exact)."""
    off = [abs(dot(w, X)) for w in D if dot(w, X)]
    eps = min(off) / (2 * max(abs(dot(w, b)) for w in D) + 1)
    return [Fr(x) + eps * y for x, y in zip(X, b)]


def flats2(V, idx):
    """Rank-2 flats among the pairwise independent vectors V[idx], as index lists."""
    seen = set(); out = []
    for i, j in itertools.combinations(idx, 2):
        if (i, j) in seen:
            continue
        f = [k for k in idx if rank([V[i], V[j], V[k]]) == 2]
        out.append(f); seen.update(itertools.combinations(f, 2))
    return out


def zaslavsky_rank4(D):
    """Projective regions m + c3 of the central rank-4 arrangement D, from its flats (no region is constructed)."""
    assert rank(D) == 4 and len({canon(w) for w in D}) == len(D)
    flats = {}
    for t in itertools.combinations(range(len(D)), 3):
        if rank([D[i] for i in t]) == 3:
            flats.setdefault(canon(cross4(*[D[i] for i in t])), set()).update(t)
    c3 = 0
    for n in flats:
        s = [k for k in range(len(D)) if dot(n, D[k]) == 0]
        c3 += sum(len(f) - 1 for f in flats2(D, s)) - len(s) + 1
    return len(D) + c3, len(flats)


def enumerate_cells(D):
    """{key: plane} over all vertices of D, each vertex's local count checked; also the vertex statistics."""
    union = {}; local = 0; V = vertices(D)
    for X in V:
        W = [w for w in D if dot(w, X) == 0]
        loc = cells.local_cells(X, W)
        if len(loc) != cells.zaslavsky_rank3(W):
            raise ArithmeticError(f'vertex {X}: {len(loc)} local regions, Zaslavsky {cells.zaslavsky_rank3(W)}')
        local += len(loc)
        for b in loc.values():
            p = perturb(D, X, b)
            union.setdefault(cells.key_of(D, p), p)
    return union, len(V), local


def monte_carlo(D, union, n, seed):
    rng = random.Random(seed); hit = miss = skipped = 0
    for _ in range(n):
        p = [rng.randint(-1000, 1000) for _ in range(4)]
        try:
            k = cells.key_of(D, p)
        except ArithmeticError:
            skipped += 1; continue
        hit += k in union; miss += k not in union
    return dict(samples=n, in_union=hit, missing=miss, non_generic=skipped)


def build(h, d):
    h7 = [r for i, r in enumerate(h) if i != d]; D = cells.duals(h7)
    assert len(D) == 56, len(D)
    G7 = cells.symmetries(h7)
    if len(G7) != 1:
        raise ArithmeticError('nontrivial stabiliser: orbit reduction needed')
    union, nv, local = enumerate_cells(D)
    count, nflats = zaslavsky_rank4(D)
    if len(union) != count or nflats != nv:
        raise ArithmeticError(f'delete {d}: {len(union)} cells found, Zaslavsky {count}; vertices {nv} vs flats {nflats}')
    mc = monte_carlo(D, union, MC_SAMPLES, 2611130300 + d)
    if mc['missing']:
        raise ArithmeticError(f'delete {d}: random planes outside the union: {mc}')
    planted = cells.key_of(D, h[d])
    if planted not in union:
        raise ArithmeticError(f'delete {d}: the deleted plane\'s cell is not enumerated')
    units = []
    for i, k in enumerate(sorted(union)):
        q, method, margin = cells.representative(D, k, union[k])
        units.append(dict(deletion=d, cell=i, key=cells.key_str(k), method=method, margin=margin,
                          planted=k == planted, eighth=[str(v) for v in q]))
    cert = dict(source=SOURCE, deleted=d, deleted_plane=h[d], seven=h7, duals=len(D), vertices=nv,
                local_regions_total=local, union=len(union), zaslavsky_rank4=count, monte_carlo=mc,
                stabiliser=len(G7), planted_key=cells.key_str(planted),
                methods={m: sum(u['method'] == m for u in units) for m in ('lp', 'witness')},
                keys_sha256=cells.sha(sorted(u['key'] for u in units)),
                reps_sha256=cells.sha([(u['key'], u['eighth']) for u in units]))
    return units, cert


def queue(by_del):
    """Each deletion's cells in a hash order (a fixed pseudo-random order, so the pilot is a spread sample), then
    interleaved in blocks of 10: ordinal modulo 10 gives every shard both deletions."""
    lists = [sorted(us, key=lambda u: hashlib.sha256(u['key'].encode()).hexdigest()) for us in by_del]
    out = []
    while any(lists):
        for lst in lists:
            out += lst[:10]; del lst[:10]
    for i, u in enumerate(out):
        u['ordinal'] = i; u['unit'] = f"d{u['deletion']}_c{u['cell']:05d}"
    return out


# ---- canonical map ----

def map_canon(links):
    """Canonical string of the face map given by the cyclic neighbour lists of the faces (cubic, multiple adjacencies
    allowed): minimum over every root (face, edge, direction) of a breadth-first relabelling; mirror images are equal.
    A vertex is the triple of faces at it; an edge run is matched with its twin by its two end vertices."""
    L = {int(f): list(c) for f, c in links.items()}

    def ends(f, i):
        c = L[f]; n = len(c)
        a, b = frozenset((f, c[i - 1], c[i])), frozenset((f, c[i], c[(i + 1) % n]))
        if len(a) != 3 or len(b) != 3:
            raise ValueError('vertex without three distinct faces')
        return a, b

    mate = {}
    for f, c in L.items():
        for i, g in enumerate(c):
            a, b = ends(f, i)
            m = [(j, 1 if ends(g, j)[0] == b else -1) for j, x in enumerate(L[g]) if x == f and set(ends(g, j)) == {a, b}]
            if len(m) != 1:
                raise ValueError(f'edge run {f}-{g} has {len(m)} twins')
            mate[f, i] = (g,) + m[0]
    best = None
    for f0, c0 in L.items():
        for i0 in range(len(c0)):
            for d0 in (1, -1):
                lab = {f0: 0}; order = [(f0, i0, d0)]; code = []
                for f, i, d in order:
                    c = L[f]
                    for t in range(len(c)):
                        pos = (i + d * t) % len(c); g = c[pos]
                        if g not in lab:
                            _, j, s = mate[f, pos]; lab[g] = len(lab); order.append((g, j, s * d))
                        code.append(lab[g])
                    code.append(-1)
                if best is None or code < best:
                    best = code
    return ' '.join('|' if x < 0 else str(x) for x in best)


def source_maps():
    return {n: map_canon(links) for n, _, links in base.fixtures()}


# ---- runner ----

def load_units():
    data = gzip.decompress(UNITS.read_bytes())
    if hashlib.sha256(data).hexdigest() != UNITS_SHA256:
        raise RuntimeError('units.json.gz differs from the frozen list')
    return json.loads(data)


def planes_of(u):
    h = cells.source_planes(SOURCE)
    return [r for i, r in enumerate(h) if i != u['deletion']] + [u['eighth']]


def classify(r):
    g = r['geometry']; chi = g['V_E_F_chi'][3]
    canon_ = map_canon(r['links'])
    return dict(genus=(2 - chi) // 2, map=canon_, map_sha=hashlib.sha256(canon_.encode()).hexdigest()[:16],
                source_map=canon_ == source_maps()[SOURCE])


def controls(units):
    c = {k: v for k, v in stage_a.controls().items() if k in ('C0_' + SOURCE, 'C2_tetra')}
    for u in units:
        if u['planted']:
            c[f"P{u['deletion']}_{u['unit']}"] = dict(planes=planes_of(u), edges_min=EDGES_MIN, key=u['key'])
    return c


def passed(name, r):
    if name.startswith('C2'):
        return r['verdict'] == 'INFEASIBLE'
    g = r.get('geometry', {})
    return r['verdict'] == 'SOLID' and g.get('all_pairs_adjacent') is True and g['V_E_F_chi'][2] == 8


def drop_raw(raw, name):
    for f in raw.glob(name + '.*'):
        f.unlink()


def run_shard(a):
    out = a.out; out.mkdir(parents=True, exist_ok=True); raw = out / 'raw'
    units = load_units()
    budget = a.budget if a.budget is not None else (PILOT_CORE_SECONDS if a.pilot else TOTAL_CORE_SECONDS) / a.shards
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    base.dump(out / f'manifest-{stamp}.json', dict(
        commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        dirty=subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], text=True),
        started_utc=stamp, shard=a.shard, shards=a.shards, cap=a.cap, budget_core_seconds=budget, pilot=a.pilot,
        units_sha256=UNITS_SHA256, python=sys.version, cpu_count=os.cpu_count(),
        executable=sys.executable.replace(str(Path.home()), '~', 1)))
    base.command([sys.executable, '-m', 'pip', 'freeze'], out / f'pip-freeze-{stamp}.txt', 60)
    rec = stage_a.records
    spent = sum(r['wall_seconds'] for f in ('controls.jsonl', 'results.jsonl') for r in rec(out / f))
    for name, u in controls(units).items():
        r = stage_a.run_unit(raw, name, dict(planes=u['planes'], edges_min=u['edges_min'], cap=a.cap))
        spent += r['wall_seconds']; ok = passed(name, r)
        row = dict(unit=name, started=stamp, passed=ok, edges_min=u['edges_min'], key=u.get('key'),
                   **{k: r.get(k) for k in ('verdict', 'wall_seconds', 'cpu_seconds', 'model_sha256', 'links',
                                            'solver', 'error_tail')}, V_E_F_chi=r.get('geometry', {}).get('V_E_F_chi'))
        if r['verdict'] == 'SOLID':
            row.update(classify(r))
        stage_a.append(out / 'controls.jsonl', row)
        if ok:
            drop_raw(raw, name)
        print(name, r['verdict'], ok, round(r['wall_seconds'], 1), row.get('map_sha', ''), flush=True)
        if not ok:
            print('CONTROL-FAILED', name, flush=True); return 3
    done = {r['unit'] for d in out.parent.glob('[0-9]*') for r in rec(d / 'results.jsonl')}
    mine = [u for u in units if u['ordinal'] % a.shards == a.shard]
    pilot = {u['unit'] for u in mine[:PILOT_UNITS]}
    if a.pilot:
        mine = mine[:PILOT_UNITS]
    todo = [u for u in mine if u['unit'] not in done]
    D = {d: cells.duals([r for i, r in enumerate(cells.source_planes(SOURCE)) if i != d]) for d in {u['deletion'] for u in todo}}
    for u in todo:
        if not stage_a.can_start(spent, a.cap, budget):
            print(f'BUDGET-STOP at {spent:.0f} of {budget:.0f} core-s; {len(todo)} were open at start', flush=True); return 4
        if cells.key_str(cells.key_of(D[u['deletion']], [Fr(v) for v in u['eighth']])) != u['key']:
            raise ArithmeticError(u['unit'] + ': representative is not in its cell')
        r = stage_a.run_unit(raw, u['unit'], dict(planes=planes_of(u), edges_min=EDGES_MIN, cap=a.cap))
        spent += r['wall_seconds']
        row = dict(unit=u['unit'], ordinal=u['ordinal'], deletion=u['deletion'], planted=u['planted'],
                   phase='pilot' if u['unit'] in pilot else 'day', started=stamp,
                   **{k: r.get(k) for k in ('verdict', 'wall_seconds', 'cpu_seconds', 'budget_fraction', 't_tables',
                                            't_solve', 'bounded_cells', 'model_sha256', 'returncode', 'error_tail')},
                   ended_by=r.get('solver', {}).get('ended_by'), solver_seconds=r.get('solver', {}).get('seconds'))
        if r['verdict'] == 'SOLID':
            row.update(links=r['links'], V_E_F_chi=r['geometry']['V_E_F_chi'], edge_runs=r['solver']['edge_runs'],
                       all_pairs=r['geometry']['all_pairs_adjacent'], **classify(r))
            if row['source_map']:                    # the record keeps the map; the planes follow from the list
                drop_raw(raw, u['unit'])
            else:                                    # raw/<unit>.output.candidate.json: verify_candidate.py --all-pairs
                print('NEW-MAP', u['unit'], row['map_sha'], 'genus', row['genus'], flush=True)
        stage_a.append(out / 'results.jsonl', row)
        print(u['unit'], r['verdict'], round(r['wall_seconds'], 1), row.get('map_sha', ''), flush=True)
    print(f'SHARD-DONE {len(todo)} units at {spent:.0f} of {budget:.0f} core-s', flush=True)
    return 0


def summary(root):
    units = load_units(); by = {u['unit']: u for u in units}
    rs = [r for d in sorted(root.glob('[0-9]*')) for r in stage_a.records(d / 'results.jsonl')]
    cs = [r for d in sorted(root.glob('[0-9]*')) for r in stage_a.records(d / 'controls.jsonl')]
    seen = [r['unit'] for r in rs]
    assert len(seen) == len(set(seen)) and set(seen) <= set(by), 'duplicate or foreign unit records'
    walls = [r['wall_seconds'] for r in rs]
    verdicts = {}
    for r in rs:
        verdicts[r['verdict']] = verdicts.get(r['verdict'], 0) + 1
    classes = {}
    for r in rs + [c for c in cs if c.get('map')]:
        if r.get('map'):
            k = (r['map_sha'], r['genus'], r['source_map'])
            classes[k] = classes.get(k, 0) + 1
    left = len(units) - len(rs)
    ctrl_s = sum(c['wall_seconds'] for c in cs)
    out = dict(units=len(units), recorded=len(rs), left=left, verdicts=verdicts,
               controls=dict(records=len(cs), failed=[c['unit'] for c in cs if not c['passed']], wall_seconds=round(ctrl_s, 1)),
               wall=dict(mean=round(statistics.mean(walls), 2), median=round(statistics.median(walls), 2),
                         max=max(walls), min=min(walls), sum_core_h=round(sum(walls) / 3600, 3)) if walls else None,
               ended_by={k: sum(r.get('ended_by') == k for r in rs) for k in {r.get('ended_by') for r in rs}},
               projected_total_core_h=round((sum(walls) + statistics.mean(walls) * left + ctrl_s) / 3600, 2) if walls else None,
               planted=[(r['unit'], r['verdict'], r.get('map_sha'), r.get('source_map')) for r in rs if by[r['unit']]['planted']],
               source_map_sha=hashlib.sha256(source_maps()[SOURCE].encode()).hexdigest()[:16],
               map_classes=[dict(map_sha=k[0], genus=k[1], source_map=k[2], records=v) for k, v in sorted(classes.items())],
               open=[r['unit'] for r in rs if r['verdict'] not in ('SOLID', 'INFEASIBLE')])
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', type=Path); ap.add_argument('--summary', type=Path)
    ap.add_argument('--out', type=Path); ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=10); ap.add_argument('--cap', type=float, default=60)
    ap.add_argument('--budget', type=float, default=None); ap.add_argument('--pilot', action='store_true')
    a = ap.parse_args()
    if a.list:
        h = cells.source_planes(SOURCE); by_del = []; certs = []
        for d in deletions(h):
            t0 = time.process_time(); us, cert = build(h, d); cert['cpu_seconds'] = round(time.process_time() - t0, 1)
            by_del.append(us); certs.append(cert)
            print(json.dumps({k: cert[k] for k in ('deleted', 'vertices', 'union', 'zaslavsky_rank4', 'monte_carlo',
                                                    'methods', 'cpu_seconds')}), flush=True)
        units = queue(by_del); a.list.mkdir(parents=True, exist_ok=True)
        data = ('[\n' + ',\n'.join(json.dumps(u, separators=(',', ':')) for u in units) + '\n]\n').encode()
        (a.list / 'units.json.gz').write_bytes(gzip.compress(data, mtime=0))
        maps = source_maps()
        for c in certs:
            c['units_json_sha256'] = hashlib.sha256(data).hexdigest()
        (a.list / 'certificate.json').write_text(json.dumps(dict(
            deletions=certs, source_maps={n: dict(canon=m, sha=hashlib.sha256(m.encode()).hexdigest()[:16])
                                          for n, m in maps.items()}), indent=1) + '\n')
        print('units', len(units), 'units JSON sha256', hashlib.sha256(data).hexdigest())
    elif a.summary:
        summary(a.summary)
    else:
        sys.exit(run_shard(a))
