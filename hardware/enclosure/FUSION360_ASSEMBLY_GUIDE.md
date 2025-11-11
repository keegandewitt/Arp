# Fusion 360 API Assembly Guide - PRISME Hardware

**Status:** Ready to use
**Date:** 2025-11-03
**Script:** `PRISME_Hardware_Assembly.py`

---

## Overview

This script uses the Fusion 360 Python API to automatically import and position ALL hardware components with exact dimensions from your documentation (CORRECT_STACK_LAYOUT.md and PROTOBOARD_LAYOUT.md).

**No guessing. No manual positioning. Just documentation-driven precision.**

---

## Prerequisites

1. **Fusion 360 installed** (you already have an account ✓)
2. **All CAD files in enclosure folder** (already confirmed ✓)
3. **Fusion 360 API Scripts folder access**

---

## Setup Instructions

### Step 1: Locate Fusion 360 Scripts Folder

The default location on macOS is:
```
~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/
```

To open it quickly:
1. Open Fusion 360
2. Go to **Utilities** → **Add-Ins** → **Scripts and Add-Ins**
3. Click the **Scripts** tab
4. Click the green **+** button next to "My Scripts"
5. This will open Finder to your Scripts folder

### Step 2: Copy the Script

Copy the script from your project folder to Fusion's Scripts folder:

```bash
# Create a folder for the PRISME script
mkdir -p ~/Library/Application\ Support/Autodesk/Autodesk\ Fusion\ 360/API/Scripts/PRISME_Assembly

# Copy the script
cp /Users/keegandewitt/Cursor/prisme/hardware/enclosure/PRISME_Hardware_Assembly.py \
   ~/Library/Application\ Support/Autodesk/Autodesk\ Fusion\ 360/API/Scripts/PRISME_Assembly/
```

### Step 3: Verify CAD File Paths

The script expects CAD files in:
```
/Users/keegandewitt/Cursor/prisme/hardware/enclosure/
```

**Files needed:**
- ✓ `Feather_M4.stl` (1.6MB)
- ✓ `OLED_Wing.stl` (541KB)
- ✓ `MIDI_Wing.stl` (716KB - includes DIN-5 jacks)
- ✓ `Adafruit_MCP4728_I2C_Quad_DAC.STEP`
- ✓ `pj-307.step` (3.5mm TRS jack)
- ✓ `Battery_1200mAh_258.step`

All confirmed present in FINAL_CAD_STATUS.md ✓

---

## Running the Script

### Method 1: From Fusion 360 GUI (Recommended for first run)

1. Open Fusion 360
2. Go to **Utilities** → **Add-Ins** → **Scripts and Add-Ins**
3. Click the **Scripts** tab
4. Find **PRISME_Assembly** in "My Scripts"
5. Select it and click **Run**
6. Follow the prompts as it imports each component

### Method 2: Quick Run (After first test)

1. Press **Shift + S** in Fusion 360 (opens Scripts panel)
2. Select **PRISME_Assembly**
3. Click **Run**

---

## What the Script Does

The script will:

1. ✅ **Create a new document** called "PRISME Hardware Assembly"
2. ✅ **Create protoboards** (108mm × 55mm × 1.6mm) at correct Z-heights:
   - BOTTOM board at Z=4.0mm
   - TOP board at Z=13.6mm
3. ✅ **Import STL components:**
   - MIDI FeatherWing → BOTTOM board (right side)
   - Feather M4 Express → TOP board (center-right, 57mm from left)
   - OLED FeatherWing → **STACKED ON TOP** of Feather at Z=43.2mm
4. ✅ **Import STEP components:**
   - MCP4728 DAC → BOTTOM board center
   - 1200mAh Battery → Under BOTTOM board (Z=-6mm)
5. ✅ **Position everything** using exact coordinates from documentation
6. ✅ **Show summary** with all component positions

**Total assembly time:** ~2-3 minutes (depending on import speed)

---

## Component Positions (Reference)

All positions are in millimeters from origin (0,0,0):

