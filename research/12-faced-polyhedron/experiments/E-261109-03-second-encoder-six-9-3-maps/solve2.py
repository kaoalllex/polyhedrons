"""Solve one enc2 formula with CaDiCaL (+DRAT, drat-trim). Usage: python3 solve2.py MAP_INDEX OUT_DIR [SOLVER_CAP] [CHECK_CAP]"""
import hashlib, json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import enc2

BIN = Path.home() / 'bin'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(e, out, name, cap, check_cap, extra=()):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    cnf, proof = out / f'{name}.cnf', out / f'{name}.drat'
    e.dimacs(cnf, extra, comment=name)
    r = dict(name=name, variables=e.nv, clauses=len(e.clauses) + len(extra), cnf_sha256=sha(cnf))
    t = time.monotonic()
    try:
        p = subprocess.run([str(BIN / 'cadical'), str(cnf), str(proof)], capture_output=True, text=True, timeout=cap)
        rc, log = p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        rc, log = None, ''
    r['solver_seconds'] = round(time.monotonic() - t, 1); r['solver_cap'] = cap
    if rc == 10:
        model = {int(v) for l in log.splitlines() if l.startswith('v ') for v in l[2:].split() if int(v)}
        sat = all(any((l in model) if l > 0 else (-l not in model) for l in c) for c in e.clauses + list(extra))
        r['status'] = 'SAT' if sat else 'SAT-MODEL-INVALID'
        (out / f'{name}.model.json').write_text(json.dumps(sorted(model)))
    elif rc == 20:
        t = time.monotonic()
        try:
            p = subprocess.run([str(BIN / 'drat-trim'), str(cnf), str(proof), '-t', str(check_cap)], capture_output=True, text=True, timeout=check_cap + 30)
            (out / f'{name}.checker.log').write_text(p.stdout)
            r['status'] = 'UNSAT-VERIFIED' if 's VERIFIED' in p.stdout else 'UNSAT-UNCHECKED'
        except subprocess.TimeoutExpired:
            r['status'] = 'UNSAT-UNCHECKED'
        r['checker_seconds'] = round(time.monotonic() - t, 1); r['proof_sha256'] = sha(proof)
    else:
        r['status'] = 'TIMEOUT' if rc is None else 'ERROR'
    cnf.unlink(missing_ok=True); proof.unlink(missing_ok=True)
    return r


if __name__ == '__main__':
    idx, out = int(sys.argv[1]), sys.argv[2]
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 1800; chk = int(sys.argv[4]) if len(sys.argv) > 4 else 1800
    m = json.loads((ROOT / 'experiments/E-261103-01-s5-map-census/results/maps_9_3.json').read_text())['maps'][idx]
    assert m['admissible']
    t = time.monotonic(); e = enc2.Enc(m['links'], gauge=True); build = round(time.monotonic() - t, 1)
    r = run(e, out, f'map{idx}', cap, chk); r['build_seconds'] = build; r['map_index'] = idx
    print(json.dumps(r)); (Path(out) / f'map{idx}.json').write_text(json.dumps(r, indent=1))
