"""Face-contraction sieve (PLAN.md). con(X) = every Tseitin definition clause plus every other clause of the plain S5
formula whose chirotope signs, through its gates, all contain element X (the rank-3 contraction chi/X). A clause subset,
so con(X) UNSAT implies the plain formula UNSAT. X ranges over the faces; X = INF (the normals) is descriptive."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent
E03 = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
sys.path.insert(0, str(E03))
import pilot

CAP = 20
PLANT = (4, 5, 6)   # C1: contradicting units on chirotope(4, 5, 6, INF), as in E-261108-02


def contraction_masks(c):
    """Per clause: the bit mask of elements contained in every chirotope 4-set of its transitive support (all ones when
    the support is empty), and whether it is a gate definition clause."""
    full = (1 << (c.n + 1)) - 1
    inter = {1: full}
    for S, v in c.qvar.items():
        inter[v] = sum(1 << e for e in S)
    gates = sorted([(z, key) for key, z in c._and.items()] + [(z, key) for key, z in c._xor.items() if len(key) == 2])
    defs = set()
    for z, key in gates:    # a gate's inputs are created before it
        m = full
        for l in key:
            m &= inter[abs(l)]
        inter[z] = m
    for key, z in c._and.items():
        defs.update([(-z, l) for l in key] + [tuple([z] + [-l for l in key])])
    for (a, b), z in ((k, z) for k, z in c._xor.items() if len(k) == 2):
        defs.update([(-z, a, b), (-z, -a, -b), (z, -a, b), (z, a, -b)])
    out = []
    for cl in c.clauses:
        m = full
        for l in cl:
            m &= inter[abs(l)]
        out.append((m, tuple(cl) in defs))
    return out


class Sub:
    def __init__(self, nv, clauses):
        self.nv, self.clauses = nv, clauses

    def dimacs(self, path, comments=()):
        pilot.CNF.dimacs(self, path, comments)


def contraction(c, masks, X):
    return [cl for cl, (m, d) in zip(c.clauses, masks) if d or m >> X & 1]


def formula_for(n, g, index):
    rec = pilot.census(n, g)['maps'][index]
    c = pilot.CNF(n); pilot.build(c, pilot.from_links(rec['links']), pilot.ALL_OPTS)
    h = hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest()
    recorded = {r['formula_sha256'] for r in RECORDS() if r.get('map_index') == index and r.get('formula_sha256')}
    if recorded and recorded != {h}:
        raise SystemExit(f'map {index}: formula hash {h} differs from recorded {recorded}')
    return c, {'formula_sha256': h, 'recorded_hash_match': bool(recorded), 'pattern': rec['extra_pattern'],
               'admissible': rec['admissible']}


_records = []


def RECORDS():
    if not _records:
        _records.extend(json.loads(p.read_text()) for p in (E03 / 'results').glob('**/result.json'))
    return _records


def control_formula(name):
    """C0: convex 9-face control, SAT. C1: C0 plus contradicting units on chirotope(PLANT + INF). C2: another map's links
    with the control's planes pinned (UNSAT-VERIFIED in E-261103-03 item 1); descriptive."""
    data = json.loads((E03 / 'control_f9.json').read_text())
    links = {int(k): v for k, v in data['negative_links' if name == 'C2' else 'links'].items()}
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
    c = pilot.CNF(9); pilot.build(c, pilot.Triangulation(9, tris, links=links, submap=True), pilot.ALL_OPTS)
    if name == 'C1':
        q = c.qvar[tuple(sorted(PLANT + (9,)))]
        c.clauses += [[q], [-q]]
    if name == 'C2':
        c.clauses += [[c.qvar[S] if v > 0 else -c.qvar[S]] for S, v in pilot.chirotope_from_planes(data['planes']).items()]
    return c, {'formula_sha256': None}


def unit(name, outroot, n, g, full_cap=0):
    out = outroot / name
    if (out / 'result.json').exists():
        return
    shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    t0 = time.monotonic()
    c, meta = control_formula(name) if name.startswith('C') else formula_for(n, g, int(name))
    masks = contraction_masks(c)
    whole = set(map(tuple, c.clauses))
    res = {'unit': name, **meta, 'variables': c.nv, 'clauses': len(c.clauses), 'by_element': {}}
    for X in range(c.n + 1):
        sub = contraction(c, masks, X)
        assert set(map(tuple, sub)) <= whole
        r = pilot.solve(Sub(c.nv, sub), out, f'X{X}', CAP, checker_timeout=CAP)
        res['by_element']['INF' if X == c.n else str(X)] = {
            'status': r['status'], 'seconds': round(r['seconds'], 3), 'clauses': r['clauses'],
            'nondef_clauses': sum(1 for m, d in masks if not d and m >> X & 1),
            'cnf_sha256': r['cnf_sha256'], 'proof_sha256': r.get('proof_sha256')}
    faces = [res['by_element'][str(X)] for X in range(c.n)]
    res['killed'] = any(f['status'] == 'UNSAT-VERIFIED' for f in faces)
    res['killing_faces'] = [X for X in range(c.n) if faces[X]['status'] == 'UNSAT-VERIFIED']
    res['face_timeouts'] = sum(f['status'] == 'TIMEOUT' for f in faces)
    if full_cap:
        r = pilot.solve(c, out, 'full', full_cap, checker_timeout=full_cap)
        res['full'] = {'status': r['status'], 'seconds': round(r['seconds'], 3)}
    res['wall_seconds'] = round(time.monotonic() - t0, 1)
    pilot.dump(out / 'result.json', res)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=10)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--only', nargs='*', help='unit names (map index, C0, C1, C2) instead of the sharded list')
    a = ap.parse_args()
    maps = [str(i) for i, r in enumerate(pilot.census(9, 3)['maps']) if r['admissible']]
    assert len(maps) == 203
    units = a.only or (['C0', 'C1', 'C2'] + maps)[a.shard::a.shards]
    a.out.mkdir(parents=True, exist_ok=True)
    for u in units:
        unit(u, a.out, 9, 3, full_cap=60 if u == 'C0' else 0)


if __name__ == '__main__':
    main()
