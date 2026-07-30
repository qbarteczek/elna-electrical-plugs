import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')
print(f"Plug X bounds: {mesh.bounds[0,0]:.3f} to {mesh.bounds[1,0]:.3f}")
