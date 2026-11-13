#!/usr/bin/env python3
"""Per-map table and the registered verdict of PLAN.md (E-261110-02).

Usage: summary.py --selftest | summary.py [RESULTS_RUN_DIR] [QUEUE_JSON]
Statuses (SPEC §4): SAT, UNSAT-VERIFIED, UNSAT-SOLVER (an unchecked or failed proof check is recorded as
UNSAT-UNCHECKED by the runner and counted here as UNSAT-SOLVER), TIMEOUT (no information). Escalation on timeouts:
more than 20 % of the maps. (11, 4) is proposed only if all 20 are UNSAT-VERIFIED and the median decided solver time
is below 600 s."""
import glob
import json
from pathlib import Path
import statistics
import sys

HERE = Path(__file__).resolve().parent
N_MAPS = 20


def verdict(units, controls_ok):
    """units: [(lutz, status, solver_seconds, sat_note)] for every recorded map unit."""
    st = [('UNSAT-SOLVER' if s == 'UNSAT-UNCHECKED' else s) for _, s, _, _ in units]
    count = {k: st.count(k) for k in ('SAT', 'UNSAT-VERIFIED', 'UNSAT-SOLVER', 'TIMEOUT')}
    decided = [sec for (_, s, sec, _), t in zip(units, st) if t in ('SAT', 'UNSAT-VERIFIED', 'UNSAT-SOLVER')]
    median = statistics.median(decided) if decided else None
    out = dict(units=len(units), median_decided_seconds=median, **count)
    sats = [(lutz, note) for lutz, s, _, note in units if s == 'SAT']
    if not controls_ok:
        out['verdict'] = 'CONTROL-FAILURE: stop, escalate'
    elif any(note == 'CANDIDATE-NEEDS-REVIEW' for _, note in sats):
        out['verdict'] = 'CANDIDATE: candidate-check before any wording; escalate'
    elif sats:
        out['verdict'] = 'SAT-NOT-REALIZED: existence open; final polynomials (I-261029-45), escalate'
    elif count['TIMEOUT'] > 0.2 * N_MAPS:
        out['verdict'] = 'TIMEOUTS>20%: record, escalate'
    elif len(units) < N_MAPS:
        out['verdict'] = 'INCOMPLETE: maps left; restart'
    elif count['UNSAT-VERIFIED'] == N_MAPS:
        out['verdict'] = ('ALL-UNSAT-VERIFIED: conditional exclusion at formula scope; '
                          + ('propose (11, 4)' if median < 600 else 'no (11, 4) proposal'))
    else:
        out['verdict'] = 'NO-SAT: unchecked UNSATs or timeouts left; replay or escalate, no negative claim'
    out['sat_maps'] = sats
    return out


def load(run, queue):
    lutz = {e['index']: e.get('lutz') for e in json.loads(Path(queue).read_text())['maps']}
    units, controls_ok = [], True
    for f in sorted(glob.glob(f'{run}/[0-9]*/results.jsonl')):
        for line in open(f):
            d = json.loads(line)
            if isinstance(d['map_index'], int):
                units.append((lutz[d['map_index']], d['status'], d['seconds'], d.get('status_note'), d))
            elif d['status'] != ('SAT' if '-neg-' not in d['map_index'] else 'UNSAT-VERIFIED'):
                controls_ok = False
    controls_ok &= not Path(run, 'stop.json').exists()
    return sorted(units, key=lambda u: u[0]), controls_ok


def table(units):
    for lutz, status, seconds, note, d in units:
        rss = max(d.get('solver_children_maxrss', 0), d.get('checker_children_maxrss', 0)) / 2 ** 30
        print(f"#{lutz:2} {status:15} solver {seconds:7.1f}s ended_by {d.get('ended_by')} checker "
              f"{d.get('checker_seconds', 0):7.1f}s {d.get('checker_ended_by', '-')} peak {rss:5.2f} GiB {note or ''}")


def selftest():
    base = [(i + 1, 'UNSAT-VERIFIED', 300.0, None) for i in range(20)]
    assert verdict(base, True)['verdict'].endswith('propose (11, 4)')
    assert verdict([(l, s, 599.0, n) for l, s, _, n in base], True)['verdict'].endswith('propose (11, 4)')
    assert verdict([(l, s, 601.0, n) for l, s, _, n in base], True)['verdict'].endswith('no (11, 4) proposal')
    t5 = [(l, 'TIMEOUT' if l <= 5 else s, 3600.0 if l <= 5 else sec, n) for l, s, sec, n in base]
    t4 = [(l, 'TIMEOUT' if l <= 4 else s, 3600.0 if l <= 4 else sec, n) for l, s, sec, n in base]
    assert verdict(t5, True)['verdict'].startswith('TIMEOUTS>20%')
    assert verdict(t4, True)['verdict'].startswith('NO-SAT')
    assert verdict(base[:19], True)['verdict'].startswith('INCOMPLETE')
    assert verdict(base, False)['verdict'].startswith('CONTROL-FAILURE')
    assert verdict(base[:19] + [(20, 'SAT', 9.0, 'SAT-NOT-REALIZED')], True)['verdict'].startswith('SAT-NOT-REALIZED')
    assert verdict(base[:19] + [(20, 'SAT', 9.0, 'CANDIDATE-NEEDS-REVIEW')], True)['verdict'].startswith('CANDIDATE')
    unchecked = base[:19] + [(20, 'UNSAT-UNCHECKED', 300.0, None)]
    v = verdict(unchecked, True)
    assert v['UNSAT-SOLVER'] == 1 and v['verdict'].startswith('NO-SAT'), v
    print('selftest OK: 5/20 timeouts escalate, 4/20 do not; median 599 s proposes (11, 4), 601 s does not; '
          'an unchecked proof is UNSAT-SOLVER, never part of a negative claim')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    run = sys.argv[1] if len(sys.argv) > 1 else str(HERE / 'results/run')
    units, ok = load(run, sys.argv[2] if len(sys.argv) > 2 else HERE / 'queue.json')
    table(units)
    print(json.dumps(verdict([u[:4] for u in units], ok), indent=1))
