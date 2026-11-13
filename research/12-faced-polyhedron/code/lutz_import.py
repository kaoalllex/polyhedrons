"""Import F. Lutz's lexicographic surface lists (`manifold_lex_d2_n<V>_o1_g<g>_#k=[[a,b,c],...]`, 1-indexed) as
oriented triangles and dual face links, with exact combinatorial checks. The input file is untrusted data: it is only
parsed (run with `python3 -I`), never executed.

Checks per entry: simplicial closed surface (distinct triangles, every edge in exactly two triangles, every vertex
link one cycle), connected, orientable (coherent orientation found), (V, E, F) and genus as named; over the file:
the entry count and pairwise non-isomorphism (canonical dart codes of E-261103-01 `census.from_links`, up to mirror).

Usage: python3 -I lutz_import.py LIST V GENUS COUNT OUT_JSON"""
from collections import Counter, defaultdict
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('census', ROOT / 'experiments/E-261103-01-s5-map-census/census.py')
census = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(census)

ENTRY = re.compile(r'manifold_lex_d2_n(\d+)_o1_g(\d+)_#(\d+)\s*=\s*(\[\[[0-9,\s\[\]]*\]\])')


def parse(text):
    """[(lutz_number, n, genus, triangles 0-based)] in file order; the triangle list is read as integers only."""
    out = []
    for m in ENTRY.finditer(text):
        triples = re.findall(r'\[(\d+),(\d+),(\d+)\]', re.sub(r'\s+', '', m.group(4)))
        out.append((int(m.group(3)), int(m.group(1)), int(m.group(2)), [tuple(int(x) - 1 for x in t) for t in triples]))
    return out


def orient(tris):
    """Coherently oriented copies of the triangles (BFS over shared edges); ValueError if non-orientable or
    disconnected."""
    by_edge = defaultdict(list)
    for i, t in enumerate(tris):
        for a, b in itertools.combinations(t, 2):
            by_edge[frozenset((a, b))].append(i)
    oriented = {0: tuple(tris[0])}
    todo = [0]
    while todo:
        i = todo.pop()
        a, b, c = oriented[i]
        for u, v in ((a, b), (b, c), (c, a)):
            j, = [k for k in by_edge[frozenset((u, v))] if k != i]
            w, = [x for x in tris[j] if x not in (u, v)]
            want = (v, u, w)  # the neighbour traverses the shared edge in the opposite direction
            if j in oriented:
                if set(zip(oriented[j], oriented[j][1:] + oriented[j][:1])) != set(zip(want, want[1:] + want[:1])):
                    raise ValueError('non-orientable')
            else:
                oriented[j] = want
                todo.append(j)
    if len(oriented) != len(tris):
        raise ValueError('disconnected')
    return [oriented[i] for i in range(len(tris))]


def links_of(oriented, n):
    """Cyclic neighbour list of every vertex: in triangle (v, x, y) the link of v steps x -> y."""
    succ = defaultdict(dict)
    for t in oriented:
        for v, x, y in (t, t[1:] + t[:1], t[2:] + t[:2]):
            if x in succ[v]:
                raise ValueError(f'vertex {v}: link not a cycle')
            succ[v][x] = y
    links = []
    for v in range(n):
        start = min(succ[v]); cyc = [start]
        while succ[v][cyc[-1]] != start:
            cyc.append(succ[v][cyc[-1]])
            if len(cyc) > len(succ[v]):
                raise ValueError(f'vertex {v}: link not a cycle')
        if len(cyc) != len(succ[v]):
            raise ValueError(f'vertex {v}: link not one cycle')
        links.append(cyc)
    return links


def check(tris, n, genus):
    """The surface checks of the module docstring; returns (oriented triangles, links, canonical code, Aut+, reflexible)."""
    if len(set(map(frozenset, tris))) != len(tris) or any(len(set(t)) != 3 or not all(0 <= x < n for x in t) for t in tris):
        raise ValueError('triangles not distinct or not on V vertices')
    edges = Counter(frozenset(e) for t in tris for e in itertools.combinations(t, 2))
    if any(c != 2 for c in edges.values()):
        raise ValueError('an edge not in exactly two triangles')
    oriented = orient(tris)
    links = links_of(oriented, n)
    V, E, F = n, len(edges), len(tris)
    if V - E + F != 2 - 2 * genus or 2 * E != 3 * F:
        raise ValueError(f'(V, E, F) = {(V, E, F)} does not match genus {genus}')
    m = census.from_links(links)
    code, aut_plus, reflexible, _, _ = m.canon()
    return oriented, links, code, aut_plus, reflexible


def import_list(path, n, genus, count):
    raw = Path(path).read_bytes()
    entries = parse(raw.decode('ascii'))
    if len(entries) != count or [e[0] for e in entries] != list(range(1, count + 1)):
        raise ValueError(f'expected entries #1..#{count}, found {len(entries)}')
    maps, codes = [], {}
    for number, en, eg, tris in entries:
        if (en, eg) != (n, genus):
            raise ValueError(f'#{number}: header (n, g) = {(en, eg)}')
        oriented, links, code, aut_plus, reflexible = check(tris, n, genus)
        digest = hashlib.sha256(json.dumps(code, separators=(',', ':')).encode()).hexdigest()
        if digest in codes:
            raise ValueError(f'#{number} isomorphic to #{codes[digest]}')
        codes[digest] = number
        maps.append(dict(lutz=number, triangles=[list(t) for t in oriented], links=links, canonical_sha256=digest,
                         aut_plus=aut_plus, reflexible=reflexible, V_E_F=[n, len(tris) * 3 // 2, len(tris)]))
    return dict(source=Path(path).name, source_sha256=hashlib.sha256(raw).hexdigest(), V=n, genus=genus,
                count=len(maps), maps=maps)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    path, n, genus, count, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5])
    result = import_list(path, n, genus, count)
    out.write_text(json.dumps(result, indent=1) + '\n')
    print(f"{result['count']} maps, pairwise non-isomorphic, source sha256 {result['source_sha256']}, "
          f"out sha256 {hashlib.sha256(out.read_bytes()).hexdigest()}")
