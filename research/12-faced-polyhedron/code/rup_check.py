"""Minimal forward RUP checker (deletions ignored, which is sound for RUP lemmas).
usage: rup_check.py formula.cnf[.gz] proof.drat  -> prints VERIFIED if every lemma is RUP
and the empty clause is derived. RAT-only lemmas are reported as failures (not verified)."""
import sys, gzip
def read_cnf(p):
    f = gzip.open(p, 'rt') if p.endswith('.gz') else open(p)
    cls = []
    for line in f:
        if line[0] in 'cp':
            continue
        l = list(map(int, line.split()))
        cls.append(l[:-1])
    return cls
cls = read_cnf(sys.argv[1])
watch = {}
units = []
assign = {}
def val(l):
    v = assign.get(abs(l))
    return None if v is None else (v if l > 0 else not v)
def add(c):
    if len(c) == 1:
        units.append(c[0]); return
    cid = len(db); db.append(list(c))
    watch.setdefault(c[0], []).append(cid); watch.setdefault(c[1], []).append(cid)
db = []
for c in cls:
    if not c:
        print('empty clause in formula'); sys.exit()
    add(c)
def propagate(trail_start_lits):
    """assign lits, unit propagate; return True on conflict. assignment is undone after."""
    trail = []
    q = []
    for l in trail_start_lits:
        v = val(l)
        if v is False: undo(trail); return True
        if v is None: assign[abs(l)] = l > 0; trail.append(abs(l)); q.append(l)
    i = 0
    while i < len(q):
        l = q[i]; i += 1
        nl = -l
        ws = watch.get(nl, [])
        j = 0
        while j < len(ws):
            cid = ws[j]; c = db[cid]
            if c[0] == nl: c[0], c[1] = c[1], c[0]
            if val(c[0]) is True: j += 1; continue
            found = False
            for k in range(2, len(c)):
                if val(c[k]) is not False:
                    c[1], c[k] = c[k], c[1]
                    watch.setdefault(c[1], []).append(cid)
                    ws[j] = ws[-1]; ws.pop(); found = True; break
            if found: continue
            v0 = val(c[0])
            if v0 is False: undo(trail); return True
            if v0 is None: assign[abs(c[0])] = c[0] > 0; trail.append(abs(c[0])); q.append(c[0])
            j += 1
    undo(trail); return False
def undo(trail):
    for v in trail: del assign[v]
nlem = 0; bad = 0; empty = False
for line in open(sys.argv[2]):
    t = line.split()
    if not t or t[0] == 'd': continue
    lem = list(map(int, t[:-1]))
    nlem += 1
    if not propagate(units + [-x for x in lem]):
        bad += 1
    if not lem:
        empty = True; break
    add(lem)
print('lemmas', nlem, 'non-RUP', bad, 'empty clause derived', empty)
print('VERIFIED' if (bad == 0 and empty) else 'NOT VERIFIED')
