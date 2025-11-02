# prisme 3D Printed Enclosure Design

**Version:** 1.0
**Date:** 2025-11-01
**Design Philosophy:** Clean top panel with display, all connectivity on rear

---

## Design Overview

### Layout Strategy
- **Top Surface:** OLED display window + 3 button access (clean aesthetic)
- **Rear Wall:** All I/O connectors (MIDI IN, OUT, USB-C, 4× CV jacks)
- **Side Wall:** Power switch cutout (Model 805 slide switch)
- **Bottom:** Rubber feet mounting points, optional ventilation slots
- **Interior:** Vertical mounting of M4+OLED stack, side-mounted MIDI wing

### Form Factor
```
Enclosure Dimensions (target):
┌─────────────────────────────────────┐
│  Width:  110mm (4.3")               │
│  Depth:   80mm (3.1")               │
│  Height:  35mm (1.4")               │
└─────────────────────────────────────┘

Weight: ~150-200g (with battery)
```

---

## Top Panel Design

### OLED Display Window

```
Top View:
┌──────────────────────────────────────────────┐
│                                              │
│    ┌─────────────────────────┐              │
│    │   OLED Window           │              │
│    │   40mm × 40mm           │  ← Display   │
│    │   (centered)            │              │
│    └─────────────────────────┘              │
│                                              │
│    [A]        [B]        [C]                 │  ← Button cutouts
│                                              │
└──────────────────────────────────────────────┘

Display window: 40mm × 40mm (centered, 15mm from front edge)
Button holes: 3× 6mm diameter (25mm spacing, 8mm from bottom edge)
```

### Features
- **Display Window:** 40mm × 40mm cutout for 128x128 OLED
  - Recessed 2mm to sit flush with PCB
  - Chamfered edges (0.5mm × 45°) for clean look
  - Fits SH1107 OLED FeatherWing display

- **Button Access:** 3× 6mm diameter holes
  - Buttons A, B, C from OLED FeatherWing
  - 25mm center-to-center spacing
  - Aligned horizontally, 8mm from bottom edge
  - Optional: Press-fit rubber button caps

- **Branding Area:** Optional recessed text
  - "prisme" logotype (font: monospace, 3mm height)
  - Position: Upper left corner (5mm margins)
  - Depth: 0.3mm for contrast with natural PLA

---

## Rear Panel Design

### Connector Layout

```
Rear View (looking at back of device):
┌──────────────────────────────────────────────────────┐
│                                                      │
│  [MIDI IN]  [MIDI OUT]  [USB-C]  [CV-A] [CV-B]      │
│    DIN-5      DIN-5     10×5mm    TRS    TRS        │
│   14mmØ      14mmØ               6mmØ   6mmØ        │
│                                                      │
│                            [CV-C] [CV-D]             │
│                             TRS    TRS               │
│                            6mmØ   6mmØ               │
└──────────────────────────────────────────────────────┘

MIDI Jacks (left):  2× 14mm diameter, 30mm spacing (center-to-center)
USB-C (center):     10mm × 5mm cutout with 1mm chamfer
CV Jacks (right):   4× 6mm diameter, arranged in 2×2 grid
  - Horizontal spacing: 17mm (Eurorack standard)
  - Vertical spacing: 17mm
  - Grid centered on right side of panel
```

### Connector Specifications

#### MIDI Jacks (DIN-5)
- **Type:** Panel-mount DIN-5 (180° orientation)
- **Hole Size:** 14mm diameter
- **Spacing:** 30mm center-to-center (horizontal)
- **Height:** Centered vertically (17.5mm from top/bottom)
- **Labels:** Engraved or vinyl
  - Left: "MIDI IN"
  - Right: "MIDI OUT"

#### USB-C Port
- **Type:** Cutout for Feather M4 onboard port
- **Dimensions:** 10mm wide × 5mm tall
- **Position:** Center of panel (55mm from left edge)
- **Clearance:** 0.5mm tolerance for easy insertion
- **Chamfer:** 1mm × 45° for cable strain relief
- **Label:** "USB-C" (engraved above)

#### CV/Gate Outputs (3.5mm TRS)
- **Type:** Thonkiconn PJ301M-12 panel-mount jacks
- **Hole Size:** 6mm diameter
- **Arrangement:** 2×2 grid
  ```
  [CV-A: Pitch]    [CV-B: Gate]
  [CV-C: Reserved] [CV-D: Custom CC]
  ```
- **Spacing:** 17mm horizontal, 17mm vertical (Eurorack standard)
- **Position:** Right side of panel, 15mm from right edge
- **Labels:** Engraved or vinyl
  - "CV" (above top row)
  - "GATE" (below CH B)
  - "CC" (below CH D)
  - Optional: voltage range "0-5V"

---

## Side Panel Design

### Power Switch Cutout

