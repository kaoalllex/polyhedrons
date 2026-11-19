"""E-261119-01: the P3-sym power ladder on known answers, with map blocking by complete paired runs.

A run is an edge of the solid: the segment of the line L_jk = plane j ^ plane k between the vertices P_jka and P_jkb
(sorted triples), written (j, k, a, b) with j < k, a < b. Its predicate in the formula (PROVED-1, PLAN.md):
  end_jk(jka) and end_jk(jkb) and ed(jka, toward P_jkb) and no end_jk(jkm) for every plane m separating P_jka, P_jkb
where ed(t, toward P) is the edge bit of the half-line at t on the side of plane a that holds P (that side is
sigma_a(jkb), the formula's s bit), and m separates the two points iff sigma_m(jka) != sigma_m(jkb); the edge passes a
vertex without an end unchanged, so the run started at jka reaches jkb and stops there. A map is blocked by the
negated conjunction of its E run predicates and of every image under the normaliser of the action (the relabellings
n with n G n^-1 = G that keep each element's determinant): such a relabelling of an invariant solid is invariant under
the same action, and runs do not depend on plane orientation or on the reflection fixed by the gauge and the mirror.

Usage: ladder.py controls OUT | ladder.py unit NAME OUT | ladder.py summary RESULTS
"""
import importlib.util
import itertools
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_spec = importlib.util.spec_from_file_location(
    'p3sym', ROOT / 'experiments/E-261118-02-equivariant-census-free-formula/p3sym.py')
p3sym = importlib.util.module_from_spec(_spec); sys.modules['p3sym'] = p3sym; _spec.loader.exec_module(p3sym)
p3 = p3sym.p3
from omsat import chirotope_from_planes  # noqa: E402

C2 = [((1, 0, 3, 2, 5, 4, 7, 6), 1)]                                     # free C2 4 x 2, a half-turn
D2, S4, C3 = p3sym.D2, p3sym.S4, p3sym.C3
# relabellings putting each known object's half-turn into C2 (new plane i = old plane ORDER_C2[i]); for Mizhaev the
# square of its rotoreflection, (0 2)(1 3)(4 6)(5 7) in p3sym.ORDER, becomes (01)(23)(45)(67)
ORDER_C2 = {'roest_vigh': p3sym.ORDER['roest_vigh'],
            'mizhaev': tuple(p3sym.ORDER['mizhaev'][i] for i in (0, 2, 1, 3, 4, 6, 5, 7))}


def normaliser(F, gens):
    """Relabellings n of the planes with n g n^-1 in G and of the same determinant for every g in G."""
    G = p3sym.group(F, gens)
    out = []
    for n in itertools.permutations(range(F)):
        inv = [0] * F
        for i, v in enumerate(n):
            inv[v] = i
        if all(G.get(tuple(n[g[inv[i]]] for i in range(F))) == d for g, d in G.items()):
            out.append(n)
    return out


def runs_of(decoded_runs):
    """p3.decode's runs (j, k, u, v) -> frozenset of (j, k, a, b), a < b the third planes of the end vertices."""
    out = set()
    for j, k, u, v in decoded_runs:
        a, = set(u) - {j, k}; b, = set(v) - {j, k}
        out.add((j, k) + tuple(sorted((a, b))))
    return frozenset(out)


def image(runs, n):
    return frozenset(tuple(sorted((n[j], n[k]))) + tuple(sorted((n[a], n[b]))) for j, k, a, b in runs)


