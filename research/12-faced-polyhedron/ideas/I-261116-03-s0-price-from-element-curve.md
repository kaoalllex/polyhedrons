---
id: I-261116-03
title: S0 per-type price from the element curve - is an exact asymmetric decision of the 59 types a laptop campaign?
date: 2026-11-16
status: open
direction: [DR8]
origin: [I-261114-03, E-261110-06, E-261114-01]
---

## Idea

Fit the normalised median solve time against the element count (9, 10, 11 from E-261114-01 and E-261110-06, 12 from
the (11, 5) probe) and extrapolate to S0 (13 elements). The (10, 4) / (9, 3) mean ratio is about 15 (68 s against
4.4 s); at that factor an S0 type costs about 4 h and the 59 types about 3 nights, less than an (11, 5) sweep of 3986
maps (about 14 nights). A scenario, not a bound: S0 has no doubled-pair encoding. The asymmetric S0 embedding
formulas were never run with our encoder (`results.md`, Track 3).

## Why / cheapest test

S0 is the defining problem; its 59 formulas are few. Cheapest test: E-261116-03, ten types at a 4 h cap, only if
the (11, 5) median is <= 20 min. Untested proposal.

Source: `reviews/strategy-review-2026-11-16.md` §5 (N4).
