"""E-261113-03 prep regressions: frozen list and cell membership, the rank-4 count against enumeration and sampling,
the count gate on a truncated vertex list, and the canonical map (invariance and separation)."""
from pathlib import Path
import random
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import census
cells = census.cells


class CensusTests(unittest.TestCase):
    def test_frozen_list_and_membership(self):
        units = census.load_units()
        self.assertEqual(len(units), 25531)
        self.assertEqual([u['ordinal'] for u in units], list(range(len(units))))
        h = cells.source_planes(census.SOURCE)
        for d in census.deletions(h):
            D = cells.duals([r for i, r in enumerate(h) if i != d])
            mine = [u for u in units if u['deletion'] == d]
            planted = [u for u in mine if u['planted']]
            self.assertEqual(len(planted), 1)
            self.assertEqual(planted[0]['key'], cells.key_str(cells.key_of(D, h[d])))
            for u in mine[::211]:
                self.assertEqual(cells.key_str(cells.key_of(D, [cells.Fr(v) for v in u['eighth']])), u['key'])
        self.assertEqual({frozenset(u['deletion'] for u in units if u['ordinal'] % 10 == k) for k in range(10)},
                         {frozenset({0, 4})})

    def small(self):
        rng = random.Random(7)
        while True:
            h = [[rng.randint(-9, 9) for _ in range(4)] for _ in range(4)]
            try:
                D = cells.duals(h)
            except ValueError:
                continue
            if len(D) == 10 and cells.rank(D) == 4:
                return D

    def test_count_matches_enumeration_and_sampling(self):
        D = self.small()
        union, nv, _ = census.enumerate_cells(D)
        count, nflats = census.zaslavsky_rank4(D)
        self.assertEqual((len(union), nv), (count, nflats))
        self.assertTrue(all(cells.key_of(D, p) == k for k, p in union.items()))
        mc = census.monte_carlo(D, union, 20000, 1)
        self.assertEqual(mc['missing'], 0)

    def test_count_gate_catches_missing_vertices(self):
        D = self.small(); V = census.vertices(D)
        with mock.patch.object(census, 'vertices', lambda D: V[:2]):
            union, _, _ = census.enumerate_cells(D)
        self.assertLess(len(union), census.zaslavsky_rank4(D)[0])

    def test_map_canon(self):
        fx = {n: links for n, _, links in census.base.fixtures()}
        rv = census.map_canon(fx['roest_vigh'])
        self.assertNotEqual(rv, census.map_canon(fx['mizhaev']))   # same (V, E, F), different maps
        for s in range(10):
            rng = random.Random(s); perm = list(range(8)); rng.shuffle(perm); L = {}
            for f, c in fx['roest_vigh'].items():
                c = [perm[x] for x in c]; k = rng.randrange(len(c)); c = c[k:] + c[:k]
                L[perm[int(f)]] = c[::-1] if rng.random() < .5 else c
            self.assertEqual(census.map_canon(L), rv)


if __name__ == '__main__':
    unittest.main()
