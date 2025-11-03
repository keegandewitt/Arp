# Missing CAD Models for Perfect Rendering

**Generated:** 2025-11-03
**Purpose:** Complete component inventory for accurate 3D enclosure visualization

---

## ✅ CAD Models We Have

| Component | File Format | Location |
|-----------|-------------|----------|
| Feather M4 Express | STL, STEP | Feather_M4.stl, Feather_M4_Express.step |
| OLED FeatherWing 128x64 | STL, STEP | OLED_Wing.stl, OLED_FeatherWing.step |
| MIDI FeatherWing | STL, STEP | MIDI_Wing.stl, MIDI_FeatherWing.step |
| **MCP4728 Quad DAC** | **STEP** | **Adafruit_MCP4728_I2C_Quad_DAC.STEP** |
| **Resistors (100Ω, 150Ω, 1kΩ, 10kΩ, 22kΩ)** | **SLDPRT** | **Resistor [value].SLDPRT** |
| **Capacitors (47µF, 0.1µF)** | **SLDPRT** | **Capacitor 47uF-25V.SLDPRT, Capacitor Ceramic 104 0.1uF.SLDPRT** |
| **Schottky Diode (1N5817)** | **SLDPRT** | **Schottky Diode 1N5817.SLDPRT** |

---

## 🔍 Critical Components - CAD Models Needed

### ~~1. MCP4728 Quad DAC (Adafruit #4470)~~ ✅ **DOWNLOADED**
- **Source:** GrabCAD - https://grabcad.com/library/adafruit-mcp4728-i2c-quad-dac-1
- **Format:** STEP file (Adafruit_MCP4728_I2C_Quad_DAC.STEP)
- **Dimensions:** ~20mm × 20mm × ~10mm (with headers)
- **Status:** ✅ Downloaded and copied to enclosure folder

### ~~2. 3.5mm TRS Panel Mount Jacks (6x total)~~ ✅ **DOWNLOADED**
- **Product:** Lsgoodcare 20-pack (Amazon B01DBOBRHQ)
- **Type:** Mono panel mount, 6mm mounting hole
- **Quantity:** 6 needed (CV OUT, TRIG OUT, CC OUT, CV IN, TRIG IN, +1 spare)
- **Exact Dimensions:** 15mm × 11mm × 9mm (L×W×H) / 0.59" × 0.43" × 0.35"
- **Panel hole:** 6mm diameter
- **✅ STATUS:** Downloaded from GrabCAD
- **File:** pj-307.step
- **Source:** https://grabcad.com/library/pj-307-stereo-connector-1

### ~~3. 5-Pin DIN-5 MIDI Jacks (2x)~~ ✅ **ALREADY HAVE**
- **Type:** Panel mount, 180° orientation
- **Quantity:** 2 (MIDI IN, MIDI OUT)
- **Dimensions:**
  - Panel hole: 15.5mm diameter
  - Thread depth: ~10mm
  - Total depth behind panel: ~25mm
- **✅ STATUS:** Included in MIDI_Wing.stl (complete FeatherWing assembly with DIN jacks)
- **File:** MIDI_Wing.stl, MIDI_FeatherWing.step
- **Note:** DIN-5 jacks are part of the complete MIDI FeatherWing CAD model

### 4. USB-C Panel Mount Breakout
- **Type:** Female USB-C breakout board
- **Panel cutout:** 9.5mm × 3.8mm rectangular
- **Depth:** ~15mm behind panel
- **Alternative:** Direct cutout for Feather M4's onboard USB-C (no extension)

### 5. Teyleten Boost Module
- **Function:** 3.7V LiPo → 5V @ 1.5A
- **Dimensions:** ~17mm × 10mm × 4mm (approximate)
- **Notes:** Generic DC-DC boost converter, can model as simple box

### 6. Slide Switch (Model 805)
- **Type:** SPDT slide switch
- **Mounting:** Panel mount or PCB mount
- **Dimensions:** ~8mm × 3mm × 5mm
- **Notes:** Can model as simple rectangular box

### 7. LiPo Battery
- **Capacity:** 500-1200mAh
- **Type:** 3.7V single-cell with JST connector
- **Dimensions (500mAh):** ~30mm × 34mm × 6mm
- **Dimensions (1200mAh):** ~35mm × 50mm × 8mm
- **Notes:** Flexible pouch, can model as soft-cornered box

---

## 📦 Passive Components ✅ **DOWNLOADED**

**Source:** GrabCAD Passive Components Library
- **URL:** https://grabcad.com/library/capacitors-diodes-resistors-1
- **Includes:** Resistors, capacitors, diodes, LEDs, transistors in various packages
- **Status:** ✅ Downloaded and copied specific components to enclosure folder

### LEDs (7 total)
- **5x White LEDs:** 3mm flat-top clear, press-fit into 3.2mm holes
  - Dimensions: 3mm diameter × 5mm height
  - Locations: CV OUT, CC OUT, CV IN, MIDI OUT, MIDI IN

- **2x RGB LEDs:** 3mm flat-top clear common cathode, 3.2mm holes
  - Dimensions: 3mm diameter × 5mm height
  - Locations: TRIG OUT, TRIG IN
  - Note: 4 leads instead of 2

