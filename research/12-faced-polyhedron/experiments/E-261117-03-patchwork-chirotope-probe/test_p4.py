"""Unit tests of p4.py (seconds): certificate edge cases, exact recompute, chart, a planted C1 solve."""
import itertools
import json
import unittest

from ortools.sat.python import cp_model

import p4


class P4Tests(unittest.TestCase):
    def test_embedded_2x2_unique_minimum_is_certified(self):
        W = [[0, 0, 9, 9], [0, 1, 9, 9], [9, 9, 0, 9], [9, 9, 9, 0]]
        want, ok, detail = p4.c0_case(W)
        self.assertEqual(want, (1, 0, 2, 3))
        self.assertTrue(ok, detail)

    def test_all_ties_are_rejected(self):
        want, ok, detail = p4.c0_case([[0] * 4 for _ in range(4)])
        self.assertIsNone(want)
        self.assertTrue(ok, detail)

    def test_planted_exact_recompute_and_chart(self):
        W, Sg, chi = p4.planted(1, n=7)
        self.assertEqual(p4.exact_chi(p4.exact_matrix(W, Sg, 25)), chi)
        rz = p4.realize(W, Sg, 1, chi)
        self.assertTrue(rz['combinatorial_match'] and rz['charted_chi_match'] and rz['q'] is not None)

    def test_chart_keeps_a_finite_chart(self):
        planes = json.loads(p4.SZ.read_text())['planes']
        H = [list(h) for h in planes] + [[0, 0, 0, 1]]
        self.assertEqual(p4.chirotope_from_planes(p4.chart(H)), p4.chirotope_from_planes(planes))
        self.assertEqual(p4.chirotope_from_planes(p4.chart(H[::-1][1:][::-1] + [[0, 0, 0, 3]])),
                         p4.chirotope_from_planes(planes))

    def test_planted_c1_is_found_and_flipped_sign_is_not(self):
        W, Sg, chi = p4.planted(2, n=6)
        rec = p4.c1_unit(('planted', chi, None, None, (16,), 30))
        self.assertEqual(rec['ladder'][-1]['status'], 'OPTIMAL')
        rz = rec['ladder'][-1]['realize']
        self.assertTrue(rz['combinatorial_match'] and rz['charted_chi_match'])
        S, bad = p4.flipped(chi)
        self.assertFalse(p4.gp_ok(bad, 6))
        self.assertTrue(p4.gp_ok(chi, 6))
        rec = p4.c1_unit(('negative', bad, None, None, (16,), 10))
        self.assertNotIn(rec['ladder'][-1]['status'], ('OPTIMAL', 'FEASIBLE'))

    def test_sign_constraint_matches_brute_force(self):
        """Fixed weights and signs: the model accepts exactly the combinatorial chirotope and rejects its negation
        on one minor."""
        W, Sg, chi = p4.planted(3, n=5)
        for flip in (None, (0, 1, 2, 3)):
            m = cp_model.CpModel()
            P = p4.P4(m, 5, 12, normalise=False, fixed_w=W)
            for i, j in itertools.product(range(5), range(4)):
                m.Add(P.sig[i][j] == int(Sg[i][j] < 0))
            m.Add(P.eps == 0)
            for S in itertools.combinations(range(5), 4):
                P.minor(S, int((chi[S] < 0) ^ (S == flip)))
            _, st, _ = p4.solve(m, 30)
            self.assertEqual(st, 'OPTIMAL' if flip is None else 'INFEASIBLE')


if __name__ == '__main__':
    unittest.main()
