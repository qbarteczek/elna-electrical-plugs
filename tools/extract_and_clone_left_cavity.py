import bpy
import numpy as np

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Load Original Plug STL
stl_path = "stls/ELNA_SUPERMATIC_PLUG_WATERTIGHT.stl"
if hasattr(bpy.ops.wm, 'stl_import'):
    bpy.ops.wm.stl_import(filepath=stl_path)
else:
    bpy.ops.import_mesh.stl(filepath=stl_path)

plug = bpy.context.active_object
plug.name = "Plug"

center_x = 32.269119
left_x = center_x - 12.7  # 19.569119
shift_x = 12.7           # Shift left cavity to center

def create_box(name, loc, size):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    return obj

def apply_boolean(target, tool, operation):
    mod = target.modifiers.new(name="Bool", type="BOOLEAN")
    mod.operation = operation
    mod.object = tool
    mod.solver = 'EXACT'  # Exact solver for manifold boolean CSG
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="Bool")

print("=== STEP 1: EXTRACT LEFT CAVITY SOLID (BOTTOM HALF) ===")
# Box around Left cavity of bottom half (Y from 0 to 36.5, X width 6.0mm strictly inside cavity)
box_bl = create_box("Box_BL", (left_x, 18.5, 4.0), (6.0, 37.0, 9.0))
# Extract Left cavity solid: Box_BL - Plug
apply_boolean(box_bl, plug, "DIFFERENCE")

print("=== STEP 2: EXTRACT LEFT CAVITY SOLID (TOP HALF) ===")
# Box around Left cavity of top half (Y from -63.5 to -26.0, X width 6.0mm)
box_tl = create_box("Box_TL", (left_x, -45.0, 4.0), (6.0, 37.0, 9.0))
# Extract Left cavity solid: Box_TL - Plug
apply_boolean(box_tl, plug, "DIFFERENCE")


print("=== STEP 3: TRANSLATE EXTRACTED SOLIDS TO CENTER ===")
box_bl.location.x += shift_x
box_tl.location.x += shift_x
bpy.context.view_layer.objects.active = box_bl
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
bpy.context.view_layer.objects.active = box_tl
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

print("=== STEP 4: CREATE FILL BLOCKS FOR ORIGINAL HORIZONTAL CENTER CAVITIES ===")
# Bottom Center Fill (original horizontal cavity is in Y range 0..17, X range 26.7..38.8)
fill_bc = create_box("Fill_BC", (center_x, 11.0, 4.0), (13.5, 24.0, 9.0))

# Top Center Fill (original horizontal cavity is in Y range -35..-25, X range 26.8..38.8)
fill_tc = create_box("Fill_TC", (center_x, -33.0, 4.0), (13.5, 24.0, 9.0))


print("=== STEP 5: UNION FILLS INTO PLUG ===")
apply_boolean(plug, fill_bc, "UNION")
apply_boolean(plug, fill_tc, "UNION")

print("=== STEP 6: SUBTRACT TRANSLATED CAVITIES FROM PLUG ===")
apply_boolean(plug, box_bl, "DIFFERENCE")
apply_boolean(plug, box_tl, "DIFFERENCE")

# Cleanup helper objects
for obj in [box_bl, box_tl, fill_bc, fill_tc]:
    if obj.name in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

print("=== STEP 7: EXPORT PERFECT SYMMETRIC STL ===")
out_path = "stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl"
bpy.context.view_layer.objects.active = plug
plug.select_set(True)
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=out_path, export_selected_objects=True)
else:
    bpy.ops.export_mesh.stl(filepath=out_path, use_selection=True)

print("EXPORT COMPLETED SUCCESSFULLY!")
