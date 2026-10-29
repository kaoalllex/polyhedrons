"""Helpers for orientable neighborly 12-vertex triangulations (triangular embeddings of K12).

Conventions (see data/README.md):
  * An oriented triangle [a, b, c] means: in the link of a, neighbour b is followed by c
    (equivalently at b, c is followed by a; at c, a is followed by b).
  * succ[v][a] = b  <=>  [v, a, b] is an oriented triangle.
  * rot(x) = neighbours of x in positive cyclic order, starting at the smallest neighbour.
  * code(T) = rot(0) + rot(1) + ... + rot(11)   (sequence of 132 labels).
  * canonical form = lexicographic minimum of code over all relabellings of T and both
    orientations; it is attained by one of the 12*11*2 "flag labellings".
"""
import itertools

N = 12
HEX = "0123456789ab"


def parse_rot_line(line):
    """Parse 'r0 | r1 | ... | r11' where ri lists the rotation of vertex i."""
    parts = line.strip().split("|")
    assert len(parts) == N
    succ = {}
    for v, p in enumerate(parts):
        r = [int(t) for t in p.split()]
        assert sorted(r) == [u for u in range(N) if u != v], (v, r)
        succ[v] = {r[i]: r[(i + 1) % len(r)] for i in range(len(r))}
    return succ


def succ_from_code(code):
    """code: string of 12 groups of 11 hex digits, optional '-' separators."""
    s = code.replace("-", "")
    assert len(s) == N * (N - 1)
    succ = {}
    for v in range(N):
        r = [HEX.index(ch) for ch in s[v * (N - 1):(v + 1) * (N - 1)]]
        succ[v] = {r[i]: r[(i + 1) % (N - 1)] for i in range(N - 1)}
    return succ


def pred_from_succ(succ):
    return {v: {b: a for a, b in succ[v].items()} for v in succ}


def rot(succ, x):
    start = min(succ[x])
    out, y = [], start
    for _ in range(N - 1):
        out.append(y)
        y = succ[x][y]
    return out


def code_of(succ):
    return [y for x in range(N) for y in rot(succ, x)]


def code_str(code):
    s = "".join(HEX[c] for c in code)
    return "-".join(s[i * (N - 1):(i + 1) * (N - 1)] for i in range(N))


def check_rule_delta(succ):
    for v in range(N):
        for a, b in succ[v].items():
            assert succ[a][b] == v and succ[b][v] == a, (v, a, b)
        # single cycle
        r = rot(succ, v)
        assert len(set(r)) == N - 1


def triangles_from_succ(succ):
    tris = set()
    for v in range(N):
        for a, b in succ[v].items():
            t = (v, a, b)
            i = t.index(min(t))
            tris.add(t[i:] + t[:i])
    return sorted(list(t) for t in tris)


def links_from_succ(succ):
    return {str(v): rot(succ, v) for v in range(N)}


def flag_labelling(succ, pred, v, a, d):
    """Labelling L (dict old->new) for flag (v,a,direction d=+1/-1)."""
    S = succ if d > 0 else pred
    L = {v: 0}
    cur = a
    for k in range(1, N):
        L[cur] = k
        cur = S[v][cur]
    return L


def relabel(succ, L, d):
    """Relabelled rotation system; d=-1 also reverses the orientation."""
    pred = pred_from_succ(succ)
    S = succ if d > 0 else pred
    return {L[x]: {L[y]: L[S[x][y]] for y in S[x]} for x in S}


def canonical(succ):
    """Return (code, aut, aut_op, autos) where autos = list of (perm list, d) automorphisms."""
    pred = pred_from_succ(succ)
    best, hits = None, []
    for v in range(N):
        for a in range(N):
            if a == v:
                continue
            for d in (1, -1):
                L = flag_labelling(succ, pred, v, a, d)
                c = code_of(relabel(succ, L, d))
                if best is None or c < best:
                    best, hits = c, [(L, d)]
                elif c == best:
                    hits.append((L, d))
    # automorphisms: g = L_j^{-1} o L_0
    L0, d0 = hits[0]
    autos = []
    for (Lj, dj) in hits:
        inv = {new: old for old, new in Lj.items()}
        g = [inv[L0[x]] for x in range(N)]
        autos.append((g, d0 * dj))
    aut = len(hits)
    aut_op = sum(1 for (_, s) in autos if s > 0)
    return best, aut, aut_op, autos, hits[0]


def to_canonical_labelling(succ):
    code, aut, aut_op, autos, (L0, d0) = canonical(succ)
    cs = relabel(succ, L0, d0)
    assert code_of(cs) == code
    return cs, code, aut, aut_op


def entry_from_succ(succ, idx=None):
    cs, code, aut, aut_op = to_canonical_labelling(succ)
    check_rule_delta(cs)
    e = {}
    if idx is not None:
        e["id"] = idx
    e["triangles"] = triangles_from_succ(cs)
    e["links"] = links_from_succ(cs)
    e["aut_order"] = aut
    e["aut_orient_preserving_order"] = aut_op
    e["chiral"] = (aut == aut_op)
    e["canonical"] = code_str(code)
    return e, cs
