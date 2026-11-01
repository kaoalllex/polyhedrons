---
id: E-261030-10
title: Realization archive with a bandit over handles
date: 2026-10-30
status: done
direction: [DR1]
origin: [I-261029-36, I-261030-16, E-261030-05, E-261030-06]
tests: [H-261030-04]
produces: []
verdict: LOW-YIELD@nights 4-5
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Climb from every exact realization (genus >= 2) along gated next handles; collect diverse realizations.

## Method

Laptop nights 4-5, job `arch` (`code/archive_climb.py`, UCB over arms, 25 % diversity tasks, Gauss gate).

## Results

818 tasks, 203 new exact realizations; archive of 247 (153 genus 2, 94 genus 3 of types 15, 53, 0, 39), all re-verified; 11 genus-4 arms, best 4 events, no genus 4. Records and archive: `results/arch/` (the archive is checked by `verify_all`). Night 4 lost about 8 h to laptop sleep.

## Conclusions

EXACT dataset of realizations; no genus 4 at this budget.

## Next

Chirotope chambers of the archive (planned E-261101-14).
