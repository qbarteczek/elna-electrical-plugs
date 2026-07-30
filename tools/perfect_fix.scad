// PERFECT FIX FOR ELNA PLUG
// This script perfectly morphs the center slots to match the left vertical slots,
// without touching any other part of the plug geometry (no protruding blocks, no wire channel blockage).

module original_plug() {
    import("../stls/ELNA_SUPERMATIC_PLUG_MANIFOLD.stl");
}

// ==========================================
// BOTTOM HALF
// ==========================================
module bottom_left_hole_solid() {
    difference() {
        // A tight bounding box around the left hole's brass insert pocket
        // Left center: X=16.046, Y=12.191. Z=0.0 to 3.5 is safe.
        translate([16.046, 12.191, 1.75]) 
            cube([10.0, 8.0, 3.5], center=true); 
        original_plug();
    }
}

module bottom_center_vertical_hole() {
    // Translate the solid hole to the center slot
    // dX = 16.746, dY = -5.709
    translate([16.746, -5.709, 0]) bottom_left_hole_solid();
}

module bottom_fill_horizontal_slot() {
    // A block that perfectly fills the center horizontal slot's brass insert pocket
    // Center center: X=32.792, Y=6.482
    // We make it slightly wider in X and Y to embed into the plastic walls.
    // Z must be strictly 0.0 to 3.0 to avoid blocking the wire channel.
    translate([32.792, 6.482, 1.5])
        cube([13.0, 9.0, 3.0], center=true);
}

// ==========================================
// TOP HALF
// ==========================================
module top_left_hole_solid() {
    difference() {
        // Top left center: X=15.609, Y=-30.408. Z=0.0 to 3.5 is safe.
        translate([15.609, -30.408, 1.75]) 
            cube([10.0, 8.0, 3.5], center=true); 
        original_plug();
    }
}

module top_center_vertical_hole() {
    // Translate the solid hole to the center slot
    // dX = 17.219, dY = -0.904
    translate([17.219, -0.904, 0]) top_left_hole_solid();
}

module top_fill_horizontal_slot() {
    // Top center center: X=32.828, Y=-31.312
    translate([32.828, -31.312, 1.5])
        cube([13.0, 9.0, 3.0], center=true);
}

// ==========================================
// FINAL ASSEMBLY
// ==========================================
difference() {
    union() {
        original_plug();
        
        // Fill the horizontal slots with solid plastic
        bottom_fill_horizontal_slot();
        top_fill_horizontal_slot();
    }
    
    // Cut the new vertical slots perfectly using the extracted void shapes
    bottom_center_vertical_hole();
    top_center_vertical_hole();
}
