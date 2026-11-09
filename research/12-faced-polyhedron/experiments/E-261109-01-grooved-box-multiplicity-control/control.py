"""Run the grooved-box controls through the S5 encoder (submap=True) with the E-261103-03 solve/check path.
Usage: python3 control.py OUT_DIR   (units: pinned positive/negative for k = 2, 3; unpinned positive for k = 2)"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / 'E-261103-03-s5-exact-decision-8-2-9-3'))
import pilot
from ladder_exact import verify


def formula(links, planes=None):
    links = {int(k): v for k, v in links.items()}
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
    c = pilot.CNF(len(links)); pilot.build(c, pilot.Triangulation(len(links), tris, links=links, submap=True), pilot.ALL_OPTS)
    if planes is not None:
        c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in pilot.chirotope_from_planes(planes).items()])
    return c


def main(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    results = {}
    for k in (2, 3):
        d = json.loads((HERE / f'control_k{k}.json').read_text())
        planes = d['planes']; H = [[float(v) for v in r] for r in planes]
        for tag, links in (('pos', d['links']), ('neg', d['negative_links'])):
            L = {int(a): b for a, b in links.items()}
            o = verify(H, L, require_all_pairs=False)
            results[f'k{k}-{tag}-exact'] = dict(V_E_F_chi=o['V_E_F_chi'], corner_triples_distinct=o['corner_triples_distinct'],
                                                edges_consistent=o['edges_consistent'], EMBEDDED=o['EMBEDDED'])
            name = f'k{k}_{tag}_pinned'
            r = pilot.solve(formula(links, planes), out, name, 120, checker_timeout=120)
            r['expected'] = 'SAT' if tag == 'pos' else pilot.UNSAT_OK
            results[name] = r
            print(name, r['status'], 'expected', r['expected'], flush=True)
    r = pilot.solve(formula(json.loads((HERE / 'control_k2.json').read_text())['links']), out, 'k2_pos_unpinned', 900, checker_timeout=120)
    r['expected'] = 'SAT (TIMEOUT = no information)'
    results['k2_pos_unpinned'] = r
    print('k2_pos_unpinned', r['status'], flush=True)
    pilot.dump(out / 'result.json', results)


if __name__ == '__main__':
    main(sys.argv[1])
