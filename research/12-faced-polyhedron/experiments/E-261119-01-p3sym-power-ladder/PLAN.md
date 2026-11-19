# E-261119-01: P3-sym power ladder on known answers and the symmetric (8, 3) slice by map blocking

Pre-registration (2026-11-19), at most 80 lines. Amendments at the end.

* **ROADMAP row / scores**: T 2 D 1 F 2 G 1 R 2; week item 1, explore, J 0. What differs from E-261118-02 (parked-methods
  rule): known-answer units at the nine-face orbit size (66 / 72 quad orbits) and map blocking by paired runs.
* **Question**: at the nine-face orbit size, does P3-sym discover known objects (free C2 at (8, 36)) and refute known
  negatives ((8, 30), (9, 39)) within its caps, and which maps does the free-C2 (8, 36) slice hold?
* **Hypotheses moved**: H-261101-07 (only through a new (8, 3) map). I-261119-02: tested (discovery and refutation
  rungs). The nine-face UNKNOWN of E-261118-02 is read by its outcome: power at 66 orbits or not.
* **H1 / H0**: H1 = U1 returns a realized model within 1.5 h and U2 or U3 ends INFEASIBLE within 1 h; H0 = U1 UNKNOWN
  (no discovery power at 66 orbits) or both refutation units UNKNOWN (no refutation power). Mixed outcomes are recorded per unit.
* **Why**: the free-C2 (8, 36) formula holds every symmetric uniform (8, 3) solid (I-261119-02 lemma, PROVED-1 sketch),
  both known objects included; (8, 2) and (9, 3) are decided negatives at formula scope (STATUS 3d).
* **Method**: `ladder.py`, `BlockFormula` = `p3sym.SymFormula` of E-261118-02 (imported unchanged; p3.py unchanged) plus
  map blocking. A run (edge) (j, k, a, b) on line L_jk between P_jka and P_jkb has the predicate end_jk(jka) and
  end_jk(jkb) and ed(jka toward P_jkb) and no end_jk(jkm) for each plane m separating the two points (sigma_m differs);
  soundness PROVED-1 (module docstring). A map is blocked by one clause per image of its E runs under the normaliser of
  the action that keeps determinants (384 for free C2 = C2 wr S4, 192 D2, 64 S4; EXACT, computed). Runs are invariant
  under reorientation and the reflection, so the gauge and the mirror do not interact with blocking. On each model:
  decode, GP, invariance, census code, known type, predicate = decode runs (pure-Python twin), bridge (E-261103-03, frozen)
  and `--all-pairs`. Block the map if realized or of a known type (both are realized in this formula by the pinned
  controls); otherwise block only that chirotope (the map stays open). Target S1 at eight faces (never S5 / S0); U2, U3
  are S5 rungs. Counters (SPEC §4): CP-SAT status, seconds, models, decode, GP, invariance, bridge status, core-seconds.
* **Units** (5 workers, seeds 0, 1, ... per model, as E-261118-02): U4 `D2_8_36_block`, `S4_8_36_block` (15 min each,
  together, first); then U1 `C2_8_36_block` (1.5 h, <= 80 models) with U2 `C2_8_30` (1 h, stop on a model); U3 `C3_9_39`
  after U2 (stop on a model), cap min(1 h, what is left of 19.0 core-h with U1 reserved at its cap). At most 10 cores.
* **Unit tests** (`test_ladder.py`, run in this commit, 5 OK, 7 s): normaliser 384 (centralises the half-turn); run
  images; both known objects pinned under free C2: OPTIMAL, invariant, own known type, predicate = decode; pinned
  blocking (own map INFEASIBLE, other map OPTIMAL); synthetic: the same end triples on one line with the other two
  pairings OPTIMAL (chi and cells pinned), the true pairing INFEASIBLE.
