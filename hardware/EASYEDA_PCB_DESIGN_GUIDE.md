# EasyEDA PCB Design Guide - PRISME Hardware

**Date:** 2025-11-04 (Session 27 - Power System Simplified)
**Purpose:** Complete reference for designing custom PCBs in EasyEDA
**Schematics:** TOP_BOARD_FINAL.svg + BOTTOM_BOARD_FINAL.svg + POWER_DISTRIBUTION.svg

---

## ⚠️ MAJOR CHANGE (Session 27): Power System Simplified

**Removed:** LiPo battery, Powerboost module, power switch, JST connectors
**Now:** **USB-C power only** - much simpler design!

---

## 📋 QUICK START

### Schematics Location:
**All current schematics:** `hardware/enclosure/CURRENT_SCHEMATICS/`

**Production-ready schematics (7 total):**
1. **`UNIFIED_SYSTEM_SCHEMATIC_V2.svg`** - Complete system overview
2. **`M4_PIN_ASSIGNMENTS.svg`** - Pin reference table
3. **`TOP_PCB_CV_IN.svg`** - CV input circuit
4. **`TOP_PCB_TRIG_IN.svg`** - TRIG input circuit
5. **`BOTTOM_PCB_DAC_OUTPUTS.svg`** - DAC output circuits
6. **`BOTTOM_PCB_STRIG.svg`** - S-Trig transistor circuit
7. **`POWER_DISTRIBUTION.svg`** - USB-only power system

See `CURRENT_SCHEMATICS/README.md` for detailed descriptions.

### Board Specifications:
- **Size:** 90mm × 55mm each (custom-cut ElectroCookie size)
- **Boards:** 2× stacked vertically with 10mm standoffs
- **Main Controller:** Feather M4 CAN Express (stacks on top)
- **Power:** **USB-C 5V input only** (no battery!), 3.3V from M4 onboard regulator

---

## 🔧 COMPLETE BILL OF MATERIALS (BOM)

**Power System Note:** This BOM reflects the **simplified USB-only design** (Session 27).
No battery, powerboost, JST connectors, or power switch needed!

### Main Boards & Modules:
| Qty | Component | Description | Supplier | Part# | Notes |
|-----|-----------|-------------|----------|-------|-------|
| 1 | Feather M4 CAN Express | Main MCU | Adafruit | 4759 | ATSAMD51J19 |
| 1 | MIDI FeatherWing | MIDI I/O | Adafruit | 4740 | UART-based |
| 1 | OLED FeatherWing | 128×64 display | Adafruit | 4650 | I2C 0x3C |
| 1 | MCP4728 | 4-ch 12-bit DAC | Adafruit | 4470 | I2C 0x60 |

