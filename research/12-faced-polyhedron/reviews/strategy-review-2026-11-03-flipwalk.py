"""Flip-walk sampler of face-neighbourly triangular maps (review check, 2026-11-03).

An oriented triangular map with F triangles is (tri, alpha, tail): tri[t] = the 3 dart ids of triangle t in
cyclic order; alpha = fixed-point-free involution on darts (edge gluing); tail[d] = vertex label of dart d;
head(d) = tail[nxt(d)].  sigma(d) = alpha(prv(d)) permutes the darts leaving one vertex; the vertex count is the
number of sigma-cycles.  Loops and multiple edges are allowed; a candidate map for the S5 target (V, g) is a
loopless map with V vertices whose underlying simple graph is K_V.

Start: canonical 4g-gon with one vertex + centre, then V-2 stellar subdivisions.  Walk: random edge flips
(Metropolis on #non-adjacent pairs + #loops).  Hits are canonicalised (BFS code, min over roots and both
orientations) and checked independently by check().
Usage (from research/12-faced-polyhedron/, venv for the controls): python3 -I reviews/strategy-review-2026-11-03-flipwalk.py V g seconds [seed] [out.json]
       python3 -I ... k12control seconds | control83 seconds | rvstart seconds
"""
import sys, json, math, random, time, itertools


def build_start(V, g, rng):
    # 4g-gon glued a b a^-1 b^-1 ...: one vertex v=0; centre c=1; triangles T_i = (c -> p_i, p_i -> p_{i+1}, p_{i+1} -> c)
    m = 4 * g
    tri, tail, alpha = [], [], {}
    for i in range(m):
        d0, d1, d2 = 3 * i, 3 * i + 1, 3 * i + 2
        tri.append([d0, d1, d2]); tail += [1, 0, 0]
    for i in range(m):
        j = (i + 1) % m
        alpha[3 * i + 2] = 3 * j; alpha[3 * j] = 3 * i + 2            # spoke between T_i and T_{i+1}
    for k in range(g):                                                  # sides a b a' b': i <-> i+2
        for s in (4 * k, 4 * k + 1):
            alpha[3 * s + 1] = 3 * (s + 2) + 1; alpha[3 * (s + 2) + 1] = 3 * s + 1
    M = TriMap(tri, alpha, tail)
    assert M.vertex_count() == 2
    for v in range(2, V):
        M.stellar(rng.randrange(len(M.tri)), v)
    return M


