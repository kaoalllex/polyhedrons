"""Lead review 2026-11-23, check K1: the full cubic (8, 3) census (all 1806 extra-edge inputs of census.extra_graphs(8, 8))
through the E-261103-01 path (census.run, enum_multi.c), split over 8 processes by input index mod 8; then the stage-A
controls (the 97 equivelar classes of E-261117-04 results/census_8_3, the two known maps, the 790 free-C2 (8, 3) codes
of E-261119-02 stage A) and the admissible strata by extra-edge degree sequence and |Aut+|. A session check, not
ledger evidence. Usage: ~/.venvs/polyhedra/bin/python -I k1_full_census_8_3.py <research root> <cap s> <scratch dir>"""
import importlib.util
import json
import multiprocessing as mp
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1]); CAP = float(sys.argv[2]); OUT = Path(sys.argv[3])
PARTS = 8


def census_module():
    spec = importlib.util.spec_from_file_location('census', ROOT / 'experiments/E-261103-01-s5-map-census/census.py')
    c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    return c


def unit(k):
    c = census_module()
    graphs = c.extra_graphs(8, 8)[k::PARTS]
    t = time.monotonic()
    res = c.run(8, 3, CAP, OUT / f'u{k}', graphs=graphs)
    return dict(k=k, inputs=len(graphs), complete=res['complete'], graphs_done=res['graphs_done'],
                classes=res['classes'], enum_s=round(res['seconds'], 1), wall_s=round(time.monotonic() - t, 1))


def degree_sequence(rec):
    deg = Counter()
    for a, b, m in rec['extra_edges']:
        deg[a] += m - 1; deg[b] += m - 1
    return ''.join(map(str, sorted((deg[v] for v in range(8)), reverse=True)))


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    with mp.Pool(PARTS) as pool:
        units = pool.map(unit, range(PARTS))
    maps = [m for k in range(PARTS) for m in json.loads((OUT / f'u{k}/maps_8_3.json').read_text())['maps']]
    codes = {json.dumps(m['code']) for m in maps}
    eq = json.loads((ROOT / 'experiments/E-261117-04-equivelar-price-pilot/results/census_8_3/maps_8_3.json').read_text())['maps']
    sys.path.insert(0, str(ROOT / 'experiments/E-261119-02-symmetric-nine-face-census'))
    import stageb
    free_c2 = set(stageb.maps_of('C2_8_3'))
    adm = [m for m in maps if m['admissible']]
    strata = Counter((degree_sequence(m), m['aut_plus']) for m in adm)
    by_deg = Counter(degree_sequence(m) for m in adm)
    summary = dict(
        purpose=__doc__.split('\n')[0], cap_s=CAP, units=units, all_complete=all(u['complete'] for u in units),
        wall_s=round(time.monotonic() - t0, 1), core_s=round(sum(u['wall_s'] for u in units), 1),
        classes=len(maps), distinct_codes=len(codes), admissible=len(adm),
        admissible_aut_plus=dict(sorted(Counter(m['aut_plus'] for m in adm).items())),
        admissible_by_extra_degree_sequence=dict(sorted(by_deg.items(), key=lambda x: -x[1])),
        admissible_by_degree_sequence_and_aut=[[d, a, n] for (d, a), n in sorted(strata.items(), key=lambda x: -x[1])],
        control_97_equivelar_present=sum(json.dumps(m['code']) in codes for m in eq), control_97_equivelar_total=len(eq),
        control_equivelar_classes_in_full=sum(all(x == 2 for x in m['extra_pattern']) for m in maps),
        control_free_c2_present=len(free_c2 & codes), control_free_c2_total=len(free_c2),
        label='session check (NUMERICAL timing; counts EXACT computation only if all_complete, coverage of census.run PROVED-1)')
    (OUT / 'maps_8_3_full.json').write_text(json.dumps(maps, separators=(',', ':')))
    print(json.dumps(summary, indent=1))
