"""Round-trip control (added after the run, PLAN Amendments): the polar planes of the Szilassi polyhedron (7 faces,
embedded, genus 1) are fed to the same pipeline as 7 points with the 14 triangles of its vertices. Some chart must
reproduce an embedded S6 (7, 1) object. Usage (research venv, from this folder): python3 control_szilassi.py OUT_DIR
Result 2026-11-16: 307 cells, 1 EMBEDDED, 1 PASS --target S6, 0 random patterns outside the enumerated cells."""
import sys,json
sys.path.insert(0,'.'); sys.path.insert(0,'../../verification'); sys.path.insert(0,'../../code')
from fractions import Fraction as Fr
import polar_transfer as P
V = [[-1.2, 0, 1.2], [1.2, 0, 1.2], [0, -1.26, -1.2], [0, 1.26, -1.2],[0.2, -0.5, -0.8], [-0.2, 0.5, -0.8], [-0.375, -0.375, -0.3], [0.375, 0.375, -0.3],[0.45, -0.25, 0.2], [-0.45, 0.25, 0.2], [-0.7, 0, 0.2], [0.7, 0, 0.2], [-0.7, -0.25, 0.2], [0.7, 0.25, 0.2]]
F = [[9, 7, 5, 2, 1, 13], [10, 8, 6, 1, 2, 14], [7, 8, 10, 11, 3, 5],[8, 7, 9, 12, 4, 6], [6, 4, 3, 11, 13, 1], [9, 12, 14, 10, 11, 13], [3, 5, 2, 14, 12, 4]]
V=[[Fr(str(x)) for x in v] for v in V]; F=[[i-1 for i in f] for f in F]
def plane(p,q,r):
    u=[q[i]-p[i] for i in range(3)]; w=[r[i]-p[i] for i in range(3)]
    n=[u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]]
    return n+[-sum(n[i]*p[i] for i in range(3))]
pl=[plane(*[V[i] for i in f[:3]]) for f in F]
# shift so every d != 0 (translation of the Szilassi model; a projective-affine image)
pts=[]
for h in pl:
    pts.append(tuple(float(x/h[3]) for x in h[:3]))
print([round(h[3],3) for h in [[float(x) for x in h] for h in pl]])
tri=[tuple(i for i,f in enumerate(F) if v in f) for v in range(14)]
assert all(len(t)==3 for t in tri)
import numpy as np
# exact integer points: scale to integers is not needed for cells (float x_F), but dual_vertices needs ints -> use rationals scaled
from math import lcm
den=lcm(*[Fr(x).limit_denominator(10**6).denominator for p in pts for x in p])
ip=[tuple(int(Fr(x).limit_denominator(10**6)*den) for x in p) for p in pts]
# h_i=(v_i,1) ~ (den*v, den)... pipeline uses (v,1): rescale coordinates by den is a projective map; use pts as ints scaled
res,rows=P.run(ip,tri,sys.argv[1],'S6')
print({k:v for k,v in res.items() if k!='passing_files'}, len(res['passing_files']))
