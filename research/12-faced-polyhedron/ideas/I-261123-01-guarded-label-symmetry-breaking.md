---
id: I-261123-01
title: Guarded face-label symmetry breaking for the census-free formula - faces by size, lex order under equal-size adjacent swaps
date: 2026-11-23
status: open
direction: [DR19]
origin: [E-261116-07, E-261119-01]
---

## Idea

The census-free formula P3 (`experiments/E-261116-07-census-free-s1-ladder/p3.py`) fixes plane orientations (sign
gauge, mirror fix) but no face labels, so each labelled solution has up to F! copies (8! at eight faces, 9! at nine)
that a CDCL or CP-SAT search refutes one by one. Break the relabelling symmetry statically, as in graph generation by
SAT (Codish, Miller, Prosser, Stuckey, IJCAI 2013; SAT Modulo Symmetries, Kirchweger-Szeider 2021): faces ordered by
size, and the upper-triangle word of the pair-multiplicity matrix lex-<= its image under each adjacent swap of two
faces **of equal size**. The minimum word over the size-sorted labellings satisfies every guarded comparison, so the
constraints keep a representative of every map orbit (PROVED-1, cross-review 2026-11-23 check B). After relabelling,
the sign gauge and the mirror fix are reapplied before a cube is assigned.

The unguarded version (comparisons also across faces of different size) is unsound: stage-A record 51 of
E-261117-04 (`3a9473fb...`, face sizes (10, 9, 10, 9, 9, 9, 8, 8)) has 0 of 96 size-sorted labellings surviving it,
4 surviving the guarded one (draft review 2026-11-23 proposed the unguarded form; the cross-review found the flaw,
re-checked in the final review).

## Why it might help

P3 v2 and P3-sym never refuted a known negative: 48 of 48 cubes UNKNOWN at 225-560 s (STATUS 3aw); free C2 at
(8, 30) UNKNOWN at 1 h (3bd). If the label symmetry is the bottleneck, a census-free formula could reach the
non-equivelar genus-4 nine-face maps that no census can (order 10^7 classes; lead review 2026-11-23). Untested proposal.

## Cheapest test

E-261123-02: the known negatives (8, 30) and (9, 39), 16 one-worker cubes each at 225 / 450 s (<= 3.0 core-h), against
E-261116-07's UNKNOWN baseline. Kill: any UNKNOWN at either rung. Blocking one chirotope does not block a map
(`p3.py` `block`), so a discovery or "nothing else" test at (8, 36) needs a whole-map-class blocker with controls.

Source: `reviews/strategy-review-2026-11-23.md` §5 N1, `-codex.md` checks B, C, `-final.md` points 3-5 (owner-approved 2026-11-23).
