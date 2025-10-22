# Hardware Build Guide
## MIDI Arpeggiator with CV/Gate Outputs - Complete Assembly Instructions

**Version:** 1.0
**Date:** 2025-10-15
**Difficulty:** Intermediate (soldering required)
**Estimated Time:** 3-4 hours

---

## Table of Contents

1. [Parts List & BOM](#parts-list--bom)
2. [Tools Required](#tools-required)
3. [Pre-Assembly Preparation](#pre-assembly-preparation)
4. [Step 1: Power Decoupling Capacitor](#step-1-power-decoupling-capacitor)
5. [Step 2: Series Protection Resistors](#step-2-series-protection-resistors)
6. [Step 3: TRS Jack Preparation](#step-3-trs-jack-preparation)
7. [Step 4: Panel Assembly](#step-4-panel-assembly)
8. [Step 5: Wiring CV/Gate Outputs](#step-5-wiring-cvgate-outputs)
9. [Step 6: FeatherWing Stack Assembly](#step-6-featherwing-stack-assembly)
10. [Step 7: Power Distribution](#step-7-power-distribution)
11. [Step 8: Final Assembly](#step-8-final-assembly)
12. [Step 9: Testing & Verification](#step-9-testing--verification)
13. [Troubleshooting](#troubleshooting)

---

## Parts List & BOM

### Core Electronics

| Item | Qty | Price | Source | Notes |
|------|-----|-------|--------|-------|
| **Adafruit Feather M4 CAN Express** | 1 | $24.95 | Adafruit #4759 | Main controller with USB-C charging |
| **Adafruit OLED FeatherWing (128x32)** | 1 | $14.95 | Adafruit #4650 | Display + 3 buttons |
| **Adafruit MIDI FeatherWing** | 1 | $9.95 | Adafruit #4740 | MIDI In/Out |
| **Adafruit MCP4728 Quad DAC** | 1 | $8.95 | Adafruit #4470 | CV/Gate output (I2C: 0x60) |
| **LiPo Battery** (500-1200mAh, 3.7V) | 1 | $7.95 | Adafruit #258 or #328 | JST connector |

**Subtotal Core:** $66.75

### Power Components

| Item | Qty | Price | Source | Notes |
|------|-----|-------|--------|-------|
| **Teyleten Boost Module** (3.7V→5V) | 1 | $0.70 | Amazon (10-pack ~$7) | Powers MCP4728 DAC |
| **Slide Switch Model 805** | 1 | $1.50 | Generic | Power distribution hub |

**Subtotal Power:** $2.20

### CV/Gate Output Components (Best Practice)

| Item | Qty | Price | Source | Notes |
|------|-----|-------|--------|-------|
| **Thonkiconn PJ301M-12** (3.5mm TRS jack) | 2 | $1.25 | Thonkiconn, Tayda, Mouser | Panel-mount jacks |
| **0.1µF Ceramic Capacitor** (50V) | 1 | $0.05 | Generic | Power decoupling for DAC |
| **100Ω Resistor** (1/4W) | 2 | $0.02 | Generic | Series protection (OUT A, OUT B) |

**Subtotal CV/Gate:** $2.59

### Wire & Connectors

| Item | Qty | Price | Source | Notes |
|------|-----|-------|--------|-------|
| **22-24 AWG Stranded Wire** (red/black) | 2 feet | $0.50 | Generic | Power distribution |
| **22-24 AWG Stranded Wire** (various colors) | 2 feet | $0.50 | Generic | Signal wiring |
| **Heat Shrink Tubing** (assorted sizes) | 1 pack | $3.00 | Generic | Insulating solder joints |
| **Jumper Wires** (F/F, M/F) | 10-15 | $1.00 | Generic | I2C connections |

**Subtotal Wire:** $5.00

### Hardware & Mounting

| Item | Qty | Price | Source | Notes |
|------|-----|-------|--------|-------|
| **M2.5 Screws** (6-10mm) | 10-20 | $1.00 | Generic | Stack mounting |
| **M3 Screws** (various lengths) | 10-15 | $1.50 | Generic | Enclosure assembly |
| **M2.5/M3 Standoffs** | 10-15 | $2.50 | Generic | Board spacing |
| **Double-sided Foam Tape** | 1 roll | $2.00 | Generic | DAC/Boost mounting |

**Subtotal Hardware:** $7.00

### Panel Connectors

| Item | Qty | Price | Source | Notes |
|------|-----|-------|--------|-------|
| **DIN-5 Panel Mount MIDI Jacks** | 2 | $2.50 | Generic | MIDI In/Out |

**Subtotal Connectors:** $5.00

### **Total Build Cost: ~$88.50**

---

## Tools Required

### Essential Tools

- ✅ **Soldering iron** (15-30W with fine tip)
- ✅ **Solder** (60/40 or lead-free, 0.8mm diameter)
- ✅ **Wire strippers** (22-24 AWG)
- ✅ **Diagonal cutters** (flush cut)
- ✅ **Multimeter** (voltage, continuity, resistance)
- ✅ **Small Phillips screwdriver**
- ✅ **Small flathead screwdriver**
- ✅ **Heat gun or lighter** (for heat shrink)

### Helpful But Optional

- ⭕ Helping hands / PCB holder
- ⭕ Solder wick or desoldering pump
- ⭕ Tweezers (for small components)
- ⭕ Wire stripper gauge
- ⭕ Digital calipers (for measurements)
- ⭕ Magnifying glass or headband magnifier

---

## Pre-Assembly Preparation

### 1. Workspace Setup

- **Clean, flat surface** with good lighting
- **Anti-static mat** (optional but recommended)
- **Organize parts** in small containers or pill boxes
- **Have documentation ready:** This guide + datasheets

### 2. Inventory Check

**Verify you have all parts from BOM:**
- [ ] All FeatherWing boards (M4, OLED, MIDI, MCP4728)
- [ ] Power components (Boost module, slide switch, battery)
- [ ] CV/Gate components (2× TRS jacks, 1× capacitor, 2× resistors)
- [ ] Wire and heat shrink
- [ ] Connectors and hardware

### 3. Test Before Assembly

**Test each FeatherWing separately:**
1. **M4 Feather:** Connect USB-C, verify CircuitPython drive appears
2. **OLED Wing:** Stack on M4, run simple display test code
3. **MIDI Wing:** Stack on M4, test MIDI loopback
4. **MCP4728 DAC:** Connect to I2C, verify address 0x60 detected

**Why test first?**
- Easier to troubleshoot individual boards
- Avoid debugging fully assembled device
- Confirm no DOA (dead on arrival) parts

---

## Step 1: Power Decoupling Capacitor

**Purpose:** Filters noise from 5V power supply, stabilizes DAC output voltage.

### Parts Needed:
- 1× 0.1µF ceramic capacitor (code 104)
- MCP4728 DAC breakout board
- Soldering iron and solder

### Instructions:

1. **Identify capacitor orientation:**
   - Ceramic capacitors are **non-polarized** (no + or -)
   - Can be installed in either direction

2. **Locate VCC and GND pads on MCP4728:**
   - **VCC:** Power input pad (connects to 5V boost)
   - **GND:** Ground pad (common ground)
   - Usually labeled on silkscreen

3. **Solder capacitor:**
   ```
   MCP4728 Breakout
   ┌─────────────────┐
   │  VCC ──┬── ...  │
   │        │        │
   │      [0.1µF]    │  ← Solder here
   │        │        │
   │  GND ──┴── ...  │
   └─────────────────┘
   ```
   - Bend capacitor leads to fit VCC-GND spacing
   - Insert leads through holes (if through-hole board)
   - Solder on underside, trim excess leads
   - **If SMD board:** Solder between VCC and GND pads with short wires

4. **Verify connection:**
   - Use multimeter continuity mode
   - Check capacitor is bridging VCC to GND
   - Should NOT beep (capacitor blocks DC)

**✅ Checkpoint:** Capacitor installed flush against board, clean solder joints.

---

## Step 2: Series Protection Resistors

**Purpose:** Limits fault current if DAC output shorted, protects DAC from damaged cables.

### Parts Needed:
- 2× 100Ω resistors (1/4W, color bands: brown-black-brown)
- MCP4728 DAC breakout board
- ~2 inches 22 AWG wire per resistor
- Heat shrink tubing

### Instructions:

1. **Prepare resistor leads:**
   - Cut 2× pieces of 22 AWG wire (~2 inches each)
   - Strip 3mm from each end
   - Tin one end of each wire

2. **Solder resistors to DAC outputs:**

   **Method A: Direct solder to pads (if board has through-hole pads)**
   ```
   MCP4728
   ┌──────────────────────┐
   │  OUT A ──[100Ω]──●   │ ← Wire 1 (CV Pitch)
   │  OUT B ──[100Ω]──●   │ ← Wire 2 (Gate)
   │  OUT C (unused)      │
   │  OUT D (unused)      │
   └──────────────────────┘
   ```
   - Solder resistor lead to OUT A pad
   - Solder wire to other resistor lead
   - Repeat for OUT B

   **Method B: Flying wires (if board has screw terminals or SMD pads)**
   - Solder wire directly to OUT A pad/terminal
   - Solder 100Ω resistor in-line with wire
   - Repeat for OUT B
   - Cover resistor and exposed leads with heat shrink

3. **Insulate connections:**
   - Slide heat shrink over resistor + leads
   - Heat with heat gun or carefully with lighter
   - Ensure no exposed metal

4. **Label wires:**
   - Use masking tape or label maker
   - Wire 1: "CV PITCH" (from OUT A + resistor)
   - Wire 2: "GATE" (from OUT B + resistor)

**✅ Checkpoint:** 2 wires with 100Ω resistors, insulated with heat shrink, labeled.

---

## Step 3: TRS Jack Preparation

**Purpose:** Wire TRS jacks for mono CV/Gate signals with TS/TRS cable compatibility.

### Parts Needed:
- 2× Thonkiconn PJ301M-12 (3.5mm TRS jacks)
- ~6 inches 22 AWG wire per jack (2× signal, 2× ground)
- Short piece of bare wire (~10mm per jack)
- Heat shrink tubing

### Instructions (per jack, repeat for both):

1. **Identify jack terminals:**
   ```
   TRS Jack (rear view)

      [Tip]  ← Longest lug (signal)
       [R]   ← Middle lug (ring)
       [S]   ← Shortest lug or threaded body (sleeve/ground)
   ```

2. **Tie Ring to Sleeve (critical step):**
   - Cut ~10mm piece of bare solid wire
   - Form small U-shape
   - Solder one end to Ring terminal
   - Solder other end to Sleeve terminal
   - **This connection is ESSENTIAL for TS cable compatibility**
   - Cover with small piece of heat shrink if terminals close together

3. **Prepare signal wire (Tip):**
   - Cut 6-8 inches of colored wire (use different colors for each jack)
   - Strip 3mm from one end
   - Tin the stripped end
   - Solder to **Tip** terminal
   - **Jack 1:** Use wire from Step 2 (CV Pitch, OUT A + 100Ω)
   - **Jack 2:** Use wire from Step 2 (Gate, OUT B + 100Ω)

4. **Prepare ground wire (Sleeve):**
   - Cut 6-8 inches of **black** wire
   - Strip 3mm from one end
   - Tin the stripped end
   - Solder to **Sleeve** terminal (where Ring is also connected)

5. **Verify wiring:**
   ```
   Jack wiring (per jack):

   TIP ────────→ Signal (from DAC OUT + 100Ω resistor)
   RING ───┐
           ├───→ Common GND
   SLEEVE ─┘
   ```

6. **Test continuity:**
   - Multimeter: Continuity mode
   - Tip to Ring: Should be OPEN (no beep)
   - Ring to Sleeve: Should be SHORT (beep)
   - Tip to Sleeve: Should be OPEN (no beep)

7. **Label jacks:**
   - Use masking tape on jack body
   - Jack 1: "CV PITCH"
   - Jack 2: "GATE"

**✅ Checkpoint:** 2× TRS jacks prepared, Ring-Sleeve tied, signal and ground wires attached, labeled.

---

## Step 4: Panel Assembly

**Purpose:** Mount all panel connectors on the rear panel before final wiring.

### Parts Needed:
- Rear panel (3D printed or fabricated)
- 2× TRS jacks (from Step 3)
- 2× DIN-5 MIDI jacks (panel mount)
- Hex nuts (included with jacks)
- Small wrench or pliers

### Instructions:

1. **Verify panel holes:**
   - **MIDI jacks:** 2× 14mm diameter holes, 30mm apart (left side)
   - **CV/Gate jacks:** 2× 6mm diameter holes, 17mm apart (right side)
   - **USB-C cutout:** 10mm × 5mm rectangle (center)
   - Deburr holes if needed (file or sandpaper)

2. **Mount DIN-5 MIDI jacks (left side):**
   - Insert jack from **outside** of panel
   - Thread retaining nut from **inside**
   - Tighten securely
   - Align pins correctly (check orientation)
   - **Far left:** MIDI IN
   - **Center left:** MIDI OUT

3. **Mount TRS jacks (CV/Gate, right side):**
   - Insert jack from **outside** of panel
   - Jack body should sit flush against panel
   - Thread retaining nut from **inside**
   - Tighten with wrench (don't overtighten plastic threads)
   - Ensure jack is straight and seated properly
   - **Center right:** CV Pitch
   - **Far right:** Gate

4. **Verify USB-C alignment:**
   - Check that M4 Feather USB-C port aligns with rear panel cutout
   - Adjust internal mounting if needed for proper alignment

5. **Label panel (optional but recommended):**
   - Use vinyl labels, laser engraving, or permanent marker
   - Labels: "MIDI IN", "OUT", "USB-C", "CV", "GATE"
   - Optional: Add polarity indicator "V-TRIG" or voltage range "0-5V"

**Rear panel layout:**
```
┌──────────────────────────────────────────────┐
│  [MIDI IN]  [OUT]  [USB-C]  [CV]   [GATE]   │
│    DIN-5    DIN-5  10×5mm   TRS     TRS      │
└──────────────────────────────────────────────┘
```

**✅ Checkpoint:** All panel connectors mounted securely on rear panel, aligned properly, labeled.

---

## Step 5: Wiring CV/Gate Outputs

**Purpose:** Connect DAC outputs to TRS jacks via protection resistors.

### Parts Needed:
- MCP4728 DAC board (with capacitor and resistors from Steps 1-2)
- 2× TRS jacks (mounted in rear panel from Step 4)
- Signal wires already attached
- Soldering iron

### Instructions:

1. **Route wires from DAC to rear panel:**
   - Position DAC near rear panel (leave 6-8 inches of wire for routing)
   - Route signal wires neatly along the internal path
   - Avoid crossing power wires

2. **Verify connections (before power-on):**
   ```
   MCP4728 DAC
   ┌──────────────────────────────┐
   │  VCC ──┬── (to 5V boost)     │
   │        │                     │
   │      [0.1µF] ← Capacitor     │
   │        │                     │
   │  GND ──┴── (to common GND)   │
   │                              │
   │  OUT A ──[100Ω]───────●      │ ── CV Pitch Jack Tip
   │  OUT B ──[100Ω]───────●      │ ── Gate Jack Tip
   │                              │
   │  GND ─────────────────●──●   │ ── Both Jack Sleeves
   └──────────────────────────────┘
   ```

3. **Connect ground wires:**
   - Both TRS jack **Sleeve** wires (black) share common ground
   - Solder both black wires to **GND** pad on MCP4728
   - Use common bus bar or wire splice if needed
   - Alternatively: Solder to common GND point in enclosure

4. **Strain relief:**
   - Leave ~10mm slack in wires near DAC
   - Use cable tie or wire clip to secure bundle
   - Ensure wires won't pull on solder joints when panel moves

**✅ Checkpoint:** DAC outputs connected to jacks through resistors, grounds tied together.

---

## Step 6: FeatherWing Stack Assembly

**Purpose:** Build the M4 + OLED stack and mount MIDI FeatherWing beside it for a low-profile footprint.

### Parts Needed:
- Adafruit M4 Feather CAN Express
- OLED FeatherWing
- MIDI FeatherWing
- M2.5 standoffs (8-12mm height)
- M2.5 screws (6-10mm)
- Stacking headers for OLED
- Female-to-female jumper wires (for MIDI wing connections)

### Instructions:

1. **Prepare headers:**
   - M4 Feather may need female headers soldered
   - OLED Wing needs male stacking headers
   - **MIDI Wing:** Install male headers (NOT stacking - it will be mounted beside the stack)
   - See Adafruit assembly guides for header installation

2. **Stack order (M4 + OLED only):**
   ```
   ┌──────────────────────┐
   │   OLED FeatherWing   │ ← Top (display + buttons)
   ├──────────────────────┤
   │ M4 Feather CAN (base)│ ← Bottom (USB-C rear-facing)
   └──────────────────────┘

   Mounted beside stack:
   ┌──────────────────────┐
   │   MIDI FeatherWing   │ ← Side-mounted (MIDI In/Out jacks to rear)
   └──────────────────────┘
   ```

3. **Install standoffs for M4+OLED stack:**
   - Use M2.5 standoffs between M4 and OLED
   - Install at 4 mounting holes (corners)
   - Height: 8-12mm (allows clearance for components)

4. **Mount MIDI FeatherWing beside stack:**
   - Use separate standoffs or foam tape to mount MIDI wing horizontally
   - Position with MIDI jacks facing **rear panel**
   - Leave 5-10mm gap between MIDI wing and M4 stack for wire routing
   - Ensure MIDI wing is at similar height to M4 for easy wiring

5. **Orient USB-C port:**
   - **Critical:** Position M4 with USB-C facing **rear panel**
   - Allows direct access for charging/programming
   - No panel-mount USB extension needed

6. **Connect MIDI FeatherWing to M4:**
   - Use jumper wires (F/F) to connect MIDI wing to M4:
     - MIDI Wing **VIN** → M4 **USB** or **3V** (power)
     - MIDI Wing **GND** → M4 **GND**
     - MIDI Wing **TX** → M4 **RX** (UART serial)
     - MIDI Wing **RX** → M4 **TX** (UART serial)
   - Route wires neatly between boards

7. **Connect I2C for MCP4728:**
   - MCP4728 needs I2C connection to M4
   - Use jumper wires (F/F or M/F):
     - M4 **SCL** → MCP4728 **SCL**
     - M4 **SDA** → MCP4728 **SDA**
   - Note: OLED also uses I2C (address 0x3C, no conflict with DAC at 0x60)

**✅ Checkpoint:** M4+OLED stack assembled, MIDI wing mounted beside stack, all connections wired, USB-C accessible.

---

## Step 7: Power Distribution

**Purpose:** Wire battery, boost module, and slide switch for power distribution.

### Parts Needed:
- Slide switch Model 805
- Teyleten boost module
- LiPo battery (JST connector)
- 22 AWG red/black wire
- Heat shrink tubing

### Wiring Architecture:

```
LiPo Battery (3.7V, JST connector)
    ↓
    (Red +) ────→ Slide Switch IN

Slide Switch OUT ─────┬───→ Wire 1: M4 Feather BAT pin
                      │
                      └───→ Wire 2: Boost Module VIN

Boost Module:
    VIN (3.7V input)
    VOUT (5V output) ───→ MCP4728 VCC
    GND ────────────────→ Common GND

Battery (Black -) ─────→ Common GND (M4 + Boost + DAC)
```

### Instructions:

1. **Prepare slide switch wiring:**
   - Cut 3× pieces of 22 AWG wire (~4-6 inches each)
   - 1× red wire: Battery + to switch IN
   - 2× red wires: Switch OUT to M4 BAT + Boost VIN

2. **Solder battery wire to switch:**
   - **Battery JST red wire** → Slide Switch **IN** terminal
   - Use heat shrink on connection

3. **Solder output wires to switch:**
   - **Wire 1 (red)** → Slide Switch **OUT** terminal → M4 BAT pin
   - **Wire 2 (red)** → Slide Switch **OUT** terminal → Boost VIN
   - Both wires share same OUT terminal (solder both together)
   - Use heat shrink on switch connections

4. **Connect boost module:**
   - **Boost VIN** ← Wire 2 from switch
   - **Boost VOUT (5V)** → MCP4728 VCC
   - **Boost GND** → Common ground bus

5. **Connect grounds:**
   - **Battery JST black wire** → Common GND
   - **M4 GND** → Common GND
   - **Boost GND** → Common GND
   - **MCP4728 GND** → Common GND
   - Use wire splice or common bus bar

6. **Adjust boost output voltage:**
   - **Before connecting to DAC:** Measure boost VOUT with multimeter
   - Adjust trim pot on boost module to **5.0V** (±0.05V)
   - **Critical:** Do NOT exceed 5.5V (may damage MCP4728)

**✅ Checkpoint:** Power distribution wired, boost outputting 5.0V, switch controls both M4 and boost.

---

## Step 8: Final Assembly

**Purpose:** Mount all components in enclosure and organize wiring.

### Instructions:

1. **Mount M4+OLED stack:**
   - Install in enclosure with standoffs or mounting brackets
   - Ensure USB-C port aligns with rear panel cutout
   - Leave access to reset button
   - Position toward front/center of enclosure

2. **Mount MIDI FeatherWing:**
   - Install beside M4 stack using standoffs or foam tape
   - Position with MIDI jacks facing rear panel
   - Ensure MIDI jacks align with rear panel DIN-5 holes
   - Leave clearance for jumper wires to M4

3. **Mount MCP4728 DAC:**
   - Use double-sided foam tape OR small standoffs
   - Position near rear panel for short wire runs to CV/Gate jacks
   - Ensure I2C wires reach M4 SCL/SDA

4. **Mount boost module:**
   - Use double-sided foam tape
   - Position near battery and slide switch
   - Ensure wires not strained

5. **Mount slide switch:**
   - Install in side panel cutout (see `805 slide switch.f3d` for dimensions)
   - Secure with mounting screws or clips
   - Label panel: "POWER" with ON/OFF indicators

6. **Install battery:**
   - Use Velcro strap or foam padding
   - Position away from PCBs (3-5mm clearance)
   - Ensure JST connector reaches switch

7. **Cable management:**
   - Route power and signal wires separately (5-10mm gap)
   - Route MIDI wing jumper wires neatly to M4 stack
   - Use cable ties or wire clips
   - Leave slack for serviceability (~10mm)
   - Organize wire bundles neatly

8. **Verify clearances:**
   - All components clear enclosure walls
   - MIDI wing jacks align with rear panel DIN-5 holes
   - M4 USB-C aligns with rear panel cutout
   - No wires pinched or strained
   - Panel cutouts align with ports
   - Battery has room for expansion

**✅ Checkpoint:** All components mounted securely, wiring organized, clearances verified.

---

## Step 9: Testing & Verification

**Purpose:** Verify all functions before closing enclosure.

### Pre-Power Checks (Multimeter):

1. **Continuity tests:**
   - [ ] Battery + to M4 BAT (through switch when ON)
   - [ ] Battery + to Boost VIN (through switch when ON)
   - [ ] Switch OFF: No continuity Battery + to outputs
   - [ ] All grounds connected (Battery -, M4 GND, Boost GND, DAC GND)

2. **Resistance tests:**
   - [ ] TRS Jack Tip to Sleeve: High impedance (>100kΩ)
   - [ ] TRS Jack Ring to Sleeve: 0Ω (direct connection)
   - [ ] No shorts between power and ground

3. **Isolation tests:**
   - [ ] VCC (5V rail) NOT shorted to GND
   - [ ] Battery + NOT shorted to GND
   - [ ] DAC outputs NOT shorted to GND or each other

### Power-On Tests:

1. **USB power test (slide switch OFF):**
   - Connect USB-C to M4 Feather
   - CIRCUITPY drive should appear
   - Upload firmware if not already installed
   - Verify OLED displays correctly
   - Press buttons to test functionality

2. **Battery power test:**
   - Disconnect USB
   - Turn slide switch ON
   - Device should power on
   - OLED should display normally

3. **Boost voltage test:**
   - Measure voltage at MCP4728 VCC pin
   - Should read **5.0V ± 0.1V**
   - If incorrect, adjust boost trim pot

### CV/Gate Output Tests:

1. **Static voltage test:**
   - Insert voltmeter probes into TRS jacks (Tip = +, Sleeve = -)
   - CV Jack: Should read 0-5V when playing MIDI notes
   - Gate Jack: Should toggle between 0V (off) and 5V (on)

2. **TS/TRS cable compatibility:**
   - Test with TS (mono) cable → Should work
   - Test with TRS (stereo) cable → Should work
   - No hum, buzz, or noise

3. **Polarity test:**
   - Navigate to Triggers menu
   - Toggle V-trig ↔ S-trig
   - V-trig: 0V off, 5V on
   - S-trig: 5V off, 0V on (inverted)

4. **Pitch accuracy test:**
   - Send MIDI note C3 (60)
   - Measure CV output: Should be 1V or 2V (depending on reference setting)
   - Send C4 (72)
   - Should be +1V higher than C3
   - Verify 1V/octave scaling

### Functional Tests:

1. **Serial console test:**
   - Connect to serial console (see README)
   - Run: `help`
   - Should show test commands
   - Run: `test i2c`
   - Should detect OLED (0x3C) and DAC (0x60)

2. **DAC test:**
   - Run: `test dac`
   - Should test all 4 channels
   - Verify voltage output on CV/Gate jacks

3. **Full hardware test:**
   - Run: `test all`
   - Verify all components pass
   - Check for errors in output

4. **MIDI loopback test:**
   - Connect MIDI Out to MIDI In (with MIDI cable)
   - Play notes on external keyboard
   - Should arpeggio correctly
   - Verify display shows pattern and BPM

**✅ Checkpoint:** All tests passed, CV/Gate outputs working, no errors.

---

## Troubleshooting

### Problem: No power when slide switch ON

**Possible causes:**
- Battery depleted
- Switch not making contact
- Wire disconnected

**Solution:**
1. Measure battery voltage (should be 3.0-4.2V)
2. Check switch continuity when ON
3. Verify solder joints on switch terminals
4. Check wire connections to BAT pin and Boost VIN

---

### Problem: Boost module not outputting 5V

**Possible causes:**
- Boost not powered (check VIN connection)
- Trim pot not adjusted
- Boost module defective

**Solution:**
1. Verify 3.7V at Boost VIN
2. Measure Boost VOUT (no load)
3. Adjust trim pot with small screwdriver (clockwise = higher voltage)
4. Test with known-good boost module

---

### Problem: No voltage on CV output

**See troubleshooting in `CV_GATE_INTEGRATION.md`**

---

### Problem: Gate stuck HIGH or LOW

**See troubleshooting in `CV_GATE_INTEGRATION.md`**

---

### Problem: TRS jack works with TS cable but not TRS

**Possible causes:**
- Ring not tied to Sleeve
- Faulty TRS cable

**Solution:**
1. Check Ring-Sleeve solder joint
2. Verify continuity between Ring and Sleeve terminals
3. Test with different TRS cable

---

### Problem: Ground loop hum/noise

**Possible causes:**
- Ground wire not connected
- Ground loop with external synth
- Inadequate power decoupling

**Solution:**
1. Verify 0.1µF capacitor on DAC VCC
2. Check all ground connections
3. Use ground lift on external synth
4. Add ferrite bead on CV cable

---

## Safety Notes

⚠️ **LiPo Battery Safety:**
- Never puncture or damage battery
- Don't discharge below 3.0V
- Charge at 500mA max (M4 built-in charger is safe)
- Store at 50% charge if not used for weeks
- Monitor for swelling or heat

⚠️ **Soldering Safety:**
- Work in ventilated area
- Don't touch iron tip (350°C / 660°F)
- Use fume extractor or fan
- Wash hands after soldering (lead solder)

⚠️ **Electrical Safety:**
- Always power off before making connections
- Double-check polarity before connecting battery
- Don't exceed 5.5V on MCP4728 VCC
- Keep CV outputs within 0-5V range

---

## Post-Assembly Checklist

**Before closing enclosure:**
- [ ] All components mounted securely
- [ ] No loose wires or solder blobs
- [ ] All solder joints clean and shiny
- [ ] Heat shrink covers all exposed connections
- [ ] Wires organized and strain-relieved
- [ ] Clearance verified for all moving parts
- [ ] USB-C port accessible
- [ ] Slide switch accessible and labeled
- [ ] All panel jacks seated flush
- [ ] Battery secure and isolated
- [ ] Continuity tests passed
- [ ] Voltage tests passed (5V boost, CV outputs)
- [ ] Functional tests passed (MIDI, CV/Gate, display)

**Final assembly:**
- [ ] Close enclosure (don't overtighten screws)
- [ ] Install rubber feet (optional)
- [ ] Apply labels to panel
- [ ] Take photos for documentation

---

## Firmware Upload

**After hardware assembly:**

1. **Connect USB-C** to M4 Feather
2. **CIRCUITPY drive** should appear
3. **Install CircuitPython libraries** (see README)
4. **Upload firmware files** using `install.py` (see INSTALLER_README)
5. **Test functionality** with hardware test commands

---

## Maintenance

### Regular Maintenance:
- **Every 3 months:** Check solder joints for cracks
- **Every 6 months:** Clean OLED display, check battery voltage
- **Annually:** Replace battery if capacity degraded

### Upgrades:
- Channels C & D available for future expansion
- Can add velocity CV, modulation CV, or clock output
- Firmware updates via USB-C (no disassembly needed)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-15 | Initial build guide with best practice components |

---

## Additional Resources

- **CV/Gate Integration:** See `CV_GATE_INTEGRATION.md`
- **Testing Procedures:** See `TESTING_GUIDE.md`
- **Enclosure Design:** See `ENCLOSURE_ROADMAP.md`
- **BOM Details:** See `BOM.md`
- **Firmware:** See `README.md`

---

**Questions? Issues?** Open a discussion or issue on GitHub.

**Happy Building!** 🔧🎹🎚️