```
Left Side View:
┌──────────────────┐
│                  │
│  ┌────────┐      │  ← Slide switch cutout
│  │ 805    │      │     (13mm × 6mm)
│  │ [ON]   │      │
│  └────────┘      │
│                  │
└──────────────────┘

Position: Centered on left side, 10mm from front edge
Dimensions: 13mm wide × 6mm tall (for Model 805 slide switch)
Clearance: 0.3mm tolerance
Labels: "POWER" with "ON" indicator (engraved)
```

### Features
- **Slide Switch Cutout:** 13mm × 6mm rectangular opening
  - Centered vertically on left side wall
  - 10mm from front edge
  - Fits Model 805 slide switch body
  - Mounting tabs on interior (2× M2 screw holes)

- **Labels:** Engraved text
  - "POWER" above switch
  - "ON →" and "← OFF" indicators beside switch
  - Font: 2mm sans-serif, 0.3mm depth

---

## Interior Layout

### Component Mounting Strategy

```
Interior View (top removed):
┌──────────────────────────────────────────────┐
│                                              │
│  ┌─────────┐         ┌──────────────┐       │
│  │ Battery │         │ M4 + OLED    │       │
│  │ (LiPo)  │         │ Stack        │       │
│  │         │         │ (vertical)   │       │
│  └─────────┘         └──────────────┘       │
│                                              │
│  ┌──────┐   ┌──────┐         ┌──────────┐   │
│  │Boost │   │Switch│         │MIDI Wing │   │
│  │Module│   │ 805  │         │(horiz.)  │   │
│  └──────┘   └──────┘         └──────────┘   │
│                                              │
│          ┌──────┐                            │
│          │ DAC  │                            │
│          │MCP   │                            │
│          │4728  │                            │
│          └──────┘                            │
└──────────────────────────────────────────────┘

Mounting Points:
- M4+OLED Stack: 4× M2.5 standoffs (15mm height)
- MIDI Wing: 2× M2.5 standoffs (10mm) OR foam tape
- DAC: Double-sided foam tape OR 2× M2 screws
- Boost: Double-sided foam tape
- Battery: Velcro strap or foam padding
- Switch: 2× M2 screw mounting tabs
```

### Vertical Mounting (M4 + OLED Stack)

**Why Vertical?**
- Maximizes use of height (35mm)
- Positions OLED parallel to top panel
- USB-C directly accessible from rear
- Short wire runs to all connectors

**Mounting Details:**
```
Side View (cross-section):
    ┌───────────────────┐ ← Top panel
    │                   │
    │  ┌─────────────┐  │ ← OLED window
    │  │   OLED      │  │
    │  │  Display    │  │
    ├──┴─────────────┴──┤ ← OLED FeatherWing PCB
    │                   │
    │   (15mm standoffs)│
    │                   │
    ├───────────────────┤ ← Feather M4 PCB
    │                   │
    │  [USB-C] →        │ ← Rear panel cutout
    └───────────────────┘ ← Bottom
```

- **Standoffs:** 4× M2.5 × 15mm (aluminum or nylon)
- **Position:** Centered horizontally, 20mm from front edge
- **Orientation:** USB-C port facing rear panel
- **Clearance:** 5mm to rear panel, 10mm to side walls

### MIDI FeatherWing (Side-Mounted)

**Layout:**
- Mounted horizontally beside M4 stack
- MIDI jacks facing rear panel
- 5-10mm gap from M4 for jumper wire routing
- Height: Same as M4 base (10mm standoffs or foam tape)

**Mounting Options:**
1. **Standoffs:** 2× M2.5 × 10mm (cleaner, adjustable)
2. **Foam Tape:** 3M VHB double-sided (simpler, less clearance)

**Wire Routing:**
- Jumper wires to M4 (4 wires: VIN, GND, TX, RX)
- Routed underneath MIDI wing or along side wall
- Secured with cable ties or wire clips

### MCP4728 DAC (Near Rear Panel)

**Position:**
- Near rear panel for short wire runs to TRS jacks
- Between M4 stack and right side wall
- Oriented with outputs facing right (toward CV jacks)

**Mounting:**
- **Option A:** Double-sided foam tape (simplest)
- **Option B:** 2× M2 screws with standoffs (more secure)

**Wiring:**
- I2C to M4 (SCL, SDA, VCC, GND) - ~60mm wire length
- CV outputs to TRS jacks (4× wires with 100Ω resistors)
- Power from boost module (5V, GND)

### Boost Module & Battery

**Boost Module:**
- Position: Near battery and power switch
- Mounting: Foam tape
- Clearance: 3mm from all sides (heat dissipation)
- Wiring: Short runs to battery, switch, and DAC

