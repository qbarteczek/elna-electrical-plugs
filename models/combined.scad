// [Konfiguracja Renderowania]
render_part = "both"; 
split_y = -0.35; 
screw_hole_d = 3.2;
screw_head_d = 6.0;
screw_1_z = 3.0;
screw_1_x = 0.0;
screw_2_z = 19.0;
screw_2_x = 0.0;

module original_plug() {
    import("../stls/elnaplug-elnasuperv1.5.stl");
}

module filled_plug() {
    union() {
        original_plug();
        intersection() {
            hull() original_plug();
            union() {
                translate([-0.19, 0.03, 11.0]) cube([4.0, 9.0, 30.0], center=true);
                translate([-10.69, 0.03, 11.0]) cube([4.0, 9.0, 30.0], center=true);
                translate([10.31, 0.03, 11.0]) cube([4.0, 9.0, 30.0], center=true);
            }
        }
    }
}

module widened_slots() {
    translate([-0.19, 0.03, 11.0]) cube([3.4, 6.9, 30.0], center=true); 
    translate([-12.89, 0.03, 11.0]) cube([3.4, 6.9, 30.0], center=true); 
    translate([12.51, 0.03, 11.0]) cube([3.4, 6.9, 30.0], center=true); 
}

module modified_plug() {
    difference() {
        filled_plug();
        widened_slots();
    }
}

module screw_holes() {
    translate([screw_1_x, split_y, screw_1_z]) {
        rotate([90, 0, 0]) cylinder(d=screw_hole_d, h=40, center=true, $fn=30);
        translate([0, 10 + 2.0, 0]) rotate([90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
        translate([0, -10 - 2.0, 0]) rotate([-90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
    }
    translate([screw_2_x, split_y, screw_2_z]) {
        rotate([90, 0, 0]) cylinder(d=screw_hole_d, h=40, center=true, $fn=30);
        translate([0, 10 + 2.0, 0]) rotate([90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
        translate([0, -10 - 2.0, 0]) rotate([-90, 0, 0]) cylinder(d=screw_head_d, h=20, $fn=30);
    }
}

module plug_with_screws() {
    difference() {
        modified_plug();
        screw_holes();
    }
}

if (render_part == "both") {
    plug_with_screws();
}
if (render_part == "bottom") {
    translate([0, 0, -split_y]) rotate([90, 0, 0])
    difference() {
        plug_with_screws();
        translate([0, split_y + 50, 0]) cube([100, 100, 100], center=true);
    }
}
if (render_part == "top") {
    translate([0, 0, split_y]) rotate([-90, 0, 0])
    difference() {
        plug_with_screws();
        translate([0, split_y - 50, 0]) cube([100, 100, 100], center=true);
    }
}
