"""Independent C3 census by triangle-orbit exact cover and equivariant edge gluing."""
import argparse
from collections import Counter
import importlib.util
import itertools
import json
import platform
import subprocess
import sys
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("census", HERE / "census.py")
census = importlib.util.module_from_spec(spec)
spec.loader.exec_module(census)


def rho(v):
    return 3 * (v // 3) + (v + 1) % 3


def cyclic(t):
    return min(t, t[1:] + t[:1], t[2:] + t[:2])


def orbit(t, normalise):
    out = set()
    for _ in range(3):
        out.add(normalise(t))
        t = tuple(map(rho, t))
    return tuple(sorted(out))


def triangle_orbits():
    orbits = {orbit(t, cyclic) for t in itertools.permutations(range(9), 3)}
    return sorted(o for o in orbits if len(o) == 1), sorted(o for o in orbits if len(o) == 3)


def gluings(triangles):
    """Every parallel-edge pairing; keep only those commuting with the fixed C3 action."""
    tri = [list(range(3 * i, 3 * i + 3)) for i in range(len(triangles))]
    tail = [v for t in triangles for v in t]
    pairs = {}
    directed = {}
    for i, t in enumerate(triangles):
        for j in range(3):
            d = 3 * i + j
            u, v = t[j], t[(j + 1) % 3]
            pairs.setdefault((u, v), []).append(d)
            directed[cyclic(t), u] = d
    action = {3 * i + j: directed[cyclic(tuple(map(rho, t))), rho(t[j])]
              for i, t in enumerate(triangles) for j in range(3)}
    choices = []
    for u, v in itertools.combinations(range(9), 2):
        a, b = pairs.get((u, v), []), pairs.get((v, u), [])
        assert len(a) == len(b) and len(a) in (1, 2)
        choices.append([list(zip(a, p)) for p in itertools.permutations(b)])
    for selections in itertools.product(*choices):
        alpha = {}
        for matching in selections:
            for a, b in matching:
                alpha[a], alpha[b] = b, a
        if any(alpha[action[d]] != action[alpha[d]] for d in action):
            continue
        m = census.review.TriMap(tri, alpha, tail)
        # Pair-count constraints do not guarantee a single link at each vertex label.
        if m.vertex_count() != 9:
            continue
        census.review.check(m, 9, 3)
        assert census.admissible(m)
        yield m


def enumerate_c3(seconds):
    started = time.monotonic()
    fixed, moving = triangle_orbits()
    columns = sorted({orbit(p, tuple) for p in itertools.permutations(range(9), 2)})
    col = {pair: i for i, o in enumerate(columns) for pair in o}
    rowcols = [Counter(col[a, b] for t in o for a, b in zip(t, t[1:] + t[:1]))
               for o in moving]
    assert all(all(v == 3 for v in c.values()) and len(c) == 3 for c in rowcols)
    rows = [tuple(c) for c in rowcols]
    unordered = [tuple(sorted(tuple(sorted(t)) for t in o)) for o in moving]
    extra_orbits = sorted({orbit(p, lambda x: tuple(sorted(x)))
                           for p in itertools.combinations(range(9), 2)})
    codes, nodes, covers = {}, 0, 0
    for extras in extra_orbits:
        demand = [1] * len(columns)
        for a, b in extras:
            demand[col[a, b]] = demand[col[b, a]] = 2
        for branches in itertools.combinations(fixed, 2):
            branch_tris = [o[0] for o in branches]
            if len({tuple(sorted(t)) for t in branch_tris}) != 2:
                continue
            rem = demand[:]
            for t in branch_tris:
                cs = {col[p] for p in zip(t, t[1:] + t[:1])}
                assert len(cs) == 1
                rem[next(iter(cs))] -= 1
            seen = set()

            def search(chosen, used):
                nonlocal nodes, covers
                nodes += 1
                if nodes % 1024 == 0 and time.monotonic() - started >= seconds:
                    raise TimeoutError("C3 cover time limit")
                key = tuple(sorted(chosen))
                if key in seen:
                    return
                seen.add(key)
                candidates = [i for i, cols in enumerate(rows) if unordered[i] not in used
                              and all(rem[c] > 0 for c in cols)]
                if not any(rem):
                    covers += 1
                    triangles = branch_tris + [t for i in chosen for t in moving[i]]
                    assert len(triangles) == 26
                    for m in gluings(triangles):
                        code = m.canon()[0]
                        codes[code] = True
                    return
                choices = [[i for i in candidates if c in rows[i]]
                           for c, r in enumerate(rem) if r > 0]
                best = min(choices, key=len)
                for i in best:
                    for c in rows[i]:
                        rem[c] -= 1
                    search(chosen + [i], used | {unordered[i]})
                    for c in rows[i]:
                        rem[c] += 1

            try:
                search([], set())
            except TimeoutError:
                return dict(complete=False, stop_reason="time_limit", nodes=nodes, covers=covers,
                            seconds=time.monotonic() - started, codes=sorted(codes))
    return dict(complete=True, stop_reason="exhausted", nodes=nodes, covers=covers,
                seconds=time.monotonic() - started, codes=sorted(codes))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    manifest_path = args.out.with_suffix(".manifest.json")
    if manifest_path.exists():
        raise FileExistsError(manifest_path)
    manifest = dict(started_utc=census.datetime.now(census.timezone.utc).isoformat(),
                    commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=HERE, text=True).strip(),
                    branch=subprocess.check_output(["git", "branch", "--show-current"], cwd=HERE, text=True).strip(),
                    dirty=bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=HERE)),
                    host=platform.platform(), python=sys.version, cpu_count=census.os.cpu_count(), workers=1,
                    seconds=args.seconds, sources={p.name: census.sha256(p) for p in
                    (Path(__file__), HERE / "census.py",
                     census.ROOT / "reviews/strategy-review-2026-11-03-flipwalk.py")})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    try:
        result = enumerate_c3(args.seconds)
        args.out.write_text(json.dumps(result, separators=(",", ":")) + "\n")
        manifest.update(exit_status=0, output_sha256=census.sha256(args.out))
    except BaseException as exc:
        manifest.update(exit_status=1, error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        manifest.update(finished_utc=census.datetime.now(census.timezone.utc).isoformat(),
                        wall_seconds=time.monotonic() - started)
        manifest["core_hours"] = manifest["wall_seconds"] / 3600
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "codes"}, indent=2))
    print("classes:", len(result["codes"]))
