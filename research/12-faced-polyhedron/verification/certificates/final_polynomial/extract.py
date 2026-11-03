"""Collect the exact final-polynomial certificates with their linkage to the SAT models (uses the encoder).

Run from research/12-faced-polyhedron/: python3 verification/certificates/final_polynomial/extract.py
Writes certificates.json; type 0 k = 9 is regenerated from its stored model (night 6 did not store multipliers)."""
import hashlib, json, os, sys, tempfile
ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, 'code')); sys.path.insert(0, os.path.join(ROOT, 'experiments', 'E-261101-25-chirotope-first'))
from omsat import CNF
import chirotope_first as CF
import final_polynomial as FP

SRC = [('experiments/E-261101-23-k-face-subinstances-face-cegar/results/0/results.jsonl', 0, 9),
       ('experiments/E-261102-01-kface-sweep-completion/results/3/results.jsonl', 53, 9),
       ('experiments/E-261102-01-kface-sweep-completion/results/6/results.jsonl', 57, 8)]
out = []
for path, tid, k in SRC:
    lines = open(path).read().splitlines()
    ln, r = [(i, json.loads(l)) for i, l in enumerate(lines) if '"final_polynomial"' in l and json.loads(l)['type'] == tid and json.loads(l)['k'] == k][0]
    T, _ = CF.load_type(tid)
    C = CNF(12); CF.build_faces(C, T, r['faces'], simple=True)
    with tempfile.NamedTemporaryFile(suffix='.cnf', delete=False) as f: tmp = f.name
    C.dimacs(tmp, comments=['E-261101-23 k-face sub-instance type %d k %d faces %s (GP, SB, TRIPLE, SIMPLE, REFLEX1, POC on these faces)' % (tid, k, r['faces'])])
    h = hashlib.sha256(open(tmp, 'rb').read()).hexdigest(); os.remove(tmp)
    chi = CF.model_chi(C, r['model_chi_pos'], 12)
    cert = r['final_polynomial'].get('certificate')
    regenerated = cert is None
    if regenerated:
        fp = FP.final_polynomial(chi, 13, time_limit=600)
        assert fp['status'] == 'NONREALIZABLE-EXACT', fp['status']
        cert = fp['certificate']
    agree = all(chi[tuple(map(int, s.split(',')))] == v for s, v in cert['signs'].items())
    print(tid, k, 'cnf hash matches record:', h == r['cnf_sha256'], '| certificate signs = model signs:', agree,
          '| regenerated:', regenerated, '| rows', len(cert['rows']), 'brackets', len(cert['signs']))
    out.append({'id': 'type%02d_k%d' % (tid, k), 'type': tid, 'k': k, 'faces': r['faces'], 'source': '%s line %d' % (path, ln + 1),
                'cnf_sha256': r['cnf_sha256'], 'cnf_rebuilt_matches': h == r['cnf_sha256'], 'signs_match_model': agree,
                'regenerated_from_model': regenerated, 'certificate': cert})
json.dump(out, open('verification/certificates/final_polynomial/certificates.json', 'w'), indent=1)
