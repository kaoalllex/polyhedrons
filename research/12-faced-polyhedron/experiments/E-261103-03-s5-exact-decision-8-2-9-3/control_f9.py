"""Positive control (c) of the item 1 launch: a convex F-face simple polyhedron (genus 0), exact rational derivation.

Writes control_fF.json (F = 9 unless --faces F): integer planes [a, b, c, d] (inside is a x + b y + c z + d <= 0) and the
cyclic face links (counter-clockwise seen from outside); negative_links is the map of another polyhedron.
Usage: python3 control_f9.py [--faces F] [--check]"""
import itertools
import json
from fractions import Fraction as F
from math import ceil, sqrt
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'code'))
from ladder_exact import solve3
from omsat import chirotope_from_planes


def polyhedron(rows):
    pts = {}
    for t in itertools.combinations(range(len(rows)), 3):
        try:
            p = solve3([rows[i] for i in t])
        except AssertionError:
            continue
        val = [sum(r[j] * p[j] for j in range(3)) + r[3] for r in rows]
        if any(v > 0 for v in val):
            continue
        if sum(v == 0 for v in val) != 3:
            raise ValueError('not simple')
        pts[t] = p
    links = {}
    for x in range(len(rows)):
        corners = [t for t in pts if x in t]
        if len(corners) < 3:
            raise ValueError('missing face')
        nbr = {}
        for t in corners:
            a, b = [y for y in t if y != x]
            nbr.setdefault(a, []).append(b); nbr.setdefault(b, []).append(a)
        n = rows[x][:3]
        centre = [sum(pts[t][j] for t in corners) / len(corners) for j in range(3)]
        first = min(nbr); order = [first]; prev = None
        while True:
            nxt = [y for y in nbr[order[-1]] if y != prev][0] if prev is not None else nbr[order[-1]][0]
            prev, cur = order[-1], nxt
            if cur == first:
                break
            order.append(cur)
        def corner(a, b):
            return pts[tuple(sorted((x, a, b)))]
        a, b = corner(order[-1], order[0]), corner(order[0], order[1])
        u = [a[j] - centre[j] for j in range(3)]; v = [b[j] - centre[j] for j in range(3)]
        cross = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        if sum(cross[j] * n[j] for j in range(3)) < 0:
            order.reverse()
        links[x] = order
    return links, len(pts)


def build(seed=2611080300, faces=9):
    rng = random.Random(seed)
    while True:
        rows = []
        for _ in range(faces):
            nrm = [rng.randint(-9, 9) for _ in range(3)]
            if any(nrm):
                rows.append(nrm + [-ceil(sqrt(sum(v * v for v in nrm)))])
        if len(rows) < faces:
            continue
        try:
            links, nv = polyhedron(rows)
        except ValueError:
            continue
        if nv == 2 * faces - 4 and all(v for v in chirotope_from_planes(rows).values()):
            return rows, links


if __name__ == '__main__':
    f = int(sys.argv[sys.argv.index('--faces') + 1]) if '--faces' in sys.argv else 9
    rows, links = build(faces=f)
    other = build(2611080301, faces=f)[1]  # a different labelled F-face map for the negative control
    assert other != links
    path = HERE / f'control_f{f}.json'
    data = dict(planes=rows, links={str(k): v for k, v in links.items()},
                negative_links={str(k): v for k, v in other.items()},
                note=f'convex simple {f}-face polyhedron, V={2 * f - 4} E={3 * f - 6} F={f}, chi=2; '
                     'inside: a x + b y + c z + d <= 0')
    if '--check' in sys.argv:
        assert json.loads(path.read_text()) == data
    else:
        path.write_text(json.dumps(data, indent=1) + '\n')
    print(rows, links)
