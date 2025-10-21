# Fusion 360 Enclosure Build Guide
## MIDI Arpeggiator Desktop Enclosure - Complete CAD Instructions

**Version:** 1.0
**Date:** 2025-10-15
**Estimated Build Time:** 45-60 minutes
**Skill Level:** Intermediate Fusion 360 user

---

## Table of Contents

1. [Setup & Preparation](#setup--preparation)
2. [Part 1: Bottom Shell](#part-1-bottom-shell)
3. [Part 2: Front Panel](#part-2-front-panel)
4. [Part 3: Rear Panel](#part-3-rear-panel)
5. [Part 4: Side Panels](#part-4-side-panels)
6. [Part 5: Top Panel](#part-5-top-panel)
7. [Part 6: Internal Features](#part-6-internal-features)
8. [Part 7: Assembly & Verification](#part-7-assembly--verification)
9. [Part 8: Export for 3D Printing](#part-8-export-for-3d-printing)

---

## Design Overview

**Enclosure Type:** Horizontal Desktop Box
**Overall External Dimensions:** 140mm (W) × 100mm (D) × 60mm (H)
**Wall Thickness:** 2.5mm
**Material:** PLA or PETG
**Printer:** Bambu Labs A1 Mini (no AMS)

**Component Layout:**
```
                    TOP VIEW
    ┌─────────────────────────────────────┐
    │         [OLED Display]              │
    │          [A] [B] [C]                │
    └─────────────────────────────────────┘

                   FRONT VIEW
    ┌─────────────────────────────────────┐
    │  [MIDI IN] [MIDI OUT] [CV] [GATE]  │ ← Front Panel
    │                                     │
    │        [Internal Stack]             │
    │                                     │
    └─────────────────────────────────────┘
         ↑                        ↑
    Slide Switch              USB-C Port
    (Left Side)              (Rear Panel)
```

---

## Setup & Preparation

### Before You Start

1. **Open Fusion 360**
2. **Create New Design:** File → New Design
3. **Save As:** `ARP_Enclosure_v1.f3d`
4. **Set Units:** Modify → Change Active Units → Millimeters (mm)

### Import Existing Component Files

**Import all existing CAD models for reference:**

1. **File → Open** each component in separate tabs:
   - `4759 Feather M4 CAN Express.f3d`
   - `4650 OLED FeatherWing.f3d`
   - `4740 MIDI FeatherWing.f3d`
   - `805 slide switch.f3d`

2. **In your main design (`ARP_Enclosure_v1`):**
   - Right-click on root component → Insert into Current Design
   - Insert each component file
   - These will serve as visual references for clearances

### Create Component Structure

**In the Browser panel, create folders:**
- Right-click root → New Component: `Bottom Shell`
- New Component: `Front Panel`
- New Component: `Rear Panel`
- New Component: `Side Panels`
- New Component: `Top Panel`
- New Component: `Reference Components` (move imported files here)

---

## Part 1: Bottom Shell

The bottom shell is the main structural component with integrated standoffs and mounting features.

### Step 1.1: Create Base Rectangle

1. **Activate Bottom Shell component** (double-click in browser)
2. **Create → Create Sketch**
3. **Select XY Plane** (origin plane)
4. **Sketch → Rectangle → Center Rectangle**
   - Click origin point
   - Width: **140mm**
   - Depth: **100mm**
   - Press Enter

### Step 1.2: Extrude Base

1. **Finish Sketch** (click checkmark or press Esc)
2. **Create → Extrude**
   - Select the rectangle profile
   - Distance: **60mm** (full height)
   - Direction: Symmetric (uncheck)
   - Operation: New Body
   - Click OK

### Step 1.3: Shell the Enclosure

1. **Modify → Shell**
   - Select **top face** of the box (this will be removed)
   - Inside Thickness: **2.5mm**
   - Click OK

**Result:** Hollow box with 2.5mm walls, open top

### Step 1.4: Create Internal Floor for Mounting

1. **Create → Create Sketch**
2. **Select bottom internal face**
3. **Sketch → Rectangle → Center Rectangle**
   - Centered on origin
   - Width: **135mm** (5mm smaller than outer)
   - Depth: **95mm** (5mm smaller than outer)
4. **Finish Sketch**
5. **Create → Extrude**
   - Distance: **2mm** (internal floor thickness)
   - Direction: Upward
   - Operation: Join

### Step 1.5: Add PCB Stack Mounting Standoffs

**Create standoffs for M4 Feather mounting holes (4 corners):**

**Reference dimensions from Feather spec:**
- Feather mounting holes: 4 holes, 2.5mm diameter
- Hole spacing: 45.72mm × 17.78mm (1.8" × 0.7")

**Position of stack in enclosure:**
- Center horizontally
- 25mm from front panel (allows room for wiring)
- 15mm from bottom (on internal floor)

**Create standoff positions:**

1. **Create → Create Sketch** on internal floor (2mm raised surface)
2. **Sketch → Circle**
   - Center 1: X = -22.86mm, Y = 15mm (front-left)
   - Diameter: **5mm** (standoff outer diameter)
3. **Repeat for 4 corners:**
   - Front-left: (-22.86, 15)
   - Front-right: (22.86, 15)
   - Rear-left: (-22.86, -2.78)
   - Rear-right: (22.86, -2.78)

4. **Finish Sketch**
5. **Create → Extrude**
   - Select all 4 circles
   - Distance: **6mm** (standoff height for stack clearance)
   - Operation: Join

### Step 1.6: Add Screw Holes to Standoffs

1. **Create → Create Sketch** on top face of standoffs
2. **Sketch → Circle** (centered on each standoff)
   - Diameter: **2.7mm** (clearance for M2.5 screw)
3. **Finish Sketch**
4. **Create → Extrude**
   - Select all 4 circles
   - Distance: **-6mm** (cut through standoffs)
   - Operation: Cut

### Step 1.7: Add Mounting Posts for Boost Module & DAC

**Boost Module position:** Left side of stack, 10mm spacing
**DAC position:** Right side of stack, 10mm spacing

**Create 2 mounting posts (foam tape mounts, no screw holes needed):**

1. **Create → Create Sketch** on internal floor
2. **Sketch → Rectangle**
   - Boost module post:
     - Position: X = -45mm, Y = 15mm
     - Size: 25mm × 15mm
   - DAC post:
     - Position: X = 45mm, Y = 15mm
     - Size: 30mm × 20mm
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **3mm** (low profile for foam tape mounting)
   - Operation: Join

### Step 1.8: Add Battery Compartment

**Battery position:** Rear of enclosure
**Battery dimensions:** 50mm × 34mm × 6mm (from spec)

1. **Create → Create Sketch** on internal floor
2. **Sketch → Rectangle**
   - Center: X = 0mm, Y = -35mm (rear section)
   - Size: 55mm × 38mm (2mm clearance around battery)
3. **Sketch → Rectangle** (inner, for Velcro strap slot)
   - Center: X = 0mm, Y = -35mm
   - Size: 50mm × 10mm (strap slot)
4. **Finish Sketch**
5. **Create → Extrude** outer rectangle
   - Distance: **8mm** (battery height + clearance)
   - Operation: Join (creates raised walls)
6. **Create → Extrude** inner rectangle
   - Distance: **-2mm** (cut slot for strap)
   - Operation: Cut

### Step 1.9: Add Corner Screw Posts for Assembly

**4 corner posts to join panels:**

1. **Create → Create Sketch** on internal bottom surface
2. **Sketch → Circle**
   - Position 4 circles in corners (5mm from edges):
     - Front-left: (-65, 45)
     - Front-right: (65, 45)
     - Rear-left: (-65, -45)
     - Rear-right: (65, -45)
   - Diameter: **6mm**
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **55mm** (almost to top, leaving 3mm for panel)
   - Operation: Join
5. **Create screw holes:**
   - Sketch on top of posts
   - Circle diameter: **3.2mm** (M3 clearance)
   - Extrude cut through posts

### Step 1.10: Add Ventilation Slots (Optional)

**Small slots in bottom for airflow:**

1. **Create → Create Sketch** on external bottom face
2. **Sketch → Slot** (centerline slot tool)
   - Create 3 slots: 40mm × 3mm
   - Spacing: 20mm apart
   - Centered on bottom
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **2.5mm** (through bottom wall)
   - Operation: Cut

---

## Part 2: Front Panel

Front panel mounts MIDI DIN-5 jacks and CV/Gate TRS jacks.

### Step 2.1: Create Front Panel Base

1. **Activate Front Panel component**
2. **Create → Create Sketch**
3. **Select YZ Plane** (front-facing)
4. **Sketch → Rectangle**
   - Center on origin
   - Width: **140mm**
   - Height: **60mm**
5. **Finish Sketch**
6. **Create → Extrude**
   - Distance: **2.5mm** (wall thickness)
   - Operation: New Body

### Step 2.2: Add MIDI Jack Holes (DIN-5)

**Layout:**
- 2 MIDI jacks, spaced 30mm apart
- Positioned left side of panel
- Center height: 30mm from bottom

**Hole diameter:** 14mm (DIN-5 standard)

1. **Create → Create Sketch** on front face of panel
2. **Sketch → Circle**
   - MIDI IN: X = -40mm, Y = 30mm, Diameter = **14mm**
   - MIDI OUT: X = -10mm, Y = 30mm, Diameter = **14mm**
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-2.5mm** (cut through panel)
   - Operation: Cut

### Step 2.3: Add CV/Gate TRS Jack Holes (3.5mm)

**Layout:**
- 2 TRS jacks, spaced 15mm apart
- Positioned right side of panel
- Center height: 30mm from bottom

**Hole diameter:** 6mm (3.5mm TRS standard)

1. **Create → Create Sketch** on front face
2. **Sketch → Circle**
   - CV (Pitch): X = 25mm, Y = 30mm, Diameter = **6mm**
   - GATE: X = 42mm, Y = 30mm, Diameter = **6mm**
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-2.5mm** (cut through)
   - Operation: Cut

### Step 2.4: Add Labels (Engraved)

**Optional: Add text labels below each jack:**

1. **Create → Create Sketch** on front face
2. **Sketch → Text**
   - Font: Arial, Bold
   - Height: **3mm**
   - Text positioning:
     - Below MIDI IN hole: "MIDI IN"
     - Below MIDI OUT hole: "MIDI OUT"
     - Below CV hole: "CV"
     - Below GATE hole: "GATE"
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-0.5mm** (shallow engraving)
   - Operation: Cut

### Step 2.5: Add Mounting Tabs

**Create tabs to attach panel to bottom shell:**

1. **Create → Create Sketch** on inside face of panel
2. **Sketch → Rectangle**
   - 4 tabs at corners (matching corner posts in bottom shell)
   - Size: 8mm × 8mm each
   - Position: 5mm from edges
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **5mm** (inward)
   - Operation: Join
5. **Add screw holes:**
   - Sketch circles (3.2mm diameter) centered on tabs
   - Extrude cut through tabs

---

## Part 3: Rear Panel

Rear panel has USB-C cutout only.

### Step 3.1: Create Rear Panel Base

1. **Activate Rear Panel component**
2. **Create → Create Sketch**
3. **Select YZ Plane** (rear-facing)
4. **Sketch → Rectangle**
   - Width: **140mm**
   - Height: **60mm**
5. **Finish Sketch**
6. **Create → Extrude**
   - Distance: **2.5mm**
   - Operation: New Body

### Step 3.2: Add USB-C Port Cutout

**USB-C position:** Centered horizontally, 15mm from bottom (aligned with M4 Feather USB port)

**Cutout dimensions:** 10mm × 5mm (with cable clearance)

1. **Create → Create Sketch** on rear face
2. **Sketch → Center Rectangle**
   - Center: X = 0mm, Y = 15mm
   - Width: **10mm**
   - Height: **5mm**
3. **Sketch → Fillet** corners
   - Radius: **1mm** (rounded corners for cable strain relief)
4. **Finish Sketch**
5. **Create → Extrude**
   - Distance: **-2.5mm** (cut through)
   - Operation: Cut

### Step 3.3: Add Label

1. **Create → Create Sketch** on rear face
2. **Sketch → Text**
   - Text: "USB-C"
   - Height: **3mm**
   - Position: Below cutout
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-0.5mm**
   - Operation: Cut

### Step 3.4: Add Mounting Tabs

**Same as front panel:**

1. Create 4 corner tabs (8mm × 8mm)
2. Extrude 5mm inward
3. Add 3.2mm screw holes

---

## Part 4: Side Panels

Left side has slide switch cutout, right side is solid.

### Step 4.1: Create Left Side Panel

1. **Activate Side Panels component**
2. **Create → Create Sketch**
3. **Select XZ Plane**
4. **Sketch → Rectangle**
   - Width: **100mm** (depth)
   - Height: **60mm**
5. **Finish Sketch**
6. **Create → Extrude**
   - Distance: **2.5mm**
   - Operation: New Body

### Step 4.2: Add Slide Switch Cutout

**Position:** Center of panel (X = 0mm, Y = 30mm)

**Critical:** Reference `805 slide switch.f3d` for exact cutout dimensions

**Approximate cutout (verify with switch model):**
- Width: **12mm**
- Height: **6mm**
- Depth: **10mm** (recessed mounting)

1. **Create → Create Sketch** on exterior side face
2. **Sketch → Rectangle**
   - Center: Midpoint of panel
   - Size: **12mm × 6mm**
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-10mm** (cut for switch body + mount)
   - Operation: Cut

**Add mounting screw holes (if switch has mounting tabs):**
1. Sketch 2 circles (2.5mm diameter) on either side of cutout
2. Extrude cut for screw access

### Step 4.3: Add Labels

1. **Sketch → Text** on exterior face
   - Above cutout: "POWER"
   - Tick marks for "ON" / "OFF" positions
2. **Extrude** -0.5mm (engraved)

### Step 4.4: Create Right Side Panel (Mirror)

1. **Create → Mirror**
   - Mirror Feature: Left side panel body
   - Mirror Plane: YZ plane
   - Create New Component: Yes (creates right panel without cutout)

### Step 4.5: Add Mounting Tabs to Both Panels

**Each side panel needs 4 mounting tabs:**

1. **Create → Create Sketch** on inside faces
2. Create 4 tabs (top/bottom, front/rear corners)
3. Extrude inward 5mm
4. Add 3.2mm screw holes

---

## Part 5: Top Panel

Top panel has OLED window and button access holes.

### Step 5.1: Create Top Panel Base

1. **Activate Top Panel component**
2. **Create → Create Sketch**
3. **Select XY Plane** (offset +57.5mm from origin - top surface)
4. **Sketch → Rectangle**
   - Width: **140mm**
   - Depth: **100mm**
5. **Finish Sketch**
6. **Create → Extrude**
   - Distance: **2.5mm** (upward)
   - Operation: New Body

### Step 5.2: Add OLED Display Window

**Display position:** Center-front of panel
**Display active area:** 25mm × 10mm (128×32 OLED)
**Window size (with margin):** 30mm × 15mm

1. **Create → Create Sketch** on top face
2. **Sketch → Center Rectangle**
   - Center: X = 0mm, Y = 20mm (forward from center)
   - Width: **30mm**
   - Height: **15mm**
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-2.5mm** (cut through)
   - Operation: Cut

### Step 5.3: Add Button Access Holes

**OLED FeatherWing buttons (A, B, C):**
- Position: Below OLED display
- Spacing: 12mm apart
- Diameter: 4mm (clearance for button caps)

1. **Create → Create Sketch** on top face
2. **Sketch → Circle**
   - Button A: X = -12mm, Y = 5mm, Diameter = **4mm**
   - Button B: X = 0mm, Y = 5mm, Diameter = **4mm**
   - Button C: X = 12mm, Y = 5mm, Diameter = **4mm**
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-2.5mm** (cut through)
   - Operation: Cut

### Step 5.4: Add Button Labels

1. **Create → Create Sketch** on top face
2. **Sketch → Text**
   - Below each button: "A", "B", "C"
   - Height: **2mm**
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-0.5mm**
   - Operation: Cut

### Step 5.5: Add Mounting Tabs

**Top panel attaches to corner posts:**

1. Create 4 corner tabs (8mm × 8mm)
2. Position to align with corner screw posts in bottom shell
3. Add 3.2mm clearance holes for M3 screws

### Step 5.6: Add Recessed Lip for Alignment

**Create lip to seat into bottom shell opening:**

1. **Create → Create Sketch** on underside of panel
2. **Sketch → Offset** the outer rectangle
   - Offset: **-1mm** inward
3. **Finish Sketch**
4. **Create → Extrude**
   - Distance: **-2mm** (downward lip)
   - Operation: Join

---

## Part 6: Internal Features

### Step 6.1: Add Wire Routing Channels

**Create channels in bottom shell for cable management:**

1. **Activate Bottom Shell component**
2. **Create → Create Sketch** on internal floor
3. **Sketch → Spline or Polyline**
   - Trace paths from:
     - Stack → Front panel jacks
     - Stack → Rear USB cutout
     - Battery → Slide switch → Stack
     - Boost module → DAC
4. **Finish Sketch**
5. **Create → Extrude**
   - Width: **3mm**
   - Depth: **1mm** (shallow channel)
   - Operation: Cut

### Step 6.2: Add Cable Tie Anchor Points

1. **Create → Create Sketch** on internal surfaces
2. **Sketch → Small rectangles** (5mm × 2mm)
   - Position: Near wire routing paths
3. **Finish Sketch**
4. **Create → Extrude**
   - Height: **3mm** (small posts)
   - Operation: Join
5. **Add slot:**
   - Sketch slot (1mm × 3mm) through post
   - Extrude cut for zip tie

### Step 6.3: Add Strain Relief for Jacks

**Create recessed pockets on inside of front panel for jack nuts:**

1. **Activate Front Panel component**
2. **Create → Create Sketch** on inside face
3. **Sketch → Concentric circles** around each jack hole
   - Outer diameter: 16mm (MIDI), 8mm (TRS)
   - Depth: 2mm
4. **Extrude cut** to recess jack mounting nuts

---

## Part 7: Assembly & Verification

### Step 7.1: Create Assembly Relationships

1. **Assemble → Joint**
   - Join front panel tabs to bottom shell corner posts
   - Repeat for rear panel, side panels, top panel

2. **Verify fit:**
   - All panels should align flush
   - Screw holes should align
   - No interference

### Step 7.2: Import Reference Components

**Insert imported models to verify clearances:**

1. **Insert → Insert into Current Design**
   - Import Feather stack models
   - Position on standoffs
2. **Check clearances:**
   - USB-C port aligns with rear cutout
   - OLED display visible through top window
   - Buttons accessible through holes
   - MIDI/CV jacks reach front panel

### Step 7.3: Measure Internal Space

1. **Inspect → Measure**
   - Verify all internal dimensions
   - Check clearances (minimum 2mm everywhere)
   - Confirm stack height fits

---

## Part 8: Export for 3D Printing

### Step 8.1: Prepare Parts for Printing

**Each part needs to be a separate STL file:**

1. **Right-click Bottom Shell** → Create Mesh (STL)
   - Refinement: High
   - Save as: `ARP_Bottom_Shell.stl`

2. **Repeat for all parts:**
   - `ARP_Front_Panel.stl`
   - `ARP_Rear_Panel.stl`
   - `ARP_Left_Side.stl`
   - `ARP_Right_Side.stl`
   - `ARP_Top_Panel.stl`

### Step 8.2: Optimize for Bambu A1 Mini

**Print settings recommendations:**

**Bottom Shell:**
- Orientation: Upside down (opening facing build plate)
- Support: Yes (for standoffs and posts)
- Infill: 20%
- Layer height: 0.2mm
- Estimated time: 2-3 hours

**Panels:**
- Orientation: Flat on largest face
- Support: Minimal (only for deep recesses)
- Infill: 15%
- Estimated time: 30-45 min each

**Total print time:** ~5-7 hours

### Step 8.3: Create Assembly Instructions

**Generate assembly drawing:**

1. **File → New Drawing**
2. **Create exploded view** of assembly
3. **Add dimensions and callouts**
4. **Export as PDF:** `ARP_Assembly_Instructions.pdf`

---

## Verification Checklist

Before printing, verify:

- [ ] Bottom shell has all mounting features (standoffs, posts, battery compartment)
- [ ] Front panel holes: 2× 14mm (MIDI), 2× 6mm (CV/Gate)
- [ ] Rear panel cutout: 10mm × 5mm (USB-C)
- [ ] Left side cutout: Slide switch (verify with .f3d model)
- [ ] Top panel: 30mm × 15mm OLED window, 3× 4mm button holes
- [ ] All panels have mounting tabs with 3.2mm screw holes
- [ ] Corner posts in bottom shell have M3 screw holes
- [ ] Wall thickness: 2.5mm throughout
- [ ] Clearances: Minimum 2mm around all components
- [ ] No interference between parts in assembly
- [ ] All labels and text readable (minimum 2mm height)

---

## Post-Print Notes

**After printing:**

1. **Remove supports** carefully
2. **Test fit components** before full assembly
3. **Deburr holes** with 3mm drill bit (MIDI) or 6mm (CV)
4. **Test screw fit** (M3 screws should thread into posts)
5. **Dry fit panels** together
6. **Insert electronics** and verify:
   - Stack fits on standoffs
   - USB-C accessible
   - OLED visible
   - Buttons pressable
   - Jacks mount flush

**If adjustments needed:**
- Return to Fusion 360
- Modify dimensions
- Re-export affected parts
- Reprint

---

## Troubleshooting

**Problem: Parts don't fit together**
- Check printer calibration (print test cube)
- Adjust tolerances in Fusion (add 0.2mm clearance)
- Verify no warping during print (use brim or raft)

**Problem: Screw holes too tight/loose**
- M3 clearance hole: 3.2mm (reprint if needed)
- Can enlarge holes with 3.5mm drill bit
- Or use M2.5 screws if holes too small

**Problem: Standoffs too short**
- Measure actual stack height with spacers
- Modify standoff height in Fusion
- Re-export and print bottom shell only

---

## Design Parameters (for easy modifications)

**To resize enclosure:**
1. Edit base rectangles in Step 1.1, 2.1, 3.1, 4.1, 5.1
2. Adjust component positions proportionally
3. Verify clearances in assembly

**To add features:**
- Additional jacks: Add holes in Step 2.2/2.3
- More mounting posts: Add in Step 1.7
- Cooling vents: Add in Step 1.10

---

## Next Steps

1. **Follow this guide in Fusion 360** (60 minutes)
2. **Verify assembly** with imported component models
3. **Export STL files** for all 6 parts
4. **Slice in Bambu Studio** with recommended settings
5. **Print and test fit** before final assembly
6. **Iterate if needed** (likely 1-2 test prints)

---

**Estimated Total Project Time:**
- CAD modeling: 60 minutes (following this guide)
- Printing: 6-8 hours (mostly unattended)
- Post-processing: 30 minutes
- Assembly: 2-3 hours (see HARDWARE_BUILD_GUIDE.md)

**Total:** 1-2 days from CAD to finished enclosure

---

## Questions or Issues?

If you encounter problems:
1. Check verification checklist above
2. Verify component dimensions against datasheets
3. Test fit before committing to full assembly
4. Share screenshots if you need help troubleshooting

Good luck with your build!
