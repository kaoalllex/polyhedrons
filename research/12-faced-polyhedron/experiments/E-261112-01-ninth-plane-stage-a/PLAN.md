# E-261112-01: ninth-plane Stage A

Pre-registration, 2026-11-12, owner's approved dialogue and filing request. No compute in this filing session.
Status is planned until the prep amendment and launch gates pass; the dialogue checks are prior session data.

* **ROADMAP / scores**: week item 1; T 2 D 2 F 2 G 1 R 2, T + D = 4; explore, direct S1 construction.
* **Question / H1 / H0**: H1: a near-copy ninth-plane cell of either fixed eight-plane source contains a cubic
  nine-face all-pairs solid. H0: none does. Tests H-261112-01; H0 here concerns only its Stage A subset.
* **Why / change from parked runs**: exact finite cells instead of random ninth planes; genus free instead of
  E = 39 (E-261107-01 / E-261108-01). No discovery rate is inferred from the Gaussian seven-plane calibration.
* **Target / scope**: S1, nine faces, all 36 pairs adjacent, cubic embedded surface, simple disk faces, genus
  free; generic open cells over the fixed Roest-Vigh and Mizhaev planes, not walls or arbitrary sources.
* **Method**: adapt the disk-aware `code/solid_cpsat.best_solid` path of E-261103-05 / E-261108-01 to hard all-pairs
  and edge runs >= 39 (not == 39), max_runs = 3. Freeze the exact model, including this restriction, before solving.
  The dialogue's `cells_exact.py`, `stage_a_reps.py`, `stage_a_price.py` are local prototypes, not run artifacts;
  port reviewed code into this experiment, with an explicit lower-bound option instead of the prototype monkeypatch.
  Include infinity in all determinant signs. Verify rational representatives, nonzero signs, unique projective
  keys, and exact symmetry actions; deduplicate the union before orbit reduction. No assumed orbit size.
* **List gate**: independently derive each local rank-3 Zaslavsky count; require equality with distinct feasible
  local representatives, then verify the exact union and orbit partition. Dialogue predictions: Roest-Vigh
  4,024 cells / 1,006 orbits, Mizhaev 3,992 / 998. Stop on a mismatch. Do not compare this subset with the full
  rank-4 count; that is Stage B. Record representative, source, sign-key and orbit hashes before the pilot.
* **Controls (separate correctness from discovery power)**: C0, both eight-plane sources unseeded, same model
  with lower bound 30, must recover an exact eight-face all-pairs solid. C1, delete plane index 0 from each
  source, locate the deleted plane's generic cell in the seven-plane extension arrangement, construct an exact
  representative through the same cell-to-arrangement-to-solver path, then require exact eight-face all-pairs
  recovery. Passing the original plane directly to the solver is not C1. Record full signs and recovered geometry.
  C2, tetrahedron with edge runs >= 7, must be INFEASIBLE through the same lower-bound path. Every shard runs
  C0/C1/C2 first at cap 60 s; UNKNOWN fails the gate as solver-limited, not as a negative. No discovery-power
  claim at nine planes follows from C0/C1. Reuse valid recorded control checks only with unchanged full provenance.
* **Pilot / grid**: after the prep amendment, 10 shards, first orbit of each source in each shard (20 cells),
  cap 60 s, <= 0.5 core-h including controls, charged to the total. Log table-build, solve and CPU time,
  limiting condition and budget fraction per unit. One cap suffices for a finite list; timed-out cells stay open.
* **Pilot gate / prediction**: planning prediction (CONJECTURE, about 50 %): all cells plus controls fit the
  7.3 core-h cap at the measured pilot cost. Require passing controls, a certified list, and measured projection
  within the cap; otherwise stop and escalate the budget/cap before the day run. Recheck D after the pilot.
* **Budget / sharding**: one prep session; <= 7.3 core-h total Stage A computation, controls and pilot included,
  10 shards, at most 10 single-thread workers, laptop on AC under caffeinate. Stable source-interleaved queue,
  unit ordinal modulo 10; total cap overrides per-cell caps. Stop/resume by manifest without redoing accepted units.
* **Power**: exhaustive coverage is earned only for the certified near-copy list if every unit finishes. This is
  not a random sample and has no estimated detection probability. The 251 old UNSAT-SOLVER session decisions
  are not credited as completed units without matching formula, representative and environment provenance.
