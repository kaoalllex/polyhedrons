"""Bounded plain-map tranche, invoked by the existing overnight runner."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
import uuid

import pilot
from pilot import HERE, ROOT, sha

QUEUE = HERE / 'tranche_queue.json'
BUDGET_SECONDS = 22319
SOLVER_CAP, CHECKER_CAP = 60, 120  # registered defaults; --timeout / --s5-checker-timeout override


def atomic(path, value):
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with tmp.open('w') as f:
        json.dump(value, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


@contextmanager
def locked(path, blocking=True):
    with path.open('a') as f:
        fcntl.flock(f, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def records(path):
    if not path.exists():
        return []
    lines = path.read_bytes().splitlines(keepends=True); result = []
    for i, line in enumerate(lines):
        try:
            result.append(json.loads(line))
        except (ValueError, UnicodeDecodeError) as exc:
            if i == len(lines) - 1 and not line.endswith(b'\n'):
                break
            raise ValueError(f'corrupt checkpoint {path}:{i + 1}') from exc
    return result


def append_checkpoint(path, record):
    # Truncate only a torn final write; completed bytes survive an interrupted repair.
    records(path)
    data = path.read_bytes() if path.exists() else b''
    if data and not data.endswith(b'\n'):
        end = data.rfind(b'\n') + 1
        try:
            json.loads(data[end:])
        except (ValueError, UnicodeDecodeError):
            with path.open('r+b') as f:
                f.truncate(end)
                f.flush(); os.fsync(f.fileno())
        else:
            with path.open('ab') as f:
                f.write(b'\n')
                f.flush(); os.fsync(f.fileno())
    with path.open('a') as f:
        f.write(json.dumps(record) + '\n'); f.flush(); os.fsync(f.fileno())


def load_queue(custom=False):
    data = json.loads(QUEUE.read_text())
    if custom:  # explicit map list (long-cap units): census identity and per-map canonical hashes only
        maps = pilot.census(9, 3)['maps']
        if sha(ROOT / 'experiments/E-261103-01-s5-map-census/results/maps_9_3.json') != data['census_sha256']:
            raise ValueError('census identity changed')
        for entry in data['maps']:
            if entry.get('control'):
                if sha(HERE / 'control_f9.json') != entry['control_sha256']:
                    raise ValueError('control identity changed')
                continue
            rec = maps[entry['index']]
            digest = hashlib.sha256(json.dumps(rec['code'], separators=(',', ':')).encode()).hexdigest()
            if not rec['admissible'] or digest != entry['canonical_sha256']:
                raise ValueError('custom queue map not admissible or identity changed')
        return data['maps']
    census_path = ROOT / 'experiments/E-261103-01-s5-map-census/results/maps_9_3.json'
    if sha(census_path) != data['census_sha256']:
        raise ValueError('census identity changed')
    seen = set()
    for name, digest in data['baseline_sha256'].items():
        path = HERE / name
        if sha(path) != digest:
            raise ValueError('baseline identity changed')
        for key in json.loads(path.read_text())['targets']:
            if '_plain' in key:
                seen.add(int(key.split('_')[0][3:]))
    maps = pilot.census(9, 3)['maps']
    expected = [i for i, r in enumerate(maps) if r['admissible'] and i not in seen][:80]
    if data['excluded_plain_indices'] != sorted(seen) or [r['index'] for r in data['maps']] != expected:
        raise ValueError('queue differs from registered new-map selection')
    for entry in data['maps']:
        rec = maps[entry['index']]
        digest = hashlib.sha256(json.dumps(rec['code'], separators=(',', ':')).encode()).hexdigest()
        if digest != entry['canonical_sha256']:
            raise ValueError('canonical map identity changed')
    return data['maps']


def check_identity(root, identity):
    path = root / 'identity.json'
    with locked(root / 'dispatch.lock'):
        if path.exists() and json.loads(path.read_text()) != identity:
            raise ValueError('source/input identity changed; resume blocked')
        if not path.exists():
            atomic(path, identity)


def latch_sat(root, record):
    with locked(root / 'dispatch.lock'):
        path = root / 'first_sat.json'
        if path.exists():
            return False
        atomic(path, dict(record, status='SAT-PENDING'))
        return True


def stopped(root):
    return any((root / name).exists() for name in ('first_sat.json', 'stop.json', 'stop.requested'))


class DispatchStopped(Exception):
    pass


@contextmanager
def dispatch_gate(root):
    with locked(root / 'dispatch.lock'):
        if stopped(root):
            raise DispatchStopped('shared stop precedes solver dispatch')
        yield


def pending(root, queue, shard, shards):
    done = set()
    checkpoints = list(root.glob('[0-9]*/results.jsonl'))
    if root == HERE / 'results':
        checkpoints += list((root / 'coverage_pilot').glob('[0-9]*/results.jsonl'))
    for path in checkpoints:
        for rec in records(path):
            if rec['status'] in ('SAT', 'UNSAT-VERIFIED', 'TIMEOUT'):
                if 'unit' in rec:
                    work = path.parent.parent.joinpath(*Path(rec['unit']).parts[-3:])
                    name = f'map{rec["map_index"]}_plain'
                    # CNF and proof files are not kept: the record must carry their hashes and a completed check.
                    needed = ['cnf_sha256'] + (['proof_sha256'] if rec['status'] == 'UNSAT-VERIFIED' else [])
                    if any(key not in rec for key in needed):
                        raise ValueError(f'missing recorded evidence hashes: {work / name}')
                    if rec['status'] == 'UNSAT-VERIFIED' and rec.get('checker_ended_by') != 'completed':
                        raise ValueError(f'proof check not completed: {work / name}')
                    if rec['status'] == 'SAT' and not (work / (name + '.model.json')).exists():
                        raise ValueError('missing saved SAT model')
                done.add(rec['map_index'])
    for entry in queue[shard::shards]:
        with locked(root / 'dispatch.lock'):
            if stopped(root):
                return
        if entry['index'] not in done:
            yield entry


def charged_seconds(root):
    path = root / 'budget.json'
    inherited = sum(json.loads(p.read_text())['wall_seconds'] for p in pilot_manifests(root))
    return inherited + (sum(json.loads(path.read_text()).values()) if path.exists() else 0)


def pilot_manifests(root):
    return sorted((root / 'coverage_pilot').glob('[0-9]*/attempt_*/manifest.json')) if root == HERE / 'results' else []


def reserve(root, seconds):
    with locked(root / 'budget.lock'):
        if charged_seconds(root) + seconds > BUDGET_SECONDS:
            raise RuntimeError('registered cumulative core budget exhausted; unresolved work remains')
        path = root / 'budget.json'
        data = json.loads(path.read_text()) if path.exists() else {}
        key = uuid.uuid4().hex; data[key] = seconds; atomic(path, data)
        return key


def finish_reservation(root, key, seconds):
    with locked(root / 'budget.lock'):
        path = root / 'budget.json'; data = json.loads(path.read_text())
        # A hard-killed attempt keeps its full reservation; never silently refund it.
        data[key] = seconds
        atomic(path, data)


def executable(name):
    path = shutil.which(name)
    if path is None:
        raise FileNotFoundError(f'required executable unavailable: {name}')
    return str(Path(path).resolve())


def sources():
    paths = [Path(__file__), Path(pilot.__file__), QUEUE, ROOT / 'overnight/run_overnight.py',
             ROOT / 'code/omsat.py', ROOT / 'code/omsat_geom.py', ROOT / 'code/omsat_sym.py',
             ROOT / 'code/omsat_validate.py',
             ROOT / 'experiments/E-261101-25-chirotope-first/final_polynomial.py',
             ROOT / 'code/ladder_exact.py', ROOT / 'experiments/E-261101-25-chirotope-first/chirotope_first.py',
             ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/test_encoder.py']
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def unit(spec):
    root = Path(spec['root']); out = Path(spec['out']); index = spec['index']
    if spec.get('control'):  # positive control: convex 9-face map, planes pinned, SAT required; never latches a first SAT
        data = json.loads((HERE / 'control_f9.json').read_text())
        links = {int(k): v for k, v in data['links'].items()}
        tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
        c = pilot.CNF(9); pilot.build(c, pilot.Triangulation(9, tris, links=links, submap=True), pilot.ALL_OPTS)
        c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in pilot.chirotope_from_planes(data['planes']).items()])
        on_sat = None
    else:
        rec = pilot.census(9, 3)['maps'][index]
        pilot.dump(out / 'map.json', rec)
        c = pilot.CNF(9); pilot.build(c, pilot.from_links(rec['links']), pilot.ALL_OPTS)
        on_sat = lambda: latch_sat(root, dict(map_index=index, unit=str(out), name=name))
    name = f'map{index}_plain'
    try:
        r = pilot.solve(c, out, name, spec['solver_cap'], checker_timeout=spec['checker_cap'], solver_gate=lambda: dispatch_gate(root),
                        on_sat=on_sat)
    except DispatchStopped:
        r = dict(status='SKIPPED-STOP')
    r.update(task=name, map_index=index, scope='control: submap formula, planes pinned' if spec.get('control')
             else 'plain uniform embedding formula',
             canonical_sha256=spec.get('canonical_sha256', spec.get('control_sha256')), unit=str(out),
             formula_sha256=hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest())
    atomic(out / 'result.json', r)


def process_stage(out, name, task, payload, first, state, remaining):
    processing = first.setdefault('processing', {})
    attempts = first.setdefault('stage_attempts', {})
    if task not in processing:
        if task in attempts:
            # A killed stage consumes its reserved cap; never rerun it or overwrite its files.
            processing[task] = dict(status='INTERRUPTED', budget_seconds=attempts[task]['budget_seconds'])
        else:
            work = out / (task + '_' + uuid.uuid4().hex); work.mkdir()
            cap = remaining(120)
            attempts[task] = dict(directory=str(work), budget_seconds=cap)
            atomic(state, first)
            processing[task] = pilot.stage(work, name, task, payload, cap)
        atomic(state, first)
    return processing[task]


def process_first_sat(root, remaining):
    path = root / 'first_sat.json'
    if not path.exists():
        return
    with locked(root / 'processing.lock'):
        first = json.loads(path.read_text())
        if first['status'] != 'SAT-PENDING':
            return
        out = Path(first['unit']); name = first['name']; index = first['map_index']
        rec = pilot.census(9, 3)['maps'][index]
        c = pilot.CNF(9); pilot.build(c, pilot.from_links(rec['links']), pilot.ALL_OPTS)
        model = json.loads((out / (name + '.model.json')).read_text())
        if not pilot.model_valid(c.clauses, model):
            raise ValueError('saved first SAT model invalid')
        values = set(model); chi = {q: 1 if v in values else -1 for q, v in c.qvar.items()}
        for task in ('hinge', 'two_stage', 'fp'):
            result = process_stage(out, name, task, pilot.payload(chi, rec['links']), first, path, remaining)
            if result.get('status') == 'ERROR':
                raise RuntimeError('first SAT processing failed: ' + task)
            if result.get('geometry', {}).get('EMBEDDED'):
                candidate = out / (name + '.candidate.json')
                pilot.dump(candidate, dict(planes=result['planes'], links=dict(enumerate(rec['links']))))
                rc = pilot.command([sys.executable, str(ROOT / 'verification/verify_candidate.py'),
                                    str(candidate), '--target', 'S5'], out / (name + '.candidate.log'), remaining(30))
                if rc != 0:
                    raise RuntimeError('candidate failed S5 verifier')
                first['status'] = 'CANDIDATE-NEEDS-REVIEW'; atomic(path, first)
                return
        first['status'] = 'FIRST-SAT-PROCESSED'; atomic(path, first)


def run(args):
    start = time.monotonic()
    shard = args.shard; shards = args.shards
    if args.workers != 1 or not 1 <= shards <= 10 or not 0 <= shard < shards:
        raise ValueError('requires one worker per shard, 1..10 shards and valid shard index')
    out = Path(args.results_dir).resolve(); root = out.parent
    if out.name != str(shard):
        raise ValueError('results-dir must end in the numeric shard index')
    out.mkdir(parents=True, exist_ok=True)
    with locked(root / f'shard{shard}.lock', blocking=False):
        pilot.CADICAL = executable(os.environ.get('CADICAL', 'cadical'))
        pilot.DRAT = executable(os.environ.get('DRAT_TRIM', 'drat-trim'))
        os.environ['CADICAL'] = pilot.CADICAL; os.environ['DRAT_TRIM'] = pilot.DRAT
        global QUEUE, BUDGET_SECONDS, SOLVER_CAP, CHECKER_CAP
        custom = getattr(args, 's5_queue', None) is not None
        if custom:
            QUEUE = Path(args.s5_queue).resolve(); BUDGET_SECONDS = args.s5_budget_seconds
            SOLVER_CAP = args.timeout; CHECKER_CAP = args.s5_checker_timeout
            if not BUDGET_SECONDS or root == HERE / 'results':
                raise ValueError('custom queue needs --s5-budget-seconds and a results dir outside results/')
        queue = load_queue(custom)[:2] if args.s5_pilot else load_queue(custom)
        identity = dict(sources=sources(), queue_sha256=sha(QUEUE), pilot=args.s5_pilot,
                        caps=[SOLVER_CAP, CHECKER_CAP], budget_seconds=BUDGET_SECONDS,
                        cadical_sha256=sha(Path(pilot.CADICAL)), drat_sha256=sha(Path(pilot.DRAT)))
        if root == HERE / 'results':
            inherited = pilot_manifests(root)
            if not inherited or any(json.loads(p.read_text())['status'] != 'SHARD-COMPLETE' for p in inherited):
                raise ValueError('production requires a completed same-path pilot without first SAT or error')
            identity['pilot_manifests_sha256'] = {str(p.relative_to(root)): sha(p) for p in inherited}
        check_identity(root, identity)
        with locked(root / 'dispatch.lock'):
            cohort = root / 'cohort.json'
            old = json.loads(cohort.read_text()) if cohort.exists() else shards
            if old != shards:
                for sibling in root.glob('shard*.lock'):
                    if sibling.name != f'shard{shard}.lock':
                        with locked(sibling, blocking=False):
                            pass
            atomic(cohort, shards)
        todo = list(pending(root, queue, shard, shards))
        if (root / 'stop.json').exists():
            raise RuntimeError('saved failure stop requires review; no automatic retry')
        if not todo and not (root / 'first_sat.json').exists():
            print('no pending units; recorded units skipped', flush=True); return
        if (root / 'first_sat.json').exists():
            if json.loads((root / 'first_sat.json').read_text())['status'] != 'SAT-PENDING':
                print('first SAT already processed; coverage remains stopped', flush=True); return
        allowance = len(todo) * (SOLVER_CAP + CHECKER_CAP) + 960
        key = reserve(root, allowance)
        deadline = start + allowance
        attempt = out / ('attempt_' + uuid.uuid4().hex)
        attempt.mkdir()
        def remaining(cap):
            seconds = min(cap, deadline - time.monotonic())
            if seconds <= 0:
                raise TimeoutError('shard hard deadline exhausted')
            return seconds
        manifest = dict(started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                        commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, timeout=5).strip(),
                        branch=subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True, timeout=5).strip(),
                        dirty=subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True, timeout=5),
                        host=platform.platform(), cpu_count=os.cpu_count(), python=sys.version,
                        shard=shard, shards=shards, workers=1, budget_seconds=allowance,
                        reservation=key, inputs=identity, status='RUNNING',
                        drat_trim_commit=os.environ.get('DRAT_TRIM_COMMIT', 'unknown; binary SHA-256 recorded'))
        atomic(attempt / 'manifest.json', manifest)
        def expired(signum, frame):
            if time.monotonic() >= deadline:
                raise TimeoutError('shard hard monotonic deadline exhausted')
        previous_alarm = signal.signal(signal.SIGALRM, expired)
        signal.setitimer(signal.ITIMER_REAL, 1, 1)
        try:
            pilot.command([sys.executable, '-m', 'pip', 'freeze'], attempt / 'pip-freeze.txt', remaining(20))
            for tool, binary in [('cadical', pilot.CADICAL), ('drat-trim', pilot.DRAT)]:
                pilot.command([binary, '--version'], attempt / (tool + '.version.log'), remaining(5))
            print('controls start', shard, flush=True)
            rc = pilot.command([sys.executable, str(HERE / 'pilot.py'), '--controls-only', '--out',
                                str(attempt / 'controls')], attempt / 'controls.log', remaining(300))
            control = attempt / 'controls/summary.json'
            if rc != 0 or not control.exists() or json.loads(control.read_text())['status'] != 'CONTROLS-PASS':
                raise RuntimeError('required controls failed or exceeded 300 seconds')
            for entry in pending(root, queue, shard, shards):
                index = entry['index']; work = attempt / f'map{index}'; work.mkdir()
                spec = dict(entry, root=str(root), out=str(work), solver_cap=SOLVER_CAP, checker_cap=CHECKER_CAP)
                atomic(work / 'spec.json', spec)
                append_checkpoint(out / 'progress.jsonl', dict(map_index=index, event='START', unit=str(work)))
                print('map', index, f'start, solver {SOLVER_CAP}s checker {CHECKER_CAP}s', flush=True)
                cap = min(SOLVER_CAP + CHECKER_CAP + 60, deadline - time.monotonic() - 360)
                if cap <= 0:
                    raise TimeoutError('first-SAT reserve reached')
                rc = pilot.command([sys.executable, str(Path(__file__)), '--unit', str(work / 'spec.json')],
                                   work / 'unit.log', cap)
                result_path = work / 'result.json'
                if rc != 0 or not result_path.exists():
                    raise RuntimeError(f'map {index} unit failed or hit hard cap; artifacts retained')
                result = json.loads(result_path.read_text())
                append_checkpoint(out / 'results.jsonl', result)
                print('map', index, result['status'], flush=True)
                if entry.get('control') and result['status'] != 'SAT':
                    raise RuntimeError(f'positive control {index} did not return SAT: {result["status"]}')
                if result['status'] not in ('SAT', 'UNSAT-VERIFIED', 'TIMEOUT', 'SKIPPED-STOP'):
                    raise RuntimeError(f'map {index}: {result["status"]}')
            process_first_sat(root, remaining)
            manifest['status'] = 'FIRST-SAT-STOP' if (root / 'first_sat.json').exists() else 'SHARD-COMPLETE'
        except (KeyboardInterrupt, InterruptedError) as exc:
            manifest.update(status='INTERRUPTED', error=repr(exc))
            raise
        except BaseException as exc:
            manifest.update(status='ERROR', error=repr(exc))
            atomic(root / 'stop.json', dict(error=repr(exc), attempt=str(attempt)))
            raise
        finally:
            # Hashes are streamed; CNF and proof files were deleted after their check (PROTOCOL.md §5).
            try:
                manifest['outputs_sha256'] = {str(p.relative_to(attempt)): sha(p) for p in attempt.rglob('*')
                                               if p.is_file() and p != attempt / 'manifest.json'}
            except TimeoutError as exc:
                manifest.update(status='ERROR', error=repr(exc), hashing='INCOMPLETE')
                atomic(root / 'stop.json', dict(error=repr(exc), attempt=str(attempt)))
                raise
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, previous_alarm)
                manifest.update(ended_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                wall_seconds=time.monotonic() - start)
                manifest['core_hours'] = manifest['wall_seconds'] / 3600
                atomic(attempt / 'manifest.json', manifest)
                finish_reservation(root, key, manifest['wall_seconds'])
            print(manifest['status'], 'wall_seconds', round(manifest['wall_seconds'], 3), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--unit', type=Path, required=True)
    unit(json.loads(ap.parse_args().unit.read_text()))
