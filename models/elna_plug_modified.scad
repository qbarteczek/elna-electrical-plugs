// Elna Sewing Machine Plug - 3 Vertical Pins Modification
// Based on exact geometric measurements of original Thingiverse model 7199180 by bamckin

render_part = "bottom"; // [top, bottom, both]

// === DOKŁADNE PARAMETRY GEOMETRYCZNE ===
// Srodek osi X dla pliku STL: 32.27 mm
stl_center_x = 32.27;
front_y = 36.37;

// Wymiary nowych otworów i komór (pionowych)
pin_slot_w = 1.6;     // szerokość otworu na pin
pin_slot_l = 5.6;     // długość otworu na pin
conn_w = 6.0;         // szerokość komory na wsuwkę mosiężną
conn_l = 14.0;        // długość komory na wsuwkę mosiężną
conn_h = 6.5;         // głębokość komory na wsuwkę

module elna_plug_modified() {
    difference() {
        union() {
            // 1. Oryginalna obudowa z pliku STL
            import("../stls/ELNA_SUPERMATIC_PLUG.stl");
            
            // 2. Zalanie (wypełnienie) starej poziomej komory i otworu środkowego
            // Stara komora miała szerokość 12.5mm
            translate([stl_center_x, front_y - 10, 3.5])
                cube([12.6, 20.0, 7.5], center=true);
        }
        
        // 3. Wycięcie NOWEGO pionowego otworu na pin (identycznego jak lewy i prawy)
        translate([stl_center_x, front_y - 2.8, 3.5])
            cube([pin_slot_w, pin_slot_l, 10.0], center=true);
            
        // 4. Wycięcie NOWEJ pionowej komory na mosiężną wsuwkę żeńską (szerokość 6.0mm)
        translate([stl_center_x, front_y - 12.0, 3.5])
            cube([conn_w, conn_l, conn_h], center=true);
            
        // 5. Udrożnienie przejścia na przewód elektryczny z głównej komory
        translate([stl_center_x, front_y - 23.0, 3.5])
            cube([4.0, 10.0, 5.5], center=true);
    }
}

module render_split() {
    if (render_part == "both") {
        elna_plug_modified();
    } else if (render_part == "bottom") {
        elna_plug_modified();
    } else if (render_part == "top") {
        // Górna symetryczna połówka (odbicie lustrzane płasko do druku)
        rotate([180, 0, 0]) translate([0, 0, -7.94]) elna_plug_modified();
    }
}

render_split();
