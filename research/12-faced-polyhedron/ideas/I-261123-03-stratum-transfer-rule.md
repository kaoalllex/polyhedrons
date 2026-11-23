---
id: I-261123-03
title: A stratum transfer rule - price a non-equivelar (9, 4) stratum only for an extra-degree pattern that holds a realized (8, 3) map
date: 2026-11-23
status: open
direction: [DR19]
origin: [E-261117-04]
---

## Idea

Stratify the full cubic (8, 3) census by the degree sequence of its extra-edge multigraph (sum 16) and record the
plain-formula outcome per stratum. A non-equivelar (9, 4) stratum (extra degrees summing to 18) is priced only when an
(8, 3) map of a matching pattern is realized, under one transfer rule pre-registered before the probe, e.g. the (8, 3)
extra degrees plus a ninth face of extra degree 2 (the pattern of subdividing one extra edge). The rule defines a
search pattern only (CONJECTURE): there is no geometric lifting lemma, and an observed 0 of N at (8, 3) bounds
nothing at (9, 4) (cross-review 2026-11-23 check D).

## Why it might help

The full non-equivelar (9, 4) census is out of reach (order 10^7 classes, >= 1000 core-h; CONJECTURE), so any slice
of it needs a reason from the rung below, as `STRATEGY.md` §2 asks ("score a finite family one rung below").

## Cheapest test

E-261123-01's per-stratum table (week item 1). Kill: the full (8, 3) pass leaves only the two known (equivelar) maps
SAT; then no non-equivelar (9, 4) stratum is run on the laptop.

Source: `reviews/strategy-review-2026-11-23.md` §5 N4, `-codex.md` check D, `-final.md` point 8 (owner-approved 2026-11-23).
