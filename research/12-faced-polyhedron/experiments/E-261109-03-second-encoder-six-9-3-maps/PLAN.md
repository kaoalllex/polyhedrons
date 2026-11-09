# E-261109-03: second encoder on six (9, 3) maps

Pre-registration (`PROTOCOL.md` §2) of `ROADMAP.md` week item 4 (idea I-261031-03), committed before any solver run.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2 (week plan item 4, lead review 2026-11-08c §7 idea 1); T + D = 4.
* **Question**: does an encoder written independently of `omsat.py` / `pilot.build` give the same verdict on six (9, 3)
  maps and on the pinned controls?
* **Hypotheses moved**: H-261101-07 only through the encoder caveat of the (9, 3) claim (item 4 follow-up tree).
* **H1**: all verdicts agree (every target UNSAT, every pinned positive SAT, every pinned negative UNSAT). **H0**: some
  instance disagrees (encoder bug on one side; the (9, 3) claim is suspended, escalate).
* **Method** (`enc2.py`): own CNF writer and solver driver (`~/bin/cadical`, DRAT, `~/bin/drat-trim`); no import of
  `omsat`, `omsat_validate`, `pilot`. Variables: the 210 signs chi of 10 elements (9 planes + infinity). Clauses: 3-term
  Grassmann-Plucker on all 5-subsets, gauge units (chi(0,1,k,inf) = + for k = 2..8; chi(0,2,3,4) = + by reorienting
  0 and inf together; sound by the gauge group action), and the embedding conditions written from Lemma 5.1 and
  section 5.1 only: (a) for each non-vertex triple, not (P in F_X and F_Y and F_Z); (b) on each line L_XY the 7 triple
  points are ordered by chi (section 5.1); membership of the gaps in F_X, F_Y is the crossing parity from the left
  (transversal crossings of the other edge segments, run ends by the side bits, collinear segments of the pair count
  as boundary), and a gap lies in both faces iff it lies in a prescribed shared segment (this replaces "F_X cap F_Y =
  e_XY" for m >= 2 segments); (c) the segments of one pair are pairwise disjoint. No INCONS, RFCONS, REFLEX1, POC.
  Soundness is PROVED-1 at best (AI-written, `SPEC.md` §5); it is exercised by the controls below.
* **Maps** (census `maps_9_3.json`, admissible, one per pattern): 40 and 43 `(1,2,3)/(2,3)`, 10 `(1,1,2,2)/(2,3)`, 30
  `(1^4,2)`, 48 `(1,1,1,3)`, 5 `(2,2,2)/(2,2,2)`. Reference verdict: UNSAT-VERIFIED of the first encoder (STATUS 3).
* **Controls** (before any target; failure stops the run): (1) differential test: for the Roest-Vigh, Mizhaev, Szilassi
  and grooved-box (k = 2, 3) planes and 200 random perturbations of each, the pinned chirotope satisfies the `enc2`
  formula of the object's own map iff `ladder_exact.verify` says EMBEDDED (0 mismatches; planes and maps from the
  existing control files, read as data); (2) pinned positives SAT with a clause-checked model (unit-propagation
  complete, so no timeout); (3) negatives UNSAT: Roest-Vigh planes against Mizhaev's map, the swapped-pairing maps of
  E-261109-01, and each target map pinned to a chirotope of another map's realization when one is available.
* **Pilot**: map 40 with solver cap 600 s, DRAT checker cap 600 s, one worker. Gate: the (b) parity encoding finishes
  building in < 60 s and map 40 decides in < 600 s. If not, one amendment adds one pre-registered strengthening at a
  time (first the first encoder's INCONS / RFCONS, then REFLEX1 / POC), each recorded; the strengthened encoder is no
  longer fully independent and the conclusion must say so.
* **Predictions**: map 40 decides within the cap without strengthening (about 50 %); all six UNSAT (about 90 %).
* **Grid**: one setting; the cap is per unit (default 1800 s solver, 1800 s checker, from the pilot).
* **Budget**: <= 1 core-h by the row for the six targets (shards run in parallel, 8 shards, laptop; units that time
  out are TIMEOUT, not results), controls < 0.1 core-h. One owner launch; nothing multi-hour from a session.
* **Power statement**: six maps of 203 and the pinned controls detect an encoder bug that changes a verdict on these
  instances; they cannot show soundness for other maps or a bug that preserves every verdict here.
* **Counter calibration**: no float diagnostic enters the verdict; exact rational chirotope signs only.
* **Scenario move**: none by itself (A / B / C unchanged). Agreement strengthens B only through the encoder caveat.
* **Outcomes**:
  * all agree, all controls pass: the claim's caveat reads "two encoders agree on six maps and all controls";
  * any disagreement: stop, (9, 3) claim suspended, escalate, record the instance and both CNFs' hashes;
  * target SAT in `enc2`: `candidate-check`, first-encoder replay, exact realization attempt; not a result before it;
  * TIMEOUT: no information; the encoder is judged unusable at this cap, not wrong.
* **Follow-up tree**: agreement -> note-package soundness chain may cite it; timeouts -> pilot amendment above.
* **Stop rule**: the six targets and controls ended, a control failure, a disagreement, or two sessions.
* **STATUS / ROADMAP**: agreement -> STATUS 3 line and the item 4 "Done"; disagreement -> STATUS claim marked suspended.

## Amendments

### 2026-11-09: pilot (session, before the owner launch; no plan change)

* Code at commit of this amendment: `enc2.py`, `difftest.py`, `solve2.py`, `units.py`, `run.sh` (8 shards, 15 units:
  7 pinned controls, 2 unpinned SAT controls (Szilassi (7,1), Roest-Vigh), the six targets; each shard first reruns the
  differential test with its own seed, 12 perturbations per object, and stops on a mismatch).
* Differential test, 808 samples (100 perturbations x 8 objects; amplitudes 3-30000 on planes scaled by 1000), plus
  Szilassi: 0 mismatches against `ladder_exact.verify`; both classes occur for every object that has a perturbation
  class (Roest-Vigh 34 EMBEDDED / 67 not, Mizhaev 32 / 69, grooved k = 2: 85 / 16, k = 3: 82 / 19; swapped-pairing and
  cross maps: 0 / 101 each). Szilassi's own planes are non-uniform (zero minors), so only its perturbations are used.
* Targets: map 40 UNSAT-VERIFIED (solver 32 s, drat-trim 19 s, 20,485 variables, 84,013 clauses) and map 30
  UNSAT-VERIFIED (65 s, 37 s) with the unstrengthened formula (no INCONS/RFCONS/REFLEX1/POC): the pilot gate holds
  (build < 60 s; map 40 < 600 s), no strengthening amendment is needed. Pilot results are not experiment results:
  these two units are rerun in the launch.
* Not run: a pinned negative for a target map (no known (9, 3) realization exists to pin).
* Launch cap per unit 1800 s solver + 1800 s checker; expected total about 10 core-min, worst case far above 1 core-h
  only if several units hit both caps (then TIMEOUT, reported as such).
