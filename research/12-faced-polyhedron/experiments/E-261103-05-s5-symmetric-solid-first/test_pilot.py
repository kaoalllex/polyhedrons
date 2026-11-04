"""Small model and exact-arrangement regressions; no random or focus search."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code'))
from ortools.sat.python import cp_model
import solid_cpsat
import solid_first

TETRA = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]]


class ModelTests(unittest.TestCase):
    def test_hard_multirun_decision_and_impossible_edge_count(self):
        a = solid_first.Arrangement(TETRA)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'model.pbtxt'
            cells, info = solid_cpsat.best_solid(a, target_edges=6, max_runs=3, model_path=path, time_limit=2)
            self.assertEqual(info['status'], 'OPTIMAL')
            self.assertTrue(info['valid'])
            self.assertEqual((info['adjacent'], info['edge_runs']), (6, 6))
            self.assertTrue(path.is_file())
            cells, info = solid_cpsat.best_solid(a, target_edges=7, max_runs=3, time_limit=2)
            self.assertIsNone(cells)
            self.assertEqual(info['status'], 'INFEASIBLE')

    def test_face_connectivity_requires_selected_bridges(self):
        for middle, expected in ((0, cp_model.INFEASIBLE), (1, cp_model.OPTIMAL)):
            model = cp_model.CpModel()
            selected = [model.NewBoolVar(str(i)) for i in range(3)]
            for var, value in zip(selected, (1, middle, 1)):
                model.Add(var == value)
            solid_cpsat.connected_faces(model, selected, [0, 0, 0], [(0, 1), (1, 2)])
            self.assertEqual(cp_model.CpSolver().Solve(model), expected)

    def test_exact_arrangement_and_multisegment_link_extraction(self):
        import pilot
        a = pilot.arrangement(TETRA)
        floating = solid_first.Arrangement(TETRA)
        self.assertEqual(a.bounded, floating.bounded)
        self.assertEqual(a.ones, floating.ones)
        self.assertEqual(len(a.bounded), 1)
        links = pilot.extract_links(a, a.bounded)
        from ladder_exact import verify
        self.assertTrue(verify(TETRA, links)['EMBEDDED'])
        with self.assertRaises(ValueError):
            pilot.arrangement(TETRA[:3] + [TETRA[0]])

    def test_legacy_one_run_api(self):
        _, info = solid_cpsat.best_solid(solid_first.Arrangement(TETRA), time_limit=2)
        self.assertTrue(info['valid'])
        self.assertEqual(info['adjacent'], 6)


if __name__ == '__main__':
    unittest.main()
