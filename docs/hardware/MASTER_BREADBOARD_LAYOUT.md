# Master Breadboard Layout Guide
**Complete System Integration - Optimized for Enclosure**

**Date:** 2025-10-31
**Purpose:** Organize entire Arp system on breadboards for enclosure integration
**Status:** Design ready - Optimized for physical enclosure constraints

### Quick Summary

This breadboard layout is **driven by the physical enclosure design**:

- **Two breadboards** (830 tie points each): Board 1 (Control) + Board 2 (Power/CV)
- **Component positioning** matches panel locations for short wire runs
- **Lightpipes** route MIDI LEDs horizontally to LEFT/RIGHT panels (~20-30mm)
- **OLED** positioned CENTER, faces TOP panel
- **Power section** on LEFT (near power switch)
- **CV section** on BACK (near CV output jacks)
- **All external I/O** routes to BACK panel (MIDI DIN-5, CV TRS)

---

## Enclosure Physical Layout (Drives Breadboard Design)

### Panel Configuration

```
                    TOP PANEL
              [OLED]  [A] [B] [C]
                       ↓
    LEFT SIDE                      RIGHT SIDE
    ┌─────────┐                   ┌─────────┐
    │ USB-C   │                   │         │
    │ Power ○ │   BREADBOARDS    │  ○ LED  │
    │ ○ LED   │                   │         │
    └─────────┘                   └─────────┘
                       ↑
                  BACK PANEL
            [MIDI IN][MIDI OUT][CV][CV]
```

**Physical Panel Layout:**
- **TOP:** OLED window + 3 buttons (A, B, C)
- **BACK:** 2× MIDI DIN-5 + 2× TRS CV jacks
- **LEFT side:** USB-C cutout + Power switch + Lightpipe (MIDI IN LED)
- **RIGHT side:** Lightpipe (MIDI OUT LED)

**Key Design Constraints:**
1. **M4 USB-C** points **LEFT** → Short path to side cutout
2. **MIDI Wing LEDs** positioned **CENTER** → Equal ~20-30mm lightpipe runs LEFT/RIGHT
3. **Power components** on **LEFT** → Near power switch
4. **CV components** at **BACK** → Near TRS jacks
5. **M4/OLED stack** in **CENTER** → OLED visible through top panel

---

## System Overview

### Components to Mount

**Board 1 (Control Board):**
- ✅ Feather M4 + OLED FeatherWing stack (CENTER, OLED faces TOP panel)
- ✅ MIDI FeatherWing (CENTER-RIGHT, LEDs accessible for LEFT/RIGHT lightpipes)
- ✅ 5V and 3.3V power distribution

**Board 2 (Power & Analog Board):**
- ✅ Teyleten Boost Module (LEFT side, 3.7V → 12V, near power switch)
- ✅ L7805 Voltage Regulator (LEFT side, 12V → 5V)
- ✅ MCP4728 Quad DAC (BACK edge, I2C, near CV jacks)
- ✅ TL072 Dual Op-Amp (BACK edge, 2× gain for CV, near MCP4728)
- ✅ 12V and 5V power distribution
- ✅ Passive components (100µF filter, 10µF L7805 caps, 100kΩ resistors, 0.1µF bypass)

### Panel-Mount Externals
- 2× 3.5mm TRS jacks (CV outputs - **BACK panel**)
- 2× DIN-5 MIDI jacks (**BACK panel**)
- 2× Lightpipes (MIDI IN/OUT LEDs → **LEFT/RIGHT sides**, ~30mm horizontal)

---

## Recommended Breadboard Setup

### Option 1: Two Full-Size Breadboards (Recommended)

**Board 1: "Control Board"** (830 tie points)
- M4/OLED/MIDI Featherwing stack
- MIDI FeatherWing
- I2C devices (MCP4728)
- 3.3V and 5V power distribution

