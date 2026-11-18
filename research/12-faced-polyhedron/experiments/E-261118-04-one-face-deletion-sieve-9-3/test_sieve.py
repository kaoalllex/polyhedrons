"""Unit tests of the deleted-face formula (no solving): encoder identity, monotonicity, Roest-Vigh's planes."""
import unittest

from sieve import build_deleted, deleted_cnf, pilot, roest_vigh, units, ALL_OPTS
from omsat import Eval, build, chirotope_from_planes
from omsat_validate import uniform


def full(T):
    c = pilot.CNF(T.n)
    build(c, T, ALL_OPTS)
    return c


class SieveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.T = pilot.from_links(pilot.census(9, 3)['maps'][0]['links'])
        cls.rv_planes, cls.rv = roest_vigh()

    def test_units(self):
        u = units()
        self.assertEqual(len(u), 203 * 9)
        self.assertEqual(len(set(u)), len(u))

    def test_no_deletion_is_the_encoder(self):
        for T in (self.T, self.rv):
            a, b = deleted_cnf(T, None), full(T)
            self.assertEqual((a.nv, a.clauses), (b.nv, b.clauses))

    def test_deleted_is_a_prefix_of_the_full_formula(self):
        ref = full(self.T)
        for S in range(9):
            d = deleted_cnf(self.T, S)
            f = pilot.CNF(9)
            build_deleted(f, self.T, S, phases=('kept', 'own'))
            self.assertEqual((f.nv, len(f.clauses), f.tags), (ref.nv, len(ref.clauses), ref.tags))
            self.assertEqual(f.clauses[:len(d.clauses)], d.clauses)
            self.assertGreater(len(f.clauses), len(d.clauses))
            self.assertGreater(d.tags['TRIPLE'], 0)
            self.assertGreater(d.tags['POC'], 0)

    def test_roest_vigh_planes_satisfy_every_deleted_formula(self):
        chi = chirotope_from_planes(self.rv_planes)
        for S in (None, *range(8)):
            B = Eval(8, chi)
            build_deleted(B, self.rv, S)
            self.assertEqual(B.violations, [], S)

    def test_shifted_planes_violate_every_deleted_formula(self):
        planes, T = roest_vigh(shifted=True)
        chi = chirotope_from_planes(planes)
        self.assertTrue(uniform(chi))
        for S in (None, *range(8)):
            B = Eval(8, chi)
            build_deleted(B, T, S)
            self.assertGreater(len(B.violations), 0, S)


if __name__ == '__main__':
    unittest.main()
