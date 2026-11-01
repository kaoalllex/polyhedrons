"""Chirotope-first realization (E-261101-25).

Algorithm v2 of the construction side. Instead of optimising intersection counts in geometry, the search runs in the
space of oriented matroids, where "embedded" is a logical constraint (FD2), and geometry enters twice: as the SEED
(the rank-3 signs of a plane set are passed to the SAT solver as assumptions, FD8: with the normals fixed the rest is
linear) and as the REALIZATION of a model (hinge-loss descent on the 715 signed determinants, then exact rounding and
`ladder_exact.verify`). When the assumptions are inconsistent with embedding, the solver's UNSAT CORE names the normal
signs that must change (core-guided relaxation, as in MaxSAT); when a model is not realizable the whole rank-3 part
is blocked (CEGAR; biquadratic final polynomials would give sharper cuts, not implemented here).

Modes
  control-szilassi   n = 7: random seed planes -> assumptions -> core-guided SAT -> realize -> exact EMBEDDED
  control-realizer   realize the exact chirotope of a known configuration from a random start (realizer only)
  run                n = 12: one type, seed planes from files (class seeds, witnesses) or random, optional face ladder

Usage: python3 chirotope_first.py MODE [--type 0] [--seeds FILE ...] [--out results.jsonl] [--timeout 120]
                                        [--rounds 40] [--ladder 7] [--realize-restarts 6]
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os
import random
import sys
import time

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'code'))
import omsat                                                     # noqa: E402
from omsat import CNF, Triangulation, Predicates, chirotope_from_planes, perm_parity   # noqa: E402
import ladder_exact                                              # noqa: E402

FULL_OPTS = dict(gp=True, triples=True, reflex=True, poc=True, symbreak=True, mirror=True)
SCALE = 10 ** 9


# ----------------------------------------------------------------------------- encoding (face-restricted copy of omsat.build)

def build_faces(C, T, faces=None, opts=FULL_OPTS):
    """omsat.build with the local clause families restricted to `faces` (None = all): TRIPLE for non-triangles
    inside the set, REFLEX1 for triangles inside the set, POC for faces in the set. GP and the normalisations are
    unchanged. With faces = all faces the formula equals omsat.build's (checked in the pilot)."""
    n = T.n
    faces = set(range(n)) if faces is None else set(faces)
    o = dict(omsat.DEFAULT_OPTS)
    o.update(opts)
    P = Predicates(C, T)
    if o['gp']:
        C.gp()
    nt = T.nontriangles()
    if o['triples']:
        for X, Y, Z in nt:
            if X in faces and Y in faces and Z in faces:
                a = C.name(('IN', X, Y, Z), P.IN(X, Y, Z))
                b = C.name(('IN', Y, Z, X), P.IN(Y, Z, X))
                c = C.name(('IN', Z, X, Y), P.IN(Z, X, Y))
                C.clause([C.NOT(a), C.NOT(b), C.NOT(c)], 'TRIPLE')
    if o['reflex'] or o['poc']:
        for X in range(n):
            if X in faces:
                for A, Bv in T.corners(X):
                    C.name(('RF', X, A, Bv), P.REFLEX(X, A, Bv))
                    C.name(('RF', X, Bv, A), P.REFLEX(X, Bv, A))
                    C.name(('RT', X, A, Bv), P.RTURN(X, A, Bv))
    if o['reflex']:
        for t in T.tris:
            X, Y, Z = t
            if X in faces and Y in faces and Z in faces:
                r = [P.REFLEX(X, Y, Z), P.REFLEX(Y, Z, X), P.REFLEX(Z, X, Y)]
                for i, j in itertools.combinations(range(3), 2):
                    C.clause([C.NOT(r[i]), C.NOT(r[j])], 'REFLEX1')
    if o['poc']:
        for X in range(n):
            if X in faces:
                cs = T.corners(X)
                w = [C.xor([P.RTURN(X, A, Bv), P.REFLEX(X, A, Bv)]) for A, Bv in cs]
                for i in range(1, len(w)):
                    C.equiv(w[0], w[i], 'POC')
    if o['symbreak']:
        INF = n
        fixed = [(0, 1, k, INF) for k in range(2, n)] + [(0, 2, 3, INF), (1, 2, 3, INF)]
        for S in fixed:
            C.clause([C.NOT(C.chi_neg(S))], 'SB_REORIENT')
        if o['mirror']:
            C.clause([C.NOT(C.chi_neg((0, 1, 2, 3)))], 'SB_MIRROR')
    return P