def decode_runs(chi, cells, F):
    """The runs of a decodable model: the run loop of p3.decode, copied (decode does not return its runs)."""
    d = p3.decode(chi, cells, F)
    if not d['ok']:
        return None
    S = set(cells); runs = []
    for j, k in itertools.combinations(range(F), 2):
        pts = [i for i in range(F) if i not in (j, k)]
        tri = {i: tuple(sorted((j, k, i))) for i in pts}
        rank = {q: sum(1 for p in pts if p != q and p3.sigma(chi, F, tri[q], p) == p3.chi_of(chi, (j, k, p, F)))
                for q in pts}
        order = sorted(pts, key=rank.get)
        seg = []
        for p, q in zip(order, order[1:]):
            V = 0
            for i in pts:
                s = p3.sigma(chi, F, tri[p], i) if i != p else p3.sigma(chi, F, tri[q], p)
                if s > 0:
                    V |= 1 << i
            seg.append(sum((V | sj << j | sk << k) in S for sj, sk in itertools.product((0, 1), repeat=2)) % 2)
        start = None
        for idx in range(len(seg) + 1):
            on = idx < len(seg) and seg[idx]
            if on and start is None:
                start = idx
            if not on and start is not None:
                runs.append((j, k, tri[order[start]], tri[order[idx]])); start = None
    assert len(runs) == d['E']
    return runs_of(runs)


def predicate_runs(chi, cells, F):
    """Pure-Python evaluation of the run predicate (module docstring) on every (j, k, a, b): the set where it holds."""
    S = set(cells)

    def occ(t):
        others = [k for k in range(F) if k not in t]
        U = sum(1 << r for r, k in enumerate(others) if p3.sigma(chi, F, t, k) > 0)
        return [p3.octant_cell(F, t, U, others, q) in S for q in range(8)]

    occs = {t: occ(t) for t in itertools.combinations(range(F), 3)}

    def ed(t, r, s):
        a, b = [x for x in range(3) if x != r]
        return sum(occs[t][(s << r) | (sa << a) | (sb << b)] for sa, sb in itertools.product((0, 1), repeat=2)) % 2

    end = lambda t, r: ed(t, r, 0) ^ ed(t, r, 1)
    out = set()
    for j, k in itertools.combinations(range(F), 2):
        for a, b in itertools.combinations([i for i in range(F) if i not in (j, k)], 2):
            u, v = tuple(sorted((j, k, a))), tuple(sorted((j, k, b)))
            if not (end(u, u.index(a)) and end(v, v.index(b))):
                continue
            if not ed(u, u.index(a), int(p3.sigma(chi, F, v, a) > 0)):
                continue
            between = [m for m in range(F) if m not in (j, k, a, b)
                       and p3.sigma(chi, F, u, m) != p3.sigma(chi, F, v, m)]
            if any(end(tuple(sorted((j, k, m))), tuple(sorted((j, k, m))).index(m)) for m in between):
                continue
            out.add((j, k, a, b))
    return frozenset(out)


