"""Cross-check of the Track-3 chirotope evaluator (omsat.Eval) against Track 4's independent
direct checker (planes.check_embedding) on shared configurations. Only this script imports
planes.py; the encoder omsat.py does not."""
import sys, os, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omsat import Eval, build, chirotope_from_planes, Triangulation
from omsat_validate import szilassi
import planes as P4
rng = random.Random(4242)
planes0, T7, _, _ = szilassi()
e0 = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'k12_first.json')))[0]
T12 = Triangulation(12, e0['triangles'], {int(k): v for k, v in e0['links'].items()})
res = dict(configs=0, IN_compared=0, IN_mismatch=0, emb_mismatch=0, embedded=0)
def run(pl, T):
    chi = chirotope_from_planes(pl)
    if any(v == 0 for v in chi.values()):
        return
    B = Eval(T.n, chi); build(B, T, dict(gp=False, triples=True))
    arr = P4.Arrangement(pl)
    r = P4.check_embedding(arr, T.tris)
    res['configs'] += 1
    for (k, X, Y, Z), v in B.named.items():
        res['IN_compared'] += 1
        if bool(v) != bool(r['in_direct'][(X, tuple(sorted((Y, Z))))]):
            res['IN_mismatch'] += 1
    mine = 'TRIPLE' not in B.violations
    res['embedded'] += mine
    if mine != r['ok_pairs'] or mine != r['ok_triples']:
        res['emb_mismatch'] += 1
for i in range(120):
    rad = [300, 3000, 10000, 20000][i % 4]
    run([[1000 * x + rng.randint(-rad, rad) for x in p] for p in planes0], T7)
for i in range(30):
    run([[rng.randint(-40, 40) for _ in range(4)] for _ in range(12)], T12)
print(res)
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'experiments', 'omsat', 'crosscheck_track4.json'), 'w'))
