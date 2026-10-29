"""Render the best period-defect configuration of one type (from overnight/results/pdefect/results.jsonl):
re-solve the closure MILP for the stored normals (phi = 0, i.e. in R^3), draw the 12 faces through the
solved vertex positions, and mark the edges where the surface fails to close (residual > 0) in red,
with the intended edge vector a_e d_e dashed. Four views + an interactive HTML (plotly).
Usage: python3 -I render_defect.py TYPE_ID OUT_PREFIX"""
import json, sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from period_defect import torus_defect, surface_edges
from gauss_degree import coherent_triangles, links_from

HERE = os.path.dirname(os.path.abspath(__file__))
FACE_COLORS = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#8a63d2',
               '#3fb6c6', '#c4553a', '#6f9e2f', '#b8860b', '#d0679d', '#5a6fb3']


def solve(tid):
    recs = [json.loads(l) for l in open(os.path.join(HERE, '..', 'overnight', 'results', 'pdefect', 'results.jsonl')) if l.strip()]
    rec = min((r for r in recs if r['type_id'] == tid and r.get('best_defect') is not None), key=lambda r: r['best_defect'])
    types = json.load(open(os.path.join(HERE, '..', 'data', 'k12_triangulations.json')))
    tri = next(t for t in types if t['id'] == tid)['triangles']
    G = np.array(rec['normals'], float); G /= np.linalg.norm(G, axis=1)[:, None]
    edges, faces, nv = surface_edges(G, tri)
    phi = {k: (0, 0, 0) for k in edges}
    val0, st, _, sol = torus_defect(G, tri, phi, time_limit=180, return_L='full')
    # the defect-optimal MILP vertex is degenerate (a few edges at the length bound); for the picture
    # take, among surfaces with residual <= 1.001 x optimum, the most compact one (min sum |a_e|)
    val, st2, _, sol2 = torus_defect(G, tri, phi, time_limit=180, return_L='full', balance_bound=val0 * 1.001 + 1e-9)
    if sol2 is not None:
        sol = sol2
    else:
        val = val0
    p, a, E = sol['p'], sol['a'], sol['E']
    print('optimal defect %.4f; picture residual %.4f; |a| range %.2f..%.2f' % (val0, val, np.abs(sol['a']).min(), np.abs(sol['a']).max()))
    res = {}
    for j, key in enumerate(E):
        t, h, d = edges[key]
        res[key] = (t, h, d, a[j], np.abs(p[h] - p[t] - a[j] * d).sum())
    ot = coherent_triangles(tri); L = links_from(ot, 12); vid = {frozenset(x): i for i, x in enumerate(ot)}
    polys = [[p[vid[frozenset((X, L[X][i], L[X][(i + 1) % len(L[X])]))]] for i in range(len(L[X]))] for X in range(12)]
    return rec, val, p, polys, res


def main(tid, out):
    rec, val, p, polys, res = solve(tid)
    c = p.mean(0); s = np.abs(p - c).max()
    P = [(np.array(q) - c) / s for q in polys]
    bad = [(k, v) for k, v in res.items() if v[4] > 1e-6]
    fig = plt.figure(figsize=(16, 13), dpi=130)
    # two full views + two views zoomed on the dense core (most vertices sit close together while a
    # few faces are stretched far out)
    rr = np.linalg.norm((p - c) / s, axis=1); core = max(np.quantile(rr, 0.6), 1e-3)
    views = [(22, 35, 1.0), (60, -60, 1.0), (22, 35, core), (-15, 200, core)]
    for i, (el, az, lim) in enumerate(views):
        ax = fig.add_subplot(2, 2, i + 1, projection='3d')
        for X, q in enumerate(P):
            ax.add_collection3d(Poly3DCollection([q], facecolor=FACE_COLORS[X], alpha=0.42, edgecolor='#333333', linewidths=0.6))
        for key, (t, h, d, aa, r) in bad:
            A = (p[t] - c) / s; B = (p[h] - c) / s; I = (p[t] + aa * d - c) / s
            ax.plot(*zip(A, B), color='#d03030', lw=2.6)
            ax.plot(*zip(A, I), color='#d03030', lw=1.2, ls='--')
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim); ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=el, azim=az); ax.set_axis_off()
        ax.set_title('full view' if lim == 1.0 else 'zoom x%.0f on the core' % (1 / lim), fontsize=12)
    fig.suptitle('Type %d, best period defect %.3f (task %s): 12 faces through the solved vertex positions;\n'
                 'red = %d edges where the surface does not close (dashed = intended edge vector)'
                 % (tid, val, rec['task'], len(bad)), fontsize=14)
    plt.tight_layout()
    fig.savefig(out + '.png', facecolor='white')
    # interactive version
    try:
        traces = []
        for X, q in enumerate(P):
            q = np.array(q); m = len(q); cen = q.mean(0)
            V = np.vstack([cen, q]); I = [0] * m; J = list(range(1, m + 1)); K = [((k % m) + 1) for k in range(1, m + 1)]
            traces.append(dict(type='mesh3d', x=V[:, 0].tolist(), y=V[:, 1].tolist(), z=V[:, 2].tolist(), i=I, j=J, k=K,
                               color=FACE_COLORS[X], opacity=0.45, name='face %d' % X, showlegend=True))
            Q = np.vstack([q, q[:1]])
            traces.append(dict(type='scatter3d', mode='lines', x=Q[:, 0].tolist(), y=Q[:, 1].tolist(), z=Q[:, 2].tolist(),
                               line=dict(color='#333333', width=2), showlegend=False, hoverinfo='skip'))
        for key, (t, h, d, aa, r) in bad:
            A = (p[t] - c) / s; B = (p[h] - c) / s
            traces.append(dict(type='scatter3d', mode='lines', x=[A[0], B[0]], y=[A[1], B[1]], z=[A[2], B[2]],
                               line=dict(color='#d03030', width=7), name='gap %.3f' % r, showlegend=False))
        html = ('<!doctype html><html><head><meta charset="utf-8"><title>Type %d defect view</title>'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.0/plotly.min.js"></script>'
                '<style>body{margin:0;background:#fff;font-family:sans-serif}#p{width:100vw;height:92vh}</style></head><body>'
                '<div style="padding:8px">Type %d, best period defect %.3f: drag to rotate; red = edges where the surface does not close</div>'
                '<div id="p"></div><script>Plotly.newPlot("p", %s, {scene:{aspectmode:"cube",xaxis:{visible:false},'
                'yaxis:{visible:false},zaxis:{visible:false}},margin:{l:0,r:0,t:0,b:0}});</script></body></html>'
                % (tid, tid, val, json.dumps(traces)))
        open(out + '.html', 'w').write(html)
    except Exception as e:                       # noqa: BLE001
        print('html skipped:', e)
    print('defect %.4f, non-closing edges %d, max residual %.3f' % (val, len(bad), max([v[4] for _, v in bad] or [0])))


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
