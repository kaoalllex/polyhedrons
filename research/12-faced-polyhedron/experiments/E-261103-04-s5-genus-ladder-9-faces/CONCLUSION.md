# E-261103-04: representation and dart-preserving surgery gates

The two combinatorial stages are concluded. The broader experiment stays running while
its geometric recovery pilot has a dated PLAN amendment awaiting implementation.

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
