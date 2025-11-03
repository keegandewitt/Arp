# PRISME Enclosure Design - CAD Files and Assembly

**Last Updated:** 2025-11-03
**Status:** Ready for Fusion 360 Assembly

---

## Overview

This folder contains all CAD models and assembly scripts for the PRISME hardware enclosure.

**Approach:** Use **Fusion 360 API** for automated, precise assembly based on documentation.

---

## Quick Start

### 1. Run Fusion 360 Assembly Script

```bash
# Copy script to Fusion 360
mkdir -p ~/Library/Application\ Support/Autodesk/Autodesk\ Fusion\ 360/API/Scripts/PRISME_Assembly
cp PRISME_Hardware_Assembly.py ~/Library/Application\ Support/Autodesk/Autodesk\ Fusion\ 360/API/Scripts/PRISME_Assembly/

# Then in Fusion 360:
# Press Shift+S → Select PRISME_Assembly → Run
```

See **[FUSION360_ASSEMBLY_GUIDE.md](FUSION360_ASSEMBLY_GUIDE.md)** for complete instructions.

---

## Files in This Folder

### **Assembly Script (USE THIS)**
- `PRISME_Hardware_Assembly.py` - Fusion 360 API script for automated assembly
- `FUSION360_ASSEMBLY_GUIDE.md` - Complete setup and usage guide

### **Documentation**
- `CORRECT_STACK_LAYOUT.md` - Authoritative vertical stack dimensions
- `FINAL_CAD_STATUS.md` - Complete component inventory
- `BACK_PANEL_LAYOUT.md` - Jack and connector positions

### **CAD Models - Adafruit Boards (STL)**
- `Feather_M4.stl` (1.6MB) - Adafruit Feather M4 Express
- `OLED_Wing.stl` (541KB) - OLED FeatherWing 128x64
- `MIDI_Wing.stl` (716KB) - MIDI FeatherWing with DIN-5 jacks

### **CAD Models - Components (STEP/SLDPRT)**
- `Adafruit_MCP4728_I2C_Quad_DAC.STEP` - Quad 12-bit DAC module
- `Battery_1200mAh_258.step` - LiPo battery (50×35×8mm)
- `pj-307.step` - 3.5mm TRS audio jack (6× needed)
- `Resistor_*.SLDPRT` - Various resistors (100Ω, 150Ω, 1kΩ, 10kΩ, 22kΩ)
- `Capacitor*.SLDPRT` - Capacitors (47µF, 0.1µF)
- `Schottky Diode 1N5817.SLDPRT` - Protection diodes

### **Enclosure STL (Previous Attempts)**
- `prisme_box_FINAL.stl` - Basic enclosure box
- `prisme_lid_FINAL.stl` - Basic enclosure lid
- *(Note: These need updating after Fusion 360 assembly)*

### **Archive**
- `archive_openscad_attempts/` - Previous OpenSCAD visualization attempts (36 files)

---

## Component Stack (Quick Reference)

```
┌─────────────────────────┐
│  OLED FeatherWing       │  Z = 43.2mm (STACKED on Feather)
└─────────────────────────┘
          ↑ 10mm headers
┌─────────────────────────┐
│  Feather M4 Express     │  Z = 25.2mm
└─────────────────────────┘
          ↑ 10mm standoffs
┌─────────────────────────┐
│  TOP Protoboard         │  Z = 13.6mm (CV IN, TRIG IN)
└─────────────────────────┘
          ↑ 8mm standoffs
┌─────────────────────────┐
│  BOTTOM Protoboard      │  Z = 4.0mm (outputs, MCP4728, MIDI)
└─────────────────────────┘
          ↑ 4mm clearance
        ╔═══════════════╗
        ║  1200mAh LiPo ║  Z = -6.0mm (under board)
        ╚═══════════════╝

Total height: 50.2mm (+ 2mm clearance = 52.2mm minimum)
```

---

## Enclosure Requirements

Based on hardware assembly:

**Internal Dimensions (minimum):**
- Width: 113mm (108mm board + 5mm clearance)
- Depth: 80-85mm (55mm board + rear jack depth ~25mm)
- Height: 52-60mm (50.2mm stack + clearance)

**Back Panel Cutouts:**

**BOTTOM ROW (Output Board):**
- 10mm: USB-C (9.5×3.8mm rectangular)
- 22mm: CV OUT jack (6mm ø) + LED hole (3.2mm ø at 29mm)
- 36mm: TRIG OUT jack (6mm ø) + RGB LED (3.2mm ø at 43mm)
- 50mm: CC OUT jack (6mm ø) + LED (3.2mm ø at 57mm)
- 72mm: MIDI OUT jack (15.5mm ø) + LED (3.2mm ø at 84mm)
- 96mm: MIDI IN jack (15.5mm ø) + LED (3.2mm ø at 108mm)

**TOP ROW (Input Board):**
- 22mm: CV IN jack (6mm ø) + LED (3.2mm ø at 29mm)
- 36mm: TRIG IN jack (6mm ø) + RGB LED (3.2mm ø at 43mm)

---

## Next Steps

1. ✅ Run Fusion 360 assembly script
2. ⬜ Design enclosure around assembled hardware
3. ⬜ Add mounting holes for standoffs
4. ⬜ Create back panel with exact jack positions
5. ⬜ Export for 3D printing or manufacturing

---

## Notes

- All dimensions verified against manufacturer specifications
- Stack heights match CORRECT_STACK_LAYOUT.md exactly
- OpenSCAD attempts archived (visualization inadequate for precision work)
- Fusion 360 chosen for professional CAD accuracy

---

**For Questions:** See FUSION360_ASSEMBLY_GUIDE.md or FINAL_CAD_STATUS.md
