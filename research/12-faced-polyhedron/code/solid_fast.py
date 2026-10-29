"""Fast (numba) evaluation of the solid-first objective, same definitions as solid_first.evaluate +
boundary_euler, on integer tables built once per arrangement. inS is a 0/1 array over bounded cells.
Returns (faces, disks, adjacency, missing, diagonal, bad_vertices, chi, runs_total)."""
import itertools
import numpy as np
import numba
import solid_first as SF


class Tables:
    def __init__(self, A):
        self.A = A
        self.cells = sorted(A.bounded); cid = {k: i for i, k in enumerate(self.cells)}
        g = lambda key: cid.get(key, -1)
        fkey = {}
        def fid(key):
            if key not in fkey:
                fkey[key] = len(fkey)
            return fkey[key]
        C4, FX, FY, PAIR, KS = [], [], [], [], []
        pairs = list(itertools.combinations(range(A.n), 2)); pidx = {p: i for i, p in enumerate(pairs)}
        for (X, Y), segs in A.ones.items():
            for k, (sv, ca, cb) in enumerate(segs):
                C4.append([g(SF._cell(sv, X, a, Y, b)) for a, b in ((1, 1), (1, -1), (-1, 1), (-1, -1))])
                FX.append([fid((X, SF._cell(sv, X, 0, Y, b))) for b in (1, -1)])
                FY.append([fid((Y, SF._cell(sv, X, a, Y, 0))) for a in (1, -1)])
                PAIR.append(pidx[(X, Y)]); KS.append(k)
        OCT, VF = [], []
        for t, p in A.P.items():
            base = list(np.sign(A.H[:, :3] @ p + A.H[:, 3]).astype(int)); row = []
            for code in range(8):
                sv = list(base)
                for q in range(3):
                    sv[t[q]] = 1 if (code >> q) & 1 else -1
                row.append(g(tuple(sv)))
            OCT.append(row)
            fl = []
            for Z in t:
                o = [w for w in t if w != Z]
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        c = list(base); c[o[0]] = s1; c[o[1]] = s2; c[Z] = 0
                        fl.append(fid((Z, tuple(c))))
            VF.append(fl)
        nf = len(fkey)
        self.nf = nf
        self.fplane = np.zeros(nf, np.int64); self.fup = np.full(nf, -1, np.int64); self.fdn = np.full(nf, -1, np.int64)
        for (Z, key), i in fkey.items():
            self.fplane[i] = Z
            up = list(key); up[Z] = 1; dn = list(key); dn[Z] = -1
            self.fup[i] = g(tuple(up)); self.fdn[i] = g(tuple(dn))
        self.C4 = np.array(C4, np.int64); self.FX = np.array(FX, np.int64); self.FY = np.array(FY, np.int64)
        self.PAIR = np.array(PAIR, np.int64); self.KS = np.array(KS, np.int64)
        self.OCT = np.array(OCT, np.int64); self.VF = np.array(VF, np.int64)
        self.n = A.n; self.npairs = len(pairs)

    def args(self):
        return (self.C4, self.FX, self.FY, self.PAIR, self.KS, self.OCT, self.VF, self.fplane, self.fup, self.fdn,
                self.n, self.npairs)


@numba.njit(cache=True)
def _find(par, a):
    while par[a] != a:
        par[a] = par[par[a]]; a = par[a]
    return a


