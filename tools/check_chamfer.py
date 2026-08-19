import trimesh
import numpy as np

mesh = trimesh.load("stls/elnaplug-elnasuperv1.5.stl")
slice_3d = mesh.section(plane_origin=[0,0,21.9], plane_normal=[0,0,1])
slice_2d, _ = slice_3d.to_planar()
polygons = slice_2d.polygons_full
for p in polygons:
    for interior in p.interiors:
        pts = list(interior.coords)
        xs = [pt[0] for pt in pts]
        ys = [pt[1] for pt in pts]
        print(f"Z=21.9 Hole: X={min(xs):.2f} to {max(xs):.2f}, Y={min(ys):.2f} to {max(ys):.2f} (W={max(xs)-min(xs):.2f}, H={max(ys)-min(ys):.2f})")
