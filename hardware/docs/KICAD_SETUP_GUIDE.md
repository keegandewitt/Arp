# KiCad Project Setup Guide - PRISME Hardware

**Created:** 2025-11-11
**Purpose:** Complete setup instructions for designing PRISME PCBs in KiCad

---

## 📂 Project Structure

```
hardware/kicad_project/
├── KICAD_SETUP_GUIDE.md           ← This file
├── COMPLETE_BOM.csv               ← Full BOM with KiCad footprints
├── eagle_imports/                 ← Adafruit Eagle files for import
│   ├── usb_c/                     (USB-C 4090 breakout)
│   ├── mcp4728/                   (MCP4728 DAC)
│   ├── midi_featherwing/          (6N138 + DIN-5)
│   ├── oled_featherwing/          (OLED + buttons)
│   └── adafruit_library/          (3.3MB component library)
├── reference_schematics/          ← Your existing schemdraw schematics
├── bom/                           ← BOM files
├── datasheets/                    ← Component datasheets
└── docs/                          ← Hardware documentation
```

---

## 🚀 Quick Start - Create New KiCad Project

### 1. Launch KiCad and Create Project
```
1. Open KiCad
2. File → New Project
3. Save to: /Users/keegandewitt/Cursor/prisme/hardware/kicad_project/
4. Project name: prisme_hardware
```

This will create:
- `prisme_hardware.kicad_pro` (project file)
- `prisme_hardware.kicad_sch` (schematic)
- `prisme_hardware.kicad_pcb` (PCB layout)

### 2. Set Up 3D Models Path (IMPORTANT!)

**KiCad Environment Variables:**

1. **Open Preferences:**
   - KiCad → Preferences → Configure Paths

2. **Add Adafruit 3D Models variable:**
   ```
   Variable Name: ADAFRUIT_3D
   Path: /Users/keegandewitt/Documents/KiCad/Adafruit_3D_Models
   ```

3. **Click OK** to save

**In your footprints, reference 3D models like this:**
```
${ADAFRUIT_3D}/4090 USB Type C/USB Type C.step
${ADAFRUIT_3D}/4470 MCP4728 DAC/MCP4728.step
${ADAFRUIT_3D}/4650 OLED FeatherWing/OLED FeatherWing.step
```

---

## 📥 Importing Eagle Files into KiCad

### Method 1: Import Entire Eagle Project
```
1. File → Import → Import Non-KiCad Project
2. Select file type: Eagle .sch or .brd
3. Browse to eagle_imports/ folder
4. Select the .sch file you want
5. Click Import
```

**For your urgent components:**
- **USB-C:** Import `eagle_imports/usb_c/Adafruit USB Type C...rev B.sch`
- **MCP4728:** Import `eagle_imports/mcp4728/Adafruit MCP4728.sch`

### Method 2: Import Eagle Library
```
1. Preferences → Manage Symbol Libraries
2. Click "+" to add library
3. Browse to: eagle_imports/adafruit_library/adafruit.lbr
4. Give it a nickname: "Adafruit"
5. Click OK
```

Now you can search for components like "Adafruit:BAT85" in the schematic editor!

---

## 🔧 Component Library Setup

### Standard KiCad Libraries (Built-in)

KiCad has most generic components:
- Resistors → Library: Device
- Capacitors → Library: Device
- LEDs → Library: Device
- Transistors → Library: Device
- DIP ICs → Library: Package_DIP
- SMD passives → Footprints in Resistor_SMD, Capacitor_SMD

### Custom/Adafruit Components

For Adafruit-specific parts, you have two options:

**Option A: Import from Eagle** (recommended for exact Adafruit footprints)
1. Import the Eagle .sch file
2. Extract the component you need
3. Save to your custom library

**Option B: Use KiCad Standard + Modify**
1. Use generic footprint (e.g., MSOP-10 for MCP4728)
2. Add 3D model manually
3. Works for most components except breakout boards

---

## 📐 Creating Your Schematics

### Hierarchical Design (Recommended)

Your design has two boards - use **hierarchical sheets**:

```
Main Schematic (prisme_hardware.kicad_sch)
├── Sheet: TOP_BOARD.kicad_sch
│   ├── CV IN circuit
│   ├── TRIG IN circuit
│   ├── MIDI IN circuit
│   └── Power decoupling
└── Sheet: BOTTOM_BOARD.kicad_sch
    ├── MCP4728 DAC
    ├── CV/TRIG/CC OUT circuits
    ├── S-Trig circuit
    ├── MIDI OUT circuit
    ├── USB-C power input
    └── Power decoupling
```

**How to create sheets:**
1. In schematic editor: Place → Hierarchical Sheet
2. Draw rectangle for sheet
3. Name it "TOP_BOARD" or "BOTTOM_BOARD"
4. Double-click to edit sub-schematic

### Using Your Reference Schematics