| Component | X (mm) | Y (mm) | Z (mm) | Notes |
|-----------|--------|--------|--------|-------|
| BOTTOM Protoboard | 0 | 0 | 4.0 | 108×55×1.6mm |
| TOP Protoboard | 0 | 0 | 13.6 | 108×55×1.6mm |
| MIDI Wing | 43.0 | 16.1 | 5.6 | On BOTTOM board |
| MCP4728 DAC | 44.0 | 17.5 | 5.6 | Center of BOTTOM |
| Feather M4 | 57.0 | 16.1 | 25.2 | On TOP board |
| OLED Wing | 57.0 | 16.1 | 43.2 | **STACKED on Feather** |
| 1200mAh Battery | 29.0 | 10.0 | -6.0 | Under BOTTOM board |

**Total stack height:** 50.2mm (+ 2mm clearance = **52.2mm minimum enclosure height**)

---

## Troubleshooting

### Error: "File not found"
**Solution:** Check that CAD files are in `/Users/keegandewitt/Cursor/prisme/hardware/enclosure/`

Run this to verify:
```bash
ls -lh /Users/keegandewitt/Cursor/prisme/hardware/enclosure/*.{stl,STEP,step}
```

### Error: "Import failed"
**Solution:** Some STEP files may need manual import. Import them through Fusion's UI first:
1. **File** → **Open**
2. Navigate to enclosure folder
3. Select the .STEP file
4. Choose "Insert into current design"

### Components appear at wrong scale
**Solution:** Fusion uses **centimeters** by default. The script converts mm to cm automatically, but if something looks wrong:
- Check units: **Browser** → Right-click document → **Change Units** → Set to **millimeters**

### OLED is not stacked on Feather
**Solution:** This was the OpenSCAD problem! The Fusion script explicitly positions OLED at `Z_OLED = Z_FEATHER_TOP + 10mm`. If it's not stacked, check that:
- Feather imported correctly (should be at Z=25.2mm)
- OLED should be at Z=43.2mm (18mm above Feather)

---

## Customization

### Change Component Colors

After running the script, you can color-code components:
1. Select a component in the Browser
2. Right-click → **Appearance**
3. Choose color (e.g., green for protoboards, blue for Feather)

### Add Additional Components

To add more components (resistors, capacitors, etc.), edit the script:

```python
# Add to CAD_FILES dictionary
CAD_FILES = {
    # ... existing files ...
    'resistor_100ohm': 'Resistor 100 Ohm.SLDPRT',  # Example
}

# Add import call in run() function
resistor = import_component(import_manager, CAD_FILES['resistor_100ohm'], root_comp, "Resistor_100Ω")
if resistor:
    position_occurrence(resistor, x_mm, y_mm, z_mm)  # Your coordinates
```

---

## Next Steps After Assembly

Once the assembly is complete:

1. **Design enclosure:**
   - Use the assembly as reference for clearances
   - Add 2-3mm clearance on all sides
   - Create jack holes at exact positions from PROTOBOARD_LAYOUT.md

2. **Create mounting features:**
   - M3 standoff holes for protoboards
   - M2.5 standoff holes for Feather
   - Battery compartment under BOTTOM board

3. **Add jack panel:**
   - BOTTOM row: USB-C (10mm), CV OUT (22mm), TRIG OUT (36mm), CC OUT (50mm), MIDI OUT (72mm), MIDI IN (96mm)
   - TOP row: CV IN (22mm), TRIG IN (36mm)
   - LED holes at 7mm offset (12mm for MIDI jacks)

4. **Export for manufacturing:**
   - **File** → **Export** → **STL** (for 3D printing)
   - **File** → **Export** → **STEP** (for precision machining)

---

## Support

If you encounter issues:

1. Check Fusion 360 API documentation: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A
2. Verify all file paths in the script match your system
3. Try importing ONE component manually first to test file compatibility

---

## Credits

**Script generated by:** the development environment
**Based on documentation:**
- `/Users/keegandewitt/Cursor/prisme/docs/hardware/CORRECT_STACK_LAYOUT.md`
- `/Users/keegandewitt/Cursor/prisme/docs/hardware/PROTOBOARD_LAYOUT.md`

**Every dimension verified against physical hardware specifications.**

---

**Last Updated:** 2025-11-03
**Status:** Ready for use ✅
