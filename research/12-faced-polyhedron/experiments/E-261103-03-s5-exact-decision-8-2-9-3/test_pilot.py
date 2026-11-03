"""Artifact and process-boundary regressions; no target decisions."""
import tempfile
import unittest
from pathlib import Path
import pilot
from omsat import CNF


class PilotTests(unittest.TestCase):
    def test_saved_models_and_proofs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            c = CNF(4); c.clauses = [[1], [2, -1]]; c.nv = 2
            r = pilot.solve(c, out, 'sat', 5)
            self.assertEqual(r['status'], 'SAT')
            self.assertTrue(pilot.model_valid(c.clauses, [1, 2]))
            self.assertFalse(pilot.model_valid(c.clauses, [-1, 2]))
            c.clauses = [[1, 2], [-1, 2], [1, -2], [-1, -2]]
            r = pilot.solve(c, out, 'unsat', 5)
            self.assertEqual(r['status'], 'UNSAT-VERIFIED')
            (out / 'broken.drat').write_text('')
            self.assertFalse(pilot.check_proof(out / 'unsat.cnf', out / 'broken.drat', out / 'broken.log', 5))

    def test_process_timeout(self):
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            r = pilot.command([sys.executable, '-c', 'import time; time.sleep(10)'], Path(tmp) / 'log', .05)
            self.assertEqual(r, None)

    def test_free_involutions_preserve_cyclic_links(self):
        maps = pilot.census(8, 2)['maps']
        for m in maps:
            p = pilot.free_c2(m['links'])
            self.assertTrue(all(p[p[i]] == i and p[i] != i for i in range(8)))
            for i, link in enumerate(m['links']):
                a = [p[x] for x in link]; b = m['links'][p[i]]
                self.assertTrue(any(a == b[j:] + b[:j] for j in range(len(b))))


if __name__ == '__main__':
    unittest.main()
