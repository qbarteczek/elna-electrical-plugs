import struct
import sys

def stl_bounds(filename):
    with open(filename, "rb") as f:
        header = f.read(80)
        num_triangles = struct.unpack("<I", f.read(4))[0]
        
        minx = miny = minz = float('inf')
        maxx = maxy = maxz = float('-inf')
        
        for _ in range(num_triangles):
            # 12 floats: normal (3), v1 (3), v2 (3), v3 (3), attribute byte count (1 uint16)
            data = struct.unpack("<12fH", f.read(50))
            vertices = data[3:12]
            xs = vertices[0::3]
            ys = vertices[1::3]
            zs = vertices[2::3]
            
            minx, maxx = min(minx, *xs), max(maxx, *xs)
            miny, maxy = min(miny, *ys), max(maxy, *ys)
            minz, maxz = min(minz, *zs), max(maxz, *zs)
            
    print(f"X: {minx:.2f} to {maxx:.2f} (Width: {maxx-minx:.2f})")
    print(f"Y: {miny:.2f} to {maxy:.2f} (Length: {maxy-miny:.2f})")
    print(f"Z: {minz:.2f} to {maxz:.2f} (Height: {maxz-minz:.2f})")

stl_bounds("stls/ELNA_SUPERMATIC_PLUG.stl")
