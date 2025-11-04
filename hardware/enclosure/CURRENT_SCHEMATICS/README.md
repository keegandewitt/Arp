# Current Production-Ready Schematics

**Last Updated:** 2025-11-04 (Session 27)
**Purpose:** These are the FINAL, clean schematics for PCB design in EasyEDA

---

## 📋 Schematic Inventory

### 1. System Overview
| File | Purpose | Size | Use For |
|------|---------|------|---------|
| **UNIFIED_SYSTEM_SCHEMATIC_V2.svg** | Complete system interconnection diagram | 35KB | Understanding overall architecture, data flow |

### 2. Circuit Details (6 Clean Schematics from Session 25)

#### Reference Table
| File | Purpose | Size | Use For |
|------|---------|------|---------|
| **M4_PIN_ASSIGNMENTS.svg** | Pin reference table | 5.6KB | Pin allocation lookup |

#### Input Circuits (TOP PCB)
| File | Purpose | Size | Use For |
|------|---------|------|---------|
| **TOP_PCB_CV_IN.svg** | CV input voltage divider + BAT85 clamp + LED | 13KB | Breadboard wiring, PCB layout |
| **TOP_PCB_TRIG_IN.svg** | TRIG input voltage divider + BAT85 clamp + RGB LED | 18KB | Breadboard wiring, PCB layout |

#### Output Circuits (BOTTOM PCB)
| File | Purpose | Size | Use For |
|------|---------|------|---------|
| **BOTTOM_PCB_DAC_OUTPUTS.svg** | MCP4728 DAC outputs (CV, CC) + LEDs | 12KB | Breadboard wiring, PCB layout |
| **BOTTOM_PCB_STRIG.svg** | S-Trig NPN transistor circuit | 6.9KB | Breadboard wiring, PCB layout |

#### Power System
| File | Purpose | Size | Use For |
|------|---------|------|---------|
| **POWER_DISTRIBUTION.svg** | USB-C → M4 → 5V/3.3V rails (no battery!) | 14KB | Power system design |

---

## 🎯 Quick Start: Which Schematic Do I Need?

**For understanding the complete system:**
→ Start with `UNIFIED_SYSTEM_SCHEMATIC_V2.svg`

**For designing PCBs in EasyEDA:**
→ Use the 6 individual circuit schematics (TOP_PCB_*, BOTTOM_PCB_*, POWER_DISTRIBUTION)

**For breadboard wiring:**
→ Use the individual circuit schematics for each functional block

**For pin lookups:**
→ Use `M4_PIN_ASSIGNMENTS.svg` or `docs/hardware/PIN_ALLOCATION_MATRIX.md`

---

## 📐 Schematic Details

### UNIFIED_SYSTEM_SCHEMATIC_V2.svg
**What it shows:**
- Complete system architecture
- All 7 LED indicators (all white 3mm LEDs with 220Ω resistors)
- Input circuits (CV IN, TRIG IN) with voltage dividers
- Output circuits (CV OUT, TRIG OUT, CC OUT) with MCP4728 DAC
- MIDI circuits (IN/OUT) via FeatherWing
- Power distribution (USB-C only, no battery)
- All component values and pin assignments

**Key features:**
- Coordinate-planned layout (no overlapping components)
- All resistor values labeled
- LED pin assignments clearly marked
- Component summary table included
- Simplified LED system (no RGB complexity)

### M4_PIN_ASSIGNMENTS.svg
**What it shows:**
- Text-based pin reference table
- Every M4 pin and its function
- I2C, UART, ADC, GPIO assignments

**Use when:** You need to look up which pin does what

### TOP_PCB_CV_IN.svg
**What it shows:**
- CV IN jack → voltage divider (10kΩ + 10kΩ) → A3 ADC
- BAT85 diode clamp to 3.3V
- White LED indicator (D4) with 220Ω resistor
- Optional 100nF smoothing capacitor

**Protection level:** Safe up to 40V+ input

### TOP_PCB_TRIG_IN.svg
**What it shows:**
- TRIG IN jack → voltage divider (10kΩ + 10kΩ) → A4 ADC
- BAT85 diode clamp to 3.3V
- White LED indicator (D11) with 220Ω resistor
- Optional 100nF smoothing capacitor

