# E-261114-02: bridge recovery control (2026-11-14)

* **Verdict: ADEQUATE.** NUMERICAL recovery/timing observations on the registered controls;
  saved-file exact S6 checks substantiate each recovered control, not a new focus witness.
* **Runs:** `results/recovery/`, ten shards on eight workers alongside the two E-261114-01 pilots;
  Cumulative worker CPU counters sum to 0.24828 core-h (<1): an upper bound, since reused workers may be counted twice.
  All units completed before shard caps; no sleep-gap detector or unique-worker CPU total was recorded.
* **Recovery:** 47/48 attempts (97.92%) across sixteen known-realizable chirotopes and three
  optimizer seeds; the sole miss was `realized_23_26110305`. All sixteen recovered on some seed.
  No coordinate warm starts. The >=0.8 prediction/gate passes; no budget-censored recovery unit.
* **Discovery:** 150/150 SAT, ten saved-file S6 PASS, all five previously unrealized maps recovered:
  Lutz 17: 1/30, 32: 3/30, 67: 3/30, 80: 2/30, 93: 1/30. These are (10,2) controls, not (10,3) results.
  All thirty chirotopes per map are distinct; first success in seed order reaches seed 26 (27th model), `model_diversity.json`.
* **Controls / change:** exact input chirotopes satisfy ALL_OPTS; sign-match rejection control passes.
  `pilot.worker` now accepts an optional optimizer seed; the historical default is unchanged.
  Focused regression confirms both streams and rejects a failed reconstruction. Every successful
  bridge output passed `verify_candidate.py --target S6`; transcripts and coordinates are retained.
* **Interpretation:** the bridge usually recovers a known-realizable chirotope, while random SAT
  models often remain unrealized. The registered remedy is >=30 models per target SAT map;
  no realizer detour is earned. A miss neither proves nonrealizability nor excludes a map (SPEC §4).
* **Hypothesis / scenarios:** H-261110-03 stays open, A/B/C unchanged; only the SAT-handling policy
  changes. Next: finish E-261114-01 pilot; use the registered many-model branch if it returns SAT.
* **Verification:** `verification/verify_all.py --quick` ALL PASS; full archive replay skipped by design.
* **Evidence:** `results/recovery/summary.json`, per-shard `results.json` and `manifest.json`;
  pre-registration `9c12d774`. The optimizer search is not exhaustive and the seeds are not claimed independent.
