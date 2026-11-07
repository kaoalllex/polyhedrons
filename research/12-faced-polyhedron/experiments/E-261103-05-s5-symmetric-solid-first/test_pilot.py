"""Small model and exact-arrangement regressions; no random or focus search."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'verification'))
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

    def test_consistency_error_is_not_a_degenerate_draw(self):
        import pilot
        huge = 10 ** 20
        rows = TETRA[:3] + [[1, 1, 1, -1], [huge, huge, huge, -huge + 1]]
        with self.assertRaises(ArithmeticError):
            pilot.arrangement(rows)

    def test_result_validation_stops_bad_status_geometry_and_topology(self):
        import pilot
        from ladder_exact import verify
        links = pilot.extract_links(pilot.arrangement(TETRA), pilot.arrangement(TETRA).bounded)
        inp = dict(planes=TETRA, edges=6)
        good = dict(solver=dict(status='OPTIMAL'), geometry=verify(TETRA, links))
        pilot.validate_result(good, inp)
        with self.assertRaises(RuntimeError):
            pilot.validate_result(dict(solver=dict(status='MODEL_INVALID')), inp)
        with self.assertRaises(ArithmeticError):
            pilot.validate_result(dict(solver=dict(status='OPTIMAL'), geometry=dict(EMBEDDED=False)), inp)
        with self.assertRaises(ArithmeticError):
            pilot.validate_result(good, dict(planes=TETRA, edges=9))

    def test_candidate_export_does_not_select_legacy_solid_parser(self):
        import pilot
        a = pilot.arrangement(TETRA); links = pilot.extract_links(a, a.bounded)
        record = pilot.candidate_record(dict(planes=TETRA, links=links, solid=sorted(a.bounded)))
        self.assertNotIn('solid', record)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'candidate.json'; pilot.dump(path, record)
            import subprocess
            result = subprocess.run([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(path), '--all-pairs'],
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_legacy_one_run_api(self):
        _, info = solid_cpsat.best_solid(solid_first.Arrangement(TETRA), time_limit=2)
        self.assertTrue(info['valid'])
        self.assertEqual(info['adjacent'], 6)


class EvidenceTests(unittest.TestCase):
    def test_saved_models_and_exact_recoveries(self):
        import json
        import pilot
        from solid_fast import Tables
        from ladder_exact import verify
        out = Path(__file__).resolve().parent / 'results/pilot'
        manifest = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(manifest['status'], 'R3-FOUND')
        for name, digest in manifest['outputs_sha256'].items():
            self.assertEqual(pilot.sha(out / name), digest, name)
        summary = json.loads((out / 'summary.json').read_text())
        for name, saved in {**summary['controls'], **summary['random']}.items():
            inp = json.loads((out / (name + '.input.json')).read_text())
            result = json.loads((out / (name + '.output.json')).read_text())
            pilot.validate_result(result, inp)
            if 'seed' in inp:
                generated, rejected = pilot.random_d2(inp['seed'])
                self.assertEqual(pilot.integer_planes(generated), pilot.integer_planes(inp['planes']))
                self.assertEqual(rejected, inp['rejected'])
            a = pilot.arrangement(inp['planes']); tables = Tables(a)
            self.assertEqual(len(a.bounded), result['bounded_cells'])
            model_path = out / (name + '.output.model.pbtxt')
            self.assertEqual(pilot.sha(model_path), result['model_sha256'])
            with tempfile.TemporaryDirectory() as tmp:
                rebuilt = Path(tmp) / 'model.pbtxt'
                solid_cpsat.best_solid(a, tables, target_edges=inp['edges'], max_runs=3,
                                       model_path=rebuilt, time_limit=.001)
                self.assertEqual(pilot.sha(rebuilt), pilot.sha(model_path))
            model = cp_model.CpModel()
            self.assertTrue(model.Proto().parse_text_format(model_path.read_text()))
            solver = cp_model.CpSolver(); solver.parameters.num_workers = 1
            solver.parameters.max_time_in_seconds = inp['solver_seconds']
            status = solver.StatusName(solver.Solve(model))
            self.assertEqual(status, result['solver']['status'])
            if 'geometry' in result:
                links = {int(k): v for k, v in result['links'].items()}
                self.assertTrue(verify(result['planes'], links)['EMBEDDED'])
                extracted = pilot.extract_links(a, {tuple(x) for x in result['solid']})
                self.assertEqual(extracted, links)
                if 'links' in inp:
                    expected = {int(k): v for k, v in inp['links'].items()}
                    self.assertTrue(all(pilot.cyclic_equal(links[i], expected[i]) for i in links))

    def test_canonical_exports_and_independent_auxiliary_check(self):
        import copy
        import json
        import subprocess
        import pilot
        out = Path(__file__).resolve().parent / 'results/recheck'
        manifest = json.loads((out / 'manifest.json').read_text())
        for name, digest in manifest['outputs_sha256'].items():
            self.assertEqual(pilot.sha(out / name), digest, name)
        candidate = json.loads((out / 'd2_seed4_15.candidate.json').read_text())
        known = json.loads((out / 'roest_vigh_15.candidate.json').read_text())
        mapping = {0: 0, 1: 3, 2: 1, 3: 2, 4: 7, 5: 4, 6: 6, 7: 5}
        for face, link in candidate['links'].items():
            self.assertTrue(pilot.cyclic_equal([mapping[x] for x in link], known['links'][str(mapping[int(face)])]))
        raw = json.loads((out.parent / 'pilot/d2_seed4_15.output.json').read_text())
        solid = {tuple(v) for v in raw['solid']}
        for perm in ([1, 0, 3, 2, 5, 4, 7, 6], [2, 3, 0, 1, 6, 7, 4, 5]):
            self.assertEqual({tuple(v[perm[i]] for i in range(8)) for v in solid}, solid)
        verifier = ROOT / 'verification/verify_candidate.py'
        for path in out.glob('*.candidate.json'):
            r = subprocess.run([sys.executable, str(verifier), str(path), '--all-pairs'], capture_output=True, text=True, timeout=10)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        checker = Path(__file__).resolve().parent / 'verify_independent.py'
        good = subprocess.run([sys.executable, str(checker), str(out / 'd2_seed4_15.candidate.json')],
                              capture_output=True, text=True, timeout=10)
        self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
        report = json.loads(good.stdout)
        self.assertEqual(report['verdict'], 'ACCEPT')
        self.assertEqual(report['V_E_F_chi'], [24, 36, 8, -4])
        self.assertEqual(report['adjacent_pairs'], 28)
        with tempfile.TemporaryDirectory() as tmp:
            bad = copy.deepcopy(candidate); bad['links']['0'][0] = bad['links']['0'][1]
            path = Path(tmp) / 'invalid.json'; pilot.dump(path, bad)
            r = subprocess.run([sys.executable, str(checker), str(path)], capture_output=True, text=True, timeout=10)
            self.assertEqual(r.returncode, 1)
            self.assertEqual(json.loads(r.stdout)['verdict'], 'REJECT')


if __name__ == '__main__':
    unittest.main()
