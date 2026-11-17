"""P3 v2 (E-261116-07): one census-free CP-SAT formula per (F, E) for a uniform cubic S1 solid.

Elements: faces 0..F-1 and INF = F (omsat convention: chi(a,b,c,d) = sign det(h_a, h_b, h_c, h_d), sorted
4-subsets are the variables, INF last). sigma_m(t) = chi(t, m) chi(t, INF) is the side of plane m at the vertex
P_t (omsat `side`). A cell is a sign vector T in {+,-}^F, stored as a bitmask (bit m set iff T_m = +).

Blocks (review dialogue-2026-11-16-strategy, Appendix A1):
  chirotope   210 signs at F = 9 with the three-term Grassmann-Pluecker relations (omsat CNF.gp clauses)
  validity    tau_T <-> OR over finite vertices t of [sigma(t) = T off t]; x_T -> tau_T
  unbounded   for each pair (j, k) and direction e: the four T with T_m = e chi(j, k, m, INF) off {j, k} get x_T = 0
  gauge       sigma_m(0,1,2) = + for m >= 3 and sigma_m(3,4,5) = + for m <= 2 (plane reorientation only)
  facets      b(i, U) <-> tau(U, i+) and tau(U, i-) and x(U, i+) xor x(U, i-)
  segments    segment V of line L_ij is real iff its four cells are valid
  vertices    solid_cpsat.ALLOWED on the eight octant bits, no-pinch per plane, no-diagonal per half-line
  ends        an end of L_ij at t is an edge on exactly one of its two half-lines; sum of ends = 2E; a pair is
              adjacent iff its line has an end
  disk        per plane: facets - segments touching a boundary facet + vertices touching one = 1, and eager
              connectivity (one root, every other boundary facet has a boundary neighbour of smaller level)
Usage: p3.py controls OUT | p3.py shard SHARD SHARDS OUT | p3.py summary RESULTS
"""
import argparse
import hashlib
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
sys.path.insert(0, str(ROOT / 'code'))
from ortools.sat.python import cp_model  # noqa: E402
from omsat import perm_parity, chirotope_from_planes  # noqa: E402
from solid_cpsat import ALLOWED  # noqa: E402

ALLOWED_SET = {sum(b << q for q, b in enumerate(occ)) for occ in ALLOWED}


def chi_of(chi, t):
    """Sign of an ordered tuple from a dict sorted 4-subset -> +-1."""
    return chi[tuple(sorted(t))] * (-1 if perm_parity(t) else 1)


def sigma(chi, F, t, m):
    return chi_of(chi, tuple(t) + (m,)) * chi_of(chi, tuple(t) + (F,))


def octant_cell(F, t, U_bits, others, q):
    """Cell bitmask from the label U on `others` (bit r of U_bits = sign of others[r]) and octant q on t."""
    T = 0
    for r, m in enumerate(others):
        if U_bits >> r & 1:
            T |= 1 << m
    for r, m in enumerate(t):
        if q >> r & 1:
            T |= 1 << m
    return T


def pattern_ends(occ):
    """Ends of the three lines through a vertex for an 8-bit octant pattern (bit q = occupancy of octant q)."""
    ends = []
    for r in range(3):
        edge = []
        for s in (0, 1):
            par = 0
            for q in range(8):
                if (q >> r & 1) == s:
                    par ^= occ >> q & 1
            edge.append(par)
        ends.append(edge[0] ^ edge[1])
    return ends


def pattern_ok(occ):
    """ALLOWED, no-pinch on each of the three planes, no-diagonal on each of the six half-lines."""
    if occ not in ALLOWED_SET:
        return False
    bit = lambda q: occ >> q & 1
    for r in range(3):
        a, b = [x for x in range(3) if x != r]
        # quadrant facets of plane r: boundary iff the octants on its two sides differ
        qb = {}
        for sa, sb in itertools.product((0, 1), repeat=2):
            q0 = (sa << a) | (sb << b)
            qb[sa, sb] = bit(q0) ^ bit(q0 | 1 << r)
        if qb[1, 1] and qb[0, 0] and not qb[1, 0] and not qb[0, 1]:
            return False
        if qb[1, 0] and qb[0, 1] and not qb[1, 1] and not qb[0, 0]:
            return False
        # half-lines of the line where planes a, b meet, on side s of plane r
        for s in (0, 1):
            c = {(sa, sb): bit((s << r) | (sa << a) | (sb << b)) for sa, sb in itertools.product((0, 1), repeat=2)}
            if c[1, 1] and c[0, 0] and not c[1, 0] and not c[0, 1]:
                return False
            if c[1, 0] and c[0, 1] and not c[1, 1] and not c[0, 0]:
                return False
    return True


