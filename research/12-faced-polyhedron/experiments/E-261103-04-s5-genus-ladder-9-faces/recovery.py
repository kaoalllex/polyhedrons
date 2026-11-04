"""Registered, bounded recovery of known geometry along saved dart-map ladders."""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / 'code'))
CONTROLS = [('szilassi', 10401), ('roest_vigh', 10402), ('mizhaev', 10403)]


class GateFailure(Exception):
    pass


def write_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def isomorphism(source, target, preserve_labels=False):
    """Find and directly check a rooted dart bijection, including orientation."""
    root = min(source.pos)
    code, order = source.code(root)
    for mirror in (False, True):
        for other in sorted(target.pos):
            other_code, other_order = target.code(other, mirror)
            if code != other_code:
                continue
            darts = dict(zip(order, other_order))
            tail = target.head if mirror else lambda d: target.tail[d]
            head = (lambda d: target.tail[d]) if mirror else target.head
            labels = {}
            for d, e in darts.items():
                labels.setdefault(source.tail[d], set()).add(tail(e))
            if any(len(values) != 1 for values in labels.values()):
                continue
            labels = {label: next(iter(values)) for label, values in labels.items()}
            if preserve_labels and (mirror or any(a != b for a, b in labels.items())):
                continue
            assert len(set(darts.values())) == len(source.pos) == len(target.pos)
            assert len(set(labels.values())) == len(labels)
            step = target.prv if mirror else target.nxt
            assert all(darts[source.nxt(d)] == step(e)
                       and darts[source.alpha[d]] == target.alpha[e]
                       and labels[source.tail[d]] == tail(e)
                       and labels[source.head(d)] == head(e)
                       for d, e in darts.items())
            return dict(darts=sorted(darts.items()), labels=sorted(labels.items()),
                        orientation_reversed=mirror)
    raise GateFailure('REPRESENTATION-FAIL: no checked dart-map isomorphism')


def export_level(data, n, genus, census, audit):
    surface = audit.check_surface(data, n, genus, simple=genus == 0)
    original = audit.restore(data, census)
    links = {}
    for cycle in original.vertices()[0]:
        label = original.tail[cycle[0]]
        links[label] = [original.head(d) for d in cycle]
    ordered = [links[v] for v in range(n)]
    try:
        rebuilt = census.from_links(ordered)
    except ValueError as error:
        raise GateFailure(f'REPRESENTATION-FAIL: {error}') from error
    # from_links numbers darts in input cycle order, then assigns new vertex labels.
    input_labels = [v for v in range(n) for _ in ordered[v]]
    relabel = {}
    for d, v in enumerate(input_labels):
        previous = relabel.setdefault(rebuilt.tail[d], v)
        assert previous == v, 'reconstruction split a labelled vertex'
    assert len(relabel) == len(set(relabel.values())) == n
    rebuilt.tail = [relabel[v] for v in rebuilt.tail]
    assert original.canon()[0] == rebuilt.canon()[0], 'canonical round trip'
    checked = isomorphism(original, rebuilt, preserve_labels=True)
    audit.check_surface(audit.snapshot(rebuilt), n, genus, simple=genus == 0)
    expected = [surface['triangles'], surface['edges'], n, 2 - 2 * genus]
    return dict(links=links, surface=surface, expected_topology=expected,
                reconstruction_labels=sorted(relabel.items()), roundtrip=checked)


def exact_check(out, stem, planes, level, target, verifier, negative=False):
    candidate = out / f'{stem}.json'
    write_json(candidate, dict(planes=planes, links=level['links']))
    started = time.monotonic()
    try:
        report = verifier._verify(dict(planes=planes, links=level['links']))
    except AssertionError as error:
        if not negative or str(error) != 'three planes not in general position':
            raise
        (out / f'{stem}.verify.txt').write_text(f'INVALID-INPUT: {error}\n')
        return dict(PASS=False, status='INVALID-INPUT', error=str(error),
                    wall_seconds=time.monotonic() - started)
    command = [sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(candidate)]
    if target:
        command += ['--target', target] if target == 'S5' else ['--all-pairs']
    checked = subprocess.run(command, capture_output=True, text=True, timeout=30)
    (out / f'{stem}.verify.txt').write_text(checked.stdout + checked.stderr)
    passed = verifier.passes(report, target)
    if checked.returncode not in (0, 1) or checked.stderr or (checked.returncode == 0) != passed:
        raise RuntimeError(f'saved-file verifier disagreed or failed for {stem}')
    topology_matches = list(report['V_E_F_chi']) == level['expected_topology']
    report.update(PASS=bool(passed and topology_matches), topology_matches=topology_matches,
                  target=target or 'embedded', wall_seconds=time.monotonic() - started,
                  adjacent_pairs=level['surface']['adjacent_pairs'])
    return report


