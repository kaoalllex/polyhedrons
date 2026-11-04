"""Bounded representation and dart-preserving surgery audits before geometry."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CENSUS = ROOT / 'experiments/E-261103-01-s5-map-census'
sys.path.insert(0, str(ROOT / 'code'))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(m):
    triangles = []
    for triangle in m.tri:
        i = triangle.index(min(triangle))
        triangles.append(triangle[i:] + triangle[:i])
    return dict(triangles=sorted(triangles),
                alpha=[[d, m.alpha[d]] for d in sorted(m.pos)],
                tail=[[d, m.tail[d]] for d in sorted(m.pos)])


def restore(data, census):
    tails = dict(data['tail'])
    tail = [0] * (max(tails) + 1)
    for d, label in tails.items():
        tail[d] = label
    return census.review.TriMap(data['triangles'], dict(data['alpha']), tail)


def check_surface(data, n, genus, simple=False):
    """Direct permutation check, independent of TriMap's traversal methods."""
    triangles = data['triangles']
    darts = [d for triangle in triangles for d in triangle]
    live = set(darts)
    assert all(len(t) == 3 for t in triangles), 'triangle size'
    assert len(darts) == len(live), 'repeated dart'
    alpha, tail = dict(data['alpha']), dict(data['tail'])
    assert len(alpha) == len(data['alpha']) and set(alpha) == live, 'alpha domain'
    assert len(tail) == len(data['tail']) and set(tail) == live, 'tail domain'
    assert all(alpha[d] in live and alpha[d] != d and alpha[alpha[d]] == d
               for d in live), 'alpha involution'
    nxt, prev = {}, {}
    for a, b, c in triangles:
        nxt.update({a: b, b: c, c: a})
        prev.update({b: a, c: b, a: c})
    assert all(tail[alpha[d]] == tail[nxt[d]]
               and tail[nxt[alpha[d]]] == tail[d] for d in live), 'endpoint labels'
    assert set(tail.values()) == set(range(n)), 'label set'
    assert all(tail[d] != tail[nxt[d]] for d in live), 'loop'
    corners = [tuple(sorted(tail[d] for d in t)) for t in triangles]
    assert all(len(set(t)) == 3 for t in corners), 'corner labels'
    assert len(corners) == len(set(corners)), 'repeated corner triple'
    unseen, labels = set(live), []
    while unseen:
        first = min(unseen)
        d, cycle = first, []
        while d in unseen:
            unseen.remove(d)
            cycle.append(d)
            d = alpha[prev[d]]
        assert d == first, 'vertex cycle'
        values = {tail[e] for e in cycle}
        assert len(values) == 1, 'vertex labels'
        labels.append(values.pop())
    assert sorted(labels) == list(range(n)), 'one vertex link per label'
    reached, todo = set(), [min(live)]
    while todo:
        d = todo.pop()
        if d not in reached:
            reached.add(d)
            todo.extend((alpha[d], nxt[d]))
    assert reached == live, 'disconnected surface'
    assert n - len(live) // 2 + len(triangles) == 2 - 2 * genus, 'Euler'
    pairs = Counter(tuple(sorted((tail[d], tail[alpha[d]])))
                    for d in live if d < alpha[d])
    if simple:
        assert all(count == 1 for count in pairs.values()), 'parallel edges'
    return dict(genus=genus, vertices=n, edges=len(live) // 2,
                triangles=len(triangles), adjacent_pairs=len(pairs),
                max_multiplicity=max(pairs.values()))


def patch_caps(m, selected):
    """Identify an annulus by its actual boundary darts and contiguous vertex fans."""
    if len(selected) != 6:
        return None
    patch = {d for t in selected for d in m.tri[t]}
    boundary = sorted(d for d in patch if m.alpha[d] not in patch)
    labels = {m.tail[d] for d in patch}
    if len(labels) != 6 or len(boundary) != 6:
        return None
    by_tail = {m.tail[d]: d for d in boundary}
    if set(by_tail) != labels:
        return None
    reached, todo = set(), [min(selected)]
    while todo:
        t = todo.pop()
        if t not in reached:
            reached.add(t)
            todo.extend(m.pos[m.alpha[d]][0] for d in m.tri[t]
                        if m.alpha[d] in patch)
    if reached != set(selected):
        return None
    internal_edges = sum(m.alpha[d] in patch for d in patch) // 2
    if len(labels) - internal_edges - len(boundary) + len(selected) != 0:
        return None
    for label in labels:
        fan = {d for d in patch if m.tail[d] == label}
        starts = sum(m.alpha[m.prv(d)] not in fan for d in fan)
        if starts != 1:
            return None
    caps, unseen = [], set(boundary)
    while unseen:
        first, cycle = min(unseen), []
        d = first
        while d in unseen:
            unseen.remove(d)
            cycle.append(d)
            d = by_tail.get(m.head(d))
        if d != first or len(cycle) != 3:
            return None
        caps.append(cycle)
    return caps if len(caps) == 2 else None