class Formula:
    """The P3 v2 CP-SAT model for F faces.

    edges: E (sum of end bits = 2E) or None; all_pairs: every pair has an end; gauge: the reorientation gauge;
    chi: dict sorted quad -> +-1 to pin (a zero raises ValueError: out of domain); disk_planes: planes with the
    Euler condition (default all); connect: eager connectivity on the disk planes; cube: [(quad, sign)] fixed."""

    def __init__(self, F, edges=None, all_pairs=True, gauge=True, chi=None, disk_planes=None, connect=True, cube=()):
        self.F = F; INF = F
        m = self.model = cp_model.CpModel()
        self.quads = list(itertools.combinations(range(F + 1), 4))
        self.p = {S: m.NewBoolVar('p%s' % '_'.join(map(str, S))) for S in self.quads}
        if chi is not None:
            if any(chi[S] not in (1, -1) for S in self.quads):
                raise ValueError('non-uniform chirotope: out of domain')
            for S in self.quads:
                m.Add(self.p[S] == (1 if chi[S] > 0 else 0))
        for S, s in cube:
            m.Add(self.p[tuple(S)] == (1 if s > 0 else 0))
        self._gp()
        self.triples = list(itertools.combinations(range(F), 3))
        # sigma bits and vertex labels
        self.s = {}
        for t in self.triples:
            for k in range(F):
                if k not in t:
                    b = m.NewBoolVar('s%s_%d' % (t, k))
                    m.AddBoolXOr([self.pos(t + (k,)), self.pos(t + (INF,)), b])   # b = (A == B)
                    self.s[t, k] = b
        if gauge:
            assert F >= 6
            for k in range(3, F):
                m.Add(self.s[(0, 1, 2), k] == 1)
            for k in range(3):
                m.Add(self.s[(3, 4, 5), k] == 1)
        self.eq = {}
        for t in self.triples:
            others = [k for k in range(F) if k not in t]
            row = []
            for U in range(1 << len(others)):
                e = m.NewBoolVar('eq%s_%d' % (t, U))
                lits = [self.s[t, k] if U >> r & 1 else self.s[t, k].Not() for r, k in enumerate(others)]
                for lit in lits:
                    m.AddImplication(e, lit)
                m.AddBoolOr([e] + [lit.Not() for lit in lits])
                self.eq[t, U] = e; row.append(e)
            m.AddExactlyOne(row)
        # cells, validity
        nT = 1 << F
        self.x = [m.NewBoolVar('x%d' % T) for T in range(nT)]
        self.tau = [m.NewBoolVar('tau%d' % T) for T in range(nT)]
        support = [[] for _ in range(nT)]
        for t in self.triples:
            others = [k for k in range(F) if k not in t]
            for U in range(1 << len(others)):
                for q in range(8):
                    support[octant_cell(F, t, U, others, q)].append(self.eq[t, U])
        for T in range(nT):
            for e in support[T]:
                m.AddImplication(e, self.tau[T])
            m.AddBoolOr(support[T]).OnlyEnforceIf(self.tau[T])
            m.AddImplication(self.x[T], self.tau[T])
        # unbounded cells: both directions of every line at infinity
        for j, k in itertools.combinations(range(F), 2):
            others = [i for i in range(F) if i not in (j, k)]
            dirs = [self.pos((j, k, i, INF)) for i in others]
            for V in range(1 << len(others)):
                match = [d if V >> r & 1 else d.Not() for r, d in enumerate(dirs)]
                for e in (1, -1):
                    lits = match if e > 0 else [d.Not() if V >> r & 1 else d for r, d in enumerate(dirs)]
                    for sj, sk in itertools.product((0, 1), repeat=2):
                        T = sum(1 << i for r, i in enumerate(others) if V >> r & 1) | sj << j | sk << k
                        m.AddBoolOr([lit.Not() for lit in lits] + [self.x[T].Not()])
        # vertices: octant occupancy multiplexed by the vertex label
        self.occ = {}
        for t in self.triples:
            others = [k for k in range(F) if k not in t]
            for q in range(8):
                self.occ[t, q] = m.NewBoolVar('o%s_%d' % (t, q))
            for U in range(1 << len(others)):
                e = self.eq[t, U]
                for q in range(8):
                    xv = self.x[octant_cell(F, t, U, others, q)]
                    m.AddBoolOr([e.Not(), self.occ[t, q].Not(), xv])
                    m.AddBoolOr([e.Not(), self.occ[t, q], xv.Not()])
            m.AddAllowedAssignments([self.occ[t, q] for q in range(8)], ALLOWED)
        self.qb = {}      # (t, r, sa, sb): quadrant facet of plane t[r] at t is boundary
        self.end = {}     # (t, r): end of the line t minus t[r] at t
        for t in self.triples:
            o = lambda q: self.occ[t, q]
            for r in range(3):
                a, b = [x for x in range(3) if x != r]
                for sa, sb in itertools.product((0, 1), repeat=2):
                    q0 = (sa << a) | (sb << b)
                    v = m.NewBoolVar('qb%s_%d_%d%d' % (t, r, sa, sb))
                    m.AddBoolXOr([o(q0), o(q0 | 1 << r), v.Not()])
                    self.qb[t, r, sa, sb] = v
                q = self.qb
                m.AddBoolOr([q[t, r, 1, 1].Not(), q[t, r, 0, 0].Not(), q[t, r, 1, 0], q[t, r, 0, 1]])
                m.AddBoolOr([q[t, r, 1, 0].Not(), q[t, r, 0, 1].Not(), q[t, r, 1, 1], q[t, r, 0, 0]])
                edge = []
                for s in (0, 1):
                    c = {(sa, sb): o((s << r) | (sa << a) | (sb << b)) for sa, sb in itertools.product((0, 1), repeat=2)}
                    m.AddBoolOr([c[1, 1].Not(), c[0, 0].Not(), c[1, 0], c[0, 1]])
                    m.AddBoolOr([c[1, 0].Not(), c[0, 1].Not(), c[1, 1], c[0, 0]])
                    ed = m.NewBoolVar('ed%s_%d_%d' % (t, r, s))
                    m.AddBoolXOr(list(c.values()) + [ed.Not()])
                    edge.append(ed)
                en = m.NewBoolVar('end%s_%d' % (t, r))
                m.AddBoolXOr(edge + [en.Not()])
                self.end[t, r] = en
        if edges is not None:
            m.Add(sum(self.end.values()) == 2 * edges)
        if all_pairs:
            for j, k in itertools.combinations(range(F), 2):
                ends = [self.end[t, t.index(i)] for i in range(F) if i not in (j, k)
                        for t in [tuple(sorted((j, k, i)))]]
                m.AddBoolOr(ends)
        m.AddBoolOr(self.x)
        # facets, segments, disks
        self.b = {}
        for i in range(F):
            for T in range(nT):
                if not T >> i & 1:
                    Tp = T | 1 << i
                    f = m.NewBoolVar('f%d_%d' % (i, T))
                    m.AddBoolXOr([self.x[T], self.x[Tp], f.Not()])
                    bb = m.NewBoolVar('b%d_%d' % (i, T))
                    m.AddBoolAnd([f, self.tau[T], self.tau[Tp]]).OnlyEnforceIf(bb)
                    m.AddBoolOr([f.Not(), self.tau[T].Not(), self.tau[Tp].Not(), bb])
                    self.b[i, T] = bb      # keyed by the cell with T_i = -
        self.euler = {}
        disk_planes = range(F) if disk_planes is None else disk_planes
        touch = {i: [] for i in range(F)}
        for i, j in itertools.combinations(range(F), 2):
            for T in range(nT):
                if T >> i & 1 or T >> j & 1:
                    continue
                cells = [T, T | 1 << i, T | 1 << j, T | 1 << i | 1 << j]
                real = m.NewBoolVar('seg%d_%d_%d' % (i, j, T))
                m.AddBoolAnd([self.tau[c] for c in cells]).OnlyEnforceIf(real)
                m.AddBoolOr([self.tau[c].Not() for c in cells] + [real])
                for X, Y in ((i, j), (j, i)):
                    fs = [self.b[X, T], self.b[X, T | 1 << Y]]
                    tv = m.NewBoolVar('touch%d_%d_%d' % (X, Y, T))
                    m.AddBoolAnd([real]).OnlyEnforceIf(tv)
                    m.AddBoolOr(fs).OnlyEnforceIf(tv)
                    m.AddBoolOr([real.Not(), tv]).OnlyEnforceIf(fs[0])
                    m.AddBoolOr([real.Not(), tv]).OnlyEnforceIf(fs[1])
                    touch[X].append(tv)
        vtouch = {i: [] for i in range(F)}
        for t in self.triples:
            for r, i in enumerate(t):
                qs = [self.qb[t, r, sa, sb] for sa, sb in itertools.product((0, 1), repeat=2)]
                v = m.NewBoolVar('vt%s_%d' % (t, r))
                m.AddMaxEquality(v, qs)
                vtouch[i].append(v)
        for i in range(F):
            fac = [self.b[i, T] for T in range(nT) if not T >> i & 1]
            ev = m.NewIntVar(-len(touch[i]), len(fac) + len(vtouch[i]), 'euler%d' % i)
            m.Add(ev == sum(fac) - sum(touch[i]) + sum(vtouch[i]))
            self.euler[i] = ev
            if i in disk_planes:
                m.Add(ev == 1)
                if connect:
                    self._connect(i)

    def pos(self, t):
        """Literal [chi(t) = +] of an ordered tuple."""
        v = self.p[tuple(sorted(t))]
        return v.Not() if perm_parity(t) else v

    def _gp(self):
        els = range(self.F + 1)
        for a, b in itertools.combinations(els, 2):
            rest = [e for e in els if e not in (a, b)]
            for c, d, e, f in itertools.combinations(rest, 4):
                pairs = [((a, b, c, d), (a, b, e, f), 0), ((a, b, c, e), (a, b, d, f), 1), ((a, b, c, f), (a, b, d, e), 0)]
                L = [(self.pos(p).Not(), self.pos(q).Not(), k) for p, q, k in pairs]   # negative bits
                for target in (0, 1):
                    for bits in itertools.product((0, 1), repeat=3):
                        cl = []
                        for (lp, lq, k), bp in zip(L, bits):
                            bq = bp ^ k ^ target
                            cl.append(lp.Not() if bp else lp)
                            cl.append(lq.Not() if bq else lq)
                        self.model.AddBoolOr(cl)

    def _connect(self, i):
        m = self.model; F = self.F
        labels = [T for T in range(1 << F) if not T >> i & 1]
        roots = []
        level = {T: m.NewIntVar(0, len(labels) - 1, 'lv%d_%d' % (i, T)) for T in labels}
        for T in labels:
            r = m.NewBoolVar('root%d_%d' % (i, T)); roots.append(r)
            m.AddImplication(r, self.b[i, T])
            ws = []
            for j in range(F):
                if j == i:
                    continue
                g = T ^ 1 << j
                w = m.NewBoolVar('w%d_%d_%d' % (i, T, j))
                m.AddImplication(w, self.b[i, g])
                m.Add(level[g] < level[T]).OnlyEnforceIf(w)
                ws.append(w)
            m.AddBoolOr([self.b[i, T].Not(), r] + ws)
        m.AddExactlyOne(roots)

    def block(self, chi):
        self.model.AddBoolOr([self.p[S].Not() if chi[S] > 0 else self.p[S] for S in self.quads])

    def solve(self, seconds, seed=0, workers=1):
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = seconds
        solver.parameters.num_workers = workers
        solver.parameters.random_seed = seed
        t0 = time.monotonic()
        st = solver.Solve(self.model)
        out = dict(status=solver.StatusName(st), seconds=round(time.monotonic() - t0, 3))
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            out['chi'] = {S: 1 if solver.Value(self.p[S]) else -1 for S in self.quads}
            out['cells'] = [T for T in range(1 << self.F) if solver.Value(self.x[T])]
            out['euler'] = {i: solver.Value(v) for i, v in self.euler.items()}
        return out


