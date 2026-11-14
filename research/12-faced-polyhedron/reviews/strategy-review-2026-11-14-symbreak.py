"""Session check of the lead review 2026-11-14 (no ledger evidence, no proofs: every UNSAT here is UNSAT-SOLVER).

Question: the plain S5 / S6 formulas (pilot.ALL_OPTS) carry no reorientation or mirror normalisation. What does
kissat need on known-answer formulas when the existing `symbreak` and `mirror` options of omsat.build are switched on?

    python3 reviews/strategy-review-2026-11-14-symbreak.py SCRATCH_DIR [CAP_SECONDS]

Units (known answers only, the (10, 3) target is not touched):
  gauge   Roest-Vigh, Mizhaev, Szilassi: a reorientation (and mirror) of the planes that satisfies the units exists,
          and the pinned chirotope is SAT with the units
  sat     four (10, 2) maps of E-261113-02: plain SAT, with units SAT
  unsat   (8, 2) #0, (9, 3) #40, (10, 4) #845: plain and with units; (10, 4) #96, #85: with units only (plain
          monolithic times are recorded in E-261108-03)
Writes reviews/strategy-review-2026-11-14-symbreak.json.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
for p in ('code', 'experiments/E-261103-03-s5-exact-decision-8-2-9-3',
          'experiments/E-261103-02-s5-omsat-multi-adjacency-encoder'):
    sys.path.insert(0, str(ROOT / p))
import pilot  # noqa: E402
import test_encoder  # noqa: E402

KISSAT = str(Path.home() / 'bin/kissat')
SB = dict(pilot.ALL_OPTS, symbreak=True, mirror=True)
# E-261108-03 results/run/kissat-B (copied from E-261113-04 cubes.py): monolithic seconds and plain CNF SHA-256.
MONO = {96: (1073.49, '859f21a94e6d9b02888a98059a96d643d9a7460f3b86f64f12291b4c08e29df0'),
        85: (2748.86, 'd89b0f3d42407482c58a5c15a9c0382b0f84cde1c3d5f5214dce696b6472aed0'),
        845: (188.38, '7b125e1c3862dd80209e5725a1e096cc6b4c38802d9dd45b63c9911a5aedd025')}


def cnf(t, opts):
    c = pilot.CNF(t.n)
    pilot.build(c, t, opts)
    return c


def run(c, out, name, cap, comments=()):
    path = out / (name + '.cnf')
    c.dimacs(path, comments=comments)
    started = time.monotonic()
    try:
        rc = subprocess.run([KISSAT, '-q', str(path)], stdout=subprocess.DEVNULL, timeout=cap).returncode
    except subprocess.TimeoutExpired:
        rc = None
    return dict(name=name, status={10: 'SAT', 20: 'UNSAT-SOLVER', None: 'TIMEOUT'}.get(rc, 'ERROR'),
                seconds=round(time.monotonic() - started, 2), cap=cap, variables=c.nv, clauses=len(c.clauses),
                cnf_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def gauge(planes, n):
    """Planes reoriented (and mirrored if needed) so that the n reorientation units and the mirror unit hold."""
    fixed = [(0, 1, k, n) for k in range(2, n)] + [(0, 2, 3, n), (1, 2, 3, n), (0, 1, 2, 3)]
    for mirror in (False, True):
        base = [[-p[0], *p[1:]] if mirror else list(p) for p in planes]
        for eps in itertools.product((1, -1), repeat=n):
            pl = [[e * x for x in p] for e, p in zip(eps, base)]
            chi = pilot.chirotope_from_planes(pl)
            if all(chi[s] > 0 for s in fixed):
                return pl, mirror
    return None, None


def main(scratch, cap=600):
    out = Path(scratch)
    out.mkdir(parents=True, exist_ok=True)
    jobs, report = [], dict(kissat='~/bin/kissat', cap=cap, gauge={}, units=[])
    for name, h, t in test_encoder.controls():
        pl, mirror = gauge(test_encoder.perturb(h), t.n)
        report['gauge'][name] = dict(found=pl is not None, mirrored=mirror)
        if pl is not None:
            c = cnf(t, SB)
            c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in pilot.chirotope_from_planes(pl).items()])
            jobs.append((c, f'gauge_{name}_pinned_sb', 60, ()))
    s6 = json.loads((ROOT / 'experiments/E-261113-02-s6-10-2-calibration-rung/maps/seeded_formulas.json').read_text())
    for m in s6['maps'][:4]:
        links = {int(k): v for k, v in m['links'].items()} if isinstance(m['links'], dict) else dict(enumerate(m['links']))
        tris = sorted({tuple(sorted((x, a, b))) for x, l in links.items() for a, b in zip(l, l[1:] + l[:1])})
        t = pilot.Triangulation(10, tris, links=links, submap=True)
        for tag, opts in (('plain', pilot.ALL_OPTS), ('sb', SB)):
            jobs.append((cnf(t, opts), f"sat_10_2_lutz{m.get('lutz', '?')}_{tag}", 60, ()))
    for (f, g, i), plain in (((8, 2, 0), True), ((9, 3, 40), True), ((10, 4, 845), True), ((10, 4, 96), False),
                             ((10, 4, 85), False)):
        t = pilot.from_links(pilot.census(f, g)['maps'][i]['links'])
        if plain:
            jobs.append((cnf(t, pilot.ALL_OPTS), f'unsat_{f}_{g}_map{i}_plain', cap,
                         (f'map{i}_plain', 'S5 pilot; interpret symmetry and model scope separately')))
        jobs.append((cnf(t, SB), f'unsat_{f}_{g}_map{i}_sb', cap, ()))
    with ThreadPoolExecutor(9) as pool:
        report['units'] = list(pool.map(lambda j: run(j[0], out, j[1], j[2], j[3]), jobs))
    for u in report['units']:
        for i, (seconds, digest) in MONO.items():
            if u['name'] == f'unsat_10_4_map{i}_plain':
                u['plain_hash_equals_record'] = u['cnf_sha256'] == digest
            if u['name'] == f'unsat_10_4_map{i}_sb':
                u['recorded_plain_seconds'] = seconds
        print(json.dumps(u))
    print(json.dumps(report['gauge']))
    (ROOT / 'reviews/strategy-review-2026-11-14-symbreak.json').write_text(json.dumps(report, indent=1) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 600)
