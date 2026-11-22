"""E-261116-09 part B, the lemma attempt (PLAN.md reading): the linear families are inconsistent over GF(2).

SEGMENT_DISJOINT, SYM, SB_ORBFLIP and SB_MIRROR clauses are linear in the chirotope bits: a SEGMENT_DISJOINT clause is
the unit NOT segment(X, W, A, C, V) = NOT (sd(XWA, V) xor sd(XWC, V)), each sd an xor of two chirotope bits (omsat
Predicates.sd); a SYM pair [p, q], [-p, -q] says p xor q = 1; an SB clause is a unit chirotope literal. The Tseitin xor
variables are expanded back to chirotope bits (CNF._xor), so each family set gives a linear system over GF(2), solved
exactly by Gaussian elimination: no SAT solver. An inconsistent system comes with a certificate (equations whose sum is
0 = 1), re-checked independently and shrunk to an irredundant one by deletion. The formula is built by ablate.build
(tranche.submap_formula, the stage-B builder, hash-checked against stage B).
Usage: python3 parity.py OUT_JSON"""
import json
import sys

import ablate as A

SETS = {'SEG': ('SEGMENT_DISJOINT',), 'SEG+SYM': ('SEGMENT_DISJOINT', 'SYM'),
        'SEG+SYM+gauge': ('SEGMENT_DISJOINT', 'SYM', 'SB_ORBFLIP', 'SB_MIRROR'), 'SYM+gauge': ('SYM', 'SB_ORBFLIP', 'SB_MIRROR')}


def expander(c):
    base = set(c.qvar.values())
    rev = {z: k for k, z in c._xor.items() if len(k) == 2}
    memo = {}
    def bits(v):
        if v in memo:
            return memo[v]
        if v in base:
            r = 1 << v
        elif v in rev:
            r = bits(rev[v][0]) ^ bits(rev[v][1])
        else:
            raise ValueError(f'variable {v} is not an xor of chirotope bits')
        memo[v] = r
        return r
    def lit(l):  # (bitmask, constant): the literal's value is xor(bits) + constant
        return bits(abs(l)), int(l < 0)
    return lit


def equations(c, tags, fams):
    lit = expander(c); eqs = []; label = []
    idx = [i for i, t in enumerate(tags) if t in fams]
    k = 0
    while k < len(idx):
        i = idx[k]; cl = c.clauses[i]; t = tags[i]
        if len(cl) == 1:
            m, s = lit(cl[0]); eqs.append((m, 1 ^ s)); label.append((t, i)); k += 1
        else:
            nxt = c.clauses[idx[k + 1]]
            assert t == tags[idx[k + 1]] and len(cl) == 2 and sorted(nxt) == sorted(-x for x in cl), (t, cl, nxt)
            (m1, s1), (m2, s2) = lit(cl[0]), lit(cl[1])
            eqs.append((m1 ^ m2, 1 ^ s1 ^ s2)); label.append((t, i)); k += 2
    return eqs, label


def inconsistent(eqs):
    """Gaussian elimination; returns a set of equation indices summing to 0 = 1, or None."""
    piv = {}  # pivot bit -> (mask, rhs, combo)
    for j, (m, r) in enumerate(eqs):
        combo = 1 << j
        while m:
            h = m.bit_length() - 1
            if h not in piv:
                piv[h] = (m, r, combo)
                break
            pm, pr, pc = piv[h]; m ^= pm; r ^= pr; combo ^= pc
        else:
            if r:
                return {i for i in range(len(eqs)) if combo >> i & 1}
    return None


def check(eqs, cert):
    m = r = 0
    for i in cert:
        m ^= eqs[i][0]; r ^= eqs[i][1]
    return m == 0 and r == 1


def shrink(eqs, cert):
    cert = sorted(cert)
    for i in list(cert):
        rest = [j for j in cert if j != i]
        sub = inconsistent([eqs[j] for j in rest])
        if sub is not None:
            cert = [rest[j] for j in sub]
    return sorted(cert)


def main(path):
    out = []
    for arm, maps, _ in A.SOURCES:
        recs = json.loads((A.CENSUS / maps).read_text())['maps']
        for i, rec in enumerate(recs):
            c, tags, digest, links = A.build(rec)
            row = dict(arm=arm, index=i, config=rec['config'], stratum=rec['stratum'][0], formula_sha256=digest)
            for name, fams in SETS.items():
                eqs, label = equations(c, tags, set(fams))
                cert = inconsistent(eqs)
                if cert is None:
                    row[name] = dict(equations=len(eqs), consistent=True)
                    continue
                assert check(eqs, cert)
                small = shrink(eqs, cert); assert check(eqs, small)
                row[name] = dict(equations=len(eqs), consistent=False, certificate=len(small),
                                 families=sorted({label[j][0] for j in small}),
                                 certificate_clauses=[label[j][1] for j in small])
            out.append(row)
    json.dump(out, open(path, 'w'), indent=None, separators=(',', ':'))
    from collections import Counter
    print(Counter((r['arm'], r['config'], *(r[n]['consistent'] for n in SETS)) for r in out))


if __name__ == '__main__':
    main(sys.argv[1])
