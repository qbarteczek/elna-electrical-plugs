
// Elna Sewing Machine Plug - 3 Vertical Pins Modification
stl_center_x = 32.27;
front_y = 36.37;

pin_slot_w = 1.6;     // szerokość otworu na pin (pionowy)
pin_slot_l = 5.6;     // długość otworu na pin (pionowy)
conn_w = 6.0;         // szerokość komory na wsuwkę mosiężną
conn_l = 14.0;        // długość komory na wsuwkę mosiężną
conn_h = 6.5;         // głębokość komory na wsuwkę

module elna_plug_raw() {
    difference() {
        union() {
            // 1. Watertight import obudowy
            import("/home/qba/Dokumenty/elna-electrical-plugs/stls/ELNA_SUPERMATIC_PLUG_WATERTIGHT.stl");
            
            // 2. Wypełnienie poziomej komory w centrum
            translate([stl_center_x, front_y - 10, 3.5])
                cube([12.6, 20.0, 7.5], center=true);
        }
        
        // 3. Wycięcie pionowego otworu na pin
        translate([stl_center_x, front_y - 2.8, 3.5])
            cube([pin_slot_w, pin_slot_l, 10.0], center=true);
            
        // 4. Wycięcie pionowej komory na mosiężną wsuwkę żeńską
        translate([stl_center_x, front_y - 12.0, 3.5])
            cube([conn_w, conn_l, conn_h], center=true);
            
        // 5. Przejście na przewód
        translate([stl_center_x, front_y - 23.0, 3.5])
            cube([4.0, 10.0, 5.5], center=true);
    }
}

elna_plug_raw();

rotate([180,0,0]) elna_plug_raw();
