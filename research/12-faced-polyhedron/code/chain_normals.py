"""Idea Q1 (own, 2026-10-30): CHAIN-CONSISTENT NORMALS. For a chain M0 (12-face sphere) -> M1 -> ... -> M6
(one tube per step, genus_ladder.chain) the Gauss degree obeys D_{M_{g+1}} = D_{M_g} + k_tau. Search ONE set
of 12 gauge normals (unit normals + orientation signs) that puts EVERY level in its class at once: degree
1 - g, robust positive covering and >= 2g+1 saddles for g = 0..6 (equivalently D_0 = +1 and k_tau = -1 for all
six handles). Then keep these normals FIXED and decide the offsets exactly level by level from the bottom
(fixed_normals_gauge.solve_gauge on each sub-map); the first UNSAT level is where the normals must move.
Usage: python3 -I chain_normals.py TYPE_ID ANNEAL_MINUTES SEED OUT_JSON [SMT_TIMEOUT_S]"""
import json, os, sys, time, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import coherent_triangles
from genus_ladder import chain
from normals_first import ClassEnergy
import gauss_gate as GG


def oriented_chain(maps, n=12):
    """Coherent orientations of all levels, each aligned with the level above (common triangles)."""
    out = [None] * len(maps)
    out[-1] = coherent_triangles([tuple(t) for t in maps[-1]])
    for i in range(len(maps) - 2, -1, -1):
        lo = coherent_triangles([tuple(t) for t in maps[i]])
        su = {frozenset(t): t for t in out[i + 1]}
        for t in lo:
            s = su.get(frozenset(t))
            if s is not None:
                if not any(t == s[k:] + s[:k] for k in range(3)):
                    lo = [(b, a, c) for a, b, c in lo]
                break
        out[i] = lo
    return out


def main():
    tid, minutes, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    smt_timeout = float(sys.argv[5]) if len(sys.argv) > 5 else 300
    types = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'k12_triangulations.json')))
    ent = next(e for e in types if e['id'] == tid)
    rng = np.random.default_rng(seed)
    maps = chain(ent['triangles'], 12, random.Random(seed))
    levels = oriented_chain(maps)
    genera = [GG.genus(m, 12) for m in maps]
    E = [ClassEnergy(ot, 1 - g, 2 * g + 1, 1500, rng, cover_margin=0.005) for ot, g in zip(levels, genera)]

    def energy(G):
        return sum(e(G)[0] for e in E)

    N = rng.standard_normal((12, 3)); N /= np.linalg.norm(N, axis=1)[:, None]
    eps = np.ones(12)
    cur = energy(eps[:, None] * N); best = (cur, N.copy(), eps.copy()); T = 3.0; t0 = time.monotonic(); it = 0
    while best[0] > 0 and time.monotonic() - t0 < 60 * minutes:
        it += 1
        N2, e2 = N.copy(), eps.copy(); k = int(rng.integers(12))
        if rng.random() < 0.08:
            e2[k] = -e2[k]
        else:
            N2[k] += float(rng.choice([0.01, 0.03, 0.1, 0.3])) * rng.standard_normal(3); N2[k] /= np.linalg.norm(N2[k])
        c2 = energy(e2[:, None] * N2)
        if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
            N, eps, cur = N2, e2, c2
            if cur < best[0]:
                best = (cur, N.copy(), eps.copy())
        T = max(0.05, T * 0.9995)
    rec = {'type_id': tid, 'seed': seed, 'genera': genera, 'anneal_energy': float(best[0]), 'iterations': it,
           'anneal_seconds': round(time.monotonic() - t0, 1)}
    G = best[2][:, None] * best[1]
    rec['per_level_degree'] = [E[i](G)[1] for i in range(len(E))]
    print('type %d: anneal energy %.1f after %d it (%.0f s); float degrees per level %s (targets %s)' % (
        tid, best[0], it, rec['anneal_seconds'], rec['per_level_degree'], [1 - g for g in genera]), flush=True)
    if best[0] == 0:
        Nint = [[int(round(v * GG.SCALE)) for v in x] for x in G]           # gauge normals (signs included)
        ok = []
        for ot, g in zip(levels, genera):
            adm, _ = GG.admissible(Nint, ot, 1 - g, n_cover=256, eps=[[1] * 12], n_confirm=1000)
            ok.append(bool(adm) and GG.saddles(Nint, ot, [1] * 12) >= 2 * g + 1)
        rec['exact_class_per_level'] = ok
        rec['normals'] = Nint
        print('  exact class check per level:', ok, flush=True)
        if all(ok):
            from fixed_normals_gauge import solve_gauge
            from ladder_exact import verify
            from gauss_degree import links_from
            rec['levels'] = []
            for ot, g in zip(levels, genera):
                ts = time.monotonic()
                st, Hs = solve_gauge(Nint, ot, timeout_s=smt_timeout)
                lv = {'genus': g, 'status': st, 'seconds': round(time.monotonic() - ts, 1)}
                if st == 'SAT':
                    lv['exact'] = bool(verify(Hs, links_from(ot, 12), require_all_pairs=(g == 6))['EMBEDDED'])
                    lv['planes'] = [[int(v) for v in h] for h in Hs]
                rec['levels'].append(lv)
                print('  genus %d at the fixed chain normals: %s in %.0f s%s' % (
                    g, st, lv['seconds'], (' (exact EMBEDDED %s)' % lv['exact']) if st == 'SAT' else ''), flush=True)
                json.dump(rec, open(out, 'w'))
                if st != 'SAT':
                    break
                if g == 6 and lv.get('exact'):
                    print('!!! CANDIDATE: genus 6 realized at chain-consistent normals', flush=True)
    rec['maps'] = [[list(t) for t in ot] for ot in levels]
    json.dump(rec, open(out, 'w'))


if __name__ == '__main__':
    main()
