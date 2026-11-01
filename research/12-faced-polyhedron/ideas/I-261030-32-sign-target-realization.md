---
id: I-261030-32
title: Realize a SAT chirotope by maximizing the minimum margin of its signs
date: 2026-10-30
status: open
direction: [DR8]
origin: []
---

## Idea

Given target signs from a SAT model, maximize the smallest signed 4x4 determinant margin over the 36 plane parameters; on failure, try a biquadratic final polynomial and block it (CEGAR).

## Why it might help

A smooth, well-conditioned problem instead of a count.

## Cheapest test

Needs a SAT model.

## Source

review 2026-10-30 direction 9; internal audit 2026-10-31 E6.
