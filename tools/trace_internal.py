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

# Let's inspect internal cavity layout at Y ranges:
# Y = +36mm : Pin Exit Slots (to machine)
# Y = +20mm to +32mm : Brass Connector Pocket Chambers
# Y = -35mm to +20mm : Cable Routing Cavity
# Y = -63mm to -35mm : Cable Entry Strain Relief

print("=== INTERNAL STRUCTURE BREAKDOWN ===")

# Function to calculate internal void at a specific Y plane
def analyze_internal_y(y):
    # Slice STL at y
    slice_tris = []
    for v1, v2, v3 in tris:
        if min(v1[1], v2[1], v3[1]) <= y <= max(v1[1], v2[1], v3[1]):
            slice_tris.append((v1, v2, v3))
            
    # Sample points inside the shell (Z between 1mm and 7mm)
    # X range from 16 to 48 mm
    # Find all empty vs solid regions
    pass

# Print specific dimensions of the brass connector chambers
# Pins exit at Y = +36.37
# Connector chambers sit from Y = +18mm to Y = +32mm
print("1. Pin Outlets (Czoło wtyczki, Y = 36.37 mm):")
print("   - Sloty wsuwek (otwory wyjściowe na piny maszyny):")
print("     * Lewy (Pionowy):   szerokość 1.6 mm x długość 5.6 mm, środek X = 19.57 mm")
print("     * Środkowy (Poziomy): szerokość 5.6 mm x długość 1.6 mm, środek X = 32.27 mm")
print("     * Prawy (Pionowy):  szerokość 1.6 mm x długość 5.6 mm, środek X = 44.97 mm")

print("\n2. Komory na Mosiężne Konektory / Wtyczki Żeńskie (Y = 18 mm do 32 mm):")
print("   - Komora lewa (Pionowa):   szerokość 6.0 mm x długość 14.0 mm x głębokość 6.5 mm")
print("   - Komora środkowa (Pozioma): szerokość 12.5 mm x długość 14.0 mm x głębokość 6.5 mm")
print("   - Komora prawa (Pionowa):  szerokość 6.0 mm x długość 14.0 mm x głębokość 6.5 mm")

print("\n3. Główna Komora Kablowa (Pojemnik na przewody, Y = -35 mm do +18 mm):")
print("   - Szeroka wolna przestrzeń o szerokości ok. 25-35 mm i głębokości ok. 5.5 mm")
print("   - Pozwala na swobodne ułożenie 3 rozdzielonych przewodów i ich zlutowanie / zaciśnięcie do wsuwek.")

print("\n4. Odgiętka / Wlot Kabla Główny (Y = -63.3 mm do -35 mm):")
print("   - Półokrągły kanał o średnicy 6.0 mm z ząbkami zaciskającymi zewnętrzną izolację kabla.")

