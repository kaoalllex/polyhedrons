# E-261116-01 run summary

INCOMPLETE

NUMERICAL; sampled formula scope, no geometric negative.

```json
{
  "statuses": {},
  "completed": 0,
  "expected": 10,
  "remaining": [
    30,
    247,
    1186,
    1342,
    1366,
    3263,
    3277,
    3565,
    3725,
    3972
  ],
  "evidence": "NUMERICAL",
  "scope": "Sampled normalised S5 (11,5) formulas only; no proofs or geometric negative",
  "verdict": "INCOMPLETE",
  "element_curve": {
    "points": {
      "9": {
        "sampled": 2,
        "median_solver_seconds": 0.2907449584999995,
        "selection": "all admissible (8,2) negative controls"
      },
      "10": {
        "sampled": 203,
        "median_solver_seconds": 2.761988999998721,
        "selection": "all admissible (9,3) negative controls"
      },
      "11": {
        "sampled": 757,
        "median_solver_seconds": 54.764740541009814,
        "selection": "normalised (10,4) A+B; four prep units plus owner remainder"
      }
    },
    "inputs_sha256": {
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/0/results.json": "da7108eac4d04ceddfb4dc8351de79ad560fc1f388ae13e268406eb72fef1095",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/1/results.json": "004cf95738d0107bb2e51c9300e0862768968dcc72c54ac24a8679a744d6bf54",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/2/results.json": "0124055b6ddde131e909acec4b700a42446e4f4d4d8008c75e70f78fc623718f",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/3/results.json": "f4cd640e5e17b1b0c25f1371bbbee0fae71916654ba4c1e07751c3ad4de2c27c",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/4/results.json": "92e7e436c5e28d94f4606b44fbd617ebb1809e0c2d55e50985e42972f9ab057b",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/5/results.json": "c4272f4561e26886670da54e173412c2a3d4da450623539533b70cf76d6cee04",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/6/results.json": "0f7c51e8341fbddff3aa9788942973a267f18e67aec7b8b76398f47b711d7d6a",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/7/results.json": "042a43a0bd9d9e0c7d3c33f7634128d088cdc498165f4b7c1908827fca3aaadd",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/8/results.json": "3171acff316a26751ed5c326c8d5b36eac34997bffea6469ad11326feece4c42",
      "experiments/E-261114-01-normalised-s6-10-3/results/negative/9/results.json": "45568986bba7b2e2e5b1e69896fe8d7ecb0bc8a56ce25395da970a3f7e3c2b0a",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/prep/summary.json": "73b72e0eb7208cef6f29e21ace413cc05af2dc8c98b030c4e44e116f47eb0e1f",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/0/results.jsonl": "e2b75a6c3dfaa25719f2fffff2474864623cb7d32bfcaad4cc682d1fa5e0e38f",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/1/results.jsonl": "6c923e0fc65a7ad74c29a13013ffe4918d8356387cc0665897d574aba2a2fe0e",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/2/results.jsonl": "8e9e0316a08ef66827aee2b5c64772c86c853b9fe7c3acb10c18035985745641",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/3/results.jsonl": "2599ede0944e36ceafdff02050f57665448a8b2029dd2994f01b8ed2b2b5d56c",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/4/results.jsonl": "60463c8c9f6686ab1b34f4e2ed7dd5cdf13f4378ff2551f3f884d1416eb1275f",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/5/results.jsonl": "6a4f35b5c71e57a8fb9265ca09c57889bca728a9c78250987d4816667eaa392a",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/6/results.jsonl": "68641e7c550becef24bca38757feafa3602bbcc19d41d6a781c2d8be3ca44370",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/7/results.jsonl": "32883b4f9ae97ac46eea4a0818ae725c74e29abbb3ecff08f94d505157d13dda",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/8/results.jsonl": "e8398fdd5f4568336ca7db8e16a26f244b37363f03b3d6ade3a51585c2839f80",
      "experiments/E-261110-06-s5-10-4-strata-ab-remainder/results/run/9/results.jsonl": "4f56eec10da84095cdfff8a1690a1113a830868bcb6d328ffa3577fc504e1c7a"
    },
    "limitation": "Known-negative lower rungs; kissat, normalised, unequal map populations; extrapolation is not a bound"
  },
  "worker_wall_hours": 0.0,
  "cpu_core_hours": 0.0,
  "max_endpoint_clock_gap": null,
  "queue_sha256": "a77c3b6c7515fa991777545f211dd4de4d84436946027de29ffeeea97b831fb4"
}
```
