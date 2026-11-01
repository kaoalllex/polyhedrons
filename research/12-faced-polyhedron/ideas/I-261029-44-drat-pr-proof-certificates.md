---
id: I-261029-44
title: DRAT / PR proof certificates for OM-SAT UNSAT
date: 2026-10-29
status: tried
direction: [DR8]
origin: []
---

## Idea
Export UNSAT runs to DRAT (drat-trim) and test PR/LPR proofs (cake_lpr) so that UNSAT is certified.

## Why it might help
An UNSAT without certificate is only a claim.

## Cheapest test
Export the F = 7 control run to DRAT, check proof size.

## Source
literature/scout-leads.md lead 4; archive/open-questions.md #4; STATUS FD5 (25/25 UNSAT-VERIFIED with drat-trim)
