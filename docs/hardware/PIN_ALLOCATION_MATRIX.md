# Feather M4 CAN - Pin Allocation Matrix

**SINGLE SOURCE OF TRUTH for all pin assignments**

**Last Updated:** 2025-10-31
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
| **D4** | ✅ Available | - | - | Free for future use |
| **D5** | 🔵 In Use | Button A | OLED FeatherWing | Fire gate pulse |
| **D6** | 🔵 In Use | Button B | OLED FeatherWing | Toggle gate mode |
| **D9** | 🔵 In Use | Button C | OLED FeatherWing | (Future: pattern select) |
| **D10** | 🔵 In Use | **S-Trig GPIO** | **NPN Transistor Circuit** | **True S-Trig output** |
| **D11** | ✅ Available | - | - | Free for future use |
| **D12** | ✅ Available | - | - | Free for future use |
| **D13** | 🔵 In Use | LED Status | Onboard LED | Visual feedback |
| **D21 (SDA)** | 🔵 In Use | I2C Data | OLED + MCP4728 | Shared bus |
| **D22 (SCL)** | 🔵 In Use | I2C Clock | OLED + MCP4728 | Shared bus |
| **D23 (MOSI)** | ✅ Available | SPI (future) | - | Reserved for expansion |
| **D24 (MISO)** | ✅ Available | SPI (future) | - | Reserved for expansion |
| **D25 (SCK)** | ✅ Available | SPI (future) | - | Reserved for expansion |
| **A0** | ✅ Available | ADC/DAC | - | Free (can do analog I/O) |
| **A1** | ✅ Available | ADC/DAC | - | Free (can do analog I/O) |
| **A2** | ✅ Available | ADC | - | Free (analog input only) |
| **A3** | ✅ Available | ADC | - | Free (analog input only) |
| **A4** | ✅ Available | ADC | - | Free (analog input only) |
| **A5** | ✅ Available | ADC | - | Free (analog input only) |
| **NEOPIXEL** | 🔵 In Use | Onboard RGB LED | Built-in | Status indicator |
| **CAN_RX** | ✅ Available | CAN Bus RX | - | Not currently used |
| **CAN_TX** | ✅ Available | CAN Bus TX | - | Not currently used |

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
| **Channel B** | ✅ Available | CV Velocity | (Future) | 0-5V |
| **Channel C** | 🔵 In Use | **V-Trig Gate** | Standard gate | 0V idle, 5V active |
| **Channel D** | ✅ Available | Trigger/Accent | (Future) | 0-5V |

---

## Gate/Trigger Output Matrix

| Output Type | Hardware | Control Pin/Channel | Idle State | Active State | Cable Type |
|-------------|----------|---------------------|------------|--------------|------------|
| **V-TRIG** | MCP4728 Ch C | DAC Channel C | 0V | 5V | TS (mono 1/4") |
| **S-TRIG** | NPN Transistor | GPIO D10 | Open circuit | Short to GND | TS (mono 1/4") |

**IMPORTANT:** These are **separate physical outputs** - use one OR the other, never both!

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
- **Currently In Use:** 8 (D5, D6, D9, D10, D13, D21, D22, NEOPIXEL)
- **Reserved:** 2 (D0, D1 for MIDI)
- **Available:** 16 pins remaining

---

## Future Pin Allocation Plan

### High Priority (Next Phase)

| Pin | Planned Use | Hardware Needed |
|-----|-------------|-----------------|
| D0, D1 | MIDI In/Out | MIDI FeatherWing (stack on) |
| A2 | Tempo potentiometer | 10kΩ pot |
| A3 | Pattern select pot | 10kΩ pot |

### Medium Priority

| Pin | Planned Use | Hardware Needed |
|-----|-------------|-----------------|
| A4 | Gate length pot | 10kΩ pot |
| A5 | Swing amount pot | 10kΩ pot |
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

---

**Last Updated:** 2025-10-31
**Status:** Active - reference this document for ALL pin usage decisions

**END OF MATRIX**
