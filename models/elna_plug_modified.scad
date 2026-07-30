// Elna Sewing Machine Plug - 3 Identical Vertical Pins Modification
// Wizualny podgląd i kompilacja w OpenSCAD (F5/F6).

/* [Render Mode] */
// Select which part to preview or export
render_part = "both"; // ["bottom": Bottom Half, "top": Top Half, "both": Both Assembled]

include <modifiers.scad>

module elna_plug_raw() {
    difference() {
        union() {
            // Import original watertight-repaired or original STL
            import("../stls/ELNA_SUPERMATIC_PLUG.stl");
            fill_blocks();
        }
        cut_blocks();
    }
}

// Center model around (0,0,0) in X and Y
module elna_plug_centered() {
    translate([-center_x, 13.0, 0])
        elna_plug_raw();
}

module render_split() {
    if (render_part == "both") {
        // Assembled view of both halves
        elna_plug_centered();
        translate([0, 0, 15.88]) mirror([0, 0, 1]) elna_plug_centered();
    } else if (render_part == "bottom") {
        // Centered bottom half
        elna_plug_centered();
    } else if (render_part == "top") {
        // Centered and flattened top half for 3D printing
        rotate([180, 0, 0]) translate([0, 0, -7.94]) elna_plug_centered();
    }
}

render_split();
