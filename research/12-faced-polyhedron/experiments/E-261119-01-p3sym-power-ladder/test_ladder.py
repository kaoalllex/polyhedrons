"""Unit tests of the E-261119-01 additions: normaliser, run images, the run predicate, map blocking (pinned)."""
import unittest

import ladder as L
from omsat import chirotope_from_planes


class LadderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.N = L.normaliser(8, L.C2)
        cls.obj = {}
        for name in ('roest_vigh', 'mizhaev'):
            h = L.known(name, L.C2)
            rec, chi, cells, runs = L.pinned_model(h, L.C2)
            cls.obj[name] = dict(rec=rec, chi=chi, cells=cells, runs=runs)

    def test_normaliser_and_domain(self):
        self.assertEqual(len(self.N), 384)                     # C2 wr S4
        self.assertEqual(L.p3sym.forced_zeros(8, L.C2), [])
        g = L.C2[0][0]
        self.assertTrue(all(tuple(n[g[n.index(i)]] for i in range(8)) == g for n in self.N))   # n g n^-1 = g

    def test_invariant_copies(self):
        for name, want in (('roest_vigh', 240), ('mizhaev', 96)):
            R = self.obj[name]['runs']
            copies = {L.image(R, p) for p in L.copy_perms(R, 8, L.C2)}
            self.assertEqual(len(copies), want, name)
            self.assertLessEqual({L.image(R, n) for n in self.N}, copies)

    def test_image(self):
        runs = frozenset({(0, 1, 2, 3), (4, 6, 5, 7)})
        n = (1, 0, 2, 3, 4, 5, 6, 7)
        self.assertEqual(L.image(runs, n), frozenset({(0, 1, 2, 3), (4, 6, 5, 7)}))
        self.assertEqual(L.image(runs, (2, 1, 0, 3, 4, 5, 6, 7)), frozenset({(1, 2, 0, 3), (4, 6, 5, 7)}))

    def test_known_objects_pinned_under_free_c2(self):
        for name, o in self.obj.items():
            self.assertEqual((o['rec']['status'], o['rec']['invariant'], o['rec']['E']), ('OPTIMAL', True, 36), name)
            self.assertEqual(L.p3sym.known_type(o['rec']['links']), name)
            self.assertEqual(L.predicate_runs(o['chi'], o['cells'], 8), o['runs'], name)

    def test_pinned_blocking(self):
        rv, mz = self.obj['roest_vigh'], self.obj['mizhaev']
        for blocked, want in ((rv, 'INFEASIBLE'), (mz, 'OPTIMAL')):
            f = L.BlockFormula(8, L.C2, edges=36, chi=rv['chi'])
            f.block_map(blocked['runs'], L.copy_perms(blocked['runs'], 8, L.C2))
            self.assertEqual(f.solve(120)['status'], want)

    def test_same_end_triples_other_pairing(self):
        rv = self.obj['roest_vigh']; R = rv['runs']
        line = next(r[:2] for r in sorted(R) if sum(x[:2] == r[:2] for x in R) == 2)
        pairs = sorted(r[2:] for r in R if r[:2] == line); e = sorted(set(pairs[0] + pairs[1]))
        for P in (((e[0], e[1]), (e[2], e[3])), ((e[0], e[2]), (e[1], e[3])), ((e[0], e[3]), (e[1], e[2]))):
            syn = frozenset({r for r in R if r[:2] != line} | {line + p for p in P})
            f = L.BlockFormula(8, L.C2, edges=36, chi=rv['chi']); f.pin_cells(rv['cells'])
            f.block_map(syn, [tuple(range(8))])
            own = sorted(P) == pairs
            self.assertEqual(f.solve(60)['status'], 'INFEASIBLE' if own else 'OPTIMAL', P)
            self.assertEqual(all(line + p in L.predicate_runs(rv['chi'], rv['cells'], 8) for p in P), own)


if __name__ == '__main__':
    unittest.main()