class BlockFormula(p3sym.SymFormula):
    """SymFormula with map blocking by complete paired runs (module docstring)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._ed = {}; self._run = {}; self.blocked = []

    def ed(self, t, r, s):
        if (t, r, s) not in self._ed:
            a, b = [x for x in range(3) if x != r]
            v = self.model.NewBoolVar('edb%s_%d_%d' % (t, r, s))
            self.model.AddBoolXOr([self.occ[t, (s << r) | (sa << a) | (sb << b)]
                                   for sa, sb in itertools.product((0, 1), repeat=2)] + [v.Not()])
            self._ed[t, r, s] = v
        return self._ed[t, r, s]

    def run_lit(self, j, k, a, b):
        """A literal implied by the run predicate of (j, k, a, b) (the converse is not needed for blocking)."""
        key = (j, k, a, b)
        if key in self._run:
            return self._run[key]
        m = self.model
        u, v = tuple(sorted((j, k, a))), tuple(sorted((j, k, b)))
        ra, rb = u.index(a), v.index(b)
        conds = [self.end[u, ra], self.end[v, rb]]
        side = self.s[v, a]
        toward = m.NewBoolVar('tw%s' % (key,))      # toward <-> ed(u, ra, sigma_a(v))
        m.AddBoolOr([side.Not(), self.ed(u, ra, 1).Not(), toward]); m.AddBoolOr([side, self.ed(u, ra, 0).Not(), toward])
        m.AddBoolOr([side.Not(), self.ed(u, ra, 1), toward.Not()]); m.AddBoolOr([side, self.ed(u, ra, 0), toward.Not()])
        conds.append(toward)
        for x in range(self.F):
            if x in (j, k, a, b):
                continue
            w = tuple(sorted((j, k, x)))
            # free_x <-> not (x separates u, v and end_jk(w))
            sep = m.NewBoolVar('sep%s_%d' % (key, x))
            m.AddBoolXOr([self.s[u, x], self.s[v, x], sep.Not()])
            free = m.NewBoolVar('fr%s_%d' % (key, x))
            m.AddBoolOr([sep.Not(), self.end[w, w.index(x)].Not(), free.Not()])
            m.AddBoolOr([sep, free]); m.AddBoolOr([self.end[w, w.index(x)], free])
            conds.append(free)
        lit = m.NewBoolVar('run%s' % (key,))
        m.AddBoolOr([c.Not() for c in conds] + [lit])
        for c in conds:
            m.AddImplication(lit, c)
        self._run[key] = lit
        return lit

    def block_map(self, runs, norm):
        """Block every image of the run set under the relabellings `norm`; returns the number of distinct clauses."""
        images = {image(runs, n) for n in norm}
        for img in sorted(images, key=sorted):
            self.model.AddBoolOr([self.run_lit(*r).Not() for r in sorted(img)])
        self.blocked.append(len(images))
        return len(images)

    def pin_cells(self, cells):
        S = set(cells)
        for T in range(1 << self.F):
            self.model.Add(self.x[T] == int(T in S))


# ----------------------------------------------------------------------------- known objects

def known(name, action):
    """(planes in normal form under the action, ORDER used) of a known eight-face object."""
    h, _ = p3sym.fixtures()[name]
    order = ORDER_C2[name] if action is C2 else p3sym.ORDER[name]
    return p3sym.normal_form(h, order, action)


def pinned_model(planes, action, E=36, cap=120):
    """Pinned solve of a known object -> (record, chi, cells, runs)."""
    F = len(planes)
    f = BlockFormula(F, action, edges=E, chi=chirotope_from_planes(planes))
    rec, r = p3sym.solve_record(f, F, cap, workers=1)
    runs = decode_runs(r['chi'], r['cells'], F) if 'cells' in r else None
    return rec, r.get('chi'), r.get('cells'), runs


def map_runs():
    """{name: run set} of both known objects in their free-C2 labelling (from pinned solves)."""
    out = {}
    for name in ('roest_vigh', 'mizhaev'):
        rec, chi, cells, runs = pinned_model(known(name, C2), C2)
        assert rec['status'] == 'OPTIMAL' and runs is not None, rec
        out[name] = runs
    return out


def code(links):
    """Smallest census code of a map (p3sym.map_codes), as a string."""
    codes = p3sym.map_codes(links)
    return str(min(codes)) if codes else None


# ----------------------------------------------------------------------------- controls (session, seconds)

def controls(out):
    """E-261118-02's controls (rerun: p3sym.py changed after they were recorded), then the free-C2 and blocking ones."""
    from ladder_exact import verify
    out.mkdir(parents=True, exist_ok=False)
    man = p3.manifest_base(); t0 = time.monotonic(); c = {}
    c['p3sym_controls_PASS'] = p3sym.controls(out / 'p3sym')['PASS']
    c['normaliser_sizes'] = [len(normaliser(8, g)) for g in (C2, D2, S4)]
    c['normaliser_PASS'] = c['normaliser_sizes'][0] == 384
    c['C2_forced_zeros_PASS'] = p3sym.forced_zeros(8, C2) == []
    N = normaliser(8, C2); runs = {}; rows = []
    for name in ('roest_vigh', 'mizhaev'):
        h = known(name, C2)
        rec, chi, cells, R = pinned_model(h, C2)
        g = verify(h, rec['links'], require_all_pairs=True) if rec.get('decode_ok') else {}
        rows.append(dict(rec, name=name + '_C2_pinned', EMBEDDED=bool(g.get('EMBEDDED')),
                         V_E_F_chi=list(g.get('V_E_F_chi', [])), planes=h, known_type=p3sym.known_type(rec['links'])))
        c[name + '_C2_pinned'] = (rec['status'] == 'OPTIMAL' and rec.get('invariant') and bool(g.get('EMBEDDED'))
                                  and list(g['V_E_F_chi']) == [24, 36, 8, -4]
                                  and p3sym.known_type(rec['links']) == name)
        c[name + '_predicate_equals_decode'] = R is not None and predicate_runs(chi, cells, 8) == R
        runs[name] = dict(R=R, chi=chi, cells=cells)
    for name in ('roest_vigh', 'mizhaev'):
        other = 'mizhaev' if name == 'roest_vigh' else 'roest_vigh'
        for blocked, want in ((name, 'INFEASIBLE'), (other, 'OPTIMAL')):
            f = BlockFormula(8, C2, edges=36, chi=runs[name]['chi']); n = f.block_map(runs[blocked]['R'], N)
            r = f.solve(120); key = '%s_pinned_%s_blocked' % (name, blocked)
            rows.append(dict(name=key, status=r['status'], seconds=r['seconds'], clauses=n))
            c[key] = r['status'] == want
    # synthetic: the same end triples on one line, the other two pairings; chi and cells of Roest-Vigh pinned
    rv = runs['roest_vigh']; line = next((j, k) for j, k in sorted({r[:2] for r in rv['R']})
                                         if sum(r[:2] == (j, k) for r in rv['R']) == 2)
    pairs = sorted(r[2:] for r in rv['R'] if r[:2] == line); ends = sorted(set(pairs[0] + pairs[1]))
    alts = [p for p in (((ends[0], ends[1]), (ends[2], ends[3])), ((ends[0], ends[2]), (ends[1], ends[3])),
                        ((ends[0], ends[3]), (ends[1], ends[2]))) if sorted(p) != pairs]
    for label, P in [('own', pairs)] + [('alt%d' % i, p) for i, p in enumerate(alts)]:
        syn = frozenset({r for r in rv['R'] if r[:2] != line} | {line + p for p in P})
        f = BlockFormula(8, C2, edges=36, chi=rv['chi']); f.pin_cells(rv['cells']); f.block_map(syn, [tuple(range(8))])
        r = f.solve(60); key = 'synthetic_pairing_' + label
        rows.append(dict(name=key, line=line, pairs=P, status=r['status'], seconds=r['seconds'],
                         predicate_holds=all(line + p in predicate_runs(rv['chi'], rv['cells'], 8) for p in P)))
        c[key] = r['status'] == ('INFEASIBLE' if label == 'own' else 'OPTIMAL') and rows[-1]['predicate_holds'] == (label == 'own')
    p3.dump(out / 'rows.json', rows)
    p3.dump(out / 'map_runs.json', {k: sorted(v['R']) for k, v in runs.items()})
    report = dict(PASS=all(v for k, v in c.items() if isinstance(v, bool)), checks=c)
    p3.dump(out / 'controls.json', report)
    man.update(wall_seconds=round(time.monotonic() - t0, 1), sources_sha256=sources())
    p3.dump(out / 'manifest.json', man)
    print(json.dumps(report, indent=1, default=str))
    return report