def gp_ok(chi, n_el):
    """Three-term Grassmann-Pluecker check of a uniform chirotope on n_el elements (independent of the CP model)."""
    for a, b in itertools.combinations(range(n_el), 2):
        rest = [e for e in range(n_el) if e not in (a, b)]
        for c, d, e, f in itertools.combinations(rest, 4):
            t1 = chi_of(chi, (a, b, c, d)) * chi_of(chi, (a, b, e, f))
            t2 = -chi_of(chi, (a, b, c, e)) * chi_of(chi, (a, b, d, f))
            t3 = chi_of(chi, (a, b, c, f)) * chi_of(chi, (a, b, d, e))
            if t1 == t2 == t3:
                return False
    return True


def decode(chi, cells, F):
    """Pure-Python reading of a model: vertex patterns, ends, runs and face cycles, from chi and the cell set.

    Returns dict(links, V, E, ends, ok, reason). Independent of the CP-SAT encoding except for the conventions."""
    S = set(cells)
    INF = F
    out = dict(ok=False)
    pats = {}; ends = {}
    for t in itertools.combinations(range(F), 3):
        others = [k for k in range(F) if k not in t]
        U = sum(1 << r for r, k in enumerate(others) if sigma(chi, F, t, k) > 0)
        occ = sum((octant_cell(F, t, U, others, q) in S) << q for q in range(8))
        if not pattern_ok(occ):
            out['reason'] = 'vertex pattern %s at %s' % (bin(occ), t); return out
        pats[t] = occ
        e = pattern_ends(occ)
        if sum(e) not in (0, 3):
            out['reason'] = 'vertex with %d ends' % sum(e); return out
        ends[t] = e
    nV = sum(1 for t in ends if sum(ends[t]) == 3)
    # runs along each line, ordered by the chirotope
    runs = []
    for j, k in itertools.combinations(range(F), 2):
        pts = [i for i in range(F) if i not in (j, k)]
        tri = {i: tuple(sorted((j, k, i))) for i in pts}
        rank = {}
        for q in pts:
            # q lies after p along d = n_j x n_k iff plane p has at P_q the sign it takes along d
            rank[q] = sum(1 for p in pts if p != q and sigma(chi, F, tri[q], p) == chi_of(chi, (j, k, p, INF)))
        if sorted(rank.values()) != list(range(len(pts))):
            out['reason'] = 'no linear order on line %s' % ((j, k),); return out
        order = sorted(pts, key=rank.get)
        seg_edges = []
        for p, q in zip(order, order[1:]):
            V = 0
            for i in pts:
                s = sigma(chi, F, tri[p], i) if i != p else sigma(chi, F, tri[q], p)
                if s > 0:
                    V |= 1 << i
            par = sum((V | sj << j | sk << k) in S for sj, sk in itertools.product((0, 1), repeat=2)) % 2
            seg_edges.append(par)
        start = None
        for idx in range(len(seg_edges) + 1):
            on = idx < len(seg_edges) and seg_edges[idx]
            if on and start is None:
                start = idx
            if not on and start is not None:
                runs.append((j, k, tri[order[start]], tri[order[idx]]))
                start = None
    for j, k, u, v in runs:
        for t in (u, v):
            r = [x for x in range(3) if t[x] not in (j, k)][0]
            if not ends[t][r]:
                out['reason'] = 'run end without an end bit'; return out
    nE = len(runs)
    if 2 * nE != sum(sum(e) for e in ends.values()):
        out['reason'] = 'ends do not pair into runs'; return out
    links = {}
    for face in range(F):
        graph = {}
        for x, y, u, v in runs:
            if face in (x, y):
                other = y if face == x else x
                graph.setdefault(u, []).append((v, other)); graph.setdefault(v, []).append((u, other))
        if not graph or any(len(es) != 2 for es in graph.values()):
            out['reason'] = 'face %d boundary is not a cubic cycle' % face; return out
        first = min(graph); current = first; previous = None; cycle = []; seen = set()
        while current not in seen:
            seen.add(current)
            options = [e for e in graph[current] if e[0] != previous]
            following, other = min(options)
            cycle.append(other); previous, current = current, following
        if current != first or seen != set(graph):
            out['reason'] = 'face %d has several boundary cycles' % face; return out
        links[face] = cycle
    out.update(ok=True, links=links, V=nV, E=nE, reason='')
    return out


