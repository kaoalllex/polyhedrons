#!/usr/bin/env python3
"""Per-pattern table and the registered verdict of PLAN.md (E-261109-06).

Usage: summary.py --selftest | summary.py [RESULTS_RUN_DIR]
A unit is decided if its status is SAT or UNSAT-SOLVER; TIMEOUT at the 3600 s cap is censored. Maps 146 and 845 enter
with their E-261108-03 kissat records. Factor f = (sum of measured kissat seconds, censored at 3600) / (sum of the (9,3)
default-CaDiCaL pattern means over the same maps), review 2026-11-09 §3.2; strata A and B are priced as N x mean x f."""
import glob, json, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAU = 3600.0
MEAN93 = {'(1, 2, 3) (2, 3)': 37, '(1, 1, 1, 3) (2, 2, 2)': 80, '(1, 1, 2, 2) (2, 3)': 96, '(1, 1, 2, 2) (2, 2, 2)': 103,
          '(2, 2, 2) (2, 2, 2)': 30}  # '(3, 3) (4,)' has no (9,3) analogue and stays out of f
STRATA = {'A': (520, 242), 'B': (237, 498)}
REUSED = {845: ('(1, 2, 3) (2, 3)', 'UNSAT-SOLVER', 188.4), 146: ('(2, 2, 2) (2, 2, 2)', 'UNSAT-SOLVER', 692.6)}
SCENARIO, NIGHT, N_MAPS = 51.0, 80.0, 360


def verdict(units, spent_h, cap_reached, controls_ok):
    """units: [(pattern, status, seconds)] for every recorded map unit, the two reused ones included; cap_reached: some
    shard ended DEADLINE-STOP (its 28800 s share no longer fits a 3600 s unit)."""
    sat = [u for u in units if u[1] == 'SAT']
    decided = [u for u in units if u[1] in ('SAT', 'UNSAT-SOLVER')]
    censored = [u for u in units if u[1] == 'TIMEOUT']
    num = sum(min(s, TAU) for p, st, s in units if p in MEAN93)
    den = sum(MEAN93[p] for p, st, s in units if p in MEAN93)
    f = num / den if den else float('inf')
    price = {h: n * m * f / 3600 for h, (n, m) in STRATA.items()}
    out = dict(sat=len(sat), decided=len(decided), censored=len(censored), units=len(units), spent_h=spent_h, f=f,
               price_A=price['A'], price_B=price['B'], nights_AB=(price['A'] + price['B']) / NIGHT)
    if not controls_ok:
        out['verdict'] = 'CONTROL-FAILURE: escalate'
    elif sat:
        out['verdict'] = 'FIRST-SAT: exact model check, realization stage'
    elif len(decided) < 300 and cap_reached:
        out['verdict'] = 'COST-MODEL-WRONG: cap reached with < 300 decided; escalate'
    elif len(censored) > 0.1 * len(units):
        out['verdict'] = 'CENSORED>10%: no A/B proposal; escalate (LOW-YIELD at 3600 s for those patterns)'
    elif len(decided) < N_MAPS:
        out['verdict'] = 'INCOMPLETE: units left; restart or escalate'
    elif out['nights_AB'] <= 4:
        out['verdict'] = 'ALL-DECIDED-0-SAT: propose stratum A nights'
    else:
        out['verdict'] = 'ALL-DECIDED-0-SAT: A/B > 4 nights; Actions after item 2 if allowed'
    out['over_1_5x_scenario'] = spent_h > 1.5 * SCENARIO
    return out


