"""Prep controls (b) and (d) of PLAN.md through the night's sub-map formula (tranche.submap_formula), kissat, DRAT.

(b1) Szilassi's planes pinned on its own coherent links: SAT.  (b2) the Lutz-imported 7-vertex torus (control (a)
shows it is the Szilassi map), unpinned: SAT.  (d) the S3 genus-3 witness `lab_type0_genus3` (12 faces, 48 of 66 pairs)
pinned on its planes (rounded at 1e9, as every exact check): SAT.  Exit 0 iff all three are SAT.
Usage: python3 prep_controls.py MAPS_7_1_JSON OUT_DIR"""
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
os.environ.setdefault('SAT_SOLVER', str(Path.home() / 'bin/kissat'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
sys.path.insert(0, str(ROOT / 'code'))
import pilot  # noqa: E402
import tranche  # noqa: E402
from gauss_degree import coherent_triangles, links_from  # noqa: E402
from omsat_validate import szilassi  # noqa: E402

S3 = ROOT / 'experiments/E-261030-03-genus-ladder-type0-genus3/results/type0_genus3_extendable_polished.json'


def pinned(links, planes):
    c = tranche.submap_formula(len(links), links)
    c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in pilot.chirotope_from_planes(planes).items()])
    return c


def main(maps71, out):
    out.mkdir(parents=True, exist_ok=False)
    report = {}
    planes, T = szilassi()[:2]
    links = {int(k): v for k, v in links_from(coherent_triangles([tuple(t) for t in T.tris]), 7).items()}
    report['b1_szilassi_pinned'] = pilot.solve(pinned(links, planes), out, 'b1_szilassi_pinned', 120)
    torus = json.loads(Path(maps71).read_text())['maps'][0]
    report['b2_lutz_torus_unpinned'] = pilot.solve(tranche.submap_formula(7, dict(enumerate(torus['links']))), out,
                                                   'b2_lutz_torus_unpinned', 120)
    s3 = json.loads(S3.read_text())
    links = {int(k): v for k, v in links_from(coherent_triangles([tuple(t) for t in s3['triangles']]), 12).items()}
    planes = [[int(round(v * 10 ** 9)) for v in h] for h in s3['planes']]
    report['d_s3_genus3_pinned'] = pilot.solve(pinned(links, planes), out, 'd_s3_genus3_pinned', 600)
    report['inputs_sha256'] = {str(p.relative_to(ROOT.parents[1])): pilot.sha(p) for p in (S3, ROOT.parents[1] / 'index.html')}
    report['inputs_sha256']['maps_7_1'] = pilot.sha(Path(maps71))
    report['PASS'] = all(report[k]['status'] == 'SAT' for k in report if k[0] in 'bd')
    pilot.dump(out / 'controls.json', report)
    print(json.dumps({k: v['status'] if isinstance(v, dict) and 'status' in v else v for k, v in report.items()
                      if k != 'inputs_sha256'}))
    return 0 if report['PASS'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], Path(sys.argv[2]).resolve()))