# ----------------------------------------------------------------------------- runner

def dump(path, value):
    path.write_text(json.dumps(value, indent=1, default=str) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def chi_json(chi):
    return {','.join(map(str, S)): v for S, v in chi.items()}


K13 = ROOT / 'reviews/dialogue-2026-11-16-strategy-checks/d2_rate.json'
K13_SHA = 'b7b5ff8438acf7ea1e7526c936604abd3407013f67ebb1cab6b797e0f7f8aafa'
SZ = ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/results/pilot/szilassi.input.json'


def load(folder, name):
    import importlib.util
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, ROOT / 'experiments' / folder / 'pilot.py')
        mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return sys.modules[name]


def manifest_base():
    git = lambda *a: subprocess.check_output(['git', '-C', str(ROOT)] + list(a), text=True).strip()
    return dict(commit=git('rev-parse', 'HEAD'), branch=git('branch', '--show-current'),
                dirty=git('status', '--porcelain'), python=sys.version, host=platform.platform(),
                ortools=__import__('ortools').__version__, started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))


def pinned_unit(args):
    """One pinned solve: (name, planes, F, E, cap, expected) -> record."""
    name, planes, E, cap = args
    from ladder_exact import verify
    F = len(planes)
    rec = dict(name=name, F=F, E=E)
    try:
        chi = chirotope_from_planes(planes)
        f = Formula(F, edges=E, chi=chi, gauge=False)
    except ValueError as exc:
        rec.update(status='OUT-OF-DOMAIN', error=str(exc)); return rec
    r = f.solve(cap)
    rec.update(status=r['status'], seconds=r['seconds'])
    if 'cells' in r:
        d = decode(r['chi'], r['cells'], F)
        rec.update(decode_ok=d['ok'], decode_reason=d['reason'])
        if d['ok']:
            g = verify(planes, d['links'], require_all_pairs=True)
            rec.update(links=d['links'], EMBEDDED=bool(g.get('EMBEDDED')), V_E_F_chi=list(g['V_E_F_chi']))
    return rec


