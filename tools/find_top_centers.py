import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

mask_tl = (mesh.vertices[:, 1] < -20.0) & (mesh.vertices[:, 1] > -40.0) & \
          (mesh.vertices[:, 0] > 12.0) & (mesh.vertices[:, 0] < 20.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_tl = mesh.vertices[mask_tl]
print(f"Top left center: X={(v_tl[:,0].min()+v_tl[:,0].max())/2:.3f}, Y={(v_tl[:,1].min()+v_tl[:,1].max())/2:.3f}")

mask_tc = (mesh.vertices[:, 1] < -20.0) & (mesh.vertices[:, 1] > -40.0) & \
          (mesh.vertices[:, 0] > 26.0) & (mesh.vertices[:, 0] < 40.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_tc = mesh.vertices[mask_tc]
print(f"Top center center: X={(v_tc[:,0].min()+v_tc[:,0].max())/2:.3f}, Y={(v_tc[:,1].min()+v_tc[:,1].max())/2:.3f}")