# ----------------------------------------------------------------------------- geometry helpers

def to_int(planes):
    return [[int(round(float(x) * SCALE)) for x in h] for h in planes]


def normalise(planes_int, n):
    """Reorient the planes (h -> -h) so that chi(0,1,k,INF) = chi(0,2,3,INF) = chi(1,2,3,INF) = +1 (the GF(2) system
    has exactly one solution), then reflect space (x -> -x) if chi(0,1,2,3) = -1. Both keep embeddedness."""
    INF = n
    for attempt in range(2):
        chi = chirotope_from_planes(planes_int)
        ck = {k: chi[(0, 1, k, INF)] for k in range(2, n)}
        if any(v == 0 for v in ck.values()) or chi[(0, 2, 3, INF)] == 0 or chi[(1, 2, 3, INF)] == 0:
            raise ValueError('degenerate seed: a normalisation quadruple is zero')
        e0 = ck[2] * ck[3] * chi[(0, 2, 3, INF)]
        e1 = ck[2] * ck[3] * chi[(1, 2, 3, INF)]
        eps = [e0, e1] + [e0 * e1 * ck[k] for k in range(2, n)]
        planes_int = [[e * x for x in h] for e, h in zip(eps, planes_int)]
        chi = chirotope_from_planes(planes_int)
        assert all(chi[(0, 1, k, INF)] == 1 for k in range(2, n)) and chi[(0, 2, 3, INF)] == 1 and chi[(1, 2, 3, INF)] == 1
        if chi[(0, 1, 2, 3)] == 1:
            return planes_int, attempt
        if chi[(0, 1, 2, 3)] == 0:
            raise ValueError('degenerate seed: chi(0,1,2,3) = 0')
        planes_int = [[-h[0], h[1], h[2], h[3]] for h in planes_int]       # mirror x -> -x
    raise RuntimeError('normalisation failed')


def rank3_quads(n):
    return [S for S in itertools.combinations(range(n + 1), 4) if n in S]


def lits_from_chi(C, chi, quads):
    out = []
    for S in quads:
        v = chi[S]
        if v:
            out.append(C.qvar[S] if v > 0 else -C.qvar[S])
    return out


# ----------------------------------------------------------------------------- SAT with timeout and cores

def _solve_child(clauses, assumptions, nchi, q):
    from pysat.solvers import Solver
    with Solver(name='cadical195', bootstrap_with=clauses) as s:
        t0 = time.time()
        r = s.solve(assumptions=assumptions)
        out = {'status': 'SAT' if r else 'UNSAT', 'seconds': time.time() - t0}
        if r:
            out['model_pos'] = [l for l in s.get_model()[:nchi + 1] if l > 0]
        else:
            out['core'] = list(s.get_core() or [])
    q.put(out)


def _maxsat_child(clauses, soft, nchi, q):
    from pysat.formula import WCNF
    from pysat.examples.rc2 import RC2
    w = WCNF()
    for c in clauses:
        w.append(c)
    for lit in soft:
        w.append([lit], weight=1)
    t0 = time.time()
    try:
        rc2 = RC2(w, solver='cd19', adapt=True, exhaust=True, minz=True)
    except Exception:
        rc2 = RC2(w, adapt=True, exhaust=True, minz=True)
    m = rc2.compute()
    out = {'status': 'SAT' if m is not None else 'UNSAT', 'seconds': time.time() - t0}
    if m is not None:
        out['model_pos'] = [l for l in m[:nchi + 1] if l > 0]
        out['cost'] = rc2.cost
    q.put(out)


def _lsu_child(clauses, soft, nchi, timeout, q):
    """Anytime MaxSAT (linear SAT-UNSAT search): returns the best model found before the timeout."""
    import threading
    from pysat.formula import WCNF
    from pysat.examples.lsu import LSU
    w = WCNF()
    for c in clauses:
        w.append(c)
    for lit in soft:
        w.append([lit], weight=1)
    t0 = time.time()
    lsu = LSU(w, solver='cd19', expect_interrupt=True)
    timer = threading.Timer(max(1.0, timeout - 3.0), lsu.interrupt)
    timer.start()
    try:
        ok = lsu.solve()
    finally:
        timer.cancel()
    out = {'status': 'SAT' if ok else 'UNSAT', 'seconds': time.time() - t0, 'optimum': bool(ok and lsu.found_optimum())}
    if ok:
        m = lsu.get_model()
        out['model_pos'] = [l for l in m[:nchi + 1] if l > 0]
        out['cost'] = lsu.cost
    q.put(out)


