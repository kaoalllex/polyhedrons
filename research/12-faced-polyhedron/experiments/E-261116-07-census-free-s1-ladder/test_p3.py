"""Unit tests of P3 v2 (PLAN: pinch, annulus, disk + annulus, ends, face cycles). Pinned chirotopes only."""
import itertools
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3  # noqa: E402
from omsat import chirotope_from_planes  # noqa: E402


def tilted(lines, zs, seed):
    """Vertical planes a x + b y + c = 0 and horizontal planes z = z0, all slightly tilted, scaled to integers,
    redrawn until the chirotope (with infinity) is uniform."""
    rng = random.Random(seed)
    for _ in range(200):
        rows = [[1000 * a + rng.randint(-9, 9), 1000 * b + rng.randint(-9, 9), rng.choice([-1, 1]) * rng.randint(3, 9),
                 1000 * c] for a, b, c in lines]
        rows += [[rng.randint(-9, 9), rng.randint(-9, 9), 1000, -1000 * z] for z in zs]
        if all(v != 0 for v in chirotope_from_planes(rows).values()):
            return rows
    raise AssertionError('no uniform tilt')


def side(row, p):
    v = sum(a * b for a, b in zip(row[:3], p)) + row[3]
    return v > 0


def all_cells(chi, F):
    out = set()
    for t in itertools.combinations(range(F), 3):
        others = [k for k in range(F) if k not in t]
        U = sum(1 << r for r, k in enumerate(others) if p3.sigma(chi, F, t, k) > 0)
        out |= {p3.octant_cell(F, t, U, others, q) for q in range(8)}
    return out


def line(p, q):
    """a x + b y + c = 0 through p and q."""
    a, b = q[1] - p[1], p[0] - q[0]
    return a, b, -(a * p[0] + b * p[1])


OUTER = [(0, 0), (24, 0), (12, 20)]
INNER = [(10, 5), (14, 5), (12, 9)]


def ring_planes(extra, seed=3):
    lines = [line(OUTER[i], OUTER[(i + 1) % 3]) for i in range(3)] + [line(INNER[i], INNER[(i + 1) % 3]) for i in range(3)]
    return tilted(lines + extra, [0, 1], seed)


def pinned(rows, solid_of, **kw):
    F = len(rows); chi = chirotope_from_planes(rows)
    cells = {T for T in all_cells(chi, F) if solid_of(T, rows)}
    f = p3.Formula(F, chi=chi, all_pairs=False, **kw)
    for T in range(1 << F):
        f.model.Add(f.x[T] == (1 if T in cells else 0))
    return f, cells


def signs(T, k):
    return bool(T >> k & 1)


def ring_member(T, rows, centroid=(12, 7, .5), inner_ref=(12, 6.5, .5)):
    # planes 0-2 outer, 3-5 inner, then extras, last two z0, z1
    F = len(rows)
    inside_outer = all(signs(T, k) == side(rows[k], centroid) for k in range(3))
    inside_inner = all(signs(T, k) == side(rows[k], inner_ref) for k in range(3, 6))
    zmid = signs(T, F - 2) == side(rows[F - 2], (0, 0, .5)) and signs(T, F - 1) == side(rows[F - 1], (0, 0, .5))
    return inside_outer and zmid and not inside_inner


class Patterns(unittest.TestCase):
    def test_pinch_pattern(self):
        occ = sum(1 << q for q in (0, 1, 3, 7))
        self.assertIn(occ, p3.ALLOWED_SET)
        self.assertFalse(p3.pattern_ok(occ))

    def test_ends_zero_or_three(self):
        ok = [occ for occ in range(256) if p3.pattern_ok(occ)]
        self.assertTrue(ok)
        for occ in ok:
            self.assertIn(sum(p3.pattern_ends(occ)), (0, 3), bin(occ))
        self.assertTrue(any(sum(p3.pattern_ends(occ)) == 3 for occ in ok))


class Disks(unittest.TestCase):
    def test_annulus(self):
        rows = ring_planes([])
        z0 = len(rows) - 2
        f, cells = pinned(rows, ring_member, disk_planes=[])
        r = f.solve(60)
        self.assertEqual(r['status'], 'OPTIMAL')
        self.assertEqual(r['euler'][z0], 0)
        self.assertEqual(r['euler'][z0 + 1], 0)
        self.assertTrue(all(r['euler'][k] == 1 for k in range(6)))
        f, _ = pinned(rows, ring_member, disk_planes=[z0], connect=False)
        self.assertEqual(f.solve(60)['status'], 'INFEASIBLE')
        f, _ = pinned(rows, ring_member, disk_planes=list(range(6)))
        self.assertEqual(f.solve(60)['status'], 'OPTIMAL')

    def test_disk_plus_annulus(self):
        d1, d2 = (1, 0, -18), (1, 0, -20)          # x = 18 and x = 20 near the corner (24, 0)
        rows = ring_planes([d1, d2])
        F = len(rows); z0 = F - 2

        def member(T, rows):
            near = signs(T, 6) == side(rows[6], (12, 7, .5))          # on the ring's side of d1
            far = signs(T, 7) == side(rows[7], (22, 1, .5))            # beyond d2
            return (ring_member(T, rows) and near) or (far and ring_member(T, rows))
        f, _ = pinned(rows, member, disk_planes=[])
        r = f.solve(120)
        self.assertEqual(r['status'], 'OPTIMAL')
        self.assertEqual(r['euler'][z0], 1)
        f, _ = pinned(rows, member, disk_planes=[z0], connect=False)
        self.assertEqual(f.solve(120)['status'], 'OPTIMAL')
        f, _ = pinned(rows, member, disk_planes=[z0], connect=True)
        self.assertEqual(f.solve(120)['status'], 'INFEASIBLE')
        f, _ = pinned(rows, member, disk_planes=[6, 7], connect=True)    # single rectangles: connected disks
        self.assertEqual(f.solve(120)['status'], 'OPTIMAL')


class Extraction(unittest.TestCase):
    def test_roest_vigh_face_cycles(self):
        p05 = p3.load('E-261103-05-s5-symmetric-solid-first', 'pilot05')
        (_, h, links), = [fx for fx in p05.fixtures() if fx[0] == 'roest_vigh']
        planes = p05.integer_planes(h)
        a = p05.arrangement(planes); tables = p05.Tables(a)
        cells, info = p05.best_solid(a, tables, time_limit=60, target_edges=36, max_runs=3)
        self.assertIsNotNone(cells, info)
        solid = {tables.cells[i] for i, v in enumerate(cells) if v}
        want = p05.extract_links(a, solid)
        bits = [sum(1 << m for m, s in enumerate(T) if s > 0) for T in solid]
        d = p3.decode(chirotope_from_planes(planes), bits, 8)
        self.assertTrue(d['ok'], d['reason'])
        self.assertEqual((d['V'], d['E']), (24, 36))
        for i in range(8):
            self.assertTrue(p05.cyclic_equal(d['links'][i], want[i]), (i, d['links'][i], want[i]))

    def test_annulus_is_rejected(self):
        rows = ring_planes([])
        chi = chirotope_from_planes(rows)
        cells = [T for T in all_cells(chi, len(rows)) if ring_member(T, rows)]
        d = p3.decode(chi, cells, len(rows))
        self.assertFalse(d['ok'])
        self.assertIn('several boundary cycles', d['reason'])


if __name__ == '__main__':
    unittest.main()
