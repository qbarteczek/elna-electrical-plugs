import trimesh

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Let's find vertices forming the inner walls of the bottom center slot
# Center is X=32.8, Y=8.3. 
# We look for points near X=27 (left end)
mask_left_end = (mesh.vertices[:, 0] > 26.5) & (mesh.vertices[:, 0] < 27.5) & \
                (mesh.vertices[:, 1] > 6.0) & (mesh.vertices[:, 1] < 10.0)
print("Bottom center left end:")
print(mesh.vertices[mask_left_end])

# Points near Y=8.3 (bottom of the slot?)
mask_bottom = (mesh.vertices[:, 0] > 32.0) & (mesh.vertices[:, 0] < 33.5) & \
              (mesh.vertices[:, 1] > 8.0) & (mesh.vertices[:, 1] < 8.6)
print("Bottom center floor/ceiling:")
print(mesh.vertices[mask_bottom])

