"""Shard runner: python3 units.py SHARD SHARDS OUT. Stage 1 differential test (fails the shard on a mismatch), stage 2 the
units of this shard (round-robin): pinned controls, unpinned SAT controls, the six (9, 3) targets."""
import json, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / 'code'))
import enc2, difftest, solve2

TARGETS = [40, 43, 10, 30, 48, 5]


def units():
    objs = {n: (h, l) for n, h, l in difftest.objects()}
    u = []
    for n in ('roest_vigh', 'mizhaev', 'grooved2', 'grooved3'):
        u.append((f'pinned_pos_{n}', 'SAT', lambda n=n: (enc2.Enc(objs[n][1]), enc2.chirotope(objs[n][0]), 300)))
    for n in ('grooved2_swapped', 'grooved3_swapped', 'rv_planes_mizhaev_map'):
        u.append((f'pinned_neg_{n}', 'UNSAT-VERIFIED', lambda n=n: (enc2.Enc(objs[n][1]), enc2.chirotope(objs[n][0]), 300)))
    u.append(('unpinned_szilassi', 'SAT', lambda: (enc2.Enc(objs['szilassi'][1], gauge=True), None, 600)))
    u.append(('unpinned_roest_vigh', 'SAT (TIMEOUT = no information)', lambda: (enc2.Enc(objs['roest_vigh'][1], gauge=True), None, 1800)))
    maps = json.loads((ROOT / 'experiments/E-261103-01-s5-map-census/results/maps_9_3.json').read_text())['maps']
    for i in TARGETS:
        u.append((f'map{i}', 'UNSAT-VERIFIED', lambda i=i: (enc2.Enc(maps[i]['links'], gauge=True), None, 1800)))
    return u


def main(shard, shards, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    import random
    t = time.monotonic()
    import io, contextlib
    buf = io.StringIO()
    random.seed(shard)
    with contextlib.redirect_stdout(buf):
        bad = difftest.main(12, seed=2611090310 + shard)
    (out / 'difftest.txt').write_text(buf.getvalue())
    print(buf.getvalue(), flush=True)
    if bad:
        sys.exit('differential test mismatch: controls failed, no unit run')
    for k, (name, expect, make) in enumerate(units()):
        if k % shards != shard:
            continue
        if any(name in f.read_text() for f in out.parent.glob('*/results.jsonl')):
            continue
        e, chi, cap = make()
        r = solve2.run(e, out, name, cap, 1800, extra=e.pin(chi) if chi else ())
        r['expected'] = expect
        with open(out / 'results.jsonl', 'a') as f:
            f.write(json.dumps(r) + '\n')
        print(json.dumps(r), flush=True)


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