Open your existing SVG schematics alongside KiCad:
```
reference_schematics/
├── TOP_PCB_CV_IN.svg           ← Reference while building CV IN circuit
├── TOP_PCB_TRIG_IN.svg         ← Reference for TRIG IN
├── BOTTOM_PCB_DAC_OUTPUTS.svg  ← Reference for DAC outputs
├── BOTTOM_PCB_STRIG.svg        ← Reference for S-Trig
└── POWER_DISTRIBUTION.svg      ← Reference for power system
```

**Workflow:**
1. Open SVG in browser or image viewer
2. Recreate circuit in KiCad schematic
3. Cross-reference component values from COMPLETE_BOM.csv

---

## 🎨 Component Footprint Selection

### From Your BOM

Every component in `COMPLETE_BOM.csv` has a suggested KiCad footprint:

**Common footprints:**
```
Resistors (SMD):     Resistor_SMD:R_0805_2012Metric
Capacitors (SMD):    Capacitor_SMD:C_0805_2012Metric
Capacitors (Electro): Capacitor_THT:CP_Radial_D5.0mm_P2.00mm
LEDs (3mm THT):      LED_THT:LED_D3.0mm
Diodes (DO-35):      Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal
Transistor (TO-92):  Package_TO_SOT_THT:TO-92_Inline
DIP-8 ICs:           Package_DIP:DIP-8_W7.62mm
3.5mm Jacks:         Connector_Audio:Jack_3.5mm_CUI_SJ1-3523NG_Horizontal
DIN-5 MIDI:          Connector_Audio:Jack_DIN-5_180degree
```

### Missing Footprints (Create Custom)

For Adafruit breakouts you'll need custom footprints:

**USB-C Breakout (4090):**
- Import from Eagle OR
- Create custom footprint:
  - Size: 20.4mm x 14.2mm
  - 8 pins: 0.1" (2.54mm) pitch
  - Reference Eagle .brd file for exact dimensions

**MCP4728 (if using breakout):**
- Import from Eagle OR
- Use standard MSOP-10 footprint if using bare IC

---

## 🖼️ 3D Models

### Adafruit 3D Models Location

**Base path:** `/Users/keegandewitt/Documents/KiCad/Adafruit_3D_Models/`

**Available models (once clone completes):**
```
4090 USB Type C/
├── USB Type C.step
├── USB Type C.stl
└── USB Type C.f3d (Fusion 360)

4470 MCP4728 DAC/
├── MCP4728.step
├── MCP4728.stl
└── MCP4728.f3d

4650 OLED FeatherWing/
├── OLED FeatherWing.step
├── OLED FeatherWing.stl
└── OLED FeatherWing.f3d

4759 Feather M4 CAN/
├── Feather M4 CAN.step
├── Feather M4 CAN.stl
└── Feather M4 CAN.f3d
```

### Adding 3D Models to Footprints

1. **In PCB Editor:**
   - Right-click footprint → Properties → 3D Settings

2. **Add model:**
   - Click "+" button
   - Browse to: `${ADAFRUIT_3D}/[product folder]/[model].step`
   - Adjust scale/rotation/offset as needed

3. **View 3D:**
   - View → 3D Viewer (Alt+3)

---

## 📊 Using the Complete BOM

### Import BOM into KiCad

1. **Open schematic editor**

2. **Place components from BOM:**
   - Add symbol (hotkey: A)
   - Search for component (e.g., "R" for resistor)
   - Set value from BOM (e.g., "10kΩ")
   - Set reference designator (e.g., "R1")

3. **Assign footprints:**
   - Tools → Assign Footprints
   - Match each symbol to footprint from BOM CSV

4. **Export BOM later:**
   - Tools → Generate BOM
   - Use CSV or XML output

### Component Sourcing from BOM

The BOM includes supplier info:
- **Adafruit parts:** Order from adafruit.com
- **BAT85 diodes:** Amazon (ALLECIN 100pcs pack)
- **Generic parts:** Digikey, Mouser, LCSC

---

## 🔌 Pin Assignments (Critical!)

### Feather M4 Connections

**From your hardware docs - these MUST match:**

| M4 Pin | Signal | Goes To | Board |
|--------|--------|---------|-------|
| USB | 5V | 5V Rail | Both |
| 3V3 | 3.3V | 3.3V Rail | Both |
| GND | Ground | GND | Both |
| SDA | I2C Data | MCP4728 | Bottom |
| SCL | I2C Clock | MCP4728 | Bottom |
| A3 | ADC | CV IN tap | Top |
| A4 | ADC | TRIG IN tap | Top |
| D4 | GPIO | CV IN LED | Top |
| D10 | GPIO | S-Trig transistor | Bottom |
| D11 | GPIO | TRIG IN LED | Top |
| D23 | GPIO | LED (future) | Top |
| D24 | GPIO | LED (future) | Top |

**Add these as net labels in your schematic!**

---

## 🎯 PCB Layout Tips

### Board Dimensions
- **Size:** 90mm × 55mm each board
- **Thickness:** 1.6mm standard
- **Layers:** 2-layer is sufficient

