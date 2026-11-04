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

    def test_source_identity_change_blocks_resume(self):
        t = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            t.check_identity(root, {'source': 'a'})
            t.check_identity(root, {'source': 'a'})
            with self.assertRaises(ValueError):
                t.check_identity(root, {'source': 'b'})

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

    def test_invalid_wrapper_modes_and_excess_workers_do_no_work(self):
        import os
        import subprocess
        for mode, count in [('typo', '1'), ('0', '9'), ('8', '8')]:
            r = subprocess.run(['bash', str(pilot.HERE / 'run.sh'), mode],
                               env=dict(os.environ, SHARDS=count), capture_output=True)
            self.assertEqual(r.returncode, 2)

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


if __name__ == '__main__':
    unittest.main()
