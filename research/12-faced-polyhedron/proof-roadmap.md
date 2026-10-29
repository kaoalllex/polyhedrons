# Roadmap: proving that no 12-face Series-1 polyhedron exists

Honest status: not proved; the evidence (no symmetric realizations, all near-misses in the wrong
topological class, symmetric obstruction already local) points towards nonexistence, but a
realization may still exist. Both directions stay open.

## Structure of a proof

1. **Reduction (rigorous, mostly written).** Any realization gives, WLOG in general position, one of
   the 59 combinatorial types and a uniform rank-4 chirotope on 12 planes + plane at infinity that
   satisfies the Grassmann–Pluecker relations and the embedding predicates (mathematical-model.md
   §2-§5, Lemma 5.1). To do: a complete written proof of Lemma 5.1 and of the in-face predicate,
   reviewed adversarially (the review was interrupted).
2. **Symmetric case: done.** 25 cases (all half-turn and 3-fold classes), our own encoder, DRAT
   proofs checked by drat-trim (user's machine). Independent of the prior third-party result.
3. **Asymmetric case: the real work.** 59 types, each a SAT instance with 715 free signs.
   * Brute force: cube-and-conquer, roughly 300 core-hours per type by the prior estimate
     (~19,000 core-hours total), with DRAT/LRAT proofs. Feasible on a cluster or a few months of
     one multi-core machine.
   * Smarter (our lead): the obstruction may be LOCAL. Symmetric instances are already UNSAT with
     only "faces are simple polygons" + "at most one reflex corner per vertex" (immersion), and for
     D3 with simplicity alone. If the asymmetric immersion instances are UNSAT and cheaper, the
     proof needs no global non-intersection clauses at all ("no polyhedral immersion exists").
4. **Certification.** Two independently written encoders of the same clause families,
   cross-validated against exact geometry (done for random instances); every clause family with a
   written soundness proof; checked DRAT/LRAT certificates; an adversarial reviewer.

## Directions, in order of expected value

1. **Immersion instances** (overnight `immersion`): decide them for as many types as possible;
   compare their cost with the full embedding instances.
2. **Minimal unsatisfiable cores** of the local symmetric instances (D3: simplicity alone). Which
   faces and which polygon properties conflict? A small core suggests a human-readable lemma.
3. **Per-face decomposition.** The simplicity of face X depends only on the rank-3 contraction at X
   (11 lines + line at infinity in plane X). Enumerate the possible local types of a face up to
   symmetry and glue them through shared contractions: a CSP with far fewer variables.
4. **Counting / topological invariants.** Proved so far: Gauss degree -5, >= 13 saddle vertices,
   <= 1 reflex corner per vertex, <= 8 reflex corners per face. Observed: local-violation counts
   are always even (a parity invariant in the spirit of Banchoff's triple-point theorem?). A
   contradiction between such counts would give a human proof.
5. **Cube-and-conquer with proofs** on the cheapest formulation that turns out UNSAT.
