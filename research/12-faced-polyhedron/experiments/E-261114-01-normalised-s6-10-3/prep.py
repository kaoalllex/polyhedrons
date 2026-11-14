"""Ten-shard known-negative gate and bounded S6 pilot, after the positive gates."""
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import controls as local
from controls import pilot, ROOT, HERE, topology
import tranche

MONO = {96: (1073.49, '859f21a94e6d9b02888a98059a96d643d9a7460f3b86f64f12291b4c08e29df0'),
        85: (2748.86, 'd89b0f3d42407482c58a5c15a9c0382b0f84cde1c3d5f5214dce696b6472aed0'),
        845: (188.38, '7b125e1c3862dd80209e5725a1e096cc6b4c38802d9dd45b63c9911a5aedd025')}


def shard(args):
    k, out, jobs = args
    dest = out / str(k); dest.mkdir(parents=True)
    rows = []; started = time.monotonic()
    for name, t, reference, target in jobs:
        c = pilot.CNF(t.n); pilot.build(c, t, dict(pilot.ALL_OPTS, symbreak=True, mirror=True))
        r = dict(name=name, **pilot.solve(c, dest, name, 1200))
        if reference:
            seconds, digest, index = reference
            plain = pilot.CNF(t.n); pilot.build(plain, t, pilot.ALL_OPTS)
            p = dest / 'baseline.cnf'
            plain.dimacs(p, comments=[f'map{index}_plain', 'S5 pilot; interpret symmetry and model scope separately'])
            r['baseline_hash_matches'] = pilot.sha(p) == digest; p.unlink()
            if not r['baseline_hash_matches']:
                raise AssertionError('baseline hash mismatch')
            r['baseline_seconds'] = seconds
            r['speedup'] = seconds / r['seconds'] if r['status'] == 'UNSAT-SOLVER' else None
        if target and r['status'] == 'SAT':
            r.update(tranche.bridge(dest, name, c, t.link, 'S6'))
        rows.append(r); pilot.dump(dest / 'results.json', rows)
        if not target and r['status'] != 'UNSAT-SOLVER':
            break
    u = resource.getrusage(resource.RUSAGE_SELF); ch = resource.getrusage(resource.RUSAGE_CHILDREN)
    pilot.dump(dest/'manifest.json', dict(shard=k, wall_seconds=time.monotonic()-started,
               cpu_seconds=u.ru_utime+u.ru_stime+ch.ru_utime+ch.ru_stime,
               commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
               dirty=True, python=sys.version, solver_sha256=pilot.sha(Path(pilot.CADICAL))))
    return rows


def main(mode, out):
    for gate in ('invariance', 'positive') + (('negative',) if mode == 'pilot' else ()):
        assert json.loads((HERE/'results'/gate/'summary.json').read_text())['PASS'], gate
    jobs = []
    if mode == 'negative':
        for f,g in ((8,2),(9,3)):
            for i,m in enumerate(pilot.census(f,g)['maps']):
                if m['admissible']:
                    jobs.append((f'f{f}_map{i}',pilot.from_links(m['links']),None,False))
        assert len(jobs)==205, len(jobs)
        for i,(seconds,digest) in MONO.items():
            jobs.append((f'f10_map{i}',pilot.from_links(pilot.census(10,4)['maps'][i]['links']),
                         (seconds,digest,i),False))
    elif mode == 'pilot':
        p = ROOT/'experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json'
        data=json.loads(p.read_text())['maps']
        for m in data[:2]:
            jobs.append((f"lutz{m['lutz']}",topology(m['links']),None,True))
    else:
        raise ValueError(mode)
    out.mkdir(parents=True,exist_ok=False)
    with ProcessPoolExecutor(10) as pool:
        rows=sum(pool.map(shard,[(k,out,jobs[k::10]) for k in range(10)]),[])
    passed=len(rows)==len(jobs) and all(r['status']=='UNSAT-SOLVER' for r in rows)
    result=dict(PASS=passed,mode=mode,expected=len(jobs),completed=len(rows),
                statuses={s:sum(r['status']==s for r in rows) for s in ('SAT','UNSAT-SOLVER','TIMEOUT','ERROR')},
                inputs_sha256={str(p.relative_to(ROOT)):pilot.sha(p) for p in
                               (Path(__file__),Path(local.__file__),ROOT/'code/omsat.py',Path(pilot.__file__))})
    if mode=='pilot':
        result['day_gate']=len(rows)==2 and all(r['status'] in ('SAT','UNSAT-SOLVER','TIMEOUT') for r in rows) and any(r['status']!='TIMEOUT' for r in rows)
    pilot.dump(out/'summary.json',result);print(json.dumps(result))
    return 0 if passed or (mode=='pilot' and len(rows)==2) else 1


if __name__=='__main__':
    sys.exit(main(sys.argv[1],Path(sys.argv[2])))
