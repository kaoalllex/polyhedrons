"""Unit tests of the stage-A enumerator: group bookkeeping, demand classes, small exact controls, the action check."""
import json
import time
import unittest

import symcensus as S


def codes(name, seconds=120):
    s = S.setup(name); out = set(); deadline = time.monotonic() + seconds
    for di in range(len(s.reps)):
        for fi in range(len(s.fchoices)):
            r = S.run_unit(name, di, fi, deadline)
            assert r['complete'], (name, di, fi)
            for mp in r['maps']:
                assert S.check_action(mp['code'], mp['action'], s.p, sum(v == s.rho[v] for v in range(s.F)))
                out.add(json.dumps(mp['code']))
    return sorted(out)


class SymCensusTests(unittest.TestCase):
    def test_normalisers(self):
        self.assertEqual([len(S.normaliser(r)) for r in (S.C3_9, S.C2F_9, S.C2_8, S.C2F_7)], [324, 384, 384, 48])

    def test_c3_nine_faces_bookkeeping(self):
        s = S.setup('C3_9_4')
        self.assertEqual((len(s.pair_orbits), len(s.excess_vectors()), len(s.reps)), (12, 352, 18))
        self.assertEqual(len(s.fchoices), 1 + 8)                          # b = 0, or b = 3 with two orientations each
        self.assertEqual(len(S.setup('C3_9_3').fchoices), 12)             # b = 2: 3 support pairs x 4 orientations
        self.assertTrue(all(len(o) == 3 for o in s.rows))

    def test_c2_fixed_face_excludes_reversed_orbits(self):
        s = S.setup('C2f_9_4')
        self.assertEqual(len(s.bad_orbits), 4)                            # (a, rho a, 8) and its reverse
        self.assertEqual(s.fixed, [])
        self.assertTrue(all(len(o) == 2 for o in s.rows))

    def test_genus_five_bookkeeping(self):
        c3, c2 = S.setup('C3_9_5'), S.setup('C2f_9_5')
        self.assertEqual((c3.k, c3.V, len(c3.excess_vectors()), len(c3.reps)), (15, 34, 3432, 83))
        self.assertEqual(sorted(len(f) for f in c3.fchoices), [1] * 6)    # b = 1: 3 face orbits x 2 orientations
        self.assertEqual((len(c2.reps), len(c2.fchoices), c2.fixed), (12288, 1, []))
        for name in ('C3_9_4', 'C2f_9_4', 'C3_9_5', 'C2f_9_5'):
            self.assertEqual(len(S.setup(name).reps), S.burnside_classes(S.setup(name)))
        self.assertEqual(len(S.units('A')), 807)                          # stage A's recorded unit list
        self.assertEqual((len(S.units('A5c3')), len(S.units('A5c2'))), (24 + 498, 1 + 3 + 6 + 114 + 12288))

    def test_szilassi(self):
        t = S.census_truth()
        self.assertEqual(codes('C2f_7_1'), t['C2f_7_1'])
        self.assertEqual(t['C2f_7_1'], t['all_7_1'])

    def test_free_c2_eight_faces_genus_two(self):
        self.assertEqual(codes('C2_8_2'), S.census_truth()['C2_8_2'])

    def test_action_check_rejects_a_wrong_action(self):
        s = S.setup('C2f_7_1')
        r = S.run_unit('C2f_7_1', 0, 0, time.monotonic() + 60)
        mp = r['maps'][0]
        self.assertTrue(S.check_action(mp['code'], mp['action'], 2, 1))
        self.assertFalse(S.check_action(mp['code'], mp['action'], 2, 3))
        n = len(mp['action']); bad = list(mp['action']); bad[0], bad[1] = bad[1], bad[0]
        self.assertFalse(S.check_action(mp['code'], bad, 2, 1))
        self.assertFalse(S.check_action(mp['code'], list(range(n)), 2, 1))


if __name__ == '__main__':
    unittest.main()