class TriMap:
    def __init__(self, tri, alpha, tail):
        self.tri = [list(t) for t in tri]
        self.alpha = dict(alpha)
        self.tail = list(tail)
        self.pos = {}
        for t, ds in enumerate(self.tri):
            for i, d in enumerate(ds):
                self.pos[d] = (t, i)

    def nxt(self, d):
        t, i = self.pos[d]; return self.tri[t][(i + 1) % 3]

    def prv(self, d):
        t, i = self.pos[d]; return self.tri[t][(i + 2) % 3]

    def head(self, d):
        return self.tail[self.nxt(d)]

    def stellar(self, t, v):
        a, b, c = self.tri[t]                       # a: x->y, b: y->z, c: z->x
        x, y, z = self.tail[a], self.tail[b], self.tail[c]
        n = len(self.tail)
        new = list(range(n, n + 6)); self.tail += [0] * 6
        # triangles (x->y, y->v, v->x), (y->z, z->v, v->y), (z->x, x->v, v->z)
        p, q, r, s, u, w = new
        self.tail[p], self.tail[q] = y, v           # p: y->v, q: v->x
        self.tail[r], self.tail[s] = z, v           # r: z->v, s: v->y
        self.tail[u], self.tail[w] = x, v           # u: x->v, w: v->z
        self.tri[t] = [a, p, q]
        self.tri.append([b, r, s]); self.tri.append([c, u, w])
        for tt in (t, len(self.tri) - 2, len(self.tri) - 1):
            for i, d in enumerate(self.tri[tt]):
                self.pos[d] = (tt, i)
        self.alpha[p] = s; self.alpha[s] = p        # y<->v
        self.alpha[r] = w; self.alpha[w] = r        # z<->v
        self.alpha[u] = q; self.alpha[q] = u        # x<->v

    def flip(self, d):
        """Flip the edge of dart d; returns (a, b, c, x) = old edge a-b, new edge c-x, or None if illegal."""
        dp = self.alpha[d]
        t, i = self.pos[d]; tp, ip = self.pos[dp]
        if t == tp:
            return None
        d1, d2 = self.tri[t][(i + 1) % 3], self.tri[t][(i + 2) % 3]        # d: a->b, d1: b->c, d2: c->a
        e1, e2 = self.tri[tp][(ip + 1) % 3], self.tri[tp][(ip + 2) % 3]    # dp: b->a, e1: a->x, e2: x->b
        a, b, c, x = self.tail[d], self.tail[dp], self.tail[d2], self.tail[e2]
        self.tri[t] = [d2, e1, d]       # c->a, a->x, x->c
        self.tri[tp] = [e2, d1, dp]     # x->b, b->c, c->x
        self.tail[d], self.tail[dp] = x, c
        for tt in (t, tp):
            for j, dd in enumerate(self.tri[tt]):
                self.pos[dd] = (tt, j)
        return a, b, c, x

    def vertex_count(self):
        seen = set(); cnt = 0
        for d in self.pos:
            if d in seen:
                continue
            cnt += 1; e = d
            while e not in seen:
                seen.add(e); e = self.alpha[self.prv(e)]
        return cnt

    def code(self, root, mirror=False):
        step = self.prv if mirror else self.nxt
        lab = {root: 0}; order = [root]; k = 0
        while k < len(order):
            d = order[k]; k += 1
            for e in (step(d), self.alpha[d]):
                if e not in lab:
                    lab[e] = len(order); order.append(e)
        return tuple((lab[step(d)], lab[self.alpha[d]]) for d in order), order

    def canon(self):
        best = None; best_or = None
        aut_plus = 0; reflex = False
        codes = {}
        for mirror in (False, True):
            for r in self.pos:
                c, order = self.code(r, mirror)
                codes[(r, mirror)] = c
                if best is None or c < best:
                    best, best_or = c, (r, mirror)
        roots_plus = [r for (r, m), c in codes.items() if c == best and m == best_or[1]]
        roots_mirror = [r for (r, m), c in codes.items() if c == best and m != best_or[1]]
        return best, len(roots_plus), len(roots_mirror) > 0, roots_plus, best_or

    def automorphisms(self):
        """Orientation-preserving automorphisms as dart permutations (from equal canonical codes)."""
        best, _, _, roots, (r0, m0) = self.canon()
        _, base = self.code(r0, m0)
        auts = []
        for r in roots:
            _, order = self.code(r, m0)
            auts.append({base[i]: order[i] for i in range(len(base))})
        return auts

    def vertices(self):
        seen = {}; cyc = []
        for d in self.pos:
            if d in seen:
                continue
            c = []; e = d
            while e not in seen:
                seen[e] = len(cyc); c.append(e); e = self.alpha[self.prv(e)]
            cyc.append(c)
        return cyc, seen


def check(M, V, g):
    """Independent check: surface, labels consistent, V vertices, loopless, K_V, Euler characteristic."""
    D = sorted(M.pos); n = len(D)
    assert n == 3 * len(M.tri)
    assert all(M.alpha[M.alpha[d]] == d and M.alpha[d] != d for d in D), 'alpha'
    assert all(M.tail[M.alpha[d]] == M.head(d) and M.head(M.alpha[d]) == M.tail[d] for d in D), 'labels'
    cyc, which = M.vertices()
    assert len(cyc) == V, ('vertex count', len(cyc))
    labels = [set(M.tail[d] for d in c) for c in cyc]
    assert all(len(s) == 1 for s in labels) and len(set(min(s) for s in labels)) == V, 'one cycle per label'
    assert not any(M.tail[d] == M.head(d) for d in D), 'loop'
    adj = {frozenset((M.tail[d], M.head(d))) for d in D}
    assert len(adj) == V * (V - 1) // 2, ('not neighbourly', len(adj))
    E = n // 2; F = len(M.tri)
    assert V - E + F == 2 - 2 * g, ('Euler', V, E, F)
    _, order = M.code(D[0]); assert len(order) == n, 'disconnected'
    return True


