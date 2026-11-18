"""Session check (thread 2026-11-16-strategy, R2): cost per unit of the C3 3+3+3 family at nine planes.

Unit: three integer planes (coefficients as in pilot.random_d2) and their images under the rational 3-fold rotation
(x, y, z) -> (y, z, x); uniform arrangements only (pilot.arrangement rejects the rest). Decision: the frozen hard
model of E-261103-05 (best_solid, cubic, 1-3 runs per pair, one disk face per plane, the solid need not be invariant),
E edges, cap CAP s, one CP-SAT worker. A timing check, not a search; any SOLID is verified exactly, saved and reported
as a candidate for the candidate-check skill, never as a result. Usage: c3_nine.py N EDGES CAP OUT.json
"""
import json
import multiprocessing as mp
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'experiments/E-261103-05-s5-symmetric-solid-first'))
import pilot  # noqa: E402

EDGES, CAP = int(sys.argv[2]), float(sys.argv[3])


def random_c3(seed):
    rng = random.Random(2611160000 + seed)
    for rejected in range(200):
        rows = []
        for _ in range(3):
            a, b, c = (rng.choice([i for i in range(-8, 9) if i]) for _ in range(3)); d = -rng.randint(1, 8)
            rows += [[a, b, c, d], [c, a, b, d], [b, c, a, d]]
        try:
            pilot.arrangement(rows)
            return rows, rejected
        except ValueError:
            pass
    raise ValueError('no uniform C3 arrangement in 200 attempts')


def unit(seed):
    t0 = time.monotonic()
    h, rejected = random_c3(seed)
    a = pilot.arrangement(h); tables = pilot.Tables(a)
    cells, info = pilot.best_solid(a, tables, time_limit=CAP, target_edges=EDGES, max_runs=3)
    out = dict(seed=seed, planes=h, rejected=rejected, bounded_cells=len(tables.cells), status=info['status'],
               seconds=round(time.monotonic() - t0, 2))
    if cells is not None:
        solid = {tables.cells[i] for i, v in enumerate(cells) if v}
        links = pilot.extract_links(a, solid)
        g = pilot.verify(h, links, require_all_pairs=True)
        out.update(links={str(k): v for k, v in links.items()}, embedded=bool(g.get('EMBEDDED')),
                   vefchi=list(g.get('V_E_F_chi', ())))
    return out


if __name__ == '__main__':
    n, path = int(sys.argv[1]), Path(sys.argv[4])
    t0 = time.monotonic()
    with mp.Pool(8) as pool:
        rows = sorted(pool.imap_unordered(unit, range(n)), key=lambda r: r['seed'])
    secs = sorted(r['seconds'] for r in rows)
    summary = dict(units=n, edges=EDGES, cap=CAP, wall_seconds=round(time.monotonic() - t0, 1),
                   core_seconds=round(sum(secs), 1), median_seconds=secs[len(secs) // 2], max_seconds=secs[-1],
                   status={s: sum(r['status'] == s for r in rows) for s in sorted({r['status'] for r in rows})},
                   bounded_cells=sorted({r['bounded_cells'] for r in rows}),
                   solids=[{k: r[k] for k in r if k != 'planes'} for r in rows if 'links' in r])
    path.write_text(json.dumps(dict(summary=summary, rows=rows), indent=1) + '\n')
    print(json.dumps(summary, indent=1))
