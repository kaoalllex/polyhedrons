# Witnesses: our notable exact objects

This is a curated list of the objects this project built that are worth showing or citing. It is one entry per
object in `witnesses.json`; the data stays in its source file, so nothing is copied twice.

| id | Object | Target | Source | Why it matters |
|---|---|---|---|---|
| `lab_type0_genus3` | 12 faces, genus 3, 48 of 66 pairs adjacent, all adjacencies single | S3 | `experiments/E-261030-03-genus-ladder-type0-genus3/results/type0_genus3_extendable_polished.json` | the best exact object: its map can be completed combinatorially to target type 0 by 3 handles (`verification/certificates/type0_handle_completion/`); the subject of ROADMAP E-261101-03 |
| `lab_solid_genus3` | 12 faces, genus 3, 48 of 66 pairs, another map | S3 | `experiments/E-261030-02-solid-first-exact-inner-n12/results/genus3_12faces_48pairs_polished.json` | found from random planes without a given map (solid-first); a dead-end map |
| `lab_s6_10_genus2` | 10 faces, genus 2, 36 of 45 pairs, single adjacencies | S6 (10,2) | `s6_10_2_polished.json` (polished copy of `s6_10_2.json`) | face-minimal in SPEC's cubic single-adjacency class; a positive control on 10 planes; literature novelty not established |

None of them is a solution: only `verification/verify_candidate.py FILE --target S0` PASS is one (`SPEC.md` §1).

## S6 (10,2): provenance and scope

Found by Claude's `s6_native.py`, seed 903, iteration 4, in dialogue `2026-11-10-strategy`;
recovered and verified by Astra. This was a bounded session check, not a pre-registered experiment.
The session logs contain 45 numerical trials (44 with 30 adjacent pairs, one with 36);
four other workers failed to start because `timeout` was unavailable. No success-rate estimate is claimed.
The source rounds the saved planes to integers at scale 1e9 and coherently orients the face cycles.
Both 1e9 and 1e12 rationalizations passed the standard embedding verifier and a separately written
rational checker; their maps agree. `verify_s6_10_2.py` preserves the latter implementation without
importing project geometry. The canonical source is checked by `verify_all.py`.

The found planes are nearly degenerate (beauty 1.8e-4: margin 5e-7, shortest edge 3e-4 of the diameter,
thinnest face 0.04; one vertex far out, principal axes 10 : 1). The site shows `s6_10_2_polished.json`:
the same map, planes moved by the `code/polish_solid.py` hill climb (a move is kept only if the map is unchanged,
the embedding energy stays 0 and `code/beauty.py` does not decrease), then rounded at scale 1e9. Beauty 4.8e-2
(margin 8.5e-3, edge 5.7e-2, fat 0.22), axes 2.4 : 1. Both verifiers check both files; counts and face sizes agree.
The polished copy adds no mathematical claim; longer polishing reached a plateau (+2 % in 20 more core-minutes).

Counts: V=24, E=36, F=10, chi=-2, genus 2; face sizes 6,6,7,7,7,7,7,8,8,9.
Checks include simple faces, cubic closed connected orientable topology, all 45 face-pair intersections,
distinct vertices, nonzero edges, independent normal triples and nonconcurrent plane quadruples.
The independent algorithm's justification is PROVED-1; AI checks are not human review.
This establishes an object in the S6 class, not a new minimality theorem or literature novelty.
It does not settle S6 (10,3), S1 with nine faces, or S0; there is no claimed geometric continuation to them.

## Rules

* **Who adds an entry.** The `candidate-check` skill, after `verify_candidate.py` passes and the object is in a
  `verify_all` check. Each entry needs `id`, `label`, `title`, `source`, `target` and `genus`.
* **How the site is built.** `export_site.py` re-verifies every entry exactly and writes the "Our search" models
  into the root `index.html`, between the LAB markers.
  * Each model is prefixed `Lab ·` and links to its source file on GitHub.
  * Never edit that block by hand. After changing `witnesses.json`, run `python3 witnesses/export_site.py`.
* **What checks it.** `verification/verify_all.py` runs `export_site.py --check`, so the site and this list
  cannot drift apart.
* **Larger data.** The 247-realization archive (`experiments/E-261030-10-realization-archive-climb/results/arch/archive.json`) is a dataset, not a list of
  witnesses. Add one of its records here only if it has a reason of its own to be shown.
