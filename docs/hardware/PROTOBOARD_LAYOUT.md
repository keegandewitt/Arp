# Protoboard Layout - Professional Grade Design with LED Indicators

## Overview

This document specifies the component layout for two ElectroCookie protoboards (custom cut to 90mm × 55mm each) designed for professional-grade CV/Gate I/O with proper filtering, protection, noise reduction, and **visual activity indicators**.

**Design Goals:**
- Commercial-quality noise rejection
- Overvoltage protection on all inputs
- Short-circuit protection on all outputs
- RF immunity
- Clean power distribution
- **Visual feedback via LED indicators (7 total: 5 white + 2 RGB)**

**Last Updated:** 2025-11-02 (added LED system)

---

## Board 1: OUTPUT BOARD (Bottom Board in Stack)

### Board Dimensions
- **Size: 90mm × 55mm (CUSTOM CUT from 97mm × 89mm ElectroCookie protoboard)**
- Mounting: 4× M3 standoffs to enclosure base (10mm height)
- Position: Below INPUT board in vertical stack
- **ALL CONNECTORS ON REAR EDGE (back panel of enclosure)**

### Rear Edge I/O (Left to Right)

```
BOTTOM ROW - OUTPUT BOARD:
[USB-C]  [CV OUT]  [TRIG OUT]  [CC OUT]  [MIDI OUT]  [MIDI IN]
  8mm      20mm       32mm        44mm      65mm        85mm
           ●LED       ●LED        ●LED      ●LED        ●LED
```

**Connectors:**
- **USB-C:** Panel mount breakout, 9.5mm × 3.8mm cutout (no LED)
- **CV OUT:** 1/8" mono jack, 6mm hole + **white LED** (activity)
- **TRIG OUT:** 1/8" mono jack, 6mm hole + **RGB LED** (mode + activity)
- **CC OUT:** 1/8" mono jack, 6mm hole + **white LED** (activity)
- **MIDI OUT:** 5-pin DIN panel mount, 15.5mm hole + **white LED** (TX activity)
- **MIDI IN:** 5-pin DIN panel mount, 15.5mm hole + **white LED** (RX activity)

**LED Details:**
- **Total: 5 LEDs** (3 white + 1 RGB)
- **Position:** 7mm to the right of each jack center
- **Mounting:** Press-fit into 3.2mm back panel holes
- **RGB Color Coding:**
  - **Green:** V-Trig mode active
  - **Red:** S-Trig mode active

---

### Component Placement Map

**Board: 90mm wide × 55mm deep**

