"""Bounded representation and dart-preserving surgery audits before geometry."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
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


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def reuse_feasibility_controls(out, result, save):
    baseline = HERE / 'results/submap-feasibility-audit'
    assert digest(baseline / 'manifest.json') == '11c8599ce486b981d52810678035d843bbb5ba1502b0e5e0e8fb23f1a4f164af'
    assert digest(baseline / 'feasibility.json') == 'd647563830d257468da5f7b07c5786c6bdd29dff61f11b0929107fd28e624db4'
    recorded = json.loads((baseline / 'manifest.json').read_text())
    current = json.loads((out / 'manifest.json').read_text())
    for name, expected in recorded['outputs'].items():
        assert digest(baseline / name) == expected, name
    for name, expected in recorded['inputs'].items():
        if name not in {str((HERE / filename).relative_to(ROOT))
                        for filename in ('audit.py', 'run.sh', 'PLAN.md')}:
            assert digest(ROOT / name) == expected, name
    for key in ('python', 'executable', 'pip_freeze', 'thread_limits'):
        assert current[key] == recorded[key], key
    for key in ('cadical', 'drat_trim'):
        assert current[key]['sha256'] == recorded[key]['sha256'], key
    previous = json.loads((baseline / 'feasibility.json').read_text())
    assert previous['controls_pass'] and previous['stop_reason'] == 'COMPLETED'
    assert [row['status'] for row in previous['controls']] == ['SAT', 'SAT', 'UNSAT-VERIFIED']
    assert previous['targets'][1]['status'] == 'UNSAT-VERIFIED'
    result.update(controls_pass=True, reused_controls_manifest_sha256=digest(baseline / 'manifest.json'))
    save()
    return previous


def alternative_units(out, deadline, result, save, solve, progress):
    previous = reuse_feasibility_controls(out, result, save)
    census = load_module('alternative_census', CENSUS / 'census.py')
    recovery = load_module('alternative_recovery', HERE / 'recovery.py')
    saved = HERE / 'results/surgery-audit/audit.json.gz'
    assert digest(saved) == '7abf382cf134792b897cdeb9854ddfb75e1444b35b2e0772951534b12f1c2fcc'
    source = next(row for row in json.loads(gzip.decompress(saved.read_bytes()))['rows']
                  if row['name'] == 'mizhaev')
    top = restore(source['levels'][0], census)
    known = restore(source['levels'][1], census)
    exports = json.loads((HERE / 'results/recovery-pilot-oriented/recovery.json').read_text())['exports']['mizhaev']
    assert recovery.export_level(source['levels'][0], 8, 3, census, sys.modules[__name__])['links'] == {
        int(k): v for k, v in exports[3]['links'].items()}
    assert recovery.export_level(source['levels'][1], 8, 2, census, sys.modules[__name__])['links'] == {
        int(k): v for k, v in exports[2]['links'].items()}
    known_code = known.canon()[0]
    if not result.get('enumeration_finalized'):
        progress('enumeration', 'start')
        enum_started = time.monotonic()
        enum_deadline = min(deadline, enum_started + 20)
        old_queue = result.get('queue', [])
        old_counts = {key: result.get(key, 0) for key in ('patches_tested', 'valid_patches')}
        queue, by_code = [], {}
        tested = valid = 0
        complete = False
        try:
            for selected in patches(top, enum_deadline):
                tested += 1
                caps = patch_caps(top, selected)
                if caps is None:
                    continue
                child, step = remove_patch(top, selected, caps, census)
                try:
                    check_surface(snapshot(child), 8, 2)
                except AssertionError:
                    continue
                check_step(snapshot(top), snapshot(child), step, 8, 3)
                assert snapshot(reverse_step(child, step, census)) == snapshot(top)
                code = child.canon()[0]
                key = hashlib.sha256(json.dumps(code, separators=(',', ':')).encode()).hexdigest()
                valid += 1
                if key in by_code:
                    by_code[key]['multiplicity'] += 1
                    continue
                level = recovery.export_level(snapshot(child), 8, 2, census, sys.modules[__name__])
                row = dict(key=key, canonical_code=code, labelled_map=snapshot(child),
                           step=step, level=level, multiplicity=1, known_unsat=code == known_code)
                if row['known_unsat']:
                    row['known_isomorphism'] = recovery.isomorphism(child, known)
                    row['known_formula'] = previous['targets'][1]
                if len(queue) < len(old_queue):
                    assert key == old_queue[len(queue)]['key'], 'changed enumeration order'
                queue.append(row)
                by_code[key] = row
                result.update(queue=queue + old_queue[len(queue):], patches_tested=tested,
                              valid_patches=valid, enumeration_complete=False)
                save()
            complete = True
        except TimeoutError:
            pass
        if len(queue) < len(old_queue):
            result.update(queue=old_queue, **old_counts, enumeration_complete=False,
                          enumeration_finalized=False, enumeration_ended_by='rebuild_cap',
                          enumeration_seconds=time.monotonic() - enum_started)
            save()
            raise RuntimeError('enumeration rebuild did not validate the full saved prefix')
        if complete:
            assert len(queue) >= len(old_queue), 'lost checkpointed class'
        result.update(queue=queue + old_queue[len(queue):], patches_tested=tested,
                      valid_patches=valid, enumeration_complete=complete,
                      enumeration_finalized=True, enumeration_seconds=time.monotonic() - enum_started,
                      enumeration_budget_seconds=20,
                      enumeration_ended_by='completed' if complete else 'enumeration_cap')
        save()
        progress('enumeration', result['enumeration_ended_by'])
    from omsat import Triangulation
    prefix = [row for row in result['queue'] if not row['known_unsat']][:8]
    result['prefix_keys'] = [row['key'] for row in prefix]
    result.setdefault('targets', [])
    save()
    for index, row in enumerate(prefix):
        if any(unit['key'] == row['key'] for unit in result['targets']):
            continue
        links = {int(k): v for k, v in row['level']['links'].items()}
        triangles = sorted({tuple(sorted((x, a, b))) for x, link in links.items()
                            for a, b in zip(link, link[1:] + link[:1])})
        triangulation = Triangulation(8, triangles, links=links, submap=True)
        stem = f'mizhaev-alt-{index:02d}'
        completed = sorted(out.glob(f'{stem}-try*.result.json'),
                           key=lambda path: int(path.name.split('-try')[1].split('.')[0]))
        if completed:
            path = completed[0]
            decision = json.loads(path.read_text())
            saved_stem = path.name[:-len('.result.json')]
            assert digest(out / f'{saved_stem}.cnf') == decision['cnf_sha256']
            if 'proof_sha256' in decision:
                assert digest(out / f'{saved_stem}.drat') == decision['proof_sha256']
            result['targets'].append(dict(key=row['key'], stem=saved_stem,
                                          recovered_completed_record=True, **decision))
            save()
            if decision['status'] == 'ERROR':
                raise RuntimeError(f'{saved_stem}: ERROR')
            continue
        attempt = 1
        while list(out.glob(f'{stem}-try{attempt}.*')):
            attempt += 1
        decision = solve(f'{stem}-try{attempt}', triangulation, None, 10, 5)
        result['targets'].append(dict(key=row['key'], stem=f'{stem}-try{attempt}', **decision))
        save()
        if decision['status'] == 'ERROR':
            raise RuntimeError(f'{stem}: ERROR')
    result.update(tested_prefix_complete=True, stop_reason='COMPLETED')
    save()
    return 0


def descendant_units(out, deadline, result, save, solve, progress):
    reuse_feasibility_controls(out, result, save)
    baseline = HERE / 'results/mizhaev-first-step-audit'
    pinned = {
        'manifest.json': '2aec3c82e688520992d6c94c594e384628b2339afc9ecc56232f855a7cef585c',
        'alternatives.json': 'b5ae33fe7e016b2baa0d7d6c795797225e0cd8565a0aa4d54eae9bfe5abfef0f',
        'mizhaev-alt-00-try1.model.json': '9c13c565f88d897b40c2a78f9fb96dc2bab144a0be0a54917c2938cdf5ec5fb4',
        'mizhaev-alt-00-try1.result.json': 'e8f4e06a3ad702cfc4b63f27f7f0776daa4338a6c79bbc1d06cc973d78d5323b',
    }
    for filename, expected in pinned.items():
        assert digest(baseline / filename) == expected, filename
    recorded = json.loads((baseline / 'manifest.json').read_text())
    for filename, expected in recorded['outputs'].items():
        assert digest(baseline / filename) == expected, filename
    for filename, expected in recorded['inputs'].items():
        if filename not in {str((HERE / name).relative_to(ROOT))
                            for name in ('audit.py', 'run.sh', 'PLAN.md')}:
            assert digest(ROOT / filename) == expected, filename
    previous = json.loads((baseline / 'alternatives.json').read_text())
    key = 'cfcddf639ecbc6e834985732af94405b24abc80bbed425feb03830349bf3dd3c'
    source = next(row for row in previous['queue'] if row['key'] == key)
    accepted = next(row for row in previous['targets'] if row['key'] == key)
    assert previous['enumeration_complete'] and accepted['status'] == 'SAT' and accepted['model_checked']
    assert digest(baseline / (accepted['stem'] + '.cnf')) == accepted['cnf_sha256']
    census = load_module('descendant_census', CENSUS / 'census.py')
    recovery = load_module('descendant_recovery', HERE / 'recovery.py')
    surgery = json.loads(gzip.decompress((HERE / 'results/surgery-audit/audit.json.gz').read_bytes()))
    old = next(row for row in surgery['rows'] if row['name'] == 'mizhaev')
    top, parent = restore(old['levels'][0], census), restore(source['labelled_map'], census)
    check_step(snapshot(top), snapshot(parent), source['step'], 8, 3)
    assert snapshot(reverse_step(parent, source['step'], census)) == snapshot(top)
    exported = recovery.export_level(snapshot(parent), 8, 2, census, sys.modules[__name__])
    assert json.loads(json.dumps(exported)) == source['level']
    recovery_saved = json.loads((HERE / 'results/recovery-pilot-oriented/recovery.json').read_text())
    published = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())
    links = published['links_0based']
    links = {int(k): v for k, v in links.items()} if isinstance(links, dict) else dict(enumerate(links))
    coherent = census.review.coherent(links)
    reference = census.from_links([coherent[v] for v in range(8)])
    reference.tail = [v for v in range(8) for _ in coherent[v]]
    alignment = recovery.isomorphism(top, reference)
    assert json.loads(json.dumps(alignment)) == next(
        row['alignment'] for row in recovery_saved['controls'] if row['name'] == 'mizhaev')
    result.update(parent_key=key, parent_sat=accepted, published_top_alignment=alignment)
    save()
    if result.get('chain_pass'):
        result['stop_reason'] = 'CHAIN-PASS'
        save()
        return 0
    if not result.get('enumeration_finalized'):
        started = time.monotonic()
        enum_deadline = min(deadline, started + 20)
        old_queue = result.get('queue', [])
        old_counts = {key: result.get(key, 0) for key in ('patches_tested', 'valid_patches')}
        queue, by_key = [], {}
        tested = valid = 0
        complete = False
        try:
            for selected in patches(parent, enum_deadline):
                tested += 1
                caps = patch_caps(parent, selected)
                if caps is None:
                    continue
                child, step = remove_patch(parent, selected, caps, census)
                try:
                    check_surface(snapshot(child), 8, 1)
                except AssertionError:
                    continue
                check_step(snapshot(parent), snapshot(child), step, 8, 2)
                assert snapshot(reverse_step(child, step, census)) == snapshot(parent)
                code = child.canon()[0]
                child_key = hashlib.sha256(json.dumps(code, separators=(',', ':')).encode()).hexdigest()
                valid += 1
                if child_key in by_key:
                    by_key[child_key]['multiplicity'] += 1
                    continue
                row = dict(key=child_key, canonical_code=code, labelled_map=snapshot(child), step=step,
                           level=recovery.export_level(snapshot(child), 8, 1, census, sys.modules[__name__]),
                           multiplicity=1)
                if len(queue) < len(old_queue):
                    assert json.loads(json.dumps(row)) == {**old_queue[len(queue)], 'multiplicity': 1}, 'changed descendant prefix'
                queue.append(row)
                by_key[child_key] = row
                result.update(queue=queue + old_queue[len(queue):], patches_tested=tested,
                              valid_patches=valid, enumeration_complete=False)
                save()
            complete = True
        except TimeoutError:
            pass
        if len(queue) < len(old_queue):
            result.update(queue=old_queue, **old_counts, enumeration_complete=False,
                          enumeration_finalized=False, enumeration_ended_by='rebuild_cap',
                          enumeration_seconds=time.monotonic() - started)
            save()
            raise RuntimeError('descendant rebuild did not validate saved prefix')
        result.update(queue=queue, patches_tested=tested, valid_patches=valid,
                      enumeration_complete=complete, enumeration_finalized=True,
                      enumeration_seconds=time.monotonic() - started,
                      enumeration_ended_by='completed' if complete else 'enumeration_cap')
        save()
    prefix = result['queue'][:8]
    result['prefix_keys'] = [row['key'] for row in prefix]
    result.setdefault('sphere_seconds', 0)
    known = restore(old['levels'][2], census)
    from omsat import Triangulation
    for index, row in enumerate(prefix):
        if time.monotonic() >= deadline:
            raise TimeoutError('registered descendant budget')
        child = restore(row['labelled_map'], census)
        decision = next((unit for unit in result['targets'] if unit['key'] == row['key']), None)
        if decision is None:
            try:
                iso = recovery.isomorphism(child, known, preserve_labels=True)
            except recovery.GateFailure:
                try:
                    iso = recovery.isomorphism(child, known)
                except recovery.GateFailure:
                    iso = None
            if iso is not None:
                decision = dict(key=row['key'], status='SAT-REUSED', isomorphism=iso,
                                evidence='submap-feasibility-audit/mizhaev-positive')
            else:
                links = {int(k): v for k, v in row['level']['links'].items()}
                triangles = sorted({tuple(sorted((x, a, b))) for x, link in links.items()
                                    for a, b in zip(link, link[1:] + link[:1])})
                stem = f'mizhaev-g1-{index:02d}'
                completed = sorted(out.glob(f'{stem}-try*.result.json'))
                if completed:
                    saved_decision = completed[0]
                    unit = json.loads(saved_decision.read_text())
                    stored_stem = saved_decision.name[:-len('.result.json')]
                    assert digest(out / f'{stored_stem}.cnf') == unit['cnf_sha256']
                    if 'proof_sha256' in unit:
                        assert digest(out / f'{stored_stem}.drat') == unit['proof_sha256']
                    decision = dict(key=row['key'], stem=stored_stem, **unit)
                else:
                    attempt = 1
                    while list(out.glob(f'{stem}-try{attempt}.*')):
                        attempt += 1
                    stem = f'{stem}-try{attempt}'
                    unit = solve(stem, Triangulation(8, triangles, links=links, submap=True), None, 10, 5)
                    decision = dict(key=row['key'], stem=stem, **unit)
            result['targets'].append(decision)
            save()
        if decision['status'] == 'ERROR':
            raise RuntimeError('descendant decision ERROR')
        if decision['status'] not in ('SAT', 'SAT-REUSED') or row.get('sphere_complete'):
            continue
        available = min(20 - result['sphere_seconds'], deadline - time.monotonic())
        if available <= 0:
            row['sphere_stop_reason'] = 'sphere_budget'
            save()
            continue
        started = time.monotonic()
        sphere_deadline = started + available
        row['sphere_complete'] = False
        try:
            for selected in patches(child, sphere_deadline):
                caps = patch_caps(child, selected)
                if caps is None:
                    continue
                sphere, step = remove_patch(child, selected, caps, census)
                try:
                    check_surface(snapshot(sphere), 8, 0, simple=True)
                except AssertionError:
                    continue
                check_step(snapshot(child), snapshot(sphere), step, 8, 1)
                assert snapshot(reverse_step(sphere, step, census)) == snapshot(child)
                levels = [snapshot(top), snapshot(parent), snapshot(child), snapshot(sphere)]
                steps = [source['step'], row['step'], step]
                rebuilt = sphere
                for inverse in reversed(steps):
                    rebuilt = reverse_step(rebuilt, inverse, census)
                assert snapshot(rebuilt) == snapshot(top) and rebuilt.canon()[0] == top.canon()[0]
                exports = [recovery.export_level(data, 8, genus, census, sys.modules[__name__])
                           for genus, data in enumerate(reversed(levels))]
                result.update(chain_pass=True, chain=dict(levels=levels, steps=steps, exports=exports,
                              same_labelled_top=True, same_canonical_top=True, genus_one_key=row['key']),
                              stop_reason='CHAIN-PASS')
                row['sphere_stop_reason'] = 'witness'
                break
            else:
                row.update(sphere_complete=True, sphere_stop_reason='exhausted')
        except TimeoutError:
            row['sphere_stop_reason'] = 'sphere_budget'
        finally:
            result['sphere_seconds'] += time.monotonic() - started
            save()
        if result.get('chain_pass'):
            break
    decided = {unit['key']: unit for unit in result['targets']}
    result['unrun_prefix_keys'] = [row['key'] for row in prefix if row['key'] not in decided]
    result['tested_prefix_complete'] = not result['unrun_prefix_keys']
    if not result.get('chain_pass'):
        resolved = (bool(prefix) or result['enumeration_complete']) and all(
                       row['key'] in decided and (decided[row['key']]['status'] == 'UNSAT-VERIFIED'
                       or row.get('sphere_complete', False)) for row in prefix)
        result['stop_reason'] = 'NO-CHAIN-IN-PREFIX' if resolved else 'UNDERPOWERED'
    save()
    progress('descendants', result['stop_reason'])
    return 0


def feasibility_worker(out, deadline, alternatives=False, descendants=False):
    result = dict(scope='two labelled auxiliary maps; uniform rank-4 OM formula only',
                  controls=[], targets=[], controls_pass=False, stop_reason='ERROR')
    if alternatives:
        result['scope'] = 'six-label annular first removals of the frozen labelled Mizhaev top; first eight other classes'
    if descendants:
        result['scope'] = 'genus-one descendants and concrete sphere chain of one frozen OM-SAT Mizhaev genus-two class'
    result_file = out / ('descendants.json' if descendants else 'alternatives.json' if alternatives else 'feasibility.json')
    if (alternatives or descendants) and result_file.exists():
        result = json.loads(result_file.read_text())
        result['stop_reason'] = 'ERROR'

    def save():
        write_json(result_file, result)

    def progress(name, phase):
        with (out / 'progress.jsonl').open('a') as stream:
            stream.write(json.dumps(dict(unit=name, phase=phase,
                                         monotonic=time.monotonic())) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        print(f'{name}: {phase}', flush=True)

    def remaining(cap):
        seconds = min(cap, deadline - time.monotonic())
        if seconds <= 0:
            raise TimeoutError('registered outer audit budget')
        return seconds

    def command(args, log, timeout):
        # Stay in the worker's process group so its watchdog also stops the solver.
        with log.open('a') as stream:
            try:
                return subprocess.run(args, stdout=stream, stderr=subprocess.STDOUT,
                                      timeout=timeout).returncode
            except subprocess.TimeoutExpired:
                return None

    save()
    try:
        from omsat import Triangulation, CNF, build
        from omsat_validate import ALL_OPTS, eval_all, compare_direct, uniform
        from ladder_exact import verify
        pilot = load_module('feasibility_pilot', HERE.parent /
                            'E-261103-03-s5-exact-decision-8-2-9-3/pilot.py')
        cadical = os.environ.get('CADICAL') or shutil.which('cadical')
        drat = os.environ.get('DRAT_TRIM') or shutil.which('drat-trim')
        assert cadical and drat, 'cadical and drat-trim must be on PATH or explicitly configured'
        saved = HERE / 'results/recovery-pilot-oriented'
        source_manifest = json.loads((saved / 'manifest.json').read_text())
        expected_inputs = {
            'roest_vigh-g0.json': '75607a1793514a6edc9572ccd02e404e37ed336658a80663c54695df8a83967f',
            'mizhaev-g1.json': 'c1446ff315c9369b9d8f541f30afb0481d1008f09d140137e9aa67c11a5d3f7a',
            'roest_vigh-g1.json': 'c26ff6f254c9ff8fab5b58949be71dcdbba76e45de9ea095de084a444b49832b',
            'mizhaev-g2.json': '45d961c197548c94f074400f491dd2b13cd8e604add133d80ada5875d30c1980',
            'recovery.json': '57bf8ce5247aef6cb515f7265375a145d2b9cce554c9d522d013ff3a86e119cd',
        }
        for filename, expected in expected_inputs.items():
            assert digest(saved / filename) == expected, filename
        exports = json.loads((saved / 'recovery.json').read_text())['exports']
        review = HERE / 'results/recovery-review'
        assert digest(review / 'report.json') == '96123d22ee993888d42a6fc29a4619c064987f4621e8c218e9808bccc9e5e573'
        assert digest(review / 'check-saved.txt.gz') == '52c5a7a6b9d52a1a52af86e858967004526678c2b08a978259fdaeee8da9d65c'

        def fixture(filename):
            path = saved / filename
            assert digest(path) == source_manifest['outputs'][filename], filename
            data = json.loads(path.read_text())
            name, genus = filename[:-5].rsplit('-g', 1)
            assert data['links'] == exports[name][int(genus)]['links'], filename
            links = {int(k): list(v) for k, v in data['links'].items()}
            assert sorted(links) == list(range(len(links)))
            triangles = sorted({tuple(sorted((x, a, b))) for x, link in links.items()
                                for a, b in zip(link, link[1:] + link[:1])})
            triangulation = Triangulation(len(links), triangles, links=links, submap=True)
            assert triangulation.link == links
            planes = [[int(round(v * 10 ** 9)) for v in row] for row in data['planes']]
            return triangulation, planes, dict(source_file=filename, source_sha256=digest(path),
                                               links=links, triangles=triangles, scale=10 ** 9,
                                               planes_integer=planes)

        def solve(name, triangulation, chi, solver_cap, checker_cap):
            started = time.monotonic()
            progress(name, 'build')
            c = CNF(triangulation.n)
            build(c, triangulation, ALL_OPTS)
            if chi is not None:
                c.clauses.extend([[c.qvar[s] if value > 0 else -c.qvar[s]]
                                  for s, value in chi.items()])
            cnf = out / f'{name}.cnf'
            proof = out / f'{name}.drat'
            c.dimacs(cnf, comments=[name, 'submap=True; ALL_OPTS; no symmetry or mirror clauses',
                                    'pinned chi' if chi is not None else 'unpinned auxiliary-map formula'])
            seconds = remaining(solver_cap)
            progress(name, 'solve')
            solve_started = time.monotonic()
            rc = command([cadical, str(cnf), str(proof)], out / f'{name}.solver.log', seconds)
            actual = time.monotonic() - solve_started
            row = dict(status='TIMEOUT' if rc is None else 'ERROR', variables=c.nv,
                       clauses=len(c.clauses), pinned=chi is not None, cnf_sha256=digest(cnf),
                       solver_returncode=rc, solver_budget_seconds=seconds, solver_seconds=actual,
                       budget_fraction=actual / seconds,
                       ended_by='solver_timeout' if rc is None else 'completed')
            row['clause_families'] = dict(c.tags)
            if rc == 10:
                model = [int(value) for line in (out / f'{name}.solver.log').read_text().splitlines()
                         if line.startswith('v ') for value in line[2:].split() if int(value)]
                write_json(out / f'{name}.model.json', model)
                stored = [[int(value) for value in line.split()[:-1]]
                          for line in cnf.read_text().splitlines() if line and line[0] not in 'cp']
                assert pilot.model_valid(stored, model), 'invalid saved SAT assignment'
                if chi is not None:
                    assert all((c.qvar[s] in model) == (value > 0) for s, value in chi.items())
                row.update(status='SAT', model_checked=True)
            elif rc == 20:
                seconds = remaining(checker_cap)
                progress(name, 'check_proof')
                check_started = time.monotonic()
                rc_check = command([drat, str(cnf), str(proof)],
                                   out / f'{name}.checker.log', seconds)
                checked = rc_check == 0 and 's VERIFIED' in (out / f'{name}.checker.log').read_text()
                row.update(status='UNSAT-VERIFIED' if checked else 'UNSAT-UNCHECKED',
                           checker_returncode=rc_check, checker_budget_seconds=seconds,
                           checker_seconds=time.monotonic() - check_started,
                           checker_ended_by='checker_timeout' if rc_check is None else 'completed')
                if name == 'roest_vigh-negative':
                    controls_module = load_module('feasibility_encoder_controls', HERE.parent /
                        'E-261103-02-s5-omsat-multi-adjacency-encoder/controls.py')
                    stored = [[int(value) for value in line.split()[:-1]]
                              for line in cnf.read_text().splitlines() if line and line[0] not in 'cp']
                    row['independently_unit_refuted'] = controls_module.unit_refutes(stored)
                    if row['independently_unit_refuted']:
                        (out / f'{name}.rup').write_text('0\n')
                        (out / f'{name}.unit-checker.log').write_text(
                            'VERIFIED: stored DIMACS refuted by independent unit propagation\n')
            if proof.exists():
                row['proof_sha256'] = digest(proof)
            row['wall_seconds'] = time.monotonic() - started
            write_json(out / f'{name}.result.json', row)
            progress(name, row['status'])
            return row

        if descendants:
            return descendant_units(out, deadline, result, save, solve, progress)
        if alternatives:
            return alternative_units(out, deadline, result, save, solve, progress)
        controls = [('roest_vigh-positive', 'roest_vigh-g0.json', True),
                    ('mizhaev-positive', 'mizhaev-g1.json', True),
                    ('roest_vigh-negative', 'roest_vigh-g1.json', False)]
        for name, filename, expected in controls:
            progress(name, 'control_geometry')
            triangulation, planes, provenance = fixture(filename)
            chi, evaluation = eval_all(planes, triangulation)
            assert uniform(chi), f'{name}: nonuniform fixed fixture'
            exact = verify(planes, triangulation.link, require_all_pairs=False)
            assert bool(exact['EMBEDDED']) == expected, f'{name}: unexpected exact geometry'
            assert bool(evaluation.violations) != expected, f'{name}: unexpected Eval clauses'
            stats = {}
            mismatches, embedded, simple = compare_direct(planes, triangulation, evaluation, stats)
            assert not mismatches and embedded == expected, name
            if expected:
                assert all(simple), name
            provenance.update(exact=exact, eval_violations=list(evaluation.violations),
                              direct_geometry=dict(mismatches=mismatches, embedded=embedded,
                                                   simple_faces=simple, predicate_counts=stats),
                              chi=[dict(elements=list(s), value=v) for s, v in chi.items()])
            write_json(out / f'{name}.fixture.json', provenance)
            row = solve(name, triangulation, chi, 10, 10)
            result['controls'].append(dict(name=name, **row))
            save()
            assert row['status'] == ('SAT' if expected else 'UNSAT-VERIFIED'), name
        result['controls_pass'] = True
        save()
        for name, filename in [('roest_vigh-target', 'roest_vigh-g1.json'),
                               ('mizhaev-target', 'mizhaev-g2.json')]:
            triangulation, _, provenance = fixture(filename)
            write_json(out / f'{name}.fixture.json', provenance)
            row = solve(name, triangulation, None, 45, 15)
            result['targets'].append(dict(name=name, **row))
            save()
            if row['status'] == 'ERROR':
                raise RuntimeError(f'{name}: {row["status"]}')
        result['stop_reason'] = 'COMPLETED'
        return 0
    except Exception as error:
        result.update(stop_reason='OUTER-TIMEOUT' if isinstance(error, TimeoutError) else
                      'CONTROL-FAIL' if not result['controls_pass'] else 'ERROR',
                      error=f'{type(error).__name__}: {error}')
        return 1
    finally:
        save()


def feasibility(out, alternatives=False, descendants=False):
    resumable = alternatives or descendants
    out.mkdir(parents=True, exist_ok=resumable)
    if resumable and (out / 'manifest.json').exists():
        attempt = 1
        while (out / f'manifest-{attempt}.json').exists():
            attempt += 1
        (out / 'manifest.json').replace(out / f'manifest-{attempt}.json')
    started = time.monotonic()
    manifest = dict(started_utc=datetime.now(timezone.utc).isoformat(), workers=1,
                    stage='descendants' if descendants else 'alternatives' if alternatives else 'feasibility',
                    wall_budget_seconds=180, finalization_reserve_seconds=3,
                    python=sys.version, executable=sys.executable, host=platform.platform(),
                    cpu_count=os.cpu_count(), virtual_env=os.environ.get('VIRTUAL_ENV'),
                    parameters=dict(submap=True, options=dict(gp=True, triples=True, inconsist=True,
                                    reflex=True, reflexconsist=True, poc=True), scale=10 ** 9,
                                    positive_solver_seconds=10, negative_solver_seconds=10,
                                    negative_checker_seconds=10, target_solver_seconds=45,
                                    target_checker_seconds=15, symmetry=False, mirror=False),
                    thread_limits={key: os.environ.get(key) for key in
                                   ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                                    'VECLIB_MAXIMUM_THREADS', 'NUMBA_NUM_THREADS')})
    if resumable:
        manifest['parameters'].update(enumeration_seconds=20, prefix_classes=8,
                                      target_solver_seconds=10, target_checker_seconds=5,
                                      controls='reused unchanged recorded evidence')
    if descendants:
        manifest['parameters']['sphere_seconds'] = 20
    status = 1
    try:
        for key, command in (
            ('commit', ['git', 'rev-parse', 'HEAD']),
            ('branch', ['git', 'branch', '--show-current']),
            ('dirty', ['git', 'status', '--porcelain']),
            ('pip_freeze', [sys.executable, '-m', 'pip', 'freeze']),
        ):
            manifest[key] = subprocess.check_output(command, cwd=ROOT, text=True,
                                                    timeout=min(10, max(.001, 177 - (time.monotonic() - started)))).strip()
        paths = [Path(__file__), HERE / 'run.sh', HERE / 'PLAN.md',
                 ROOT / 'code/omsat.py', ROOT / 'code/omsat_validate.py',
                 ROOT / 'code/omsat_geom.py', ROOT / 'code/ladder_exact.py',
                 HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3/pilot.py',
                 HERE.parent / 'E-261103-02-s5-omsat-multi-adjacency-encoder/controls.py']
        saved = HERE / 'results/recovery-pilot-oriented'
        paths.extend(saved / filename for filename in ('manifest.json', 'roest_vigh-g0.json',
                     'mizhaev-g1.json', 'roest_vigh-g1.json', 'mizhaev-g2.json', 'recovery.json'))
        paths.extend(HERE / 'results/recovery-review' / filename for filename in
                     ('report.json', 'check-saved.txt.gz'))
        if resumable:
            paths.extend([HERE / 'recovery.py', CENSUS / 'census.py',
                          ROOT / 'reviews/strategy-review-2026-11-03-flipwalk.py',
                          HERE / 'results/surgery-audit/audit.json.gz',
                          HERE / 'results/submap-feasibility-audit/manifest.json',
                          HERE / 'results/submap-feasibility-audit/feasibility.json'])
        if descendants:
            paths.append(ROOT / 'literature/mizhaev2026-planes.json')
            paths.extend(HERE / 'results/mizhaev-first-step-audit' / filename for filename in
                         ('manifest.json', 'alternatives.json', 'mizhaev-alt-00-try1.model.json',
                          'mizhaev-alt-00-try1.result.json'))
        manifest['inputs'] = {str(path.relative_to(ROOT)): digest(path) for path in paths}
        for key, executable in [('cadical', os.environ.get('CADICAL') or shutil.which('cadical')),
                                ('drat_trim', os.environ.get('DRAT_TRIM') or shutil.which('drat-trim'))]:
            assert executable, f'{key} is unavailable'
            manifest[key] = dict(executable=executable, sha256=digest(Path(executable)))
            if key == 'cadical':
                manifest[key]['version'] = subprocess.check_output([executable, '--version'], text=True, timeout=5).strip()
            else:
                manifest[key]['source_commit'] = os.environ.get('DRAT_TRIM_COMMIT', 'UNKNOWN')
        write_json(out / 'manifest.json', manifest)
        with (out / 'stdout.txt').open('a') as stdout, (out / 'stderr.txt').open('a') as stderr:
            command = [sys.executable, str(Path(__file__).resolve()),
                       '--feasibility-worker', str(out), '--deadline', str(started + 177)]
            if alternatives:
                command.append('--alternatives')
            if descendants:
                command.append('--descendants')
            process = subprocess.Popen(command,
                                       stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                status = process.wait(timeout=max(.001, 177 - (time.monotonic() - started)))
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=1)
                manifest['outer_timeout'] = True
                status = 124
    except Exception as error:
        manifest['error'] = f'{type(error).__name__}: {error}'
    finally:
        elapsed = time.monotonic() - started
        result_file = out / ('descendants.json' if descendants else 'alternatives.json' if alternatives else 'feasibility.json')
        if manifest.get('outer_timeout') and result_file.exists():
            result = json.loads(result_file.read_text())
            result['stop_reason'] = 'OUTER-TIMEOUT'
            write_json(result_file, result)
        manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(), exit_status=status,
                        wall_seconds=elapsed, core_hours=elapsed / 3600,
                        budget_fraction=elapsed / 180,
                        ended_by='outer_timeout' if manifest.get('outer_timeout') else
                        'error' if 'error' in manifest else 'completed')
        if resumable:
            manifest['cumulative_core_hours'] = elapsed / 3600 + sum(
                json.loads(path.read_text())['core_hours'] for path in out.glob('manifest-*.json'))
        manifest['outputs'] = {path.name: digest(path) for path in out.iterdir()
                               if path.is_file() and path.name != 'manifest.json'}
        write_json(out / 'manifest.json', manifest)
    return status


def om_realization(out, continuation=False):
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    deadline = started + 297
    manifest = dict(stage='om-continuation' if continuation else 'om-realization', started_utc=datetime.now(timezone.utc).isoformat(),
                    workers=1, wall_budget_seconds=300, finalization_reserve_seconds=3,
                    python=sys.version, executable=sys.executable, virtual_env=os.environ.get('VIRTUAL_ENV'),
                    host=platform.platform(), cpu_count=os.cpu_count(), cwd=os.getcwd(),
                    parameters=dict(unit_seconds=10, seed=26110303, integer_scale=10 ** 9,
                                    methods=['hinge', 'two_stage'], starts=['warm', 'unseeded']),
                    thread_limits={key: os.environ.get(key) for key in
                                   ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                                    'VECLIB_MAXIMUM_THREADS', 'NUMBA_NUM_THREADS')}, inputs={})
    result = dict(controls=[], targets=[], bindings=[], controls_pass=False,
                  accepted=[], stop_reason='ERROR', scope='three frozen intermediate OMs; fixed starts and caps')

    def save():
        write_json(out / 'realization.json', result)

    def remaining(cap):
        value = min(cap, deadline - time.monotonic())
        if value <= 0:
            raise TimeoutError('registered realization work deadline')
        return value

    def run_command(command, log, cap):
        seconds = remaining(cap)
        begin = time.monotonic()
        with log.open('w') as stream:
            process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT,
                                       start_new_session=True)
            try:
                rc = process.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                rc = None
            finally:
                # Reap the whole group even if a worker exits before its descendants.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
        return rc, dict(seconds=time.monotonic() - begin, budget_seconds=seconds,
                        ended_by='unit_timeout' if rc is None else 'completed')

    def expired(signum, frame):
        raise TimeoutError('registered realization work deadline or termination')

    old_alarm = signal.signal(signal.SIGALRM, expired)
    old_term = signal.signal(signal.SIGTERM, expired)
    signal.setitimer(signal.ITIMER_REAL, remaining(297))
    status = 1
    save()
    try:
        for key, command in (('commit', ['git', 'rev-parse', 'HEAD']),
                             ('branch', ['git', 'branch', '--show-current']),
                             ('dirty', ['git', 'status', '--porcelain']),
                             ('pip_freeze', [sys.executable, '-m', 'pip', 'freeze'])):
            manifest[key] = subprocess.check_output(command, cwd=ROOT, text=True,
                                                    timeout=remaining(10)).strip()
        baseline_names = [
            ('submap-feasibility-audit', '11c8599ce486b981d52810678035d843bbb5ba1502b0e5e0e8fb23f1a4f164af'),
            ('mizhaev-first-step-audit', '2aec3c82e688520992d6c94c594e384628b2339afc9ecc56232f855a7cef585c'),
            ('mizhaev-descendant-audit', 'cfa6cabad2397840456f949f13d545349d34c1553c3eea5403da546ed136dd1d')]
        baselines = {}
        for name, expected in baseline_names:
            folder = HERE / 'results' / name
            assert digest(folder / 'manifest.json') == expected, name
            recorded = json.loads((folder / 'manifest.json').read_text())
            assert recorded['exit_status'] == 0, name
            for filename, checksum in recorded['outputs'].items():
                path = folder / filename
                assert digest(path) == checksum, path
                manifest['inputs'][str(path.relative_to(ROOT))] = checksum
            manifest['inputs'][str((folder / 'manifest.json').relative_to(ROOT))] = expected
            baselines[name] = recorded
        exceptions = {str((HERE / filename).relative_to(ROOT))
                      for filename in ('audit.py', 'run.sh', 'PLAN.md')}
        manifest['historical_source_exceptions'] = sorted(exceptions)
        latest = baselines['mizhaev-descendant-audit']
        for filename, checksum in latest['inputs'].items():
            if filename not in exceptions:
                assert digest(ROOT / filename) == checksum, filename
                manifest['inputs'][filename] = checksum
        for key in ('python', 'executable', 'pip_freeze', 'thread_limits'):
            assert manifest[key] == latest[key], key
        for path in [Path(__file__), HERE / 'run.sh', HERE / 'PLAN.md',
                     ROOT / 'verification/verify_candidate.py', ROOT / 'code/control_rost_vigh.py',
                     HERE.parent / 'E-261101-25-chirotope-first/chirotope_first.py',
                     HERE / 'results/recovery-review/independent.py']:
            manifest['inputs'][str(path.relative_to(ROOT))] = digest(path)
        write_json(out / 'manifest.json', manifest)
        pilot = load_module('realization_pilot', HERE.parent /
                            'E-261103-03-s5-exact-decision-8-2-9-3/pilot.py')
        from omsat import Triangulation, CNF, build, chirotope_from_planes
        from omsat_validate import ALL_OPTS
        from ladder_exact import verify
        from control_rost_vigh import build as roest_build
        old = json.loads((HERE / 'results/recovery-pilot-oriented/recovery.json').read_text())
        descendants = json.loads((HERE / 'results/mizhaev-descendant-audit/descendants.json').read_text())
        assert descendants['chain_pass'] and descendants['stop_reason'] == 'CHAIN-PASS'
        assert digest(HERE / 'results/mizhaev-descendant-audit/descendants.json') == \
            'b3421714a16e086ec0eda0fc5ad87bc0e55bc2ea018cfd20aa58f7d8b836aaf1'
        alternatives = json.loads((HERE / 'results/mizhaev-first-step-audit/alternatives.json').read_text())
        top_planes, _ = roest_build()
        published = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())
        tops = dict(roest_vigh=top_planes, mizhaev=published['planes_abcd_zero_form'])
        aligned = {}
        for name, planes in tops.items():
            alignment = next(row['alignment'] for row in old['controls'] if row['name'] == name)
            labels = dict(alignment['labels'])
            assert sorted(labels) == list(range(8)) and sorted(labels.values()) == list(range(8))
            aligned[name] = [[float(v) for v in planes[labels[label]]] for label in range(8)]
            assert verify(aligned[name], {int(k): v for k, v in old['exports'][name][3]['links'].items()})['EMBEDDED']
        units = [
            ('roest_vigh', 1, 'submap-feasibility-audit', 'roest_vigh-target', old['exports']['roest_vigh'][1]),
            ('mizhaev', 1, 'mizhaev-descendant-audit', 'mizhaev-g1-00-try1', descendants['chain']['exports'][1]),
            ('mizhaev', 2, 'mizhaev-first-step-audit', 'mizhaev-alt-00-try1', descendants['chain']['exports'][2])]
        prepared = []
        for name, genus, folder, stem, level in units:
            links = {int(k): v for k, v in level['links'].items()}
            if name == 'mizhaev':
                source = descendants if genus == 1 else alternatives
                decision = next(row for row in source['targets'] if row['stem'] == stem)
                queued = next(row for row in source['queue'] if row['key'] == decision['key'])
                assert queued['level']['links'] == level['links']
            triangles = sorted({tuple(sorted((x, a, b))) for x, link in links.items()
                                for a, b in zip(link, link[1:] + link[:1])})
            c = CNF(8)
            build(c, Triangulation(8, triangles, links=links, submap=True), ALL_OPTS)
            saved = HERE / 'results' / folder
            data = json.loads((saved / (stem + '.result.json')).read_text())
            assert data['status'] == 'SAT' and data['model_checked']
            stored = []
            for line in (saved / (stem + '.cnf')).read_text().splitlines():
                if line.startswith('p '):
                    assert list(map(int, line.split()[2:])) == [c.nv, len(c.clauses)]
                elif line and not line.startswith('c'):
                    values = list(map(int, line.split()))
                    assert values[-1] == 0
                    stored.append(values[:-1])
            assert stored == c.clauses, stem
            model = json.loads((saved / (stem + '.model.json')).read_text())
            assert {abs(v) for v in model} == set(range(1, c.nv + 1)) and len(model) == c.nv
            assert pilot.model_valid(stored, model), stem
            assignment = set(model)
            chi = {q: 1 if var in assignment else -1 for q, var in c.qvar.items()}
            assert len(chi) == 126 and all(chi.values())
            result['bindings'].append(dict(name=f'{name}-g{genus}', cnf_sha256=digest(saved / (stem + '.cnf')),
                                           model_sha256=digest(saved / (stem + '.model.json')),
                                           clauses_match=True, model_checked=True, signs=len(chi)))
            prepared.append((name, genus, level, chi))
            save()

        def attempt(stem, method, chi, level, start):
            inp, op = out / (stem + '.input.json'), out / (stem + '.output.json')
            write_json(inp, pilot.payload(chi, [level['links'][str(v)] for v in range(8)], start))
            rc, timing = run_command([sys.executable, str(Path(pilot.__file__)), '--task', method,
                                      '--input', str(inp), '--output', str(op)], out / (stem + '.log'), 10)
            row = json.loads(op.read_text()) if rc == 0 else dict(status='TIMEOUT' if rc is None else 'ERROR')
            row.update(name=stem, method=method, warm=start is not None, **timing)
            row['budget_fraction'] = row['seconds'] / row['budget_seconds']
            if rc not in (0, None):
                raise RuntimeError(f'realizer worker failed: {stem}; returncode={rc}')
            if row.get('signs_match'):
                # The shared worker requires all pairs; intermediate maps do not.
                row['worker_geometry'] = row['geometry']
                row['geometry'] = json.loads(json.dumps(verify(
                    row['planes'], {int(k): v for k, v in level['links'].items()}, require_all_pairs=False)))
            row['accepted'] = bool(row.get('signs_match') and row.get('geometry', {}).get('EMBEDDED')
                                   and row['geometry']['V_E_F_chi'] == level['expected_topology'])
            if row.get('signs_match') and not row['accepted']:
                raise ArithmeticError(f'sign reconstruction disagrees with geometry: {stem}')
            print(f'{stem}: wrong={row.get("wrong_signs")} accepted={row["accepted"]} {row["ended_by"]}', flush=True)
            return row

        for name in tops:
            level = old['exports'][name][3]
            h = [[int(round(v * 10 ** 9)) for v in plane] for plane in aligned[name]]
            chi = chirotope_from_planes(h)
            assert all(chi.values())
            for method in ('hinge', 'two_stage'):
                for warm in (True, False):
                    stem = f'control-{name}-{method}-{"warm" if warm else "unseeded"}'
                    row = attempt(stem, method, chi, level, aligned[name] if warm else None)
                    result['controls'].append(row)
                    save()
                    if warm and not row['accepted']:
                        result['stop_reason'] = 'UNDERPOWERED/CONTROL-FAIL'
                        return 0
            flipped = dict(chi)
            q = next(iter(flipped))
            flipped[q] *= -1
            assert not pilot.reconstruction_ok(0, chirotope_from_planes(h) == flipped)
        rejected = json.loads((HERE / 'results/recovery-pilot-oriented/roest_vigh-g1.json').read_text())
        assert not verify(rejected['planes'], {int(k): v for k, v in rejected['links'].items()},
                          require_all_pairs=False)['EMBEDDED']
        result.update(controls_pass=True, negative_sign_control='REJECTED', negative_geometry_control='REJECTED',
                      construction_power={method: 'CONTROL-PASS' if all(row['accepted'] for row in result['controls']
                                          if row['method'] == method and not row['warm']) else 'UNDERPOWERED'
                                          for method in ('hinge', 'two_stage')})
        save()
        if continuation:
            # Roest-Vigh g1 was accepted in intermediate-om-realization-review; realize each Mizhaev map once.
            prepared = [unit for unit in prepared if unit[0] == 'mizhaev']
            result['scope'] = 'alternative Mizhaev g1/g2 saved OMs; first acceptance per map'
        for name, genus, level, chi in prepared:
            for method, warm in ((m, w) for m in ('hinge', 'two_stage') for w in (True, False)):
                stem = f'{name}-g{genus}-{method}-{"warm" if warm else "unseeded"}'
                row = attempt(stem, method, chi, level, aligned[name] if warm else None)
                result['targets'].append(row)
                save()
                if row['accepted']:
                    candidate = dict(planes=row['planes'], links=level['links'])
                    path = out / (stem + '.candidate.json')
                    write_json(path, candidate)
                    row['candidate'] = path.name
                    row['review_status'] = 'UNVERIFIED'
                    save()
                    rc, timing = run_command([sys.executable, str(ROOT / 'verification/verify_candidate.py'),
                                              str(path)], out / (stem + '.verify.log'), remaining(30))
                    assert rc == 0, f'candidate verifier rejected {stem}'
                    independent = load_module('realization_independent', HERE / 'results/recovery-review/independent.py')
                    import numpy as np
                    h = np.asarray(row['planes'], dtype=float)
                    h /= np.linalg.norm(h[:, :3], axis=1)[:, None]
                    reports = {'original': independent.check(candidate, level['expected_topology'])}
                    for scale in (10 ** 9, 10 ** 12):
                        rounded = [[int(round(float(v) * scale)) for v in plane] for plane in h]
                        assert chirotope_from_planes(rounded) == chi
                        reports[str(scale)] = independent.check(dict(planes=rounded, links=level['links']),
                                                                 level['expected_topology'])
                    write_json(out / (stem + '.independent.json'), json.loads(json.dumps(reports, default=str)))
                    row.update(review_status='AGENT-REVIEW-PENDING', verifier_timing=timing,
                               robustness='integer-rescaling; optimizer output is already rounded at 1e-9')
                    result['accepted'].append(path.name)
                    result['stop_reason'] = 'CANDIDATE-REVIEW'
                    save()
                    if not continuation:
                        return 0
                    break
        if result['accepted']:
            status = 0
            return 0
        result['stop_reason'] = 'NO-RECOVERY-IN-QUEUE'
        status = 0
    except Exception as error:
        result.update(stop_reason='TIMEOUT' if isinstance(error, TimeoutError) else 'ERROR',
                      error=f'{type(error).__name__}: {error}')
        print(result['error'], file=sys.stderr, flush=True)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_alarm)
        signal.signal(signal.SIGTERM, old_term)
        save()
        elapsed = time.monotonic() - started
        # Successful early stops return zero as well as recording a successful manifest.
        status = 0 if result['stop_reason'] in ('CANDIDATE-REVIEW', 'UNDERPOWERED/CONTROL-FAIL',
                                               'NO-RECOVERY-IN-QUEUE') else status
        manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(), exit_status=status,
                        wall_seconds=elapsed, core_hours=elapsed / 3600, budget_fraction=elapsed / 300,
                        ended_by=result['stop_reason'], outputs={p.name: digest(p) for p in out.iterdir()
                                                               if p.is_file() and p.name != 'manifest.json'})
        write_json(out / 'manifest.json', manifest)
    return status


def snapshot(m):
    triangles = []
    for triangle in m.tri:
        i = triangle.index(min(triangle))
        triangles.append(triangle[i:] + triangle[:i])
    return dict(triangles=sorted(triangles),
                alpha=[[d, m.alpha[d]] for d in sorted(m.pos)],
                tail=[[d, m.tail[d]] for d in sorted(m.pos)])


def restore(data, census):
    tails = dict(data['tail'])
    tail = [0] * (max(tails) + 1)
    for d, label in tails.items():
        tail[d] = label
    return census.review.TriMap(data['triangles'], dict(data['alpha']), tail)


def check_surface(data, n, genus, simple=False):
    """Direct permutation check, independent of TriMap's traversal methods."""
    triangles = data['triangles']
    darts = [d for triangle in triangles for d in triangle]
    live = set(darts)
    assert all(len(t) == 3 for t in triangles), 'triangle size'
    assert len(darts) == len(live), 'repeated dart'
    alpha, tail = dict(data['alpha']), dict(data['tail'])
    assert len(alpha) == len(data['alpha']) and set(alpha) == live, 'alpha domain'
    assert len(tail) == len(data['tail']) and set(tail) == live, 'tail domain'
    assert all(alpha[d] in live and alpha[d] != d and alpha[alpha[d]] == d
               for d in live), 'alpha involution'
    nxt, prev = {}, {}
    for a, b, c in triangles:
        nxt.update({a: b, b: c, c: a})
        prev.update({b: a, c: b, a: c})
    assert all(tail[alpha[d]] == tail[nxt[d]]
               and tail[nxt[alpha[d]]] == tail[d] for d in live), 'endpoint labels'
    assert set(tail.values()) == set(range(n)), 'label set'
    assert all(tail[d] != tail[nxt[d]] for d in live), 'loop'
    corners = [tuple(sorted(tail[d] for d in t)) for t in triangles]
    assert all(len(set(t)) == 3 for t in corners), 'corner labels'
    assert len(corners) == len(set(corners)), 'repeated corner triple'
    unseen, labels = set(live), []
    while unseen:
        first = min(unseen)
        d, cycle = first, []
        while d in unseen:
            unseen.remove(d)
            cycle.append(d)
            d = alpha[prev[d]]
        assert d == first, 'vertex cycle'
        values = {tail[e] for e in cycle}
        assert len(values) == 1, 'vertex labels'
        labels.append(values.pop())
    assert sorted(labels) == list(range(n)), 'one vertex link per label'
    reached, todo = set(), [min(live)]
    while todo:
        d = todo.pop()
        if d not in reached:
            reached.add(d)
            todo.extend((alpha[d], nxt[d]))
    assert reached == live, 'disconnected surface'
    assert n - len(live) // 2 + len(triangles) == 2 - 2 * genus, 'Euler'
    pairs = Counter(tuple(sorted((tail[d], tail[alpha[d]])))
                    for d in live if d < alpha[d])
    if simple:
        assert all(count == 1 for count in pairs.values()), 'parallel edges'
    return dict(genus=genus, vertices=n, edges=len(live) // 2,
                triangles=len(triangles), adjacent_pairs=len(pairs),
                max_multiplicity=max(pairs.values()))