def lsu_maxsat(clauses, soft, nchi, timeout):
    ctx = mp.get_context('fork')
    q = ctx.Queue()
    p = ctx.Process(target=_lsu_child, args=(clauses, soft, nchi, timeout, q), daemon=True)
    t0 = time.time()
    p.start()
    p.join(timeout + 30)
    if p.is_alive():
        p.terminate(); p.join()
        return {'status': 'TIMEOUT', 'seconds': time.time() - t0}
    try:
        return q.get(timeout=5)
    except Exception:
        return {'status': 'ERROR', 'seconds': time.time() - t0}


def maxsat(clauses, soft, nchi, timeout):
    ctx = mp.get_context('fork')
    q = ctx.Queue()
    p = ctx.Process(target=_maxsat_child, args=(clauses, soft, nchi, q), daemon=True)
    t0 = time.time()
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate(); p.join()
        return {'status': 'TIMEOUT', 'seconds': time.time() - t0}
    try:
        return q.get(timeout=5)
    except Exception:
        return {'status': 'ERROR', 'seconds': time.time() - t0}


def solve(clauses, assumptions, nchi, timeout):
    ctx = mp.get_context('fork')
    q = ctx.Queue()
    p = ctx.Process(target=_solve_child, args=(clauses, assumptions, nchi, q), daemon=True)
    t0 = time.time()
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return {'status': 'TIMEOUT', 'seconds': time.time() - t0}
    try:
        return q.get(timeout=5)
    except Exception:
        return {'status': 'ERROR', 'seconds': time.time() - t0}


def model_chi(C, model_pos, n):
    pos = set(model_pos)
    return {S: (1 if C.qvar[S] in pos else -1) for S in itertools.combinations(range(n + 1), 4)}


def core_guided(C, clauses, assumptions, n, timeout, max_rounds, log, readd=0, readd_timeout=20):
    """Release the assumptions named by each UNSAT core until SAT, TIMEOUT or no assumptions left. After SAT, try to
    re-add up to `readd` released literals one at a time (keeping those that stay SAT), so the model changes as few
    signs of the seed as possible."""
    A = list(assumptions)
    released = []
    history = []
    for rnd in range(max_rounds):
        r = solve(clauses, A, C.nv if hasattr(C, 'nv') else 0, timeout)
        history.append({'round': rnd, 'assumptions': len(A), 'status': r['status'], 'seconds': round(r.get('seconds', 0), 1),
                        'core': len(r.get('core', []))})
        log('  round %d: %d assumptions -> %s in %.1fs%s' % (rnd, len(A), r['status'], r.get('seconds', 0),
            (', core %d' % len(r['core'])) if r['status'] == 'UNSAT' else ''))
        if r['status'] == 'SAT':
            model = r['model_pos']
            if readd and released:
                kept = 0
                for lit in list(released)[:readd]:
                    r2 = solve(clauses, A + [lit], C.nv, readd_timeout)
                    if r2['status'] == 'SAT':
                        A.append(lit); released.remove(lit); model = r2['model_pos']; kept += 1
                history.append({'round': rnd, 'readd_tried': min(readd, len(released) + kept), 'readd_kept': kept})
                log('  re-add: kept %d released literals; %d assumptions now' % (kept, len(A)))
            return 'SAT', model_chi(C, model, n), released, history
        if r['status'] != 'UNSAT':
            return r['status'], None, released, history
        core = set(r['core'])
        if not core:
            return 'UNSAT-NOASSUMPTIONS', None, released, history       # the instance itself is UNSAT
        A = [a for a in A if a not in core]
        released += sorted(core)
        if not A:
            r = solve(clauses, [], C.nv, timeout)
            history.append({'round': rnd + 1, 'assumptions': 0, 'status': r['status'], 'seconds': round(r.get('seconds', 0), 1)})
            if r['status'] == 'SAT':
                return 'SAT', model_chi(C, r['model_pos'], n), released, history
            return r['status'], None, released, history
    return 'ROUNDS', None, released, history


# ----------------------------------------------------------------------------- realization of a chirotope

def _cofactors(M):
    """M: (Q,4,4). Returns (Q,4,4) array K with K[q,r,i] = d det(M_q) / d M_q[r,i]."""
    Q = M.shape[0]
    K = np.empty_like(M)
    rows = np.arange(4)
    for r in range(4):
        rr = [x for x in rows if x != r]
        for i in range(4):
            cc = [x for x in rows if x != i]
            minor = M[:, rr][:, :, cc]
            K[:, r, i] = ((-1) ** (r + i)) * np.linalg.det(minor)
    return K


