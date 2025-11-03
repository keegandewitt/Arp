# Protoboard Layout - Professional Grade Design

## Overview

This document specifies the component layout for two ElectroCookie protoboards (3.8" × 3.5" each) designed for professional-grade CV/Gate I/O with proper filtering, protection, and noise reduction.

**Design Goals:**
- Commercial-quality noise rejection
- Overvoltage protection on all inputs
- Short-circuit protection on all outputs
- RF immunity
- Clean power distribution

---

## Board 1: OUTPUT BOARD (Bottom Board in Stack)

### Board Dimensions
- **Size: 75mm × 50mm (CUSTOM CUT from 97mm × 89mm ElectroCookie protoboard)**
- Mounting: 4× M3 standoffs to enclosure base
- Position: Below INPUT board in vertical stack
- **ALL CONNECTORS ON REAR EDGE (back panel of enclosure)**

### Rear Edge I/O (Left to Right)
```
[CV Out]  [V-Trig/S-Trig]  [Custom CC]
  13mm         23mm           33mm     ← distances from left edge

All 1/8" (3.5mm) mono jacks, 10mm spacing
```

### Component Placement Map

**Board: 75mm wide × 50mm deep**

```
REAR EDGE (Back panel of enclosure):
═══════════════════════════════════════════════════════════════════════
  13mm      23mm      33mm
   ↓         ↓         ↓
 [CV OUT] [V/S-TRIG] [CUSTOM CC]  ← 1/8" mono jacks (6mm holes, 10mm spacing)
═══════════════════════════════════════════════════════════════════════

FRONT SECTION (Component side):

+5V RAIL ═══════════════════════════════════════════════════════
  [C1] [C2]
  47µF 0.1µF  ← Power caps
   │    │
   └────┴──→ 5V

CENTER AREA:
  ┌──────────────────────────┐  [C3] [C4]
  │     MCP4728 MODULE       │  0.1µF decoupling caps
  │   (I2C 4-CH 12-bit DAC)  │
  │   4× M2.5 standoffs      │
  │                          │
  │  CH A  CH B  CH C  CH D  │
  │   │     │     │     │    │
  └───┼─────┼─────┼─────┼────┘
      │     │     │     │
      │     │     │     └──[R4]──[C8] (future channel)
      │     │     │        100Ω  100nF
      │     │     │
      │     │     └──[R3]──────────┐  V-Trig path (no cap)
      │     │        100Ω          │
      │     │                       │
      │     └──[R2]──[C7]──────────┼───┐  Custom CC
      │        100Ω  100nF         │   │
      │                             │   │
      └──[R1]──[C6]────────────────┼───┼──┐  CV Out
         100Ω  100nF               │   │  │
                                    │   │  │
S-TRIG CIRCUIT (shares jack with V-Trig):  │  │
  [D10 IN] ──→ [R5] ──→ NPN (2N3904)      │  │
               1kΩ       │                  │  │
                    COLL ├─[R6]────────────┘  │  S-Trig path
                         │  100Ω               │
                     EMIT └──→ GND             │
                                                │
Wire routing to rear jacks: ────────────────────┘

CONNECTIONS TO FEATHER:
  [SDA] [SCL] [5V] [GND] [D10]  ← Header pins
   │     │     │    │      │
   └─────┴─────┴────┴──────┴──→ To Feather stack

GND RAIL ═══════════════════════════════════════════════════════
```

### Bill of Materials - OUTPUT BOARD

| Qty | Component | Value/Part | Purpose |
|-----|-----------|------------|---------|
| 1 | MCP4728 Module | I2C DAC | 4-channel CV output |
| 1 | Electrolytic Cap | 47µF 16V | Bulk power supply |
| 4 | Ceramic Cap | 0.1µF 50V | Bypass/decoupling |
| 3 | Ceramic Cap | 100nF 50V | CV output smoothing |
| 4 | Resistor | 100Ω 1/4W | Output protection |
| 1 | Resistor | 1kΩ 1/4W | NPN base current |
| 1 | NPN Transistor | 2N3904 | S-Trig switching |
| 3 | 1/8" mono jack | 3.5mm panel mount | CV Out, V-Trig/S-Trig, Custom CC |
| 1 | 5-pin header | Male 0.1" | I2C + Power + D10 to Feather |
| 4 | M2.5 standoffs | 10mm | MCP4728 mounting |
| - | Wire | 22-24 AWG | Internal connections |

