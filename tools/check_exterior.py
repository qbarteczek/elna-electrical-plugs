import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

mask = (mesh.vertices[:, 1] > 10.0) & (mesh.vertices[:, 1] < 13.0) & \
       (mesh.vertices[:, 2] > 1.0) & (mesh.vertices[:, 2] < 2.0)
v = mesh.vertices[mask]
print(f"At Y=10-13, Z=1-2, X goes from {v[:, 0].min():.3f} to {v[:, 0].max():.3f}")

mask2 = (mesh.vertices[:, 1] > 10.0) & (mesh.vertices[:, 1] < 13.0) & \
       (mesh.vertices[:, 2] > 4.0) & (mesh.vertices[:, 2] < 5.0)
v2 = mesh.vertices[mask2]
print(f"At Y=10-13, Z=4-5, X goes from {v2[:, 0].min():.3f} to {v2[:, 0].max():.3f}")
