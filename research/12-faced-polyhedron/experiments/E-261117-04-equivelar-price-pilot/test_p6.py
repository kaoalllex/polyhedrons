"""Unit tests of p6.py (PLAN.md, stage A; amendment 1, stage B; amendment 2, stage C), run before compute:
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



class StageCTests(unittest.TestCase):
    """Amendment 2: the plain (9, 4) pass on the admissible classes."""

    @classmethod
    def setUpClass(cls):
        cls.recs = json.loads(p6.MAPS_C.read_text())['maps']

    def test_k2_codes(self):
        k2 = p6.k2_codes()
        self.assertEqual(len(set(k2)), 10)
        pats = [p6.pattern(p6.links_of(t, 9)) for t in k2]
        self.assertEqual(pats[:8], ['+'.join(map(str, q)) for q in p6.partitions(9)])
        self.assertEqual(pats[8:], ['9', '3+2+2+2'])
        shas = [p6.B.code_sha(json.loads(t)) for t in k2]
        self.assertEqual(shas[8][:12], '2ecc586672c5'); self.assertEqual(shas[9][:12], '205d0f6d2d57')

    def test_build_is_reproducible_and_chunked(self):
        controls, counts, recs = p6.build_c(check=True)  # asserts the committed maps file and both queues
        self.assertTrue(all(controls.values()))
        self.assertEqual((counts['records'], counts['chunk0'], counts['symmetric']), (1071, 91, 111))
        self.assertEqual([r['k2'] for r in recs[:10]], list(range(10)))
        self.assertTrue(all(r['chunk'] == 0 for r in recs[:91]) and all(r['chunk'] == 1 for r in recs[91:]))
        self.assertEqual(len({r['canonical_sha256'] for r in recs}), 1071)
        order = [r['pattern'] for r in recs[91:]]
        self.assertEqual(order, sorted(order, key=counts['chunk1_order'].index))

    def test_queues(self):
        q0 = json.loads((p6.HERE / 'queue_stageC_c0.json').read_text())
        q1 = json.loads((p6.HERE / 'queue_stageC_c1.json').read_text())
        for q, n, first in ((q0, 91, 0), (q1, 980, 91)):
            self.assertEqual((q['case'], q['control_file'], q['shards'], q['lean_unsat']), ([9, 4], 'control_f9.json',
                                                                                          10, True))
            self.assertEqual(q['maps_sha256'], p6.B.sha(p6.MAPS_C))
            ctrl = [r for r in q['maps'] if r.get('control')]
            self.assertEqual(sorted(r['index'] for r in ctrl),
                             sorted(f'control-f9{neg}-s{s}' for neg in ('', '-neg') for s in range(10)))
            self.assertTrue(all(r['control_sha256'] == p6.B.sha(p6.F9) for r in ctrl))
            units = [r for r in q['maps'] if not r.get('control')]
            self.assertEqual([r['index'] for r in units], list(range(first, first + n)))
            self.assertTrue(all(r['solver_cap'] == 60 and r['seed'] == 0 for r in units))
            self.assertTrue(all(r['canonical_sha256'] == self.recs[r['index']]['canonical_sha256'] for r in units))
            for s in range(10):
                self.assertEqual([r.get('control') for r in q['maps'][s::10][:2]], ['positive', 'negative'])

    def test_plain_record_builds_the_10_element_formula(self):
        c = tranche.submap_formula(9, dict(enumerate(self.recs[0]['links'])))
        self.assertEqual(len(c.qvar), 210)  # 4-subsets of 10 elements: 9 planes and the plane at infinity

    def test_price_summary_and_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / 'stageC_c0'; (d / '0').mkdir(parents=True)
            rows = [dict(map_index='control-f9-s0', status='SAT', seconds=0.1),
                    dict(map_index='control-f9-neg-s0', status='UNSAT-SOLVER', seconds=0.1)]
            for i, r in enumerate(self.recs[:91]):
                rows.append(dict(map_index=i, status='TIMEOUT' if i == 0 else 'UNSAT-SOLVER', budget_seconds=60,
                                 seconds=60.0 if i == 0 else 2.0))
            (d / '0/results.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
            solver = 60 + 90 * 2.0
            (d / 'budget.json').write_text(json.dumps({'0:x': 2 * solver}))
            out = p6.price([d])
            todo = Counter(r['pattern'] for r in self.recs if r['chunk'] == 1)
            mean = {p: (2.0 if p != '9' else (60 + 13 * 2.0) / 14) for p in todo}
            want = 2 * sum(n * mean[p] for p, n in todo.items())
            self.assertEqual(out['projected_core_s'], round(want))
            self.assertEqual(out['projected_wall_s'], round(want / 10 * 1.5))
            self.assertEqual((out['units'], out['sampled'], out['unpriced_patterns']), (980, 91, []))
            s = p6.summary([d], p6.MAPS_C)
            self.assertTrue(s['controls_pass']); self.assertEqual(s['controls'], 2)
            self.assertEqual(s['k2'], {0: 'TIMEOUT', **{k: 'UNSAT-SOLVER' for k in range(1, 10)}})
            written = {}
            write, p6.write = p6.write, lambda path, text, check: written.update({path.name: json.loads(text)})
            try:
                p6.followup([d], 'stageC')
            finally:
                p6.write = write
            q = written['queue_stageC_retry.json']
            self.assertEqual([r['index'] for r in q['maps'] if not r.get('control')], [0])
            self.assertEqual(q['maps'][-1]['solver_cap'], 600); self.assertEqual(q['case'], [9, 4])


if __name__ == '__main__':
    unittest.main()
