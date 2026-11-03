---
id: E-261101-17
title: Geometry of the realization spaces - chord widths, shrinkage per handle, connectivity of the archive
date: 2026-11-01
status: planned
direction: [DR13, DR17]
origin: [I-261101-09, I-261030-21, E-261030-10]
tests: [H-261101-09, H-261101-10]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 1 2 | budget: about 10 core-h on the laptop, no new objects claimed. Before any
> compute: `PLAN.md` (skill `experiment-start`).

## Goal

Width distributions of the realization regions of the archived genus-2 and genus-3 polyhedra, the width ratio
between a genus-2 parent and its genus-3 child, and the component structure of the 54 type-15 genus-3 realizations.

## Next

Stop rule: 2,000 hit-and-run steps on each of 10 realizations (5 genus 2, 5 genus 3, including parent-child pairs)
and the 54 x 53 / 2 straight-segment tests; or earlier if the widths at genus 3 are already below 1e-3 in every
normal direction (then the conclusion is clear).

## Starting point

* Membership oracle: `code/ladder_exact.verify(H, links, require_all_pairs=False)['EMBEDDED']` with the realization's
  own links (`gauss_degree.links_from(coherent_triangles(tris))`). Normalise planes to unit normals; move in the
  36 coordinates; a chord is found by doubling then bisection (20 steps) on each side; use the maximal feasible
  interval containing the current point (the region is not convex; this is a Markov chain on its component).
* Split the directions: offsets only (the fibre is a cone, FD8, so chords there measure its inradius) and normals
  only (where the thinness lives); report both distributions, never the mixed one alone.
* Speed: a float pre-filter (`code/fastviol.py` or the float margins of `local_viol`) before every exact
  verification; exact arithmetic only on candidate chord endpoints and accepted points.
* Report per realization: chord-length quantiles, the fraction of chords shorter than 0.05 and 0.1 in the normal
  directions (compare with the control of E-261030-11), and the estimated log-volume ratio child / parent from
  matched directions.
* Connectivity: segments between pairs of type-15 realizations tested at 100 points exactly; then hit-and-run paths
  from each realization for 500 steps and the pairwise minimal distance reached.
* Positive control: the Szilassi polyhedron's region (genus 1) must be wide (chords of order 0.1-1); negative
  control: a genus-4 attempt (`E-261030-04`) is not EMBEDDED, so hit-and-run must refuse to start there.
* Outcomes: strong shrinkage per handle supports H-261101-09 and closes E-261101-04 by theory; comparable widths
  weaken it and make a power study worth running. Many components support H-261101-10's spirit (continuation
  cannot wander); one component makes E-261101-19 cheaper.
