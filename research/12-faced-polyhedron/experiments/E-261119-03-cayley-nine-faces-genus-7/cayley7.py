"""Face-transitive cubic nine-face maps at genus 7 (valency 14), by two independent enumerations, and the plain
formula (10 elements) on every admissible class.

Reuses the slot parametrisation of E-261117-01 `cayley.py` (labellings, `by_phi`, `trimap`, census codes). Its
`brute` runs over all (k-1)! cyclic orders, 13! per labelling at k = 14, out of reach; `rho_dfs` enumerates the same
set (cyclic orders rho starting at slot 0 whose face permutation phi = rho o iota is triangular) depth first,
pruning a partial rho as soon as its partial phi violates a necessary triangle condition. It shares no code with
`by_phi`, which builds phi first. Its equality with `brute` is checked on the lower rungs (test_cayley7.py).
"""
from concurrent.futures import ProcessPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
N1 = ROOT / 'experiments/E-261117-01-cayley-census-9-4'
_spec = importlib.util.spec_from_file_location('cayley', N1 / 'cayley.py')
cayley = importlib.util.module_from_spec(_spec)
sys.modules['cayley'] = cayley
_spec.loader.exec_module(cayley)
census = cayley.census


def partial_ok(G, labels, phi, x):
    """Necessary conditions on the phi-orbit through x, given the slots assigned so far (None = unknown)."""
    y = phi[x]
    if y == x:
        return G.order[labels[x]] == 3
    if phi[y] is not None:
        z = phi[y]
        if z in (x, y):
            return False
        if G.mul[G.mul[labels[x]][labels[y]]][labels[z]] != G.e:
            return False
        if phi[z] is not None and phi[z] != x:
            return False
    return True


def rho_dfs(G, labels, iota):
    k = len(labels)
    rho = [None] * k
    phi = [None] * k
    used = [False] * k
    used[0] = True
    pre = [None] * k          # pre[v] = u with phi[u] = v

    def consistent(x):
        u = pre[x]
        w = pre[u] if u is not None else None
        return all(partial_ok(G, labels, phi, v) for v in (x, u, w) if v is not None)

    def extend(cur, depth):
        if depth == k - 1:
            rho[cur] = 0
            x = iota[cur]; phi[x] = 0; pre[0] = x
            if consistent(x) and cayley.triangular(G, labels, phi):
                yield tuple(rho)
            phi[x] = None; pre[0] = None; rho[cur] = None
            return
        for nxt in range(1, k):
            if used[nxt]:
                continue
            rho[cur] = nxt
            x = iota[cur]; phi[x] = nxt; pre[nxt] = x
            if consistent(x):
                used[nxt] = True
                yield from extend(nxt, depth + 1)
                used[nxt] = False
            phi[x] = None; pre[nxt] = None; rho[cur] = None

    yield from extend(0, 0)


METHODS = dict(brute=cayley.brute, by_phi=cayley.by_phi, rho_dfs=rho_dfs)


def job(args):
    F, genus, method, gi, w, W, canon_all = args
    G = cayley.GROUPS[F]()[gi]; k = cayley.valency(F, genus)
    s = dict(labellings=0, raw=0, valid=0, admissible=0)
    classes = {}
    for i, (labels, iota) in enumerate(cayley.labellings(G, k)):
        if i % W != w:
            continue
        s['labellings'] += 1
        for rho in METHODS[method](G, labels, iota):
            s['raw'] += 1
            M = cayley.trimap(G, labels, iota, rho)
            try:
                cayley.review.check(M, F, genus)
            except AssertionError:
                continue
            s['valid'] += 1
            ok = census.admissible(M); s['admissible'] += ok
            if not (ok or canon_all):
                continue
            code = M.canon()[0]
            if code not in classes:
                classes[code] = dict(admissible=ok, witness=dict(
                    group=G.name, labels=[list(G.el[a]) if isinstance(G.el[a], tuple) else G.el[a] for a in labels],
                    iota=list(iota), rho=list(rho)))
    return G.name, s, classes


def run(F, genus, method, workers=1, canon_all=True):
    """As cayley.run, with the method table above; canon_all=False classifies only the admissible maps (the
    canonical code costs ~11 ms per map at valency 14)."""
    k = cayley.valency(F, genus)
    stats = dict(F=F, genus=genus, valency=k, method=method, workers=workers, groups={},
                 classes_of='all valid maps' if canon_all else 'admissible maps only')
    started = time.monotonic()
    names = [G.name for G in cayley.GROUPS[F]()] if k else []
    jobs = [(F, genus, method, gi, w, workers, canon_all) for gi in range(len(names)) for w in range(workers)]
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


