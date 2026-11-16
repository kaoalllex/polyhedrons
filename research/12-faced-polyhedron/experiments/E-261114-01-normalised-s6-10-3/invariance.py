"""Exact clause-family invariance gate; ten independent deterministic shards, no target solving."""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder'))
from omsat import Eval, Triangulation, build, chirotope_from_planes
from omsat_validate import ALL_OPTS
from test_encoder import controls


class Trace(Eval):
    def __init__(self, n, chi):
        super().__init__(n, chi)
        self.truth = []

    def clause(self, lits, tag):
        self.truth.append((tag, any(lits)))
        super().clause(lits, tag)

    def equiv(self, a, b, tag):
        self.clause([a == b], tag)


def evaluate(t, chi):
    b = Trace(t.n, chi)
    build(b, t, ALL_OPTS)
    return b


def maps():
    ts = [(name, t) for name, _, t in controls() if name != 'mizhaev']
    p = ROOT / 'experiments/E-261113-02-s6-10-2-calibration-rung/maps/seeded_formulas.json'
    m = json.loads(p.read_text())['maps'][0]
    links = {int(k): v for k, v in m['links'].items()} if isinstance(m['links'], dict) else dict(enumerate(m['links']))
    tris = sorted({tuple(sorted((x, a, b))) for x, l in links.items() for a, b in zip(l, l[1:] + l[:1])})
    ts.append(('s6_10_2', Triangulation(10, tris, links=links, submap=True)))
    return ts


def shard(k):
    started = time.monotonic()
    rng = random.Random(2611140100 + k)
    record = dict(shard=k, seed=2611140100 + k, samples=0, comparisons=0, failures=[], families={}, mutation_detected=False)
    for name, t in maps():
        counts = Counter()
        for trial in range(10):
            while True:
                h = [[rng.randint(-40, 40) for _ in range(4)] for _ in range(t.n)]
                chi = chirotope_from_planes(h)
                if all(chi.values()):
                    break
            base = evaluate(t, chi)
            counts.update(tag for tag, _ in base.truth)
            assert 'GP' not in base.violations
            if not record['mutation_detected']:
                for q in chi:
                    bad = dict(chi); bad[q] *= -1
                    e = Eval(t.n, bad)
                    if e.gp():
                        record['mutation_detected'] = True
                        break
            for face in list(range(t.n)) + ['mirror']:
                changed = {q: -v if face == 'mirror' or face in q else v for q, v in chi.items()}
                after = evaluate(t, changed)
                record['comparisons'] += 1
                if after.truth != base.truth or Counter(after.violations) != Counter(base.violations):
                    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(base.truth, after.truth)) if a != b]
                    record['failures'].append(dict(map=name, trial=trial, transform=face,
                                                   differences=diffs[:8], planes=h,
                                                   before=dict(Counter(base.violations)),
                                                   after=dict(Counter(after.violations))))
                    record['seconds'] = time.monotonic() - started
                    return record
            record['samples'] += 1
        record['families'][name] = dict(counts)
    record['seconds'] = time.monotonic() - started
    return record


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    with ProcessPoolExecutor(10) as pool:
        rows = list(pool.map(shard, range(10)))
    for r in rows:
        (out / f"shard{r['shard']}.json").write_text(json.dumps(r, indent=2) + '\n')
    paths = [Path(__file__), ROOT / 'code/omsat.py', ROOT / 'code/omsat_validate.py',
             ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/test_encoder.py',
             ROOT / 'experiments/E-261113-02-s6-10-2-calibration-rung/maps/seeded_formulas.json']
    result = dict(PASS=all(not r['failures'] and r['mutation_detected'] for r in rows),
                  samples=sum(r['samples'] for r in rows), comparisons=sum(r['comparisons'] for r in rows),
                  wall_seconds=time.monotonic() - start,
                  commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  dirty=bool(subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()),
                  python=sys.version, inputs_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    return 0 if result['PASS'] else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