def controls(out):
    import multiprocessing as mp
    out.mkdir(parents=True, exist_ok=False)
    man = manifest_base(); t0 = time.monotonic()
    report = dict(PASS=False, checks={})
    assert sha(K13) == K13_SHA, 'K13 archive hash changed'
    k13 = json.loads(K13.read_text())['rows']
    sz = json.loads(SZ.read_text())
    p05 = load('E-261103-05-s5-symmetric-solid-first', 'pilot05')
    fx = {name: (h, links) for name, h, links in p05.fixtures()}
    units = [('k13_%d' % r['seed'], r['planes'], 36, 60) for r in k13]
    units += [('roest_vigh', fx['roest_vigh'][0], 36, 120), ('mizhaev', fx['mizhaev'][0], 36, 120),
              ('szilassi_perturbed', sz['planes'], 21, 120), ('szilassi_raw', sz['raw_planes'], 21, 60),
              ('negative_tetra_e7', [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-1, -1, -1, 1]], 7, 60)]
    with mp.Pool(int(os.environ.get('WORKERS', '8'))) as pool:
        rows = pool.map(pinned_unit, units, chunksize=1)
    dump(out / 'L0_rows.json', rows)
    by = {r['name']: r for r in rows}
    k13_match = []
    for r in k13:
        mine = by['k13_%d' % r['seed']]
        want = 'OPTIMAL' if r['status'] == 'OPTIMAL' else 'INFEASIBLE'
        got = mine['status']
        ok = got == want and (want == 'INFEASIBLE' or (mine.get('EMBEDDED') and mine.get('V_E_F_chi') == [24, 36, 8, -4]))
        k13_match.append(ok)
    report['checks']['L0_k13'] = dict(units=len(k13), matched=sum(k13_match),
                                      mismatched=[k13[i]['seed'] for i, ok in enumerate(k13_match) if not ok])
    good = lambda n, vefc: by[n]['status'] == 'OPTIMAL' and by[n].get('EMBEDDED') and by[n].get('V_E_F_chi') == vefc
    report['checks']['L0_roest_vigh'] = bool(good('roest_vigh', [24, 36, 8, -4]))
    report['checks']['L0_mizhaev'] = bool(good('mizhaev', [24, 36, 8, -4]))
    report['checks']['L0_szilassi_perturbed'] = bool(good('szilassi_perturbed', [14, 21, 7, 0]))
    report['checks']['L0_szilassi_raw_rejected'] = by['szilassi_raw']['status'] == 'OUT-OF-DOMAIN'
    report['checks']['neg_tetra_e7'] = by['negative_tetra_e7']['status'] == 'INFEASIBLE'
    # negative: Roest-Vigh's chirotope with one sign flipped must violate GP and be INFEASIBLE
    chi = chirotope_from_planes(fx['roest_vigh'][0])
    flip = next(S for S in sorted(chi) if not gp_ok({**chi, S: -chi[S]}, 9))
    r = Formula(8, edges=36, chi={**chi, flip: -chi[flip]}, gauge=False).solve(60)
    report['checks']['neg_rv_flipped_sign'] = dict(quad=flip, status=r['status'], PASS=r['status'] == 'INFEASIBLE')
    # stage-B reachability: each known (8, 3) chirotope, reoriented into the gauge and mirror-normalised, satisfies
    # the stage-B formula of its cube
    for name in ('roest_vigh', 'mizhaev'):
        h, c = gauged(fx[name][0])
        g = chirotope_from_planes(h)
        r = Formula(8, edges=36, chi=g, cube=cube(8, c)).solve(120)
        d = decode(r['chi'], r['cells'], 8) if 'cells' in r else dict(ok=False)
        from ladder_exact import verify
        emb = bool(d['ok'] and verify(h, d['links'], require_all_pairs=True).get('EMBEDDED'))
        report['checks']['gauge_' + name] = dict(cube=c, status=r['status'], EMBEDDED=emb, PASS=r['status'] == 'OPTIMAL' and emb)
    # L1: (7, 21) free, gauge
    f = Formula(7, edges=21)
    r = f.solve(float(os.environ.get('L1_CAP', '1200')), seed=0)
    l1 = dict(status=r['status'], seconds=r['seconds'])
    if 'cells' in r:
        d = decode(r['chi'], r['cells'], 7)
        l1.update(gp_ok=gp_ok(r['chi'], 8), decode_ok=d['ok'], decode_reason=d['reason'], links=d.get('links'),
                  chi=chi_json(r['chi']), cells=r['cells'])
        l1['szilassi_map'] = bool(d['ok'] and all(sorted(v) == [k for k in range(7) if k != i] for i, v in d['links'].items()))
        dump(out / 'L1_model.json', l1)
        l1['bridge'] = bridge(out, 'L1', r['chi'], d['links']) if d['ok'] else None
    report['checks']['L1'] = {k: v for k, v in l1.items() if k not in ('chi', 'cells')}
    c = report['checks']
    report['PASS'] = bool(c['L0_k13']['matched'] == len(k13) and c['L0_roest_vigh'] and c['L0_mizhaev']
                          and c['L0_szilassi_perturbed'] and c['L0_szilassi_raw_rejected'] and c['neg_tetra_e7']
                          and c['neg_rv_flipped_sign']['PASS'] and c['gauge_roest_vigh']['PASS']
                          and c['gauge_mizhaev']['PASS'] and l1['status'] == 'OPTIMAL' and l1.get('gp_ok')
                          and l1.get('szilassi_map'))
    dump(out / 'controls.json', report)
    man.update(wall_seconds=round(time.monotonic() - t0, 1), outputs_sha256={p.name: sha(p) for p in out.iterdir()},
               sources_sha256={str(p.relative_to(ROOT)): sha(p) for p in (Path(__file__).resolve(), K13, SZ)})
    dump(out / 'manifest.json', man)
    print(json.dumps(report, indent=1, default=str))


