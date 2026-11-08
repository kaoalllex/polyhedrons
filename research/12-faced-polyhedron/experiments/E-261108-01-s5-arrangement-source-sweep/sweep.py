"""Arrangement-source sweep: the E-261107-01 engine (nine.py, unchanged) on 300 nine-plane arrangements from three sources."""
import argparse
import gzip
import json
import math
from pathlib import Path
import random
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'E-261107-01-s5-nine-plane-solid-first-pilot'))
import nine
base = nine.base

FAMILIES = ('rv9', 'mz9', 'inv9')
PER_FAMILY = 100
NZ = [i for i in range(-8, 9) if i]


def ninth(rows, rng):
    """Random plane at the scale of the 8 known ones: offset 0.3-1.0 of the median plane distance from the origin."""
    scale = statistics.median(abs(r[3]) / math.sqrt(sum(x * x for x in r[:3])) for r in rows)
    n = [rng.choice(NZ) for _ in range(3)]
    return n + [-max(1, round(rng.uniform(.3, 1) * scale * math.sqrt(sum(x * x for x in n))))]


def involution_planes(rng):
    """C2 about z, (x, y, z) -> (-x, -y, z): 4 swapped pairs + 1 fixed plane through the axis. (A mirror makes 4 planes
    meet at points of the mirror plane, and a z-normal fixed plane has dependent normals: both are non-uniform.)"""
    pairs = []
    for _ in range(4):
        a, b, c = (rng.choice(NZ) for _ in range(3)); d = -rng.randint(1, 8)
        pairs += [[a, b, c, d], [-a, -b, c, d]]
    a, b = rng.choice(NZ), rng.choice(NZ)
    return pairs + [[a, b, 0, 0]]


def planes(family, seed):
    """Deterministic uniform draw; returns (rows, rejected). seed 0..99 within the family."""
    rng = random.Random(2611080100 + 1000 * FAMILIES.index(family) + seed)
    if family != 'inv9':
        known = dict((n, h) for n, h, _ in base.fixtures())['roest_vigh' if family == 'rv9' else 'mizhaev']
    for rejected in range(200):
        rows = involution_planes(rng) if family == 'inv9' else base.integer_planes(known) + [ninth(known, rng)]
        try:
            base.arrangement(rows)
            return rows, rejected
        except ValueError:
            continue
    raise ValueError('no uniform arrangement in 200 draws')


def units():
    """300 units interleaved by family so that a budget cut or a shard split keeps the families balanced."""
    return [f'{f}_s{s:03d}' for s in range(PER_FAMILY) for f in FAMILIES]


def controls():
    tetra = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]]
    c = {'neg_tetra_E7': dict(planes=tetra, edges=7, cap=5),
         'neg_nine_E33': dict(planes=nine.planes('c3', 0)[0], edges=33, cap=60)}
    for name, h, links in base.fixtures():
        c[name + '_E36'] = dict(planes=h, links=links, edges=36, cap=60)
    return c


def passed(name, r):
    v = nine.verdict(r)
    return v == 'INFEASIBLE' if name.startswith('neg_') else v == 'SOLID' and r.get('expected_map_match') is True


def done_units(out):
    f = out / 'results.jsonl'
    return {json.loads(l)['unit'] for l in f.read_text().splitlines()} if f.exists() else set()


def append(path, rec):
    with path.open('a') as s:
        s.write(json.dumps(rec) + '\n')


def run_shard(args):
    out = args.out; out.mkdir(parents=True, exist_ok=True)
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
                    started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), shard=args.shard,
                    shards=args.shards, cap=args.cap, budget_seconds=args.budget)
    base.dump(out / f'manifest-{int(time.time())}.json', manifest)
    spent = 0.0
    for name, u in controls().items():  # every shard, every start: engine sanity before any unit
        r = nine.run_unit(out, name, u); spent += r['wall_seconds']
        append(out / 'controls.jsonl', dict(unit=name, verdict=nine.verdict(r), passed=passed(name, r),
                                            wall_seconds=r['wall_seconds']))
        if not passed(name, r):
            print('CONTROL-FAILED', name, nine.verdict(r), flush=True); return 3
    mine = [u for i, u in enumerate(units()) if i % args.shards == args.shard and u not in done_units(out)]
    spent += sum(json.loads(l).get('wall_seconds', 0) for l in (out / 'results.jsonl').read_text().splitlines()) \
        if (out / 'results.jsonl').exists() else 0
    for name in mine:
        if spent >= args.budget:
            print(f'BUDGET-STOP after {spent:.0f} s; {len(mine)} left at start', flush=True); return 4
        family, seed = name.split('_s')
        rows, rej = planes(family, int(seed))
        r = nine.run_unit(out, name, dict(planes=rows, edges=nine.E9, cap=args.cap, rejected=rej))
        spent += r['wall_seconds']
        mp = out / f'{name}.output.model.pbtxt'
        if mp.exists():
            with mp.open('rb') as f, gzip.open(str(mp) + '.gz', 'wb') as g:
                g.write(f.read())
            mp.unlink()
        append(out / 'results.jsonl', dict(unit=name, verdict=nine.verdict(r), wall_seconds=r['wall_seconds'],
                                           rejected=rej, ended_by=r.get('phase_a', {}).get('ended_by'),
                                           model_sha256=r.get('model_sha256') or r.get('phase_a', {}).get('model_sha256'),
                                           solid=nine.verdict(r) == 'SOLID'))
        print(name, nine.verdict(r), round(r['wall_seconds'], 1), flush=True)
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path); ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=10); ap.add_argument('--cap', type=int, default=60)
    ap.add_argument('--budget', type=float, default=720, help='core-seconds per shard, controls included')
    ap.add_argument('--list', action='store_true', help='print the draws and exit')
    a = ap.parse_args()
    if a.list:
        for u in units():
            f, s = u.split('_s'); print(u, planes(f, int(s)))
    else:
        sys.exit(run_shard(a))
