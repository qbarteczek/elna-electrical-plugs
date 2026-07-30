import bpy
import bmesh

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Load Original Plug STL
stl_path = "references/original_zip/files/ELNA_SUPERMATIC_PLUG.stl"
if hasattr(bpy.ops.wm, 'stl_import'):
    bpy.ops.wm.stl_import(filepath=stl_path)
else:
    bpy.ops.import_mesh.stl(filepath=stl_path)

plug = bpy.context.active_object
plug.name = "Plug"

# Center X = 32.269119
# Left X = 19.569119 (Shift = +12.7mm)
center_x = 32.269119
left_x = 19.569119
shift_x = 12.7

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
    mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="Bool")

print("=== 1. EXTRACT LEFT CAVITY SOLID (BOTTOM HALF) ===")
# Box around Left cavity of bottom half (X width 5.8mm, Y from 0.4 to 36.3, Z from -1 to 8.5)
box_bl = create_box("Box_BL", (left_x, 18.4, 3.8), (5.8, 36.5, 9.0))
apply_boolean(box_bl, plug, "DIFFERENCE")

print("=== 2. EXTRACT LEFT CAVITY SOLID (TOP HALF) ===")
# Box around Left cavity of top half (X width 5.8mm, Y from -63.3 to -26.0, Z from -1 to 8.5)
box_tl = create_box("Box_TL", (left_x, -44.8, 3.8), (5.8, 36.5, 9.0))
apply_boolean(box_tl, plug, "DIFFERENCE")

print("=== 3. TRANSLATE CAVITY SOLIDS TO CENTER ===")
box_bl.location.x += shift_x
box_tl.location.x += shift_x
bpy.context.view_layer.objects.active = box_bl
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
bpy.context.view_layer.objects.active = box_tl
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

print("=== 4. CREATE FILL BLOCKS FOR ORIGINAL HORIZONTAL CENTER CAVITIES ===")
fill_b = create_box("Fill_B", (center_x, 8.5, 3.5), (12.4, 17.0, 7.5))
fill_t = create_box("Fill_T", (center_x, -30.2, 3.5), (12.4, 11.0, 7.5))

print("=== 5. UNION FILLS INTO PLUG ===")
apply_boolean(plug, fill_b, "UNION")
apply_boolean(plug, fill_t, "UNION")

print("=== 6. SUBTRACT TRANSLATED CAVITIES FROM PLUG ===")
apply_boolean(plug, box_bl, "DIFFERENCE")
apply_boolean(plug, box_tl, "DIFFERENCE")

# Cleanup helper objects
for obj in [box_bl, box_tl, fill_b, fill_t]:
    if obj.name in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

print("=== 7. MESH CLEANUP (MERGE BY DISTANCE & REPAIR) ===")
bpy.context.view_layer.objects.active = plug
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')

print("=== 8. EXPORT PERFECT STL ===")
out_path = "stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl"
plug.select_set(True)
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=out_path, export_selected_objects=True)
else:
    bpy.ops.export_mesh.stl(filepath=out_path, use_selection=True)

print("COMPLETED!")
