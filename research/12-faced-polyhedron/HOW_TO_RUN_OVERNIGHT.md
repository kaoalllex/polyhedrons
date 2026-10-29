# How to run the overnight search / Как запустить ночной расчёт

Everything runs locally, unattended, resumes after interruptions, and saves results into the
repository. Details of each job: `overnight/README.md`.

## 1. One-time setup / Однократная подготовка

```bash
git clone https://github.com/kaoalllex/polyhedrons
cd polyhedrons
git checkout claude/wonderful-carson-saxyck
python3 -m pip install numpy scipy numba python-sat z3-solver sympy
```

Python 3.10+; Linux or macOS (on Windows use WSL).

## 2. Start / Запуск

```bash
cd research/12-faced-polyhedron/overnight
python3 run_overnight.py gnormals --hours 8 --workers 7 --git
```

* `--hours` — how long to run (the program stops by itself) / сколько часов работать.
* `--workers` — number of CPU cores minus one / число ядер минус одно.
* `--git` — commit results every 30 min and immediately on a candidate / коммитить результаты
  каждые 30 минут и сразу при находке. Add `--push` to push automatically / с `--push`
  ещё и пушить.

If the computer turns off, run **the same command** again: finished tasks are skipped.
Если компьютер выключился — запустите **ту же команду** ещё раз, работа продолжится.

Progress / прогресс: `python3 run_overnight.py status`

## 3. After the run / После расчёта

```bash
cd ../../..        # repository root
git pull
git add research/12-faced-polyhedron/overnight/results
git commit -m "overnight results"
git push
```

## 4. Other jobs (optional) / Другие задачи (по желанию)

| Command | Purpose |
|---|---|
| `python3 run_overnight.py gnormals ...` | **main**: topologically admissible normals + exact offset search (all 59 types) |
| `python3 run_overnight.py sym --hours 6 --workers 7 --git` | certified UNSAT for all symmetric cases (needs `cadical` and `drat-trim` on PATH for proofs, see `overnight/README.md`) |
| `python3 run_overnight.py cube --maps 1 --hours 8 --workers 7 --git` | cube-and-conquer on the full asymmetric SAT instance of Lutz map #1 |
| `python3 run_overnight.py ils --hours 4 --workers 7 --git` | local search with exact plane relocation from known near-misses |

Run one job at a time (each uses all `--workers`). The old `normals` job is superseded: all its
seeds are excluded instantly by the Gauss-map prefilter.

If anything prints `CANDIDATE`, the configuration is saved under
`overnight/results/<job>/CANDIDATES/` and committed at once — push it and tell Claude.
