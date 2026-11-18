"""Eight small exact orbit-count shards for the R2 dialogue check."""
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
import json
from pathlib import Path
import time


def count_orbits(size):
    permutation = (1, 2, 0, 4, 5, 3, 7, 8, 6, 9)
    subsets = set(combinations(range(10), size))
    representatives = set()
    fixed = 0
    for subset in subsets:
        moved = tuple(sorted(permutation[i] for i in subset))
        moved_twice = tuple(sorted(permutation[i] for i in moved))
        representatives.add(min(subset, moved, moved_twice))
        fixed += moved == subset
    assert 3 * len(representatives) == len(subsets) + 2 * fixed
    return dict(size=size, subsets=len(subsets), fixed=fixed,
                orbits=len(representatives))


if __name__ == "__main__":
    started = time.monotonic()
    with ProcessPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(count_orbits, range(1, 9)))
    assert rows[3] == dict(size=4, subsets=210, fixed=3, orbits=72)
    output = dict(label="EXACT session arithmetic, outside verify_all",
                  workers=8, rows=rows,
                  wall_seconds=time.monotonic() - started)
    Path(__file__).with_suffix(".json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output))
