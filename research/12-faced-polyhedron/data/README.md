# Data: neighborly orientable 12-vertex triangulations of the genus-6 surface

Written 2026-10-29 by the combinatorial-topology researcher (Track 2).
These are the duals of the combinatorial types of the 12-face polyhedron (see
`../mathematical-model.md` §1.3). **They are abstract surfaces; nothing here says anything
about realizability in R^3 with planar faces.**

## Files

| File | Content |
|---|---|
| `k12_first.json` | One triangulation (first solution found), same format as below (list with 1 entry). It is identical (same canonical labelling) to entry `id 2` of the full list (HackerPoet no.18, Lutz #15); it has no `id` field. |
| `k12_triangulations.json` | The complete isomorphism-free list: **59 entries**. |
| `k12_invariants.json` | Per type: automorphism group (all elements as permutations with order, orientation character, fixed vertices / edges / triangles), vertex / edge / triangle / non-face-triple orbits. |
| `k12_literature_map.json` | Our `id` <-> `no.NN` in `literature/HackerPoet-NeighborlyPolyhedra/topologies.txt` (apparently ABS96 numbering) <-> `#NN` in the Lutz-format file `literature/Hashirama1337s-szilassi-12/code/k12_g6_lutz.txt` (Lutz `manifold_lex_d2_n12_o1_g6` numbering, provenance unverified). |
| `k12_summary.csv` | One row per type: id, external numbers, group orders, group structure, chirality, orbit counts. |
| `enum_k12_raw_output.txt` | Raw output of `code/enum_k12.c` (canonical codes, |Aut|, hit counts). |

## Format of `k12_triangulations.json`

A JSON list; entry fields:

* `id` (int): 0-based index; entries are sorted by `canonical` (string order).
* `triangles`: 44 triples `[a,b,c]`, vertices `0..11`, written with the smallest vertex first.
  **Orientation convention:** every triple is oriented coherently with one global orientation:
  the 132 directed edges `a->b, b->c, c->a` of the 44 triples are pairwise distinct
  (each edge is traversed once in each direction).
* `links`: `{"v": [l0, ..., l10]}` -- the 11 neighbours of `v` in cyclic order, starting at the
  smallest neighbour, such that `[v, l_i, l_{i+1}]` (indices mod 11) is (a cyclic rotation of) an
  oriented triangle of the list. In words: around `v`, the oriented triangle `[v,a,b]` means
  "`a` is followed by `b`". Dually: around face `v` of the polyhedron, the neighbouring faces
  appear in the order `links[v]`.
* `aut_order` (int): order of the full automorphism group = number of permutations of the 12
  vertices mapping the set of (unoriented) triangles onto itself (orientation-reversing maps
  included).
* `aut_orient_preserving_order` (int): number of those automorphisms that map every oriented
  triangle to an oriented triangle (equivalently, preserve the orientation of the surface).
  Always `aut_order / aut_orient_preserving_order` is 1 or 2.
* `chiral` (bool): **`true` iff the triangulation has NO orientation-reversing automorphism**
  (`aut_order == aut_orient_preserving_order`), i.e. the oriented surface is *not* isomorphic
  to its mirror image by an orientation-preserving isomorphism (the mirror image is a
  different oriented type). `false` ("achiral"/reflexible) iff some automorphism reverses the
  orientation.
* `canonical` (string): 12 groups of 11 hex digits (`0-9,a,b`) joined by `-`.
  Group `x` = `rot(x)` = the neighbours of `x` in positive cyclic order (as in `links`),
  starting at the smallest neighbour. `canonical` = the lexicographically smallest such string
  over **all relabellings of the vertices and both orientations**; this minimum is attained among
  the 12*11*2 = 264 "flag labellings" (vertex `v -> 0`, a neighbour `a -> 1`, the rest of the link
  of `v` read forward or backward -> `2..11`), so group 0 is always `123456789ab`.
  Every entry is stored in its canonical labelling, i.e. `canonical` equals the
  concatenation of its own `links` (for `x>=1`, `links[x]` starts with 0).
  Two triangulations are isomorphic (as simplicial complexes) iff their canonical strings agree.

Extra keys are not used; geometric-interest invariants live in `k12_invariants.json`:
`group` (structure of Aut), `group_orient_preserving`, `vertex_orbits` (orbits of Aut on the 12
vertices = the 12 faces of the polyhedron), `num_edge_orbits`, `num_triangle_orbits`
(= orbits on the 44 polyhedron vertices), `num_nonface_triple_orbits` (the 176 triples that
are not triangles, relevant for the 176 forbidden-triple conditions), `has_orientation_reversing_involution`,
and `elements` (each nontrivial automorphism: `perm` with `perm[x]` = image of `x`, `order`,
`orientation` +1/-1, `fixed_vertices`, `fixed_edges_pointwise`, `swapped_edges`
(edges `{u,v}` with `g(u)=v, g(v)=u`), `fixed_triangles` (as sets)).

## How it was produced / how to re-check

```
gcc -O2 -o enum_k12 code/enum_k12.c && ./enum_k12 > data/enum_k12_raw_output.txt    # ~19 s
python3 code/build_json.py data/enum_k12_raw_output.txt data/k12_triangulations.json
python3 code/check_triangulations.py data/k12_triangulations.json --selftest         # ~5 s
gcc -O2 -o enum2_k12 code/enum2_k12.c && ./enum2_k12 orient print > sols.txt          # ~65 s
python3 code/classify_enum2.py sols.txt data/k12_triangulations.json                   # ~26 s
python3 code/k12_invariants.py data/k12_triangulations.json data/k12_invariants.json
python3 -I code/compare_literature.py data/k12_triangulations.json \
   --hackerpoet literature/HackerPoet-NeighborlyPolyhedra/topologies.txt \
   --lutz literature/Hashirama1337s-szilassi-12/code/k12_g6_lutz.txt --out data/k12_literature_map.json
```

`check_triangulations.py` uses only the `triangles` field and re-derives everything else
(see its docstring); it does not import `k12_tools.py`.
