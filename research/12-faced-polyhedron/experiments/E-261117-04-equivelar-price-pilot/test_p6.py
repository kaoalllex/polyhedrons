"""Unit tests of p6.py (PLAN.md, stage A and amendment 1, stage B), run before the census and the formulas:
python3 -m unittest test_p6"""
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
        self.assertEqual(list(p6.partitions(9)), [(9,), (7, 2), (6, 3), (5, 4), (5, 2, 2), (4, 3, 2), (3, 3, 3),
                                                  (3, 2, 2, 2)])

    def test_cycle_unions_are_the_2_regular_patterns(self):
        for n in (8, 9):
            for parts in p6.partitions(n):
                edges = p6.cycle_union(parts)
                self.assertEqual(len(edges), n)
                self.assertTrue(all(a != b for a, b in edges))
                deg = Counter(v for e in edges for v in e)
                self.assertEqual(sorted(deg.values()), [2] * n)
                self.assertEqual(components(edges, n), sorted(parts, reverse=True))

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


class StageBTests(unittest.TestCase):
    """Amendment 1: the (9, 4) census in root-stride units."""

    def test_census_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = p6.S.census.run(9, 4, 0, Path(tmp) / 'a', graphs=[p6.cycle_union((9,))], stride=30, offset=29)
            self.assertFalse(r['complete'])  # nine extra edges accepted; a zero time limit is a partial run
            self.assertEqual((r['stride'], r['offset']), (30, 29))
            with self.assertRaises(ValueError):  # twelve extra edges
                p6.S.census.run(7, 3, 0, Path(tmp) / 'b')
            with self.assertRaises(ValueError):
                p6.S.census.run(8, 3, 0, Path(tmp) / 'c', graphs=[p6.cycle_union((8,))], stride=3, offset=3)

    def test_root_stride_split_covers_the_unsplit_run(self):
        g = [p6.cycle_union((4, 2, 2))]
        with tempfile.TemporaryDirectory() as tmp:
            whole = p6.S.census.run(8, 3, 60, Path(tmp) / 'w', graphs=g)
            parts = [p6.S.census.run(8, 3, 60, Path(tmp) / str(o), graphs=g, stride=3, offset=o) for o in range(3)]
        self.assertTrue(whole['complete'] and all(r['complete'] for r in parts))
        self.assertEqual(whole['seeded'], whole['roots'])
        self.assertTrue(all(r['roots'] == whole['roots'] for r in parts))
        self.assertEqual(sum(r['seeded'] for r in parts), whole['roots'])
        codes = lambda r: {json.dumps(m['code']) for m in r['maps']}
        self.assertEqual(set().union(*map(codes, parts)), codes(whole))
        self.assertEqual(len(codes(whole)), 6)  # 4+2+2 in stage A: 6 classes

    def test_units(self):
        u = p6.units(9, 4)
        self.assertEqual(len(u), 8 * 30)
        self.assertEqual(u[:8], [(parts, 0) for parts in p6.partitions(9)])
        self.assertEqual(len({p6.unit_dir(9, 4, p, o) for p, o in u}), 240)
        self.assertEqual(p6.unit_dir(9, 4, (3, 3, 3), 7, True).name, '3+3+3-o07-r')
        self.assertEqual(len(p6.units(8, 3)), 7 * 3)

    def test_symmetric_lists(self):
        eq = {f: {t for t in p6.B.maps_of(f) if p6.equivelar(p6.links_of(t, 9))} for f in ('C3_9_4', 'C2f_9_4')}
        both = eq['C3_9_4'] | eq['C2f_9_4']
        self.assertEqual(len(both), 111)  # K2 of the final lead review 2026-11-22
        self.assertEqual(Counter(p6.pattern(p6.links_of(t, 9)) for t in both),
                         Counter({'9': 50, '7+2': 16, '5+4': 16, '6+3': 8, '5+2+2': 8, '3+2+2+2': 8, '4+3+2': 4,
                                  '3+3+3': 1}))

    def test_face_transitive_9_4(self):
        ft = json.loads(p6.FT_9_4.read_text())['maps']
        self.assertEqual(len(ft), 2)
        self.assertTrue(all(p6.equivelar(m['links']) and not m['admissible'] for m in ft))

    def test_has_rotation(self):
        rec = {'autos': [(2, 1, 1, 0), (3, 0, 0, 0)]}
        self.assertTrue(p6.has_rotation(rec, 3, 0) and p6.has_rotation(rec, 2, 1))
        self.assertFalse(p6.has_rotation(rec, 2, 0) or p6.has_rotation(rec, 3, 3))

    def test_merge_flags_incomplete_patterns_and_mismatches(self):
        ref = json.loads((p6.CENSUS / 'maps_8_3.json').read_text())['maps']
        mine = [m for m in ref if p6.pattern(m['links']) == '4+2+2']
        with tempfile.TemporaryDirectory() as tmp:
            census_dir, p6.census_dir = p6.census_dir, lambda n, g: Path(tmp)
            try:
                for o, maps in ((0, mine), (1, [dict(mine[0], aut_plus=-1)])):
                    d = p6.unit_dir(8, 3, (4, 2, 2), o); d.mkdir(parents=True)
                    (d / 'manifest.json').write_text(json.dumps(dict(exit_status=0, wall_seconds=1,
                                                                     finished_utc='x')))
                    (d / 'maps_8_3.json').write_text(json.dumps(dict(complete=True, classes=len(maps), roots=9,
                                                                     seeded=3, seconds=1, maps=maps)))
                out, controls, maps = p6.merge(8, 3, prune=True)
                self.assertFalse(out['complete'])
                self.assertEqual(out['patterns']['4+2+2']['offsets_complete'], 2)
                self.assertFalse(out['patterns']['4+2+2']['complete'])
                self.assertEqual(len(maps), 6)
                self.assertFalse(controls['no_record_mismatch'])
                self.assertFalse(controls['stage_a_census_reproduced'])
                self.assertTrue((d / 'maps_8_3.json').exists())  # nothing pruned while incomplete
                line = p6.census_b(8, 3, budget=0)
                self.assertEqual((line['stop_reason'], line['pending']), ('budget', 19))
                self.assertEqual(p6.census_b(8, 3, wall=0)['stop_reason'], 'wall')
            finally:
                p6.census_dir = census_dir


if __name__ == '__main__':
    unittest.main()
