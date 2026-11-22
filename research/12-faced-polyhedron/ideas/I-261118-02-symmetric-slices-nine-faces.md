---
id: I-261118-02
title: Symmetric slices at nine faces - the eight-face groups cannot act, C3 3+3+3 covers every order-3 rotation, the uniform families listed
date: 2026-11-18
status: tried
direction: [DR19, DR11]
origin: [I-261117-02, I-261113-04, E-261117-01]
---

## Idea

PROVED-1 sketch (lead review 2026-11-18, unreviewed). (a) A symmetry fixing a face keeps its outward normal: the face
is perpendicular to a rotation axis or has its normal in a mirror; no inversion or rotoreflection fixes a face. (b) A
rotation fixes at most one face (dialogue 2026-11-16 §6, PROVED-1). (c) A rotation of order >= 4 sends a plane to
>= 4 planes through one axis point (non-uniform). Hence D2 and S4 have only 4-orbits on nine faces (impossible);
every order-3 rotation acts freely, and an equivariant perturbation makes it uniform with infinity, so C3 3+3+3 covers
D3, C3v and C3h. Uniform families: C3 3+3+3 and Cs 4 x 2 + 1 (standard chart), C2 4 x 2 + 1 and Cs 3 x 2 + 3 (moved
chart). With orbits {0,1,2}, {3,4,5}, {6,7,8}, the P3 gauge (vertices 012 and 345, both fixed by the rotation) is
equivariant: its bits are constant on orbits and set by flipping whole orbits.

## Why it might help

It lists every symmetric family worth a formula at nine faces, so E-261118-02 runs a complete list, not a sample.

## Cheapest test

A written proof in the lemma session E-261116-09; checks on the known objects; E-261118-02's gauge reachability control.

Source: `reviews/strategy-review-2026-11-18.md` §5 N2.

## 2026-11-19 correction (E-261118-02, deviation 1)

Cs 4 x 2 + 1 and Cs 3 x 2 + 3 are not uniform: a mirror swapping two pairs of planes makes the four planes concurrent
(A = diag(R, 1), det A = -1, so det(Ah, h, Ak, k) = -D = D; PROVED-1, exact check in `test_p3sym.py`), so chi of those
four is 0 in every chart. Uniform families left at nine faces: C3 3+3+3 (standard chart; E-261118-02, UNKNOWN at 1 h)
and C2 4 x 2 + 1 (moved chart; not run). `STRATEGY.md` §1's family list: to the lead.

## 2026-11-22 (E-261116-09)

Written as L3 (coverage up to Cs; the gauge by orbit flips), PROVED-1: `experiments/E-261116-09-uniformity-perturbation-lemmas/LEMMAS.md`.
