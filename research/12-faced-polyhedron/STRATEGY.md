# Strategy

Set by the owner on 2026-11-03; changed only by the owner, with a dated entry in the log at the end. `ROADMAP.md`
orders the work under this strategy; `STATUS.md` owns the numbers; `SPEC.md` owns the definitions.

## 1. Targets

* **Focus target: S5 at (10, 4)** (owner, 2026-11-08, lead review `reviews/strategy-review-2026-11-08d.md`), a maximal
  face-neighbourly polyhedron with 10 faces and genus 4: embedded, cubic, every two faces adjacent, exactly three
  adjacencies beyond the 45 pairs (V, E, F, chi = 32, 48, 10, -6). Success is only
  `verification/verify_candidate.py FILE --target S5` PASS with these counts, then `candidate-check`.
  * Why (10, 4): the two smaller minimal-genus cases are decided. All admissible (8, 2) and (9, 3) plain formulas are
    UNSAT-VERIFIED (EXACT, formula scope); the geometric reading "no S5 polyhedron at (8, 2) or (9, 3)" is PROVED-1,
    conditional on census coverage and encoder soundness (`STATUS.md` 3d). (10, 4) is the next case and the first
    genus where every heuristic engine of ours failed; nothing is in print for it (CLAIMED, web check of 2026-11-08).
  * **Gate.** The exact plain route at default settings is out of laptop reach (E-261103-07: 10/10 TIMEOUT; untested
    estimate 1,200-4,900 core-h). A speed-up benchmark decides the compute route: two laptop nights, a campaign on
    GitHub Actions, or none. If no route exists, the owner chooses between an Actions campaign, a return to S0 and
    consolidation only.
  * Symmetric realizations are allowed; uniform symmetric formulas apply only to face-free rotations.
* **Side track: the (8, 2) / (9, 3) negative result.** Consolidate it at low compute (a positive control with pairs of
  multiplicity >= 3, an independent census, a second encoder), then regenerate and archive the proofs and write a note.
  The note says plainly that no independent (human) review took place (owner, 2026-11-08).
* **Compute.** GitHub Actions may be tried as a compute source (owner, 2026-11-08); first a calibration wave on maps
  with known answers.
* **Defining problem: S0 (Szilassi-12, (12, 6)), parked 2026-11-03, not abandoned.** Every S0 result stays as it is
  (FD rows, certificates, witnesses, the engine-score table, the 59-type data, all experiment folders). Work on S0
  resumes when the owner says so or when a focus result transfers (a method that passes R4, a structural fact
  about face-neighbourly maps). The S0 snapshot at parking time is `STATUS.md` as of 2026-11-03.

## 2. Stance: risky, jump-first

* **Compute is scarce** (one laptop, at most 10 cores, free GitHub Actions); ideas are cheap. Prefer methods that
  can succeed in one night over methods that need a campaign.
* **Jump, do not climb.** Evidence suggests a ravine between genus 3 and 4 for handle ladders at nearly fixed planes
  (H-261101-10; the Gauss gate on 21 of 21 type-0 arms; night 7: no engine passes R4). Methods that reach the target
  genus directly get priority: symmetric ansatzes with few parameters (legal for S5), arrangement first (E-261101-16),
  embedded first, planar later (I-261103-01), chirotope-first on small instances.
* **Risky ideas are welcome and killed fast.** Every new engine gets a one-session pilot on the benchmark ladder
  (R1 Szilassi, then a rung with a known answer at the target's size) with a stated kill criterion; a pass earns a
  night, a fail parks the idea with its failure mode written down.
* **Exploration share: one run in two**, not one in four (PROTOCOL 8a), while the focus target has no result.
* **Follow-up rule.** A follow-up of a finished experiment enters the queue only if its outcome changes a decision
  in the scenario table or the focus plan; "the engine was cut by a cap" alone is not enough.
* **The exact side continues at low cost** where it is cheap and reusable for both targets (certificates,
  rank-3 relaxations, the final-polynomial pipeline), never at the cost of a focus night.

## 3. Process

* Hard rules are unchanged (`CLAUDE.md`, `PROTOCOL.md`): pre-registration, exact verification, scoped claims,
  labels, no fabricated results.
* **Weekly lead review** (owner, 2026-11-07): the lead (strongest model) reviews the week's work about once a
  week and writes the week plan; lab sessions execute it with light documentation (`PROTOCOL.md` §8b). The review
  is skipped while no new work exists, and is called early after any result that moves a scenario by 0.1 or more:
  `.claude/skills/strategy-review` in a separate session with the strongest model at high effort; it writes
  `reviews/strategy-review-YYYY-MM-DD.md` and a proposed `ROADMAP.md` order, and changes nothing else without the
  owner's approval.

## Log

* 2026-11-03: created. Focus S5 (9, 3), stretch (10, 4); S0 parked; risky, jump-first stance; exploration one in
  two; follow-up rule; regular strategy reviews. First review under this strategy:
  `reviews/REVIEW_PROMPT_2026-11-03.md`.
* 2026-11-07: owner's process change: weekly lead review with a week plan; lab sessions light and cheap; review
  cadence by elapsed work, not calendar (`PROTOCOL.md` §8b).
* 2026-11-08 (owner's request, lead review M2): §1 no longer names the free C3 ansatz as the natural first ansatz;
  all 8 uniform free-C3 formulas are UNSAT. Targets and stance unchanged.
* 2026-11-08 (owner's decision on lead review 2026-11-08d): focus moves to S5 at (10, 4), gated by a speed-up
  benchmark; the (8, 2) / (9, 3) negative result becomes a side track towards a note marked as not independently
  reviewed; GitHub Actions approved for a trial. Stance and S0 parking unchanged.