### Semiconductors:
| Qty | Component | Description | Package | Supplier | Part# |
|-----|-----------|-------------|---------|----------|-------|
| 2 | BAT85 | Schottky diode 30V 200mA | DO-35 | Amazon | [ALLECIN 100pcs](https://www.amazon.com/ALLECIN-BAT85-Schottky-Rectifier-Switching/dp/B0CKSNPVH8/) |
| 1 | 2N3904 | NPN transistor | TO-92 | Any | Generic |
| 7 | White LED | 3mm status LED | 3mm | Any | Generic | All indicators simplified to white |

### Resistors (1/4W, 5% or 1%):
| Qty | Value | Purpose | Designators |
|-----|-------|---------|-------------|
| 4 | 10kΩ | Input voltage dividers | R1, R2, R4, R5 |
| 5 | 100Ω | Output series protection | R_OUT1-4, R_STRIG |
| 1 | 1kΩ | Transistor base (S-Trig) | R_BASE |
| 7 | **220Ω** | **LED current limiting (all white LEDs)** | **R_LED1-7** |

### Capacitors:
| Qty | Value | Type | Voltage | Purpose | Designators |
|-----|-------|------|---------|---------|-------------|
| 1 | 47µF | Electrolytic | 16V+ | 5V bulk (bottom) | C1 |
| 1 | 0.1µF | Ceramic X7R | 50V | 5V bypass (bottom) | C2 |
| 1 | 10µF | Electrolytic | 16V+ | 3.3V bulk (bottom) | C9 |
| 1 | 0.1µF | Ceramic X7R | 50V | 3.3V bypass (bottom) | C10 |
| 1 | 10µF | Electrolytic | 16V+ | 5V bulk (top) | C11 |
| 1 | 0.1µF | Ceramic X7R | 50V | 5V bypass (top) | C12 |
| 1 | 10µF | Electrolytic | 16V+ | 3.3V bulk (top) | C13 |
| 1 | 0.1µF | Ceramic X7R | 50V | 3.3V bypass (top) | C14 |
| 2 | 100nF | Ceramic X7R | 50V | ADC smoothing (optional) | C15, C16 |

### Connectors:
| Qty | Type | Purpose | Notes |
|-----|------|---------|-------|
| 6-7 | 3.5mm TS Jack | CV/TRIG I/O | PJ-324M or equivalent |
| 1 | USB-C Breakout | Power input | Adafruit 4090 |
| 2 | DIN-5 (180°) | MIDI I/O | On MIDI FeatherWing |
| 1 | Stacking headers | Feather connection | Female headers |

### Hardware:
| Qty | Part | Size | Purpose |
|-----|------|------|---------|
| 8 | M3 standoff | 10mm | Board spacing |
| 16 | M3 screw | 6mm | Mount boards |
| 4 | M3 nut | Standard | Bottom mounting |

---

## 🔌 FEATHER M4 PIN CONNECTIONS (CRITICAL!)

### All Connections Between M4 and PCBs:

This table shows EVERY connection you need to make on your PCBs. Each PCB connection point must have a header pin or wire pad to connect to the M4.

#### Power Connections:
| M4 Pin | Signal | Goes To | PCB Board | Notes |
|--------|--------|---------|-----------|-------|
| USB | 5V | 5V Rail | Both boards | Powers MCP4728 DAC |
| 3V3 | 3.3V | 3.3V Rail | Both boards | Powers MIDI, OLED, LEDs, BAT85 clamps |
| GND | Ground | Common GND | Both boards | Multiple GND pins available |

#### I2C Bus (Shared):
| M4 Pin | Signal | Goes To | Device Address | PCB Board |
|--------|--------|---------|----------------|-----------|
| SDA | I2C Data | OLED Wing | 0x3C | Pre-built (stacked) |
| SDA | I2C Data | MCP4728 DAC | 0x60 | Bottom PCB |
| SCL | I2C Clock | OLED Wing | 0x3C | Pre-built (stacked) |
| SCL | I2C Clock | MCP4728 DAC | 0x60 | Bottom PCB |

#### UART (MIDI):
| M4 Pin | Signal | Goes To | PCB Board | Notes |
|--------|--------|---------|-----------|-------|
| RX | Serial RX | MIDI Wing RX | Pre-built (stacked) | MIDI IN data |
| TX | Serial TX | MIDI Wing TX | Pre-built (stacked) | MIDI OUT data |

#### ADC Inputs (Input PCB):
| M4 Pin | Signal | Comes From | PCB Board | Notes |
|--------|--------|------------|-----------|-------|
| A3 | ADC Input | CV IN voltage divider TAP | Top PCB | 0-3.3V from 0-5V input |
| A4 | ADC Input | TRIG IN voltage divider TAP | Top PCB | 0-3.3V from 0-5V input |

#### GPIO Outputs (LEDs):
| M4 Pin | Signal | Goes To | PCB Board | Current Limit |
|--------|--------|---------|-----------|---------------|
| D4 | GPIO Out | CV IN LED (white) | Top PCB | 220Ω resistor |
| D10 | GPIO Out | S-Trig transistor base | Bottom PCB | 1kΩ resistor |
| D11 | GPIO Out | TRIG IN LED R (RGB) | Top PCB | 220Ω resistor |
| D23 | GPIO Out | TRIG IN LED G (RGB) | Top PCB | 220Ω resistor |
| D24 | GPIO Out | TRIG IN LED B (RGB) | Top PCB | 220Ω resistor |

### How to Connect in EasyEDA:

1. **On each PCB schematic**, add connection points (test pads or headers) labeled:
   - `M4_A3`, `M4_A4` (top board ADC inputs)
   - `M4_SDA`, `M4_SCL` (bottom board I2C)
   - `M4_D4`, `M4_D10`, `M4_D11`, `M4_D23`, `M4_D24` (GPIO outputs)
   - `M4_5V`, `M4_3V3`, `M4_GND` (power on both boards)

2. **These are OFF-BOARD connections** - they won't route to other components on the PCB itself

3. **In the physical build**, you'll connect these PCB pads to M4 pins using:
   - Stacking headers (if PCBs mount directly)
   - Wire jumpers (if PCBs are separate)

---

## 📐 TOP BOARD (Input) - Detailed Schematic

### Purpose:
- CV IN and TRIG IN protection circuits
- Input LEDs
- Power rail decoupling for top section
- **Connection points to M4 pins: A3, A4, D4, D11, D23, D24, 5V, 3V3, GND**

### Circuits:

#### CV IN (Jack → A3):
```
CV IN Jack TIP
    ↓
  R1 (10kΩ) ────→ Voltage divider upper
    ↓
  [TAP POINT]
    ├─→ To M4 Pin A3 (ADC input)
    ├─→ D1 BAT85 anode (protection diode)
    │    ↓ (cathode)
    │   3.3V Rail
    └─→ C15 (100nF optional smoothing)
        ↓
       GND
    ↓
  R2 (10kΩ) ────→ Voltage divider lower
    ↓
   GND

CV IN Jack SLEEVE → GND
```

**Protection Analysis:**
- Without D1: Safe up to 6.6V input (60%)
- With D1 (BAT85): Safe up to 40V+ input (100%)
- Voltage division: 5V → 2.5V
- Diode clamp: Max 3.7V to ADC

#### TRIG IN (Jack → A4):
```
TRIG IN Jack TIP
    ↓
  R4 (10kΩ)
    ↓
  [TAP POINT]
    ├─→ To M4 Pin A4
    ├─→ D2 BAT85 anode
    │    ↓ (cathode)
    │   3.3V Rail
    └─→ C16 (100nF optional)
        ↓
       GND
    ↓
  R5 (10kΩ)
    ↓
   GND

TRIG IN Jack SLEEVE → GND
```

#### Input LEDs:
```
CV IN LED:
  M4 Pin D4 → R3 (220Ω) → LED1 (White) → GND

TRIG IN RGB LED:
  M4 Pin D11 → R6 (220Ω) → LED2 Red → GND
  M4 Pin D23 → (220Ω) → LED2 Green → GND
  M4 Pin D24 → (220Ω) → LED2 Blue → GND
```

#### Power Decoupling (Top Board):
```
5V Rail:
  From M4 USB → C11 (10µF bulk) → C12 (0.1µF bypass) → To LEDs if needed

3.3V Rail:
  From M4 3V3 → C13 (10µF bulk) → C14 (0.1µF bypass) → To LEDs, BAT85 reference
```

---

## 📐 BOTTOM BOARD (Output) - Detailed Schematic

### Purpose:
- CV, TRIG, CC outputs via MCP4728 DAC
- S-Trig transistor circuit
- Power distribution and decoupling
- USB-C power input
- MIDI FeatherWing connections
- **Connection points to M4 pins: SDA, SCL, D10, 5V, 3V3, GND**

### Circuits:

#### Power Distribution:
```
USB-C 5V Input
    ↓
  M4 USB Pin
    ↓
  C1 (47µF bulk) + C2 (0.1µF bypass)
    ↓
  MCP4728 VDD (DAC power, needs 5V for 0-5V output)

M4 3V3 Output
    ↓
  C9 (10µF bulk) + C10 (0.1µF bypass)
    ↓
  MIDI FeatherWing + OLED FeatherWing + LEDs
```

**CRITICAL:** Both rails must have proper decoupling!
- 5V: Bulk + bypass near DAC
- 3.3V: Bulk + bypass near MIDI/OLED

#### MCP4728 Connections:
```
I2C Bus:
  M4 SDA (D21) → MCP4728 SDA
  M4 SCL (D22) → MCP4728 SCL

Power:
  5V → MCP4728 VDD
  GND → MCP4728 GND

I2C Address: 0x60 (factory default)
```

#### CV OUT (Channel A - 0-5V Direct):
```
MCP4728 VA Pin
    ↓
  R1 (100Ω) ────→ Short-circuit protection
    ↓
  CV OUT Jack TIP
    │
   Jack SLEEVE → GND

LED Indicator:
  CV OUT → R7 (220Ω) → LED3 (White) → GND
  (Driven by M4 Pin D12)
```

**Output Specs:**
- Range: 0-5V (5 octaves)
- Standard: 1V/octave Eurorack
- Resolution: 12-bit (4096 steps)
- MIDI mapping: Note 0 = 0V, Note 60 = 5V

**Note:** MCP4728 Channel B (VB pin) is **unused/floating** and reserved for future expansion.

#### TRIG OUT - V-Trig Mode (Channel C):
```
MCP4728 VC Pin
    ↓
  R2 (100Ω)
    ↓
  TRIG OUT Jack TIP
    │
   Jack SLEEVE → GND
```

**Output Specs:**
- Range: 0-5V gate
- Logic: 0V = off, 5V = on
- Rise/fall time: <1µs (DAC limited)

#### TRIG OUT - S-Trig Mode (GPIO D10 via Transistor):
```
M4 Pin D10
    ↓
  R8 (1kΩ) ────→ Base current limit
    ↓
  Q1 (2N3904) Base
    │
   Collector → R9 (100Ω) → TRIG OUT Jack TIP (same jack as V-Trig)
    │
   Emitter → GND

Jack SLEEVE → GND
```

**Operation:**
- D10 LOW (0V): Transistor OFF, jack open (idle)
- D10 HIGH (3.3V): Transistor ON, jack shorted to GND (trigger)
- Compatible with: ARP, Korg MS-20, Yamaha CS, etc.

**RGB LED Indicator:**
```
  M4 Pin A0 → R10 (220Ω) → LED4 Red → GND
  M4 Pin A1 → (220Ω) → LED4 Green → GND
  M4 Pin A2 → (220Ω) → LED4 Blue → GND
```

#### CC OUT (Channel D - MIDI CC to Voltage):
```
MCP4728 VD Pin
    ↓
  R3 (100Ω)
    ↓
  CC OUT Jack TIP
    │
   Jack SLEEVE → GND

LED Indicator:
  CC OUT → R11 (220Ω) → LED5 (White) → GND
```

**Output Specs:**
- Range: 0-5V
- Mapping: CC value 0-127 → 0-5V
- Use: Mod wheel, expression, aftertouch, etc.

#### Channel D (Future Expansion):
```
MCP4728 VD Pin
    ↓
  R4 (100Ω) ────→ Footprint for future
    ↓
  [Unpopulated jack]
```

**Reserved for:**
- Additional CV output
- Velocity CV
- Aftertouch CV
- Custom mod source

---

## 🔌 CONNECTOR PINOUTS

### 3.5mm TS Jacks (All I/O):
```
TIP (switched): Signal
SLEEVE: GND

When cable inserted: TIP contact closes
```

### USB-C Breakout (Power Input):
```
VBUS: 5V to M4 USB pin
GND: Common ground
D+/D-: Not used (M4 has own USB for programming)
```

### Feather Stacking Headers:
```
All M4 pins pass through to FeatherWings:
- USB, 3V3, GND (power distribution)
- SDA, SCL (I2C bus for DAC + OLED)
- RX, TX (UART for MIDI)
- All GPIO pins available
```

---

## 📏 PCB LAYOUT GUIDELINES

### Board Stack (Bottom to Top):
```
1. BOTTOM BOARD (90mm × 55mm)
   - MCP4728 DAC (center-left)
   - Output jacks (rear edge)
   - USB-C breakout (rear edge)
   - 2N3904 transistor (near TRIG OUT)
   - Power decoupling caps (near DAC and edges)

2. INPUT BOARD (90mm × 55mm)
   - Input jacks (rear edge)
   - Voltage dividers (near jacks)
   - BAT85 diodes (near ADC connection points)
   - LED indicators (front edge)

3. FEATHER M4 STACK
   - Feather M4 CAN Express
   - MIDI FeatherWing
   - OLED FeatherWing (top)
```

### Spacing:
- Bottom to input board: 10mm standoffs
- Input to Feather stack: 15mm clearance (wire routing)
- Total stack height: ~35mm

### Rear Panel Jack Layout:
```
TOP ROW (Input Board):
  [CV IN]    [TRIG IN]
   20mm       32mm from left edge

BOTTOM ROW (Output Board):
  [USB-C]  [CV OUT]  [TRIG OUT]  [CC OUT]  [MIDI OUT]  [MIDI IN]
   8mm      20mm      32mm        44mm      65mm        85mm from left edge
```

### Trace Width Recommendations:
- **Power rails (5V, 3.3V):** 20-30 mil (0.5-0.75mm)
- **Ground:** Pour/fill preferred, or 30+ mil
- **Signal traces:** 10-15 mil (0.25-0.4mm)
- **I2C (SDA, SCL):** 10-15 mil, keep <100mm
- **High current (USB):** 30+ mil

### Ground Plane:
- **Use ground pour on both layers**
- Connect with vias (every 20-30mm)
- Star ground at USB-C input
- Keep analog (DAC) and digital (I2C) grounds separate initially, join at single point

### Decoupling Cap Placement:
- **As close as possible** to IC power pins (<5mm)
- Bulk cap (10µF/47µF): Within 10mm
- Bypass cap (0.1µF): Within 2-3mm
- Via to ground plane directly from cap

---

## 🎨 EASYEDA DESIGN CHECKLIST

### Schematic Phase:
- [ ] Import reference schematics (TOP_BOARD_FINAL.svg, BOTTOM_BOARD_FINAL.svg)
- [ ] Create schematic for each board
- [ ] Assign footprints to all components
- [ ] Run electrical rule check (ERC)
- [ ] Verify I2C addresses (OLED 0x3C, DAC 0x60)
- [ ] Check all pin connections to M4

### PCB Layout Phase:
- [ ] Set board dimensions: 90mm × 55mm
- [ ] Place connectors on rear edge first (per layout above)
- [ ] Place ICs (MCP4728, 2N3904)
- [ ] Place decoupling caps near ICs
- [ ] Route power rails first (thick traces)
- [ ] Route I2C bus (keep traces short)
- [ ] Route signals
- [ ] Add ground pour (top and bottom)
- [ ] Run design rule check (DRC)
- [ ] Verify clearances (minimum 8 mil / 0.2mm)

### Manufacturing Prep:
- [ ] Add mounting holes (M3, 3.2mm drill, 6mm pad)
- [ ] Add silkscreen labels for all jacks
- [ ] Add polarity markers for diodes, LEDs, electrolytics
- [ ] Add version number and date
- [ ] Generate Gerber files
- [ ] Check Gerber in viewer
- [ ] Order boards!

---

## 🔍 COMPONENT FOOTPRINTS (EasyEDA)

### Resistors & Capacitors:
- **Through-hole resistors:** AXIAL-0.4 (1/4W)
- **Ceramic caps (0.1µF, 100nF):** 5mm pitch or 0805 SMD
- **Electrolytic caps:** Radial, 2.5mm or 5mm pitch (check diameter)

### Semiconductors:
- **BAT85 diode:** DO-35 (same as 1N4148)
- **2N3904 transistor:** TO-92
- **LEDs (3mm):** LED-3MM
- **LEDs (5mm RGB):** LED-5MM-RGB

### ICs:
- **MCP4728:** MSOP-10 or DIP-10 (recommend DIP for breadboard compatibility)

### Connectors:
- **3.5mm TS jack:** PJ-324M footprint
- **USB-C breakout:** Adafruit 4090 dimensions (check datasheet)
- **Feather headers:** 0.1" (2.54mm) female headers, 16-pin

---

## ⚡ POWER BUDGET ANALYSIS

### 5V Rail (from USB):
```
MCP4728 DAC:           ~10mA (typical)
Total 5V:              ~10-15mA
USB capability:        500mA (USB 2.0)
Margin:                Excellent (97% available)
```

### 3.3V Rail (from M4 regulator):
```
M4 itself:             ~50mA (typical, no WiFi)
MIDI FeatherWing:      ~20mA
OLED FeatherWing:      ~20mA (active display)
LEDs (7 channels):     ~70mA max (all on, full brightness)
Total 3.3V:            ~160mA max
M4 regulator:          500mA capability
Margin:                Good (68% available)
```

**Conclusion:** No external regulators needed, M4 can handle everything!

---

## 🛡️ PROTECTION & SAFETY FEATURES

### Input Protection (60% → 100%):
**Current (voltage dividers only):**
- Safe range: 0-6.6V input
- Protection method: 2× 10kΩ divider (5V → 2.5V)
- Risk: Damage above ~7V

**With BAT85 diodes (recommended):**
- Safe range: 0-40V+ input
- Protection method: Divider + Schottky clamp
- Clamp voltage: 3.7V max (within M4 3.8V absolute max)
- Risk: None

### Output Protection:
- **All DAC outputs:** 100Ω series resistors
- **S-Trig output:** 100Ω series resistor
- **Purpose:** Limit current on shorts, protect DAC/transistor
- **Max short current:** ~50mA (safe for all components)

### Power Protection:
- **USB-C:** Built-in protection on breakout board
- **Reverse polarity:** M4 has onboard protection
- **Overcurrent:** USB port current limiting

---

## 📝 DESIGN NOTES FOR EASYEDA

### Both Power Rails are CRITICAL:
```
Common mistake: Only showing 5V rail in schematics

MUST SHOW BOTH:
- 5V: Powers MCP4728 DAC
- 3.3V: Powers MIDI, OLED, all LEDs

Each rail needs:
- Bulk capacitor (10µF or 47µF)
- Bypass capacitor (0.1µF)
- Placed near loads
```

### BAT85 Diode Orientation:
```
CRITICAL: Get polarity right!

Symbol: ──|>|──
        Anode → Cathode

Physical diode:
  [Glass body] [Black band]
               ↑ Cathode

Connection:
  Anode (no band) → TAP point (ADC connection)
  Cathode (band) → 3.3V rail

Test before power:
  Multimeter diode mode
  Red on TAP, Black on 3.3V = 0.4V (forward)
  Swap probes = OL (reverse)
```

### No Op-Amp on CV Output:
```
Do NOT add TL072/LM358N circuit!

User eliminated this design.

Current design:
  MCP4728 → 100Ω → Jack (0-5V direct)

This is CORRECT and WORKS:
  - 1V/octave Eurorack standard ✓
  - 5 octaves (C0-C5) ✓
  - Simpler circuit ✓
  - No +12V needed ✓
```

### Transistor for S-Trig:
```
2N3904 NPN transistor pinout (flat side facing you):

  E  B  C
  |  |  |

Connections:
  Base (B) ← from R8 (1kΩ) ← GPIO D10
  Collector (C) → R9 (100Ω) → Jack TIP
  Emitter (E) → GND
```

---

## 🎯 FINAL VERIFICATION CHECKLIST

Before ordering PCBs:

### Electrical:
- [ ] Both 5V and 3.3V rails present
- [ ] All power rails have decoupling caps
- [ ] BAT85 diodes correct polarity
- [ ] All voltage dividers are 2× 10kΩ
- [ ] All outputs have 100Ω series protection
- [ ] I2C addresses correct (0x3C, 0x60)
- [ ] No op-amp circuit (eliminated design)

### Mechanical:
- [ ] Board size 90mm × 55mm
- [ ] Mounting holes 3.2mm diameter
- [ ] Jack spacing matches rear panel
- [ ] Clearance for stacking (10mm standoffs)
- [ ] No components too tall (height limit ~10mm)

### Manufacturing:
- [ ] Minimum trace width 10 mil (0.25mm)
- [ ] Minimum clearance 8 mil (0.2mm)
- [ ] Ground pour on both layers
- [ ] Silkscreen readable (>40mil text)
- [ ] All components have footprints
- [ ] Gerber files generated

---

## 📦 RECOMMENDED PCB MANUFACTURER SETTINGS

### PCB Specs for JLCPCB/PCBWay:
- **Board size:** 90mm × 55mm × 1.6mm
- **Layers:** 2-layer
- **Copper weight:** 1 oz (standard)
- **Solder mask:** Green (or your choice)
- **Silkscreen:** White
- **Surface finish:** HASL (lead-free) or ENIG
- **Minimum trace/space:** 6/6 mil (0.15mm)
- **Minimum hole:** 0.3mm
- **Quantity:** 5 boards minimum (typical)

### Cost Estimate:
- **PCBs only:** ~$5-15 for 5 boards
- **Shipping:** ~$5-20 (depends on speed)
- **Total:** ~$10-35
- **Timeline:** 1-2 weeks (standard), 3-5 days (express)

---

## 🔗 REFERENCE FILES

**Schematics:**
- `hardware/enclosure/TOP_BOARD_FINAL.svg`
- `hardware/enclosure/BOTTOM_BOARD_FINAL.svg`

**Truth Documents:**
- `hardware/ACTUAL_HARDWARE_TRUTH.md` (design verification)
- `docs/hardware/HARDWARE_AUDIT_CORRECTIONS.md` (corrections to old docs)

**Protection Guides:**
- `hardware/FINAL_PROTECTION_RECOMMENDATION.md` (BAT85 diodes)
- `hardware/DIODE_INSTALLATION_DIAGRAM.md` (installation)

**BOM:**
- Amazon BAT85: https://www.amazon.com/ALLECIN-BAT85-Schottky-Rectifier-Switching/dp/B0CKSNPVH8/

---

## ✅ YOU'RE READY!

You now have:
- ✅ Complete, accurate schematics
- ✅ Full BOM with sources
- ✅ PCB layout guidelines
- ✅ EasyEDA design checklist
- ✅ BAT85 diodes ordered

**Next steps:**
1. Open EasyEDA
2. Create new project
3. Import/reference schematic SVGs
4. Build schematics in EasyEDA
5. Assign footprints
6. Design PCB layouts
7. Run DRC checks
8. Order boards!

**Good luck with your PCB design!** 🎉
