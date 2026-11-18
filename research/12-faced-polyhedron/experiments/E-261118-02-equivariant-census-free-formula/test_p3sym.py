"""Unit tests of P3-sym: group bookkeeping, forced zeros (with an exact geometric check), normal forms, one pinned solve."""
import random
import unittest

from p3sym import C3, D2, S4, GROUP, ORDER, fixtures, forced_zeros, group, invariant, normal_form, pinned, quad_orbits
from omsat import chirotope_from_planes, det4


class P3SymTests(unittest.TestCase):
    def test_quad_orbits_match_the_lead_review(self):
        self.assertEqual((quad_orbits(8, D2), quad_orbits(8, S4), quad_orbits(9, C3)), (36, 34, 72))

    def test_group_orders_and_inconsistent_determinants(self):
        self.assertEqual([len(group(8, D2)), len(group(8, S4)), len(group(9, C3))], [4, 4, 3])
        g = (1, 0, 2, 3, 4, 5, 6, 7)
        with self.assertRaises(ValueError):
            group(8, [(g, 1), (g, -1)])

    def test_forced_zeros(self):
        self.assertEqual([forced_zeros(8, D2), forced_zeros(8, S4), forced_zeros(9, C3)], [[], [], []])
        self.assertIn((0, 1, 2, 3), forced_zeros(8, [((1, 2, 3, 0, 5, 6, 7, 4), 1)]))          # C4
        self.assertIn((0, 1, 2, 3), forced_zeros(7, [((1, 0, 3, 2, 5, 4, 6), -1)]))            # Cs 3 x 2 + 1
        self.assertIn((0, 1, 6, 7), forced_zeros(7, [((1, 0, 3, 2, 5, 4, 6), 1)]))             # C2 3 x 2 + 1
        self.assertIn((0, 1, 2, 3), forced_zeros(9, [((1, 0, 3, 2, 5, 4, 7, 6, 8), -1)]))      # Cs 4 x 2 + 1

    def test_forced_zeros_are_geometric(self):
        rng = random.Random(26111802)
        r = lambda: [rng.choice([i for i in range(-9, 10) if i]) for _ in range(4)]
        for _ in range(20):
            a, b = r(), r()
            mirror = lambda h: [h[0], h[1], -h[2], h[3]]               # z -> -z
            half = lambda h: [-h[0], -h[1], h[2], h[3]]                # half-turn about z
            self.assertEqual(det4([a, mirror(a), b, mirror(b)]), 0)    # two mirror pairs are concurrent
            self.assertEqual(det4([a, half(a), [0, 0, 1, b[3]], [0, 0, 0, 1]]), 0)   # a half-turn pair, its fixed face, INF
            self.assertNotEqual(det4([a, half(a), b, half(b)]), 0)

    def test_normal_forms(self):
        fx = fixtures()
        for name in ('roest_vigh', 'mizhaev'):
            h = normal_form(fx[name][0], ORDER[name], GROUP[name])
            chi = chirotope_from_planes(h)
            self.assertTrue(invariant(chi, [], 8, GROUP[name]))
            self.assertFalse(invariant(chi, [], 8, S4 if name == 'roest_vigh' else D2))

    def test_pinned_roest_vigh(self):
        h = normal_form(fixtures()['roest_vigh'][0], ORDER['roest_vigh'], D2)
        r = pinned('rv', h, D2)
        self.assertEqual((r['status'], r['EMBEDDED'], r['invariant'], r['V_E_F_chi']), ('OPTIMAL', True, True, [24, 36, 8, -4]))
        self.assertEqual(pinned('rv_s4', h, S4)['status'], 'INFEASIBLE')


if __name__ == '__main__':
    unittest.main()
