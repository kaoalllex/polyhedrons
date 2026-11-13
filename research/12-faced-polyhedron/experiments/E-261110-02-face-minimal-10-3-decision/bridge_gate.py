"""Bridge gate of PLAN.md (2026-11-12 amendment) on the S6 (10,2) witness map, through the night's code.

G1 pinned: the witness planes' chirotope as unit clauses on the night's sub-map formula (tranche.submap_formula):
   SAT expected.
G2 unpinned: the same formula without units: SAT expected (a foreign model: the solver never sees coordinates).
G3 bridge: the G2 model through the night's SAT processing (tranche.bridge: hinge, two_stage, fp with tranche.BRIDGE,
   no start planes, then `verify_candidate.py --target S6` on the saved file); PASS only if it returns a candidate that
   passes with the witness's (V, E, F, chi). The witness planes are read only for G1 and to record chi agreement.
Usage: python3 bridge_gate.py OUT_DIR   (kissat at $SAT_SOLVER, default ~/bin/kissat; drat-trim at $DRAT_TRIM)"""
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
os.environ.setdefault('SAT_SOLVER', str(Path.home() / 'bin/kissat'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
import pilot  # noqa: E402
import tranche  # noqa: E402

WITNESS = ROOT / 'witnesses/s6_10_2.json'
EXPECTED = [24, 36, 10, -2]


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    data = json.loads(WITNESS.read_text())
    links = {int(k): v for k, v in data['links'].items()}
    report = dict(witness_sha256=pilot.sha(WITNESS), solver_sha256=pilot.sha(Path(pilot.CADICAL)),
                  drat_sha256=pilot.sha(Path(pilot.DRAT)), bridge=tranche.BRIDGE, gates={})
    r1 = r2 = {}
    try:
        c = tranche.submap_formula(10, links)
        witness_chi = pilot.chirotope_from_planes(data['planes'])
        c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in witness_chi.items()])
        report['gates']['G1_pinned'] = r1 = pilot.solve(c, out, 'g1_pinned', 600)
        c = tranche.submap_formula(10, links)
        report['gates']['G2_unpinned'] = r2 = pilot.solve(c, out, 'g2_unpinned', 3600)
        if r2['status'] == 'SAT':
            model = set(json.loads((out / 'g2_unpinned.model.json').read_text()))
            agree = sum((v in model) == (witness_chi[q] > 0) for q, v in c.qvar.items())
            g3 = report['gates']['G3_bridge'] = dict(chi_agree_with_witness=agree, chi_size=len(c.qvar))
            g3.update(tranche.bridge(out, 'g2_unpinned', c, links, 'S6'))
            log = out / 'g2_unpinned.candidate.log'
            line = log.read_text().splitlines()[0] if log.exists() else ''
            g3['V_E_F_chi'] = json.loads(line.split(' ', 1)[1])['V_E_F_chi'] if line.startswith('0 ') else None
            g3['PASS'] = g3['status_note'] == 'CANDIDATE-NEEDS-REVIEW' and g3['V_E_F_chi'] == EXPECTED
        report['PASS'] = (r1['status'] == 'SAT' and r2['status'] == 'SAT'
                          and report['gates'].get('G3_bridge', {}).get('PASS', False))
    finally:
        report['wall_seconds'] = time.monotonic() - started
        pilot.dump(out / 'gate.json', report)
    print(json.dumps(dict(PASS=report.get('PASS'), G1=r1.get('status'), G2=r2.get('status'),
                          G3=report['gates'].get('G3_bridge', {}).get('status_note'))))
    return 0 if report.get('PASS') else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
