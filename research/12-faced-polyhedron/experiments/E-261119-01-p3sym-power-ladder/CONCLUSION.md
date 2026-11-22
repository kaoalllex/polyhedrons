# E-261119-01: conclusion

**Discovery PASS, refutation UNKNOWN; the symmetric (8, 3) slice OPEN after its two known maps**: unpinned P3-sym with
free C2 at (8, 36) (66 quad orbits) returned Mizhaev's map in 59 s and, with it blocked, Roest-Vigh's in 81 s, both
realized; with both blocked it ran 5257 s to the 1.5 h cap, UNKNOWN. Free C2 at (8, 30) and C3 3+3+3 at (9, 39), both
predicted INFEASIBLE by STATUS 3d, ended UNKNOWN at 1 h. U4 (D2, S4 with blocking) was decided in the pilot (amendment 2).

* **Runs**: PLAN `c6313628`, amendments `0cfcf241`, `0de9a2f8`. First owner launch at `3a8112fc`, 2026-11-19
  19:10:05 UTC: shard 2 (U3, still waiting for U2) ended 19:45:38 and shards 0, 1 (U1, U2) 20:01:14, all with no
  record and `exit_status: 0` (the pattern of the launcher's stop, then kill; no sleep in the power log; the reason is
  not recorded); 2 x 51.2 min x 5 workers = 8.53 core-h spent and discarded, the units in flight rerun from their
  start. Second launch at `ba349496`, 2026-11-20 06:24:59-08:25:06 UTC (2 h 0.1 min against about 2.0 h), no sleep, AC:
  U1 and U2 together, U3 from U2's end (cap min(1 h, budget left) = 1 h); shards 3-9 idle by design; every
  `exit_status: 0`; `dirty_files: 10` are the untracked result folders. Unit records (`ladder.py summary results`):
  7.50 + 5.00 + 5.00 = 17.50 core-h against <= 17.5. With the session (about 0.74) and the discarded launch, about 26.8
  core-h against the PLAN's hard <= 20: an overrun of 6.8 core-h, all of it in the discarded first launch. Python
  3.14.6, OR-Tools 9.15.6755, `ladder.py` / `p3sym.py` / `p3.py` SHA-256 identical in both launches' manifests.
* **Controls** (amendment 2): controls and both unpinned blocking controls PASS; in-run positive: U1's two known maps.
  The refutation units have no in-run negative control beyond 3d's decided answers, which they are.
* **Results** (`results/{0,1,2}/results.jsonl`): U1 (21 150 variables, 133 167 constraints): OPTIMAL 59.1 s
  (Mizhaev, 96 copies blocked), OPTIMAL 80.6 s (Roest-Vigh, 240 copies blocked), then UNKNOWN 5256.8 s. U2 (same size):
  UNKNOWN 3599.8 s. U3 (51 283 / 362 265): UNKNOWN 3600.1 s. No model in U2 or U3, no new map, no stop file.
* **Prediction vs outcome**: P1, P2 held; P3 held (pilot); P4: a model (0.8) and both known maps (0.6) held, ends
  INFEASIBLE (0.3) and a new map (0.05) did not; P5 (0.4) and P6 (0.25) did not; P7 (0.97) held. H1 holds for discovery,
  H0 for refutation (both refutation units UNKNOWN).
* **Exact verification**: both U1 models: GP, invariance, decode, predicate = decode; the bridge's `--all-pairs` PASS
  (V E F chi 24 36 8 -4, `results/0/*.candidate.log`), census codes of the known types. The copy counts 96 / 240 equal
  amendment 1's brute force over S8. Known objects (registered controls): `candidate-check` does not apply. No proofs.
* **What may be claimed** (method scope: one host, one seed, 5 workers): P3-sym finds both known symmetric eight-face
  maps at 66 quad orbits within 2.5 min (EXACT realizations); the first in 59 s against 2.3 s (D2) and 5.0 s (S4) at
  36 / 34 orbits (3bb).
* **What may NOT be claimed**: that the free-C2 (8, 36) formula holds no third map (U1 UNKNOWN; owner's question 5
  stays open); anything from U2 or U3 (a timeout is not a result); that the nine-face UNKNOWNs of 3bb speak against a
  C3 object: P3-sym showed no refutation power at 66 or 72 orbits within 1 h. Not run: other caps, seeds, worker counts.
* **Hypotheses**: I-261119-02 tested (discovery rung passed, refutation rungs undecided). H-261101-07 unchanged.
* **Verdict**: discovery rung PASS; refutation rungs UNDERPOWERED@10.0 core-h (1 h each, 5 workers, one seed); the
  symmetric (8, 3) slice OPEN, UNKNOWN@7.5 core-h after two known maps.
* **Next step**: the follow-up tree's "otherwise" branch: item 2 (E-261119-02 stage A, owner launch). To the lead: a
  P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides; the budget overrun of the
  discarded launch.
* **Rows updated**: `STATUS.md` 3bd and header, `ROADMAP.md` State done, `experiment-log.md` (2026-11-20), README,
  I-261119-02.
