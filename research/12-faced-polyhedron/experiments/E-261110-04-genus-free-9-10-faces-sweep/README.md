---
id: E-261110-04
title: Genus-free sweep at 9 and 10 planes - every pair adjacent, multiple adjacencies allowed, E free
date: 2026-11-10
status: done
concluded: 2026-11-18
verdict: LOW-YIELD@63.8 core-h (no nine-face hit; C3 / C2 cells p >= ~9e-4 rejected each; geo arm below K13)
direction: [DR7, DR18, DR12]
origin: [I-261110-03, I-261110-01, E-261107-01, E-261108-01, E-261110-03]
tests: []
produces: []
preregistered: true
---

> **Done 2026-11-18** (`CONCLUSION.md`, STATUS 3ay). Owner night, 63.8 core-h, controls passed. C3 3+3+3 and C2
> 4 x 2 + 1 at nine planes, E = 45 and 51: no hit in about 3,830 arrangements per cell (10-19 % UNKNOWN at the cap),
> so p >= ~9e-4 is rejected per cell for these families, box and cap only. Geometric boxes at eight planes: no solid in
> 551 / 557 distinct chirotopes, below K13's uniform box; parked. No candidate; E-261101-08 not opened.

> **Amended 2026-11-17, week item 5** (owner-approved night; `reviews/dialogue-2026-11-16-strategy.md` §2 row 5, Appendix A7). One owner night
> <= 80 core-h, 10 shards, nine planes, E in {45, 51}, frozen engine of E-261103-05 (hard model, cap 20 s):
> (1) C3 3+3+3, the rotation (x, y, z) -> (y, z, x), K13's integer box (unit cost: K14, 13.5 s median);
> (2) C2 4 x 2 + 1 with a far plane as infinity (E-261117-02 passed 2026-11-17, STATUS 3av; its seven-plane rate is a
> rung-below number, not a nine-plane forecast; reuse `n2.draw` / `n2.chart`); (3) the geometric-box arm (K13's D2
> 2 x 4 sampler with coefficients +-q^w, q in {2, 3}, cap 15 s, E = 36, baseline the archived K13). Kill: a failed
> control; zero verified hits parks that distribution and cap (299 units without a hit reject p >= 0.01 for that box
> only). What differs from the parked run: no E-261110-03 gate, symmetric families with a measured unit cost (K14)
> instead of "the 8-plane winner"; the PLAN states this and the power. Session checks: `reviews/dialogue-2026-11-16-strategy.md` §6.

> Was: reopened by the owner, 2026-11-16b, as the follow-up of E-261110-03 only (week item 3): runs after a family
> scores >= 10 positives at 8 planes; nine planes, E in {45, 51}; one owner night <= 80 core-h. Needs a new `PLAN.md`.

> Parked by the owner, 2026-11-12; not run. Replaced by E-261112-01/02 (exact ninth-plane cells).
> Historical proposal below is retained, not an active launch instruction. Recovery alone did not establish
> discovery power. No hypothesis change or negative result; future sampling needs a new power statement and PLAN.

## Goal

Target T3 of I-261110-03: nine (then ten) mutually adjacent faces at any genus; nothing is in print for nine
(CLAIMED, web search 2026-11-10). The two (9, 3) solid-first sweeps fixed E = 39; this run frees the genus:
E in {45, 51} at nine planes (genus 4, 5), E = 54 at ten (genus 5), by the parity rule E = 3F mod 6.

Families: the E-261110-03 winner carried to 9 and 10 planes; candidates are C3 / D3 with three orbits, 4 wedges + 1
plane, 5 wedges. Inner solver and exact verification as in E-261110-03; first-witness stop.

What is different from the parked (9, 3) arrangement-first runs (E-261107-01, E-261108-01; `ROADMAP.md` parked
methods): E is free instead of 39, and the family arrives with a measured hit rate from the 8-plane rung.

## Next

Stop rule: the night, or the first exact all-pairs solid (`verify_candidate.py --all-pairs`, then `candidate-check`).
A witness is an S1 object at 9 or 10 faces with its genus and multiplicities reported; never S5 unless its genus is
the minimal one, never S0. No witness -> LOW-YIELD at the budget for that family, with the 8-plane rate as the power
statement.
