"""Session check of lead review 2026-11-18 §5 N1: orbits of a plane permutation group on the chirotope quadruples
(F planes plus the plane at infinity, which every affine symmetry fixes). Usage: python3 strategy-review-2026-11-18-orbits.py"""
import itertools


def orbits(F, gens):
    inf, seen, count, fixed = F, set(), 0, 0
    for S in itertools.combinations(range(F + 1), 4):
        if S in seen:
            continue
        orb, todo = {S}, [S]
        while todo:
            T = todo.pop()
            for g in gens:
                U = tuple(sorted(g[e] if e != inf else inf for e in T))
                if U not in orb:
                    orb.add(U)
                    todo.append(U)
        seen |= orb
        count += 1
        fixed += len(orb) == 1
    return count, fixed


print('C3 3+3+3, nine planes:', orbits(9, [[1, 2, 0, 4, 5, 3, 7, 8, 6]]), 'of 210')
print('D2 2 x 4, eight planes:', orbits(8, [[1, 0, 3, 2, 5, 4, 7, 6], [2, 3, 0, 1, 6, 7, 4, 5]]), 'of 126')
print('S4 2 x 4, eight planes:', orbits(8, [[1, 2, 3, 0, 5, 6, 7, 4]]), 'of 126')
print('Cs 4 x 2 + 1, nine planes:', orbits(9, [[1, 0, 3, 2, 5, 4, 7, 6, 8]]), 'of 210')
print('no symmetry, seven planes:', orbits(7, []), 'of 70')
