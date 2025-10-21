# Enclosure Roadmap

## Project Overview
Custom enclosure for MIDI Arpeggiator based on Adafruit M4 Express with FeatherWings stack.

## Design Decisions (All Confirmed ✅)
- ✓ **Form Factor:** Horizontal Desktop Box (desktop-only, no portability features)
- ✓ **Manufacturing:** 3D Printing with Fusion 360 on Bambu Labs A1 Mini (no AMS-lite)
- ✓ **Finish:** Raw 3D print (no painting or post-processing)
- ✓ **Power & Charging:** USB-C on M4 Feather CAN (charging + programming)
- ✓ **5V Boost:** Teyleten Multi-Function Boost Module (3.7V→5V @ 1.5A, ~$0.70 each)
- ✓ **Power Switch:** Slide switch Model 805 - acts as power distribution/splitter point
- ✓ **CV Output:** Adafruit MCP4728 Quad DAC (4 channels, 0-5V, 12-bit, I2C)
- ✓ **CV Labeling:** Generic "CV 1-4" (reprogrammable for any function)
- ✓ **External Controls:** None - using only OLED Wing's 3 buttons
- ✓ **No Second MIDI FeatherWing:** Using external DAC instead

## Hardware Components to Accommodate

### Electronics Stack
- **Adafruit Feather M4 CAN Express** (base board, main controller with built-in USB-C LiPo charging)
- **OLED FeatherWing** (128x32 display with buttons A, B, C)
- **MIDI FeatherWing** (DIN-5 MIDI jacks for note data IN/OUT)
- **Teyleten Multi-Function Boost Module** (3.7V→5V @ 1.5A, adjustable voltage)
- **MCP4728 Quad DAC Breakout** (I2C, 4-channel 12-bit DAC, 0-5V output)
- **LiPo Battery** (500-1200mAh, ~50x34x6mm typical)
- **Slide Switch Model 805** (power distribution point)

### Connectors & External Access
- **USB-C Port** (M4 Express) - **Direct access for charging + programming**
- **Slide Switch Model 805** (power distribution) - **Side panel, controls all power**
- **MIDI Connections (Standard MIDI FeatherWing):**
  - 1x MIDI IN Jack (5-pin DIN) - Note data input from keyboard
  - 1x MIDI OUT Jack (5-pin DIN) - Arpeggiated output to synthesizer
- **CV Outputs (MCP4728 Quad DAC):**
  - 4x 1/8" TRS jacks (0-5V, 1V/octave compatible)
  - Panel-mount 3.5mm mono jacks required
  - Perfect for vintage synths (Moog, ARP, Roland, etc.)

### Physical Dimensions Reference