```
REAR EDGE (Back panel of enclosure):
════════════════════════════════════════════════════════════════════════════════
  8mm   20mm    32mm    44mm         65mm    85mm
   ↓     ↓       ↓       ↓             ↓       ↓
[USB-C][CV OUT][TRIG OUT][CC OUT]  [MIDI OUT][MIDI IN]
        ●LED     ●RGB      ●LED        ●LED      ●LED
════════════════════════════════════════════════════════════════════════════════

FRONT SECTION (Component side):

+5V RAIL ══════════════════════════════════════════════════════════════════
  [C1] [C2]
  47µF 0.1µF  ← Power caps
   │    │
   └────┴──→ 5V (from Feather via stacking headers)

LEFT AREA - USB-C BREAKOUT:
  [USB-C Panel Mount Breakout]
       │
       └──→ To Feather USB (via extension cable)

CENTER AREA - MCP4728 DAC:
  ┌──────────────────────────┐  [C3] [C4]
  │     MCP4728 MODULE       │  0.1µF DAC decoupling caps
  │   (I2C 4-CH 12-bit DAC)  │
  │   4× M2.5 standoffs      │
  │                          │
  │  CH A  CH B  CH C  CH D  │
  │   │     │     │     │    │
  └───┼─────┼─────┼─────┼────┘
      │     │     │     │
      │     │     │     └──[R4]──[C8]──→ (future expansion)
      │     │     │        100Ω  100nF
      │     │     │
      │     │     └──[R3]──[C7]──→ CC OUT jack
      │     │        100Ω  100nF
      │     │
      │     └──[R2]──────────────→ TRIG OUT jack (no cap - fast edges)
      │        100Ω
      │
      └──[R1]──[C6]──→ CV OUT jack
         100Ω  100nF

S-TRIG CIRCUIT (shares TRIG OUT jack):
  [D10 from Feather] ──[R5]──→ NPN Base (2N3904)
                        1kΩ      │
                            COLL─┼─[R6]──→ TRIG OUT jack
                                 │  100Ω
                             EMIT─┴──→ GND

RIGHT AREA - MIDI FEATHERWING:
  ┌─────────────────────────────────────┐
  │     MIDI FEATHERWING                │
  │     (Horizontal orientation)        │  ← Stacks on Feather via headers
  │                                     │     Position: Right side of board
  │   [MIDI OUT]              [MIDI IN] │ ← Jacks align with rear edge holes
  │      │                        │     │
  └──────┼────────────────────────┼─────┘
         │                        │
         └──→ 65mm                └──→ 85mm (distances from left edge)

ACTIVITY LED CIRCUITS (5 LEDs on OUTPUT board):

  WHITE LEDs (4× standard 3mm):
    [D12]    ──[R7]──→  LED (CV OUT white)   ──→ GND
    [D25]    ──[R8]──→  LED (CC OUT white)   ──→ GND
    [CAN_TX] ──[R9]──→  LED (MIDI OUT white) ──→ GND
    [A5]     ──[R10]──→ LED (MIDI IN white)  ──→ GND

    150Ω current limiting resistors

  RGB LED (1× TRIG OUT, common cathode 3mm):
    [A0] ──[R11]──→ RED channel   ──┐
    [A1] ──[R12]──→ GREEN channel ──┼──→ Common cathode → GND
    [A2] ──[R13]──→ BLUE channel  ──┘

    150Ω current limiting resistors (3× total for RGB)

    LED Behavior:
    - GREEN on: V-Trig mode active (gate HIGH)
    - RED on: S-Trig mode active (gate LOW)
    - Brightness varies with activity

  LED Physical Mounting:
    - All LEDs positioned 7mm right of jack centers
    - Press-fit into 3.2mm back panel holes
    - Flat-top 3mm clear LEDs (wide viewing angle)
    - Leads soldered to protoboard traces

CONNECTIONS TO FEATHER STACK:
  [SDA][SCL][5V][GND][D10][D12][D25][CAN_TX][A0][A1][A2][A5]
   │    │    │   │    │    │    │     │      │   │   │   │
   └────┴────┴───┴────┴────┴────┴─────┴──────┴───┴───┴───┴──→ 12-pin header
                                                               to Feather stack

GND RAIL ═══════════════════════════════════════════════════════════════════
```

---

### Bill of Materials - OUTPUT BOARD

| Qty | Component | Value/Part | Purpose |
|-----|-----------|------------|---------|
| 1 | MCP4728 Module | I2C DAC | 4-channel CV output |
| 1 | MIDI FeatherWing | Adafruit #2063 | MIDI I/O |
| 1 | USB-C Breakout | Panel mount | Power/programming extension |
| 1 | Electrolytic Cap | 47µF 16V | Bulk power supply |
| 4 | Ceramic Cap | 0.1µF 50V | Bypass/decoupling |
| 4 | Ceramic Cap | 100nF 50V | Output smoothing (3 used, 1 spare) |
| 4 | Resistor | 100Ω 1/4W | Output protection |
| 1 | Resistor | 1kΩ 1/4W | NPN base current limiting |
| 7 | Resistor | 150Ω 1/4W | **LED current limiting (4 white + 3 RGB channels)** |
| 1 | NPN Transistor | 2N3904 | S-Trig switching |
| 3 | 1/8" mono jack | 3.5mm panel | CV/TRIG/CC outputs |
| 2 | 5-pin DIN jack | Panel mount | MIDI IN/OUT (via FeatherWing) |
| 4 | LED | **3mm white clear flat-top** | **Activity indicators (CV, CC, MIDI×2)** |
| 1 | RGB LED | **3mm clear flat-top, common cathode** | **TRIG OUT mode + activity** |
| 1 | 12-pin header | Male 0.1" | To Feather stack (expanded for LEDs) |
| 4 | M2.5 standoffs | 10mm | MCP4728 mounting |
| - | Wire | 22-24 AWG | Internal connections |

---

## Board 2: INPUT BOARD (Top Board in Stack)

