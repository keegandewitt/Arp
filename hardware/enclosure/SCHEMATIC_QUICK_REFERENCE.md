# PRISME Schematic Quick Reference

**Date:** 2025-11-03 (Session 25)
**Purpose:** Guide to the clean, organized schematics for EasyEDA PCB design

---

## 📁 Schematic Files (Use These!)

### 1. **M4_PIN_ASSIGNMENTS.svg** (START HERE)
- **Purpose:** Complete M4 pin reference
- **Shows:** Every connection between M4 and your custom PCBs
- **Use for:** Understanding which M4 pins connect where
- **Format:** Text-based reference (no circuit diagram)

**Key Info:**
- Power: USB (5V), 3V3 (3.3V), GND
- I2C: SDA, SCL (shared with OLED and DAC)
- UART: RX, TX (MIDI Wing)
- ADC: A3 (CV IN), A4 (TRIG IN)
- GPIO: D4, D10, D11, D23, D24 (LEDs + S-Trig)

---

### 2. **TOP_PCB_CV_IN.svg** (Input Board - CV Circuit)
- **Purpose:** CV input protection circuit
- **Shows:** Voltage divider, BAT85 clamp, LED indicator
- **PCB:** Top board (input board)

**Components:**
- R1, R2: 10kΩ voltage divider (5V → 2.5V)
- D1: BAT85 Schottky diode (clamp to 3.7V max)
- R3: 1kΩ LED current limit
- LED1: White 3mm LED
- C15: 100nF smoothing (optional)
- Jack: 3.5mm TS mono

**Connections to M4:**
- TAP → M4 Pin A3 (ADC input)
- LED anode ← M4 Pin D4 (GPIO output)
- 3.3V ← M4 3V3 (BAT85 clamp reference)
- GND → M4 GND

---

### 3. **TOP_PCB_TRIG_IN.svg** (Input Board - TRIG Circuit)
- **Purpose:** TRIG input protection circuit
- **Shows:** Voltage divider, BAT85 clamp, RGB LED indicator
- **PCB:** Top board (input board)

**Components:**
- R4, R5: 10kΩ voltage divider (5V → 2.5V)
- D2: BAT85 Schottky diode (clamp to 3.7V max)
- R6: 330Ω RGB LED current limit (×3 channels)
- LED2: RGB 5mm common cathode
- C16: 100nF smoothing (optional)
- Jack: 3.5mm TS mono

**Connections to M4:**
- TAP → M4 Pin A4 (ADC input)
- LED Red ← M4 Pin D11 (GPIO)
- LED Green ← M4 Pin D23 (GPIO)
- LED Blue ← M4 Pin D24 (GPIO)
- 3.3V ← M4 3V3 (BAT85 clamp reference)
- GND → M4 GND

---

### 4. **BOTTOM_PCB_DAC_OUTPUTS.svg** (Output Board - DAC)
- **Purpose:** CV, TRIG, CC output circuits via MCP4728 DAC
- **Shows:** DAC connections, output protection resistors
- **PCB:** Bottom board (output board)

**MCP4728 Connections:**
- VDD ← 5V (CRITICAL: Needs 5V for 0-5V output)
- GND → Common ground
- SDA ← M4 SDA (I2C, shared with OLED)
- SCL ← M4 SCL (I2C, shared with OLED)
- I2C Address: 0x60 (factory default)

**Outputs:**
- Channel A (VA) → R1 (100Ω) → CV OUT jack
- Channel B (VB) → R2 (100Ω) → TRIG OUT jack (V-Trig mode)
- Channel C (VC) → R3 (100Ω) → CC OUT jack
- Channel D (VD) → Available for future expansion

**Output Specs:**
- Range: 0-5V (5 octaves, C0 to C5)
- Standard: 1V/octave Eurorack
- Resolution: 12-bit (4096 steps)

**Connections to M4:**
- SDA ← M4 SDA
- SCL ← M4 SCL
- 5V ← M4 USB
- GND → M4 GND

---

### 5. **BOTTOM_PCB_STRIG.svg** (Output Board - S-Trig)
- **Purpose:** S-Trig output (switch to ground for vintage synths)
- **Shows:** NPN transistor switching circuit
- **PCB:** Bottom board (output board)

**Components:**
- Q1: 2N3904 NPN transistor (TO-92)
- R8: 1kΩ base resistor (GPIO protection)
- R9: 100Ω collector resistor (output protection)
- Jack: Same as TRIG OUT (user selects V-Trig or S-Trig in software)

**Operation:**
- D10 LOW (0V): Transistor OFF, jack tip OPEN (idle)
- D10 HIGH (3.3V): Transistor ON, jack tip to GND (triggered)

**Connections to M4:**
- Base ← M4 Pin D10 (via R8 1kΩ)
- GND → M4 GND

**Compatible with:** ARP, Korg MS-20, Yamaha CS vintage synths

---

### 6. **POWER_DISTRIBUTION.svg** (Both Boards)
- **Purpose:** Power rail decoupling for both PCBs
- **Shows:** Capacitor placement for clean power
- **PCB:** Both top and bottom boards

