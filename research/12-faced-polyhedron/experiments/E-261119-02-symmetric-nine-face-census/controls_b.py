"""E-261119-02 amendment 3 controls: the stage-B symmetric formulas on generic symmetric planes, on every pricing
record (maps/pricing.json: every stratum of both (9, 4) families).

Formula: the record's build_sym formula as stage B builds it (tranche.submap_formula: mirror and orbit-flip gauge on,
sym_planes_only as recorded) with only the Grassmann-Pluecker, symmetry and gauge clauses (`triples` and the corner
families off), so generic planes, which realize no map, can satisfy it.
* positive: random integer planes symmetric under the record's rotation (C2 4 x 2 + 1: the half-turn
  (x, y, z) -> (-x, -y, z), the fixed face z = d, moved chart by E-261117-02 `n2.chart`; C3: the cyclic coordinate
  rotation, standard chart), brought to the build_sym gauge (`n2.gauge`) and pinned. Must be SAT: an UNSAT would mean
  the symmetry or gauge clauses exclude genuine symmetric configurations, so stage B's fast UNSATs could be artifacts.
* wrong action: planes drawn the same way but symmetric under a conjugate rotation t g t (t a transposition with
  t g t != g; not a map automorphism), gauged for and pinned into the record's formula. Must be UNSAT: the symmetry
  clauses must reject planes that lack the record's symmetry.
* unpinned: the positive formula alone, SAT.
Usage: python3 controls_b.py OUT_JSON"""
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / 'E-261118-03-s5-11-5-plane-only-price-probe'))
sys.path.insert(0, str(HERE.parent / 'E-261103-02-s5-omsat-multi-adjacency-encoder'))
from controls_12 import OPTS, symmetric_planes as c2_planes  # noqa: E402
from controls import symmetric_planes as c3_planes  # noqa: E402
from n2 import chart, gauge, pin, sat  # noqa: E402
from omsat import chirotope_from_planes  # noqa: E402
from omsat_sym import build_sym, closure  # noqa: E402
import pilot  # noqa: E402

DRAWS, SEED, CAP = 5, 2611200301, 120


def formula(links, g, planes_only):
    n = len(links)
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
    t = pilot.Triangulation(n, tris, links=links, submap=True)
    G = sorted(closure([tuple(g)], n))
    return build_sym(t, G, {x: 1 for x in G}, dict(OPTS, sym_planes_only=planes_only))[0], G


def draw(g, planes_only, rng):
    """Uniform chirotope of planes symmetric under g, in the record's chart; None if this draw is degenerate."""
    if planes_only:
        moved = chart(c2_planes(g, rng))
        return None if moved is None else chirotope_from_planes(moved[1])
    chi = chirotope_from_planes(c3_planes(g, 3, rng.randrange(1 << 30)))
    return chi if all(chi.values()) else None


def wrong(g, rng):
    n = len(g)
    while True:
        a, b = rng.sample(range(n), 2)
        t = list(range(n)); t[a], t[b] = b, a
        h = [t[g[t[x]]] for x in range(n)]
        if h != list(g):
            return h


def main(out):
    recs = json.loads((HERE / 'maps/pricing.json').read_text())['maps']
    report = {}
    for i, rec in enumerate(recs):
        links = dict(enumerate(rec['links'])); n = len(links); g = rec['sym_generator']; po = rec['sym_planes_only']
        assert pilot.ALL_OPTS.keys() <= OPTS.keys(), 'every map clause family is switched off'
        c, G = formula(links, g, po)
        rng = random.Random(SEED + i); pos, neg = [], []
        while len(pos) < DRAWS:
            chi = draw(g, po, rng)
            if chi is None:
                continue
            pos.append(sat(pin(c, gauge(chi, G, n)[0]), CAP))
            h = wrong(g, rng)
            while (chi_w := draw(h, po, rng)) is None:
                pass
            neg.append(dict(wrong_generator=h, **sat(pin(c, gauge(chi_w, G, n)[0]), CAP)))
        free = sat(c.clauses, CAP)
        report[i] = dict(config=rec['config'], stratum=rec['stratum'], canonical_sha256=rec['canonical_sha256'],
                         positive=pos, wrong_action=neg, unpinned=free,
                         PASS=all(r['status'] == 'SAT' for r in pos) and all(r['status'] == 'UNSAT' for r in neg)
                         and free['status'] == 'SAT')
    report['PASS'] = all(v['PASS'] for v in report.values())
    Path(out).write_text(json.dumps(report, indent=1) + '\n')
    print('records', len(recs), 'pass', sum(v['PASS'] for k, v in report.items() if k != 'PASS'), 'PASS', report['PASS'])


if __name__ == '__main__':
    main(sys.argv[1])
