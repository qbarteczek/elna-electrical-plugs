import struct

def load_stl(filename):
    tris = []
    with open(filename, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        for _ in range(n):
            d = struct.unpack("<12fH", f.read(50))
            tris.append((d[3:6], d[6:9], d[9:12]))
    return tris

tris = load_stl("references/original_zip/files/ELNA_SUPERMATIC_PLUG.stl")

# Function to get 2D line segments at a plane Y = y_plane
def get_slice_segments(y_plane):
    segments = []
    for v1, v2, v3 in tris:
        # Check edges
        pts = []
        for (a, b) in [(v1, v2), (v2, v3), (v3, v1)]:
            (x1, y1, z1), (x2, y2, z2) = a, b
            if (y1 <= y_plane <= y2) or (y2 <= y_plane <= y1):
                if y1 != y2:
                    t = (y_plane - y1) / (y2 - y1)
                    x = x1 + t * (x2 - x1)
                    z = z1 + t * (z2 - z1)
                    pts.append((x, z))
        if len(pts) == 2:
            segments.append((pts[0], pts[1]))
    return segments

# Let's inspect the slice at Y = 35.0 (Front tip where pins exit)
segs = get_slice_segments(35.0)
print(f"Slice at Y = 35.0 mm: {len(segs)} segments")

# Print X range of segments
xs = [p[0] for s in segs for p in s]
zs = [p[1] for s in segs for p in s]
if xs:
    print(f"X range at Y=35: {min(xs):.2f} to {max(xs):.2f}")
    print(f"Z range at Y=35: {min(zs):.2f} to {max(zs):.2f}")

# Let's render a 2D ASCII grid of the cross section at Y = 35.0 (resolution 0.5mm)
def render_ascii_slice(y_val):
    segs = get_slice_segments(y_val)
    if not segs:
        print(f"No segments at Y={y_val}")
        return
    
    # We sample a ray cast from -X to +X at different Z levels
    print(f"\n================ CROSS SECTION AT Y = {y_val:.1f} mm ================")
    grid = []
    for z in [i*0.5 for i in range(17)]: # Z from 0 to 8mm
        row = []
        for x in [16 + i*0.5 for i in range(66)]: # X from 16 to 49mm
            # Count ray crossings to test inside/outside
            crossings = 0
            for (p1, p2) in segs:
                (x1, z1), (x2, z2) = p1, p2
                if (z1 <= z < z2) or (z2 <= z < z1):
                    if z1 != z2:
                        x_int = x1 + (z - z1) * (x2 - x1) / (z2 - z1)
                        if x_int > x:
                            crossings += 1
            row.append('#' if (crossings % 2 == 1) else '.')
        grid.append(f"{z:4.1f} | " + "".join(row))
    print("\n".join(reversed(grid)))

render_ascii_slice(35.0)
render_ascii_slice(25.0)
render_ascii_slice(0.0)
render_ascii_slice(-30.0)

