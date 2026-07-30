// OpenSCAD modifiers for Elna Plug - 3 Vertical Pins Modification
mode = "both"; // ["fill", "cut", "both"]

// === GEOMETRIC PARAMETERS ===
center_x = 32.269119;
body_front_y = 36.372837;
cap_front_y = -63.325489;

pin_slot_w = 1.6;     // Width of pin insertion slot
pin_slot_l = 5.6;     // Length of pin insertion slot
conn_w = 6.0;         // Width of brass connector chamber
conn_l = 14.0;        // Length of brass connector chamber
conn_h = 5.5;         // Height of brass connector chamber
wire_w = 4.0;         // Width of wire channel
wire_l = 10.0;        // Length of wire channel

module fill_blocks() {
    // Fill bottom center horizontal chamber
    translate([center_x, 11.0, 3.5])
        cube([13.5, 24.0, 8.0], center=true);
        
    // Fill top center horizontal chamber
    translate([center_x, -33.0, 3.5])
        cube([13.5, 24.0, 8.0], center=true);
}

module cut_blocks() {
    // --- BOTTOM HALF ---
    // Vertical pin entry slot
    translate([center_x, body_front_y - 2.8, 3.5])
        cube([pin_slot_w, pin_slot_l, 10.0], center=true);
    // Vertical brass connector chamber
    translate([center_x, body_front_y - 12.0, 5.26])
        cube([conn_w, conn_l, conn_h], center=true);
    // Wire channel
    translate([center_x, body_front_y - 23.0, 5.26])
        cube([wire_w, wire_l, conn_h], center=true);

    // --- TOP HALF ---
    // Vertical pin entry slot
    translate([center_x, cap_front_y + 2.8, 3.5])
        cube([pin_slot_w, pin_slot_l, 10.0], center=true);
    // Vertical brass connector chamber
    translate([center_x, cap_front_y + 12.0, 5.26])
        cube([conn_w, conn_l, conn_h], center=true);
    // Wire channel
    translate([center_x, cap_front_y + 23.0, 5.26])
        cube([wire_w, wire_l, conn_h], center=true);
}

if (mode == "fill") {
    fill_blocks();
} else if (mode == "cut") {
    cut_blocks();
}
