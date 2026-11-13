"""Shard runner of PLAN.md: python3 units.py CASE SHARD SHARDS OUT (CASE 8_2 or 9_3; NO_PROOF=1, SAT_SOLVER=kissat).

Controls first (any failure exits non-zero before a target unit): c1 the plain formula of each map of CASE rebuilds to
its recorded CNF hash; c2 clause families: V2 = plain minus SEGMENT_DISJOINT only, V1 has neither TRIPLE nor
SEGMENT_DISJOINT, and on the single-adjacency convex f9 map V2 is byte-identical to plain; c3 the pinned Roest-Vigh and
Mizhaev chirotopes (E-261103-02 positives) SAT under V1 and V2; c4 the convex f9 planes pinned on the swapped map
UNSAT under V2 (V1 recorded, no expectation). Then the units of this shard (round-robin over V2 maps, then V1 maps);
recorded units in any shard's results.jsonl are skipped."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNNER = ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'
sys.path.insert(0, str(RUNNER))
import pilot  # noqa: E402

VARIANTS = {'V2': dict(pilot.ALL_OPTS, no_segment_disjoint=True), 'V1': dict(pilot.ALL_OPTS, triples=False)}
MAPS = {'8_2': [0, 1], '9_3': [40, 43, 10, 30, 48, 5]}
# Plain-formula CNF SHA-256 as recorded (E-261103-03 results/pilot/manifest.json, paired_9_3_continued/summary.json,
# results/0/results.jsonl), with the DIMACS comments of pilot.solve.
PLAIN_SHA256 = {
    (8, 2, 0): '816bf6ca8975c2ae49548bb51a5c555cacedc828248b85fb1c7b58797c0808bc',
    (8, 2, 1): 'fd02c429a6cf9749d98bc63f798fe3557da2fa49101ae3cebbf2bab87192775c',
    (9, 3, 40): 'fe46b9ccb4fa0934745a04b3fc6e5b43236e470980cf1ae49ca071af28385e16',
    (9, 3, 43): '59aeba201964fdcd475bb72acec295dea973be888aebb76e6d62ec81910dd50b',
    (9, 3, 10): 'acc4062d6233cbab63411122582a667b3af700f063221c501847ee479b76b1f2',
    (9, 3, 30): 'e2369d780f160953b104a1adac952c7b6af6ab9958bcf58f0a5c4915171ce8cc',
    (9, 3, 48): '6fb5ef1da8f708d04a6cba57e975af9f9f539d8a7f22aaf301bf9138246d2d8b',
    (9, 3, 5): '38f8ea6cf957e5d03bd3eec39c36f3b35d4562bbc626a30bb6aca5fd0b709aff'}
SOLVER_CAP, CONTROL_CAP = 900, 60


def formula(links, opts, submap=False):
    """The plain formula (from_links); submap=True for the non-neighborly convex control map, as tranche.unit builds it."""
    if submap:
        tris = sorted({tuple(sorted((x, a, b))) for x, link in enumerate(links) for a, b in zip(link, link[1:] + link[:1])})
        t = pilot.Triangulation(len(links), tris, links=dict(enumerate(links)), submap=True)
    else:
        t = pilot.from_links(links)
    c = pilot.CNF(len(links)); pilot.build(c, t, opts)
    return c


def cnf_sha(c, name):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / 'x.cnf'
        c.dimacs(p, comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
        return hashlib.sha256(p.read_bytes()).hexdigest()


def pinned(c, planes):
    c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in pilot.chirotope_from_planes(planes).items()])
    return c


def controls(case, out):
    f, g = map(int, case.split('_'))
    census = pilot.census(f, g)['maps']
    report, ok = {}, True
    for i in MAPS[case]:
        links = census[i]['links']
        plain = formula(links, pilot.ALL_OPTS)
        v1, v2 = formula(links, VARIANTS['V1']), formula(links, VARIANTS['V2'])
        rest = {k: v for k, v in plain.tags.items() if k != 'SEGMENT_DISJOINT'}
        c1 = cnf_sha(plain, f'map{i}_plain') == PLAIN_SHA256[(f, g, i)]
        c2 = (plain.tags.get('SEGMENT_DISJOINT', 0) > 0 and v2.tags == rest
              and not {'TRIPLE', 'SEGMENT_DISJOINT'} & set(v1.tags))
        report[f'map{i}'] = dict(c1_plain_hash=c1, c2_families=c2, plain_tags=plain.tags, v1_tags=v1.tags, v2_tags=v2.tags)
        ok &= c1 and c2
    f9 = json.loads((RUNNER / 'control_f9.json').read_text())
    f9_links = [f9['links'][str(k)] for k in range(len(f9['links']))]
    same = (cnf_sha(formula(f9_links, VARIANTS['V2'], True), 'f9') == cnf_sha(formula(f9_links, pilot.ALL_OPTS, True), 'f9'))
    report['c2_f9_v2_equals_plain'] = same; ok &= same
    for name, planes, t in pilot.controls()[:2]:
        for v, opts in VARIANTS.items():
            c = pilot.CNF(t.n); pilot.build(c, t, opts)
            r = pilot.solve(pinned(c, planes), out, f'c3_{name}_{v}', CONTROL_CAP)
            report[f'c3_{name}_{v}'] = r['status']; ok &= r['status'] == 'SAT'
    for v, opts in VARIANTS.items():
        neg = {int(k): x for k, x in f9['negative_links'].items()}
        r = pilot.solve(pinned(formula([neg[k] for k in range(len(neg))], opts, True), f9['planes']), out, f'c4_f9_negative_{v}',
                        CONTROL_CAP)
        report[f'c4_f9_negative_{v}'] = r['status']
        if v == 'V2':
            ok &= r['status'] == pilot.UNSAT_OK
    report['status'] = 'CONTROLS-PASS' if ok else 'CONTROLS-FAIL'
    pilot.dump(out / 'controls.json', report)
    return ok


def main(case, shard, shards, out):
    assert pilot.NO_PROOF and 'kissat' in pilot.CADICAL, 'run through run.sh (kissat, NO_PROOF=1)'
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    if not controls(case, out):
        sys.exit('controls failed: no unit run')
    f, g = map(int, case.split('_'))
    census = pilot.census(f, g)['maps']
    units = [(v, i) for v in VARIANTS for i in MAPS[case]]
    done = {json.loads(l)['task'] for p in out.parent.glob('*/results.jsonl') for l in p.read_text().splitlines()}
    for k, (v, i) in enumerate(units):
        name = f'map{i}_{v}'
        if k % shards != shard or name in done or (out.parent / 'stop.requested').exists():
            continue
        r = pilot.solve(formula(census[i]['links'], VARIANTS[v]), out, name, SOLVER_CAP)
        r.update(task=name, case=[f, g], map_index=i, variant=v, options=VARIANTS[v], solver=pilot.CADICAL,
                 scope=f'{v} relaxation of the plain uniform embedding formula; a SAT is about this formula only')
        with open(out / 'results.jsonl', 'a') as fh:
            fh.write(json.dumps(r) + '\n')
        print(name, r['status'], round(r['seconds'], 1), flush=True)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
