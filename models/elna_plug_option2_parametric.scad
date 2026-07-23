// Opcja 2: Pełny model parametryczny tworzony od zera
// Odbudowany na podstawie przybliżonych gabarytów oryginalnej wtyczki (48x100mm)

render_part = "bottom"; // [top, bottom, both]

// Gabaryty
plug_width = 48.0;
plug_length = 100.0;
plug_height = 16.0; // pełna wysokość złączonych 2 połówek
corner_radius = 6.0;
back_taper = 8.0; // zwężenie z tyłu wtyczki

// Tolerancja druku
print_tolerance = 0.2; 

// Piny
pin_spacing = 8.5; 
pin_slot_width = 1.6 + print_tolerance;
pin_slot_length = 5.6 + print_tolerance;

module outer_shell() {
    hull() {
        // Przednie rogi (strona wtykana do maszyny)
        translate([plug_width/2 - corner_radius, plug_length/2 - corner_radius, 0]) 
            cylinder(r=corner_radius, h=plug_height, center=true, $fn=50);
        translate([-plug_width/2 + corner_radius, plug_length/2 - corner_radius, 0]) 
            cylinder(r=corner_radius, h=plug_height, center=true, $fn=50);
            
        // Tylne rogi (zwężone na dłoń i kabel)
        translate([plug_width/2 - corner_radius - back_taper, -plug_length/2 + corner_radius, 0]) 
            cylinder(r=corner_radius, h=plug_height, center=true, $fn=50);
        translate([-plug_width/2 + corner_radius + back_taper, -plug_length/2 + corner_radius, 0]) 
            cylinder(r=corner_radius, h=plug_height, center=true, $fn=50);
    }
}

module screw_holes() {
    translate([0, 0, 0]) {
        cylinder(d=3.2, h=plug_height+2, center=true, $fn=30);
        translate([0, 0, plug_height/2 - 3]) cylinder(d=6.0, h=6.5, center=true, $fn=30);
        translate([0, 0, -plug_height/2 + 3]) cylinder(d=6.5 / cos(30), h=6.5, center=true, $fn=6); 
    }
}

module cable_strain_relief() {
    translate([0, -plug_length/2 + 10, 0]) {
        rotate([90,0,0]) cylinder(d=6.5, h=25, center=true, $fn=30);
        for(y = [-4: 4: 4]) {
            translate([0, y, 0])
                rotate([0, 90, 0]) cylinder(d=5.0, h=8.0, center=true, $fn=30);
        }
    }
}

module pin_slots() {
    // 3 piny ustawione pionowo
    for(x = [-pin_spacing, 0, pin_spacing]) {
        // Wylot pinu
        translate([x, plug_length/2 - 5, 0])
            cube([pin_slot_width, pin_slot_length, plug_height + 2], center=true);
            
        // Wnęka na złącze
        translate([x, plug_length/2 - 18, 0])
            cube([6.0, 20.0, plug_height - 4], center=true);
    }
}

module inner_cavity() {
    // Główna komora wewnątrz wtyczki na ułożenie przewodów
    hull() {
        // Przednia część komory (blisko wnęk na złącza)
        translate([plug_width/2 - corner_radius - 3, plug_length/2 - 25, 0]) 
            cylinder(r=corner_radius, h=plug_height - 6, center=true, $fn=30);
        translate([-plug_width/2 + corner_radius + 3, plug_length/2 - 25, 0]) 
            cylinder(r=corner_radius, h=plug_height - 6, center=true, $fn=30);
            
        // Tylna część komory (zbliża się do wlotu kabla)
        translate([plug_width/2 - corner_radius - back_taper - 3, -plug_length/2 + 25, 0]) 
            cylinder(r=corner_radius, h=plug_height - 6, center=true, $fn=30);
        translate([-plug_width/2 + corner_radius + back_taper + 3, -plug_length/2 + 25, 0]) 
            cylinder(r=corner_radius, h=plug_height - 6, center=true, $fn=30);
    }
}

module elna_plug_option2() {
    difference() {
        outer_shell();
        inner_cavity();
        screw_holes();
        cable_strain_relief();
        pin_slots();
    }
}

module render_split() {
    if (render_part == "both") {
        elna_plug_option2();
    } else if (render_part == "bottom") {
        difference() {
            elna_plug_option2();
            translate([0, 0, plug_height]) cube([plug_width+5, plug_length+5, plug_height*2], center=true);
        }
    } else if (render_part == "top") {
        rotate([180, 0, 0]) difference() {
            elna_plug_option2();
            translate([0, 0, -plug_height]) cube([plug_width+5, plug_length+5, plug_height*2], center=true);
        }
    }
}

render_split();
