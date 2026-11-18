"""Cayley census: triangular maps on which a group G acts regularly on the vertices, every vertex pair adjacent.

A vertex-regular orientation-preserving action identifies the vertices with G and the darts with G x slots. The data
at the identity are a slot label s (slot -> G minus e), a slot involution iota with s(iota x) = s(x)^-1, and a
rotation rho (one k-cycle on the slots). Dart (g, x) runs from g to g s(x); its reverse is (g s(x), iota x); the
face successor is (g s(x), rho(iota x)). With phi = rho o iota a slot orbit of length L whose label product has
order m traces faces of length L m, so all faces are triangles iff every phi-cycle is a fixed point with a label of
order 3 or a 3-cycle with product e.

Two independent enumerations of the valid rotations: `brute` runs over all (k-1)! cyclic orders (the raw count);
`by_phi` builds phi from 3-cycles and fixed points and keeps rho = phi o iota when it is one k-cycle.
Dual vertices are the faces of the polyhedron; (F, g) below is the polyhedron's face count and genus.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('census', ROOT / 'experiments/E-261103-01-s5-map-census/census.py')
census = importlib.util.module_from_spec(spec)
spec.loader.exec_module(census)
review = census.review


class Group:
    def __init__(self, name, elements, mul):
        self.name = name
        self.el = list(elements)
        idx = {e: i for i, e in enumerate(self.el)}
        self.n = len(self.el)
        self.mul = [[idx[mul(a, b)] for b in self.el] for a in self.el]
        self.e = next(i for i in range(self.n) if all(self.mul[i][j] == j for j in range(self.n)))
        self.inv = [next(j for j in range(self.n) if self.mul[i][j] == self.e) for i in range(self.n)]
        assert all(self.mul[self.mul[a][b]][c] == self.mul[a][self.mul[b][c]]
                   for a in range(self.n) for b in range(self.n) for c in range(self.n)), name
        self.order = []
        for a in range(self.n):
            k, p = 1, a
            while p != self.e:
                p = self.mul[p][a]; k += 1
            self.order.append(k)

    def spectrum(self):
        return tuple(sorted(self.order))


def abelian(*mods):
    return Group('x'.join(f'Z{m}' for m in mods), itertools.product(*(range(m) for m in mods)),
                 lambda a, b: tuple((x + y) % m for x, y, m in zip(a, b, mods)))


def dihedral(m):
    return Group(f'D{m}', itertools.product(range(m), range(2)),
                 lambda a, b: ((a[0] + (-1) ** a[1] * b[0]) % m, (a[1] + b[1]) % 2))


def quaternion():
    # (sign, unit), unit 0..3 = 1, i, j, k
    table = {(0, 0): (1, 0), (0, 1): (1, 1), (0, 2): (1, 2), (0, 3): (1, 3), (1, 0): (1, 1), (2, 0): (1, 2),
             (3, 0): (1, 3), (1, 1): (-1, 0), (2, 2): (-1, 0), (3, 3): (-1, 0), (1, 2): (1, 3), (2, 3): (1, 1),
             (3, 1): (1, 2), (2, 1): (-1, 3), (3, 2): (-1, 1), (1, 3): (-1, 2)}
    def mul(a, b):
        s, u = table[a[1], b[1]]
        return (a[0] * b[0] * s, u)
    return Group('Q8', itertools.product((1, -1), range(4)), mul)


def dicyclic3():
    # Dic3 = <a, x | a^6, x^2 = a^3, x a x^-1 = a^-1>, elements a^i x^j
    def mul(p, q):
        (i, j), (k, l) = p, q
        if j == 0:
            return ((i + k) % 6, l)
        return ((i - k + 3 * l) % 6, (1 + l) % 2)
    return Group('Dic3', itertools.product(range(6), range(2)), mul)


def alternating4():
    perms = [p for p in itertools.permutations(range(4))
             if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0]
    return Group('A4', perms, lambda a, b: tuple(a[b[i]] for i in range(4)))


GROUPS = {
    7: lambda: [abelian(7)],
    8: lambda: [abelian(8), abelian(4, 2), abelian(2, 2, 2), dihedral(4), quaternion()],
    9: lambda: [abelian(9), abelian(3, 3)],
    12: lambda: [abelian(12), abelian(6, 2), dihedral(6), dicyclic3(), alternating4()],
}


def valency(F, genus):
    """Dual degree of a vertex-transitive (F, genus) map: F - E + 2E/3 = 2 - 2g, k = 2E / F."""
    E = 3 * (F - 2 + 2 * genus)
    return 2 * E // F if (2 * E) % F == 0 else None


def labellings(G, k):
    """Every slot labelling (sorted label list) and every compatible slot involution iota."""
    others = [a for a in range(G.n) if a != G.e]
    for extra in itertools.combinations_with_replacement(others, k - len(others)):
        labels = sorted(others + list(extra))
        count = {a: labels.count(a) for a in others}
        if any(count[a] != count[G.inv[a]] for a in others):
            continue
        slots = {a: [x for x in range(k) if labels[x] == a] for a in others}
        choices = []
        for a in others:
            b = G.inv[a]
            if a < b:
                choices.append([list(zip(slots[a], p)) for p in itertools.permutations(slots[b])])
            elif a == b:
                choices.append(list(involutions(slots[a])))
        for parts in itertools.product(*choices):
            iota = [None] * k
            for pairs in parts:
                for x, y in pairs:
                    iota[x] = y; iota[y] = x
            assert all(labels[iota[x]] == G.inv[labels[x]] for x in range(k))
            yield labels, tuple(iota)


def involutions(items):
    if not items:
        yield []
        return
    a, rest = items[0], items[1:]
    for pairs in involutions(rest):
        yield [(a, a)] + pairs
    for i, b in enumerate(rest):
        for pairs in involutions(rest[:i] + rest[i + 1:]):
            yield [(a, b)] + pairs


def triangular(G, labels, phi):
    for x in range(len(phi)):
        y = phi[x]
        if y == x:
            if G.order[labels[x]] != 3:
                return False
        elif phi[phi[y]] != x or G.mul[G.mul[labels[x]][labels[y]]][labels[phi[y]]] != G.e:
            return False
    return True


def brute(G, labels, iota):
    k = len(labels)
    for tail in itertools.permutations(range(1, k)):
        cyc = (0,) + tail
        rho = [0] * k
        for i in range(k):
            rho[cyc[i]] = cyc[(i + 1) % k]
        phi = [rho[iota[x]] for x in range(k)]
        if triangular(G, labels, phi):
            yield tuple(rho)


def by_phi(G, labels, iota):
    k = len(labels)
    def grow(phi):
        free = [x for x in range(k) if phi[x] is None]
        if not free:
            yield list(phi)
            return
        x = free[0]
        if G.order[labels[x]] == 3:
            phi[x] = x
            yield from grow(phi)
            phi[x] = None
        for y, z in itertools.permutations(free[1:], 2):
            if G.mul[G.mul[labels[x]][labels[y]]][labels[z]] == G.e:
                phi[x], phi[y], phi[z] = y, z, x
                yield from grow(phi)
                phi[x] = phi[y] = phi[z] = None
    for phi in grow([None] * k):
        rho = [phi[iota[y]] for y in range(k)]    # rho = phi o iota, iota an involution
        x, n = rho[0], 1
        while x != 0:
            x = rho[x]; n += 1
        if n == k:
            yield tuple(rho)


def trimap(G, labels, iota, rho):
    k = len(labels)
    dart = lambda g, x: g * k + x
    alpha = {dart(g, x): dart(G.mul[g][labels[x]], iota[x]) for g in range(G.n) for x in range(k)}
    tri, seen = [], set()
    for d in range(G.n * k):
        if d in seen:
            continue
        t, e = [], d
        while e not in seen:
            seen.add(e); t.append(e)
            g, x = divmod(e, k)
            e = dart(G.mul[g][labels[x]], rho[iota[x]])
        assert len(t) == 3 and e == d, 'non-triangular face'
        tri.append(t)
    return review.TriMap(tri, alpha, [d // k for d in range(G.n * k)])


def job(args):
    """One worker's share: labellings w, w + W, ... of group gi."""
    F, genus, method, gi, w, W = args
    G = GROUPS[F]()[gi]; k = valency(F, genus)
    s = dict(labellings=0, raw=0, valid=0, admissible=0)
    classes = {}
    for i, (labels, iota) in enumerate(labellings(G, k)):
        if i % W != w:
            continue
        s['labellings'] += 1
        for rho in (brute if method == 'brute' else by_phi)(G, labels, iota):
            s['raw'] += 1
            M = trimap(G, labels, iota, rho)
            try:
                review.check(M, F, genus)
            except AssertionError:
                continue
            s['valid'] += 1
            ok = census.admissible(M); s['admissible'] += ok
            code = M.canon()[0]
            if code not in classes:
                classes[code] = dict(admissible=ok, witness=dict(
                    group=G.name, labels=[list(G.el[a]) if isinstance(G.el[a], tuple) else G.el[a] for a in labels],
                    iota=list(iota), rho=list(rho)))
    return G.name, s, classes


