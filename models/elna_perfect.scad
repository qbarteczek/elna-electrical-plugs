// Modyfikacja wtyczki Elna Sewing Machine - 3 Identyczne Pionowe Wsuwki / Piny
// Zmiana dotyczy WYŁĄCZNIE wgłębienia centralnego. Lewe i prawe wgłębienia oraz obudowa pozostają oryginalne.

center_x = 32.27;        // Środek osi centralnej wtyczki (X)
body_front_y = 36.37;    // Przód dolnej połówki obudowy (Y)
cap_front_y = -63.33;    // Przód górnej połówki obudowy (Y)

// Dokładne wymiary pionowej wnęki i kanału (zgodne z rowkami sąsiednimi)
pin_slot_w = 1.6;        // Szerokość otworu wsadowego pinu (mm)
pin_slot_l = 5.6;        // Długość otworu wsadowego pinu (mm)
conn_w = 6.0;            // Szerokość komory na mosiężną wsuwkę żeńską (mm)
conn_l = 14.0;           // Długość komory na wsuwkę (mm)
conn_h = 5.5;            // Głębokość komory (od Z=2.515 do górnej krawędzi)
wire_w = 4.0;            // Szerokość kanału na przewód (mm)
wire_l = 10.0;           // Długość kanału na przewód (mm)

module fill_blocks() {
    // Wypełnienie wyłącznie oryginalnej poziomej komory w części dolnej
    translate([center_x, 11, 3.5])
        cube([13.0, 24.0, 8.0], center=true);
        
    // Wypełnienie wyłącznie oryginalnej poziomej komory w części górnej
    translate([center_x, -33, 3.5])
        cube([13.0, 24.0, 8.0], center=true);
}

module cut_blocks() {
    // --- DOLNA POŁÓWKA OBUDOWY ---
    // Otwór wsadowy pinu (przelotowy)
    translate([center_x, body_front_y - 2.8, 3.5])
        cube([pin_slot_w, pin_slot_l, 10.0], center=true);
    // Komora na wsuwkę żeńską (dno na Z = 2.515 mm, dokładnie jak w sąsiednich rowkach)
    translate([center_x, body_front_y - 12.0, 5.26])
        cube([conn_w, conn_l, conn_h], center=true);
    // Kanał doprowadzający przewód (dno na Z = 2.515 mm)
    translate([center_x, body_front_y - 23.0, 5.26])
        cube([wire_w, wire_l, conn_h], center=true);

    // --- GÓRNA POŁÓWKA OBUDOWY ---
    // Otwór wsadowy pinu (przelotowy)
    translate([center_x, cap_front_y + 2.8, 3.5])
        cube([pin_slot_w, pin_slot_l, 10.0], center=true);
    // Komora na wsuwkę żeńską (dno na Z = 2.515 mm)
    translate([center_x, cap_front_y + 12.0, 5.26])
        cube([conn_w, conn_l, conn_h], center=true);
    // Kanał doprowadzający przewód (dno na Z = 2.515 mm)
    translate([center_x, cap_front_y + 23.0, 5.26])
        cube([wire_w, wire_l, conn_h], center=true);
}


module final_plug() {
    difference() {
        union() {
            import("../stls/ELNA_SUPERMATIC_PLUG_WATERTIGHT.stl");
            fill_blocks();
        }
        cut_blocks();
    }
}

final_plug();

