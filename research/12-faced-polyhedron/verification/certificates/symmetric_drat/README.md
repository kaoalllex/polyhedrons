# DRAT certificates of the symmetric cases (FD5, FD6)

The certificates behind `STATUS.md` FD5 (no symmetric embedding) and FD6 (no symmetric polyhedral immersion):
25 symmetry classes each, every one UNSAT, every proof checked by drat-trim.

The archives are too large for git. They are attached to the GitHub release
[`state-2026-11-01`](https://github.com/kaoalllex/polyhedrons/releases/tag/state-2026-11-01):

| Archive | Size | Content | Result records |
|---|---|---|---|
| `symmetric-sym-drat.tar.xz` | 422 MB | 25 CNF + 25 DRAT (FD5, embedding) | `experiments/E-261029-13-symmetric-embedding-certificates/results/sym/results.jsonl` |
| `symmetric-symimm-drat.tar.xz` | 438 MB | 25 CNF + 25 DRAT (FD6, immersion) | `experiments/E-261029-15-symmetric-immersion-certificates/results/symimm/results.jsonl` |

`SHA256SUMS` in this folder holds the archive hashes. Each record in the two `results.jsonl` files holds the
SHA-256 of its CNF (`cnf_sha256`) and of its proof (`proof_sha256`). A copy of those records is inside each
archive (`files/results.jsonl`).

## Provenance

* **Original runs.** Nights 1-2 (2026-10-29). Those proofs were deleted after checking: `run_overnight.py`
  deleted them by default, and since 2026-11-01 it keeps them.
* **Regeneration.** 2026-11-01 from commit 72ccc52. The encoder (`code/omsat.py`, `code/omsat_sym.py`) was last
  changed in 831039f.
* **Command.**

  ```
  run_overnight.py sym [--sym-immersion] --keep-proofs --keep-cnf
  ```

* **Result.** All 50 CNFs and all 50 proofs are bit-identical to the hashes recorded by the original runs, and
  all 50 were VERIFIED again.
* **Solver and checker.**
  * Solver: CaDiCaL 3.0.1 (git c607304), single-threaded.
  * Checker: drat-trim, git 2e3b2dc (2024-11-25).

## Check them yourself

```bash
gh release download state-2026-11-01 -R kaoalllex/polyhedrons -p 'symmetric-*.tar.xz'
shasum -a 256 -c SHA256SUMS
tar -xJf symmetric-sym-drat.tar.xz          # -> files/sym_*.cnf, files/sym_*.drat, files/results.jsonl
drat-trim files/sym_36_C2_0.cnf files/sym_36_C2_0.drat    # expect "s VERIFIED"; repeat for every case
```

To check that the current encoder still produces the same formulas, re-generate a CNF with
`run_overnight.py sym --only <task> --results-dir /tmp/x` and compare its SHA-256 with `cnf_sha256`.

The soundness of the encoding is a separate question:
* FD5 rests on Lemma 5.1 (FD2, PROVED-1).
* For FD6 the soundness argument is the subject of ROADMAP E-261101-10; until then FD6 is EXACT, not CERTIFIED.
