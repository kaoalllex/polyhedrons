"""Lead review 2026-11-19 session check (not ledger evidence): quad-orbit counts and forced zero signs.

A quad S of elements (planes 0..F-1, plus INF = F in the standard chart) is forced to sign 0 by a symmetry g with
determinant det if g(S) = S and det * sign(g restricted to S) = -1. Pure Python, seconds:
    python3 research/12-faced-polyhedron/reviews/strategy-review-2026-11-19-orbits.py
"""
import itertools


def perm_sign(p, S):
    S = sorted(S)
    idx = {s: i for i, s in enumerate(S)}
    q = [idx[p[s]] for s in S]
    sign, seen = 1, [False] * len(q)
    for i in range(len(q)):
        j, length = i, 0
        while not seen[j]:
            seen[j], j, length = True, q[j], length + 1
        if length and length % 2 == 0:
            sign = -sign
    return sign


def elements(F, p, with_inf):
    return list(range(F)) + ([F] if with_inf else []), list(p) + ([F] if with_inf else [])


def forced(F, p, det, with_inf):
    els, P = elements(F, p, with_inf)
    return [S for S in itertools.combinations(els, 4)
            if {P[s] for s in S} == set(S) and det * perm_sign(P, S) == -1]


def quad_orbits(F, gens, with_inf=True):
    els, _ = elements(F, gens[0], with_inf)
    G = {tuple(els)}
    frontier = list(G)
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                gg = list(g) + ([F] if with_inf else [])
                y = tuple(gg[x[i]] for i in range(len(els)))
                if y not in G:
                    G.add(y)
                    new.append(y)
        frontier = new
    return len({min(tuple(sorted(g[e] for e in S)) for g in G) for S in itertools.combinations(els, 4)})


def involution(k, f):
    """k free 2-orbits (0 1)(2 3)..., then f fixed elements."""
    return [2 * (i // 2) + 1 - i % 2 for i in range(2 * k)] + list(range(2 * k, 2 * k + f))


if __name__ == '__main__':
    D2 = [(1, 0, 3, 2, 5, 4, 7, 6), (2, 3, 0, 1, 6, 7, 4, 5)]
    S4 = [(1, 2, 3, 0, 5, 6, 7, 4)]
    C2 = [tuple(involution(4, 0))]
    C3 = [(1, 2, 0, 4, 5, 3, 7, 8, 6)]
    print('quad orbits (standard chart): D2 8 =', quad_orbits(8, D2), '| S4 8 =', quad_orbits(8, S4),
          '| free C2 8 =', quad_orbits(8, C2), '| C3 9 =', quad_orbits(9, C3), '| plain 7, 8, 9 = 70, 126, 210')
    print('F=8 free half-turn, standard chart: forced zeros', len(forced(8, involution(4, 0), 1, True)))
    print('F=8 mirror (k free 2-orbits, f fixed), standard chart:',
          {(k, 8 - 2 * k): len(forced(8, involution(k, 8 - 2 * k), -1, True)) for k in range(5)})
    print('F=9 half-turn 4 x 2 + 1: standard chart', len(forced(9, involution(4, 1), 1, True)),
          '| plane-only', len(forced(9, involution(4, 1), 1, False)))
    print('F=9 mirror, plane-only:', {(k, 9 - 2 * k): len(forced(9, involution(k, 9 - 2 * k), -1, False)) for k in range(5)})
    print('F=11 mirror, plane-only:', {(k, 11 - 2 * k): len(forced(11, involution(k, 11 - 2 * k), -1, False))
                                       for k in range(6)})
