# E-261103-02: multiple-adjacency OM-SAT encoder

Pre-registration, 2026-11-03. No experimental run precedes this commit.

* **ROADMAP scores:** T 2 D 2 F 2 G 2 R 2; T + D = 4.
* **Question:** Can the existing OM-SAT predicates encode admissible multi-edge maps while retaining the S0 formulas?
* **Hypotheses moved:** none (`tests: []`); this validates infrastructure for DR19 and E-261103-03.
* **H1 / H0:** shared segments can be reconstructed from links and encoded with determinant signs / a named obstruction prevents this extension.
* **Region:** reuse E-261103-01 datasets without enumeration; target S5 (8,2) preparation, preserving S0.
* **Implementation:** extend `code/omsat.py` map validation and per-segment predicates; generalize `omsat_sym.build_sym` using T.n; extend independent Fraction geometry in `omsat_geom.py`; reuse `omsat_validate.py`. Keep the single-adjacency circuit construction unchanged. Add a bounded experiment control script, runner, and a quick regression in `verify_all.py`.
* **Map invariant:** distinct corner triples, one face cycle, identical segment endpoint pairings at both faces. Derive each segment from an occurrence in links, rather than arbitrarily pairing the partners of an edge. Reject inconsistent and non-admissible maps before encoding.
* **Predicates:** shared-segment union for boundary membership; XOR each transversal edge crossing and each collinear boundary run; reject overlaps between distinct shared segments. Re-derive reflex and turn predicates using the unique incident segment at a corner. Document the extended Lemma 5.1 at PROVED-1 only.
* **Controls:** own-map Eval and chi-pinned CNF SAT for uniform perturbations of Roest-Vigh, Mizhaev and Szilassi. Their published planes have symmetry degeneracies: record zero determinants and retain the raw input; use deterministic small integer perturbations for the uniform encoder, never silently assign signs to zero determinants. Compare every predicate with exact direct geometry on exactly 1,000 accepted uniform perturbations of each object (fixed seeds; small and large radii). Require zero mismatches and count rejected degeneracies separately. Negative controls: Roest-Vigh planes on Mizhaev links, and one-sided swapped parallel-edge pairing; reject malformed pairing or require fixed-chi UNSAT. Preserve every negative CNF and solver proof if a solve is used.
* **Verifier guard:** test all 37 non-admissible (9,3) census records return EMBEDDED False without raising. The guard already exists at the base commit; do not rewrite it unnecessarily.
* **S0 regression:** compare serialized CNF hashes with base e13b79e for representative existing single-adjacency plain/symmetric configurations; reuse existing exact controls. Do not re-run the census.
* **Symmetry controls:** exercise C2 (including fixed faces), free C3, and D3 proper-isometry relations, with known exact or deliberately degenerate configurations. A symmetry forcing a zero determinant is outside the uniform ansatz and must be recorded explicitly, never interpreted as geometric nonexistence. Validate automorphisms against segment pairings.
* **Pilot:** one uniform configuration per object; own-map SAT, both negative controls, and first (8,2) CNF build after positive gates. Then the fixed perturbation counts. Unit tests are bounded development controls.
* **Predictions / decisions:** the single-edge circuits remain identical (otherwise fix the regression); multi-edge direct predicates agree (otherwise stop target preparation and fix or document obstruction). No uncertain existence prediction is applicable to infrastructure validation.
* **Grid:** perturbation radii span unchanged embedding chambers and configurations with defects; use fixed seeds and exact rational comparisons. No optimization or target search.
* **Budget:** one worker, each solver/control subprocess capped at 60 seconds; full perturbation control capped at 600 seconds, runner hard cap 900 seconds; at most 0.25 core-hours per full attempt. One shard. Development estimate 1-2 sessions.
* **Pilot gate / binding limit:** completion of all prescribed counts, not solver time. Any timeout is a failed/underpowered validation and stops the dependent work. No long run is authorized or proposed by this plan.
* **Power:** detects a single mismatch among the sampled predicates and breaks in the specified controls; cannot prove correctness for all chirotopes or decide realizability of any S5 target map.
* **Counters:** exact predicate mismatch counts, clause violations, SAT status, EMBEDDED, nonsimple_faces, bad_pairs where applicable. Timings are resource diagnostics, not evidence.
* **Counter calibration:** no float threshold in the verdict. Positive and defective perturbations calibrate both Boolean values; report observed coverage per predicate. No saturation-based measurement.
* **Scenario move:** A / B / C unchanged by all outcomes; controls validate a tool, not existence or nonexistence.
* **Outcomes:** SAT under pinned chi validates that configuration only. Fixed-chi UNSAT validates a negative control only. Unpinned target SAT is not requested. Timeout/UNKNOWN/ERROR conveys no geometric information. Near-miss never counts as a result.
* **Stop:** all README controls pass and the first census (8,2) CNF is built, or a written named obstruction. Do not solve target instances; that is E-261103-03. Do not launch long runs, subagents, push or open a PR.
* **Ledger:** set running at pre-registration. At conclusion update README, STATUS DR19/3b, ROADMAP state, append experiment-log and refresh graph; retain S0 rows and evidence levels. No FD/witness row changes.

## Amendments

Append dated implementation findings, control failures and pilot results here; preserve this pre-registration.

### 2026-11-03: implementation findings before full controls

The original Roest-Vigh and Mizhaev plane sets are already uniform (no zero determinants); they are the
primary pinned positive controls. Only raw Szilassi needs a uniform perturbation. The initial wording
above overestimated degeneracy of the eight-face inputs. Own-map Eval and pinned CNF SAT pass for both
original eight-face inputs. Development checks on 20 broad perturbations per object found no mismatch.
All development checks are bounded, not target searches; the original quick verifier passed (archive skipped).

Symmetry needs an explicit scope restriction: a proper half-turn fixing a cooriented face plane and
swapping two others forces chi(fixed, swapped pair, infinity) = 0. Thus uniform C2 with fixed faces
(and the (9,3) D3 actions containing these) can be encoded but cannot cover such geometric realizations.
The controls must exhibit the forced-zero quadruple and retain the symmetry-only contradictory CNF;
no geometric exclusion follows. C2 free and C3 free get positive uniform symmetry-only pinned controls.
The general asymmetric formulas remain available for every admissible census map.

### 2026-11-03: bounded pilot gate

`results/pilot/manifest.json` records a completed 4.92-second single-worker pilot (0.001366 core-hours).
All own-map pinned controls, both negatives, independent unit refutations, the six S0 hashes and
C2-free/C3-free symmetry controls pass. C2-fixed/D3 symmetry-only contradictions are explicitly scoped
to the uniform ansatz. One direct perturbation per object has zero mismatches; the first (8,2) CNF
was built, never solved. The next bounded validation is exactly the pre-registered 1,000 accepted
perturbations per object. Its binding limit should be count completion; the 600/900-second caps remain.
No long-run gate is opened: this infrastructure experiment has no target run.
