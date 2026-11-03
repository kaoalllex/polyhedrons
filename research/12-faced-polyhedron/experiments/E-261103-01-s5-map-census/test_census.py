"""Focused census controls; run with the project venv from any directory."""
import importlib.util
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


class CensusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("census", HERE / "census.py")
        cls.census = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.census)

    def test_extra_graphs(self):
        # Two extra edges: parallel, adjacent, or disjoint.
        self.assertEqual(len(self.census.extra_graphs(8, 2)), 3)
        self.assertEqual(len(self.census.extra_graphs(9, 3)), 8)

    def test_c3_triangle_orbits(self):
        spec = importlib.util.spec_from_file_location("c3", HERE / "c3_crosscheck.py")
        c3 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(c3)
        fixed, moving = c3.triangle_orbits()
        self.assertEqual(len(fixed), 6)
        self.assertEqual(len(moving), 54)
        self.assertTrue(all(len(o) == 1 for o in fixed))
        self.assertTrue(all(len(o) == 3 for o in moving))

    def test_szilassi_complete_and_invariant(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.census.run(7, 1, 10, Path(tmp))
        self.assertTrue(result["complete"])
        self.assertEqual(len(result["maps"]), 1)
        rec = result["maps"][0]
        self.assertEqual(rec["aut_plus"], 42)
        self.assertFalse(rec["reflexible"])
        self.assertTrue(rec["admissible"])
        m = self.census.from_code(rec["code"])
        self.census.review.check(m, 7, 1)
        # Mirroring changes the tail of a dart to its former head.
        mirror = self.census.review.TriMap([t[::-1] for t in m.tri], m.alpha,
                                         [6 - m.head(d) for d in range(len(m.tail))])
        self.assertEqual(m.canon()[0], mirror.canon()[0])

    def test_timeout_is_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.census.run(9, 3, 0, Path(tmp))
        self.assertFalse(result["complete"])
        self.assertEqual(result["stop_reason"], "time_limit")

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "graphs.txt"
            existing.write_text("keep this input\n")
            with self.assertRaises(FileExistsError):
                self.census.run(7, 1, 0, Path(tmp))
            self.assertEqual(existing.read_text(), "keep this input\n")

    def test_negative_controls(self):
        # Two oppositely oriented triangles glued along their three edges are a sphere,
        # with the same unordered corner triple occurring twice (inadmissible).
        m = self.census.review.TriMap([[0, 1, 2], [3, 4, 5]],
                                     {0: 5, 5: 0, 1: 4, 4: 1, 2: 3, 3: 2},
                                     [0, 1, 2, 0, 2, 1])
        self.census.review.check(m, 3, 0)
        self.assertFalse(self.census.admissible(m))
        with self.assertRaises(AssertionError):
            self.census.review.check(m, 3, 1)
        m.alpha[0] = 0
        with self.assertRaises(AssertionError):
            self.census.review.check(m, 3, 0)

    def test_sample_pairing_and_catalogue_comparison(self):
        samples = json.loads((self.census.ROOT /
                              "reviews/strategy-review-2026-11-03-maps.json").read_text())
        for key, records in samples["maps"].items():
            n, genus = map(int, key.split("_"))
            for rec in records:
                m = self.census.from_links(rec["links"])
                self.census.review.check(m, n, genus)
                self.assertEqual(self.census.admissible(m), rec["distinct_corners"])

    def test_saved_censuses_and_controls(self):
        root = HERE / "results"
        exports = json.loads((root / "exports.json").read_text())
        for name, meta in exports.items():
            raw = gzip.decompress((root / meta["archive"]).read_bytes())
            self.assertEqual(hashlib.sha256(raw).hexdigest(), meta["source_sha256"])
            self.assertEqual(self.census.sha256(root / name), meta["sha256"])
            original = json.loads(raw)
            result = json.loads((root / name).read_text())
            self.assertTrue(result["complete"])
            self.assertEqual(result["graphs_done"], result["graphs_total"])
            original_codes = {tuple(map(tuple, m["code"])) for m in original["maps"]}
            codes = {tuple(map(tuple, m["code"])) for m in result["maps"]}
            self.assertEqual(original_codes, codes)
            self.assertEqual(len(codes), result["classes"])
            for m in result["maps"]:
                self.assertEqual(m, json.loads(json.dumps(self.census.record(
                    m["code"], result["n"], result["genus"]))))
            source_dir = (root / meta["source"]).parent
            manifest = json.loads((source_dir / "manifest.json").read_text())
            for filename, digest in manifest["files"].items():
                if filename == "enum_multi":
                    continue  # Compiled executables are hashed, not archived.
                payload = raw if filename.startswith("maps_") else (source_dir / filename).read_bytes()
                self.assertEqual(hashlib.sha256(payload).hexdigest(), digest)

        samples = json.loads((self.census.ROOT /
                              "reviews/strategy-review-2026-11-03-maps.json").read_text())["maps"]
        for key, records in samples.items():
            result = json.loads((root / f"maps_{key}.json").read_text())
            wanted = {self.census.from_links(r["links"]).canon()[0] for r in records}
            actual = {tuple(map(tuple, r["code"])) for r in result["maps"]}
            self.assertEqual(actual, wanted)

        catalog = json.loads((self.census.ROOT / "data/k12_triangulations.json").read_text())
        result = json.loads((root / "maps_12_6.json").read_text())
        actual = {tuple(map(tuple, m["code"])): m for m in result["maps"]}
        self.assertEqual(len(actual), 59)
        for rec in catalog:
            code = self.census.from_links([rec["links"][str(v)] for v in range(12)]).canon()[0]
            self.assertIn(code, actual)
            self.assertEqual(actual[code]["aut_plus"], rec["aut_orient_preserving_order"])
            self.assertEqual(actual[code]["reflexible"], not rec["chiral"])

        c3 = json.loads((root / "c3-verified.json").read_text())
        manifest = json.loads((root / "c3-verified.manifest.json").read_text())
        self.assertEqual(self.census.sha256(root / "c3-verified.json"), manifest["output_sha256"])
        self.assertTrue(c3["complete"])
        focus = json.loads((root / "maps_9_3.json").read_text())["maps"]
        symmetric = {tuple(map(tuple, m["code"])) for m in focus if m["admissible"]
                     and any(a[0] == 3 and a[1] == a[2] == 0 for a in m["autos"])}
        self.assertEqual(len(symmetric), 8)
        self.assertEqual(symmetric, {tuple(map(tuple, code)) for code in c3["codes"]})

    def test_focus_census_reproduces_saved_codes(self):
        saved = json.loads((HERE / "results/maps_9_3.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            result = self.census.run(9, 3, 60, Path(tmp))
        self.assertTrue(result["complete"])
        self.assertEqual({tuple(map(tuple, m["code"])) for m in result["maps"]},
                         {tuple(map(tuple, m["code"])) for m in saved["maps"]})



if __name__ == "__main__":
    unittest.main()
