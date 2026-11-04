# E-261103-04: representation and dart-preserving surgery gates

The combinatorial stages and bounded geometric pilot are concluded. The broader
experiment stays running with its focus recovery gate closed. See the final section
for the pilot verdict and next decision.

## Legacy representation audit

## Runs and controls

Pre-registration `040562a`; control-orientation amendment `2eeb39f`. Both runs used
one core on the owner's laptop through `bash .../run.sh 0`, with the research environment
activated. No scheduler or executable substitution was used. The amended run used the
registered `OUT` override and completed normally.

| Attempt | Wall seconds | Core-hours | Stop reason |
|---|---:|---:|---|
| `results/representation-audit` | 1.294180499999129 | 0.00035949458333309144 | ValueError loading the un-oriented Mizhaev cycles |
| `results/representation-audit-oriented` | 0.7285505420004483 | 0.0002023751505556801 | COMPLETE |
| Total | 2.0227310419995774 | 0.0005618697338887716 | Both manifests retained |

The successful attempt used 0.006071254516670403 of its 120-second wall budget.
The intended binding limit was completion of the finite audit, and it completed.
Preparation and evidence review are outside these measured run totals.

Szilassi round-trips with the same canonical dart code. The parallel-edge negative
control Roest-Vigh fails the legacy conversion as predicted. Mizhaev also fails after
its supplied face cycles are made coherent with the existing review helper. Both
control loading and the positive/negative diagnostic controls pass in the amended run.

All 203 admissible focus maps fail in `coherent_triangles` with the assertion text
`not orientable`. The supplied maps are oriented surfaces. Here that assertion
reports a limitation of grouping edge copies by their endpoint labels.

The first attempt retained the focus outcomes and Roest-Vigh failure, then stopped
on `ValueError: links do not uniquely identify parallel-edge pairing; use dart code`
when loading Mizhaev. The amendment reuses `review.coherent` for supplied face links.
The failed attempt is preserved with its source hashes and exit status.

## Claim and scope

**PROVED-1, implementation scope.** The unmodified triangle-to-links path cannot
represent any supplied (9,3) focus map or either (8,3) recovery control.

In `gauss_degree.coherent_triangles`, the final `seen` set stores ordered pairs of
vertex labels and asserts that each pair occurs only once. A loopless input on F
labels therefore has at most F(F-1) triangle-side occurrences if this assertion
passes. A triangular dual map with E edges has exactly 2E such occurrences. At
(9,3), 2E = 78 > 9*8 = 72. At (8,3), 2E = 72 > 8*7 = 56. The supplied maps are
loopless and have distinct corner triples. Independently of how the BFS orients
those triples, a completed traversal must violate that assertion. Earlier traversal
failure would also prevent the conversion. For Szilassi, 2E = 42 = 7*6, and the
positive control round-trips. This argument has no external human review.

The registered prediction, at least one focus mismatch, holds. Geometric recovery
power and tube decomposition coverage remain unmeasured. No optimization, candidate
verification, SAT call or saved-proof replay ran. Hypotheses H-261101-07 and
H-261103-02 and the A/B/C credences retain their preceding statuses.

## Verdict and next stage

**OPEN, representation gate failed.** This audit diagnoses the current conversion.
It provides no LOW-YIELD or REFUTED verdict on geometric ladders and no S5 existence
or non-existence conclusion. The geometric pilot and night remain unactivated.

Next, prepare a committed amendment for dart-preserving tube removal. Reuse the
census `TriMap` representation and its alpha pairing. Check each surgery for a
connected orientable surface, one vertex-link cycle per face label, distinct corner
triples and the intended Euler characteristic. Check that any sphere endpoint is
a simple triangulation before invoking convex realizability. Do not infer that
all focus maps admit such a chain from the current triangle-only tube finder.
Once chains preserve the original canonical top-map code, register and run R1 and
both (8,3) recovery controls before any nine-plane geometric search.

Evidence is in both `results/*/audit.json` files and their `manifest.json` files.
Output hashes were checked against the manifests. The failed attempt's source
versions are retained in its commit. This audit has no `verify_all.py` integration,
and no EXACT ledger upgrade is made. The unchanged previously checked research
suite is reused for its former scope. Ledger wording and evidence links receive
focused review only.

