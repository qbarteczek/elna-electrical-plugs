import trimesh
import numpy as np

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Let's find the bounding box of the actual empty space for Bottom Left slot
# We look for the inner walls.
mask_bl = (mesh.vertices[:, 1] > 6.0) & (mesh.vertices[:, 1] < 11.0) & \
          (mesh.vertices[:, 0] > 17.0) & (mesh.vertices[:, 0] < 20.0) & \
          (mesh.vertices[:, 2] < 3.5)

v_bl = mesh.vertices[mask_bl]
print("Bottom left slot inner vertices:")
print(f"X: {v_bl[:, 0].min():.3f} to {v_bl[:, 0].max():.3f}")
print(f"Y: {v_bl[:, 1].min():.3f} to {v_bl[:, 1].max():.3f}")
print(f"Z: {v_bl[:, 2].min():.3f} to {v_bl[:, 2].max():.3f}")

# And Bottom Center slot
mask_bc = (mesh.vertices[:, 1] > 6.0) & (mesh.vertices[:, 1] < 11.0) & \
          (mesh.vertices[:, 0] > 26.0) & (mesh.vertices[:, 0] < 40.0) & \
          (mesh.vertices[:, 2] < 3.5)

v_bc = mesh.vertices[mask_bc]
print("Bottom center slot inner vertices:")
print(f"X: {v_bc[:, 0].min():.3f} to {v_bc[:, 0].max():.3f}")
print(f"Y: {v_bc[:, 1].min():.3f} to {v_bc[:, 1].max():.3f}")
print(f"Z: {v_bc[:, 2].min():.3f} to {v_bc[:, 2].max():.3f}")

