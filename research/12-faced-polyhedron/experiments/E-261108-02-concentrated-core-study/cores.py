"""Face-support sub-formulas of plain (9,3) formulas (PLAN.md). sub(F) = the clauses whose variables depend only on the
chirotope signs of 4-subsets inside F + {INF}; a clause subset, so sub(F) UNSAT implies the whole formula UNSAT."""
import argparse
import hashlib
import itertools
import json
import multiprocessing as mp
from pathlib import Path
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent
E03 = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
sys.path.insert(0, str(E03))
import pilot

N = 9
KMIN, KMAX, KDESC = 3, 6, 8   # verdict levels 3..6; 7..8 are descriptive (PLAN amendment)
CAP = 20
INDEX = True
MAPS = [40, 43, 58, 59, 60, 66, 67, 90, 111, 123,
        48, 74, 75, 94, 100, 102, 171, 174, 176, 177, 181, 184, 199, 200]
COMPARATORS = [5, 6, 20, 0, 1, 2]
PLANT = (4, 5, 6)   # C1: contradicting units on chirotope(4, 5, 6, INF); no symmetry-normalisation unit touches it


class Formula:
    """index=True: definition clauses of Tseitin gates are always kept; a constraint clause is indexed by the faces of the
    named predicates / chirotope signs it mentions (the face tuple of its constraint instance). index=False (strict): every
    clause is indexed by the faces its variables transitively depend on."""

    def __init__(self, c, planted=(), index=True):
        self.nv = c.nv
        qv = set(c.qvar.values())
        sup = {v: sum(1 << e for e in S if e < N) for S, v in c.qvar.items()}
        sup[1] = 0
        gates = sorted([(z, key) for key, z in c._and.items()] + [(z, key) for key, z in c._xor.items() if len(key) == 2])
        defs = set()
        for key, z in c._and.items():
            defs.update([(-z, l) for l in key] + [tuple([z] + [-l for l in key])])
        for (a, b), z in ((k, z) for k, z in c._xor.items() if len(k) == 2):
            defs.update([(-z, a, b), (-z, -a, -b), (z, -a, b), (z, a, -b)])
        named = {}
        if index:
            for key, lit in c.named.items():
                m = sum(1 << x for x in key[1:] if isinstance(x, int) and x < N)
                v = abs(lit)
                if v not in qv and v != 1 and (v not in named or bin(m).count('1') < bin(named[v]).count('1')):
                    named[v] = m
        for z, key in gates:    # a gate's inputs are created before it
            sup[z] = 0
            for l in key:
                sup[z] |= sup[abs(l)]
            if z in named:
                sup[z] = named[z]
        for z, m in named.items():
            sup[z] = m
        self.symbreak = {cl[0] for cl in c.clauses if len(cl) == 1 and abs(cl[0]) in qv}   # before planting
        self.groups = {}
        for cl in list(c.clauses) + [list(u) for u in planted]:
            if index and tuple(cl) in defs:
                m = 0
            else:
                m = self._m(sup, cl)
            self.groups.setdefault(m, []).append(cl)

    @staticmethod
    def _m(sup, cl):
        m = 0
        for l in cl:
            m |= sup[abs(l)]
        return m

    def sub(self, F, drop_symbreak=False):
        out = [cl for m, g in self.groups.items() if m & ~F == 0 for cl in g]
        if drop_symbreak:
            out = [cl for cl in out if not (len(cl) == 1 and cl[0] in self.symbreak)]
        return out


class Sub:
    def __init__(self, nv, clauses):
        self.nv, self.clauses = nv, clauses

    def dimacs(self, path, comments=()):
        pilot.CNF.dimacs(self, path, comments)


def mask(F):
    return sum(1 << e for e in F)


def solve_sub(fm, F, out, name, drop_symbreak=False):
    r = pilot.solve(Sub(fm.nv, fm.sub(mask(F), drop_symbreak)), out, name, CAP, checker_timeout=CAP)
    return {'faces': list(F), 'status': r['status'], 'seconds': round(r['seconds'], 3), 'clauses': r['clauses'],
            'cnf_sha256': r['cnf_sha256'], 'proof_sha256': r.get('proof_sha256')}


def formula_for(index):
    rec = pilot.census(9, 3)['maps'][index]
    c = pilot.CNF(9); pilot.build(c, pilot.from_links(rec['links']), pilot.ALL_OPTS)
    h = hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest()
    recs = [json.loads(p.read_text()) for p in (E03 / 'results').glob('**/result.json')]
    recorded = {r['formula_sha256'] for r in recs if r.get('map_index') == index and r.get('formula_sha256')}
    if recorded and recorded != {h}:
        raise SystemExit(f'map {index}: formula hash {h} differs from recorded {recorded}')
    return Formula(c, index=INDEX), {'formula_sha256': h, 'recorded_hash_match': bool(recorded), 'pattern': rec['extra_pattern']}


