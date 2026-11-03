"""Independent checker of biquadratic final-polynomial certificates (standard library only, exact arithmetic).

A certificate claims: no configuration of vectors in R^4 in general position has the listed bracket signs. Each row is
a 3-term Grassmann-Pluecker relation, given as three pairs of sorted 4-subsets (the claimed dominant pair first), a
flag selecting one of the two other pairs, and a positive rational multiplier y. The checker re-derives everything
from the relation itself, without the code that produced it:
  1. the three pairs are the three pairings tau+{a,b}|tau+{c,d}, tau+{a,c}|tau+{b,d}, tau+{a,d}|tau+{b,c} of one
     relation [tab][tcd] - [tac][tbd] + [tad][tbc] = 0 (t = tau sorted, a < b < c < d);
  2. with the listed signs, exactly one term has the sign opposite to the other two, and it is the claimed dominant
     pair (then in any realization |dominant| = |o1| + |o2| > |o_i|, so log|dominant| - log|other| > 0);
  3. sum_i y_i (log|dominant_i| - log|other_i|) is identically zero as a linear form in the log|bracket| values,
     with every y_i > 0: a positive combination of strict inequalities equal to 0 > 0, so no realization exists.

Usage: python3 -I verify.py certificates.json        PASS / FAIL per certificate, exit 1 on any FAIL
       python3 -I verify.py certificates.json --selftest   also the controls (GP identity, mutations, realizable signs)
"""
import itertools
import json
import random
import sys
from fractions import Fraction


def parity(seq):
    p = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            p ^= seq[i] > seq[j]
    return p


def osign(signs, tup):
    """Sign of the ordered bracket tup from the sign of its sorted key."""
    v = signs[tuple(sorted(tup))]
    return -v if parity(tup) else v


def check(cert):
    """Returns (ok, reason)."""
    signs = {tuple(int(x) for x in k.split(',')): int(v) for k, v in cert['signs'].items()}
    if any(v not in (1, -1) for v in signs.values()):
        return False, 'a bracket sign is not +1 / -1'
    form = {}
    if not cert['rows']:
        return False, 'no rows'
    for rel, flag, y in cert['rows']:
        y = Fraction(y)
        if y <= 0:
            return False, 'multiplier %s not positive' % y
        pairs = [frozenset(tuple(S) for S in pair) for pair in rel]
        brackets = [tuple(S) for pair in rel for S in pair]
        if len(pairs) != 3 or any(len(p) != 2 for p in pairs) or any(len(set(S)) != 4 or list(S) != sorted(S) for S in brackets):
            return False, 'malformed relation %s' % rel
        tau = set(brackets[0])
        for S in brackets:
            tau &= set(S)
        if len(tau) != 2:
            return False, 'no common pair tau in %s' % rel
        t = tuple(sorted(tau))
        rest = sorted(set().union(*map(set, brackets)) - tau)
        if len(rest) != 4:
            return False, 'relation does not span 6 elements: %s' % rel
        a, b, c, d = rest
        terms = [((a, b), (c, d), 1), ((a, c), (b, d), -1), ((a, d), (b, c), 1)]
        key = lambda xy: tuple(sorted(t + xy))
        want = [frozenset((key(p), key(q))) for p, q, _ in terms]
        if sorted(map(sorted, want)) != sorted(map(sorted, pairs)):
            return False, 'pairs are not the three pairings of tau %s and %s' % (t, rest)
        tsign = []
        for p, q, coef in terms:
            if key(p) not in signs or key(q) not in signs:
                return False, 'sign missing for a bracket of %s' % rel
            tsign.append(coef * osign(signs, t + p) * osign(signs, t + q))
        odd = [i for i in range(3) if tsign.count(tsign[i]) == 1]
        if len(odd) != 1:
            return False, 'signs of %s violate the GP axiom (all three terms of one sign)' % rel
        if want[odd[0]] != pairs[0]:
            return False, 'claimed dominant pair of %s is not the term of opposite sign' % rel
        if flag not in (0, 1):
            return False, 'bad flag %r' % flag
        other = pairs[1 + flag]
        for S in pairs[0]:
            form[S] = form.get(S, 0) + y
        for S in other:
            form[S] = form.get(S, 0) - y
    if any(v != 0 for v in form.values()):
        return False, 'the combination is not identically zero (%d nonzero coefficients)' % sum(1 for v in form.values() if v)
    return True, '%d rows, %d brackets' % (len(cert['rows']), len(signs))


def det4(M):
    return sum((-1) ** parity(p) * M[0][p[0]] * M[1][p[1]] * M[2][p[2]] * M[3][p[3]] for p in itertools.permutations(range(4)))


def selftest(certs):
    rng = random.Random(0)
    fails = []
    for _ in range(200):                                       # the 3-term GP identity with this sign convention
        V = [[rng.randint(-9, 9) for _ in range(4)] for _ in range(6)]
        br = lambda *ix: det4([V[i] for i in ix])
        if br(0, 1, 2, 3) * br(0, 1, 4, 5) - br(0, 1, 2, 4) * br(0, 1, 3, 5) + br(0, 1, 2, 5) * br(0, 1, 3, 4) != 0:
            fails.append('GP identity')
            break
    for e in certs:
        c = e['certificate']
        m = json.loads(json.dumps(c)); m['rows'][0][2] = str(Fraction(m['rows'][0][2]) * 2)
        if check(m)[0]:
            fails.append('%s: doubled multiplier accepted' % e['id'])
        for k in list(c['signs'])[:5]:
            m = json.loads(json.dumps(c)); m['signs'][k] = -m['signs'][k]
            if check(m)[0]:
                fails.append('%s: flipped sign %s accepted' % (e['id'], k))
        for trial in range(20):                                # realizable signs must never pass
            V = [[rng.randint(-50, 50) for _ in range(4)] for _ in range(13)]
            m = json.loads(json.dumps(c))
            for k in m['signs']:
                d = det4([V[int(i)] for i in k.split(',')])
                m['signs'][k] = 1 if d > 0 else -1 if d < 0 else 0
            if all(v != 0 for v in m['signs'].values()) and check(m)[0]:
                fails.append('%s: signs of a realization accepted' % e['id'])
    return fails


def main():
    certs = json.load(open(sys.argv[1]))
    bad = 0
    for e in certs:
        ok, why = check(e['certificate'])
        link = e.get('cnf_rebuilt_matches') and e.get('signs_match_model')
        print('%s type %d k %d: %s (%s); linkage to the SAT model (recorded, made with the encoder): %s'
              % (e['id'], e['type'], e['k'], 'PASS' if ok else 'FAIL', why, 'yes' if link else 'NO'))
        bad += not (ok and link)
    if '--selftest' in sys.argv:
        f = selftest(certs)
        print('selftest: %s' % ('PASS (GP identity, mutated certificates rejected, realizable signs rejected)' if not f else 'FAIL ' + '; '.join(f)))
        bad += bool(f)
    print('ALL PASS' if not bad else '%d FAIL' % bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
