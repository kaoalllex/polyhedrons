"""Session check of the ideas triage 2026-11-18 (owner idea: allow one curved face).

Local surgery: a new non-planar face S replaces a disk D on the surface of a known eight-face object. D must be a
thin neighbourhood of a tree in the 1-skeleton, since a band through a face interior splits that face. Each tree
edge consumes one adjacency segment, so only pairs with multiplicity >= 2 may lose a segment, at most m - 1 each.
S touches every face incident to a tree vertex. The question: does a legal tree touch all eight faces?
Usage (research venv): python3 reviews/ideas-triage-2026-11-18-strip.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'code'))
from control_rost_vigh import CYCLES as RV  # noqa: E402

MZ = json.load(open(os.path.join(HERE, '..', 'literature', 'mizhaev2026-planes.json')))['face_walks_1based']


def check(name, cycles):
    faces_of, edge_faces = {}, {}
    for nm, c in cycles.items():
        for v in c:
            faces_of.setdefault(v, set()).add(nm)
        for k in range(len(c)):
            edge_faces.setdefault(frozenset((c[k], c[(k + 1) % len(c)])), set()).add(nm)
    assert all(len(f) == 2 for f in edge_faces.values())
    mult = {}
    for f in edge_faces.values():
        mult[frozenset(f)] = mult.get(frozenset(f), 0) + 1
    multi = [e for e, f in edge_faces.items() if mult[frozenset(f)] >= 2]
    adj = {}
    for e in multi:
        a, b = tuple(e)
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    # components of the multi-edge graph; a legal tree lies in one component and touches at most its faces
    comps, best, seen = [], 0, set()
    for v in adj:
        if v in seen:
            continue
        comp, stack = set(), [v]
        while stack:
            x = stack.pop()
            if x not in comp:
                comp.add(x)
                stack += adj[x]
        seen |= comp
        comps.append(len(comp))
        best = max(best, len(set().union(*(faces_of[x] for x in comp))))
    print('%s: %d faces, %d multi pairs, %d multi edges, components (vertices) %s, faces touched by a whole '
          'component at most %d of %d' % (name, len(cycles), sum(1 for m in mult.values() if m >= 2), len(multi),
                                          sorted(comps), best, len(cycles)))


check('Roest-Vigh', RV)
check('Mizhaev', MZ)
