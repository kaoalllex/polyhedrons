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

## Night 7 data (E-261102-03, E-261102-04, 2026-11-03)

* Chirotope-first with the cap lifted: on R6k the successes came after 6-284 alternations (k = 8: 22, 31, 183, 270;
  k = 9: 6, 91, 92, 284), 8/8 within 120 min against 2/20 at the 20-alternation cap; spread like a geometric count
  at ~1 % per alternation (n = 8). For this engine a longer chain was worth it at k <= 9. On the full maps the new
  limits are time and the SAT cost at k >= 10, not the seed.
* Genus-ladder search on R5: every success within 3 min; the two seeds that failed at 6 min failed again at 40 min
  (164-167 restarts each, best energy 1). For this engine the outcome per seed is decided early: more seeds, not more
  minutes, which is the case for restarts / successive halving.
* So the two engines want opposite schedules; a halving schedule needs a signal per engine, still not found for
  chirotope-first (wrong signs did not separate in E-261101-26). Status stays open.