def sources():
    return {str(p.relative_to(ROOT)): p3.sha(p) for p in (Path(__file__).resolve(), Path(p3sym.__file__).resolve(),
                                                          Path(p3.__file__).resolve())}


def known_runs():
    """{name: run set} recorded by the controls."""
    return {k: frozenset(tuple(r) for r in v) for k, v in
            json.loads((HERE / 'results/controls/map_runs.json').read_text()).items()}


# ----------------------------------------------------------------------------- units (owner run)

# name -> F, E, action, workers, cap seconds, models at most, block (map blocking on), pre (known maps blocked at the
# start), after (units recorded first; at most 10 cores at any time), stop_on_model (a model is a contradiction: stop)
U = lambda F, E, action, cap, models, block=False, pre=(), after=(), stop_on_model=False: dict(
    F=F, E=E, action=action, workers=5, cap=cap, models=models, block=block, pre=pre, after=after,
    stop_on_model=stop_on_model)
UNITS = {'D2_8_36_block': U(8, 36, D2, 900, 40, block=True),
         'S4_8_36_block': U(8, 36, S4, 900, 40, block=True),
         'C2_8_36_block': U(8, 36, C2, 5400, 80, block=True, after=('D2_8_36_block', 'S4_8_36_block')),
         'C2_8_30': U(8, 30, C2, 3600, 1, after=('D2_8_36_block', 'S4_8_36_block'), stop_on_model=True),
         'C3_9_39': U(9, 39, C3, 3600, 1, after=('C2_8_30',), stop_on_model=True),
         # session blocking controls (pilot): one known map blocked from the start, the other must come back
         'C2_8_36_pre_rv': U(8, 36, C2, 600, 1, block=True, pre=('roest_vigh',)),
         'C2_8_36_pre_mz': U(8, 36, C2, 600, 1, block=True, pre=('mizhaev',))}
