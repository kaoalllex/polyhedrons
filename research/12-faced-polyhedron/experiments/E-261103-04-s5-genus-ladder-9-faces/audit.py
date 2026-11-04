"""Audit the legacy triangle-to-links conversion before geometric ladder work."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CENSUS = ROOT / 'experiments/E-261103-01-s5-map-census'
sys.path.insert(0, str(ROOT / 'code'))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def roundtrip(name, m, census):
    from gauss_degree import coherent_triangles, links_from
    edges = Counter((m.tail[d], m.head(d)) for d in m.pos)
    row = dict(name=name, vertices=m.vertex_count(), edges=len(m.pos) // 2,
               triangles=len(m.tri), max_directed_multiplicity=max(edges.values()))
    try:
        triangles = [tuple(m.tail[d] for d in t) for t in m.tri]
        links = links_from(coherent_triangles(triangles), m.vertex_count())
        recovered = census.from_links([links[v] for v in range(m.vertex_count())])
        row['same_dart_code'] = recovered.canon()[0] == m.canon()[0]
        row['recovered_edges'] = len(recovered.pos) // 2
        row['status'] = 'ROUNDTRIP-PASS' if row['same_dart_code'] else 'ROUNDTRIP-FAIL'
    except (AssertionError, ValueError, KeyError) as error:
        row.update(status='ROUNDTRIP-FAIL', error_type=type(error).__name__, error=str(error))
    return row


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    manifest = dict(started_utc=datetime.now(timezone.utc).isoformat(), workers=1,
                    host=platform.platform(), cpu_count=os.cpu_count(),
                    python=sys.version, parameters=dict(wall_seconds=120))
    for key, command in (
        ('commit', ['git', 'rev-parse', 'HEAD']),
        ('branch', ['git', 'branch', '--show-current']),
        ('dirty', ['git', 'status', '--porcelain']),
        ('pip_freeze', [sys.executable, '-m', 'pip', 'freeze']),
    ):
        manifest[key] = subprocess.check_output(command, cwd=ROOT, text=True).strip()
    paths = [Path(__file__), HERE / 'PLAN.md', HERE / 'run.sh', CENSUS / 'census.py',
             ROOT / 'reviews/strategy-review-2026-11-03-flipwalk.py',
             ROOT / 'code/gauss_degree.py', ROOT / 'code/control_rost_vigh.py',
             ROOT / 'literature/mizhaev2026-planes.json',
             CENSUS / 'results/maps_7_1.json', CENSUS / 'results/maps_9_3.json']
    manifest['inputs'] = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    result = dict(rows=[], scope='legacy triangle-to-links round-trip only')

    def save():
        (out / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')

    def expired(signum, frame):
        raise TimeoutError('registered 120-second audit budget')

    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, max(0.001, 120 - (time.monotonic() - started)))
    try:
        census = load_module('s5_census', CENSUS / 'census.py')
        # Frozen census maps retain parallel-edge identities in their dart codes.
        for filename, prefix in (('maps_7_1.json', 'szilassi'), ('maps_9_3.json', 'focus')):
            data = json.loads((CENSUS / 'results' / filename).read_text())
            for index, record in enumerate(data['maps']):
                if record['admissible']:
                    m = census.from_code(record['code'])
                    result['rows'].append(roundtrip(f'{prefix}_{index}', m, census))
                    save()
        from control_rost_vigh import build
        _, links = build()
        mizhaev = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())['links_0based']
        if isinstance(mizhaev, dict):
            mizhaev = [mizhaev[str(v)] for v in range(len(mizhaev))]
        for name, link in (('roest_vigh', [links[v] for v in range(len(links))]),
                           ('mizhaev', mizhaev)):
            result['rows'].append(roundtrip(name, census.from_links(list(census.review.coherent(dict(enumerate(link))).values())), census))
            save()
        rows = result['rows']
        positive = [r for r in rows if r['name'].startswith('szilassi_')]
        negative = next(r for r in rows if r['name'] == 'roest_vigh')
        result['controls_pass'] = (len(positive) == 1
                                  and positive[0]['status'] == 'ROUNDTRIP-PASS'
                                  and negative['max_directed_multiplicity'] > 1
                                  and negative['status'] == 'ROUNDTRIP-FAIL')
        result['gate_pass'] = (result['controls_pass']
                               and all(r['status'] == 'ROUNDTRIP-PASS' for r in rows
                                       if not r['name'].startswith('szilassi_')))
        result['stop_reason'] = 'COMPLETE'
        manifest['exit_status'] = 0
    except BaseException as error:
        result.update(stop_reason=type(error).__name__, error=str(error))
        manifest['exit_status'] = 1
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
        save()
        elapsed = time.monotonic() - started
        manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(),
                        wall_seconds=elapsed, core_hours=elapsed / 3600,
                        budget_fraction=elapsed / 120,
                        outputs={'audit.json': digest(out / 'audit.json')})
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    main(parser.parse_args().out)