def run(F, genus, method, workers=1):
    k = valency(F, genus)
    stats = dict(F=F, genus=genus, valency=k, method=method, workers=workers, groups={})
    started = time.monotonic()
    names = [G.name for G in GROUPS[F]()] if k else []
    jobs = [(F, genus, method, gi, w, workers) for gi in range(len(names)) for w in range(workers)]
    with ProcessPoolExecutor(workers) as pool:
        results = list(pool.map(job, jobs)) if jobs else []
    classes = {}
    for name in names:
        s = dict(labellings=0, raw=0, valid=0, admissible=0)
        for gname, part, found in results:
            if gname != name:
                continue
            for key in s:
                s[key] += part[key]
            for code, c in found.items():
                classes.setdefault(code, dict(admissible=c['admissible'], groups=set(), witness=c['witness']))
                classes[code]['groups'].add(name)
        if method == 'brute':
            s['rotations_tried'] = s['labellings'] * math.factorial(k - 1)
        s['distinct_valid'] = sum(name in c['groups'] for c in classes.values())
        s['distinct_admissible'] = sum(name in c['groups'] and c['admissible'] for c in classes.values())
        stats['groups'][name] = s
    stats['seconds'] = time.monotonic() - started
    stats['core_seconds_bound'] = stats['seconds'] * workers
    maps = []
    for code in sorted(classes, key=lambda c: (not classes[c]['admissible'], c)):
        rec = census.record([list(p) for p in code], F, genus)
        assert rec['admissible'] == classes[code]['admissible']
        assert rec['aut_plus'] % F == 0, 'a vertex-regular group must divide Aut+'
        rec.update(cayley_groups=sorted(classes[code]['groups']), witness=classes[code]['witness'])
        maps.append(rec)
    stats['distinct_valid'] = len(maps)
    stats['distinct_admissible'] = sum(m['admissible'] for m in maps)
    return stats, maps


