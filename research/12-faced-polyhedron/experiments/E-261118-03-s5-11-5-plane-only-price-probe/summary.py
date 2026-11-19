#!/usr/bin/env python3
"""Price gate and readings of PLAN.md (E-261118-03).

Usage: summary.py --selftest | summary.py [RESULTS_RUN_DIR] [QUEUE_JSON]
A unit is one (map, kissat seed) of the plane-only C2 formula. Statuses (SPEC §4): SAT, UNSAT-SOLVER (no proofs),
TIMEOUT (no information; counted as +inf in the median, so the 1800 s cap cannot pass the 360 s gate).
Readings: CONTROL-FAILURE (a shard control or the N2 chain failed) first; INCOMPLETE; NIGHT = both maps with a median
over their four seeds <= 360 s; CLOSED otherwise. CANDIDATE = a SAT model realized with `--target S5` PASS."""
import glob
import json
import math
from pathlib import Path
from statistics import median
import sys

HERE = Path(__file__).resolve().parent
N_UNITS, GATE_SECONDS = 8, 360


def map_median(units):
    return median(u[3] if u[2] in ('SAT', 'UNSAT-SOLVER') else math.inf for u in units)


def reading(units, controls_ok):
    """units: [(census_index, seed, status, solver_seconds, note)] for every recorded unit."""
    by_map = {}
    for u in units:
        by_map.setdefault(u[0], []).append(u)
    medians = {m: map_median(us) for m, us in sorted(by_map.items())}
    out = dict(units=len(units), status={k: sum(u[2] == k for u in units) for k in ('SAT', 'UNSAT-SOLVER', 'TIMEOUT')},
               medians={m: (None if math.isinf(v) else round(v, 1)) for m, v in medians.items()},
               solver_core_hours=round(sum(u[3] for u in units) / 3600, 3))
    if not controls_ok:
        readings = ['CONTROL-FAILURE: repair, no reading']
    elif len(units) < N_UNITS:
        readings = ['INCOMPLETE: units left; restart']
    elif len(medians) == 2 and all(v <= GATE_SECONDS for v in medians.values()):
        readings = ['NIGHT: the 20 Aut+ = 2 maps in one owner night (<= 80 core-h), new queue by amendment']
    else:
        readings = ['CLOSED: (11, 5) closes for the laptop; no further (11, 5) item']
    if any(u[4] == 'CANDIDATE-NEEDS-REVIEW' for u in units):
        readings.append('CANDIDATE: candidate-check, escalate')
    if any(u[4] == 'EMBEDDED-BUT-TARGET-FAIL' for u in units):
        readings.append('EMBEDDED-BUT-TARGET-FAIL present: check before any wording')
    out['readings'] = readings
    return out


def load(run, queue):
    q = json.loads(Path(queue).read_text())
    recs = json.loads((HERE.parents[1] / q['maps_file']).read_text())['maps']
    units, controls_ok = [], True
    for f in sorted(glob.glob(f'{run}/[0-9]*/results.jsonl')):
        for line in open(f):
            d = json.loads(line)
            if isinstance(d['map_index'], int):
                rec = recs[d['map_index']]
                units.append((rec['census_index'], rec['seed'], d['status'], d['seconds'], d.get('status_note')))
            elif d['status'] != ('SAT' if '-neg-' not in d['map_index'] else 'UNSAT-SOLVER'):
                controls_ok = False
    controls_ok &= not Path(run, 'stop.json').exists()
    return sorted(units), controls_ok


def selftest():
    def units(a, b):
        return [(m, s, st, t, None) for m, ts in ((1, a), (2, b)) for s, (st, t) in enumerate(ts)]
    fast, slow, out = ('UNSAT-SOLVER', 359.0), ('UNSAT-SOLVER', 361.0), ('TIMEOUT', 1800.0)
    assert reading(units([fast] * 4, [fast] * 4), True)['readings'][0].startswith('NIGHT')
    assert reading(units([fast] * 4, [slow] * 4), True)['readings'][0].startswith('CLOSED')
    assert reading(units([fast] * 3 + [out], [('SAT', 10.0)] * 3 + [out]), True)['readings'][0].startswith('NIGHT')
    assert reading(units([fast] * 2 + [out] * 2, [fast] * 4), True)['readings'][0].startswith('CLOSED')
    assert reading(units([out] * 4, [out] * 4), True)['readings'][0].startswith('CLOSED')
    assert reading(units([fast] * 4, [fast] * 4), False)['readings'][0].startswith('CONTROL-FAILURE')
    assert reading(units([fast] * 4, [fast] * 3), True)['readings'][0].startswith('INCOMPLETE')
    sat = [(1, 0, 'SAT', 5.0, 'CANDIDATE-NEEDS-REVIEW')] + units([fast] * 4, [fast] * 4)[1:]
    assert 'CANDIDATE' in reading(sat, True)['readings'][1]
    print('selftest OK: medians 359/361 s on each side of the gate; one TIMEOUT of four passes, two fail; '
          'all TIMEOUT closes; control failure and incomplete first')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    run = sys.argv[1] if len(sys.argv) > 1 else str(HERE / 'results/run')
    us, ok = load(run, sys.argv[2] if len(sys.argv) > 2 else HERE / 'queue.json')
    for u in us:
        print(f'map {u[0]:<5} seed {u[1]} {u[2]:13} solver {u[3]:7.1f}s {u[4] or ""}')
    print(json.dumps(reading(us, ok), indent=1))