def patch_caps(m, selected):
    """Identify an annulus by its actual boundary darts and contiguous vertex fans."""
    if len(selected) != 6:
        return None
    patch = {d for t in selected for d in m.tri[t]}
    boundary = sorted(d for d in patch if m.alpha[d] not in patch)
    labels = {m.tail[d] for d in patch}
    if len(labels) != 6 or len(boundary) != 6:
        return None
    by_tail = {m.tail[d]: d for d in boundary}
    if set(by_tail) != labels:
        return None
    reached, todo = set(), [min(selected)]
    while todo:
        t = todo.pop()
        if t not in reached:
            reached.add(t)
            todo.extend(m.pos[m.alpha[d]][0] for d in m.tri[t]
                        if m.alpha[d] in patch)
    if reached != set(selected):
        return None
    internal_edges = sum(m.alpha[d] in patch for d in patch) // 2
    if len(labels) - internal_edges - len(boundary) + len(selected) != 0:
        return None
    for label in labels:
        fan = {d for d in patch if m.tail[d] == label}
        starts = sum(m.alpha[m.prv(d)] not in fan for d in fan)
        if starts != 1:
            return None
    caps, unseen = [], set(boundary)
    while unseen:
        first, cycle = min(unseen), []
        d = first
        while d in unseen:
            unseen.remove(d)
            cycle.append(d)
            d = by_tail.get(m.head(d))
        if d != first or len(cycle) != 3:
            return None
        caps.append(cycle)
    return caps if len(caps) == 2 else None


