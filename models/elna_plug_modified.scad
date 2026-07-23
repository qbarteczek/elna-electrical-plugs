// Elna Sewing Machine Plug - 3 Vertical Pins Modification
// Based on exact geometric measurements of original Thingiverse model 7199180 by bamckin

/* [Konfiguracja Renderowania] */
// Wybierz część do wyrenderowania w OpenSCAD
render_part = "bottom"; // [bottom:Dolna Połówka do druku, top:Górna Połówka do druku, both:Obie Złożone (Podgląd wtyczki)]

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

module elna_plug_raw() {
    difference() {
        union() {
            // 1. Oryginalna obudowa z pliku STL
            import("../stls/ELNA_SUPERMATIC_PLUG.stl");
            
            // 2. Zalanie (wypełnienie) starej poziomej komory i otworu środkowego
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

// Główny wycentrowany model (wycentrowany w osi X i Y wokół [0,0,0])
module elna_plug_centered() {
    translate([-stl_center_x, 13.0, 0])
        elna_plug_raw();
}

module render_split() {
    if (render_part == "both") {
        // Podgląd obu złączonych połówek wtyczki w osi 0
        elna_plug_centered();
        translate([0, 0, 15.88]) mirror([0, 0, 1]) elna_plug_centered();
    } else if (render_part == "bottom") {
        // Dolna połówka wycentrowana
        elna_plug_centered();
    } else if (render_part == "top") {
        // Górna połówka zorientowana płasko do druku 3D (bez podpór)
        rotate([180, 0, 0]) translate([0, 0, -7.94]) elna_plug_centered();
    }
}

render_split();