def patches(m, deadline):
    """Enumerate connected six-triangle subsets without identifying parallel edges."""
    neighbors = [{m.pos[m.alpha[d]][0] for d in t} for t in m.tri]
    for root in range(len(m.tri)):
        todo, seen = [(root,)], set()
        while todo:
            if time.monotonic() >= deadline:
                raise TimeoutError('per-map wall cap')
            chosen = todo.pop()
            if chosen in seen:
                continue
            seen.add(chosen)
            if len({m.tail[d] for t in chosen for d in m.tri[t]}) > 6:
                continue
            if len(chosen) == 6:
                yield chosen
                continue
            border = set().union(*(neighbors[t] for t in chosen)) - set(chosen)
            for t in sorted(border, reverse=True):
                if t > root:
                    todo.append(tuple(sorted((*chosen, t))))


def remove_patch(m, selected, caps, census):
    patch = {d for t in selected for d in m.tri[t]}
    internal = sorted(d for d in patch if m.alpha[d] in patch)
    alpha = {d: a for d, a in m.alpha.items() if d not in internal}
    triangles = [t for i, t in enumerate(m.tri) if i not in selected] + caps
    child = census.review.TriMap(triangles, alpha, m.tail)
    step = dict(removed_triangles=[m.tri[t] for t in selected], caps=caps,
                internal_alpha=[[d, m.alpha[d]] for d in internal],
                internal_tail=[[d, m.tail[d]] for d in internal])
    return child, step


def reverse_step(child, step, census):
    data = snapshot(child)
    cap_sets = {frozenset(t) for t in step['caps']}
    data['triangles'] = [t for t in data['triangles'] if frozenset(t) not in cap_sets]
    data['triangles'].extend(step['removed_triangles'])
    data['alpha'].extend(step['internal_alpha'])
    data['tail'].extend(step['internal_tail'])
    return restore(data, census)


def check_step(before, after, step, n, genus):
    """Check a recorded transition using edge incidence and patch link graphs."""
    check_surface(before, n, genus)
    check_surface(after, n, genus - 1)
    alpha, tail = dict(before['alpha']), dict(before['tail'])
    removed, caps = step['removed_triangles'], step['caps']
    assert len(removed) == 6 and len(caps) == 2, 'patch/cap sizes'
    old_tri = {tuple(t) for t in before['triangles']}
    normalize = lambda t: tuple(t[t.index(min(t)):] + t[:t.index(min(t))])
    gone = {normalize(t) for t in removed}
    assert len(gone) == 6 and gone <= old_tri, 'removed triangle identity'
    assert {tuple(t) for t in after['triangles']} == (old_tri - gone) | {
        normalize(t) for t in caps}, 'outside triangles changed'
    patch = {d for t in removed for d in t}
    internal = {d for d in patch if alpha[d] in patch}
    boundary = patch - internal
    assert set(d for t in caps for d in t) == boundary, 'cap boundary'
    assert len(boundary) == 6, 'boundary size'
    assert dict(step['internal_alpha']) == {d: alpha[d] for d in internal}, 'inverse alpha'
    assert dict(step['internal_tail']) == {d: tail[d] for d in internal}, 'inverse tails'
    assert dict(after['alpha']) == {d: a for d, a in alpha.items() if d not in internal}, 'surviving alpha'
    assert dict(after['tail']) == {d: v for d, v in tail.items() if d not in internal}, 'surviving tails'
    vertices = {tail[d] for d in patch}
    edge = lambda d: min(d, alpha[d])
    assert len(vertices) == 6 and len(vertices) - len({edge(d) for d in patch}) + 6 == 0, 'patch Euler'
    # Each patch vertex has a connected interval as its link, with two boundary ends.
    for v in vertices:
        links = {}
        for triangle in removed:
            for i, d in enumerate(triangle):
                if tail[d] == v:
                    a, b = edge(triangle[i - 1]), edge(d)
                    links.setdefault(a, []).append(b)
                    links.setdefault(b, []).append(a)
        degrees = sorted(map(len, links.values()))
        assert degrees.count(1) == 2 and all(k in (1, 2) for k in degrees), 'patch vertex link degrees'
        reached, todo = set(), [min(links)]
        while todo:
            e = todo.pop()
            if e not in reached:
                reached.add(e)
                todo.extend(links[e])
        assert reached == set(links), 'patch vertex link disconnected'
    cap_labels = [{tail[d] for d in t} for t in caps]
    assert all(len(s) == 3 for s in cap_labels) and not cap_labels[0] & cap_labels[1], 'boundary cycles'
    incident = {d: i for i, t in enumerate(removed) for d in t}
    reached, todo = set(), [0]
    while todo:
        t = todo.pop()
        if t not in reached:
            reached.add(t)
            todo.extend(incident[alpha[d]] for d in removed[t] if alpha[d] in patch)
    assert len(reached) == 6, 'patch disconnected'


