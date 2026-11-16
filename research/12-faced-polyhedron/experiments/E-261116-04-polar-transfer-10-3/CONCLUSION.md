# E-261116-04: polar transfer of the HLZ (10, 3) vertex realizations

* **Verdict: NO-CHART-EMBEDDED@1.37 core-h** (10 shards, 435-518 s each). NUMERICAL, SPEC §4 instance scope: the 20
  EG-Models 2006.02.001 realizations (17 in the 5x5x5 cube, 3 larger), polar planes, every chart whose cell has
  margin >= 1e-7. No candidate.
* **Prediction vs outcome:** (a) no PASS: held. (b) some chart EMBEDDED (non-S6): failed, 0 of 56137 (17 registered
  objects: 48 224 charts, 2771-2858 per object; the 3 larger ones: 7 913). H0 holds in its scope; the 17 and the 3 behave alike.
* **Controls:** octahedron -> cube, 9 EMBEDDED of 52 in every shard (both signs). The all-zero outcome is constant,
  so a control with the other sign at higher genus was added after the run (`control_szilassi.py`, PLAN
  Amendments): Szilassi polar gives 307 cells, 1 EMBEDDED = PASS `--target S6` at (7, 1). Cell coverage: 200000
  random l per object give no sign pattern outside the enumerated cells (0 for all 20).
* **Claims:** for each of the 20 given realizations, no affine chart of its polar planes is an embedded polyhedron
  (NUMERICAL, instance scope; float LP, cells thinner than 1e-7 unenumerated; verifier on planes rounded at 1e-9).
  Each of the 20 vertex-minimal (10, 3) maps is covered by one realization. Must not be claimed: anything about
  other realizations of the same maps, a non-existence of S6 (10, 3), UNSAT or a geometric negative, S5 or S0.
* **Not run:** exact-arithmetic cell enumeration; other realizations of the same maps; polar of non-general position.
* **Hypotheses:** H-261110-03 unchanged; S0 A/B/C unchanged. I-261116-01 parked with 56137 charts tried.
* **Next:** week item 5 done; the plan has no further items. The lead decides the next S6 step and the replay
  I-261116-05.
