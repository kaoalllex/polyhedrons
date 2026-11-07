"""Check the final accepted recovery scope at two plane rationalization scales."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction
import time
import traceback
import independent

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
INPUT = ROOT / 'experiments/E-261103-04-s5-genus-ladder-9-faces/results/recovery-pilot-oriented'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

started = time.monotonic()
result = json.loads((INPUT / 'recovery.json').read_text())
assert all(unit['status'] != 'RUNNING' for unit in result['units'])
report = dict(evidence='PROVED-1 supplied-input standalone rational computation, unreviewed',
              pilot_sha256=digest(INPUT / 'recovery.json'),
              verifier_sha256=digest(OUT / 'independent.py'),
              driver_sha256=digest(Path(__file__)), rows=[],
              reused_source=str(ROOT / 'experiments/E-261103-05-s5-symmetric-solid-first/verify_independent.py'),
              reused_source_sha256=digest(ROOT / 'experiments/E-261103-05-s5-symmetric-solid-first/verify_independent.py'))
for unit in result['units']:
    for rec in unit['levels']:
        if not rec.get('exact', {}).get('PASS'):
            continue
        name, genus = unit['name'], rec['genus']
        path = INPUT / f'{name}-g{genus}.json'
        record = json.loads(path.read_text())
        expected = result['exports'][name][genus]['expected_topology']
        row = dict(name=name, genus=genus, file=path.name, input_sha256=digest(path), scales=[])
        report['rows'].append(row)
        for scale in (10**9, 10**12):
            integer = dict(planes=[[int(round(float(v)*scale)) for v in plane] for plane in record['planes']],
                           links=record['links'])
            try:
                verified = independent.check(integer, expected, require_all_pairs=name == 'szilassi' and genus == 1)
                verified['min_abs_normal_determinant'] /= scale**3
                verified['min_abs_plane_determinant'] /= scale**4
                verified['min_abs_nonincident_plane_value'] /= scale
                verified['rationalization_scale'] = scale
                bad = dict(planes=[p[:] for p in integer['planes']], links=integer['links'])
                bad['planes'][1] = bad['planes'][0][:]
                try:
                    independent.check(bad, expected)
                    raise AssertionError('duplicate-plane negative control accepted')
                except ValueError as error:
                    verified['duplicate_plane_rejected'] = str(error)
            except Exception as error:
                verified = dict(verdict='REJECT', error=f'{type(error).__name__}: {error}',
                                traceback=traceback.format_exc(), rationalization_scale=scale)
            row['scales'].append(verified)
            print(name, genus, scale, verified['verdict'], verified.get('error', ''), flush=True)
assert report['rows'], 'no accepted recoveries to check'
report['verdict'] = 'ACCEPT' if all(s['verdict'] == 'ACCEPT' for r in report['rows'] for s in r['scales']) else 'REJECT'
report['wall_seconds'] = time.monotonic() - started
(OUT/'report.json').write_text(json.dumps(report, indent=2, default=str)+'\n')
print(report['verdict'],len(report['rows']),report['wall_seconds'])
raise SystemExit(0 if report['verdict'] == 'ACCEPT' else 1)
