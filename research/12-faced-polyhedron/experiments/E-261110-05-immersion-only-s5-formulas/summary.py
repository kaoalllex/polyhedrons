#!/usr/bin/env python3
"""Per-map V2 / V1 table and the registered readings of PLAN.md (E-261110-05).

Usage: summary.py --selftest | summary.py RESULTS_DIR [RESULTS_DIR ...]   (the (8, 2) prep dir and the (9, 3) run dir)
Every map's plain formula is UNSAT-VERIFIED (STATUS 3d); V1, V2 are relaxations, so a SAT is about that formula only.
Readings: any V2 SAT -> SEGMENT-NECESSARY (H-261110-01 supported on that map); V1 UNSAT-SOLVER on an (8, 2) map ->
LOCAL (one session of core mining on the (8, 2) formulas); a map with V1 SAT and V2 UNSAT-SOLVER -> TRIPLES-CARRY
(H-261110-01 weakened on that map). TIMEOUT: no information."""
import glob
import json
import sys


def readings(units):
    """units: {(case, map, variant): status}."""
    maps = sorted({(c, m) for c, m, _ in units})
    out = []
    v2_sat = [cm for cm in maps if units.get(cm + ('V2',)) == 'SAT']
    if v2_sat:
        out.append(f'SEGMENT-NECESSARY on {v2_sat}: H-261110-01 supported, theory paragraph')
    local = [cm for cm in maps if cm[0] == (8, 2) and units.get(cm + ('V1',)) == 'UNSAT-SOLVER']
    if local:
        out.append(f'LOCAL on {local}: one session of core mining on the (8, 2) formulas')
    carry = [cm for cm in maps if units.get(cm + ('V1',)) == 'SAT' and units.get(cm + ('V2',)) == 'UNSAT-SOLVER']
    if carry:
        out.append(f'TRIPLES-CARRY on {carry}: H-261110-01 weakened on these maps')
    return out or ['NO-READING: record (timeouts or V1 UNSAT at (9, 3) only)']


def load(dirs):
    units, controls = {}, []
    for d in dirs:
        for f in glob.glob(f'{d}/[0-9]*/results.jsonl'):
            for line in open(f):
                r = json.loads(line)
                units[(tuple(r['case']), r['map_index'], r['variant'])] = r['status']
        controls += [json.load(open(f))['status'] for f in glob.glob(f'{d}/[0-9]*/controls.json')]
    return units, controls


def selftest():
    k = lambda m, v: ((8, 2), m, v) if m < 2 else ((9, 3), m, v)  # noqa: E731
    assert readings({k(0, 'V2'): 'SAT', k(0, 'V1'): 'SAT'})[0].startswith('SEGMENT-NECESSARY')
    assert readings({k(0, 'V2'): 'UNSAT-SOLVER', k(0, 'V1'): 'UNSAT-SOLVER'})[0].startswith('LOCAL')
    assert readings({k(40, 'V2'): 'UNSAT-SOLVER', k(40, 'V1'): 'UNSAT-SOLVER'})[0].startswith('NO-READING')
    assert readings({k(40, 'V2'): 'UNSAT-SOLVER', k(40, 'V1'): 'SAT'})[0].startswith('TRIPLES-CARRY')
    assert readings({k(40, 'V2'): 'TIMEOUT', k(40, 'V1'): 'SAT'})[0].startswith('NO-READING')
    print('selftest OK')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    units, controls = load(sys.argv[1:])
    for (case, m, v), s in sorted(units.items()):
        print(f'{case} map {m:3} {v}: {s}')
    print('controls', controls)
    print(json.dumps(readings(units), indent=1) if all(c == 'CONTROLS-PASS' for c in controls) and controls
          else 'CONTROL-FAILURE: stop, escalate')