@numba.njit(cache=True)
def fast_eval(inS, C4, FX, FY, PAIR, KS, OCT, VF, fplane, fup, fdn, n, npairs):
    nf = fplane.shape[0]; no = C4.shape[0]
    par = np.arange(nf)
    bnd = np.zeros(nf, np.bool_)
    for f in range(nf):
        a = fup[f] >= 0 and inS[fup[f]] == 1
        b = fdn[f] >= 0 and inS[fdn[f]] == 1
        bnd[f] = a != b
    diag = 0; E1 = 0
    isedge = np.zeros(no, np.bool_); ex = np.zeros(no, np.int64); ey = np.zeros(no, np.int64)
    for j in range(no):
        occ = np.zeros(4, np.bool_); cnt = 0
        for q in range(4):
            c = C4[j, q]
            occ[q] = c >= 0 and inS[c] == 1
            cnt += occ[q]
        if cnt == 0 or cnt == 4:
            continue
        E1 += 1
        if cnt == 2 and occ[0] == occ[3]:
            diag += 1
            continue
        # occ order: (++), (+-), (-+), (--) for (sX, sY)
        fxp = occ[0] != occ[2]; fxm = occ[1] != occ[3]
        fyp = occ[0] != occ[1]; fym = occ[2] != occ[3]
        if cnt == 2:
            if fxp and fxm:
                ra = _find(par, FX[j, 0]); rb = _find(par, FX[j, 1])
                if ra != rb:
                    par[ra] = rb
            if fyp and fym:
                ra = _find(par, FY[j, 0]); rb = _find(par, FY[j, 1])
                if ra != rb:
                    par[ra] = rb
        else:
            isedge[j] = True
            ex[j] = FX[j, 0] if fxp else FX[j, 1]
            ey[j] = FY[j, 0] if fyp else FY[j, 1]
    # faces per plane and disk check
    rootmark = np.full(nf, -1, np.int64)
    comps = np.zeros(n, np.int64)
    F2 = 0
    for f in range(nf):
        if bnd[f]:
            F2 += 1
            r = _find(par, f)
            if rootmark[r] < 0:
                rootmark[r] = 1; comps[fplane[f]] += 1
    faces = 0
    for X in range(n):
        faces += abs(comps[X] - 1) if comps[X] > 0 else 1
    # Euler characteristic of each component: facets - incident 1-cells + incident vertices
    nfac = np.zeros(nf, np.int64); ned = np.zeros(nf, np.int64); nve = np.zeros(nf, np.int64)
    for f in range(nf):
        if bnd[f]:
            nfac[_find(par, f)] += 1
    for j in range(no):
        seen0 = -1
        for q in range(2):
            f = FX[j, q]
            if bnd[f]:
                r = _find(par, f)
                if r != seen0:
                    ned[r] += 1; seen0 = r
        seen0 = -1
        for q in range(2):
            f = FY[j, q]
            if bnd[f]:
                r = _find(par, f)
                if r != seen0:
                    ned[r] += 1; seen0 = r
    nv = OCT.shape[0]
    for v in range(nv):
        for z in range(3):
            seen0 = -1
            for q in range(4):
                f = VF[v, 4 * z + q]
                if bnd[f]:
                    r = _find(par, f)
                    if r != seen0 and r != -2:
                        # a vertex is counted once per component of this plane
                        ok = True
                        for qq in range(q):
                            f2 = VF[v, 4 * z + qq]
                            if bnd[f2] and _find(par, f2) == r:
                                ok = False
                        if ok:
                            nve[r] += 1
                        seen0 = r
    disks = 0
    for f in range(nf):
        if bnd[f] and _find(par, f) == f:
            if nfac[f] - ned[f] + nve[f] != 1:
                disks += 1
    # vertices: manifold check and chi
    badv = 0; V0 = 0
    for v in range(nv):
        occ = np.zeros(8, np.bool_); k = 0
        for q in range(8):
            c = OCT[v, q]
            occ[q] = c >= 0 and inS[c] == 1
            k += occ[q]
        if k == 0 or k == 8:
            continue
        V0 += 1
        for val in (True, False):
            start = -1; total = 0
            for q in range(8):
                if occ[q] == val:
                    total += 1
                    if start < 0:
                        start = q
            seen = np.zeros(8, np.bool_); stack = np.zeros(8, np.int64); sp = 0
            seen[start] = True; stack[0] = start; sp = 1; cnt = 1
            while sp > 0:
                sp -= 1; a = stack[sp]
                for bit in range(3):
                    b = a ^ (1 << bit)
                    if occ[b] == val and not seen[b]:
                        seen[b] = True; stack[sp] = b; sp += 1; cnt += 1
            if cnt != total:
                badv += 1
                break
    # edge runs per pair of planes
    runs = np.zeros(npairs, np.int64)
    prevp = -1; prevk = -10; prx = -1; pry = -1
    for j in range(no):
        if not isedge[j]:
            continue
        rx = _find(par, ex[j]); ry = _find(par, ey[j]); p = PAIR[j]
        if p != prevp or KS[j] != prevk + 1 or rx != prx or ry != pry:
            runs[p] += 1
        prevp = p; prevk = KS[j]; prx = rx; pry = ry
    adj = 0; missing = 0; rt = 0
    for p in range(npairs):
        adj += abs(runs[p] - 1); rt += runs[p]
        if runs[p] == 0:
            missing += 1
    chi = V0 - E1 + F2
    return faces, disks, adj, missing, diag, badv, chi, rt