**Board 2: "Power & Analog Board"** (830 tie points)
- Teyleten boost (12V generation)
- L7805 regulator (12V → 5V)
- TL072 op-amp (CV gain stage)
- 12V power distribution
- CV output circuitry

### Option 2: Single Large Breadboard (Tight)

**One 1660+ tie point breadboard:**
- More compact
- Harder to troubleshoot
- Less recommended

---

## Board 1: Control Board Layout

**Component Positioning Strategy:**
- **CENTER:** M4/OLED stack (OLED faces TOP panel)
- **CENTER-RIGHT:** MIDI Wing (LEDs positioned for equal-length lightpipe runs LEFT/RIGHT)
- **LEFT side:** 5V power input from Board 2
- **BACK edge:** I2C connections route to Board 2 (MCP4728 is on Board 2 near CV jacks)

```
┌─────────────────────────────────────────────────────────────────┐
│  POWER RAILS (TOP)                                               │
│  ==============================================================  │
│  (+) 5V  ────────────────────────────────────────────────────  │ ← From Board 2
│  (-) GND ────────────────────────────────────────────────────  │ ← Common GND
│  (+) 3.3V ───────────────────────────────────────────────────  │ ← From M4 3V3 pin
│  (-) GND ────────────────────────────────────────────────────  │
│                                                                  │
│  COMPONENTS (Positioned for enclosure layout)                   │
│                                                                  │
│  LEFT              CENTER                       RIGHT            │
│                                                                  │
│  [5V IN]←─    ┌──────────────────┐         ┌─────────────┐     │
│  (from         │   M4 FEATHER     │         │   MIDI      │     │
│   Board 2)     │   + OLED STACK   │   ↔I2C→ │   WING      │     │
│                │                  │         │             │     │
│                │  OLED faces ↑    │         │  LED ●──┐   │     │ ← MIDI IN LED
│                │  (TOP panel)     │         │         │   │     │   (lightpipe LEFT)
│                └──────────────────┘         │  LED ●──┼───│     │ ← MIDI OUT LED
│                        ↕ I2C                │         │   │     │   (lightpipe RIGHT)
│                        ↓                    │  [JACKS]│   │     │
│                  (to Board 2                └─────────┼───┘     │
│                   MCP4728)                            │          │
│                                                       │          │
│  Wire routing to Board 2:                         Lightpipes    │
│  - I2C (SDA/SCL) → MCP4728                       route to       │
│  - MIDI RX/TX connections                       LEFT/RIGHT      │
│                                                   panels         │
│                                                                  │
│  POWER RAILS (BOTTOM)                                            │
│  ==============================================================  │
│  (+) 5V  ────────────────────────────────────────────────────  │
│  (-) GND ────────────────────────────────────────────────────  │
└─────────────────────────────────────────────────────────────────┘

         ↑ TOP (OLED visible)              ↑ BACK (MIDI jacks wire to panel)
```

### Key Connections on Board 1

**Power Distribution:**
```
5V rail source:
  - From Board 2 L7805 output
  - OR from M4 USB pin (when USB connected)

3.3V rail source:
  - From M4 3V3 output pin (onboard regulator)

GND rails:
  - Common ground for entire system
```

**M4 Stack Mounting:**
1. Use male header pins or standoffs
2. Insert headers into breadboard holes
3. Stack sits above breadboard surface
4. Access to all M4 pins via breadboard rows

**MIDI FeatherWing Position:**
- Mount CENTER-RIGHT of breadboard, ~1-2" from M4 stack
- LEDs must be accessible from above for lightpipe coupling
- Position LEDs for equal-length runs to LEFT/RIGHT side panels (~20-30mm each)
- Wire MIDI RX/TX to M4 UART pins (orange/purple wires)
- MIDI jacks route to BACK panel (wired externally to panel-mount DIN-5 jacks)

