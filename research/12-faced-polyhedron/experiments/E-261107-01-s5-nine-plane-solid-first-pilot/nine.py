"""Nine-plane solid-first target pilot: the E-261103-05 engine on uniform 9-plane arrangements."""
import argparse
import concurrent.futures as cf
import json
from pathlib import Path
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'E-261103-05-s5-symmetric-solid-first'))
import pilot as base
from ladder_exact import verify
from solid_fast import Tables
from solid_cpsat import best_solid

E9 = 39  # genus 3, 9 faces: V - E + F = -4 with 3V = 2E


def planes(family, seed):
    """Deterministic uniform draw; returns (rows, rejected). C3: 3 orbits of the cyclic coordinate shift."""
    rng = random.Random(2611070100 + 1000 * ('c3', 'd2p1', 'rand').index(family) + seed)
    nz = [i for i in range(-8, 9) if i]
    for rejected in range(200):
        if family == 'c3':
            rows = []
            for _ in range(3):
                a, b, c = (rng.choice(nz) for _ in range(3)); d = -rng.randint(1, 8)
                rows += [[a, b, c, d], [c, a, b, d], [b, c, a, d]]
        elif family == 'd2p1':
            rows = []
            for _ in range(2):
                abc = [rng.choice(nz) for _ in range(3)]; d = -rng.randint(1, 8)
                rows += [[s * x for s, x in zip(sg, abc)] + [d]
                         for sg in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
            rows.append([rng.choice(nz) for _ in range(3)] + [-rng.randint(1, 8)])
        else:
            rows = [[rng.choice(nz) for _ in range(3)] + [-rng.randint(1, 8)] for _ in range(9)]
        try:
            base.arrangement(rows)
            return rows, rejected
        except ValueError:
            continue
    raise ValueError('no uniform arrangement in 200 draws')


def worker(args):
    u = json.loads(args.input.read_text()); h = base.integer_planes(u['planes'])
    a = base.arrangement(h); tables = Tables(a)
    mp = args.output.with_suffix('.model.pbtxt')
    cells, info = best_solid(a, tables, time_limit=u['cap'], target_edges=u['edges'], max_runs=3, model_path=mp)
    res = dict(phase_a=info, bounded_cells=len(tables.cells), model_sha256=base.sha(mp))
    if cells is not None:
        solid = {tables.cells[i] for i, v in enumerate(cells) if v}
        links = base.extract_links(a, solid)
        res.update(planes=h, links=links, geometry=verify(h, links, require_all_pairs=True))
        if 'links' in u:
            exp = {int(k): v for k, v in u['links'].items()}
            res['expected_map_match'] = all(base.cyclic_equal(links[i], exp[i]) for i in range(len(h)))
        base.validate_result(dict(solver=info, geometry=res['geometry']), dict(planes=h, edges=u['edges']))
        base.dump(args.output.with_suffix('.candidate.json'), base.candidate_record(res))
    if u.get('diagnostic_cap') and (cells is None or 'links' in u):  # best pair count, diagnostic only
        _, d = best_solid(a, tables, time_limit=u['diagnostic_cap'], max_runs=3, max_cuts=0)
        res['pairs_diagnostic'] = d
    base.dump(args.output, res)


def run_unit(out, name, u):
    ip, op = out / (name + '.input.json'), out / (name + '.output.json'); base.dump(ip, u)
    t0 = time.monotonic(); budget = u['cap'] + u.get('diagnostic_cap', 0) + 30
    rc = base.command([sys.executable, str(Path(__file__).resolve()), '--input', str(ip), '--output', str(op)],
                      out / (name + '.log'), budget)
    r = json.loads(op.read_text()) if rc == 0 else dict(status='HARD-TIMEOUT' if rc is None else 'ERROR')
    r.update(unit=name, wall_seconds=time.monotonic() - t0, returncode=rc, budget_seconds=budget)
    base.dump(out / (name + '.result.json'), r)
    return r


def verdict(r):
    st = r.get('phase_a', {}).get('status', r.get('status'))
    return 'SOLID' if r.get('geometry', {}).get('EMBEDDED') else st


def main(args):
    out = args.out; out.mkdir(parents=True, exist_ok=False)
    t0 = time.monotonic(); cap = args.cap
    tetra = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]]
    c3_0 = planes('c3', 0)[0]
    controls = {'neg_tetra_E7': dict(planes=tetra, edges=7, cap=5),
                'neg_nine_E33': dict(planes=c3_0, edges=33, cap=60)}
    for name, h, links in base.fixtures():
        controls[name + '_E36'] = dict(planes=h, links=links, edges=36, cap=60, diagnostic_cap=60)
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
                    started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), workers=args.workers, cap=cap,
                    seeds=args.seeds)
    base.dump(out / 'manifest.json', manifest)
    summary = dict(controls={}, units={}, status='RUNNING')
    with cf.ThreadPoolExecutor(args.workers) as pool:
        res = dict(zip(controls, pool.map(lambda kv: run_unit(out, *kv), controls.items())))
        summary['controls'] = {k: verdict(v) for k, v in res.items()}
        ok = (summary['controls']['neg_tetra_E7'] == 'INFEASIBLE' and summary['controls']['neg_nine_E33'] == 'INFEASIBLE'
              and all(res[k].get('expected_map_match') and res[k]['pairs_diagnostic']['adjacent'] == 28
                  for k in res if k.endswith('_E36')))
        if not ok:
            summary['status'] = 'CONTROL-FAILED'
        else:
            jobs = {}
            for fam in ('c3', 'd2p1', 'rand'):
                for s in range(args.seeds):
                    rows, rej = planes(fam, s)
                    jobs[f'{fam}_s{s}'] = dict(planes=rows, edges=E9, cap=cap, diagnostic_cap=60, rejected=rej)
            futs = {pool.submit(run_unit, out, k, u): k for k, u in jobs.items()}
            for f in cf.as_completed(futs):
                r = f.result(); summary['units'][futs[f]] = dict(
                    verdict=verdict(r), pairs=r.get('pairs_diagnostic', {}).get('adjacent'), wall=round(r['wall_seconds'], 1))
                base.dump(out / 'summary.json', summary)
            found = [k for k, v in summary['units'].items() if v['verdict'] == 'SOLID']
            summary['status'] = 'SOLID-FOUND' if found else 'NO-36-PAIR-SOLID'
    manifest.update(ended_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), wall_seconds=time.monotonic() - t0,
                    core_hours_upper=(time.monotonic() - t0) * args.workers / 3600, status=summary['status'])
    base.dump(out / 'summary.json', summary); base.dump(out / 'manifest.json', manifest)
    print(summary['status'], json.dumps(summary['controls']), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path); ap.add_argument('--input', type=Path); ap.add_argument('--output', type=Path)
    ap.add_argument('--workers', type=int, default=10); ap.add_argument('--seeds', type=int, default=10)
    ap.add_argument('--cap', type=int, default=180)
    a = ap.parse_args()
    worker(a) if a.input else main(a)
