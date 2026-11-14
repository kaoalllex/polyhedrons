"""Coverage scheduling and failure-path controls; no focus-map solver calls."""
import json
from pathlib import Path
import tempfile
import unittest
import sys
from unittest.mock import patch
import pilot


class TrancheTests(unittest.TestCase):
    def module(self):
        import tranche
        return tranche

    def test_queue_excludes_attempted_tail_and_detects_input_drift(self):
        t = self.module()
        queue = t.load_queue()
        self.assertEqual(len(queue), 80)
        self.assertEqual([r['index'] for r in queue[:4]], [8, 9, 11, 12])
        self.assertFalse({0, 1, 2, 3, 4, 5, 6, 7, 10, 30, 40, 48} & {r['index'] for r in queue})
        with patch.object(t, 'sha', return_value='changed'):
            with self.assertRaises(ValueError):
                t.load_queue()

    def test_torn_tail_is_repaired_but_interior_corruption_blocks_resume(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'results.jsonl'
            prefix = b'{ "map_index":8, "status":"TIMEOUT" }\n'
            path.write_bytes(prefix + b'{"map_')
            t.append_checkpoint(path, dict(map_index=9, status='UNSAT-VERIFIED'))
            self.assertTrue(path.read_bytes().startswith(prefix))
            self.assertEqual([r['map_index'] for r in t.records(path)], [8, 9])
            path.write_text('{}\nBROKEN\n{}\n')
            with self.assertRaises(ValueError):
                t.records(path)

    def test_resume_repartitions_without_repeating_completed_units(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / '0').mkdir()
            t.append_checkpoint(root / '0/results.jsonl', dict(map_index=8, status='TIMEOUT'))
            queue = [dict(index=i) for i in (8, 9, 11, 12)]
            self.assertEqual([r['index'] for r in t.pending(root, queue, 0, 1)], [9, 11, 12])
            a = list(t.pending(root, queue, 0, 2)); b = list(t.pending(root, queue, 1, 2))
            self.assertEqual(sorted(r['index'] for r in a + b), [9, 11, 12])

    def test_first_sat_is_global_and_persistent_and_stops_next_dispatch(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            units = t.pending(root, [dict(index=8), dict(index=9)], 0, 1)
            self.assertEqual(next(units)['index'], 8)
            self.assertTrue(t.latch_sat(root, dict(map_index=8, unit='first')))
            self.assertFalse(t.latch_sat(root, dict(map_index=9, unit='second')))
            self.assertEqual(list(units), [])
            self.assertEqual(json.loads((root / 'first_sat.json').read_text())['unit'], 'first')
            self.assertEqual(list(t.pending(root, [dict(index=11)], 0, 1)), [])

    def test_budget_keeps_killed_reservations_and_refunds_finished_attempts(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = t.reserve(root, 100)
            second = t.reserve(root, 200)
            t.finish_reservation(root, second, 20)
            self.assertEqual(t.charged_seconds(root), 120)
            with self.assertRaises(RuntimeError):
                t.reserve(root, 22300)
            self.assertEqual(t.charged_seconds(root), 120)
            t.finish_reservation(root, first, 30)
            self.assertEqual(t.charged_seconds(root), 50)

    def test_item5a_wrapper_runs_the_item5a_queue_with_night_caps(self):
        import os
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); executable = tmp / 'python3'; calls = tmp / 'calls.jsonl'
            executable.write_text(f'#!{sys.executable}\n' +
                'import json, os, sys\n'
                'with open(os.environ["WRAPPER_CALLS"], "a") as f:\n'
                '    f.write(json.dumps(sys.argv[1:]) + "\\n")\n')
            executable.chmod(0o755)
            env = dict(os.environ, PYTHON=str(executable), SHARDS='10', WRAPPER_CALLS=str(calls), S5A_RESULTS=str(tmp / 'r'))
            r = subprocess.run(['/bin/bash', str(pilot.HERE / 'run.sh'), '9'], env=env, capture_output=True, text=True, timeout=5)
            self.assertEqual(r.returncode, 0, r.stderr)
            (args,) = [json.loads(line) for line in calls.read_text().splitlines()]
            value = lambda flag: args[args.index(flag) + 1]
            self.assertEqual([args[1], value('--shard'), value('--shards'), value('--timeout'), value('--s5-checker-timeout'),
                              value('--s5-budget-seconds'), value('--hours')], ['s5', '9', '10', '1800', '2700', '288000', '8'])
            self.assertEqual(Path(value('--s5-queue')).name, 'queue_item5a.json')
            self.assertEqual(Path(value('--results-dir')), tmp / 'r/9')
            self.assertIn('exit_status: 0', (tmp / 'r/9/manifest.txt').read_text())

    def test_probe_queue_selects_case_control_and_per_map_caps(self):
        t = self.module()
        probe = pilot.ROOT / 'experiments/E-261103-07-s5-10-4-census-symmetry/queue_probe.json'
        with patch.object(t, 'QUEUE', probe), patch.object(t, 'CASE', t.CASE), patch.object(t, 'CONTROL', t.CONTROL):
            queue = t.load_queue(custom=True)
            self.assertEqual((t.CASE, t.CONTROL), ((10, 4), 'control_f10.json'))
        self.assertEqual((t.CASE, t.CONTROL), ((9, 3), 'control_f9.json'))
        shard0 = queue[0::10]
        self.assertEqual([e.get('control') for e in shard0], ['positive', 'negative', None])
        maps = [e for e in queue if 'control' not in e]
        self.assertEqual(sorted((e['solver_cap'], e['checker_cap']) for e in maps), [(300, 450)] * 6 + [(1800, 2700)] * 4)

    def test_imported_map_queue_checks_identity_and_builds_submap_formulas(self):
        t = self.module()
        night = pilot.ROOT / 'experiments/E-261110-02-face-minimal-10-3-decision/queue.json'
        with patch.object(t, 'QUEUE', night), patch.object(t, 'CASE', t.CASE), patch.object(t, 'CONTROL', t.CONTROL), \
                patch.object(t, 'MAPS_FILE', None):
            queue = t.load_queue(custom=True)
            self.assertEqual((t.CASE, t.CONTROL, t.MAPS_FILE), ((10, 3), 'control_f10.json',
                             'experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json'))
            maps = t.imported_maps(t.MAPS_FILE)
        self.assertIsNone(t.MAPS_FILE)
        self.assertEqual([e.get('control') for e in queue[0::10]], ['positive', 'negative', None, None])
        self.assertEqual(sorted(e['index'] for e in queue if 'control' not in e), list(range(20)))
        c = t.submap_formula(10, dict(enumerate(maps[0]['links'])))
        self.assertEqual(len(c.qvar), 330)
        with tempfile.TemporaryDirectory() as tmp:
            bad = json.loads(night.read_text()); bad['maps'][-1]['canonical_sha256'] = '0' * 64
            path = Path(tmp) / 'queue.json'; path.write_text(json.dumps(bad))
            with patch.object(t, 'QUEUE', path), patch.object(t, 'CASE', t.CASE), patch.object(t, 'CONTROL', t.CONTROL), \
                    patch.object(t, 'MAPS_FILE', None), self.assertRaisesRegex(ValueError, 'imported map identity'):
                t.load_queue(custom=True)

    def test_shard_budget_share_survives_restarts(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp, patch.object(t, 'BUDGET_SECONDS', 300):
            root = Path(tmp)
            a = t.reserve(root, 100, shard=0); t.reserve(root, 100, shard=1)
            t.finish_reservation(root, a, 40)
            b = t.reserve(root, 60, shard=0); t.finish_reservation(root, b, 60)
            self.assertEqual((t.shard_charged(root, 0), t.shard_charged(root, 1)), (100, 100))
            self.assertEqual(t.charged_seconds(root), 200)

    def test_source_identity_change_blocks_resume(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            t.check_identity(root, {'source': 'a'})
            t.check_identity(root, {'source': 'a'})
            with self.assertRaises(ValueError):
                t.check_identity(root, {'source': 'b'})

    @unittest.skipUnless(Path(pilot.CADICAL).is_file() and Path(pilot.DRAT).is_file(), 'external proof tools unavailable')
    def test_saved_failure_stop_is_an_error_instead_of_completed_work(self):
        from types import SimpleNamespace
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'stop.json').write_text('{"error":"failed control"}')
            args = SimpleNamespace(shard=0, shards=1, workers=1, results_dir=str(root / '0'), s5_pilot=True)
            with patch.dict('os.environ', {'CADICAL': pilot.CADICAL, 'DRAT_TRIM': pilot.DRAT}):
                with self.assertRaisesRegex(RuntimeError, 'saved failure stop'):
                    t.run(args)

    def test_production_inherits_pilot_units_and_charges_its_resources(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            here = Path(tmp); root = here / 'results'; saved = root / 'coverage_pilot/0'
            saved.mkdir(parents=True); attempt = saved / 'attempt_test'; attempt.mkdir()
            (attempt / 'manifest.json').write_text('{"status":"SHARD-COMPLETE","wall_seconds":142}')
            t.append_checkpoint(saved / 'results.jsonl', dict(map_index=8, status='TIMEOUT'))
            with patch.object(t, 'HERE', here):
                self.assertEqual([r['index'] for r in t.pending(root, [dict(index=8), dict(index=9)], 0, 1)], [9])
                self.assertEqual(t.charged_seconds(root), 142)

    def test_resume_reads_multiple_saved_units_from_the_same_checkpoint(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index in (8, 9):
                work = root / f'0/attempt_saved/map{index}'; work.mkdir(parents=True)
                t.append_checkpoint(root / '0/results.jsonl', dict(map_index=index, status='TIMEOUT', unit=str(work),
                                                                   cnf_sha256='recorded'))
            self.assertEqual([r['index'] for r in t.pending(root, [dict(index=i) for i in (8, 9, 11)], 0, 1)], [11])

    def test_executable_names_resolve_from_path_before_hashing(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            tool = Path(tmp) / 'local-solver'
            tool.write_text('#!/bin/sh\nexit 0\n'); tool.chmod(0o755)
            with patch.dict('os.environ', {'PATH': tmp}):
                self.assertEqual(t.executable('local-solver'), str(tool.resolve()))
                with self.assertRaises(FileNotFoundError):
                    t.executable('missing-solver')

    def test_resume_rejects_missing_checked_evidence(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / '0').mkdir(); work = root / '0/work'; work.mkdir()
            t.append_checkpoint(root / '0/results.jsonl', dict(map_index=8, status='UNSAT-VERIFIED',
                unit=str(work), cnf_sha256='lost', proof_sha256='lost'))
            with self.assertRaises(ValueError):
                list(t.pending(root, [dict(index=8)], 0, 1))

    def test_resume_accepts_recorded_hashes_without_files(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); work = root / '0/attempt_saved/map8'; work.mkdir(parents=True)
            t.append_checkpoint(root / '0/results.jsonl', dict(map_index=8, status='UNSAT-VERIFIED', unit=str(work),
                cnf_sha256='c', proof_sha256='p', checker_ended_by='completed'))
            t.append_checkpoint(root / '0/results.jsonl', dict(map_index=9, status='TIMEOUT', unit=str(work)))
            with self.assertRaises(ValueError):
                list(t.pending(root, [dict(index=8)], 0, 1))
            (root / '0/results.jsonl').write_text((root / '0/results.jsonl').read_text().splitlines()[0] + '\n')
            self.assertEqual(list(t.pending(root, [dict(index=8)], 0, 1)), [])

    def test_invalid_wrapper_modes_and_excess_workers_do_no_work(self):
        import os
        import subprocess
        for mode, count in [('typo', '1'), ('0', '11'), ('8', '8')]:
            r = subprocess.run(['bash', str(pilot.HERE / 'run.sh'), mode],
                               env=dict(os.environ, SHARDS=count), capture_output=True)
            self.assertEqual(r.returncode, 2)

    def test_wrapper_dispatches_shards_and_pilot_on_system_bash(self):
        import os
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); executable = tmp / 'python3'; calls = tmp / 'calls.jsonl'
            executable.write_text(f'#!{sys.executable}\n' +
                'import json, os, sys\n'
                'with open(os.environ["WRAPPER_CALLS"], "a") as f:\n'
                '    f.write(json.dumps({"args": sys.argv[1:], "threads": '
                '{key: os.environ.get(key) for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", '
                '"VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS")}}) + "\\n")\n')
            executable.chmod(0o755)
            for mode in [str(i) for i in range(8)] + ['coverage-pilot']:
                with self.subTest(mode=mode):
                    calls.unlink(missing_ok=True)
                    env = dict(os.environ, PATH=str(tmp) + os.pathsep + os.environ['PATH'], PYTHON=str(executable),
                               SHARDS='8', WRAPPER_CALLS=str(calls))
                    r = subprocess.run(['/bin/bash', str(pilot.HERE / 'run.sh')] +
                                       (['coverage-pilot'] if mode == 'coverage-pilot' else ['coverage', mode]),
                                       env=env, capture_output=True, text=True, timeout=5)
                    self.assertEqual(r.returncode, 0, r.stderr)
                    records = [json.loads(line) for line in calls.read_text().splitlines()]
                    self.assertEqual([rec['args'][1] for rec in records], ['s5', 'status'])
                    args = records[0]['args']
                    self.assertEqual(args[args.index('--workers') + 1], '1')
                    self.assertEqual(args[args.index('--shard') + 1], '0' if mode == 'coverage-pilot' else mode)
                    self.assertEqual(args[args.index('--shards') + 1], '1' if mode == 'coverage-pilot' else '8')
                    self.assertEqual('--s5-pilot' in args, mode == 'coverage-pilot')
                    self.assertEqual(set(records[0]['threads'].values()), {'1'})

    def test_detached_wrapper_uses_project_python_without_an_active_environment(self):
        import os
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp); interpreter = home / '.venvs/polyhedra/bin/python'
            interpreter.parent.mkdir(parents=True)
            calls = home / 'calls.jsonl'
            interpreter.write_text(f'#!{sys.executable}\n' +
                'import json, os, sys\n'
                'with open(os.environ["WRAPPER_CALLS"], "a") as f:\n'
                '    f.write(json.dumps(sys.argv[1:]) + "\\n")\n')
            interpreter.chmod(0o755)
            wrong = home / 'bin/python3'; wrong.parent.mkdir()
            wrong.write_text('#!/bin/sh\nexit 73\n'); wrong.chmod(0o755)
            env = dict(os.environ, HOME=str(home), PATH=str(wrong.parent) + os.pathsep + os.environ['PATH'],
                       SHARDS='8', WRAPPER_CALLS=str(calls))
            env.pop('VIRTUAL_ENV', None); env.pop('PYTHON', None)
            r = subprocess.run(['/bin/bash', str(pilot.HERE / 'run.sh'), 'coverage', '0'], env=env,
                               capture_output=True, text=True, timeout=5)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual([json.loads(line)[1] for line in calls.read_text().splitlines()], ['s5', 'status'])

    def test_nested_timeout_reaps_the_solver_process(self):
        import os
        import time
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); pidfile = out / 'pid'
            sleeper = f'import os,time; open({str(pidfile)!r}, "w").write(str(os.getpid())); time.sleep(20)'
            wrapper = ('import sys; from pathlib import Path; sys.path.insert(0, ' + repr(str(pilot.HERE)) + '); '
                       'import pilot; pilot.command([' + repr(sys.executable) + ', "-c", ' + repr(sleeper) + '], '
                       'Path(' + repr(str(out / 'inner.log')) + '), 10)')
            self.assertIsNone(pilot.command([sys.executable, '-c', wrapper], out / 'outer.log', .5))
            self.assertTrue(pidfile.exists(), 'nested solver never started')
            pid = int(pidfile.read_text())
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                pass
            else:
                os.kill(pid, 9)
                self.fail('nested solver survived outer timeout')

    def test_sat_between_selection_and_spawn_blocks_solver_start(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); marker = root / 'spawned'
            selected = t.pending(root, [dict(index=8)], 0, 1)
            self.assertEqual(next(selected)['index'], 8)
            t.latch_sat(root, dict(map_index=9, unit='another-worker'))
            with self.assertRaises(t.DispatchStopped):
                pilot.command([sys.executable, '-c', f'open({str(marker)!r}, "w").close()'],
                              root / 'unit.log', 5, gate=lambda: t.dispatch_gate(root))
            self.assertFalse(marker.exists())

    def test_formula_options_are_part_of_resume_identity(self):
        t = self.module()
        self.assertIn('code/omsat_validate.py', t.sources())

    def test_status_accepts_shared_budget_and_lock_files(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'budget.json').write_text('{}')
            (root / 'dispatch.lock').touch(); (root / '0').mkdir()
            (root / '0/results.jsonl').write_text('{"task":"map8","status":"TIMEOUT"}\n')
            r = subprocess.run([sys.executable, str(pilot.ROOT / 'overnight/run_overnight.py'),
                                'status', '--results-dir', str(root)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn('TIMEOUT', r.stdout)

    def test_interrupted_sat_stage_is_preserved_without_repeating_its_budget(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); first = dict(processing={}, stage_attempts={})
            state = out / 'first_sat.json'
            with patch.object(pilot, 'stage', side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    t.process_stage(out, 'model', 'hinge', {}, first, state, lambda cap: cap)
            old = dict(first['stage_attempts']['hinge'])
            marker = Path(old['directory']) / 'raw.log'; marker.write_text('preserve')
            result = t.process_stage(out, 'model', 'hinge', {}, first, state, lambda cap: cap)
            self.assertEqual(result['status'], 'INTERRUPTED')
            self.assertEqual(first['stage_attempts']['hinge'], old)
            self.assertEqual(marker.read_text(), 'preserve')

    @unittest.skipUnless(Path(pilot.CADICAL).is_file() and Path(pilot.DRAT).is_file(), 'external proof tools unavailable')
    def test_solver_has_separate_checker_budget_and_sat_callback(self):
        from omsat import CNF
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp); c = CNF(4); c.nv = 2
            c.clauses = [[1, 2], [-1, 2], [1, -2], [-1, -2]]
            with patch.object(pilot, 'check_proof', wraps=pilot.check_proof) as check:
                r = pilot.solve(c, out, 'negative', 5, checker_timeout=7)
                self.assertEqual(r['status'], 'UNSAT-VERIFIED')
                self.assertEqual(check.call_args.args[-1], 7)
            c.clauses = [[1]]
            called = []
            r = pilot.solve(c, out, 'positive', 5, checker_timeout=7,
                            on_sat=lambda: called.append((out / 'positive.model.json').exists()))
            self.assertEqual(r['status'], 'SAT')
            self.assertEqual(called, [True])


class RecordedPathTests(unittest.TestCase):
    def test_records_keep_paths_relative_to_the_repository(self):
        import tranche
        inside = tranche.ROOT / 'experiments' / 'E-x' / 'results' / '0'
        self.assertEqual(tranche.recorded(inside), 'research/12-faced-polyhedron/experiments/E-x/results/0')
        self.assertEqual(tranche.REPO / tranche.recorded(inside), inside)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(tranche.recorded(tmp), str(Path(tmp).resolve()))
            self.assertEqual(tranche.REPO / tranche.recorded(tmp), Path(tmp).resolve())


class TrancheEvidenceTests(unittest.TestCase):
    def test_saved_same_path_pilot_evidence(self):
        import hashlib
        import tranche
        from test_pilot import artifact_sha, dropped, fresh_check, replay_requested
        root = pilot.HERE / 'results/coverage_pilot'
        manifests = list(root.glob('[0-9]*/attempt_*/manifest.json'))
        if not manifests:
            self.skipTest('same-path pilot has not run')
        for path in manifests:
            manifest = json.loads(path.read_text())
            if manifest['status'] == 'RUNNING':
                self.skipTest('same-path pilot still running')
            self.assertIn(manifest['status'], ('SHARD-COMPLETE', 'FIRST-SAT-STOP'))
            self.assertLess(manifest['wall_seconds'], manifest['budget_seconds'])
            self.assertEqual(manifest['workers'], 1)
            controls = json.loads((path.parent / 'controls/summary.json').read_text())
            self.assertEqual(controls['status'], 'CONTROLS-PASS')
            targets = {f'map{r["map_index"]}_plain': r for r in tranche.records(path.parent.parent / 'results.jsonl')}
            for name, digest in manifest['outputs_sha256'].items():
                artifact = path.parent / name
                if dropped(artifact):
                    continue
                self.assertEqual(artifact_sha(artifact), digest, name)
        recs = tranche.records(root / '0/results.jsonl')
        self.assertTrue(recs)
        self.assertTrue({r['map_index'] for r in recs} <= {8, 9})
        for rec in recs:
            index = rec['map_index']; name = f'map{index}_plain'
            # Recorded launch paths are provenance; artifact checks also work in a fresh checkout.
            relative = Path(rec['unit']).parts[-3:]
            self.assertTrue(relative[0].isdigit())
            self.assertEqual(relative[-1], f'map{index}')
            work = root.joinpath(*relative)
            c = pilot.CNF(9); pilot.build(c, pilot.from_links(pilot.census(9, 3)['maps'][index]['links']), pilot.ALL_OPTS)
            self.assertEqual(rec['formula_sha256'], hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest())
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                c.dimacs(tmp / 'rebuilt.cnf', comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
                self.assertEqual(pilot.sha(tmp / 'rebuilt.cnf'), rec['cnf_sha256'])
                if rec['status'] == 'UNSAT-VERIFIED':
                    self.assertIn('proof_sha256', rec)
                    self.assertIn('s VERIFIED', (work / (name + '.checker.log')).read_text())
                    if replay_requested():
                        self.assertTrue(fresh_check(tmp / 'rebuilt.cnf', tmp, 120))
                elif rec['status'] == 'SAT':
                    self.assertTrue(pilot.model_valid(c.clauses, json.loads((work / (name + '.model.json')).read_text())))
                else:
                    self.assertEqual(rec['status'], 'TIMEOUT')
            self.assertEqual(rec['budget_seconds'], 60)
        self.assertLess(tranche.charged_seconds(root), 6.2 * 3600)


if __name__ == '__main__':
    unittest.main()
