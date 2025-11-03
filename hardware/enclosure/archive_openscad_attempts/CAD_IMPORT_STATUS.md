# CAD Model Import Status

**Updated:** 2025-11-03
**Purpose:** Track progress on importing real CAD models into OpenSCAD visualization

---

## ✅ Successfully Downloaded CAD Models

### Adafruit Hardware (STL + STEP)
- **Feather M4 Express** - `Feather_M4.stl`, `Feather_M4_Express.step`
- **OLED FeatherWing 128x64** - `OLED_Wing.stl`, `OLED_FeatherWing.step`
- **MIDI FeatherWing** - `MIDI_Wing.stl`, `MIDI_FeatherWing.step`

### MCP4728 Quad DAC (STEP)
- **File:** `Adafruit_MCP4728_I2C_Quad_DAC.STEP`
- **Source:** GrabCAD
- **Status:** ✅ Downloaded and copied to enclosure folder

### Passive Components (SLDPRT - SolidWorks)
- **Resistor 100 Ohm.SLDPRT** - Output protection
- **Resistor 150 Ohm.SLDPRT** - LED current limiting
- **Resistor 1K Ohm.SLDPRT** - NPN base resistor
- **Resistor 10K Ohm.SLDPRT** - Voltage divider series
- **Resistor 22K Ohm.SLDPRT** - Voltage divider to ground
- **Capacitor 47uF-25V.SLDPRT** - Bulk power supply filtering
- **Capacitor Ceramic 104 0.1uF.SLDPRT** - Bypass/decoupling
- **Schottky Diode 1N5817.SLDPRT** - Input protection (similar to BAT85)

---

## 📋 OpenSCAD Integration Status

### Created Files
1. **`hardware_stack_with_cad.scad`** - New visualization file that imports real CAD models
   - Uses `import()` for Feather, OLED, and MIDI Wing STL files
   - Includes modules for passive components (LEDs, resistors, capacitors, diodes)
   - Accurate positioning based on PROTOBOARD_LAYOUT.md
   - Height markers showing stack dimensions

2. **`MISSING_CAD_MODELS.md`** - Updated inventory document
   - Marked MCP4728 and passive components as ✅ DOWNLOADED
   - Lists remaining needed components (jacks, connectors)

### Integration Notes
- **STL files:** Can be directly imported into OpenSCAD with `import("filename.stl")`
- **STEP files:** OpenSCAD doesn't natively support STEP - may need conversion to STL
- **SLDPRT files:** SolidWorks format - need to export as STL for OpenSCAD use

### Current Issue
- OpenSCAD reports "mesh not closed" error on one or more imported STL files
- This is common with downloaded STL files and doesn't prevent rendering
- Image generation is in progress

---

## 🔧 File Format Conversion Needed

### For MCP4728 DAC
- **Current:** STEP file (Adafruit_MCP4728_I2C_Quad_DAC.STEP)
- **Need:** Convert to STL for OpenSCAD import
- **Options:**
  1. Use FreeCAD: Import STEP → Export STL
  2. Use online converter
  3. Use simple box placeholder for now (20mm × 20mm × 10mm)

### For Passive Components (SLDPRT files)
- **Current:** SolidWorks format (.SLDPRT)
- **Need:** Convert to STL for OpenSCAD import
- **Options:**
  1. Use FreeCAD: Batch import SLDPRT → Export STL
  2. Create simplified OpenSCAD modules (cylinders, boxes) with correct dimensions
  3. For detailed visualization, conversion recommended

---

## 🎯 Next Steps

### HIGH PRIORITY
1. ✅ **Import Feather, OLED, MIDI Wing STLs** - DONE in hardware_stack_with_cad.scad
2. ⚠️ **Convert MCP4728 STEP to STL** - In progress (using placeholder for now)
3. ⚠️ **Test render and verify positioning** - OpenSCAD render in progress
4. ⚠️ **Find 3.5mm TRS jack CAD models** - Still needed (6 jacks)
5. ⚠️ **Find DIN-5 MIDI jack CAD models** - Still needed (2 jacks)

### MEDIUM PRIORITY
6. Convert passive component SLDPRT files to STL (or use simplified geometry)
7. Add LED models with correct positioning (7mm offset for TRS, 12mm for MIDI)
8. Add battery placeholder (soft-cornered box)
9. Add boost module and switch placeholders

### LOW PRIORITY
10. Wire routing visualization
11. Standoff and screw details
12. Enclosure walls and mounting features

---

## 📐 Key Positioning Data

### Component Locations (from PROTOBOARD_LAYOUT.md)

**BOTTOM Board (OUTPUT):**
- MCP4728 DAC: Center of board (~44mm from left, ~27.5mm from front)
- MIDI Wing: Right side (93mm from left, centered vertically)
- LEDs: 29mm (CV OUT), 43mm (TRIG OUT), 57mm (CC OUT), 84mm (MIDI OUT), 108mm (MIDI IN)

**TOP Board (INPUT):**
- OLED Wing: FAR LEFT (5mm from left edge)
- Feather M4: CENTER-RIGHT (55mm from left edge)
- LEDs: 29mm (CV IN), 43mm (TRIG IN)

### Stack Heights
```
Bottom board:     0.0mm → 1.6mm    (1.6mm PCB)
Air gap:          1.6mm → 9.6mm   (8mm standoffs)
Top board:        9.6mm → 11.2mm  (1.6mm PCB)
Air gap:          11.2mm → 21.2mm (10mm standoffs)
Feather/OLED:     21.2mm → 28.2mm (7mm height, parallel mounting)
```

**Total stack height:** 28.2mm (excluding enclosure walls)

---

## 🐛 Known Issues

1. **OpenSCAD "mesh not closed" error**
   - Source: Imported STL files may have topology issues
   - Impact: Warning only, doesn't prevent rendering
   - Solution: Ignore or repair meshes in MeshLab/netfabb

2. **MCP4728 STEP file not directly usable**
   - OpenSCAD doesn't support STEP format
   - Using placeholder box for now
   - Need FreeCAD or similar to convert

3. **Passive components in SolidWorks format**
   - OpenSCAD can't import .SLDPRT files
   - Options: Convert to STL or use simplified geometry
   - Decision: Use simplified geometric modules for resistors/caps/diodes

---

## 📚 File References

- BOM: `/docs/hardware/BOM.md`
- Layout: `/docs/hardware/PROTOBOARD_LAYOUT.md`
- Back Panel: `/hardware/enclosure/BACK_PANEL_LAYOUT.md`
- Original visualization: `/hardware/enclosure/hardware_stack_accurate.scad`
- **New CAD-based visualization:** `/hardware/enclosure/hardware_stack_with_cad.scad`
- Inventory: `/hardware/enclosure/MISSING_CAD_MODELS.md`

---

**END OF STATUS DOCUMENT**
