"""Exact check of a saved candidate file, whatever its format (one entry point for every claim).

Supported JSON layouts:
  * {planes, triangles} or {planes, map}  - map-based results (genus ladder, archive records);
  * {planes, links} or a list of such records - ladder results with cyclic neighbour lists;
  * {real: [...]}                          - the realization archive (overnight/results/arch/archive.json);
  * {planes, solid}                        - solid-first results (delegated to code/verify_solid.py).
Every record is checked in rational arithmetic by code/ladder_exact.verify (planes rounded at 1e-9, as everywhere).

Usage: python3 verify_candidate.py FILE.json [--all-pairs | --target S0] [--min-genus G]
  (default)    EMBEDDED: an embedded polyhedron on the given map (any face count, doubled adjacencies allowed);
  --all-pairs  ... and every two faces are adjacent (S1 allows doubled adjacencies);
  --target S0  the strict target of SPEC.md section 1: EMBEDDED, 12 faces, every two faces share exactly one
               edge, (V, E, F, chi) = (44, 66, 12, -10). This is the only check that may be called a solution.
Prints one line per record with its PASS flag; exit status 1 if any checked record fails."""
import ast
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
    if p.returncode != 0:
        return {'EMBEDDED': False, 'report': last}
    r = ast.literal_eval(last)
    return {'EMBEDDED': r['EXACT_EMBEDDED'], 'all_pairs_adjacent': r['adjacent_pairs'] == r['of'],
            'single_adjacency': r['E'] == r['adjacent_pairs'], 'V_E_F_chi': (r['V'], r['E'], r['faces'], r['chi']),
            'report': r}


def _verify(r):
    from ladder_exact import verify
    L = _links(r)
    out = verify(r['planes'], L, require_all_pairs=False)
    out['single_adjacency'] = all(len(v) == len(set(v)) for v in L.values())
    return out


def passes(rep, target=None):
    """target None: EMBEDDED; 'all-pairs': + every pair adjacent; 'S0': the strict target of SPEC.md section 1."""
    ok = bool(rep['EMBEDDED'])
    if target in ('all-pairs', 'S0'):
        ok = ok and bool(rep.get('all_pairs_adjacent'))
    if target == 'S0':
        ok = ok and bool(rep.get('single_adjacency')) and tuple(rep.get('V_E_F_chi', ())) == (44, 66, 12, -10)
    return ok


def verify_file(path, all_pairs=False, min_genus=None, target=None):
    """List of exact reports (dicts with keys EMBEDDED and PASS), one per checked record."""
    target = target or ('all-pairs' if all_pairs else None)
    d = json.load(open(path))
    if isinstance(d, dict) and 'solid' in d:
        reps = [_solid(path)]
    else:
        recs = d['real'] if isinstance(d, dict) and 'real' in d else d if isinstance(d, list) else [d]
        if min_genus is not None:
            recs = [r for r in recs if int(r.get('genus', 0)) >= min_genus]
        reps = [_verify(r) for r in recs]
    for rep in reps:
        rep['target'] = target or 'embedded'
        rep['PASS'] = passes(rep, target)
    return reps


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    mg = int(args[args.index('--min-genus') + 1]) if '--min-genus' in args else None
    target = args[args.index('--target') + 1] if '--target' in args else None
    if target not in (None, 'S0'):
        sys.exit('only --target S0 is implemented (S1 = --all-pairs)')
    reps = verify_file(args[0], '--all-pairs' in args, mg, target)
    for i, r in enumerate(reps):
        print(i, json.dumps({k: v for k, v in r.items() if k != 'corner_triples_distinct'}, default=str))
    bad = sum(1 for r in reps if not r['PASS'])
    print('%d record(s), target %s: %d PASS, %d fail' % (len(reps), reps[0]['target'] if reps else '-',
                                                         len(reps) - bad, bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
