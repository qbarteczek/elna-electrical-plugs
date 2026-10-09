original_stl = "elnaplug-elnasuperv1.5.stl";
extra = 1.0;

module slot(w, h, depth) {
    cube([w, h, depth], center=true);
}

difference() {
    import(original_stl);
    
    // Middle slot
    translate([0, 0, 0]) slot(3 + extra, 8 + extra, 100);
    // Left slot
    translate([-10.5, 0, 0]) slot(3 + extra, 8 + extra, 100);
    // Right slot
    translate([10.5, 0, 0]) slot(3 + extra, 8 + extra, 100);
}
