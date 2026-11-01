---
id: E-261029-02
title: Benchmark of published numerical near-misses
date: 2026-10-29
status: done
direction: [DR5]
origin: [L:hackerpoet, L:mokijulio2026]
tests: []
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

How close the best known numerical attempts are, measured with one counter.

## Method

`code/import_hackerpoet.py` converts 1797 `.obj` near-misses to planes; `code/fastviol.py` counts violated forbidden triples (float).

## Results

Best count 4 on symmetric maps, 5 on maps with trivial automorphism group (topologies 33, 36). The counter agrees with the source's own count on 1049/1797 files (float32 rounding explains the rest). Seeds: `overnight/data/seeds.json` (input data of later jobs).

## Conclusions

NUMERICAL benchmark only; the counter is a float diagnostic (SPEC counters).

## Next

The Gauss prefilter (E-261029-08) shows these near-misses are topologically far from solutions.