* **Counters (SPEC section 4)**: SAT/CANDIDATE, UNSAT-SOLVER, UNKNOWN/timeout, ERROR per formula;
  EMBEDDED, adjacent_pairs, nonsimple_faces, bad_pairs on geometry, with V/E/F/genus and multiplicities.
  Store model hashes, rational planes, SAT models, actual orbit sizes, limits and wall/CPU seconds in manifests.
* **Counter calibration**: no floating geometric diagnostic decides a verdict; exact signs and counts do.
  Unit-test the budget boundary below/at/above its cap; time predicts cost only and proves no geometry.
* **Outcomes / follow-up**: SAT is CANDIDATE until `verification/verify_candidate.py FILE --all-pairs` PASS with
  nine faces, then `candidate-check`; stop target work for that verification. Success supports H-261112-01.
  INFEASIBLE without checked proof is UNSAT-SOLVER for that exact model, never a family negative. An exhausted
  list is a scoped search outcome only. UNKNOWN is solver-limited; record unresolved IDs, do not raise caps silently.
  Near-misses and control failures are not results; stop, diagnose, escalate on a repeated failure.
  Stage B needs its own PLAN, full count/orbit certificate and 50-cell timing gate; a Stage A miss does not earn it.
* **Scenario move**: no numeric credence change from this filing, UNSAT-SOLVER or timeout. A verified nine-face
  witness settles the nine-face existence question; genus determines which older scenario row it addresses.
  S0 unchanged. Record changes only after verification; no inference to S5 or arbitrary-source non-existence.
* **Stop rule / ledger**: first candidate, any failed control/count/hash/orbit check, all queued units ended, or
  the aggregate cap. Conclude with scope, completed/unresolved IDs and next gate; update H-261112-01, STATUS and
  ROADMAP in the conclusion commit, with no family exclusion from an unproved solver answer.

## Amendments

**Amendment 1 (prep, 2026-11-12; lab session).** List: `cells.py` ported from the prototypes with exact checks
(each local b verified, per-plane found = Zaslavsky 2 (1 + c2): RV 510 x 8, Mizhaev 508/504; nonzero 84 signs;
symmetries permute D; orbit partition checked per key). Union/orbits: RV 4,024/1,006, Mizhaev 3,992/998, every
orbit size 4 (EXACT, matches the predictions). Representatives: max-margin LP rounded to 1e-9, all 2,004 verified
exactly (no witness fallback). `list/units.json` SHA-256 ef132bc7...b360, pinned in `stage_a.py`; key, orbit and
representative hashes in `list/certificate.json`. Queue: source-interleaved in blocks of 10, so the pilot (first
two units of each shard) is one orbit per source per shard. Formula: `best_solid(target_edges=39,
edges_at_least=True, max_runs=3)`, an explicit option of `code/solid_cpsat.py` (equality path unchanged,
E-261103-05 tests pass); cap 60 s, one worker, hard limit cap + 30 s per unit process. Controls as registered; C1
uses `cells.representative` (LP point, not the deleted plane). Runner: `run.sh` / `stage_a.py`; shard budget =
total / SHARDS over every start (`PILOT=1`: 0.5 core-h, first two units); first SOLID writes `results/CANDIDATE`
and stops all shards; ERROR units keep raw files and do not stop. Startup check through `overnight/launch.sh` with
`BUDGET=1` (2 shards, then 1 after an edit): C0/C1 SOLID (V E F chi 24 36 8 -4), C2 INFEASIBLE, ~10 s per start,
BUDGET-STOP before any unit; records in `startup/`. Unit branch covered by a stub-solver test; no target unit solved.

**Amendment 2 (owner, 2026-11-12, before any target unit).** Budget raised from 7.3 to 12 core-h total (owner's
decision on the pilot-gate escalation, made in advance). Pilot and day run are one launch: each shard's first two
units are its pilot; before its next unit the runner applies the registered gate automatically (both pilot records,
no ERROR, spent + mean pilot wall over all shards x remaining units <= the shard's 1.2 core-h), else exit 6 and the
remaining units wait for an owner decision. Controls, list, formula and cap unchanged; stub-solver tests cover the
gate both ways; startup check 3 (`startup/check-3`) passes as before.
