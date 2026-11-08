---
id: E-261108-01
title: Arrangement-source sweep for solid-first - 300 nine-plane arrangements from Roest-Vigh, Mizhaev and C2 sources
date: 2026-11-08
status: running
direction: [DR7, DR18, DR19]
origin: [E-261107-01, E-261103-05, I-261103-04]
tests: [H-261103-02, H-261101-07]
produces: []
preregistered: true
---

> Week plan item 4 (`ROADMAP.md`). Explore run of the E-261107-01 engine, unchanged, on 300 arrangements.

## Goal

100 Roest-Vigh planes + a random ninth plane, 100 Mizhaev + a random ninth, 100 random C2-invariant arrangements;
hard decision for a 36-pair embedded solid, cap 60 s, <= 2 core-h, 10 shards. See `PLAN.md`.

## Next

Owner launch (`overnight/launch.sh 261108-01 start|status|stop`), then `experiment-conclude`.
