import bpy
import bmesh

bpy.ops.wm.read_factory_settings(use_empty=True)

# Load final STL
stl_in = "stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl"
if hasattr(bpy.ops.wm, 'stl_import'):
    bpy.ops.wm.stl_import(filepath=stl_in)
else:
    bpy.ops.import_mesh.stl(filepath=stl_in)

obj = bpy.context.active_object
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Remesh / Repair using Voxel Remesh or 3D Print cleanup
mod = obj.modifiers.new(name="Remesh", type='REMESH')
mod.mode = 'VOXEL'
mod.voxel_size = 0.15  # 0.15mm voxel resolution for ultra-sharp 3D print precision
bpy.ops.object.modifier_apply(modifier="Remesh")

# Smooth subtle voxel artifacting while preserving sharp edges
mod_s = obj.modifiers.new(name="Smooth", type='CORRECTIVE_SMOOTH')
mod_s.smooth_type = 'LENGTH_WEIGHTED'
mod_s.factor = 0.5
mod_s.iterations = 5
bpy.ops.object.modifier_apply(modifier="Smooth")

stl_out = "stls/exports/ELNA_SUPERMATIC_PLUG_WATERTIGHT_CLEAN.stl"
if hasattr(bpy.ops.wm, 'stl_export'):
    bpy.ops.wm.stl_export(filepath=stl_out)
else:
    bpy.ops.export_mesh.stl(filepath=stl_out, use_selection=True)

print("REPAIRED WATERTIGHT EXPORT COMPLETE!")