def patches(m, deadline):
    """Enumerate connected six-triangle subsets without identifying parallel edges."""
    neighbors = [{m.pos[m.alpha[d]][0] for d in t} for t in m.tri]
    for root in range(len(m.tri)):
        todo, seen = [(root,)], set()
        while todo:
            if time.monotonic() >= deadline:
                raise TimeoutError('per-map wall cap')
            chosen = todo.pop()
            if chosen in seen:
                continue
            seen.add(chosen)
            if len({m.tail[d] for t in chosen for d in m.tri[t]}) > 6:
                continue
            if len(chosen) == 6:
                yield chosen
                continue
            border = set().union(*(neighbors[t] for t in chosen)) - set(chosen)
            for t in sorted(border, reverse=True):
                if t > root:
                    todo.append(tuple(sorted((*chosen, t))))


def remove_patch(m, selected, caps, census):
    patch = {d for t in selected for d in m.tri[t]}
    internal = sorted(d for d in patch if m.alpha[d] in patch)
    alpha = {d: a for d, a in m.alpha.items() if d not in internal}
    triangles = [t for i, t in enumerate(m.tri) if i not in selected] + caps
    child = census.review.TriMap(triangles, alpha, m.tail)
    step = dict(removed_triangles=[m.tri[t] for t in selected], caps=caps,
                internal_alpha=[[d, m.alpha[d]] for d in internal],
                internal_tail=[[d, m.tail[d]] for d in internal])
    return child, step