def control_formula(name):
    """C0: convex control, SAT. C1: C0 plus contradicting units on chirotope(PLANT + INF). C2: another map's links with the
    control's planes pinned (UNSAT-VERIFIED in item 1); its core size is not known in advance, only cross-checked."""
    data = json.loads((E03 / 'control_f9.json').read_text())
    links = {int(k): v for k, v in data['negative_links' if name == 'C2' else 'links'].items()}
    tris = sorted({tuple(sorted((x, a, b))) for x, link in links.items() for a, b in zip(link, link[1:] + link[:1])})
    c = pilot.CNF(9); pilot.build(c, pilot.Triangulation(9, tris, links=links, submap=True), pilot.ALL_OPTS)
    planted = []
    if name == 'C1':
        q = c.qvar[tuple(sorted(PLANT + (N,)))]
        planted = [[q], [-q]]
    if name == 'C2':
        planted = [[c.qvar[S] if v > 0 else -c.qvar[S]] for S, v in pilot.chirotope_from_planes(data['planes']).items()]
    return Formula(c, planted=planted, index=INDEX), {'formula_sha256': None}


def study(fm, out):
    levels = {k: [solve_sub(fm, F, out, f'k{k}_' + ''.join(map(str, F))) for F in itertools.combinations(range(N), k)]
              for k in range(KMIN, KDESC + 1)}
    unsat = {k: [r['faces'] for r in v if r['status'] == 'UNSAT-VERIFIED'] for k, v in levels.items()}
    kmin = next((k for k in range(KMIN, KMAX + 1) if unsat[k]), None)
    mins = unsat[kmin] if kmin else []
    armN = [solve_sub(fm, F, out, 'N_' + ''.join(map(str, F)), drop_symbreak=True) for F in mins]
    six = {tuple(F) for F in unsat[KMAX]}
    # monotone: every superset of an UNSAT set must be UNSAT or TIMEOUT (a SAT or an error means a bug)
    mono = all(r['status'] in ('UNSAT-VERIFIED', 'TIMEOUT') for k2 in range(KMIN + 1, KDESC + 1) for r in levels[k2]
               if any(set(F) <= set(r['faces']) for k in range(KMIN, k2) for F in unsat[k]))
    return {'kmin': kmin, 'min_sets': mins, 'n_unsat_by_level': {k: len(v) for k, v in unsat.items()},
            'unsat6': unsat[KMAX], 'timeouts': {k: sum(r['status'] == 'TIMEOUT' for r in v) for k, v in levels.items()},
            'other_status': sorted({r['status'] for v in levels.values() for r in v}
                                   - {'UNSAT-VERIFIED', 'SAT', 'TIMEOUT'}),
            'armN': armN, 'monotone_ok': mono, 'levels': levels,
            'solver_seconds': round(sum(r['seconds'] for v in levels.values() for r in v), 1)}


def _core_child(nv, groups, q):
    from pysat.solvers import Cadical153
    s, sel = Cadical153(), {}
    for i, (m, g) in enumerate(sorted(groups.items())):
        if m:
            sel[m] = nv + 1 + i
        for cl in g:
            s.add_clause(([-sel[m]] if m else []) + cl)
    if s.solve(assumptions=list(sel.values())):
        q.put(('SAT', None)); return
    inv = {v: m for m, v in sel.items()}
    q.put(('UNSAT', [inv[l] for l in s.get_core()]))


def cross_check(fm, out, kmin, cap=300):
    """Independent method: one assumption literal per support group, solver core, union of the core groups' faces."""
    ctx = mp.get_context('fork'); q = ctx.Queue()
    p = ctx.Process(target=_core_child, args=(fm.nv, fm.groups, q), daemon=True)
    p.start(); p.join(cap)
    if p.is_alive():
        p.terminate(); p.join(); return {'status': 'UNRESOLVED'}
    st, core = q.get(timeout=5)
    if st == 'SAT':
        return {'status': 'SAT'}
    u = 0
    for m in core:
        u |= m
    U = [e for e in range(N) if u >> e & 1]
    r = {'core_groups': len(core), 'union_faces': U}
    r['sub_union'] = solve_sub(fm, U, out, 'U') if len(U) < N else {'status': 'whole formula'}
    ok = (kmin is None or len(U) >= kmin) and r['sub_union']['status'] in ('UNSAT-VERIFIED', 'whole formula')
    r['status'] = 'OK' if ok else 'DISAGREE'
    return r


def unit(name, outroot, cross=False):
    out = outroot / name
    if (out / 'result.json').exists():
        return
    shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    t0 = time.monotonic()
    if name.startswith('C'):
        fm, meta = control_formula(name)
    else:
        fm, meta = formula_for(int(name))
    res = study(fm, out)
    if cross:
        res['cross_check'] = cross_check(fm, out, res['kmin'])
    res.update(meta, unit=name, wall_seconds=round(time.monotonic() - t0, 1))
    pilot.dump(out / 'result.json', res)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=10)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--only', nargs='*', help='unit names (map index, C0, C1) instead of the sharded list')
    ap.add_argument('--strict', action='store_true', help='arm S: index every clause by transitive variable support')
    ap.add_argument('--cross', action='store_true', help='add the assumption-core cross-check to the units run')
    a = ap.parse_args()
    global INDEX
    INDEX = not a.strict
    units = a.only or (['C0', 'C1', 'C2'] + [str(i) for i in MAPS + COMPARATORS])[a.shard::a.shards]
    a.out.mkdir(parents=True, exist_ok=True)
    for u in units:
        unit(u, a.out, cross=a.cross or u in ('C1', 'C2'))


if __name__ == '__main__':
    main()
