---
id: I-261030-16
title: Bandit scheduler (successive halving / UCB) over realization-handle arms
date: 2026-10-30
status: tried
direction: [DR1]
origin: [owner]
---

## Idea
Allocate a fixed CPU budget over discrete arms with successive halving or UCB instead of a GP.

## Why it might help
The start energy is a good prior (17 -> 4, 27 -> 7).

## Cheapest test
Successive halving over (realization, handle) arms.

## Source
ideas/search-algorithms.md Evaluation #3; STATUS DR1 (11 arms nights 4-5)
