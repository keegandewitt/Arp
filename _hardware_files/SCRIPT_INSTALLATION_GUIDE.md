# Fusion 360 Auto-Generate Script - Installation Guide
## Automatically Build Your Enclosure in 60 Seconds

**Script:** `generate_enclosure.py`
**Version:** 1.0
**Compatibility:** Fusion 360 (all recent versions)

---

## What This Script Does

The Python script automatically creates:
- ✅ Bottom shell with mounting standoffs, posts, and battery compartment
- ✅ Front panel with MIDI jack holes (2× 14mm) and CV/Gate holes (2× 6mm)
- ✅ Rear panel with USB-C cutout (10mm × 5mm)
- ✅ Left side panel with slide switch cutout (12mm × 6mm)
- ✅ Right side panel (solid)
- ✅ Top panel with OLED window (30mm × 15mm) and button holes (3× 4mm)

**Total generation time:** 30-60 seconds

---

## Installation Steps

### Step 1: Locate the Script

The script is located at:
```
_hardware_files/generate_enclosure.py
```

Keep this file accessible - you'll need to browse to it from Fusion 360.

### Step 2: Open Fusion 360

1. Launch **Fusion 360**
2. Sign in to your account
3. Wait for the home screen to load

### Step 3: Access Scripts & Add-Ins

**Two ways to access:**

**Method A: Via Tools Menu**
1. Click **Tools** (top menu bar)
2. Click **Add-Ins**
3. Click **Scripts and Add-Ins**

**Method B: Via Keyboard Shortcut**
1. Press **Shift + S** (opens Scripts and Add-Ins dialog)

### Step 4: Add the Script

In the "Scripts and Add-Ins" dialog:

1. Click the **"Scripts"** tab (if not already selected)
2. Click the green **"+"** button (Add Script)
3. Browse to `_hardware_files/generate_enclosure.py`
4. Select the file
5. Click **"Open"**

The script should now appear in the list under "My Scripts"

### Step 5: Run the Script

1. Find **"generate_enclosure"** in the script list
2. Click on it to select it
3. Click the **"Run"** button

**You'll see a message:**
> "Starting enclosure generation... This will take 30-60 seconds."

