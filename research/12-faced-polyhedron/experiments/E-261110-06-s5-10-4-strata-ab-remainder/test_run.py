"""Exercise SAT continuation and interrupted seed recovery without solving target formulas."""
import argparse
import gzip
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import run


class RunnerTests(unittest.TestCase):
    def exercise(self, interrupted=False, custom=False, stop_on_sat=False, full_cap=False):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); out=root/'0'; out.mkdir()
            queue=root/'queue.json'
            data=dict(inputs_sha256={},maps=[dict(index=i,pattern='test',solver_cap=1) for i in range(16)])
            if stop_on_sat:
                data.update(stop_on_sat=True, solver_opts=['--sat'])
            if full_cap:
                data.update(truncate_to_budget=True, full_cap=True)
                for entry in data['maps']:
                    entry['solver_cap'] = 200
            if custom:
                (root/'maps.json.gz').write_bytes(gzip.compress(json.dumps({'maps':[{'links':[]}]*16}).encode()))
                (root/'controls.json').write_text('{"PASS":true}')
                data.update(case=[11,5],census_file='maps.json.gz',controls_file='controls.json',truncate_to_budget=True)
            queue.write_text(json.dumps(data))
            args=argparse.Namespace(results_dir=str(out),shard=0,shards=8,workers=1,
                                    s5_queue=str(queue),s5_budget_seconds=800,hours=1)
            calls=[]
            def solve(c,dest,name,cap,**kwargs):
                if stop_on_sat:
                    self.assertEqual(run.pilot.SOLVER_OPTS, ['--sat'])
                    with kwargs['solver_gate']():
                        pass
                calls.append(name)
                return dict(status='SAT' if 'map0_' in name else 'UNSAT-SOLVER',seconds=.01)
            def bridge(*args):
                self.assertFalse(run.tranche.BRIDGE['submap'])
                if interrupted:
                    raise InterruptedError('test interruption')
                return dict(processing={},candidate=None)
            with patch.object(run,'ROOT',root), patch.object(run.prep,'controls',return_value={}), patch.object(run.pilot,'census',return_value={'maps':[{'links':[]}]*16}) as census, patch.object(run.pilot,'from_links') as topology, patch.object(run.pilot,'CNF'), patch.object(run.pilot,'build'), patch.object(run.pilot,'solve',side_effect=solve), patch.object(run.tranche,'bridge',side_effect=bridge):
                topology.return_value.n=11 if custom else 10
                if interrupted:
                    with self.assertRaises(InterruptedError):
                        run.run(args)
                    self.assertTrue((out/'map0/map0_seed0.json').exists())
                    self.assertFalse((root/'stop.json').exists())
                else:
                    run.run(args)
                    rows=run.tranche.records(out/'results.jsonl')
                    if full_cap:
                        self.assertEqual(rows, [])
                        self.assertEqual(calls, [])
                    elif stop_on_sat:
                        self.assertEqual([r['map_index'] for r in rows], [0])
                        self.assertEqual(len(rows[0]['models']), 1)
                        self.assertNotIn('processing', rows[0]['models'][0])
                        self.assertFalse(rows[0]['bridge_complete'])
                        self.assertEqual(len(calls), 1)
                        self.assertTrue((root/'first_sat.json').exists())
                        with self.assertRaises(run.tranche.DispatchStopped):
                            with run.tranche.dispatch_gate(root):
                                self.fail('dispatch after SAT latch')
                    else:
                        self.assertEqual([r['map_index'] for r in rows],[0,8])
                        self.assertEqual(len(rows[0]['models']),30)
                        self.assertTrue(rows[0]['bridge_complete'])
                        self.assertEqual(len(calls),31)
                        self.assertFalse((root/'first_sat.json').exists())
                    count = len(calls)
                    run.run(args)
                    self.assertEqual(len(calls),count)
                    if custom:
                        census.assert_not_called()

    def test_sat_processes_thirty_seeds_and_continues_next_map(self):
        self.exercise()

    def test_interruption_preserves_checked_seed_without_failure_latch(self):
        self.exercise(True)

    def test_custom_size_uses_frozen_compressed_census_and_resumes(self):
        self.exercise(custom=True)

    def test_first_sat_preserves_model_and_stops_dispatch_without_bridge(self):
        self.exercise(stop_on_sat=True)

    def test_full_cap_leaves_unaffordable_units_pending(self):
        self.exercise(full_cap=True)


if __name__=='__main__':
    unittest.main()
