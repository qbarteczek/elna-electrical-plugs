import trimesh

cut = trimesh.load('stls/exports/modifier_cut.stl')
print(f"modifier_cut bounds:")
print(f"X: {cut.bounds[0,0]:.3f} to {cut.bounds[1,0]:.3f} (Width: {cut.bounds[1,0]-cut.bounds[0,0]:.3f})")
print(f"Y: {cut.bounds[0,1]:.3f} to {cut.bounds[1,1]:.3f} (Depth: {cut.bounds[1,1]-cut.bounds[0,1]:.3f})")
print(f"Z: {cut.bounds[0,2]:.3f} to {cut.bounds[1,2]:.3f} (Height: {cut.bounds[1,2]-cut.bounds[0,2]:.3f})")