### Board Dimensions
- **Size: 90mm × 55mm (CUSTOM CUT from 97mm × 89mm ElectroCookie protoboard)**
- Mounting: 4× M3 metal standoffs to OUTPUT board (10mm height)
- Position: Above OUTPUT board, below Feather stack
- **ALL CONNECTORS ON REAR EDGE (back panel of enclosure)**

### Rear Edge I/O (Left to Right)

```
TOP ROW - INPUT BOARD:
     [CV IN]  [TRIG IN]
      20mm      32mm
      ●LED      ●RGB
```

**Connectors:**
- **CV IN:** 1/8" mono jack, 6mm hole + **white LED** (activity)
- **TRIG IN:** 1/8" mono jack, 6mm hole + **RGB LED** (mode + activity)

**LED Details:**
- **Total: 2 LEDs** (1 white + 1 RGB)
- **Position:** 7mm to the right of each jack center
- **Mounting:** Press-fit into 3.2mm back panel holes
- **RGB Color Coding:**
  - **Green:** V-Trig mode detected
  - **Red:** S-Trig mode detected

---

### Component Placement Map

**Board: 90mm wide × 55mm deep**

```
REAR EDGE (Back panel of enclosure):
════════════════════════════════════════════════════════════════════════════════
      20mm      32mm
       ↓         ↓
     [CV IN]  [TRIG IN]
      ●LED      ●RGB
════════════════════════════════════════════════════════════════════════════════

FRONT SECTION (Component side):

+5V RAIL ══════════════════════════════════════════════════════════════════
  [C1] [C2]
  47µF 0.1µF  ← Power caps
   │    │
   └────┴──→ 5V (from OUTPUT board via stacking headers)

LEFT AREA - CV INPUT PROTECTION CIRCUIT (A3):
  [CV IN JACK] ──┬──[R1]──[R2]──┬────────── GND
  (20mm)         │   10kΩ  10kΩ  │
                GND              │
                                 ├──[R3]──[C3]──[D1]──→ A3 to Feather
                                 │   10kΩ  100nF BAT85
                                 │          │      │
                                 └──[R4]────┤      └──→ 3.3V rail (clamp)
                                    22kΩ    │
                                           GND

  Voltage scaling: 0.524× (5V → 2.62V safe for 3.3V ADC)

CENTER AREA - TRIG INPUT PROTECTION CIRCUIT (A4):
  [TRIG IN JACK]─┬──[R5]──[R6]──┬────────── GND
  (32mm)         │   10kΩ  10kΩ  │
                GND              │
                                 ├──[R7]──[C7]──[D2]──→ A4 to Feather
                                 │   10kΩ  100nF BAT85
                                 │          │      │
                                 └──[R8]────┤      └──→ 3.3V rail (clamp)
                                    22kΩ    │
                                           GND

  Voltage scaling: 0.524× (5V → 2.62V safe for 3.3V ADC)

ACTIVITY LED CIRCUITS (2 LEDs on INPUT board):

  WHITE LED (1× standard 3mm):
    [D4] ──[R9]──→ LED (CV IN white) ──→ GND

    150Ω current limiting resistor

  RGB LED (1× TRIG IN, common cathode 3mm):
    [D11] ──[R10]──→ RED channel   ──┐
    [D23] ──[R11]──→ GREEN channel ──┼──→ Common cathode → GND
    [D24] ──[R12]──→ BLUE channel  ──┘

    150Ω current limiting resistors (3× total for RGB)

    LED Behavior:
    - GREEN on: V-Trig mode detected (voltage >2V)
    - RED on: S-Trig mode detected (voltage <1V)
    - Brightness varies with input signal strength

  LED Physical Mounting:
    - All LEDs positioned 7mm right of jack centers
    - Press-fit into 3.2mm back panel holes
    - Flat-top 3mm clear LEDs (wide viewing angle)
    - Leads soldered to protoboard traces

CONNECTIONS TO FEATHER STACK:
  [A3][A4][3.3V][GND][D4][D11][D23][D24]
   │   │    │    │    │    │    │    │
   └───┴────┴────┴────┴────┴────┴────┴──→ 8-pin header to Feather stack

GND RAIL ═══════════════════════════════════════════════════════════════════
```

---

### Bill of Materials - INPUT BOARD

