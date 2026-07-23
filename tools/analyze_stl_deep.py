import struct

def get_triangles(filename):
    tris = []
    with open(filename, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        for _ in range(n):
            d = struct.unpack("<12fH", f.read(50))
            tris.append((d[0:3], d[3:6], d[6:9], d[9:12]))
    return tris

tris = get_triangles("references/original_zip/files/ELNA_SUPERMATIC_PLUG.stl")

# Get all vertices
verts = []
for norm, v1, v2, v3 in tris:
    verts.extend([v1, v2, v3])

min_x, max_x = min(v[0] for v in verts), max(v[0] for v in verts)
min_y, max_y = min(v[1] for v in verts), max(v[1] for v in verts)
min_z, max_z = min(v[2] for v in verts), max(v[2] for v in verts)

print("=== GLOBAL BOUNDING BOX ===")
print(f"X: {min_x:.3f} to {max_x:.3f} (Width: {max_x - min_x:.3f} mm)")
print(f"Y: {min_y:.3f} to {max_y:.3f} (Length: {max_y - min_y:.3f} mm)")
print(f"Z: {min_z:.3f} to {max_z:.3f} (Height: {max_z - min_z:.3f} mm)")

# Slice Y into 10mm segments to see profile evolution
y_steps = range(int(min_y), int(max_y), 5)
print("\n=== PROFILE EVOLUTION ALONG Y (LENGTH) ===")
for y_start in y_steps:
    y_end = y_start + 5
    v_in_slice = [v for v in verts if y_start <= v[1] < y_end]
    if v_in_slice:
        sx_min = min(v[0] for v in v_in_slice)
        sx_max = max(v[0] for v in v_in_slice)
        sz_min = min(v[2] for v in v_in_slice)
        sz_max = max(v[2] for v in v_in_slice)
        print(f"Y [{y_start:3d} .. {y_end:3d} mm]: X span = {sx_max-sx_min:5.2f} mm (X: {sx_min:5.2f}..{sx_max:5.2f}), Z span = {sz_max-sz_min:5.2f} mm (Z: {sz_min:5.2f}..{sz_max:5.2f})")

