import bpy
import sys
import math

def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Add light
    bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(20, 20, 50))
    light = bpy.context.active_object
    light.data.energy = 3.0
    
    bpy.ops.object.light_add(type='AREA', radius=10, align='WORLD', location=(32, -40, 30))
    light2 = bpy.context.active_object
    light2.data.energy = 500.0
    
    # Add camera
    # The plug is from X:14 to 50, Y:-40 to 40. Center is ~ (32, 0, 0)
    # The modified slot is at Y=8 (bottom half) and Y=-26 (top half)
    bpy.ops.object.camera_add(location=(32, 35, 45))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(50), 0, math.radians(180))
    bpy.context.scene.camera = cam
    
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 384
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 12
    bpy.context.scene.eevee.taa_render_samples = 16

def render_mesh(stl_path, out_path):
    setup_scene()
    
    # Import STL
    if hasattr(bpy.ops.wm, 'stl_import'):
        bpy.ops.wm.stl_import(filepath=stl_path)
    else:
        bpy.ops.import_mesh.stl(filepath=stl_path)
        
    obj = bpy.context.active_object
    
    # Add a simple material
    mat = bpy.data.materials.new(name="Plastic")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.2, 0.4, 0.8, 1) # Blueish plastic
    bsdf.inputs['Roughness'].default_value = 0.3
    obj.data.materials.append(mat)
    
    # Render
    bpy.context.scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    # Render Original
    render_mesh("references/original_zip/files/ELNA_SUPERMATIC_PLUG.stl", "/home/qba/Dokumenty/elna-electrical-plugs/images/render_original.png")
    
    # Render Final
    render_mesh("stls/exports/ELNA_SUPERMATIC_PLUG_FINAL.stl", "/home/qba/Dokumenty/elna-electrical-plugs/images/render_final.png")

