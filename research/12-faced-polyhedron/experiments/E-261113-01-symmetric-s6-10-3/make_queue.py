"""Build the inputs of PLAN.md part (b): maps/sym_formulas.json (the ten symmetric formula records: the imported
(10, 3) map plus `sym_generator`, one per conjugacy class under Aut: C3 with one fixed face on Lutz #1, 2, 4, 8, 14,
15; free C2 on #6, #12 and both classes of #20), queue.json (10 shards: the two convex f10 controls, then one formula;
cap 3600 s, no proof) and queue_pilot.json (2 shards, Lutz #1 C3 and #6 C2 at 300 s).
Usage: python3 make_queue.py [--check]"""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
from omsat_sym import automorphisms, closure, compose  # noqa: E402

RUNNER = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
SOURCE = ROOT / 'experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json'
FORMULAS = HERE / 'maps/sym_formulas.json'
PLAN = [(1, 'C3'), (2, 'C3'), (4, 'C3'), (8, 'C3'), (14, 'C3'), (15, 'C3'), (6, 'C2'), (12, 'C2'), (20, 'C2')]
SOLVER_CAP, CHECKER_CAP, PILOT_CAP = 3600, 60, 300


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classes(rec, kind):
    """One generator per class of subgroups (conjugacy under the full Aut): C3 fixing one face, or free C2."""
    n = len(rec['links'])
    tris = rec['triangles'] if isinstance(rec['triangles'], list) else json.loads(rec['triangles'])
    auts = automorphisms([tuple(t) for t in tris], n)
    e = tuple(range(n))
    order, fixed = (3, 1) if kind == 'C3' else (2, 0)
    power = lambda p, k: p if k == 1 else compose(p, power(p, k - 1))  # noqa: E731
    gens = sorted(p for p, eps in auts if eps == 1 and p != e and power(p, order) == e
                  and sum(p[i] == i for i in range(n)) == fixed)
    inv = lambda a: tuple(sorted(range(n), key=lambda i: a[i]))  # noqa: E731
    out = []
    for p in gens:
        H = closure([p], n)
        if not any(frozenset(compose(compose(a, h), inv(a)) for h in H) in [closure([q], n) for q in out] for a, _ in auts):
            out.append(p)
    return out


def formulas():
    maps = {m['lutz']: m for m in json.loads(SOURCE.read_text())['maps']}
    out = []
    for lutz, kind in PLAN:
        for k, p in enumerate(classes(maps[lutz], kind)):
            out.append(dict(maps[lutz], sym_group=kind, sym_class=k, sym_generator=list(p)))
    assert [(r['lutz'], r['sym_group']) for r in out] == [(l, k) for l, k in PLAN] + [(20, 'C2')], 'class counts'
    out.sort(key=lambda r: (r['sym_group'] != 'C3', r['lutz'], r['sym_class']))
    return dict(source=str(SOURCE.relative_to(ROOT)), source_sha256=sha(SOURCE),
                note='E-261113-01 PLAN.md part (b): rotation ansatz, det rho = +1', maps=out)


def queue(shards, picks, solver_cap, target):
    records = json.loads(FORMULAS.read_text())['maps']
    control = dict(control_sha256=sha(RUNNER / 'control_f10.json'), solver_cap=60, checker_cap=120)
    rows = [dict(index=f'control-f10{neg}-s{s}', control=kind, **control)
            for neg, kind in [('', 'positive'), ('-neg', 'negative')] for s in range(shards)]
    rows += [dict(index=i, lutz=records[i]['lutz'], sym_group=records[i]['sym_group'], sym_class=records[i]['sym_class'],
                  solver_cap=solver_cap, checker_cap=CHECKER_CAP, canonical_sha256=records[i]['canonical_sha256'])
             for i in picks]
    return dict(target=target, target_check='S6', case=[10, 3], maps_file=str(FORMULAS.relative_to(ROOT)),
                maps_sha256=sha(FORMULAS), control_file='control_f10.json', shards=shards, maps=rows)


def main():
    check = '--check' in sys.argv
    text = json.dumps(formulas(), indent=1) + '\n'
    if check:
        assert FORMULAS.read_text() == text, FORMULAS
    else:
        FORMULAS.parent.mkdir(exist_ok=True)
        FORMULAS.write_text(text)
    recs = json.loads(text)['maps']
    pilot = [next(i for i, r in enumerate(recs) if (r['lutz'], r['sym_group']) == key) for key in [(1, 'C3'), (6, 'C2')]]
    built = {'queue.json': queue(10, range(10), SOLVER_CAP, 'S6 (10,3) E-261113-01 (b), ten symmetric formulas, '
                                                          'kissat, no proof, submap=True'),
             'queue_pilot.json': queue(2, pilot, PILOT_CAP, 'S6 (10,3) E-261113-01 (b) pilot, Lutz #1 C3, #6 C2 at 300 s')}
    for name, data in built.items():
        path, out = HERE / name, json.dumps(data, indent=1) + '\n'
        if check:
            assert path.read_text() == out, path
        else:
            path.write_text(out)
        print(name, 'sha256', sha(path), 'formulas', len([e for e in data['maps'] if isinstance(e['index'], int)]))
    print('sym_formulas.json sha256', sha(FORMULAS), [(r['lutz'], r['sym_group'], r['sym_generator']) for r in recs])


if __name__ == '__main__':
    main()
