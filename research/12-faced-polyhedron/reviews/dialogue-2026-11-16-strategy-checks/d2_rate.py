"""Session check (thread 2026-11-16-strategy, R2): hit rate of the random D2 2 x 4 family at eight planes.

Unit: one arrangement from pilot.random_d2(seed) of E-261103-05, decided by the frozen hard model of that pilot
(best_solid, 36 edges, 1-3 runs per pair, one disk face per plane, asymmetric solid allowed), cap 15 s, one CP-SAT
worker. Seeds 0-4 repeat the recorded pilot (0-3 INFEASIBLE, 4 SOLID) and serve as the control. Every SOLID goes
through ladder_exact.verify and is compared, by neighbour lists up to per-face reversal, with the Roest-Vigh and Mizhaev maps.
Not ledger evidence. Usage: d2_rate.py N OUT.json
"""
import itertools
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'experiments/E-261103-05-s5-symmetric-solid-first'))
import pilot  # noqa: E402  (adds ROOT/code to sys.path)


def links_isomorphic(la, lb):
    """Relabelling of faces carrying every neighbour list of la to lb up to rotation and reversal PER FACE.

    extract_links does not orient the faces coherently, so this is the comparison of pilot.cyclic_equal: weaker
    than a map isomorphism (necessary, not sufficient)."""
    n = len(la)
    for p in itertools.permutations(range(n)):
        if all(pilot.cyclic_equal([p[j] for j in la[i]], list(lb[p[i]])) for i in range(n)):
            return True
    return False


def unit(seed):
    t0 = time.monotonic()
    h, rejected = pilot.random_d2(seed)
    a = pilot.arrangement(h); tables = pilot.Tables(a)
    cells, info = pilot.best_solid(a, tables, time_limit=15, target_edges=36, max_runs=3)
    out = dict(seed=seed, planes=h, rejected=rejected, status=info['status'], seconds=round(time.monotonic() - t0, 2))
    if cells is not None:
        solid = {tables.cells[i] for i, v in enumerate(cells) if v}
        links = pilot.extract_links(a, solid)
        g = pilot.verify(h, links, require_all_pairs=True)
        mult = sorted(links[i].count(j) for i in range(8) for j in range(i + 1, 8))
        out.update(links={str(k): v for k, v in links.items()}, embedded=bool(g.get('EMBEDDED')),
                   vefchi=list(g.get('V_E_F_chi', ())), pair_multiplicities=mult,
                   face_sizes=sorted(len(links[i]) for i in range(8)))
        for name, _, known in pilot.fixtures():
            out['links_iso_' + name] = links_isomorphic(links, {int(k): list(v) for k, v in known.items()})
    return out


if __name__ == '__main__':
    n, path = int(sys.argv[1]), Path(sys.argv[2])
    t0 = time.monotonic()
    with mp.Pool(8) as pool:
        rows = sorted(pool.imap_unordered(unit, range(n)), key=lambda r: r['seed'])
    hits = [r for r in rows if 'links' in r]
    summary = dict(units=n, wall_seconds=round(time.monotonic() - t0, 1),
                   core_seconds=round(sum(r['seconds'] for r in rows), 1),
                   status={s: sum(r['status'] == s for r in rows) for s in sorted({r['status'] for r in rows})},
                   hits=[{k: r[k] for k in r if k not in ('planes', 'links')} for r in hits])
    path.write_text(json.dumps(dict(summary=summary, rows=rows), indent=1) + '\n')
    print(json.dumps(summary, indent=1))
