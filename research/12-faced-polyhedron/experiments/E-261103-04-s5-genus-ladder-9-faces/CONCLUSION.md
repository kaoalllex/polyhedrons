# E-261103-04: representation gate concluded

This concludes the first registered stage. The broader experiment stays running while
its geometric recovery pilot awaits a dart-preserving implementation and amendment.

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
