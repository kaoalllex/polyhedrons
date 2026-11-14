# Normalisation soundness (PROVED-1, unreviewed)

Scope: uniform realizable chirotopes with INF fixed, for the geometric completeness of the normalised
ALL_OPTS formula; not a claim that every abstract OM has a realization. Reorienting one face plane changes
neither its geometric plane nor the vertices and polygons specified by the links. Reflecting space also
preserves incidence, intersections, reflex corners and polygon simplicity. Thus the geometric predicates
encoded by SEGMENT_DISJOINT, TRIPLE, INCONS, RFCONS and REFLEX1 are unchanged; the orientation bit
RTURN xor REFLEX changes by the same bit at every corner of a given face, preserving POC. GP is preserved
algebraically: in each three-term relation every reoriented element occurs with the same parity in each
term, and global sign reversal occurs twice per term. For attainability, write plane signs as bits x_i:
the four normalisation triples on {0,1,2,3} have coefficient matrix J-I over F2, invertible since
(J-I)^2=I in dimension four. They uniquely fix x_0,...,x_3; each remaining (0,1,k,INF) fixes x_k.
If chi(0,1,2,3) is then negative, reflect space and reverse every face plane. Reflection flips every
4-bracket, while reversal of all face planes flips the brackets containing INF (three face factors)
and preserves those without INF (four factors). The normalisation triples remain positive and the
mirror bracket becomes positive. Therefore no uniform geometric witness is lost by the added units,
conditional on the existing predicate soundness arguments. The random exact tests in invariance.py
check each emitted constraint (equivalence pairs grouped) on realizable chirotopes; they do not prove
invariance for arbitrary nonrealizable OMs. No new geometric exclusion follows without proof checking.
