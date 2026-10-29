# Polyhedrons

**Live page: https://kaoalllex.github.io/polyhedrons/**

Interactive 3D viewer of polyhedra in which every face shares an edge with every other face:

- Tetrahedron
- Császár polyhedron (1949): the dual case, where every vertex is joined to every other vertex
- Szilassi polyhedron (1977): 7 faces, genus 1
- Mizhaev equivelar octahedron (2026): 8 faces, genus 3

Link to a specific model with a hash, e.g. `#szilassi`, `#csaszar`, `#tetrahedron`.

## Why these polyhedra are special

In a typical polyhedron a face touches only a few neighbours. A cube's top face, for example, never
touches its bottom face. In the polyhedra here, **every face touches every other face**. That is very
hard to achieve with flat faces and straight edges, and above 4 faces it forces the polyhedron
to have holes, like a donut.

The number of holes (the genus `g`) comes from Euler's formula `V − E + F = 2 − 2g`. The viewer
computes it and checks it for each model.

The models fall into two classic series, plus one that stands apart.

### Series 1: every face touches every other face

Every pair of faces shares exactly one edge. With `F` faces, each face is an `(F−1)`-gon, three
faces meet at every vertex, and the number of holes is `g = (F−3)(F−4)/12`. The genus must be a
whole number, so only some face counts are possible: 4, 7, 12, 15, 16, …

| Polyhedron | Faces | Face shape | Vertices | Edges | Holes | Status |
|---|---|---|---|---|---|---|
| Tetrahedron | 4 | triangle | 4 | 6 | 0 | known |
| Szilassi (1977) | 7 | hexagon | 14 | 21 | 1 | known |
| next one | 12 | 11-gon | 44 | 66 | 6 | **open problem** |

- **Tetrahedron.** The only polyhedron without holes where every face touches every other.
- **Szilassi polyhedron.** It shows that a map on a torus can need 7 colours: every face borders
  all the others, so no two faces can share a colour.
- **The next one** would have 12 faces, each an 11-gon touching the other 11, with three edges at
  every vertex. Nobody has built it, and nobody has proved it impossible. The hard part is to make
  all 12 faces flat without the polyhedron passing through itself.

### Series 2: every vertex is joined to every other vertex

The "mirror image" (dual) of series 1: swap faces and vertices. All faces are triangles, every
pair of vertices is joined by an edge, so the polyhedron has no diagonals at all. With `V` vertices,
`g = (V−3)(V−4)/12`.

| Polyhedron | Vertices | Faces | Edges | Holes | Status |
|---|---|---|---|---|---|
| Tetrahedron | 4 | 4 | 6 | 0 | known |
| Császár (1949) | 7 | 14 | 21 | 1 | known |
| next one | 12 | 44 | 66 | 6 | **impossible** |

The tetrahedron is its own dual, so it starts both series. Here the next step is settled:
in 2010 Lars Schewe proved that a 12-vertex polyhedron of this kind cannot be built without
self-intersections.

### Standing apart: the Mizhaev octahedron

8 flat nine-sided faces, 24 vertices, 36 edges, three faces at every vertex, and three holes
(`24 − 36 + 8 = −4`, so `g = 3`). Every face still meets every other, but the rule is relaxed:
20 pairs of faces share one edge, and the other 8 pairs share two.

It cannot belong to series 1: for 8 faces the formula gives `(8−3)(8−4)/12 = 20/12`, which is not
a whole number. We know of no formula for this relaxed series, so it is not clear which polyhedron
comes next or how many holes it would have. All its vertices have integer coordinates, so every
property can be checked exactly, with no rounding.

## Research on the 12-face problem

Ongoing computer search: `research/12-faced-polyhedron/` (notes, code, results).
To run the overnight search locally see
[`research/12-faced-polyhedron/HOW_TO_RUN_OVERNIGHT.md`](research/12-faced-polyhedron/HOW_TO_RUN_OVERNIGHT.md).

## Viewer controls

- **Faces:** show or hide individual faces to look inside the model.
- **Lamp:** a point light you can switch on, drag by its arrows (or move with the X/Y/Z sliders),
  and dim or brighten. Faces block its light and cast shadows.
- **Light background:** switch between dark and light themes.

## See also

- [A genus-3 polyhedron, relaxed](https://ex.rs/a-genus-3-polyhedron-relaxed/): another interactive
  visualisation of Mizhaev's octahedron, which morphs it into a smooth genus-3 surface.
- [Ruslan Mizhaev, arXiv:2609.17700](https://arxiv.org/abs/2609.17700)
- [Szilassi polyhedron](https://en.wikipedia.org/wiki/Szilassi_polyhedron) and
  [Császár polyhedron](https://en.wikipedia.org/wiki/Cs%C3%A1sz%C3%A1r_polyhedron) on Wikipedia
