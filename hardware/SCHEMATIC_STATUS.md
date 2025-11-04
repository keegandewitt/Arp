# PRISME Hardware Schematics - Status & Reference

**Last Updated:** 2025-11-03 (Session 25)
**Purpose:** Complete hardware audit and schematic generation for EasyEDA PCB design

---

## Schematic Files Generated

### ✅ TOP_BOARD_SCHEMATIC.svg (COMPLETE)
**File:** `hardware/enclosure/TOP_BOARD_SCHEMATIC.svg` (41KB)
**Status:** ✅ **COMPLETE** - Includes all components

**Contains:**
1. **Feather M4 CAN Express** (main controller)
   - ATSAMD51, 120MHz, 192KB RAM
   - CircuitPython 10.0.3
   - I2C: D21(SDA), D22(SCL) → OLED + MCP4728
   - MIDI: D0(RX), D1(TX) → Bottom board
   - ADC: A3(TRIG), A4(CV) ← Input circuits
   - GPIO: D4-D25, A0-A5 → LEDs, S-Trig

2. **OLED FeatherWing 128x64** (stacked on M4)
   - SH1107 driver, I2C 0x3C
   - Buttons: A(D5), B(D6), C(D9)
   - Stacking headers connect to M4

3. **Power Distribution**
   - 5V Rail: C11 (10uF), C12 (0.1uF)
   - From stacking headers

4. **CV Input Protection Circuit**
   - Jack → R14 (10k) → voltage divider (R15 10k to GND) → 2.62V
   - BAT85 diode clamp to 3.3V
   - Dual RC filter: C3 (100nF) + C4 (10nF)
   - Output to A4 ADC

5. **TRIG Input Protection Circuit** (identical to CV)
   - Jack → R16 (10k) → voltage divider (R17 10k to GND) → 2.62V
   - BAT85 diode clamp to 3.3V
   - Filter: C5 (100nF)
   - Output to A3 ADC

6. **CV Activity LED**
   - GPIO D5 → R18 (150Ω) → White 3mm LED → GND
   - Position: Rear panel, 7mm right of CV jack

7. **TRIG RGB Mode/Activity LED**
   - GPIO D6 → R19 (150Ω) → RED LED → GND
   - GPIO D9 → R20 (150Ω) → GREEN LED → GND
   - GPIO D11 → R21 (150Ω) → BLUE LED → GND
   - Color: GREEN = V-Trig mode | RED = S-Trig mode
   - Position: Rear panel, 7mm right of TRIG jack

---

### ⚠️ BOTTOM_BOARD_SCHEMATIC.svg (PARTIAL)
**File:** `hardware/enclosure/BOTTOM_BOARD_SCHEMATIC.svg` (39KB)
**Status:** ⚠️ **PARTIAL** - Missing USB-C and MCP4728 module blocks

**Contains:**
1. **CV Output Circuit** (MCP4728 Channel A)
   - CH_A (0-5V) → R1 (100Ω) → C6 (100nF) filter → CV OUT Jack
   - Purpose: 1V/octave pitch (0-5V = 5 octaves, MIDI 0-60)
   - LED: D12 → R7 (150Ω) → White 3mm LED → GND

2. **TRIG Output Circuit - Dual Mode** (MCP4728 Channel B + GPIO D10)
   - **V-Trig Mode:** CH_B (0-5V) → R2 (100Ω) → TRIG OUT Jack
   - **S-Trig Mode:** GPIO D10 → R5 (1kΩ) → Q1 (2N3904 NPN) collector to jack, emitter to GND, R6 (100Ω) in collector
   - RGB LED:
     - A0 → R11 (150Ω) → RED LED → GND
     - A1 → R12 (150Ω) → GREEN LED → GND
     - A2 → R13 (150Ω) → BLUE LED → GND

3. **CC Output Circuit** (MCP4728 Channel C)
   - CH_C (0-5V) → R3 (100Ω) → C7 (100nF) filter → CC OUT Jack
   - Purpose: Custom CC mapping with Learn Mode
   - LED: D25 → R8 (150Ω) → White 3mm LED → GND

4. **MIDI Activity LEDs**
   - MIDI OUT: CAN_TX → R9 (150Ω) → White 3mm LED → GND
   - MIDI IN: A5 → R10 (150Ω) → White 3mm LED → GND

5. **Power Distribution**
   - 5V Rail: C1 (47uF), C2 (0.1uF)
   - 3.3V Rail: C9 (10uF), C10 (0.1uF)

**Missing (to add in EasyEDA):**
- ❌ USB-C Panel Mount Breakout (rear panel, 8mm from left)
- ❌ MCP4728 4-Channel DAC Module (I2C 0x60, SDA/SCL from M4, VDD 5V, decoupling C3/C4)

---

## Complete Component List

### TOP BOARD (Input Board)
**Semiconductors:**
- 1× Feather M4 CAN Express (ATSAMD51)
- 1× OLED FeatherWing 128x64 (SH1107)
- 2× BAT85 Schottky diodes (D2, D3)
- 5× White 3mm LEDs (CV activity)
- 1× RGB 3mm LED (TRIG mode/activity)

**Resistors:**
- 4× 10kΩ (R14, R15, R16, R17) - voltage dividers
- 4× 150Ω (R18, R19, R20, R21) - LED current limiting

