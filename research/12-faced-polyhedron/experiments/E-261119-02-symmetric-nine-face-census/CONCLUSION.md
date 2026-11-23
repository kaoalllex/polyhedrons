# E-261119-02: conclusion

**SYMMETRIC-NINE-FACE-ROUTE-ENDS-AT-GENUS-4 (formula scope)**: no C3 3+3+3 or C2 4 x 2 + 1 map with a SAT uniform
symmetric formula at genus 4, no C3 map at genus 5, and none among a uniformly random 10 % of the C2 4 x 2 + 1 (9, 5)
list. Every decided formula is UNSAT-SOLVER (no proof): planning evidence, never a negative result. This conclusion
covers amendment 6 (pass 1 on the random 10 %); stages A, B and amendments 1-5 are in STATUS 3be-3bh and the README.

* **Runs** (amendment 6, owner launch, `STAGE=B5p1`, 10 shards, lean, kissat seed 0, cap 5 s, no proofs): chunks 0-9
  of the frozen random order (seed 2611220601; 97830 of 978228 maps, one rotation group each). Started 2026-11-22
  07:22Z, stop requested during chunk 5 at 08:03Z, resumed 08:54Z (claim files, recorded units skipped), last
  shard finished 09:40Z: ~1.4 h of running wall. **14.32 core-h** (sum of the per-shard `SHARD-COMPLETE wall_seconds`
  in `results/stageB5-pass1/*/night.log`, controls included) against the projected ~14.3 and the 20 core-h cap. The
  manifests (`results/stageB5-pass1-c*/*/manifest.txt`) hold start, finish and exit status per launch; the stop
  reason and the cap ledger are in the `night.log` lines, not in the manifests (the committed logs drop the per-map `map N start / UNSAT-SOLVER` lines,
  which `results.jsonl` repeats).
* **Audit** (`audit_pass1.py` -> `pass1_summary.json`, session, stdlib only): 97830 of 97830 planned maps have exactly
  one final record, every one `UNSAT-SOLVER` with `ended_by: completed`; 0 duplicates, 0 TIMEOUT, 0 UNKNOWN, 0 SAT.
  The 5 `SKIPPED-STOP` records of chunk 5 (units in flight at the stop; maps 0, 268, 279, 414, 417) each have a later
  final record. Solver time per map: max 2.01 s, mean 0.158 s. The ten maps files match the SHA-256 pinned in
  `pass1_9_5.json`. The SHA-256 of every shard's `results.jsonl` is in `pass1_summary.json`; the 77 MB of lean records
  themselves stay untracked (lean output; rebuild by the committed runner from the pinned inputs).
* **Controls** (all passed, on every one of the 100 shard-chunks): the pinned f9 positive (SAT, model checked) and the
  wrong-pairing negative (UNSAT-SOLVER), 10 + 10 per chunk. The lean (8, 3) rung and the B5p1 smoke of the amendment-6
  checks (README) repeated the recorded statuses and hashes before the launch.
* **Prediction vs outcome**: T1 (every record decides within 5 s, 0.85) held, max 2.01 s; T2 (no SAT, 0.9) held;
  T3 (within 20 core-h, 0.9) held, 14.32.
* **Power** (both lines are formula scope, and describe the sample, not any map outside it):
  rule of three on 97830 of 97830 decided with 0 SAT: the per-map rate of SAT formulas is < 3.1e-5 (95 % upper
  bound). Finite population: the 10 % is a uniform sample without replacement of the 978228; a single SAT formula
  escapes it with probability 0.90, M = 10 with 0.35, and the largest M not rejected at the 5 % level (hypergeometric,
  P(0 SAT in sample) >= 0.05) is **28**, so at most 28 SAT formulas among the 978228 at 95 %. The two lines are
  consistent: the second is the weaker statement about the full list. A SAT formula concentrated in a stratum the
  random order under-sampled is not excluded by either line.
* **What may be claimed**: 97830 of the 978228 C2 4 x 2 + 1 (9, 5) maps, a uniform random sample, have an UNSAT-SOLVER
  uniform symmetric formula (plane-only, moved chart, one rotation group per map, cap 5 s, kissat seed 0);
  with 3bf, every per-map uniform symmetric formula run so far at genus 4 and on this sample at genus 5 is
  UNSAT-SOLVER. Planning use only.
* **What may NOT be claimed**: any negative statement about a map (no proof checked); anything about the other 90 %
  (chunks 10-99, postponed by the owner), non-symmetric realizations of these maps, mirrors, C2 3 x 2 + 3, other
  genera; "the symmetric route is refuted" (it is closed for the laptop at genus 4, not refuted).
* **Records of the close-out** (week item 5):
  * **862-action note**: the free half-turn inventory of the 790 free-C2 (8, 3) maps is 862 labelled actions, derived
    from Aut+ (review K1, own search from the canonical codes). The stage-A records (822) miss 40 actions on 23 maps
    (17 after Aut+ conjugation, 14 on 13 maps after full map-group conjugation) because `symcensus.py`:344 keeps the first
    action per unit. So the (8, 3) free-C2 stage-A rung is complete as a census of maps, not of actions; amendment 7
    (the conditional symmetric pass, week item 2) skipped because week item 1 left no map UNKNOWN or SAT without a
    realization, so the 40 actions were not run and nothing is claimed about them.
  * **Parity scope correction**: the "up to 42 %" exclusion rate of Lemma P (STATUS 3bi) is pooled by triple-pair
    count; single multiplicity strata reach 16 of 33 and 2 of 4 (NUMERICAL, from the final review row 14, not rerun
    here). It is a rate on priced records, not a rate per map of any list.
  * **Axis-alternation lemma** (C3, fixed vertices alternate along the axis, so b is even, b <= 3; PROVED-1, single AI
    author, one more AI model agrees in the cross-review): a paper item only (OUTLINE B8). Genus 6 already has b = 2 in the census,
    so it prunes nothing new for the laptop plan.
  * **Manifest budget rule** (final review row 12): every future manifest records an aggregate elapsed budget across
    workers and restarts and the stop reason. This run's manifests do not (see Runs); no change to its result.
* **Hypotheses**: H-261101-07 stays open. Its evidence gets this line: at genus 4 and 5 the symmetric nine-face route
  (the two families that every symmetric S1 nine-face object belongs to except Cs, L3) has no SAT formula at formula
  scope; genus 2 and 3 at their maximal cases are already decided at formula scope (STATUS 3d); the other cases are
  open. The `tests:` links of E-261119-02 and E-261119-03 are removed (final review, week item 5).
* **Verdict**: **UNSAT-SOLVER on 97830 of 97830 (random 10 %), 0 SAT@14.32 core-h** (symmetric route closed for the
  laptop at genus 4; the C2 (9, 5) remainder postponed, parity pass with the paper). Not LOW-YIELD: this is a price and
  a sample, the underlying SAT rate being < 3.1e-5 per sampled map.
* **Next step**: none from this experiment. Week items 4 (P6 stage C: the (9, 4) plain pass) and the lead review.
* **Rows updated**: `STATUS.md` 3bm and header, `ROADMAP.md` (item 5, E-261119-02 and E-261119-03 rows),
  `experiment-log.md`, `paper/OUTLINE.md` B8, `hypotheses/H-261101-07*.md`, both READMEs.
