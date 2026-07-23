// Scena poglądowa wtyczki Elna - Widok złożony i rozłożony
// Zawiera kabel, mosiężne wsuwki/gniazda i obie połówki obudowy

use <elna_plug_option2_parametric.scad>

// =====================
// PARAMETRY SCENY
// =====================
view_mode = "assembled"; // ["assembled", "exploded"]

// Parametry wtyczki (muszą być spójne z option2)
plug_width = 48.0;
plug_length = 100.0;
plug_height = 16.0;
corner_radius = 6.0;
back_taper = 8.0;
pin_spacing = 8.5;
pin_slot_width = 1.6;
pin_slot_length = 5.6;
print_tolerance = 0.2;

// Grubość ściany obudowy
wall = 3.0;

// Odstęp w widoku rozłożonym
explode_gap = 20;

// =====================
// BRYŁY POMOCNICZE
// =====================

module outer_hull() {
    hull() {
        translate([ plug_width/2 - corner_radius,  plug_length/2 - corner_radius, 0]) cylinder(r=corner_radius, h=plug_height, center=true, $fn=60);
        translate([-plug_width/2 + corner_radius,  plug_length/2 - corner_radius, 0]) cylinder(r=corner_radius, h=plug_height, center=true, $fn=60);
        translate([ plug_width/2 - corner_radius - back_taper, -plug_length/2 + corner_radius, 0]) cylinder(r=corner_radius, h=plug_height, center=true, $fn=60);
        translate([-plug_width/2 + corner_radius + back_taper, -plug_length/2 + corner_radius, 0]) cylinder(r=corner_radius, h=plug_height, center=true, $fn=60);
    }
}

module half_plug_body(flip=false) {
    rot = flip ? [180, 0, 0] : [0, 0, 0];
    rotate(rot) {
        difference() {
            outer_hull();
            // Wnętrze komory
            hull() {
                translate([ plug_width/2 - corner_radius - 3,  plug_length/2 - 25, 0]) cylinder(r=corner_radius, h=plug_height-6, center=true, $fn=40);
                translate([-plug_width/2 + corner_radius + 3,  plug_length/2 - 25, 0]) cylinder(r=corner_radius, h=plug_height-6, center=true, $fn=40);
                translate([ plug_width/2 - corner_radius - back_taper - 3, -plug_length/2 + 25, 0]) cylinder(r=corner_radius, h=plug_height-6, center=true, $fn=40);
                translate([-plug_width/2 + corner_radius + back_taper + 3, -plug_length/2 + 25, 0]) cylinder(r=corner_radius, h=plug_height-6, center=true, $fn=40);
            }
            // Kanał kabla
            translate([0, -plug_length/2 + 10, 0]) rotate([90,0,0]) cylinder(d=6.5, h=25, center=true, $fn=40);
            // Otwory na piny
            for(x = [-pin_spacing, 0, pin_spacing]) {
                translate([x, plug_length/2 - 5, 0]) cube([pin_slot_width, pin_slot_length, plug_height+2], center=true);
                translate([x, plug_length/2 - 18, 0]) cube([6.0, 20.0, plug_height - 4], center=true);
            }
            // Śruba centralna
            translate([0, 0, 0]) {
                cylinder(d=3.2, h=plug_height+2, center=true, $fn=30);
                translate([0,0, plug_height/2 - 3]) cylinder(d=6.0, h=6.5, center=true, $fn=30);
                translate([0,0,-plug_height/2 + 3]) cylinder(d=6.5/cos(30), h=6.5, center=true, $fn=6);
            }
            // Odcinamy połówkę (zawsze bierzemy dolną, flip=true ją obraca)
            translate([0, 0, plug_height]) cube([plug_width+10, plug_length+10, plug_height*2], center=true);
        }
    }
}

// =====================
// ELEMENTY WNĘTRZA
// =====================