## Dart-preserving surgery audit (2026-11-04)

The surgery amendment was pre-registered in `5725a38`. Implementation `cfb99e2`
ran from a clean working tree in the activated research environment through the
actual bounded entry point, from the repository root

```bash
STAGE=surgery bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

No executable, scheduler or fixture substitution was used. The run completed
normally with exit status zero and stop reason COMPLETE. The finite search ended
before its wall and state caps. The manifest records 11.100107874999594 wall seconds,
0.0030833632986109983 core-hours, and a budget fraction of 0.03700035958333198.
Including the two legacy attempts, all three experiment manifests sum to
13.1228389169991713 wall seconds and 0.00364523303249976984 core-hours. Preparation,
packing and post-run evidence checking are outside those measured run totals.

| Input scope | Inputs | Checked chains to simple spheres | Unresolved |
|---|---:|---:|---:|
| Szilassi (7,1) | 1 | 1 | 0 |
| Roest-Vigh and Mizhaev (8,3) | 2 | 2 | 0 |
| Admissible frozen focus maps (9,3) | 203 | 203 | 0 |

Every accepted transition preserves outside triangle cycles and surviving alpha
pairings, reduces the genus by one, and passes the direct surface check. The saved
patch check verifies boundary incidence, connected patch vertex links, annulus
Euler characteristic and patch connectivity. Every chain reverses to exactly its
labelled top data and the same canonical code. All sphere endpoints pass the simple
triangulation checks. The negative controls reject a broken alpha involution, a
mismatched tail label and the disconnected cap-triangle fixture. The Szilassi
capped-map compatibility check agrees with the legacy tube finder. H1 for the
registered combinatorial controls holds on the supplied inputs.

### Evidence and reproduction

The immutable run output is retained losslessly as `results/surgery-audit/audit.json.gz`.
Its decompressed bytes have the original `audit.json` SHA-256 recorded in the run
manifest. Compression SHA-256 is
`7abf382cf134792b897cdeb9854ddfb75e1444b35b2e0772951534b12f1c2fcc`.
All declared input hashes were compared both with the run's files and with their
versions in the recorded implementation commit. The original output hash and exact
gzip round-trip equality pass. The manifest retains the original generating code
provenance.

After the run, commit `2ff5953` strengthened the saved checker to compare every top
map with its named census/control input, reject duplicate or incomplete rows, and
read compressed evidence. The saved evidence was checked once with that version

```bash
python3 research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/audit.py \
  --check-saved research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/results/surgery-audit/audit.json.gz
```

It returned `PASS: 206 saved maps, source identities, surface/patch checks and reversible chains`.
The actual transcript is `results/surgery-audit/check-saved.txt`. The search was
not repeated for this additional provenance check. Source binding and all recorded
transitions pass. The checker uses direct permutations and patch edge incidence
alongside the surgery implementation's TriMap operations. It has the same AI author
and no external human review.

### Claim, verdict and next stage

**PROVED-1, supplied-input computation.** Every admissible map in the frozen (9,3)
census, and the supplied Szilassi and two (8,3) controls, has a checked reversible
chain of the registered six-triangle surgeries to a simple sphere triangulation.
This is a representation-readiness claim. It is conditional on the checks in the
recorded implementation and saved checker. The audit is outside `verify_all.py`
and receives no EXACT promotion. Census completeness retains its prior label.

**OPEN, surgery gate passed.** The failed legacy conversion remains documented.
The replacement meets the registered combinatorial gate. Geometric recovery power,
embeddedness at intermediate levels and focus realizability remain unmeasured.
No candidate, SAT call or proof replay was produced. H-261101-07, H-261103-02 and
the A/B/C credences retain their previous statuses. No FD or witness row changes.

The dated geometric recovery amendment in PLAN now registers R1 and both (8,3)
controls with explicit seeds, budgets and stop rules. Next implement that pilot.
Export geometry inputs with preserved face labels and verify the links-to-dart round trip before passing each level to the energy and
exact verifier. Focus geometry remains gated on those recovery controls. The
experiment remains running, with no active process or pending owner launch.

Only experiment-local executable code changed. The actual runner, its structural
controls and the enhanced saved-evidence checker supplied the affected checks.
The previous quick-suite result is reused for its unchanged shared-code scope.
The graph/ledger update receives its required metadata check. No new CI, external
human review, geometric search or sleep telemetry was checked.

## Bounded geometric recovery pilot (2026-11-04)

Pre-registration `871d8cc`, first implementation `5643bc5`, reflected-reference
correction and committed amendment `70347ad`. Both attempts used the activated
`/Users/a.konyaev/.venvs/polyhedra` environment from the repository root, one shard
and one worker. The actual registered entry points were

```bash
source /Users/a.konyaev/.venvs/polyhedra/bin/activate
STAGE=recovery bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
OUT="$PWD/research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/results/recovery-pilot-oriented" STAGE=recovery bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

