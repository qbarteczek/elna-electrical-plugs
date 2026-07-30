import trimesh
import numpy as np

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Measure bottom center slot
mask_bc = (mesh.vertices[:, 1] > 2.0) & (mesh.vertices[:, 1] < 14.0) & \
          (mesh.vertices[:, 0] > 26.0) & (mesh.vertices[:, 0] < 40.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_bc = mesh.vertices[mask_bc]
print("Bottom center slot:")
print(f"X: {v_bc[:, 0].min():.3f} to {v_bc[:, 0].max():.3f}")
print(f"Y: {v_bc[:, 1].min():.3f} to {v_bc[:, 1].max():.3f}")
print(f"Z: {v_bc[:, 2].min():.3f} to {v_bc[:, 2].max():.3f}")

# Measure bottom left slot
mask_bl = (mesh.vertices[:, 1] > 2.0) & (mesh.vertices[:, 1] < 14.0) & \
          (mesh.vertices[:, 0] > 12.0) & (mesh.vertices[:, 0] < 26.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_bl = mesh.vertices[mask_bl]
print("Bottom left slot:")
print(f"X: {v_bl[:, 0].min():.3f} to {v_bl[:, 0].max():.3f}")
print(f"Y: {v_bl[:, 1].min():.3f} to {v_bl[:, 1].max():.3f}")
print(f"Z: {v_bl[:, 2].min():.3f} to {v_bl[:, 2].max():.3f}")

# Measure top center slot
mask_tc = (mesh.vertices[:, 1] < -20.0) & (mesh.vertices[:, 1] > -40.0) & \
          (mesh.vertices[:, 0] > 26.0) & (mesh.vertices[:, 0] < 40.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_tc = mesh.vertices[mask_tc]
print("Top center slot:")
print(f"X: {v_tc[:, 0].min():.3f} to {v_tc[:, 0].max():.3f}")
print(f"Y: {v_tc[:, 1].min():.3f} to {v_tc[:, 1].max():.3f}")
print(f"Z: {v_tc[:, 2].min():.3f} to {v_tc[:, 2].max():.3f}")

# Measure top left slot
mask_tl = (mesh.vertices[:, 1] < -20.0) & (mesh.vertices[:, 1] > -40.0) & \
          (mesh.vertices[:, 0] > 12.0) & (mesh.vertices[:, 0] < 26.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_tl = mesh.vertices[mask_tl]
print("Top left slot:")
print(f"X: {v_tl[:, 0].min():.3f} to {v_tl[:, 0].max():.3f}")
print(f"Y: {v_tl[:, 1].min():.3f} to {v_tl[:, 1].max():.3f}")
print(f"Z: {v_tl[:, 2].min():.3f} to {v_tl[:, 2].max():.3f}")

