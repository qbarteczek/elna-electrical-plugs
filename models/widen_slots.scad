module original_plug() {
    import("../stls/elnaplug-elnasuperv1.5.stl");
}

module filled_plug() {
    union() {
        original_plug();
        // Tworzymy idealnie dopasowane wypełnienie starych otworów:
        // Bierzemy wypukłą powłokę (hull) całej wtyczki, żeby uzyskać jej idealne granice,
        // a następnie przecinamy to z naszymi klockami wypełniającymi.
        // Dzięki temu wypełnienie nie wystaje ani o mikrometr poza oryginalną powierzchnię!
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
    // Nowe, idealnie prostokątne otwory w prawidłowych osiach
    translate([-0.19, 0.03, 11.0]) cube([3.4, 6.9, 30.0], center=true);
    translate([-10.69, 0.03, 11.0]) cube([3.4, 6.9, 30.0], center=true);
    translate([10.31, 0.03, 11.0]) cube([3.4, 6.9, 30.0], center=true);
}

difference() {
    filled_plug();
    widened_slots();
}
