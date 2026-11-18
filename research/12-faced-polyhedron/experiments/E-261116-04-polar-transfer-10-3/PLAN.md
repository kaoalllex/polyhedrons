# E-261116-04: polar transfer of the HLZ (10, 3) vertex realizations

* **ROADMAP row / scores**: T 1 D 2 F 2 G 1 R 2 (T + D = 3). Week item 5; explore, jump 2; I-261116-01.
* **Question**: is some affine chart of the polar of a known vertex realization of a (10, 3) map an S6 object?
* **Hypotheses moved**: H-261110-03 only on a PASS (existence of S6 at (10, 3)); a no-PASS moves nothing.
* **H1 / H0**: H1: some chart of some object passes `--target S6`. H0: none does (scope below).
* **Why**: polarity maps vertex planes to face planes and edge lines to edge lines exactly; only embeddedness is not
  preserved (`literature/README.md`: no transfer by duality, a general statement, not a test of these objects).
* **Data** (untrusted, read-only, never run): `literature/eg-models-2006.02.001/` from EG-Models 2006.02.001 (HLZ),
  obj archive sha256 `27a99831...ad1`; 20 files, 17 in the 5x5x5 cube (the registered objects), 3 larger ones
  (26888, 28962, 29173) run as extras and reported separately. Faces of each obj are the triangulation; no Lutz match.
* **Method** (`polar_transfer.py`): planes h_i = (v_i, 1); dual vertices x_F (one per triangle, 28); a chart is a
  plane at infinity l; the charts are the cells of {l : x_F . l = 0}, mod l -> -l. Cells found by incremental
  Chebyshev LPs (float, scipy/highs); one interior point per cell; planes h M^-1; each chart through
  `verify_candidate.py --target S6` (exact rational check of the rounded planes, SPEC §4 counters EMBEDDED, PASS).
  Deviation from the ROADMAP wording "exact LP": the LP is float; cells with margin < 1e-7 (unit x_F, |l|_inf <= 1)
  are not enumerated. Counted check: 200000 random l give no sign pattern outside the enumerated set.
* **Target**: S6 at (10, 3) only: single adjacencies, (F, g) = (10, 3), 42 edges. Not S5, not S0.
* **Controls**: positive/negative on one object: octahedron -> cube (the verifier needs cubic vertices, so cube ->
  octahedron cannot be checked). Must give exactly 9 EMBEDDED charts of 52 (pilot result); both signs occur.
  A plain `EMBEDDED` count per object is also reported (non-S6 reading needs no extra check).
* **Pilot** (done before this commit, not a result): control run; object 14542 with 1 and 120 charts, 0 pass.
  Per chart ~0.08 s, ~2850 charts per object: ~4 min per object, ~10 min on 10 shards (ROADMAP said "seconds").
* **Pilot gate**: control must give 9 of 52 in every shard before maps run (`run.sh` enforces it).
* **Predictions**: (a) no chart of any 5x5x5 object passes S6, ~90 %; (b) some chart of some object is EMBEDDED
  (any adjacency, not necessarily S6), ~40 %: informative either way.
* **Grid**: all cells; no parameter. MIN_MARGIN 1e-7 fixed.
* **Budget**: ~0.5 core-h total, laptop, 10 shards (`matrix.json`), no proofs. Run from `run.sh` (never `caffeinate`
  needed at this size but allowed). Stop rule: all 20 objects done or a failed control.
* **Power**: tests these 17 (+3) realizations in all charts with margin >= 1e-7. It does not test other
  realizations of the same maps, other maps, or vertex positions near-degenerate. No claim for (10, 3) existence.
* **Proofs**: none. A no-PASS is a finite computation labelled NUMERICAL, instance scope; no negative claim.
* **Counter calibration**: no float diagnostic enters the verdict except the cell margin (control: the 52 cells of
  the control are all found, so MIN_MARGIN does not drop cells there).
* **Scenario move**: PASS -> `candidate-check`, escalate, S6 (10, 3) existence (A up). No PASS -> no change to A/B/C.
* **Outcomes**: PASS: exact verify of the file, `candidate-check`, then lead. EMBEDDED-but-not-S6 charts: record
  counts. Failed control or error: investigate, no blind retry. Timeout: not a result.
* **Follow-up tree**: none PASS -> park I-261116-01 with the count of charts tried and the EMBEDDED counts. PASS ->
  escalate; no further experiment without the lead.
* **Stop rule**: as Budget.
* **STATUS / ROADMAP**: outcome row in STATUS, ROADMAP State; ledger by `experiment-conclude`.

## Amendments

### 2026-11-16, after the run (no PLAN item changed)
* Result: 0 EMBEDDED, 0 PASS in 56137 charts, so prediction (b) failed. The constant 0 was checked before
  interpretation: the octahedron -> cube control gives 9 of 52 (both signs), but it is convex and genus 0. Added
  `control_szilassi.py` (polar of the embedded Szilassi polyhedron through the same pipeline): 307 cells, exactly 1
  EMBEDDED and PASS `--target S6` at (7, 1). So the pipeline finds an embedded chart when one exists (genus 1).
* Reading of the failures (one object, every 20th chart): 7-10 of 10 faces non-simple and 17-24 bad face pairs.