class Realizer:
    def __init__(self, n, chi, margin=0.05, wnorm=0.1):
        self.n = n
        self.quads = [S for S in itertools.combinations(range(n + 1), 4) if chi[S] != 0]
        self.sign = np.array([chi[S] for S in self.quads], float)
        self.idx = np.array(self.quads)                     # (Q,4) element indices, n = INF
        self.margin = margin
        self.wnorm = wnorm

    def rows(self, x):
        H = np.vstack([x.reshape(self.n, 4), np.array([[0, 0, 0, 1.0]])])
        return H

    def loss_grad(self, x):
        H = self.rows(x)
        M = H[self.idx]                                      # (Q,4,4)
        det = np.linalg.det(M)
        norms = np.linalg.norm(M, axis=2)                    # (Q,4)
        s = norms.prod(axis=1)
        f = self.sign * det / s
        viol = np.maximum(0.0, self.margin - f)
        loss = float((viol ** 2).sum())
        K = _cofactors(M)                                    # d det / d rows
        # d f / d row_r = sign/s * (K_r - det * row_r / |row_r|^2)
        dfd = (self.sign / s)[:, None, None] * (K - (det[:, None] / norms ** 2)[:, :, None] * M)
        g_rows = (-2 * viol)[:, None, None] * dfd            # (Q,4,4)
        G = np.zeros_like(H)
        np.add.at(G, self.idx, g_rows)
        G = G[:self.n]
        # keep |h_X| near 1
        hn = np.linalg.norm(H[:self.n], axis=1)
        loss += self.wnorm * float(((hn ** 2 - 1) ** 2).sum())
        G += self.wnorm * (4 * (hn ** 2 - 1))[:, None] * H[:self.n]
        return loss, G.ravel()

    def fit(self, x0, maxiter=3000):
        res = minimize(self.loss_grad, x0, jac=True, method='L-BFGS-B', options={'maxiter': maxiter, 'maxfun': maxiter * 2})
        return res.x, res.fun

    def check_exact(self, x):
        planes = to_int(x.reshape(self.n, 4))
        chi = chirotope_from_planes(planes)
        bad = [S for S, sgn in zip(self.quads, self.sign) if chi[S] != sgn]
        return planes, bad


def realize(chi, n, start_planes=None, restarts=6, rng=None, log=print, margin=0.05):
    rng = rng or np.random.default_rng(0)
    R = Realizer(n, chi, margin=margin)
    best = None
    for k in range(restarts):
        if start_planes is not None and k == 0:
            x0 = np.array(start_planes, float).ravel()
            x0 = (x0.reshape(n, 4) / np.linalg.norm(x0.reshape(n, 4), axis=1)[:, None]).ravel()
        elif start_planes is not None and k < restarts - 1:
            x0 = (np.array(start_planes, float) / np.linalg.norm(np.array(start_planes, float), axis=1)[:, None]).ravel()
            x0 = x0 + rng.normal(scale=0.05 * k, size=x0.shape)
        else:
            x0 = rng.normal(size=4 * n)
        t0 = time.time()
        x, fval = R.fit(x0)
        planes, bad = R.check_exact(x)
        log('  realize restart %d: loss %.3g, %d/%d signs wrong, %.1fs' % (k, fval, len(bad), len(R.quads), time.time() - t0))
        if best is None or len(bad) < best[1]:
            best = (planes, len(bad), fval)
        if not bad:
            return planes, 0
    return best[0], best[1]


# ----------------------------------------------------------------------------- drivers

def load_type(tid):
    types = omsat.load_types(os.path.join(ROOT, 'data', 'k12_triangulations.json'))
    for i, T, e in types:
        if int(i) == int(tid):
            return T, e
    raise KeyError(tid)


def exact_verify(planes_int, T):
    links = {X: list(T.link[X]) for X in range(T.n)}
    r = ladder_exact.verify(planes_int, links, require_all_pairs=True)
    return bool(r['EMBEDDED']), {k: r[k] for k in r if k in ('all_pairs_adjacent', 'points_distinct', 'corner_triples_distinct', 'nonsimple_faces', 'bad_pairs')}


