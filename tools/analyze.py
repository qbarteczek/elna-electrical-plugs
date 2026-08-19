import sys
from stl import mesh

def analyze_stl(filepath):
    try:
        your_mesh = mesh.Mesh.from_file(filepath)
        minx = your_mesh.x.min()
        maxx = your_mesh.x.max()
        miny = your_mesh.y.min()
        maxy = your_mesh.y.max()
        minz = your_mesh.z.min()
        maxz = your_mesh.z.max()
        print(f"File: {filepath}")
        print(f"X: {minx} to {maxx} (center: {(minx+maxx)/2})")
        print(f"Y: {miny} to {maxy} (center: {(miny+maxy)/2})")
        print(f"Z: {minz} to {maxz} (center: {(minz+maxz)/2})")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

analyze_stl(sys.argv[1])
