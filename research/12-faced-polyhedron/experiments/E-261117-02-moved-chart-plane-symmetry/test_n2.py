"""Regression for E-261117-02: the control chain reruns and matches the saved record; every saved hit passes
verify_candidate --all-pairs and comes from its recorded draw and chart."""
import json
from pathlib import Path
import tempfile
import unittest

import n2

HERE = Path(__file__).resolve().parent


class N2Tests(unittest.TestCase):
    def test_controls_rerun_match_saved(self):
        saved = json.loads((HERE / 'results/controls/controls.json').read_text())
        with tempfile.TemporaryDirectory() as d:
            new = n2.controls(Path(d) / 'controls')
        self.assertTrue(new['PASS'])
        for k in ('K1_plane_only_determinants', 'K2_far_plane', 'K3_moved_chart', 'negative_controls'):
            self.assertEqual(json.loads(json.dumps(new[k], default=str))['PASS'], saved[k]['PASS'], k)
        self.assertEqual(new['K3_moved_chart']['planes'], saved['K3_moved_chart']['planes'])
        k4 = new['K4_sat_controls']
        self.assertEqual([k4[k]['status'] for k in ('pinned_no_gauge', 'pinned_gauge', 'free_gauge', 'free_symbreak')],
                         ['SAT', 'SAT', 'SAT', 'UNSAT'])
        self.assertFalse(k4['symbreak_reachable_equivariantly'])

    def test_saved_hits(self):
        hits = sorted((HERE / 'results/hits').glob('*.json'))
        self.assertTrue(hits)
        for p in hits:
            r = json.loads(p.read_text())
            arm, i = p.stem.split('_')
            rows, hp, hm, _ = n2.draw(arm, int(i))
            self.assertEqual((rows, hp, hm), (r['source_planes'], r['far_plane'], r['planes']), p.name)
            self.assertEqual(n2.verify_candidate(p)['returncode'], 0, p.name)


if __name__ == '__main__':
    unittest.main()