def bridge(out, name, chi, links, budget=(90, 90, 60), seed=26110303):
    """The frozen bridge of E-261103-03 (hinge, two_stage, fp), then the saved-file --all-pairs check."""
    p03 = load('E-261103-03-s5-exact-decision-8-2-9-3', 'pilot03')
    n = len(links)
    processing = {}
    for task, cap in zip(('hinge', 'two_stage', 'fp'), budget):
        res = processing[task] = p03.stage(out, '%s_%s' % (name, task), task,
                                           p03.payload(chi, [links[i] for i in range(n)], restarts=6,
                                                       optimizer_seed=seed), cap)
        res.pop('chi', None)
        if res.get('geometry', {}).get('EMBEDDED'):
            cand = out / (name + '.candidate.json')
            dump(cand, dict(planes=res['planes'], links={str(k): v for k, v in links.items()}))
            log = out / (name + '.candidate.log')
            with log.open('w') as stream:
                rc = subprocess.call([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(cand),
                                      '--all-pairs'], stdout=stream, stderr=subprocess.STDOUT, timeout=120)
            return dict(processing=processing, candidate=cand.name, all_pairs_rc=rc,
                        status_note='REALIZED-ALL-PAIRS-PASS' if rc == 0 else 'EMBEDDED-BUT-CHECK-FAIL')
        if res.get('independent_check'):
            return dict(processing=processing, status_note='NON-REALIZABLE-CERTIFIED')
    return dict(processing=processing, status_note='MODEL-NOT-REALIZED')