// Mosiężna wsuwka (żeńskie gniazdo)
module brass_connector(height=12) {
    color("goldenrod") {
        // Główna rurka wsuwki
        difference() {
            cylinder(d=5.0, h=height, center=true, $fn=20);
            cylinder(d=3.5, h=height+1, center=true, $fn=20);
        }
        // Kołnierz tylny
        translate([0, 0, -height/2 + 1]) cylinder(d=6.5, h=2, center=true, $fn=20);
        // Skrzydełka zaciskowe (blaszki)
        for(a = [0, 180]) rotate([0, 0, a]) translate([3, 0, height/2 - 3]) {
            cube([2, 1, 6], center=true);
        }
    }
}

// Końcówka przewodu z blaszką zaciskową
module wire_with_connector(wire_len=50, wire_d=1.5, col="red") {
    color("goldenrod") {
        translate([0, 0, wire_len/2]) cylinder(d=5.0, h=8, center=true, $fn=20);
    }
    color(col) {
        cylinder(d=wire_d, h=wire_len, center=true, $fn=16);
    }
}

// Kabel zbiorczy z opleceniem
module cable(len=70) {
    // Izolacja zewnętrzna
    color("black", 0.9) cylinder(d=7.0, h=len, center=true, $fn=30);
    // Żyły wewnętrzne (3 przewody w wiązce)
    color("brown") translate([1.5, 0, 0])  cylinder(d=2.0, h=len, center=true, $fn=16);
    color("blue")  translate([-1.5, 0, 0]) cylinder(d=2.0, h=len, center=true, $fn=16);
    color("yellow") translate([0, 0, 0])   cylinder(d=2.0, h=len-5, center=true, $fn=16);
}

// =====================
// WIDOKI
// =====================

module scene_assembled() {
    // Dolna połówka
    color("#3a7bd5", 0.85) half_plug_body(flip=false);
    
    // Górna połówka (odbita i uniesiona na właściwą wysokość)
    color("#3a7bd5", 0.85) translate([0, 0, plug_height]) mirror([0,0,1]) half_plug_body(flip=false);
    
    // Kabel wychodzący z tyłu
    translate([0, -plug_length/2 - 15, 0]) rotate([90, 0, 0]) cable(len=30);
    
    // Śruba centralna
    color("silver") translate([0, 0, plug_height/2 - 1]) cylinder(d=3.0, h=plug_height+2, center=true, $fn=20);
}

module scene_exploded() {
    e = explode_gap;
    
    // Górna połówka (uniesiona)
    color("#3a7bd5", 0.9) translate([0, 0, plug_height/2 + e]) half_plug_body(flip=false);
    
    // Dolna połówka
    color("#3a7bd5", 0.9) translate([0, 0, -plug_height/2]) half_plug_body(flip=false);
    
    // Mosiężne wsuwki (widoczne w przestrzeni między połówkami)
    for(x = [-pin_spacing, 0, pin_spacing]) {
        translate([x, plug_length/2 - 14, 0]) rotate([90, 0, 0]) brass_connector(height=12);
    }
    
    // Przewody elektryczne
    color("brown") translate([-pin_spacing, 0, 0]) rotate([90, 0, 0]) wire_with_connector(wire_len=55, col="brown");
    color("blue")  translate([0,  0, 0]) rotate([90, 0, 0]) wire_with_connector(wire_len=55, col="blue");
    color("yellow") translate([pin_spacing, 0, 0]) rotate([90, 0, 0]) wire_with_connector(wire_len=55, col="yellow");
    
    // Kabel zbiorczy
    translate([0, -plug_length/2 - 15, 0]) rotate([90, 0, 0]) cable(len=30);
    
    // Śruba
    color("silver") translate([0, 0, e + plug_height/2 + 5]) cylinder(d=3.0, h=plug_height+5, center=true, $fn=20);
}

// =====================
// RENDER
// =====================

if (view_mode == "assembled") {
    scene_assembled();
} else {
    scene_exploded();
}
