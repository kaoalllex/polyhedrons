"""Build the inputs of PLAN.md.

maps/formulas.json   the 20 admissible (11, 5) maps with Aut+ = 2 of the E-261116-01 census, their orientation-preserving
                     involution (recomputed here from the links) and its fixed faces; two maps drawn by a frozen seed,
                     each as four records (kissat seeds 0-3) of the plane-only C2 formula in a moved chart
maps/control.json    the N2 Szilassi chain at seven faces: Szilassi's map with its half-turn, plane-only (seeds 0-3) and
                     the standard-chart formula (INF fixed by the half-turn, forced zeros; seeds 0-5)
queue.json           10 shards: convex f11 pinned controls on every shard, one (11, 5) record on shards 0-7;
                     cap 1800 s, the checker cap (unused without proofs) carries the three 120 s bridge stages
queue_control.json   10 shards, one Szilassi record each, cap 60 s
queue_pilot.json     queue.json with a 120 s solver cap (the pilot runs shards 0 and 4: both maps, seed 0)
maps/formulas_rest.json, queue_rest.json   amendment 2 (the NIGHT follow-up): the other 18 maps, same records and caps
Usage: python3 make_queue.py [--check]"""
import gzip
import hashlib
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'experiments/E-261117-02-moved-chart-plane-symmetry'))
from omsat_validate import szilassi  # noqa: E402
from omsat_sym import links_from_oriented, orient  # noqa: E402
from n2 import G_SZ  # noqa: E402

RUNNER = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
CENSUS = ROOT / 'experiments/E-261116-01-s5-11-5-census-cost-probe/results/census/maps_11_5.json.gz'
CENSUS_SHA256 = 'a35cf8fb7f611e6f01c02ecc31ff97d74a3db3271d6b461d67e7dca1320d3604'
CONTROL_F11 = '../E-261116-01-s5-11-5-census-cost-probe/control_f11.json'
FORMULAS, CONTROL = HERE / 'maps/formulas.json', HERE / 'maps/control.json'
REST = HERE / 'maps/formulas_rest.json'
DRAW_SEED, N_MAPS, SEEDS = 2611180301, 2, (0, 1, 2, 3)
SOLVER_CAP, BRIDGE_CAP, SHARDS = 1800, 360, 10
GROUP = 'C2 (half-turn fixing one face), plane-only, moved chart'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_sha(code):
    return hashlib.sha256(json.dumps(code, separators=(',', ':')).encode()).hexdigest()


def rotations(links):
    """Orientation-preserving automorphisms of a map given by its cyclic links (repeated neighbours allowed): face
    permutations p with links[p(v)] a cyclic rotation of p(links[v]) for every face v."""
    n = len(links); out = set()
    def same(a, b):
        return len(a) == len(b) and any(a[k:] + a[:k] == b for k in range(len(a)))
    for w in range(n):
        for r in range(len(links[w]) if len(links[w]) == len(links[0]) else 0):
            g = {0: w}; todo = [(0, r)]; ok = True
            while todo and ok:
                v, off = todo.pop()
                lv, lw = links[v], links[g[v]]
                for i, x in enumerate(lv):
                    y = lw[(i + off) % len(lw)]
                    if x in g:
                        ok = g[x] == y
                    elif y in g.values() or len(links[x]) != len(links[y]):
                        ok = False
                    else:
                        g[x] = y
                        lx, ly = links[x], links[y]
                        offs = [o for o in range(len(ly)) if all(lx[j] not in g or g[lx[j]] == ly[(j + o) % len(ly)]
                                                                 for j in range(len(lx)))]
                        ok = bool(offs)
                        if ok:
                            todo.append((x, offs[0]))
                    if not ok:
                        break
            if ok and len(g) == n:
                p = tuple(g[i] for i in range(n))
                if all(same([p[x] for x in links[v]], links[p[v]]) for v in range(n)):
                    out.add(p)
    return sorted(out)


