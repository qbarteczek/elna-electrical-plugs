// Skrypt do powiększenia otworów z 3mm do 3.2mm
// Dostosuj poniższe współrzędne X i Y, aby idealnie nałożyć większe walce na istniejące otwory w STL.

/* [Wymiary Otworów] */
// Nowa średnica otworu
new_hole_d = 3.2; 

/* [Pozycje Otworów (do dopasowania)] */
// Otwór 1
hole_1_x = 0;
hole_1_y = 5;

// Otwór 2
hole_2_x = -8;
hole_2_y = -5;

// Otwór 3
hole_3_x = 8;
hole_3_y = -5;

module original_stl() {
    // Import oryginalnego pliku STL
    import("../stls/elnaplug-elnasuperv1.5.stl");
}

module new_holes() {
    // Te walce "wywiercą" nowe otwory 3.2mm
    translate([hole_1_x, hole_1_y, 0]) cylinder(d=new_hole_d, h=100, center=true, $fn=50);
    translate([hole_2_x, hole_2_y, 0]) cylinder(d=new_hole_d, h=100, center=true, $fn=50);
    translate([hole_3_x, hole_3_y, 0]) cylinder(d=new_hole_d, h=100, center=true, $fn=50);
}

// Rysowanie z wyciętymi nowymi otworami
difference() {
    original_stl();
    new_holes();
}

// ODKOMENTUJ PONIŻSZĄ LINIĘ (usuń //), aby podświetlić walce na czerwono i ułatwić ich pozycjonowanie!
// color("red") new_holes();
