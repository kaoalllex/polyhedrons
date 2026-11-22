"""Final lead review 2026-11-22, check K2: generator-free plain formula (tranche.submap_formula without generator, E-261103-03 path) on equivelar
(9, 4) maps of pass 1: the lowest canonical hash per extra-edge cycle pattern, plus the two priced equivelar records.
Usage: ~/.venvs/polyhedra/bin/python -I k2_plain_equivelar_9_4.py <research root> <cap seconds> <scratch dir>"""
import json
import multiprocessing as mp
import os
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1]); CAP = int(sys.argv[2]); OUT = Path(sys.argv[3])
E2 = ROOT / 'experiments/E-261119-02-symmetric-nine-face-census'
sys.path.insert(0, str(E2))
import controls_b  # noqa: E402,F401  (sys.path for tranche / pilot / omsat)
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
import tranche  # noqa: E402
KISSAT = str(Path.home() / 'bin/kissat')


def pattern(links):
    extra = Counter()
    for v, l in enumerate(links):
        for w, m in Counter(l).items():
            if v < w and m > 1:
                extra[(v, w)] = m - 1
    adj = defaultdict(list)
    for (v, w), m in extra.items():
        adj[v] += [w] * m; adj[w] += [v] * m
    seen, sizes = set(), []
    for v in range(len(links)):
        if v in seen:
            continue
        st, comp = [v], set()
        while st:
            x = st.pop()
            if x in comp:
                continue
            comp.add(x); st += adj[x]
        seen |= comp; sizes.append(len(comp))
    return '+'.join(map(str, sorted(sizes, reverse=True)))


def solve(job):
    tag, links = job
    t0 = time.monotonic()
    c = tranche.submap_formula(9, dict(enumerate(links)))
    tb = time.monotonic() - t0
    with tempfile.NamedTemporaryFile('w', suffix='.cnf', dir=OUT, delete=True) as f:
        f.write(f'p cnf {c.nv} {len(c.clauses)}\n'); f.write(''.join(' '.join(map(str, cl)) + ' 0\n' for cl in c.clauses)); f.flush()
        t1 = time.monotonic()
        try:
            rc = subprocess.run([KISSAT, '-q', '-n', f'--time={CAP}', f.name], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, timeout=CAP + 10).returncode
        except subprocess.TimeoutExpired:
            rc = 0
        ts = time.monotonic() - t1
    return dict(tag=tag, status={10: 'SAT', 20: 'UNSAT-SOLVER'}.get(rc, 'UNKNOWN'), build_s=round(tb, 1),
                solve_s=round(ts, 1), nv=c.nv, ncl=len(c.clauses))


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    recs = json.loads((E2 / 'maps/pass1.json').read_text())['maps']
    eq = {}
    for r in recs:
        if all(len(l) == 10 for l in r['links']):
            eq.setdefault(r['canonical_sha256'], r)
    by = defaultdict(list)
    for h, r in eq.items():
        by[pattern(r['links'])].append(h)
    print('equivelar codes', len(eq), {p: len(v) for p, v in sorted(by.items())}, flush=True)
    jobs = [('%s %s' % (p, min(v)[:12]), eq[min(v)]['links']) for p, v in sorted(by.items())]
    pr = json.loads((E2 / 'maps/pricing.json').read_text())['maps']
    for i, r in enumerate(pr):
        if all(len(l) == 10 for l in r['links']):
            jobs.append(('pricing[%d] %s %s' % (i, pattern(r['links']), r['canonical_sha256'][:12]), r['links']))
    with mp.Pool(8) as pool:
        for res in pool.imap_unordered(solve, jobs):
            print(json.dumps(res), flush=True)
