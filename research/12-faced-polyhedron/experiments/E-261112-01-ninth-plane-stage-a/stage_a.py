"""E-261112-01 runner: hard S1 decision (all pairs adjacent, <= 3 runs per pair, connected disk faces, edge runs
>= K, genus free) on the frozen Stage A list, one shard of SHARDS; C0/C1/C2 controls first on every start.

  K = 39 at nine planes, 30 at eight (cubic: E = 3 (n - 2) + 6 g, all pairs force g >= 3 resp. 2).
  C0: each eight-plane source, K = 30, must give an exactly verified all-pairs solid.
  C1: plane 0 of each source deleted; its generic cell in the seven-plane extension arrangement gets a representative
      from cells.representative (the units' path; it must be an LP point, not the deleted plane), K = 30, must
      give an exactly verified all-pairs solid.
  C2: tetrahedron, K = 7, must be INFEASIBLE.
A SOLID is a CANDIDATE only (verify_candidate.py --all-pairs, candidate-check). INFEASIBLE is UNSAT-SOLVER for this
exact model; UNKNOWN / HARD-TIMEOUT leave the unit open. The shard budget (core-s; total / SHARDS) covers controls,
pilot and units of every start; a unit starts only if spent + cap + OVERHEAD <= budget. The shard's first two units
are its pilot; before its first later unit the pilot gate requires both pilot records, no ERROR, and spent + mean
pilot wall (all shards' records) x remaining units <= budget, else the shard stops (exit 6) for an owner decision.
Usage: stage_a.py --out DIR --shard S --shards N [--cap 60] [--budget B] [--pilot]   (run.sh drives it)"""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cells  # noqa: E402
base = cells.base
from ladder_exact import verify  # noqa: E402  (code/ is on the path through pilot.py)
from solid_cpsat import best_solid  # noqa: E402
from solid_fast import Tables  # noqa: E402

UNITS = HERE / 'list' / 'units.json'
UNITS_SHA256 = 'ef132bc74c243121842406543ca7a9b36d55ef1af4f6974c66e50b5b1f67b360'
TOTAL_CORE_SECONDS = 12 * 3600                   # owner's budget decision, 2026-11-12 (amendment 2)
OVERHEAD = 30                                        # process start + arrangement + tables, seconds
PILOT_UNITS, PILOT_CORE_SECONDS = 2, 0.5 * 3600
TETRA = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]]


def can_start(spent, cap, budget):
    return spent + cap + OVERHEAD <= budget


def projection_ok(spent, mean_unit, remaining, budget):
    """Pilot gate: the shard's spent time plus the measured mean pilot cost of its remaining units fits."""
    return spent + mean_unit * remaining <= budget


