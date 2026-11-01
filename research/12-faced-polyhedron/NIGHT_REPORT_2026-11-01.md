# Night report: nights 4 and 5 (2026-10-30 23:00 -> 2026-11-01 00:45)

Scripts: `overnight/run_night4.sh 8 11` (gate, then `arch --gauss-gate` + `n5`) and `overnight/run_night5.sh 8 11`
(gate, then `n5` on 10 cores + `arch` control on 1 core). Raw results: `overnight/results/{arch,gate,n5}/`.
Analysis: `python3 overnight/analyze_n5.py` plus the per-night split and exact re-check described below.

## Headline

No genus-4 polyhedron, no SAT offset system, no candidate. Genus 3 is reproducible (94 exactly embedded
realizations of 4 types), genus 4 was never reached by any engine. **12,202 exact offset decisions at
Gauss-admissible normals: 0 SAT.** The class-aware tools (gate, normals-first, k-drift) do not break the
genus-3 plateau. These jobs should not be run again on the strict target (see "Verdicts").

## Run log

| Night | Wall time | Jobs | Notes |
|---|---|---|---|
| 4 | 10-30 23:00 -> 10-31 16:05 | gate, arch (1/3 cores, gated), n5 | laptop slept 00:18 -> 08:09 (~8 h lost); restarted by hand at 08:09 |
| 5 | 10-31 16:22 -> 11-01 00:45 | gate, n5 (10 cores), arch control (1 core) | ran without interruption |

Ops lesson: neither script wraps the run in `caffeinate`; every future night script must (see the
`overnight-run-script` skill and `PROTOCOL.md`).

## Numbers

### arch (archive + bandit over handles, exact check of every zero)

| | Night 4 | Night 5 |
|---|---|---|
| tasks | 712 | 106 |
| new exact realizations | 187 (genus 2: 102, genus 3: 85) | 16 (genus 2: 13, genus 3: 3) |
| genus-4 arm tasks | 7, best 4.0 events | 4, best 5.0 events |
| archive at the end | 231 realizations | 247 realizations (153 genus 2, 94 genus 3) |

Genus-3 realizations in the archive by type: type 15: 54, type 53: 33, type 0: 6, type 39: 1.
**Exact re-check (this report): all 94 genus-3 realizations pass `ladder_exact.verify` (EMBEDDED)** -
script: links from `gauss_degree.links_from(coherent_triangles(map))`, `require_all_pairs=False`.

### gate (Gauss gate T1 for every realization x next handle)

232 realizations gated (76 new in night 5). Own Gauss degree = 1 - g on every one (the degree theorem
holds 232 / 232 times). Type 0 genus 3: 21 arms, k_tau = 0 on all 21 (the next map is out of class; this
confirms the review diagnosis of the type-0 genus-4 plateau). Type 53 genus 3: 64 arms, k_tau in {0, +1},
never -1. Genus-2 arms of other types: k_tau = -1 on a minority (e.g. type 45: 22 / 123).
Test 2.2 (night-3 chains): 352 of 378 failed ladder levels are out of their Gauss class (93 %), 26 in class.

### n5 (normals first + exact offsets; k-drift; direct genus 6)

| | Night 4 | Night 5 | Total |
|---|---|---|---|
| tasks (all NOT_REALIZED) | 204 | 228 | 432 |
| exact UNSAT (z3) | 5,914 | 6,047 | 12,202 |
| no admissible normals | 915 | 1,012 | 1,983 |
| gate failed after the exact check | 217 | 270 | 493 |
| SAT | 0 | 0 | **0** |
| core-hours (task wall time) | 69.8 | 77.7 | 147.5 |

Per-night columns count finished tasks (`results.jsonl` stats); the total counts every logged decision in
`attempts/` (241 more UNSATs from tasks cut off at the time limit).

By method (both nights): g6 (direct genus 6, types 0, 11, 58): 1,486 UNSAT; kdrift: 7,074 UNSAT;
nfirst: 3,642 UNSAT. z3 median 8-21 s; no timeouts recorded.
By normal-space radius around the seed: r = 0: 80 UNSAT; r = 0.02: 2,142; r = 0.05: 2,657;
r = 0.1: 2,855; r = 0.2: 2,982.

k-drift: 153 of 192 drift tasks reached the next Gauss class (T1_PASS, 27 types), **every one with the
hemisphere margin pinned at exactly 0** (max -0.0, none > 1e-6): the drift reaches the class only on its
wall. The genus-4 class (own degree -3) was reached 11 times (types 0, 39, 53; handles (0,5,8)-(2,6,7) and
(1,2,10)-(4,7,9)); all their offset problems are UNSAT.

## What these nights establish (and what they do not)

1. **Robust constructive plateau at genus 3.** Five nights, ten engines, 30+ types: genus 3 for 4 types
   (now 94 exact realizations), genus 4 never. This is a reproducible fact about our search methods, not a
   theorem about the polyhedra.
2. **The Gauss class is necessary but far from sufficient.** In-class seeds (k_tau = -1, T1_PASS) are
   UNSAT for the offsets at every radius, including r = 0 (80 times).
3. **Pinned hemisphere margin.** All 153 class-reaching drifts end with margin exactly 0. A systematic
   phenomenon with an unknown cause; candidate for a lemma ("the handle normals of an embedded polyhedron
   cannot leave a closed hemisphere") - the cheapest new theory question these nights produced.
4. **Low statistical power of the UNSAT counts.** The only positive control (`nf_control.py`, realization
   A on its own map) was SAT at r = 0.05 and UNSAT at r >= 0.1. So UNSATs at r >= 0.1 are weak evidence,
   and even at r <= 0.05 the control SAT rate is unknown (one trial). 12,202 UNSATs do NOT show that the
   next level is unrealizable; they show that this sampling scheme does not find realizations.
5. **Not established**: impossibility of genus 4 for any type; impossibility of genus 6; any property of
   types not tried.

## Verdicts (feed `STATUS.md`)

* `arch`, `glad`, `n5`, `kdrift`, normals-first climbing on the strict target: **DEAD at this budget**
  (~250 core-hours over nights 3-5, zero genus-4 progress). Keep the data (archive, class seeds, attempts).
* Data products kept: `overnight/results/arch/archive.json` (247 exact realizations, chirotopes),
  `overnight/results/n5/class_seeds/`, `overnight/results/n5/attempts/` (normals + status per decision).

## Follow-ups worth a small experiment (pre-register in `ROADMAP.md`)

* Power study for normals-first: `nf_control.py` on 20-50 realized maps x radii {0.01, 0.02, 0.05} to
  estimate the control SAT rate; only then is "0 SAT in N in-class tries" interpretable.
* Pinned-margin lemma: prove or refute on the 153 drift endpoints (theory first, then a 1-hour test).
* UNSAT-core mining at r = 0 (80 instances): extract small cores, look for a common geometric reason.