* **Controls** (`run.sh controls`, session): E-261118-02's controls rerun (p3sym.py changed after they were recorded);
  normaliser sizes, no forced zero for free C2; both objects in free-C2 normal form pinned: OPTIMAL, EMBEDDED (V E F chi
  24 36 8 -4), invariant, own type; predicate = decode; each pinned with its own map blocked INFEASIBLE and with the other
  blocked OPTIMAL; the synthetic pairing test. Negative controls: the wrong-group and orbit-flipped ones of E-261118-02
  and the own-map blocks. Unpinned blocking controls (`UNITSET=blockctl`, pilot, 300 s each, together): free C2 at
  (8, 36) with Roest-Vigh's map blocked returns Mizhaev's, and the reverse.
* **Pilot** (session, <= 1.0 core-h with the controls): controls; blockctl; then the five run units at `PILOT_CAP=60`
  through `run.sh` with manifests. Exposes build or memory faults, the blocking path on unpinned models, broken records.
* **Pilot gate**: controls PASS; each blockctl returns the other known map (a new realized map -> `candidate-check`,
  stop); every unit builds, solves and records. A blockctl UNKNOWN at 300 s or a failed control: repair once or amend
  with the owner's word. Every run-unit pilot ending by its cap (U4 included) needs a changed set-up or the owner's word.
* **Predictions**: (P1) controls pass (0.95); (P2) both blockctl units return the other map within 300 s (0.6); (P3) U4
  D2 returns Roest-Vigh's map first (0.9) and ends INFEASIBLE within 15 min (0.4); (P4) U1 returns a model within 1.5 h
  (0.8), both known maps (0.6), ends INFEASIBLE (0.3), a new realized (8, 3) map (0.05); (P5) U2 INFEASIBLE within 1 h
  (0.4); (P6) U3 INFEASIBLE within its cap (0.25); (P7) no model in U2 or U3 (0.97).
* **Grid**: one cap per unit (the row's); one seed schedule. The question is per unit.
* **Budget**: session <= 1.0 core-h; owner run <= 19.0 core-h, about 2.3 h wall, one evening; total <= 20 core-h.
* **Power**: decides only what CP-SAT finds within the caps on 5 workers, one host; UNKNOWN carries no information. U1
  measures time to the first model of a 66-orbit formula with a known answer; U2 / U3 time to refute a 66 / 72-orbit
  formula with a known negative answer. Nothing about other caps, seeds, worker counts or nine faces.
* **Proofs**: none. Every INFEASIBLE is UNSAT-SOLVER (planning).
* **Counter calibration**: no float diagnostic enters the verdict; statuses are CP-SAT's; invariance, known type and
  predicate = decode are booleans with controls on both sides (pinned own / other map, synthetic pairings).
* **Scenario move**: none for existence (known answers), unless a new (8, 3) map is realized.
* **Outcomes**:
  * U1 / U4 model realized: known type -> blocked, continue; new map with `--all-pairs` PASS -> stop, `candidate-check`,
    escalate (meets E-261112-02's reopening condition). Not realized, unknown type -> chirotope blocked, map open.
  * U1 / U4 INFEASIBLE after blocks: "this P3-sym formula with these blocks is INFEASIBLE", UNSAT-SOLVER (planning); no
    claim on maps left open. U2 / U3 INFEASIBLE: refutation power at that orbit size (UNSAT-SOLVER).
  * U2 / U3 model: stop the run (stop.candidate); decode, GP, Euler, darts, census code, action; transport chi into the
    3d map CNF and evaluate its clause families; bridge; a PASS -> `--target S5`, `candidate-check`, escalate.
  * UNKNOWN at a cap: no information. U1 UNKNOWN with no model -> P3-sym parked for nine faces (no power at 66 orbits).
* **Follow-up tree**: a failed control -> repair. Otherwise record each unit and go to E-261119-02 (C3 nine faces per
  map). No C3 night from this experiment: one needs a changed nine-plane discovery test and the owner's word.
* **Stop rule**: a failed control or blocking control; all units at their caps or decided; a model in U2 / U3; the
  first verified new candidate; or 20 core-h.
* **STATUS / ROADMAP**: row to done with the per-unit verdict; one STATUS line (formula scope, host, caps); I-261119-02
  tested; H-261101-07 note only on a new map.
* **Deviations from the row**: (1) known-type maps are blocked even when a model's bridge fails (their realization in
  this formula is the pinned control); (2) U3's cap may be below 1 h (the budget with the session's 1.0 core-h);
  (3) the unpinned blocking controls run as pilot units (300 s), not as instant session checks.

