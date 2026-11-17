# Session checks of dialogue 2026-11-16-strategy

Copied on 2026-11-17 from the dialogue thread (`dialogue/threads/`, not in git) so that review §6 can be reproduced.
They are session checks, not ledger evidence (`SPEC.md` §5): no manifest, no shards, no independent rerun. The only
change from the thread copies is the repository root in the two `claude` scripts (`parents[5]` -> `parents[2]`); the
JSON files are the original outputs.

| File | Author | What | SHA-256 |
|---|---|---|---|
| `d2_rate.py` | claude | K13: hit rate of the D2 2 x 4 family at eight planes (`d2_rate.py 240 d2_rate.json`) | `ed607de897b91cbc5b209e7a162d4e20362c6f4f1567a5418259bf86841cbf92` |
| `d2_rate.json` | claude | K13 output: 17 SOLID, 223 INFEASIBLE | `b7b5ff8438acf7ea1e7526c936604abd3407013f67ebb1cab6b797e0f7f8aafa` |
| `c3_nine.py` | claude | K14: cost per unit of C3 3+3+3 at nine planes (`c3_nine.py 80 45 20 c3_nine_e45.json`) | `0d155e9dc59aeacaff2ef7c0f302be690fab28165059cac37868b70cce4e0eef` |
| `c3_nine_e45.json` | claude | K14 output: 70 INFEASIBLE, 10 UNKNOWN at 20 s | `e6b89f2bb8d6d01709f2e23aeb636119209d5105f5b4cbce06e68fa0b889c6ff` |
| `check_c3_orbits.py` | astra | orbits of (012)(345)(678) on k-subsets of ten elements (writes the JSON beside itself) | `593128c224eff5fa4b95326c77d6397af6ed63dc777812a315f7c0cae751af98` |
| `check_c3_orbits.json` | astra | its output: 72 orbits on the 210 four-subsets, three fixed | `3eb53cdcc24e85b159b28d13a04d5183134d9e2ed9a8c4e7b6370b053cf6d6f2` |

Run from the repository with the research environment activated, e.g.
`python3 research/12-faced-polyhedron/reviews/dialogue-2026-11-16-strategy-checks/d2_rate.py 240 /tmp/d2_rate.json`
(eight worker processes).
