import bpy

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
body_front_y = 36.372837
cap_front_y = -63.325489

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

print("=== STEP 1: CREATE FILL BLOCKS ===")
fill_b = create_box("Fill_B", (center_x, 11.0, 3.5), (13.0, 24.0, 8.0))
fill_t = create_box("Fill_T", (center_x, -33.0, 3.5), (13.0, 24.0, 8.0))

print("=== STEP 2: UNION FILLS INTO PLUG ===")
apply_boolean(plug, fill_b, "UNION")
apply_boolean(plug, fill_t, "UNION")

print("=== STEP 3: CREATE EXACT CUTTERS ===")
# Bottom Cutters
cut_b_slot = create_box("Cut_B_Slot", (center_x, body_front_y - 2.8, 3.5), (1.6, 5.6, 10.0))
cut_b_conn = create_box("Cut_B_Conn", (center_x, body_front_y - 12.0, 5.26), (6.0, 14.0, 5.5))
cut_b_wire = create_box("Cut_B_Wire", (center_x, body_front_y - 23.0, 5.26), (4.0, 10.0, 5.5))

# Top Cutters
cut_t_slot = create_box("Cut_T_Slot", (center_x, cap_front_y + 2.8, 3.5), (1.6, 5.6, 10.0))
cut_t_conn = create_box("Cut_T_Conn", (center_x, cap_front_y + 12.0, 5.26), (6.0, 14.0, 5.5))
cut_t_wire = create_box("Cut_T_Wire", (center_x, cap_front_y + 23.0, 5.26), (4.0, 10.0, 5.5))

print("=== STEP 4: SUBTRACT CUTTERS FROM PLUG ===")
for cutter in [cut_b_slot, cut_b_conn, cut_b_wire, cut_t_slot, cut_t_conn, cut_t_wire]:
    apply_boolean(plug, cutter, "DIFFERENCE")

# Cleanup helper objects
for obj in [fill_b, fill_t, cut_b_slot, cut_b_conn, cut_b_wire, cut_t_slot, cut_t_conn, cut_t_wire]:
    if obj.name in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

print("=== STEP 5: EXPORT PERFECT STL ===")
out_path = "stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl"
bpy.context.view_layer.objects.active = plug
plug.select_set(True)
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=out_path, export_selected_objects=True)
else:
    bpy.ops.export_mesh.stl(filepath=out_path, use_selection=True)

print("EXPORT COMPLETED SUCCESSFULLY!")
