# Type-0 genus-3 -> genus-6 combinatorial completion certificate

Source: the owner's process audit of 2026-10-31 (not kept in the repository), imported 2026-11-01 and re-run here
(PASS). The certificate stands on its own: `verify.py` checks it with the standard library only.

* `certificate.json` - four triangulated maps (genus 3, 4, 5, 6) and the three explicit handle surgeries
  (remove two disjoint triangles, insert a six-triangle annulus, +6 adjacencies each):
  (1,2,10)-(4,7,9), (0,5,8)-(2,6,7), (0,9,11)-(3,5,10).
* `verify.py` - standard-library verifier: orientability, manifold vertex links, Euler characteristic, each
  handle transition, the source-file SHA-256, and the match of the final map with catalog type 0.

```bash
python3 -I verify.py certificate.json \
  --source ../../../experiments/genus_ladder/type0_genus3_extendable.json \
  --catalog ../../../data/k12_triangulations.json
```

Scope: a combinatorial sequence of closed orientable triangulated surfaces only. No geometric embedding in
R^3 is claimed for genus 4, 5 or 6 (the genus-3 level is embedded: `ladder_exact.verify`).
