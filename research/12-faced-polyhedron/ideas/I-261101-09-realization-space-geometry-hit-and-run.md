---
id: I-261101-09
title: Measure the realization spaces of the archived polyhedra - widths, volume ratio per handle, connectivity
date: 2026-11-01
status: open
direction: [DR13, DR17]
origin: [I-261030-21, E-261030-10, E-261030-11]
---

## Idea

Treat the realization space of each archived genus-2 and genus-3 polyhedron as a geometric object and measure
it. Hit-and-run in plane space (R^36, or the 24 affine-normalised coordinates): from the current planes pick a
random direction, find the feasible interval along the line by bisection on the exact verifier
(`code/ladder_exact.verify`, `require_all_pairs=False`, EMBEDDED on its own map), jump to a uniform point of that
interval. Record: the chord-length distribution (widths), the fraction of chords shorter than 0.05 and 0.1 in the
normal directions, and for ladder pairs (a genus-2 parent and its genus-3 child on the same planes family) the
ratio of widths. Connectivity: for pairs of the 54 type-15 genus-3 realizations test the straight segment at 100
points exactly, then short hit-and-run paths; report the components.

## Why it might help

The only quantitative fact about thinness is one control (SAT at r = 0.05, UNSAT at r = 0.1). A width
distribution and its shrinkage per handle say how much any sampling search can ever find at genus 6 (H-261101-09),
and the component structure says whether continuation (E-261101-19) can move between realizations. Cross-field:
Monte Carlo volume estimation (hit-and-run, Smith 1984; Lovasz-Vempala), solution-space entropy in random CSPs.

## Cheapest test

One type-0 genus-3 realization, 2,000 hit-and-run steps, about 2 core-hours; plot the chord lengths.

## Source

Strategy review 2026-11-01, section 3 (parametrised family) and hypothesis H-R1.
