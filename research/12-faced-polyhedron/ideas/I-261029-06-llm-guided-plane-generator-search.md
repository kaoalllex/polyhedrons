---
id: I-261029-06
title: LLM-guided search for plane-set generators (FunSearch style)
date: 2026-10-29
status: open
origin: [owner]
---

## Idea
Agents write programs that generate plane sets, scored by Gauss filter, period defect and violations (FunSearch / AlphaEvolve). Later small-budget variant: evolve the search code itself, with the exact verifier as the only judge.

## Why it might help
Search for generators, not objects; a benchmark exists (ladder n = 7, genus 3 -> 4); reward hacking happened three times, so only the exact verifier may judge.

## Cheapest test
20 generators x 1 min.

## Source
ideas/cross-field-ideas.md X6; ideas/search-algorithms.md item 11 and 'Evaluation' #4 (medium-low, later, small budget)
