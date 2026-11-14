---
id: I-261114-04
title: Handle-neighbourhood SAT - solve a (10, 3) formula from the chirotope of a realized (10, 2) parent
date: 2026-11-14
status: open
direction: [DR19, DR13, DR17]
origin: [E-261101-25, E-261113-02, owner]
---

## Idea

For a (10, 3) map, list the (10, 2) maps left by removing one handle, realize them (SAT in seconds, E-261113-02),
and solve the (10, 3) formula with solver phases or assumptions taken from a parent's chirotope. It is the one
testable form of "transitions between realization spaces" in the owner's notes of 2026-11-13.

## Why / cheapest test

What differs from E-261101-25 (chirotope-first at 12 faces): 11 elements and SAT calls of seconds. Rung with known
answers first: genus-2 parents of genus-3 archive realizations. Only if (10, 3) keeps TIMEOUT units after
E-261114-01 and E-261114-03. Untested proposal.

Source: `reviews/strategy-review-2026-11-14.md` §6 (N4).
