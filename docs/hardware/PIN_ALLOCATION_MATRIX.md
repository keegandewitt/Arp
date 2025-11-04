# Feather M4 CAN - Pin Allocation Matrix

**SINGLE SOURCE OF TRUTH for all pin assignments**

**Last Updated:** 2025-11-02
**Hardware:** Adafruit Feather M4 CAN Express
**Purpose:** Central reference for all pin usage - prevents conflicts

---

## 🔴 CRITICAL RULE

**BEFORE using ANY pin, check this document first!**

Any code that uses GPIO pins MUST reference this matrix.

---

## Complete Pin Allocation Table

| Pin | Status | Function | Hardware | Notes |
|-----|--------|----------|----------|-------|
| **D0 (RX)** | 🔶 Reserved | MIDI In (UART RX) | MIDI FeatherWing | Not yet installed |
| **D1 (TX)** | 🔶 Reserved | MIDI Out (UART TX) | MIDI FeatherWing | Not yet installed |
| **D4** | 🔵 In Use | **CV IN LED** | **White LED (3mm)** | **Activity indicator** |
| **D5** | 🔵 In Use | Button A | OLED FeatherWing | Fire gate pulse |
| **D6** | 🔵 In Use | Button B | OLED FeatherWing | Toggle gate mode |
| **D9** | 🔵 In Use | Button C | OLED FeatherWing | (Future: pattern select) |
| **D10** | 🔵 In Use | **S-Trig GPIO** | **NPN Transistor Circuit** | **True S-Trig output** |
| **D11** | 🔵 In Use | **TRIG IN LED** | **White LED (3mm)** | **Activity indicator** |
| **D12** | 🔵 In Use | **CV OUT LED** | **White LED (3mm)** | **Activity indicator** |
| **D13** | 🔵 In Use | LED Status | Onboard LED | Visual feedback |
| **D21 (SDA)** | 🔵 In Use | I2C Data | OLED + MCP4728 | Shared bus |
| **D22 (SCL)** | 🔵 In Use | I2C Clock | OLED + MCP4728 | Shared bus |
| **D23 (MOSI)** | ✅ Available | - | - | Freed from RGB LED |
| **D24 (MISO)** | ✅ Available | - | - | Freed from RGB LED |
| **D25 (SCK)** | 🔵 In Use | **CC OUT LED** | **White LED (3mm)** | **Activity indicator** |
| **A0** | 🔵 In Use | **TRIG OUT LED** | **White LED (3mm)** | **Activity indicator** |
| **A1** | ✅ Available | - | - | Freed from RGB LED |
| **A2** | ✅ Available | - | - | Freed from RGB LED |
| **A3** | 🔵 In Use | **CV Pitch Input** | **Voltage Divider (20k/22k)** | **1V/octave (0-5V)** |
| **A4** | 🔵 In Use | **Gate Input** | **Voltage Divider (20k/22k)** | **V-Trig/S-Trig modes** |
| **A5** | 🔵 In Use | **MIDI IN LED** | **White LED (3mm)** | **RX activity indicator** |
| **NEOPIXEL** | 🔵 In Use | Onboard RGB LED | Built-in | Status indicator |
| **CAN_RX** | ✅ Available | CAN Bus RX | - | Not currently used |
| **CAN_TX** | 🔵 In Use | **MIDI OUT LED** | **White LED (3mm)** | **TX activity indicator** |

---

## I2C Device Addresses (Shared Bus: D21/D22)

| Address | Device | Status | Purpose |
|---------|--------|--------|---------|
| **0x3C** | SH1107 OLED | 🔵 In Use | 128x64 display |
| **0x60** | MCP4728 DAC | 🔵 In Use | 4-channel CV/Gate output |
| **0x4D** | MIDI FeatherWing | 🔶 Reserved | Not yet installed |

---

## MCP4728 DAC Channel Allocation

| Channel | Status | Function | Output Type | Voltage Range |
|---------|--------|----------|-------------|---------------|
| **Channel A** | 🔵 In Use | CV Pitch | 1V/octave | 0-5V (0-10V with LM358N) |
| **Channel B** | ⚪ Unused | (Reserved for future) | Unused/Floating | Leave unconnected |
| **Channel C** | 🔵 In Use | **V-Trig Gate** | Standard gate | 0V idle, 5V active |
| **Channel D** | 🔵 In Use | **CC OUT** | MIDI CC → Voltage | 0-5V |