---

## Board 2: INPUT BOARD (Top Board in Stack)

### Board Dimensions
- **Size: 75mm × 50mm (CUSTOM CUT from 97mm × 89mm ElectroCookie protoboard)**
- Mounting: 4× M3 metal standoffs to OUTPUT board
- Position: Above OUTPUT board, below Feather stack
- **ALL CONNECTORS ON REAR EDGE (back panel of enclosure)**

### Rear Edge I/O (Left to Right)
```
TOP ROW:     [CV IN] [GATE IN]    [MIDI IN] [MIDI OUT]
              13mm     23mm         35.5mm     55.5mm   ← distances from left edge

BOTTOM ROW:  [USB-C]
              58.5mm ← distance from left edge (right edge aligned with MIDI Out right edge)

1/8" jacks: 6mm holes, 10mm spacing
MIDI DIN: 15mm holes, 20mm spacing
USB-C: 9.5mm × 3.8mm rectangular cutout (positioned at bottom row height)
```

### Component Placement Map

**Board: 75mm wide × 50mm deep**

```
REAR EDGE (Back panel of enclosure):
═══════════════════════════════════════════════════════════════════════════
TOP ROW:
  13mm     23mm       35.5mm      55.5mm
   ↓        ↓           ↓           ↓
 [CV IN] [GATE IN]  [MIDI IN]  [MIDI OUT]
                     (5-pin DIN) (5-pin DIN)

BOTTOM ROW:
                                         58.5mm
                                           ↓
                                        [USB-C]
                                     (panel mount)
                                     (right edge aligned with MIDI Out)
═══════════════════════════════════════════════════════════════════════════

FRONT SECTION (Component side):

+5V RAIL ═══════════════════════════════════════════════════════
  [C1] [C2]
  47µF 0.1µF  ← Power caps
   │    │
   └────┴──→ 5V (from Feather via OUTPUT board)

LEFT AREA - CV INPUT CIRCUIT (A3):
  [CV IN JACK] ──┬──[R1]──[R2]──┬────────── GND
  (rear edge)    │   10kΩ  10kΩ  │
                GND              │
                                 ├──[R3]──[C3]──[D1]──→ [A3 OUT]
                                 │   10kΩ  100nF  BAT85   To Feather
                                 │          │      │
                                 └──[R4]────┤      └──→ +3.3V (clamp)
                                    22kΩ    │
                                           GND

LEFT AREA - GATE INPUT CIRCUIT (A4):
  [GATE IN JACK] ─┬──[R5]──[R6]──┬────────── GND
  (rear edge)     │   10kΩ  10kΩ  │
                 GND              │
                                  ├──[R7]──[C4]──[D2]──→ [A4 OUT]
                                  │   10kΩ  100nF  BAT85   To Feather
                                  │          │      │
                                  └──[R8]────┤      └──→ +3.3V (clamp)
                                     22kΩ    │
                                            GND

RIGHT AREA - MIDI ROUTING:
  [MIDI IN JACK]  ────→ Wire to MIDI FeatherWing RX
  [MIDI OUT JACK] ────→ Wire to MIDI FeatherWing TX
  (Both on rear edge, panel-mount 5-pin DIN jacks)

  [USB-C JACK] ────→ USB-C extension cable to Feather M4
  (On rear edge, panel-mount breakout)

CONNECTIONS TO FEATHER:
  [A3] [A4] [GND] [MIDI TX] [MIDI RX]  ← Header pins
   │    │    │       │          │
   └────┴────┴───────┴──────────┴──→ To Feather stack

GND RAIL ═══════════════════════════════════════════════════════
```

### Bill of Materials - INPUT BOARD

