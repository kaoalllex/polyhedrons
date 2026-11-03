#!/usr/bin/env bash
# Bounded single-worker validation: bash run.sh [pilot|0]. No target solving.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
exec "$PYTHON" - "$HERE" "${1:-0}" <<'PY'
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tarfile
import time

here = Path(sys.argv[1])
shard = sys.argv[2]
assert shard in ('pilot', '0'), 'only pilot and shard 0 are registered'
out = here / 'results' / shard
out.mkdir(parents=True, exist_ok=False)
root = here.parents[1]
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
started = time.monotonic()
manifest = dict(commit=git('rev-parse', 'HEAD'), branch=git('branch', '--show-current'),
                dirty=git('status', '--porcelain'), workers=1, cpu_count=__import__('os').cpu_count(),
                host=platform.node(), os=platform.platform(), python=sys.version,
                started_utc=datetime.now(timezone.utc).isoformat(), shard=shard,
                trials=1 if shard == 'pilot' else 1000, hard_cap_seconds=900,
                parameters=dict(seed_base=261103020, radii=[1,10,300,3000,10000,40000], scale=1000))
sources = [root / 'code' / p for p in ('omsat.py','omsat_sym.py','omsat_geom.py','omsat_validate.py','ladder_exact.py','control_rost_vigh.py')]
sources += [here / p for p in ('controls.py','test_encoder.py','PLAN.md','s0_baseline.json','run.sh')]
inputs = sources + [root / 'literature/mizhaev2026-planes.json', root.parents[1] / 'index.html']
inputs += [root / f'experiments/E-261103-01-s5-map-census/results/maps_{f}_{g}.json' for f,g in ((8,2),(9,3))]
manifest['inputs_sha256'] = {str(p.relative_to(root.parents[1])): digest(p) for p in inputs}
with tarfile.open(out / 'source.tar.gz', 'w:gz') as tar:
    for p in sources:
        tar.add(p, arcname=str(p.relative_to(root)))
(out / 'pip-freeze.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
rc = 1
try:
    with (out / 'controls.log').open('w') as log:
        command = [sys.executable, '-u', str(here / 'controls.py'), '--trials', str(manifest['trials']), '--out', str(out)]
        rc = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=900).returncode
except subprocess.TimeoutExpired:
    rc = 124
finally:
    elapsed = time.monotonic() - started
    manifest.update(finished_utc=datetime.now(timezone.utc).isoformat(), exit_status=rc,
                    wall_seconds=elapsed, core_hours=elapsed/3600, ended_by='hard_cap' if rc==124 else 'completed',
                    budget_fraction=elapsed/900,
                    outputs_sha256={p.name:digest(p) for p in out.iterdir() if p.name!='manifest.json' and p.is_file()})
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (out / 'manifest.txt').write_text('\n'.join(f'{k}: {v}' for k,v in manifest.items() if not isinstance(v,dict)) + '\n')
print((out / 'controls.log').read_text())
print('exit_status:',rc,'wall_seconds:',round(elapsed,2),'core_hours:',round(elapsed/3600,6))
sys.exit(rc)
PY
