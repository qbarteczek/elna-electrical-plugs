import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Check Z bounds of the plug at X=10..20, Y=8..15
mask = (mesh.vertices[:, 0] > 10.0) & (mesh.vertices[:, 0] < 20.0) & \
       (mesh.vertices[:, 1] > 8.0) & (mesh.vertices[:, 1] < 15.0)
v = mesh.vertices[mask]
print(f"At X=10..20, Y=8..15, Z goes from {v[:, 2].min():.3f} to {v[:, 2].max():.3f}")

