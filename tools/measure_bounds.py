import trimesh
import numpy as np

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Find the Z of the exterior shell at top center
# X around 32.8, Y around -30.0
mask_top = (mesh.vertices[:, 1] > -32.0) & (mesh.vertices[:, 1] < -28.0) & \
           (mesh.vertices[:, 0] > 31.0) & (mesh.vertices[:, 0] < 34.0)

v_top = mesh.vertices[mask_top]
print(f"Top piece at X=32.8, Y=-30.0 has Z from {v_top[:, 2].min():.3f} to {v_top[:, 2].max():.3f}")

# Find the Z of the exterior shell at bottom center
# X around 32.8, Y around 8.0
mask_bot = (mesh.vertices[:, 1] > 6.0) & (mesh.vertices[:, 1] < 10.0) & \
           (mesh.vertices[:, 0] > 31.0) & (mesh.vertices[:, 0] < 34.0)

v_bot = mesh.vertices[mask_bot]
print(f"Bottom piece at X=32.8, Y=8.0 has Z from {v_bot[:, 2].min():.3f} to {v_bot[:, 2].max():.3f}")

