# PRISME Enclosure & Hardware - Complete Rebuild Plan

## Design Reference
Based on hand-drawn sketch dated 2025-11-02

---

## 1. BACK PANEL LAYOUT (Definitive)

### TOP ROW - INPUT BOARD JACKS (2 jacks + 2 LEDs)
```
CV IN  ○        TRIG IN  ○
  ●                ●
```
- **CV IN:** 1/8" mono jack, 6mm hole
- **TRIG IN:** 1/8" mono jack, 6mm hole
- **Activity LEDs:** 3mm white LEDs, 3mm holes, 7mm right of each jack
- **Spacing:** 12mm jack center-to-center
- **Position:** Center-left of back panel

### BOTTOM ROW - OUTPUT BOARD JACKS (6 jacks + 5 LEDs)
```
USB-C    CV OUT ○   TRIG OUT ○   CC OUT ○      MIDI OUT ○   MIDI IN ○
 ▭         ●            ●           ●              ◯             ◯
```
- **USB-C:** Panel mount, 9.5mm × 3.8mm rectangular cutout (no LED)
- **CV OUT:** 1/8" mono jack, 6mm hole + 3mm LED
- **TRIG OUT:** 1/8" mono jack, 6mm hole + 3mm LED
- **CC OUT:** 1/8" mono jack, 6mm hole + 3mm LED
- **MIDI OUT:** 5-pin DIN, 15.5mm hole + 3mm LED
- **MIDI IN:** 5-pin DIN, 15.5mm hole + 3mm LED
- **Activity LEDs:** 3mm white LEDs, 3mm holes, 7mm right of each jack

**Spacing:**
- 1/8" jacks: 12mm center-to-center
- MIDI jacks: 20mm center-to-center (standard MIDI spacing)
- LEDs: 7mm offset right from jack center

**Total indicators:** 7 activity LEDs (white, 3mm clear)

---

## 2. PROTOBOARD SPECIFICATIONS

### Stock Material
- **Source:** ElectroCookie protoboards
- **Stock size:** 97mm × 89mm
- **Features:** Power rails, 0.1" grid, through-hole pads
- **Cut to size:** Custom dimensions to fit enclosure

### OUTPUT BOARD (Bottom Protoboard)

**Custom Size:** 90mm × 55mm (cut from stock)

**Rear Edge Layout (left to right):**
```
Position (mm from left):
10mm:  USB-C panel mount breakout
25mm:  CV OUT jack
37mm:  TRIG OUT jack
49mm:  CC OUT jack
70mm:  MIDI OUT jack (from FeatherWing)
85mm:  MIDI IN jack (from FeatherWing)
```