| Qty | Component | Value/Part | Purpose |
|-----|-----------|------------|---------|
| 1 | Electrolytic Cap | 47µF 16V | Bulk power supply |
| 1 | Ceramic Cap | 0.1µF 50V | High-freq bypass |
| 2 | Ceramic Cap | 100nF 50V | Input filtering |
| 4 | Resistor | 10kΩ 1/4W | Voltage divider (series) |
| 2 | Resistor | 22kΩ 1/4W | Voltage divider (to GND) |
| 2 | Resistor | 10kΩ 1/4W | Series input protection |
| 4 | Resistor | 150Ω 1/4W | **LED current limiting (1 white + 3 RGB channels)** |
| 2 | Schottky Diode | BAT85 | Overvoltage clamp to 3.3V |
| 2 | 1/8" mono jack | 3.5mm panel | CV/TRIG inputs |
| 1 | LED | **3mm white clear flat-top** | **CV IN activity indicator** |
| 1 | RGB LED | **3mm clear flat-top, common cathode** | **TRIG IN mode + activity** |
| 1 | 8-pin header | Male 0.1" | To Feather stack (expanded for LEDs) |
| - | Wire | 22-24 AWG | Internal connections |

---

## Circuit Explanations

### Input Protection (Each Input)

**Voltage Divider:**
```
External 0-5V → [10kΩ] → [10kΩ] → [22kΩ to GND]
                           ↓
                    Tap point (scaled voltage)
```
**Scaling:** 22kΩ / (20kΩ + 22kΩ) = 0.524
**Result:** 5V input → 2.62V at tap (safe for 3.3V ADC)

**Protection Chain:**
```
Tap → [10kΩ series] → [100nF to GND] → [BAT85 to 3.3V] → ADC Pin
```

1. **10kΩ series resistor:** Current limiting if ADC pin shorts
2. **100nF capacitor:** Low-pass filter (cutoff ~160Hz with 10kΩ)
3. **BAT85 diode:** Clamps overvoltage to 3.3V rail (backup protection)

**Filtering Performance:**
- Removes RF interference
- Smooths voltage spikes
- Preserves CV signal integrity (DC to ~150Hz)

### Output Protection (Each CV Output)

```
DAC Channel → [100Ω series] → [100nF to GND] → Output Jack
```

1. **100Ω resistor:** Short-circuit protection (limits current to 50mA at 5V)
2. **100nF capacitor:** Smooths DAC switching noise

**Gate outputs:** Only 100Ω resistor, NO capacitor (capacitor would slow rise/fall times)

### LED Indicator System

**LED Current Calculations (3.3V GPIO):**

**White LED (typical Vf = 3.0V):**
- Current: (3.3V - 3.0V) / 150Ω = **2mA** (visible, power-efficient)

**RGB LED channels:**
- Red (Vf = 2.0V): (3.3V - 2.0V) / 150Ω = **8.7mA** (bright)
- Green (Vf = 3.0V): (3.3V - 3.0V) / 150Ω = **2mA** (dimmer but visible)
- Blue (Vf = 3.0V): (3.3V - 3.0V) / 150Ω = **2mA** (dimmer but visible)

**Total Power Budget:**
- 5 white LEDs × 2mA = 10mA
- 2 RGB LEDs × ~3mA (one channel active) = 6mA
- **Total typical: ~16-20mA** (negligible impact on battery life)

**Detection Logic:**

1. **Input LEDs (monitored via ADC):**
   - Sample at 100Hz
   - CV IN white: ON when voltage > 0.1V
   - TRIG IN RGB: GREEN (V-Trig >2V), RED (S-Trig <1V)

2. **Output LEDs (software controlled):**
   - CV OUT white: ON when DAC Ch A active
   - TRIG OUT RGB: GREEN (V-Trig mode), RED (S-Trig mode)
   - CC OUT white: ON when DAC Ch B active

3. **MIDI LEDs (UART monitoring):**
   - MIDI OUT: pulse 50ms on TX activity
   - MIDI IN: pulse 50ms on RX activity

---

## Power Distribution Strategy

### Daisy-Chain Power Topology

