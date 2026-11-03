"""Bounded S5 decision pilot. Each negative claim is scoped to its saved formula."""
import argparse
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
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder'))
sys.path.insert(0, str(ROOT / 'experiments/E-261101-25-chirotope-first'))
from test_encoder import controls, from_links, EncoderTests
from omsat import CNF, build, chirotope_from_planes
from omsat_validate import ALL_OPTS
from omsat_sym import build_sym
from ladder_exact import verify

CADICAL = os.environ.get('CADICAL', str(Path.home() / 'bin/cadical'))
DRAT = os.environ.get('DRAT_TRIM', str(Path.home() / 'bin/drat-trim'))


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def command(args, log, timeout):
    with log.open('w') as stream:
        p = subprocess.Popen(args, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            return p.wait(timeout=max(.001, timeout))
        except BaseException as exc:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            if not isinstance(exc, subprocess.TimeoutExpired):
                raise
            return None


def model_valid(clauses, model):
    values = set(model)
    return not any(-v in values for v in values) and all(any(v in values for v in cl) for cl in clauses)


def check_proof(cnf, proof, log, timeout):
    rc = command([DRAT, str(cnf), str(proof)], log, timeout)
    return rc == 0 and 's VERIFIED' in log.read_text()


def solve(c, out, name, timeout):
    cnf = out / (name + '.cnf'); proof = out / (name + '.drat')
    c.dimacs(cnf, comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
    started = time.monotonic()
    rc = command([CADICAL, str(cnf), str(proof)], out / (name + '.solver.log'), timeout)
    elapsed = time.monotonic() - started
    r = dict(status='TIMEOUT' if rc is None else 'ERROR', seconds=elapsed, budget_seconds=timeout,
             budget_fraction=elapsed / timeout, ended_by='solver_timeout' if rc is None else 'completed',
             variables=c.nv, clauses=len(c.clauses), cnf_sha256=sha(cnf))
    if rc == 10:
        model = [int(v) for line in (out / (name + '.solver.log')).read_text().splitlines()
                 if line.startswith('v ') for v in line[2:].split() if int(v)]
        assert model_valid(c.clauses, model), 'invalid SAT assignment'
        dump(out / (name + '.model.json'), model)
        r.update(status='SAT', model_checked=True)
    elif rc == 20:
        # Checking has its own bounded allocation; the caller bounds the whole unit too.
        ok = check_proof(cnf, proof, out / (name + '.checker.log'), timeout)
        r.update(status='UNSAT-VERIFIED' if ok else 'UNSAT-UNCHECKED')
    if proof.exists():
        r['proof_sha256'] = sha(proof)
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
        planes, bad = fn(chi, len(data['links']), start_planes=data.get('start_planes'),
                         restarts=2 if args.task == 'two_stage' and data.get('start_planes') is not None else 1,
                         rng=np.random.default_rng(26110303))
        match = reconstruction_ok(bad, planes is not None and chirotope_from_planes(planes) == chi)
        result = dict(wrong_signs=bad, signs_match=match)
        if match:
            result['geometry'] = verify(planes, dict(enumerate(data['links'])))
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


def payload(chi, links, start=None):
    return dict(chi={','.join(map(str, k)): v for k, v in chi.items()}, links=links, start_planes=start)


def arm_deadline(seconds):
    def expired(signum, frame):
        raise TimeoutError("pilot computation deadline exhausted")
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)


def main(out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); deadline = start + 900; control_deadline = start + 480
    report = dict(status='RUNNING', controls={}, targets={})
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
                    python=sys.version, host=platform.platform(), started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                    workers=1, wall_budget_seconds=900)
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
        assert r['status'] == 'UNSAT-VERIFIED', r
        EncoderTests('test_all_nonadmissible_census_maps_are_rejected_without_geometry').test_all_nonadmissible_census_maps_are_rejected_without_geometry()
        report['controls']['inadmissible_maps'] = 'REJECTED'
        report['construction_power'] = 'CONTROL-PASS' if all(unseeded) else 'UNDERPOWERED'
        save()
        # Solve every formula before spending the residual budget on model processing.
        formulas = {}
        for i, rec in enumerate(census(8, 2)['maps']):
            t = from_links(rec['links']); dump(out / f'map{i}.json', rec)
            for symmetric in (False, True):
                name = f'map{i}_{"C2" if symmetric else "plain"}'
                if symmetric:
                    p = free_c2(rec['links']); identity = tuple(range(8)); group = [identity, p]
                    c, _, _ = build_sym(t, group, {g: 1 for g in group}, ALL_OPTS)
                else:
                    c = CNF(8); build(c, t, ALL_OPTS)
                # Allow a full solver interval and a proof-check interval within the hard cap.
                r = solve(c, out, name, remaining(120) / 2)
                r['scope'] = 'uniform free-C2 ansatz' if symmetric else 'plain embedding formula'
                report['targets'][name] = r; formulas[name] = (c, rec)
                save(); print(name, r['status'], round(r['seconds'], 2), flush=True)
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
        report['status'] = 'PILOT-COMPLETE'
    except TimeoutError as exc:
        report.update(status='PILOT-TIMEOUT', error=str(exc))
    except BaseException as exc:
        report.update(status='ERROR', error=repr(exc))
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        save()
        manifest.update(wall_seconds=time.monotonic() - start, status=report['status'])
        manifest['core_hours'] = manifest['wall_seconds'] / 3600
        manifest['outputs_sha256'] = {p.name: sha(p) for p in out.iterdir() if p.is_file() and p.name != 'manifest.json'}
        manifest['sources_sha256'] = {str(p.relative_to(ROOT)): sha(p) for p in
                                      [Path(__file__).resolve(), ROOT / 'code/omsat.py', ROOT / 'code/omsat_geom.py', ROOT / 'code/omsat_sym.py']}
        dump(out / 'manifest.json', manifest)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path)
    ap.add_argument('--task', choices=('hinge', 'two_stage', 'fp'))
    ap.add_argument('--input', type=Path); ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if args.task:
        worker(args)
    else:
        assert args.out is not None
        main(args.out)
