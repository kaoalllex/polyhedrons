"""E-261119-02 stage A: census of admissible triangular maps with a prescribed rotation of the vertices.

The dual of a cubic S1 / S5 solid with F faces is a triangulated closed orientable surface: vertices = faces, triangles =
solid vertices, edges = solid edges (pair multiplicity = number of edges between two faces). Admissible = distinct
corner triples (census.py). A rotation of the solid permuting the faces as rho is an orientation-preserving map
automorphism that acts on vertices as rho. Completeness (PROVED-1, PLAN.md): such a map's oriented triangles form a
rho-invariant set with distinct supports, a union of fixed triangles and moving orbits (rows); every directed pair
(a, b) is the side of exactly m(ab) triangles, and m is rho-invariant; the gluing alpha (dart u->v with a dart v->u)
commutes with the dart action. So the search covers, per excess vector of the pair orbits (up to the normaliser of
<rho>, which maps rho-maps to rho-maps), per choice of fixed triangles: every exact cover of the directed-pair orbit
demands by rows, then every equivariant gluing, then the vertex-link check (one cycle per vertex) and census.review.check.

Usage: symcensus.py shard SHARD SHARDS OUT SECONDS [STAGE] | symcensus.py summary OUT [STAGE] | symcensus.py units [STAGE]
STAGE: A (genus 4 targets, default), A5c3 or A5c2 (genus 5, C3 or C2 family, PLAN amendment 4)
"""
from collections import Counter
import functools
import importlib.util
import itertools
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CENSUS_DIR = ROOT / 'experiments/E-261103-01-s5-map-census'
_spec = importlib.util.spec_from_file_location('census', CENSUS_DIR / 'census.py')
census = importlib.util.module_from_spec(_spec); sys.modules['census'] = census; _spec.loader.exec_module(census)
review = census.review

C3_9 = (1, 2, 0, 4, 5, 3, 7, 8, 6)                  # 3 + 3 + 3
C2F_9 = (1, 0, 3, 2, 5, 4, 7, 6, 8)                 # 4 x 2 + 1 (one fixed face)
C2F_7 = (1, 0, 3, 2, 5, 4, 6)                       # 3 x 2 + 1 (Szilassi's family)
C2_8 = (1, 0, 3, 2, 5, 4, 7, 6)                     # 4 x 2, free
# name -> (F, genus, rho, role); C3 before C2 within a stage (PLAN.md). Stage A: targets C3_9_4 and C2f_9_4, the rest
# are controls; amendment 4 (genus 5): stage A5c3 (C3_9_5 with the C3 control), stage A5c2 (C2f_9_5 with the C2 ones)
CONFIGS = {'C3_9_3': (9, 3, C3_9, 'control'), 'C3_9_4': (9, 4, C3_9, 'target'),
           'C2f_7_1': (7, 1, C2F_7, 'control'), 'C2_8_2': (8, 2, C2_8, 'control'),
           'C2f_9_3': (9, 3, C2F_9, 'control'), 'C2_8_3': (8, 3, C2_8, 'control'),
           'C2f_9_4': (9, 4, C2F_9, 'target'), 'C3_9_5': (9, 5, C3_9, 'target'), 'C2f_9_5': (9, 5, C2F_9, 'target')}
FAMILY = {n: 'C3' if n.startswith('C3') else 'C2' for n in CONFIGS}
STAGES = {'A': ['C3_9_3', 'C3_9_4', 'C2f_7_1', 'C2_8_2', 'C2f_9_3', 'C2_8_3', 'C2f_9_4'],
          'A5c3': ['C3_9_3', 'C3_9_5'], 'A5c2': ['C2f_7_1', 'C2_8_2', 'C2f_9_3', 'C2_8_3', 'C2f_9_5']}
TARGETS = {'A': {'C3': 'C3_9_4', 'C2': 'C2f_9_4'}, 'A5c3': {'C3': 'C3_9_5'}, 'A5c2': {'C2': 'C2f_9_5'}}
MAX_MULT = 3


def compose(a, b):
    """(a o b)(v) = a[b[v]]."""
    return tuple(a[v] for v in b)


def powers(rho):
    G = [tuple(range(len(rho)))]
    while compose(rho, G[-1]) != G[0]:
        G.append(compose(rho, G[-1]))
    return G


