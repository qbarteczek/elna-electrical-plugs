import trimesh
import os

def verify_stl(path):
    if not os.path.exists(path):
        print(f"[-] File {path} does not exist!")
        return False
        
    mesh = trimesh.load(path)
    print(f"\n[+] Loaded {path}:")
    print(f"    Vertices: {len(mesh.vertices)}")
    print(f"    Faces: {len(mesh.faces)}")
    print(f"    Overall bounds: {mesh.bounds.tolist()}")
    
    # Split into connected bodies
    bodies = mesh.split()
    print(f"    Connected shells count: {len(bodies)}")
    
    all_watertight = True
    for i, body in enumerate(bodies):
        is_w = body.is_watertight
        if not is_w:
            all_watertight = False
        print(f"      Shell {i}: vertices={len(body.vertices)}, faces={len(body.faces)}, watertight={is_w}, bounds={body.bounds.tolist()}")
        
    if all_watertight:
        print("    [PASS] All individual shells are watertight and closed!")
    else:
        print("    [WARN] Some individual shells are not watertight!")
        
    return all_watertight

print("=== VERIFYING EXPORTED ELNA PLUG STL MODELS ===")
verify_stl("stls/exports/elna_plug_modified_bottom.stl")
verify_stl("stls/exports/elna_plug_modified_top.stl")
