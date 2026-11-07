"""Bounded disk-aware solid-first controls and random D2 recovery pilot."""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
import numpy as np
from ladder_exact import solve3, verify
from solid_fast import Tables
from solid_cpsat import best_solid


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def integer_planes(rows):
    out = []
    for row in rows:
        q = [Fraction(str(x)) for x in row]
        scale = math.lcm(*(x.denominator for x in q))
        h = [int(x * scale) for x in q]
        common = math.gcd(*h)
        if not common or not any(h[:3]):
            raise ValueError('zero plane normal')
        out.append([x // common for x in h])
    return out


def sign(x):
    return (x > 0) - (x < 0)


def arrangement(rows):
    """Exact chamber/segment combinatorics, with checked float points for existing Tables."""
    h = integer_planes(rows); n = len(h)
    points = {}; cells = {}; unbounded = set(); ones = {}
    for t in itertools.combinations(range(n), 3):
        try:
            p = solve3([h[i] for i in t])
        except AssertionError as exc:
            raise ValueError('nonuniform triple of normals') from exc
        base = [sign(sum(a * b for a, b in zip(row[:3], p)) + row[3]) for row in h]
        if any(base[i] == 0 for i in range(n) if i not in t):
            raise ValueError('four concurrent planes')
        pf = np.array([float(x) for x in p])
        floating = np.sign(np.asarray(h, float)[:, :3] @ pf + np.asarray(h, float)[:, 3])
        if any(int(floating[i]) != base[i] for i in range(n) if i not in t):
            raise ArithmeticError('float point signs disagree with exact arrangement')
        points[t] = p
        for octant in itertools.product((-1, 1), repeat=3):
            key = base[:]
            for i, s in zip(t, octant):
                key[i] = s
            cells.setdefault(tuple(key), []).append(pf)
    for x, y in itertools.combinations(range(n), 2):
        a, b = h[x], h[y]
        d = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
        for direction in (-1, 1):
            base = [sign(direction * sum(a * b for a, b in zip(row[:3], d))) for row in h]
            if any(base[i] == 0 for i in range(n) if i not in (x, y)):
                raise ValueError('nonuniform direction at infinity')
            for sx, sy in itertools.product((-1, 1), repeat=2):
                key = base[:]; key[x] = sx; key[y] = sy; unbounded.add(tuple(key))
        ordered = sorted((sum(a * b for a, b in zip(points[tuple(sorted((x, y, z)))], d)), z)
                         for z in range(n) if z not in (x, y))
        segments = []
        for (_, z), (_, w) in zip(ordered, ordered[1:]):
            p, q = points[tuple(sorted((x, y, z)))], points[tuple(sorted((x, y, w)))]
            mid = [(a + b) / 2 for a, b in zip(p, q)]
            base = [sign(sum(a * b for a, b in zip(row[:3], mid)) + row[3]) for row in h]
            base[x] = base[y] = 0
            if any(base[i] == 0 for i in range(n) if i not in (x, y)):
                raise ValueError('degenerate segment midpoint')
            segments.append((tuple(base), z, w))
        ones[(x, y)] = segments
    return SimpleNamespace(H=np.asarray(h, float), n=n, P={t: np.array([float(x) for x in p]) for t, p in points.items()},
                           cells=cells, bounded=set(cells) - unbounded, ones=ones)


def extract_links(a, solid):
    """Trace actual boundary edge runs; triangle sets alone lose parallel-edge pairing."""
    from solid_first import _cell
    edges = []
    for (x, y), segments in a.ones.items():
        active = [sum(_cell(sv, x, sx, y, sy) in solid for sx, sy in itertools.product((-1, 1), repeat=2)) % 2
                  for sv, _, _ in segments]
        start = None
        for k in range(len(segments) + 1):
            if k < len(segments) and active[k]:
                if start is None:
                    start = k
            elif start is not None:
                edges.append((x, y, tuple(sorted((x, y, segments[start][1]))),
                              tuple(sorted((x, y, segments[k - 1][2])))))
                start = None
    links = {}
    for face in range(a.n):
        graph = {}
        for x, y, u, v in edges:
            if face in (x, y):
                other = y if face == x else x
                graph.setdefault(u, []).append((v, other)); graph.setdefault(v, []).append((u, other))
        if not graph or any(len(es) != 2 for es in graph.values()):
            raise ValueError('boundary is not a cubic face cycle')
        first = min(graph); current = first; previous = None; cycle = []; seen = set()
        while current not in seen:
            seen.add(current)
            options = [e for e in graph[current] if e[0] != previous]
            following, other = min(options)
            cycle.append(other); previous, current = current, following
        if current != first or seen != set(graph):
            raise ValueError('face has multiple boundary cycles')
        links[face] = cycle
    return links


def cyclic_equal(a, b):
    return any(a == row[k:] + row[:k] for row in (b, b[::-1]) for k in range(len(row)))


def candidate_record(result):
    return dict(planes=result['planes'], links=result['links'])


def validate_result(result, inp):
    status = result['solver']['status']
    if status not in ('OPTIMAL', 'FEASIBLE', 'INFEASIBLE', 'UNKNOWN'):
        raise RuntimeError('unexpected CP-SAT status: ' + status)
    if status in ('OPTIMAL', 'FEASIBLE'):
        g = result.get('geometry', {})
        e = inp['edges']; n = len(inp['planes'])
        if (not g.get('EMBEDDED') or e % 3 or
                tuple(g.get('V_E_F_chi', ())) != (2 * e // 3, e, n, n - e // 3)):
            raise ArithmeticError('hard model disagrees with exact geometry/topology')


def worker(args):
    inp = json.loads(args.input.read_text()); h = integer_planes(inp['planes'])
    a = arrangement(h); tables = Tables(a)
    model_path = args.output.with_suffix('.model.pbtxt')
    cells, info = best_solid(a, tables, time_limit=inp['solver_seconds'], target_edges=inp['edges'], max_runs=3,
                             model_path=model_path)
    result = dict(solver=info, bounded_cells=len(tables.cells), model_sha256=sha(model_path))
    if cells is not None:
        assert info['valid'], 'hard disk model disagrees with boundary diagnostics'
        solid = {tables.cells[i] for i, value in enumerate(cells) if value}
        links = extract_links(a, solid)
        result.update(planes=h, links=links, solid=sorted(solid), geometry=verify(h, links, require_all_pairs=True))
        if 'links' in inp:
            expected = {int(k): v for k, v in inp['links'].items()}
            result['expected_map_match'] = all(cyclic_equal(links[i], expected[i]) for i in range(len(h)))
    validate_result(result, inp)
    dump(args.output, result)
    if 'geometry' in result:
        dump(args.output.with_suffix('.candidate.json'), candidate_record(result))


def command(args, log, timeout):
    with log.open('w') as stream:
        p = subprocess.Popen(args, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            return p.wait(timeout=max(.001, timeout))
        except BaseException as exc:
            os.killpg(p.pid, signal.SIGKILL); p.wait()
            if not isinstance(exc, subprocess.TimeoutExpired):
                raise
            return None


def fixtures():
    from control_rost_vigh import build
    h, links = build()
    mz = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())
    raw = mz['links_0based']
    ml = {int(k): v for k, v in raw.items()} if isinstance(raw, dict) else dict(enumerate(raw))
    return [('roest_vigh', h, links), ('mizhaev', mz['planes_abcd_zero_form'], ml)]


def random_d2(seed):
    import random
    rng = random.Random(2611030500 + seed)
    signs = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    rejected = 0
    while rejected < 200:
        rows = []
        for orbit in range(2):
            abc = [rng.choice([i for i in range(-8, 9) if i]) for _ in range(3)]; d = -rng.randint(1, 8)
            rows.extend([[s * a for s, a in zip(sg, abc)] + [d] for sg in signs])
        try:
            arrangement(rows)
            return rows, rejected
        except ValueError:
            rejected += 1
    raise ValueError('no uniform D2 arrangement in 200 attempts')


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); deadline = start + 2400
    report = dict(status='RUNNING', controls={}, random={}, target='S1 controls (8,3); focus S5 (9,3) not run')
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    branch=subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
                    started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), python=sys.version,
                    host=platform.platform(), cpu_count=os.cpu_count(), workers=1, wall_budget_seconds=2400)
    dump(out / 'manifest.json', manifest)
    command([sys.executable, '-m', 'pip', 'freeze'], out / 'pip-freeze.txt', 20)
    def remaining(cap):
        value = min(cap, deadline - time.monotonic())
        if value <= 0:
            raise TimeoutError('pilot deadline exhausted')
        return value
    def save():
        dump(out / 'summary.json', report)
    def expired(signum, frame):
        raise TimeoutError('pilot hard deadline exhausted')
    def run(name, inp):
        ip = out / (name + '.input.json'); op = out / (name + '.output.json'); dump(ip, inp)
        t0 = time.monotonic()
        rc = command([sys.executable, str(Path(__file__).resolve()), '--input', str(ip), '--output', str(op)],
                     out / (name + '.log'), remaining(inp['solver_seconds'] + 20))
        result = json.loads(op.read_text()) if rc == 0 else dict(status='HARD-TIMEOUT' if rc is None else 'ERROR')
        result.update(wall_seconds=time.monotonic() - t0, subprocess_returncode=rc,
                      subprocess_budget_seconds=inp['solver_seconds'] + 20)
        if result.get('status') == 'ERROR':
            raise RuntimeError(name + ' failed; see raw log')
        return result
    signal.signal(signal.SIGALRM, expired); signal.setitimer(signal.ITIMER_REAL, remaining(2400))
    try:
        tetra = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]]
        r = run('negative_tetra', dict(planes=tetra, edges=7, solver_seconds=5))
        report['controls']['negative_tetra'] = r; save()
        assert r.get('solver', {}).get('status') == 'INFEASIBLE', r
        for name, h, links in fixtures():
            passed = False
            for cap in (15, 60):
                key = f'{name}_{cap}'
                r = run(key, dict(planes=h, links=links, edges=36, solver_seconds=cap))
                report['controls'][key] = r; save()
                geometry = r.get('geometry', {})
                passed = (geometry.get('EMBEDDED') and geometry.get('V_E_F_chi') == [24, 36, 8, -4]
                          and r.get('expected_map_match'))
                print(key, r.get('solver', {}).get('status', r.get('status')), 'exact_known_map', bool(passed), flush=True)
                if passed:
                    break
                if r.get('solver', {}).get('status') == 'INFEASIBLE':
                    break
            if not passed:
                report['status'] = 'R2-FAILED'; save(); return
        for seed in range(16):
            h, rejected = random_d2(seed)
            for cap in (15, 60):
                name = f'd2_seed{seed}_{cap}'
                r = run(name, dict(planes=h, edges=36, solver_seconds=cap, seed=seed, rejected=rejected))
                report['random'][name] = r; save()
                geometry = r.get('geometry', {})
                passed = geometry.get('EMBEDDED') and geometry.get('V_E_F_chi') == [24, 36, 8, -4]
                print(name, r.get('solver', {}).get('status', r.get('status')), 'exact_8_3', bool(passed), flush=True)
                if passed:
                    report['status'] = 'R3-FOUND'; save(); return
                if r.get('solver', {}).get('status') == 'INFEASIBLE':
                    break
        report['status'] = 'R3-NOT-FOUND'
    except TimeoutError as exc:
        report.update(status='PILOT-TIMEOUT', error=str(exc))
    except BaseException as exc:
        report.update(status='ERROR', error=repr(exc)); raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0); save()
        manifest['status'] = report['status']
        manifest['ended_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        manifest['sources_sha256'] = {str(p.relative_to(ROOT)): sha(p) for p in
                                      (Path(__file__).resolve(), ROOT / 'code/solid_cpsat.py', ROOT / 'code/solid_fast.py')}
        manifest['outputs_sha256'] = {p.name: sha(p) for p in out.iterdir() if p.is_file() and p.name != 'manifest.json'}
        manifest['wall_seconds'] = time.monotonic() - start; manifest['core_hours'] = manifest['wall_seconds'] / 3600
        dump(out / 'manifest.json', manifest)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path); ap.add_argument('--input', type=Path); ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.input:
        worker(args)
    else:
        main(args.out)
