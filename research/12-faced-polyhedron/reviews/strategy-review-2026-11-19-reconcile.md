# Reconcile: Codex second opinion vs applied lead review 2026-11-19

Sources: `strategy-review-2026-11-19-codex.md` (C), `strategy-review-2026-11-19.md` (L). Codex agrees on the order (nine faces,
census main investment, P6 fallback, weight 0.45) and on the §4 lemmas. Disputed or reported points:

| # | Codex point | Verdict | Evidence (label) |
|---|---|---|---|
| 1 | U2, U3 "expected INFEASIBLE" are predictions, not known answers (C §2) | accept | 3d's checked refutations are of the map CNFs (`STATUS.md:183-206`, EXACT, formula scope); P3 may not claim (8, 30), (9, 39) UNSAT (`E-261116-07/CONCLUSION.md:49-50`); P3 => map CNF unproved (PROVED-1, C) |
| 2 | Block complete paired runs, not signs; a failed-bridge map stays open; "only the known maps" overclaims (C §2) | accept | `p3.py:312-313` blocks the sign vector only; end bits lose pairings (`STATUS.md:160-162`); safety argument PROVED-1 (C); the claim becomes formula scope, UNSAT-SOLVER |
| 3 | Drop the automatic 60 core-h C3 night (C digest 6) | accept | U1 has 9 elements / 256 cells, target 10 / 512 (C, NUMERICAL); L itself: fast U2, U3 leave "no C3 object or a rare one" (L:72-73, CONJECTURE); C3 at genus 4 is covered per map by item 2 |
| 4 | "0, 3 or 6 fixed triangles, any multiplicity" (`ROADMAP.md:122-123`) is wrong | accept, checked | admissible = distinct corner triples (`census.py:131-133`, `STATUS.md:160`): <= 1 fixed triangle per face orbit, multiplicity <= 3 (PROVED-1); counts below EXACT (session) |
| 5 | Gate C3 and C2 separately in the shared 1 core-h | accept | a complete validated list does not depend on the other enumerator (Recommendation); `ROADMAP.md:125` couples them |
| 6 | Stage B: positive nine-face fixed-face control, wrong pairing/action, `build_sym`, inherited action; price one map per stratum first; genus 5 only for a covered, decided family | accept | (9, 3) negatives are UNSAT without symmetry, so cannot catch an all-rejecting clause (C §3, PROVED-1); `make_queue.py:94` takes the involution from links, sound only when unique; 10 core-h at 600 s = 60 caps (`STRATEGY.md:64-65`) |
| 7 | "U1 and the census rung agree map by map" (`ROADMAP.md:127`) | accept | census membership predicts no SAT; compare only on common decoded maps (C §3, Recommendation) |
| 8 | Item 1 D 2 -> 1 | accept | without the night item 1 decides blocker safety, the (8, 3) slice and refutation times only; T + D = 3 keeps the gate |
| 9 | "100x faster" (L:5); process cost "fine" from counts (L §6.5) | accept, no diff | 3600/90 = 40, 3600/17 = 212, censored, formula changed (`E-261118-03/CONCLUSION.md:1-4`, NUMERICAL); neither phrase is in STATUS, STRATEGY or ROADMAP (grep) |
| 10 | §5: b = 0 for a geometric C3 solid; planted nine-plane C3 discovery control | unresolved | untested proposals (C §5); folded only where free: stage A records b per map (b = 3 kept); the planted control is named as a C3 night's precondition, not scheduled |

**Check (point 4).** `python3 -I reviews/strategy-review-2026-11-19-reconcile.py`: 0.14 s wall, 1 process. Normaliser of the
free C3 in S9: 324; 12 pair orbits; 364 multisets of three, 352 with multiplicity <= 3, **18 classes** (Codex reproduced);
6 oriented fixed triangles on 3 supports, so b in {0, 3} (30 - b = 0 mod 3). EXACT, one session.

## Diff to the week plan (applied only after the owner's approval)

* E-261119-01 (`ROADMAP.md:105`, :154, README:13-14): drop "its pass branch earns a J-2 night"; scores 2 1 2 1 2. Blocking
  (:108-109, Goal): "block that map by its complete paired runs (one predicate per run on line ij with end triples ijk, ijl;
  the negated conjunction of its E runs and every image under the normaliser, 384 for free C2); a map whose bridge fails
  stays open". Budget (:111): "hard aggregate <= 20 core-h incl. controls and bridges". Controls (:113): "a synthetic unit
  test (same end triples, different pairing); each known object pinned with its own map blocked INFEASIBLE, the other SAT".
* E-261119-01 tree (:114-119, Next): "U2 or U3 SAT -> stop: decode, GP, Euler, darts, census code, action; transport chi into
  the 3d map CNF and evaluate its clause families; bridge; a PASS -> `--target S5`, `candidate-check`, escalate (INFEASIBLE
  there is a prediction)". The night branch and "U1 model, U3 UNKNOWN" -> "otherwise record each unit, go to item 2; a C3
  night needs a changed nine-plane discovery test (e.g. Codex §5's planted control) and the owner's word". The blocking
  claim -> "this P3-sym free-C2 formula with these blocks is INFEASIBLE", UNSAT-SOLVER, no claim on failed-bridge maps.
* E-261119-02 (`ROADMAP.md:122-130`, :155, README): "0 or 3 fixed triangles, pair multiplicity <= 3, 18 C3 demand classes;
  deadline inside gluing; covers, gluings, codes, time per stratum and b per map recorded". Gate: "per family in a shared
  1 core-h, C3 first; a complete family passing its controls goes to stage B". Stage B: "one map per multiplicity stratum
  priced first; controls: generic moved nine-plane signs pinned on symmetry + gauge (`build_sym`), a realizable nine-face
  fixed-face positive, a wrong pairing, a wrong action; action inherited on canonical darts"; "compared with U1 only on
  common decoded maps"; "a complete family all UNSAT-SOLVER -> genus 5 for it"; "neither family advances -> item 3".
* Item 3 trigger (:131, :166): "only if neither census family advances". Item 4 (:134): "input: Codex review §4 (every
  group element, powers included; the stabiliser test is not a full dependency test)".
* `STRATEGY.md:11-14`: "for C3 once its power is measured at the nine-face size on known answers (E-261119-01, ...)" ->
  "calibrated on known answers (E-261119-01: discovery at eight faces, refutation at nine, the symmetric (8, 3) slice; a
  C3 nine-face night needs a changed discovery test and the owner's word)"; "is the fallback" -> "is the fallback if
  neither census family advances". Log: one line for this decision. Credences unchanged.

**Week item 1 waits only for the owner's answer**: no PLAN is committed and nothing runs. If approved, its PLAN carries the
blocker, tree and budget above; until then the approved plan stands, and item 2's stage A may start in parallel.
