import bpy
import os

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Path to the original STL
stl_path = "stls/ELNA_SUPERMATIC_PLUG.stl"
if not os.path.exists(stl_path):
    print(f"Error: Original STL file {stl_path} not found!")
    exit(1)

# 1. Load STL
if hasattr(bpy.ops.wm, 'stl_import'):
    bpy.ops.wm.stl_import(filepath=stl_path)
else:
    bpy.ops.import_mesh.stl(filepath=stl_path)

imported_obj = bpy.context.active_object

# 2. Separate by loose parts to isolate bottom and top halves
bpy.context.view_layer.objects.active = imported_obj
bpy.ops.object.select_all(action='DESELECT')
imported_obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

separated_objs = [obj for obj in bpy.data.objects if obj.type == 'MESH']

# Group objects into bottom and top halves using Y coordinate center
bottom_parts = []
top_parts = []
for obj in separated_objs:
    y_sum = sum(v.co.y for v in obj.data.vertices)
    y_center = y_sum / len(obj.data.vertices)
    if y_center > -10.0:
        bottom_parts.append(obj)
    else:
        top_parts.append(obj)

# Join bottom parts into a single object
bpy.ops.object.select_all(action='DESELECT')
for o in bottom_parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = bottom_parts[0]
bpy.ops.object.join()
bottom_half = bpy.context.active_object
bottom_half.name = "BottomHalf"

# Join top parts into a single object
bpy.ops.object.select_all(action='DESELECT')
for o in top_parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = top_parts[0]
bpy.ops.object.join()
top_half = bpy.context.active_object
top_half.name = "TopHalf"

# Geometric constants (exactly match left/right spacing)
center_x = 32.269119
left_x = center_x - 12.7  # 19.569119
shift_x = 12.7            # Shift distance from left to center

def create_box(name, loc, size):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    # Apply scale so boolean operations work correctly
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj

def apply_boolean(target, tool, operation):
    mod = target.modifiers.new(name="Bool", type="BOOLEAN")
    mod.operation = operation
    mod.object = tool
    mod.solver = 'EXACT'
    
    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="Bool")

# === 3. BOTTOM HALF MODIFICATION ===
print("=== Modifying Bottom Half ===")
# Create a bounding box enclosing the left vertical slot
box_bl = create_box("Box_BL", (left_x, 18.5, 4.0), (6.0, 37.0, 9.0))

# Duplicate bottom_half to extract the cavity volume
bottom_half_copy = bottom_half.copy()
bottom_half_copy.data = bottom_half.data.copy()
bpy.context.collection.objects.link(bottom_half_copy)

# LeftCavity = Box_BL - BottomHalf
apply_boolean(box_bl, bottom_half_copy, "DIFFERENCE")
bpy.data.objects.remove(bottom_half_copy, do_unlink=True)

# Translate the cavity shape to the center slot
box_bl.location.x += shift_x
bpy.ops.object.select_all(action='DESELECT')
box_bl.select_set(True)
bpy.context.view_layer.objects.active = box_bl
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

# Fill the original center horizontal cavity in bottom_half
fill_bc = create_box("Fill_BC", (center_x, 11.0, 4.0), (13.5, 24.0, 9.0))
apply_boolean(bottom_half, fill_bc, "UNION")
bpy.data.objects.remove(fill_bc, do_unlink=True)

# Subtract the translated left cavity from bottom_half
apply_boolean(bottom_half, box_bl, "DIFFERENCE")
bpy.data.objects.remove(box_bl, do_unlink=True)


# === 4. TOP HALF MODIFICATION ===
print("=== Modifying Top Half ===")
# Create a bounding box enclosing the left vertical slot
box_tl = create_box("Box_TL", (left_x, -45.0, 4.0), (6.0, 37.0, 9.0))

# Duplicate top_half to extract the cavity volume
top_half_copy = top_half.copy()
top_half_copy.data = top_half.data.copy()
bpy.context.collection.objects.link(top_half_copy)