**Capacitors:**
- 2× 10uF (C11 - 5V bulk)
- 2× 0.1uF (C12 - 5V bypass)
- 2× 100nF (C3, C5 - input filters)
- 1× 10nF (C4 - CV second-stage filter)

**Connectors:**
- 2× 1/8" TRS jacks (CV IN, TRIG IN) - rear panel
- Stacking headers (connect to M4)

### BOTTOM BOARD (Output Board)
**Semiconductors:**
- 1× MCP4728 4-channel DAC module (I2C 0x60)
- 1× 2N3904 NPN transistor (Q1 - S-Trig)
- 3× White 3mm LEDs (CV, CC, MIDI OUT)
- 1× White 3mm LED (MIDI IN)
- 1× RGB 3mm LED (TRIG mode/activity)

**Resistors:**
- 4× 100Ω (R1, R2, R3, R6) - DAC series protection
- 1× 1kΩ (R5) - NPN base resistor
- 5× 150Ω (R7, R8, R9, R10, R11, R12, R13) - LED current limiting

**Capacitors:**
- 1× 47uF (C1 - 5V bulk)
- 3× 0.1uF (C2, C3, C4 - bypass/DAC decoupling)
- 1× 10uF (C9 - 3.3V bulk)
- 1× 0.1uF (C10 - 3.3V bypass)
- 2× 100nF (C6, C7 - output filters)

**Connectors:**
- 1× USB-C panel mount breakout (rear panel, 8mm from left)
- 3× 1/8" TRS jacks (CV OUT, TRIG OUT, CC OUT) - rear panel
- 2× 5-pin DIN panel mount (MIDI OUT, MIDI IN) - rear panel

---

## Rear Panel Layout (Bottom Board)

```
Position from left edge:
8mm   - USB-C breakout (9.5mm × 3.8mm cutout)
20mm  - CV OUT jack (6mm hole) + LED at 27mm
32mm  - TRIG OUT jack (6mm hole) + RGB LED at 39mm
44mm  - CC OUT jack (6mm hole) + LED at 51mm
65mm  - MIDI OUT jack (15.5mm hole) + LED at 72mm
85mm  - MIDI IN jack (15.5mm hole) + LED at 92mm
```

---

## Complete Documentation Reference

**Comprehensive Hardware Audit:**
- `docs/hardware/COMPREHENSIVE_HARDWARE_AUDIT.md` (1,389 lines) - Complete specification
- `docs/hardware/AUDIT_SUMMARY_INDEX.md` - Quick reference index

**Key Documents:**
- `docs/hardware/PROTOBOARD_LAYOUT.md` - Physical layout
- `docs/hardware/PIN_ALLOCATION_MATRIX.md` - M4 pin assignments
- `docs/hardware/JACK_WIRING_GUIDE.md` - Assembly instructions
- `docs/hardware/BACK_PANEL_LAYOUT.md` - Connector positions

**Schematic Generators:**
- `hardware/enclosure/generate_top_board_schematic.py` - TOP board generator
- `hardware/enclosure/generate_bottom_board_schematic.py` - BOTTOM board generator

---

## Next Steps for EasyEDA PCB Design

1. **Import Component Footprints:**
   - Feather M4 CAN Express (Adafruit footprint)
   - OLED FeatherWing 128x64 (stacking headers)
   - MCP4728 DAC module (breakout board footprint)
   - USB-C panel mount breakout
   - 1/8" TRS jacks (panel mount)
   - 5-pin DIN jacks (panel mount)
   - 3mm LEDs (flat-top)
   - Standard SMD/TH resistors and capacitors

2. **Create Schematics:**
   - Use TOP_BOARD_SCHEMATIC.svg as reference for TOP board
   - Use BOTTOM_BOARD_SCHEMATIC.svg + add USB-C + MCP4728 blocks for BOTTOM board
   - Verify all pin connections match PIN_ALLOCATION_MATRIX.md

3. **Design PCB Layout:**
   - Board size: 90mm × 55mm (custom cut from 97mm × 89mm ElectroCookie)
   - Rear edge connector positions from BACK_PANEL_LAYOUT.md
   - Component placement from PROTOBOARD_LAYOUT.md
   - Keep I2C traces short (SDA/SCL to both OLED and DAC)

4. **Design Rules:**
   - Track width: 0.3mm minimum (signal), 0.5mm (power)
   - Clearance: 0.3mm minimum
   - Via size: 0.6mm hole, 1.0mm pad
   - Power traces: 0.8mm+ for 5V and 3.3V rails
   - Ground plane: Pour on both layers

5. **Manufacturing:**
   - 2-layer PCB (FR4)
   - 1.6mm thickness
   - HASL or ENIG finish
   - Silkscreen: Component labels + polarity marks
   - Soldermask: Standard green (or black for stealth)

---

## Notes

- **I2C Bus:** Shared between OLED (0x3C) and MCP4728 (0x60)
- **Power Budget:** 100-150mA typical, <200mA max
- **1V/Octave:** 0-5V range = 5 octaves (MIDI notes 0-60, C0-C4)
- **Input Protection:** Scales 0-5V → 0-2.62V safe for 3.3V ADC
- **S-Trig:** True switch-based (open/short to GND), not voltage
- **LED Indicators:** 150Ω resistors for ~10mA @ 3.3V logic

---

**Status:** Ready for EasyEDA PCB design! All component values, connections, and positions documented.