def roest_vigh_code():
    sys.path.insert(0, str(ROOT / 'code'))
    from control_rost_vigh import build
    _, links = build()
    links = [links[i] for i in range(len(links))]
    M = census.from_links(links)
    review.check(M, 8, 3)
    return M.canon()[0]


def stage_a(out, workers):
    """Both enumerations at (8, 3) and (9, 4); kill if they disagree or Roest-Vigh's map is missing."""
    out.mkdir(parents=True, exist_ok=False)
    report = dict(stages={})
    for F, genus in ((8, 3), (9, 4)):
        runs = {m: run(F, genus, m, workers) for m in ('brute', 'by_phi')}
        (b_stats, b_maps), (p_stats, p_maps) = runs['brute'], runs['by_phi']
        agree = [m['code'] for m in b_maps] == [m['code'] for m in p_maps] and all(
            b_stats['groups'][g]['raw'] == p_stats['groups'][g]['raw'] for g in b_stats['groups'])
        report['stages'][f'{F}_{genus}'] = dict(brute=b_stats, by_phi=p_stats, methods_agree=agree)
        (out / f'maps_{F}_{genus}.json').write_text(json.dumps(dict(stats=b_stats, maps=b_maps), separators=(',', ':')) + '\n')
        if not agree:
            report['KILL'] = f'({F}, {genus}): the two enumerations disagree'
            break
        if F == 8:
            rv = [list(p) for p in roest_vigh_code()]
            hit = [i for i, m in enumerate(b_maps) if m['code'] == rv]
            report['roest_vigh'] = dict(found=bool(hit), index=hit)
            if not hit:
                report['KILL'] = "Roest-Vigh's map missing at order 8"
                break
    report['PASS'] = 'KILL' not in report
    (out / 'census.json').write_text(json.dumps(report, indent=1) + '\n')
    return report


def main():
    if sys.argv[1:2] == ['stage_a']:
        report = stage_a(Path(sys.argv[2]), int(sys.argv[3]))
        print(json.dumps({k: v for k, v in report.items() if k != 'stages'}))
        sys.exit(0 if report['PASS'] else 1)
    ap = argparse.ArgumentParser()
    ap.add_argument('F', type=int)
    ap.add_argument('genus', type=int)
    ap.add_argument('--method', choices=('brute', 'by_phi'), default='by_phi')
    ap.add_argument('--workers', type=int, default=1)
    ap.add_argument('--out', type=Path)
    a = ap.parse_args()
    stats, maps = run(a.F, a.genus, a.method, a.workers)
    print(json.dumps(stats, indent=1))
    if a.out:
        a.out.write_text(json.dumps(dict(stats=stats, maps=maps), separators=(',', ':')) + '\n')


if __name__ == '__main__':
    main()