**Component Placement Map:**
```
REAR EDGE (back panel):
═══════════════════════════════════════════════════════
  10mm    25mm    37mm    49mm        70mm    85mm
   ↓       ↓       ↓       ↓            ↓       ↓
[USB-C] [CV OUT][TRIG][CC OUT]    [MIDI OUT][MIDI IN]
═══════════════════════════════════════════════════════

COMPONENT AREA:

  [USB-C Breakout Board]  [47µF][0.1µF]  ← Power caps (left)
       │                     │     │
       │                     └─────┴──→ 5V rail
       └──→ To Feather USB

  ┌────────────────────────┐              [0.1µF] ← DAC decoupling
  │   MCP4728 DAC MODULE   │              [0.1µF]
  │   4-CH 12-bit I2C      │
  │   M2.5 standoffs       │
  │                        │
  │  CH_A  CH_B  CH_C  CH_D│
  └───┼────┼────┼────┼─────┘
      │    │    │    │
      │    │    │    └─[R4][C4]──→ (future expansion)
      │    │    │       100Ω 100nF
      │    │    │
      │    │    └─[R3][C3]──→ CC OUT jack
      │    │       100Ω 100nF
      │    │
      │    └─[R2]──────────→ TRIG OUT jack (no cap - fast edges)
      │       100Ω
      │
      └─[R1][C1]──────────→ CV OUT jack
         100Ω 100nF

  S-TRIG CIRCUIT (shares TRIG OUT jack):
    [D10 from Feather] ──[R5]──→ NPN (2N3904)
                          1kΩ      │
                              COLL─┼─[R6]──→ TRIG OUT jack
                                   │  100Ω
                               EMIT─┴──→ GND

  ┌─────────────────────────────────────┐
  │     MIDI FEATHERWING                │
  │     (Horizontal orientation)        │
  │                                     │
  │   [MIDI OUT]              [MIDI IN] │ ← Jacks align with rear edge
  └──────────────────────────────────────┘
       Stack on Feather via headers
       Position: Right side of board

  ACTIVITY LED CIRCUITS (5 LEDs on OUTPUT board):
    [D12] ──[150Ω]──→ LED1 (CV OUT) ──→ GND
    [A0]  ──[150Ω]──→ LED2 (TRIG OUT) ──→ GND
    [A1]  ──[150Ω]──→ LED3 (CC OUT) ──→ GND
    [A2]  ──[150Ω]──→ LED4 (MIDI OUT) ──→ GND
    [A5]  ──[150Ω]──→ LED5 (MIDI IN) ──→ GND

    LEDs: 3mm white, clear lens
    Position: 7mm right of each jack
    Each LED passes through back panel hole

  CONNECTIONS TO FEATHER:
    [SDA][SCL][5V][GND][D10][D12][A0][A1][A2][A5] ← Header to Feather stack
```

**Bill of Materials - OUTPUT BOARD:**
| Qty | Component | Value/Part | Purpose |
|-----|-----------|------------|---------|
| 1 | MCP4728 Module | I2C DAC | 4-channel CV output |
| 1 | MIDI FeatherWing | Adafruit #2063 | MIDI I/O |
| 1 | USB-C Breakout | Panel mount | Power/programming |
| 1 | Electrolytic Cap | 47µF 16V | Bulk power |
| 4 | Ceramic Cap | 0.1µF 50V | Bypass/decoupling |
| 4 | Ceramic Cap | 100nF 50V | Output smoothing (3 used, 1 spare) |
| 4 | Resistor | 100Ω 1/4W | Output protection |
| 1 | Resistor | 1kΩ 1/4W | NPN base |
| 5 | Resistor | 150Ω 1/4W | LED current limiting |
| 1 | NPN Transistor | 2N3904 | S-Trig switching |
| 3 | 1/8" mono jack | 3.5mm panel | CV/TRIG/CC outputs |
| 5 | LED | 3mm white clear | Activity indicators |
| 1 | 10-pin header | Male 0.1" | To Feather stack (expanded for LEDs) |
| 4 | M2.5 standoffs | 10mm | MCP4728 mounting |

### INPUT BOARD (Top Protoboard)

**Custom Size:** 90mm × 55mm (cut from stock)

**Rear Edge Layout (left to right):**
```
Position (mm from left):
25mm:  CV IN jack
37mm:  TRIG IN jack
```