ORDER_RUN = ('D2_8_36_block', 'S4_8_36_block', 'C2_8_36_block', 'C2_8_30', 'C3_9_39')
RUN_BUDGET = 19.0 * 3600        # core-seconds of the owner run (20 core-h minus at most 1.0 in the session)
LAST = 'C3_9_39'                # its cap shrinks to what the budget leaves (PLAN.md)


def records(results):
    return [json.loads(line) for p in sorted(Path(results).glob('*/results.jsonl'))
            for line in p.read_text().splitlines() if line.strip()]


def run_unit(name, out, cap):
    u = UNITS[name]; F, workers = u['F'], u['workers']
    t0 = time.monotonic(); deadline = t0 + cap
    f = BlockFormula(F, u['action'], edges=u['E'])
    N = normaliser(F, u['action']) if u['block'] else None
    for name0 in u['pre']:
        f.block_map(known_runs()[name0], N)
    proto = f.model.Proto()
    rec = dict(id=name, F=F, E=u['E'], workers=workers, cap=round(cap, 1), build_seconds=round(time.monotonic() - t0, 2),
               variables=len(proto.variables), constraints=len(proto.constraints), pre=list(u['pre']),
               normaliser=len(N) if N else None, models=[], blocked_maps=[], solves=[])
    while len(rec['models']) < u['models']:
        left = deadline - time.monotonic()
        if left <= 1:
            rec['ended_by'] = 'cap'; break
        m, r = p3sym.solve_record(f, F, left, workers, seed=len(rec['models']))
        rec['solves'].append(dict(status=m['status'], seconds=m['seconds']))
        if 'chi' not in r:
            rec['ended_by'] = 'infeasible' if m['status'] == 'INFEASIBLE' else 'cap'; break
        k = len(rec['models']); mname = '%s_m%d' % (name, k)
        p3.dump(out / (mname + '.model.json'), dict(m, chi=p3.chi_json(r['chi']), cells=r['cells']))
        R = decode_runs(r['chi'], r['cells'], F) if m['decode_ok'] else None
        if R is not None:
            m['code'] = code(m['links']); m['known_type'] = p3sym.known_type(m['links'])
            m['predicate_equals_decode'] = predicate_runs(r['chi'], r['cells'], F) == R
        if m['decode_ok'] and m['gp_ok'] and m.get('invariant'):
            left = deadline - time.monotonic()
            m['bridge'] = p3.bridge(out, mname, r['chi'], m['links'],
                                    tuple(max(1, min(c, left / 3)) for c in (90, 90, 60)))
        note = (m.get('bridge') or {}).get('status_note')
        rec['models'].append({k2: v for k2, v in m.items() if k2 != 'links'})
        if u['stop_on_model']:
            rec['ended_by'] = 'model: stop (contradiction with 3d, PLAN.md tree)'
            (out.parent / 'stop.candidate').write_text(mname + '\n'); break
        if note == 'REALIZED-ALL-PAIRS-PASS' and not m.get('known_type'):
            rec['ended_by'] = 'new map realized: stop (candidate-check)'
            (out.parent / 'stop.candidate').write_text(mname + '\n'); break
        if u['block'] and R is not None and m.get('invariant') and (note == 'REALIZED-ALL-PAIRS-PASS' or m.get('known_type')):
            rec['blocked_maps'].append(dict(model=mname, code=m['code'], clauses=f.block_map(R, N)))
        else:
            f.block(r['chi'])              # the map stays open (bridge failed, unknown type): this chirotope only
    else:
        rec['ended_by'] = 'models'
    rec['wall_seconds'] = round(time.monotonic() - t0, 1)
    rec['core_seconds'] = round(rec['wall_seconds'] * workers, 1)
    return rec


