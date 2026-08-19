import trimesh
import numpy as np

def dump_slices(filepath):
    mesh = trimesh.load(filepath)
    bounds = mesh.bounds
    z_min, z_max = bounds[0][2], bounds[1][2]
    
    # We slice across Z
    slice_3d = mesh.section(plane_origin=[0,0,10.0], plane_normal=[0,0,1])
    if slice_3d is not None:
        lines = slice_3d.discrete
        print(f"\n--- Z = 10.0 ---")
        for idx, line in enumerate(lines):
            min_xy = np.min(line, axis=0)
            max_xy = np.max(line, axis=0)
            center = (min_xy + max_xy) / 2
            width = max_xy[0] - min_xy[0]
            height = max_xy[1] - min_xy[1]
            print(f"Contour {idx}: Center: X={center[0]:.2f}, Y={center[1]:.2f} | W={width:.2f}, H={height:.2f}")

dump_slices("stls/elnaplug-elnasuperv1.5.stl")