**Component Placement Map:**
```
REAR EDGE (back panel):
═══════════════════════════════════════════════════════
       25mm    37mm
        ↓       ↓
      [CV IN][TRIG IN]
═══════════════════════════════════════════════════════

COMPONENT AREA:

  [47µF][0.1µF]  ← Power caps
    │     │
    └─────┴──→ 5V rail (from OUTPUT board)

  CV INPUT PROTECTION CIRCUIT (A3):
    [CV IN JACK] ──┬──[R1]──[R2]──┬────── GND
                   │   10kΩ  10kΩ  │
                  GND              │
                                   ├──[R3]──[C3]──[D1]──→ A3 to Feather
                                   │   10kΩ  100nF BAT85
                                   │          │      │
                                   └──[R4]────┤      └──→ 3.3V rail (clamp)
                                      22kΩ    │
                                             GND

  TRIG INPUT PROTECTION CIRCUIT (A4):
    [TRIG IN JACK]─┬──[R5]──[R6]──┬────── GND
                   │   10kΩ  10kΩ  │
                  GND              │
                                   ├──[R7]──[C7]──[D2]──→ A4 to Feather
                                   │   10kΩ  100nF BAT85
                                   │          │      │
                                   └──[R8]────┤      └──→ 3.3V rail (clamp)
                                      22kΩ    │
                                             GND

  ACTIVITY LED CIRCUITS (2 LEDs on INPUT board):
    [D4]  ──[150Ω]──→ LED6 (CV IN) ──→ GND
    [D11] ──[150Ω]──→ LED7 (TRIG IN) ──→ GND

    LEDs: 3mm white, clear lens
    Position: 7mm right of each jack
    Each LED passes through back panel hole

  CONNECTIONS TO FEATHER:
    [A3][A4][3.3V][GND][D4][D11] ← Header to Feather stack
```

**Bill of Materials - INPUT BOARD:**
| Qty | Component | Value/Part | Purpose |
|-----|-----------|------------|---------|
| 1 | Electrolytic Cap | 47µF 16V | Bulk power |
| 1 | Ceramic Cap | 0.1µF 50V | High-freq bypass |
| 2 | Ceramic Cap | 100nF 50V | Input filtering |
| 4 | Resistor | 10kΩ 1/4W | Voltage divider (series) |
| 2 | Resistor | 22kΩ 1/4W | Voltage divider (to GND) |
| 2 | Resistor | 10kΩ 1/4W | Series protection |
| 2 | Resistor | 150Ω 1/4W | LED current limiting |
| 2 | Schottky Diode | BAT85 | Overvoltage clamp |
| 2 | 1/8" mono jack | 3.5mm panel | CV/TRIG inputs |
| 2 | LED | 3mm white clear | Activity indicators |
| 1 | 6-pin header | Male 0.1" | To Feather stack (expanded for LEDs) |

---

## 3. ENCLOSURE DESIGN

### Internal Dimensions
- **Width:** 95mm (accommodates MIDI FeatherWing + margins)
- **Depth:** 65mm (50mm boards + 15mm battery space)
- **Height:** 60mm (two jack rows + labels + clearance)

### Wall Specifications
- **Side walls:** 3.5mm
- **Base:** 4mm
- **Top:** 2.5mm
- **Corner radius:** 2mm

### External Dimensions (calculated)
- **Width:** 102mm
- **Depth:** 72mm
- **Total height:** 66.5mm (box + lid)

### Back Panel Jack Positions

**Jack Heights (Y from base):**
- **Top row:** 45mm
- **Bottom row:** 20mm
- **Row spacing:** 25mm

**Jack X-positions (from left edge, including wall offset):**

*Calculations (left edge = 3.5mm wall + margin):*

**TOP ROW:**
- CV IN: 28.5mm
- TRIG IN: 40.5mm

**BOTTOM ROW:**
- USB-C: 13.5mm (left edge)
- CV OUT: 28.5mm (aligned with CV IN)
- TRIG OUT: 40.5mm (aligned with TRIG IN)
- CC OUT: 52.5mm
- MIDI OUT: 73.5mm
- MIDI IN: 88.5mm (near right edge)

### Top Panel Features
- **OLED cutout:** 30mm × 16mm at (10mm, 20mm) from front-left
- **Button holes:** 3× 6.5mm diameter at (48mm, 20mm/31mm/42mm)
- **Screw holes:** 4× M3 countersunk at corners

### Ventilation
- **Side walls:** 4× slots per side
- **Slot dimensions:** 1.5mm × 20mm
- **Spacing:** 10mm between slots

---

## 4. COMPONENT STACK & SPACING