def random_planes(n, rng):
    N = rng.normal(size=(n, 3))
    N /= np.linalg.norm(N, axis=1)[:, None]
    d = rng.uniform(-1, 1, size=(n, 1))
    return np.hstack([N, d])


def one_run(T, seed_planes, args, log, tag, faces_order=None):
    n = T.n
    rec = {'tag': tag, 'n': n, 'steps': []}
    planes = to_int(seed_planes)
    planes, mirrored = normalise(planes, n)
    rec['mirrored'] = mirrored
    rng = np.random.default_rng(abs(hash(tag)) % (2 ** 32))
    ks = list(range(args.ladder, n + 1)) if (args.ladder and faces_order is not None) else [n]
    if args.kmax:
        ks = [k for k in ks if k <= args.kmax]
    for k in ks:
        faces = None if k == n else faces_order[:k]
        C = CNF(n)
        build_faces(C, T, faces)
        quads = rank3_quads(n) if args.assume == 'rank3' else list(itertools.combinations(range(n + 1), 4))
        log('[%s] k=%d faces=%s: %d vars, %d clauses' % (tag, k, 'all' if faces is None else faces, C.nv, len(C.clauses)))
        # alternating projections: (SAT model closest to the current chirotope) <-> (realizable configuration closest to the model)
        step = None
        blocks = []
        for it in range(args.alt):
            chi_seed = chirotope_from_planes(planes)
            assumptions = lits_from_chi(C, chi_seed, quads)
            t0 = time.time()
            if args.solver in ('maxsat', 'lsu'):
                r = (maxsat if args.solver == 'maxsat' else lsu_maxsat)(C.clauses, assumptions, C.nv, args.timeout)
                status = r['status']
                hist = [{'maxsat': status, 'seconds': round(r.get('seconds', 0), 1), 'cost': r.get('cost')}]
                released = list(range(r.get('cost', 0))) if status == 'SAT' else []
                chi_model = model_chi(C, r['model_pos'], n) if status == 'SAT' else None
                log('  maxsat: %s in %.1fs, flipped signs %s' % (status, r.get('seconds', 0), r.get('cost')))
            else:
                status, chi_model, released, hist = core_guided(C, C.clauses, assumptions, n, args.timeout, args.rounds, log,
                                                                readd=args.readd, readd_timeout=min(20.0, args.timeout))
            step = {'k': k, 'faces': faces, 'iteration': it, 'vars': C.nv, 'clauses': len(C.clauses), 'assumptions': len(assumptions),
                    'status': status, 'released': len(released), 'rounds': len(hist), 'sat_seconds': round(time.time() - t0, 1), 'history': hist}
            if status != 'SAT':
                rec['steps'].append(step)
                rec['result'] = status
                return rec
            planes_f, nbad = realize(chi_model, n, start_planes=planes, restarts=args.realize_restarts, rng=rng, log=log)
            step['realized_wrong_signs'] = nbad
            rec['steps'].append(step)
            log('  alternation %d: released %d, wrong signs after realization %d' % (it, len(released), nbad))
            if nbad == 0:
                planes = planes_f
                break
            if args.block:
                # the model's values on the signs it flipped relative to the seed: forbid this exact combination
                flipped = [S for S in quads if chi_seed.get(S) and chi_model[S] != chi_seed[S]]
                if flipped:
                    clause = [(-C.qvar[S] if chi_model[S] > 0 else C.qvar[S]) for S in flipped]
                    C.clauses.append(clause)
                    blocks.append(len(flipped))
                    step['blocked_flips'] = len(flipped)
                    log('  blocked a model with %d flipped signs (%d blocks so far)' % (len(flipped), len(blocks)))
            planes = planes_f
        if nbad:
            rec['result'] = 'NOT-REALIZED'
            rec['planes_best'] = planes
            return rec
        rec['planes_k%d' % k] = planes
        if faces is None:
            emb, info = exact_verify(planes, T)
            step['exact'] = info
            step['EMBEDDED'] = emb
            rec['result'] = 'EMBEDDED' if emb else 'MODEL-REALIZED-NOT-EMBEDDED'
            rec['planes'] = planes
            return rec
    rec['result'] = 'LADDER-END'
    return rec


