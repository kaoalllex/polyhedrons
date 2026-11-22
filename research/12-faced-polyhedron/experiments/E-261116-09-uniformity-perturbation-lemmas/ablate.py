"""E-261116-09 part B (PLAN.md): clause-family ablation of the E-261119-02 stage-B symmetric formulas.

Each record's formula is built by tranche.submap_formula (E-261103-03), the stage-B builder, while every clause is
tagged with the family that added it (CNF.clause tags; CNF.gp -> GP; clauses added outside them are Tseitin
definitions, DEF, always kept: they define fresh variables and never constrain the chirotope). The untagged formula's
formula_sha256 must equal the hash stage B recorded for the same canonical map. A subformula keeps DEF and a set S of
families; clauses are only added as S grows, so a superset of an UNSAT set is UNSAT and a subset of a SAT set is SAT.
Amendment 1 (PLAN.md): stage 1 (probe), every record: the full formula, each family dropped alone, the plain formula
(SYM and both gauges off) and the pilot's candidate {GP, SEGMENT_DISJOINT, TRIPLE} with its 2-subsets, cap CAP;
stage 2 (enum), the first record of every stratum: every set of size <= ENUM_MAX by size (supersets of a found UNSAT set
and subsets of a found SAT set implied, not solved), cap ENUM_CAP. kissat in a child process killed at the cap; UNKNOWN
and SKIPPED (past the wall deadline) are never used for implication.
Controls on the same filtered path: DRAWS symmetric generic plane draws pinned under the symmetry-only families
(GP, SYM, SB_ORBFLIP, SB_MIRROR) must be SAT and DRAWS wrong-action draws UNSAT (controls_b.draw / wrong, n2.gauge);
the (8, 3) rung's known SAT units must be SAT with all families, their models satisfying every clause.
Every UNSAT here is UNSAT-SOLVER for its exact subformula; no proof, no negative result.
Usage: python3 ablate.py OUT_DIR [--records N] [--workers 10] [--wall SECONDS]"""
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
CENSUS = EXP / 'E-261119-02-symmetric-nine-face-census'
sys.path.insert(0, str(CENSUS))
import controls_b  # noqa: E402  (puts code/, E-261117-02, E-261103-03, E-261118-03 and E-261103-02 on sys.path)
sys.path.insert(0, str(EXP / 'E-261103-03-s5-exact-decision-8-2-9-3'))
import tranche  # noqa: E402
import pilot  # noqa: E402
import omsat  # noqa: E402
from n2 import gauge  # noqa: E402
from pysat.solvers import Solver  # noqa: E402
import tempfile  # noqa: E402

CAP, DRAWS, SEED = 5, 5, 2611220901
ENUM_MAX, ENUM_CAP = 3, 2
CANDIDATE = ('GP', 'SEGMENT_DISJOINT', 'TRIPLE')
KISSAT = os.environ.get('KISSAT', str(Path.home() / 'bin/kissat'))
TMP = None  # set per run: OUT/tmp, emptied as it goes


def sat(clauses, cap):
    """kissat (the stage-B solver) in a child process, killed at cap: amendment 1 (n2.sat's in-process interrupt does not
    fire while CaDiCaL holds the GIL; pilot: 223 s on a 10 s cap)."""
    nv = max(abs(l) for cl in clauses for l in cl)
    with tempfile.NamedTemporaryFile('w', suffix='.cnf', dir=TMP, delete=True) as f:
        f.write(f'p cnf {nv} {len(clauses)}\n'); f.write(''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)); f.flush()
        t0 = time.monotonic()
        try:
            rc = subprocess.run([KISSAT, '-q', '-n', f'--time={cap}', f.name], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, timeout=cap + 5).returncode
        except subprocess.TimeoutExpired:
            rc = 0
    return dict(status={10: 'SAT', 20: 'UNSAT'}.get(rc, 'UNKNOWN'), seconds=round(time.monotonic() - t0, 3))
