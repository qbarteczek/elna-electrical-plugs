import trimesh

mesh = trimesh.load('stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl')
print(f"Final mesh has {len(mesh.vertices)} vertices and {len(mesh.faces)} faces.")
print(f"Is watertight: {mesh.is_watertight}")