---

## Gate/Trigger Output Matrix

| Output Type | Hardware | Control Pin/Channel | Idle State | Active State | Cable Type |
|-------------|----------|---------------------|------------|--------------|------------|
| **V-TRIG** | MCP4728 Ch C | DAC Channel C | 0V | 5V | TS (mono 1/4") |
| **S-TRIG** | NPN Transistor | GPIO D10 | Open circuit | Short to GND | TS (mono 1/4") |

**IMPORTANT:** These are **separate physical outputs** - use one OR the other, never both!

---

## CV/Gate Input Matrix

| Input Type | Pin | Hardware | Voltage Range | Detection Modes | Cable Type |
|------------|-----|----------|---------------|-----------------|------------|
| **CV Pitch** | A3 | Voltage Divider (20k/22k) | 0-5V (1V/octave) | N/A | TS (mono 1/4") |
| **Gate** | A4 | Voltage Divider (20k/22k) | 0-5V | V-Trig or S-Trig | TS (mono 1/4") |

### CV Input Voltage Divider Circuit

**Both A3 and A4 use the same protection circuit:**

```
External Input (0-5V)
    ↓
  [20kΩ] ← Series resistance (2× 10kΩ in series)
    ↓
    +--→ M4 Pin (A3 or A4)
    |
  [22kΩ] ← To ground
    |
   GND
```

**Scaling Factor:** 0.524 (22k / 42k)
**Max Safe Voltage:** 5V input → 2.62V at pin ✓

### Gate Input Modes

| Mode | Detection Logic | Use Case |
|------|----------------|----------|
| **V-Trig** | Voltage >2.0V = gate HIGH | Modern modular (Eurorack) |
| **S-Trig** | Voltage <1.0V = gate HIGH (inverted) | Vintage modular (Moog, ARP) |

**IMPORTANT:** The voltage divider is required for BOTH modes because external S-Trig sources may pull the idle state to 5V, 12V, or higher voltages.

---

## Button Mapping (OLED FeatherWing)

| Button | Pin | Current Function | Future Function |
|--------|-----|------------------|-----------------|
| **A** | D5 | Fire gate pulse | Pattern select |
| **B** | D6 | Toggle V-TRIG/S-TRIG | Tempo/Division |
| **C** | D9 | (Unused in gate test) | Settings menu |

---

## Pin Usage Statistics

- **Total GPIO Pins:** 26
- **Currently In Use:** 17 pins
  - **Buttons:** D5, D6, D9 (3 pins)
  - **S-Trig Circuit:** D10 (1 pin)
  - **I2C Bus:** D21, D22 (2 pins)
  - **CV/Gate Inputs:** A3, A4 (2 pins)
  - **LED Indicators:** D4, D11, D12, D25, A0, A5, CAN_TX (7 pins - all white LEDs)
  - **Status LEDs:** D13, NEOPIXEL (2 pins)
- **Reserved:** 2 (D0, D1 for MIDI)
- **Available:** 7 pins (CAN_RX, D23, D24, A1, A2, + 2 others)

---

## Future Pin Allocation Plan

### High Priority (Next Phase)

| Pin | Planned Use | Hardware Needed |
|-----|-------------|-----------------|
| D0, D1 | MIDI In/Out | MIDI FeatherWing (stack on) |
| A2 | Tempo potentiometer | 10kΩ pot |

### Medium Priority

| Pin | Planned Use | Hardware Needed |
|-----|-------------|-----------------|
| A5 | Gate length/Swing pot | 10kΩ pot |
| D11 | Encoder A | Rotary encoder |
| D12 | Encoder B | Rotary encoder |

### Low Priority (Expansion)

| Pin | Planned Use | Hardware Needed |
|-----|-------------|-----------------|
| D23-D25 | SPI (SD card?) | SD card module |
| CAN_RX/TX | CAN bus | CAN transceiver |

---

## Adding New Pin Usage

**Before using a new pin:**

1. ✅ Check this document - is the pin available?
2. ✅ Update this table with new usage
3. ✅ Commit changes to git
4. ✅ Update any affected code comments

**Template for adding pins:**
```markdown
| **DXX** | 🔵 In Use | [Function] | [Hardware] | [Notes] |
```

**Status Legend:**
- 🔵 **In Use** - Currently active in code
- 🔶 **Reserved** - Planned but not yet implemented
- ✅ **Available** - Free to use

---

## Pin Conflict Prevention

**Common conflicts to avoid:**

1. ❌ **Don't use D0/D1** - Reserved for MIDI FeatherWing
2. ❌ **Don't use D21/D22** - Shared I2C bus only
3. ❌ **Don't reassign button pins** - UI consistency
4. ❌ **Don't use D13 for input** - It's the onboard LED
5. ✅ **Always check this document first**

---

## S-Trig Circuit Detail

**Pin D10 drives NPN transistor:**

```
D10 (GPIO) → 1kΩ resistor → Transistor BASE
                             Transistor EMITTER → GND
                             Transistor COLLECTOR → S-Trig TIP
```

**Control logic:**
- `D10 = LOW (0V)` → Transistor OFF → S-Trig IDLE (open circuit)
- `D10 = HIGH (3.3V)` → Transistor ON → S-Trig ACTIVE (short to GND)

---

## Related Documentation

- **Hardware Build:** `docs/hardware/HARDWARE_BUILD_GUIDE.md`
- **I2C Architecture:** `docs/hardware/I2C_ARCHITECTURE.md`
- **S-Trig Circuit:** `docs/hardware/TRUE_STRIG_CIRCUIT.md`
- **Breadboard Wiring:** `docs/hardware/STRIG_BREADBOARD_GUIDE.md`
- **CV Input System:** `docs/hardware/CV_INPUT_SYSTEM.md`

---

## LED Indicator System (Simplified 2025-11-04)

### Complete LED Pin Mapping - All White 3mm LEDs

| Jack | LED Type | GPIO Pin | Board | Resistor | Behavior |
|------|----------|----------|-------|----------|----------|
| **CV IN** | White 3mm | D4 | TOP | 220Ω | ON when voltage detected on A3 |
| **TRIG IN** | White 3mm | D11 | TOP | 220Ω | ON when voltage detected on A4 |
| **CV OUT** | White 3mm | D12 | BOTTOM | 220Ω | ON when DAC Ch A active |
| **TRIG OUT** | White 3mm | A0 | BOTTOM | 220Ω | ON when gate output active |
| **CC OUT** | White 3mm | D25 | BOTTOM | 220Ω | ON when DAC Ch D active |
| **MIDI OUT** | White 3mm | CAN_TX | BOTTOM | 220Ω | Pulse on UART TX activity |
| **MIDI IN** | White 3mm | A5 | BOTTOM | 220Ω | Pulse on UART RX activity |

### Hardware Specifications

**White LEDs (7 total):**
- Type: 3mm flat-top clear high-efficiency
- Forward voltage: ~3.0V
- Current limiting: 220Ω resistor per LED
- Operating current: ~2mA @ 3.3V GPIO
- Power per LED: ~7mW

**Total Power Budget:**
- White LEDs: 7 × 2mA = 14mA
- **Total typical: ~14mA** (negligible load on USB 3.3V regulator)

### Physical Mounting

- **LED position:** 7mm to the right of each jack center
- **Hole diameter:** 3.2mm (press-fit for 3mm LEDs)
- **LED style:** Flat-top (wide viewing angle, flush mounting)
- **Wiring:** Leads soldered directly to protoboard traces
- **Current limiting:** 220Ω resistors on each LED/channel

### Software Detection Logic

1. **Input Monitoring (CV IN, TRIG IN):**
   - Periodic ADC sampling @ 100Hz
   - Threshold detection for activity
   - Optional: PWM brightness proportional to voltage level

2. **Output Status (CV OUT, TRIG OUT, CC OUT):**
   - Direct software control based on internal state
   - Real-time reflection of DAC/GPIO output state
   - Optional: PWM brightness proportional to output voltage

3. **MIDI Activity (MIDI IN, MIDI OUT):**
   - UART buffer monitoring
   - Pulse on message detection (50-100ms)
   - Debouncing to prevent flicker

---

**Last Updated:** 2025-11-04 (simplified to 7 white LEDs, removed RGB complexity)
**Status:** Active - reference this document for ALL pin usage decisions

**END OF MATRIX**
