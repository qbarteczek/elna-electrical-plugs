// =========================================================================
// ELNA PLUG PARAMETRIC HOLE MODIFIER
// =========================================================================

// Wartość, o którą chcesz powiększyć (lub pomniejszyć) otwory:
// Wpisz wartość dodatnią, np. 0.5 lub 1.0, aby powiększyć otwory.
// Wpisz wartość ujemną, np. -0.5 lub -1.0, aby pomniejszyć otwory.
// Wpisz 0, by zachować wymiar oryginalny.
extra = 0.5; 

// Ścieżka do oryginalnego pliku STL
// (Ponieważ projekt jest zapisany w tym samym folderze, wystarczy podać tylko nazwę)
original_stl = "elnaplug-elnasuperv1.5.stl"; 

// =========================================================================
// LOGIKA MODELU (Zwykle nie wymaga zmian)
// =========================================================================
// Oryginalne wymiary szczelin w pliku bazowym zostały zmierzone jako 3x8 mm.
orig_w = 3.0;
orig_h = 8.0;

module hole_shape(w, h, depth) {
    // Prostokątny kształt otworów, jak w oryginale
    cube([w, h, depth], center=true);
}

// Blok wypełniający całkowicie stare otwory
module hole_filler() {
    // Solidny blok 3x8mm uzupełniający lukę w oryginale (100mm to bezpieczna głębokość)
    hole_shape(orig_w, orig_h, 100); 
}

// Otwór właściwy do wycięcia (uwzględnia nową, zmienioną szerokość)
module new_hole() {
    // Nowy otwór jest wycinany na głębokość 102mm by zapobiec błędom renderingu
    hole_shape(orig_w + extra, orig_h + extra, 102);
}

// BUDOWANIE MODELU
difference() {
    // 1. Konstrukcja pełnej bryły (Oryginał + "zabetonowane" stare otwory)
    union() {
        import(original_stl);
        
        translate([0, 0, 0]) hole_filler();
        translate([-10.5, 0, 0]) hole_filler();
        translate([10.5, 0, 0]) hole_filler();
    }
    
    // 2. Wycinanie nowych otworów, dopasowanych do zmiennej "extra"
    translate([0, 0, 0]) new_hole();
    translate([-10.5, 0, 0]) new_hole();
    translate([10.5, 0, 0]) new_hole();
}
