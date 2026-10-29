from track4_common import *
import re

def load_szilassi():
    src = open(os.path.join(HERE, "..", "..", "..", "index.html")).read()
    i = src.index("szilassi: {")
    blk = src[i:i + 2500]
    vs = re.search(r"vertices:\s*\[(.*?)\],\s*\n\s*//", blk, re.S).group(1)
    verts = [tuple(Fraction(x) for x in m.split(",")) for m in re.findall(r"\[([^\]]+)\]", vs)]
    fs = re.search(r"faces:\s*\[(.*?)\],\s*\n\s*colors", blk, re.S).group(1)
    faces = [[int(x) - 1 for x in m.split(",")] for m in re.findall(r"\[([^\]]+)\]", fs)]
    return verts, faces

def szilassi_arr():
    verts, faces = load_szilassi()
    H = planes_from_polyhedron(verts, faces)
    tris = {}
    for v in range(len(verts)):
        fl = tuple(sorted(i for i, f in enumerate(faces) if v in f))
        assert len(fl) == 3, (v, fl)
        tris[fl] = 1
    return verts, faces, H, sorted(tris)

if __name__ == "__main__":
    verts, faces, H, tris = szilassi_arr()
    print("nverts", len(verts), "faces", faces)
    print("planes", H)
    print("triangles(dual)", tris, len(tris), "valid:", valid_triangulation(tris, 7))
    arr = Arrangement(H)
    print("GP:", arr.check_general_position(), arr.check_general_position_dets())