def stage_a(out, workers):
    """Rung: rho_dfs against the saved brute counts and classes of E-261117-01 at (8, 3) and (9, 4); then both
    enumerations at (9, 7). Kill on any disagreement."""
    out.mkdir(parents=True, exist_ok=False)
    report = dict(rung={}, stages={})
    saved = json.loads((N1 / 'results/census/census.json').read_text())
    for F, genus in ((8, 3), (9, 4)):
        stats, maps = run(F, genus, 'rho_dfs', workers)
        old = json.loads((N1 / f'results/census/maps_{F}_{genus}.json').read_text())['maps']
        brute = saved['stages'][f'{F}_{genus}']['brute']['groups']
        agree = [m['code'] for m in maps] == [m['code'] for m in old] and all(
            stats['groups'][g]['raw'] == brute[g]['raw'] for g in brute)
        report['rung'][f'{F}_{genus}'] = dict(rho_dfs=stats, agrees_with_saved_brute=agree)
        if not agree:
            report['KILL'] = f'({F}, {genus}): rho_dfs disagrees with the saved brute run'
    if 'KILL' not in report:
        runs = {m: run(9, 7, m, workers, canon_all=False) for m in ('by_phi', 'rho_dfs')}
        (a_stats, a_maps), (b_stats, b_maps) = runs['by_phi'], runs['rho_dfs']
        agree = [m['code'] for m in a_maps] == [m['code'] for m in b_maps] and all(
            a_stats['groups'][g][c] == b_stats['groups'][g][c] for g in a_stats['groups']
            for c in ('raw', 'valid', 'admissible'))
        report['stages']['9_7'] = dict(by_phi=a_stats, rho_dfs=b_stats, methods_agree=agree)
        (out / 'maps_9_7.json').write_text(json.dumps(dict(stats=a_stats, maps=a_maps), separators=(',', ':')) + '\n')
        if not agree:
            report['KILL'] = '(9, 7): the two enumerations disagree'
    report['PASS'] = 'KILL' not in report
    (out / 'census.json').write_text(json.dumps(report, indent=1) + '\n')
    return report


def stage_b(out, cap):
    """Plain formula (10 elements) on every admissible (9, 7) class, after a per-map pinned GP calibration."""
    os.environ.setdefault('NO_PROOF', '1')
    sys.path.insert(0, str(N1))
    import formulas
    from formulas import pilot
    assert pilot.NO_PROOF, 'no proofs in this experiment (PLAN.md)'
    maps = [m for m in json.loads((out.parent / 'census/maps_9_7.json').read_text())['maps'] if m['admissible']]
    out.mkdir(parents=True, exist_ok=False)
    import random
    rng = random.Random(261119)
    with (out / 'results.jsonl').open('a') as log:
        for i, m in enumerate(maps):
            while True:
                chi = pilot.chirotope_from_planes([[rng.randint(-100, 100) for _ in range(4)] for _ in range(9)])
                if all(chi.values()):
                    break
            c = pilot.CNF(9); c.defs_only = True; pilot.build(c, pilot.from_links(m['links']), pilot.ALL_OPTS); c.gp()
            ctl = pilot.solve(formulas.pinned(c, chi), out, f'map{i}_gp_control', cap)
            r = pilot.solve(formulas.formula(m['links'], None), out, f'map{i}_plain', cap)
            r.update(unit=f'map{i}_plain', map=i, scope='plain formula, 10 elements', cap_seconds=cap,
                     gp_control=ctl['status'],
                     map_code_sha256=hashlib.sha256(json.dumps(m['code']).encode()).hexdigest())
            log.write(json.dumps(r) + '\n'); log.flush()
            print(r['unit'], r['status'], 'control', ctl['status'], round(r['seconds'], 1), flush=True)
            if ctl['status'] != 'SAT':
                raise RuntimeError(f'map {i}: the pinned GP control is {ctl["status"]}, not SAT')


if __name__ == '__main__':
    if sys.argv[1] == 'stage_a':
        rep = stage_a(Path(sys.argv[2]), int(sys.argv[3]))
        print(json.dumps({k: v for k, v in rep.items() if k not in ('stages', 'rung')}))
        sys.exit(0 if rep['PASS'] else 1)
    if sys.argv[1] == 'stage_b':
        stage_b(Path(sys.argv[2]), float(sys.argv[3]))