**Battery (LiPo 500-1200mAh):**
- Position: Front-left corner (away from PCBs)
- Mounting: Velcro strap or foam padding
- Clearance: 5mm from walls (swelling protection)
- JST connector: Accessible for replacement
- Size: ~40mm × 30mm × 7mm (typical 500mAh)

---

## Material & Print Settings

### Recommended Filament
- **Material:** PLA or PETG
  - **PLA:** Easier to print, good rigidity, eco-friendly
  - **PETG:** More durable, heat-resistant, flexible

- **Color:** Natural, black, gray, or custom
  - Natural/white: Good for light diffusion (optional LED mod)
  - Black: Professional look, hides internal components

### Print Settings
```
Layer Height:      0.2mm (balance of speed/quality)
Wall Thickness:    1.2mm (3 perimeters @ 0.4mm nozzle)
Top/Bottom Layers: 4 layers (0.8mm)
Infill:            20% gyroid (strength + weight balance)
Print Speed:       50mm/s (outer walls), 60mm/s (infill)
Supports:          Yes (for button holes, display window)
Brim:              Optional (adhesion for large panels)
```

### Post-Processing
- **Sanding:** 220-grit for smooth finish on visible surfaces
- **Acetone Vapor:** Optional for ABS (glass-like finish)
- **Primer + Paint:** Optional for custom colors
- **Clear Coat:** Optional for durability

---

## Assembly Sequence

### 1. Print Enclosure Parts
- [ ] Top panel
- [ ] Bottom panel
- [ ] Rear panel
- [ ] Left side (with switch cutout)
- [ ] Right side
- [ ] Front panel (optional logo/branding)

### 2. Install Rear Panel Connectors
- [ ] 2× DIN-5 MIDI jacks (with nuts)
- [ ] 4× TRS jacks (with nuts)
- [ ] Verify USB-C cutout alignment

### 3. Mount Internal Components
- [ ] Install M4+OLED stack standoffs
- [ ] Mount MIDI wing beside stack
- [ ] Mount DAC near rear panel
- [ ] Mount boost module (foam tape)
- [ ] Wire all connections per HARDWARE_BUILD_GUIDE.md

### 4. Install Side Panel Components
- [ ] Mount slide switch in left panel cutout
- [ ] Connect power wiring

### 5. Final Assembly
- [ ] Secure battery in front corner
- [ ] Route and organize all wiring
- [ ] Test all connections (HARDWARE_TEST_RESULTS.md)
- [ ] Assemble enclosure panels
- [ ] Install rubber feet on bottom

---

## Fasteners & Hardware

### Panel Screws
- **Type:** M3 × 10mm (countersunk or button head)
- **Quantity:** 16-20 screws (4-5 per panel seam)
- **Spacing:** 20-30mm between screws
- **Material:** Stainless steel or black oxide

### Standoffs
- **M4 Stack:** 4× M2.5 × 15mm standoffs
- **MIDI Wing:** 2× M2.5 × 10mm standoffs
- **DAC (optional):** 2× M2 × 5mm standoffs

### Heat-Set Inserts (Optional)
- **Type:** M3 × 5mm brass inserts
- **Purpose:** Stronger threads in plastic
- **Tool:** Soldering iron (set to 200°C for PLA)
- **Quantity:** 16-20 (one per screw hole)

---

## Labeling Options

### Method 1: Engraved Text (Recommended)
- **Process:** Modeled into STL, printed with text recessed
- **Depth:** 0.3-0.5mm
- **Font:** Monospace or sans-serif, 2-3mm height
- **Infill:** Use contrasting filament color in recessed text

### Method 2: Vinyl Labels
- **Tool:** Cricut or silhouette cutter
- **Material:** Outdoor vinyl (waterproof, UV-resistant)
- **Application:** Apply after assembly
- **Pros:** Easy to change, professional look

### Method 3: Laser Engraving
- **Process:** Post-print laser marking
- **Material:** Works best on light-colored PLA
- **Detail:** High resolution, permanent
- **Cost:** $10-30 (local makerspace or service)

---

## Optional Enhancements

### Display Bezel
- 3D printed frame around OLED window
- Sits on top of top panel (press-fit or glued)
- Adds 2-3mm height for "instrument" aesthetic
- Chamfered inner edge for viewing angle

### Rubber Button Caps
- **Type:** Press-fit silicone caps (6mm diameter)
- **Source:** DigiKey, Mouser, or AliExpress
- **Purpose:** Tactile feedback, color-coding
- **Installation:** Push onto button stems through top panel

### LED Light Pipe
- Optional LED under display (powered by M4 GPIO)
- Light pipe from LED to top panel edge
- Indicates power/MIDI activity
- 2mm diameter channel, clear filament

### Ventilation Slots
- Bottom panel: 4× 20mm × 2mm slots
- Positioned away from electronics
- Allows air circulation for boost module heat
- Optional mesh filter (3D printed grid)