def invariants(M, V):
    mult = {}
    for d in M.pos:
        u, v = M.tail[d], M.head(d)
        if u < v:
            mult[(u, v)] = mult.get((u, v), 0) + 1
    deg = [0] * V
    for d in M.pos:
        deg[M.tail[d]] += 1
    extra = sorted((u, v, m) for (u, v), m in mult.items() if m > 1)
    exdeg = [0] * V
    for u, v, m in extra:
        exdeg[u] += m - 1; exdeg[v] += m - 1
    return {'degrees': sorted(deg), 'extra_edges': extra, 'extra_pattern': sorted(x for x in exdeg if x)}


def aut_report(M):
    auts = M.automorphisms()
    cyc, which = M.vertices()
    out = []
    for a in auts:
        # order
        k = 1; p = dict(a)
        while any(p[d] != d for d in p):
            p = {d: a[p[d]] for d in p}; k += 1
        if k == 1:
            continue
        fixed_v = sum(1 for c in cyc if which[a[c[0]]] == which[c[0]])
        fixed_e = sum(1 for d in M.pos if a[d] in (d, M.alpha[d])) // 2
        fixed_t = sum(1 for t in M.tri if M.pos[a[t[0]]][0] == M.pos[t[0]][0])
        out.append((k, fixed_v, fixed_e, fixed_t))
    return sorted(out)


def walk(V, g, seconds, seed, T=0.6, loopw=2.0, log=None):
    rng = random.Random(seed)
    M = build_start(V, g, rng)
    E = len(M.pos) // 2
    mult = [[0] * V for _ in range(V)]
    for d in M.pos:
        if d < M.alpha[d]:                      # one count per edge
            u, v = sorted((M.tail[d], M.head(d)))
            mult[u][v] += 1
    loops = sum(mult[u][u] for u in range(V))
    nonadj = sum(1 for u in range(V) for v in range(u + 1, V) if mult[u][v] == 0)
    f = nonadj + loopw * loops
    darts = sorted(M.pos)
    found = {}; t0 = time.time(); steps = acc = 0; hits = 0
    def pr(u, v):
        return (u, v) if u <= v else (v, u)
    while time.time() - t0 < seconds:
        steps += 1
        d = darts[rng.randrange(len(darts))]
        res = M.flip(d)
        if res is None:
            continue
        a, b, c, x = res
        da, db = 0, 0
        u, v = pr(a, b); mult[u][v] -= 1
        if u == v:
            da -= loopw
        elif mult[u][v] == 0:
            da += 1
        u, v = pr(c, x); mult[u][v] += 1
        if u == v:
            da += loopw
        elif mult[u][v] == 1:
            da -= 1
        if da <= 0 or rng.random() < math.exp(-da / T):
            f += da; acc += 1
            if acc % 200000 == 0:               # consistency of the incremental objective
                m2 = {}
                for dd in M.pos:
                    if dd < M.alpha[dd]:
                        k2 = tuple(sorted((M.tail[dd], M.head(dd)))); m2[k2] = m2.get(k2, 0) + 1
                na2 = sum(1 for u in range(V) for v in range(u + 1, V) if (u, v) not in m2)
                lo2 = sum(m2.get((u, u), 0) for u in range(V))
                assert abs(f - (na2 + loopw * lo2)) < 1e-9, (f, na2, lo2)
            if f == 0:
                hits += 1
                key, autp, refl, _, _ = M.canon()
                if key not in found:
                    check(M, V, g)
                    inv = invariants(M, V)
                    inv.update(aut_plus=autp, reflexible=refl, first_seen_s=round(time.time() - t0, 1),
                               autos=aut_report(M),
                               links=[[M.head(d) for d in c] for c in sorted(M.vertices()[0], key=lambda c: M.tail[c[0]])])
                    found[key] = inv
                    if log:
                        print('  new class #%d at %.0fs: deg %s extra %s |Aut+| %d refl %s autos %s' % (
                            len(found), time.time() - t0, inv['degrees'], inv['extra_pattern'], autp, refl,
                            inv['autos']), file=log, flush=True)
                else:
                    found[key]['seen'] = found[key].get('seen', 1) + 1
        else:
            # undo: flip the same edge back (dart d now carries the new diagonal)
            M.flip(d)
            u, v = pr(c, x); mult[u][v] -= 1
            u, v = pr(a, b); mult[u][v] += 1
    return found, steps, acc, hits