### Vertical Stack (base to top):
```
SIDE VIEW:

    ┌──────────────────────┐
    │   OLED FeatherWing   │  ← Top panel buttons/display align
    ├──────────────────────┤
    │   Feather M4 Express │
    │   (with battery JST) │
    └──────────────────────┘
            ↕ 15mm standoffs
    ┌──────────────────────┐
    │   INPUT BOARD        │  ← CV IN, TRIG IN jacks (rear)
    └──────────────────────┘
            ↕ 10mm standoffs (M3 metal)
    ┌──────────────────────┐
    │   OUTPUT BOARD       │  ← 6 jacks on rear edge
    │   (with MIDI wing)   │
    └──────────────────────┘
            ↕ 10mm standoffs to base
    ═══════════════════════
         Enclosure Base
         (battery underneath)
```

### Battery Placement
- **Component:** 1200mAh 3.7V LiPo
- **Dimensions:** 37mm × 52mm × 7mm
- **Location:** Under OUTPUT board, front section
- **Clearance:** 8mm space (7mm battery + 1mm clearance)
- **Connection:** JST connector to Feather M4

---

## 5. LABELS

### Back Panel Labels (Debossed)
- **Font:** Helvetica Bold
- **Size:** 2.5mm
- **Depth:** 0.8mm (recessed into surface)

**TOP ROW (above jacks):**
- "CV IN" (above CV IN jack)
- "TRIG IN" (above TRIG IN jack)

**BOTTOM ROW (below jacks):**
- "USB-C" (below USB-C)
- "CV OUT" (below CV OUT)
- "TRIG OUT" (below TRIG OUT)
- "CC OUT" (below CC OUT)
- "MIDI OUT" (below MIDI OUT)
- "MIDI IN" (below MIDI IN)

---

## 6. WIRING & CONNECTIONS

### Power Distribution
```
USB-C (5V) ──→ Feather M4 USB
                   │
                   ├──→ LiPo charger (internal)
                   │
                   └──→ 5V out to boards
                         │
                         ├──→ OUTPUT board 5V rail
                         │     ├──→ MCP4728
                         │     └──→ MIDI FeatherWing
                         │
                         └──→ INPUT board 5V rail

Feather 3.3V ──→ INPUT board (for clamp diodes)
```

### I2C Bus
```
Feather SDA/SCL ──→ MCP4728 (OUTPUT board)
                 └──→ (future I2C devices)
```

### Analog Inputs
```
INPUT board A3 ──→ Feather A3 (CV IN)
INPUT board A4 ──→ Feather A4 (TRIG IN)
```

### Digital Outputs
```
Feather D10 ──→ S-Trig circuit (OUTPUT board)
```

### MIDI
```
Feather TX/RX ──→ MIDI FeatherWing (via stacking headers)
```

### Activity LED Control

**GPIO Pin Allocation for LEDs:**

| Jack | LED Pin | Detection Logic | Software Implementation |
|------|---------|-----------------|-------------------------|
| CV IN | D4 | Monitor A3 ADC | LED on when voltage > 0.1V |
| TRIG IN | D11 | Monitor A4 ADC | LED on when gate HIGH (>2V) |
| CV OUT | D12 | Software controlled | LED on when DAC Ch A outputting |
| TRIG OUT | A0 | Software controlled | LED on when DAC Ch C or D10 active |
| CC OUT | A1 | Software controlled | LED on when DAC Ch B outputting |
| MIDI OUT | A2 | Monitor UART TX | LED pulse on TX activity |
| MIDI IN | A5 | Monitor UART RX | LED pulse on RX activity |

**Detection Methods:**

1. **Input Monitoring (CV IN, TRIG IN):**
   - Periodic ADC reads (100Hz sampling)
   - Threshold detection
   - LED on while signal present

2. **Output Status (CV OUT, TRIG OUT, CC OUT):**
   - Software-controlled based on internal state
   - LED mirrors output activity directly

3. **MIDI Activity (MIDI IN, MIDI OUT):**
   - Monitor UART buffer activity
   - LED pulse (50-100ms) on message detection
   - Debounce to prevent flickering

