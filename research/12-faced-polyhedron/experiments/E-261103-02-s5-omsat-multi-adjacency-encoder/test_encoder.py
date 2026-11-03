"""Bounded regressions for the multi-adjacency extension (no target solving)."""
import itertools
import json
import gzip
import hashlib
import random
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'code'))
from omsat import Triangulation
from control_rost_vigh import build as roest_vigh
from ladder_exact import verify
from omsat import chirotope_from_planes
from omsat_validate import eval_all, compare_direct, cnf_check, szilassi, uniform, ALL_OPTS
from omsat_sym import build_sym


def controls():
    h, links = roest_vigh()
    d = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())
    sh, st, _, _ = szilassi()
    return [('roest_vigh', h, from_links(links)),
            ('mizhaev', d['planes_abcd_zero_form'], from_links(d['links_0based'])), ('szilassi', sh, st)]


def perturb(h, seed=7):
    rng = random.Random(seed)
    for _ in range(100):
        p = [[1000000 * v + rng.randint(-3, 3) for v in row] for row in h]
        if uniform(chirotope_from_planes(p)):
            return p
    raise AssertionError('no uniform perturbation within 100 tries')


def from_links(links):
    links = {int(k): v for k, v in links.items()} if isinstance(links, dict) else dict(enumerate(links))
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items()
                   for a, b in zip(link, link[1:] + link[:1])})
    return Triangulation(len(links), tris, links)


class EncoderTests(unittest.TestCase):
    def test_saved_full_control_evidence(self):
        out = Path(__file__).resolve().parent / 'results/0'
        if not (out / 'manifest.json').exists():
            self.skipTest('full control artifacts have not been generated yet')
        manifest = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(manifest['exit_status'], 0)
        for name, digest in manifest['outputs_sha256'].items():
            self.assertEqual(hashlib.sha256((out / name).read_bytes()).hexdigest(), digest, name)
        summary = json.loads((out / 'summary.json').read_text())
        self.assertEqual(summary['status'], 'PASS')
        self.assertEqual(summary['trials_per_object'], 1000)
        for name, _, t in controls():
            r = summary['controls'][name]
            self.assertEqual(r['status'], 'SAT')
            self.assertEqual(r['backend_check']['named_mismatch'], 0)
            self.assertEqual(r['perturbations']['accepted'], 1000)
            self.assertEqual(r['perturbations']['mismatches'], 0)
            self.assertGreater(r['perturbations']['embedded'], 0)
            self.assertGreater(r['perturbations']['defective'], 0)
            with gzip.open(out / (name + '.perturbations.jsonl.gz'), 'rt') as stream:
                samples = [json.loads(line) for line in stream]
            self.assertEqual(len(samples), 1000)
            self.assertTrue(all(not s['mismatches'] for s in samples))
            # Replay every radius cell, including configurations with defects.
            for sample in samples[:6]:
                _, ev = eval_all(sample['planes'], t)
                mism, emb, _ = compare_direct(sample['planes'], t, ev, {})
                self.assertEqual(mism, [])
                self.assertEqual(emb, sample['embedded'])
        from controls import unit_refutes, s0_regression
        self.assertTrue(s0_regression())
        for name in ('roest_vigh', 'mizhaev', 'szilassi', 'C2_free', 'C3_free'):
            model = set(json.loads((out / (name + '.model.json')).read_text()))
            with gzip.open(out / (name + '.cnf.gz'), 'rt') as stream:
                for line in stream:
                    if line[0] not in 'cp':
                        self.assertTrue(any(int(x) in model for x in line.split()[:-1]))
        for name in ('roest_vigh_on_mizhaev', 'C2_fixed', 'D3'):
            with gzip.open(out / (name + '.cnf.gz'), 'rt') as stream:
                clauses = [[int(x) for x in line.split()[:-1]] for line in stream if line[0] not in 'cp']
            self.assertTrue(unit_refutes(clauses))
        self.assertEqual(summary['negative_pairing'], 'REJECTED')
        self.assertFalse(summary['first_8_2']['solved'])

    def test_own_map_eval_geometry_and_pinned_cnf(self):
        for name, h, t in controls():
            with self.subTest(name=name):
                h = h if uniform(chirotope_from_planes(h)) else perturb(h)
                _, ev = eval_all(h, t)
                self.assertEqual(ev.violations, [])
                mism, embedded, _ = compare_direct(h, t, ev, {})
                self.assertEqual(mism, [])
                self.assertTrue(embedded)
                self.assertTrue(cnf_check(h, t)['sat'])

    def test_symmetric_builder_uses_face_count(self):
        _, _, t = controls()[0]
        identity = tuple(range(t.n))
        c, basis, orbits = build_sym(t, [identity], {identity: 1}, ALL_OPTS)
        self.assertEqual(c.n, 8)
        self.assertEqual(len(c.qvar), 126)
        self.assertTrue(all(q[-1] == 8 for q in basis))

    def test_parallel_segments_use_link_pairing(self):
        _, links = roest_vigh()
        t = from_links(links)
        for x, link in links.items():
            for i, y in enumerate(link):
                endpoints = {link[i - 1], link[(i + 1) % len(link)]}
                self.assertIn(frozenset(endpoints), [frozenset(s) for s in t.segments(x, y)])
                for z in endpoints:
                    self.assertEqual({t.other_partner(x, y, z)}, endpoints - {z})

    def test_one_sided_parallel_pairing_is_rejected(self):
        _, links = roest_vigh()
        x = next(x for x, link in links.items() if len(set(link)) < len(link))
        y = next(y for y in links[x] if links[x].count(y) == 2)
        i, j = [i for i, z in enumerate(links[x]) if z == y]
        # Reverse the arc between copies: same two edge occurrences, different endpoint pairing.
        links[x][i + 1:j] = reversed(links[x][i + 1:j])
        with self.assertRaises((AssertionError, ValueError)):
            from_links(links)

    def test_all_nonadmissible_census_maps_are_rejected_without_geometry(self):
        d = json.loads((ROOT / 'experiments/E-261103-01-s5-map-census/results/maps_9_3.json').read_text())
        bad = [m for m in d['maps'] if not m['admissible']]
        self.assertEqual(len(bad), 37)
        for m in bad:
            links = dict(enumerate(m['links']))
            r = verify([[0, 0, 0, 0]] * 9, links)
            self.assertFalse(r['EMBEDDED'])
            with self.assertRaises((AssertionError, ValueError)):
                from_links(links)

    def test_census_admissible_maps_include_tripled_edges(self):
        for f, g in ((8, 2), (9, 3)):
            d = json.loads((ROOT / f'experiments/E-261103-01-s5-map-census/results/maps_{f}_{g}.json').read_text())
            for m in d['maps']:
                if m['admissible']:
                    t = from_links(m['links'])
                    self.assertEqual(sum(len(t.segments(x, y)) for x, y in itertools.combinations(range(f), 2)),
                                     3 * (f + 2 * g - 2))


if __name__ == '__main__':
    unittest.main()
