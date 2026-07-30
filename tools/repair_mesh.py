import pymeshlab
import sys

input_file = "stls/ELNA_SUPERMATIC_PLUG.stl"
output_file = "stls/ELNA_SUPERMATIC_PLUG_WATERTIGHT.stl"

ms = pymeshlab.MeshSet()
ms.load_new_mesh(input_file)

# Basic repair steps
ms.apply_filter("meshing_merge_close_vertices")
ms.apply_filter("meshing_remove_duplicate_faces")
ms.apply_filter("meshing_remove_duplicate_vertices")
ms.apply_filter("meshing_repair_non_manifold_edges")
ms.apply_filter("meshing_repair_non_manifold_vertices")

# Close holes
# maxholesize: max size of the hole to be closed, in number of edges
ms.apply_filter("meshing_close_holes", maxholesize=1000)

ms.save_current_mesh(output_file)
print(f"Saved repaired file to (Zapisano naprawiony plik do) {output_file}")
