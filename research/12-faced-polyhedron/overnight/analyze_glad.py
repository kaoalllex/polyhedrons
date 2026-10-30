"""Summarize a genus-ladder run (job 'glad'): per task the highest exactly realized genus, the best
violation count per level, the branching attempts, and for every near-realization (best < 3) whether it
is a degenerate limit (shortest edge or corner-plane margin tiny relative to the diameter).
Usage: python3 -I analyze_glad.py [RESULTS_JSONL]   (default: results/glad/results.jsonl)"""
import json, os, sys
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'code'))
from gauss_degree import coherent_triangles, links_from
from ladder import pack, degeneracy


def degen(planes, tris):
    H = np.array(planes, float); nr = np.linalg.norm(H[:, :3], axis=1); H[:, :3] /= nr[:, None]; H[:, 3] /= nr
    LK, M, _ = pack(links_from(coherent_triangles([tuple(t) for t in tris]), len(H)))
    return degeneracy(H, LK, M)


def main(path):
    R = [json.loads(l) for l in open(path) if l.strip()]
    print('%d tasks; highest exactly realized genus: %s' % (len(R), dict(sorted(Counter(r['top_exact_genus'] for r in R).items()))))
    near = []
    for r in sorted(R, key=lambda r: (-r['top_exact_genus'], r['task'])):
        lv = [(l['genus'], round(l['best'], 2)) for l in r['levels']]
        br = r.get('branch')
        bs = '' if not br else '  branch from %d: %s' % (br['from_genus'], sorted(round(t['best'], 2) for t in br['tried']))
        print('%-7s type %2d top %d  %s%s' % (r['task'], r['type_id'], r['top_exact_genus'], lv, bs))
        for l in r['levels']:
            if 0.5 <= l['best'] < 3 and l['genus'] > r['top_exact_genus']:
                near.append((l['best'], r['task'], l['genus'], l['planes'], l['triangles']))
        for t in (br or {}).get('tried', []):
            if 0.5 <= t['best'] < 3 and 'planes' in t and 'triangles' in t:     # older runs: no triangles saved
                near.append((t['best'], r['task'] + '/branch', t['genus'], t['planes'], t['triangles']))
    print('\nnear-realizations above the realized genus (best < 3): degenerate if edge < 1e-5 or margin < 1e-7')
    for b, task, g, planes, tris in sorted(near, key=lambda x: (-x[2], x[0])):
        e, m = degen(planes, tris)
        print('  %-14s genus %d best %.3f  edge %.1e margin %.1e %s' % (task, g, b, e, m, 'DEGENERATE' if (e < 1e-5 or m < 1e-7) else ''))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'results', 'glad', 'results.jsonl'))
