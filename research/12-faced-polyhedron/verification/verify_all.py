"""One command for the project's evidence base: positive controls, saved witnesses, negative controls,
certificates. Run it before claiming anything and in CI (.github/workflows/verify.yml).

Usage: python3 verify_all.py [--quick]     (--quick skips the 94-record archive re-check)
Exit status 0 iff every check gives its expected outcome."""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
CODE = os.path.join(ROOT, 'code')
sys.path.insert(0, HERE)
from verify_candidate import passes, verify_file  # noqa: E402


def run(args, cwd, needle):
    p = subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True)
    out = p.stdout + p.stderr
    ok = needle(out) if callable(needle) else needle in out
    return p.returncode == 0 and ok, (out.strip().splitlines() or [''])[-1][:110]


def files(expect, *paths, min_genus=None, genus=None):
    reps = [r for p in paths for r in verify_file(os.path.join(ROOT, p), min_genus=min_genus)]
    got = [r['EMBEDDED'] for r in reps]
    gs = sorted({(2 - r['V_E_F_chi'][3]) // 2 for r in reps if 'V_E_F_chi' in r})
    ok = bool(got) and all(g == expect for g in got) and (genus is None or gs == [genus])
    return ok, '%d record(s), EMBEDDED %s, genus %s' % (len(got), sorted(set(got)), gs)


def english_only():
    """Repository files are in English: no Cyrillic in any tracked text file."""
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    tracked = subprocess.run(['git', 'ls-files', '-z'], cwd=top, capture_output=True, text=True).stdout.split('\0')
    bad = []
    for f in filter(None, tracked):
        try:
            text = open(os.path.join(top, f), encoding='utf-8').read()
        except (UnicodeDecodeError, OSError):
            continue
        if re.search('[\u0400-\u04ff]', text):
            bad.append(f)
    return not bad, '%d tracked file(s) with Cyrillic%s' % (len(bad), (': ' + ', '.join(bad[:3])) if bad else '')


def s0_rejects_roest_vigh():
    """The strict target must reject an embedded all-pairs object with doubled adjacencies."""
    sys.path.insert(0, CODE)
    from control_rost_vigh import build
    from verify_candidate import _verify
    H, links = build()
    rep = _verify({'planes': H, 'links': links})
    s1, s0, s5 = passes(rep, 'all-pairs'), passes(rep, 'S0'), passes(rep, 'S5')
    return s1 and not s0 and not s5, 'Roest-Vigh: all-pairs %s, S0 %s, S5 %s (8 faces at genus 3, maximum 9)' % (s1, s0, s5)


GL = 'experiments/E-261030-03-genus-ladder-type0-genus3/results/'
G4 = 'experiments/E-261030-04-type0-genus4-attempts/results/'
SF = 'experiments/E-261030-02-solid-first-exact-inner-n12/results/'
CHECKS = [
    ('repository: English only (no Cyrillic in tracked files)', english_only),
    ('research graph: ideas, hypotheses, experiments; links resolve; map/graph.json in sync',
     lambda: run(['trace.py', '--check'], HERE, 'in sync; ')),
    ('combinatorics: 59 types, independent checker + relabelling selftest',
     lambda: run(['check_triangulations.py', '../data/k12_triangulations.json', '--selftest'], CODE,
                 'OK: selftest')),
    ('combinatorics: S5 census, saved maps, sampler and K12 controls, C3 cross-check',
     lambda: run(['test_census.py'], os.path.join(ROOT, 'experiments', 'E-261103-01-s5-map-census'),
                 lambda out: '\nOK' in out)),
    ('OM-SAT: multiple adjacencies, pinned controls, saved evidence and S0 regression',
     lambda: run(['test_encoder.py'], os.path.join(ROOT, 'experiments', 'E-261103-02-s5-omsat-multi-adjacency-encoder'),
                 lambda out: '\nOK' in out and 'skipped=' not in out)),
    ('OM-SAT: S5 (8,2)/(9,3) saved formulas, proofs and controls',
     lambda: run(['test_pilot.py', 'EvidenceTests'], os.path.join(ROOT, 'experiments', 'E-261103-03-s5-exact-decision-8-2-9-3'),
                 lambda out: '\nOK' in out)),
    ('solid-first: multirun disk model, known controls, random D2 recovery, independent checker',
     lambda: run(['test_pilot.py'], os.path.join(ROOT, 'experiments', 'E-261103-05-s5-symmetric-solid-first'),
                 lambda out: '\nOK' in out and 'skipped=' not in out)),
    ('Lemma 5.1 on perturbed Szilassi planes (n = 7, 0 mismatches)',
     lambda: run(['test_szilassi.py'], HERE, lambda out: re.findall(r"'trials': \d+", out) and not re.search(
         r"'zero_viol_NOT_embedded': [1-9]|'pos_viol_but_embedded': [1-9]", out))),
    ('positive control: Roest-Vigh 8 faces, doubled adjacencies, Gauss degree -2',
     lambda: run(['control_rost_vigh.py'], CODE, 'own degree -2 target -2')),
    ('positive control: Szilassi found without a map (solid-first)',
     lambda: files(True, 'experiments/E-261029-20-solid-first-n7/results/szilassi_found_without_map.json')),
    ('witness: type-0 genus-3 extendable realizations (5 files)',
     lambda: files(True, *[GL + 'type0_genus3_extendable%s.json' % s for s in ('', '_b', '_c', '_d', '_polished')],
                   genus=3)),
    ('witness: solid-first genus-3 (other map)',
     lambda: files(True, SF + 'genus3_12faces_48pairs.json',
                   SF + 'genus3_12faces_48pairs_polished.json', genus=3)),
    ('witness: solid-first genus-2',
     lambda: files(True, SF + 'genus2_12faces_42pairs.json', genus=2)),
    ('negative control: --target S0 and S5 reject Roest-Vigh (doubled adjacencies; not maximal)', s0_rejects_roest_vigh),
    ('positive control: --target S5 accepts Szilassi (7 faces, genus 1, maximal)',
     lambda: (lambda r: (all(x['PASS'] for x in r), '%d record(s), S5 PASS %s' % (len(r), [x['PASS'] for x in r])))(
         verify_file(os.path.join(ROOT, 'experiments/E-261029-20-solid-first-n7/results/szilassi_found_without_map.json'), target='S5'))),
    ('site: lab models in index.html = exactly re-verified witnesses/witnesses.json',
     lambda: run(['export_site.py', '--check'], os.path.join(ROOT, 'witnesses'), 'in sync')),
    ('negative control: genus-4 attempts are NOT embedded',
     lambda: files(False, G4 + 'type0_genus4_attempt_4viol.json', G4 + 'type0_genus4_attempt_degenerate.json')),
    ('certificate: type-0 handle completion genus 3 -> 6 (combinatorial)',
     lambda: run(['verify.py', 'certificate.json', '--source', '../../../' + GL + 'type0_genus3_extendable.json',
                  '--catalog', '../../../data/k12_triangulations.json'],
                 os.path.join(HERE, 'certificates', 'type0_handle_completion'), 'PASS')),
    ('certificate: three biquadratic final polynomials (k-face SAT models of types 0, 53, 57), independent checker',
     lambda: run(['-I', 'verify.py', 'certificates.json', '--selftest'], os.path.join(HERE, 'certificates', 'final_polynomial'), 'ALL PASS')),
    ('archive: every genus-3 realization (nights 3-5)',
     lambda: files(True, 'experiments/E-261030-10-realization-archive-climb/results/arch/archive.json', min_genus=3, genus=3)),
]


def main():
    quick = '--quick' in sys.argv
    fails = 0
    for name, fn in CHECKS:
        if quick and name.startswith('archive'):
            print('SKIP  %s' % name)
            continue
        t = time.time()
        try:
            ok, detail = fn()
        except Exception as e:  # a crashing check is a failed check, never a silent pass
            ok, detail = False, '%s: %s' % (type(e).__name__, e)
        fails += not ok
        print('%s  %-72s %5.1fs  %s' % ('PASS' if ok else 'FAIL', name, time.time() - t, detail), flush=True)
    print('ALL PASS' if not fails else '%d FAILED' % fails)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
