// Elna Sewing Machine Power Plug - middle socket notch widened to match
// the two outer (good) notches. Modifies ONLY the middle notch on each half;
// everything else is the untouched original geometry from thing:7199180.
//
// Measured directly from the pristine original mesh:
//   BOTTOM half (front edge Y=36.37):
//     Notch 1 (left,  good):  X 19.769 .. 23.216
//     Notch 2 (middle, bad):  X 29.787 .. 34.794   <- replaced
//     Notch 3 (right, good):  X 41.365 .. 44.769
//   TOP half (front edge Y=-63.33, mirrored):
//     Notch 1 (left,  good):  X 19.769 .. 23.198
//     Notch 2 (middle, bad):  X 29.769 .. 34.769   <- replaced
//     Notch 3 (right, good):  X 41.340 .. 44.769

module original_plug() {
    import("ELNA_SUPERMATIC_PLUG_ORIGINAL.stl");
}

// ---------- BOTTOM HALF ----------
BOT_N1_CX = 21.49;   // (19.769+23.216)/2
BOT_N2_CX = 32.29;   // (29.787+34.794)/2
BOT_DX = BOT_N2_CX - BOT_N1_CX;

module bot_notch1_void() {
    difference() {
        translate([BOT_N1_CX, 24.5, 4.5]) cube([5.5, 27, 9], center=true);
        original_plug();
    }
}
module bot_notch2_clone() {
    translate([BOT_DX, 0, 0]) bot_notch1_void();
}
module bot_fill_old_notch2() {
    intersection() {
        hull() original_plug();
        translate([BOT_N2_CX, 24.5, 5.6]) cube([5.5, 27, 3.0], center=true);
    }
}

// ---------- TOP HALF ----------
TOP_N1_CX = 21.48;   // (19.769+23.198)/2
TOP_N2_CX = 32.27;   // (29.769+34.769)/2
TOP_DX = TOP_N2_CX - TOP_N1_CX;

module top_notch1_void() {
    difference() {
        translate([TOP_N1_CX, -51.46, 4.5]) cube([5.5, 27, 9], center=true);
        original_plug();
    }
}
module top_notch2_clone() {
    translate([TOP_DX, 0, 0]) top_notch1_void();
}
module top_fill_old_notch2() {
    intersection() {
        hull() original_plug();
        translate([TOP_N2_CX, -51.46, 5.6]) cube([5.5, 27, 3.0], center=true);
    }
}

difference() {
    union() {
        original_plug();
        bot_fill_old_notch2();
        top_fill_old_notch2();
    }
    bot_notch2_clone();
    top_notch2_clone();
}
