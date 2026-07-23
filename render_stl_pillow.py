import struct
import math
from PIL import Image, ImageDraw

def load_stl(filename):
    tris = []
    with open(filename, "rb") as f:
        header = f.read(80)
        if header.startswith(b"solid") and not b"facet" in header[:20]:
            # Could be ASCII or binary with solid header
            pass
        
        # Try ASCII first
        f.seek(0)
        lines = f.readlines()
        if lines[0].strip().startswith(b"solid") and any(b"facet" in l for l in lines[:10]):
            # ASCII STL
            norm = (0, 0, 1)
            v1 = v2 = v3 = None
            pts = []
            for line in lines:
                line_str = line.decode('utf-8', errors='ignore').strip()
                if line_str.startswith("facet normal"):
                    parts = line_str.split()
                    norm = (float(parts[2]), float(parts[3]), float(parts[4]))
                elif line_str.startswith("vertex"):
                    parts = line_str.split()
                    pts.append((float(parts[1]), float(parts[2]), float(parts[3])))
                    if len(pts) == 3:
                        tris.append((norm, pts[0], pts[1], pts[2]))
                        pts = []
            return tris

    # Binary fallback
    with open(filename, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        for _ in range(n):
            d = struct.unpack("<12fH", f.read(50))
            norm = d[0:3]
            v1, v2, v3 = d[3:6], d[6:9], d[9:12]
            tris.append((norm, v1, v2, v3))
    return tris

def normalize(v):
    l = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    if l == 0: return (0, 0, 1)
    return (v[0]/l, v[1]/l, v[2]/l)

def cross(u, v):
    return (
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0]
    )

def sub(u, v):
    return (u[0]-v[0], u[1]-v[1], u[2]-v[2])

def dot(u, v):
    return u[0]*v[0] + u[1]*v[0]*0 + u[2]*v[2]

def rotate_pt(pt, rot_x, rot_z):
    x, y, z = pt
    # rot Z
    rad_z = math.radians(rot_z)
    cz, sz = math.cos(rad_z), math.sin(rad_z)
    rx = x * cz - y * sz
    ry = x * sz + y * cz
    rz = z
    
    # rot X
    rad_x = math.radians(rot_x)
    cx, sx = math.cos(rad_x), math.sin(rad_x)
    fx = rx
    fy = ry * cx - rz * sx
    fz = ry * sx + rz * cx
    return (fx, fy, fz)

def render_mesh(stl_path, out_png, width=1200, height=900, rot_x=65, rot_z=45, base_color=(60, 140, 230)):
    tris = load_stl(stl_path)
    print(f"Loaded {len(tris)} triangles from {stl_path}")
    
    all_pts = []
    for norm, v1, v2, v3 in tris:
        all_pts.extend([v1, v2, v3])
    
    min_x = min(p[0] for p in all_pts)
    max_x = max(p[0] for p in all_pts)
    min_y = min(p[1] for p in all_pts)
    max_y = max(p[1] for p in all_pts)
    min_z = min(p[2] for p in all_pts)
    max_z = max(p[2] for p in all_pts)
    
    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    cz = (min_z + max_z) / 2.0
    
    rot_tris = []
    light_dir = normalize((0.6, 0.4, 0.8))
    
    transformed_pts = []
    for norm, v1, v2, v3 in tris:
        p1 = (v1[0]-cx, v1[1]-cy, v1[2]-cz)
        p2 = (v2[0]-cx, v2[1]-cy, v2[2]-cz)
        p3 = (v3[0]-cx, v3[1]-cy, v3[2]-cz)
        
        rp1 = rotate_pt(p1, rot_x, rot_z)
        rp2 = rotate_pt(p2, rot_x, rot_z)
        rp3 = rotate_pt(p3, rot_x, rot_z)
        
        transformed_pts.extend([rp1, rp2, rp3])
        
        u = sub(rp2, rp1)
        v = sub(rp3, rp1)
        fn = normalize(cross(u, v))
        
        avg_z = (rp1[2] + rp2[2] + rp3[2]) / 3.0
        
        # Diffuse + Specular
        diff = max(0.0, dot(fn, light_dir))
        intensity = 0.3 + 0.7 * diff
        
        r = int(min(255, max(0, base_color[0] * intensity)))
        g = int(min(255, max(0, base_color[1] * intensity)))
        b = int(min(255, max(0, base_color[2] * intensity)))
        
        rot_tris.append((avg_z, [rp1, rp2, rp3], (r, g, b)))
        
    rot_tris.sort(key=lambda t: t[0])
    
    min_rx = min(p[0] for p in transformed_pts)
    max_rx = max(p[0] for p in transformed_pts)
    min_ry = min(p[1] for p in transformed_pts)
    max_ry = max(p[1] for p in transformed_pts)
    
    span_x = max_rx - min_rx
    span_y = max_ry - min_ry
    
    scale = min((width - 160) / span_x, (height - 160) / span_y)
    
    img = Image.new("RGBA", (width, height), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    grid_color = (230, 235, 242, 255)
    for gx in range(0, width, 40):
        draw.line([(gx, 0), (gx, height)], fill=grid_color)
    for gy in range(0, height, 40):
        draw.line([(0, gy), (width, gy)], fill=grid_color)
        
    canvas_cx = width / 2.0
    canvas_cy = height / 2.0
    
    for avg_z, pts, color in rot_tris:
        poly_2d = []
        for pt in pts:
            sx = canvas_cx + pt[0] * scale
            sy = canvas_cy - pt[1] * scale
            poly_2d.append((sx, sy))
            
        outline_c = (max(0, color[0]-25), max(0, color[1]-25), max(0, color[2]-25))
        draw.polygon(poly_2d, fill=color, outline=outline_c)
        
    img.save(out_png, "PNG")
    print(f"Rendered 3D image saved to {out_png}")

# Render both STL files and original reference STL
render_mesh("stls/exports/elna_plug_modified_bottom.stl", "renders/preview_modified.png", rot_x=60, rot_z=35, base_color=(50, 130, 230))
render_mesh("stls/exports/elna_plug_modified_top.stl", "renders/preview_top.png", rot_x=60, rot_z=215, base_color=(40, 170, 110))
render_mesh("references/original_zip/files/ELNA_SUPERMATIC_PLUG.stl", "renders/preview_both.png", rot_x=60, rot_z=35, base_color=(220, 120, 50))