def surgery_chain(name, top, n, genus, census, global_deadline):
    started = time.monotonic()
    deadline = min(global_deadline, started + 5)
    row = dict(name=name, n=n, top_genus=genus, status='NO-CHAIN', expanded_states=0, patches_tested=0,
               surgeries=0, levels=[snapshot(top)], steps=[], reached_genus=genus)
    seen = set()

    def descend(m, g, levels, steps):
        if time.monotonic() >= deadline:
            raise TimeoutError('per-map wall cap')
        check_surface(snapshot(m), n, g)
        code = m.canon()[0]
        if code in seen:
            return False
        if row['expanded_states'] == 256:
            row['status'] = 'STATE-CAP'
            return False
        seen.add(code)
        row['expanded_states'] += 1
        if g < row['reached_genus']:
            row.update(levels=levels, steps=steps, reached_genus=g)
        if g == 0:
            try:
                check_surface(snapshot(m), n, 0, simple=True)
            except AssertionError:
                return False
            row.update(status='CHAIN-PASS', levels=levels, steps=steps)
            return True
        for selected in patches(m, deadline):
            row['patches_tested'] += 1
            caps = patch_caps(m, selected)
            if caps is None:
                continue
            child, step = remove_patch(m, selected, caps, census)
            try:
                check_surface(snapshot(child), n, g - 1)
            except AssertionError:
                continue
            row['surgeries'] += 1
            restored = reverse_step(child, step, census)
            assert snapshot(restored) == snapshot(m), 'labelled inverse mismatch'
            assert restored.canon()[0] == code, 'canonical inverse mismatch'
            check_step(snapshot(m), snapshot(child), step, n, g)
            if descend(child, g - 1, levels + [snapshot(child)], steps + [step]):
                return True
            if row['status'] == 'STATE-CAP':
                return False
        return False

    try:
        descend(top, genus, [snapshot(top)], [])
    except TimeoutError as error:
        row.update(status='TIMEOUT', limit=str(error))
    row['wall_seconds'] = time.monotonic() - started
    row['budget_fraction'] = row['wall_seconds'] / 5
    rebuilt = restore(row['levels'][-1], census)
    for step in reversed(row['steps']):
        rebuilt = reverse_step(rebuilt, step, census)
    row['same_labelled_top'] = snapshot(rebuilt) == snapshot(top)
    row['same_canonical_top'] = rebuilt.canon()[0] == top.canon()[0]
    assert row['same_labelled_top'] and row['same_canonical_top'], 'chain inverse'
    return row


def check_saved_surgery(path, census):
    evidence = json.loads(path.read_text())
    for row in evidence['rows']:
        n, genus = row['n'], row['top_genus']
        levels, steps = row['levels'], row['steps']
        assert len(levels) == len(steps) + 1, 'saved chain length'
        assert row['reached_genus'] == genus - len(steps), 'saved reached genus'
        for index, level in enumerate(levels):
            check_surface(level, n, genus - index,
                          simple=row['status'] == 'CHAIN-PASS' and index == len(steps))
        for index, step in enumerate(steps):
            check_step(levels[index], levels[index + 1], step, n, genus - index)
        top = restore(levels[0], census)
        rebuilt = restore(levels[-1], census)
        for step in reversed(steps):
            rebuilt = reverse_step(rebuilt, step, census)
        assert snapshot(rebuilt) == levels[0], 'saved labelled top'
        assert rebuilt.canon()[0] == top.canon()[0], 'saved canonical top'
        if row['status'] == 'CHAIN-PASS':
            assert row['reached_genus'] == 0, 'saved endpoint genus'


