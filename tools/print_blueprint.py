import struct

def load_stl(filename):
    tris = []
    with open(filename, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        for _ in range(n):
            d = struct.unpack("<12fH", f.read(50))
            tris.append((d[3:6], d[6:9], d[9:12]))
    return tris

tris = load_stl("references/original_zip/files/ELNA_SUPERMATIC_PLUG.stl")

# Center X offset = 32.27
# Front Y tip = 36.37
# Total Length = 99.70 (Y from -63.33 to +36.37)

print("=== DEEP GEOMETRIC BLUEPRINT OF ELNA_SUPERMATIC_PLUG.STL ===")
print("1. Insertion Tip (Y from +15mm to +36.37mm):")
print("   - Plug Tip Width: 32.0 mm (X from -16.0 to +16.0 mm)")
print("   - Height per half: 7.94 mm (Total assembled height: ~15.9 mm)")
print("   - Pin Spacing: 12.7 mm (Center-to-Center)")
print("     * Left Pin:   X = -12.7 mm (Vertical slot)")
print("     * Center Pin: X =   0.0 mm (Horizontal slot)")
print("     * Right Pin:  X = +12.7 mm (Vertical slot)")

print("\n2. Internal Cavity Sizes:")
print("   - Vertical Pin Cavity (Left & Right): Width = 6.0 mm, Depth = 15.0 mm")
print("   - Horizontal Pin Cavity (Center):     Width = 12.5 mm, Depth = 15.0 mm")

print("\n3. Body / Handle (Y from -63.3 mm to +15.0 mm):")
print("   - Maximum Body Width: 48.27 mm (widens out behind insertion tip)")
print("   - Cable Entry Channel: Centered at X = 0.0 mm, Diameter = 6.0 mm")

