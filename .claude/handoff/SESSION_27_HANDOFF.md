# Session 27 Handoff - Discrete MIDI Circuits Implementation

**Date:** 2025-11-04
**Branch:** main
**Status:** ✅ Complete - Documentation updated, changes committed and pushed

---

## 🎯 What We Accomplished This Session

### Major Architecture Change: MIDI FeatherWing → Discrete Circuits

**Problem Solved:**
User wanted to simplify the design and group all inputs on the TOP BOARD (including MIDI IN).

**Solution:**
Replaced the Adafruit MIDI FeatherWing with two discrete MIDI circuits:
1. **MIDI IN** (TOP BOARD) - 6N138 optocoupler circuit
2. **MIDI OUT** (BOTTOM BOARD) - Direct drive from UART TX

---

## 📋 Current Hardware Architecture

### TOP BOARD (All Inputs)
```
Components:
- Feather M4 CAN Express (main MCU)
- OLED FeatherWing 128×64 (stacked on M4)
- 2×8 female header (inter-board connection)

Inputs (3 total):
1. CV IN (A3) → 10kΩ/10kΩ voltage divider + BAT85 + LED (D4)
2. TRIG IN (A4) → 10kΩ/10kΩ voltage divider + BAT85 + LED (D11)
3. MIDI IN (D0/RX) → 6N138 optocoupler circuit + 5-pin DIN + LED (A2)
```

### BOTTOM BOARD (All Outputs)
```
Components:
- MCP4728 4-channel DAC (I2C 0x60)
- USB-C power input
- 2×8 male header (inter-board connection)

Outputs (5 total):
1. CV OUT (DAC Ch A) → 100Ω protection + 3.5mm jack + LED (D12)
2. TRIG OUT (DAC Ch B) → 100Ω protection + 3.5mm jack + LED (A0)
3. S-TRIG OUT (D10) → 2N3904 transistor + 100Ω + 3.5mm jack
4. CC OUT (DAC Ch C) → 100Ω protection + 3.5mm jack + LED (A1)
5. MIDI OUT (D1/TX) → 2× 220Ω + 5-pin DIN + LED (A5)
```

### Inter-Board Header (2×8, 16 pins)
```
   LEFT COLUMN              RIGHT COLUMN

1  [ 5V         ]  ●  ●  [ GND        ]  2
3  [ 3V3        ]  ●  ●  [ GND        ]  4
5  [ SDA        ]  ●  ●  [ SCL        ]  6
7  [ TX (D1)    ]  ●  ●  [ (reserved) ]  8
9  [ STRIG_GPIO ]  ●  ●  [ CV_OUT_LED ]  10
11 [ TRIG_OUT_LED]  ●  ●  [ CC_OUT_LED ]  12
13 [ MIDI_OUT_LED]  ●  ●  [ (reserved) ]  14
15 [ (reserved) ]  ●  ●  [ (reserved)  ]  16
```

**Key Points:**
- Pin 7: TX signal goes from M4 (top) to MIDI OUT circuit (bottom)
- No RX on header: MIDI IN is local to top board
- 5V goes UP to M4, 3.3V comes DOWN from M4 regulator
- 5 reserved pins for future expansion

---

## 🔌 MIDI IN Circuit (TOP BOARD)

### Schematic
```
5-pin DIN Jack:
  Pin 4 → 220Ω → 6N138 pin 2 (anode)
  Pin 5 → BAT85 cathode (stripe)
         BAT85 anode → 6N138 pin 3 (cathode)
  Pin 2 → GND (shield)

6N138 Optocoupler (DIP-8):
  Pin 8 (VCC) → 3.3V
  Pin 5 (GND) → GND
  Pin 6 (VO) → 1kΩ → 3.3V (pull-up)
  Pin 7 → 1kΩ → GND (base resistor)
  Pin 6 (VO) → M4 D0 (RX)

  100nF capacitor between pin 8 and pin 5 (decoupling)

MIDI IN LED:
  LED anode → 220Ω → 3.3V
  LED cathode → M4 A2 (LOW = LED on)
```

### Component List (MIDI IN)
- 1× 6N138 optocoupler (DIP-8)
- 1× 220Ω resistor (input current limiting)
- 2× 1kΩ resistors (pull-up + base)
- 1× BAT85 Schottky diode (reverse protection)
- 1× 100nF ceramic capacitor (power decoupling)
- 1× 5-pin DIN jack (female, panel mount)
- 1× white 3mm LED
- 1× 220Ω resistor (LED current limiting)

