---
id: I-261114-02
title: Bridge recovery control - does the SAT-to-coordinates bridge recover chirotopes that are known to be realizable
date: 2026-11-14
status: open
direction: [DR19]
origin: [E-261113-02, I-261029-57]
---

## Idea

The frozen bridge realized 16 of 153 (10, 2) models (E-261113-02). Two readings: most SAT models are not realizable,
or the bridge misses realizable ones. Feed the bridge the exact chirotopes of the 16 realized objects (recovery),
and 30 solver seeds on five maps it never realized (models per map).

## Why / cheapest test

The reading decides how a SAT at (10, 3) or (10, 4) is judged: recovery >= 0.8 means many models per SAT are the
remedy; recovery <= 0.3 means the realizer needs a session before any target SAT is called unrealized. Cheapest
test: E-261114-02, under 1 core-h. Untested proposal.

Source: `reviews/strategy-review-2026-11-14.md` §2 item 3; approved by the owner on 2026-11-14.
