---
id: E-261101-02
title: Check the type-0 handle-completion certificate
date: 2026-11-01
status: done
direction: [DR1]
origin: [E-261030-03, owner]
tests: [H-261101-05]
produces: [C:type0_handle_completion]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Confirm that the type-0 genus-3 map extends to the target map by three explicit handles.

## Method

Standard-library verifier `verification/certificates/type0_handle_completion/verify.py`.

## Results

PASS: three handles (1,2,10)-(4,7,9), (0,5,8)-(2,6,7), (0,9,11)-(3,5,10); the final map equals catalogue type 0.

## Conclusions

EXACT, combinatorial only: no genus-4-6 geometry is claimed.

## Next

Dossier (planned E-261101-03).