def surgery_controls(m, row, census):
    data = snapshot(m)
    negative = {}
    for name in ('broken_alpha', 'wrong_tail'):
        broken = json.loads(json.dumps(data))
        if name == 'broken_alpha':
            broken['alpha'][0][1] = broken['alpha'][0][0]
        else:
            broken['tail'][0][1] = (broken['tail'][0][1] + 1) % 7
        try:
            check_surface(broken, 7, 1)
        except AssertionError as error:
            negative[name] = str(error)
    assert negative.get('broken_alpha') == 'alpha involution', 'alpha negative control'
    assert negative.get('wrong_tail') == 'endpoint labels', 'tail negative control'
    assert row['steps'], 'missing patch control fixture'
    step = row['steps'][0]
    child = restore(row['levels'][1], census)
    cap_sets = {frozenset(t) for t in step['caps']}
    selected = [i for i, t in enumerate(child.tri) if frozenset(t) in cap_sets]
    assert patch_caps(child, selected) is None, 'disconnected caps accepted'
    negative['disconnected_caps'] = 'rejected'
    from tubes import tubes
    from gauss_degree import coherent_triangles, links_from
    triples = [tuple(m.tail[d] for d in t) for t in m.tri]
    target_code = child.canon()[0]
    compatibility = False
    for a, b, removed in tubes(triples, 7):
        remaining = [tuple(sorted(t)) for t in triples]
        for t in removed:
            remaining.remove(tuple(sorted(t)))
        links = links_from(coherent_triangles(remaining + [tuple(a), tuple(b)]), 7)
        recovered = census.from_links([links[v] for v in range(7)])
        if recovered.canon()[0] == target_code:
            compatibility = True
            break
    assert compatibility, 'legacy Szilassi capped-map mismatch'
    return dict(negative=negative, legacy_capped_map_match=compatibility)


def run_surgery(census, result, save, deadline):
    records = json.loads((CENSUS / 'results/maps_7_1.json').read_text())['maps']
    szilassi = next(record for record in records if record['admissible'])
    controls = [('szilassi', census.from_code(szilassi['code']), 7, 1)]
    from control_rost_vigh import build
    _, links = build()
    mizhaev = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())['links_0based']
    if isinstance(mizhaev, dict):
        mizhaev = [mizhaev[str(v)] for v in range(len(mizhaev))]
    for name, link in (('roest_vigh', links), ('mizhaev', mizhaev)):
        coherent = census.review.coherent(dict(enumerate(link)) if isinstance(link, list) else link)
        m = census.from_links([coherent[v] for v in range(8)])
        controls.append((name, m, 8, 3))
    result.update(controls_pass=False, gate_pass=False, focus_processed=0)
    for name, m, n, genus in controls:
        census.review.check(m, n, genus)
        row = surgery_chain(name, m, n, genus, census, deadline)
        result['rows'].append(row)
        save()
        if row['status'] != 'CHAIN-PASS':
            result.update(stop_reason='CONTROL-FAIL', failed_control=name)
            return
        if name == 'szilassi':
            try:
                result['structural_controls'] = surgery_controls(m, row, census)
            except AssertionError as error:
                result.update(stop_reason='CONTROL-FAIL', failed_control='structural', error=str(error))
                return
            save()
    result.update(controls_pass=True, gate_pass=True)
    records = json.loads((CENSUS / 'results/maps_9_3.json').read_text())['maps']
    for index, record in enumerate(records):
        if not record['admissible']:
            continue
        if time.monotonic() >= deadline:
            result['stop_reason'] = 'TIMEOUT'
            return
        m = census.from_code(record['code'])
        census.review.check(m, 9, 3)
        result['rows'].append(surgery_chain(f'focus_{index}', m, 9, 3, census, deadline))
        result['focus_processed'] += 1
        save()
    result['stop_reason'] = 'COMPLETE'


def roundtrip(name, m, census):
    from gauss_degree import coherent_triangles, links_from
    edges = Counter((m.tail[d], m.head(d)) for d in m.pos)
    row = dict(name=name, vertices=m.vertex_count(), edges=len(m.pos) // 2,
               triangles=len(m.tri), max_directed_multiplicity=max(edges.values()))
    try:
        triangles = [tuple(m.tail[d] for d in t) for t in m.tri]
        links = links_from(coherent_triangles(triangles), m.vertex_count())
        recovered = census.from_links([links[v] for v in range(m.vertex_count())])
        row['same_dart_code'] = recovered.canon()[0] == m.canon()[0]
        row['recovered_edges'] = len(recovered.pos) // 2
        row['status'] = 'ROUNDTRIP-PASS' if row['same_dart_code'] else 'ROUNDTRIP-FAIL'
    except (AssertionError, ValueError, KeyError) as error:
        row.update(status='ROUNDTRIP-FAIL', error_type=type(error).__name__, error=str(error))
    return row


