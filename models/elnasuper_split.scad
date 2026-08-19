// Elna elnasuper plug - Split into two screwable halves
// Wzorowane na Elna Supermatic Plug
// Oparty o oryginalny model: elnaplug-elnasuperv1.5.stl

/* [Konfiguracja Renderowania] */
// Wybierz część do wyrenderowania w OpenSCAD
render_part = "both"; // [bottom:Dolna Połówka do druku, top:Górna Połówka do druku, both:Obie Złożone (Podgląd)]

/* [Parametry Cięcia] */
// Środek osi Y (miejsce cięcia na połówki)
split_y = -0.35; 

/* [Otwory na Śruby] */
// Średnica otworu na śrubę (np. M3 = 3.2mm luzu)
screw_hole_d = 3.2;
// Średnica łba śruby lub nakrętki (dla pogłębienia)
screw_head_d = 6.0;

// Śruba 1 (Z, X)
screw_1_z = 3.0;
screw_1_x = 0.0;

// Śruba 2 (Z, X)
screw_2_z = 19.0;
screw_2_x = 0.0;

use <widen_slots.scad>

module modified_plug() {
    difference() {
        filled_plug();
        widened_slots();
    }
}

module screw_holes() {
    // Śruba 1
    translate([screw_1_x, split_y, screw_1_z]) {
        // Przelot na śrubę
        rotate([90, 0, 0]) cylinder(d=screw_hole_d, h=40, center=true, $fn=30);
        // Pogłębienie góra (top part)
        translate([0, 10 + 2.0, 0]) rotate([90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
        // Pogłębienie dół (bottom part)
        translate([0, -10 - 2.0, 0]) rotate([-90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
    }
    // Śruba 2
    translate([screw_2_x, split_y, screw_2_z]) {
        // Przelot na śrubę
        rotate([90, 0, 0]) cylinder(d=screw_hole_d, h=40, center=true, $fn=30);
        // Pogłębienie góra (top part)
        translate([0, 10 + 2.0, 0]) rotate([90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
        // Pogłębienie dół (bottom part)
        translate([0, -10 - 2.0, 0]) rotate([-90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
    }
}

module plug_with_screws() {
    difference() {
        modified_plug();
        screw_holes();
    }
}

module render_split() {
    if (render_part == "both") {
        plug_with_screws();
    } else if (render_part == "bottom") {
        // Dolna połówka zorientowana płasko do druku (cięciem do stołu)
        translate([0, 0, -split_y]) rotate([90, 0, 0])
        difference() {
            plug_with_screws();
            // Ucinamy górną część
            translate([0, split_y + 50, 0]) cube([100, 100, 100], center=true);
        }
    } else if (render_part == "top") {
        // Górna połówka zorientowana płasko do druku (cięciem do stołu)
        translate([0, 0, split_y]) rotate([-90, 0, 0])
        difference() {
            plug_with_screws();
            // Ucinamy dolną część
            translate([0, split_y - 50, 0]) cube([100, 100, 100], center=true);
        }
    }
}

render_split();
