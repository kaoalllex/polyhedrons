---
id: E-261101-01
title: Regenerate and publish the symmetric DRAT certificates
date: 2026-11-01
status: done
direction: [DR8]
origin: [E-261029-13, E-261029-15]
tests: []
produces: [C:symmetric_drat]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

The night runs had deleted their proofs after checking; make them public.

## Method

`run_overnight.py sym [--sym-immersion] --keep-proofs --keep-cnf`; compare hashes with the recorded ones; drat-trim.

## Results

All 50 CNFs and proofs bit-identical to the recorded SHA-256; 50/50 VERIFIED again; published in the GitHub release `state-2026-11-01` (`verification/certificates/symmetric_drat/`).

## Conclusions

EXACT: the certificates of FD5 and FD6 are public and reproducible.

## Next

Zenodo DOI before a write-up.