def reverse_step(child, step, census):
    data = snapshot(child)
    cap_sets = {frozenset(t) for t in step['caps']}
    data['triangles'] = [t for t in data['triangles'] if frozenset(t) not in cap_sets]
    data['triangles'].extend(step['removed_triangles'])
    data['alpha'].extend(step['internal_alpha'])
    data['tail'].extend(step['internal_tail'])
    return restore(data, census)


def check_step(before, after, step, n, genus):
    """Check a recorded transition using edge incidence and patch link graphs."""
    check_surface(before, n, genus)
    check_surface(after, n, genus - 1)
    alpha, tail = dict(before['alpha']), dict(before['tail'])
    removed, caps = step['removed_triangles'], step['caps']
    assert len(removed) == 6 and len(caps) == 2, 'patch/cap sizes'
    old_tri = {tuple(t) for t in before['triangles']}
    normalize = lambda t: tuple(t[t.index(min(t)):] + t[:t.index(min(t))])
    gone = {normalize(t) for t in removed}
    assert len(gone) == 6 and gone <= old_tri, 'removed triangle identity'
    assert {tuple(t) for t in after['triangles']} == (old_tri - gone) | {
        normalize(t) for t in caps}, 'outside triangles changed'
    patch = {d for t in removed for d in t}
    internal = {d for d in patch if alpha[d] in patch}
    boundary = patch - internal
    assert set(d for t in caps for d in t) == boundary, 'cap boundary'
    assert len(boundary) == 6, 'boundary size'
    assert dict(step['internal_alpha']) == {d: alpha[d] for d in internal}, 'inverse alpha'
    assert dict(step['internal_tail']) == {d: tail[d] for d in internal}, 'inverse tails'
    assert dict(after['alpha']) == {d: a for d, a in alpha.items() if d not in internal}, 'surviving alpha'
    assert dict(after['tail']) == {d: v for d, v in tail.items() if d not in internal}, 'surviving tails'
    vertices = {tail[d] for d in patch}
    edge = lambda d: min(d, alpha[d])
    assert len(vertices) == 6 and len(vertices) - len({edge(d) for d in patch}) + 6 == 0, 'patch Euler'
    # Each patch vertex has a connected interval as its link, with two boundary ends.
    for v in vertices:
        links = {}
        for triangle in removed:
            for i, d in enumerate(triangle):
                if tail[d] == v:
                    a, b = edge(triangle[i - 1]), edge(d)
                    links.setdefault(a, []).append(b)
                    links.setdefault(b, []).append(a)
        degrees = sorted(map(len, links.values()))
        assert degrees.count(1) == 2 and all(k in (1, 2) for k in degrees), 'patch vertex link degrees'
        reached, todo = set(), [min(links)]
        while todo:
            e = todo.pop()
            if e not in reached:
                reached.add(e)
                todo.extend(links[e])
        assert reached == set(links), 'patch vertex link disconnected'
    cap_labels = [{tail[d] for d in t} for t in caps]
    assert all(len(s) == 3 for s in cap_labels) and not cap_labels[0] & cap_labels[1], 'boundary cycles'
    incident = {d: i for i, t in enumerate(removed) for d in t}
    reached, todo = set(), [0]
    while todo:
        t = todo.pop()
        if t not in reached:
            reached.add(t)
            todo.extend(incident[alpha[d]] for d in removed[t] if alpha[d] in patch)
    assert len(reached) == 6, 'patch disconnected'