**I2C Bus to Board 2:**
- SDA (yellow wire, 6-12") → Board 2 MCP4728
- SCL (green wire, 6-12") → Board 2 MCP4728
- MCP4728 is located on Board 2 near CV output section

---

## Board 2: Power & Analog Board Layout

**Component Positioning Strategy:**
- **LEFT side:** Teyleten boost + L7805 (power switch is on LEFT panel)
- **BACK edge:** MCP4728 DAC + TL072 Op-Amp (CV jacks are on BACK panel)
- **CENTER:** Power rail distribution and interconnects

```
┌──────────────────────────────────────────────────────────────────┐
│  POWER RAILS (TOP)                                                │
│  ===============================================================  │
│  (+) 12V ──────────────────────────────────────────────────────  │ ← Teyleten OUT
│  (-) GND ──────────────────────────────────────────────────────  │ ← Common GND
│  (+) 5V  ──────────────────────────────────────────────────────  │ ← L7805 OUT
│  (-) GND ──────────────────────────────────────────────────────  │
│                                                                   │
│  COMPONENTS (Positioned for enclosure layout)                    │
│                                                                   │
│  LEFT (Power)         CENTER              BACK (CV Outputs)      │
│                                                                   │
│  ┌──────────┐                         ┌──────────┐               │
│  │ TEYLETEN │    [5V to Board 1]──→   │ MCP4728  │               │
│  │  BOOST   │                          │   DAC    │               │
│  │ 3.7V→12V │    100µF                 │ (I2C)    │               │
│  └────┬─────┘    filter               └────┬─────┘               │
│       │          cap                        │ VA,VB               │
│      12V                                    ↓                     │
│       ↓                                                           │
│  ┌──────────┐                         ┌──────────┐               │
│  │  L7805   │                          │  TL072   │               │
│  │[IN][G][O]│                          │  Op-Amp  │               │
│  │ 12V  5V  │    Power Section        │  DIP-8   │  CV Section  │
│  └──┬───┬───┘                          └────┬─────┘               │
│  10µF 10µF     (Near switch)                │                     │
│   │    │                                    ↓                     │
│   │    └──→ 5V rail ──→ Board 1        CV OUT ──→ [Panel Jack]   │
│   │                                     (BACK)    (BACK panel)    │
│   └──→ 12V rail                                                   │
│                                                                   │
│  Passive Components:                                              │
│  - 100µF electrolytic (12V rail filter)                          │
│  - 10µF caps (L7805 input/output stabilization)                  │
│  - 2× 100kΩ resistors (TL072 gain network: 2× amplification)    │
│  - 0.1µF bypass cap (TL072 Pin 8 power decoupling)              │
│                                                                   │
│  [Battery IN]←─ From power switch (LEFT panel)                   │
│                                                                   │
│  POWER RAILS (BOTTOM)                                             │
│  ===============================================================  │
│  (+) 12V ──────────────────────────────────────────────────────  │
│  (-) GND ──────────────────────────────────────────────────────  │
└──────────────────────────────────────────────────────────────────┘

    ↑ LEFT (Power switch)                ↑ BACK (CV jacks, MIDI jacks)
```

### Key Connections on Board 2

**Teyleten Boost Module:**
```
Input:  Battery 3.7V (JST connector)
Output: 12V @ 1A
Mount:  Use double-sided tape or zip-tie to breadboard edge
Wire:   12V output → 12V power rail
        GND → GND power rail
```

**L7805 Voltage Regulator (TO-220 package):**
```
Pin 1 (IN):   12V rail + 10µF capacitor to GND
Pin 2 (GND):  GND rail
Pin 3 (OUT):  5V rail + 10µF capacitor to GND
                        + jumper wire to Board 1 5V rail

Heat Management:
  - Should run cool with <500mA load
  - If hot, add small heatsink
```

**MCP4728 Quad DAC (I2C):**
```
Pin Connections:
  SDA: From Board 1 M4 SDA (yellow wire, 6-12" long)
  SCL: From Board 1 M4 SCL (green wire, 6-12" long)
  VDD: 5V rail
  VSS: GND rail
  VOUT A: TL072 Channel 1 input (Pin 3) - short wire
  VOUT B: TL072 Channel 2 input (Pin 5) - short wire

Position:
  - BACK edge of breadboard (near CV output jacks)
  - I2C wires run to Board 1 M4 stack
  - DAC outputs route locally to TL072 on same board
```

**TL072 Op-Amp Circuit (Dual CV Outputs):**
```
Power:
  Pin 8 (VCC+):  12V rail + 0.1µF bypass cap to GND
  Pin 4 (GND):   GND rail

Channel 1 (CV Pitch):
  Pin 3 (+IN):   MCP4728 VA (short wire, local on Board 2)
  Pin 2 (-IN):   Feedback node (R1/R2 junction)
  Pin 1 (OUT):   CV output → Panel jack TRS (tip)

Channel 2 (CV Gate):
  Pin 5 (+IN):   MCP4728 VB (short wire, local on Board 2)
  Pin 6 (-IN):   Feedback node (R3/R4 junction)
  Pin 7 (OUT):   CV output → Panel jack TRS (tip)

Resistor Network (per channel):
  R1, R3 (100kΩ): Feedback (Pin 2/6 to Pin 1/7)
  R2, R4 (100kΩ): To GND (sets 2× gain: 0-5V → 0-10V)
```

---

## Power Rail Distribution Strategy

### Four Power Rails

| Rail | Voltage | Source | Consumers |
|------|---------|--------|-----------|
| **12V** | 12V | Teyleten boost | TL072, L7805 input |
| **5V** | 5V | L7805 output | MCP4728, MIDI Wing, (M4 backup) |
| **3.3V** | 3.3V | M4 onboard regulator | OLED, I2C pullups |
| **GND** | 0V | Common ground | Everything |

### Power Rail Implementation

**On each breadboard:**
1. **Top two rails:** Power (+) and Ground (-)
2. **Bottom two rails:** Power (+) and Ground (-)
3. **Link rails** on each side with jumper wires

**Board 1 Rails:**
- Top: 5V (+), GND (-)
- Bottom: 3.3V (+), GND (-)

**Board 2 Rails:**
- Top: 12V (+), GND (-)
- Bottom: 5V (+), GND (-)

**Inter-Board Connections:**
```
Board 2 → Board 1:
  - 5V rail (L7805 output) → Board 1 5V rail (red jumper, 22 AWG)
  - GND rail → Board 1 GND rail (black jumper, 22 AWG)
```

---

## Component Mounting Strategies

### Feather Stack (M4 + OLED)

**Method 1: Header Pin Mount (Recommended)**
```
1. Solder male header pins to M4 bottom
2. Insert header pins into breadboard
3. M4 sits ~8mm above breadboard
4. Stack OLED on top via stacking headers
5. All pins accessible via breadboard rows
```

**Method 2: Standoff Mount**
```
1. Use M2.5 standoffs (10-15mm height)
2. Mount standoffs to breadboard with double-sided tape
3. Screw M4 to standoffs
4. Wire individual connections with jumpers
5. More stable, but harder to access pins
```

### MIDI FeatherWing

**Separate Mount (not stacked):**
```
Reason: Need access to LEDs for lightpipe coupling

Position:
  - 1-2" away from M4 stack
  - LEDs facing UP (accessible from above)
  - MIDI jacks facing edge of breadboard (for panel wiring)

Mount:
  - Header pins into breadboard
  - OR standoffs if using panel-mount MIDI jacks

Wiring:
  - RX → M4 TX (D1)
  - TX → M4 RX (D0)
  - VCC → 5V rail
  - GND → GND rail
```

### MCP4728 DAC

**Location: Board 2 (near CV outputs)**

**DIP Socket or Direct Mount:**
```
Option 1: IC socket in breadboard (easy removal)
Option 2: Breakout board with header pins

Connections:
  - SDA → Board 1 M4 SDA (yellow wire, 6-12" inter-board)
  - SCL → Board 1 M4 SCL (green wire, 6-12" inter-board)
  - VDD → 5V rail on Board 2 (red)
  - VSS → GND rail on Board 2 (black)
  - VOUT A → TL072 Pin 3 (blue wire, 2-3" local)
  - VOUT B → TL072 Pin 5 (blue wire, 2-3" local)

Position on Board 2:
  - BACK edge of breadboard
  - Adjacent to TL072 op-amp (short signal paths)
  - Near CV panel jack wiring points
```

### TL072 Op-Amp

**DIP-8 Package - Direct Breadboard:**
```
1. Straddle center gap of breadboard
2. All 8 pins in separate rows
3. Easy to add resistors/caps nearby
4. 0.1µF bypass cap immediately adjacent

Pin Access:
  Pin 1: CV OUT - long wire to panel jack
  Pin 2: Junction of R1/R2 (feedback network)
  Pin 3: Input from MCP4728
  Pin 4: GND rail
  Pin 8: 12V rail + bypass cap
```

### L7805 Voltage Regulator

**TO-220 Package - Three Pins:**
```
Mount Options:

1. Direct to breadboard:
   - Bend legs to fit 3 adjacent holes
   - May need to bend tab out of the way

2. Vertical mount with wires:
   - Solder short wires to each pin
   - Insert wires into breadboard
   - Secure regulator with zip-tie

Capacitors:
  - Input:  10µF electrolytic (12V side)
  - Output: 10µF electrolytic (5V side)
  - Place close to regulator pins
```

### Teyleten Boost Module

**PCB Module - Wire Connections:**
```
Mount:
  - Double-sided foam tape to breadboard edge
  - OR zip-tie through breadboard holes
  - Keep away from sensitive circuits (switching noise)

Wiring:
  IN-  (Battery -) → GND rail
  IN+  (Battery +) → Switch → Battery+
  OUT- → GND rail
  OUT+ → 12V rail

Stability:
  - Add 100µF electrolytic cap across 12V output
  - Keeps voltage stable under load
```

---

## Lightpipe Integration for MIDI LEDs

### MIDI FeatherWing LED Access

**Current LEDs:**
- MIDI IN LED (D1): Red SMD, ~3mm
- MIDI OUT LED (D2): Red SMD, ~3mm

**Lightpipe Coupling Strategy:**

```
Top View of MIDI FeatherWing:

    ┌─────────────────────┐
    │   MIDI FeatherWing  │
    │                     │
    │   ●  LED D1 (IN)    │ ← Lightpipe coupling point
    │   ●  LED D2 (OUT)   │ ← Lightpipe coupling point
    │                     │
    │   [DIN-5 Jacks]     │
    └─────────────────────┘

Lightpipe Placement:
  - Mount 3mm acrylic rods vertically
  - Position input end directly over each LED (1-2mm gap)
  - Route through case to left/right panel indicators
```

### Enclosure Lightpipe Routing

**LED to Case Exterior:**

```
Side View (Conceptual):

Interior                           Exterior
─────────────────────────────────────────────────

MIDI Wing LED ● ←─[3mm rod]─→ ● Panel Indicator
  (breadboard)    (20-30mm)      (left side)

MIDI Wing LED ● ←─[3mm rod]─→ ● Panel Indicator
  (breadboard)    (20-30mm)      (right side)
```

**Implementation:**
1. **Drill 3mm holes** in left/right case panels
2. **Position breadboard** so MIDI Wing LEDs align with holes
3. **Insert acrylic lightpipes:**
   - Input end: 2mm from LED (coupling cone if 3D printed)
   - Output end: Flush with or slightly protruding from panel
4. **Secure with friction fit** or small dab of CA glue

**Benefits:**
- No external LED wiring
- Uses existing MIDI Wing LEDs
- Clean internal layout
- Professional appearance

---

## Wire Management

### Color Coding Standard

| Color | Use |
|-------|-----|
| **Red** | Positive power (+5V, +12V, +3.3V) |
| **Black** | Ground (GND) |
| **Yellow** | I2C SDA (data) |
| **Green** | I2C SCL (clock) |
| **Blue** | Analog signals (CV, DAC outputs) |
| **Orange** | UART TX |
| **Purple** | UART RX |
| **White** | Gate/Trigger signals |
| **Brown** | Miscellaneous |

### Wire Lengths

**Power Distribution:**
- Same board: 2-3" (50-75mm)
- Between boards: 6-8" (150-200mm)

**Signal Wires:**
- I2C (SDA/SCL): 3-4" max (minimize noise)
- UART (MIDI): 3-4"
- DAC to Op-Amp: 6-12" (between boards)
- Op-Amp to Panel Jacks: 12-18" (to case)

### Cable Routing Tips

1. **Keep power separate from signals:**
   - Route 12V/5V wires along board edges
   - Route I2C/UART through center

2. **Twist pairs for noise reduction:**
   - DAC output + GND (to op-amp)
   - CV output + GND (to panel jacks)

3. **Strain relief:**
   - Tape wire bundles to breadboard edges
   - Leave slack for movement/adjustments

4. **Label wires:**
   - Use label maker or masking tape
   - Helps during troubleshooting

---

## Component Placement Checklist

### Board 1: Control Board
- [ ] M4/OLED stack mounted CENTER (header pins or standoffs)
- [ ] OLED orientation verified (faces TOP panel, visible through window)
- [ ] MIDI FeatherWing mounted CENTER-RIGHT (LEDs accessible from above)
- [ ] MIDI Wing LEDs positioned for equal-length lightpipe runs (~20-30mm LEFT/RIGHT)
- [ ] 5V power rail connected (from Board 2)
- [ ] 3.3V power rail connected from M4 3V3 pin
- [ ] GND rails linked (all four rails common ground)
- [ ] I2C wires routed to Board 2 (SDA/SCL, yellow/green, 6-12")

### Board 2: Power & Analog Board
- [ ] Teyleten boost module secured LEFT side (near power switch, 12V generation)
- [ ] L7805 regulator mounted LEFT side (12V → 5V, near boost module)
- [ ] 10µF caps on L7805 input/output (stabilization)
- [ ] 100µF filter cap on 12V rail (switching noise reduction)
- [ ] MCP4728 DAC mounted BACK edge (near CV jacks, I2C device)
- [ ] TL072 op-amp inserted BACK edge (straddles center gap, near MCP4728)
- [ ] 4× 100kΩ resistors placed (dual 2× gain networks for both channels)
- [ ] 0.1µF bypass cap near TL072 Pin 8
- [ ] 12V power rail active (check with multimeter)
- [ ] 5V power rail active (check with multimeter)
- [ ] GND rails linked (all four rails common ground)
- [ ] Inter-board 5V connection to Board 1 (red wire, LEFT side routing)

### Inter-Board Connections
- [ ] 5V rail: Board 2 → Board 1 (red wire, LEFT side routing)
- [ ] GND rail: Board 2 → Board 1 (black wire, common throughout)
- [ ] I2C SDA: Board 1 M4 → Board 2 MCP4728 (yellow wire, 6-12")
- [ ] I2C SCL: Board 1 M4 → Board 2 MCP4728 (green wire, 6-12")
- [ ] MCP4728 VA/VB outputs → TL072 inputs (local on Board 2, blue wires 2-3")
- [ ] Common ground verified with multimeter (all GND points = 0V)

### External Connections
- [ ] Battery JST → Power switch (LEFT panel) → Teyleten boost input
- [ ] TL072 Ch1 output (Pin 1) → CV jack 1 TRS tip (BACK panel, twisted pair)
- [ ] TL072 Ch2 output (Pin 7) → CV jack 2 TRS tip (BACK panel, twisted pair)
- [ ] GND → Both CV jacks sleeves (BACK panel)
- [ ] MIDI Wing positioned: LEDs accessible, equal distance to LEFT/RIGHT panels
- [ ] Lightpipe MIDI IN: LED to LEFT side panel (~20-30mm, 3mm acrylic)
- [ ] Lightpipe MIDI OUT: LED to RIGHT side panel (~20-30mm, 3mm acrylic)
- [ ] Panel-mount MIDI DIN-5 jacks wired (BACK panel, to MIDI Wing)

---

## Power-Up Sequence (Safe Testing)

### Step 1: Visual Inspection
1. Check all power connections (no shorts)
2. Verify component orientation (ICs, electrolytics)
3. Ensure common ground throughout

### Step 2: Power Rail Test (No ICs)
1. **Remove all ICs** (M4, MCP4728, TL072)
2. Connect battery to Teyleten boost
3. Measure 12V rail: Should read ~12V
4. Measure 5V rail: Should read ~5V
5. Check for excessive heat

### Step 3: Add ICs One at a Time
1. **Insert M4 first** → Check 3.3V rail (~3.3V)
2. **Insert OLED** → Display should light up
3. **Insert MCP4728** → I2C scan should detect 0x60
4. **Insert TL072** → Check 12V on Pin 8

### Step 4: Functional Test
1. **Run MCP4728 test code** → Measure DAC outputs
2. **Check TL072 gain** → 0-5V input should yield 0-10V output
3. **Test MIDI** → Send/receive MIDI messages, LEDs blink
4. **Verify lightpipes** → Light transmitted from LEDs to panel

---

## Troubleshooting Guide

### No 12V on Rail
- Check Teyleten boost connections
- Verify battery voltage (>3.5V)
- Measure boost output with multimeter

### No 5V on Rail
- Check L7805 input (should be ~12V)
- Verify L7805 orientation (pinout correct?)
- Check for excessive load (>1A)

### M4 Not Booting
- Check 5V or USB power
- Verify GND connection
- Check for shorts on power rails

### MCP4728 Not Detected
- Verify I2C wiring (SDA/SCL not swapped)
- Check 5V on MCP4728 VDD pin
- Try I2C scan in CircuitPython (should see 0x60)

### TL072 No Output
- Verify 12V on Pin 8
- Check input signal from MCP4728 (should be 0-5V)
- Verify resistor connections (100kΩ each)

### MIDI Not Working
- Check RX/TX wiring (may be swapped)
- Verify 5V power to MIDI Wing
- Test with MIDI loopback cable

---

## Next Steps

After breadboard assembly:

1. ✅ Power-up testing (follow sequence above)
2. ✅ Full functional test (run all test scripts)
3. ✅ Measure and document final wire lengths for enclosure
4. ✅ Design 3D enclosure around breadboard dimensions
5. ✅ Design lightpipe mounts for left/right MIDI indicators
6. ✅ Design panel cutouts for jacks and USB-C
7. ✅ Consider upgrading to custom PCB (future)

---

## Breadboard to Enclosure Transition

### Mounting Breadboards in Case

**Adhesive Mount:**
- Use 3M VHB double-sided tape
- Stick breadboards to enclosure floor
- Ensures stability during transport

**Screw Mount:**
- Drill holes in breadboard mounting holes
- Use M3 screws and standoffs
- Most secure method

**Modular Tray:**
- 3D print tray that fits breadboards
- Breadboards slide into tray slots
- Tray mounts to enclosure with screws

### Cable Management in Enclosure

1. **Power bundle** (red/black) - Route along back edge
2. **I2C bundle** (yellow/green) - Keep short and direct
3. **CV outputs** (blue/black) - Twisted pair to front panel jacks
4. **MIDI external** - DIN jacks to case, minimal exposed wire

---

**Document Version:** 1.0
**Last Updated:** 2025-10-31
**Status:** Ready for assembly
