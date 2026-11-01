"""Biquadratic final polynomials (Bokowski, Richter-Gebert) for a uniform rank-4 chirotope on 13 elements.

Every 3-term Grassmann-Pluecker relation  [tau a b][tau c d] - [tau a c][tau b d] + [tau a d][tau b c] = 0  has, for a
uniform chirotope, exactly one term whose sign differs from the other two; in a realization that term dominates each of
the others in absolute value. Taking logarithms L(S) = log |[S]| gives two strict linear inequalities per relation.
If the system over all relations has no solution, no realization exists, and the Farkas multipliers are the final
polynomial. The multipliers are rounded to rationals and the identity sum y_i A_i = 0 is re-checked exactly, so a
certificate labelled EXACT is a proof of non-realizability of that chirotope. Feasibility of the LP proves nothing
(biquadratic final polynomials are not complete).
"""
import itertools
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix


def _sign(chi, tup):
    """chi value of an ordered tuple via the sorted key and the permutation parity."""
    s = tuple(sorted(tup))
    p = 0
    t = list(tup)
    for i in range(len(t)):
        for j in range(i + 1, len(t)):
            if t[i] > t[j]:
                p ^= 1
    v = chi[s]
    return -v if p else v, s


def relations(chi, n_elems):
    """Yield (dominant pair, other pair 1, other pair 2) as triples of sorted 4-subset keys, one per GP relation."""
    E = list(range(n_elems))
    for tau in itertools.combinations(E, 2):
        rest = [e for e in E if e not in tau]
        for a, b, c, d in itertools.combinations(rest, 4):
            s1, k1 = _sign(chi, tau + (a, b)); s2, k2 = _sign(chi, tau + (c, d))
            s3, k3 = _sign(chi, tau + (a, c)); s4, k4 = _sign(chi, tau + (b, d))
            s5, k5 = _sign(chi, tau + (a, d)); s6, k6 = _sign(chi, tau + (b, c))
            if 0 in (s1, s2, s3, s4, s5, s6):
                continue
            t1, t2, t3 = s1 * s2, -s3 * s4, s5 * s6
            terms = [((k1, k2), t1), ((k3, k4), t2), ((k5, k6), t3)]
            if t1 == t2 == t3:
                raise ValueError('GP axiom violated at %s %s' % (tau, (a, b, c, d)))
            dom = [i for i in range(3) if sum(1 for j in range(3) if terms[j][1] == terms[i][1]) == 1][0]
            others = [terms[i][0] for i in range(3) if i != dom]
            yield terms[dom][0], others[0], others[1]


def final_polynomial(chi, n_elems=13, tol=1e-9):
    """Returns dict(status, t_star, support (list of relation indices), brackets (sorted 4-subsets in the support),
    exact (bool), n_relations)."""
    keys = sorted(chi)
    kidx = {k: i for i, k in enumerate(keys)}
    rows, cols, vals, rel_of_row = [], [], [], []
    rels = list(relations(chi, n_elems))
    r = 0
    for ridx, (dom, o1, o2) in enumerate(rels):
        for other in (o1, o2):
            # L[dom0] + L[dom1] - L[other0] - L[other1] >= t
            for k in dom:
                rows.append(r); cols.append(kidx[k]); vals.append(1.0)
            for k in other:
                rows.append(r); cols.append(kidx[k]); vals.append(-1.0)
            rel_of_row.append(ridx); r += 1
    A = csr_matrix((vals, (rows, cols)), shape=(r, len(keys)))
    # maximise t s.t. A L - t >= 0, L in [-1, 1]
    A_ub = csr_matrix(np.hstack([-A.toarray(), np.ones((r, 1))])) if r < 20000 else None
    if A_ub is None:
        from scipy.sparse import hstack
        A_ub = hstack([-A, csr_matrix(np.ones((r, 1)))]).tocsr()
    c = np.zeros(len(keys) + 1); c[-1] = -1.0
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(r), bounds=[(-1, 1)] * len(keys) + [(None, None)], method='highs')
    out = {'n_relations': len(rels), 'n_inequalities': r, 'lp_status': int(res.status)}
    if res.status != 0:
        out['status'] = 'LP-ERROR'; return out
    t_star = float(res.x[-1]); out['t_star'] = t_star
    if t_star > tol:
        out['status'] = 'FEASIBLE'; out['exact'] = False; return out
    y = -np.asarray(res.ineqlin.marginals)           # multipliers >= 0 for the <= rows
    sup = [i for i in range(r) if y[i] > 1e-9]
    out['support_rows'] = sup
    out['support'] = sorted(set(rel_of_row[i] for i in sup))
    bracket_set = set()
    for i in sup:
        dom, o1, o2 = rels[rel_of_row[i]]
        other = o1 if (i % 2 == 0) else o2
        bracket_set.update(dom); bracket_set.update(other)
    out['brackets'] = sorted(bracket_set)
    # exact check: rational multipliers, sum y_i A_i = 0 exactly and sum y_i > 0
    yr = [Fraction(float(y[i])).limit_denominator(10 ** 6) for i in sup]
    comb = {}
    for yi, i in zip(yr, sup):
        if yi <= 0:
            continue
        dom, o1, o2 = rels[rel_of_row[i]]
        other = o1 if (i % 2 == 0) else o2
        for k in dom:
            comb[k] = comb.get(k, 0) + yi
        for k in other:
            comb[k] = comb.get(k, 0) - yi
    out['exact'] = all(v == 0 for v in comb.values()) and sum(yr) > 0
    out['status'] = 'NONREALIZABLE-EXACT' if out['exact'] else 'NONREALIZABLE-NUMERICAL'
    return out


def cut_clause(C, chi, brackets):
    """Sound cut: at least one of these brackets must have a different sign (literal form for the OM-SAT CNF)."""
    return [(-C.qvar[S] if chi[S] > 0 else C.qvar[S]) for S in brackets]