def greedy_face_order(T):
    """Faces ordered so that each prefix spans as many triangles of T as possible."""
    n = T.n
    order = [0]
    while len(order) < n:
        best = None
        for X in range(n):
            if X in order:
                continue
            cnt = sum(1 for t in T.tris if X in t and all(y in order for y in t if y != X))
            if best is None or cnt > best[0]:
                best = (cnt, X)
        order.append(best[1])
    return order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['control-szilassi', 'control-realizer', 'run', 'count-clauses'])
    ap.add_argument('--type', type=int, default=0)
    ap.add_argument('--seeds', nargs='*', default=[])
    ap.add_argument('--random-seeds', type=int, default=0)
    ap.add_argument('--out', default=os.path.join(HERE, 'results', 'pilot.jsonl'))
    ap.add_argument('--timeout', type=float, default=120)
    ap.add_argument('--rounds', type=int, default=40)
    ap.add_argument('--ladder', type=int, default=0, help='start the face ladder at this k (0 = full instance only)')
    ap.add_argument('--realize-restarts', type=int, default=6)
    ap.add_argument('--rng', type=int, default=1)
    ap.add_argument('--assume', choices=['all', 'rank3'], default='all', help='which signs of the seed become assumptions')
    ap.add_argument('--readd', type=int, default=30, help='after SAT, try to re-add this many released literals')
    ap.add_argument('--alt', type=int, default=6, help='alternating projections per ladder step')
    ap.add_argument('--solver', choices=['core', 'maxsat', 'lsu'], default='core',
                    help='core: core-guided release + greedy re-add (minimal correction set); maxsat: exact RC2 (minimum flips, slow at n = 12); lsu: anytime MaxSAT, best model before the timeout')
    ap.add_argument('--kmax', type=int, default=0, help='stop the ladder after this k (0 = go to n)')
    ap.add_argument('--block', type=int, default=1, help='1: after a model fails to realize, forbid its exact set of flipped signs (heuristic no-good)')
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    log = lambda *a: print(time.strftime('%H:%M:%S'), *a, flush=True)
    rng = np.random.default_rng(args.rng)

    if args.mode == 'count-clauses':
        T, _ = load_type(args.type)
        C1 = CNF(12); omsat.build(C1, T, FULL_OPTS)
        C2 = CNF(12); build_faces(C2, T, None)
        log('omsat.build: %d vars %d clauses | build_faces(all): %d vars %d clauses | equal: %s' % (
            C1.nv, len(C1.clauses), C2.nv, len(C2.clauses), C1.clauses == C2.clauses))
        return

    if args.mode == 'control-szilassi':
        sz = json.load(open(os.path.join(HERE, 'szilassi_control.json')))
        T = Triangulation(7, [tuple(t) for t in sz['triangles']])
        for i in range(max(1, args.random_seeds)):
            seed = random_planes(7, rng)
            rec = one_run(T, seed, args, log, 'szilassi-random-%d' % i)
            log('RESULT', rec['result'], [ (s['status'], s['released'], s.get('EMBEDDED')) for s in rec['steps']])
            with open(args.out, 'a') as f:
                f.write(json.dumps(rec) + '\n')
        return

    if args.mode == 'control-realizer':
        for path in args.seeds:
            d = json.load(open(path))
            planes = d['planes']
            n = len(planes)
            chi = chirotope_from_planes(to_int(planes))
            zeros = sum(1 for v in chi.values() if v == 0)
            log('realizer control on %s: n=%d, %d zero quads' % (os.path.basename(path), n, zeros))
            t0 = time.time()
            pl, nbad = realize(chi, n, start_planes=None, restarts=args.realize_restarts, rng=rng, log=log)
            log('RESULT realizer: wrong signs %d, %.1fs' % (nbad, time.time() - t0))
            with open(args.out, 'a') as f:
                f.write(json.dumps({'tag': 'realizer-control', 'file': path, 'n': n, 'wrong_signs': nbad, 'seconds': time.time() - t0}) + '\n')
        return

    T, entry = load_type(args.type)
    order = greedy_face_order(T)
    seeds = []
    for path in args.seeds:
        d = json.load(open(path))
        seeds.append((os.path.basename(path), d['planes']))
    for i in range(args.random_seeds):
        seeds.append(('random-%d' % i, random_planes(12, rng).tolist()))
    for name, planes in seeds:
        rec = one_run(T, planes, args, log, 'type%d-%s' % (args.type, name), faces_order=order)
        rec['type'] = args.type
        rec['face_order'] = order
        log('RESULT', rec['result'], [(s['k'], s['status'], s['released'], s['rounds'], s.get('realized_wrong_signs')) for s in rec['steps']])
        with open(args.out, 'a') as f:
            f.write(json.dumps(rec) + '\n')


if __name__ == '__main__':
    main()