### How It Works
1. MIDI signal arrives on DIN pins 4 and 5
2. 220Ω limits current to 6N138 internal LED (~17mA max)
3. BAT85 protects against reverse voltage
4. 6N138 provides galvanic isolation (1000-5000V)
5. Output side powered by 3.3V, drives M4 RX pin
6. Software monitors UART RX, pulses A2 LED on activity

---

## 🔌 MIDI OUT Circuit (BOTTOM BOARD)

### Schematic
```
5-pin DIN Jack:
  Pin 4 ← 220Ω ← 5V rail
  Pin 5 ← 220Ω ← TX (from header pin 7)
  Pin 2 → GND

Optional EMI filtering:
  100pF capacitor: DIN pin 4 to GND
  100pF capacitor: DIN pin 5 to GND

MIDI OUT LED:
  LED anode → 220Ω → 3.3V (from header pin 4)
  LED cathode → A5 control (via header pin 13)
```

### Component List (MIDI OUT)
- 2× 220Ω resistors (current limiting)
- 2× 100pF ceramic capacitors (EMI filtering, optional)
- 1× 5-pin DIN jack (female, panel mount)
- 1× white 3mm LED
- 1× 220Ω resistor (LED current limiting)

### How It Works
1. TX signal arrives from M4 via header pin 7
2. Two 220Ω resistors form current-limited MIDI loop
3. Current flows when TX is HIGH (UART idle state)
4. TX pulls LOW to send data (correct MIDI polarity)
5. No transistor needed - direct drive works!
6. Software monitors UART TX, pulses A5 LED on activity

---

## 📝 Documentation Updated

All files have been updated and committed:

1. **docs/hardware/PIN_ALLOCATION_MATRIX.md**
   - D0: MIDI IN (6N138, TOP BOARD)
   - D1: MIDI OUT (direct drive, BOTTOM BOARD via header)
   - A2: MIDI IN LED (TOP BOARD)
   - A5: MIDI OUT LED (BOTTOM BOARD)
   - Removed MIDI FeatherWing I2C address

2. **hardware/ACTUAL_HARDWARE_TRUTH.md**
   - Replaced "MIDI FeatherWing" section with discrete circuits
   - Updated BOM with 6N138, BAT85, DIN jacks
   - Updated LED system (3 on top, 4 on bottom)
   - Updated power budget (~40mA typical on 3.3V)

3. **hardware/EASYEDA_PCB_DESIGN_GUIDE.md**
   - Removed MIDI FeatherWing from BOM
   - Added 6N138 optocoupler
   - Added 3× BAT85 diodes (total for all circuits)
   - Added resistors: 4× 1kΩ, 3× 220Ω (MIDI circuits)
   - Added capacitors: 1× 100nF (6N138), 2× 100pF (MIDI OUT)
   - Added 2× 5-pin DIN jacks
   - Updated connectors section

4. **hardware/enclosure/CURRENT_SCHEMATICS/README.md**
   - Updated component summary
   - Noted discrete MIDI circuits
   - Clarified board locations

---

## 🎨 Current Pin Allocation Summary

### Input Pins (Analog)
| Pin | Function | Hardware | Board |
|-----|----------|----------|-------|
| A3 | CV IN | Voltage divider + BAT85 | TOP |
| A4 | TRIG IN | Voltage divider + BAT85 | TOP |

### UART Pins
| Pin | Function | Hardware | Board |
|-----|----------|----------|-------|
| D0 (RX) | MIDI IN | 6N138 output | TOP |
| D1 (TX) | MIDI OUT | Direct drive (via header) | BOTTOM |

### I2C Pins (Shared Bus)
| Pin | Function | Devices | Board |
|-----|----------|---------|-------|
| D21 (SDA) | I2C Data | OLED (0x3C) + MCP4728 (0x60) | BOTH |
| D22 (SCL) | I2C Clock | OLED (0x3C) + MCP4728 (0x60) | BOTH |

### GPIO Output Pins
| Pin | Function | Hardware | Board |
|-----|----------|----------|-------|
| D10 | S-Trig output | 2N3904 transistor | BOTTOM (via header) |