The first attempt stopped before geometric verification or optimization with
`REPRESENTATION-FAIL: no checked dart-map isomorphism`. The failed reference
alignment treated a reflected dart's tail as the original tail. The correction
uses the original head, checking both endpoints and the triangle/alpha maps.
Its registered reflected-map fixture and all subsequent alignments pass. Both
attempts, their manifests and traceback/stdout/stderr remain immutable.

### Controls, prediction and stopping levels

The amended attempt passed all three published-plane positive controls, all three
duplicate-plane negative controls, and all ten labelled level round trips.
The positive control objectives are zero. Singular negative fixtures receive
controlled INVALID-INPUT rejection. Those objective values are diagnostics.
Exact reports and the saved-file verifier determine acceptance. Lower levels
omit the complete-adjacency requirement, while the top controls check it.
Reference planes were used only for the deterministic controls.

| Recovery unit | Seed | Exactly accepted genera | First rejected genus | `nonsimple_faces` at rejection | `bad_pairs` at rejection | Unvisited genera |
|---|---:|---|---:|---|---|---|
| Szilassi | 10401 | 0, 1 | none | none | none | none |
| Roest-Vigh | 10402 | 0 | 1 | [1, 6] | [] | 2, 3 |
| Mizhaev | 10403 | 0, 1 | 2 | [0, 4] | [] | 3 |

The H1 prediction that all controls recover failed. Each rejected level exhausted
its requested optimizer time and returned objective 2, followed by exact rejection.
The actual optimization times were 45.00141483299922 and 45.00208762500006 seconds,
respectively, or 1.000031440733316 and 1.000046391666668 of the requested time.
Other visited levels stopped at the optimizer's energy threshold, then passed
exact checking. Their times, budget fractions and restart counts are in
`results/recovery-pilot-oriented/recovery.json`. Every visited level retains its
planes and full verifier transcript, including both rejected outputs.

The Szilassi top saved-file check returned

```text
0 {"all_pairs_adjacent": true, "V_E_F_chi": [14, 21, 7, 0], "points_distinct": true, "simple_faces": 7, "nonsimple_faces": [], "edges_consistent": true, "bad_pairs": [], "EMBEDDED": true, "single_adjacency": true, "target": "S5", "PASS": true}
1 record(s), target S5: 1 PASS, 0 fail
```

This is S5 (7,1), the known auxiliary control. All its adjacency multiplicities
are one. The other accepted outputs are auxiliary embedded lower levels. The
Mizhaev genus-one level has 22 adjacent pairs and two doubled pairs. None of the
accepted outputs is the focus S5 (9,3) object. The two (8,3) top geometries passed
only as supplied deterministic controls, with the S1 `--all-pairs` check.

### Independent checking and provenance

The candidate-check adversarial verifier checked all five accepted recoveries with
a standalone rational implementation adapted from E-261103-05's independent
polygon-section checker. It imports neither `ladder_exact` nor `verify_candidate`.
Both rounding scales, 1e-9 and 1e-12, pass. Checks cover cubic topology,
orientability, face simplicity, all pair intersections including absent pairs,
all arrangement triple determinants, four-plane determinants, distinct vertices,
positive edge lengths and duplicate-plane negative controls. The minimum recorded
nonincident plane value after undoing the rationalization scale is about
0.0006908445965. It is a diagnostic for these plane gauges.

