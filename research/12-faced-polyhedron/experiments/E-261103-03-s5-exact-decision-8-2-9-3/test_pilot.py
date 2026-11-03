"""Artifact and process-boundary regressions; no target decisions."""
import json
import gzip
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path
import pilot
from omsat import CNF


def artifact_sha(path):
    opener = path.open if path.exists() else path.with_suffix(path.suffix + '.gz').open
    with opener('rb') as raw:
        stream = raw if path.exists() else gzip.GzipFile(fileobj=raw)
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def unpack(path, destination):
    if path.exists():
        return path
    with gzip.open(str(path) + '.gz', 'rb') as src, destination.open('wb') as dst:
        shutil.copyfileobj(src, dst)
    return destination


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
        self.assertEqual([i for i, _, p in units if p is None], [0, 5, 10, 30, 40, 48, 1, 2, 3, 4, 6, 7])
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
    def test_paired_evidence(self):
        base = Path(__file__).resolve().parent / 'results'
        out = base / 'paired_9_3_continued'
        if not (out / 'manifest.json').exists():
            self.skipTest('paired pilot artifacts unavailable')
        manifest = json.loads((out / 'manifest.json').read_text())
        if manifest['status'] == 'RUNNING':
            self.skipTest('paired pilot still running')
        summary = json.loads((out / 'summary.json').read_text())
        self.assertEqual(summary['status'], 'PILOT-COMPLETE')
        self.assertEqual(len(summary['targets']), 20)
        self.assertLess(sum(json.loads((d / 'manifest.json').read_text())['core_hours']
                            for d in (base / 'paired_9_3', out)), 1)
        for folder in (base / 'paired_9_3', out):
            record = json.loads((folder / 'manifest.json').read_text())
            for name, digest in record['outputs_sha256'].items():
                path = folder / name
                target = summary['targets'].get(name.removesuffix('.drat'), {})
                if (name.endswith('.drat') and target.get('status') in ('TIMEOUT', 'INTERRUPTED')
                        and not path.exists() and not Path(str(path) + '.gz').exists()):
                    # Partial proofs stay on the run host; they support no negative claim.
                    continue
                self.assertEqual(artifact_sha(path), digest, name)
        from omsat_sym import closure
        for name, r in summary['targets'].items():
            folder = base / Path(r.get('artifact_dir', str(out))).name
            i = r['map_index']; rec = pilot.census(9, 3)['maps'][i]
            t = pilot.from_links(rec['links'])
            if name.endswith('C3'):
                p = pilot.free_c3(rec['links']); group = sorted(closure([p], 9))
                c, _, _ = pilot.build_sym(t, group, {g: 1 for g in group}, pilot.ALL_OPTS)
            else:
                c = pilot.CNF(9); pilot.build(c, t, pilot.ALL_OPTS)
            with tempfile.TemporaryDirectory() as tmp:
                rebuilt = Path(tmp) / 'rebuilt.cnf'
                c.dimacs(rebuilt, comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
                self.assertEqual(pilot.sha(rebuilt), artifact_sha(folder / (name + '.cnf')))
                if r['status'] == 'UNSAT-VERIFIED':
                    if Path(pilot.DRAT).is_file():
                        proof = unpack(folder / (name + '.drat'), Path(tmp) / 'proof.drat')
                        self.assertTrue(pilot.check_proof(rebuilt, proof, Path(tmp) / 'log', 60))
                    else:
                        self.assertIn('s VERIFIED', (folder / (name + '.checker.log')).read_text())
                elif r['status'] == 'SAT':
                    self.assertTrue(pilot.model_valid(c.clauses, json.loads((folder / (name + '.model.json')).read_text())))
                else:
                    self.assertIn(r['status'], ('TIMEOUT', 'INTERRUPTED'))
        self.assertEqual(summary['controls']['nine_plane_control']['status'], 'SAT')
        self.assertEqual(summary['controls']['C3_control']['status'], 'SAT')
        from omsat_validate import eval_all, compare_direct
        inp = json.loads((out / 'nine_plane_control.input.json').read_text())
        t = pilot.from_links(pilot.census(9, 3)['maps'][0]['links'])
        _, ev = eval_all(inp['planes'], t)
        mismatches, _, _ = compare_direct(inp['planes'], t, ev, {})
        self.assertEqual(mismatches, [])

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
