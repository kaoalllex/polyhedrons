# Strategy review, 2026-11-10: laptop-only compute, three constructive targets, harness changes

## Owner digest (ten lines; the rest is reference)

1. **What this is.** A lead session that files the handoff of the 2026-11-10 strategy session
   (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md`) in the project's formats. It ran no solver and produced no result.
2. **Decided by the owner, recorded:** compute is the laptop only (no Actions, no rented compute); harness items 1-7
   approved (item 8 after two good manual mornings). Four wording items are applied (`PROTOCOL.md` §8b).
3. **Verdict (Recommendation).** The handoff's case against (10, 4) is a hypothesis, not a finding: "multiplicity is
   what the solver refutes" rests on solve times (NUMERICAL). The plan below is still right, because two cheap tests
   decide it (E-261110-05, <= 3 core-h; E-261110-02, one night) before six more (10, 4) nights are spent.
4. **Approval 1: `STRATEGY.md` text** (§2 below): focus = three constructive targets on the laptop.
5. **Approval 2: `SPEC.md` S6** (§3 below): face-minimal polyhedra with single adjacencies; S0 is not weakened.
6. **Approval 3: the week plan and the proposed credences** (`ROADMAP.md`, "Week plan" and "Decision point").
7. **Approval 4: the E-261110-02 night**: (10, 3), 20 maps, <= 80 core-h, after a prep session and its amendment.
8. **First item** after approval: the E-261110-02 prep (converter, controls, two-map pilot, smoke test).
9. **Without approval** only the cube-and-conquer pilot runs (item 3 of the approved 2026-11-09 plan).
10. **Corrections to the handoff** made here are listed in §5; none changes its direction.

## 1. Scope and checks of this session

Evidence cut: `9f125b5c` on `lab/2026-11-09`. Labels are `SPEC.md` §5; **Recommendation** marks a judgment. Checks
run (seconds): the counting formulas of §4 by hand (elementary); `code/omsat.py` read for the gating of
`SEGMENT_DISJOINT` (EXACT reading); two web searches for the triangulation counts (CLAIMED); `verification/trace.py`.
Not run: any solver, the session's wedge script (not in the repository), `verify_all.py --quick` (no code changed).

## 2. Proposed `STRATEGY.md` text (not applied; the owner changes that file)

Replace the "Focus target" and "Compute" bullets of §1 by:

```
* **Focus (owner, 2026-11-10): constructive, laptop-only, three targets in parallel.**
  * **S6 at (10, 3) first**: the duals of the 20 vertex-minimal genus-3 triangulations (10 faces, 42 of 45 pairs
    adjacent, every adjacency single). One night decides it either way (E-261110-02). Success is only
    `verification/verify_candidate.py FILE --target S6` PASS with these counts, then `candidate-check`.
  * **S1 with the genus free**: nine or ten mutually adjacent faces at any genus (E-261110-04), then relaxed
    Szilassi-12 at genus >= 7 (E-261101-08), both gated by the family scoring at 8 planes (E-261110-03). Success is
    `verify_candidate.py FILE --all-pairs` PASS with the face count, genus and multiplicities reported, then
    `candidate-check`.
  * **S5 at (10, 4)** continues only under the rule of E-261110-06: strata A and B run as laptop nights if the
    cube-and-conquer pilot prices them at <= 3 nights, otherwise as one explore night.
  * These targets are reported as S6 or S1, never as S0 or S5. Symmetric realizations are allowed (FD5 covers the
    59 single-adjacency (12, 6) maps only).
* **Compute: the owner's laptop only** (owner, 2026-11-10): at most 10 cores, 8-10 shards per splittable run, nights
  under `caffeinate`; no rented compute, no GitHub Actions.
```

In §2, "Compute is scarce (one laptop, at most 10 cores, free GitHub Actions)" loses "free GitHub Actions", and one
bullet is added:

```
* **Score the sampler first.** An arrangement family is scored on a rung with known answers (8 planes) before it is
  used on a target, and its report includes the wedge covariate.
```

Log entry:

```
* 2026-11-10 (owner's decisions on the handoff of the 2026-11-10 strategy session,
  `reviews/strategy-review-2026-11-10.md`): compute is laptop-only, no rented compute, no Actions; the (10, 4) route
  is demoted to the rule of E-261110-06; three constructive targets (S6 at (10, 3); S1 with the genus free at 9, 10
  and 12 faces) adopted for one week of tests; the wedge ansatz is an explore item gated by E-261110-03. The side
  track and S0 parking are unchanged.
```

The side-track and S0 bullets stay as they are. If the text is approved, the first paragraph of the root `CLAUDE.md`
and `AGENTS.md` ("Current focus") and their rule "or to GitHub Actions" need the same update by the owner.

## 3. Proposed `SPEC.md` entry S6 (not applied)

Row for the §2 table:

```
| S6 | **Face-minimal polyhedron with single adjacencies (F, g)**: embedded, cubic, every face a planar simple polygon,
every two faces share at most one edge (the dual map is a simplicial complex), and F is the vertex count of the
vertex-minimal triangulations of the orientable surface of genus g: (7, 1) Szilassi, (10, 2), (10, 3), (11, 4),
(12, 5); (12, 6) is S0. Not every pair of faces is adjacent: the adjacent pairs number E = 3 (F + 2g - 2) (21, 36,
42, 51, 60, 66). Success check: `verify_candidate.py FILE --target S6` PASS (EMBEDDED, cubic, F and genus from the
list, every adjacency single, adjacent pairs = E) | (7, 1) known; (10, 2) to (12, 5) unknown to us (nothing found in
print for the face version, CLAIMED, web search 2026-11-10); (12, 5) is S3 at genus 5; symmetric realizations
allowed (FD5 is about S0 only) |
```

Change-log line: "§2 adds S6 (face-minimal polyhedra with single adjacencies) and its check `--target S6`; S0 is
unchanged and not weakened; an S6 object is never a solution". `--target S6` is built in the E-261110-02 prep only
after the approval; until then a (10, 3) candidate is checked by the plain EMBEDDED verdict plus the stated counts.

Scope that the entry must keep (elementary counting, PROVED-1): "face-minimal" means minimal among **cubic**
polyhedra with pairwise single adjacencies (F (F - 1) / 2 >= 3 (F + 2g - 2)). Non-cubic polyhedra and polyhedra with
multiple adjacencies can have fewer faces (Roest-Vigh: 8 faces at genus 3).

## 4. What was filed

| Handoff | Filed as | Note |
|---|---|---|
| I-A wedge-plate ansatz | I-261110-01 | observation recorded as weak; dated section in I-261101-20 |
| I-B face-minimal ladder (T2) | I-261110-02 | dated section in I-261101-07; `L:hlz2010` added |
| I-C genus-free relaxed targets (T1, T3) | I-261110-03 | dated section in I-261030-06 |
| I-D multiplicity test | I-261110-04 | dated section in I-261108-01 |
| I-E XOR-aware solving, I-F chart normalisation | I-261110-05, I-261110-06 | low priority, no slot |
| I-G edge-convexity bits | I-261110-07 | dated section in E-261101-15, no new experiment |
| H-A, H-B, H-C | H-261110-01, -02, -03 | status open |
| E-A edge-type tool and null | E-261110-01 | PLAN committed |
| E-B (10, 3) decision | E-261110-02 | PLAN committed; night needs approval |
| E-C family scoring at 8 planes | E-261110-03 | README |
| E-D (9, g), (10, g) sweep | E-261110-04 | README, gated |
| E-E relaxed Szilassi-12 | **E-261101-08**, corrected and extended | no duplicate folder |
| E-F immersion-only formulas | E-261110-05 | README, variant V2 added |
| E-G (10, 4) remainder | E-261110-06 | README with the rule |

Counting used throughout (cubic: V = 2E/3, g = 1 + (E - 3F) / 6, E = 3F mod 6): F = 8: E = 30, 36, 42; F = 9: 39,
45, 51; F = 10: 48, 54; F = 12: 66, 72, 78. Credences (CONJECTURE, planning weights of the handoff session): the
proposed table is in `ROADMAP.md`, "Decision point".

## 5. Corrections and open points (audit of the handoff)

1. **E-261101-08 miscount, fixed.** "Three doubled pairs, genus 7" contradicted the row's own d = 6g - 36; the
   smallest relaxed 12-face case has six extra segments (README and ROADMAP row corrected).
2. **"Fewest faces for genus 3" is scoped to the cubic single-adjacency class** (§3). A 9-face genus-3 cubic
   polyhedron needs multiple adjacencies; only the all-pairs case (S5 (9, 3)) is excluded, at formula scope.
3. **Map counts.** 865, 20 and 59 were confirmed by a web search (CLAIMED); 821 and 751,593 were **not**. The
   vertex version at genus 5 is mixed (realized examples and non-realizable ones), not "fails". None of these numbers
   is in `STATUS.md`; the E-261110-02 prep reads the primary tables.
4. **The 20 maps are not on disk** (`literature/` has only genus-6 lists). The prep fetches Lutz's list as untrusted
   data; if that fails, an own enumeration is a lead decision.
5. **Test (ii) of H-A could not separate its two readings.** `SEGMENT_DISJOINT` is emitted only under `triples`
   (`code/omsat.py` 562-568), so the immersion-only formula drops the global triples and the segment clauses
   together. E-261110-05 adds variant V2 (plain without `SEGMENT_DISJOINT`); the week item's follow-up tree uses it.
6. **DRAT at (10, 3)**: checked in the run and then deleted (`PROTOCOL.md` §5), not "kept"; keeping 20 proofs is the
   owner's word at launch.
7. **S0 credence.** The handoff's 0.05 is recorded, the S0 table (A = 0.20) is left alone: no S0 experiment ran
   since 2026-11-01, and the handoff itself argues that the S5 negatives say little about S0. Owner's call.
8. **(10, 4) credence** proposed as 0.10 / 0.50 / 0.40; the handoff gave only "exists 0.10", the split is this
   session's (laptop-only compute raises "cannot tell").
9. **Wedges.** Nothing in the files calls the wedge structure a regularity; E-261110-01 recomputes the observation
   and the null (with the S4 family, which the handoff did not simulate) before E-261110-03 uses the covariate.
10. **Outside the handoff's list, changed for consistency:** "night reports included" removed from the root
    `CLAUDE.md` / `AGENTS.md` skill list; the `.agents/skills` mirrors follow `.claude/skills`; `README.md` marks
    `reports/` frozen. `STATUS.md`: only the stale "next" phrase of its header was updated; no row changed (no result).

## 6. Three things to do first

1. Owner: the four approvals of the digest.
2. Lab (Opus, high): the E-261110-02 prep, then the owner's night.
3. Lab (Opus, medium), in one chained session: the cube-and-conquer pilot, then E-261110-01 with the E-261110-03 prep.

## Owner's decisions (2026-11-10)

All four approvals of the digest given: the `STRATEGY.md` text (§2), `SPEC.md` S6 (§3), the week plan and credences
(S0 table unchanged), the E-261110-02 night after its prep and amendment 1. Applied the same day.