The portable checker, driver and hash-bound report are retained in
`results/recovery-review/`. After replacing temporary absolute paths with relative
paths, its actual saved entry point was exercised. The final replay followed a
correction making a REJECT report produce nonzero process exit status

```bash
python3 research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/results/recovery-review/run_check.py
```

It printed ACCEPT for each of the ten (candidate, rounding-scale) checks and
`ACCEPT 5`. Its report binds every input, the generating pilot output, both checker
sources and the reused independent implementation. The original agent-side check took 0.19046429099944362 seconds. Portability and
exit-status corrections were checked on the saved inputs. The final source-bound
replay took 0.18809479199990164 seconds, with its transcript retained as
`results/recovery-review/check-saved.txt.gz`. These post-run checks are outside the
run manifests.
AI agents are not independent human reviewers. The standalone checks are outside
`verify_all.py`, so their evidence label remains PROVED-1.

All output hashes in both pilot manifests pass. The amended run's declared input
hashes match the files used. The unchanged surgery checker source matches commit
`2ff5953` byte for byte. Its saved acceptance transcript and original evidence
hash are reused, without repeating the surgery search or checker.

### Resources, verdict and next decision

| Attempt | Wall seconds | Core-hours | Stop reason |
|---|---:|---:|---|
| `results/recovery-pilot` | 3.625599000000875 | 0.0010071108333335765 | REPRESENTATION-FAIL before geometry |
| `results/recovery-pilot-oriented` | 105.64823350000006 | 0.029346731527777795 | UNDERPOWERED, normal exit 0 |
| Recovery total | 109.27383250000094 | 0.030353842361111372 | Both attempts retained |

The amended attempt used 0.17608038916666677 of its outer wall budget. It ended
by the registered per-unit stopping rules, without the outer cap binding.
Imports took 0.7137856659992394 seconds. Positive objective evaluation including
cached JIT startup took 0.16487816700100666 seconds. Optimization and exact check
timings are separate in the saved records. JIT compilation alone was not isolated.
All five experiment run manifests, including the preceding combinatorial stages,
sum to 122.3966714170001 wall seconds / 0.03399907539361114 core-hours. Preparation,
independent review and metadata checks are outside this sum.

**PROVED-1, supplied-input computation.** The corrected geometric path preserves
the registered control maps and exactly recovers the Szilassi ladder. It also
recovers the saved Roest-Vigh sphere and Mizhaev genus-zero/one levels. All accepted
outputs pass the independent checks at both scales.

**UNDERPOWERED at one seed per control and 45 seconds per visited level.** Full
(8,3) recovery was not demonstrated. The higher levels listed above were not run.
This pilot does not decide whether either rejected intermediate map is realizable,
whether more time would recover it, or whether another surgery chain would help.
The all-control gate for focus geometry remains closed. H-261101-07,
H-261103-02 and the A/B/C credences retain their preceding statuses. No FD/witness
row changes, focus geometry, night, new CI, sleep telemetry or human review.

A possible next calibration amendment would test only the two failed levels,
from their saved exactly accepted parents, on the original 3/10-minute grid and
fixed paired seeds. Its maximum requested optimizer time would be
2 levels x (3 + 10) minutes = 26 minutes on one core, plus a separately bounded
verification/startup reserve. That would measure conditional level recovery,
with full top recovery still open. This is a costed proposal awaiting a decision
and a committed amendment. The time cap alone does not justify a night or an
expansion of focus search. Another option is to reassess the chosen intermediate
maps or chain before spending that budget. The experiment remains running with
no active process and no owner launch command pending.

Only experiment-local recovery code and dispatch changed. The actual entry-point
pilot, exact saved-file checks and independent portable checker supply the affected
verification. Static Python/shell checks and diff/graph metadata checks pass.
The recorded shared-code quick-suite PASS is reused for unchanged scope. No fresh
solver, certificate replay or integrated suite was needed for this isolated path.

## Conditional grid registration and startup (2026-11-04)

The preceding proposal is selected as a conditional calibration, not a repeated
pilot or a focus expansion. Pre-registration `b851f8c`, implementation `3f3aeda`.
The uncertainty is whether either frozen failed level can be recovered from its
saved accepted parent at the original short/night budget choices. A success can
select a budget for a separately registered continuation. No accepted cell would
justify another cap increase without reassessing the intermediate maps or chain.
No probability estimate or production/night power claim is made.

