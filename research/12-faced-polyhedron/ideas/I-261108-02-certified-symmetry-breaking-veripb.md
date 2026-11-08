---
id: I-261108-02
title: Certified symmetry breaking - lex-leader clauses with VeriPB proofs for the (9, 3) maps with a map automorphism
date: 2026-11-08
status: open
direction: [DR19, DR8]
origin: [I-261029-43, E-261103-03]
---

## Idea

21 unresolved (9, 3) maps have Aut+ >= 2, and their plain formulas inherit that symmetry. Lex-leader clauses (BreakID)
could shorten the refutations. Plain DRAT cannot certify such clauses. VeriPB proof logging can (Bogaerts, Gocht,
McCreesh, Nordström 2022, "Certified symmetry and dominance breaking").

## Why it might help

It keeps the certificate chain of SPEC §4 while removing the symmetric redundancy that makes CDCL refutations long.
Untested.

## Cheapest test

Two Aut+ = 2 unresolved maps with BreakID clauses, timed against the plain formula (about 0.5 core-h). Certify with VeriPB
only after a >= 3x speed-up.

## Source

Strategy review 2026-11-08, §7.4.
