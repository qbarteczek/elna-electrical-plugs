import trimesh
import numpy as np

mesh = trimesh.load("elnaplug_widened_slots.stl")
slice_3d = mesh.section(plane_origin=[0,0,21.9], plane_normal=[0,0,1])
if slice_3d:
    slice_2d, _ = slice_3d.to_planar()
    polygons = slice_2d.polygons_full
    print("Z=21.9")
    for p in polygons:
        for interior in p.interiors:
            pts = list(interior.coords)
            print("  Hole:", pts)

slice_3d = mesh.section(plane_origin=[0,0,10.0], plane_normal=[0,0,1])
if slice_3d:
    slice_2d, _ = slice_3d.to_planar()
    polygons = slice_2d.polygons_full
    print("Z=10.0")
    for p in polygons:
        for interior in p.interiors:
            pts = list(interior.coords)
            print("  Hole:", pts)