The actual entry point was exercised once in the activated research environment
from the repository root, with no executable or scheduler substitution:

```bash
STARTUP_ONLY=1 STAGE=calibration bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

It returned STARTUP-PASS, exit zero, using 1.7459750840025663 wall seconds /
0.00048499307888960174 core-hours, fraction 0.014549792366688052 of its cap.
All six experiment manifests now sum to 124.14264650100267 wall seconds /
0.03448406847250074 core-hours. Preparation and post-run checks are outside
these totals. Evidence is in `results/recovery-grid-startup/`. The generating
implementation commit, parameters, dependency versions, input/output hashes,
thread limits and logs are retained in its manifest. The pip provenance command
printed an unwritable-cache warning and successfully recorded dependency versions;
worker stderr is empty.

All deterministic positive/negative controls and ten labelled round trips pass.
All declared startup input/output hashes pass. The four frozen planned cells match
PLAN, with no optimization and no completed search units. The prior pilot output
hashes, exact parent PASS and labelled links match; saved independent acceptance
at both scales is bound to the same parent bytes and checker sources. Its saved
successful transcript and the unchanged surgery acceptance are reused, not replayed.
Python compilation, shell syntax and three invalid stage/startup combinations pass
(the latter reject with exit two). Static review confirms each full-grid cell
initializes from its original parent, never another cell, and calls the unchanged
shared optimizer. The optimization loop itself has not run in calibration mode.
The previous shared-code quick-suite PASS is reused; no new integrated suite or
CI was needed for the isolated dispatch and parameter-selection change.

**PROVED-1, implementation readiness only.** STARTUP-PASS is not a geometric
recovery result. The completed pilot's UNDERPOWERED verdict, hypotheses and
credences are unchanged. The full grid awaits explicit owner authorization under
the standing long-run rule; no active process, focus geometry or night. README
records the ready launch command. Conditional successes still require exact saved
checks and candidate-check before any result claim. Even a full grid with accepted
cells leaves full eight-face recovery gated. No human review or FD/witness change.

## Conditional failed-level grid concluded (2026-11-04)

Pre-registration `b851f8c`, implementation `3f3aeda`, generating HEAD `281881d`.
The owner explicitly authorized this grid after startup acceptance. The actual
registered command ran from the repository root in the activated research
environment on AC power, under caffeinate/nice, with one worker and one thread
per numerical library. Evidence is retained in `results/recovery-grid/`.

```bash
STAGE=calibration caffeinate -dimsu nice -n 10 bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

Two earlier launch attempts stopped before Python and before OUT creation. The
sandbox rejected nice with `setpriority: Operation not permitted`, and a background
launch did not survive the tool shell. The surviving foreground exec session ran
the registered command with the required environment permission. These attempts
produced no optimizer work or experiment manifest. Their launcher logs are local
`/private/tmp/polyhedrons-E-261103-04-recovery-grid-launch*.log` files, outside the
retained run evidence. The successful run has a clean generating working tree.

### Controls, prediction and exact outcomes

All three supplied-plane positive controls, three duplicate-plane negative
controls and ten labelled round trips pass. Positive objectives have zero events,
zero depth and value zero. Negative objectives receive controlled INVALID-INPUT
singular-matrix rejection. Verdicts use exact reports. Positive exact reports have
simple faces and no bad pairs, providing a nonfailing control for the same defect
checks that reject the search outputs. The repeated objective value below is a
search diagnostic and receives no structural interpretation.

| Unit | Genus | RNG seed | Requested seconds | Optimization seconds | Restarts | `nonsimple_faces` | `bad_pairs` | Exact outcome |
|---|---:|---:|---:|---:|---:|---|---|---|
| Roest-Vigh | 1 | 1040201 | 180 | 180.00055116600197 | 63 | [1, 6] | [] | REJECT |
| Mizhaev | 2 | 1040302 | 180 | 180.0005625829981 | 49 | [0, 4] | [] | REJECT |
| Roest-Vigh | 1 | 1040201 | 600 | 600.0015438750015 | 191 | [1, 6] | [] | REJECT |
| Mizhaev | 2 | 1040302 | 600 | 600.0020673750005 | 164 | [0, 4] | [] | REJECT |