## Amendments

### 2026-11-19: amendment 1, the unpinned blocking control failed; blocking repaired to all invariant copies

Controls at `c6313628` (`results/controls-normaliser/`): all PASS. Unpinned blocking controls (`results/blockctl-normaliser/`,
300 s, 5 workers each, 0.38 core-h): with Roest-Vigh's map blocked the formula returned Roest-Vigh's map again (171 s,
realized, `--all-pairs` PASS) in a labelling outside the 96 blocked normaliser images; the reverse returned Roest-Vigh's
(101 s; passes). Cause (EXACT, brute force over S8): Roest-Vigh's run set has 8 plane automorphisms, 5 of them free
involutions in 3 classes, so it has 240 free-C2-invariant labelled copies, of which the normaliser reaches 96 (Mizhaev:
4, 1, 96, 96). The blocks were sound but incomplete; the row's "images under the normaliser" do not block a map whose
automorphisms hold non-conjugate free involutions. Repair (allowed once by the pilot gate): block every relabelling of
the run set invariant under the action's permutations (`copy_perms`; each is a copy of the same map, and every model's
map is invariant, so only that map is excluded; a superset of the normaliser images). Unit tests 6 OK (new: 240 / 96
copies, normaliser images inside). Session budget raised to <= 1.6 core-h (blockctl rerun), the owner run to <= 18.4
core-h (`RUN_BUDGET`); U3's cap is what that leaves (deviation 2). Next: controls and blockctl rerun, then the run pilot
on shards 0, 1, 3, 4 at 60 s (U1's formula and blocking path are exercised by blockctl). To the lead: the normaliser
rule under-blocks (Roest-Vigh 96 of 240), relevant to E-261119-02's per-map blocking if it uses it.

### 2026-11-19: amendment 2, controls and blocking controls pass; U4 decided in the pilot; the owner run is U1, U2, U3

At `0cfcf241`: controls PASS (`results/controls/`; invariant copies 240 / 96, normaliser images inside). Blocking
controls (`results/blockctl/`, 0.11 core-h): Roest-Vigh's map blocked -> Mizhaev's in 33 s, Mizhaev's blocked ->
Roest-Vigh's in 41 s, both realized, `--all-pairs` PASS, predicate = decode (P2 held). Run pilot (`results/pilot/`, cap
60 s, shards in the pre-amendment numbering 0, 1, 3, 4; 0.23 core-h): U4 D2 returned Roest-Vigh's map in 2.3 s (realized,
`--all-pairs` PASS), blocked by 48 copies, then INFEASIBLE, 22.4 s in all; S4 returned Mizhaev's in 2.4 s, 16 copies
blocked, then INFEASIBLE, 21.8 s. U2 (8, 30) and U3 (9, 39) built (21 150 / 51 283 variables), solved and recorded
UNKNOWN at 60 s (expected). Every unit exit 0. U4 is decided below its 15-min cap, so it is not rerun (as E-261118-02
amendment 1; same seeds): "the P3-sym D2 (S4) formula at (8, 36) with Roest-Vigh's (Mizhaev's) map blocked is
INFEASIBLE", UNSAT-SOLVER (planning); P3 held. Owner run (`UNITSET` unset): shard 0 U1 (1.5 h) and shard 1 U2 (1 h)
together, shard 2 U3 after U2, cap min(1 h, 18.4 core-h - used - U1 reserved) = 1 h; <= 17.5 core-h, about 2.0 h wall;
session total about 0.74 core-h; all <= 18.3 core-h. Gate passed (controls, blocking controls, every unit records; not
every pilot unit ended by its cap).
