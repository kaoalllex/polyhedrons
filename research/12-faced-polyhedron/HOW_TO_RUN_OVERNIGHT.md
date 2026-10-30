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
./run_night.sh 8 7
```

`8` = hours, `7` = workers (CPU cores minus one). Phase 1 verifies all symmetric cases (`sym`),
phase 2 tests every type for a polyhedral immersion (`immersion`). An `UNSAT` in phase 2 would
mean that type has no immersion and hence no embedding — it is committed immediately.
Часы и число ядер — аргументы скрипта. Фаза 1 — проверка симметричных случаев, фаза 2 — есть ли
у каждого из 59 типов погружение (UNSAT = у типа нет и вложения; коммитится сразу).

Optional for certified proofs in phase 1 / для сертификатов в фазе 1: install `cadical` and
`drat-trim` (see `overnight/README.md`); without them phase 1 results are marked unverified.

* `--hours` — how long to run (the program stops by itself) / сколько часов работать.
* `--workers` — number of CPU cores minus one / число ядер минус одно.
* `--git` — commit results every 30 min and immediately on a candidate / коммитить результаты
  каждые 30 минут и сразу при находке. Add `--push` to push automatically / с `--push`
  ещё и пушить.

If the computer turns off, run **the same command** again: finished tasks are skipped.
Если компьютер выключился — запустите **ту же команду** ещё раз, работа продолжится.

Progress / прогресс: `python3 run_overnight.py status`

### Night 2 / Вторая ночь

```bash
cd research/12-faced-polyhedron/overnight
git pull
./run_night2.sh 8 7
```

Phase 1 (~15 min): DRAT-certified proof that no SYMMETRIC polyhedral immersion exists.
Phase 2: period-defect search over all 59 types (a defect of 0 is saved as a CANDIDATE).
Фаза 1 — сертификаты «нет симметричных погружений», фаза 2 — поиск нормалей с нулевым
«дефектом периодов» по всем 59 типам.

### Night 3 / Третья ночь

Start only after the previous night job has exited (commit its results first, then merge):
Запускать только после того, как прошлый ночной расчёт завершился (сначала закоммитить его
результаты, потом подтянуть origin):

```bash
cd research/12-faced-polyhedron/overnight
git add -A results && git commit -m "overnight results"
git pull
./run_night3.sh 8 7
```

Revised 2026-10-30: the whole night is the **genus ladder** over all 59 types (2 chains each): every
neighbourly 12-face map = a simple 12-faced polyhedron + 6 handles; the job realizes genus 0, 1, 2, ...
step by step (each level seeded from the one below, exact check). Result per type: the highest
exactly realized genus; genus 6 = a solution (saved as CANDIDATE and committed at once). When a chain
reaches genus >= 2 and then stalls, the job branches for up to 30 min: from the highest realized
polyhedron it tries every next handle that keeps all 66 pairs reachable (`code/beam_ladder.py`).
Вся ночь — «лестница рода» по всем 59 типам: для каждого типа — наибольший точно реализованный род;
род 6 = решение.

### Night 4 / Четвёртая ночь

After night 3 has finished (commit its results first, then merge):
После окончания третьей ночи (сначала закоммитить её результаты, потом подтянуть origin):

```bash
cd research/12-faced-polyhedron/overnight
git add -A results && git commit -m "night 3 results" && git push
git fetch origin
git merge origin/claude/practical-archimedes-e5p1fi
./run_night4.sh 8 11
```

Revised 2026-10-30 evening: phase 1 `gate` (Gauss gate, minutes), then in parallel `arch --gauss-gate` on a
third of the cores and `n5` (normals first + exact offsets, drift to handle degree -1, genus 6) on the rest
(see the Night 5 section below for what `n5` does). Morning summary: `python3 analyze_n5.py`.

Realization archive + bandit (`code/archive_climb.py`): every exactly realized polyhedron of genus >= 2 from
night 3 is a starting point; every next handle that keeps all 66 pairs reachable is an "arm"; time goes to
the most promising arms, and a quarter of it to new, different realizations of the same polyhedra
(the trick that gave the best genus-4 attempts by hand). The log shows edge and margin of each best
attempt: tiny values (near 3e-5 / 1e-6) mean a degenerate limit, not a near-solution.
Архив реализаций + «бандит»: старт от всех точно реализованных полиэдров рода >= 2 из третьей ночи.

Sleep / lid close: the time budget counts awake time only, so closing the laptop lid (the Mac sleeps,
processes freeze) costs nothing; on wake the run continues with the remaining budget. Plug in the power
before opening the lid: all workers resume at once. No `caffeinate` needed.
Сон / закрытая крышка: бюджет считается только по времени бодрствования, так что в дороге ничего не
теряется; после пробуждения расчёт продолжается.

### Night 5 / Пятая ночь

After night 4 has finished. The night-5 code is on branch `claude/practical-archimedes-e5p1fi` (the research
branch + the session of 2026-10-30 afternoon); merge it into the branch you run from:
После окончания четвёртой ночи. Код пятой ночи лежит в ветке `claude/practical-archimedes-e5p1fi`;
влейте её в рабочую ветку:

```bash
cd research/12-faced-polyhedron/overnight
git add -A results && git commit -m "night 4 results" && git push
git fetch origin
git merge origin/claude/practical-archimedes-e5p1fi
./run_night5.sh 8 11
```

Why (independent review 2026-10-30): the genus-4 plateau is a Gauss-map degree obstruction. At every saved
genus-3 polyhedron the next handle contributes degree k_tau = 0, but genus 4 needs -1, so starting the next
level from the planes of the level below starts in an excluded class. Night 5 therefore moves the NORMALS
first and decides the offsets exactly:
* phase 1, `gate` (minutes): for every exactly realized polyhedron (nights 3-4, `experiments/genus_ladder/`)
  and every next handle: degree, k_tau, admissible orientations (test T1); and test 2.2 on the night-3 chains;
* phase 2, `n5` (all but one core): `nfirst` = anneal the normals near a realization into the next map's
  class, then z3 decides EXACTLY whether offsets exist (SAT = next genus, re-checked by the exact
  verifier, saved to `results/n5/realized/` and climbed further at once); `kdrift` = move the polyhedron
  (staying embedded) until k_tau = -1, then the same; `g6` = genus 6 directly from random normals;
* one core: night-4 `arch` as the control.
Morning summary: `python3 analyze_n5.py`.
Почему: плато рода 4 — это препятствие степени отображения Гаусса (вклад ручки 0 вместо −1). Ночь 5
сначала двигает нормали в нужный класс, а смещения решает точно (z3); найденный род сразу
проверяется точным верификатором и поднимается дальше. Утренняя сводка: `python3 analyze_n5.py`.

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
| `python3 run_overnight.py immersion --hours 8 --workers 7 --git` | OM-SAT: does each type admit a polyhedral immersion (no global clauses)? |
| `python3 run_overnight.py gnormals --hours 8 --workers 7 --git` | Gauss-admissible normals + exact offset search (all 59 types); mostly fast UNSAT expected |
| `python3 run_overnight.py sym --hours 6 --workers 7 --git` | certified UNSAT for all symmetric cases (needs `cadical` and `drat-trim` on PATH for proofs, see `overnight/README.md`) |
| `python3 run_overnight.py cube --maps 1 --hours 8 --workers 7 --git` | cube-and-conquer on the full asymmetric SAT instance of Lutz map #1 |
| `python3 run_overnight.py ils --hours 4 --workers 7 --git` | local search with exact plane relocation from known near-misses |

Run one job at a time (each uses all `--workers`). The old `normals` job is superseded: all its
seeds are excluded instantly by the Gauss-map prefilter.

If anything prints `CANDIDATE`, the configuration is saved under
`overnight/results/<job>/CANDIDATES/` and committed at once — push it and tell Claude.
