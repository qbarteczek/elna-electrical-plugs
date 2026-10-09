# Elna sewing machine plugs — 3D-printable remixes

Small dimensional fixes to two existing Thingiverse models of Elna sewing machine plugs.
Neither model is my original design; see [Attribution and licence](#attribution-and-licence).

*PL: Drobne poprawki wymiarowe dwóch istniejących modeli wtyczek do maszyn Elna (zasilająca i pedału).
Oba modele bazowe pochodzą z Thingiverse i nie są mojego autorstwa.*

> **Mains voltage.** These housings carry 230 V. Do not print them in PLA; use PETG, ABS, ASA or a
> PC blend, with high infill. You build and use them at your own risk.

## 1. Power plug (Elna SP / Star series)

Base model: [Thingiverse 7199180](https://www.thingiverse.com/thing:7199180) by bamckin.
Two-part housing for the 32 × 13 mm socket.

In the original mesh the middle notch on the front edge of both halves is about 5.0 mm wide, while
the two outer notches are about 3.4 mm. `final_plug.scad` replaces the middle notch with a copy of
the outer one, separately on each half, and leaves the rest of the geometry untouched.

| File | What it is |
|---|---|
| `ELNA_SUPERMATIC_PLUG_ORIGINAL.stl` | unmodified original, input for the script |
| `final_plug.scad` | the fix (OpenSCAD) |
| `ELNA_SUPERMATIC_PLUG_naciecie_poprawione.stl` | output of `final_plug.scad` |
| `ELNA_SUPERMATIC_PLUG_srodkowy_otwor_wyrownany.stl` | an earlier export with the middle hole aligned; its source script was not preserved |
| `PODGLAD_*.png` | preview renders |

Render with a recent OpenSCAD build that has the Manifold backend:

```
openscad --backend=manifold -o out.stl final_plug.scad
```

Expected result: 1040 vertices, 2084 facets, genus 2, status NoError. OpenSCAD repairs the original
mesh on import (it is not manifold), so check the result in your slicer before printing.

Not verified on a real part: whether the wider middle notch in the original is a defect or
intentional. Measure your machine's socket first.

## 2. Foot controller plug (Elna elnasuper)

Base model: [Thingiverse 6924689](https://www.thingiverse.com/thing:6924689) by sfiveo13
(`elnaplug-elnasuperv1.5.stl`, plus the connector cover `elna_elnasuper_connector_cover.stl`).
The original has three 3.0 × 8.0 mm slots.

Variants with resized slots, each with its OpenSCAD source next to the STL:

| File | Slot size |
|---|---|
| `elnaplug-elnasuperv1.5_6.6x3.2mm.stl` | 3.2 × 6.6 mm |
| `elnaplug-elnasuperv1.5_6.6x3.3mm.stl` | 3.3 × 6.6 mm |
| `elnaplug-elnasuperv1.5_6.6x3.4mm.stl` | 3.4 × 6.6 mm |
| `elnaplug-elnasuperv1.5_6.6x3.5mm.stl` | 3.5 × 6.6 mm |
| `elnaplug-elnasuperv1.5_plus0.5mm.stl` | original slots enlarged by 0.5 mm (`elna_0_5mm.scad`) |
| `elnaplug-elnasuperv1.5_plus1.0mm.stl` | original slots enlarged by 1.0 mm (`elna_1_0mm.scad`) |
| `elna_plug_parametric_project75.stl` | original slots enlarged by 0.75 mm |

`elna_plug_parametric_project.scad` is the general version: set `extra` to grow or shrink the
original slots by any amount.

## Attribution and licence

Both base models were published on Thingiverse under Creative Commons Attribution-ShareAlike:

- Elna Sewing Machine Power Plug by **bamckin** — https://www.thingiverse.com/thing:7199180
- Elna elnasuper foot controller connector by **sfiveo13** — https://www.thingiverse.com/thing:6924689

Their original licence notes and descriptions are in `references/`. The modified models and the
scripts in this repository are shared under the same Attribution-ShareAlike terms; see `LICENSE.md`.

An earlier, different modification of the power plug (three vertical pins) used to live in this
repository; it remains in the commit history.