### Resistors (~20 total)
- **Values:** 100Ω, 150Ω, 1kΩ, 10kΩ, 22kΩ
- **Type:** 1/4W axial through-hole
- **Dimensions:** ~6mm length × 2.5mm diameter
- **Model as:** Simple cylinder

### Capacitors
- **2x Electrolytic (47µF 16V):**
  - Dimensions: 5mm diameter × 11mm height
  - Type: Radial through-hole

- **~8x Ceramic (0.1µF, 100nF 50V):**
  - Dimensions: 5mm × 2.5mm × 2mm
  - Type: Radial disc ceramic

### Diodes
- **2x BAT85 Schottky:**
  - Dimensions: 4mm length × 2mm diameter
  - Type: DO-35 glass package

- **1x 2N3904 NPN Transistor:**
  - Dimensions: TO-92 package (4.5mm × 5mm × 4mm)
  - Type: Through-hole transistor

### Standoffs & Hardware
- **M3 Standoffs (8mm-10mm):**
  - Female-Female, hex brass
  - Dimensions: 5mm hex × specified length

- **M2.5 Standoffs (10mm-15mm):**
  - Female-Female, hex brass
  - Dimensions: 4.5mm hex × specified length

---

## 🎯 Modeling Priority

### HIGH PRIORITY (affects enclosure dimensions)
1. ✅ **MCP4728 DAC - DOWNLOADED**
2. ⚠️ 3.5mm TRS jacks - Critical for back panel spacing (STILL NEEDED)
3. ⚠️ DIN-5 MIDI jacks - Large diameter (15.5mm), affects spacing (STILL NEEDED)
4. ⚠️ LiPo battery - Affects internal volume requirements (can model as box)

### MEDIUM PRIORITY (visual accuracy)
5. USB-C breakout or cutout dimensions
6. Boost module placement
7. LED positions and mounting

### LOW PRIORITY (can use simplified geometry)
8. Passive components (resistors, caps, diodes)
9. Standoffs and screws
10. Wire routing

---

## 📐 Component Dimensions Summary

### Bottom Board (OUTPUT)
- **Board:** 108mm × 55mm × 1.6mm protoboard
- **Major components:**
  - MCP4728: ~20mm × 20mm, center of board
  - MIDI FeatherWing: 50.8mm × 22.8mm, right side
  - Boost module: 17mm × 10mm, front section
  - Battery: 30-50mm × 34-50mm, under OUTPUT board
  - 5 LEDs: 3mm diameter, 7mm offset from jacks

### Top Board (INPUT)
- **Board:** 108mm × 55mm × 1.6mm protoboard
- **Major components:**
  - OLED FeatherWing: 50.9mm × 22.9mm, FAR LEFT
  - Feather M4: 50.8mm × 22.8mm, CENTER-RIGHT
  - Input protection circuits: small (10mm × 10mm area each)
  - 2 LEDs: 3mm diameter, 7mm offset from jacks

### Back Panel Jacks (distances from left edge)
**BOTTOM ROW (OUTPUT board):**
- USB-C: 10mm (9.5mm × 3.8mm cutout)
- CV OUT: 22mm + LED at 29mm
- TRIG OUT: 36mm + RGB LED at 43mm
- CC OUT: 50mm + LED at 57mm
- MIDI OUT: 72mm + LED at 84mm (12mm offset!)
- MIDI IN: 96mm + LED at 108mm (12mm offset!)

**TOP ROW (INPUT board):**
- CV IN: 22mm + LED at 29mm
- TRIG IN: 36mm + RGB LED at 43mm

---

## 🔨 Next Steps

1. **Download MCP4728 STEP file from GrabCAD** (requires account)
2. **Search for generic CAD models:**
   - "3.5mm panel mount jack CAD" or "PJ-307 jack"
   - "DIN 41524 5-pin MIDI jack CAD"
   - "USB-C panel mount breakout"
3. **Create simple OpenSCAD modules for:**
   - LEDs (cylinder with flat top)
   - Resistors (cylinder)
   - Capacitors (cylinder for electrolytic, box for ceramic)
   - Battery (rounded box)
   - Standoffs (hex cylinder)
4. **Update hardware_stack_accurate.scad with all components**

---

## 📚 References

### Project Documentation
- BOM: `/docs/hardware/BOM.md`
- Protoboard Layout: `/docs/hardware/PROTOBOARD_LAYOUT.md`
- Back Panel Layout: `/hardware/enclosure/BACK_PANEL_LAYOUT.md`

### CAD Resource Libraries
- **Adafruit CAD Parts:** https://github.com/adafruit/Adafruit_CAD_Parts
  - Official Adafruit repository with STEP/STL files for products
  - Battery models: #258 (1200mAh), #328 (2500mAh)
  - Feather boards, FeatherWings, breakouts, and more
- **GrabCAD Community Library:** https://grabcad.com
  - MCP4728 DAC: https://grabcad.com/library/adafruit-mcp4728-i2c-quad-dac-1
  - PJ-307 3.5mm jack: https://grabcad.com/library/pj-307-stereo-connector-1
  - Passive components: https://grabcad.com/library/capacitors-diodes-resistors-1

---

**END OF DOCUMENT**
