"""Draw the research map: one sector per research direction, grouped by area.
Filled = answered/done, hatched light fill = started (in progress), empty outline = not started.
Usage: python3 research_map.py OUT_PREFIX   (writes OUT_PREFIX.png and OUT_PREFIX.svg)"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Patch

DONE, STARTED, TODO = 'done', 'started', 'todo'
AREAS = [  # (area, colour, [(direction, status), ...]); colours: validated categorical slots 1-5
    ('Reduction &\ncombinatorics', '#2a78d6', [
        ('Face-plane reduction', DONE), ('59 types re-enumerated', DONE),
        ('Lemma 5.1 + review', DONE), ('Per-face decomposition', TODO)]),
    ('Constructive\nsearch', '#eb6834', [
        ('Prior near-misses analysed', DONE), ('Geometry-first SAT', DONE),
        ('Exact plane relocation', DONE), ('Admissible normals + exact offsets', DONE),
        ('Polar / dual-mesh / tube seeds', DONE), ('Symmetric planes, asym. triangulation', DONE),
        ('Numerical immersion search', STARTED), ('Period-defect search (night 2)', STARTED),
        ('3-torus relaxation', STARTED), ('Torus "deflation" homotopy', TODO)]),
    ('Topology &\ntheory', '#1baf7a', [
        ('Gauss-degree filter', DONE), ('Local lemma (curvature)', DONE), ('Parity theorem', DONE),
        ('Handle-period obstruction', STARTED), ('Farkas certificates -> lemma', TODO),
        ('Lensing-type invariants', TODO), ('Maxwell-Cremona, genus g', TODO),
        ('Discharging (Gauss-Bonnet)', TODO), ('Winding-number classifier', DONE)]),
    ('Impossibility\nproofs', '#eda100', [
        ('No symm. embedding (certified)', DONE), ('No symm. immersion (certified)', DONE),
        ('Asymmetric immersion SAT', STARTED), ('Cube-and-conquer, asymmetric', TODO),
        ('Second independent encoder', TODO), ('LRAT / formal checking', TODO),
        ('Write-up + expert review', TODO), ('Final polynomials (SDP)', TODO),
        ('Projective symmetries (corollary)', TODO)]),
    ('Cross-field\nideas', '#e87ba4', [
        ('External AI reviews', DONE), ('Szilassi embryo', DONE), ('CSG read-once solids', TODO),
        ('Moment-curve / Tietze ansatz', TODO), ('Star-tracker hashing', TODO),
        ('Genus ladder (g = 7)', TODO), ('Island-model evolution', TODO),
        ('Screw-orbit planes', DONE), ('GWAS on near-misses', STARTED), ('Ladder n = 8..11', TODO),
        ('Difference map (RRR)', TODO), ('Rare-event estimation', TODO), ('Tropical / patchwork seeds', TODO),
        ('CEGAR loop', TODO), ('Local-search SAT', TODO), ('Planarization flow', TODO)]),
]
INK, INK2, SURFACE = '#0b0b0b', '#52514e', '#fcfcfb'


def main(out):
    items = [(a, c, d, s) for a, c, lst in AREAS for d, s in lst]
    n = len(items)
    step = 360.0 / n
    fig, ax = plt.subplots(figsize=(13, 13), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.95, 2.12); ax.set_aspect('equal'); ax.axis('off')
    R0, R1 = 0.48, 1.0
    for i, (area, col, name, st) in enumerate(items):
        th1 = 90 - i * step
        th2 = th1 - step
        if st == DONE:
            w = Wedge((0, 0), R1, th2, th1, width=R1 - R0, facecolor=col, edgecolor=SURFACE, linewidth=2)
        elif st == STARTED:
            w = Wedge((0, 0), R1, th2, th1, width=R1 - R0, facecolor=col + '59', edgecolor=SURFACE,
                      linewidth=2, hatch='////')
        else:
            w = Wedge((0, 0), R1 - 0.012, th2 + 0.8, th1 - 0.8, width=R1 - R0 - 0.024, facecolor=SURFACE,
                      edgecolor=col, linewidth=1.6)
        ax.add_patch(w)
        mid = np.deg2rad((th1 + th2) / 2)
        x, y = 1.04 * np.cos(mid), 1.04 * np.sin(mid)
        ang = np.rad2deg(mid)
        rot = ang if -90 <= ang <= 90 else ang + 180
        ha = 'left' if -90 <= ang <= 90 else 'right'
        if ang < -90:
            rot, ha = ang + 180, 'right'
        ax.text(x, y, name, rotation=rot, rotation_mode='anchor', ha=ha, va='center', fontsize=10.5,
                color=INK if st != TODO else INK2)
    # area band (inner ring) with names
    k = 0
    for area, col, lst in AREAS:
        th1 = 90 - k * step
        th2 = th1 - len(lst) * step
        ax.add_patch(Wedge((0, 0), R0 - 0.03, th2, th1, width=0.07, facecolor=col, edgecolor=SURFACE, linewidth=2))
        k += len(lst)
    nd = sum(1 for *_, s in items if s == DONE); ns = sum(1 for *_, s in items if s == STARTED)
    nt = n - nd - ns
    ax.text(0, 2.0, '12-face Series-1 polyhedron: research map (2026-10-29)', ha='center', fontsize=16,
            color=INK, fontweight='bold')
    ax.text(0, 1.9, '%d directions: %d done, %d in progress, %d not started' % (n, nd, ns, nt),
            ha='center', fontsize=12, color=INK2)
    ax.text(0, 0.06, str(n), ha='center', va='center', fontsize=34, color=INK, fontweight='bold')
    ax.text(0, -0.12, 'directions', ha='center', va='center', fontsize=12, color=INK2)
    handles = [Patch(facecolor='#8a8a86', edgecolor=SURFACE, label='done / answered'),
               Patch(facecolor='#8a8a8659', edgecolor='#8a8a86', hatch='////', label='started, in progress'),
               Patch(facecolor=SURFACE, edgecolor='#8a8a86', label='not started')]
    leg1 = ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False,
                     fontsize=12)
    ax.add_artist(leg1)
    ah = [Patch(facecolor=col, edgecolor=SURFACE, label=area.replace('\n', ' ')) for area, col, _ in AREAS]
    ax.legend(handles=ah, loc='upper center', bbox_to_anchor=(0.5, -0.035), ncol=5, frameon=False, fontsize=11.5)
    fig.savefig(out + '.png', facecolor=SURFACE, bbox_inches='tight')
    fig.savefig(out + '.svg', facecolor=SURFACE, bbox_inches='tight')


if __name__ == '__main__':
    main(sys.argv[1])
