"""Step 3(c): n=12 random arrangements: SAT / UNSAT / timeout and MaxSAT distance-to-solution."""
import sys, time, json, multiprocessing as mp
from track4_common import *

def _work(kind, H, args, conn):
    try:
        arr = Arrangement(H)
        t0 = time.time()
        if kind == "sat":
            st, tris, info = geomsat.solve_sat(arr, **args)
            conn.send(dict(status=st, tris=tris, info=info, secs=time.time() - t0))
        elif kind == "cpsat":
            c, lb, tris, st, info = geomsat.solve_cpsat(arr, **args)
            prof = violation_profile(arr, tris) if tris else None
            conn.send(dict(status="CPSAT_" + st, cost=c, lb=lb, tris=tris, info=info, profile=prof, secs=time.time() - t0))
        else:
            cost, tris, info = geomsat.solve_maxsat(arr, **args)
            prof = violation_profile(arr, tris) if tris else None
            conn.send(dict(status="OPT", cost=cost, tris=tris, info=info, profile=prof, secs=time.time() - t0))
    except Exception as e:
        import traceback
        conn.send(dict(status="ERROR", err=traceback.format_exc()))

def run_timeout(kind, H, timeout, args=None):
    a, b = mp.Pipe(False)
    p = mp.Process(target=_work, args=(kind, H, args or {}, b))
    p.start()
    t0 = time.time()
    if a.poll(timeout):
        r = a.recv()
    else:
        r = dict(status="TIMEOUT", secs=time.time() - t0)
    p.terminate(); p.join()
    return r

def batch(kind, dists, per_dist, timeout, seed, nproc=2, out=None, n=12):
    rng = random.Random(seed)
    jobs = []
    for dist in dists:
        for i in range(per_dist):
            arr = random_planes(n, dist, rng)
            jobs.append((dist, i, arr.H))
    results = []
    active = []
    def launch(job):
        dist, i, H = job
        a, b = mp.Pipe(False)
        p = mp.Process(target=_work, args=(kind, H, ({"time_limit": timeout * 0.8} if kind == "cpsat" else {}), b))
        p.start()
        return dict(job=job, p=p, conn=a, t0=time.time())
    queue = list(jobs)
    while queue or active:
        while queue and len(active) < nproc:
            active.append(launch(queue.pop(0)))
        time.sleep(0.05)
        for w in list(active):
            r = None
            if w["conn"].poll():
                r = w["conn"].recv()
            elif time.time() - w["t0"] > timeout:
                r = dict(status="TIMEOUT", secs=time.time() - w["t0"])
            if r is not None:
                w["p"].terminate(); w["p"].join(); active.remove(w)
                r["dist"], r["idx"], r["H"] = w["job"][0], w["job"][1], w["job"][2]
                results.append(r)
                s = {k: v for k, v in r.items() if k not in ("H", "tris")}
                print(json.dumps(s, default=str)[:400], flush=True)
                if out:
                    json.dump(results, open(out, "w"), default=str)
    return results

if __name__ == "__main__":
    kind, per, timeout, seed = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
    nproc = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    dists = ["sphere_unif", "tangent", "near_tangent", "gauss", "pts3", "small_off"]
    batch(kind, dists, per, timeout, seed, nproc, out=os.path.join(SCRATCH, f"n12_{kind}_{seed}.json"))
