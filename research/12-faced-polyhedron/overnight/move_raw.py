#!/usr/bin/env python3
"""Move raw per-unit run output that git ignores (attempt_*/ logs, specs, maps; see the root .gitignore) out of the
checkout into ../polyhedrons-data/<same path>, so the checkout holds what is committed. Each file is copied,
its SHA-256 compared, and only then removed here. Tracked files are never touched; an existing copy with other
content is never overwritten. Refuses while a recorded run process (results/launch.pids) is alive.

Usage: python3 move_raw.py [--dry-run] [--data DIR]      (DIR defaults to $POLYHEDRONS_DATA or ../polyhedrons-data)
"""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent / 'experiments'


def sha(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--data', type=Path)
    args = parser.parse_args()
    root = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, text=True).strip())
    data = (args.data or Path(os.environ.get('POLYHEDRONS_DATA', root.parent / 'polyhedrons-data'))).resolve()
    running = [line.split()[-1] for pids in EXPERIMENTS.glob('*/results/launch.pids')
               for line in pids.read_text().splitlines() if line.split() and line.split()[-1].isdigit()
               and alive(int(line.split()[-1]))]
    if running:
        sys.exit('refused: run processes are alive ({}); move raw output after the run'.format(', '.join(running)))
    listed = subprocess.check_output(
        ['git', 'ls-files', '-z', '--others', '--ignored', '--exclude-standard', '--',
         ':(glob)research/12-faced-polyhedron/experiments/**/attempt_*/**'], cwd=root)
    files = [name for name in listed.decode().split('\0') if name]
    moved = size = 0
    for name in files:
        source, target = root / name, data / name
        if not source.is_file() or source.is_symlink():
            continue
        digest = sha(source)
        if target.exists() and sha(target) != digest:
            sys.exit('refused: {} exists with other content'.format(target))
        size += source.stat().st_size
        moved += 1
        if args.dry_run:
            continue
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if sha(target) != digest:
                sys.exit('copy check failed for {}'.format(name))
        source.unlink()
    if not args.dry_run:
        for directory in sorted(EXPERIMENTS.glob('**/attempt_*/**/'), key=lambda p: -len(p.parts)):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
    print('{} {} files, {:.1f} MB, to {}'.format('would move' if args.dry_run else 'moved', moved, size / 1048576, data))


if __name__ == '__main__':
    main()
