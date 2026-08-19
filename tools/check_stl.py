import trimesh
import numpy as np

mesh = trimesh.load("elnaplug_widened_slots.stl")
slice_3d = mesh.section(plane_origin=[0,0,10.0], plane_normal=[0,0,1])
lines = slice_3d.discrete
for idx, line in enumerate(lines):
    min_xy = np.min(line, axis=0)
    max_xy = np.max(line, axis=0)
    center = (min_xy + max_xy) / 2
    width = max_xy[0] - min_xy[0]
    height = max_xy[1] - min_xy[1]
    print(f"Contour {idx}: Center: X={center[0]:.2f}, Y={center[1]:.2f} | W={width:.2f}, H={height:.2f}")