def main(out, stage='representation'):
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    budget = 300 if stage == 'surgery' else 120
    manifest = dict(started_utc=datetime.now(timezone.utc).isoformat(), workers=1,
                    host=platform.platform(), cpu_count=os.cpu_count(),
                    python=sys.version, executable=sys.executable,
                    cwd=os.getcwd(), virtual_env=os.environ.get('VIRTUAL_ENV'),
                    parameters=dict(stage=stage, wall_seconds=budget))
    if stage == 'surgery':
        manifest['parameters'].update(per_map_seconds=5, expanded_states=256)
    for key, command in (
        ('commit', ['git', 'rev-parse', 'HEAD']),
        ('branch', ['git', 'branch', '--show-current']),
        ('dirty', ['git', 'status', '--porcelain']),
        ('pip_freeze', [sys.executable, '-m', 'pip', 'freeze']),
    ):
        manifest[key] = subprocess.check_output(command, cwd=ROOT, text=True).strip()
    paths = [Path(__file__), HERE / 'PLAN.md', HERE / 'run.sh', CENSUS / 'census.py',
             ROOT / 'reviews/strategy-review-2026-11-03-flipwalk.py',
             ROOT / 'code/gauss_degree.py', ROOT / 'code/control_rost_vigh.py',
             ROOT / 'literature/mizhaev2026-planes.json',
             CENSUS / 'results/maps_7_1.json', CENSUS / 'results/maps_9_3.json']
    if stage == 'surgery':
        paths.append(ROOT / 'code/tubes.py')
    manifest['inputs'] = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    scope = 'dart-preserving six-triangle surgery' if stage == 'surgery' else 'legacy triangle-to-links round-trip only'
    result = dict(rows=[], scope=scope)

    def save():
        (out / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')

    def expired(signum, frame):
        raise TimeoutError(f'registered {budget}-second audit budget')

    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, max(0.001, budget - (time.monotonic() - started)))
    try:
        census = load_module('s5_census', CENSUS / 'census.py')
        if stage == 'surgery':
            run_surgery(census, result, save, started + budget)
            save()
            check_saved_surgery(out / 'audit.json', census)
            result['saved_evidence_check'] = 'PASS'
            manifest['exit_status'] = 0
            print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))
            return
        # Frozen census maps retain parallel-edge identities in their dart codes.
        for filename, prefix in (('maps_7_1.json', 'szilassi'), ('maps_9_3.json', 'focus')):
            data = json.loads((CENSUS / 'results' / filename).read_text())
            for index, record in enumerate(data['maps']):
                if record['admissible']:
                    m = census.from_code(record['code'])
                    result['rows'].append(roundtrip(f'{prefix}_{index}', m, census))
                    save()
        from control_rost_vigh import build
        _, links = build()
        mizhaev = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())['links_0based']
        if isinstance(mizhaev, dict):
            mizhaev = [mizhaev[str(v)] for v in range(len(mizhaev))]
        for name, link in (('roest_vigh', [links[v] for v in range(len(links))]),
                           ('mizhaev', mizhaev)):
            result['rows'].append(roundtrip(name, census.from_links(list(census.review.coherent(dict(enumerate(link))).values())), census))
            save()
        rows = result['rows']
        positive = [r for r in rows if r['name'].startswith('szilassi_')]
        negative = next(r for r in rows if r['name'] == 'roest_vigh')
        result['controls_pass'] = (len(positive) == 1
                                  and positive[0]['status'] == 'ROUNDTRIP-PASS'
                                  and negative['max_directed_multiplicity'] > 1
                                  and negative['status'] == 'ROUNDTRIP-FAIL')
        result['gate_pass'] = (result['controls_pass']
                               and all(r['status'] == 'ROUNDTRIP-PASS' for r in rows
                                       if not r['name'].startswith('szilassi_')))
        result['stop_reason'] = 'COMPLETE'
        manifest['exit_status'] = 0
    except BaseException as error:
        result.update(stop_reason=type(error).__name__, error=str(error))
        if stage == 'surgery':
            result.update(gate_pass=False, error_type=type(error).__name__,
                          stop_reason='TIMEOUT' if isinstance(error, TimeoutError) else 'ERROR')
        manifest['exit_status'] = 1
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
        save()
        elapsed = time.monotonic() - started
        manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(),
                        wall_seconds=elapsed, core_hours=elapsed / 3600,
                        budget_fraction=elapsed / budget,
                        outputs={'audit.json': digest(out / 'audit.json')})
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--stage', choices=('representation', 'surgery'), default='representation')
    args = parser.parse_args()
    main(args.out, args.stage)
