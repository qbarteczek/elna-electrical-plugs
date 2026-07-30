import struct

with open('stls/ELNA_SUPERMATIC_PLUG.stl', 'rb') as f:
    f.read(80)
    n = struct.unpack('<I', f.read(4))[0]
    tris = [struct.unpack('<12fH', f.read(50)) for _ in range(n)]

p1_pts = []
p2_pts = []

for t in tris:
    avg_y = sum(t[4:12:3])/3
    pts = [(t[3],t[4],t[5]), (t[6],t[7],t[8]), (t[9],t[10],t[11])]
    if avg_y > 0:
        p1_pts.extend(pts)
    else:
        p2_pts.extend(pts)

def get_y_bounds(pts, x_min, x_max, z_max):
    filtered = [p[1] for p in pts if x_min < p[0] < x_max and p[2] < z_max]
    if filtered:
        return min(filtered), max(filtered)
    return None, None

print(f"Piece 1 Y bounds: {min(p[1] for p in p1_pts):.2f} to {max(p[1] for p in p1_pts):.2f}")
print(f"Piece 1 Left Hole Y bounds: {get_y_bounds(p1_pts, 18.0, 21.0, 7.0)}")

print(f"Piece 2 Y bounds: {min(p[1] for p in p2_pts):.2f} to {max(p[1] for p in p2_pts):.2f}")
print(f"Piece 2 Left Hole Y bounds: {get_y_bounds(p2_pts, 18.0, 21.0, 7.0)}")
