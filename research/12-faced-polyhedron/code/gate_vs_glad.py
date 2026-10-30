"""Night-3 branching attempts versus the Gauss gate of their arm (results/gate x results/glad): does the
handle degree k_tau at the realized seed (k_tau = -1: the next map is already in its class in the seed's
orientation) predict the outcome of the event-energy search from that seed?
Usage: python3 -I gate_vs_glad.py [RESULTS_DIR]"""
import hashlib, json, os, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
res = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'overnight', 'results')


def rkey(planes, tris):     # = run_overnight._rkey
    h = hashlib.sha256(json.dumps([[round(float(v), 9) for v in p] for p in planes]).encode()
                       + json.dumps(sorted(sorted(int(x) for x in t) for t in tris)).encode())
    return h.hexdigest()[:10]


gate = {}
for l in open(os.path.join(res, 'gate', 'results.jsonl')):
    r = json.loads(l)
    if r.get('status') == 'GATE':
        gate[r['task'][2:]] = r
rows = []
for l in open(os.path.join(res, 'glad', 'results.jsonl')):
    r = json.loads(l)
    br = r.get('branch')
    if not br:
        continue
    base = next((lv for lv in r['levels'] if lv['genus'] == br['from_genus'] and lv.get('exact')), None)
    if base is None:
        continue
    g = gate.get(rkey(base['planes'], base['triangles']))
    if g is None:
        continue
    arms = {json.dumps(a['tube']): a for a in g['arms']}
    for t in br['tried']:
        if t.get('genus') != br['from_genus'] + 1:
            continue                                   # only the first step from the gated seed
        a = arms.get(json.dumps(t['tube']))
        if a is None:
            continue
        rows.append((r['task'], r['type_id'], a.get('k_tau'), bool(a.get('pass')), a.get('hemisphere_margin'),
                     t['best'], bool(t.get('exact'))))
by = defaultdict(list)
for row in rows:
    by[row[2]].append(row)
print('%d first-step branch attempts with a gated arm' % len(rows))
for k in sorted(by, key=str):
    b = sorted(x[5] for x in by[k])
    print('k_tau %s: %d attempts, realized %d, best counts %s, mean %.2f' % (
        k, len(b), sum(x[6] for x in by[k]), b, sum(b) / len(b)))
for p in (True, False):
    b = [x[5] for x in rows if x[3] == p]
    if b:
        print('T1 %s: %d attempts, realized %d, mean best %.2f' % ('pass' if p else 'fail', len(b),
              sum(x[6] for x in rows if x[3] == p), sum(b) / len(b)))
for x in rows:
    if x[6]:
        print('REALIZED from seed:', x)
print('by hemisphere margin of the six handle normals at the seed:')
for lo, hi in ((-9, 0.005), (0.005, 0.05), (0.05, 0.15), (0.15, 9)):
    b = [x for x in rows if x[4] is not None and lo <= x[4] < hi]
    if b:
        print('  margin [%g, %g): %d attempts, realized %d, best <= 1.01: %d, mean best %.2f' % (
            lo, hi, len(b), sum(x[6] for x in b), sum(1 for x in b if x[5] <= 1.01), sum(x[5] for x in b) / len(b)))