Each cell stopped at REQUESTED-TIME and then received exact rejection, with
objective 2. The requested-time fractions are in recovery.json. Roest-Vigh reports
V/E/F/chi = 16/24/8/0 and 21 adjacent pairs. Mizhaev reports 20/30/8/-2 and 25
adjacent pairs. Each report has matching topology, distinct corner triples and
vertices, and consistent edges. The nonsimple-face defects prevent embedding.
The saved-file verifier transcripts retain full output and report zero PASS for
every cell. There are no accepted recoveries requiring independent candidate
review. The conditional H1 prediction failed in all registered cells.

Each cell used its original accepted parent, with unchanged labels and the same
paired seed across budgets. No rejected output or other cell seeded a search.
Roest-Vigh genera two/three and Mizhaev genus three were outside this conditional
grid, as were alternative parents, seeds, chains and focus maps.

### Resources and verification

The attempt exited normally with status zero and stop reason UNDERPOWERED.
It used 1561.8850308330002 wall seconds / 0.4338569530091667 core-hours, fraction
0.8677139060183334 of its outer cap. Per-cell requested time was the binding limit.
The outer cap did not bind and all four planned cells ran. All seven experiment
manifests sum to 1686.0276773340029 wall seconds / 0.46834102148166745 core-hours.
Preparation, unsuccessful pre-Python launches and post-run checking are outside
these manifest totals. No sleep telemetry was collected.

Every declared current source/input hash and every saved output hash matches the
finalized manifest. The four initial in-process exact checks and saved-file
transcripts are reused. The registered startup, unchanged parent independent
acceptance, surgery acceptance and shared-code quick-suite PASS are reused for
their existing scope. No changed code or input calls for another solver, verifier,
proof replay or integrated suite. Ledger and handover changes receive diff,
evidence-link and graph metadata review.

### Verdict and next decision

**PROVED-1, supplied-input computation.** The four saved outputs are rejected for
embedding by the registered exact checks. **UNDERPOWERED at the registered paired
3/10-minute budgets from the two frozen parents.** The deterministic controls test
implementation readiness but provide no search-power estimate for these
intermediate maps. H-261101-07, H-261103-02 and the A/B/C credences retain their
preceding statuses. Full eight-face recovery and focus geometry remain gated.

Follow the registered no-success branch and reassess the two intermediate maps
or chain selection before another geometric search. The next concrete preparation
is to check whether the existing multi-adjacency exact encoding covers these
incomplete-adjacency auxiliary maps, then register a bounded map-feasibility audit
if it does. That audit would separate an intermediate-map obstruction from a
failure to recover geometry from these parents. An UNSAT could only be interpreted
with the exact formula, certificate and encoding scope retained. No audit or new
search is activated by this conclusion. The broader experiment remains running,
with this calibration stage complete and no active process.

### Source review for the next audit

Focused CodeGraph navigation and source review found the existing submap path in
`code/omsat.py`. `Triangulation.__init__` accepts `submap=True`, preserves supplied
links and checks segment pairing. `Predicates.E` returns false for absent edges,
and the multi-adjacency ray predicate iterates over prescribed segments, including
an empty list for an absent pair. `build` constrains all non-corner triples and
adds segment-disjoint clauses independently of the map's genus. This identifies
an existing implementation path for the proposed audit. Its soundness remains
PROVED-1, with the extended argument in E-261103-02/SOUNDNESS.md.

The E-261103-02 `test_encoder.from_links` helper constructs Triangulation with the
default `submap=False`. A local audit must explicitly select `submap=True` after
preserving the saved labelled links. Before interpreting target decisions, it
must pin the known embedded Roest-Vigh sphere and Mizhaev genus-one parents under
this same encoding, plus a rejected fixed-chirotope fixture with a retained
certificate. These controls specifically exercise absent face pairs together with
parallel edges. This session performs source review only. Formula construction,
SAT solving, proof checking and any realizability stage need a committed audit
amendment first. A SAT oriented matroid would still need a geometric realization.
