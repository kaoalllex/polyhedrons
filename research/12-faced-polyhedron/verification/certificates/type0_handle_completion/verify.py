#!/usr/bin/env python3
"""Independently verify a genus-3 -> genus-6 *combinatorial* handle-chain certificate.

This checks closed orientable triangulated maps and the three explicit handle surgeries.
It deliberately does NOT claim geometric embeddings for genus 4, 5, or 6.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from collections import defaultdict, deque
from pathlib import Path


def edges_of(tris):
    return {tuple(sorted(e)) for t in tris for e in itertools.combinations(t, 2)}


def check_map(tris, n=12):
    tris = [tuple(map(int, t)) for t in tris]
    assert len(tris) == len(set(tuple(sorted(t)) for t in tris)), "duplicate triangles"
    assert all(len(t) == 3 and len(set(t)) == 3 and min(t) >= 0 and max(t) < n for t in tris), "bad triangle"
    assert set(v for t in tris for v in t) == set(range(n)), "not all 12 vertices are used"

    edge_faces = defaultdict(list)
    oriented = []
    for i, (a, b, c) in enumerate(tris):
        for u, v in ((a, b), (b, c), (c, a)):
            edge_faces[tuple(sorted((u, v)))].append((i, 1 if u < v else -1))
    assert all(len(inc) == 2 for inc in edge_faces.values()), "edge incidence is not exactly two"

    # The dual graph must be connected, and the triangle orientations must be globally consistent.
    adj = [[] for _ in tris]
    for edge, inc in edge_faces.items():
        (i, di), (j, dj) = inc
        adj[i].append((j, -di * dj))
        adj[j].append((i, -di * dj))
    orientation = {0: 1}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j, relation in adj[i]:
            required = orientation[i] * relation
            if j in orientation:
                assert orientation[j] == required, "surface is non-orientable"
            else:
                orientation[j] = required
                queue.append(j)
    assert len(orientation) == len(tris), "triangle adjacency graph is disconnected"

    # Each vertex link must be one cycle (2-regular and connected).
    for v in range(n):
        link = defaultdict(set)
        incident = [t for t in tris if v in t]
        for t in incident:
            a, b = [x for x in t if x != v]
            link[a].add(b)
            link[b].add(a)
        assert link and all(len(ns) == 2 for ns in link.values()), f"link at vertex {v} is not 2-regular"
        start = next(iter(link))
        seen = {start}
        stack = [start]
        while stack:
            x = stack.pop()
            for y in link[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        assert len(seen) == len(link), f"link at vertex {v} is disconnected"

    V, E, F = n, len(edge_faces), len(tris)
    chi = V - E + F
    assert (2 - chi) % 2 == 0 and chi <= 2, "not an orientable closed surface Euler characteristic"
    genus = (2 - chi) // 2
    return {"V": V, "E": E, "F": F, "chi": chi, "genus": genus, "adjacent_pairs": E}


def verify(cert_path: Path, source_path: Path | None, catalog_path: Path | None):
    cert = json.loads(cert_path.read_text())
    if source_path:
        digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
        assert digest == cert["source_sha256"], "source file SHA-256 mismatch"
        initial = json.loads(source_path.read_text())
        assert {tuple(sorted(t)) for t in initial["triangles"]} == {
            tuple(sorted(t)) for t in cert["levels"][0]["map_triangles"]
        }, "certificate initial map does not match source JSON"

    assert len(cert["levels"]) == 4, "expected genus 3, 4, 5, 6 levels"
    for i, level in enumerate(cert["levels"]):
        inv = check_map(level["map_triangles"], 12)
        for key in ("genus", "triangles", "adjacent_pairs", "chi"):
            observed = inv["F"] if key == "triangles" else inv[key]
            assert observed == level[key], f"level {i}: mismatch in {key}: {observed} != {level[key]}"
        expected = {"genus": 3 + i, "F": 32 + 4 * i, "E": 48 + 6 * i, "chi": -4 - 2 * i}
        for key, value in expected.items():
            assert inv[key] == value, f"level {i}: unexpected {key}: {inv[key]} != {value}"
        print(f"genus {inv['genus']}: V={inv['V']} E={inv['E']} F={inv['F']} chi={inv['chi']}; orientable closed map OK")

    assert len(cert["handle_attachments"]) == 3
    for i, surgery in enumerate(cert["handle_attachments"]):
        old = {tuple(sorted(t)) for t in cert["levels"][i]["map_triangles"]}
        new = {tuple(sorted(t)) for t in cert["levels"][i + 1]["map_triangles"]}
        removed = {tuple(sorted(t)) for t in surgery["remove_triangles"]}
        inserted = {tuple(sorted(t)) for t in surgery["insert_triangles"]}
        assert len(removed) == 2 and removed <= old, f"handle {i+1}: missing removed triangles"
        assert len(inserted) == 6 and len(inserted & old) == 0, f"handle {i+1}: expected six new triangles"
        assert new == (old - removed) | inserted, f"handle {i+1}: map transition mismatch"
        old_edges, new_edges = edges_of(old), edges_of(new)
        added = new_edges - old_edges
        listed = {tuple(sorted(e)) for e in surgery["new_adjacencies"]}
        assert len(added) == 6 and added == listed, f"handle {i+1}: new adjacency certificate mismatch"
        print(f"  handle {i+1}: remove {sorted(removed)}; add 6 triangles; +6 new adjacencies")

    if catalog_path:
        catalog = json.loads(catalog_path.read_text())
        target = next(item for item in catalog if item["id"] == 0)
        final_set = {tuple(sorted(t)) for t in cert["levels"][-1]["map_triangles"]}
        catalog_set = {tuple(sorted(t)) for t in target["triangles"]}
        assert final_set == catalog_set, "final map is not catalog type 0 under current labels"
        print("final genus-6 map matches catalog type 0 under the saved vertex labels")
    print("PASS: combinatorial completion certificate verified; no genus-4/5/6 geometry is asserted")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("certificate", type=Path)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--catalog", type=Path)
    args = ap.parse_args()
    verify(args.certificate, args.source, args.catalog)
