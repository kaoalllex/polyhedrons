"""P3-sym (E-261118-02): the census-free formula of E-261116-07 with an opt-in group action on the planes.

An action is a list of generators (perm, det): perm maps plane i to plane perm[i] (INF is fixed), det = +-1 is the
determinant of the isometry. For a solid invariant under an isometry group fixing the origin, with outward planes
h_m = (n_m, -d_m), A = diag(g, 1) is orthogonal and A h_m = lambda h_perm(m) with lambda > 0, so (PROVED-1, PLAN.md):
  chi(perm S) = det chi(S) for every quad S        (det A = det g, A fixes h_INF)
  x_T = x_gT, gT has bit perm(m) iff T has bit m  ((A h).(A x^) = h.x^)
Outward planes carry the trivial orientation cocycle, and so does every reorientation constant on orbits; the orbit
gauge (sigma_k(t) = + for the least plane k of each orbit, t = 012 or 345 not containing k) fixes those flips, and the
mirror normalisation chi(0, 3, 6, INF) = + the global reflection (it negates chi, keeps cells, gauge and action).
The equalities of sigma, tau, b and end are implied by those of chi and x; they are stated to help presolve.

Usage: p3sym.py controls OUT | p3sym.py unit NAME OUT | p3sym.py summary RESULTS
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
sys.path.insert(0, str(ROOT / 'code'))
_spec = importlib.util.spec_from_file_location('p3', ROOT / 'experiments/E-261116-07-census-free-s1-ladder/p3.py')
p3 = importlib.util.module_from_spec(_spec); sys.modules['p3'] = p3; _spec.loader.exec_module(p3)
from omsat import chirotope_from_planes  # noqa: E402
from omsat_sym import sym_consistency  # noqa: E402

D2 = [((1, 0, 3, 2, 5, 4, 7, 6), 1), ((2, 3, 0, 1, 6, 7, 4, 5), 1)]     # 2 x 4, three half-turns
S4 = [((1, 2, 3, 0, 5, 6, 7, 4), -1)]                                     # 2 x 4, a rotoreflection of order 4
C3 = [((1, 2, 0, 4, 5, 3, 7, 8, 6), 1)]                                   # 3 + 3 + 3, a rotation of order 3
MIRROR = (0, 3, 6)


def group(F, gens):
    """Closure {perm: det}; ValueError if one permutation gets both determinants."""
    G = {tuple(range(F)): 1}; frontier = list(G)
    while frontier:
        new = []
        for x in frontier:
            for g, d in gens:
                y = tuple(g[x[i]] for i in range(F)); dy = d * G[x]
                if y in G:
                    if G[y] != dy:
                        raise ValueError('inconsistent determinants for %s' % (y,))
                    continue
                G[y] = dy; new.append(y)
        frontier = new
    return G


def forced_zeros(F, gens):
    """Quads whose sign the action forces to 0 (an element fixing S as a set with det * parity = -1)."""
    G = group(F, gens)
    return sorted({S for S, _ in sym_consistency(list(G), G, n=F)})


def orbits(F, gens):
    G = group(F, gens)
    return sorted({tuple(sorted({g[i] for g in G})) for i in range(F)})


def quad_orbits(F, gens):
    G = group(F, gens)
    img = lambda g, S: tuple(sorted(g[e] if e < F else F for e in S))
    return len({min(img(g, S) for g in G) for S in itertools.combinations(range(F + 1), 4)})


def gauge_pairs(F, gens):
    """(t, k): sigma_k(t) = + for the least plane k of each orbit."""
    return [((0, 1, 2) if O[0] >= 3 else (3, 4, 5), O[0]) for O in orbits(F, gens)]


def cell(g, T, F):
    return sum(1 << g[m] for m in range(F) if T >> m & 1)


class SymFormula(p3.Formula):
    """p3.Formula restricted to solids invariant under `action`; gauge = the orbit gauge, mirror = chi(0,3,6,INF) = +."""

    def __init__(self, F, action, gauge=True, mirror=True, **kw):
        bad = forced_zeros(F, action)
        if bad:
            raise ValueError('the action forces chi%s = 0: out of domain' % (bad[0],))
        super().__init__(F, gauge=False, **kw)
        self.action = action
        m = self.model; INF = F
        eq = lambda a, b: (m.AddImplication(a, b), m.AddImplication(b, a))
        for g, d in action:
            P = list(g) + [INF]
            for S in self.quads:
                src = self.p[S]
                eq(self.pos(tuple(P[e] for e in S)), src if d > 0 else src.Not())
            for T in range(1 << F):
                eq(self.x[T], self.x[cell(g, T, F)])
                eq(self.tau[T], self.tau[cell(g, T, F)])
            for t in self.triples:
                gt = tuple(sorted(g[i] for i in t))
                for k in range(F):
                    if k not in t:
                        eq(self.s[t, k], self.s[gt, g[k]])
                for r in range(3):
                    eq(self.end[t, r], self.end[gt, gt.index(g[t[r]])])
            for (i, T), v in self.b.items():
                eq(v, self.b[g[i], cell(g, T, F)])
        if gauge:
            for t, k in gauge_pairs(F, action):
                m.Add(self.s[t, k] == 1)
        if mirror:
            m.Add(self.p[MIRROR + (INF,)] == 1)


def invariant(chi, cells, F, action):
    """Pure-Python check of a model against the action (independent of the CP-SAT constraints)."""
    S = set(cells)
    for g, d in action:
        P = list(g) + [F]
        if any(p3.chi_of(chi, tuple(P[e] for e in Q)) != d * chi[Q] for Q in chi):
            return False
        if {cell(g, T, F) for T in S} != S:
            return False
    return True


# ----------------------------------------------------------------------------- known objects in normal form

def oriented(planes, action):
    """The reorientation (one sign per plane, first in lexicographic order) whose chirotope satisfies the action."""
    F = len(planes)
    for r in itertools.product((1, -1), repeat=F):
        h = [[s * v for v in row] for s, row in zip(r, planes)]
        chi = chirotope_from_planes(h)
        if all(chi[Q] for Q in chi) and invariant(chi, [], F, action):
            return h
    raise ValueError('no orientation satisfies the action')


def normal_form(planes, order, action):
    """Relabel (new plane i = old plane order[i]), orient for the action, flip orbits into the orbit gauge, reflect
    x -> -x if chi(0, 3, 6, INF) < 0."""
    F = len(planes)
    h = oriented([list(map(int, planes[i])) for i in order], action)
    chi = chirotope_from_planes(h)
    for t, k in gauge_pairs(F, action):
        if p3.sigma(chi, F, t, k) < 0:
            O = next(O for O in orbits(F, action) if k in O)
            h = [[-v for v in row] if i in O else row for i, row in enumerate(h)]
            chi = chirotope_from_planes(h)
    if chi[MIRROR + (F,)] < 0:
        h = [[-row[0]] + row[1:] for row in h]
        chi = chirotope_from_planes(h)
    assert invariant(chi, [], F, action) and chi[MIRROR + (F,)] > 0
    assert all(p3.sigma(chi, F, t, k) > 0 for t, k in gauge_pairs(F, action))
    return h


def fixtures():
    """{name: (planes, links)} of the two known eight-face objects (E-261103-05 fixtures)."""
    p05 = p3.load('E-261103-05-s5-symmetric-solid-first', 'pilot05')
    return {name: (h, links) for name, h, links in p05.fixtures()}


# Relabellings that put each object's chirotope automorphisms into the standard generators (PLAN.md, EXACT):
# Roest-Vigh's planes already carry D2 as listed; Mizhaev's rotoreflection is (0 6 1 7)(2 5 3 4).
ORDER = {'roest_vigh': (0, 1, 2, 3, 4, 5, 6, 7), 'mizhaev': (0, 6, 1, 7, 2, 5, 3, 4)}
GROUP = {'roest_vigh': D2, 'mizhaev': S4}


def relabel_links(links, order):
    new = {old: i for i, old in enumerate(order)}
    return {new[f]: [new[j] for j in links[f]] for f in links}


# ----------------------------------------------------------------------------- runs

def solve_record(f, F, cap, workers, seed=0):
    r = f.solve(cap, seed=seed, workers=workers)
    rec = dict(status=r['status'], seconds=r['seconds'])
    if 'cells' in r:
        d = p3.decode(r['chi'], r['cells'], F)
        rec.update(gp_ok=p3.gp_ok(r['chi'], F + 1), decode_ok=d['ok'], decode_reason=d['reason'],
                   links=d.get('links'), V=d.get('V'), E=d.get('E'))
        if getattr(f, 'action', None):
            rec['invariant'] = invariant(r['chi'], r['cells'], F, f.action)
    return rec, r


def pinned(name, planes, action, gauge=True, mirror=True, cap=120):
    """One pinned solve of a known object (or a corrupted copy) under an action -> record with EMBEDDED."""
    from ladder_exact import verify
    F = len(planes)
    try:
        f = SymFormula(F, action, gauge=gauge, mirror=mirror, edges=36, chi=chirotope_from_planes(planes))
    except ValueError as exc:
        return dict(name=name, status='OUT-OF-DOMAIN', error=str(exc))
    rec, _ = solve_record(f, F, cap, workers=1)
    rec['name'] = name
    if rec.get('decode_ok'):
        g = verify(planes, rec['links'], require_all_pairs=True)
        rec.update(EMBEDDED=bool(g.get('EMBEDDED')), V_E_F_chi=list(g['V_E_F_chi']))
    return rec


def controls(out):
    out.mkdir(parents=True, exist_ok=False)
    man = p3.manifest_base(); t0 = time.monotonic()
    fx = fixtures(); c = {}
    # group bookkeeping (EXACT): orbit counts of the lead review, forced zeros of the excluded families
    c['quad_orbits'] = dict(D2=quad_orbits(8, D2), S4=quad_orbits(8, S4), C3=quad_orbits(9, C3))
    c['quad_orbits_PASS'] = c['quad_orbits'] == dict(D2=36, S4=34, C3=72)
    excluded = {'C4_2x4': [((1, 2, 3, 0, 5, 6, 7, 4), 1)],
                'Cs_3x2+1': [((1, 0, 3, 2, 5, 4, 6), -1)], 'C2_3x2+1_standard_chart': [((1, 0, 3, 2, 5, 4, 6), 1)],
                'Cs_4x2+1': [((1, 0, 3, 2, 5, 4, 7, 6, 8), -1)]}
    c['forced_zeros'] = {k: forced_zeros(len(g[0][0]), g)[:3] for k, g in excluded.items()}
    c['forced_zeros']['in_domain'] = {k: forced_zeros(F, g) for k, F, g in (('D2', 8, D2), ('S4', 8, S4), ('C3', 9, C3))}
    c['forced_zeros_PASS'] = (all(c['forced_zeros'][k] for k in excluded)
                              and not any(c['forced_zeros']['in_domain'].values()))
    rows = []
    for name in ('roest_vigh', 'mizhaev'):
        h, links = fx[name]
        nf = normal_form(h, ORDER[name], GROUP[name])
        rows.append(dict(pinned(name + '_normal_form', nf, GROUP[name]), planes=nf))
        other = S4 if name == 'roest_vigh' else D2
        rows.append(pinned(name + '_wrong_group', nf, other))
    rv = normal_form(fx['roest_vigh'][0], ORDER['roest_vigh'], D2)
    rows.append(pinned('roest_vigh_raw_orientation_gauge_off', [list(map(int, r)) for r in fx['roest_vigh'][0]], D2,
                       gauge=False, mirror=False))
    # one orbit of quads flipped: still equivariant, breaks the Grassmann-Pluecker relations
    chi = chirotope_from_planes(rv); G = group(8, D2)
    for Q in sorted(chi):
        orb = {tuple(sorted(g[e] if e < 8 else 8 for e in Q)) for g in G}
        bad = {S: (-chi[S] if S in orb else chi[S]) for S in chi}
        if invariant(bad, [], 8, D2) and not p3.gp_ok(bad, 9):
            break
    f = SymFormula(8, D2, edges=36, chi=bad)
    r = f.solve(60)
    rows.append(dict(name='roest_vigh_orbit_flipped', orbit=sorted(orb), status=r['status'], seconds=r['seconds']))
    p3.dump(out / 'pinned_rows.json', rows)
    by = {r['name']: r for r in rows}
    good = lambda n: (by[n]['status'] == 'OPTIMAL' and by[n].get('EMBEDDED') and by[n].get('invariant')
                      and by[n].get('V_E_F_chi') == [24, 36, 8, -4])
    for n in ('roest_vigh_normal_form', 'mizhaev_normal_form', 'roest_vigh_raw_orientation_gauge_off'):
        c[n] = good(n)
    for n in ('roest_vigh_wrong_group', 'mizhaev_wrong_group', 'roest_vigh_orbit_flipped'):
        c[n] = by[n]['status'] == 'INFEASIBLE'
    report = dict(PASS=all(v for k, v in c.items() if isinstance(v, bool)), checks=c)
    p3.dump(out / 'controls.json', report)
    man.update(wall_seconds=round(time.monotonic() - t0, 1), outputs_sha256={p.name: p3.sha(p) for p in out.iterdir()},
               sources_sha256={str(p.relative_to(ROOT)): p3.sha(p) for p in (Path(__file__).resolve(),
                                                                         Path(p3.__file__).resolve())})
    p3.dump(out / 'manifest.json', man)
    print(json.dumps(report, indent=1, default=str))
    return report


# Units (PLAN.md and amendment 1): name -> F, E, action or None (then the plain cube of E-261116-07), workers, cap
# seconds, models at most, units that must be recorded first (at most 10 cores at any time).
U = lambda F, E, action, cube, workers, cap, models, after=(): dict(F=F, E=E, action=action, cube=cube, workers=workers,
                                                                   cap=cap, models=models, after=after)
UNITS = {'D2_8_36': U(8, 36, D2, None, 5, 1800, 3), 'S4_8_36': U(8, 36, S4, None, 5, 1800, 3),
         'C3_9_45': U(9, 45, C3, None, 5, 3600, 20), 'C3_9_51': U(9, 51, C3, None, 5, 3600, 20),
         'C3_9_57': U(9, 57, C3, None, 5, 3600, 20, after=('C3_9_45',)),
         'plain_cube5_8_36': U(8, 36, None, 5, 8, 900, 3, after=('C3_9_45', 'C3_9_51', 'C3_9_57'))}
RUN_BUDGET = 5.6 * 3600          # core-seconds of the rung units (6 core-h minus the session's controls and pilot)
RUNG = ('D2_8_36', 'S4_8_36', 'plain_cube5_8_36')


def records(results):
    return [json.loads(line) for p in sorted(Path(results).glob('*/results.jsonl')) for line in p.read_text().splitlines()
            if line.strip()]


def map_codes(links):
    """Census canonical codes (E-261103-01, minimised over orientation) of a map given by per-face links of arbitrary
    direction: every choice of directions that the census accepts."""
    sys.path.insert(0, str(ROOT / 'experiments/E-261103-01-s5-map-census'))
    import census
    L = [links[i] for i in range(len(links))]; out = set()
    for flips in itertools.product((0, 1), repeat=len(L)):
        try:
            out.add(census.from_links([l[::-1] if f else l for l, f in zip(L, flips)]).canon()[0])
        except (ValueError, AssertionError):
            continue
    return out


def known_type(links):
    """The known eight-face object whose map is the given one, or None (EXACT, census codes)."""
    if len(links) != 8:
        return None
    codes = map_codes(links)
    return next((name for name, (_, l) in fixtures().items() if codes & map_codes(l)), None)


def run_unit(name, out, cap=None):
    u = UNITS[name]; F, workers = u['F'], u['workers']
    cap = u['cap'] if cap is None else cap
    t0 = time.monotonic(); deadline = t0 + cap
    f = SymFormula(F, u['action'], edges=u['E']) if u['action'] else p3.Formula(F, edges=u['E'], cube=p3.cube(F, u['cube']))
    proto = f.model.Proto()
    rec = dict(id=name, F=F, E=u['E'], workers=workers, cap=round(cap, 1), build_seconds=round(time.monotonic() - t0, 2),
               variables=len(proto.variables), constraints=len(proto.constraints), models=[], solves=[])
    while len(rec['models']) < u['models']:
        left = deadline - time.monotonic()
        if left <= 1:
            rec['ended_by'] = 'cap'; break
        m, r = solve_record(f, F, left, workers, seed=len(rec['models']))
        rec['solves'].append(dict(status=m['status'], seconds=m['seconds']))
        if 'chi' not in r:
            rec['ended_by'] = 'infeasible' if m['status'] == 'INFEASIBLE' else 'cap'; break
        k = len(rec['models']); mname = '%s_m%d' % (name, k)
        p3.dump(out / (mname + '.model.json'), dict(m, chi=p3.chi_json(r['chi']), cells=r['cells']))
        if m['decode_ok'] and m['gp_ok'] and m.get('invariant', True):
            left = deadline - time.monotonic()
            m['bridge'] = p3.bridge(out, mname, r['chi'], m['links'], tuple(max(1, min(c, left / 3)) for c in (90, 90, 60)))
            if m['bridge'].get('status_note') == 'REALIZED-ALL-PAIRS-PASS':
                m['known_type'] = known_type(m['links'])
        rec['models'].append({k2: v for k2, v in m.items() if k2 != 'links'})
        if (m.get('bridge') or {}).get('status_note') == 'REALIZED-ALL-PAIRS-PASS':
            rec['ended_by'] = 'realized'; break
        f.block(r['chi'])
    else:
        rec['ended_by'] = 'models'
    rec['wall_seconds'] = round(time.monotonic() - t0, 1)
    rec['core_seconds'] = round(rec['wall_seconds'] * workers, 1)
    return rec


def unit(name, out):
    """One unit into OUT/results.jsonl, after the units it waits for; the plain side unit fits the rung budget."""
    out.mkdir(parents=True, exist_ok=True)
    results = out.parent
    if name in {r['id'] for r in records(results)}:
        return
    man = p3.manifest_base(); man.update(unit=name)
    p3.dump(out / ('manifest-%d.json' % int(time.time())), man)
    while not set(UNITS[name]['after']) <= {r['id'] for r in records(results)}:
        if (results / 'stop.requested').exists():
            return
        time.sleep(30)
    cap = None
    if name == 'plain_cube5_8_36':
        used = sum(r['core_seconds'] for r in records(results) if r['id'] in RUNG)
        cap = min(UNITS[name]['cap'], (RUN_BUDGET - used) / UNITS[name]['workers'])
        if cap < 60:
            rec = dict(id=name, ended_by='skipped: budget', budget_core_seconds_left=round(RUN_BUDGET - used, 1),
                       wall_seconds=0, core_seconds=0, models=[])
            with (out / 'results.jsonl').open('a') as fh:
                fh.write(json.dumps(rec) + '\n')
            return
    if os.environ.get('P3SYM_CAP'):                 # pilot: the unit cut to this cap
        cap = min(cap or UNITS[name]['cap'], float(os.environ['P3SYM_CAP']))
    rec = run_unit(name, out, cap)
    with (out / 'results.jsonl').open('a') as fh:
        fh.write(json.dumps(rec, default=str) + '\n')


def summary(results):
    rows = records(results)
    rep = {r['id']: {k: r.get(k) for k in ('ended_by', 'cap', 'wall_seconds', 'core_seconds', 'variables', 'constraints')}
           for r in rows}
    for r in rows:
        rep[r['id']]['models'] = [{k: m.get(k) for k in ('status', 'seconds', 'gp_ok', 'decode_ok', 'invariant', 'V', 'E',
                                                         'known_type')}
                                  | dict(bridge=(m.get('bridge') or {}).get('status_note')) for m in r['models']]
    rep['core_hours'] = round(sum(r.get('core_seconds', 0) for r in rows) / 3600, 2)
    print(json.dumps(rep, indent=1))
    return rep


if __name__ == '__main__':
    mode, *rest = sys.argv[1:]
    if mode == 'controls':
        sys.exit(0 if controls(Path(rest[0]))['PASS'] else 1)
    elif mode == 'unit':
        unit(rest[0], Path(rest[1]))
    elif mode == 'summary':
        summary(rest[0])
    elif mode == 'types':            # known type of every saved realized candidate under RESULTS
        rows = {str(p.relative_to(rest[0])): known_type({int(k): v for k, v in json.loads(p.read_text())['links'].items()})
                for p in sorted(Path(rest[0]).rglob('*.candidate.json'))}
        print(json.dumps(rows, indent=1))
    else:
        raise SystemExit(__doc__)
