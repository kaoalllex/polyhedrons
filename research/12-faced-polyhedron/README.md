# Research: the 12-face polyhedron (Series 1, F = 12)

Does a polyhedron embedded in R^3 exist with 12 planar simple faces, every two sharing exactly one edge, three
faces per vertex (V = 44, E = 66, genus 6)? Open since Szilassi (1977) found the 7-face one. Exact statement:
`SPEC.md`.

**State (2026-11-01):** no solution and no impossibility proof. Certified: no symmetric solution. Checked by
DRAT proofs, write-up pending: not even a symmetric polyhedral immersion. Best exact object: genus 3 (48 of 66 adjacent pairs) on a map that is
combinatorially completable to a target map. Genus 4 was never reached. Details and verdicts: `STATUS.md`.

## Read in this order

New here? Start with `GLOSSARY.md` (the key terms in plain words).

1. `STATUS.md` - foundations, exact witnesses, every direction with its verdict, what may be claimed.
2. `ROADMAP.md` - the scored, pre-registered experiment queue and the parked methods.
3. `PROTOCOL.md` - how experiments are run, verified, recorded; branches; laptop and GitHub Actions.
4. `SPEC.md` - target, relaxed targets, degeneracies, counters, evidence labels.
5. `experiments/E##-*/CONCLUSION.md` (evidence), `experiment-log.md` (append-only chronology), `results.md` (frozen
   evidence up to 2026-11-01) when you need details.

## Layout

| Path | Content |
|---|---|
| `SPEC.md`, `STATUS.md`, `ROADMAP.md`, `PROTOCOL.md` | the four living control documents |
| `GLOSSARY.md` | the key terms in plain words |
| `results.md`, `experiment-log.md` | evidence up to 2026-11-01 (frozen); chronology (append-only) |
| `CONTINUE_PROMPT.md` | hand-over prompt for a new AI session |
| `theory/` | mathematical model, theory notes (lemmas, Gauss degree), proof roadmap |
| `proof-no-symmetric-immersion/` | write-up of the symmetric-immersion theorem (ROADMAP E08) |
| `code/` | all scripts; registry with status per module: `code/README.md` |
| `verification/` | exact verifiers, `verify_all.py`, `verify_candidate.py`, certificates, foundations report |
| `experiments/` | `E##-slug/` pre-registered experiments (template `_template/`); legacy artifact folders |
| `overnight/` | night-run framework (`run_overnight.py`, `run_night*.sh`, `HOW_TO_RUN.md`) and its results |
| `data/` | the 59 combinatorial types with invariants (`data/README.md`) |
| `literature/` | source matrix (`literature/README.md`), third-party data (untrusted), notes |
| `reviews/` | independent reviews and audits (2026-10-30 review, 2026-10-31 audits, fresh-eyes review) |
| `reports/` | night reports |
| `ideas/` | idea backlog (cross-field ideas, search algorithms, brainstorms) - not a plan |
| `witnesses/` | curated exact objects (`witnesses.json`); source of the site's "Lab ·" models |
| `figures/` | pictures and interactive HTML of results |
| `archive/` | superseded documents (sprint board, old protocol, old continue prompts) |

## Verify everything (one command)

```bash
cd research/12-faced-polyhedron
python3 -m pip install -r requirements.txt
python3 verification/verify_all.py          # 9 checks, ~15 s; --quick skips the archive re-check
python3 verification/verify_candidate.py experiments/E-261030-03-genus-ladder-type0-genus3/results/type0_genus3_extendable.json
```

CI runs `verify_all.py` on every push touching `research/` (`.github/workflows/verify.yml`).

## Run an experiment

Pick the top open row of `ROADMAP.md`, copy `experiments/_template/` to `experiments/E##-slug/`, fill `PLAN.md`
before any compute, then run `run.sh` on the laptop (`caffeinate -dimsu bash run.sh 0`) or push branch
`experiment/E##-slug` with `[run]` in the commit message (GitHub Actions, one job per shard of `matrix.json`).
Full rules: `PROTOCOL.md`.
