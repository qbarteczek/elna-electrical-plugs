import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Left slot is near X=16.0, Y=12.2
# Find all vertices in a small box around it, and plot their X, Y bounds
mask = (mesh.vertices[:, 0] > 14.0) & (mesh.vertices[:, 0] < 18.0) & \
       (mesh.vertices[:, 1] > 9.0) & (mesh.vertices[:, 1] < 15.0) & \
       (mesh.vertices[:, 2] > 0.5) & (mesh.vertices[:, 2] < 2.5)

v = mesh.vertices[mask]
print("Left Slot Cavity Bounds:")
print(f"X: {v[:, 0].min():.3f} to {v[:, 0].max():.3f} (Width: {v[:, 0].max()-v[:, 0].min():.3f})")
print(f"Y: {v[:, 1].min():.3f} to {v[:, 1].max():.3f} (Length: {v[:, 1].max()-v[:, 1].min():.3f})")