def tnorm(t):
    return min(t, t[1:] + t[:1], t[2:] + t[:2])


def timg(g, t):
    return tnorm(tuple(g[v] for v in t))


@functools.lru_cache(maxsize=None)
def normaliser(rho):
    G = set(powers(rho)); F = len(rho)
    out = []
    for s in itertools.permutations(range(F)):
        inv = [0] * F
        for i, v in enumerate(s):
            inv[v] = i
        if tuple(s[rho[inv[v]]] for v in range(F)) in G:      # s rho s^-1 in <rho>
            out.append(s)
    return out


class Setup:
    def __init__(self, F, genus, rho):
        self.F, self.genus, self.rho = F, genus, tuple(rho)
        self.G = powers(self.rho); self.p = len(self.G)
        self.E = 3 * (F + 2 * genus - 2)
        self.V = 2 * self.E // 3
        self.k = self.E - F * (F - 1) // 2
        assert self.k >= 0
        oriented = {tnorm(t) for t in itertools.permutations(range(F), 3)}
        orbits = {tuple(sorted({timg(g, t) for g in self.G})) for t in oriented}
        self.fixed = sorted(o[0] for o in orbits if len(o) == 1)
        self.fixed_supports = sorted({frozenset(t) for t in self.fixed}, key=sorted)
        self.rows = sorted(o for o in orbits if len(o) > 1 and len({frozenset(t) for t in o}) == len(o))
        self.bad_orbits = sorted(o for o in orbits if len(o) > 1 and len({frozenset(t) for t in o}) < len(o))
        self.row_key = [frozenset(frozenset(t) for t in o) for o in self.rows]
        dpairs = list(itertools.permutations(range(F), 2))
        self.columns = sorted({tuple(sorted({(g[a], g[b]) for g in self.G})) for a, b in dpairs})
        self.col = {pr: i for i, c in enumerate(self.columns) for pr in c}
        self.row_vec = [Counter(self.col[t[i], t[(i + 1) % 3]] for t in o for i in range(3)) for o in self.rows]
        self.pair_orbits = sorted({tuple(sorted({tuple(sorted((g[a], g[b]))) for g in self.G}))
                                   for a, b in itertools.combinations(range(F), 2)})
        self.porb = {pr: i for i, o in enumerate(self.pair_orbits) for pr in o}

    # ---- demands: excess e_O in 0..MAX_MULT-1 per pair orbit, sum e_O |O| = k, up to the normaliser
    def excess_vectors(self):
        sizes = [len(o) for o in self.pair_orbits]; out = []

        def rec(i, left, cur):
            if left == 0:
                out.append(tuple(cur + [0] * (len(sizes) - i))); return
            if i == len(sizes):
                return
            for e in range(MAX_MULT):
                if e * sizes[i] > left:
                    break
                rec(i + 1, left - e * sizes[i], cur + [e])
        rec(0, self.k, [])
        return out

    def demand_reps(self):
        N = normaliser(self.rho)
        perm = []
        for s in N:
            perm.append([self.porb[tuple(sorted((s[a], s[b])))] for a, b in (o[0] for o in self.pair_orbits)])
        # one pass per orbit: the first enumerated member is the representative, keyed by the orbit's least sorted
        # (orbit, excess) list
        reps = {}; seen = set()
        for e in self.excess_vectors():
            if e in seen:
                continue
            images = set()
            for P in perm:
                img = [0] * len(e)
                for i, x in enumerate(e):
                    img[P[i]] = x
                images.add(tuple(img))
            seen |= images
            reps[min(tuple((j, x) for j, x in enumerate(img) if x) for img in images)] = e
        return [reps[k] for k in sorted(reps)], len(N)

    def fixed_choices(self):
        """Lists of fixed oriented triangles: b distinct supports, any orientation, with (V - b) = 0 mod p."""
        by_support = [[t for t in self.fixed if frozenset(t) == s] for s in self.fixed_supports]
        out = []
        for b in range(len(by_support) + 1):
            if (self.V - b) % self.p:
                continue
            for sup in itertools.combinations(range(len(by_support)), b):
                for pick in itertools.product(*(by_support[i] for i in sup)):
                    out.append(list(pick))
        return out

    def mult(self, e):
        return {pr: 1 + e[self.porb[pr]] for pr in self.porb}

    # ---- exact cover of the directed-pair demands by rows (each row at most once, distinct supports)
    def covers(self, e, fixed, deadline, stats):
        m = self.mult(e)
        rem = [sum(m[tuple(sorted(pr))] for pr in c) for c in self.columns]
        for t in fixed:
            for i in range(3):
                rem[self.col[t[i], t[(i + 1) % 3]]] -= 1
        if min(rem) < 0:
            return
        need = self.V - len(fixed)
        nrow = len(self.rows)
        by_col = [[] for _ in self.columns]
        for i, vec in enumerate(self.row_vec):
            for c in vec:
                by_col[c].append(i)
        banned = [False] * nrow; used = Counter(); chosen = []
        fits = lambda i: (not banned[i] and not used[self.row_key[i]]
                          and all(rem[c] >= n for c, n in self.row_vec[i].items()))

        def rec():
            stats['nodes'] += 1
            if stats['nodes'] % 512 == 0 and time.monotonic() > deadline:
                raise TimeoutError
            best = None
            for c, r in enumerate(rem):
                if r > 0:
                    cand = [i for i in by_col[c] if fits(i)]
                    if not cand:
                        return
                    if best is None or len(cand) < len(best):
                        best = cand
            if best is None:
                assert sum(len(self.rows[i]) for i in chosen) == need
                yield list(chosen); return
            tried = []
            for i in best:
                for c, n in self.row_vec[i].items():
                    rem[c] -= n
                used[self.row_key[i]] += 1; chosen.append(i)
                yield from rec()
                chosen.pop(); used[self.row_key[i]] -= 1
                for c, n in self.row_vec[i].items():
                    rem[c] += n
                banned[i] = True; tried.append(i)
            for i in tried:
                banned[i] = False
        yield from rec()

    # ---- equivariant gluings of one triangle set
    def gluings(self, triangles, deadline, stats):
        index = {}
        for i, t in enumerate(triangles):
            for j in range(3):
                index[tnorm(t), t[j]] = 3 * i + j
        dact = [[index[timg(g, t), g[t[j]]] for t in triangles for j in range(3)] for g in self.G]
        pairs = {}
        for i, t in enumerate(triangles):
            for j in range(3):
                u, v = t[j], t[(j + 1) % 3]
                pairs.setdefault((min(u, v), max(u, v)), ([], []))[0 if u < v else 1].append(3 * i + j)
        reps = [o[0] for o in self.pair_orbits]
        choices = []
        for pr in reps:
            a, b = pairs[pr]
            assert len(a) == len(b) and 1 <= len(a) <= MAX_MULT
            choices.append([list(zip(a, q)) for q in itertools.permutations(b)])
        for sel in itertools.product(*choices):
            stats['gluings'] += 1
            if stats['gluings'] % 256 == 0 and time.monotonic() > deadline:
                raise TimeoutError
            alpha = {}; ok = True
            for matching in sel:
                for a, b in matching:
                    for g in dact:
                        x, y = g[a], g[b]
                        if x == y or alpha.get(x, y) != y or alpha.get(y, x) != x:
                            ok = False; break
                        alpha[x], alpha[y] = y, x
                    if not ok:
                        break
                if not ok:
                    break
            if ok:
                assert len(alpha) == 3 * len(triangles)
                yield alpha, dact[1]

    def maps(self, e, fixed, deadline, stats):
        """Yield (TriMap, dart action of rho) for every admissible rho-map with excess e and these fixed triangles."""
        for chosen in self.covers(e, fixed, deadline, stats):
            stats['covers'] += 1
            triangles = list(fixed) + [t for i in chosen for t in self.rows[i]]
            assert len(triangles) == self.V
            tri = [[3 * i, 3 * i + 1, 3 * i + 2] for i in range(len(triangles))]
            tail = [v for t in triangles for v in t]
            for alpha, act in self.gluings(triangles, deadline, stats):
                m = review.TriMap(tri, alpha, tail)
                if m.vertex_count() != self.F:
                    continue
                review.check(m, self.F, self.genus)
                assert census.admissible(m)
                yield m, act


