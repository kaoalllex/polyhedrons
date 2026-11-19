"""Amendment 1 control: the plane-only symmetry clauses and the build_sym gauge at 12 elements, on the exact
involution of each of the 20 (11, 5) Aut+ = 2 maps (the two drawn ones and, amendment 2, the other 18).

For each map: random integer planes symmetric under the half-turn (x, y, z) -> (-x, -y, z) acting as the map's
involution (the fixed face gets a plane z = d, each swapped pair (a, g a) gets h and its image), a far plane as
infinity (E-261117-02 `n2.chart`), the moved chirotope brought to the build_sym gauge (`n2.gauge`) and pinned into the
formula of the map with only the Grassmann-Pluecker clauses plus the symmetry and gauge clauses (`triples` and the
corner families off). Must be SAT for every draw: an UNSAT would mean the symmetry or gauge clauses exclude genuine
symmetric configurations, so a fast UNSAT of the full formula could be an artifact. The unpinned formula must be SAT.
Usage: python3 controls_12.py OUT_JSON"""
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'experiments/E-261117-02-moved-chart-plane-symmetry'))
sys.path.insert(0, str(HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'))
from omsat import chirotope_from_planes  # noqa: E402
from omsat_sym import build_sym, closure  # noqa: E402
from n2 import chart, gauge, pin, sat  # noqa: E402
import pilot  # noqa: E402

OPTS = dict(gp=True, triples=False, inconsist=False, reflex=False, reflexconsist=False, poc=False,
            sym_planes_only=True)
DRAWS = 5


def symmetric_planes(g, rng):
    n = len(g); h = [None] * n
    for a in range(n):
        if h[a] is not None:
            continue
        if g[a] == a:
            h[a] = [0, 0, rng.choice([-1, 1]), rng.randint(-9, 9) or 1]
        else:
            r = [rng.choice([v for v in range(-9, 10) if v]) for _ in range(4)]
            h[a], h[g[a]] = r, [-r[0], -r[1], r[2], r[3]]
    return h


def main(out):
    recs = [r for f in ('formulas.json', 'formulas_rest.json') for r in json.loads((HERE / 'maps' / f).read_text())['maps']]
    report = {}
    for rec in [r for r in recs if r['seed'] == 0]:
        links = dict(enumerate(rec['links'])); n = len(links)
        tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
        t = pilot.Triangulation(n, tris, links=links, submap=True)
        G = sorted(closure([tuple(rec['sym_generator'])], n))
        c, basis, orbs = build_sym(t, G, {x: 1 for x in G}, OPTS)
        rng = random.Random(2611180311 + rec['census_index']); rows = []
        while len(rows) < DRAWS:
            h = symmetric_planes(rec['sym_generator'], rng)
            moved = chart(h)
            if moved is None:
                continue
            chi, flip = gauge(chirotope_from_planes(moved[1]), G, n)
            rows.append(dict(far_plane=moved[0], flipped=flip, **sat(pin(c, chi), 120)))
        free = sat(c.clauses, 120)
        report[rec['census_index']] = dict(pinned=rows, unpinned=free, orbits=orbs,
                                           PASS=all(r['status'] == 'SAT' for r in rows) and free['status'] == 'SAT')
    report['PASS'] = all(v['PASS'] for v in report.values())
    Path(out).write_text(json.dumps(report, indent=1, default=str) + '\n')
    print(json.dumps({k: (v['PASS'] if isinstance(v, dict) else v) for k, v in report.items()}))


if __name__ == '__main__':
    main(sys.argv[1])
