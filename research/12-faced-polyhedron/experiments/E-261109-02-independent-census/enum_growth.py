"""Independent census of face-neighbourly triangular maps (F vertices, genus g, underlying graph K_F).

Algorithm (shares no code with E-261103-01): grow an oriented triangulated surface triangle by triangle.
A triangle is an ordered vertex triple (a, b, c); its sides are a->b, b->c, c->a. The lowest-numbered open side
u->v is glued either to an existing open side v->u or to a side of a new triangle (v, u, w), w an existing vertex
or the next unused label. Edge-multiplicity pruning: the pairs of K_F need C(F,2) edges, so the excess over one
edge per pair is bounded by E - C(F,2). Final checks: all vertices used, every pair present, every vertex link one
cycle. Classes are deduplicated by a label-free canonical form (BFS code over all root sides and both orientations).
"""
import json
import sys
import time
from itertools import count


def canon(partner, ntri):
    """partner: dict (t, i) -> (t2, i2). Return (code, orientation-preserving automorphisms, mirror-equivalent)."""
    best = {False: None, True: None}
    auts = 0
    for mirror in (False, True):
        if mirror:
            mp = lambda i: (1 - i) % 3 if i < 2 else 2
            P = {(t, mp(i)): (t2, mp(i2)) for (t, i), (t2, i2) in partner.items()}
        else:
            P = partner
        for rt in range(ntri):
            for ri in range(3):
                order, idx = [rt], {rt: 0}
                entry = {rt: ri}
                code = []
                q = 0
                while q < len(order):
                    t = order[q]
                    q += 1
                    row = []
                    for k in range(3):
                        s = (entry[t] + k) % 3
                        t2, i2 = P[(t, s)]
                        if t2 not in idx:
                            idx[t2] = len(order)
                            order.append(t2)
                            entry[t2] = i2
                        row.append((idx[t2], (i2 - entry[t2]) % 3))
                    code.append(tuple(row))
                code = tuple(code)
                if best[mirror] is None or code < best[mirror]:
                    best[mirror] = code
                    cnt = 1
                elif code == best[mirror]:
                    cnt += 1
        if mirror is False:
            auts = cnt
    m0, m1 = best[False], best[True]
    return min(m0, m1), auts, m0 == m1


def pair(u, v):
    return (u, v) if u < v else (v, u)


def enumerate_maps(F, g, log=None):
    T = 2 * (F + 2 * g - 2)
    E = 3 * T // 2
    extra = E - F * (F - 1) // 2
    assert extra >= 0
    tris = [(0, 1, 2)]
    partner = {}
    closed = {}      # pair -> closed edges
    opened = {}      # (u, v) directed -> open sides u->v
    found = {}
    nodes = [0]

    def lower_bound_excess():
        pairs = set(closed) | {pair(*d) for d in opened}
        ex = 0
        for p in pairs:
            ex += closed.get(p, 0) + max(opened.get(p, 0), opened.get((p[1], p[0]), 0)) - 1
        return ex

    def add_open(a, b, d):
        opened[(a, b)] = opened.get((a, b), 0) + d
        if not opened[(a, b)]:
            del opened[(a, b)]

    def open_sides():
        return [(t, i) for t in range(len(tris)) for i in range(3) if (t, i) not in partner]

    def side(t, i):
        tr = tris[t]
        return tr[i], tr[(i + 1) % 3]

    for i in range(3):
        a, b = side(0, i)
        add_open(a, b, 1)

    def finish():
        nv = 1 + max(max(t) for t in tris)
        if nv != F:
            return
        if len({pair(*side(t, i)) for t in range(T) for i in range(3)}) != F * (F - 1) // 2:
            return
        # vertex links: corners (t, i) at vertex tris[t][i]; walk around the vertex via partners
        seen = set()
        for t in range(T):
            for i in range(3):
                if (t, i) in seen:
                    continue
                v = tris[t][i]
                cur, n = (t, i), 0
                while cur not in seen:
                    seen.add(cur)
                    n += 1
                    # corner (t,i) has incoming side (i-1) and outgoing side i; cross the outgoing side
                    t2, i2 = partner[(cur[0], cur[1])]
                    # partner side i2 is v-incident: it is the incoming side of the next corner at v
                    cur = (t2, (i2 + 1) % 3)
                if cur != (t, i):
                    return
                total = sum(1 for tt in range(T) for ii in range(3) if tris[tt][ii] == v)
                if n != total:
                    return
        code, aut, refl = canon(dict(partner), T)
        if code not in found:
            found[code] = dict(tris=list(tris), partner=dict(partner), aut_plus=aut, reflexible=refl)

    def rec():
        nodes[0] += 1
        os_ = open_sides()
        nt = len(tris)
        if not os_:
            if nt == T:
                finish()
            return
        if nt == T and False:
            return
        r = T - nt
        if (len(os_) + r) % 2:
            return
        if len(os_) > 2 * r + 0 and len(os_) - 2 * r > 0:
            # each remaining new triangle closes at most one open side by itself plus glues; bound is loose
            pass
        t, i = os_[0]
        u, v = side(t, i)
        # (a) glue to an existing open side v->u
        for (t2, i2) in os_[1:]:
            if side(t2, i2) == (v, u):
                partner[(t, i)] = (t2, i2)
                partner[(t2, i2)] = (t, i)
                add_open(u, v, -1)
                add_open(v, u, -1)
                p = pair(u, v)
                closed[p] = closed.get(p, 0) + 1
                if lower_bound_excess() <= extra:
                    rec()
                closed[p] -= 1
                if not closed[p]:
                    del closed[p]
                add_open(u, v, 1)
                add_open(v, u, 1)
                del partner[(t, i)], partner[(t2, i2)]
        # (b) new triangle (v, u, w)
        if nt < T:
            nv = 1 + max(max(x) for x in tris)
            for w in range(min(nv + 1, F)):
                if w == u or w == v:
                    continue
                new = (v, u, w)
                tris.append(new)
                k = len(tris) - 1
                partner[(t, i)] = (k, 0)
                partner[(k, 0)] = (t, i)
                add_open(u, v, -1)
                p = pair(u, v)
                closed[p] = closed.get(p, 0) + 1
                add_open(u, w, 1)   # side 1 of new: u->w
                add_open(w, v, 1)   # side 2 of new: w->v
                if lower_bound_excess() <= extra:
                    rec()
                add_open(u, w, -1)
                add_open(w, v, -1)
                closed[p] -= 1
                if not closed[p]:
                    del closed[p]
                add_open(u, v, 1)
                del partner[(t, i)], partner[(k, 0)]
                tris.pop()

    t0 = time.time()
    rec()
    return found, nodes[0], time.time() - t0, T


def admissible(tris):
    return len({tuple(sorted(t)) for t in tris}) == len(tris)


if __name__ == "__main__":
    F, g = int(sys.argv[1]), int(sys.argv[2])
    found, nodes, sec, T = enumerate_maps(F, g)
    adm = sum(admissible(m["tris"]) for m in found.values())
    print(json.dumps(dict(F=F, g=g, classes=len(found), admissible=adm, nodes=nodes, seconds=round(sec, 3))))
