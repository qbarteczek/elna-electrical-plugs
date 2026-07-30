import bpy
import sys

# Uruchomienie: blender --background --python tools/blender_extract_hole.py

bpy.ops.wm.read_factory_settings(use_empty=True)

def load_stl(filepath):
    if hasattr(bpy.ops.wm, 'stl_import'):
        bpy.ops.wm.stl_import(filepath=filepath)
    else:
        bpy.ops.import_mesh.stl(filepath=filepath)
    return bpy.context.active_object

def create_box(name, location, scale):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (scale[0]/2, scale[1]/2, scale[2]/2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

print("Loading original plug...")
plug = load_stl("stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl")
plug.name = "OriginalPlug"

print("Creating bounding boxes...")
box_bottom = create_box("BoxBottom", (19.57, 14.25, 3.75), (10.0, 45.0, 8.0))
box_top = create_box("BoxTop", (19.57, -26.68, 3.75), (10.0, 75.0, 8.0))

print("Extracting holes...")
# Subtract plug from BoxBottom
bpy.context.view_layer.objects.active = box_bottom
mod_diff1 = box_bottom.modifiers.new(name="Difference", type="BOOLEAN")
mod_diff1.operation = "DIFFERENCE"
mod_diff1.object = plug
mod_diff1.solver = "EXACT"
bpy.ops.object.modifier_apply(modifier="Difference")

# Subtract plug from BoxTop
bpy.context.view_layer.objects.active = box_top
mod_diff2 = box_top.modifiers.new(name="Difference", type="BOOLEAN")
mod_diff2.operation = "DIFFERENCE"
mod_diff2.object = plug
mod_diff2.solver = "EXACT"
bpy.ops.object.modifier_apply(modifier="Difference")

print("Translating holes to center...")
box_bottom.location.x += 12.7
box_top.location.x += 12.7
bpy.context.view_layer.objects.active = box_bottom
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
bpy.context.view_layer.objects.active = box_top
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

# Join them together
box_bottom.select_set(True)
box_top.select_set(True)
bpy.context.view_layer.objects.active = box_bottom
bpy.ops.object.join()

output_file = "stls/exports/modifier_cut.stl"
print(f"Exporting exactly duplicated hole to {output_file}...")
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=output_file)
else:
    bpy.ops.export_mesh.stl(filepath=output_file, use_selection=True)

print("Done!")
