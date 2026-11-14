"""Bounded ten-shard recovery/discovery control using the existing bridge."""
from concurrent.futures import ProcessPoolExecutor
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent/'E-261114-01-normalised-s6-10-3'))
import controls as source
from controls import pilot, topology
import tranche

for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[key]='1'


def jobs():
    out=[]
    known=[j for j in source.jobs() if j[0].startswith('realized_')]
    for name,h,t in known:
        for seed in (26110303,26110304,26110305):
            out.append((name+'_'+str(seed),'recovery',h,t,seed))
    run=ROOT/'experiments/E-261113-02-s6-10-2-calibration-rung/results/run'
    data=json.loads((run.parents[1]/'maps/seeded_formulas.json').read_text())['maps']
    realized=set()
    for p in run.glob('*/results.jsonl'):
        for line in p.read_text().splitlines():
            r=json.loads(line)
            if r.get('candidate_verify_rc')==0:
                realized.add(data[int(r['map_index'])]['lutz'])
    chosen={}
    for m in data:
        if m['lutz'] not in realized and m['lutz']!=739:
            chosen[m['lutz']]=m
    for lutz in sorted(chosen)[:5]:
        for seed in range(30):
            out.append((f'lutz{lutz}_seed{seed}','discovery',None,topology(chosen[lutz]['links']),seed))
    assert len(out)==198
    return out


def shard(args):
    k,dest,work=args; dest=dest/str(k);dest.mkdir(parents=True)
    started=time.monotonic(); deadline=started+350
    command=pilot.command
    def bounded(argv,log,timeout,gate=None):
        return command(argv,log,min(timeout,max(.001,deadline-time.monotonic())),gate)
    pilot.command=bounded
    rows=[]
    for name,arm,h,t,seed in work:
        if time.monotonic()>=deadline:
            break
        c=pilot.CNF(t.n)
        row=dict(name=name,arm=arm,seed=seed)
        if arm=='recovery':
            chi=pilot.chirotope_from_planes(h)
            from omsat import Eval
            e=Eval(t.n,chi);pilot.build(e,t,pilot.ALL_OPTS)
            assert not e.violations
            assert pilot.reconstruction_ok(0,True) and not pilot.reconstruction_ok(0,False)
            pilot.dump(dest/(name+'.model.json'),[v if chi[q]>0 else -v for q,v in c.qvar.items()])
            tranche.BRIDGE=dict(submap=True,restarts=6,optimizer_seed=seed)
            row['status']='PINNED-EXACT'
        else:
            pilot.build(c,t,dict(pilot.ALL_OPTS,symbreak=True,mirror=True))
            pilot.SOLVER_OPTS=[f'--seed={seed}']
            row.update(pilot.solve(c,dest,name,min(60,max(.001,deadline-time.monotonic()))))
            tranche.BRIDGE=dict(submap=True,restarts=6)
        if row['status'] in ('PINNED-EXACT','SAT'):
            row.update(tranche.bridge(dest,name,c,t.link,'S6'))
        row['censored']=time.monotonic()>=deadline
        rows.append(row);pilot.dump(dest/'results.json',rows)
    u=resource.getrusage(resource.RUSAGE_SELF);ch=resource.getrusage(resource.RUSAGE_CHILDREN)
    pilot.dump(dest/'manifest.json',dict(shard=k,wall_seconds=time.monotonic()-started,
               cpu_seconds=u.ru_utime+u.ru_stime+ch.ru_utime+ch.ru_stime,python=sys.version,
               commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),dirty=True))
    return rows


def main(out):
    work=jobs();out.mkdir(parents=True,exist_ok=False)
    with ProcessPoolExecutor(8) as pool:
        rows=sum(pool.map(shard,[(k,out,work[k::10]) for k in range(10)]),[])
    recovery=[r for r in rows if r['arm']=='recovery']
    complete=len(recovery)==48 and not any(r['censored'] for r in recovery)
    hits=sum(r.get('candidate_verify_rc')==0 for r in recovery)
    report=dict(recovery_completed=len(recovery),recovery_expected=48,recovered=hits,
                complete=complete,discovery_completed=sum(r['arm']=='discovery' for r in rows),
                recovery_fraction=hits/48 if complete else None,
                verdict='UNDERPOWERED' if not complete else 'ADEQUATE' if hits/48>=.8 else 'REALIZER-WORK' if hits/48<=.3 else 'INTERMEDIATE',
                sources_sha256={str(p.relative_to(ROOT)):pilot.sha(p) for p in (Path(__file__),Path(source.__file__),Path(pilot.__file__),Path(tranche.__file__))})
    pilot.dump(out/'summary.json',report);print(json.dumps(report))


if __name__=='__main__':
    main(Path(sys.argv[1]))
