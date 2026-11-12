"""E-261112-01 prep regressions: budget boundary, the lower-bound model path, frozen list hash and cell membership."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cells
import stage_a
import solid_first
import solid_cpsat


class StageATests(unittest.TestCase):
    def test_budget_boundary(self):
        cap, budget = 60, 1000
        edge = budget - cap - stage_a.OVERHEAD
        self.assertTrue(stage_a.can_start(edge - 1, cap, budget))
        self.assertTrue(stage_a.can_start(edge, cap, budget))
        self.assertFalse(stage_a.can_start(edge + 1, cap, budget))

    def test_lower_bound_on_tetrahedron(self):
        a = solid_first.Arrangement(stage_a.TETRA)
        sel, info = solid_cpsat.best_solid(a, target_edges=6, edges_at_least=True, max_runs=3, time_limit=5)
        self.assertTrue(info['valid'] and info['edge_runs'] >= 6)
        sel, info = solid_cpsat.best_solid(a, target_edges=7, edges_at_least=True, max_runs=3, time_limit=5)
        self.assertIsNone(sel)
        self.assertEqual(info['status'], 'INFEASIBLE')

    def test_frozen_list_and_membership(self):
        units = stage_a.load_units()
        self.assertEqual(len(units), 2004)
        self.assertEqual([u['ordinal'] for u in units], list(range(2004)))
        for s in cells.SOURCES:
            D = cells.duals(cells.source_planes(s))
            for u in [u for u in units if u['source'] == s][::97]:
                p = [cells.Fr(v) for v in u['ninth']]
                self.assertEqual(cells.key_str(cells.key_of(D, p)), u['key'])
        first = [{u['source'] for u in units if u['ordinal'] % 10 == k and u['ordinal'] < 20} for k in range(10)]
        self.assertTrue(all(f == set(cells.SOURCES) for f in first))

    def test_unit_branch_without_solver(self):
        """Controls and units with a stub solver: resume, candidate flag and budget stop, no target computation."""
        verdicts = iter(['INFEASIBLE', 'SOLID'])
        def fake(raw, name, u):
            v = 'INFEASIBLE' if name.startswith('C2') else 'SOLID' if name.startswith('C') else next(verdicts)
            g = dict(all_pairs_adjacent=True, V_E_F_chi=[8, 0, 8, 0], EMBEDDED=v == 'SOLID')
            return dict(verdict=v, wall_seconds=1.0, solver=dict(status=v, edge_runs=39), geometry=g, planes=[], links={})
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(stage_a, 'run_unit', fake), \
                mock.patch.object(stage_a, 'c1_unit', lambda n: dict(planes=[], edges_min=30, method='lp', differs=True)):
            out = Path(tmp) / '3'
            args = lambda b: mock.Mock(out=out, shard=3, shards=10, cap=60, budget=b, pilot=False)
            self.assertEqual(stage_a.run_shard(args(5 + 60 + stage_a.OVERHEAD)), 4)    # controls 5 s, one unit fits
            self.assertEqual(stage_a.run_shard(args(1e6)), 5)                         # resumes, second unit SOLID
            rec = [r['unit'] for r in stage_a.records(out / 'results.jsonl')]
            units = [u['unit'] for u in stage_a.load_units() if u['ordinal'] % 10 == 3]
            self.assertEqual(rec, units[:2])
            self.assertTrue((Path(tmp) / 'CANDIDATE').exists())
            self.assertEqual(stage_a.run_shard(args(1e6)), 5)                         # flag stops every shard

    def test_pilot_gate(self):
        self.assertTrue(stage_a.projection_ok(100, 2, 50, 200))
        self.assertFalse(stage_a.projection_ok(100, 2, 51, 200))
        def fake(raw, name, u):
            v = 'SOLID' if name.startswith(('C0', 'C1')) else 'INFEASIBLE'
            g = dict(all_pairs_adjacent=True, V_E_F_chi=[8, 0, 8, 0], EMBEDDED=v == 'SOLID')
            return dict(verdict=v, wall_seconds=1.0, solver=dict(status=v), geometry=g, planes=[], links={})
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(stage_a, 'run_unit', fake), \
                mock.patch.object(stage_a, 'c1_unit', lambda n: dict(planes=[], edges_min=30, method='lp', differs=True)):
            out = Path(tmp) / '3'
            args = lambda b: mock.Mock(out=out, shard=3, shards=10, cap=60, budget=b, pilot=False)
            self.assertEqual(stage_a.run_shard(args(150)), 6)        # pilot fits, 198 more units x 1 s do not
            rec = stage_a.records(out / 'results.jsonl')
            self.assertEqual([r['phase'] for r in rec], ['pilot', 'pilot'])
            self.assertEqual(stage_a.run_shard(args(1e6)), 0)        # gate passes, the shard completes
            rec = stage_a.records(out / 'results.jsonl')
            self.assertEqual(len(rec), 201)
            self.assertEqual({r['phase'] for r in rec[2:]}, {'day'})


if __name__ == '__main__':
    unittest.main()