def surgery_chain(name, top, n, genus, census, global_deadline):
    started = time.monotonic()
    deadline = min(global_deadline, started + 5)
    row = dict(name=name, n=n, top_genus=genus, status='NO-CHAIN', expanded_states=0, patches_tested=0,
               surgeries=0, levels=[snapshot(top)], steps=[], reached_genus=genus)
    seen = set()

    def descend(m, g, levels, steps):
        if time.monotonic() >= deadline:
            raise TimeoutError('per-map wall cap')
        check_surface(snapshot(m), n, g)
        code = m.canon()[0]
        if code in seen:
            return False
        if row['expanded_states'] == 256:
            row['status'] = 'STATE-CAP'
            return False
        seen.add(code)
        row['expanded_states'] += 1
        if g < row['reached_genus']:
            row.update(levels=levels, steps=steps, reached_genus=g)
        if g == 0:
            try:
                check_surface(snapshot(m), n, 0, simple=True)
            except AssertionError:
                return False
            row.update(status='CHAIN-PASS', levels=levels, steps=steps)
            return True
        for selected in patches(m, deadline):
            row['patches_tested'] += 1
            caps = patch_caps(m, selected)
            if caps is None:
                continue
            child, step = remove_patch(m, selected, caps, census)
            try:
                check_surface(snapshot(child), n, g - 1)
            except AssertionError:
                continue
            row['surgeries'] += 1
            restored = reverse_step(child, step, census)
            assert snapshot(restored) == snapshot(m), 'labelled inverse mismatch'
            assert restored.canon()[0] == code, 'canonical inverse mismatch'
            check_step(snapshot(m), snapshot(child), step, n, g)
            if descend(child, g - 1, levels + [snapshot(child)], steps + [step]):
                return True
            if row['status'] == 'STATE-CAP':
                return False
        return False

    try:
        descend(top, genus, [snapshot(top)], [])
    except TimeoutError as error:
        row.update(status='TIMEOUT', limit=str(error))
    row['wall_seconds'] = time.monotonic() - started
    row['budget_fraction'] = row['wall_seconds'] / 5
    rebuilt = restore(row['levels'][-1], census)
    for step in reversed(row['steps']):
        rebuilt = reverse_step(rebuilt, step, census)
    row['same_labelled_top'] = snapshot(rebuilt) == snapshot(top)
    row['same_canonical_top'] = rebuilt.canon()[0] == top.canon()[0]
    assert row['same_labelled_top'] and row['same_canonical_top'], 'chain inverse'
    return row


