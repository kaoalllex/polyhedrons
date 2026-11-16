"""Prepare the registered census, size controls and frozen stratified price queue."""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / 'E-261110-06-s5-10-4-strata-ab-remainder'))
import prep as previous
from prep import pilot
sys.path.insert(0, str(HERE.parent / 'E-261114-01-normalised-s6-10-3'))
import controls
sys.path.insert(0, str(Path(pilot.__file__).parent))
import control_f9


def load_census():
    path = ROOT / 'experiments/E-261103-01-s5-map-census/census.py'
    spec = importlib.util.spec_from_file_location('census', path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def prepare(reuse=False):
    dest = HERE / 'results/census'
    census = load_census()
    data = json.loads((dest/'maps_11_5.json').read_text()) if reuse else census.run(11, 5, 540, dest)
    if reuse:
        manifest = json.loads((dest/'manifest.json').read_text())
        assert manifest['files']['maps_11_5.json'] == pilot.sha(dest/'maps_11_5.json')
    reference = json.loads((ROOT / 'reviews/strategy-review-2026-11-16-census-11-5.json').read_text())
    rows = [r for r in data['maps'] if r['admissible']]
    digest = hashlib.sha256('\n'.join(sorted(str(r['code']) for r in data['maps'])).encode()).hexdigest()
    checks = dict(complete=data['complete'] and data['stop_reason'] == 'exhausted',
                  classes=data['classes'] == reference['classes'], admissible=len(rows) == reference['admissible'],
                  codes=digest == reference['codes_sha256'],
                  patterns=dict(Counter(str(r['extra_pattern']) for r in rows)) == reference['extra_patterns_admissible'],
                  autos=dict(Counter(str(r['aut_plus']) for r in rows)) == reference['aut_plus_admissible'])
    # The raw map file includes enumerator timing; compare canonical codes rather than its byte hash.
    for r in data['maps']:
        m = census.from_code(r['code']); census.review.check(m, 11, 5)
        assert census.admissible(m) == r['admissible']
    checks['euler_and_admissibility'] = True
    report = dict(PASS=all(checks.values()), checks=checks, classes=data['classes'], admissible=len(rows),
                  codes_sha256=digest, reference_sha256=pilot.sha(ROOT/'reviews/strategy-review-2026-11-16-census-11-5.json'))
    pilot.dump(HERE/'results/census-check.json', report)
    assert report['PASS'], report
    raw = (dest/'maps_11_5.json').read_bytes()
    (dest/'maps_11_5.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    print(json.dumps(report), flush=True)


def control_shard(spec):
    k, jobs, data = spec
    dest = HERE / 'results/controls' / str(k); dest.mkdir(parents=True, exist_ok=True)
    rows = []; start = time.monotonic()
    for name, pinned, negative in jobs:
        t = controls.topology(data['negative_links'] if negative else data['links'])
        c = pilot.CNF(11); pilot.build(c, t, dict(pilot.ALL_OPTS, symbreak=True, mirror=True))
        if pinned:
            chi, transform = controls.gauge(pilot.chirotope_from_planes(data['planes']), 11, True)
            c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()])
        r = dict(name=name, **pilot.solve(c, dest, name, 60))
        r['passed'] = r['status'] == ('UNSAT-SOLVER' if negative else 'SAT')
        rows.append(r); pilot.dump(dest/'results.json', rows)
    pilot.dump(dest/'manifest.json', dict(shard=k, wall_seconds=time.monotonic()-start,
               python=sys.version, commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
               solver_sha256=pilot.sha(Path(pilot.CADICAL))))
    return rows


def size_controls():
    reused = previous.controls()
    rows, links = control_f9.build(faces=11)
    other = control_f9.build(2611080301, faces=11)[1]
    assert other != links
    data = dict(planes=rows, links=links, negative_links=other)
    assert control_f9.polyhedron(rows)[1] == 18
    pilot.dump(HERE/'control_f11.json', data)
    jobs = [('convex_f11_pinned', True, False), ('convex_f11_unpinned', False, False),
            ('convex_f11_wrong_map', True, True)]
    with ProcessPoolExecutor(10) as pool:
        results = sum(pool.map(control_shard, [(k, jobs[k::10], data) for k in range(10)]), [])
    inputs = (Path(__file__), Path(control_f9.__file__), Path(controls.__file__),
              ROOT/'code/omsat.py', Path(pilot.__file__), HERE/'control_f11.json')
    report = dict(PASS=len(results)==3 and all(r['passed'] for r in results), rows=results,
                  reuse=reused, inputs_sha256={str(p.relative_to(ROOT)):pilot.sha(p) for p in inputs})
    pilot.dump(HERE/'results/controls/summary.json', report)
    print(json.dumps(report), flush=True)
    assert report['PASS'], 'size control failed'


def queue():
    assert json.loads((HERE/'results/census-check.json').read_text())['PASS']
    assert json.loads((HERE/'results/controls/summary.json').read_text())['PASS']
    path = HERE/'results/census/maps_11_5.json.gz'
    with gzip.open(path, 'rt') as stream:
        data = json.load(stream)
    rng = random.Random(26111601); entries = []; populations = {}
    for pattern, count in [([1,1,1,1],5), ([1,1,2],4), ([2,2],1)]:
        indices = [i for i,m in enumerate(data['maps']) if m['admissible'] and m['extra_pattern']==pattern]
        populations[str(pattern)] = len(indices)
        for i in rng.sample(indices, count):
            m = data['maps'][i]
            entries.append(dict(index=i, pattern=str(pattern), solver_cap=3600,
                                canonical_sha256=hashlib.sha256(json.dumps(m['code'],separators=(',',':')).encode()).hexdigest()))
    inputs = [path, HERE/'results/census-check.json', HERE/'results/controls/summary.json', Path(__file__),
              HERE/'run.sh', ROOT/'code/omsat.py', Path(pilot.__file__), Path(previous.tranche.__file__)]
    record = dict(target='S5 (11,5)', case=[11,5], seed=26111601, populations=populations,
                  census_file=str(path.relative_to(ROOT)), truncate_to_budget=True,
                  controls_file=str((HERE/'results/controls/summary.json').relative_to(ROOT)),
                  inputs_sha256={str(p.relative_to(ROOT)):pilot.sha(p) for p in inputs}, maps=entries)
    pilot.dump(HERE/'queue.json', record)
    print('frozen maps:', [e['index'] for e in entries], flush=True)


if __name__ == '__main__':
    {'census':prepare, 'census-check':lambda:prepare(reuse=True), 'controls':size_controls, 'queue':queue}[sys.argv[1]]()