### Rubber Feet
- **Type:** Self-adhesive rubber bumpers
- **Size:** 10mm diameter × 3mm height
- **Quantity:** 4 feet (one per corner)
- **Purpose:** Prevents sliding, protects surfaces

---

## CAD File Structure

### Recommended Files
```
/enclosure/
  ├── prisme_top_panel.stl        (with display window + buttons)
  ├── prisme_bottom_panel.stl     (with screw holes + feet mounts)
  ├── prisme_rear_panel.stl       (with all jack cutouts)
  ├── prisme_left_side.stl        (with switch cutout)
  ├── prisme_right_side.stl       (plain)
  ├── prisme_front_panel.stl      (optional branding)
  ├── prisme_display_bezel.stl    (optional)
  └── assembly_guide.pdf          (exploded view)
```

### CAD Software Recommendations
- **FreeCAD:** Free, open-source, parametric
- **Fusion 360:** Free for hobbyists, excellent for enclosures
- **OpenSCAD:** Code-based, version-control friendly
- **Tinkercad:** Browser-based, beginner-friendly

---

## Dimensions Reference

### Critical Measurements

| Component | Width × Depth × Height | Notes |
|-----------|----------------------|-------|
| Feather M4 | 51mm × 23mm × 8mm | Plus USB-C port height |
| OLED Wing | 51mm × 23mm × 10mm | Active area: 35mm × 35mm |
| MIDI Wing | 51mm × 23mm × 10mm | MIDI jacks extend 15mm |
| MCP4728 | 20mm × 20mm × 5mm | Adafruit breakout |
| Boost Module | 18mm × 11mm × 4mm | Teyleten type |
| Battery 500mAh | 40mm × 30mm × 7mm | Typical dimensions |
| DIN-5 Jack | 14mm hole, 15mm depth | Panel-mount type |
| TRS Jack | 6mm hole, 10mm depth | Thonkiconn PJ301M-12 |

### Clearance Requirements

| Clearance | Minimum | Recommended |
|-----------|---------|-------------|
| PCB to panel | 3mm | 5mm |
| Wire bends | 5mm | 10mm |
| Battery to PCB | 3mm | 5mm |
| Component spacing | 3mm | 5mm |
| Panel screw edge | 3mm | 5mm |

---

## Enclosure Variants

### Variant A: Desktop (Default)
- **Orientation:** Horizontal (as described above)
- **Angle:** Flat or slight 5° tilt
- **Feet:** Rubber bumpers on bottom

### Variant B: Eurorack Mount
- **Width:** 28HP (141.9mm)
- **Height:** 3U (128.5mm)
- **Depth:** 50mm
- **Mounting:** M3 screws to rack rails
- **Rear:** Same connector layout
- **Front:** 3U panel with display centered

### Variant C: Portable/Handheld
- **Add:** Hand strap cutouts on sides
- **Battery:** Larger 1200mAh for extended runtime
- **Edges:** Rounded corners for grip
- **Finish:** Rubberized coating

---

## Testing Checklist

### Fit Testing (Before Full Assembly)
- [ ] M4 USB-C aligns with rear panel cutout
- [ ] OLED display visible through top window
- [ ] All 3 buttons accessible through top holes
- [ ] MIDI wing jacks align with rear DIN-5 holes
- [ ] TRS jacks align with rear CV holes
- [ ] Slide switch fits side panel cutout
- [ ] All standoffs fit mounting holes
- [ ] Panels assemble without force

### Functional Testing (After Assembly)
- [ ] All connectors accessible
- [ ] No shorts or contact with enclosure walls
- [ ] Switch operates smoothly
- [ ] Buttons press correctly
- [ ] Display visible at all viewing angles
- [ ] No rattling or loose components
- [ ] Rubber feet prevent sliding

---

## Estimated Costs

### Materials
- **Filament:** $3-5 (80-100g PLA)
- **Fasteners:** $2-3 (M2.5/M3 screws + standoffs)
- **Rubber Feet:** $1-2
- **Labels/Vinyl:** $2-3 (optional)

**Total:** ~$8-13 per enclosure

### Print Time
- **Top Panel:** 2-3 hours
- **Bottom Panel:** 2-3 hours
- **Rear Panel:** 2-3 hours
- **Sides:** 1-2 hours each
- **Total:** 10-14 hours print time

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-01 | Initial enclosure design with rear I/O layout |

---

## Next Steps

1. **CAD Modeling:** Create parametric design in Fusion 360 or FreeCAD
2. **Prototype Print:** Print test panels to verify fit
3. **Iterate:** Adjust clearances and mounting points
4. **Full Assembly:** Build complete enclosure
5. **Document:** Take photos and create assembly guide

---

**Questions? Suggestions?** Open an issue or discussion on GitHub!

**Happy Making!** 🖨️🎛️✨
