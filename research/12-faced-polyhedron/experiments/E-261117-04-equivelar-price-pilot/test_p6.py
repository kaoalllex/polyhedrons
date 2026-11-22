"""Unit tests of p6.py (PLAN.md, stage A), run before the census and the formulas: python3 -m unittest test_p6"""
from collections import Counter
import json
from pathlib import Path
import tempfile
import unittest

import p6
import tranche  # noqa: E402  (on sys.path through p6)


def components(edges, n):
    parent = list(range(n))

    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for a, b in edges:
        parent[find(a)] = find(b)
    return sorted(Counter(find(v) for v in range(n)).values(), reverse=True)


class P6Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.known = p6.S.known_8_3_codes()
        cls.free = p6.B.maps_of('C2_8_3')
        cls.H, cls.rv = p6.control_rost_vigh.build()

    def test_partitions(self):
        self.assertEqual(list(p6.partitions(8)), [(8,), (6, 2), (5, 3), (4, 4), (4, 2, 2), (3, 3, 2), (2, 2, 2, 2)])
        self.assertEqual(len(list(p6.partitions(9))), 8)

    def test_cycle_unions_are_the_2_regular_patterns(self):
        for parts in p6.partitions(8):
            edges = p6.cycle_union(parts)
            self.assertEqual(len(edges), 8)
            self.assertTrue(all(a != b for a, b in edges))
            deg = Counter(v for e in edges for v in e)
            self.assertEqual(sorted(deg.values()), [2] * 8)
            self.assertEqual(components(edges, 8), sorted(parts, reverse=True))

    def test_census_rejects_a_wrong_input_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                p6.S.census.run(8, 3, 1, Path(tmp) / 'out', graphs=[[(0, 1)]])

    def test_known_maps_equivelar_patterns(self):
        pats = {k: p6.pattern(p6.links_of(t)) for k, t in self.known.items()}
        self.assertTrue(all(p6.equivelar(p6.links_of(t)) for t in self.known.values()))
        self.assertEqual(sorted(pats.values()), ['4+4', '8'])

    def test_free_c2_list(self):
        self.assertEqual(len(self.free), 790)
        self.assertEqual(sum(p6.equivelar(p6.links_of(t)) for t in self.free), 45)
        self.assertTrue(set(self.known.values()) <= set(self.free))

    def test_free_half_turn(self):
        self.assertTrue(p6.free_half_turn({'autos': [(2, 0, 4, 0)]}))
        self.assertFalse(p6.free_half_turn({'autos': [(2, 2, 0, 0), (4, 0, 0, 0)]}))
        ft = json.loads(p6.FT.read_text())['maps']
        self.assertTrue(p6.free_half_turn(ft[0]))  # Roest-Vigh's class: SAT under its free half-turns (E-261119-02)

    def test_pinned_control_calibration(self):
        rv_list = [self.rv[i] for i in range(8)]
        self.assertEqual(p6.violations(self.H, self.rv), 0)
        eq = {t for t in self.free if p6.equivelar(p6.links_of(t))}
        neg, t = p6.negative_links(rv_list, self.known['roest_vigh'], eq)
        self.assertNotEqual(t, self.known['roest_vigh'])
        self.assertEqual(p6.doubled(neg), p6.doubled(rv_list))
        self.assertGreater(p6.violations(self.H, neg), 0)

    def test_queue_layout(self):
        with tempfile.NamedTemporaryFile('w', dir=p6.HERE, suffix='.json') as f, \
                tempfile.NamedTemporaryFile('w', dir=p6.HERE, suffix='.json') as c:
            f.write('{}'); f.flush(); c.write('{}'); c.flush()
            control, p6.CONTROL = p6.CONTROL, Path(c.name)
            try:
                recs = [dict(seed=0, canonical_sha256=str(i)) for i in range(25)]
                q = p6.queue(Path(f.name), range(25), recs, 60)
            finally:
                p6.CONTROL = control
        rows = q['maps']
        for s in range(10):
            mine = rows[s::10]
            self.assertEqual([r.get('control') for r in mine[:2]], ['positive', 'negative'])
            self.assertFalse(any(r.get('control') for r in mine[2:]))
        self.assertEqual(q['case'], [8, 3]); self.assertTrue(q['lean_unsat'])
        self.assertTrue((p6.B.RUNNER / q['control_file']).resolve().parent == p6.HERE)

    def test_plain_record_builds_the_generator_free_formula(self):
        links = p6.links_of(self.known['mizhaev'])
        c = tranche.submap_formula(8, dict(enumerate(links)))
        self.assertEqual(len(c.qvar), 126)  # 4-subsets of 9 elements: 8 planes and the plane at infinity
        self.assertGreater(len(c.clauses), 0)


if __name__ == '__main__':
    unittest.main()
