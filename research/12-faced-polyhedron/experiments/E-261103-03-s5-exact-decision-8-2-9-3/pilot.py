"""Bounded S5 decision pilot. Each negative claim is scoped to its saved formula."""
import argparse
from contextlib import nullcontext
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import resource
import shlex
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder'))
sys.path.insert(0, str(ROOT / 'experiments/E-261101-25-chirotope-first'))
from test_encoder import controls, from_links, EncoderTests
from omsat import CNF, Triangulation, build, chirotope_from_planes
from omsat_validate import ALL_OPTS
from omsat_sym import build_sym, closure
from ladder_exact import verify

# SAT_SOLVER / SOLVER_OPTS select another DRAT-producing solver (E-261108-03); the default stays plain CaDiCaL.
CADICAL = os.environ.get('SAT_SOLVER') or os.environ.get('CADICAL', str(Path.home() / 'bin/cadical'))
SOLVER_OPTS = shlex.split(os.environ.get('SOLVER_OPTS', ''))
# NO_PROOF=1: no DRAT; an UNSAT is the solver's claim (UNSAT-SOLVER), usable to skip a map, never as a negative result.
NO_PROOF = os.environ.get('NO_PROOF') == '1'
UNSAT_OK = 'UNSAT-SOLVER' if NO_PROOF else 'UNSAT-VERIFIED'
DRAT = os.environ.get('DRAT_TRIM', str(Path.home() / 'bin/drat-trim'))


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def command(args, log, timeout, gate=None):
    def interrupted(signum, frame):
        raise InterruptedError('command interrupted by SIGTERM')
    old_handler = signal.signal(signal.SIGTERM, interrupted)
    with log.open('w') as stream:
        try:
            with gate() if gate is not None else nullcontext():
                p = subprocess.Popen(args, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                return p.wait(timeout=max(.001, timeout))
            except BaseException as exc:
                # Nested command wrappers get a chance to reap their own process groups.
                try:
                    os.killpg(p.pid, signal.SIGTERM)
                    p.wait(timeout=1)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    pass
                finally:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    p.wait()
                if not isinstance(exc, subprocess.TimeoutExpired):
                    raise
                return None
        finally:
            signal.signal(signal.SIGTERM, old_handler)


def model_valid(clauses, model):
    values = set(model)
    return not any(-v in values for v in values) and all(any(v in values for v in cl) for cl in clauses)


def check_proof(cnf, proof, log, timeout):
    rc = command([DRAT, str(cnf), str(proof)], log, timeout)
    return rc == 0 and 's VERIFIED' in log.read_text()


def solve(c, out, name, timeout, checker_timeout=None, on_sat=None, solver_gate=None):
    checker_timeout = timeout if checker_timeout is None else checker_timeout
    cnf = out / (name + '.cnf'); proof = out / (name + '.drat')
    c.dimacs(cnf, comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
    started = time.monotonic()
    rc = command([CADICAL, *SOLVER_OPTS, str(cnf)] + ([] if NO_PROOF else [str(proof)]), out / (name + '.solver.log'), timeout, gate=solver_gate)
    elapsed = time.monotonic() - started
    r = dict(status='TIMEOUT' if rc is None else 'ERROR', seconds=elapsed, budget_seconds=timeout,
             budget_fraction=elapsed / timeout, ended_by='solver_timeout' if rc is None else 'completed',
             variables=c.nv, clauses=len(c.clauses), cnf_sha256=sha(cnf),
             # peak RSS of finished children so far (bytes on macOS, KiB on Linux): solver here, max with checker below
             solver_children_maxrss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    if rc == 10:
        model = [int(v) for line in (out / (name + '.solver.log')).read_text().splitlines()
                 if line.startswith('v ') for v in line[2:].split() if int(v)]
        assert model_valid(c.clauses, model), 'invalid SAT assignment'
        dump(out / (name + '.model.json'), model)
        r.update(status='SAT', model_checked=True)
        if on_sat is not None:
            on_sat()
    elif rc == 20 and NO_PROOF:
        r.update(status='UNSAT-SOLVER')
    elif rc == 20:
        # Checking has its own bounded allocation; the caller bounds the whole unit too.
        check_started = time.monotonic()
        ok = check_proof(cnf, proof, out / (name + '.checker.log'), checker_timeout)
        r.update(status='UNSAT-VERIFIED' if ok else 'UNSAT-UNCHECKED',
                 checker_seconds=time.monotonic() - check_started, checker_budget_seconds=checker_timeout,
                 checker_ended_by='completed' if ok else 'failed_or_timeout',
                 checker_children_maxrss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    if proof.exists():
        r['proof_sha256'] = sha(proof)
    # The proof was checked above; records keep the hashes and transcripts, not the files (PROTOCOL.md §5).
    for path in (cnf, proof):
        path.unlink(missing_ok=True)
    return r


def census(f, g):
    return json.loads((ROOT / f'experiments/E-261103-01-s5-map-census/results/maps_{f}_{g}.json').read_text())


def free_c2(links):
    # Perfect matchings enumerate all free involutions, preserving the actual cyclic links.
    def match(left, p):
        if not left:
            yield tuple(p)
            return
        a, *rest = left
        for b in rest:
            q = p[:]; q[a] = b; q[b] = a
            yield from match([v for v in rest if v != b], q)
    for p in match(list(range(len(links))), [-1] * len(links)):
        if all(any([p[v] for v in link] == links[p[i]][j:] + links[p[i]][:j]
                   for j in range(len(link))) for i, link in enumerate(links)):
            return p
    raise ValueError('no free orientation-preserving C2')


def free_c3(links):
    # The image of face 0 and its cyclic link determines every face image.
    for image, link in enumerate(links):
        if len(link) != len(links[0]):
            continue
        for shift in range(len(link)):
            p = {0: image}
            for a, b in zip(links[0], link[shift:] + link[:shift]):
                if a in p and p[a] != b:
                    break
                p[a] = b
            else:
                if len(p) != 9 or len(set(p.values())) != 9:
                    continue
                q = tuple(p[k] for k in range(9))
                if not all(q[k] != k and q[q[q[k]]] == k for k in range(9)):
                    continue
                if all(any([q[v] for v in a] == links[q[k]][j:] + links[q[k]][:j]
                           for j in range(len(a))) for k, a in enumerate(links)):
                    return q
    return None


def paired_formulas():
    maps = census(9, 3)['maps']
    paired = [(i, rec, free_c3(rec['links'])) for i, rec in enumerate(maps)
              if rec['admissible'] and rec['aut_plus'] % 3 == 0]
    paired = [(i, rec, p) for i, rec, p in paired if p is not None]
    assert len(paired) == 8
    ids = {i for i, _, _ in paired}
    order = [paired[0], paired[5]]
    early = [unit for i, rec, p in order for unit in ((i, rec, p), (i, rec, None))]
    extra = [(i, maps[i], None) for i in (10, 30, 40, 48)]
    assert all(rec['admissible'] for _, rec, _ in extra)
    rest = [unit for i, rec, p in paired if i not in (0, 5)
            for unit in ((i, rec, p), (i, rec, None))]
    return early + extra + rest


def grid_units():
    baseline = json.loads((HERE / 'results/paired_9_3_continued/summary.json').read_text())['targets']
    maps = census(9, 3)['maps']
    units = []
    for cap in (60, 300):
        for i in (0, 1, 40, 48):
            r = baseline[f'map{i}_plain']
            assert r['status'] in ('TIMEOUT', 'INTERRUPTED')
            if cap == 60 and r['status'] == 'TIMEOUT' and r['budget_seconds'] >= 60:
                continue
            units.append((i, maps[i], None, cap))
    return units


def reconstruction_ok(wrong_signs, exact_match):
    return wrong_signs == 0 and exact_match


def worker(args):
    data = json.loads(args.input.read_text())
    chi = {tuple(map(int, k.split(','))): v for k, v in data['chi'].items()}
    if args.task == 'fp':
        import final_polynomial as fp
        result = fp.final_polynomial(chi, len(data['links']) + 1, time_limit=120)
        if result.get('certificate'):
            spec = importlib.util.spec_from_file_location('fp_checker', ROOT / 'verification/certificates/final_polynomial/verify.py')
            checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
            cert = result['certificate']
            linked = all(chi[tuple(map(int, k.split(',')))] == v for k, v in cert['signs'].items())
            result['independent_check'] = checker.check(cert)
            assert linked and result['independent_check'][0]
    else:
        import chirotope_first as cf
        import numpy as np
        fn = cf.realize if args.task == 'hinge' else cf.realize2
        # A payload may name its restart count (E-261110-02 bridge); the default keeps the E-261103-03 behaviour.
        planes, bad = fn(chi, len(data['links']), start_planes=data.get('start_planes'),
                         restarts=data.get('restarts') or
                         (2 if args.task == 'two_stage' and data.get('start_planes') is not None else 1),
                         rng=np.random.default_rng(26110303))
        match = reconstruction_ok(bad, planes is not None and chirotope_from_planes(planes) == chi)
        result = dict(wrong_signs=bad, signs_match=match)
        if match:
            # A sub-map (S6) has non-adjacent pairs by definition, so the all-pairs requirement is dropped for it.
            result['geometry'] = verify(planes, dict(enumerate(data['links'])), require_all_pairs=not data.get('submap'))
            result['planes'] = [[int(x) for x in row] for row in planes]
    dump(args.output, result)


def stage(out, name, task, inp, budget):
    ip = out / (name + '.input.json'); op = out / (name + '.output.json')
    dump(ip, inp)
    t0 = time.monotonic()
    rc = command([sys.executable, str(Path(__file__).resolve()), '--task', task,
                  '--input', str(ip), '--output', str(op)], out / (name + '.log'), budget)
    result = json.loads(op.read_text()) if rc == 0 else dict(status='TIMEOUT' if rc is None else 'ERROR')
    result.update(seconds=time.monotonic() - t0, budget_seconds=budget,
                  ended_by='hard_timeout' if rc is None else 'completed')
    return result


def payload(chi, links, start=None, **options):
    return dict(chi={','.join(map(str, k)): v for k, v in chi.items()}, links=links, start_planes=start, **options)


def arm_deadline(seconds):
    def expired(signum, frame):
        raise TimeoutError("pilot computation deadline exhausted")
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)


def main(out, paired=False, resume=None, grid=False, controls_only=False):
    out.mkdir(parents=True, exist_ok=False)
    previous = json.loads((resume / 'manifest.json').read_text()) if resume else None
    prior_seconds = previous['wall_seconds'] if previous and not grid else 0
    start = time.monotonic(); deadline = start + (3300 - prior_seconds if paired else 900); control_deadline = start + 300
    report = dict(status='RUNNING', controls={}, targets={})
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
                    python=sys.version, host=platform.platform(), started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                    workers=1, wall_budget_seconds=3300 if paired else 900,
                    branch=subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip(),
                    cpu_count=os.cpu_count(), family='grid_9_3' if grid else ('paired_9_3' if paired else 'warmup_8_2'))
    manifest['prior_wall_seconds'] = prior_seconds
    manifest['resume'] = str(resume) if resume else None
    dump(out / 'manifest.json', manifest)
    command([sys.executable, '-m', 'pip', 'freeze'], out / 'pip-freeze.txt', 20)
    def remaining(cap, end=deadline):
        value = min(cap, end - time.monotonic())
        if value <= 0:
            raise TimeoutError('stage budget exhausted')
        return value
    def save():
        dump(out / 'summary.json', report)
    arm_deadline(max(.001, deadline - time.monotonic()))
    try:
        fixtures = controls()[:2]
        unseeded = []
        for name, h, t in fixtures:
            links = [t.link[i] for i in range(t.n)]
            chi = chirotope_from_planes(h)
            c = CNF(t.n); build(c, t, ALL_OPTS)
            c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()])
            r = solve(c, out, name, remaining(30, control_deadline) / 2)
            assert r['status'] == 'SAT', r
            report['controls'][name] = r
            for method in ('hinge', 'two_stage'):
                for warm in (True, False):
                    key = f'{name}_{method}_{"warm" if warm else "unseeded"}'
                    result = stage(out, key, method, payload(chi, links, h if warm else None), remaining(45, control_deadline))
                    report['controls'][key] = result; save()
                    good = result.get('signs_match') and result.get('geometry', {}).get('EMBEDDED')
                    if warm:
                        assert good, (key, result)
                    else:
                        unseeded.append(bool(good))
        h, t = fixtures[0][1], fixtures[1][2]
        c = CNF(t.n); build(c, t, ALL_OPTS)
        c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chirotope_from_planes(h).items()])
        r = solve(c, out, 'negative_cross_map', remaining(30, control_deadline) / 2)
        report['controls']['negative_cross_map'] = r
        assert r['status'] == UNSAT_OK, r
        EncoderTests('test_all_nonadmissible_census_maps_are_rejected_without_geometry').test_all_nonadmissible_census_maps_are_rejected_without_geometry()
        report['controls']['inadmissible_maps'] = 'REJECTED'
        report['construction_power'] = 'CONTROL-PASS' if all(unseeded) else 'UNDERPOWERED'
        save()
        if paired:
            from controls import symmetric_planes
            units = paired_formulas()
            if resume and not grid:
                prior = json.loads((resume / 'summary.json').read_text())
                report['targets'] = prior['targets']
                for log in resume.glob('map*.solver.log'):
                    name = log.name.removesuffix('.solver.log')
                    if name not in report['targets']:
                        report['targets'][name] = dict(status='INTERRUPTED', ended_by='panel_correction',
                                                      map_index=int(name.split('_')[0][3:]))
                for r in report['targets'].values():
                    r['artifact_dir'] = str(resume)
            # Rebuild/replay the completed small-case evidence; no new target solve.
            from test_pilot import EvidenceTests
            EvidenceTests('test_saved_evidence').test_saved_evidence()
            report['controls']['eight_face_evidence'] = 'REPLAY-PASS'
            EncoderTests('test_one_sided_parallel_pairing_is_rejected').test_one_sided_parallel_pairing_is_rejected()
            report['controls']['malformed_pairing'] = 'REJECTED'
            from omsat_validate import eval_all, compare_direct
            import random
            rng = random.Random(261104)
            while True:
                h = [[rng.randint(-100, 100) for _ in range(4)] for _ in range(9)]
                chi = chirotope_from_planes(h)
                if all(chi.values()):
                    break
            t = from_links(units[0][1]['links'])
            _, ev = eval_all(h, t)
            stats = {}; mismatches, embedded, simple = compare_direct(h, t, ev, stats)
            assert not mismatches, mismatches
            c = CNF(9); c.defs_only = True; build(c, t, ALL_OPTS)
            c.gp()
            c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()])
            dump(out / 'nine_plane_control.input.json', dict(planes=h, seed=261104, stats=stats))
            r = solve(c, out, 'nine_plane_control', remaining(60, control_deadline) / 2)
            report['controls']['nine_plane_control'] = r; save()
            assert r['status'] == 'SAT', r
            i, rec, p = units[0]
            group = sorted(closure([p], 9))
            for seed in range(100):
                h = symmetric_planes(p, 3, seed)
                chi = chirotope_from_planes(h)
                if all(chi.values()):
                    break
            else:
                raise AssertionError('no uniform C3 control')
            c, _, _ = build_sym(from_links(rec['links']), group, {g: 1 for g in group},
                                dict(gp=True, triples=False), mirror=False, orbfix=False)
            c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()])
            dump(out / 'C3_control.input.json', dict(planes=h, permutation=p, seed=seed))
            r = solve(c, out, 'C3_control', remaining(30, control_deadline) / 2)
            report['controls']['C3_control'] = r; save()
            assert r['status'] == 'SAT', r
        else:
            units = [(i, rec, free_c2(rec['links']) if sym else None)
                     for i, rec in enumerate(census(8, 2)['maps']) for sym in (False, True)]
        if controls_only:
            report['status'] = 'CONTROLS-PASS'; save(); return
        if grid:
            baseline_path = HERE / 'results/paired_9_3_continued/summary.json'
            report['baseline'] = dict(path=str(baseline_path), sha256=sha(baseline_path),
                                      maps=[0, 1, 40, 48], reused_sixty_second_cells=[40, 48])
            units = grid_units()
        else:
            units = [(i, rec, p, 60) for i, rec, p in units]
        decided = set()
        # Solve every formula before spending the residual budget on model processing.
        formulas = {}
        for i, rec, p, cap in units:
            if grid and i in decided:
                continue
            mode = ('C3' if paired else 'C2') if p is not None else 'plain'
            name = f'map{i}_{mode}' + (f'_t{cap}' if grid else '')
            if name in report['targets']:
                continue
            t = from_links(rec['links']); dump(out / f'map{i}.json', rec)
            dump(out / f'map{i}.identity.json', dict(canonical_sha256=hashlib.sha256(json.dumps(rec['code'], separators=(',', ':')).encode()).hexdigest(), group=sorted(closure([p], t.n)) if p is not None else []))
            if p is not None:
                group = sorted(closure([p], t.n))
                c, _, _ = build_sym(t, group, {g: 1 for g in group}, ALL_OPTS)
            else:
                c = CNF(t.n); build(c, t, ALL_OPTS)
            r = solve(c, out, name, remaining(cap, deadline - 360) if grid else remaining(120) / 2)
            r.update(scope=f'uniform free-{mode} ansatz' if p is not None else 'plain embedding formula',
                     map_index=i, permutation=p)
            if grid:
                r['cutoff_seconds'] = cap
                r['formula_sha256'] = hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest()
                if r['status'] in ('SAT', 'UNSAT-VERIFIED'):
                    decided.add(i)
            report['targets'][name] = r
            if r['status'] == 'SAT':
                formulas[name] = (c, rec)
            save(); print(name, r['status'], round(r['seconds'], 2), flush=True)
            if r['status'] in ('ERROR', 'UNSAT-UNCHECKED'):
                raise RuntimeError((name, r))
            if paired and r['status'] == 'SAT':
                break
        for name, (c, rec) in formulas.items():
            if report['targets'][name]['status'] != 'SAT':
                continue
            model = set(json.loads((out / (name + '.model.json')).read_text()))
            chi = {q: 1 if v in model else -1 for q, v in c.qvar.items()}
            inp = payload(chi, rec['links']); results = {}
            report['targets'][name]['processing'] = results
            for task in ('hinge', 'two_stage', 'fp'):
                result = stage(out, name + '_' + task, task, inp, remaining(120))
                results[task] = result; save()
                if result.get('geometry', {}).get('EMBEDDED'):
                    dump(out / (name + '.candidate.json'), dict(planes=result['planes'], links=dict(enumerate(rec['links']))))
                    report['status'] = 'CANDIDATE'; save(); return
        report['status'] = 'FIRST-SAT-PROCESSED' if paired and formulas else 'PILOT-COMPLETE'
    except TimeoutError as exc:
        report.update(status='PILOT-TIMEOUT', error=str(exc))
    except BaseException as exc:
        report.update(status='ERROR', error=repr(exc))
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        save()
        manifest.update(status=report['status'], ended_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        manifest['outputs_sha256'] = {p.name: sha(p) for p in out.iterdir() if p.is_file() and p.name != 'manifest.json'}
        manifest['sources_sha256'] = {str(p.relative_to(ROOT)): sha(p) for p in
                                      [Path(__file__).resolve(), ROOT / 'code/omsat.py', ROOT / 'code/omsat_geom.py', ROOT / 'code/omsat_sym.py']}
        manifest['wall_seconds'] = time.monotonic() - start
        manifest['core_hours'] = manifest['wall_seconds'] / 3600
        manifest['inputs_sha256'] = {'maps': sha(ROOT / ('experiments/E-261103-01-s5-map-census/results/maps_9_3.json' if paired else 'experiments/E-261103-01-s5-map-census/results/maps_8_2.json'))}
        dump(out / 'manifest.json', manifest)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path)
    ap.add_argument('--paired', action='store_true')
    ap.add_argument('--grid', action='store_true')
    ap.add_argument('--resume', type=Path)
    ap.add_argument('--controls-only', action='store_true')
    ap.add_argument('--task', choices=('hinge', 'two_stage', 'fp'))
    ap.add_argument('--input', type=Path); ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.task:
        worker(args)
    else:
        assert args.out is not None
        main(args.out, paired=args.paired or args.grid or args.controls_only, resume=args.resume,
             grid=args.grid, controls_only=args.controls_only)