```
Feather 5V/GND (from USB-C or battery)
    ↓
OUTPUT Board (47µF + 0.1µF local)
    ├──→ MCP4728 (~10mA)
    ├──→ MIDI FeatherWing (~20mA)
    └──→ 4 LEDs + 1 RGB (~10mA)
    ↓
INPUT Board (47µF + 0.1µF local)
    └──→ 1 LED + 1 RGB (~6mA)

Total current: ~50mA typical (huge safety margin vs. 500mA USB limit)
```

**Why this works:**
- Each board has local bulk + bypass capacitors
- Feather USB provides up to 500mA
- Total current draw <100mA (includes LEDs)
- Battery runtime: 1200mAh / 100mA = **12+ hours**

---

## Mounting Specifications

### Board Spacing (Vertical Stack)

```
                    SIDE VIEW

    ┌──────────────┐
    │   FEATHER    │  ← Mounted to INPUT board
    │    STACK     │     via M2.5 standoffs (15mm)
    └──────────────┘
          ↕ 15mm gap (for wire routing)
    ┌──────────────┐
    │  INPUT BOARD │  ← M3 standoffs to OUTPUT board (10mm)
    └──────────────┘     Rear jacks at 27mm height
          ↕ 10mm gap (board thickness + standoff)
    ┌──────────────┐
    │ OUTPUT BOARD │  ← M3 standoffs to enclosure base (10mm)
    │ (MIDI wing)  │     Rear jacks at 15mm height
    └──────────────┘
          ↕ 10mm
    ═══════════════
     Enclosure Base
     (battery under OUTPUT board, front section)
```

### Standoff Specifications

| Connection | Type | Height | Thread | Notes |
|------------|------|--------|--------|-------|
| OUTPUT board → Base | M3 Female-Female | 10mm | M3 | Enclosure mounting |
| INPUT board → OUTPUT board | **M3 Metal Standoffs** | 10mm | M3 | **Critical: Ensures jack alignment** |
| Feather → INPUT board | M2.5 Female-Female | 15mm | M2.5 | Component stack |
| MCP4728 → OUTPUT board | M2.5 Male-Female | 10mm | M2.5 | DAC module mounting |

**IMPORTANT:** The M3 standoffs between INPUT and OUTPUT boards provide rigid alignment for all jacks. Jacks are soldered directly to board edges and pass through enclosure clearance holes. LEDs press-fit into adjacent 3.2mm holes. No panel mounting hardware (washers/nuts) needed!

---

## Professional Design Notes

### Grounding

- **Star ground topology:** All grounds meet at OUTPUT board's GND rail
- **Single point ground:** Prevents ground loops
- **Heavy ground traces:** Use multiple parallel traces on power rails
- **LED ground returns:** Tied directly to main GND rail

### Component Selection

- **Resistors:** 1% metal film for precision (voltage dividers, LED current limiting)
- **Capacitors:**
  - Ceramic: X7R or C0G/NP0 dielectric (stable, low ESR)
  - Electrolytic: Low-ESR type for power supply
- **Diodes:** BAT85 Schottky (fast, low forward drop)
- **LEDs:** High-efficiency flat-top 3mm (wide viewing angle, low current)

### PCB Layout Best Practices

- **Short traces:** Keep analog signals short and direct
- **Bypass caps:** Place within 0.5" of IC power pins
- **Separate analog/digital:** Keep I2C traces away from analog signals
- **LED routing:** Keep LED traces short to minimize voltage drop
- **Ground plane:** Use power rails as pseudo ground plane

---

## Testing Checklist

After assembly, verify:

1. ✓ No shorts between 5V and GND rails
2. ✓ MCP4728 responds to I2C scan
3. ✓ Input voltage dividers scale correctly (5V → 2.62V)
4. ✓ Overvoltage clamps activate at 3.3V
5. ✓ CV outputs swing 0-5V cleanly
6. ✓ Gate outputs have fast rise/fall times (<1ms)
7. ✓ S-Trig pulls to ground when active
8. ✓ No noise on CV outputs (scope check)
9. ✓ **All 7 LEDs illuminate when activated**
10. ✓ **RGB LEDs show correct colors (green/red for V-Trig/S-Trig)**
11. ✓ **LED brightness correlates with signal activity**
12. ✓ **MIDI LEDs pulse on TX/RX activity**

---

**Last Updated:** 2025-11-02
**Status:** Design Complete with LED System - Ready for Assembly

**END OF DOCUMENT**
