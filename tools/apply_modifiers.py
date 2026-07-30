import trimesh
import os

print("Loading STL (Wczytywanie STL)...")
# Load the original plug (use the best available version)
plug = trimesh.load('stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl', process=False)
fill = trimesh.load('stls/exports/modifier_fill.stl', process=False)
cut = trimesh.load('stls/exports/modifier_cut.stl', process=False)

print("Repairing geometry if necessary (Naprawianie geometrii)...")
if not plug.is_watertight:
    trimesh.repair.fill_holes(plug)
if not fill.is_watertight:
    trimesh.repair.fill_holes(fill)
if not cut.is_watertight:
    trimesh.repair.fill_holes(cut)

print("Executing Boolean operations (Wykonywanie operacji Boole'a)...")
try:
    # Booleans in trimesh can be brittle, let's try the default engine (blender if available, else exact)
    # First, add the fill blocks
    step1 = plug.union(fill)
    # Then subtract the cut blocks
    final = step1.difference(cut)
    
    print("Saving final STL (Zapisywanie gotowego STL)...")
    final.export('stls/exports/elna_plug_modified_final.stl')
    print("Success (Sukces)! Saved stls/exports/elna_plug_modified_final.stl")
except Exception as e:
    print(f"Boolean operation error (Błąd operacji Boole'a): {e}")
    print("Use modifiers_fill.stl and modifiers_cut.stl in your Slicer e.g., PrusaSlicer (Użyj plików modifiers_fill.stl oraz modifiers_cut.stl w swoim Slicerze).")