# LeftCavity = Box_TL - TopHalf
apply_boolean(box_tl, top_half_copy, "DIFFERENCE")
bpy.data.objects.remove(top_half_copy, do_unlink=True)

# Translate the cavity shape to the center slot
box_tl.location.x += shift_x
bpy.ops.object.select_all(action='DESELECT')
box_tl.select_set(True)
bpy.context.view_layer.objects.active = box_tl
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

# Fill the original center horizontal cavity in top_half
fill_tc = create_box("Fill_TC", (center_x, -33.0, 4.0), (13.5, 24.0, 9.0))
apply_boolean(top_half, fill_tc, "UNION")
bpy.data.objects.remove(fill_tc, do_unlink=True)

# Subtract the translated left cavity from top_half
apply_boolean(top_half, box_tl, "DIFFERENCE")
bpy.data.objects.remove(box_tl, do_unlink=True)


# === 5. MESH CLEANUP & VERTEX WELDING ===
# This welds duplicate boundary vertices from boolean cuts, making meshes watertight
for obj in [bottom_half, top_half]:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # Merge overlapping vertices with threshold
    bpy.ops.mesh.remove_doubles(threshold=0.0005)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')


# === 6. CENTERING & ORIENTING FOR SUPPORTLESS 3D PRINTING ===
# --- Bottom Half Centering & Alignment ---
bpy.ops.object.select_all(action='DESELECT')
bottom_half.select_set(True)
bpy.context.view_layer.objects.active = bottom_half

xs = [v.co.x for v in bottom_half.data.vertices]
ys = [v.co.y for v in bottom_half.data.vertices]
zs = [v.co.z for v in bottom_half.data.vertices]
min_b = [min(xs), min(ys), min(zs)]
max_b = [max(xs), max(ys), max(zs)]
center_b_x = (min_b[0] + max_b[0]) / 2.0
center_b_y = (min_b[1] + max_b[1]) / 2.0

bottom_half.location.x -= center_b_x
bottom_half.location.y -= center_b_y
bottom_half.location.z -= min_b[2]
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)


# --- Top Half Centering, Alignment & Rotation ---
# In the original mesh, the top half is upside down (split face up). 
# We rotate it 180 degrees around X axis to lay it flat for printing without supports.
bpy.ops.object.select_all(action='DESELECT')
top_half.select_set(True)
bpy.context.view_layer.objects.active = top_half

top_half.rotation_euler.x = 3.14159265359
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

xs_t = [v.co.x for v in top_half.data.vertices]
ys_t = [v.co.y for v in top_half.data.vertices]
zs_t = [v.co.z for v in top_half.data.vertices]
min_t = [min(xs_t), min(ys_t), min(zs_t)]
max_t = [max(xs_t), max(ys_t), max(zs_t)]
center_t_x = (min_t[0] + max_t[0]) / 2.0
center_t_y = (min_t[1] + max_t[1]) / 2.0

top_half.location.x -= center_t_x
top_half.location.y -= center_t_y
top_half.location.z -= min_t[2]
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)


# === 7. EXPORT PLUG PARTS ===
out_dir = "stls/exports"
os.makedirs(out_dir, exist_ok=True)
out_b = os.path.join(out_dir, "elna_plug_modified_bottom.stl")
out_t = os.path.join(out_dir, "elna_plug_modified_top.stl")

# Export Bottom Half
bpy.ops.object.select_all(action='DESELECT')
bottom_half.select_set(True)
bpy.context.view_layer.objects.active = bottom_half
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=out_b, export_selected_objects=True)
else:
    bpy.ops.export_mesh.stl(filepath=out_b, use_selection=True)

# Export Top Half
bpy.ops.object.select_all(action='DESELECT')
top_half.select_set(True)
bpy.context.view_layer.objects.active = top_half
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=out_t, export_selected_objects=True)
else:
    bpy.ops.export_mesh.stl(filepath=out_t, use_selection=True)

print("Export of modified bottom and top halves complete!")
