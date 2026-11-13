# E-261113-01: conclusion

2026-11-13. Part (a) ran in the prep session (amendment 1 and the part (a) section of `PLAN.md`); part (b) is one owner
launch (`launch.sh 13-01 start`), 10 shards, root `results/run/`, commit `b6bcdf3c` in every attempt manifest, tree
clean except the untracked `results/run/`, `queue.json` sha256 `2ec652e8...ce7c` and `no_proof: true` as pinned,
Python 3.14.6, kissat 4.0.4 (`8af8e56f`). One start per shard, no restart.

* **Runs**: (a) seconds in the session, no solver (`results/a/tetra.json`). (b) started 11:29:00 UTC, every shard
  `SHARD-COMPLETE`, `exit_status 0`, all ended by 11:29:15 UTC: wall **15 s** of the ~1 h plan; **0.034 core-h** of
  the 10 core-h cap (sum of `core_hours` in the ten attempt manifests; pilot 0.005 core-h). No sleep gap. Per shard:
  the two convex f10 controls, then one formula (shards 0-5: C3 on Lutz #1, 2, 4, 8, 14, 15; 6-7: free C2 on #6, #12;
  8-9: the two free C2 classes of #20).
* **Controls**: prep c1-c7 pass (amendment 2). In all 10 shards the encoder controls report `CONTROLS-PASS` and the
  convex f10 positive is SAT with `model_checked`, the negative UNSAT-SOLVER (20/20). Every formula ended
  UNSAT-SOLVER, a constant outcome; the measuring path returns SAT on the same code for both ansatzes when an
  object exists (c3, c5 free C2 unpinned SAT and realized; c7 C3 with a fixed face SAT unpinned), and c6 shows per
  formula that the symmetric gp-only part is satisfiable, so the UNSATs come from the polyhedron clauses.
  Pilot reproducibility: #1 and #6 have the same CNF SHA-256 and outcome in pilot and run.
* **Results**: (a) 816 units, 0 EMBEDDED (amendment "part (a) run"). (b) 10/10 formulas **UNSAT-SOLVER**, 0 SAT, 0
  TIMEOUT; kissat time 0.4-0.6 s for the six C3 formulas, 1.9-4.1 s for the four C2; 11,167-11,175 variables,
  151,827-152,506 clauses, 10 distinct CNF SHA-256 (`results/run/*/results.jsonl`). `summary.py`: "ALL-UNSAT-SOLVER".
  No bridge run, no candidate.
* **Prediction vs outcome**: P1 ((a) no EMBEDDED, ~70 %) held. P2 (>= 8 of 10 decided, ~50 %) held, 10/10 in
  seconds. P3 (a SAT formula, ~15 %) not observed. P4 (c5 passes, ~60 %) held in prep.
* **Exact verification**: nothing to verify (no SAT, no EMBEDDED unit); no UNSAT used as evidence, no proofs.
* **What may be claimed**: (a) family scope (T-symmetric realizations of Lutz #15, `SPEC.md` §4.2): no embedded
  realization of Lutz #15 whose rotation symmetries act as Aut+(#15) = T; exact computation by `tetra.py` over all 48
  equivariant labellings and every interval and wall of `t` (exact rationals; not in `verify_all`), coverage by the
  reduction and interval constancy, both PROVED-1 (this experiment, unreviewed). Cause: every equivariant labelling
  puts map vertices on the forced quadruple points for every `t`. (b) instance scope: kissat returns UNSAT without a
  checked proof on each of the ten symmetric formulas; this ranks the C3 / free C2 ansatzes of these maps below the
  asymmetric formulas for search, nothing more.
* **What may NOT be claimed**: that any of these maps, or (10, 3), has no S6 realization, or no symmetric one; any
  negative from (b) (UNSAT-SOLVER, `SPEC.md` §4). Not run: proofs for (b) (owner, 2026-11-13); C2 with two fixed faces
  (#15, 16, 17, 19, 20; I-261113-04, nonuniform encoder); improper symmetries (the screen took rotations only); other
  groups on #15 (only T acting as Aut+); the eight maps without a rotation; a second solver.
* **Verdict for the direction** (DR19 / DR8 / DR18, S6 at (10, 3), symmetric rotation ansatz): **OPEN@0.034 core-h**:
  the ten uniform C3 / free C2 formulas are exhausted with UNSAT-SOLVER and the T family of #15 with 0 EMBEDDED; the
  asymmetric formulas stay at 20/20 TIMEOUT (STATUS 3af). No scenario move ("(10, 3) exists" stays 0.25, CONJECTURE);
  H-261110-03 stays open; S0 table unchanged.
* **Next step**: the registered branch "all UNSAT-SOLVER -> scoped search outcome, a replay with proofs only on the
  owner's word" is taken; no new ROADMAP row. Week item 2 (E-261113-02) next. For the lead: the remaining symmetric
  routes at (10, 3) are fixed-face C2 (I-261113-04, deferred) and improper symmetries.
* **Rows updated**: `STATUS.md` section 3ag and "As of"; `ROADMAP.md` E-261113-01 State `done`; H-261110-03 evidence;
  I-261113-01 `tried`; `experiment-log.md` (2026-11-13).