| Qty | Component | Value/Part | Purpose |
|-----|-----------|------------|---------|
| 1 | Electrolytic Cap | 47µF 16V | Bulk power supply |
| 1 | Ceramic Cap | 0.1µF 50V | High-freq bypass |
| 2 | Ceramic Cap | 100nF 50V | Input low-pass filter |
| 4 | Resistor | 10kΩ 1/4W | Voltage divider (series) |
| 2 | Resistor | 22kΩ 1/4W | Voltage divider (to GND) |
| 2 | Resistor | 10kΩ 1/4W | Series input protection |
| 2 | Schottky Diode | BAT85 | Overvoltage clamp to 3.3V |
| 2 | 1/8" mono jack | 3.5mm panel mount | CV In, Gate In |
| 2 | 5-pin DIN jack | Panel mount | MIDI In, MIDI Out |
| 1 | USB-C panel mount | Breakout board | Programming/power |
| 1 | 5-pin header | Male 0.1" | Analog + MIDI to Feather |
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
**Result:** 5V input → 2.62V at tap

**Protection Chain:**
```
Tap → [10kΩ series] → [100nF to GND] → [BAT85 to 3.3V] → ADC Pin
```

1. **10kΩ series resistor:** Current limiting if ADC pin shorts
2. **100nF capacitor:** Low-pass filter (cutoff ~160Hz with 10kΩ)
3. **BAT85 diode:** Clamps overvoltage to 3.3V rail (protection if divider fails)

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

---

## Power Distribution Strategy

### Daisy-Chain Power Topology

```
Feather 5V/GND
    ↓
OUTPUT Board (47µF + 0.1µF local)
    ↓
INPUT Board (47µF + 0.1µF local)
```

**Why this works:**
- Each board has local bulk + bypass capacitors
- Feather USB provides up to 500mA (plenty for this design)
- MCP4728: ~10mA typical
- Total current: <100mA (huge safety margin)

---

## Mounting Specifications

### Board Spacing (Vertical Stack)

```
                    SIDE VIEW

    ┌──────────────┐
    │   FEATHER    │  ← Mounted to enclosure base
    │    STACK     │     via M2.5 standoffs
    └──────────────┘
          ↕ 15mm gap (for wire routing)
    ┌──────────────┐
    │  INPUT BOARD │  ← M3 standoffs to OUTPUT board
    └──────────────┘
          ↕ 10mm gap (board thickness + standoff)
    ┌──────────────┐
    │ OUTPUT BOARD │  ← M3 standoffs to enclosure base
    └──────────────┘
          ↕
    ═══════════════
     Enclosure Base
```

### Standoff Specifications

| Connection | Type | Height | Thread | Notes |
|------------|------|--------|--------|-------|
| OUTPUT board → Base | M3 Female-Female | 10-15mm | M3 | Enclosure mounting |
| INPUT board → OUTPUT board | **M3 Metal Standoffs** | 10mm | M3 | **Critical: Ensures jack alignment** |
| Feather → Base | M2.5 Female-Female | 15mm | M2.5 | Component stack |
| MCP4728 → OUTPUT board | M2.5 Male-Female | 10mm | M2.5 | DAC module mounting |

**IMPORTANT:** The M3 standoffs between INPUT and OUTPUT boards provide rigid alignment for all jacks. Jacks are soldered directly to board edges and pass through enclosure clearance holes. No panel mounting hardware (washers/nuts) needed!

---

## Professional Design Notes

### Grounding

- **Star ground topology:** All grounds meet at OUTPUT board's GND rail
- **Single point ground:** Prevents ground loops
- **Heavy ground traces:** Use multiple parallel traces on power rails

### Component Selection

- **Resistors:** 1% metal film for precision (voltage dividers)
- **Capacitors:**
  - Ceramic: X7R or C0G/NP0 dielectric (stable, low ESR)
  - Electrolytic: Low-ESR type for power supply
- **Diodes:** BAT85 Schottky (fast, low forward drop)

### PCB Layout Best Practices

- **Short traces:** Keep analog signals short and direct
- **Bypass caps:** Place within 0.5" of IC power pins
- **Separate analog/digital:** Keep I2C traces away from analog signals
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

---

**Last Updated:** 2025-11-02
**Status:** Design Complete - Ready for Assembly
