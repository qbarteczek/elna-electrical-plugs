import trimesh
import numpy as np
from shapely.geometry import Polygon

mesh = trimesh.load("stls/elnaplug-elnasuperv1.5.stl")
slice_3d = mesh.section(plane_origin=[0,0,10.0], plane_normal=[0,0,1])
slice_2d, _ = slice_3d.to_planar()
polygons = slice_2d.polygons_full
for p in polygons:
    for interior in p.interiors:
        pts = list(interior.coords)
        print("Hole contour points:")
        for pt in pts:
            print(f"  {pt[0]:.2f}, {pt[1]:.2f}")
