# Witnesses: our notable exact objects

This is a curated list of the objects this project built that are worth showing or citing. It is one entry per
object in `witnesses.json`; the data stays in its source file, so nothing is copied twice.

| id | Object | Target | Source | Why it matters |
|---|---|---|---|---|
| `lab_type0_genus3` | 12 faces, genus 3, 48 of 66 pairs adjacent, all adjacencies single | S3 | `experiments/E-261030-03-genus-ladder-type0-genus3/results/type0_genus3_extendable_polished.json` | the best exact object: its map can be completed combinatorially to target type 0 by 3 handles (`verification/certificates/type0_handle_completion/`); the subject of ROADMAP E01 |
| `lab_solid_genus3` | 12 faces, genus 3, 48 of 66 pairs, another map | S3 | `experiments/E-261030-02-solid-first-exact-inner-n12/results/genus3_12faces_48pairs_polished.json` | found from random planes without a given map (solid-first); a dead-end map |

None of them is a solution: only `verification/verify_candidate.py FILE --target S0` PASS is one (`SPEC.md` §1).

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