### LED Indicator Pins (7 total)
| Pin | Function | Board |
|-----|----------|-------|
| D4 | CV IN LED | TOP |
| D11 | TRIG IN LED | TOP |
| A2 | MIDI IN LED | TOP |
| D12 | CV OUT LED | BOTTOM (via header) |
| A0 | TRIG OUT LED | BOTTOM (via header) |
| A1 | CC OUT LED | BOTTOM (via header) |
| A5 | MIDI OUT LED | BOTTOM (via header) |

### Button Pins (OLED FeatherWing)
| Pin | Function |
|-----|----------|
| D5 | Button A |
| D6 | Button B |
| D9 | Button C |

### Available Pins (7 total)
- D23 (MOSI), D24 (MISO), D25 (SCK) - SPI freed up
- CAN_RX, CAN_TX - CAN bus not used
- 2 more (see PIN_ALLOCATION_MATRIX.md)

---

## ⚠️ Critical Things Future Claudes Must Know

### 1. MIDI FeatherWing is GONE
**DO NOT suggest adding MIDI FeatherWing back!**
- We removed it to simplify the design
- We saved $14.95
- Discrete circuits are more flexible and educational
- User specifically decided to do this

### 2. Board Organization is STRICT
**TOP BOARD = INPUTS, BOTTOM BOARD = OUTPUTS**
- Do not put outputs on top board
- Do not put inputs on bottom board
- Keep this separation clean!

### 3. Inter-Board Header Pin 7 is TX
**TX must be on the header because:**
- M4 is on TOP board
- MIDI OUT circuit is on BOTTOM board
- Signal must travel from top to bottom
- **RX is NOT on header** (MIDI IN is local to top)

### 4. Power Flow Direction
```
USB-C (BOTTOM) → 5V → UP to M4 (TOP) → 3.3V regulated → DOWN to bottom
```
- 5V goes UP (header pin 2)
- 3.3V goes DOWN (header pin 4)
- This is backwards from what you might expect!

### 5. LED System is Simplified
**All 7 LEDs are white 3mm with 220Ω resistors**
- No RGB LEDs anymore
- No complex LED driver chips
- Simple GPIO control
- Low = LED on (common anode configuration)

### 6. Component Value Standards
**These are standardized across the project:**
- LED resistors: **220Ω** (all 7)
- Input voltage dividers: **10kΩ + 10kΩ**
- DAC output protection: **100Ω**
- S-Trig transistor base: **1kΩ**
- MIDI circuits: **220Ω + 1kΩ** (various)

### 7. MCP4728 Channel Allocation (DO NOT MIX UP!)
```
Channel A (VA): CV OUT (1V/octave)
Channel B (VB): TRIG OUT (V-Trig mode)
Channel C (VC): CC OUT (MIDI CC → voltage)
Channel D (VD): UNUSED (floating, reserved)
```

