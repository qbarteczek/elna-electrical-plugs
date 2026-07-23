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

# Find holes at the front tip (around Y = 36)
front_tris = [t for t in tris if all(v[1] > 20 for v in (t[1], t[2], t[3]))]

print(f"Total triangles near front (Y > 20): {len(front_tris)}")

# Let's slice at Y = 30 mm and find all X intervals that are hollow or solid
# Create a 2D grid at Y = 30 and Y = 36 to inspect cross section
def print_slice(y_val):
    print(f"\n--- Cross Section at Y = {y_val} mm ---")
    grid_x = [round(x, 1) for x in [16 + i*0.5 for i in range(66)]] # X from 16 to 49
    grid_z = [round(z, 1) for z in [i*0.5 for i in range(17)]] # Z from 0 to 8
    
    # Check triangles that intersect this Y plane
    slice_tris = []
    for norm, v1, v2, v3 in tris:
        y_coords = [v1[1], v2[1], v3[1]]
        if min(y_coords) <= y_val <= max(y_coords):
            slice_tris.append((v1, v2, v3))
            
    print(f"Number of intersecting triangles at Y={y_val}: {len(slice_tris)}")

print_slice(36.0)
print_slice(30.0)
print_slice(20.0)
print_slice(-10.0)
