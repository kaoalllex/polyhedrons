"""Enumerator controls against the independent census of E-261103-01 (no target maps)."""
import json
from pathlib import Path
import unittest

import cayley

CENSUS = cayley.ROOT / 'experiments/E-261103-01-s5-map-census/results'


def census_codes(F, genus, keep=lambda m: True):
    maps = json.loads((CENSUS / f'maps_{F}_{genus}.json').read_text())['maps']
    return {tuple(map(tuple, m['code'])) for m in maps if m['admissible'] and keep(m)}


def vertex_regular(m, F):
    # Free action of a group of order |Aut+| = F: no non-identity automorphism fixes a vertex.
    return m['aut_plus'] == F and all(fixed_v == 0 for _, fixed_v, _, _ in m['autos'])


class Groups(unittest.TestCase):
    def test_groups_are_pairwise_distinct(self):
        for F, make in cayley.GROUPS.items():
            groups = make()
            self.assertTrue(all(G.n == F for G in groups))
            spectra = [G.spectrum() for G in groups]
            self.assertEqual(len(set(spectra)), len(groups))

    def test_order_eight_spectra(self):
        q8 = cayley.quaternion(); d4 = cayley.dihedral(4)
        self.assertEqual(sum(o == 2 for o in q8.order), 1)
        self.assertEqual(sum(o == 2 for o in d4.order), 5)

    def test_valency(self):
        self.assertEqual(cayley.valency(9, 4), 10)
        self.assertEqual(cayley.valency(8, 3), 9)
        self.assertIsNone(cayley.valency(9, 3))


class Census(unittest.TestCase):
    def codes(self, F, genus, method):
        _, maps = cayley.run(F, genus, method, workers=2)
        return {tuple(map(tuple, m['code'])) for m in maps if m['admissible']}

    def test_k7_both_methods(self):
        expected = census_codes(7, 1)
        self.assertEqual(len(expected), 1)
        self.assertEqual(self.codes(7, 1, 'brute'), expected)
        self.assertEqual(self.codes(7, 1, 'by_phi'), expected)

    def test_k12_equals_vertex_regular_census_classes(self):
        expected = census_codes(12, 6, lambda m: vertex_regular(m, 12))
        self.assertEqual(self.codes(12, 6, 'by_phi'), expected)


class Symmetry(unittest.TestCase):
    def test_link_automorphisms_and_free_c3_on_the_9_3_census(self):
        import formulas
        maps = json.loads((CENSUS / 'maps_9_3.json').read_text())['maps']
        with_c3 = 0
        for m in maps:
            if not m['admissible']:
                continue
            aut, gens = formulas.free_c3_classes(m['links'])
            self.assertEqual(aut, m['aut_plus'])
            with_c3 += bool(gens)
            if gens:
                self.assertIsNotNone(formulas.pilot.free_c3(m['links']))
        self.assertEqual(with_c3, 8)   # STATUS.md section 3c: eight admissible maps with a free C3


if __name__ == '__main__':
    unittest.main()
