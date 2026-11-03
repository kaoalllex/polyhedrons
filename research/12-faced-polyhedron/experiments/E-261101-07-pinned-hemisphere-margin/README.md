---
id: E-261101-07
title: Why does every class-reaching drift end at margin 0?
date: 2026-11-01
status: done
direction: [DR3]
origin: [I-261101-03, E-261030-11]
tests: [H-261101-03]
produces: []
verdict: ARTEFACT (measuring function floors at 0; see CONCLUSION.md)
preregistered: false
---

> Done 2026-11-01 without compute: the margin is an artefact of `gauss_gate.hemisphere_margin`, which returns 0 for
> every set not in an open hemisphere; and k_tau != 0 forces that anyway. Details: `CONCLUSION.md`. The real question
> (can in-class normals be reached inside the realization space?) is E-261101-19.

## Goal

A lemma about handle normals of an embedded polyhedron, or an artefact of the drift rule.

## Next

Stop rule: proof, counterexample, or a written reason it is an artefact

## Starting point (moved from ROADMAP.md)

153/153 drifts reached the next class with margin exactly 0. Either a theorem (handle normals of an embedded
polyhedron cannot leave a closed hemisphere in that configuration) or an artefact of the drift's acceptance
rule. First read `kdrift.py`'s acceptance rule and margin definition; then try to prove; then a 1-hour test that
forces the margin positive. Outcome either way is a short note in `theory/theory-notes.md`.
