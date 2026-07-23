# Elna Sewing Machines - 3D Printable Electrical Plugs

<p align="center">
  <img src="images/IMG_2005.JPG" height="300" />
  <img src="images/preview_modified.png" height="300" />
</p>
**⚠️ Ważna Informacja:** Ten projekt jest wyłącznie **modyfikacją (remixem)** istniejącego już projektu i nie jest moim bezpośrednim autorskim dziełem. Pierwotnym autorem pomysłu i głównego modelu wtyczki jest użytkownik **bamckin** z serwisu Thingiverse. 
Oryginalny projekt znajduje się pod adresem: [Elna Sewing Machine Power Plug (Thing: 7199180)](https://www.thingiverse.com/thing:7199180).

Wszystkie zdjęcia poglądowe w folderze `images/` oraz pierwotny plik STL w folderze `stls/` nie należą do mnie. Zostały one dołączone do tego repozytorium wyłącznie w celach referencyjnych i edukacyjnych, jako punkt wyjścia dla opracowanych tu modyfikacji.

---

Modyfikacja 3D wtyczki zasilającej do maszyn do szycia Elna (seria SP / Star / Supermatic). 

Projekt jest modyfikacją (remixem) bazowym oryginalnego modelu [Thingiverse 7199180](https://www.thingiverse.com/thing:7199180) autorstwa **bamckin**.

## Specyfikacja Modyfikacji
* **Układ pinów:** Wszystkie **3 piny ustawione pionowo** (w oryginalnym modelu środkowy pin był poziomy).
* **Rozstaw osi pinów:** Dokładnie **12.7 mm** (pół cala) pomiędzy osiami sąsiednich pinów.
* **Komory wewnętrzne:** Wyprofilowane pod wymiary standardowych mosiężnych żeńskich końcówek konektorowych (wszystkie 3 komory pionowe o wymiarach 6.0 mm × 14.0 mm).
* **Udrożnienie kablowe:** Zachowana obszerna komora na ułożenie przewodów oraz odgiętka z ząbkami zaciskającymi na tyłach wtyczki.

## Pliki w Repozytorium
* `models/elna_plug_modified.scad` – Główny kod OpenSCAD dokonujący precyzyjnej modyfikacji na obrysie STL.
* `stls/exports/elna_plug_modified_bottom.stl` – Gotowa dolna połówka wtyczki do druku 3D.
* `stls/exports/elna_plug_modified_top.stl` – Gotowa górna połówka wtyczki do druku 3D.
* `renders/` – Wyrenderowane grafiki poglądowe z programu OpenSCAD.
* `tools/` – Skrypty Python wykorzystane do precyzyjnej analizy geometrii siatki STL.

## Wymagania dotyczące druku 3D
Z uwagi na to, że element ten ma bezpośredni kontakt z przewodami pod napięciem (230V) oraz elementami mosiężnymi mogącymi się nagrzewać:
- **NIE UŻYWAJ PLA** (zbyt niska temperatura mięknienia).
- **Zalecane materiały:** PETG, ABS, ASA, PC-Blend.
- Należy zastosować wysokie wypełnienie (np. 50-100% z 4 obrysami), aby wtyczka nie pękła pod naciskiem kabla.

## Montaż Elementów Stykowych
Modele służą wyłącznie jako obudowy. Aby zbudować wtyczkę, należy użyć rurek z mosiądzu lub uniwersalnych wsuwek konektorowych 2.8mm / 4.8mm dociśniętych na zarobionych przewodach.
Po włożeniu zaciśniętych przewodów w odpowiednie kanały wydruku, obie połówki obudowy należy skręcić śrubą M3.

## Licencja
Projekt udostępniany na licencji **GPL-3.0** w zgodzie z zasadami open-source dla projektów pochodnych. Zobacz plik [LICENSE](LICENSE).