def map_info(m, act, fixed):
    """Canonical code, the rho action on canonical darts, b (fixed triangles) and fixed edges."""
    code, _, _, _, (r0, m0) = m.canon()
    _, order = m.code(r0, m0)
    lab = {d: i for i, d in enumerate(order)}
    return dict(code=[list(x) for x in code], action=[lab[act[order[i]]] for i in range(len(order))],
                b=len(fixed), fixed_edges=sum(1 for d in m.pos if m.alpha[d] == act[d]) // 2)


def check_action(code, action, p, fixed_vertices):
    """Independent check on the canonical code alone: the action is a map automorphism of order p (it commutes with
    the triangle step and alpha) whose vertex permutation has exactly `fixed_vertices` fixed points."""
    step = [x for x, _ in code]; alpha = [a for _, a in code]; n = len(code)
    if any(action[step[d]] != step[action[d]] or action[alpha[d]] != alpha[action[d]] for d in range(n)):
        return False
    q = list(range(n)); k = 0
    while True:
        q = [action[d] for d in q]; k += 1
        if q == list(range(n)):
            break
    M = census.from_code([tuple(x) for x in code])
    cyc, which = M.vertices()
    fixed = sum(1 for c in cyc if which[action[c[0]]] == which[c[0]])
    return k == p and fixed == fixed_vertices


def burnside_classes(s):
    """Number of excess-vector classes by Burnside's lemma (a count independent of demand_reps): the mean over the
    normaliser of the vectors constant on the cycles of its action on the pair orbits."""
    sizes = [len(o) for o in s.pair_orbits]; N = normaliser(s.rho); total = 0
    for g in N:
        P = [s.porb[tuple(sorted((g[a], g[b])))] for a, b in (o[0] for o in s.pair_orbits)]
        seen = [False] * len(P); ways = Counter({0: 1})
        for i in range(len(P)):
            if seen[i]:
                continue
            L = 0; j = i
            while not seen[j]:
                seen[j] = True; j = P[j]; L += 1
            ways = sum((Counter({t + e * sizes[i] * L: w}) for t, w in ways.items() for e in range(MAX_MULT)
                        if t + e * sizes[i] * L <= s.k), Counter())
        total += ways[s.k]
    assert total % len(N) == 0
    return total // len(N)


# ----------------------------------------------------------------------------- units, shards, summary

def units(stage='A'):
    """Deterministic unit list of a stage: (config, demand index, fixed-choice index), C3 configs first."""
    out = []
    for name in STAGES[stage]:
        s = setup(name)
        out += [(name, di, fi) for di in range(len(s.reps)) for fi in range(len(s.fchoices))]
    return out


_SETUPS = {}


def setup(name):
    if name not in _SETUPS:
        F, g, rho, _ = CONFIGS[name]
        s = Setup(F, g, rho); s.reps, s.nnorm = s.demand_reps(); s.fchoices = s.fixed_choices()
        _SETUPS[name] = s
    return _SETUPS[name]


def run_unit(name, di, fi, deadline):
    s = setup(name); e = s.reps[di]; fixed = s.fchoices[fi]
    stats = Counter(); t0 = time.monotonic(); found = {}
    rec = dict(config=name, demand=di, fixed=fi, b=len(fixed),
               excess={'%d-%d' % s.pair_orbits[i][0]: x for i, x in enumerate(e) if x},
               mult_pattern=sorted((1 + x for x in e if x), reverse=True))
    try:
        for m, act in s.maps(e, fixed, deadline, stats):
            info = map_info(m, act, fixed)
            key = json.dumps(info['code'])
            stats['map_hits'] += 1
            found.setdefault(key, info)
        rec['complete'] = True
    except TimeoutError:
        rec['complete'] = False
    rec.update(nodes=stats['nodes'], covers=stats['covers'], gluings=stats['gluings'], map_hits=stats['map_hits'],
               seconds=round(time.monotonic() - t0, 3), maps=list(found.values()))
    return rec


def manifest():
    git = lambda *a: subprocess.check_output(['git', '-C', str(ROOT)] + list(a), text=True).strip()
    return dict(commit=git('rev-parse', 'HEAD'), dirty=git('status', '--porcelain'), python=sys.version,
                host=platform.platform(), started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                sources_sha256={str(p.relative_to(ROOT)): __import__('hashlib').sha256(p.read_bytes()).hexdigest()
                                for p in (Path(__file__).resolve(), CENSUS_DIR / 'census.py',
                                          ROOT / 'reviews/strategy-review-2026-11-03-flipwalk.py')})


def shard(sh, shards, out, seconds, stage='A'):
    """Claim units in order (O_EXCL claim files shared by all shards) until the deadline; one record per unit."""
    deadline = time.monotonic() + seconds
    out = Path(out); claims = out / 'claims'; claims.mkdir(parents=True, exist_ok=True)
    mine = out / str(sh); mine.mkdir(parents=True, exist_ok=True)
    (mine / ('manifest-%d.json' % int(time.time()))).write_text(json.dumps(dict(manifest(), shard=sh, shards=shards,
                                                                               seconds=seconds, stage=stage),
                                                                          indent=1) + '\n')
    for name, di, fi in units(stage):
        if time.monotonic() > deadline or (out / 'stop.requested').exists():
            break
        try:
            os.close(os.open(claims / ('%s_%d_%d' % (name, di, fi)), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        except FileExistsError:
            continue
        rec = run_unit(name, di, fi, deadline)
        rec['shard'] = sh
        with (mine / 'results.jsonl').open('a') as fh:
            fh.write(json.dumps(rec) + '\n')


def records(out):
    return [json.loads(l) for p in sorted(Path(out).glob('*/results.jsonl')) for l in p.read_text().splitlines() if l]


def census_truth():
    """Control lists from the E-261103-01 census (admissible classes with an automorphism of the family's type)."""
    load = lambda n, g: json.loads((CENSUS_DIR / 'results' / ('maps_%d_%d.json' % (n, g))).read_text())['maps']
    with_aut = lambda maps, order, fixed_v: sorted(json.dumps(m['code']) for m in maps if m['admissible']
                                                   and any(a[0] == order and a[1] == fixed_v for a in m['autos']))
    m93, m82, m71 = load(9, 3), load(8, 2), load(7, 1)
    c3x = json.loads((CENSUS_DIR / 'results/c3-crosscheck.json').read_text())['codes']
    return {'C3_9_3': with_aut(m93, 3, 0), 'C3_9_3_crosscheck': sorted(json.dumps(c) for c in c3x),
            'C2f_9_3': with_aut(m93, 2, 1), 'C2_8_2': with_aut(m82, 2, 0), 'C2f_7_1': with_aut(m71, 2, 1),
            'all_7_1': sorted(json.dumps(m['code']) for m in m71)}


def known_8_3_codes():
    """Canonical dual-map codes of Roest-Vigh's and Mizhaev's maps (flip-walk review conventions)."""
    sys.path.insert(0, str(ROOT / 'code'))
    import control_rost_vigh
    _, rv = control_rost_vigh.build()
    mz = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())['links_0based']
    mz = {int(k): v for k, v in mz.items()} if isinstance(mz, dict) else dict(enumerate(mz))
    out = {}
    for name, links in (('roest_vigh', rv), ('mizhaev', mz)):
        M = review.dual_map(review.coherent(links)); review.check(M, 8, 3)
        out[name] = json.dumps([list(x) for x in M.canon()[0]])
    return out


def summary(out, write=True, stage='A'):
    rows = records(out); U = units(stage); T = TARGETS[stage]
    rep = {}
    for name in STAGES[stage]:
        F, g, rho, role = CONFIGS[name]
        rs = [r for r in rows if r['config'] == name]
        planned = sum(1 for u in U if u[0] == name)
        codes = {}
        for r in rs:
            for mp in r['maps']:
                k = json.dumps(mp['code'])
                c = codes.setdefault(k, dict(b=set(), fixed_edges=set(), actions=set(), strata=set()))
                c['b'].add(mp['b']); c['fixed_edges'].add(mp['fixed_edges']); c['actions'].add(tuple(mp['action']))
                c['strata'].add('b%d m%s' % (r['b'], ''.join(map(str, r['mult_pattern']))))
                c.setdefault('action_ok', True)
                c['action_ok'] &= check_action(mp['code'], mp['action'], len(setup(name).G), sum(
                    1 for v in range(F) if rho[v] == v))
        strata = {}
        for r in rs:
            st = strata.setdefault('b%d m%s' % (r['b'], ''.join(map(str, r['mult_pattern']))), Counter())
            for k in ('covers', 'gluings', 'map_hits', 'nodes', 'seconds'):
                st[k] += r[k]
            st['units'] += 1; st['complete'] += r['complete']
        for st in strata.values():
            st['seconds'] = round(st['seconds'], 2)
        s = setup(name)
        rep[name] = dict(role=role, family=FAMILY[name], F=F, genus=g, units_planned=planned, units_recorded=len(rs),
                         complete=len(rs) == planned and all(r['complete'] for r in rs),
                         demand_classes=len(s.reps), normaliser=s.nnorm, fixed_choices=len(s.fchoices),
                         rows=len(s.rows), columns=len(s.columns), classes=len(codes),
                         seconds=round(sum(r['seconds'] for r in rs), 2), strata={k: dict(v) for k, v in strata.items()},
                         codes=sorted(codes),
                         per_map=[dict(code=k, b=sorted(v['b']), fixed_edges=sorted(v['fixed_edges']),
                                       actions=len(v['actions']), strata=sorted(v['strata']), action_ok=v['action_ok'])
                                  for k, v in sorted(codes.items())])
    truth = census_truth(); c = {}
    got = lambda n: rep[n]['codes'] if rep[n]['complete'] else None
    if stage == 'A':
        c['C3_demand_classes_18'] = rep['C3_9_4']['demand_classes'] == 18
    else:
        for fam, name in T.items():
            c[fam + '_demand_classes_burnside'] = rep[name]['demand_classes'] == burnside_classes(setup(name))
    if 'C3' in T:
        c['C3_9_3_equals_census'] = (got('C3_9_3') == truth['C3_9_3'] == truth['C3_9_3_crosscheck']
                                     and len(truth['C3_9_3']) == 8)
    if 'C2' in T:
        k83 = known_8_3_codes()
        c['C2f_9_3_equals_census'] = got('C2f_9_3') == truth['C2f_9_3']
        c['C2_8_2_equals_census'] = got('C2_8_2') == truth['C2_8_2']
        c['C2f_7_1_is_szilassi'] = got('C2f_7_1') == truth['C2f_7_1'] == truth['all_7_1']
        c['C2_8_3_holds_both_known'] = rep['C2_8_3']['complete'] and set(k83.values()) <= set(rep['C2_8_3']['codes'])
    for fam in T:
        c['actions_ok_' + fam] = all(p['action_ok'] for r in rep.values() if r['family'] == fam for p in r['per_map'])
    fam_controls = dict(C3=('C3_9_3_equals_census',), C2=('C2f_9_3_equals_census', 'C2_8_2_equals_census',
                                                          'C2f_7_1_is_szilassi', 'C2_8_3_holds_both_known'))
    gate = {fam: all(c[k] for k in fam_controls[fam] + ('actions_ok_' + fam,)) and rep[name]['complete']
            and all(v for k, v in c.items() if k.startswith(fam + '_demand_classes')) for fam, name in T.items()}
    res = dict(stage=stage, controls=c, gate=gate, truth_sizes={k: len(v) for k, v in truth.items()}, configs=rep,
               core_seconds=round(sum(r['seconds'] for r in rows), 1))
    if write:
        (Path(out) / 'summary.json').write_text(json.dumps(res, indent=1) + '\n')
    brief = {k: v for k, v in res.items() if k != 'configs'}
    brief['configs'] = {n: {k: v for k, v in r.items() if k not in ('codes', 'per_map')} for n, r in rep.items()}
    print(json.dumps(brief, indent=1))
    return res


if __name__ == '__main__':
    mode, *rest = sys.argv[1:]
    if mode == 'shard':
        shard(int(rest[0]), int(rest[1]), rest[2], float(rest[3]), *rest[4:])
    elif mode == 'summary':
        summary(rest[0], stage=(rest[1:] or ['A'])[0])
    elif mode == 'units':
        print(Counter(u[0] for u in units(*rest)))
    else:
        raise SystemExit(__doc__)