SYM_ONLY = ('GP', 'SYM', 'SB_ORBFLIP', 'SB_MIRROR')
SOURCES = [('pricing_9_4', 'maps/pricing.json', ['stageB-pricing']),
           ('pricing_9_5', 'maps/pricing_9_5.json', ['stageB5-pricing_9_5', 'stageB5-pricing_lean']),
           ('rung_8_3', 'maps/rung_8_3.json', ['stageB-rung_8_3']),
           ('rung_9_3', 'maps/rung_9_3.json', ['stageB-rung_9_3'])]

_clause, _gp = omsat.CNF.clause, omsat.CNF.gp


def _tagged_clause(self, lits, tag):
    n = len(self.clauses); _clause(self, lits, tag)
    if len(self.clauses) > n:
        self.__dict__.setdefault('ctag', {})[n] = tag


def _tagged_gp(self):
    n = len(self.clauses); _gp(self)
    self.__dict__.setdefault('ctag', {}).update({i: 'GP' for i in range(n, len(self.clauses))})


omsat.CNF.clause, omsat.CNF.gp = _tagged_clause, _tagged_gp


def recorded_hashes():
    out = defaultdict(set)
    for _, _, dirs in SOURCES:
        for d in dirs:
            for p in (CENSUS / 'results' / d).glob('*/results.jsonl'):
                for line in p.read_text().splitlines():
                    r = json.loads(line)
                    if not str(r.get('map_index', '')).startswith('control'):
                        out[r['canonical_sha256']].add(r['formula_sha256'])
    return out


def build(rec):
    links = dict(enumerate(rec['links'] if isinstance(rec['links'], list) else json.loads(rec['links'])))
    c = tranche.submap_formula(len(links), links, rec['sym_generator'], rec['sym_planes_only'])
    tags = [c.ctag.get(i, 'DEF') for i in range(len(c.clauses))]
    digest = hashlib.sha256(json.dumps([c.nv, c.clauses], separators=(',', ':')).encode()).hexdigest()
    return c, tags, digest, links


def sub(c, tags, S):
    return [cl for cl, t in zip(c.clauses, tags) if t == 'DEF' or t in S]


