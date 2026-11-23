#!/usr/bin/env python3
"""Audit of the amendment-6 pass-1 run (chunks 0-9 of the (9, 5) C2 4 x 2 + 1 list): writes pass1_summary.json.

Checks per chunk: every planned map has exactly one final UNSAT-SOLVER record that ended `completed`; SKIPPED-STOP
records (units in flight at a stop) have a later final record; the pinned f9 controls hold on every shard; the maps
files match the SHA-256 pinned in pass1_9_5.json. Records the SHA-256 of every shard's results.jsonl.
"""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
pins = json.loads((HERE / 'pass1_9_5.json').read_text())['chunks']
summary, maximum, total_seconds, finals = {}, 0.0, 0.0, 0
for k in range(10):
    folder = HERE / 'results' / ('stageB5-pass1-c%03d' % k)
    final, skipped, controls, hashes = {}, [], collections.Counter(), {}
    maps_sha = hashlib.sha256((HERE / 'maps' / 'pass1_9_5' / ('c%03d.json' % k)).read_bytes()).hexdigest()
    assert maps_sha == pins[str(k)]['maps_sha256'], k
    for path in sorted(folder.glob('[0-9]/results.jsonl')):
        hashes[path.parent.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if str(r['map_index']).startswith('control'):
                controls[(r['map_index'].startswith('control-f9-neg'), r['status'])] += 1
            elif r['status'] == 'SKIPPED-STOP':
                skipped.append(r['map_index'])
            else:
                assert r['map_index'] not in final and r['status'] == 'UNSAT-SOLVER' and r['ended_by'] == 'completed', r
                final[r['map_index']] = r['seconds']
    assert len(final) == pins[str(k)]['records'] and all(i in final for i in skipped), k
    assert controls == {(False, 'SAT'): 10, (True, 'UNSAT-SOLVER'): 10}, controls
    maximum = max(maximum, max(final.values()))
    total_seconds += sum(final.values())
    finals += len(final)
    summary[k] = {'records': len(final), 'skipped_stop_rerun': skipped, 'results_jsonl_sha256': hashes}
out = {'records': finals, 'status': 'UNSAT-SOLVER', 'max_solver_seconds': maximum,
       'mean_solver_seconds': total_seconds / finals, 'chunks': summary}
(HERE / 'pass1_summary.json').write_text(json.dumps(out, indent=1) + '\n')
print(finals, maximum, total_seconds / finals)
