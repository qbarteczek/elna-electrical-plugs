import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

print(f"Whole mesh Z bounds: {mesh.bounds[0,2]:.3f} to {mesh.bounds[1,2]:.3f}")

# Top piece bounding box
mask_top_piece = (mesh.vertices[:, 1] < -18.0)
v_top = mesh.vertices[mask_top_piece]
print(f"Top piece Z bounds: {v_top[:, 2].min():.3f} to {v_top[:, 2].max():.3f}")

# Bottom piece bounding box
mask_bot_piece = (mesh.vertices[:, 1] > 0.0)
v_bot = mesh.vertices[mask_bot_piece]
print(f"Bottom piece Z bounds: {v_bot[:, 2].min():.3f} to {v_bot[:, 2].max():.3f}")
