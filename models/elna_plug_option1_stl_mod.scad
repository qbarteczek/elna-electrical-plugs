// Opcja 1: Modyfikacja oryginalnego pliku STL
// Zaimportowanie oryginalnej połówki wtyczki, zalanie środkowego otworu i wycięcie go w pionie.

// Ustaw te wartości w OpenSCAD za pomocą suwaków (Customizer) lub ręcznie,
// tak aby zielony "korek" idealnie przykrył stary, poziomy otwór środkowy.
hole_x = 24.1; // [-10 : 0.1 : 50]
hole_y = 10.0; // [-60 : 0.1 : 40]

// Wymiary szczeliny na wsuwkę
pin_slot_width = 1.6;
pin_slot_length = 5.6;

// Wymiary wnęki na sam mosiężny konektor z zaciśniętym kablem (wewnątrz wtyczki)
connector_width = 6.0;
connector_length = 15.0;

module elna_plug_option1() {
    difference() {
        union() {
            // Import oryginalnego pliku STL
            import("../stls/ELNA_SUPERMATIC_PLUG.stl");
            
            // "Korek" zalewający oryginalny, poziomy otwór (oraz jego wnękę)
            // Dzięki temu mamy "pełny" materiał, w którym możemy wyciąć nowy kształt.
            color("green")
            translate([hole_x, hole_y, 4]) 
                cube([pin_slot_length + 2, pin_slot_width + 4, 15], center=true);
                
            // Dodatkowy korek na wnękę wewnętrzną (jeśli była pozioma)
            color("darkgreen")
            translate([hole_x, hole_y - 10, 4])
                cube([16, 16, 15], center=true);
        }
        
        // Wycięcie pionowej szczeliny na pin wylotowy
        color("red")
        translate([hole_x, hole_y, 4])
            cube([pin_slot_width, pin_slot_length, 20], center=true);
            
        // Wycięcie obszernej wnęki na konektor kabla wewnątrz obudowy
        color("darkred")
        translate([hole_x, hole_y - 12, 4])
            cube([connector_width, connector_length, 20], center=true);
            
        // Gwarancja przejścia na przewód elektryczny (kanał łączący wnękę z główną komorą STL)
        color("blue")
        translate([hole_x, hole_y - 25, 4])
            cube([4, 20, 15], center=true);
    }
}

elna_plug_option1();