# stage B units: L2 cubes, then L3 cubes. MIRROR is fixed + (a reflection negates every sign and keeps the gauge);
# the four cube bits are outside the gauge.
MIRROR = (0, 3, 6)
CUBE_QUADS = [(1, 4, 6), (2, 5, 7), (0, 4, 7), (1, 5, 7)]
L2_CAP = {30: 225, 39: 450}            # seconds per cube: 16 x 225 s = 1 core-h, 16 x 450 s = 2 core-h
L3_CAP = 560                           # seconds per cube for solve + bridge: 16 x 560 s < 2.5 core-h
L3_MODELS = [2] * 14 + [1] * 2         # at most 30 distinct signed chirotopes


def cube(F, c):
    return [(MIRROR + (F,), 1)] + [(q + (F,), 1 if c >> r & 1 else -1) for r, q in enumerate(CUBE_QUADS)]


def gauged(planes):
    """Reorient planes into the gauge, mirror (x -> -x) if the MIRROR sign is -, and return (planes, cube index)."""
    h = [list(map(int, row)) for row in planes]; F = len(h)
    for t, ms in (((0, 1, 2), range(3, F)), ((3, 4, 5), range(3))):
        chi = chirotope_from_planes(h)
        for m in ms:
            if sigma(chi, F, t, m) < 0:
                h[m] = [-v for v in h[m]]
    chi = chirotope_from_planes(h)
    if chi[MIRROR + (F,)] < 0:
        h = [[-row[0]] + row[1:] for row in h]
        chi = chirotope_from_planes(h)
    assert chi[MIRROR + (F,)] > 0
    return h, sum(1 << r for r, q in enumerate(CUBE_QUADS) if chi[q + (F,)] > 0)


