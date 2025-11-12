# PRISME KiCad Project

**Project:** PRISME MIDI/CV Translation Hub
**Location:** `/Users/keegandewitt/Cursor/prisme/hardware/kicad_prisme_project/`

---

## 📂 This Directory Contains:

```
hardware/kicad_prisme_project/
├── PROJECT_README.md          ← This file
├── KICAD_SETUP_GUIDE.md       ← KiCad setup instructions
├── COMPLETE_BOM.csv           ← Full bill of materials
├── reference_schematics/      ← Your SVG schematics
├── docs/                      ← Project-specific docs
├── bom/                       ← BOM exports
└── datasheets/                ← Component datasheets
```

**Your actual KiCad project files (.kicad_pro, .kicad_sch, .kicad_pcb) will be created here.**

---

## 🌍 Universal Libraries (NOT in this folder)

**Adafruit resources are in a SHARED location accessible to all projects:**

### Location:
```
/Users/keegandewitt/Documents/KiCad/
├── Adafruit_3D_Models/        ← 455 3D models (STEP/STL/F3D)
└── Adafruit_Eagle_Library/    ← Eagle imports (.sch/.brd/.lbr)
```

### Why?
- ✅ Access from ANY KiCad project
- ✅ Access from ANY Claude Code session
- ✅ No duplication across projects
- ✅ Update once, applies everywhere

**See:** `/Users/keegandewitt/Documents/KiCad/README_KICAD_LIBRARIES.md`

---

## 🔧 KiCad Environment Variables

**You already added:**
```
ADAFRUIT_3D → /Users/keegandewitt/Documents/KiCad/Adafruit_3D_Models
```

**Also add:**
```
ADAFRUIT_EAGLE → /Users/keegandewitt/Documents/KiCad/Adafruit_Eagle_Library
```

---

## 🚀 Creating Your KiCad Project

### Step 1: Create New Project

```
1. KiCad → File → New Project
2. Navigate to: /Users/keegandewitt/Cursor/prisme/hardware/kicad_prisme_project/
3. Name: prisme_hardware
4. Click Save
```

This creates:
- `prisme_hardware.kicad_pro` (in this directory)
- `prisme_hardware.kicad_sch`
- `prisme_hardware.kicad_pcb`

### Step 2: Import Eagle Components

**USB-C Breakout:**
```
File → Import → Non-KiCad Project
Browse to: /Users/keegandewitt/Documents/KiCad/Adafruit_Eagle_Library/usb_c/
Select: Adafruit USB Type C Downstream Breakout rev B.sch
```

**MCP4728 DAC:**
```
File → Import → Non-KiCad Project
Browse to: /Users/keegandewitt/Documents/KiCad/Adafruit_Eagle_Library/mcp4728/
Select: Adafruit MCP4728.sch
```

### Step 3: Add Adafruit Component Library

```
Preferences → Manage Symbol Libraries → Add
Browse to: /Users/keegandewitt/Documents/KiCad/Adafruit_Eagle_Library/adafruit_library/adafruit.lbr
Nickname: Adafruit
```

---

## 📋 Using Your Resources

### Reference Schematics (Open alongside KiCad):
```
reference_schematics/BOTTOM_PCB_DAC_OUTPUTS.svg
reference_schematics/BOTTOM_PCB_STRIG.svg
reference_schematics/TOP_PCB_CV_IN.svg
reference_schematics/TOP_PCB_TRIG_IN.svg
reference_schematics/POWER_DISTRIBUTION.svg
```

### Complete BOM:
```
COMPLETE_BOM.csv
```
- All component values
- KiCad footprints
- Designators (R1, C1, etc.)
- Supplier info

### Project Docs:
```
docs/ACTUAL_HARDWARE_TRUTH.md
docs/EASYEDA_PCB_DESIGN_GUIDE.md
docs/SCHEMATICS_READY_FOR_PCB.md
```

---

## ✅ Quick Start Checklist

- [x] Universal libraries set up in `/Users/keegandewitt/Documents/KiCad/`
- [x] Environment variable `ADAFRUIT_3D` configured
- [ ] Environment variable `ADAFRUIT_EAGLE` configured
- [ ] Create new KiCad project in this directory
- [ ] Import USB-C and MCP4728 Eagle files
- [ ] Add Adafruit library
- [ ] Build schematics using reference SVGs
- [ ] Design PCB layouts
- [ ] Run DRC/ERC checks
- [ ] Generate Gerbers
- [ ] Order boards!

---

**Ready to start designing!** 🎉

See `KICAD_SETUP_GUIDE.md` for detailed step-by-step instructions.
