---
id: I-261030-15
title: Two-level evolution: discrete handle lattice plus continuous optimizer
date: 2026-10-30
status: tried
direction: [DR1]
origin: [owner]
---

## Idea
Population of (type, sub-map, realization) with mutations add/remove/swap a handle; continuous layer annealing or CMA-ES.

## Why it might help
It is what works now: discrete choices moved genus 4 from 8 to 2 violations in two hours.

## Cheapest test
Proof of concept on type 0 at equal 4 core-hours: fixed chain vs branching ladder vs branching + archive + halving.

## Source
ideas/search-algorithms.md Evaluation #2; STATUS DR1
