---
id: H-261101-09
title: The realization regions are thin and shrink sharply per handle, so sampling has no power at any genus
date: 2026-11-01
status: open
origin: [I-261101-09, E-261030-11, H-261101-04]
---

## Statement

The realization region of an S3 polyhedron has widths in plane space that shrink by a large constant factor
with every handle; fixed-normal and normals-first sampling therefore has near-zero power at genus 4 and above,
whatever the truth about genus 6. The 12,202 UNSATs of nights 4-5 are explained by this alone.

## Rival

Widths are comparable across genus; the UNSAT streak carries information about the next level (H-261101-04).

## Evidence so far

One control: SAT at radius 0.05, UNSAT at 0.1 (E-261030-11). The Wendel estimate of the fresh-eyes review
(`reviews/fresh-eyes-review.md` 2.3) predicts rarity of closable normals.

## What would move it

E-261101-17 (width distributions and the genus-2 to genus-3 ratio); E-261101-04 at radii 0.005-0.02.