def check_saved_surgery(path, census):
    raw = gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes()
    evidence = json.loads(raw)
    expected = {}
    for filename, prefix in (('maps_7_1.json', 'szilassi'), ('maps_9_3.json', 'focus')):
        records = json.loads((CENSUS / 'results' / filename).read_text())['maps']
        for index, record in enumerate(records):
            if record['admissible']:
                name = 'szilassi' if prefix == 'szilassi' else f'focus_{index}'
                expected[name] = census.from_code(record['code'])
    from control_rost_vigh import build
    _, links = build()
    mizhaev = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())['links_0based']
    if isinstance(mizhaev, dict):
        mizhaev = {int(v): neighbors for v, neighbors in mizhaev.items()}
    else:
        mizhaev = dict(enumerate(mizhaev))
    for name, link in (('roest_vigh', links), ('mizhaev', mizhaev)):
        coherent = census.review.coherent(link)
        expected[name] = census.from_links([coherent[v] for v in range(8)])
    names = [row['name'] for row in evidence['rows']]
    assert len(names) == len(set(names)), 'duplicate evidence rows'
    for row in evidence['rows']:
        n, genus = row['n'], row['top_genus']
        levels, steps = row['levels'], row['steps']
        assert len(levels) == len(steps) + 1, 'saved chain length'
        assert row['reached_genus'] == genus - len(steps), 'saved reached genus'
        for index, level in enumerate(levels):
            check_surface(level, n, genus - index,
                          simple=row['status'] == 'CHAIN-PASS' and index == len(steps))
        for index, step in enumerate(steps):
            check_step(levels[index], levels[index + 1], step, n, genus - index)
        top = restore(levels[0], census)
        assert snapshot(top) == snapshot(expected[row['name']]), 'saved input-map identity'
        rebuilt = restore(levels[-1], census)
        for step in reversed(steps):
            rebuilt = reverse_step(rebuilt, step, census)
        assert snapshot(rebuilt) == levels[0], 'saved labelled top'
        assert rebuilt.canon()[0] == top.canon()[0], 'saved canonical top'
        if row['status'] == 'CHAIN-PASS':
            assert row['reached_genus'] == 0, 'saved endpoint genus'
    controls = {'szilassi', 'roest_vigh', 'mizhaev'}
    if evidence['controls_pass']:
        assert controls <= set(names), 'missing control rows'
        assert all(row['status'] == 'CHAIN-PASS' for row in evidence['rows']
                   if row['name'] in controls), 'failed positive control'
        assert evidence['structural_controls'] == dict(
            negative=dict(broken_alpha='alpha involution', wrong_tail='endpoint labels',
                          disconnected_caps='rejected'), legacy_capped_map_match=True), 'structural outcomes'
    if evidence['stop_reason'] == 'COMPLETE':
        assert set(names) == set(expected), 'incomplete saved scope'
        assert evidence['focus_processed'] == len(set(expected) - controls), 'saved focus count'
    return len(names)


