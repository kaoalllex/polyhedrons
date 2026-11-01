# Fresh-eyes audit of the 12-face research workflow (2026-11-01)

Scope: branch `claude/research-restructure` (3 commits ahead of `main`, no PR yet), the four control
documents and everything around them, the agent/skill/prompt layer. Paths below are relative to
`research/12-faced-polyhedron/` unless they start with `.claude/`, `.github/` or `/`.
Nothing in the repository was modified. `verification/verify_all.py --quick` was run with the
`polyhedra` venv: **8 PASS, 1 SKIP (archive), ALL PASS, 12 s**. Last CI run of `verify` on this branch: success
(run 41287132262).

## Verdict

1. The restructure is good and mostly real: one SPEC, one ledger, a scored queue with stop rules, a
   pre-registration template, a one-command verifier in CI. It is closer to working lab practice than most
   one-person projects. Link hygiene is fine: no broken references to moved files outside `archive/`.
2. But the system breaks its own rules in several places. STATUS labels contradict SPEC §5 (FD1/FD2/FD6/FD8),
   two queued items fail the ROADMAP's own T + D >= 3 gate (E05, E10), and `results.md` still uses the old
   label vocabulary (0 SPEC labels).
3. The machine "success criterion" does not encode S0. `ladder_exact.verify(require_all_pairs=True)` accepts
   doubled-adjacency (S1) objects of any face count. Checked: the 8-face Roest-Vigh S1 control returns
   `EMBEDDED True, all_pairs_adjacent True`. E09 is about to generate 12-face S1 objects.
4. The AI layer has not been migrated. The 7 agents use their own label scheme ([P]/[K]/[C]/[N]) and stale
   CPU limits (4 cores). None of them knows about ROADMAP, the stop list or `verify_candidate.py`. The
   `computational-search` description advertises exactly the black-box engines on the stop list. There is no
   project CLAUDE.md, so the rules reach a session only if someone pastes the right prompt.
5. Biggest non-document risks: the only copies of the certificates (DRAT, 860 MB) and 3.2 GB of work data are
   on one laptop. There is no LICENSE, CITATION, tag or DOI. There are two run frameworks with different
   provenance (`overnight/run_overnight.py` vs `experiments/_template/run.sh`), and the sleep / `caffeinate`
   guidance contradicts itself (it already cost 8 h).

## Findings

Severity: **critical** = can produce a false claim or lose irreplaceable data; **major** = undermines the
workflow's guarantees; **minor** = friction or drift.

