---
id: I-261116-07
title: Uniformity lemma - a cubic embedded polyhedron survives a generic perturbation of its planes, so uniform formulas lose no cubic object
date: 2026-11-16
status: tried
direction: [DR19]
origin: [E-261116-05, E-261103-02]
---

## Idea

For a cubic embedded polyhedron with planar simple faces, a small generic perturbation of the face planes (and of the
plane at infinity) keeps every vertex, edge and face and the embedding: every vertex lies on exactly three planes, and
embeddedness is an open condition. So the uniform asymmetric formulas (E-261103-02, E-261114-01) lose no cubic object;
symmetric formulas are not covered (a fixed face can force non-uniformity, `E-261103-02/SOUNDNESS.md:65-78`).

## Why it might help

It removes "non-uniform" from the scope of the paper items B2-B4 and D3 (`E-261116-05/CONCLUSION.md:27`). Untested
proposal: the openness step and the plane at infinity need a written argument.

## Cheapest test

One page in E-261116-09; check each step against the encoder's assumptions (`SOUNDNESS.md:48`).

Source: `reviews/strategy-review-2026-11-16b.md` §5 (N2).

## 2026-11-22 (E-261116-09)

Written as L1 (and the equivariant L2), PROVED-1: `experiments/E-261116-09-uniformity-perturbation-lemmas/LEMMAS.md`.