def worker(inp_path, out_path):
    u = json.loads(inp_path.read_text()); h = base.integer_planes(u['planes'])
    t0 = time.process_time(); a = base.arrangement(h); tables = Tables(a); t1 = time.process_time()
    mp = out_path.with_suffix('.model.pbtxt')
    sel, info = best_solid(a, tables, time_limit=u['cap'], target_edges=u['edges_min'], edges_at_least=True,
                           max_runs=3, model_path=mp)
    res = dict(solver=info, bounded_cells=len(tables.cells), model_sha256=base.sha(mp),
               t_tables=round(t1 - t0, 3), t_solve=round(time.process_time() - t1, 3))
    if sel is not None:
        assert info['valid'], 'hard disk model disagrees with boundary diagnostics'
        solid = {tables.cells[i] for i, v in enumerate(sel) if v}
        links = base.extract_links(a, solid); g = verify(h, links, require_all_pairs=True)
        e, n = info['edge_runs'], len(h)
        if not (g['EMBEDDED'] and g['all_pairs_adjacent'] and e >= u['edges_min'] and e % 3 == 0
                and tuple(g['V_E_F_chi']) == (2 * e // 3, e, n, n - e // 3)):
            raise ArithmeticError('hard model disagrees with exact geometry/topology')
        res.update(planes=h, links=links, geometry=g)
        base.dump(out_path.with_suffix('.candidate.json'), base.candidate_record(res))
    base.dump(out_path, res)


def verdict(r):
    if r.get('geometry', {}).get('EMBEDDED'):
        return 'SOLID'
    return r.get('solver', {}).get('status', r.get('status'))


def run_unit(raw, name, u):
    """One unit in a child process with a hard wall limit; raw files are kept only for SOLID / ERROR units."""
    raw.mkdir(parents=True, exist_ok=True)
    ip, op, log = raw / (name + '.input.json'), raw / (name + '.output.json'), raw / (name + '.log')
    base.dump(ip, u)
    c0 = resource.getrusage(resource.RUSAGE_CHILDREN); t0 = time.monotonic(); limit = u['cap'] + OVERHEAD
    rc = base.command([sys.executable, str(Path(__file__).resolve()), '--input', str(ip), '--output', str(op)], log, limit)
    c1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    r = json.loads(op.read_text()) if rc == 0 else dict(status='HARD-TIMEOUT' if rc is None else 'ERROR')
    if rc not in (0, None):
        r['error_tail'] = log.read_text()[-600:]
    r.update(wall_seconds=round(time.monotonic() - t0, 3), returncode=rc, hard_limit_seconds=limit,
             cpu_seconds=round(c1.ru_utime + c1.ru_stime - c0.ru_utime - c0.ru_stime, 3))
    r['verdict'] = verdict(r); r['budget_fraction'] = round(r['wall_seconds'] / u['cap'], 3)
    if r['verdict'] not in ('SOLID', 'ERROR'):
        for f in raw.glob(name + '.*'):
            f.unlink()
    return r


def c1_unit(name):
    h = cells.source_planes(name); h7 = h[1:]; D7 = cells.duals(h7)
    key = cells.key_of(D7, h[0])
    p, method, margin = cells.representative(D7, key, h[0])
    return dict(planes=h7 + [[str(v) for v in p]], edges_min=30, deleted=h[0], key=cells.key_str(key),
                method=method, margin=margin, differs=cells.canon(p) != cells.canon(h[0]))


def controls():
    c = {}
    for name in cells.SOURCES:
        c['C0_' + name] = dict(planes=cells.source_planes(name), edges_min=30)
        c['C1_' + name] = c1_unit(name)
    c['C2_tetra'] = dict(planes=TETRA, edges_min=7)
    return c


def passed(name, u, r):
    if name.startswith('C2'):
        return r['verdict'] == 'INFEASIBLE'
    ok = r['verdict'] == 'SOLID' and r['geometry']['all_pairs_adjacent'] and r['geometry']['V_E_F_chi'][2] == 8
    return ok and (name.startswith('C0') or (u['method'] == 'lp' and u['differs']))


def records(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def append(path, rec):
    with path.open('a') as s:
        s.write(json.dumps(rec) + '\n')


def load_units():
    if base.sha(UNITS) != UNITS_SHA256:
        raise RuntimeError('units.json differs from the frozen list')
    return json.loads(UNITS.read_text())


def run_shard(a):
    out = a.out; out.mkdir(parents=True, exist_ok=True); raw = out / 'raw'
    flag = out.parent / 'CANDIDATE'
    units = load_units()
    budget = a.budget if a.budget is not None else (PILOT_CORE_SECONDS if a.pilot else TOTAL_CORE_SECONDS) / a.shards
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], text=True),
                    started_utc=stamp, shard=a.shard, shards=a.shards, cap=a.cap, budget_core_seconds=budget,
                    pilot=a.pilot, units_sha256=UNITS_SHA256, python=sys.version,
                    executable=sys.executable.replace(str(Path.home()), '~', 1),   # no home directory in records
                    cpu_count=os.cpu_count())
    base.dump(out / f'manifest-{stamp}.json', manifest)
    base.command([sys.executable, '-m', 'pip', 'freeze'], out / f'pip-freeze-{stamp}.txt', 60)
    spent = sum(r['wall_seconds'] for f in ('controls.jsonl', 'results.jsonl') for r in records(out / f))
    for name, u in controls().items():
        u = dict(u, cap=a.cap); r = run_unit(raw, name, u); spent += r['wall_seconds']
        ok = passed(name, u, r)
        append(out / 'controls.jsonl', dict(unit=name, started=stamp, passed=ok, **{k: v for k, v in u.items() if k != 'cap'},
                                            **{k: r.get(k) for k in ('verdict', 'wall_seconds', 'cpu_seconds', 'model_sha256',
                                                                     'links', 'solver', 'error_tail')},
                                            V_E_F_chi=r.get('geometry', {}).get('V_E_F_chi')))
        if ok:                                       # the record holds the recovered map; raw files only on failure
            for f in raw.glob(name + '.*'):
                f.unlink()
        print(name, r['verdict'], ok, round(r['wall_seconds'], 1), flush=True)
        if not ok:
            print('CONTROL-FAILED', name, flush=True); return 3
    done = {r['unit'] for d in out.parent.glob('[0-9]*') for r in records(d / 'results.jsonl')}
    mine = [u for u in units if u['ordinal'] % a.shards == a.shard]
    pilot = {u['unit'] for u in mine[:PILOT_UNITS]}
    if a.pilot:
        mine = mine[:PILOT_UNITS]
    todo = [u for u in mine if u['unit'] not in done]
    gate = False
    D = {s: cells.duals(cells.source_planes(s)) for s in cells.SOURCES}
    for u in todo:
        if flag.exists():
            print('CANDIDATE-STOP', flag.read_text().strip(), flush=True); return 5
        if not can_start(spent, a.cap, budget):
            print(f'BUDGET-STOP at {spent:.0f} of {budget:.0f} core-s; {len(todo)} were open at start', flush=True); return 4
        if u['unit'] not in pilot and not gate:           # pilot gate, once per start, before the first day unit
            own = [r for r in records(out / 'results.jsonl') if r['unit'] in pilot]
            walls = [r['wall_seconds'] for d in out.parent.glob('[0-9]*') for r in records(d / 'results.jsonl')
                     if r.get('phase') == 'pilot']
            left = sum(v['unit'] not in pilot for v in todo[todo.index(u):])
            mean = sum(walls) / len(walls) if walls else float('inf')
            if len(own) < len(pilot) or any(r['verdict'] == 'ERROR' for r in own) or \
                    not projection_ok(spent, mean, left, budget):
                print(f'PILOT-GATE-STOP: spent {spent:.0f} + {left} x {mean:.1f} s vs {budget:.0f} core-s; '
                      f'pilot records {len(own)}/{len(pilot)}', flush=True); return 6
            print(f'PILOT-GATE-PASS: spent {spent:.0f} + {left} x {mean:.1f} s <= {budget:.0f} core-s', flush=True)
            gate = True
        p = [cells.Fr(v) for v in u['ninth']]
        if cells.key_str(cells.key_of(D[u['source']], p)) != u['key']:
            raise ArithmeticError(u['unit'] + ': representative is not in its cell')
        r = run_unit(raw, u['unit'], dict(planes=cells.source_planes(u['source']) + [u['ninth']], edges_min=39, cap=a.cap))
        spent += r['wall_seconds']
        rec = dict(unit=u['unit'], ordinal=u['ordinal'], source=u['source'], orbit_size=u['orbit_size'],
                   phase='pilot' if u['unit'] in pilot else 'day', started=stamp,
                   **{k: r.get(k) for k in ('verdict', 'wall_seconds', 'cpu_seconds', 'budget_fraction', 't_tables', 't_solve',
                                            'bounded_cells', 'model_sha256', 'returncode', 'error_tail')},
                   ended_by=r.get('solver', {}).get('ended_by'), solver_seconds=r.get('solver', {}).get('seconds'))
        if r['verdict'] == 'SOLID':
            rec.update(planes=r['planes'], links=r['links'], geometry=r['geometry'], edge_runs=r['solver']['edge_runs'])
        append(out / 'results.jsonl', rec)
        print(u['unit'], r['verdict'], round(r['wall_seconds'], 1), flush=True)
        if r['verdict'] == 'SOLID':
            flag.write_text(f"{u['unit']} shard {a.shard} {stamp}\n")
            print('CANDIDATE', u['unit'], 'run verify_candidate.py --all-pairs, then candidate-check', flush=True); return 5
    print(f'SHARD-DONE {len(todo)} units at {spent:.0f} of {budget:.0f} core-s', flush=True)
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path); ap.add_argument('--input', type=Path); ap.add_argument('--output', type=Path)
    ap.add_argument('--shard', type=int, default=0); ap.add_argument('--shards', type=int, default=10)
    ap.add_argument('--cap', type=float, default=60); ap.add_argument('--budget', type=float, default=None)
    ap.add_argument('--pilot', action='store_true')
    a = ap.parse_args()
    if a.input:
        worker(a.input, a.output)
    else:
        sys.exit(run_shard(a))