def surgery_controls(m, row, census):
    data = snapshot(m)
    negative = {}
    for name in ('broken_alpha', 'wrong_tail'):
        broken = json.loads(json.dumps(data))
        if name == 'broken_alpha':
            broken['alpha'][0][1] = broken['alpha'][0][0]
        else:
            broken['tail'][0][1] = (broken['tail'][0][1] + 1) % 7
        try:
            check_surface(broken, 7, 1)
        except AssertionError as error:
            negative[name] = str(error)
    assert negative.get('broken_alpha') == 'alpha involution', 'alpha negative control'
    assert negative.get('wrong_tail') == 'endpoint labels', 'tail negative control'
    assert row['steps'], 'missing patch control fixture'
    step = row['steps'][0]
    child = restore(row['levels'][1], census)
    cap_sets = {frozenset(t) for t in step['caps']}
    selected = [i for i, t in enumerate(child.tri) if frozenset(t) in cap_sets]
    assert patch_caps(child, selected) is None, 'disconnected caps accepted'
    negative['disconnected_caps'] = 'rejected'
    from tubes import tubes
    from gauss_degree import coherent_triangles, links_from
    triples = [tuple(m.tail[d] for d in t) for t in m.tri]
    target_code = child.canon()[0]
    compatibility = False
    for a, b, removed in tubes(triples, 7):
        remaining = [tuple(sorted(t)) for t in triples]
        for t in removed:
            remaining.remove(tuple(sorted(t)))
        links = links_from(coherent_triangles(remaining + [tuple(a), tuple(b)]), 7)
        recovered = census.from_links([links[v] for v in range(7)])
        if recovered.canon()[0] == target_code:
            compatibility = True
            break
    assert compatibility, 'legacy Szilassi capped-map mismatch'
    return dict(negative=negative, legacy_capped_map_match=compatibility)