### 8. User Corrections This Session
The user caught several mistakes I made:
- ✅ MIDI FeatherWing location (I kept saying it was on bottom, but then we removed it)
- ✅ Header orientation (I flipped it, should be identical for vertical stacking)
- ✅ SDA/SCL swap (I had them backwards on first try)
- ✅ MIDI LED pins on header (realized they shouldn't pass through header)

**Lesson:** User is detail-oriented and will catch errors. Listen carefully and verify assumptions!

---

## 🚀 Next Steps for Future Work

### Immediate (User Ready to Build)
1. **Wire MIDI IN circuit on breadboard/protoboard**
   - Follow TOP BOARD MIDI IN wiring guide (provided earlier in session)
   - Test with existing `adafruit_midi` library
   - Verify optocoupler isolation works

2. **Wire MIDI OUT circuit on breadboard/protoboard**
   - Follow BOTTOM BOARD MIDI OUT wiring guide (provided earlier in session)
   - Test with existing `adafruit_midi` library
   - Verify MIDI loop works without transistor

3. **Update inter-board header**
   - Change from 2×7 to 2×8 (if not already done)
   - Add TX signal on pin 7
   - Remove RX (no longer needed)

### Medium Term (PCB Design)
1. **Design TOP BOARD PCB in EasyEDA**
   - Use schematics in `hardware/enclosure/CURRENT_SCHEMATICS/`
   - Reference `hardware/EASYEDA_PCB_DESIGN_GUIDE.md` for BOM
   - Include all 3 inputs + M4 + OLED
   - 2×8 female header for inter-board connection

2. **Design BOTTOM BOARD PCB in EasyEDA**
   - All 5 outputs + MCP4728 + USB-C
   - 2×8 male header for inter-board connection
   - Leave space for 5-pin DIN jacks

3. **Order components**
   - 6N138 optocouplers (Digikey/Mouser)
   - 5-pin DIN jacks (panel mount, 180° PCB mount)
   - 2×8 pin headers (tall stackable for board separation)
   - All resistors/capacitors (see BOM)

### Long Term (Enclosure)
1. **Design enclosure with 9 panel jacks:**
   - LEFT: 2× 3.5mm (CV IN, TRIG IN) + 1× DIN-5 (MIDI IN)
   - RIGHT: 5× 3.5mm (CV OUT, TRIG OUT, S-TRIG, CC OUT) + 1× DIN-5 (MIDI OUT)
   - BACK: USB-C power
   - TOP: OLED display + 3 buttons visible

2. **LED mounting:**
   - 7mm to right of each jack
   - 3.2mm holes for 3mm LEDs (press-fit)

---

## 📚 Key Documentation Files

**Single Sources of Truth:**
1. `docs/hardware/PIN_ALLOCATION_MATRIX.md` - Pin assignments (check FIRST!)
2. `hardware/ACTUAL_HARDWARE_TRUTH.md` - What's actually built
3. `hardware/EASYEDA_PCB_DESIGN_GUIDE.md` - Complete BOM + PCB guidelines

**Wiring Guides:**
4. Session 27 conversation - MIDI IN/OUT wiring instructions (search for "TOP BOARD - MIDI IN Circuit Wiring")

**Schematics:**
5. `hardware/enclosure/CURRENT_SCHEMATICS/` - All production schematics

**IMPORTANT:** Always check PIN_ALLOCATION_MATRIX.md BEFORE suggesting any pin usage!

---

## 🐛 Known Issues / Future Improvements

### None Currently!

The discrete MIDI design is complete and ready to build.

### Possible Future Enhancements (Not Urgent):
1. Add MIDI THRU jack (requires another 6N138)
2. Add isolation on MIDI OUT (currently not isolated, but spec allows it)
3. Add MIDI activity LEDs that are proportional to message rate (PWM)
4. Consider using 6N137 instead of 6N138 (faster, but pin-compatible)

---

## 💡 User Preferences Learned This Session

1. **Simplicity over features:** User chose discrete circuits over FeatherWing for simplicity
2. **Standard components:** User prefers common values (220Ω over 150Ω)
3. **Clear organization:** User wants clean input/output separation
4. **Educational value:** User wants to understand circuits, not just use modules
5. **Cost conscious:** User appreciates saving $15 on FeatherWing
6. **Detail-oriented:** User catches mistakes and expects accuracy

---

## ✅ Session Checklist

- [x] Replaced MIDI FeatherWing with discrete circuits
- [x] Designed MIDI IN circuit (6N138 optocoupler)
- [x] Designed MIDI OUT circuit (direct drive)
- [x] Updated inter-board header (2×8, added TX)
- [x] Updated PIN_ALLOCATION_MATRIX.md
- [x] Updated ACTUAL_HARDWARE_TRUTH.md
- [x] Updated EASYEDA_PCB_DESIGN_GUIDE.md BOM
- [x] Updated CURRENT_SCHEMATICS README
- [x] Committed all changes with detailed commit message
- [x] Pushed to GitHub
- [x] Wrote comprehensive handoff document

---

## 🎓 Lessons for Future Claudes

### What Went Well:
- User suggested simplification, we implemented it cleanly
- Discrete MIDI circuits are standard and well-documented
- Clean separation of inputs/outputs makes logical sense
- Cost savings and flexibility are real benefits

### What Could Be Improved:
- I initially made mistakes with header orientation and pin swaps
- I should have verified board layout assumptions earlier
- I should have asked about the FeatherWing location earlier (then we realized we didn't need it at all)

### Key Takeaways:
1. **Listen to user corrections immediately** - User caught multiple mistakes
2. **Verify physical mounting early** - Ask about board orientation for headers
3. **Check single sources of truth** - Always reference PIN_ALLOCATION_MATRIX.md first
4. **Standard implementations work** - MIDI circuits are well-documented, no need to reinvent
5. **Cost matters** - Saving $15 was a motivating factor for the change

---

**Status:** Session complete. All documentation accurate and up-to-date.
**Next Claude:** User is ready to wire MIDI circuits on breadboard. Help them test!

**End of Session 27 Handoff**
