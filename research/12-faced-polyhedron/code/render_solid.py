"""Render a solid-first result (planes + solid cells) or a map-based one (planes + triangles) as a polyhedron: four views (PNG) + interactive
plotly HTML. Usage: python3 -I render_solid.py RESULT_JSON OUT_PREFIX TITLE"""
import json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from gauss_degree import coherent_triangles, links_from
from ladder import polygons

COL = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#8a63d2', '#3fb6c6', '#c4553a', '#6f9e2f', '#b8860b',
       '#d0679d', '#5a6fb3']
r = json.load(open(sys.argv[1])); out = sys.argv[2]; title = sys.argv[3]
H = np.array(r['planes'], float); n = len(H); A = SF.Arrangement(H)
if 'solid' in r:
    tris = SF.extract_map(A, {tuple(x) for x in r['solid']})
else:                                                   # a map-based result: planes + dual triangles
    tris = [tuple(t) for t in r['triangles']]
L = links_from(coherent_triangles(tris), n); P = polygons(A.H, L)
V = np.vstack(list(P.values())); c = V.mean(0); s = np.abs(V - c).max()
Q = {X: (q - c) / s for X, q in P.items()}
fig = plt.figure(figsize=(16, 13), dpi=130)
for i, (el, az) in enumerate([(25, 30), (25, 120), (70, -60), (-20, 210)]):
    ax = fig.add_subplot(2, 2, i + 1, projection='3d')
    for X, q in Q.items():
        ax.add_collection3d(Poly3DCollection([q], facecolor=COL[X % 12], alpha=0.55, edgecolor='#222222', linewidths=0.7))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1); ax.set_box_aspect((1, 1, 1)); ax.view_init(el, az); ax.set_axis_off()
fig.suptitle(title, fontsize=14); plt.tight_layout(); fig.savefig(out + '.png', facecolor='white')
traces = []
for X, q in Q.items():
    m = len(q); cen = q.mean(0); Vt = np.vstack([cen, q])
    traces.append(dict(type='mesh3d', x=Vt[:, 0].tolist(), y=Vt[:, 1].tolist(), z=Vt[:, 2].tolist(), i=[0] * m,
                       j=list(range(1, m + 1)), k=[(k % m) + 1 for k in range(1, m + 1)], color=COL[X % 12], opacity=0.6,
                       name='face %d' % X))
    Qc = np.vstack([q, q[:1]])
    traces.append(dict(type='scatter3d', mode='lines', x=Qc[:, 0].tolist(), y=Qc[:, 1].tolist(), z=Qc[:, 2].tolist(),
                       line=dict(color='#222222', width=3), showlegend=False, hoverinfo='skip'))
html = ('<!doctype html><html><head><meta charset="utf-8"><title>%s</title><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.0/plotly.min.js"></script>'
        '<style>body{margin:0;background:#fff;font-family:sans-serif}#p{width:100vw;height:92vh}</style></head><body>'
        '<div style="padding:8px">%s - drag to rotate</div><div id="p"></div><script>Plotly.newPlot("p", %s, {scene:{aspectmode:"cube",'
        'xaxis:{visible:false},yaxis:{visible:false},zaxis:{visible:false}},margin:{l:0,r:0,t:0,b:0}});</script></body></html>'
        % (title, title, json.dumps(traces)))
open(out + '.html', 'w').write(html)
print('rendered', out, {X: len(q) for X, q in P.items()})
