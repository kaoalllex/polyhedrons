---
id: I-261101-19
title: Farkas-certificate descent - the exact gradient of offset infeasibility with respect to the normals
date: 2026-11-01
status: open
direction: [DR2, DR4, DR17]
origin: [FD8, FD9, I-261029-03, E-261030-11]
---

## Idea

At fixed normals the offset problem is a linear feasibility system A(n) d > 0 over the cells of a hyperplane
arrangement (FD8). When it is infeasible, the LP returns a Farkas certificate y >= 0 with y^T A(n) = 0. The
constraint matrix depends smoothly on the normals, so y^T (dA/dn) is the **exact gradient of the infeasibility
measure with respect to the normals**: moving the normals against it is the steepest way to make the system less
infeasible (sensitivity analysis of infeasible LPs; the same object as the period functional of FD9 and the
"Farkas certificate mining" of the fresh-eyes review, used here as an engine, not as a diagnostic). Loop: Gauss-gate
check (FD7) -> LP on offsets (one sign cell at a time, or the MaxSAT relaxation for the cell choice) -> if UNSAT, the
certificate's gradient step on the normals -> repeat; every SAT is checked exactly (`verify_candidate.py`).

## Why it might help

Every engine so far moved the normals by annealing or by random radii and asked an exact oracle afterwards
(12,202 UNSATs with no direction information). The certificate tells which constraints conflict and how the normals
must move to resolve them; that is the difference between a blind and a guided search in the 16 normal dimensions.
"What is different" (parked-method rule for DR2/DR4): the move is the exact dual gradient, not a random or annealed
step.

## Cheapest test

The 80 radius-0 in-class seeds of nights 4-5 (`E-261030-11/results/n5/class_seeds/`): run 50 certificate steps
from each; does the infeasibility measure decrease monotonically, and does any seed reach SAT at the sphere level
(target S3, genus 0 of the chain) or at its own level? Positive control: a genus-3 realization's normals perturbed
by 0.1 (UNSAT by the nights-4/5 control) must come back to SAT in a few steps.

## Source

Strategy review follow-up 2026-11-01; `reviews/fresh-eyes-review.md` section 3 idea 4 (the certificate as data).
