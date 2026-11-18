"""Post-run diagnostic (conclusion, 2026-11-18): distinct labeled affine chirotopes per (arm, E) in the night.

The engine's verdict depends only on the affine arrangement, so units with equal labeled chirotopes of
(planes + the plane at infinity) are repeated tests. Infinity is (0, 0, 0, 1) for the standard chart and the recorded
far plane for c2. Exact integer determinants (Bareiss). Also reports the archived K13 draws and whether every class has
one status. Usage: python3 classes.py results > results/classes.json
"""
import collections
import glob
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
K13 = os.path.join(HERE, '../../reviews/dialogue-2026-11-16-strategy-checks/d2_rate.json')


def sign_det(m):
    m = [list(r) for r in m]; n = len(m); s = 1; prev = 1
    for c in range(n - 1):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return 0
        if p != c:
            m[c], m[p] = m[p], m[c]; s = -s
        for r in range(c + 1, n):
            for k in range(c + 1, n):
                m[r][k] = (m[r][k] * m[c][c] - m[r][c] * m[c][k]) // prev
        prev = m[c][c]
    d = m[n - 1][n - 1] * s
    return (d > 0) - (d < 0)


def chirotope(planes, infinity):
    v = [list(map(int, r)) for r in planes] + [list(map(int, infinity))]
    return tuple(sign_det([v[i] for i in q]) for q in itertools.combinations(range(len(v)), 4))


def report(groups):
    out = {}
    for key, rows in sorted(groups.items()):
        cls = collections.defaultdict(set)
        for planes, inf, status in rows:
            cls[chirotope(planes, inf)].add(status)
        out[key] = dict(units=len(rows), classes=len(cls),
                        classes_by_status={'/'.join(sorted(s)): n
                                           for s, n in collections.Counter(frozenset(v) for v in cls.values()).items()})
    return out


def main(results):
    groups = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(results, '[0-9]', 'results.jsonl'))):
        for line in open(f):
            r = json.loads(line)
            groups['%s_E%d' % (r['arm'], r['edges'])].append(
                (r['planes'], r['far_plane'] or [0, 0, 0, 1], r['status']))
    for r in json.load(open(K13))['rows']:
        groups['k13_archive_E36'].append((r['planes'], [0, 0, 0, 1], r['status']))
    json.dump(report(groups), sys.stdout, indent=1)
    print()


if __name__ == '__main__':
    main(sys.argv[1])
