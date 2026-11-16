"""Censored stratified pricing; planning decisions only, never a geometric negative."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def element_curve():
    negative = ROOT/'experiments/E-261114-01-normalised-s6-10-3/results/negative'
    result = {}; inputs = {}
    for faces in (8, 9):
        seconds = []
        for p in sorted(negative.glob('[0-9]*/results.json')):
            inputs[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
            seconds.extend(r['seconds'] for r in json.loads(p.read_text()) if r['name'].startswith(f'f{faces}_'))
        result[str(faces+1)] = dict(sampled=len(seconds), median_solver_seconds=statistics.median(seconds),
                                    selection=f'all admissible ({faces},{faces-6}) negative controls')
    source = ROOT/'experiments/E-261110-06-s5-10-4-strata-ab-remainder'
    rows = {}
    p = source/'results/prep/summary.json'
    inputs[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    for r in json.loads(p.read_text())['rows']:
        if r['map_index'] in (96,926,85,852):
            rows[r['map_index']] = r
    for p in sorted((source/'results/run').glob('[0-9]*/results.jsonl')):
        inputs[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
        for line in p.read_text().splitlines():
            r = json.loads(line); rows[r['map_index']] = r
    result['11'] = dict(sampled=len(rows), median_solver_seconds=statistics.median(r['seconds'] for r in rows.values()),
                        selection='normalised (10,4) A+B; four prep units plus owner remainder')
    return dict(points=result, inputs_sha256=inputs,
                limitation='Known-negative lower rungs; kissat, normalised, unequal map populations; extrapolation is not a bound')


def verdict(queue, rows):
    by_id = {r['map_index']: r for r in rows}
    expected = {e['index'] for e in queue['maps']}
    if len(by_id) != len(rows) or set(by_id)-expected:
        raise ValueError('duplicate or foreign map record')
    if any(r['status'] not in ('SAT','UNSAT-SOLVER','TIMEOUT','ERROR') for r in rows):
        raise ValueError('unexpected solver status')
    counts = dict(Counter(r['status'] for r in rows))
    result = dict(statuses=counts, completed=len(rows), expected=len(expected),
                  remaining=sorted(expected-set(by_id)), evidence='NUMERICAL',
                  scope='Sampled normalised S5 (11,5) formulas only; no proofs or geometric negative')
    if counts.get('SAT'):
        result['verdict'] = 'SAT-REVIEW'
        result['incomplete_model_sets'] = [r['map_index'] for r in rows if r['status']=='SAT' and not r['bridge_complete']]
    elif counts.get('ERROR'):
        result['verdict'] = 'ERROR'
    elif result['remaining']:
        result['verdict'] = 'INCOMPLETE'
    else:
        lower = [r['models'][0]['seconds'] for r in rows]
        upper = [math.inf if r['status']=='TIMEOUT' else r['models'][0]['seconds'] for r in rows]
        lo, hi = statistics.median(lower), statistics.median(upper)
        result.update(median_solver_seconds_lower=lo, median_solver_seconds_upper=hi if math.isfinite(hi) else None,
                      median_censored=lo != hi, s0_price_probe_allowed=lo==hi and hi<=1200)
        price = 0.; strata = {}
        for pattern, population in queue['populations'].items():
            sample = [r for r in rows if r['pattern']==pattern]
            mean = statistics.mean(r['price_seconds'] for r in sample)
            strata[pattern] = dict(population=population, sampled=len(sample), mean_lower_seconds=mean,
                                   censored=any(r['status']=='TIMEOUT' for r in sample))
            price += population*mean/3600
        censored = bool(counts.get('TIMEOUT'))
        result.update(strata=strata, projected_core_hours_lower=price, projected_nights_lower=price/80,
                      price_censored=censored)
        result['verdict'] = ('NO-SWEEP-SYMMETRIC-SLICE' if counts.get('TIMEOUT',0)>=5 or price>320
                             else 'OWNER-SWEEP' if not censored and price<=80 else 'LEAD-REVIEW')
    return result


def main():
    root = Path(sys.argv[1]) if len(sys.argv)>1 else HERE/(HERE/'launch.results').read_text().strip()
    root.mkdir(parents=True, exist_ok=True)
    queue = json.loads((HERE/'queue.json').read_text())
    rows = [json.loads(l) for p in sorted(root.glob('[0-9]*/results.jsonl')) for l in p.read_text().splitlines()]
    result = verdict(queue, rows)
    result['element_curve'] = element_curve()
    if 'median_solver_seconds_lower' in result:
        result['element_curve']['points']['12'] = dict(sampled=len(rows),
            median_solver_seconds_lower=result['median_solver_seconds_lower'],
            median_solver_seconds_upper=result['median_solver_seconds_upper'],
            selection='ten stratified (11,5) probe maps')
    manifests = [json.loads(p.read_text()) for p in root.glob('[0-9]*/manifest-*.json')]
    result['worker_wall_hours'] = sum(m['wall_seconds'] for m in manifests)/3600
    result['cpu_core_hours'] = sum(m['cpu_seconds'] for m in manifests)/3600
    result['max_endpoint_clock_gap'] = max((m['endpoint_clock_gap'] for m in manifests), default=None)
    result['queue_sha256'] = hashlib.sha256((HERE/'queue.json').read_bytes()).hexdigest()
    (root/'verdict.json').write_text(json.dumps(result,indent=2)+'\n')
    (root/'SUMMARY.md').write_text('# E-261116-01 run summary\n\n'+result['verdict']+'\n\n'+
                                  'NUMERICAL; sampled formula scope, no geometric negative.\n\n```json\n'+
                                  json.dumps(result,indent=2)+'\n```\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