def k12_control(seconds, seed=1):
    """Canonical codes of the 59 types from data/k12_triangulations.json; walk at (12, 6); every hit must be one of them."""
    data = json.load(open('data/k12_triangulations.json'))
    codes = {}
    for rec in data:
        tris = rec['triangles']
        tri, tail, alpha = [], [], {}
        dart_of = {}
        for t, (a, b, c) in enumerate(tris):
            ds = [3 * t, 3 * t + 1, 3 * t + 2]
            tri.append(ds); tail += [a, b, c]
            for d, (u, v) in zip(ds, ((a, b), (b, c), (c, a))):
                dart_of[(u, v)] = d
        for (u, v), d in dart_of.items():
            alpha[d] = dart_of[(v, u)]
        M = TriMap(tri, alpha, tail)
        check(M, 12, 6)
        key, autp, refl, _, _ = M.canon()
        codes[key] = (rec['id'], autp, refl)
    print('59 types canonicalised: %d distinct codes; |Aut+| histogram %s; reflexible %d' % (
        len(codes), sorted(set(v[1] for v in codes.values())), sum(v[2] for v in codes.values())))
    found, steps, acc, hits = walk(12, 6, seconds, seed)
    ids = sorted(codes[k][0] for k in found if k in codes)
    bad = [k for k in found if k not in codes]
    print('walk (12,6) %ds: %d steps, %d accepted, %d hits, %d classes found, %d NOT among the 59, ids %s' % (
        seconds, steps, acc, hits, len(found), len(bad), ids))
    for k in found:
        if k in codes:
            assert codes[k][1] == found[k]['aut_plus'] and codes[k][2] == found[k]['reflexible']




# ----------------------------------------------------------------------------- controls on the known 8-face objects
def dual_map(links):
    """Oriented dual triangular map of a cubic polyhedron given by coherently oriented face links (cyclic neighbour lists,
    repeats = multiple adjacencies). Corner i of face X = (X, L[i], L[i+1]); edge i of X (line X cap L[i]) joins corners
    i-1 and i, so alpha pairs dart L[i]->X of corner i-1 with dart X->L[i] of corner i."""
    tri, tail, alpha, tid, dart_at = [], [], {}, {}, {}
    for X, L in links.items():
        m = len(L)
        for i in range(m):
            key = frozenset((X, L[i], L[(i + 1) % m]))
            if key not in tid:
                t = len(tri); tid[key] = t
                ds = [3 * t, 3 * t + 1, 3 * t + 2]
                tri.append(ds); tail += [X, L[i], L[(i + 1) % m]]
                for d, (u, v) in zip(ds, ((X, L[i]), (L[i], L[(i + 1) % m]), (L[(i + 1) % m], X))):
                    dart_at[(t, u, v)] = d
    for X, L in links.items():
        m = len(L)
        for i in range(m):
            Y = L[i]
            d1 = dart_at[(tid[frozenset((X, L[i - 1], Y))], Y, X)]
            d2 = dart_at[(tid[frozenset((X, Y, L[(i + 1) % m]))], X, Y)]
            assert alpha.get(d1, d2) == d2
            alpha[d1] = d2; alpha[d2] = d1
    return TriMap(tri, alpha, tail)


def coherent(links):
    """Reverse face cycles so that every shared edge is traversed in opposite directions by its two faces."""
    links = {X: list(L) for X, L in links.items()}
    corner = lambda X, i: frozenset((X, links[X][i % len(links[X])], links[X][(i + 1) % len(links[X])]))
    done = {0}; queue = [0]
    while queue:
        X = queue.pop(); L = links[X]
        for i in range(len(L)):
            Y = L[i]; A, B = corner(X, i - 1), corner(X, i)
            js = [j for j in range(len(links[Y])) if links[Y][j] == X and {corner(Y, j - 1), corner(Y, j)} == {A, B}]
            assert len(js) == 1, (X, Y, js)
            ok = corner(Y, js[0] - 1) == B and corner(Y, js[0]) == A
            if Y in done:
                assert ok, ('not orientable or inconsistent links', X, Y)
            else:
                if not ok:
                    links[Y] = links[Y][::-1]
                done.add(Y); queue.append(Y)
    return links


