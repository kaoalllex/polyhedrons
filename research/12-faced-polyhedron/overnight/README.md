# Overnight runs (autonomous, resumable)

Long computations for the 12-face Series-1 polyhedron problem, designed to run unattended on a
local machine for hours, survive interruptions, and leave results in git for later analysis.

## Setup

```bash
git clone https://github.com/kaoalllex/polyhedrons && cd polyhedrons
git checkout claude/wonderful-carson-saxyck
python3 -m pip install numpy scipy numba python-sat z3-solver sympy
cd research/12-faced-polyhedron/overnight
```

Python 3.10+. Linux or macOS recommended (on Windows use WSL). Optional, only for the `sym`
job's certified proofs: build CaDiCaL and drat-trim and put them on `PATH`
(or pass `--cadical PATH --drat-trim PATH`):

```bash
git clone https://github.com/arminbiere/cadical && (cd cadical && ./configure && make) && cp cadical/build/cadical ~/bin/
git clone https://github.com/marijnheule/drat-trim && (cd drat-trim && make) && cp drat-trim/drat-trim ~/bin/
```

## Jobs (one per invocation; re-run the same command to resume)

| Job | What it decides | Default per-task timeout |
|---|---|---|
| `normals` | **Main constructive experiment (E1).** For each near-miss seed (1005 configurations from HackerPoet/NeighborlyPolyhedra, `data/seeds.json`, sorted by violation count), fix the 12 face normals and decide EXACTLY (z3, linear real arithmetic) whether any choice of the 12 plane offsets gives an embedded polyhedron. Then the same for perturbed normals (sigma 0.003-0.1) of the best seeds. Every SAT answer is re-checked by an independent exact rational checker; a positive check is saved as a CANDIDATE and committed immediately. | 1800 s |
| `sym` | Every symmetric case (each conjugacy class of half-turn and 3-fold subgroups of Aut of all 59 maps; these imply all larger groups). Expected: all UNSAT (claimed by prior work; 4 cases already reproduced here). With cadical + drat-trim each UNSAT gets a checked DRAT proof (status `UNSAT-VERIFIED`); a SAT would contradict the claimed theorem and is saved as a CANDIDATE. | 4 h |
| `cube` | Cube-and-conquer on the full asymmetric OM-SAT instance of Lutz map(s) `--maps` (default #1, which a third party claims UNSAT after ~300 core-hours). Reports the refuted fraction of the search space; timed-out cubes are split. Experimental. | 900 s per cube |
| `ils` | Iterated local search from the seeds: exact single-plane relocation (global optimum over all positions of one plane) plus random kicks. A configuration with 0 violations is re-checked exactly and saved as a CANDIDATE. | 20 min per seed |

Recommended night (adjust `--workers` to the number of cores minus one):

```bash
python3 run_overnight.py normals --hours 8 --workers 7 --git
```

Other runs:

```bash
python3 run_overnight.py sym --hours 6 --workers 7 --git
python3 run_overnight.py ils --hours 4 --workers 7 --git
python3 run_overnight.py cube --maps 1 --hours 8 --workers 7 --git
python3 run_overnight.py status
```

`--git` commits `results/` every 30 minutes (`--commit-minutes`), on stop, and immediately when
a candidate appears; add `--push` to push each commit. Otherwise commit and push `results/`
yourself when the run ends:

```bash
git add research/12-faced-polyhedron/overnight/results && git commit -m "overnight results" && git push
```

## Files

* `results/<job>/results.jsonl`: one JSON record per finished task, appended and fsync'ed
  after every task. A power cut loses only the tasks that were running; re-running the same
  command skips finished tasks.
* `results/<job>/CANDIDATES/`: anything that passed an exact check (or, for `sym`, a SAT).
* `results/cube_map<k>/state.json`: open cubes and refuted fraction (atomic writes).
* `work/`: large temporary CNF/proof files (not committed).

## Interpreting results

* `normals`: `UNSAT` = no embedded polyhedron has exactly these face normals (any offsets), for
  that seed's combinatorial type. `UNKNOWN` = timeout. `SAT` + `exact_embedded: true` = a
  genuine solution (planes are integers; verify again independently before announcing).
* Numerical counts in `ils` are floating point; only the exact re-check counts as evidence.
