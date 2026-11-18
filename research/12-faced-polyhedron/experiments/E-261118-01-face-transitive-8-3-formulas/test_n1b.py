"""Unit tests of the N1b units and formulas (no solving): unit list, Roest-Vigh calibration, gauge, negatives."""
import unittest

from n1b import OPTS, classes, control_rost_vigh, gauge, links_of, pilot, units
from omsat import Eval, chirotope_from_planes


def violations(planes, links, kind):
    B = Eval(len(planes), chirotope_from_planes(planes))
    pilot.build(B, pilot.from_links(links), OPTS[kind])
    return len(B.violations)


class N1bTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        h, links = control_rost_vigh.build()
        cls.h, cls.links = h, [links[k] for k in range(8)]

    def test_units(self):
        self.assertEqual([m['reflexible'] for m in classes()], [False] * 4 + [True] * 2)
        u = units()
        self.assertEqual(len(u), (6 + 4) * 2)
        self.assertEqual(len(set(u)), len(u))
        self.assertEqual(u[0], (0, 'map', 'plain'))
        self.assertEqual(OPTS['plain'], pilot.ALL_OPTS)
        self.assertTrue(OPTS['normalised']['symbreak'] and OPTS['normalised']['mirror'])

    def test_mirror_links_are_a_map(self):
        for i in range(4):
            self.assertEqual(pilot.from_links(links_of(i, 'mirror')).n, 8)

    def test_roest_vigh_planes_satisfy_the_plain_formula_in_both_orientations(self):
        mirrored = [[a, b, -c, d] for a, b, c, d in self.h]
        self.assertEqual(violations(self.h, self.links, 'plain'), 0)
        self.assertEqual(violations(mirrored, [l[::-1] for l in self.links], 'plain'), 0)

    def test_gauge_is_unique_and_satisfies_the_normalised_formula(self):
        self.assertGreater(violations(self.h, self.links, 'normalised'), 0)
        (g,) = gauge(self.h, self.links)
        self.assertEqual(violations(g, self.links, 'normalised'), 0)

    def test_roest_vigh_planes_violate_the_other_classes(self):
        for i in range(1, 6):
            self.assertGreater(violations(self.h, links_of(i, 'map'), 'plain'), 0, i)


if __name__ == '__main__':
    unittest.main()