**FeatherWing Stack:**
- **M4 Feather CAN Express:** 50.8mm x 22.86mm x ~8mm (2" x 0.9" x 0.3" with headers)
- **MIDI FeatherWing:** 50.8mm x 22.86mm x ~8mm
- **OLED FeatherWing:** 50.8mm x 22.86mm x ~15mm (with display and buttons)
- **Stack Height (total):** ~30-40mm (depending on header/spacer configuration)
- **OLED Display Area:** 128x32 pixels (~25mm x 10mm viewing area)

**Additional Modules:**
- **Teyleten Boost Module:** 22mm x 11mm x 3.6mm (0.87" x 0.43" x 0.14")
- **Adafruit MCP4728 DAC:** 25.7mm x 17.8mm x 4.6mm (1.0" x 0.7" x 0.2")
- **Combined footprint:** Can mount side-by-side in ~50mm x 20mm area

**Panel Components:**
- **DIN-5 MIDI Jack:** 14mm diameter mounting hole (x2 for MIDI IN/OUT)
- **1/8" TRS Jack (3.5mm):** 6mm diameter mounting hole (x4 for CV outputs 1-4)
- **USB-C Port (M4):** 9mm x 4mm cutout (with clearance)
- **Slide Switch Model 805:** See `_hardware_files/805 slide switch.f3d` for exact dimensions

**Battery:**
- **LiPo (500-1200mAh):** Approximately 50mm x 34mm x 6mm (varies by capacity)

**Enclosure Planning:**
- **Minimum internal space:** ~120mm x 80mm x 50mm (estimate)
- **Module placement:** Teyleten Boost + MCP4728 mount beside stack on foam tape or standoffs

---

## Phase 1: Design Requirements & Planning

### 1.1 Form Factor Decision ✓ CONFIRMED
**Selected:** Horizontal Desktop Box
- Top panel: OLED display window with button access
- Front panel: MIDI jacks (panel-mount DIN-5 connectors)
- Rear panel: USB-C port cutout (direct access to M4 Express port)
- Side panel: Slide switch cutout for battery disconnect
- Pros: Stable, traditional MIDI device look, easy to access all controls
- Note: Position M4 Express with USB-C facing rear panel for easy cable access

### 1.2 Material Selection ✓ CONFIRMED
**Selected:** 3D Printed (PLA or PETG recommended)
- Design in Fusion 360
- Export STL files for slicing
- Material recommendations:
  - **PLA:** Easiest to print, rigid, good for prototypes
  - **PETG:** More durable, slightly flexible, better layer adhesion
  - **ABS:** Strong but requires heated enclosure, prone to warping

- [ ] Consider finishing options:
  - Sanding surfaces (120→220→400 grit) for smooth finish
  - Apply filler primer to hide layer lines
  - Paint with spray paint (matte black, vintage beige, or custom color)
  - Clear coat for protection and professional look

### 1.3 Access & Serviceability
- [ ] **Top Access:**
  - Removable top panel for display viewing
  - Clear acrylic window over OLED
  - Button access (cutouts or extended buttons)

- [ ] **Bottom Access:**
  - Removable bottom plate for battery replacement
  - Screws accessible (4x M3 or M4)
  - Rubber feet mounting points

- [ ] **Internal Access:**
  - Snap-fit or screwed assembly
  - Allow firmware updates via USB without full disassembly
  - SD card access (if applicable)

---

## Phase 2: Mechanical Design

### 2.1 CAD Modeling
- [ ] Import existing Fusion 360 models into new assembly:
  - `_hardware_files/4759 Feather M4 CAN Express.f3d`
  - `_hardware_files/4650 OLED FeatherWing.f3d`
  - `_hardware_files/4740 MIDI FeatherWing.f3d` (x1 only)
  - `_hardware_files/805 slide switch.f3d`
  - Find/create models for Teyleten Boost Module and MCP4728 breakout

- [ ] Create enclosure assembly:
  - Stack FeatherWings in proper order (bottom to top):
    1. M4 Express (base) - **USB-C port facing rear for charging/programming**
    2. MIDI FeatherWing (DIN-5 MIDI note data IN/OUT)
    3. OLED FeatherWing (display on top)
  - Position Teyleten Boost Module alongside stack
  - Position MCP4728 DAC breakout near front panel (short wiring to TRS jacks)
  - Position battery in remaining space (not underneath stack)
  - Define mounting strategy (M2.5 or M3 standoffs for stack, double-sided tape or standoffs for Boost/DAC)
  - **Plan wire routing (Slide Switch as Power Distribution Hub):**
    - Battery + (red) → Slide Switch IN terminal
    - Slide Switch OUT terminal → splits to TWO destinations:
      - Wire 1: M4 Feather BAT pin (for charging via USB-C)
      - Wire 2: Teyleten Boost Module VIN (3.7V input)
    - Battery - (black) → Common GND (M4 + Boost Module + MCP4728)
    - Teyleten Boost 5V OUT → MCP4728 VCC (powers DAC)
    - M4 SCL/SDA → MCP4728 I2C (control)
    - MCP4728 outputs (A, B, C, D) → Front panel TRS jacks (CV)

- [ ] Design enclosure components:
  - **Bottom shell:** Main electronics cavity with integrated standoffs for stack, mounting posts for Boost and DAC
  - **Top panel:** Display window cutout + button access holes
  - **Front panel:** 2x DIN-5 MIDI jack mounting holes (IN + OUT) + 4x 1/8" TRS jack mounting holes (CV 1-4)
  - **Rear panel:** USB-C cutout (M4 charging + programming) - single port!
  - **Side panel:** Slide switch cutout and mounting features (acts as power distribution point)
  - Optional: Integrated corner posts for screw assembly
  - Ensure adequate space for internal wiring and component placement

### 2.2 Mounting & Support
- [ ] **PCB Stack Mounting:**
  - M2.5 or M3 standoffs (8-12mm height)
  - Align with Feather mounting holes
  - Ensure stack stability (3 boards stacked)

- [ ] **Teyleten Boost Module Mounting:**
  - Double-sided foam tape OR small standoffs
  - Mount alongside main stack
  - Position for easy wiring from slide switch to VIN
  - Ensure 5V output can reach MCP4728

- [ ] **MCP4728 DAC Mounting:**
  - Double-sided foam tape OR small standoffs
  - Position near front panel for short CV output wiring
  - Ensure I2C wires can reach M4 SCL/SDA pins
  - Connect 5V from Boost Module to DAC VCC

- [ ] **Battery Mounting:**
  - Velcro strap or mounting clips
  - Ensure JST connector reaches slide switch
  - Isolate from PCBs (foam padding or divider)

- [ ] **Slide Switch Wiring (Power Distribution Hub):**
  - Battery + wire → Switch IN terminal
  - Switch OUT terminal → solder TWO wires:
    - Wire 1 to M4 BAT pin
    - Wire 2 to Teyleten Boost VIN
  - Use heat shrink on solder joints for insulation
  - Route wires neatly to avoid strain

- [ ] **Cable Management:**
  - Internal routing channels for I2C, power, CV signals
  - Strain relief for external cables (MIDI, CV outputs)
  - Keep power and signal wires separated
  - Label internal connections for serviceability
  - Organize wire bundle from slide switch to M4 + Boost Module

### 2.3 Panel Cutouts & Features

#### Top Panel (Display & Controls)
- [ ] OLED display window:
  - Size: 30mm x 15mm (with margins)
  - Flush mount or recessed 1-2mm
  - Clear acrylic or open cutout

- [ ] Button access (3 buttons):
  - **Option A:** Extended button caps through panel holes
  - **Option B:** Cutouts for direct button access
  - **Option C:** External momentary switches wired to button pads

- [ ] Labeling:
  - Engraved or printed labels (A, B, C)
  - Pattern cycle indicators
  - Status LEDs (optional)

#### Front Panel (Connectors)
- [ ] **MIDI Jacks (2 total - MIDI FeatherWing):**
  - Standard panel-mount DIN-5 (14mm holes)
  - MIDI IN: Note data input from keyboard/controller
  - MIDI OUT: Arpeggiated output to synthesizer
  - Label: "MIDI IN", "MIDI OUT"
  - Spacing: 20-25mm center-to-center

- [ ] **CV Output Jacks (4 total - MCP4728 Quad DAC):**
  - Panel-mount 3.5mm mono jacks (6mm holes)
  - Connected to MCP4728 outputs A, B, C, D via internal wiring
  - 12-bit resolution, **0-5V output range** (1V/octave compatible!)
  - Perfect for: CV pitch, gates, modulation, vintage synth control
  - Label: "CV 1", "CV 2", "CV 3", "CV 4" (or "PITCH", "GATE", "MOD 1", "MOD 2")
  - Spacing: 12-15mm center-to-center (closer spacing for 4 jacks)
  - **Wiring:** Short jumper wires from MCP4728 breakout to TRS jack tips + grounds

**Front Panel Layout Suggestion:**
```
[MIDI IN] [MIDI OUT]         [CV 1] [CV 2] [CV 3] [CV 4]
  DIN-5     DIN-5               TRS    TRS    TRS    TRS
                               (0-5V) (0-5V) (0-5V) (0-5V)
```

#### Rear/Side Panel (Power & Programming)
- [ ] **USB-C Port (M4 Express - Rear Panel):**
  - Cutout for M4 Express USB-C port (direct access for charging AND programming)
  - Size: 9mm x 4mm (with clearance for connector + cable strain relief)
  - Position enclosure to align M4 USB-C with rear panel opening
  - No panel-mount connector needed - direct board access
  - Label: "USB-C" or "CHARGE/PROG"

- [ ] **Slide Switch (Side Panel):**
  - Cutout for Model 805 slide switch (power distribution hub)
  - Reference `_hardware_files/805 slide switch.f3d` for exact dimensions
  - Mount switch through side panel for easy access
  - Critical function: Controls power to BOTH M4 BAT pin AND Boost Module
  - Label: "POWER" with ON/OFF indicators
  - **Note:** This switch distributes battery power to two destinations

#### Bottom Panel
- [ ] **Ventilation (optional):**
  - Small vent holes or slots (M4 doesn't generate much heat)
  - Prevents dust accumulation

- [ ] **Rubber feet:**
  - 4x adhesive rubber feet (8-10mm diameter)
  - Recessed screw holes for mounting (optional)

- [ ] **Battery access:**
  - Removable panel section with 4 screws
  - Gasket or seal (optional)

### 2.4 Tolerances & Clearances
- [ ] Add clearances:
  - **PCB to shell:** 2-3mm minimum
  - **Connectors to panel:** 0.3-0.5mm (tight fit)
  - **Display to window:** 0.5-1mm
  - **Battery to PCB:** 3-5mm (allow for expansion)

- [ ] Account for:
  - 3D print tolerance: ±0.2mm
  - Screw hole clearance: +0.3mm
  - Heat expansion (if using battery)

---

## Phase 3: Prototyping & Testing

### 3.1 Proof of Concept
- [ ] Create simple cardboard mockup
  - Validate dimensions and button placement
  - Test ergonomics and viewing angle
  - Identify potential issues early

- [ ] 3D print prototype (if using 3D printing)
  - Print bottom shell first
  - Test PCB fit before printing full enclosure
  - Iterate on fitment issues

### 3.2 Assembly Test
- [ ] Test assembly process:
  - Can PCBs be inserted easily?
  - Do standoffs align correctly?
  - Are cables and battery accessible?

- [ ] Test button functionality:
  - Do buttons actuate smoothly?
  - Is button travel adequate (1-2mm)?
  - Can buttons be pressed without flex?

- [ ] Test connector alignment:
  - Do MIDI jacks align with panel holes?
  - Is USB port accessible with cable?
  - Check for strain on internal connections

### 3.3 Functional Testing
- [ ] Verify electrical functionality:
  - Does device power on correctly?
  - Do MIDI connections work?
  - Is display visible and clear?

- [ ] Test thermal performance:
  - Monitor temperature during extended use
  - Ensure battery doesn't overheat
  - Check for hotspots

- [ ] EMI/RFI testing (optional):
  - Check for interference with MIDI signals
  - Test near other audio equipment
  - Consider adding ferrite cores if needed

---

## Phase 4: Finishing & Production

### 4.1 Surface Finishing
- [x] **3D Print Finish:** Raw print, no post-processing
  - Bambu Labs A1 Mini produces good surface quality out of the box
  - Single color filament (PLA or PETG recommended)
  - Optional: Light deburring of sharp edges with hobby knife
  - No sanding, painting, or coating required

### 4.2 Labels & Branding
- [ ] Create labels for:
  - Device name/logo
  - Button functions (A/B/C, Pattern, Clock)
  - Connector labels:
    - Front panel: "MIDI IN", "MIDI OUT", "CV 1", "CV 2", "CV 3", "CV 4"
    - Rear panel: "USB-C" or "CHARGE/PROG" (single USB-C port!)
    - Side panel: "POWER" with ON/OFF indicators (slide switch)
  - Safety warnings (battery, LiPo charging)
  - Optional: CV voltage range label "0-5V" or "1V/OCT"

- [ ] Choose labeling method:
  - Laser engraved
  - Vinyl stickers
  - Screen printed
  - CNC engraved

### 4.3 Hardware & Fasteners
- [ ] Acquire fasteners:
  - M2.5 or M3 screws (various lengths: 6mm, 8mm, 12mm)
  - M2.5 or M3 standoffs (brass or nylon)
  - M3 or M4 screws for panel assembly (4-8 pieces)
  - Washers and lock washers (optional)

- [ ] Acquire accessories:
  - Rubber feet (4x)
  - Clear acrylic sheet (for window, if applicable)
  - Double-sided tape or adhesive (for battery mounting)

### 4.4 Assembly Jig (Optional)
- [ ] Create assembly jig for repeatable builds:
  - Alignment tool for PCB stack
  - Fastener guide
  - Cable routing template

---

## Phase 5: Documentation

### 5.1 Assembly Instructions
- [ ] Create step-by-step assembly guide:
  - Parts list and BOM
  - Exploded view diagram
  - Assembly order (bottom-up or top-down)
  - Torque specifications (if critical)

- [ ] Include photos:
  - Each assembly step
  - Connector orientation
  - Battery installation
  - Cable routing

### 5.2 Enclosure Files
- [ ] Prepare manufacturing files:
  - **For 3D printing:** Export STL files
  - **For laser cutting:** Export DXF/SVG files (with kerf compensation)
  - **For CNC:** Export STEP or IGES files

- [ ] Version control:
  - Save native CAD files (Fusion 360)
  - Export dated versions
  - Maintain changelog

### 5.3 Maintenance Guide
- [ ] Document maintenance procedures:
  - How to replace battery
  - How to clean display
  - How to access USB port for firmware updates
  - Troubleshooting connector issues

---

## Phase 6: Enhancements & Variants

### 6.1 Optional Features
- [ ] **LED Status Indicators:**
  - Power LED (green)
  - MIDI activity LEDs (red/yellow)
  - Clock sync indicator

- [ ] **External Power Jack:**
  - 5V DC barrel jack (2.1mm)
  - Alternative to USB power
  - Wiring to M4 Express VIN pin

- [ ] **Expansion Port:**
  - Breakout for unused GPIO pins
  - Future expansion (expression pedal, etc.)

- [ ] **Kickstand or Tilt Mechanism:**
  - Adjustable viewing angle (5-45°)
  - Foldable or detachable

### 6.2 Design Variants
- [ ] **Compact Version:**
  - Minimal enclosure, open sides
  - Display and MIDI jacks only

- [ ] **Rackmount Version:**
  - 1U or 2U rack ears
  - Front panel display
  - Rear panel MIDI connections

- [ ] **Portable Version:**
  - Carrying handle
  - Latched enclosure
  - Internal cable storage

### 6.3 Color & Aesthetic Options
- [ ] Design color schemes:
  - Classic black/silver
  - Retro beige/brown
  - Modern white/matte
  - Custom color matching

- [ ] Create variants for different materials:
  - Transparent acrylic version
  - Brushed metal version
  - Wood veneer version

---

## Bill of Materials (BOM) - Enclosure

### Structural Components
| Part | Qty | Notes |
|------|-----|-------|
| Bottom shell | 1 | 3D printed or laser-cut assembly |
| Top panel/shell | 1 | With display window and button access |
| Front panel | 1 | MIDI jack mounting |
| Rear panel | 1 | USB access |
| Side panels (optional) | 2 | Depends on design |

### Fasteners & Hardware
| Part | Qty | Notes |
|------|-----|-------|
| M2.5 or M3 standoffs (8-12mm) | 8-12 | For PCB stack mounting |
| M2.5 or M3 screws (6mm) | 8-12 | PCB mounting |
| M3 or M4 screws (10mm) | 4-8 | Panel assembly |
| Rubber feet | 4 | Adhesive or screw-mount |
| Washers | As needed | For secure fastening |

### Power & Control Components
| Part | Qty | Price | Notes |
|------|-----|-------|-------|
| **Teyleten Multi-Function Boost Module** | 1 | ~$0.70 | 3.7V→5V @ 1.5A ($7 for 10 pack on Amazon) |
| **MCP4728 Quad DAC Breakout** | 1 | ~$7 | I2C 12-bit 4-channel DAC (Adafruit or SparkFun) |
| Slide switch (Model 805) | 1 | Included | Power distribution hub - see `_hardware_files/805 slide switch.f3d` |
| 22AWG hookup wire | ~2 feet | ~$2 | For slide switch power distribution wiring |
| Heat shrink tubing | As needed | ~$2 | Insulate solder joints on slide switch |

### Connectors & Cables
| Part | Qty | Notes |
|------|-----|-------|
| Panel-mount MIDI jacks (DIN-5) | 2 | MIDI IN + MIDI OUT (MIDI FeatherWing) |
| Panel-mount 1/8" TRS jacks (3.5mm mono) | 4 | CV outputs 1-4 (connected to MCP4728) |
| Internal MIDI cables | As needed | Connect MIDI FeatherWing to panel-mount DIN-5 jacks |
| Jumper wires (male-to-male/female) | 10-15 | I2C, 5V power, CV output wiring |
| JST extension cable (optional) | 1 | If battery needs extra length to reach slide switch |

### Optional Components
| Part | Qty | Notes |
|------|-----|-------|
| Clear acrylic sheet (2mm) | 1 | Display window |
| LED bezels | 2-3 | For status LEDs |
| Velcro strap | 1 | Battery mounting |
| Foam padding | As needed | Vibration dampening, battery isolation |

### Finishing Materials
| Part | Qty | Notes |
|------|-----|-------|
| Primer (if painting) | 1 can | For 3D prints |
| Spray paint | 1-2 cans | Color of choice |
| Clear coat | 1 can | Protection |
| Vinyl labels | 1 sheet | Connector labels, branding |

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Planning | 1-2 days | None |
| Phase 2: CAD Design | 3-5 days | Phase 1 complete, CAD files imported |
| Phase 3: Prototyping | 1-2 weeks | Phase 2 complete, 3D printer/materials available |
| Phase 4: Finishing | 3-5 days | Phase 3 complete, all parts fit |
| Phase 5: Documentation | 2-3 days | Phase 4 complete |
| Phase 6: Enhancements (optional) | Ongoing | Any phase |

**Total estimated time:** 3-4 weeks (excluding optional enhancements)

---

## Design Considerations & Best Practices

### Ergonomics
- Display should be visible at 30-60° viewing angle
- Buttons should be easy to reach without looking
- Device should be stable when pressing buttons (no rocking)

### MIDI Signal Integrity
- Keep MIDI cables away from power lines
- Use shielded cable if possible (though DIN-5 MIDI is robust)
- Ground the enclosure if using metal

### Battery Safety
- Ensure adequate ventilation around battery
- Isolate battery from PCBs (at least 3mm clearance)
- Use LiPo-safe charging practices
- Consider LiPo fire-resistant bag for transport

### Serviceability
- Make battery replacement easy (4 screws max)
- USB port accessible without tools
- Display and buttons accessible for cleaning
- Document internal layout for future modifications

### Future-Proofing
- Leave room for additional components (encoders, potentiometers)
- Plan for cable routing if adding external switches
- Consider modular design (stackable, expandable)

---

## Resources & References

### CAD Files
- Fusion 360 files: `_hardware_files/`
- Adafruit CAD library: https://github.com/adafruit/Adafruit_CAD_Parts
- MIDI DIN-5 jack models: https://www.switchcraft.com (12B series)

### Design Inspiration
- Teenage Engineering (minimalist aesthetic)
- Elektron (professional MIDI gear)
- DIY Eurorack modules (modular design)

### Manufacturing Services
- **3D Printing:** Shapeways, Xometry, local makerspaces
- **Laser Cutting:** Ponoko, SendCutSend
- **CNC:** Protolabs, Xometry
- **PCB Fabrication (if creating custom panels):** OSH Park, JLCPCB

### Tools & Software
- **CAD:** Fusion 360 (already have files)
- **Slicing (3D print):** Cura, PrusaSlicer
- **Vector editing (laser cut):** Inkscape, Adobe Illustrator
- **Rendering:** KeyShot, Fusion 360 built-in

---

## Next Steps

1. **Choose form factor** (horizontal, vertical, angled)
2. **Select material** (3D print PLA recommended for prototype)
3. **Import CAD models** into Fusion 360 assembly
4. **Sketch enclosure outline** based on stack dimensions
5. **Create cardboard mockup** to validate ergonomics
6. **Design and print prototype bottom shell**
7. **Iterate and refine** based on fit testing
8. **Complete full enclosure design**
9. **Print/fabricate final version**
10. **Assemble and enjoy!**

---

## Questions to Answer Before Starting

**Confirmed Decisions:**
- ✓ **Form Factor:** Horizontal desktop box
- ✓ **Manufacturing:** 3D printing with Fusion 360
- ✓ **Power:** Direct USB-C access from M4 Express
- ✓ **Power Switch:** Model 805 slide switch

**Finalized Decisions:**
- ✓ **CV Output Labeling:** Generic "CV 1-4" (can be reprogrammed for any function)
- ✓ **Portability:** Desktop-only (no handle or protective features needed)
- ✓ **3D Printer:** Bambu Labs A1 Mini (no AMS-lite) - single color prints
- ✓ **Aesthetic:** Clean, functional design
- ✓ **External Controls:** None - keeping it simple with just 3 buttons on OLED Wing
- ✓ **Finish:** Raw 3D print (no painting or post-processing required)

**Configuration Summary:**
- **Stack:** M4 Feather CAN Express + MIDI FeatherWing + OLED FeatherWing
- **Power:** USB-C charging via M4 Feather (built-in LiPo charger)
- **5V Boost:** Teyleten Multi-Function Boost Module (3.7V→5V @ 1.5A, $0.70)
- **Power Distribution:** Slide switch Model 805 splits battery to M4 BAT + Boost Module
- **CV Output:** MCP4728 Quad DAC (4 channels, 0-5V, I2C)
- **Front panel:** 2x DIN-5 MIDI (IN/OUT) + 4x 1/8" TRS (CV 1-4, 0-5V)
- **Rear panel:** USB-C only (charging + programming, single port!)
- **Side panel:** Model 805 slide switch (power distribution hub)
- **Top panel:** OLED display + 3 button access
- **Benefits:** True 0-5V CV (1V/octave), 4 channels, USB-C charging, simpler/cheaper design

## Power & CV Output Technical Notes

### Power Architecture (Slide Switch as Distribution Hub)
```
LiPo Battery (3.7V, 500-1200mAh)
    ↓
    JST connector
    ↓
Slide Switch Model 805 (Power Distribution Hub)
    ↓
    ├──→ Wire 1: M4 Feather BAT pin (for USB-C charging + powers stack)
    │
    └──→ Wire 2: Teyleten Boost Module VIN (3.7V input)
             ↓
         Boost to 5V @ 1.5A
             ↓
         MCP4728 DAC (VCC + VREF = 5V)
             ↓
        4× CV Outputs (0-5V each)

When USB-C plugged in:
- M4 charges battery @ 500mA
- M4 also powers stack from USB
- Boost Module continues powering MCP4728 from battery
```

### MCP4728 Quad DAC Specifications
- **Resolution:** 12-bit (4096 steps per channel)
- **Voltage Range:** 0-5V (when powered by 5V from Teyleten Boost)
- **Channels:** 4 independent outputs (A, B, C, D)
- **Interface:** I2C (address 0x60 default)
- **Output Impedance:** Low (~1kΩ), suitable for direct CV connection
- **Power:** 5V from Teyleten Boost Module @ 1.5A

### Wiring Details
**I2C (Control):**
- M4 SCL → MCP4728 SCL
- M4 SDA → MCP4728 SDA
- Note: OLED FeatherWing also uses I2C (0x3C), no conflict with MCP4728 (0x60)

**Power Distribution from Slide Switch:**
- Battery + → Slide Switch IN
- Slide Switch OUT → Split to:
  - M4 Feather BAT pin (for charging circuit)
  - Teyleten Boost VIN (for 5V generation)
- Battery - → Common GND (all boards)

**5V Power:**
- Teyleten Boost 5V OUT → MCP4728 VCC
- Teyleten Boost GND → MCP4728 GND

### CircuitPython Usage Example
```python
import board
import busio
import adafruit_mcp4728

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4728
dac = adafruit_mcp4728.MCP4728(i2c)

# Set CV outputs (0-65535 maps to 0-5V)
dac.channel_a.value = 32768  # 2.5V
dac.channel_b.value = 65535  # 5V (max)
dac.channel_c.value = 0      # 0V
dac.channel_d.value = 49152  # 3.75V

# 1V/Octave pitch CV example
def midi_note_to_cv(midi_note, base_note=36):
    """Convert MIDI note to 1V/octave CV (C1 = 1V)"""
    volts = (midi_note - base_note) / 12.0 + 1.0  # C1 (36) = 1V
    dac_value = int((volts / 5.0) * 65535)
    return max(0, min(65535, dac_value))

# Send MIDI note 60 (C3) as CV (3V output)
dac.channel_a.value = midi_note_to_cv(60)
```

### CV Applications (4 Channels)
**Suggested channel assignments:**
- **CV 1:** Pitch (1V/octave, tracks arp notes)
- **CV 2:** Gate (0V = off, 5V = on when note playing)
- **CV 3:** Velocity/Modulation (0-5V proportional to MIDI velocity)
- **CV 4:** Clock/Trigger (pulses on each arp step)

**Compatible Vintage Synths:**
- Moog (Source, Prodigy, Minimoog): 1V/octave ✅
- ARP (Odyssey, 2600): 1V/octave ✅
- Roland (SH-101, Juno-60): 1V/octave ✅
- Korg (MS-20, MS-10): 1V/octave ✅
- Sequential Circuits (Prophet-5): 1V/octave ✅

Once these final questions are answered, we can begin CAD modeling!
