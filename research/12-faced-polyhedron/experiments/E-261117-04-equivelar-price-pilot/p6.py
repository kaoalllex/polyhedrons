"""E-261117-04 (P6) stage A: the equivelar (8, 3) census, the plain-formula records and the pinned control (PLAN.md).

  p6.py census                 the seven cycle-union inputs (partitions of 8 into parts >= 2) through enum_multi.c
                               (E-261103-01 census.run) -> results/census_8_3/
  p6.py build [--check]        maps/stageA.json, queue_stageA.json, control_rv8.json; the census controls -> stdout
  p6.py followup RESULTS       after the stage-A run: queue_stageA_retry.json (TIMEOUT units, cap RETRY_CAP) and
                               maps/stageA_models.json + queue_stageA_models.json (SAT units not realized, seeds 1-30)
  p6.py summary [--models] RESULTS...
                               statuses, the two SAT rates, controls and realized objects -> stdout (JSON)

Records: every admissible census class and every free-C2 (8, 3) map of E-261119-02 stage A that is not equivelar, in
the code's orientation, no generator (the plain sub-map formula of tranche.submap_formula), kissat seed 0."""
from collections import Counter, defaultdict
import itertools
import json
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
E2 = ROOT / 'experiments/E-261119-02-symmetric-nine-face-census'
for p in (E2, ROOT / 'code', ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'):
    sys.path.insert(0, str(p))
import stageb as B  # noqa: E402  (symcensus, census, review; maps_of, links_and_groups, code_sha, sha)
import pilot  # noqa: E402
import control_rost_vigh  # noqa: E402
from omsat import Eval  # noqa: E402

S = B.S
F, G = 8, 3
CENSUS = HERE / 'results/census_8_3'
FT = ROOT / 'experiments/E-261117-01-cayley-census-9-4/results/census/maps_8_3.json'
MAPS, MODELS, CONTROL = HERE / 'maps/stageA.json', HERE / 'maps/stageA_models.json', HERE / 'control_rv8.json'
SHARDS, SOLVER_CAP, CHECKER_CAP, RETRY_CAP, CENSUS_SECONDS = 10, 60, 360, 600, 600
MODEL_SEEDS = range(1, 31)


def partitions(n, largest=None):
    """Partitions of n into parts >= 2, parts in decreasing order."""
    if n == 0:
        yield ()
        return
    for p in range(min(n, largest or n), 1, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest


def cycle_union(parts):
    """The loopless 2-regular extra-edge multigraph with one cycle per part; a part 2 is one pair taken twice."""
    edges, o = [], 0
    for p in parts:
        edges += [(o, o + 1)] * 2 if p == 2 else [tuple(sorted((o + i, o + (i + 1) % p))) for i in range(p)]
        o += p
    return edges


def pattern(links):
    """Component sizes of the extra-edge multigraph (multiplicity - 1 per face pair), e.g. '4+4'."""
    extra = Counter()
    for v, link in enumerate(links):
        for w, m in Counter(link).items():
            if v < w and m > 1:
                extra[v, w] = m - 1
    adj = defaultdict(list)
    for (v, w), m in extra.items():
        adj[v] += [w] * m; adj[w] += [v] * m
    seen, sizes = set(), []
    for v in range(len(links)):
        if v in seen or v not in adj:
            continue
        todo, comp = [v], set()
        while todo:
            x = todo.pop()
            if x not in comp:
                comp.add(x); todo += adj[x]
        seen |= comp; sizes.append(len(comp))
    return '+'.join(map(str, sorted(sizes, reverse=True)))


def equivelar(links):
    return all(len(link) == len(links) + 1 for link in links)


def links_of(text):
    return B.links_and_groups(json.loads(text), [], F)[0]


def free_half_turn(rec):
    """An orientation-preserving involution fixing no face (census `autos`: order, fixed faces, edges, triangles)."""
    return any(k == 2 and fixed_faces == 0 for k, fixed_faces, *_ in rec['autos'])


def doubled(links):
    return sorted((v, w, m) for v, link in enumerate(links) for w, m in Counter(link).items() if v < w and m > 1)


def relabel(links, perm):
    out = [None] * len(links)
    for v, link in enumerate(links):
        out[perm[v]] = [perm[w] for w in link]
    return out


def violations(planes, links):
    """Clauses of the plain sub-map formula of these links violated by the chirotope of these planes."""
    links = dict(enumerate(links)) if isinstance(links, list) else links
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
    e = Eval(len(links), pilot.chirotope_from_planes(planes))
    pilot.build(e, pilot.Triangulation(len(links), tris, links=links, submap=True), pilot.ALL_OPTS)
    return len(e.violations)


def negative_links(rv_links, rv_text, texts):
    """The first class (code order) other than Roest-Vigh's with his extra-edge pattern, relabelled (first permutation
    in lexicographic order) so that its doubled face pairs are exactly his: a different map on the same multigraph."""
    target = doubled(rv_links)
    for t in sorted(texts):
        links = links_of(t)
        if t == rv_text or pattern(links) != pattern(rv_links):
            continue
        for perm in itertools.permutations(range(F)):
            moved = relabel(links, perm)
            if doubled(moved) == target:
                return moved, t
    raise ValueError('no other class on the Roest-Vigh multigraph')


def census_run():
    return S.census.run(F, G, CENSUS_SECONDS, CENSUS, graphs=[cycle_union(p) for p in partitions(F)])


def build(check=False):
    res = json.loads((CENSUS / f'maps_{F}_{G}.json').read_text())
    texts = {json.dumps(m['code']): m for m in res['maps']}
    free = B.maps_of('C2_8_3')
    ft = [json.dumps(m['code']) for m in json.loads(FT.read_text())['maps']]
    known = {v: k for k, v in S.known_8_3_codes().items()}
    eq_free = {t for t in free if equivelar(links_of(t))}
    progress = (CENSUS / 'progress.txt').read_text().splitlines()
    adm = {t: m for t, m in texts.items() if m['admissible']}
    H, rv = control_rost_vigh.build()
    rv_list = [rv[i] for i in range(F)]
    rv_text = S.known_8_3_codes()['roest_vigh']
    neg, neg_text = negative_links(rv_list, rv_text, adm)
    controls = dict(
        census_complete=res['complete'] and sum('complete=1' in s for s in progress) == len(list(partitions(F))),
        all_equivelar=all(equivelar(links_of(t)) for t in texts),
        known_present=set(known) <= set(adm), face_transitive_present=set(ft) <= set(texts),
        free_equivelar_present=eq_free <= set(adm), free_half_turn_listed=all(t in free for t, m in adm.items()
                                                                               if free_half_turn(m)),
        pinned_positive_violations_zero=violations(H, rv) == 0, pinned_negative_violations_positive=violations(H, neg) > 0)
    counts = dict(classes=len(texts), admissible=len(adm), free=len(free), free_equivelar=len(eq_free),
                  free_half_turn_classes=sum(free_half_turn(m) for m in adm.values()),
                  patterns=dict(sorted(Counter(pattern(links_of(t)) for t in adm).items())),
                  known_patterns={known[t]: pattern(links_of(t)) for t in known},
                  negative_class_sha256=B.code_sha(json.loads(neg_text)))

    def record(t, config):
        links = links_of(t)
        return dict(config=config, links=links, canonical_sha256=B.code_sha(json.loads(t)), equivelar=equivelar(links),
                    pattern=pattern(links) if equivelar(links) else None, free_c2=t in free, known=known.get(t),
                    face_transitive=ft.index(t) if t in ft else None, seed=0)
    recs = [record(t, 'P6_8_3') for t in sorted(adm)] + [record(t, 'C2_8_3') for t in sorted(set(free) - eq_free)]
    files = [(MAPS, dict(note='E-261117-04 stage A: admissible equivelar (8, 3) classes, then the non-equivelar free-C2 '
                               '(8, 3) maps of E-261119-02 stage A; plain sub-map formula, seed 0', maps=recs)),
             (CONTROL, dict(planes=H, links={str(k): v for k, v in rv.items()},
                            negative_links={str(k): v for k, v in enumerate(neg)},
                            note="Roest-Vigh's planes pinned: on his links (positive, SAT) and on another (8, 3) class "
                                 'relabelled onto his doubled face pairs (negative, UNSAT)'))]
    for path, data in files:
        write(path, json.dumps(data, indent=1) + '\n', check)
    write(HERE / 'queue_stageA.json', json.dumps(queue(MAPS, range(len(recs)), recs, SOLVER_CAP), indent=1) + '\n',
          check)
    print(json.dumps(dict(controls=controls, counts=counts, records=len(recs)), indent=1))
    return controls, counts, recs


def write(path, text, check):
    if check:
        assert path.read_text() == text, path
    else:
        path.parent.mkdir(exist_ok=True); path.write_text(text)


def queue(maps_file, indices, recs, cap):
    c = dict(control_sha256=B.sha(CONTROL), solver_cap=60, checker_cap=120)
    rows = [dict(index=f'control-rv8{neg}-s{s}', control=kind, **c)
            for neg, kind in [('', 'positive'), ('-neg', 'negative')] for s in range(SHARDS)]
    rows += [dict(index=i, seed=recs[i]['seed'], solver_cap=cap, checker_cap=CHECKER_CAP,
                  canonical_sha256=recs[i]['canonical_sha256']) for i in indices]
    return dict(target=f'E-261117-04 stage A {maps_file.stem}, kissat, no proof', target_check='all-pairs',
                case=[F, G], maps_file=str(maps_file.relative_to(ROOT)), maps_sha256=B.sha(maps_file), shards=SHARDS,
                control_file=os.path.relpath(CONTROL, B.RUNNER), lean_unsat=True, maps=rows)


def results(dirs):
    """map_index -> the last recorded result over the shards of these result directories."""
    out = {}
    for d in dirs:
        for path in sorted(Path(d).glob('[0-9]*/results.jsonl')):
            for line in path.read_text().splitlines():
                r = json.loads(line)
                out[r['map_index']] = r
    return out


def realized(r):
    return r.get('status') == 'SAT' and r.get('candidate_verify_rc') == 0


def followup(dirs):
    recs = json.loads(MAPS.read_text())['maps']; res = results(dirs)
    retry = sorted(i for i, r in res.items() if isinstance(i, int) and r['status'] == 'TIMEOUT')
    open_sat = sorted(i for i, r in res.items() if isinstance(i, int) and r['status'] == 'SAT' and not realized(r))
    if retry:
        write(HERE / 'queue_stageA_retry.json', json.dumps(queue(MAPS, retry, recs, RETRY_CAP), indent=1) + '\n', False)
    if open_sat:
        models = [dict(recs[i], seed=s, stage_a_index=i) for i in open_sat for s in MODEL_SEEDS]
        write(MODELS, json.dumps(dict(note='E-261117-04 stage A: SAT units not realized, kissat seeds 1-30',
                                      maps=models), indent=1) + '\n', False)
        write(HERE / 'queue_stageA_models.json',
              json.dumps(queue(MODELS, range(len(models)), models, SOLVER_CAP), indent=1) + '\n', False)
    print(json.dumps(dict(retry=retry, sat_not_realized=open_sat)))


def vefc(r):
    log = (ROOT.parents[1] / r['candidate']).with_suffix('').with_suffix('.candidate.log')
    m = re.search(r'"V_E_F_chi": \[([-\d, ]+)\]', log.read_text()) if log.exists() else None
    return [int(x) for x in m.group(1).split(',')] if m else None


def summary(dirs, maps_file=MAPS):
    recs = json.loads(maps_file.read_text())['maps']; res = results(dirs)
    ctrl = {k: r['status'] for k, r in res.items() if not isinstance(k, int)}
    units = {i: r for i, r in res.items() if isinstance(i, int)}
    by = defaultdict(Counter)
    for i, r in units.items():
        by['equivelar' if recs[i]['equivelar'] else 'not_equivelar'][r['status']] += 1
    sat = [dict(index=i, sha=recs[i]['canonical_sha256'][:12], equivelar=recs[i]['equivelar'],
                pattern=recs[i]['pattern'], known=recs[i]['known'], free_c2=recs[i]['free_c2'],
                status_note=r.get('status_note'), realized=realized(r), V_E_F_chi=vefc(r) if realized(r) else None)
           for i, r in sorted(units.items()) if r['status'] == 'SAT']
    ft = {recs[i]['face_transitive']: units[i]['status'] for i in units if recs[i]['face_transitive'] is not None}
    out = dict(units=len(units), of=len(recs), statuses=dict(by), sat=sat,
               controls_pass=all(s == ('SAT' if '-neg' not in k else 'UNSAT-SOLVER') for k, s in ctrl.items()),
               controls=len(ctrl), face_transitive=dict(sorted(ft.items())),
               known={recs[i]['known']: units[i]['status'] for i in units if recs[i]['known']})
    print(json.dumps(out, indent=1))
    return out


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'census':
        r = census_run(); print(json.dumps({k: v for k, v in r.items() if k != 'maps'}))
    elif cmd == 'build':
        build('--check' in sys.argv)
    elif cmd == 'followup':
        followup(sys.argv[2:])
    elif cmd == 'summary':
        models = '--models' in sys.argv
        summary([a for a in sys.argv[2:] if a != '--models'], MODELS if models else MAPS)
    else:
        sys.exit(__doc__)
