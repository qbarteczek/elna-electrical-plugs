import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Bottom right slot
mask_br = (mesh.vertices[:, 1] > 6.0) & (mesh.vertices[:, 1] < 15.0) & \
          (mesh.vertices[:, 0] > 40.0) & (mesh.vertices[:, 0] < 50.0) & \
          (mesh.vertices[:, 2] < 3.5)

v_br = mesh.vertices[mask_br]
print("Bottom right slot:")
print(f"X: {v_br[:, 0].min():.3f} to {v_br[:, 0].max():.3f}")
print(f"Y: {v_br[:, 1].min():.3f} to {v_br[:, 1].max():.3f}")
print(f"Z: {v_br[:, 2].min():.3f} to {v_br[:, 2].max():.3f}")
