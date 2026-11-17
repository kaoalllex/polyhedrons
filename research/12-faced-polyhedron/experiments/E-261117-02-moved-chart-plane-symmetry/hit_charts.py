"""Descriptive, not in the verdict: for every saved hit, the sign of the old homogeneous coordinate
w = (1 + n . v') / R at each solid vertex v' of the moved chart (X = M^-1 (v', 1), see n2.py). All positive: the
vertices lie in the standard affine chart; mixed: the solid crosses the old plane at infinity, so it exists only in
a moved chart. For c2 hits also whether the links are invariant under the draw's half-turn (0)(1 2)(3 4)(5 6), up to
cyclic order and reversal (necessary for a symmetric solid, not sufficient). Usage: python3 hit_charts.py results/hits"""
from fractions import Fraction
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'code'))
from ladder_exact import solve3

out = {}
for p in sorted(Path(sys.argv[1]).glob('*.json')):
    r = json.loads(p.read_text())
    links = {int(k): v for k, v in r['links'].items()}
    nrm = [-x for x in r['far_plane'][:3]]
    corners = {tuple(sorted((x, l[i], l[(i + 1) % len(l)]))) for x, l in links.items() for i in range(len(l))}
    w = [1 + sum(Fraction(a) * b for a, b in zip(nrm, solve3([r['planes'][i] for i in t]))) > 0 for t in corners]
    out[p.stem] = dict(vertices=len(corners), old_w_positive=sum(w), in_standard_chart=all(w))
    if p.stem.startswith('c2'):
        g = [0, 2, 1, 4, 3, 6, 5]
        out[p.stem]['links_half_turn_invariant'] = all(
            any([g[y] for y in links[x]] == row[k:] + row[:k] for row in (links[g[x]], links[g[x]][::-1])
                for k in range(len(row))) for x in links)
print(json.dumps(out, indent=1))
