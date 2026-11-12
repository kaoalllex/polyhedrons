---
id: I-261108-07
title: GitHub Actions calibration wave - decide known (9, 3) maps on runners to measure their speed and proof handling
date: 2026-11-08
status: parked  # owner 2026-11-10: out of the near-term plan
direction: [DR19]
origin: [owner, E-261103-07]
---

## Idea

The repository is public, so standard GitHub Actions runners are free (CLAIMED, GitHub's terms), up to 20 parallel jobs
of at most 6 h on the free plan (CLAIMED). Run about 20 jobs on (9, 3) maps with known UNSAT (for example map 7, 1239 s
on the laptop) through the existing `experiment.yml`, with proofs checked inside the job.

## Why it might help

A (10, 4) campaign of hundreds of core-h is out of laptop reach but may fit a few Actions waves. The workflow has never
run an experiment (its runs so far were skipped). The owner approved a trial on 2026-11-08. Untested.

## Cheapest test

One wave of 20 jobs: laptop/runner time ratio per map, proof size against the runner's disk, artefact upload of hashes
and transcripts. Needs a pushed branch or a workflow on `main`.

## Source

Lead review 2026-11-08d, §6 idea N4 and audit A9; queue item 6, conditional on the speed-up benchmark.
