"""Differential test of enc2 against exact geometry (ladder_exact.verify): the pinned chirotope of a plane set satisfies
the enc2 formula of a map iff verify says EMBEDDED. Usage: python3 difftest.py [N_PERTURBATIONS]"""
import json, random, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code')); sys.path.insert(0, str(HERE))
import enc2
from ladder_exact import verify
import control_rost_vigh as RV


def objects():
    rv_h, rv_l = RV.build()
    mz = json.loads((ROOT / 'literature/mizhaev2026-planes.json').read_text())
    out = [('roest_vigh', rv_h, rv_l), ('mizhaev', mz['planes_abcd_zero_form'], {int(k): v for k, v in mz['links_0based'].items()})]
    for k in (2, 3):
        g = json.loads((ROOT / f'experiments/E-261109-01-grooved-box-multiplicity-control/control_k{k}.json').read_text())
        out.append((f'grooved{k}', g['planes'], {int(a): b for a, b in g['links'].items()}))
        out.append((f'grooved{k}_swapped', g['planes'], {int(a): b for a, b in g['negative_links'].items()}))
    from szilassi import szilassi_arr
    _, faces, sh, _ = szilassi_arr()
    sl = {f: [[g for g in range(7) if g != f and a in faces[g] and b in faces[g]][0]
              for a, b in zip(faces[f], faces[f][1:] + faces[f][:1])] for f in range(7)}
    out.append(('szilassi', [[float(v) for v in r] for r in sh], sl))
    out.append(('rv_planes_mizhaev_map', rv_h, out[1][2]))
    out.append(('mizhaev_planes_rv_map', mz['planes_abcd_zero_form'], rv_l))
    return out


def exact(h, links):
    return bool(verify([[float(v) for v in r] for r in h], links, require_all_pairs=False)['EMBEDDED'])


def main(n=100, seed=2611090301):
    rng = random.Random(seed); tally = {}; bad = []
    for name, h, links in objects():
        e = enc2.Enc(links)
        cases = [('own', h)]
        for i in range(n):
            amp = rng.choice([3, 30, 300, 1000, 3000, 10000, 30000])
            cases.append((f'pert{amp}', [[v * 1000 + rng.randint(-amp, amp) for v in r] for r in h]))
        for tag, p in cases:
            try:
                chi = enc2.chirotope(p)
            except ValueError:
                tally.setdefault(name, {}).setdefault('nonuniform', 0); tally[name]['nonuniform'] += 1; continue
            try:
                ex = exact(p, links)
            except Exception as err:
                ex = f'verify-error:{type(err).__name__}'
            mine = e.holds(chi)
            key = f'exact={ex} enc2={mine}'
            tally.setdefault(name, {}).setdefault(key, 0); tally[name][key] += 1
            if ex != mine:
                bad.append((name, tag))
    for k, v in tally.items():
        print(k, v)
    print('MISMATCHES', len(bad), bad[:10])
    return len(bad)


if __name__ == '__main__':
    sys.exit(1 if main(int(sys.argv[1]) if len(sys.argv) > 1 else 100) else 0)
