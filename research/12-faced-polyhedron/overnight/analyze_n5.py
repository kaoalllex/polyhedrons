"""Summarize night 5: the Gauss gate (job `gate`) and the normals-first ladder (job `n5`).
Gate: per realization genus / own degree, arms passing T1, the k_tau values; test 2.2 summary.
n5: per kind (nfirst / kdrift / g6) the status counts of every decided normal set (attempt logs), kdrift
class seeds (k_tau = -1 reached, T1 pass), and every exact realization (re-checked here with ladder_exact).
Usage: python3 -I analyze_n5.py [RESULTS_DIR]   (default: results/)"""
import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'code'))


def jl(path):
    out = []
    if os.path.exists(path):
        for line in open(path):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def main(res):
    gate = [r for r in jl(os.path.join(res, 'gate', 'results.jsonl')) if r.get('status') == 'GATE']
    if gate:
        by = defaultdict(list)
        for r in gate:
            by[(r['type_id'], r['genus'])].append(r)
        print('GATE: %d realizations' % len(gate))
        for (t, g), rs in sorted(by.items(), key=lambda x: (str(x[0][0]), x[0][1])):
            arms = [a for r in rs for a in r['arms']]
            print('  type %s genus %d: %d realizations (own degree %s), %d arms, T1 pass %d, k_tau %s' % (
                t, g, len(rs), dict(Counter(r.get('own_degree') for r in rs)), len(arms),
                sum(1 for a in arms if a.get('pass')), dict(Counter(a.get('k_tau') for a in arms))))
    ch = os.path.join(res, 'gate', 'chains_2_2.json')
    if os.path.exists(ch):
        print('TEST 2.2:', json.load(open(ch))['summary'])
    n5 = jl(os.path.join(res, 'n5', 'results.jsonl'))
    if not n5:
        return
    print('N5: %d tasks, %s' % (len(n5), dict(Counter(r.get('status') for r in n5))))
    att = os.path.join(res, 'n5', 'attempts')
    per = defaultdict(Counter); smt = defaultdict(list)
    if os.path.isdir(att):
        for f in sorted(os.listdir(att)):
            kind = f.split('_')[0]
            for a in jl(os.path.join(att, f)):
                per[kind][a['status']] += 1
                if 'smt_seconds' in a:
                    smt[kind].append(a['smt_seconds'])
    for kind in sorted(per):
        s = sorted(smt[kind])
        print('  %-3s decided normal sets: %s; z3 median %.0f s' % (kind, dict(per[kind]), s[len(s) // 2] if s else 0))
    kd = [r for r in n5 if r.get('kind') == 'kdrift']
    print('  kdrift: %s' % dict(Counter((r.get('drift') or {}).get('status') for r in kd)))
    for r in kd:
        d = r.get('drift') or {}
        if d.get('status') in ('T1_PASS', 'K_REACHED'):
            print('    %s %s k_tau %s margin %.4f t1 %s' % (r['task'], d['status'], d.get('k_tau'), d.get('hemisphere_margin') or 0, d.get('t1')))
    rd = os.path.join(res, 'n5', 'realized')
    if os.path.isdir(rd) and os.listdir(rd):
        from gauss_degree import coherent_triangles, links_from
        from ladder_exact import verify
        from gauss_gate import genus
        print('REALIZED (re-checked exactly):')
        for f in sorted(os.listdir(rd)):
            d = json.load(open(os.path.join(rd, f)))
            L = links_from(coherent_triangles([tuple(t) for t in d['triangles']]), len(d['planes']))
            g = genus(d['triangles'], len(d['planes']))
            ex = verify(d['planes'], L, require_all_pairs=(g == 6))
            print('  %s type %s genus %d: EMBEDDED %s %s' % (f, d.get('type_id'), g, ex['EMBEDDED'], ex['V_E_F_chi']))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'results'))
