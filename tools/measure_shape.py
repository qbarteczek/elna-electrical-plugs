import trimesh
import numpy as np

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Let's find vertices in the bottom center groove
# X: 26.7 to 38.8. Center X is 32.79
# Y: 0.2 to 16.4. Center Y is 8.3
mask_bc = (mesh.vertices[:, 1] > 0.0) & (mesh.vertices[:, 1] < 17.0) & \
          (mesh.vertices[:, 0] > 26.0) & (mesh.vertices[:, 0] < 40.0) & \
          (mesh.vertices[:, 2] < 7.0)

v = mesh.vertices[mask_bc]
hist, bins = np.histogram(v[:, 0], bins=20)
print("Bottom Center X distribution:")
for i in range(len(hist)):
    if hist[i] > 0:
        print(f"X {bins[i]:.2f} - {bins[i+1]:.2f}: {hist[i]} vertices")

# Top Center
mask_tc = (mesh.vertices[:, 1] > -35.0) & (mesh.vertices[:, 1] < -18.0) & \
          (mesh.vertices[:, 0] > 26.0) & (mesh.vertices[:, 0] < 40.0) & \
          (mesh.vertices[:, 2] < 7.0)

v2 = mesh.vertices[mask_tc]
hist2, bins2 = np.histogram(v2[:, 0], bins=20)
print("\nTop Center X distribution:")
for i in range(len(hist2)):
    if hist2[i] > 0:
        print(f"X {bins2[i]:.2f} - {bins2[i+1]:.2f}: {hist2[i]} vertices")
