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
from verify_candidate import verify_file  # noqa: E402


def run(args, cwd, needle):
    p = subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True)
    out = p.stdout + p.stderr
    ok = needle(out) if callable(needle) else needle in out
    return p.returncode == 0 and ok, (out.strip().splitlines() or [''])[-1][:110]


def files(expect, *paths, min_genus=None):
    reps = [r for p in paths for r in verify_file(os.path.join(ROOT, p), min_genus=min_genus)]
    got = [r['EMBEDDED'] for r in reps]
    return bool(got) and all(g == expect for g in got), '%d record(s), EMBEDDED %s' % (len(got), sorted(set(got)))


GL = 'experiments/genus_ladder/'
CHECKS = [
    ('combinatorics: 59 types, independent checker + relabelling selftest',
     lambda: run(['check_triangulations.py', '../data/k12_triangulations.json', '--selftest'], CODE,
                 'OK: selftest')),
    ('Lemma 5.1 on perturbed Szilassi planes (n = 7, 0 mismatches)',
     lambda: run(['test_szilassi.py'], HERE, lambda out: re.findall(r"'trials': \d+", out) and not re.search(
         r"'zero_viol_NOT_embedded': [1-9]|'pos_viol_but_embedded': [1-9]", out))),
    ('positive control: Roest-Vigh 8 faces, doubled adjacencies, Gauss degree -2',
     lambda: run(['control_rost_vigh.py'], CODE, 'own degree -2 target -2')),
    ('positive control: Szilassi found without a map (solid-first)',
     lambda: files(True, 'experiments/solid_first/szilassi_found_without_map.json')),
    ('witness: type-0 genus-3 extendable realizations (5 files)',
     lambda: files(True, *[GL + 'type0_genus3_extendable%s.json' % s for s in ('', '_b', '_c', '_d', '_polished')])),
    ('witness: solid-first genus-3 (other map) and genus-2',
     lambda: files(True, 'experiments/solid_first/genus3_12faces_48pairs.json',
                   'experiments/solid_first/genus3_12faces_48pairs_polished.json',
                   'experiments/solid_first/genus2_12faces_42pairs.json')),
    ('negative control: genus-4 attempts are NOT embedded',
     lambda: files(False, GL + 'type0_genus4_attempt_4viol.json', GL + 'type0_genus4_attempt_degenerate.json')),
    ('certificate: type-0 handle completion genus 3 -> 6 (combinatorial)',
     lambda: run(['verify.py', 'certificate.json', '--source', '../../../' + GL + 'type0_genus3_extendable.json',
                  '--catalog', '../../../data/k12_triangulations.json'],
                 os.path.join(HERE, 'certificates', 'type0_handle_completion'), 'PASS')),
    ('archive: every genus-3 realization (nights 3-5)',
     lambda: files(True, 'overnight/results/arch/archive.json', min_genus=3)),
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