def load(run):
    queue = {e['index']: e.get('pattern') for e in json.loads((HERE / 'queue.json').read_text())['maps']}
    units, controls_ok, cap = [], True, False
    for f in sorted(glob.glob(f'{run}/[0-9]*/results.jsonl')):
        for line in open(f):
            d = json.loads(line)
            if isinstance(d['map_index'], int):
                units.append((queue[d['map_index']], d['status'], d['seconds']))
            elif d['status'] != ('SAT' if '-neg-' not in d['map_index'] else 'UNSAT-SOLVER'):
                controls_ok = False
    controls_ok &= not Path(run, 'stop.json').exists()
    cap = any(json.loads(Path(m).read_text())['status'] == 'DEADLINE-STOP' for m in glob.glob(f'{run}/[0-9]*/attempt_*/manifest.json'))
    units += list(REUSED.values())
    budget = Path(run, 'budget.json')
    spent = sum(json.loads(budget.read_text()).values()) / 3600 if budget.exists() else 0.0
    return units, spent, cap, controls_ok


def table(units):
    for p in list(MEAN93) + ['(3, 3) (4,)']:
        u = [x for x in units if x[0] == p]
        d = [s for _, st, s in u if st in ('SAT', 'UNSAT-SOLVER')]
        c = sum(1 for _, st, _ in u if st == 'TIMEOUT')
        print(f'{p:24} n={len(u):3} decided={len(d):3} censored={c:2} median={statistics.median(d) if d else 0:7.1f}s '
              f'max={max(d) if d else 0:7.1f}s sum={sum(min(s, TAU) for _, _, s in u) / 3600:6.2f} core-h')


def selftest():
    ps = list(MEAN93)
    base = [(ps[i % 5], 'UNSAT-SOLVER', MEAN93[ps[i % 5]] * 5.5) for i in range(359)] + [('(3, 3) (4,)', 'UNSAT-SOLVER', 60)]
    v = verdict(base, 50.0, False, True)
    assert abs(v['f'] - 5.5) < 1e-9 and v['nights_AB'] > 4 and v['verdict'].startswith('ALL-DECIDED') and 'Actions' in v['verdict'], v
    fast = [(p, st, s / 5.5 * 4.0) for p, st, s in base]
    v = verdict(fast, 40.0, False, True)
    assert v['nights_AB'] <= 4 and v['verdict'] == 'ALL-DECIDED-0-SAT: propose stratum A nights', v  # f = 4: 3.4 nights
    cens = [(p, 'TIMEOUT' if i < 37 else st, TAU if i < 37 else s) for i, (p, st, s) in enumerate(base)]  # 37/360 > 10 %
    assert verdict(cens, 60.0, False, True)['verdict'].startswith('CENSORED'), cens[:1]
    cens36 = [(p, 'TIMEOUT' if i < 36 else st, TAU if i < 36 else s) for i, (p, st, s) in enumerate(base)]  # 36/360 = 10 %
    assert not verdict(cens36, 60.0, False, True)['verdict'].startswith('CENSORED')
    assert verdict(base[:299], 80.0, True, True)['verdict'].startswith('COST-MODEL-WRONG')
    assert verdict(base[:300], 80.0, True, True)['verdict'].startswith('INCOMPLETE')
    assert verdict(base[:299], 30.0, False, True)['verdict'].startswith('INCOMPLETE')
    assert verdict(base + [(ps[0], 'SAT', 9.0)], 50.0, False, True)['verdict'].startswith('FIRST-SAT')
    assert verdict(base, 50.0, False, False)['verdict'].startswith('CONTROL')
    assert verdict(base, 76.6, False, True)['over_1_5x_scenario'] and not verdict(base, 76.4, False, True)['over_1_5x_scenario']
    print('selftest OK: f = 5.5 -> %.2f nights (Actions); f = 4 -> %.2f nights (stratum A); censored 37/360 escalates, 36/360 not'
          % (verdict(base, 50, False, True)['nights_AB'], verdict(fast, 40, False, True)['nights_AB']))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    run = sys.argv[1] if len(sys.argv) > 1 else str(HERE / 'results/run')
    units, spent, cap, ok = load(run)
    table(units)
    print(json.dumps(verdict(units, spent, cap, ok), indent=1))
