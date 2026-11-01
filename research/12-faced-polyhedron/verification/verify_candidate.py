"""Exact check of a saved candidate file, whatever its format (one entry point for every claim).

Supported JSON layouts:
  * {planes, triangles} or {planes, map}  - map-based results (genus ladder, archive records);
  * {planes, links} or a list of such records - ladder results with cyclic neighbour lists;
  * {real: [...]}                          - the realization archive (overnight/results/arch/archive.json);
  * {planes, solid}                        - solid-first results (delegated to code/verify_solid.py).
Every record is checked in rational arithmetic by code/ladder_exact.verify (planes rounded at 1e-9, as everywhere).

Usage: python3 verify_candidate.py FILE.json [--all-pairs] [--min-genus G]
Prints one line per record; exit status 1 if any checked record is not EMBEDDED."""
import json
import os
import subprocess
import sys

CODE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code'))
sys.path.insert(0, CODE)


def _links(r):
    if 'links' in r:
        return {int(k): v for k, v in r['links'].items()}
    from gauss_degree import coherent_triangles, links_from
    tris = r.get('triangles')
    if tris is None:
        tris = [tuple(map(int, t.split(','))) for t in r['map'].split(';')]
    return links_from(coherent_triangles([tuple(t) for t in tris]), len(r['planes']))


def _solid(path):
    p = subprocess.run([sys.executable, 'verify_solid.py', os.path.abspath(path)], cwd=CODE,
                       capture_output=True, text=True)
    last = (p.stdout.strip().splitlines() or [p.stderr.strip()])[-1]
    return {'EMBEDDED': p.returncode == 0 and "'EXACT_EMBEDDED': True" in last, 'report': last}


def verify_file(path, all_pairs=False, min_genus=None):
    """List of exact reports (dicts with key EMBEDDED), one per checked record."""
    from ladder_exact import verify
    d = json.load(open(path))
    if isinstance(d, dict) and 'solid' in d:
        return [_solid(path)]
    recs = d['real'] if isinstance(d, dict) and 'real' in d else d if isinstance(d, list) else [d]
    if min_genus is not None:
        recs = [r for r in recs if int(r.get('genus', 0)) >= min_genus]
    return [verify(r['planes'], _links(r), require_all_pairs=all_pairs) for r in recs]


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    mg = int(args[args.index('--min-genus') + 1]) if '--min-genus' in args else None
    reps = verify_file(args[0], '--all-pairs' in args, mg)
    for i, r in enumerate(reps):
        print(i, json.dumps({k: v for k, v in r.items() if k != 'corner_triples_distinct'}, default=str))
    bad = sum(1 for r in reps if not r['EMBEDDED'])
    print('%d record(s), %d EMBEDDED, %d not' % (len(reps), len(reps) - bad, bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
