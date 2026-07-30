import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Find center of left pin hole (by finding the deepest/lowest Z point?)
# Or just average X and Y of the hole vertices
mask_bl = (mesh.vertices[:, 1] > 6.0) & (mesh.vertices[:, 1] < 15.0) & \
          (mesh.vertices[:, 0] > 12.0) & (mesh.vertices[:, 0] < 20.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_bl = mesh.vertices[mask_bl]
cx_l = (v_bl[:, 0].min() + v_bl[:, 0].max()) / 2
cy_l = (v_bl[:, 1].min() + v_bl[:, 1].max()) / 2
print(f"Left center: X={cx_l:.3f}, Y={cy_l:.3f}")

mask_bc = (mesh.vertices[:, 1] > 2.0) & (mesh.vertices[:, 1] < 11.0) & \
          (mesh.vertices[:, 0] > 26.0) & (mesh.vertices[:, 0] < 40.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_bc = mesh.vertices[mask_bc]
cx_c = (v_bc[:, 0].min() + v_bc[:, 0].max()) / 2
cy_c = (v_bc[:, 1].min() + v_bc[:, 1].max()) / 2
print(f"Center center: X={cx_c:.3f}, Y={cy_c:.3f}")

mask_br = (mesh.vertices[:, 1] > 10.0) & (mesh.vertices[:, 1] < 19.0) & \
          (mesh.vertices[:, 0] > 40.0) & (mesh.vertices[:, 0] < 50.0) & \
          (mesh.vertices[:, 2] < 3.5)
v_br = mesh.vertices[mask_br]
cx_r = (v_br[:, 0].min() + v_br[:, 0].max()) / 2
cy_r = (v_br[:, 1].min() + v_br[:, 1].max()) / 2
print(f"Right center: X={cx_r:.3f}, Y={cy_r:.3f}")