def formulas(rest=False):
    assert sha(CENSUS) == CENSUS_SHA256, 'census changed'
    with gzip.open(CENSUS, 'rt') as stream:
        maps = json.load(stream)['maps']
    pool = []
    for i, m in enumerate(maps):
        if m['admissible'] and m['aut_plus'] == 2:
            rots = rotations(m['links'])
            assert len(rots) == 2, (i, rots)
            g = rots[1]
            assert all(g[g[f]] == f for f in range(11))
            pool.append(dict(census_index=i, involution=list(g), fixed_faces=[f for f in range(11) if g[f] == f]))
    assert len(pool) == 20 and all(len(p['fixed_faces']) == 1 for p in pool)
    drawn = sorted(random.Random(DRAW_SEED).sample([p['census_index'] for p in pool], N_MAPS))
    out = [dict(census_index=i, links=maps[i]['links'], canonical_sha256=code_sha(maps[i]['code']),
                extra_pattern=maps[i]['extra_pattern'], sym_generator=p['involution'], fixed_faces=p['fixed_faces'],
                sym_planes_only=True, sym_group=GROUP, seed=s)
           for i in (sorted(set(p['census_index'] for p in pool) - set(drawn)) if rest else drawn)
           for p in pool if p['census_index'] == i for s in SEEDS]
    return dict(census=str(CENSUS.relative_to(ROOT)), census_sha256=CENSUS_SHA256, draw_seed=DRAW_SEED,
                pool=pool, drawn=drawn, note='E-261118-03 PLAN.md: plane-only C2 formulas, kissat seeds 0-3', maps=out)


def control():
    links = links_from_oriented(orient(szilassi()[1].tris), 7)[0]
    links = [links[k] for k in range(7)]
    rots = rotations(links)
    assert len(rots) == 42 and G_SZ in rots, 'Szilassi map: Aut+ 42 with the half-turn'
    base = dict(links=links, canonical_sha256=hashlib.sha256(json.dumps(links).encode()).hexdigest(),
                sym_generator=list(G_SZ), sym_group='C2 (Szilassi half-turn, fixes face 5)')
    recs = [dict(base, role='positive: plane-only, moved chart', sym_planes_only=True, seed=s) for s in SEEDS]
    recs += [dict(base, role='negative: standard chart, INF fixed', sym_planes_only=False, seed=s) for s in range(6)]
    return dict(note='E-261118-03 PLAN.md: the N2 Szilassi chain through the runner', maps=recs)


def queue(records_file, records, case, target, solver_cap, controls):
    rows = []
    if controls:
        c = dict(control_sha256=sha(RUNNER / CONTROL_F11), solver_cap=60, checker_cap=120)
        rows += [dict(index=f'control-f11{neg}-s{s}', control=kind, **c)
                 for neg, kind in [('', 'positive'), ('-neg', 'negative')] for s in range(SHARDS)]
    rows += [dict(index=i, seed=r['seed'], solver_cap=solver_cap, checker_cap=BRIDGE_CAP,
                  canonical_sha256=r['canonical_sha256']) for i, r in enumerate(records)]
    data = dict(target=target, target_check='S5', case=list(case), maps_file=str(records_file.relative_to(ROOT)),
                maps_sha256=sha(records_file), shards=SHARDS, maps=rows)
    if controls:
        data['control_file'] = CONTROL_F11
    return data


def main():
    check = '--check' in sys.argv
    for path, data in [(FORMULAS, formulas()), (CONTROL, control()), (REST, formulas(rest=True))]:
        text = json.dumps(data, indent=1) + '\n'
        if check:
            assert path.read_text() == text, path
        else:
            path.parent.mkdir(exist_ok=True); path.write_text(text)
    recs, ctrl = json.loads(FORMULAS.read_text())['maps'], json.loads(CONTROL.read_text())['maps']
    rest = json.loads(REST.read_text())['maps']
    built = {'queue.json': queue(FORMULAS, recs, (11, 5), 'S5 (11,5) E-261118-03 plane-only price probe, kissat seeds '
                                 '0-3, no proof', SOLVER_CAP, True),
             'queue_control.json': queue(CONTROL, ctrl, (7, 1), 'E-261118-03 N2 Szilassi chain through the runner',
                                         60, False),
             'queue_pilot.json': queue(FORMULAS, recs, (11, 5), 'E-261118-03 pilot, solver cap 120 s', 120, True),
             'queue_rest.json': queue(REST, rest, (11, 5), 'S5 (11,5) E-261118-03 amendment 2: the other 18 Aut+ = 2 '
                                      'maps, kissat seeds 0-3, no proof', SOLVER_CAP, True)}
    for name, data in built.items():
        path, out = HERE / name, json.dumps(data, indent=1) + '\n'
        if check:
            assert path.read_text() == out, path
        else:
            path.write_text(out)
        print(name, 'sha256', sha(path), 'units', len([e for e in data['maps'] if isinstance(e['index'], int)]))
    print('formulas.json sha256', sha(FORMULAS), 'drawn', json.loads(FORMULAS.read_text())['drawn'])


if __name__ == '__main__':
    main()
