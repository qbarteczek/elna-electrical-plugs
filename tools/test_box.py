import trimesh
import numpy as np

mesh = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl')

# Define the box
box = trimesh.creation.box(extents=[10, 6, 3.0], transform=trimesh.transformations.translation_matrix([18.52, 8.3, 1.5]))

# Check if any part of the box is outside the mesh exterior.
# We can just export the box and visually check, but wait, we can just do the boolean!
# Let's do the boolean with trimesh!
# Trimesh boolean can be slow/buggy, let's use Blender.
