#!/usr/bin/env python3
"""Time-to-SAT distribution, bridge realization rate and the registered readings of PLAN.md (E-261113-02).

Usage: summary.py --selftest | summary.py [RESULTS_RUN_DIR] [QUEUE_JSON]
A unit is one (map, kissat seed). Statuses (SPEC §4): SAT, UNSAT-SOLVER (no proofs), TIMEOUT (no information).
Readings (PLAN.md): LIGHT = median SAT time < 60 s and no TIMEOUT; HEAVY-TAIL = a map SAT on one seed and TIMEOUT on
another, or a seed spread (max >= 60 s and max >= 10 x min) on >= 10 % of the maps SAT on all three seeds (checked
before LIGHT); bridge rate < 50 % of SAT
models realized; the drawn maps under 0.3 core-h of solver + bridge time -> the full 865."""
import glob
import json
from pathlib import Path
from statistics import median
import sys

HERE = Path(__file__).resolve().parent
N_UNITS = 153


def reading(units, controls_ok):
    """units: [(lutz, seed, role, status, solver_seconds, bridge_seconds, note)] for every recorded unit."""
    drawn = [u for u in units if u[2] == 'drawn']
    sat = [u for u in drawn if u[3] == 'SAT']
    by_map = {}
    for u in drawn:
        by_map.setdefault(u[0], []).append(u)
    mixed = sorted(m for m, us in by_map.items() if {'SAT', 'TIMEOUT'} <= {u[3] for u in us})
    all_sat = [us for us in by_map.values() if len(us) == 3 and all(u[3] == 'SAT' for u in us)]
    spread = [us for us in all_sat if max(u[4] for u in us) >= max(60, 10 * min(u[4] for u in us))]
    realized = [u for u in units if u[3] == 'SAT' and u[6] == 'CANDIDATE-NEEDS-REVIEW']
    sat_all = [u for u in units if u[3] == 'SAT']
    core_h = sum(u[4] + u[5] for u in drawn) / 3600
    out = dict(units=len(units), drawn_units=len(drawn), maps=len(by_map),
               status={k: sum(u[3] == k for u in drawn) for k in ('SAT', 'UNSAT-SOLVER', 'TIMEOUT')},
               sat_maps=sum(any(u[3] == 'SAT' for u in us) for us in by_map.values()),
               median_sat_seconds=median(u[4] for u in sat) if sat else None,
               max_sat_seconds=max((u[4] for u in sat), default=None),
               mixed_maps=mixed, spread_maps=len(spread), all_sat_maps=len(all_sat),
               bridge=f'{len(realized)}/{len(sat_all)}', target_fail=sum(u[6] == 'EMBEDDED-BUT-TARGET-FAIL' for u in units),
               drawn_core_hours=round(core_h, 3))
    witness = [u for u in units if u[2] == 'witness control']
    readings = []
    if not controls_ok or (witness and not any(u[3] == 'SAT' for u in witness)):
        readings.append('CONTROL-FAILURE: stop, escalate')
    elif len(units) < N_UNITS:
        readings.append('INCOMPLETE: units left; restart')
    else:
        if mixed or (all_sat and len(spread) >= 0.1 * len(all_sat)):
            readings.append('HEAVY-TAIL: propose a seed-portfolio day run on (10,3) to the owner')
        elif sat and out['median_sat_seconds'] < 60 and out['status']['TIMEOUT'] == 0:
            readings.append('LIGHT: (10,3) timeouts read "probably UNSAT" for planning (never a claim); route = item 4')
        else:
            readings.append('NEITHER: record, no route change')
        if sat_all and len(realized) < 0.5 * len(sat_all):
            readings.append('BRIDGE<50%: E-261113-01 follow-up takes more models per SAT')
        if core_h < 0.3:
            readings.append('CHEAP: the full 865 in the same budget (follow-up branch)')
        if out['target_fail']:
            readings.append('EMBEDDED-BUT-TARGET-FAIL present: check before any wording')
    out['readings'] = readings
    return out