**LED behavior:** Brightness proportional to gate voltage (PWM capable)

### BOTTOM_PCB_DAC_OUTPUTS.svg
**What it shows:**
- MCP4728 I2C DAC (address 0x60)
- Channel A: CV OUT (1V/octave) with 100Ω protection + white LED (D12)
- Channel D: CC OUT (MIDI CC → voltage) with 100Ω protection + white LED (D25)
- 5V power decoupling (47µF + 0.1µF)

**Output range:** 0-5V (5 octaves for CV)

### BOTTOM_PCB_STRIG.svg
**What it shows:**
- GPIO D10 → 220Ω resistor → 2N3904 NPN transistor
- Collector → 100Ω protection → S-Trig output jack
- White LED indicator (A0) with 220Ω resistor showing gate state

**Operation:** GPIO HIGH = jack pulls to GND (true S-Trig)

### POWER_DISTRIBUTION.svg
**What it shows:**
- USB-C connector → M4 USB pin
- M4 5V passthrough to devices
- M4 3.3V regulator (500mA capacity)
- Decoupling capacitors for both rails
- Power budget: ~75mA typical, ~120mA max (4× margin)

**Key change (Session 27):** Removed battery and powerboost - USB-only now!

---

## 🔍 LED Indicator Reference

All 7 LED indicators shown in unified schematic (all white 3mm LEDs with 220Ω resistors):

**Input LEDs (TOP PCB):**
1. D4 - CV IN activity (white, PWM capable for brightness proportional to voltage)
2. D11 - TRIG IN activity (white, PWM capable for brightness proportional to gate)

**Output LEDs (BOTTOM PCB):**
3. D12 - CV OUT activity (white, PWM capable for brightness proportional to voltage)
4. A0 - TRIG OUT gate state (white, PWM capable for brightness proportional to gate)
5. D25 - CC OUT activity (white, PWM capable for brightness proportional to voltage)

**MIDI LEDs (MIDI FeatherWing):**
6. CAN_TX - MIDI OUT activity (white, pulse on TX)
7. A5 - MIDI IN activity (white, pulse on RX)

---

## 📦 Component Summary

**Complete BOM available in:** `hardware/EASYEDA_PCB_DESIGN_GUIDE.md`

**Key components:**
- Feather M4 CAN Express (main MCU)
- MCP4728 4-channel 12-bit DAC (I2C 0x60)
- OLED FeatherWing 128×64 (I2C 0x3C) - STACKED ON TOP BOARD
- MIDI FeatherWing (UART TX/RX) - BOTTOM BOARD (not stacked, far left)
- 2× BAT85 Schottky diodes (input protection)
- 1× 2N3904 NPN transistor (S-Trig circuit)
- 7× white 3mm LEDs (all indicators simplified)
- Various resistors and capacitors (see schematics)

---

## 🗂️ Related Documentation

- **`hardware/ACTUAL_HARDWARE_TRUTH.md`** - Single source of hardware truth
- **`hardware/EASYEDA_PCB_DESIGN_GUIDE.md`** - Complete BOM and PCB guidelines
- **`docs/hardware/PIN_ALLOCATION_MATRIX.md`** - Complete pin assignment table
- **`hardware/POWER_SYSTEM_SIMPLIFICATION.md`** - USB-only power rationale

---

## 🗃️ Archived Schematics

Outdated/iterative schematics have been moved to `_archived_iterations/` folder.
These include Session 26 attempts with overlapping components and various naming iterations.

**Do not use archived schematics for PCB design!**

---

## ✅ Verification Checklist

Before using these schematics for PCB design:
- [ ] Read `hardware/ACTUAL_HARDWARE_TRUTH.md` to verify components exist
- [ ] Check `hardware/EASYEDA_PCB_DESIGN_GUIDE.md` for complete BOM
- [ ] Review power budget in `POWER_DISTRIBUTION.svg`
- [ ] Verify pin assignments match `PIN_ALLOCATION_MATRIX.md`
- [ ] Confirm USB-only power is acceptable for your use case

---

**Status:** ✅ Production-ready (LED system simplified to 7 white LEDs)
**Session:** 27 (2025-11-04)
**Next:** Use these schematics to design PCBs in EasyEDA