**Power Consumption:**
- 7 LEDs × 20mA = 140mA max (all LEDs on)
- Typical usage: 2-3 LEDs active = 40-60mA
- Well within Feather M4's capabilities

---

## 7. ASSEMBLY ORDER

1. **Cut protoboards** to size (90mm × 55mm each)
2. **OUTPUT board assembly:**
   - Solder power rails and distribution
   - Mount MCP4728 module on standoffs
   - Install output protection circuits
   - Install S-Trig circuit
   - Solder MIDI FeatherWing stacking headers
   - Mount USB-C breakout
   - Solder 3× output jacks to rear edge
   - Stack MIDI FeatherWing (jacks align with rear edge)
3. **INPUT board assembly:**
   - Solder power rails
   - Install input protection circuits
   - Solder 2× input jacks to rear edge
4. **Enclosure preparation:**
   - 3D print box and lid
   - Test fit all boards
5. **Stack assembly:**
   - Mount OUTPUT board to enclosure base (10mm standoffs)
   - Mount INPUT board on OUTPUT board (10mm M3 metal standoffs)
   - Mount Feather stack on INPUT board (15mm standoffs)
6. **Wiring:**
   - Connect USB-C to Feather
   - Connect battery to Feather
   - Wire inter-board headers (power, I2C, analog, digital)
7. **Testing:**
   - Power-on test
   - I2C device scan
   - Input voltage scaling test
   - Output voltage test
   - MIDI loopback test
8. **Final assembly:**
   - Secure battery with double-sided tape
   - Route cables neatly
   - Install lid with M3 screws

---

## 8. IMPLEMENTATION STEPS

### Step 1: Update OpenSCAD File
- Set correct internal dimensions (95 × 65 × 60mm)
- Define all 8 jack positions (2 top, 6 bottom)
- **Add 7 LED holes (3mm diameter, 7mm right of each jack)**
- Add proper labels for all jacks
- Ensure USB-C rectangular cutout
- Verify MIDI jack spacing

### Step 2: Rewrite PROTOBOARD_LAYOUT.md
- Document 90mm × 55mm custom board size
- Complete OUTPUT board layout with MIDI FeatherWing + **5 LEDs**
- Complete INPUT board layout + **2 LEDs**
- Include battery specifications and placement
- Update all BOMs with LEDs and resistors

### Step 3: Update JACK_WIRING_GUIDE.md
- Document all 8 jacks with correct positions
- **Document 7 LED indicators with positions**
- Wire color assignments
- Connection diagrams

### Step 4: Update PIN_ALLOCATION_MATRIX.md
- **Allocate 7 GPIO pins for LEDs (D4, D11, D12, A0, A1, A2, A5)**
- Mark pins as "In Use" for LED control
- Document detection logic for each LED

### Step 5: Generate Preview Renders
- Full assembly view
- Back panel detail view
- Top panel view
- Verify all jack positions match sketch

---

## QUESTIONS TO RESOLVE

1. **Exact protoboard cut dimensions?** Proposed 90mm × 55mm - confirm this fits all components
2. **Battery exact placement?** Front section under OUTPUT board - any preference?
3. **USB-C breakout specific model?** Need part number for exact mounting holes
4. **Jack spacing refinement?** Proposed positions - verify they're comfortable for patching

## ✅ CONFIRMED ADDITIONS

**Activity LED System (Added 2025-11-02):**
- 7× 3mm white clear LEDs (ordered)
- 7× 150Ω current limiting resistors
- 7 GPIO pins allocated (D4, D11, D12, A0, A1, A2, A5)
- 3mm holes positioned 7mm right of each jack
- Simple on/off activity indication
- Detection logic defined for inputs, outputs, and MIDI

---

**Status:** PLAN COMPLETE WITH LED SYSTEM - AWAITING APPROVAL BEFORE IMPLEMENTATION
