"""E-261118-01 (N1b): the plain and normalised S1 formulas (9 elements) of the six face-transitive (8, 3) classes of
E-261117-01, and of the mirror map of each chiral class (the census classes are up to reflection; the encoder's
invariance under reversing every link is not proved, so both orientations run). A SAT model goes through the bridge
of E-261103-03 (hinge, two_stage) and, if EMBEDDED, `verify_candidate.py --all-pairs`.

Usage: python3 n1b.py --shard K --shards N --cap SECONDS --budget SECONDS --out DIR   (one shard)
       python3 n1b.py --controls --cap SECONDS --out NEW_DIR
"""
import argparse
import itertools
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
import pilot  # noqa: E402  (E-261103-03: solve(), stage(), payload(), from_links(); SAT_SOLVER and NO_PROOF from env)
from omsat import Eval, chirotope_from_planes  # noqa: E402
import control_rost_vigh  # noqa: E402

MAPS = ROOT / 'experiments/E-261117-01-cayley-census-9-4/results/census/maps_8_3.json'
OPTS = {'plain': pilot.ALL_OPTS, 'normalised': dict(pilot.ALL_OPTS, symbreak=True, mirror=True)}
BRIDGE = dict(submap=False, restarts=6)


def classes():
    return json.loads(MAPS.read_text())['maps']


def units():
    """(class, orientation, formula): class-major, so class 0 (Roest-Vigh's, the positive control) comes first."""
    out = []
    for i, m in enumerate(classes()):
        for orient in ('map',) + (() if m['reflexible'] else ('mirror',)):
            out += [(i, orient, f) for f in OPTS]
    return out


def links_of(i, orient):
    links = classes()[i]['links']
    return links if orient == 'map' else [link[::-1] for link in links]


def formula(links, kind):
    c = pilot.CNF(len(links))
    pilot.build(c, pilot.from_links(links), OPTS[kind])
    return c


def pinned(c, planes):
    c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chirotope_from_planes(planes).items()])
    return c


def gauge(planes, links):
    """The representatives of the same polyhedron (planes reoriented, space reflected in z) meeting the normalised
    units; E-261114-01 SOUNDNESS.md says there is exactly one."""
    T = pilot.from_links(links)
    hits = []
    for m in (1, -1):
        for s in itertools.product((1, -1), repeat=len(planes)):
            p = [[si * a, si * b, si * m * c, si * d] for (a, b, c, d), si in zip(planes, s)]
            B = Eval(len(planes), chirotope_from_planes(p))
            pilot.build(B, T, OPTS['normalised'])
            if not B.violations:
                hits.append(p)
    return hits


def bridge(out, name, c, links):
    """The realization stages on one checked model; an EMBEDDED result is re-checked from its saved file."""
    model = set(json.loads((out / (name + '.model.json')).read_text()))
    chi = {q: 1 if v in model else -1 for q, v in c.qvar.items()}
    stages = {}
    for task in ('hinge', 'two_stage'):
        r = stages[task] = pilot.stage(out, f'{name}_{task}', task, pilot.payload(chi, links, **BRIDGE), 120)
        if r.get('geometry', {}).get('EMBEDDED'):
            cand = out / (name + '.candidate.json')
            pilot.dump(cand, dict(planes=r['planes'], links=dict(enumerate(links))))
            rc = pilot.command([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(cand), '--all-pairs'],
                               out / (name + '.candidate.log'), 60)
            return dict(bridge=stages, candidate=cand.name, all_pairs_rc=rc,
                        status_note='CANDIDATE-NEEDS-REVIEW' if rc == 0 else 'EMBEDDED-BUT-ALL-PAIRS-FAIL')
    best = min((s.get('wrong_signs') for s in stages.values() if s.get('wrong_signs') is not None), default=None)
    return dict(bridge=stages, best_wrong_signs=best, status_note='SAT-NOT-REALIZED')


def controls(out, cap):
    """Positive: Roest-Vigh's planes pinned on his own map, plain formula, and their gauge representative pinned on
    the normalised one: SAT. Negative: his planes pinned on the plain formulas of classes 1-5: UNSAT."""
    out.mkdir(parents=True, exist_ok=False)
    h, rv_links = control_rost_vigh.build()
    rv_links = [rv_links[k] for k in range(len(rv_links))]
    (g,) = gauge(h, rv_links)
    jobs = [('rv_own_map_pinned_plain', 'SAT', pinned(formula(rv_links, 'plain'), h)),
            ('rv_own_map_pinned_normalised', 'SAT', pinned(formula(rv_links, 'normalised'), g))]
    jobs += [(f'rv_planes_on_class{i}', pilot.UNSAT_OK, pinned(formula(links_of(i, 'map'), 'plain'), h)) for i in range(1, 6)]
    summary = {}
    for name, expected, c in jobs:
        r = pilot.solve(c, out, name, cap)
        r.update(expected=expected, passed=r['status'] == expected)
        summary[name] = r
        print(f'{name}: {r["status"]} {r["seconds"]:.1f} s (expected {expected})', flush=True)
    summary = dict(passed=all(r['passed'] for r in summary.values()), solver=os.path.basename(pilot.CADICAL),
                   cap=cap, controls=summary)
    pilot.dump(out / 'controls.json', summary)
    return summary['passed']


def done_keys(out):
    keys = set()
    for path in out.parent.glob('*/results.jsonl'):
        for line in path.read_text().splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue  # a torn last line: that unit reruns
            keys.add((r['class_index'], r['orientation'], r['formula']))
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=1)
    ap.add_argument('--cap', type=float, default=600)
    ap.add_argument('--budget', type=float, default=0, help='solver seconds of this shard over all restarts')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--controls', action='store_true', help='run the controls into --out instead of the shard')
    a = ap.parse_args()
    if a.controls:
        sys.exit(0 if controls(a.out, a.cap) else 1)
    a.out.mkdir(parents=True, exist_ok=True)
    work = a.out / 'work'
    work.mkdir(exist_ok=True)
    records = a.out / 'results.jsonl'
    spent = sum(json.loads(line)['seconds'] for line in records.read_text().splitlines()) if records.exists() else 0.0
    done = done_keys(a.out)
    mine = [u for k, u in enumerate(units()) if k % a.shards == a.shard and u not in done]
    for i, orient, kind in mine:
        if (a.out / 'STOP').exists() or spent >= a.budget:
            print(f'shard {a.shard}: stop ({"STOP file" if spent < a.budget else "budget"}), spent {spent:.0f} s', flush=True)
            break
        links = links_of(i, orient)
        c = formula(links, kind)
        name = f'class{i}_{orient}_{kind}'
        r = pilot.solve(c, work, name, min(a.cap, a.budget - spent))
        spent += r['seconds']
        if r['status'] == 'SAT':
            for p in work.glob(name + '.model.json'):
                os.replace(p, a.out / p.name)
            r.update(bridge(a.out, name, c, links))
        for p in work.glob(name + '.*'):
            p.unlink()
        r.update(class_index=i, orientation=orient, formula=kind, solver=os.path.basename(pilot.CADICAL),
                 scope=f'S1 (8, 3) {kind} formula (9 elements), face-transitive class {i}, {orient} orientation',
                 finished_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        with records.open('a') as f:
            f.write(json.dumps(r) + '\n')
        print(f'{name}: {r["status"]} {r["seconds"]:.1f} s {r.get("status_note", "")}', flush=True)


if __name__ == '__main__':
    main()