def objective(planes, links, ladder, np):
    try:
        packed, sizes, _ = ladder.pack(links)
        events, depth = ladder.pair_energy(np.asarray(planes, dtype=float), packed, sizes)
        value = float(events + ladder.DEPTH_W * np.tanh(depth))
        return dict(value=value if np.isfinite(value) else None,
                    events=int(events), depth=float(depth) if np.isfinite(depth) else None)
    except (ValueError, ZeroDivisionError, np.linalg.LinAlgError) as error:
        return dict(status='INVALID-INPUT', error=f'{type(error).__name__}: {error}')


def worker(out, calibration=False, startup_only=False):
    result = dict(stage='calibration' if calibration else 'recovery', controls=[], units=[],
                  exports={}, controls_pass=False, conditional_pass=False,
                  recovery_pass=False, stop_reason='ERROR', timings={})
    def save():
        write_json(out / 'recovery.json', result)
    save()
    try:
        started = time.monotonic()
        import numpy as np
        import genus_ladder as ladder
        import audit
        from control_rost_vigh import build
        ladder.EXTRA = None
        ladder.DEPTH_W = 0.01
        census = audit.load_module('recovery_census', audit.CENSUS / 'census.py')
        verifier = audit.load_module('recovery_verifier', ROOT / 'verification/verify_candidate.py')
        result['timings']['imports_seconds'] = time.monotonic() - started
        saved = HERE / 'results/surgery-audit'
        manifest = json.loads((saved / 'manifest.json').read_text())
        raw = gzip.decompress((saved / 'audit.json.gz').read_bytes())
        assert hashlib.sha256(raw).hexdigest() == manifest['outputs']['audit.json']
        assert (saved / 'check-saved.txt').read_text().strip() == (
            'PASS: 206 saved maps, source identities, surface/patch checks and reversible chains')
        for relative in ('experiments/E-261103-01-s5-map-census/census.py',
                         'reviews/strategy-review-2026-11-03-flipwalk.py',
                         'experiments/E-261103-01-s5-map-census/results/maps_7_1.json',
                         'code/control_rost_vigh.py', 'literature/mizhaev2026-planes.json'):
            assert digest(ROOT / relative) == manifest['inputs'][relative], relative
        result['reused_surgery_check'] = dict(transcript_sha256=digest(saved / 'check-saved.txt'),
                                             checker_commit='2ff5953')
        rows = json.loads(raw)['rows']
        szilassi = json.loads((ROOT / 'experiments/E-261101-25-chirotope-first/szilassi_control.json').read_text())
        roest_planes, roest_links = build()
        mizhaev = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())
        source_links = dict(
            szilassi=ladder.links_from(ladder.coherent_triangles(szilassi['triangles']), 7),
            roest_vigh=roest_links,
            mizhaev={int(v): neighbors for v, neighbors in mizhaev['links_0based'].items()}
            if isinstance(mizhaev['links_0based'], dict) else dict(enumerate(mizhaev['links_0based'])))
        source_planes = dict(szilassi=szilassi['planes'], roest_vigh=roest_planes,
                             mizhaev=mizhaev['planes_abcd_zero_form'])
        prepared = {}
        for name, seed in CONTROLS:
            row = next(row for row in rows if row['name'] == name)
            n, top_genus = row['n'], row['top_genus']
            assert row['status'] == 'CHAIN-PASS' and len(row['levels']) == top_genus + 1
            levels = []
            result['exports'][name] = levels
            for genus, data in enumerate(reversed(row['levels'])):
                levels.append(export_level(data, n, genus, census, audit))
                save()
            top = audit.restore(row['levels'][0], census)
            coherent = census.review.coherent(source_links[name])
            reference = census.from_links([coherent[v] for v in range(n)])
            reference.tail = [v for v in range(n) for _ in coherent[v]]
            reflected = census.review.TriMap([list(reversed(t)) for t in top.tri],
                top.alpha, [top.head(d) if d in top.pos else 0 for d in range(len(top.tail))])
            isomorphism(top, reflected)
            alignment = isomorphism(top, reference)
            labels = dict(alignment['labels'])
            planes = [[float(v) for v in source_planes[name][labels[label]]] for label in range(n)]
            control = dict(name=name, seed=seed, alignment=alignment)
            result['controls'].append(control)
            target = 'S5' if name == 'szilassi' else 'all-pairs'
            control['positive'] = exact_check(out, f'{name}-positive', planes, levels[-1], target, verifier)
            save()
            if not control['positive']['PASS']:
                raise GateFailure(f'CONTROL-FAIL: {name} positive')
            begin = time.monotonic()
            control['positive_objective'] = objective(planes, levels[-1]['links'], ladder, np)
            result['timings'].setdefault('objective_seconds_including_jit', 0)
            result['timings']['objective_seconds_including_jit'] += time.monotonic() - begin
            negative = [list(plane) for plane in planes]
            negative[1] = list(negative[0])
            control['negative'] = exact_check(out, f'{name}-negative', negative, levels[-1],
                                               target, verifier, negative=True)
            control['negative_objective'] = objective(negative, levels[-1]['links'], ladder, np)
            save()
            if control['negative']['PASS']:
                raise GateFailure(f'CONTROL-FAIL: {name} negative accepted')
            prepared[name] = (n, levels, target)
            print(f'{name}: deterministic controls PASS, {len(levels)} labelled round trips PASS', flush=True)
        result['controls_pass'] = True
        save()
        if calibration:
            previous = HERE / 'results/recovery-pilot-oriented'
            prior_manifest = json.loads((previous / 'manifest.json').read_text())
            for filename, expected in prior_manifest['outputs'].items():
                assert digest(previous / filename) == expected, filename
            prior = json.loads((previous / 'recovery.json').read_text())
            review_dir = HERE / 'results/recovery-review'
            review = json.loads((review_dir / 'report.json').read_text())
            assert review['pilot_sha256'] == digest(previous / 'recovery.json')
            assert review['verifier_sha256'] == digest(review_dir / 'independent.py')
            assert review['driver_sha256'] == digest(review_dir / 'run_check.py')
            assert review['reused_source_sha256'] == digest(HERE.parent /
                'E-261103-05-s5-symmetric-solid-first/verify_independent.py')
            assert review['verdict'] == 'ACCEPT'
            transcript = gzip.decompress((review_dir / 'check-saved.txt.gz').read_bytes()).decode()
            assert transcript.strip().splitlines()[-1].split()[:2] == ['ACCEPT', '5']
            result['reused_parent_review'] = dict(report_sha256=digest(review_dir / 'report.json'),
                transcript_sha256=digest(review_dir / 'check-saved.txt.gz'))
            cells = []
            parents = {}
            for name, genus, seed in [('roest_vigh', 1, 1040201), ('mizhaev', 2, 1040302)]:
                _, levels, _ = prepared[name]
                assert json.loads(json.dumps(levels)) == prior['exports'][name], name
                unit = next(unit for unit in prior['units'] if unit['name'] == name)
                parent_level = next(level for level in unit['levels'] if level['genus'] == genus - 1)
                failed = next(level for level in unit['levels'] if level['genus'] == genus)
                assert parent_level['exact']['PASS'] and not failed['exact']['PASS']
                assert failed['rng_seed'] == seed
                filename = f'{name}-g{genus - 1}.json'
                parent = json.loads((previous / filename).read_text())
                assert parent['links'] == json.loads(json.dumps(levels[genus - 1]['links']))
                accepted = next(row for row in review['rows'] if row['file'] == filename)
                assert accepted['input_sha256'] == digest(previous / filename)
                assert len(accepted['scales']) == 2
                assert all(scale['verdict'] == 'ACCEPT' for scale in accepted['scales'])
                parents[name] = parent['planes']
                for seconds in (180, 600):
                    cells.append(dict(name=name, genus=genus, rng_seed=seed,
                        parent_file=filename, parent_sha256=digest(previous / filename),
                        requested_seconds=seconds))
            cells.sort(key=lambda cell: (cell['requested_seconds'], cell['name'] != 'roest_vigh'))
            result['planned_cells'] = cells
            save()
            if startup_only:
                result['stop_reason'] = 'STARTUP-PASS'
                return 0
            for cell in cells:
                name, genus, seconds = cell['name'], cell['genus'], cell['requested_seconds']
                n, levels, _ = prepared[name]
                record = dict(cell, status='RUNNING')
                result['units'].append(record)
                save()
                print(f'{name}: conditional genus {genus}, budget {seconds}s', flush=True)
                begin = time.monotonic()
                (best, planes), restarts = ladder.search(levels[genus]['links'], n, seconds / 60,
                    np.random.default_rng(cell['rng_seed']), seed_planes=parents[name])
                elapsed = time.monotonic() - begin
                record.update(optimization_seconds=elapsed, budget_fraction=elapsed / seconds,
                    restarts=restarts, objective=float(best),
                    optimizer_stop='ENERGY-THRESHOLD' if best < 0.5 else 'REQUESTED-TIME')
                if planes is None:
                    raise RuntimeError('optimizer returned no plane set')
                record['exact'] = exact_check(out, f'{name}-g{genus}-{seconds}s', planes.tolist(),
                    levels[genus], None, verifier)
                record['status'] = 'EXACT-PASS' if record['exact']['PASS'] else 'EXACT-REJECTION'
                result['conditional_pass'] |= record['exact']['PASS']
                save()
            result['stop_reason'] = 'CONDITIONAL-PASS' if result['conditional_pass'] else 'UNDERPOWERED'
            return 0
        for name, seed in CONTROLS:
            n, levels, target = prepared[name]
            unit = dict(name=name, seed=seed, levels=[], status='RUNNING')
            result['units'].append(unit)
            seed_planes = None
            for genus, level in enumerate(levels):
                record = dict(genus=genus, rng_seed=100 * seed + genus, requested_seconds=45)
                unit['levels'].append(record)
                print(f'{name}: searching genus {genus}, seed {record["rng_seed"]}', flush=True)
                save()
                begin = time.monotonic()
                (best, planes), restarts = ladder.search(level['links'], n, 45 / 60,
                    np.random.default_rng(record['rng_seed']), seed_planes=seed_planes)
                elapsed = time.monotonic() - begin
                record.update(optimization_seconds=elapsed, budget_fraction=elapsed / 45,
                              restarts=restarts, objective=float(best),
                              optimizer_stop='ENERGY-THRESHOLD' if best < 0.5 else 'REQUESTED-TIME')
                if planes is None:
                    raise RuntimeError('optimizer returned no plane set')
                plane_list = planes.tolist()
                selected_target = target if genus == len(levels) - 1 else None
                record['exact'] = exact_check(out, f'{name}-g{genus}', plane_list, level,
                                               selected_target, verifier)
                record['stop_reason'] = 'EXACT-PASS' if record['exact']['PASS'] else 'EXACT-REJECTION'
                save()
                print(f'{name}: genus {genus} {record["stop_reason"]}, '
                      f'objective {best}, optimizer {elapsed:.3f}s', flush=True)
                if not record['exact']['PASS']:
                    unit['status'] = 'UNDERPOWERED'
                    break
                seed_planes = plane_list
            else:
                unit['status'] = 'RECOVERY-PASS'
            save()
        result['recovery_pass'] = all(unit['status'] == 'RECOVERY-PASS' for unit in result['units'])
        result['stop_reason'] = 'RECOVERY-PASS' if result['recovery_pass'] else 'UNDERPOWERED'
        return 0
    except GateFailure as error:
        result.update(stop_reason=str(error).split(':')[0], error=str(error))
        traceback.print_exc()
        return 1
    except BaseException as error:
        result.update(stop_reason='ERROR', error=f'{type(error).__name__}: {error}',
                      traceback=traceback.format_exc())
        traceback.print_exc()
        return 1
    finally:
        save()
        print(json.dumps({k: result[k] for k in ('controls_pass', 'recovery_pass', 'stop_reason')}), flush=True)