| ID | Sev | Area | Finding | Evidence | Recommendation |
|---|---|---|---|---|---|
| F01 | critical | verification | The SPEC calls one check "the only success criterion", but it does not check S0. `verify(..., require_all_pairs=True)` checks neither 12 faces, nor single adjacency, nor V=44/E=66/chi=-10. A 12-face S1 object with doubled pairs passes and `verify_candidate --all-pairs` exits 0. Reproduced on Roest-Vigh: `8 True True (24, 36, 8, -4)`. | `SPEC.md:26-28`; `code/ladder_exact.py:141-142`; `verification/verify_candidate.py:38-60`; `ROADMAP.md:40` (E09 targets 12-face S1) | Add `--target S0` to `verify_candidate.py`: require `len(planes)==12`, no repeated neighbour in any `links[X]`, `V_E_F_chi==(44,66,12,-10)`, `all_pairs_adjacent`, `EMBEDDED`. Point SPEC §1 at that flag and add the Roest-Vigh file as a negative control for it in `verify_all`. ~15 lines. |
| F02 | major | verification | `--all-pairs` is ignored for solid-first files: `_solid` always calls `verify_solid.py`, which runs with `require_all_pairs=False`. The default of `verify_candidate` is also the relaxed check (the library default is the opposite). | `verify_candidate.py:31-35,42-43`; `code/verify_solid.py:19`; `ladder_exact.py:61` | Pass the target through to the solid path, or reject `--all-pairs/--target` for solid files. Print the target in every output line. |
| F03 | major | verification | The witness checks prove "embedded" but not the claimed property. A regression that drops a witness to genus 2 or 42 pairs would still PASS. `verify_all` says nothing about 48/66 or genus 3. | `verification/verify_all.py:26-29,44-49`; claims in `STATUS.md:36` | `files()` should also compare `V_E_F_chi` / adjacent-pair count to the expected value per check (e.g. `chi=-4`, 48 pairs). |
| F04 | major | ledger | STATUS uses labels that SPEC forbids. FD1 is "PROVED" with caveat "reviewers were AI agents", while SPEC says PROVED needs an independent reviewer and AI agents do not count. Same for FD2 "PROVED + EXACT tests" and FD8. FD6 is "CERTIFIED", but SPEC requires a written soundness argument and its own caveat says the soundness proofs are pending. | `STATUS.md:20,21,25,27`; `SPEC.md:77-85`; `proof-no-symmetric-immersion/README.md:29-31` | Relabel FD1/FD2/FD8 as PROVED-1 (+EXACT). Make FD6 "EXACT (DRAT-checked); CERTIFIED after E08". Soften `README.md:7-8` ("Certified: ... not even a symmetric polyhedral immersion") the same way. Lint it (F17). |
| F05 | major | ledger | `results.md` was not migrated to SPEC §5. It has 0 SPEC labels and uses `[N]`, `[E]`, `[P]`, `[K]`, `[computed]`, while SPEC says "use these labels in STATUS.md and results.md". | `SPEC.md:73`; `grep` of `results.md` | Do not relabel 275 lines. Freeze `results.md` as historical (header line + move to `archive/` or mark it frozen), and let new evidence live in `experiments/E##/CONCLUSION.md`. See F09. |
| F06 | major | roadmap | Two queued items fail the ROADMAP's own gate: E05 (T1 D1) and E10 (T1 D1) have T + D = 2 < 3, and the rule says "do not run". | `ROADMAP.md:12,36,41`; `PROTOCOL.md:26` | Either re-score with a written reason or move them to an "ideas / below the gate" list. The rule only means something if it is applied to the first queue. |
| F07 | major | roadmap / feedback loop | The queue has no state column (open / running / done / killed / blocked), and no item links to its folder or branch. "The top open item", the hand-over rule of `CONTINUE_PROMPT.md:28` and `PROTOCOL.md:90-91`, cannot be determined once E01 is done. No ordering rule either: E01 (sum 8) sits above E03/E06 (sum 10) with no stated reason. | `ROADMAP.md:28-41`; `CONTINUE_PROMPT.md:28` | Add a `State` column and a `Folder` column. State the ordering rule in one line, e.g. "E01 first because it validates FD10, the verifier every other item relies on" (that reason is in `ROADMAP.md:55`). `CONCLUSION.md` gets a "ROADMAP row updated" line. |
| F08 | major | roadmap | Detail sections exist for E01-E04 and E06 only. E05 and E07-E10 have no hypothesis or outcome meaning, although the ROADMAP says "every item states what SAT / UNSAT / timeout / near-miss would mean before it runs". | `ROADMAP.md:13` vs sections at `:47-86` | This is fine if `PLAN.md` carries it. Change the sentence to "before it runs, in its PLAN.md", so the ROADMAP stays a queue, not a second plan. |
| F09 | major | single source of truth | The same facts are kept by hand in 5-7 places: 25/25 UNSAT, 94/247 realizations, 12,202 UNSAT, genus 3 = 48/66. They appear in `README.md:7-9`, `STATUS.md:9-14`, `results.md:265ff`, `experiment-log.md:628-641`, `reports/NIGHT_REPORT_2026-11-01.md`, `proof-no-symmetric-immersion/README.md:19-28` and root `README.md`. STATUS itself admits this is a manual sync ("never let it drift from results.md"). PROTOCOL asks for three writes per conclusion. | `STATUS.md:4-5`; `PROTOCOL.md:36` | One fact, one home. STATUS owns verdicts and numbers. CONCLUSION.md / night reports own the evidence. `experiment-log.md` gets a 1-3 line dated pointer. README files link to STATUS instead of restating numbers (keep a one-line state at most). Drop `results.md` from the per-conclusion write list. |
| F10 | critical | data / provenance | The only copies of the certificates behind FD5/FD6 (`symmetric-{sym,symimm}-drat.tar.xz`, 860 MB, plus `SHA256SUMS`) and the 3.2 GB work dir are on the owner's MacBook. Publishing them is a TODO. | `ROADMAP.md:21-25`; `overnight/work/regen/release/` (local, gitignored `.gitignore:6`) | Today: create a GitHub release on a tag (files are < 2 GB each) and attach both tarballs + `SHA256SUMS`. Then enable the GitHub-Zenodo integration for a DOI. Record URL + archive SHA-256 in STATUS FD5/FD6. |
| F11 | major | provenance | The certificate records have CNF/proof SHA-256 but no encoder commit and no solver/checker versions (cadical, drat-trim). These binaries are outside `requirements.txt`, and CI cannot re-check anything about FD5/FD6. | `overnight/results/sym/results.jsonl` (first record); `requirements.txt:3-10`; `verify_all.py:33-58` (no SAT check) | Put `cadical --version`, the drat-trim commit and the encoder commit into the release README. Add a cheap `verify_all` check: re-encode 2-3 small symmetric instances (e.g. #54 T) and compare `cnf_sha256` with the JSONL. It proves HEAD still produces the certified formulas, without any solver. |
| F12 | major | licensing / citation | No `LICENSE`, no `CITATION.cff`, no tag, no DOI. The repository is public. Vendored third-party code (`literature/Hashirama1337s-szilassi-12/code/omsat.py`, `autos.py`) is MIT with "LICENSE-CODE", but the licence file is not vendored. Licence of HackerPoet `print_data.py` not recorded. | `git ls-files`; `literature/Hashirama1337s-szilassi-12/README.md:202-210` | Add `LICENSE` (code: MIT; data/text: CC BY 4.0 is the norm here) and `CITATION.cff`. Copy the upstream `LICENSE-CODE` next to vendored code or keep only data. Tag `state-2026-11-01` after merge (already a TODO at `ROADMAP.md:26`). |
| F13 | major | compute ops | The sleep guidance contradicts itself in three places. PROTOCOL says "always under `caffeinate -dimsu` (night 4 lost 8 h to sleep)". HOW_TO_RUN says "No `caffeinate` needed". The skill's checklist never mentions caffeinate, and no `run_night*.sh` uses it. The monotonic budget protects the budget, not the night: idle sleep with the lid open still loses the hours. | `PROTOCOL.md:65`; `overnight/HOW_TO_RUN.md:112-115`; `.claude/skills/overnight-run-script/SKILL.md:11-21,23-37`; `experiment-log.md` night-4 entry | One rule everywhere: wrap the night script in `caffeinate -dimsu` (or `caffeinate -i` in the script) with AC power and the lid open. Lid close = pause (budget-safe). Fix HOW_TO_RUN:115 and add it as checklist item 0 of the skill. |
| F14 | major | code / workflow | Two run frameworks with different guarantees. `overnight/run_overnight.py` has resume, `--git` commits, JSONL, but no manifest (no commit SHA, no pip freeze, no core-hours). `experiments/_template/run.sh` has a manifest but no resume, no checkpoint helper, no commits. PROTOCOL wants both: manifest (§5) and the skill (§6). The skill only knows the first, the template only the second. STATUS's compute ledger promises exact core-hours "from now on" (`STATUS.md:101`), which only `run.sh` provides. | `overnight/run_overnight.py:21-22,102-125`; `experiments/_template/run.sh:13-29`; `PROTOCOL.md:55-67` | Simplest bridge: an experiment's `run.sh` calls `run_overnight.py <job> ... --out "$OUT"` (or symlinks its results dir), so a laptop night gets manifest + resume. Update the skill to say so. Do not build a third framework. |
| F15 | major | certificates | `run_overnight.py` still deletes proofs by default (`keep_proofs` false). Only the documented command line was changed, and that default is what lost the original certificates. | `overnight/run_overnight.py:911,1246`; `ROADMAP.md:21`; commit 85ef222 | Flip the default to keep (`--no-keep-proofs` for space-constrained runs). One line. |
| F16 | major | stop rules | The stop list is prose only. Every dead engine is still one command away (`run_overnight.py` jobs, `run_night4/5.sh`). Neither the workflow nor run.sh checks that an `experiments/<ID>` matches a ROADMAP row that passes the gate. The workflow accepts any `[A-Za-z0-9._-]` id. | `ROADMAP.md:88-92`; `.github/workflows/experiment.yml:36-40`; `overnight/run_night4.sh`, `run_night5.sh` | Cheap enforcement: (a) the lint in F17 checks that each `experiments/E##-*` has a PLAN.md and a ROADMAP row with T+D>=3; (b) the workflow's id regex becomes `^E[0-9]{2}-`; (c) move `run_night*.sh` to `overnight/archive/` (history; reopening = copy back with a STATUS reason). |
| F17 | major | doc drift | Nothing checks the control documents themselves. Labels, gate scores, paths and IDs drift by hand (F04, F06 are the proof). | - | Add `verification/lint_docs.py` (~60 lines) to `verify_all`: STATUS Level column ⊆ SPEC §5 labels; ROADMAP rows T+D>=3; backticked repo paths in the control docs exist (template placeholders `E##`, `<ID>` excluded); every `experiments/E??-*` folder has PLAN.md + ROADMAP row. |
| F18 | major | AI layer | No project-level `CLAUDE.md`. The invariant rules (Russian to the owner, English files, stop list, verify before claims, ask before large subagent tasks, no pty) reach a session only if `CONTINUE_PROMPT.md` is pasted. They never reach a session the owner opens ad hoc. | `ls /Users/a.konyaev/src/my/polyhedrons` (no CLAUDE.md); `CONTINUE_PROMPT.md:3-4` | Add a short root `CLAUDE.md` (≤ 30 lines): site vs research split, read order (STATUS → ROADMAP → PROTOCOL → SPEC), the 6 hard rules, verify command with the venv path, skill names. Then `CONTINUE_PROMPT.md` shrinks to the hand-over delta (see S5). |
| F19 | major | AI layer | `computational-search` is described as "penalty optimization over face planes, multistart, annealing, evolutionary search, continuation", which is the DR6 stop list. The description is what routes tasks to an agent. Its rules tell it to append to `experiment-log.md` and put results in `experiments/` (legacy layout). It says nothing about E##, PLAN.md, the stop list or `verify_candidate.py`. | `.claude/agents/computational-search.md:3,12-14,21`; `ROADMAP.md:90-92`; `STATUS.md:58` | Rewrite the description around exact solvers / pre-registered experiments ("implements and runs a pre-registered ROADMAP experiment: ..."). Rules: work inside `experiments/E##-slug/`, check the stop list, verify every candidate with `verify_candidate.py --target`, report counters by SPEC §4 names. |
| F20 | major | AI layer | Agents use a different evidence vocabulary than SPEC: [P]/[K]/[C]/[N] in `mathematical-researcher` and `combinatorial-topology`; "proved / claimed / computational / conjectured" in `literature-researcher`. The only label SPEC knows for AI-written proofs is PROVED-1, and agents cannot produce PROVED. | `.claude/agents/mathematical-researcher.md:18-19`; `combinatorial-topology.md:18`; `literature-researcher.md:18`; `SPEC.md:73-85` | Replace with "Label every statement with a `SPEC.md` §5 label; an AI-written proof is at most PROVED-1". One line per agent. |
| F21 | minor | AI layer | Stale resource rules: "4 shared cores, at most 2 processes" in 3 agents, vs the 11-worker MacBook and 4-CPU Actions runners. The rule's origin (a shared sandbox) is no longer stated. | `.claude/agents/algebraic-geometry.md:22`; `combinatorial-topology.md:19-20`; `computational-search.md:19-20`; `PROTOCOL.md:65,73` | One line: "inside an interactive session: ≤ 2 heavy processes with timeouts; long runs go to a laptop night or Actions via `run.sh`". |
| F22 | minor | AI layer | Output locations conflict with the layout. `mathematical-researcher` writes long-form results "to files in `research/12-faced-polyhedron/`" (the root, next to the control docs). `algebraic-geometry` / `computational-search` put code in `code/`, while `code/README.md:60-61` says an experiment's own script goes in its folder. `interdisciplinary-scout` has no output home (the backlog is `ideas/`). `literature-researcher` is not told to update the matrix's read-level column. | `mathematical-researcher.md:26`; `algebraic-geometry.md:23`; `code/README.md:60-61`; `literature/README.md:8-10` | theory → `theory/`, experiment code → `experiments/E##/`, leads → one line each in `ideas/`, literature → a row in `literature/README.md`. |
| F23 | major | AI layer | `proof-no-symmetric-immersion/CONTINUE_PROMPT.md` contradicts PROTOCOL in three ways. It says "commit and push as you go" on branch `main`. It calls `adversarial-verifier` an "independent reviewer". It never mentions SPEC/STATUS or that this work *is* ROADMAP E08 (and overlaps E07, the second-encoder comparison). | `proof-no-symmetric-immersion/CONTINUE_PROMPT.md:4,9,28-29,33`; `PROTOCOL.md:47-48,83-85`; `SPEC.md:84-85`; `ROADMAP.md:38-39` | Rewrite as "E08" with branch `experiment/E08-...`, read SPEC/STATUS first, `adversarial-verifier` = filter, human review = separate step, merge via PR after `verify_all`. Or fold it into `experiments/E08-.../PLAN.md` and delete the separate prompt. |
| F24 | major | AI layer / git | `CONTINUE_PROMPT.md` points sessions at `main`, but `main` does not have the restructure yet (`git show main:.../SPEC.md` fails; 3 commits unmerged, no PR). `experiment.yml`'s manual trigger also needs the file on main. | `CONTINUE_PROMPT.md:3-4`; `PROTOCOL.md:71-72` | Merge the branch (owner action), then tag. Until then the prompt must name `claude/research-restructure`. |
| F25 | minor | AI layer | `CONTINUE_PROMPT.md` is fully static: no "state of the last session / in-flight work / open TODOs" block. Real hand-over items currently live only in ROADMAP Phase 0 TODOs and in the owner's untracked `TODO.md`: DRAT publication, tag, merge. | `CONTINUE_PROMPT.md:1-28`; `ROADMAP.md:25-26`; `/Users/a.konyaev/src/my/polyhedrons/TODO.md` | Static rules → CLAUDE.md (F18). CONTINUE_PROMPT keeps a dated "Hand-over" block written by the session-handover skill (S5). |
| F26 | minor | stale refs | `HOW_TO_RUN.md` tells the owner to merge `origin/claude/practical-archimedes-e5p1fi`, a branch that no longer exists on the remote. `results.md:145` and `experiment-log.md:112` cite `experiments/omsat/sym_54_T.drat`, which is gitignored (`*.drat`) and absent. | `overnight/HOW_TO_RUN.md:114-125`; `.gitignore:4-5`; `git branch -a` | Replace the night-5 merge block with "run from `main` or `experiment/E##`". Add "(not kept; regenerate with ...)" after the .drat mention. |
| F27 | minor | tests | `verify_all` skips the verifier's own power tests: `test_mutants.py` (mutated predicates must disagree), `test_v1_v2.py`, `test_v3_fastviol.py`. The external audit asked for "negative mutants" in CI. | `verification/test_mutants.py:1-2`; `verify_all.py:33-58` | Add `test_mutants.py 1` as a 10th check if it runs in seconds. That is the negative control for the verifier itself. |
| F28 | minor | dependencies | `python-sat==1.9.dev17` is a pre-release pin. Python 3.14 is the only tested version. Solver binaries are not pinned (F11). No lock with hashes. | `requirements.txt:6`; `.github/workflows/*.yml:64` | Acceptable for now. Note in requirements that the pin is a dev build, and why. Docker is over-engineering at this stage; a release README with binary versions is enough. |
| F29 | minor | ids / layout | ID schemes coexist without a map: E## (queue), FD#/DR# (ledger), night N (reports, `overnight/results/<job>`), legacy G/Q/R. ROADMAP E08 lives in `proof-no-symmetric-immersion/`, not `experiments/E08-*`. Nights are not experiments. The ledger rows cite DR#, but DRs do not cite which E## tests them (only free text). | `PROTOCOL.md:50-53`; `STATUS.md:51-69`; `ROADMAP.md:30-41` | Add a `DR` column to the ROADMAP table (E02→DR2, E03→DR10, E06→DR9...). Future nights run as `experiments/E##/run.sh`, so "night N" stops being an ID. |
| F30 | minor | log | `experiment-log.md` (append-only chronology) has no entry for the restructure itself, the DRAT regeneration, or the type-0 certificate import. The last entry is the night-4/5 analysis. | `experiment-log.md:628-641`; commits 72ccc52, e7adba8, 85ef222 | Append one dated entry. The handover skill should always do this. |
| F31 | minor | CI / Pages | Pages builds from `main` root, so every research commit on `main` (including `--git --push` night commits) triggers a Pages build. The whole `research/` tree is published on the site. | `gh run list` (pages-build-deployment on main); `overnight/run_overnight.py:122-123` | Fine if intended. Otherwise switch Pages to a GitHub Actions deploy of `index.html` only. Never push night commits straight to `main`. |
| F32 | minor | definition of done | Several stop rules are expected outcomes, not stop conditions. E05 "agrees with sampling on all 232" (what if it disagrees?). E01 "done when a referee-style package exists" (who judges?). No time-box on E04 ("theory + 1 h"), which has no compute stop. | `ROADMAP.md:32,35-36` | Pattern: "stop after <budget> or <condition>; outcome X → next Y". Let `PLAN.md` carry the details. |
| F33 | minor | over-engineering | The Actions experiment runner is untested: no `experiments/E##-*` folder exists yet and no `experiment` workflow run. The PR-per-experiment flow plus long-lived branches is heavy for one owner who already merges branches by hand (`TODO.md`). Five scoring dimensions are fine; the T+D gate is the part that matters. | `.github/workflows/experiment.yml`; `gh run list` (no `experiment` runs) | Pilot the runner on E02 (it really is embarrassingly parallel: 30 maps x 3 radii) before relying on it. Allow docs-only commits straight to main when `verify` is green. |
| F34 | minor | science practice | No route to a human reviewer, although SPEC and PROTOCOL make one a precondition for every theorem-level claim. The only concrete contact is an e-mail draft inside the proof prompt. Natural peers are already in the literature matrix: Pirozhkov (E07), Moki & Julio (FD5 overlap), Bokowski. | `SPEC.md:84-85`; `PROTOCOL.md:47-48`; `proof-no-symmetric-immersion/CONTINUE_PROMPT.md:31-32`; `literature/README.md:18-20` | Add one ROADMAP row (no compute): "request external review of FD5/FD6 + E01 dossier"; owner sends it. Opening a GitHub Discussion or issue in the peer repo with the CNF hashes is the cheapest form. |

### What is already good (keep it)

* `SPEC.md` counters table with an "Allowed in claims" column (`SPEC.md:51-71`) and the solver-outcome rules.
* `STATUS.md` §4 "may / may not be claimed" and verdicts that carry their budget (`DEAD@budget`).
* The `PLAN.md` template: outcomes decided in advance, power statement, amendments section
  (`experiments/_template/PLAN.md`). A git-committed PLAN.md before the run is a real pre-registration,
  because `run.sh` records the commit SHA.
* `verify_all.py` treats a crashing check as a failure (`verify_all.py:71-72`), and it has both positive and
  negative controls.
* `code/README.md` registry covers every module (checked: no unlisted file).
* No broken references to archived files: all hits for `sprint-board`, `METHODS_PROTOCOL`, `next-steps`, ... point
  into `archive/` or are inside historical reviews.

## Proposed skills and prompts

Keep the set small. Every skill below replaces a step that today depends on an agent remembering PROTOCOL.
They go in `.claude/skills/<name>/SKILL.md`.

### Add

**S1 `experiment-start`**
Trigger: "Use when starting work on a ROADMAP item (E##) or when asked to run/launch/pre-register an
experiment for the 12-face research."
1. Read `STATUS.md` §3 and the `ROADMAP.md` row. Refuse if the row's T + D < 3, or if the method is on the
   stop list and STATUS has no written reopening reason. Say which.
2. Create branch `experiment/E##-slug` from up-to-date `main`. Copy `experiments/_template/` to
   `experiments/E##-slug/`.
3. Fill `PLAN.md` from the row and the ROADMAP detail section: hypothesis H1/H0, target S0-S4, SPEC §4
   counter names, positive and negative control, power statement, outcome meanings, stop rule.
4. Edit `run.sh`: bounded command writing into `$OUT`. For a laptop night, call `run_overnight.py ... --out "$OUT"`
   (see `overnight-run-script`). Set `matrix.json`.
5. Pilot: run shard 0 with a minutes-scale budget. The positive control must pass. Record it in PLAN amendments.
6. Commit PLAN.md *before* the full run (the pre-registration). Set the ROADMAP row State = running.
7. Hand the owner the exact launch command (laptop with `caffeinate -dimsu`, or the push with `[run]`).
   Never start a multi-hour run from a session.

**S2 `experiment-conclude`** (also covers night reports; replaces ad-hoc `NIGHT_REPORT_*` writing)
Trigger: "Use when a run of a pre-registered experiment has finished, or when night/Actions results arrive
and must be analysed and recorded."
1. Collect the results: `gh run download <id>` for Actions shards, or the `results/` of the laptop run. Sum
   core-hours from every `manifest.txt`.
2. Check the controls first. If the positive control failed, the verdict is "underpowered", not DEAD.
3. Run every candidate through `verification/verify_candidate.py --target <S#>`. Keep the formula hash for
   every UNSAT used as evidence.
4. Write `CONCLUSION.md` from the template: prediction vs outcome, claims with SPEC §5 labels, non-claims.
5. Update in the same commit: the `STATUS.md` row(s) (verdict + budget), the ROADMAP row (State, plus a new
   row if a follow-up passes the gate), and a 1-3 line `experiment-log.md` entry pointing to CONCLUSION.md.
   Do not restate numbers elsewhere.
6. Run `verify_all.py` (with lint). Open a PR to `main`. Report to the owner in Russian: outcome, what changed
   in STATUS, the proposed next item.

**S3 `candidate-check`**
Trigger: "Use whenever any search, solver or agent reports a candidate, a near-miss, 'zero violations',
'EMBEDDED', or a new witness for the 12-face problem, before anyone calls it a result."
1. Save the candidate as JSON in a supported layout (`verify_candidate.py` docstring). Never re-type numbers.
2. `verify_candidate.py FILE --target S0` (or the stated S-target). Paste the full output.
3. If EMBEDDED for S0: stop all other work. Run an independent re-check by the `adversarial-verifier` agent,
   which re-implements the checks without importing `ladder_exact`, and an exact-rational re-check at a second
   rounding scale (1e-12).
4. Check SPEC §3 degeneracies explicitly: four planes through a point, coincident vertices, zero-length edges.
5. Classify: S0 solution / S1-S4 object / non-embedded. Use the label EXACT only if `verify_all` can reproduce
   it, which means adding the file to `verify_all` CHECKS.
6. Report the verdict with its target label. Never write "found" for anything other than S0 EMBEDDED.

**S4 `ledger-update`** (small; can be a section of S2 if you prefer fewer skills)
Trigger: "Use when editing STATUS.md, ROADMAP.md or SPEC.md."
1. Labels only from SPEC §5. An AI-written proof is PROVED-1. CERTIFIED only with a checked certificate +
   written soundness argument + recorded hashes.
2. Every verdict carries its budget. Reopening a stop-listed direction needs a dated reason in STATUS.
3. New ROADMAP rows: scores, T + D >= 3, budget, stop rule, DR link, State.
4. SPEC changes only via its change log.
5. Run `verification/lint_docs.py` before committing.

**S5 `session-handover`**
Trigger: "Use at the end of a research session, before the owner closes it, or when asked to prepare the
continue prompt."
1. `git status`: list uncommitted work. Commit on the session branch. Never push to `main` directly.
2. Append the dated `experiment-log.md` entry (what was done, commits, outcomes).
3. Rewrite only the "Hand-over" block of `CONTINUE_PROMPT.md`: branch to open, in-flight runs (where, how to
   collect), open owner actions (merge PR X, publish release, send e-mail), next ROADMAP item.
4. Check `STATUS.md` "As of" date and the ROADMAP State column match reality.
5. Run `verify_all.py --quick`.
6. Give the owner, in Russian, the exact commands to run (push, merge, launch).

### Update

**U1 `overnight-run-script`** (`.claude/skills/overnight-run-script/SKILL.md`)
* New step 0: the script runs under `caffeinate -dimsu` on AC power. Lid close = pause, budget-safe because
  of monotonic time. Fix the contradiction with `HOW_TO_RUN.md:115` (F13).
* New step: the night is an experiment. The wrapper lives in `experiments/E##-slug/run.sh`, writes the
  manifest, and calls `run_overnight.py ... --out "$OUT"` (F14). `--git` commits go to the experiment branch,
  never `main`.
* SAT jobs keep proofs and CNFs (F15). Record solver versions in the manifest.
* Refuse stop-listed jobs (F16).
* Reference implementation: `run_night5.sh` instead of `run_night2.sh`, or the E## run.sh once it exists.

**U2 all 7 agents** (`.claude/agents/*.md`): one shared preamble of 5 lines replacing the per-file variants.
"Read SPEC, STATUS, the ROADMAP row you are serving; work inside `experiments/E##-slug/` or `theory/`; SPEC §5
labels only (AI proof ≤ PROVED-1); stop list applies; every candidate through `verify_candidate.py --target`;
no commits." Then role-specific changes:
* `computational-search`: new description (F19). Model sonnet is fine for implementation.
* `adversarial-verifier`: add "check against SPEC §1 S0 *including single adjacency* and §3 degeneracies; for
  E01, write the second verifier without importing `code/ladder_exact.py`". This agent is the natural executor
  of E01 step 1.
* `literature-researcher`: "update the read level in `literature/README.md`".
* `interdisciplinary-scout`: "write each lead as one line in `ideas/` with a proposed T D F G R score".
  Otherwise its leads never reach the queue.
* `mathematical-researcher`: output to `theory/`; labels per SPEC.

**U3 `CONTINUE_PROMPT.md`**: move the static rules to CLAUDE.md (F18). Keep the title, the branch and a dated
"Hand-over" block (S5).

**U4 `proof-no-symmetric-immersion/CONTINUE_PROMPT.md`**: rewrite as the E08 brief (F23), or delete it once
`experiments/E08-*/PLAN.md` exists.

**Add (not a skill) — root `CLAUDE.md`**, ≤ 30 lines. Repo = public site (`index.html`, GitHub Pages from `main`)
+ research. For research work read `research/12-faced-polyhedron/STATUS.md` → `ROADMAP.md` → `PROTOCOL.md` →
`SPEC.md`. The hard rules: no weakening of the target, no fabricated results, SPEC labels, stop list, verify
with `~/.venvs/polyhedra/bin/python verification/verify_all.py --quick`, ask before large subagent tasks and
before long runs, Russian to the owner and English in files. Skill names S1-S5.

### Remove / merge

* Nothing needs deleting outright. `interdisciplinary-scout` and `literature-researcher` overlap in practice
  (both web-search and write leads). Keep both only if the scout's output path (`ideas/`, scored) is added.
  Otherwise drop the scout: the backlog in `ideas/` is already larger than the queue can absorb.
* Merge S4 into S2 if you want four skills instead of five.
* `overnight/run_night*.sh`: archive them (F16). They are history and the main way to rerun stop-listed work
  by accident.

## Prioritised actions

| # | Action | Fixes | Size |
|---|---|---|---|
| 1 | Publish the two DRAT tarballs + `SHA256SUMS` as a GitHub release; back up `overnight/work/` off-laptop; record URL + SHA in STATUS FD5/FD6 | F10 | S |
| 2 | `verify_candidate.py --target S0` (12 faces, single adjacencies, V/E/chi), plus Roest-Vigh as a negative control in `verify_all`; fix the solid path | F01, F02 | S |
| 3 | Relabel FD1/FD2/FD8 → PROVED-1, FD6 → EXACT until E08; soften the README "Certified ... immersion" sentence | F04 | S |
| 4 | Merge `claude/research-restructure` into `main` via PR, tag `state-2026-11-01`, add `LICENSE` + `CITATION.cff` + the upstream MIT notice for vendored code; then the Zenodo DOI | F12, F24 | S |
| 5 | Root `CLAUDE.md`; slim `CONTINUE_PROMPT.md` to a hand-over block | F18, F25 | S |
| 6 | ROADMAP: State/Folder/DR columns, explicit ordering reason, move E05/E10 below the gate or re-score them | F06, F07, F29 | S |
| 7 | One sleep rule (caffeinate + monotonic) in PROTOCOL, HOW_TO_RUN, the skill and the scripts; flip `--keep-proofs` default | F13, F15 | S |
| 8 | Agent preamble + `computational-search` description rewrite + label vocabulary | F19-F22 | S |
| 9 | `verification/lint_docs.py` in `verify_all` (labels, gate, paths, E## folder ↔ ROADMAP row); workflow id regex `^E[0-9]{2}-` | F16, F17 | M |
| 10 | `verify_all` witness checks assert genus / pair count; add `test_mutants.py`; add re-encode-and-hash check for 2-3 symmetric CNFs | F03, F11, F27 | M |
| 11 | Skills S1 `experiment-start`, S2 `experiment-conclude`, S3 `candidate-check`, S5 `session-handover` (S4 inside S2) | AI layer | M |
| 12 | Single source of truth: freeze `results.md`; STATUS owns numbers; READMEs link instead of restating; PROTOCOL §2.7 write list = CONCLUSION + STATUS + ROADMAP + 1-line log | F05, F09 | M |
| 13 | Bridge `run.sh` ↔ `run_overnight.py` (`--out`), update `overnight-run-script`; archive `run_night*.sh`; fix stale HOW_TO_RUN branch block | F14, F16, F26 | M |
| 14 | Pilot the Actions runner on E02 (small matrix) before trusting it; decide on Pages scope | F31, F33 | M |
| 15 | ROADMAP row for external human review (FD5/FD6 and the E01 dossier) to Pirozhkov / Moki & Julio / Bokowski; rewrite the proof prompt as E08 | F23, F34 | S (writing) / L (waiting) |

Not checked: the mathematics itself (lemmas, encoder soundness), `index.html`, the content of `theory/`,
`ideas/` and most of `reviews/`. Runtime of the full (non-quick) `verify_all` locally (CI total 1 m 16 s).
Whether `test_mutants.py` runs in seconds. Whether Zenodo/GitHub limits allow the 438 MB asset under the
owner's account settings.