4. Click **OK**
5. Wait while the script runs (you'll see Fusion 360 working)

### Step 6: Script Completes

When finished, you'll see:
> "Enclosure generation complete!
>
> Next steps:
> 1. Review the design
> 2. Export each component as STL
> 3. Slice and print"

6. Click **OK**

---

## What You'll See

After the script runs, your Fusion 360 Browser panel will show:

```
Untitled (your new design)
├─ Bottom_Shell
│  └─ Body, Sketches, Features
├─ Front_Panel
│  └─ Body, Sketches, Features
├─ Rear_Panel
│  └─ Body, Sketches, Features
├─ Left_Side_Panel
│  └─ Body, Sketches, Features
├─ Right_Side_Panel
│  └─ Body, Sketches, Features
└─ Top_Panel
   └─ Body, Sketches, Features
```

Each component is a separate, editable part!

---

## Verify the Design

### Check Component Visibility

**Toggle components on/off:**
1. In Browser panel, click the eye icon next to each component
2. This hides/shows parts to inspect individually

### Inspect Features

**Bottom Shell should have:**
- Hollow box (2.5mm walls)
- 4 PCB standoffs with screw holes
- 2 module mounting posts (boost + DAC)
- Battery compartment with strap slot
- 4 corner posts with screw holes

**Front Panel should have:**
- 2 large holes (14mm - MIDI jacks)
- 2 small holes (6mm - CV/Gate jacks)

**Rear Panel should have:**
- 1 rectangular cutout (USB-C port)

**Left Side Panel should have:**
- 1 rectangular cutout (slide switch)

**Right Side Panel:**
- Solid (no cutouts)

**Top Panel should have:**
- 1 rectangular window (OLED display)
- 3 circular holes (buttons A, B, C)

---

## Export STL Files for Printing

### Export Each Component Separately

**For each component (repeat 6 times):**

1. **Right-click** on component name (e.g., "Bottom_Shell")
2. Select **"Save As STL"**
3. **Configure STL settings:**
   - Refinement: **High** or **Medium**
   - Format: **Binary** (smaller file size)
   - Unit: **Millimeters**
4. **Save as:**
   - Bottom_Shell → `ARP_Bottom_Shell.stl`
   - Front_Panel → `ARP_Front_Panel.stl`
   - Rear_Panel → `ARP_Rear_Panel.stl`
   - Left_Side_Panel → `ARP_Left_Side.stl`
   - Right_Side_Panel → `ARP_Right_Side.stl`
   - Top_Panel → `ARP_Top_Panel.stl`

### Quick Export Tip

**Export all at once (alternative method):**
1. Go to **File → 3D Print**
2. Select each body individually
3. Export to STL
4. Repeat for all 6 parts

---

## Import into Bambu Studio

### Step 1: Open Bambu Studio

1. Launch **Bambu Studio**
2. Create new project or open existing

### Step 2: Import STL Files

1. Click **"Add"** or drag files into build plate
2. Select all 6 STL files:
   - `ARP_Bottom_Shell.stl`
   - `ARP_Front_Panel.stl`
   - `ARP_Rear_Panel.stl`
   - `ARP_Left_Side.stl`
   - `ARP_Right_Side.stl`
   - `ARP_Top_Panel.stl`

### Step 3: Orient Parts for Printing

**Bottom Shell:**
- Rotate **upside down** (opening facing build plate)
- This minimizes support material
- Add **tree supports** for standoffs

**All Panels:**
- Orient **flat** on largest face
- No rotation needed (should auto-orient correctly)
- Minimal or no supports required

### Step 4: Configure Print Settings

**Recommended settings for Bambu A1 Mini:**

| Setting | Value |
|---------|-------|
| **Material** | PLA or PETG |
| **Layer Height** | 0.2mm (standard) |
| **Infill** | 15-20% |
| **Wall Loops** | 3-4 |
| **Support Type** | Tree supports (for bottom shell only) |
| **Build Plate Adhesion** | Brim (5mm) recommended |

### Step 5: Slice and Print

1. Click **"Slice"**
2. Review estimated time (should be 5-7 hours total)
3. Check filament usage (~100-150g)
4. Send to printer or save to SD card

---

## Print Order Recommendation

**Phase 1: Test Fit (print first):**
1. Bottom Shell (~2-3 hours)

**After bottom shell completes:**
- Test fit with actual PCB stack
- Verify standoff height and spacing
- Check component clearances

**Phase 2: Complete Enclosure (if fit is good):**
2. Front Panel (~45 min)
3. Rear Panel (~30 min)
4. Left Side Panel (~30 min)
5. Right Side Panel (~30 min)
6. Top Panel (~45 min)

**Total print time:** 5-7 hours

---

## Troubleshooting

### Problem: Script won't run / error message

**Possible causes:**
- Fusion 360 version incompatibility
- Script file path incorrect
- Python API changes

**Solutions:**
1. Update Fusion 360 to latest version
2. Verify script file path is correct
3. Check script appears in "My Scripts" list
4. Try restarting Fusion 360

### Problem: Components don't appear after running

**Check:**
1. Look in Browser panel (left side)
2. Expand component tree
3. Click eye icons to show/hide
4. Use **View → Fit** to zoom to model

### Problem: STL export fails

**Solutions:**
1. Select component first (right-click in Browser)
2. Ensure component has a valid body
3. Try **File → Export** instead of "Save As STL"
4. Export as STEP first, then convert to STL

### Problem: Parts don't fit when printed

**Likely causes:**
1. Printer calibration needed
2. Dimensional accuracy off
3. Shrinkage/warping during print

**Solutions:**
1. Print calibration cube (20mm test)
2. Adjust X/Y compensation in slicer
3. Increase clearances in script (edit dimensions at top)
4. Reprint affected parts

---

## Modifying the Design

### Edit Dimensions Before Running Script

**Open the script in a text editor:**

At the top of `generate_enclosure.py`, you'll find:

```python
# Enclosure dimensions (all in cm for Fusion 360 API)
ENCLOSURE_WIDTH = 14.0  # 140mm
ENCLOSURE_DEPTH = 10.0  # 100mm
ENCLOSURE_HEIGHT = 6.0  # 60mm
WALL_THICKNESS = 0.25   # 2.5mm
```

**Change these values to resize the enclosure!**

**Example: Make it 20mm wider:**
```python
ENCLOSURE_WIDTH = 16.0  # 160mm (was 14.0)
```

Save the script and re-run it in Fusion 360.

### Edit Components After Generation

**All components are fully editable:**

1. Double-click any component in Browser
2. Expand **Features** to see sketches and extrudes
3. Right-click features to **Edit** or **Delete**
4. Add new sketches and features as needed

**Common edits:**
- Add more mounting holes
- Adjust cutout sizes
- Add text labels (embossed or engraved)
- Add ventilation slots
- Modify standoff heights

---

## Save Your Design

**Don't forget to save!**

1. **File → Save**
2. Name: `ARP_Enclosure_v1`
3. Save to Fusion 360 cloud or local drive
4. Create versions as you iterate

---

## Next Steps

After generating and exporting:

1. ✅ **Print parts** (5-7 hours)
2. ✅ **Remove supports** and clean up prints
3. ✅ **Test fit components** (see HARDWARE_BUILD_GUIDE.md)
4. ✅ **Assemble enclosure** with M3 screws
5. ✅ **Install electronics** following build guide

---

## Script Customization Tips

### Adding Text Labels

**To add engraved text to panels:**

1. After script runs, activate the component you want to label
2. **Create → Create Sketch** on the face
3. **Sketch → Text**
4. Enter text, position, and size
5. **Create → Extrude** (cut direction, -0.5mm depth)

### Adding More Holes

**Example: Add extra CV jack:**

1. Edit Front Panel component
2. Find the `create_cv_holes` sketch
3. Right-click → **Edit Sketch**
4. Add another circle (6mm diameter)
5. Finish sketch (hole will cut automatically)

### Changing Colors (Visual Only)

**Make components different colors in Fusion:**

1. Right-click component → **Appearance**
2. Select material/color from library
3. This is visual only (doesn't affect STL)

---

## Resources

**Fusion 360 API Documentation:**
- https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A

**Bambu Studio Guides:**
- https://wiki.bambulab.com/en/software/bambu-studio

**3D Printing Tips:**
- Layer adhesion: Increase bed temp by 5°C if parts warp
- Support removal: Use needle-nose pliers, work slowly
- Hole sizing: If too tight, drill out with correct size bit

---

## Estimated Project Timeline

| Task | Duration |
|------|----------|
| Install and run script | 5 minutes |
| Review and export STLs | 10 minutes |
| Slice in Bambu Studio | 10 minutes |
| Print all parts | 5-7 hours (unattended) |
| Post-processing | 30 minutes |
| Assembly | 2-3 hours |
| **Total active time** | **1 hour** |
| **Total elapsed time** | **8-11 hours** |

---

## Support

**If you encounter issues:**

1. Check this troubleshooting guide
2. Verify Fusion 360 version is up to date
3. Try the manual build guide (FUSION360_BUILD_GUIDE.md) instead
4. Review script code for dimension adjustments

**Script version:** 1.0
**Last updated:** 2025-10-15

---

**Ready to build? Run the script and start printing!** 🚀
