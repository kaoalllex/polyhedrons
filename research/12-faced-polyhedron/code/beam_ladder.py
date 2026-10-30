"""Branching genus ladder: instead of one fixed chain M0 -> M6, grow from a REALIZED level by every
possible next handle. From an exactly embedded polyhedron (planes + dual triangles) list all tubes
whose six new edges are new (handle_add.candidates), keep those after which all n(n-1)/2 pairs are
still reachable (handle_add.reach), order them by the pair energy of the new map at the current
planes, and search each (annealing + CMA-ES, seeded from the current planes; float zeros re-checked
exactly). Every realized next level is saved and climbed further (depth first).
Usage: python3 -I beam_ladder.py LEVEL_JSON MINUTES_PER_CANDIDATE SEED OUT_DIR [WORKERS]"""
import json, os, sys
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from handle_add import candidates, reach
from ladder import pack, pair_energy
from genus_ladder import search
from ladder_exact import verify


def genus_of(tris, n):
    E = len({frozenset(e) for t in tris for e in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2]))})
    return (2 - (n - E + len(tris))) // 2


def extendable(tris, n):
    full = n * (n - 1) // 2
    out = []
    for t1, t2, R, L in candidates(tris, n):
        r, _ = reach(R, n, node_limit=3000)
        if r == full:
            out.append((t1, t2, R, L))
    return out


def work(args):
    planes, R, L, minutes, seed = args
    rng = np.random.default_rng(seed)
    (b, H), runs = search(L, len(planes), minutes, rng, planes)
    rec = {'best': float(b), 'planes': H.tolist(), 'triangles': [list(t) for t in R]}
    if b < 0.5:
        rec['exact'] = bool(verify(H.tolist(), L, require_all_pairs=False)['EMBEDDED'])
    return rec


def climb(level, minutes, seed, out_dir, workers, path=()):
    H = np.array(level['planes'], float); n = len(H); tris = [tuple(t) for t in level['triangles']]
    g = genus_of(tris, n)
    C = extendable(tris, n)
    order = []
    for i, (t1, t2, R, L) in enumerate(C):
        LK, M, _ = pack(L); e, o = pair_energy(H, LK, M); order.append((e, o, i))
    order.sort()
    print('genus %d %s: %d extendable handles, start energies %s' % (g, path, len(C), [(int(e), i) for e, o, i in order]), flush=True)
    jobs = [(level['planes'], C[i][2], C[i][3], minutes, seed * 1000 + i) for e, o, i in order]
    with Pool(workers) as P:
        recs = P.map(work, jobs)
    log = []
    for (e, o, i), rec in zip(order, recs):
        rec['tube'] = [list(C[i][0]), list(C[i][1])]; rec['genus'] = g + 1; rec['start_energy'] = float(e)
        log.append({k: rec[k] for k in ('tube', 'best', 'start_energy') if k in rec} | {'exact': rec.get('exact', False)})
        print('  genus %d via tube %s-%s: best %.3f %s' % (g + 1, C[i][0], C[i][1], rec['best'], 'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
    json.dump(log, open(os.path.join(out_dir, 'genus%d_%s.json' % (g + 1, '_'.join(map(str, path)) or 'root')), 'w'))
    for (e, o, i), rec in zip(order, recs):
        if rec.get('exact'):
            name = os.path.join(out_dir, 'realized_genus%d_%s.json' % (g + 1, '_'.join(map(str, path + (i,)))))
            json.dump(rec, open(name, 'w'))
            if g + 1 == (n - 3) * (n - 4) // 12:
                print('!!! FULL GENUS REALIZED:', name, flush=True)
                return True
            if climb(rec, minutes, seed, out_dir, workers, path + (i,)):
                return True
    return False


if __name__ == '__main__':
    lv = json.load(open(sys.argv[1])); minutes = float(sys.argv[2]); seed = int(sys.argv[3]); out_dir = sys.argv[4]
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    os.makedirs(out_dir, exist_ok=True)
    climb(lv, minutes, seed, out_dir, workers)
