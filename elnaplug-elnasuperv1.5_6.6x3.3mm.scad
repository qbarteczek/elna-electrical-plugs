// Elna Supermatic / Elnasuper Foot Controller Plug
// Wymiar otworów: 6.6 x 3.3 mm (długość x szerokość)
$fn = 60;

slot_w = 3.3; // szerokość otworu (X) w mm
slot_h = 6.6; // długość otworu (Y) w mm

difference() {
    union() {
        import("elnaplug-elnasuperv1.5.stl");
        
        // Wypełnienie oryginalnych otworów (3.0 x 8.0 mm)
        for (x = [-10.5, 0, 10.5]) {
            translate([x, 0, 11])
                cube([3.05, 8.05, 22.0], center=true);
        }
    }
    
    // Wycięcie nowych otworów 6.6x3.3mm
    for (x = [-10.5, 0, 10.5]) {
        translate([x, 0, 11])
            cube([slot_w, slot_h, 26.0], center=true);
    }
}