**5V Rail (Powers DAC):**
- Top board: C11 (10µF bulk) + C12 (0.1µF bypass)
- Bottom board: C1 (47µF bulk) + C2 (0.1µF bypass)
- Source: M4 USB pin

**3.3V Rail (Powers MIDI, OLED, LEDs, BAT85 clamps):**
- Top board: C13 (10µF bulk) + C14 (0.1µF bypass)
- Bottom board: C9 (10µF bulk) + C10 (0.1µF bypass)
- Source: M4 3V3 pin

**CRITICAL:**
- Both rails MUST be present on BOTH boards
- Place bulk caps near power entry points
- Place bypass caps near ICs

---

## 🎯 For EasyEDA PCB Design

### Step 1: Reference M4_PIN_ASSIGNMENTS.svg
- Understand which M4 pins you need to connect
- Know which signals go to which board

### Step 2: Design Top PCB (Input Board)
- Reference: TOP_PCB_CV_IN.svg + TOP_PCB_TRIG_IN.svg
- Add connection pads labeled: `M4_A3`, `M4_A4`, `M4_D4`, `M4_D11`, `M4_D23`, `M4_D24`, `M4_5V`, `M4_3V3`, `M4_GND`
- Place components per schematics
- Add power decoupling per POWER_DISTRIBUTION.svg

### Step 3: Design Bottom PCB (Output Board)
- Reference: BOTTOM_PCB_DAC_OUTPUTS.svg + BOTTOM_PCB_STRIG.svg
- Add connection pads labeled: `M4_SDA`, `M4_SCL`, `M4_D10`, `M4_5V`, `M4_3V3`, `M4_GND`
- Place MCP4728 DAC footprint
- Add output jacks and protection resistors
- Add S-Trig transistor circuit
- Add power decoupling per POWER_DISTRIBUTION.svg

### Step 4: Physical Assembly
- Wire PCB pads to M4 pins using jumpers or stacking headers
- M4, MIDI Wing, OLED Wing are pre-built (don't need PCBs)

---

## 📋 Complete Component List by Board

### Top PCB (Input Board):
- 2× 10kΩ resistors (R1, R2) - CV divider
- 2× 10kΩ resistors (R4, R5) - TRIG divider
- 2× BAT85 diodes (D1, D2) - Protection clamps
- 1× 1kΩ resistor (R3) - CV LED
- 3× 330Ω resistors (R6) - RGB LED channels
- 1× White LED (LED1)
- 1× RGB LED (LED2)
- 2× 100nF capacitors (C15, C16) - Optional smoothing
- 1× 10µF capacitor (C11) - 5V bulk
- 1× 0.1µF capacitor (C12) - 5V bypass
- 1× 10µF capacitor (C13) - 3.3V bulk
- 1× 0.1µF capacitor (C14) - 3.3V bypass
- 2× 3.5mm TS jacks - CV IN, TRIG IN
- 9× connection pads - To M4 pins

### Bottom PCB (Output Board):
- 1× MCP4728 DAC - I2C 4-ch 12-bit
- 1× 2N3904 NPN transistor (Q1) - S-Trig
- 3× 100Ω resistors (R1, R2, R3) - DAC output protection
- 1× 100Ω resistor (R9) - S-Trig collector
- 1× 1kΩ resistor (R8) - Transistor base
- 1× 47µF capacitor (C1) - 5V bulk
- 1× 0.1µF capacitor (C2) - 5V bypass
- 1× 10µF capacitor (C9) - 3.3V bulk
- 1× 0.1µF capacitor (C10) - 3.3V bypass
- 3× 3.5mm TS jacks - CV OUT, TRIG OUT, CC OUT
- 1× USB-C breakout - Power input (Adafruit 4090)
- 6× connection pads - To M4 pins

---

## ✅ Ready for EasyEDA

You now have:
- ✅ Clean, focused schematics (6 files)
- ✅ Complete M4 pin reference
- ✅ Component values for every part
- ✅ Power distribution guide
- ✅ Connection pad labels
- ✅ Complete BOM

**Start with M4_PIN_ASSIGNMENTS.svg to understand the system, then use the individual circuit schematics to build your PCB layouts in EasyEDA.**

---

**Files to Use:**
```
hardware/enclosure/
├── M4_PIN_ASSIGNMENTS.svg          ← Start here
├── TOP_PCB_CV_IN.svg               ← Input board CV circuit
├── TOP_PCB_TRIG_IN.svg             ← Input board TRIG circuit
├── BOTTOM_PCB_DAC_OUTPUTS.svg      ← Output board DAC
├── BOTTOM_PCB_STRIG.svg            ← Output board S-Trig
└── POWER_DISTRIBUTION.svg          ← Both boards power
```

**Design Guide:**
```
hardware/
└── EASYEDA_PCB_DESIGN_GUIDE.md     ← Complete BOM + layout guidelines
```

**Good luck with your PCB design!**
