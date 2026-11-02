---
id: I-261102-01
title: Adaptive time per seed on the target (successive halving / restarts), with the progress signal calibrated on the benchmark ladder
date: 2026-11-02
status: open
direction: [DR8, DR17]
origin: [E-261101-26, E-261101-25, owner]
---

## Idea

On the 12-face target, give a seed more wall time while it shows progress and stop the hopeless ones early
(successive halving: run all seeds for a short budget, keep the better half by a progress signal, double the
budget, repeat), or use Luby-style restarts if time to success is heavy-tailed. On the benchmark ladder itself the
budget stays fixed per rung, so engines remain comparable.

## Why it might help

E-261101-25 / E-261102-02 give every seed the same 40 minutes; most seeds end at TIME-CAP. If a cheap signal
predicts which seeds will succeed, the same night tests several times more seeds, or runs the promising ones much
longer.

## Cheapest test

From night 7 (E-261101-26) data, no new compute: (1) the distribution of time to success per rung (heavy tail ->
restarts; light tail -> longer budgets); (2) does the progress signal in `progress.jsonl` (realized wrong signs per
alternation, final-polynomial FEASIBLE vs NONREALIZABLE) separate the seeds that succeed from those that do not, on
R6k and R4 where the answer is known? Check the signal on controls on both sides before using it
(`reviews/strategy-review-2026-11-01.md` 5.1: `hemisphere_margin` looked like progress and was a floor). If it
separates, E-261102-02 gets an amendment with the halving schedule before it runs.

## Result of the cheapest test (E-261101-26, 2026-11-02)

The time per seed was never the binding limit: every failed unit stopped at the 20-alternation cap after 15-39 % of its
budget. Per alternation, successes look roughly memoryless (after 3-16 alternations, about 2 % per alternation at
k = 7), and the wrong-sign trajectory does not separate successes from failures (n = 6 successes). Successive halving
has no signal to select on in this data; the open knob is the alternation cap (`--alt`), not the minutes
(`CONCLUSION.md` of E-261101-26). Status stays open: n is small, and the one alternative signal, final-polynomial
labels, showed no pattern either.

## Source

Owner's question in the session of 2026-11-02 (should the per-seed timeout grow with the chance of success).
