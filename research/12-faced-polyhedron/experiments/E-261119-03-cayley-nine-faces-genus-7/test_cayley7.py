"""Controls for rho_dfs: the exact brute set per labelling on small rungs, and the census classes K7, K12."""
import itertools
import json
import unittest

import cayley7

cayley = cayley7.cayley
CENSUS = cayley7.ROOT / 'experiments/E-261103-01-s5-map-census/results'


def census_codes(F, genus, keep=lambda m: True):
    maps = json.loads((CENSUS / f'maps_{F}_{genus}.json').read_text())['maps']
    return {tuple(map(tuple, m['code'])) for m in maps if m['admissible'] and keep(m)}


class RhoDfs(unittest.TestCase):
    def assert_same_as_brute(self, F, genus, per_group):
        k = cayley.valency(F, genus)
        hits = 0
        for G in cayley.GROUPS[F]():
            for labels, iota in itertools.islice(cayley.labellings(G, k), per_group):
                a = set(cayley.brute(G, labels, iota)); b = list(cayley7.rho_dfs(G, labels, iota))
                self.assertEqual(len(b), len(set(b)))
                self.assertEqual(set(b), a, (G.name, labels, iota))
                hits += len(a)
        return hits

    def test_brute_set_on_k7(self):
        self.assertGreater(self.assert_same_as_brute(7, 1, None), 0)

    def test_brute_set_on_order_eight(self):
        self.assertGreater(self.assert_same_as_brute(8, 3, 4), 0)

    def test_rejects_everything_brute_rejects_at_9_4_z9(self):
        G = cayley.GROUPS[9]()[0]
        for labels, iota in cayley.labellings(G, 10):
            self.assertEqual(list(cayley7.rho_dfs(G, labels, iota)), [])

    def test_census_classes_k7_k12(self):
        for F, genus, keep in ((7, 1, lambda m: True),
                               (12, 6, lambda m: m['aut_plus'] == 12 and all(v == 0 for _, v, _, _ in m['autos']))):
            _, maps = cayley7.run(F, genus, 'rho_dfs', workers=2)
            self.assertEqual({tuple(map(tuple, m['code'])) for m in maps if m['admissible']},
                             census_codes(F, genus, keep))

    def test_valency_genus_7(self):
        self.assertEqual(cayley.valency(9, 7), 14)
        self.assertIsNone(cayley.valency(9, 5))
        self.assertIsNone(cayley.valency(9, 6))


if __name__ == '__main__':
    unittest.main()
