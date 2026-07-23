// Elna Sewing Machine Power Plug - Parametric Base
// Remix based on work by bamckin (Thingiverse: 7199180)

// --- Konfiguracja Renderowania ---
// "top" = Górna połówka
// "bottom" = Dolna połówka
// "both" = Obie złożone ze sobą (podgląd)
render_part = "bottom"; // [top, bottom, both]

// Pokazuj oryginalny plik STL w tle jako punkt odniesienia
show_reference_stl = true; 

// Tolerancja druku (luz dla dopasowania części)
print_tolerance = 0.2; 

// --- Główne wymiary obudowy ---
plug_width = 32.0;
plug_height = 13.0;
plug_length = 45.0;

// Wymiary śruby M3
m3_screw_dia = 3.0 + print_tolerance;
m3_head_dia = 5.5 + print_tolerance;
m3_nut_dia = 6.2 + print_tolerance; // szerokość miedzy przeciwleglymi scianami szesciokąta
m3_nut_thickness = 2.4 + print_tolerance;

// Wymiary odgiętki/blokady kabla
cable_dia = 6.0;

module draw_imported_reference() {
    if (show_reference_stl) {
        // Transparentny model w ramach referencji
        %translate([0,0,0]) import("../stls/ELNA_SUPERMATIC_PLUG.stl");
    }
}

module screw_holes() {
    // Środkowy punkt na śrubę zabezpieczającą
    translate([0, 0, 0]) {
        // Przelotowy otwór na śrubę M3
        cylinder(d=m3_screw_dia, h=plug_height+2, center=true, $fn=30);
        
        // Gniazdo na łeb śruby (w górnej połówce)
        translate([0, 0, plug_height/2 - 2])
            cylinder(d=m3_head_dia, h=4, center=true, $fn=30);
            
        // Gniazdo na nakrętkę sześciokątną (w dolnej połówce)
        translate([0, 0, -plug_height/2 + 2])
            cylinder(d=m3_nut_dia / cos(30), h=4, center=true, $fn=6); // 6 ścianek = nakrętka
    }
}

module cable_strain_relief() {
    // Kanał na kabel na końcu obudowy (część tylna)
    translate([0, -plug_length/2 + 5, 0]) {
        rotate([90,0,0]) cylinder(d=cable_dia + print_tolerance, h=20, center=true, $fn=30);
        
        // Ząbki wbijające się delikatnie w izolację, blokujące kabel
        for(y = [-2: 2: 2]) {
            translate([0, y - plug_length/2 + 10, 0])
                rotate([0, 90, 0]) cylinder(d=cable_dia - 1, h=cable_dia+2, center=true, $fn=30);
        }
    }
}

module elna_plug_base() {
    difference() {
        // Główny blok obudowy
        cube([plug_width, plug_length, plug_height], center=true);
        
        // Wycięcia na śruby spinające obudowę
        screw_holes();
        
        // Otwory i zabezpieczenie na kabel
        cable_strain_relief();
        
        // Przestrzeń wewnętrzna na piny mosiężne i złączki 
        // (Wymaga dalszego dopracowania względem STL)
        translate([0, 10, 0]) cube([plug_width - 8, plug_length - 20, plug_height - 4], center=true);
    }
}

// System renderujący (Podział na części)
module render_split() {
    if (render_part == "both") {
        elna_plug_base();
        draw_imported_reference();
    } else if (render_part == "bottom") {
        difference() {
            elna_plug_base();
            // Odcinamy górną połowę (Z > 0)
            translate([0, 0, plug_height]) cube([plug_width+5, plug_length+5, plug_height*2], center=true);
        }
        draw_imported_reference();
    } else if (render_part == "top") {
        // Obracamy płasko do druku (bez podpór)
        rotate([180, 0, 0]) difference() {
            elna_plug_base();
            // Odcinamy dolną połowę (Z < 0)
            translate([0, 0, -plug_height]) cube([plug_width+5, plug_length+5, plug_height*2], center=true);
        }
    }
}

render_split();
