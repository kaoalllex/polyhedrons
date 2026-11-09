# E-261109-03: conclusion

* **Runs**: pre-registration `cd79dda`, pilot `5cc9726`; one owner launch on the laptop, 8 shards, 15 units, all exit 0,
  wall 20-150 s per shard (sum 636 s, one process each = 0.18 core-h). The manifests print `core_hours` 2.49 in total
  because they multiply by `workers: 14` (the machine's cores) although each shard ran one process; the 0.18 is the
  measured single-process figure. Budget <= 1 core-h holds on that figure.
* **Controls**: all passed. Differential test in every shard (8 x 12 perturbations per object, own seeds; earlier 808
  samples in the pilot): 0 mismatches against `ladder_exact.verify`. Pinned positives SAT (Roest-Vigh, Mizhaev, grooved
  k = 2, 3), pinned negatives UNSAT-VERIFIED (grooved swapped k = 2, 3; Roest-Vigh planes with Mizhaev's map), unpinned
  SAT with a clause-checked model: Szilassi (7,1) and Roest-Vigh (8,3).
* **Prediction vs outcome**: map 40 decides without strengthening (~50 %): yes, 40 s. All six UNSAT (~90 %): yes; all
  six UNSAT-VERIFIED (drat-trim): solver 20-81 s, checker 10-46 s. No timeout.
* **Exact verification**: no candidate. Per-unit CNF and proof SHA-256 and checker transcripts are in
  `results/*/results.jsonl` and `*.checker.log`.
* **What may be claimed**: EXACT (computation): `enc2.py`, written from Lemma 5.1 and section 5.1 without INCONS, RFCONS,
  REFLEX1, POC, agrees with the first encoder (UNSAT) on (9,3) maps 40, 43, 10, 30, 48, 5 (one per pattern, `(1,2,3)`
  twice) and with exact geometry on 8 objects and ~1,300 perturbed instances. The encoder caveat of the (9,3) claim
  reads "two encoders agree on six maps and all controls". The embedding characterization of `enc2` (Lemma 5.1 plus
  line-interval parity and segment disjointness) is PROVED-1 at best (AI-written, no review).
* **What may NOT be claimed**: soundness of either encoder on the other 197 admissible maps; independence from the
  author's reading of Lemma 5.1 (same session author wrote both the lemma use and `enc2`); a human-reviewed proof; a
  pinned negative on a target map (none exists at (9,3)); anything about (10,4).
* **Verdict for the direction**: FOUNDATION (audit passed; H-261101-07 credence unchanged).
* **Next step**: week item 5 (union of two matched solids, I-261108-11 stage 1).
* **Rows updated**: `STATUS.md` 3aa, `ROADMAP.md` State `done` and item 4 Done, `experiment-log.md` 2026-11-09.