def known_8_3():
    sys.path.insert(0, 'code')
    import control_rost_vigh
    _, links_rv = control_rost_vigh.build()
    mz = json.load(open('literature/mizhaev2026-planes.json'))['links_0based']
    links_mz = {int(k): v for k, v in mz.items()} if isinstance(mz, dict) else {i: v for i, v in enumerate(mz)}
    out = {}
    for name, links in (('Roest-Vigh', links_rv), ('Mizhaev', links_mz)):
        M = dual_map(coherent(links)); check(M, 8, 3)
        key, autp, refl, _, _ = M.canon()
        print('%s: dual map checked (8 vertices, genus 3, K8 + 8 extra); |Aut+| = %d, reflexible %s, extra %s, autos %s' % (
            name, autp, refl, invariants(M, 8)['extra_edges'], aut_report(M)))
        out[key] = (name, M)
    print('the two maps are %s' % ('distinct' if len(out) == 2 else 'THE SAME'))
    return out


def control83(seconds):
    """Walk at (8, 3); report whether the two known maps are among the classes found (they were not in 150 s: the (8, 3)
    space is far from saturated, 22,666 classes seen, so this is a power statement, not a failure of the walker)."""
    known = known_8_3()
    found, steps, acc, hits = walk(8, 3, seconds, 1)
    print('walk (8,3) %ds: %d steps, %d accepted, %d hits, %d classes' % (seconds, steps, acc, hits, len(found)))
    for key, (name, _) in known.items():
        print('  %s found: %s' % (name, key in found))
    t = sorted(v['first_seen_s'] for v in found.values())
    print('first-seen quantiles (s):', [t[int(q * (len(t) - 1))] for q in (0, 0.5, 0.9, 0.99, 1)])


def rvstart(seconds):
    """Ergodicity control: the (9, 3) walk started from a stellar subdivision of the Roest-Vigh dual map."""
    known = known_8_3()
    M = [m for name, m in known.values() if name == 'Roest-Vigh'][0]
    rng = random.Random(7); M.stellar(rng.randrange(len(M.tri)), 8)
    global build_start
    build_start = lambda V, g, rng: M
    found, steps, acc, hits = walk(9, 3, seconds, 7)
    print('RV-start walk (9,3) %ds: %d classes' % (seconds, len(found)))


if __name__ == '__main__':
    if sys.argv[1] == 'k12control':
        k12_control(int(sys.argv[2])); sys.exit()
    if sys.argv[1] == 'control83':
        control83(int(sys.argv[2])); sys.exit()
    if sys.argv[1] == 'rvstart':
        rvstart(int(sys.argv[2])); sys.exit()
    V, g, secs = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    found, steps, acc, hits = walk(V, g, secs, seed, log=sys.stderr)
    E = 3 * (V + 2 * g - 2)
    print('(V, g) = (%d, %d): E = %d, F = %d, extra = %d; %d s, %d steps, %d accepted, %d hits at f = 0' % (
        V, g, E, 2 * E // 3, E - V * (V - 1) // 2, secs, steps, acc, hits))
    print('distinct classes (up to isomorphism and mirror): %d' % len(found))
    from collections import Counter
    print('|Aut+| histogram:', sorted(Counter(v['aut_plus'] for v in found.values()).items()))
    print('reflexible:', sum(v['reflexible'] for v in found.values()))
    print('extra-edge patterns:', sorted(Counter(tuple(v['extra_pattern']) for v in found.values()).items()))
    seen = [v.get('seen', 1) for v in found.values()]
    print('seen once %d, twice %d' % (sum(1 for s in seen if s == 1), sum(1 for s in seen if s == 2)))
    if len(sys.argv) > 5:
        json.dump([dict(v, code=repr(k)) for k, v in found.items()], open(sys.argv[5], 'w'))
        print('written', sys.argv[5])
