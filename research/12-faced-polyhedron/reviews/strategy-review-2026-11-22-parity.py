"""Lead review 2026-11-22, session check (not ledger evidence): price and yield of the GF(2) collinear-segment parity
pass (Lemma P, E-261116-09 part B) on the E-261119-02 stage-B inputs, to answer the owner's question whether it belongs
in week item 2's tree. Reuses E-261116-09's ablate.build (the stage-B builder) and parity.equations / inconsistent /
check unchanged; no solver, no shrink (certificate size is not needed for counts). Every inconsistent system's
certificate is re-checked by parity.check.
Counts are keyed (config, equivelar, SEG consistent, SEG+SYM consistent); an inconsistent SEG system excludes the map for
every cubic embedded realization, an inconsistent SEG+SYM system excludes it under that action (Lemma P, PROVED-1).
Usage: python3 -I strategy-review-2026-11-22-parity.py OUT_JSON [--per-chunk N] [--workers 10]"""
import argparse
from collections import Counter
import json
import multiprocessing as mp
from pathlib import Path
import sys
import time

EXP = Path(__file__).resolve().parents[1] / 'experiments'
sys.path.insert(0, str(EXP / 'E-261116-09-uniformity-perturbation-lemmas'))
import ablate as A  # noqa: E402
import parity as P  # noqa: E402

SETS = {'SEG': {'SEGMENT_DISJOINT'}, 'SEG+SYM': {'SEGMENT_DISJOINT', 'SYM'}}


def one(rec):
    t0 = time.process_time()
    c, tags, _, links = A.build(rec)
    t1 = time.process_time()
    row = dict(config=rec['config'], stratum=rec['stratum'][0], equivelar=len({len(v) for v in links.values()}) == 1)
    for name, fams in SETS.items():
        eqs, _ = P.equations(c, tags, fams)
        cert = P.inconsistent(eqs)
        assert cert is None or P.check(eqs, cert)
        row[name] = cert is None
    row['build_s'], row['parity_s'] = round(t1 - t0, 4), round(time.process_time() - t1, 4)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--per-chunk', type=int, default=500); ap.add_argument('--workers', type=int, default=10)
    a = ap.parse_args()
    maps = A.CENSUS / 'maps'
    recs = json.loads((maps / 'pass1.json').read_text())['maps']
    for k in range(10):  # chunks 0-9 are a prefix of the frozen random order (amendment 6): the head of each is a random sample
        recs += json.loads((maps / 'pass1_9_5' / ('c%03d.json' % k)).read_text())['maps'][:a.per_chunk]
    t0 = time.monotonic()
    with mp.Pool(a.workers) as pool:
        rows = pool.map(one, recs, chunksize=20)
    wall = time.monotonic() - t0
    by = Counter((r['config'], r['stratum'], r['SEG'], r['SEG+SYM']) for r in rows)
    cfg = Counter((r['config'], r['equivelar'], r['SEG'], r['SEG+SYM']) for r in rows)
    cpu = sum(r['build_s'] + r['parity_s'] for r in rows)
    summary = dict(records=len(rows), wall_s=round(wall, 1), workers=a.workers, cpu_s=round(cpu, 1),
                   build_s=round(sum(r['build_s'] for r in rows), 1), parity_s=round(sum(r['parity_s'] for r in rows), 1),
                   by_config=[[*k, v] for k, v in sorted(cfg.items())], by_stratum=[[*k, v] for k, v in sorted(by.items())])
    json.dump(summary, open(a.out, 'w'), indent=0)
    print(json.dumps({k: v for k, v in summary.items() if k != 'by_stratum'}, indent=1))


if __name__ == '__main__':
    main()
