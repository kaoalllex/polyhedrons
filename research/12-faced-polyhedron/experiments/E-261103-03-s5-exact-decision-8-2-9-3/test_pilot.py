"""Artifact and process-boundary regressions; no target decisions."""
import json
import tempfile
import unittest
from pathlib import Path
import pilot
from omsat import CNF


class PilotTests(unittest.TestCase):
    @unittest.skipUnless(Path(pilot.CADICAL).is_file() and Path(pilot.DRAT).is_file(), "external proof tools unavailable")
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

    def test_realizer_fallback_is_not_recovery(self):
        self.assertFalse(pilot.reconstruction_ok(10 ** 6, True))
        self.assertFalse(pilot.reconstruction_ok(0, False))
        self.assertTrue(pilot.reconstruction_ok(0, True))

    def test_deadline_interrupts_python_work(self):
        import signal
        import time
        try:
            pilot.arm_deadline(.02)
            with self.assertRaises(TimeoutError):
                time.sleep(1)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)

    def test_process_timeout(self):
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            r = pilot.command([sys.executable, '-c', 'import time; time.sleep(10)'], Path(tmp) / 'log', .05)
            self.assertEqual(r, None)

    def test_paired_selection_has_twenty_formulas_on_twelve_maps(self):
        units = pilot.paired_formulas()
        self.assertEqual(len(units), 20)
        self.assertEqual(len({i for i, rec, perm in units}), 12)
        symmetric = [(i, rec, p) for i, rec, p in units if p is not None]
        self.assertEqual(len(symmetric), 8)
        for i, rec, p in symmetric:
            self.assertTrue(rec['admissible'])
            self.assertTrue(all(p[k] != k and p[p[p[k]]] == k for k in range(9)))
            self.assertTrue(any(j == i and q is None for j, _, q in units))
            for k, link in enumerate(rec['links']):
                a = [p[v] for v in link]; b = rec['links'][p[k]]
                self.assertTrue(any(a == b[j:] + b[:j] for j in range(len(b))))

    def test_free_involutions_preserve_cyclic_links(self):
        maps = pilot.census(8, 2)['maps']
        for m in maps:
            p = pilot.free_c2(m['links'])
            self.assertTrue(all(p[p[i]] == i and p[i] != i for i in range(8)))
            for i, link in enumerate(m['links']):
                a = [p[x] for x in link]; b = m['links'][p[i]]
                self.assertTrue(any(a == b[j:] + b[:j] for j in range(len(b))))


class EvidenceTests(unittest.TestCase):
    def test_saved_evidence(self):
        out = Path(__file__).resolve().parent / 'results/pilot'
        manifest = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(manifest['status'], 'PILOT-COMPLETE')
        for name, digest in manifest['outputs_sha256'].items():
            self.assertEqual(pilot.sha(out / name), digest, name)
        summary = json.loads((out / 'summary.json').read_text())
        self.assertEqual(summary['construction_power'], 'CONTROL-PASS')
        for name, result in summary['controls'].items():
            if isinstance(result, dict) and 'signs_match' in result:
                self.assertTrue(pilot.reconstruction_ok(result['wrong_signs'], result['signs_match']))
                inp = json.loads((out / (name + '.input.json')).read_text())
                chi = pilot.chirotope_from_planes(result['planes'])
                self.assertEqual({','.join(map(str, k)): v for k, v in chi.items()}, inp['chi'])
                self.assertTrue(pilot.verify(result['planes'], dict(enumerate(inp['links'])))['EMBEDDED'])
        print('DRAT replay: fresh external checks' if Path(pilot.DRAT).is_file() else 'DRAT replay: hashes and saved transcripts only', flush=True)
        for name, result in summary['targets'].items():
            self.assertEqual(result['status'], 'UNSAT-VERIFIED')
            i = int(name[3]); rec = pilot.census(8, 2)['maps'][i]
            self.assertEqual(json.loads((out / f'map{i}.json').read_text()), rec)
            t = pilot.from_links(rec['links'])
            if name.endswith('C2'):
                g = pilot.free_c2(rec['links']); identity = tuple(range(8))
                c, _, _ = pilot.build_sym(t, [identity, g], {identity: 1, g: 1}, pilot.ALL_OPTS)
            else:
                c = pilot.CNF(8); pilot.build(c, t, pilot.ALL_OPTS)
            with tempfile.TemporaryDirectory() as tmp:
                rebuilt = Path(tmp) / 'rebuilt.cnf'
                c.dimacs(rebuilt, comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
                self.assertEqual(pilot.sha(rebuilt), result['cnf_sha256'])
                if Path(pilot.DRAT).is_file():
                    self.assertTrue(pilot.check_proof(out / (name + '.cnf'), out / (name + '.drat'), Path(tmp) / 'checker.log', 60))
                else:
                    self.assertIn('s VERIFIED', (out / (name + '.checker.log')).read_text())


if __name__ == '__main__':
    unittest.main()
