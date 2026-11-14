# E-YYMMDD-NN: <short title>

Pre-registration, at most 80 lines (`PROTOCOL.md` §8b). Fill in and commit BEFORE any compute (`PROTOCOL.md` §2). Do not edit after the run starts;
add dated amendments at the end instead.

* **ROADMAP row / scores**: T _ D _ F _ G _ R _ (T + D >= 3 required)
* **Question**: one sentence.
* **Hypotheses moved** (the `tests` of the README header) and how each outcome moves them:
* **Hypothesis H1** (and the rival H0):
* **Why this region / type / configuration** (the theory or invariant that motivates it):
* **Method**: scripts, parameters, target (SPEC S0-S4), counters used (SPEC §4).
* **Controls**: positive (must succeed: ...), negative (must fail: ...).
* **Pilot** (minutes; what bug in the idea it could expose):
* **Pilot gate** (PROTOCOL §2.4): the limit that should bind in the long run, and what the pilot must show
  (per unit: the limit that ended it and the budget fraction used; the projected outcome) for the long run to start.
* **Predictions** (written before the run): at least one with a real chance (~30-70 %) of failing, each tied to
  a decision.
* **Grid** (PROTOCOL §2.5): the parameter the outcome depends on and its values, or why one setting suffices.
* **Budget**: core-hours, wall time, shards (`matrix.json`), where (laptop / Actions).
* **Power statement**: what the budget can and cannot detect.
* **Proofs**: none by default (UNSATs are `UNSAT-SOLVER`); DRAT only for a named negative claim or on the owner's word.
* **Counter calibration**: for every float diagnostic in the planned verdict, a control input on each side of its
  threshold (a saturating measure is not a measurement).
* **Scenario move**: how each outcome moves the three credences of the `ROADMAP.md` decision point (A exists /
  B all OM-UNSAT / C OM-SAT but non-realizable), one line each.
* **Outcomes and their meaning** (decided now):
  * SAT / found: ...
  * UNSAT: ... (scope of the formula)
  * timeout / UNKNOWN: no information; next step ...
  * near-miss: counts only if non-degenerate and exactly re-checked
* **Follow-up tree**: the conditional next steps allowed without a new amendment (`PROTOCOL.md` §8b).
* **Stop rule**:
* **What changes in `STATUS.md` / `ROADMAP.md` for each outcome**:

## Amendments
