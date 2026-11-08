"""Artifact and process-boundary regressions; no target decisions."""
import json
import os
import gzip
import hashlib
import tempfile
import unittest
from pathlib import Path
import pilot
from omsat import CNF


def replay_requested():
    requested = os.environ.get('REPLAY_DRAT') == '1'
    if requested and not (Path(pilot.DRAT).is_file() and Path(pilot.CADICAL).is_file()):
        raise RuntimeError('REPLAY_DRAT=1 requires cadical and drat-trim')
    return requested


def dropped(path):
    """CNF and proof files are deleted after their check (PROTOCOL.md §5); their hashes stay in the records."""
    return (path.name.endswith(('.cnf', '.drat', '.cnf.gz', '.drat.gz'))
            and not path.exists() and not Path(str(path) + '.gz').exists())


def fresh_check(cnf, tmp, cap):
    """Audit replay without a kept proof: solve the rebuilt formula again and check the new proof."""
    proof = Path(tmp) / 'fresh.drat'
    rc = pilot.command([pilot.CADICAL, str(cnf), str(proof)], Path(tmp) / 'fresh.solver.log', cap)
    return rc == 20 and pilot.check_proof(cnf, proof, Path(tmp) / 'fresh.checker.log', cap)


def artifact_sha(path):
    opener = path.open if path.exists() else path.with_suffix(path.suffix + '.gz').open
    with opener('rb') as raw:
        stream = raw if path.exists() else gzip.GzipFile(fileobj=raw)
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


