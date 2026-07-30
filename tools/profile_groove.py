import trimesh
import numpy as np

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Find center of left pin hole
mask_lp = (mesh.vertices[:, 1] > 33.0) & (mesh.vertices[:, 1] < 37.0) & \
          (mesh.vertices[:, 0] > 15.0) & (mesh.vertices[:, 0] < 22.0)
v_lp = mesh.vertices[mask_lp]
c_lp = (v_lp[:, 0].min() + v_lp[:, 0].max()) / 2

# Find center of middle pin hole
mask_mp = (mesh.vertices[:, 1] > 33.0) & (mesh.vertices[:, 1] < 37.0) & \
          (mesh.vertices[:, 0] > 29.0) & (mesh.vertices[:, 0] < 35.0)
v_mp = mesh.vertices[mask_mp]
c_mp = (v_mp[:, 0].min() + v_mp[:, 0].max()) / 2

print(f"Left pin hole center: {c_lp:.3f}")
print(f"Middle pin hole center: {c_mp:.3f}")
print(f"Distance: {c_mp - c_lp:.3f}")

# Verify left slot center
mask_left = (mesh.vertices[:, 1] > 0.0) & (mesh.vertices[:, 1] < 17.0) & \
          (mesh.vertices[:, 0] > 14.0) & (mesh.vertices[:, 0] < 24.0) & \
          (mesh.vertices[:, 2] < 7.0)
v_l = mesh.vertices[mask_left]
c_l = (v_l[:, 0].min() + v_l[:, 0].max()) / 2
print(f"Left slot center: {c_l:.3f}")
print(f"Translation to middle: {c_mp - c_l:.3f}")
print(f"Should be middle center: {c_l + (c_mp - c_lp):.3f}")