def units():
    out = [dict(id='L2_8_30_c%02d' % c, F=8, E=30, cube=c, cap=L2_CAP[30]) for c in range(16)]
    out += [dict(id='L2_9_39_c%02d' % c, F=9, E=39, cube=c, cap=L2_CAP[39]) for c in range(16)]
    out += [dict(id='L3_8_36_c%02d' % c, F=8, E=36, cube=c, cap=L3_CAP, max_models=L3_MODELS[c]) for c in range(16)]
    return out


def run_unit(u, out):
    if os.environ.get('P3_CAP'):                    # pilot: every unit cut to this cap
        u = dict(u, cap=min(u['cap'], float(os.environ['P3_CAP'])))
    t0 = time.monotonic(); deadline = t0 + u['cap']
    f = Formula(u['F'], edges=u['E'], cube=cube(u['F'], u['cube']))
    build = round(time.monotonic() - t0, 2)
    rec = dict(u, build_seconds=build, models=[])
    want = u.get('max_models', 1)
    while len(rec['models']) < want:
        left = deadline - time.monotonic()
        if left <= 1:
            rec['ended_by'] = 'cap'; break
        r = f.solve(left, seed=len(rec['models']))
        rec.setdefault('solves', []).append(dict(status=r['status'], seconds=r['seconds']))
        if r['status'] != 'OPTIMAL' and r['status'] != 'FEASIBLE':
            rec['ended_by'] = 'infeasible' if r['status'] == 'INFEASIBLE' else 'cap'
            break
        d = decode(r['chi'], r['cells'], u['F'])
        k = len(rec['models']); name = '%s_m%d' % (u['id'], k)
        model = dict(chi=chi_json(r['chi']), cells=r['cells'], gp_ok=gp_ok(r['chi'], u['F'] + 1),
                     decode_ok=d['ok'], decode_reason=d['reason'], links=d.get('links'), V=d.get('V'), E=d.get('E'))
        dump(out / (name + '.model.json'), model)
        entry = {k2: model[k2] for k2 in ('gp_ok', 'decode_ok', 'decode_reason', 'V', 'E')}
        if u['id'].startswith('L3') and d['ok']:
            left = deadline - time.monotonic()
            caps = tuple(max(1, min(c, left / 3)) for c in (90, 90, 60))
            entry['bridge'] = bridge(out, name, r['chi'], d['links'], caps)
        rec['models'].append(entry)
        if u['id'].startswith('L2'):
            rec['ended_by'] = 'SAT'; break
        f.block(r['chi'])
    else:
        rec['ended_by'] = 'models'
    rec['wall_seconds'] = round(time.monotonic() - t0, 1)
    return rec


def shard(s, n, out):
    out.mkdir(parents=True, exist_ok=True)
    done = set()
    for p in out.parent.glob('*/results.jsonl'):
        done |= {json.loads(line)['id'] for line in p.read_text().splitlines() if line.strip()}
    man = manifest_base(); man.update(shard=s, shards=n)
    dump(out / ('manifest-%d.json' % int(time.time())), man)
    for i, u in enumerate(units()):
        if i % n != s or u['id'] in done:
            continue
        if (out.parent / 'stop.requested').exists():
            break
        rec = run_unit(u, out)
        with (out / 'results.jsonl').open('a') as fh:
            fh.write(json.dumps(rec, default=str) + '\n')


def summary(results):
    rows = [json.loads(line) for p in sorted(Path(results).glob('*/results.jsonl')) for line in p.read_text().splitlines()
            if line.strip()]
    rep = {}
    for key in ('L2_8_30', 'L2_9_39', 'L3_8_36'):
        rs = [r for r in rows if r['id'].startswith(key)]
        rep[key] = dict(units=len(rs), ended_by={e: sum(r.get('ended_by') == e for r in rs)
                                                 for e in sorted({r.get('ended_by') for r in rs})},
                        core_seconds=round(sum(r['wall_seconds'] for r in rs), 1))
        ms = [m for r in rs for m in r['models']]
        if ms:
            rep[key]['models'] = len(ms)
            rep[key]['decode_ok'] = sum(m['decode_ok'] for m in ms)
            rep[key]['gp_ok'] = sum(m['gp_ok'] for m in ms)
            rep[key]['bridge'] = {s: sum((m.get('bridge') or {}).get('status_note') == s for m in ms)
                                  for s in sorted({(m.get('bridge') or {}).get('status_note') for m in ms}, key=str)}
    print(json.dumps(rep, indent=1))
    return rep


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['controls', 'shard', 'summary'])
    ap.add_argument('rest', nargs='*')
    a = ap.parse_args()
    if a.mode == 'controls':
        controls(Path(a.rest[0]))
    elif a.mode == 'shard':
        shard(int(a.rest[0]), int(a.rest[1]), Path(a.rest[2]))
    else:
        summary(a.rest[0])
