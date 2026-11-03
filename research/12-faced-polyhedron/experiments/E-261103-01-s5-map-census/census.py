"""Bounded exhaustive triangular-map census; Python standard library and a C compiler."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
spec = importlib.util.spec_from_file_location(
    "s5_review", ROOT / "reviews/strategy-review-2026-11-03-flipwalk.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def graph_code(edges):
    """Canonicalize small extra-edge graphs component by component (isolates omitted)."""
    if not edges:
        return ()
    deg = Counter(v for e in edges for v in e)
    unseen = set(deg)
    components = []
    while unseen:
        todo = [min(unseen)]
        component = set(todo)
        while todo:
            v = todo.pop()
            for a, b in edges:
                if v in (a, b):
                    w = b if v == a else a
                    if w not in component:
                        component.add(w)
                        todo.append(w)
        unseen -= component
        groups = [[v for v in sorted(component) if deg[v] == d]
                  for d in sorted({deg[v] for v in component}, reverse=True)]
        local = [e for e in edges if e[0] in component]
        best = None
        for parts in itertools.product(*(itertools.permutations(g) for g in groups)):
            order = tuple(itertools.chain.from_iterable(parts))
            label = {v: i for i, v in enumerate(order)}
            code = tuple(sorted(tuple(sorted((label[a], label[b]))) for a, b in local))
            if best is None or code < best:
                best = code
        components.append((len(component), best))
    offset, result = 0, []
    for size, code in sorted(components):
        result.extend((a + offset, b + offset) for a, b in code)
        offset += size
    return tuple(result)


def extra_graphs(n, k):
    graphs = {()}
    for _ in range(k):
        next_graphs = set()
        for edges in graphs:
            active = 1 + max((v for e in edges for v in e), default=-1)
            for a, b in itertools.combinations(range(min(n, active + 2)), 2):
                next_graphs.add(graph_code(edges + ((a, b),)))
        graphs = next_graphs
    out = []
    for edges in sorted(graphs):
        deg = Counter(v for e in edges for v in e)
        root = max(range(n), key=lambda v: deg[v])
        label = list(range(n))
        label[0], label[root] = root, 0
        out.append(tuple(sorted(tuple(sorted((label[a], label[b]))) for a, b in edges)))
    return out


def from_code(code):
    """Recover phi, alpha and vertex labels; retain pairing even for repeated triples."""
    nd = len(code)
    step, alpha = zip(*code)
    assert sorted(step) == list(range(nd))
    assert all(0 <= a < nd and a != d and alpha[a] == d for d, a in enumerate(alpha))
    prev = [0] * nd
    for d, e in enumerate(step):
        prev[e] = d
    tri, seen = [], set()
    for d in range(nd):
        if d in seen:
            continue
        t = [d, step[d], step[step[d]]]
        assert len(set(t)) == 3 and step[t[-1]] == d
        assert not seen.intersection(t)
        tri.append(t)
        seen.update(t)
    tail = [-1] * nd
    vertex = 0
    for d in range(nd):
        if tail[d] != -1:
            continue
        e = d
        while tail[e] == -1:
            tail[e] = vertex
            e = alpha[prev[e]]
        assert e == d
        vertex += 1
    return review.TriMap(tri, dict(enumerate(alpha)), tail)


def from_links(links):
    """Recover a map when the two endpoint corners uniquely identify every edge copy."""
    darts = [(v, i) for v, neighbors in enumerate(links) for i in range(len(neighbors))]
    ids = {p: d for d, p in enumerate(darts)}
    alpha = []
    for v, i in darts:
        neighbors = links[v]
        w = neighbors[i]
        other = links[w]
        matches = [j for j, x in enumerate(other) if x == v
                   and other[j - 1] == neighbors[(i + 1) % len(neighbors)]
                   and other[(j + 1) % len(other)] == neighbors[i - 1]]
        if len(matches) != 1:
            raise ValueError("links do not uniquely identify parallel-edge pairing; use dart code")
        alpha.append(ids[w, matches[0]])
    prev = [ids[v, (i - 1) % len(links[v])] for v, i in darts]
    return from_code([(prev[alpha[d]], alpha[d]) for d in range(len(darts))])


def admissible(m):
    triples = [tuple(sorted(m.tail[d] for d in t)) for t in m.tri]
    return len(set(triples)) == len(triples)


def record(code, n, genus):
    m = from_code(code)
    review.check(m, n, genus)
    canonical, aut, reflexible, _, _ = m.canon()
    assert canonical == tuple(map(tuple, code)), "C/Python canonical-code mismatch"
    rec = review.invariants(m, n)
    rec.update(code=code, admissible=admissible(m), aut_plus=aut, reflexible=reflexible,
               autos=review.aut_report(m),
               links=[[m.head(d) for d in c] for c in m.vertices()[0]])
    return rec


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(n, genus, seconds, out):
    k = 3 * (n + 2 * genus - 2) - n * (n - 1) // 2
    if not 3 <= n <= 12 or not 0 <= k <= 8 or seconds < 0:
        raise ValueError("requires 3..12 vertices, 0..8 extra edges and nonnegative seconds")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise FileExistsError("choose a fresh output directory; existing runs are immutable")
    started = time.monotonic()
    manifest = dict(started_utc=datetime.now(timezone.utc).isoformat(),
                    commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    branch=subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
                    dirty=bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT)),
                    host=platform.platform(), cpu_count=os.cpu_count(), python=sys.version,
                    workers=1, n=n, genus=genus, seconds=seconds,
                    sources={p.name: sha256(p) for p in (HERE / "enum_multi.c", Path(__file__),
                              ROOT / "reviews/strategy-review-2026-11-03-flipwalk.py")})
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with (out / "pip-freeze.txt").open("w") as f:
        subprocess.run([sys.executable, "-m", "pip", "--no-cache-dir", "freeze"], stdout=f, check=True)
    try:
        graphs = extra_graphs(n, k)
        input_path = out / "graphs.txt"
        input_path.write_text(f"{n} {genus} {k} {len(graphs)}\n" + "".join(
            " ".join(str(v) for e in edges for v in e) + "\n" for edges in graphs))
        binary = out / "enum_multi"
        cc = os.environ.get("CC", "cc")
        manifest["compiler"] = subprocess.check_output([cc, "--version"], text=True).splitlines()[0]
        subprocess.run([cc, "-O3", "-std=c11", "-Wall", "-Wextra", "-Werror",
                        str(HERE / "enum_multi.c"), "-o", str(binary)], check=True)
        with (out / "raw.jsonl").open("w") as f, (out / "progress.txt").open("w") as log:
            subprocess.run([str(binary.resolve()), str(input_path.resolve()), str(seconds)],
                           stdout=f, stderr=log, timeout=seconds + 15, check=True)
        rows = [json.loads(s) for s in (out / "raw.jsonl").read_text().splitlines()]
        result = rows.pop()
        assert result.pop("summary") is True
        result.update(n=n, genus=genus, maps=[record(r["code"], n, genus) for r in rows])
        assert result["classes"] == len(result["maps"])
        (out / f"maps_{n}_{genus}.json").write_text(json.dumps(result, separators=(",", ":")) + "\n")
        manifest["exit_status"] = 0
        return result
    except BaseException as exc:
        manifest.update(exit_status=1, error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(),
                        wall_seconds=time.monotonic() - started)
        manifest["core_hours"] = manifest["wall_seconds"] / 3600
        manifest["files"] = {p.name: sha256(p) for p in out.iterdir()
                             if p.is_file() and p.name != "manifest.json"}
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("genus", type=int)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.n, args.genus, args.seconds, args.out)
    print(json.dumps({k: v for k, v in result.items() if k != "maps"}, indent=2))
