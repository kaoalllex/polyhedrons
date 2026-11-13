"""Build the inputs of PLAN.md: maps/seeded_formulas.json (50 of Lutz's 865 (10, 2) maps drawn by a frozen seed, plus
the S6 (10, 2) witness map Lutz #739 as an end-to-end control, each map as three records with kissat seeds 0, 1, 2),
queue.json (10 shards: the two convex f10 controls, then the seeded records round-robin; solver cap 300 s; the checker
cap, unused without proofs, carries the three 120 s bridge stages) and queue_pilot.json (2 shards: #739 and the first
drawn map, three seeds each). The Lutz list is untrusted data, only parsed by code/lutz_import.py.
Usage: python3 make_queue.py [--check]"""
import hashlib
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
import lutz_import  # noqa: E402

RUNNER = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
SOURCE = ROOT / 'literature/lutz-manifold-page/manifolds_lex_d2_n10_o1_g2.txt'
SOURCE_SHA256 = '66012aea7471a3250a46018391d5ca0a2d8ecb8ac8d929787a8a7ec3ab3e67f1'
FORMULAS = HERE / 'maps/seeded_formulas.json'
DRAW_SEED, N_MAPS, WITNESS_LUTZ, SEEDS = 2611130201, 50, 739, (0, 1, 2)
SOLVER_CAP, BRIDGE_CAP = 300, 360


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def formulas():
    assert sha(SOURCE) == SOURCE_SHA256, 'Lutz list changed'
    imported = lutz_import.import_list(SOURCE, 10, 2, 865)
    drawn = sorted(random.Random(DRAW_SEED).sample(range(1, 866), N_MAPS))
    picks = drawn + ([WITNESS_LUTZ] if WITNESS_LUTZ not in drawn else [])
    maps = {m['lutz']: m for m in imported['maps']}
    out = [dict(maps[n], seed=s, role='witness control' if n == WITNESS_LUTZ else 'drawn') for n in picks for s in SEEDS]
    return dict(source=str(SOURCE.relative_to(ROOT)), source_sha256=SOURCE_SHA256, draw_seed=DRAW_SEED, drawn=drawn,
                note='E-261113-02 PLAN.md: submap=True formulas, kissat seeds 0-2', maps=out)


def queue(shards, picks, target):
    records = json.loads(FORMULAS.read_text())['maps']
    control = dict(control_sha256=sha(RUNNER / 'control_f10.json'), solver_cap=60, checker_cap=120)
    rows = [dict(index=f'control-f10{neg}-s{s}', control=kind, **control)
            for neg, kind in [('', 'positive'), ('-neg', 'negative')] for s in range(shards)]
    rows += [dict(index=i, lutz=records[i]['lutz'], seed=records[i]['seed'], solver_cap=SOLVER_CAP, checker_cap=BRIDGE_CAP,
                  canonical_sha256=records[i]['canonical_sha256']) for i in picks]
    return dict(target=target, target_check='S6', case=[10, 2], maps_file=str(FORMULAS.relative_to(ROOT)),
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
    pilot = [i for i, r in enumerate(recs) if r['lutz'] in (WITNESS_LUTZ, recs[0]['lutz'])]
    built = {'queue.json': queue(10, range(len(recs)), 'S6 (10,2) E-261113-02 calibration rung, kissat seeds 0-2, '
                                                       'no proof, submap=True'),
             'queue_pilot.json': queue(2, pilot, f'S6 (10,2) E-261113-02 pilot, Lutz #{WITNESS_LUTZ} and '
                                                 f'#{recs[0]["lutz"]}, seeds 0-2')}
    for name, data in built.items():
        path, out = HERE / name, json.dumps(data, indent=1) + '\n'
        if check:
            assert path.read_text() == out, path
        else:
            path.write_text(out)
        print(name, 'sha256', sha(path), 'units', len([e for e in data['maps'] if isinstance(e['index'], int)]))
    print('seeded_formulas.json sha256', sha(FORMULAS), 'maps', sorted({r['lutz'] for r in recs}))


if __name__ == '__main__':
    main()