def pinned(c, clauses, chi):
    return clauses + [[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()]


def solver(c, tags, deadline, cap):
    """Status of a family set with monotone implication (supersets of UNSAT, subsets of SAT); UNKNOWN implies nothing."""
    known, times = {}, []
    def status(S):
        S = frozenset(S)
        if S in known:
            return known[S]
        if any(k <= S and v == 'UNSAT' for k, v in known.items()):
            return 'UNSAT*'
        if any(S <= k and v == 'SAT' for k, v in known.items()):
            return 'SAT*'
        if time.monotonic() > deadline:
            known[S] = 'SKIPPED'
            return 'SKIPPED'
        r = sat(sub(c, tags, S), cap); known[S] = r['status']; times.append(r['seconds'])
        return known[S]
    return status, known, times


def probes(c, tags, fams, deadline):
    """Stage 1 (amendment 1), every record: full, each family dropped, the plain formula (no SYM, no gauge) and the
    pilot's candidate {GP, SEGMENT_DISJOINT, TRIPLE} with its 2-subsets."""
    status, known, times = solver(c, tags, deadline, CAP)
    full = status(fams)
    out = dict(full=full, drop_one={f: status(set(fams) - {f}) for f in fams},
               plain=status(set(fams) - {'SYM', 'SB_ORBFLIP', 'SB_MIRROR'}),
               candidate={' '.join(S): status(S) for S in [CANDIDATE] + [tuple(T) for T in itertools.combinations(CANDIDATE, 2)]})
    out.update(solved=len(known), solver_seconds=round(sum(times), 3), max_seconds=round(max(times, default=0), 3))
    return out


def enumerate_sets(c, tags, fams, deadline):
    """Stage 2 (amendment 1), one record per stratum: every set of size <= ENUM_MAX by size, cap ENUM_CAP."""
    status, known, times = solver(c, tags, deadline, ENUM_CAP)
    if status(fams) != 'UNSAT':
        return dict(full=known[frozenset(fams)])
    minimal = []
    for size in range(1, ENUM_MAX + 1):
        for S in map(frozenset, itertools.combinations(fams, size)):
            if not any(m <= S for m in minimal) and status(S) == 'UNSAT':
                minimal.append(S)
    uncertain = [sorted(S) for S in minimal if any(T < S and v in ('UNKNOWN', 'SKIPPED') for T, v in known.items())]
    return dict(full='UNSAT', minimal_sets=sorted(sorted(S) for S in minimal), minimal_uncertain=uncertain,
                unknown_sets=sorted(sorted(S) for S, v in known.items() if v == 'UNKNOWN'),
                skipped=sum(v == 'SKIPPED' for v in known.values()), solved=len(known),
                solver_seconds=round(sum(times), 3), max_seconds=round(max(times, default=0), 3))


def draw(g, planes_only, rng):
    """controls_b.draw, with the rotation order taken from g (controls_b assumes order 3 in the standard chart; the
    (8, 3) rung has free half-turns there)."""
    if planes_only:
        return controls_b.draw(g, True, rng)
    order = 2 if all(g[g[x]] == x for x in range(len(g))) else 3
    chi = controls_b.chirotope_from_planes(controls_b.c3_planes(g, order, rng.randrange(1 << 30)))
    return chi if all(chi.values()) else None


def controls(c, tags, rec, i):
    links = rec['links'] if isinstance(rec['links'], list) else json.loads(rec['links'])
    n = len(links); g = rec['sym_generator']; po = rec['sym_planes_only']
    G = sorted(pilot.closure([tuple(g)], n))
    base = sub(c, tags, set(SYM_ONLY)); rng = random.Random(SEED + i); pos, neg = [], []
    while len(pos) < DRAWS:
        chi = draw(g, po, rng)
        if chi is None:
            continue
        pos.append(sat(pinned(c, base, gauge(chi, G, n)[0]), CAP)['status'])
        h = controls_b.wrong(g, rng)
        while (chi_w := draw(h, po, rng)) is None:
            pass
        neg.append(sat(pinned(c, base, gauge(chi_w, G, n)[0]), CAP)['status'])
    return dict(positive=pos, wrong_action=neg, PASS=all(s == 'SAT' for s in pos) and all(s == 'UNSAT' for s in neg))


def model_check(c):
    with Solver(name='cadical195', bootstrap_with=c.clauses) as s:
        ok = s.solve()
        m = set(s.get_model()) if ok else set()
    return dict(status='SAT' if ok else 'UNSAT', model_satisfies_all=ok and all(any(l in m for l in cl) for cl in c.clauses))


def work(job):
    global TMP
    stage, arm, i, rec, hashes, deadline, TMP = job
    t0 = time.monotonic()
    c, tags, digest, _ = build(rec)
    fams = sorted({t for t in tags if t != 'DEF'})
    out = dict(stage=stage, arm=arm, index=i, config=rec['config'], stratum=rec['stratum'],
               canonical_sha256=rec['canonical_sha256'], families=fams, formula_sha256=digest,
               hash_matches_stage_b=digest in hashes.get(rec['canonical_sha256'], ()))
    if stage == 'probe':
        out['family_clauses'] = {f: tags.count(f) for f in fams}; out['def_clauses'] = tags.count('DEF')
        if arm == 'rung_8_3':
            out['model'] = model_check(c)
        out['controls'] = controls(c, tags, rec, i)
        out['probes'] = probes(c, tags, fams, deadline)
    else:
        out['enum'] = enumerate_sets(c, tags, fams, deadline)
    out['wall_seconds'] = round(time.monotonic() - t0, 3)
    return out


def summarise(rows):
    P = [r for r in rows if r['stage'] == 'probe']; E = [r for r in rows if r['stage'] == 'enum']
    s = dict(records=len(P), enum_records=len(E), controls_pass=all(r['controls']['PASS'] for r in P),
             hashes_match=all(r['hash_matches_stage_b'] for r in rows),
             rung_8_3=[dict(index=r['index'], full=r['probes']['full'], model=r['model']) for r in P if r['arm'] == 'rung_8_3'])
    def tally(rs, get):
        t = defaultdict(int)
        for r in rs:
            t[get(r)] += 1
        return dict(sorted(t.items()))
    for scope, keyf in (('arm', lambda r: f"{r['arm']} {r['config']}"),
                        ('stratum', lambda r: f"{r['arm']} {r['config']} {r['stratum'][0]}")):
        groups = defaultdict(list)
        for r in P:
            groups[keyf(r)].append(r)
        s[scope] = {k: dict(records=len(rs), full=tally(rs, lambda r: r['probes']['full']),
                            plain=tally(rs, lambda r: r['probes']['plain']),
                            candidate={S: tally(rs, lambda r: r['probes']['candidate'][S]) for S in rs[0]['probes']['candidate']},
                            drop_one={f: tally(rs, lambda r: r['probes']['drop_one'].get(f, 'absent'))
                                      for f in sorted({f for r in rs for f in r['families']})})
                    for k, rs in sorted(groups.items())}
    s['enum'] = {f"{r['arm']} {r['config']} {r['stratum'][0]}": {k: v for k, v in r['enum'].items() if k != 'unknown_sets'}
                 for r in E}
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--records', type=int); ap.add_argument('--workers', type=int, default=10)
    ap.add_argument('--wall', type=float, default=720.0)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=False); (out / 'tmp').mkdir()
    start = time.monotonic(); deadline = start + a.wall
    manifest = dict(commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True).count('\n'),
                    branch=subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip(),
                    host=platform.platform(), python=sys.version.split()[0], workers=a.workers, cap_seconds=CAP,
                    wall_budget_seconds=a.wall, started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    hashes = {k: sorted(v) for k, v in recorded_hashes().items()}
    jobs, enum, seen = [], [], set()
    for arm, path, _ in SOURCES:
        recs = json.loads((CENSUS / path).read_text())['maps']
        for i, r in enumerate(recs[:a.records] if a.records else recs):
            jobs.append(('probe', arm, i, r, hashes, deadline, str(out / 'tmp')))
            key = (arm, r['config'], r['stratum'][0])
            if arm != 'rung_8_3' and key not in seen:
                seen.add(key); enum.append(('enum', arm, i, r, hashes, deadline, str(out / 'tmp')))
    jobs += enum
    rows = []
    with mp.Pool(a.workers) as pool, (out / 'records.jsonl').open('w') as f:
        for r in pool.imap_unordered(work, jobs):
            rows.append(r); f.write(json.dumps(r, separators=(',', ':')) + '\n'); f.flush()
    manifest.update(wall_seconds=round(time.monotonic() - start, 1), records=len(rows),
                    solver_seconds=round(sum(r.get('probes', r.get('enum', {})).get('solver_seconds', 0) for r in rows), 1),
                    skipped=sum(json.dumps(r).count('SKIPPED') for r in rows))
    (out / 'tmp').rmdir()
    manifest['solver'] = subprocess.run([KISSAT, '--version'], capture_output=True, text=True).stdout.strip()
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    s = summarise(rows); (out / 'summary.json').write_text(json.dumps(s, indent=1) + '\n')
    print(json.dumps(dict(manifest=manifest, controls_pass=s['controls_pass'], hashes_match=s['hashes_match'],
                          rung_8_3=s['rung_8_3'], arm=s['arm']), indent=1))


if __name__ == '__main__':
    main()
