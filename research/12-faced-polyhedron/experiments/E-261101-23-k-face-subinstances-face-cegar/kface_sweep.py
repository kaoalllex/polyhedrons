"""E-261101-23: k-face sub-instances of the asymmetric OM-SAT encoding, decided with CaDiCaL and DRAT proofs.

For a type T and k, the sub-instance keeps GP, the normalisations and the local clause families (TRIPLE, SIMPLE,
REFLEX1, POC) of the first k faces of the greedy order (I-261101-18: the face ladder is monotone, so an UNSAT here
excludes the type for every realization). SAT models are saved and realized with the E-261101-25 realizer (a realized
model is a k-face partial object of the type with simple faces in the right combinatorial class).

Usage: python3 kface_sweep.py --types 0 1 2 --ks 8 9 10 --timeouts 300 600 1200 --out results/0
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'code'))
sys.path.insert(0, os.path.join(ROOT, 'experiments', 'E-261101-25-chirotope-first'))
import numpy as np                                                   # noqa: E402
from omsat import CNF                                                # noqa: E402
import chirotope_first as CF                                         # noqa: E402

CADICAL = os.environ.get('CADICAL', os.path.expanduser('~/bin/cadical'))
DRAT_TRIM = os.environ.get('DRAT_TRIM', os.path.expanduser('~/bin/drat-trim'))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run_one(tid, k, timeout, out_dir, log, realize_restarts=6):
    T, _ = CF.load_type(tid)
    order = CF.greedy_face_order(T)
    faces = order[:k]
    C = CNF(12)
    CF.build_faces(C, T, faces, simple=True)
    base = os.path.join(out_dir, 'type%02d_k%02d' % (tid, k))
    cnf, proof = base + '.cnf', base + '.drat'
    C.dimacs(cnf, comments=['E-261101-23 k-face sub-instance type %d k %d faces %s (GP, SB, TRIPLE, SIMPLE, REFLEX1, POC on these faces)' % (tid, k, faces)])
    rec = {'type': tid, 'k': k, 'faces': faces, 'vars': C.nv, 'clauses': len(C.clauses), 'timeout': timeout,
           'cnf_sha256': sha256(cnf), 'started': time.strftime('%Y-%m-%dT%H:%M:%S')}
    t0 = time.time()
    r = subprocess.run([CADICAL, '-t', str(int(timeout)), cnf, proof], capture_output=True, text=True)
    rec['solve_seconds'] = round(time.time() - t0, 1)
    rc = r.returncode
    if rc == 20:
        rec['status'] = 'UNSAT'
        t1 = time.time()
        d = subprocess.run([DRAT_TRIM, cnf, proof], capture_output=True, text=True, timeout=max(600, 4 * timeout))
        rec['drat_trim'] = 'VERIFIED' if 's VERIFIED' in d.stdout else 'NOT-VERIFIED'
        rec['drat_trim_seconds'] = round(time.time() - t1, 1)
        rec['proof_sha256'] = sha256(proof)
        rec['proof_bytes'] = os.path.getsize(proof)
        log('type %d k %d: UNSAT in %.0fs, drat-trim %s (%.0fs, %d MB)' % (tid, k, rec['solve_seconds'], rec['drat_trim'], rec['drat_trim_seconds'], rec['proof_bytes'] >> 20))
    elif rc == 10:
        rec['status'] = 'SAT'
        pos = set()
        for line in r.stdout.splitlines():
            if line.startswith('v '):
                pos.update(int(x) for x in line[2:].split() if int(x) > 0)
        chi = CF.model_chi(C, [l for l in pos if l <= C.nv], 12)
        rec['model_chi_pos'] = sorted(l for l in pos if l <= C.nv and l in set(C.qvar.values()))
        if os.path.exists(proof):
            os.remove(proof)
        rng = np.random.default_rng(tid * 100 + k)
        t1 = time.time()
        planes, nbad = CF.realize2(chi, 12, start_planes=None, restarts=realize_restarts, rng=rng, log=log)
        if nbad:
            planes, nbad = CF.realize(chi, 12, start_planes=None, restarts=realize_restarts, rng=rng, log=log)
        rec['realized_wrong_signs'] = nbad
        rec['realize_seconds'] = round(time.time() - t1, 1)
        if nbad == 0:
            rec['planes'] = planes
            rec['partial_object'] = 'k-face model realized (chirotope matches exactly; faces in the set simple and pairwise correct by the clauses)'
        else:
            try:
                import final_polynomial as FP
                fp = FP.final_polynomial(chi, 13)
                rec['final_polynomial'] = {kk: fp[kk] for kk in fp if kk in ('status', 't_star', 'exact', 'n_relations')}
                if fp.get('status', '').startswith('NONREALIZABLE'):
                    rec['final_polynomial']['brackets'] = len(fp['brackets'])
            except Exception as e:
                rec['final_polynomial'] = {'status': 'ERROR', 'error': str(e)}
        log('type %d k %d: SAT in %.0fs, realized wrong signs %d, FP %s' % (tid, k, rec['solve_seconds'], nbad, rec.get('final_polynomial', {}).get('status', '-')))
    else:
        rec['status'] = 'TIMEOUT' if rc == 0 else 'ERROR(rc=%d)' % rc
        if os.path.exists(proof):
            os.remove(proof)
        log('type %d k %d: %s after %.0fs' % (tid, k, rec['status'], rec['solve_seconds']))
    if rec['status'] != 'UNSAT':
        os.remove(cnf)                 # keep CNFs only for certified UNSATs (the hash is recorded for all)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--types', nargs='+', type=int, required=True)
    ap.add_argument('--ks', nargs='+', type=int, default=[8, 9, 10])
    ap.add_argument('--timeouts', nargs='+', type=float, default=[300, 600, 1200])
    ap.add_argument('--out', required=True)
    ap.add_argument('--stop-at-first-unsat', type=int, default=1, help='within a type, stop increasing k after an UNSAT (larger k are UNSAT too)')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    log = lambda *a: print(time.strftime('%H:%M:%S'), *a, flush=True)
    outp = os.path.join(args.out, 'results.jsonl')
    done = set()
    unsat_types = set()
    if os.path.exists(outp):
        for line in open(outp):
            r = json.loads(line); done.add((r['type'], r['k']))
            if r.get('status') == 'UNSAT':
                unsat_types.add(r['type'])
    for tid in args.types:
        if tid in unsat_types and args.stop_at_first_unsat:
            log('type %d: an UNSAT is already recorded, larger k skipped' % tid)
            continue
        for k, to in zip(args.ks, args.timeouts):
            if (tid, k) in done:
                log('type %d k %d: already recorded, skipped' % (tid, k))
                continue
            rec = run_one(tid, k, to, args.out, log)
            with open(outp, 'a') as f:
                f.write(json.dumps(rec) + '\n')
            if rec['status'] == 'UNSAT' and args.stop_at_first_unsat:
                break


if __name__ == '__main__':
    main()
