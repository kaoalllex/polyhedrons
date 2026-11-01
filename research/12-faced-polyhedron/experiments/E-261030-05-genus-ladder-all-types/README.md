---
id: E-261030-05
title: Genus ladder over all 59 types
date: 2026-10-30
status: done
direction: [DR1]
origin: [E-261030-03, I-261030-22]
tests: [H-261030-04]
produces: []
verdict: LOW-YIELD@night 3
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Highest exactly realized genus per type (2 chains each).

## Method

Laptop night 3, job `glad` (genus ladder with branching for up to 30 min from the highest level).

## Results

118 tasks: genus 3 for types 39 and 53, genus 2 in 37 chains, genus 1 in 74; types 52 and 56 cannot be reduced to the sphere. Records: `results/glad/results.jsonl` (`overnight/analyze_glad.py`).

## Conclusions

EXACT realizations (they seed the archive); no genus 4.

## Next

Gauss gate on the results (E-261030-06), archive climb (E-261030-10).