class PilotTests(unittest.TestCase):
    def test_saved_proof_replay_requires_explicit_opt_in(self):
        from unittest.mock import patch
        with patch.dict(os.environ, {}, clear=True), patch.object(Path, 'is_file', return_value=True):
            self.assertFalse(replay_requested())
        with patch.dict(os.environ, {'REPLAY_DRAT': '1'}):
            with patch.object(Path, 'is_file', return_value=True):
                self.assertTrue(replay_requested())
            with patch.object(Path, 'is_file', return_value=False):
                with self.assertRaises(RuntimeError):
                    replay_requested()

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
            self.assertIn('proof_sha256', r)
            self.assertFalse((out / 'unsat.cnf').exists() or (out / 'unsat.drat').exists())
            c.dimacs(out / 'unsat.cnf'); (out / 'broken.drat').write_text('')
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

    def test_grid_uses_prior_sixty_second_cells_without_repeating_decisions(self):
        units = pilot.grid_units()
        self.assertEqual([(i, cap) for i, rec, p, cap in units],
                         [(0, 60), (1, 60), (0, 300), (1, 300), (40, 300), (48, 300)])
        self.assertTrue(all(rec['admissible'] and p is None for _, rec, p, _ in units))
        self.assertEqual({i for i, _, _, _ in units}, {0, 1, 40, 48})

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
    def test_free_c3_control_and_mirror_gauge_by_determinant_expansion(self):
        import itertools
        import math
        inp = json.loads((Path(__file__).resolve().parent / 'results/paired_9_3_continued/C3_control.input.json').read_text())
        h = inp['planes']; p = inp['permutation']
        self.assertTrue(all(h[p[i]] == [h[i][1], h[i][2], h[i][0], h[i][3]] for i in range(9)))
        # Independent Leibniz expansion; no encoder determinant helper.
        def signs(planes):
            rows = planes + [[0, 0, 0, 1]]
            result = {}
            for q in itertools.combinations(range(10), 4):
                det = sum((-1) ** sum(a > b for i, a in enumerate(perm) for b in perm[i + 1:])
                          * math.prod(rows[q[i]][perm[i]] for i in range(4))
                          for perm in itertools.permutations(range(4)))
                self.assertNotEqual(det, 0)
                result[q] = 1 if det > 0 else -1
            return result
        original = signs(h)
        # Reflection perpendicular to (1,1,1), global face reorientation, positive scale 3.
        reflected = [[2 * sum(row[:3]) - 3 * a for a in row[:3]] + [-3 * row[3]] for row in h]
        mirrored = signs(reflected)
        self.assertTrue(all(mirrored[q] == (value if 9 in q else -value) for q, value in original.items()))
        self.assertTrue(all(reflected[p[i]] == [reflected[i][1], reflected[i][2], reflected[i][0], reflected[i][3]] for i in range(9)))
        self.assertTrue(all(rec['aut_plus'] in (3, 6) for rec in pilot.census(9, 3)['maps'][:8]))

    def test_grid_evidence(self):
        out = Path(__file__).resolve().parent / 'results/grid_9_3'
        if not (out / 'manifest.json').exists():
            self.skipTest('grid artifacts unavailable')
        manifest = json.loads((out / 'manifest.json').read_text())
        if manifest['status'] == 'RUNNING':
            self.skipTest('grid still running')
        summary = json.loads((out / 'summary.json').read_text())
        self.assertIn(summary['status'], ('PILOT-COMPLETE', 'FIRST-SAT-PROCESSED', 'CANDIDATE'))
        self.assertEqual(manifest['family'], 'grid_9_3')
        self.assertLess(manifest['core_hours'], 1)
        for name, digest in manifest['outputs_sha256'].items():
            path = out / name
            if dropped(path):
                continue
            self.assertEqual(artifact_sha(path), digest, name)
        baseline = out.parent / 'paired_9_3_continued/summary.json'
        self.assertEqual(pilot.sha(baseline), summary['baseline']['sha256'])
        decided = set()
        for name, r in summary['targets'].items():
            i = r['map_index']; cap = r['cutoff_seconds']
            self.assertIn(i, (0, 1, 40, 48))
            self.assertIn(cap, (60, 300))
            self.assertNotIn(i, decided)
            self.assertLessEqual(r['budget_seconds'], cap)
            rec = pilot.census(9, 3)['maps'][i]
            c = pilot.CNF(9); pilot.build(c, pilot.from_links(rec['links']), pilot.ALL_OPTS)
            self.assertEqual(hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest(), r['formula_sha256'])
            with tempfile.TemporaryDirectory() as tmp:
                rebuilt = Path(tmp) / 'rebuilt.cnf'
                c.dimacs(rebuilt, comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
                self.assertEqual(pilot.sha(rebuilt), r['cnf_sha256'])
                if r['status'] == 'UNSAT-VERIFIED':
                    decided.add(i)
                    self.assertLessEqual(r['checker_budget_seconds'], cap)
                    if replay_requested():
                        self.assertTrue(fresh_check(rebuilt, tmp, cap))
                    else:
                        self.assertIn('s VERIFIED', (out / (name + '.checker.log')).read_text())
                elif r['status'] == 'SAT':
                    decided.add(i)
                    self.assertTrue(pilot.model_valid(c.clauses, json.loads((out / (name + '.model.json')).read_text())))
                else:
                    self.assertEqual(r['status'], 'TIMEOUT')
        if summary['status'] == 'PILOT-COMPLETE':
            for i in (0, 1, 40, 48):
                self.assertTrue(i in decided or f'map{i}_plain_t300' in summary['targets'])
        self.assertEqual(summary['controls']['nine_plane_control']['status'], 'SAT')
        self.assertEqual(summary['controls']['C3_control']['status'], 'SAT')

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
                if dropped(path):
                    continue
                self.assertEqual(artifact_sha(path), digest, name)
        from omsat_sym import closure
        for name, r in summary['targets'].items():
            folder = base / Path(r.get('artifact_dir', str(out))).name
            digest = r.get('cnf_sha256') or json.loads((folder / 'manifest.json').read_text())['outputs_sha256'][name + '.cnf']
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
                self.assertEqual(pilot.sha(rebuilt), digest)
                if r['status'] == 'UNSAT-VERIFIED':
                    if replay_requested():
                        self.assertTrue(fresh_check(rebuilt, tmp, 60))
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
            if not dropped(out / name):
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
        print('DRAT replay: fresh external checks' if replay_requested() else 'DRAT replay: hashes and saved transcripts only', flush=True)
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
                if replay_requested():
                    self.assertTrue(fresh_check(rebuilt, tmp, 60))
                else:
                    self.assertIn('s VERIFIED', (out / (name + '.checker.log')).read_text())


if __name__ == '__main__':
    unittest.main()
