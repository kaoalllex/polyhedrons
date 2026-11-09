# E-261109-01: conclusion

* **Runs**: commit 5c26f2a (PLAN), one run `control.py results/0` from the session; no `manifest.txt` (not a `run.sh`
  run); total solver time 2.0 s on one core (< 0.001 core-h, from `result.json`), not a manifest figure.
* **Controls**: this is the control. All five units ended as predicted; every pinned negative is a valid map (distinct
  corner triples, consistent edges, chi = 2) that `ladder_exact` rejects (EMBEDDED False), so it is not a loader rejection.
* **Prediction vs outcome**: pinned SAT k = 2, 3 (80 %): confirmed; unpinned k = 2 SAT within 900 s (55 %): confirmed, 0.19 s.
* **Exact verification**: objects `control_k{2,3}.json` via `ladder_exact.verify(require_all_pairs=False)`: k = 2 F 12, V 20, E 30,
  top/front multiplicity 3, EMBEDDED; k = 3 F 15, V 26, E 39, multiplicity 4, EMBEDDED. Pinned SAT models checked against the
  clauses; UNSAT checked by drat-trim (checker logs kept; CNF SHA-256 and proof SHA-256 in `results/0/result.json`).
  Pinned negatives: k = 2 UNSAT-VERIFIED (CNF 0b73945a...), k = 3 UNSAT-VERIFIED (CNF 9d643fed...).
* **What may be claimed** (EXACT, instance scope): the E-261103-02 encoder with `submap=True` and `ALL_OPTS` accepts a real
  embedded polyhedron whose top/front pair shares 3 and 4 collinear segments (pinned and, for k = 2, unpinned), and
  rejects the same planes on a map with a different segment pairing. Removes the A1 caveat "m >= 3 untested by a positive
  control" for the 18 (9,3), one (8,2) and 109 (10,4) maps, as far as this configuration is representative.
* **What may NOT be claimed**: coverage of other positions of the multiple segments, m >= 5, several multiple pairs in one
  map, or pairs where both faces have other multiplicities; unpinned k = 3 (15 elements) was not run; nothing about
  non-cubic objects. Not an independent review (AI session only).
* **Verdict for the direction**: FOUNDATION (control passed).
* **Next step**: week item 3 (independent census, I-261108-08); items 2-4 proceed; the item 1 caveat on (10,4) UNSATs is lifted.
* **Rows updated**: `STATUS.md` 3y, `ROADMAP.md` State done, `experiment-log.md` 2026-11-09.