def load(run, queue):
    entries = {e['index']: e for e in json.loads(Path(queue).read_text())['maps']}
    recs = json.loads((HERE.parents[1] / json.loads(Path(queue).read_text())['maps_file']).read_text())['maps']
    units, controls_ok = [], True
    for f in sorted(glob.glob(f'{run}/[0-9]*/results.jsonl')):
        for line in open(f):
            d = json.loads(line)
            if isinstance(d['map_index'], int):
                rec = recs[d['map_index']]
                bridge = sum(p.get('seconds', 0) for p in d.get('processing', {}).values())
                units.append((rec['lutz'], rec['seed'], rec['role'], d['status'], d['seconds'], bridge, d.get('status_note')))
            elif d['status'] != ('SAT' if '-neg-' not in d['map_index'] else 'UNSAT-SOLVER'):
                controls_ok = False
    assert all(isinstance(k, str) or k < len(recs) for k in entries)
    controls_ok &= not Path(run, 'stop.json').exists()
    return sorted(units), controls_ok


def selftest():
    def maps(times, note='CANDIDATE-NEEDS-REVIEW'):
        u = [(m, s, 'drawn', 'SAT' if t is not None else 'TIMEOUT', t if t is not None else 300.0, 5.0 if t else 0.0,
              note if t is not None else None) for m, ts in enumerate(times) for s, t in enumerate(ts)]
        return u + [(739, s, 'witness control', 'SAT', 1.0, 5.0, note) for s in range(3)]
    light = maps([[59.0, 59.0, 59.0]] * 50)
    assert reading(light, True)['readings'][0].startswith('LIGHT') and len(light) == N_UNITS
    slow = maps([[61.0, 61.0, 61.0]] * 50)
    assert reading(slow, True)['readings'][0].startswith('NEITHER')
    mixed = maps([[1.0, None, 1.0]] + [[1.0] * 3] * 49)
    assert reading(mixed, True)['readings'][0].startswith('HEAVY-TAIL')
    spread5 = maps([[6.0, 6.0, 60.0]] * 5 + [[1.0] * 3] * 45)
    spread4 = maps([[6.0, 6.0, 60.0]] * 4 + [[1.0] * 3] * 46)
    assert reading(maps([[1.0, 1.0, 59.0]] * 50), True)['readings'][0].startswith('LIGHT')
    assert reading(spread5, True)['readings'][0].startswith('HEAVY-TAIL')
    assert reading(spread4, True)['readings'][0].startswith('LIGHT')
    half = [u if u[0] % 2 else u[:6] + ('SAT-NOT-REALIZED',) for u in maps([[1.0] * 3] * 50)]
    assert not any(r.startswith('BRIDGE') for r in reading(half, True)['readings'])
    low = [u if u[0] % 2 and u[0] > 1 else u[:6] + ('SAT-NOT-REALIZED',) for u in maps([[1.0] * 3] * 50)]
    assert any(r.startswith('BRIDGE') for r in reading(low, True)['readings'])
    cheap = maps([[1.0] * 3] * 50)  # 150 x 6 s = 0.25 core-h
    dear = maps([[3.0] * 3] * 50)   # 150 x 8 s = 0.33 core-h
    assert any(r.startswith('CHEAP') for r in reading(cheap, True)['readings'])
    assert not any(r.startswith('CHEAP') for r in reading(dear, True)['readings'])
    assert reading(light, False)['readings'][0].startswith('CONTROL-FAILURE')
    assert reading(light[:-1], True)['readings'][0].startswith('INCOMPLETE')
    print('selftest OK: median 59/61 s, mixed map, spread 5/4 of 50 (max 60 s; 59 s is no spread), bridge 50 %/48 %, 0.25/0.33 core-h on each side')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    run = sys.argv[1] if len(sys.argv) > 1 else str(HERE / 'results/run')
    units, ok = load(run, sys.argv[2] if len(sys.argv) > 2 else HERE / 'queue.json')
    for u in units:
        print(f'#{u[0]:<4} seed {u[1]} {u[2]:15} {u[3]:13} solver {u[4]:7.1f}s bridge {u[5]:6.1f}s {u[6] or ""}')
    print(json.dumps(reading(units, ok), indent=1))
