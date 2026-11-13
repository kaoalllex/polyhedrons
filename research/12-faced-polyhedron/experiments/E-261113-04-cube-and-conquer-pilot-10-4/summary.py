#!/usr/bin/env python3
"""Per-arm cube totals and the registered readings of PLAN.md (E-261113-04).

Usage: summary.py --selftest | summary.py RESULTS_DIR
Ratio r = summed kissat solver seconds of an arm's cubes / its recorded monolithic seconds (E-261108-03). An arm is
COMPLETE when all 512 cubes are decided; otherwise r is a lower bound. Readings: any SAT cube -> CONTRADICTION (the
monolithic answer was UNSAT-SOLVER; escalate); r >= 0.7 on both arms (lower bounds count) -> PARK; both arms COMPLETE
with r <= 0.5 -> CUBES-WIN; anything else -> BETWEEN. Calibration: map 845 monolithic / 188.38 s outside
[0.75, 1.33] marks the reading UNCALIBRATED (lead decides). A + B price: r_max x 6.06 nights (f = 7.16) and x 4.18
nights (the 96 / 85 ratios), E-261109-06."""
import glob
import json
import sys

CUBES, PARK, WIN, BAND = 512, 0.7, 0.5, (0.75, 1.33)
NIGHTS = (6.06, 4.18)


def arms(rows):
    out = {}
    for i in sorted({r['map_index'] for r in rows if r.get('cube') is not None}, reverse=True):
        rs = [r for r in rows if r['map_index'] == i and r.get('cube') is not None]
        mono = rs[0]['monolithic_seconds']
        st = [r['status'] for r in rs]
        decided = sum(s in ('SAT', 'UNSAT-SOLVER') for s in st)
        secs = sum(r['seconds'] for r in rs)
        out[i] = dict(cubes=len(rs), decided=decided, sat=st.count('SAT'), timeout=st.count('TIMEOUT'),
                      skipped=st.count('SKIPPED-ARM-CAP'), seconds=round(secs, 1), monolithic=round(mono, 1),
                      ratio=round(secs / mono, 3), complete=decided == CUBES,
                      max_cube=round(max(r['seconds'] for r in rs), 1))
    return out


def reading(a, calibration):
    if any(x['sat'] for x in a.values()):
        return 'CONTRADICTION: a SAT cube of a formula kissat called UNSAT; run candidate-check on nothing, escalate'
    if len(a) < 2:
        return 'INCOMPLETE: fewer than two arms recorded'
    r_max = max(x['ratio'] for x in a.values())
    if all(x['ratio'] >= PARK for x in a.values()):
        out = f'PARK: r >= {PARK} on both arms; cube-and-conquer parked at this budget'
    elif all(x['complete'] and x['ratio'] <= WIN for x in a.values()):
        out = (f'CUBES-WIN: r <= {WIN} on both; propose the eight asymmetric (10, 3) maps with cubes to the owner; '
               f'A + B priced at {r_max * NIGHTS[0]:.2f} / {r_max * NIGHTS[1]:.2f} nights')
    else:
        out = 'BETWEEN: record, no change'
    if calibration is None or not BAND[0] <= calibration <= BAND[1]:
        out = f'UNCALIBRATED (845 ratio {calibration}): ' + out
    return out


def load(d):
    rows = [json.loads(l) for f in glob.glob(f'{d}/[0-9]*/results.jsonl') for l in open(f) if l.strip()]
    controls = [json.load(open(f))['status'] for f in glob.glob(f'{d}/[0-9]*/controls.json')]
    cal = [r for r in rows if r.get('cube') is None and r['map_index'] == 845]
    calibration = (round(cal[0]['seconds'] / cal[0]['reference_seconds'], 3)
                   if cal and cal[0]['status'] == 'UNSAT-SOLVER' else None)
    return rows, controls, calibration


def selftest():
    def rows(i, mono, secs, status='UNSAT-SOLVER', n=CUBES):
        return [dict(map_index=i, cube=k, monolithic_seconds=mono, seconds=secs, status=status) for k in range(n)]
    win = arms(rows(96, 1000, 0.5) + rows(85, 2000, 1.0))
    assert win[96]['ratio'] == 0.256 and win[85]['complete']
    assert reading(win, 1.0).startswith('CUBES-WIN') and '1.55' in reading(win, 1.0)
    assert reading(win, 1.5).startswith('UNCALIBRATED') and 'CUBES-WIN' in reading(win, 1.5)
    assert reading(arms(rows(96, 1000, 2.0) + rows(85, 2000, 3.0)), 1.0).startswith('PARK')
    assert reading(arms(rows(96, 1000, 0.5) + rows(85, 2000, 3.0)), 1.0).startswith('BETWEEN')
    cut = arms(rows(96, 1000, 0.5) + rows(85, 2000, 1.0, n=500) + rows(85, 2000, 0, 'SKIPPED-ARM-CAP', 12))
    assert not cut[85]['complete'] and reading(cut, 1.0).startswith('BETWEEN')
    lb = arms(rows(96, 1000, 100, 'TIMEOUT', 8) + rows(85, 2000, 200, 'TIMEOUT', 8))
    assert reading(lb, 1.0).startswith('PARK')
    sat = arms(rows(96, 1000, 0.5) + rows(85, 2000, 1.0, 'SAT', 1))
    assert reading(sat, 1.0).startswith('CONTRADICTION')
    print('selftest OK')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    rows, controls, calibration = load(sys.argv[1])
    a = arms(rows)
    for i, x in a.items():
        print(f'map {i}: {x}')
    print('calibration 845 ratio', calibration, '| controls', controls)
    print(reading(a, calibration) if controls and all(c == 'CONTROLS-PASS' for c in controls)
          else 'CONTROL-FAILURE: stop, escalate')
