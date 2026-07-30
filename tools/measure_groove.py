import trimesh
import numpy as np

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Measure left groove in top piece
mask_left_top = (mesh.vertices[:, 2] < 7.0) & (mesh.vertices[:, 0] > 19.57 - 5.0) & (mesh.vertices[:, 0] < 19.57 + 5.0) & (mesh.vertices[:, 1] < -10)
verts_left_top = mesh.vertices[mask_left_top]

y_vals = np.sort(verts_left_top[:, 1])
print(f"Top half left groove Y min: {y_vals[0]:.2f}, Y max: {y_vals[-1]:.2f}")

hist, bins = np.histogram(verts_left_top[:, 1], bins=20)
for i in range(len(hist)):
    if hist[i] > 0:
        print(f"Y from {bins[i]:.2f} to {bins[i+1]:.2f}: {hist[i]} vertices")
