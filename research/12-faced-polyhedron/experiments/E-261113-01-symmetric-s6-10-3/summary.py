#!/usr/bin/env python3
"""Per-formula table and the registered verdict of PLAN.md part (b) (E-261113-01).

Usage: summary.py --selftest | summary.py [RESULTS_RUN_DIR] [QUEUE_JSON]
Statuses (SPEC §4): SAT, UNSAT-SOLVER (no proofs, owner 2026-11-13; never a negative claim), TIMEOUT (no information).
Escalation on timeouts: more than 20 % of the ten formulas."""
import glob
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
N_FORMULAS = 10


def verdict(units, controls_ok):
    """units: [(label, status, solver_seconds, sat_note)] for every recorded formula unit."""
    st = [s for _, s, _, _ in units]
    count = {k: st.count(k) for k in ('SAT', 'UNSAT-SOLVER', 'TIMEOUT')}
    out = dict(units=len(units), **count)
    sats = [(label, note) for label, s, _, note in units if s == 'SAT']
    if not controls_ok:
        out['verdict'] = 'CONTROL-FAILURE: stop, escalate'
    elif any(note == 'CANDIDATE-NEEDS-REVIEW' for _, note in sats):
        out['verdict'] = 'CANDIDATE: candidate-check before any wording; escalate'
    elif sats:
        out['verdict'] = 'SAT-NOT-REALIZED: at least 6 models by seed through the bridge, then escalate'
    elif count['TIMEOUT'] > 0.2 * N_FORMULAS:
        out['verdict'] = 'TIMEOUTS>20%: record, escalate'
    elif len(units) < N_FORMULAS:
        out['verdict'] = 'INCOMPLETE: formulas left; restart'
    elif count['UNSAT-SOLVER'] == N_FORMULAS:
        out['verdict'] = 'ALL-UNSAT-SOLVER: scoped search outcome, ranks the maps; no exclusion, no negative claim'
    else:
        out['verdict'] = 'NO-SAT: UNSAT-SOLVER and timeouts; no negative claim'
    out['sat_formulas'] = sats
    return out


def load(run, queue):
    label = {e['index']: f"#{e['lutz']} {e['sym_group']}/{e['sym_class']}" for e in json.loads(Path(queue).read_text())['maps']
             if isinstance(e['index'], int)}
    units, controls_ok = [], True
    for f in sorted(glob.glob(f'{run}/[0-9]*/results.jsonl')):
        for line in open(f):
            d = json.loads(line)
            if isinstance(d['map_index'], int):
                units.append((label[d['map_index']], d['status'], d['seconds'], d.get('status_note'), d))
            elif d['status'] != ('SAT' if '-neg-' not in d['map_index'] else 'UNSAT-SOLVER'):
                controls_ok = False
    controls_ok &= not Path(run, 'stop.json').exists()
    return sorted(units, key=lambda u: u[0]), controls_ok


def selftest():
    base = [(f'f{i}', 'UNSAT-SOLVER', 300.0, None) for i in range(10)]
    assert verdict(base, True)['verdict'].startswith('ALL-UNSAT-SOLVER')
    t3 = [(l, 'TIMEOUT' if i < 3 else s, sec, n) for i, (l, s, sec, n) in enumerate(base)]
    t2 = [(l, 'TIMEOUT' if i < 2 else s, sec, n) for i, (l, s, sec, n) in enumerate(base)]
    assert verdict(t3, True)['verdict'].startswith('TIMEOUTS>20%')
    assert verdict(t2, True)['verdict'].startswith('NO-SAT')
    assert verdict(base[:9], True)['verdict'].startswith('INCOMPLETE')
    assert verdict(base, False)['verdict'].startswith('CONTROL-FAILURE')
    assert verdict(base[:9] + [('f9', 'SAT', 9.0, 'SAT-NOT-REALIZED')], True)['verdict'].startswith('SAT-NOT-REALIZED')
    assert verdict(base[:9] + [('f9', 'SAT', 9.0, 'CANDIDATE-NEEDS-REVIEW')], True)['verdict'].startswith('CANDIDATE')
    print('selftest OK: 3/10 timeouts escalate, 2/10 do not; UNSAT-SOLVER answers are never a negative claim')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    run = sys.argv[1] if len(sys.argv) > 1 else str(HERE / 'results/run')
    units, ok = load(run, sys.argv[2] if len(sys.argv) > 2 else HERE / 'queue.json')
    for lab, status, seconds, note, d in units:
        print(f"{lab:12} {status:13} solver {seconds:7.1f}s ended_by {d.get('ended_by')} {note or ''}")
    print(json.dumps(verdict([u[:4] for u in units], ok), indent=1))
