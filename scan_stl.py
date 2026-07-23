import struct
import sys

def point_in_triangle_2d(p, a, b, c):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def scan(filename, z_slice):
    triangles = []
    with open(filename, "rb") as f:
        f.read(80)
        num_triangles = struct.unpack("<I", f.read(4))[0]
        for _ in range(num_triangles):
            data = struct.unpack("<12fH", f.read(50))
            v1, v2, v3 = data[3:6], data[6:9], data[9:12]
            
            # If triangle crosses Z slice
            zmin = min(v1[2], v2[2], v3[2])
            zmax = max(v1[2], v2[2], v3[2])
            if zmin <= z_slice <= zmax:
                triangles.append((v1, v2, v3))
                
    # We will just do a simple grid
    minx, maxx = 0, 48
    miny, maxy = -63, 36
    
    # Let's project triangles intersecting the Z slice to 2D
    # This is a very crude intersection, actually we just check if 2D point is in any 2D projected triangle
    # of the ones that cross Z. It's an approximation but good enough for ASCII art.
    
    out = []
    for y in range(int(maxy), int(miny)-1, -2):
        row = []
        for x in range(int(minx), int(maxx)+1, 1):
            hit = False
            for t in triangles:
                if point_in_triangle_2d((x, y), t[0][:2], t[1][:2], t[2][:2]):
                    hit = True
                    break
            row.append('#' if hit else ' ')
        out.append("".join(row))
    
    print("\n".join(out))

scan("stls/ELNA_SUPERMATIC_PLUG.stl", 4.0)
