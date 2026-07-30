import bpy
import sys
import math

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Load plug
if hasattr(bpy.ops.wm, 'stl_import'):
    bpy.ops.wm.stl_import(filepath="stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl")
else:
    bpy.ops.import_mesh.stl(filepath="stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl")
plug = bpy.context.active_object
plug.name = "Plug"

# Helpers
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

# ================= BOTTOM HALF =================
# 1. Create tight bounding box around Left Hole (X=16.046, Y=12.191)
box_bl = create_box("BoxBL", (16.046, 12.191, 1.75), (10.0, 8.0, 3.5))

# 2. Extract Hole: BoxBL - Plug
apply_boolean(box_bl, plug, "DIFFERENCE")

# 3. Translate Hole to Center (dX=16.746, dY=-5.709)
box_bl.location.x += 16.746
box_bl.location.y -= 5.709

# 4. Create Fill block for Center (Z=1.5, height=3.0)
fill_bc = create_box("FillBC", (32.792, 6.482, 1.5), (13.0, 9.0, 3.0))

# ================= TOP HALF =================
# 1. Create tight bounding box around Left Hole (X=15.609, Y=-30.408)
box_tl = create_box("BoxTL", (15.609, -30.408, 1.75), (10.0, 8.0, 3.5))

# 2. Extract Hole: BoxTL - Plug
apply_boolean(box_tl, plug, "DIFFERENCE")

# 3. Translate Hole to Center (dX=17.219, dY=-0.904)
box_tl.location.x += 17.219
box_tl.location.y -= 0.904

# 4. Create Fill block for Center
fill_tc = create_box("FillTC", (32.828, -31.312, 1.5), (13.0, 9.0, 3.0))

# ================= FINAL APPLY TO PLUG =================
# Add fills
apply_boolean(plug, fill_bc, "UNION")
apply_boolean(plug, fill_tc, "UNION")

# Subtract translated holes
apply_boolean(plug, box_bl, "DIFFERENCE")
apply_boolean(plug, box_tl, "DIFFERENCE")

# Cleanup tools
bpy.data.objects.remove(box_bl, do_unlink=True)
bpy.data.objects.remove(fill_bc, do_unlink=True)
bpy.data.objects.remove(box_tl, do_unlink=True)
bpy.data.objects.remove(fill_tc, do_unlink=True)

# Export
bpy.context.view_layer.objects.active = plug
plug.select_set(True)
out = "stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl"
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=out, export_selected_objects=True)
else:
    bpy.ops.export_mesh.stl(filepath=out, use_selection=True)

print("Done perfectly!")
