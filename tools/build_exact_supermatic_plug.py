import bpy

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Load Original Plug STL
stl_path = "stls/ELNA_SUPERMATIC_PLUG.stl"
if hasattr(bpy.ops.wm, 'stl_import'):
    bpy.ops.wm.stl_import(filepath=stl_path)
else:
    bpy.ops.import_mesh.stl(filepath=stl_path)

plug = bpy.context.active_object
plug.name = "Plug"

# Center of plug is X = 32.269119
center_x = 32.269119
body_front_y = 36.372837
cap_front_y = -63.325489

# Original pin centers in STL:
orig_left_x = 18.994854
orig_center_x = 32.791787
orig_right_x = 44.817112

# Target pin centers (exactly 12.7mm pitch, symmetric around center_x):
target_left_x = center_x - 12.7  # 19.569119
target_center_x = center_x        # 32.269119
target_right_x = center_x + 12.7 # 44.969119

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
    mod.solver = 'FLOAT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="Bool")

print("=== STEP 1: CREATE FILL BLOCKS FOR ALL THREE ORIGINAL CAVITIES ===")
# Bottom fills (original cavities - sized strictly inside to avoid leaking outside outer walls)
fill_l_b = create_box("Fill_L_B", (19.59, 18.4, 3.8), (5.8, 37.0, 9.0))
fill_c_b = create_box("Fill_C_B", (orig_center_x, 18.4, 3.8), (12.0, 37.0, 9.0))
fill_r_b = create_box("Fill_R_B", (44.22, 18.4, 3.8), (5.8, 37.0, 9.0))

# Top fills
fill_l_t = create_box("Fill_L_T", (19.59, -44.8, 3.8), (5.8, 37.0, 9.0))
fill_c_t = create_box("Fill_C_T", (orig_center_x, -44.8, 3.8), (12.0, 37.0, 9.0))
fill_r_t = create_box("Fill_R_T", (44.22, -44.8, 3.8), (5.8, 37.0, 9.0))


print("=== STEP 2: UNION FILLS INTO PLUG ===")
for fill in [fill_l_b, fill_c_b, fill_r_b, fill_l_t, fill_c_t, fill_r_t]:
    apply_boolean(plug, fill, "UNION")

print("=== STEP 3: CREATE PERFECT SYMMETRIC CUTTERS (ALL 3 VERTICAL) ===")
cutters = []

# --- BOTTOM HALF CUTTERS (Y > 0) ---
# Left Pin Cavity (vertical)
cutters.append(create_box("Cut_L_B_Slot", (target_left_x, body_front_y - 2.8, 3.5), (1.6, 5.6, 10.0)))
cutters.append(create_box("Cut_L_B_Conn", (target_left_x, body_front_y - 12.0, 5.265), (6.0, 14.0, 5.5)))
cutters.append(create_box("Cut_L_B_Wire", (target_left_x, body_front_y - 23.0, 5.265), (4.0, 10.0, 5.5)))

# Right Pin Cavity (vertical)
cutters.append(create_box("Cut_R_B_Slot", (target_right_x, body_front_y - 2.8, 3.5), (1.6, 5.6, 10.0)))
cutters.append(create_box("Cut_R_B_Conn", (target_right_x, body_front_y - 12.0, 5.265), (6.0, 14.0, 5.5)))
cutters.append(create_box("Cut_R_B_Wire", (target_right_x, body_front_y - 23.0, 5.265), (4.0, 10.0, 5.5)))

# Center Pin Cavity (vertical - modified to match left/right exactly!)
cutters.append(create_box("Cut_C_B_Slot", (target_center_x, body_front_y - 2.8, 3.5), (1.6, 5.6, 10.0)))
cutters.append(create_box("Cut_C_B_Conn", (target_center_x, body_front_y - 12.0, 5.265), (6.0, 14.0, 5.5)))
cutters.append(create_box("Cut_C_B_Wire", (target_center_x, body_front_y - 23.0, 5.265), (4.0, 10.0, 5.5)))

# --- TOP HALF CUTTERS (Y < 0) ---
# Left Pin Cavity (vertical)
cutters.append(create_box("Cut_L_T_Slot", (target_left_x, cap_front_y + 2.8, 3.5), (1.6, 5.6, 10.0)))
cutters.append(create_box("Cut_L_T_Conn", (target_left_x, cap_front_y + 12.0, 5.265), (6.0, 14.0, 5.5)))
cutters.append(create_box("Cut_L_T_Wire", (target_left_x, cap_front_y + 23.0, 5.265), (4.0, 10.0, 5.5)))

# Right Pin Cavity (vertical)
cutters.append(create_box("Cut_R_T_Slot", (target_right_x, cap_front_y + 2.8, 3.5), (1.6, 5.6, 10.0)))
cutters.append(create_box("Cut_R_T_Conn", (target_right_x, cap_front_y + 12.0, 5.265), (6.0, 14.0, 5.5)))
cutters.append(create_box("Cut_R_T_Wire", (target_right_x, cap_front_y + 23.0, 5.265), (4.0, 10.0, 5.5)))

# Center Pin Cavity (vertical)
cutters.append(create_box("Cut_C_T_Slot", (target_center_x, cap_front_y + 2.8, 3.5), (1.6, 5.6, 10.0)))
cutters.append(create_box("Cut_C_T_Conn", (target_center_x, cap_front_y + 12.0, 5.265), (6.0, 14.0, 5.5)))
cutters.append(create_box("Cut_C_T_Wire", (target_center_x, cap_front_y + 23.0, 5.265), (4.0, 10.0, 5.5)))

print("=== STEP 4: SUBTRACT CUTTERS FROM PLUG ===")
for cutter in cutters:
    apply_boolean(plug, cutter, "DIFFERENCE")

# Cleanup helper objects by name string
helper_names = [fill_l_b.name, fill_c_b.name, fill_r_b.name, fill_l_t.name, fill_c_t.name, fill_r_t.name] + [c.name for c in cutters]
for name in helper_names:
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

print("=== STEP 5: MESH CLEANUP (MERGE BY DISTANCE) ===")
bpy.context.view_layer.objects.active = plug
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')

print("=== STEP 6: EXPORT PERFECT STL ===")
out_path = "stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl"
bpy.ops.object.select_all(action='DESELECT')
plug.select_set(True)
bpy.context.view_layer.objects.active = plug
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=out_path, export_selected_objects=True)
else:
    bpy.ops.export_mesh.stl(filepath=out_path, use_selection=True)

print("EXPORT OF SYMMETRICAL 3-VERTICAL PIN PLUG COMPLETE!")
