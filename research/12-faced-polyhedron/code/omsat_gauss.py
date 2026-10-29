"""Gauss-map degree / covering clauses for formulation A (OM-SAT), families F7 + F8.

Adds k abstract generic DIRECTIONS u_1..u_k as new elements of the rank-3 oriented matroid of the
face normals (kappa(a,b,c) = chi(a,b,c,inf) = sign det(n_a,n_b,n_c), kappa(u,a,b) = new variables
psi_u(a,b) = sign det(u,n_a,n_b)), constrained by the uniform 3-term Grassmann-Pluecker relations
involving u. For every real realization any generic real u gives a satisfying assignment, so the
clauses are sound. For each u:
    deg(u) = #(negative triangles containing u) - #(positive ...) must equal -chi/2 ... i.e.
    sum_T sign(T) [u in cone T] = chi/2,  and  some positive triangle contains u  (gauss_degree.py).
Triangle signs use gauge normals g_X = (-1)^{Wn_X} n_X, Wn_X = (RTURN xor REFLEX) at a corner of
face X (true iff face X is clockwise about n_X); requires the poc family (F6) and coherent links.
"""
import itertools

from pysat.card import CardEnc, EncType


def add_gauss(C, P, T, k=3, target=None):
    n = T.n
    INF = n
    if target is None:
        V = len({frozenset(t) for t in T.tris})
        chi = n - n * (n - 1) // 2 + V
        target = chi // 2
    # gauge bits
    Wn = []
    for X in range(n):
        A, B = T.corners(X)[0]
        Wn.append(C.xor([P.RTURN(X, A, B), P.REFLEX(X, A, B)]))
    # oriented triangles from coherent links
    otri = {}
    for X in range(n):
        L = T.link[X]
        for i in range(len(L)):
            t = (X, L[i], L[(i + 1) % len(L)])
            otri.setdefault(frozenset(t), t)
    otris = list(otri.values())

    def kneg_faces(a, b, c):
        return C.chi_neg((a, b, c, INF))

    for j in range(k):
        psi = {}
        for a, b in itertools.combinations(range(n), 2):
            psi[(a, b)] = C.new()
        U = 'u'

        def kneg(t):
            """literal: kappa(t) < 0 for an ordered triple t of faces and/or U."""
            if U not in t:
                return kneg_faces(*t)
            rest = [x for x in t if x != U]
            pos = t.index(U)
            a, b = rest
            lit = psi[(a, b)] if a < b else -psi[(b, a)]
            # move U to the front: positions 0,1,2 -> 0,1,2 transpositions
            if pos == 1:
                lit = -lit
            return lit

        # 3-term GP relations involving U (uniform): not all three terms of equal sign
        elems = list(range(n)) + [U]
        for x in elems:
            others = [e for e in elems if e != x]
            for a, b, c, d in itertools.combinations(others, 4):
                if U != x and U not in (a, b, c, d):
                    continue
                n1 = C.xor([kneg((x, a, b)), kneg((x, c, d))])
                n2 = -C.xor([kneg((x, a, c)), kneg((x, b, d))])
                n3 = C.xor([kneg((x, a, d)), kneg((x, b, c))])
                C.clause([n1, n2, n3], 'GAUSS_GP')
                C.clause([-n1, -n2, -n3], 'GAUSS_GP')
        pin, nin = [], []
        for a, b, c in otris:
            sneg = C.xor([Wn[a], Wn[b], Wn[c], kneg((a, b, c))])
            base = C.xor([kneg((a, b, c))])
            c1 = -C.xor([kneg((U, b, c)), Wn[a], base])
            c2 = -C.xor([kneg((a, U, c)), Wn[b], base])
            c3 = -C.xor([kneg((a, b, U)), Wn[c], base])
            inside = C.and_([c1, c2, c3])
            pin.append(C.and_([-sneg, inside]))
            nin.append(C.and_([sneg, inside]))
        # sum nin - sum pin = -target  <=>  sum nin + sum(not pin) = len - target
        lits = nin + [-x for x in pin]
        enc = CardEnc.equals(lits=lits, bound=len(otris) - target, top_id=C.nv, encoding=EncType.seqcounter)
        C.nv = max(C.nv, enc.nv)
        for cl in enc.clauses:
            C.clause(cl, 'GAUSS_DEG')
        C.clause(pin, 'GAUSS_COVER')
    return target