def unit(name, out):
    """One unit into OUT/results.jsonl, after the units it waits for; LAST takes what the budget leaves."""
    out.mkdir(parents=True, exist_ok=True)
    results = out.parent
    if name in {r['id'] for r in records(results)}:
        return
    man = p3.manifest_base(); man.update(unit=name, sources_sha256=sources())
    p3.dump(out / ('manifest-%d.json' % int(time.time())), man)
    while not set(UNITS[name]['after']) <= {r['id'] for r in records(results)}:
        if (results / 'stop.requested').exists():
            return
        time.sleep(30)
    cap = UNITS[name]['cap']
    rec = None
    if (results / 'stop.candidate').exists():
        rec = dict(id=name, ended_by='skipped: stop.candidate', wall_seconds=0, core_seconds=0, models=[])
    elif name == LAST:
        done = records(results)
        used = sum(r['core_seconds'] for r in done if r['id'] in ORDER_RUN)
        running = sum(UNITS[n]['cap'] * UNITS[n]['workers'] for n in ORDER_RUN
                      if n != name and n not in {r['id'] for r in done})
        cap = min(cap, (RUN_BUDGET - used - running) / UNITS[name]['workers'])
        if cap < 60:
            rec = dict(id=name, ended_by='skipped: budget', wall_seconds=0, core_seconds=0, models=[])
    if os.environ.get('P3SYM_CAP'):                 # pilot: the unit cut to this cap
        cap = min(cap, float(os.environ['P3SYM_CAP']))
    rec = rec or run_unit(name, out, cap)
    with (out / 'results.jsonl').open('a') as fh:
        fh.write(json.dumps(rec, default=str) + '\n')


def summary(results):
    rows = records(results)
    rep = {r['id']: {k: r.get(k) for k in ('ended_by', 'cap', 'wall_seconds', 'core_seconds', 'variables',
                                           'constraints', 'pre', 'blocked_maps')} for r in rows}
    for r in rows:
        rep[r['id']]['models'] = [{k: m.get(k) for k in ('status', 'seconds', 'gp_ok', 'decode_ok', 'invariant', 'V', 'E',
                                                         'known_type', 'code', 'predicate_equals_decode')}
                                  | dict(bridge=(m.get('bridge') or {}).get('status_note')) for m in r['models']]
    rep['core_hours'] = round(sum(r.get('core_seconds', 0) for r in rows) / 3600, 2)
    print(json.dumps(rep, indent=1, default=str))
    return rep


if __name__ == '__main__':
    mode, *rest = sys.argv[1:]
    if mode == 'controls':
        sys.exit(0 if controls(Path(rest[0]))['PASS'] else 1)
    elif mode == 'unit':
        unit(rest[0], Path(rest[1]))
    elif mode == 'summary':
        summary(rest[0])
    else:
        raise SystemExit(__doc__)
