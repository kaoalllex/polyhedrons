"""Lead review 2026-11-23, check K2: the plain generator-free formula at 9 elements (tranche.submap_formula, the
E-261117-04 stage-A formula) on a random sample of K1's admissible (8, 3) classes with trivial Aut+ that are not
equivelar, in the code's orientation, kissat cap in seconds; prices the full (8, 3) pass. A session check, not ledger
evidence. Usage: ~/.venvs/polyhedra/bin/python -I k2_plain_sample_8_3.py <research root> <K1 maps json> <n> <cap s> <scratch>"""
import json
import multiprocessing as mp
import random
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1]); MAPS = Path(sys.argv[2]); N = int(sys.argv[3]); CAP = int(sys.argv[4]); OUT = Path(sys.argv[5])
E2 = ROOT / 'experiments/E-261119-02-symmetric-nine-face-census'
sys.path.insert(0, str(E2))
import controls_b  # noqa: E402,F401  (sys.path for tranche / pilot / omsat)
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
import tranche  # noqa: E402
KISSAT = str(Path.home() / 'bin/kissat')


def degree_sequence(rec):
    deg = Counter()
    for a, b, m in rec['extra_edges']:
        deg[a] += m - 1; deg[b] += m - 1
    return ''.join(map(str, sorted((deg[v] for v in range(8)), reverse=True)))


def solve(job):
    tag, links = job
    t0 = time.monotonic()
    c = tranche.submap_formula(8, dict(enumerate(links)))
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
    return dict(tag=tag, status={10: 'SAT', 20: 'UNSAT-SOLVER'}.get(rc, 'UNKNOWN'), build_s=round(tb, 2),
                solve_s=round(ts, 2))


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    pool_maps = [m for m in json.loads(MAPS.read_text()) if m['admissible'] and m['aut_plus'] == 1
                 and not all(x == 2 for x in m['extra_pattern'])]
    sample = random.Random(2611230201).sample(pool_maps, N)
    jobs = [('%s %d' % (degree_sequence(m), i), m['links']) for i, m in enumerate(sample)]
    t = time.monotonic()
    with mp.Pool(8) as pool:
        res = pool.map(solve, jobs)
    for r in res:
        print(json.dumps(r))
    st = Counter(r['status'] for r in res)
    solve_s = sorted(r['solve_s'] for r in res); build_s = [r['build_s'] for r in res]
    print(json.dumps(dict(pool=len(pool_maps), n=N, cap_s=CAP, statuses=st, wall_s=round(time.monotonic() - t, 1),
                          solve_mean=round(sum(solve_s) / N, 3), solve_median=solve_s[N // 2], solve_max=solve_s[-1],
                          build_mean=round(sum(build_s) / N, 3))))