def run(out, calibration=False, startup_only=False):
    started = time.monotonic()
    wall_seconds = 120 if startup_only else 1800 if calibration else 600
    out.mkdir(parents=True, exist_ok=False)
    manifest = dict(started_utc=datetime.now(timezone.utc).isoformat(), workers=1,
                    host=platform.platform(), cpu_count=os.cpu_count(), python=sys.version,
                    executable=sys.executable, virtual_env=os.environ.get('VIRTUAL_ENV'),
                    cwd=os.getcwd(), shard=0,
                    parameters=dict(stage='calibration' if calibration else 'recovery',
                                    startup_only=startup_only, wall_seconds=wall_seconds,
                                    level_seconds=[180, 600] if calibration else 45,
                                    seeds={'roest_vigh': 1040201, 'mizhaev': 1040302} if calibration else dict(CONTROLS),
                                    finalization_reserve_seconds=3))
    result = dict(stop_reason='ERROR', controls_pass=False, recovery_pass=False)
    exit_status = 1
    try:
        for key, command in (
            ('commit', ['git', 'rev-parse', 'HEAD']),
            ('branch', ['git', 'branch', '--show-current']),
            ('dirty', ['git', 'status', '--porcelain']),
            ('pip_freeze', [sys.executable, '-m', 'pip', 'freeze']),
        ):
            manifest[key] = subprocess.check_output(command, cwd=ROOT, text=True, timeout=15).strip()
        saved = HERE / 'results/surgery-audit'
        paths = [Path(__file__), HERE / 'audit.py', HERE / 'PLAN.md', HERE / 'run.sh',
                 saved / 'audit.json.gz', saved / 'manifest.json', saved / 'check-saved.txt',
                 ROOT / 'experiments/E-261103-01-s5-map-census/census.py',
                 ROOT / 'experiments/E-261103-01-s5-map-census/results/maps_7_1.json',
                 ROOT / 'experiments/E-261101-25-chirotope-first/szilassi_control.json',
                 ROOT / 'reviews/strategy-review-2026-11-03-flipwalk.py',
                 ROOT / 'literature/mizhaev2026-planes.json',
                 ROOT / 'verification/verify_candidate.py']
        paths += [ROOT / 'code' / f'{name}.py' for name in
                  ('genus_ladder', 'ladder', 'ladder_exact', 'gauss_degree', 'control_rost_vigh', 'tubes')]
        if calibration:
            paths += [HERE / 'results' / directory / filename for directory, filenames in (
                ('recovery-pilot-oriented', ('manifest.json', 'recovery.json', 'roest_vigh-g0.json', 'mizhaev-g1.json')),
                ('recovery-review', ('report.json', 'independent.py', 'run_check.py', 'check-saved.txt.gz')))
                for filename in filenames]
            paths.append(HERE.parent / 'E-261103-05-s5-symmetric-solid-first/verify_independent.py')
        manifest['inputs'] = {str(path.relative_to(ROOT)): digest(path) for path in paths}
        manifest['thread_limits'] = {key: os.environ.get(key) for key in
                                    ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                                     'VECLIB_MAXIMUM_THREADS', 'NUMBA_NUM_THREADS')}
        write_json(out / 'manifest.json', manifest)
        with (out / 'stdout.txt').open('w') as stdout, (out / 'stderr.txt').open('w') as stderr:
            command = [sys.executable, str(Path(__file__).resolve()), '--worker', str(out)]
            if calibration:
                command += ['--calibration']
            if startup_only:
                command += ['--startup-only']
            process = subprocess.Popen(command,
                                       stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                exit_status = process.wait(timeout=max(0.01, wall_seconds - 3 - (time.monotonic() - started)))
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=1)
                exit_status = 124
        if (out / 'recovery.json').exists():
            result = json.loads((out / 'recovery.json').read_text())
        if exit_status == 124:
            result.update(stop_reason='TIMEOUT', recovery_pass=False)
        elif exit_status != 0 and result['stop_reason'] not in ('ERROR', 'CONTROL-FAIL', 'REPRESENTATION-FAIL'):
            result.update(stop_reason='ERROR', recovery_pass=False)
    except BaseException as error:
        result.update(stop_reason='ERROR', error=f'{type(error).__name__}: {error}')
        traceback.print_exc()
    finally:
        write_json(out / 'recovery.json', result)
        elapsed = time.monotonic() - started
        manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(), exit_status=exit_status,
                        wall_seconds=elapsed, core_hours=elapsed / 3600, budget_fraction=elapsed / wall_seconds,
                        stop_reason=result['stop_reason'],
                        outputs={path.name: digest(path) for path in out.iterdir()
                                 if path.is_file() and path.name != 'manifest.json'})
        write_json(out / 'manifest.json', manifest)
    print(json.dumps(dict(stop_reason=result['stop_reason'], wall_seconds=elapsed,
                         controls_pass=result['controls_pass'], recovery_pass=result['recovery_pass'])))
    return exit_status


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--calibration', action='store_true')
    parser.add_argument('--startup-only', action='store_true')
    args = parser.parse_args()
    if args.startup_only and not args.calibration:
        parser.error('--startup-only requires --calibration')
    if args.worker:
        sys.exit(worker(args.worker.resolve(), args.calibration, args.startup_only))
    if args.out is None:
        parser.error('--out is required')
    sys.exit(run(args.out.resolve(), args.calibration, args.startup_only))