### Stack Configuration
```
TOP:    OLED FeatherWing (stacked on M4)
        ↓ (female headers)
MIDDLE: Feather M4 CAN Express
        ↓ (stacking headers to bottom board)
BOTTOM: Your custom bottom PCB
        ↓ (10mm standoffs)
BASE:   Your custom top PCB
```

**Inter-board connections:**
- Use 2×8 header for signals between your two custom boards
- Feather stacks via 2×16 headers

### Component Placement
- **Power components near M4 connection point**
- **DAC close to output jacks** (short traces)
- **Keep I2C traces short** (SDA/SCL to MCP4728)
- **Ground plane on both layers**

---

## ✅ Checklist Before PCB Fabrication

### Design Rules Check (DRC)
```
1. Inspect → Design Rules Checker
2. Run DRC
3. Fix all errors (warnings optional)
4. Check:
   - No unconnected nets
   - Trace widths ≥ 0.2mm (8mil)
   - Clearances ≥ 0.2mm
   - Via sizes appropriate
```

### Electrical Rules Check (ERC)
```
1. In schematic: Inspect → Electrical Rules Checker
2. Run ERC
3. Fix all errors:
   - All pins connected
   - Power flags set
   - No floating nets
```

### 3D Visualization
```
1. View → 3D Viewer
2. Check:
   - All components have 3D models
   - No collisions
   - Board stackup looks correct
   - Connectors accessible from enclosure
```

### Generate Manufacturing Files
```
1. File → Fabrication Outputs → Gerbers
2. Include:
   - All copper layers
   - Silkscreen (F.Silks, B.Silks)
   - Soldermask (F.Mask, B.Mask)
   - Paste (F.Paste, B.Paste if SMD)
   - Edge.Cuts
3. File → Fabrication Outputs → Drill Files
4. Zip all files for manufacturer
```

---

## 🏭 Recommended PCB Manufacturers

### For Prototyping (1-10 boards):
- **JLCPCB** - Cheapest, fast (1 week), good quality
- **OSH Park** - USA-based, purple boards, 2 weeks
- **PCBWay** - Good quality, more expensive

### For Small Production (10-100 boards):
- **JLCPCB** - Assembly service available
- **PCBWay** - Assembly + enclosure services
- **Seeed Studio** - Fusion PCB service

**Upload:** Gerber ZIP file + drill files

---

## 🔍 Troubleshooting

### Eagle Import Issues
**Problem:** Eagle import fails or looks wrong
**Solution:**
- Try importing .brd file instead of .sch
- Extract footprints only from PCB layout
- Manually recreate schematic symbols if needed

### Missing Footprints
**Problem:** Can't find footprint for component
**Solution:**
1. Search KiCad standard libraries first
2. Check Adafruit Eagle library
3. Create custom footprint using Footprint Editor
4. Import from SnapEDA or Ultra Librarian

### 3D Models Not Showing
**Problem:** 3D models don't load
**Solution:**
1. Check ADAFRUIT_3D path variable is set correctly
2. Verify 3D model file exists
3. Check file permissions
4. Try absolute path instead of variable

### Pin Assignment Confusion
**Problem:** Not sure which M4 pin to use
**Solution:**
- Reference: `docs/hardware/PIN_ALLOCATION_MATRIX.md`
- Or: `reference_schematics/M4_PIN_ASSIGNMENTS.svg`
- Your BOM CSV has "Notes" column with pin info

---

## 📚 Additional Resources

### KiCad Documentation
- Official docs: https://docs.kicad.org/
- Getting started: https://docs.kicad.org/8.0/en/getting_started_in_kicad/
- PCB design: https://docs.kicad.org/8.0/en/pcbnew/

### Your Project Docs
- **Hardware truth:** `docs/ACTUAL_HARDWARE_TRUTH.md`
- **EasyEDA guide:** `docs/EASYEDA_PCB_DESIGN_GUIDE.md` (mostly applies to KiCad too)
- **Schematics:** `docs/SCHEMATICS_READY_FOR_PCB.md`

### Component Datasheets
(To be added to `datasheets/` folder)
- MCP4728 DAC
- 6N138 Optocoupler
- 2N3904 Transistor
- BAT85 Schottky Diode

---

## 🎉 Next Steps

1. **Wait for Adafruit 3D repo to finish cloning** (background process)
2. **Create new KiCad project** as shown above
3. **Import USB-C and MCP4728** Eagle files first (urgent)
4. **Create hierarchical schematics** (TOP_BOARD + BOTTOM_BOARD)
5. **Reference your SVG schematics** while building circuits
6. **Assign footprints** from COMPLETE_BOM.csv
7. **Add 3D models** for visualization
8. **Design PCB layout**
9. **Run DRC/ERC checks**
10. **Generate Gerbers and order boards!**

---

**Ready to build your PCBs!** 🚀

Let me know when the Adafruit 3D repo finishes cloning and I'll help you create the index file.