def run_surgery(census, result, save, deadline):
    records = json.loads((CENSUS / 'results/maps_7_1.json').read_text())['maps']
    szilassi = next(record for record in records if record['admissible'])
    controls = [('szilassi', census.from_code(szilassi['code']), 7, 1)]
    from control_rost_vigh import build
    _, links = build()
    mizhaev = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())['links_0based']
    if isinstance(mizhaev, dict):
        mizhaev = [mizhaev[str(v)] for v in range(len(mizhaev))]
    for name, link in (('roest_vigh', links), ('mizhaev', mizhaev)):
        coherent = census.review.coherent(dict(enumerate(link)) if isinstance(link, list) else link)
        m = census.from_links([coherent[v] for v in range(8)])
        controls.append((name, m, 8, 3))
    result.update(controls_pass=False, gate_pass=False, focus_processed=0)
    for name, m, n, genus in controls:
        census.review.check(m, n, genus)
        row = surgery_chain(name, m, n, genus, census, deadline)
        result['rows'].append(row)
        save()
        if row['status'] != 'CHAIN-PASS':
            result.update(stop_reason='CONTROL-FAIL', failed_control=name)
            return
        if name == 'szilassi':
            try:
                result['structural_controls'] = surgery_controls(m, row, census)
            except AssertionError as error:
                result.update(stop_reason='CONTROL-FAIL', failed_control='structural', error=str(error))
                return
            save()
    result.update(controls_pass=True, gate_pass=True)
    records = json.loads((CENSUS / 'results/maps_9_3.json').read_text())['maps']
    for index, record in enumerate(records):
        if not record['admissible']:
            continue
        if time.monotonic() >= deadline:
            result['stop_reason'] = 'TIMEOUT'
            return
        m = census.from_code(record['code'])
        census.review.check(m, 9, 3)
        result['rows'].append(surgery_chain(f'focus_{index}', m, 9, 3, census, deadline))
        result['focus_processed'] += 1
        save()
    result['stop_reason'] = 'COMPLETE'


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


def main(out, stage='representation'):
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    budget = 300 if stage == 'surgery' else 120
    manifest = dict(started_utc=datetime.now(timezone.utc).isoformat(), workers=1,
                    host=platform.platform(), cpu_count=os.cpu_count(),
                    python=sys.version, executable=sys.executable,
                    cwd=os.getcwd(), virtual_env=os.environ.get('VIRTUAL_ENV'),
                    parameters=dict(stage=stage, wall_seconds=budget))
    if stage == 'surgery':
        manifest['parameters'].update(per_map_seconds=5, expanded_states=256)
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
    if stage == 'surgery':
        paths.append(ROOT / 'code/tubes.py')
    manifest['inputs'] = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    scope = 'dart-preserving six-triangle surgery' if stage == 'surgery' else 'legacy triangle-to-links round-trip only'
    result = dict(rows=[], scope=scope)

    def save():
        (out / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')

    def expired(signum, frame):
        raise TimeoutError(f'registered {budget}-second audit budget')

    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, max(0.001, budget - (time.monotonic() - started)))
    try:
        census = load_module('s5_census', CENSUS / 'census.py')
        if stage == 'surgery':
            run_surgery(census, result, save, started + budget)
            save()
            check_saved_surgery(out / 'audit.json', census)
            result['saved_evidence_check'] = 'PASS'
            manifest['exit_status'] = 0
            print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))
            return
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
        if stage == 'surgery':
            result.update(gate_pass=False, error_type=type(error).__name__,
                          stop_reason='TIMEOUT' if isinstance(error, TimeoutError) else 'ERROR')
        manifest['exit_status'] = 1
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
        save()
        elapsed = time.monotonic() - started
        manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(),
                        wall_seconds=elapsed, core_hours=elapsed / 3600,
                        budget_fraction=elapsed / budget,
                        outputs={'audit.json': digest(out / 'audit.json')})
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--out', type=Path)
    mode.add_argument('--check-saved', type=Path)
    mode.add_argument('--feasibility-worker', type=Path)
    parser.add_argument('--alternatives', action='store_true')
    parser.add_argument('--descendants', action='store_true')
    parser.add_argument('--deadline', type=float)
    parser.add_argument('--stage', choices=('representation', 'surgery', 'feasibility', 'alternatives', 'descendants', 'om-realization', 'om-continuation'), default='representation')
    args = parser.parse_args()
    if args.feasibility_worker:
        if args.deadline is None:
            parser.error('--feasibility-worker requires --deadline')
        sys.exit(feasibility_worker(args.feasibility_worker, args.deadline, args.alternatives, args.descendants))
    elif args.check_saved:
        census = load_module('s5_census', CENSUS / 'census.py')
        count = check_saved_surgery(args.check_saved, census)
        print(f'PASS: {count} saved maps, source identities, surface/patch checks and reversible chains')
    elif args.stage in ('om-realization', 'om-continuation'):
        sys.exit(om_realization(args.out.resolve(), args.stage == 'om-continuation'))
    elif args.stage in ('feasibility', 'alternatives', 'descendants'):
        sys.exit(feasibility(args.out.resolve(), args.stage == 'alternatives', args.stage == 'descendants'))
    else:
        main(args.out, args.stage)
