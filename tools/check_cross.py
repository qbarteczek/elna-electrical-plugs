import trimesh
import numpy as np
mesh = trimesh.load("stls/elnaplug-elnasuperv1.5.stl")
slice_3d = mesh.section(plane_origin=[0,0,0], plane_normal=[1,0,0])
if slice_3d:
    slice_2d, _ = slice_3d.to_planar()
    print("ORIGINAL")
    for p in slice_2d.polygons_full:
        print("  Exterior:", list(p.exterior.coords))

mesh2 = trimesh.load("elnaplug_widened_slots.stl")
slice_3d2 = mesh2.section(plane_origin=[0,0,0], plane_normal=[1,0,0])
if slice_3d2:
    slice_2d2, _ = slice_3d2.to_planar()
    print("\n\nWIDENED")
    for p in slice_2d2.polygons_full:
        print("  Exterior:", list(p.exterior.coords))
