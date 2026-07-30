import bpy
import sys

# Execution (Uruchomienie): blender --background --python tools/blender_csg.py

# Clearing default scene (Czyszczenie domyślnej sceny)
bpy.ops.wm.read_factory_settings(use_empty=True)

# Helper function to load STL and return the object (Funkcja pomocnicza)
def load_stl(filepath):
    # W nowym Blenderze 4.0+ używamy wm.stl_import lub stl.import
    if hasattr(bpy.ops.wm, 'stl_import'):
        bpy.ops.wm.stl_import(filepath=filepath)
    else:
        bpy.ops.import_mesh.stl(filepath=filepath)
    # the imported object should be active
    return bpy.context.active_object

print("Loading objects (Ładowanie obiektów)...")
orig_obj = load_stl("stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl")
orig_obj.name = "OriginalPlug"

fill_obj = load_stl("stls/exports/modifier_fill.stl")
fill_obj.name = "FillBlock"

cut_obj = load_stl("stls/exports/modifier_cut.stl")
cut_obj.name = "CutBlock"

print("Executing Boolean UNION - adding plastic (Wykonywanie Boolean UNION)...")
bpy.context.view_layer.objects.active = orig_obj
mod_union = orig_obj.modifiers.new(name="Union", type="BOOLEAN")
mod_union.operation = "UNION"
mod_union.object = fill_obj
mod_union.solver = "FLOAT"
bpy.ops.object.modifier_apply(modifier="Union")

print("Executing Boolean DIFFERENCE - cutting chambers (Wykonywanie Boolean DIFFERENCE)...")
mod_diff = orig_obj.modifiers.new(name="Difference", type="BOOLEAN")
mod_diff.operation = "DIFFERENCE"
mod_diff.object = cut_obj
mod_diff.solver = "FLOAT"
bpy.ops.object.modifier_apply(modifier="Difference")

# Removing helper objects (Usuwanie obiektów pomocniczych)
bpy.data.objects.remove(fill_obj, do_unlink=True)
bpy.data.objects.remove(cut_obj, do_unlink=True)

# Final export (Eksport końcowy)
output_file = "stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl"
print(f"Exporting to (Eksport do) {output_file}...")

if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=output_file)
else:
    bpy.ops.export_mesh.stl(filepath=output_file, use_selection=True)

print("Done (Gotowe)!")
