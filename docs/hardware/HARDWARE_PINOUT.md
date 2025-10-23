# Hardware Pinout Diagram

## M4 Express + FeatherWings Connection Guide

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    ADAFRUIT M4 EXPRESS (Base Board)                       ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌─────────────────────────────────────────────────────────────────────┐  ║
║  │                         OLED FeatherWing                            │  ║
║  │                         (128x32 OLED)                               │  ║
║  ├─────────────────────────────────────────────────────────────────────┤  ║
║  │  SCL  ───────────────────────── board.SCL (I2C Clock)              │  ║
║  │  SDA  ───────────────────────── board.SDA (I2C Data)               │  ║
║  │  D9   ───────────────────────── Button A (Previous Pattern)        │  ║
║  │  D6   ───────────────────────── Button B (Confirm)                 │  ║
║  │  D5   ───────────────────────── Button C (Next Pattern)            │  ║
║  │  3.3V ───────────────────────── Power                              │  ║
║  │  GND  ───────────────────────── Ground                             │  ║
║  └─────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝


┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐
│   MIDI FeatherWing #1 (MIDI I/O)      │  │   MIDI FeatherWing #2 (Clock In)      │
│   Handles Note Data In/Out             │  │   Handles External MIDI Clock          │
├────────────────────────────────────────┤  ├────────────────────────────────────────┤
│                                        │  │                                        │
│  TX  ──────────── board.TX (GPIO #1)  │  │  TX  ──────────── board.D10            │
│  RX  ──────────── board.RX (GPIO #0)  │  │  RX  ──────────── board.D11            │
│  3.3V ──────────── Power               │  │  3.3V ──────────── Power               │
│  GND  ──────────── Ground              │  │  GND  ──────────── Ground              │
│                                        │  │                                        │
│  [MIDI IN]  ← From MIDI Keyboard       │  │  [MIDI IN]  ← From Clock Source        │
│  [MIDI OUT] → To Synthesizer           │  │  [MIDI OUT] → Not Used                 │
│                                        │  │                                        │
└────────────────────────────────────────┘  └────────────────────────────────────────┘
```

## Pin Assignment Summary

### M4 Express Pin Usage

| Pin       | Function                        | Connected To              |
|-----------|---------------------------------|---------------------------|
| **SCL**   | I2C Clock                       | OLED FeatherWing          |
| **SDA**   | I2C Data                        | OLED FeatherWing          |
| **TX**    | UART0 TX (MIDI Out)             | MIDI FeatherWing #1       |
| **RX**    | UART0 RX (MIDI In)              | MIDI FeatherWing #1       |
| **D10**   | UART1 TX (Clock Out - unused)   | MIDI FeatherWing #2       |
| **D11**   | UART1 RX (Clock In)             | MIDI FeatherWing #2       |
| **D9**    | Button A Input                  | OLED FeatherWing          |
| **D6**    | Button B Input                  | OLED FeatherWing          |
| **D5**    | Button C Input                  | OLED FeatherWing          |
| **D13**   | LED (optional, disabled)        | Onboard LED               |

## Physical Stacking Configuration

### Option 1: OLED on Top (Recommended)
```
     ┌─────────────────────────┐
     │  OLED FeatherWing       │  ← Display visible, buttons accessible
     │  (Stacked directly)     │
     ├─────────────────────────┤
     │  M4 Express             │
     └─────────────────────────┘
           │           │
           │           │
    ┌──────┘           └──────┐
    │                          │
  Wired                      Wired
Connection                 Connection
    │                          │
┌───┴────────┐         ┌───────┴───┐
│ MIDI       │         │ MIDI       │
│ Wing #1    │         │ Wing #2    │
│ (I/O)      │         │ (Clock)    │
└────────────┘         └────────────┘
```

### Option 2: All Stacked (Compact)
```
     ┌─────────────────────────┐
     │  OLED FeatherWing       │  ← Top (buttons accessible)
     ├─────────────────────────┤
     │  MIDI FeatherWing #1    │
     ├─────────────────────────┤
     │  MIDI FeatherWing #2    │
     ├─────────────────────────┤
     │  M4 Express (Base)      │
     └─────────────────────────┘
```
**Note:** With full stacking, ensure headers have enough height to reach through all layers.

## MIDI Connections

### Basic Setup (Internal Clock)
```
MIDI Keyboard → [MIDI IN]  → MIDI Wing #1 → [MIDI OUT] → Synthesizer
                                 ↓
                            M4 Express
                                 ↓
                         OLED Display Shows:
                         "BPM: 120 (Int)"
```

### Full Setup (External Clock)
```
MIDI Keyboard → [MIDI IN]  → MIDI Wing #1 → [MIDI OUT] → Synthesizer
                                 ↓
Clock Source  → [MIDI IN]  → MIDI Wing #2   M4 Express
(Sequencer)                                     ↓
                                         OLED Display Shows:
                                         "BPM: 120 (Ext)"
```

## Hardware Notes

### Power Considerations
- **USB Power:** Sufficient for all three FeatherWings
- **Battery Power:** Use LiPo battery (500mAh recommended)
  - Auto deep-sleep after 60 seconds of inactivity
  - Battery life: 6-7 hours continuous, days with sleep mode
  - Wake from sleep: Press any button (A, B, or C)

### UART Pin Selection (M4 Express)
The M4 Express typically has these UART-capable pins:
- **UART0:** TX (board.TX), RX (board.RX) ← Used for MIDI I/O
- **UART1:** D10, D11 ← Used for MIDI Clock
- **UART2:** D0, D1 (if available, alternate option)

**To change UART pins:** Edit `code.py` lines 36-41:
```python
# MIDI FeatherWing #2 alternate pins (if D10/D11 don't work)
uart_clock = busio.UART(
    board.D0, board.D1,  # Change these pins
    baudrate=31250,
    timeout=0
)
```

### I2C Addresses
- **OLED Display:** 0x3C (default, auto-detected)
- **MCP4728 DAC:** 0x60 or 0x64 (default, check with I2C scan)

### Button Pins (Pre-configured on OLED FeatherWing)
- **Button A:** D9 (hardwired on FeatherWing)
- **Button B:** D6 (hardwired on FeatherWing)
- **Button C:** D5 (hardwired on FeatherWing)

## Troubleshooting Pin Conflicts

### If buttons don't work:
1. Check that D9, D6, D5 are not used by other FeatherWings
2. Verify OLED FeatherWing is properly seated
3. Check serial console for button press debug messages

### If MIDI FeatherWing #2 doesn't work:
1. Verify D10, D11 are available (not used by other hardware)
2. Try alternate UART pins (D0, D1 or other UART-capable pins)
3. Update `code.py` line 38 with new pin assignments
4. Check UART baud rate is 31250 (MIDI standard)

### If OLED doesn't display:
1. Verify I2C pins SCL/SDA are not in use by other devices
2. Check that I2C address 0x3C is correct
3. Test I2C with `i2cdetect` or CircuitPython I2C scan

## FeatherWing Compatibility

### Verified Compatible M4 Boards:
- Adafruit Feather M4 Express
- Adafruit Metro M4 Express (with adapter)
- Adafruit ItsyBitsy M4 Express (requires breakout)

### Required FeatherWings:
1. **Adafruit OLED FeatherWing** (128x32 or 128x64)
   - Product ID: 4650 (128x64) or 2900 (128x32)
   - Includes buttons A, B, C

2. **Adafruit MIDI FeatherWing** (x2)
   - Product ID: 4740
   - Provides DIN-5 MIDI In/Out jacks
   - Optocoupler isolation on MIDI In

## Connector & Bus Occupancy Reference

**Last Updated:** 2025-10-23

### JST SH (STEMMA QT) Connectors

| Connector Location | Status | Connected To | Notes |
|-------------------|--------|--------------|-------|
| **M4 Feather JST SH** | 🔴 RESERVED | Battery (future) | Save for LiPo battery integration |
| **OLED FeatherWing JST SH #1** | ✅ OCCUPIED | MCP4728 DAC | STEMMA QT cable to DAC |
| **OLED FeatherWing JST SH #2** | 🟢 AVAILABLE | - | Can daisy-chain additional I2C devices |
| **MCP4728 DAC JST SH #1** | ✅ OCCUPIED | OLED FeatherWing | Receives I2C from OLED |
| **MCP4728 DAC JST SH #2** | 🟢 AVAILABLE | - | Can daisy-chain additional I2C devices |

**Key:**
- 🔴 RESERVED = Intentionally left open for specific future use
- ✅ OCCUPIED = Currently connected
- 🟢 AVAILABLE = Free for expansion

### I2C Bus (Shared by Multiple Devices)

| Device | I2C Address | SDA Pin | SCL Pin | Connection Method |
|--------|-------------|---------|---------|-------------------|
| **OLED FeatherWing** | 0x3C | D21 (SDA) | D22 (SCL) | Stacked headers |
| **MCP4728 DAC** | 0x60* | D21 (SDA) | D22 (SCL) | STEMMA QT cable from OLED |

**Notes:**
- I2C is a shared bus - all devices use the same SDA/SCL lines
- *MCP4728 may be 0x64 if using MCP4728A4 variant (check with I2C scan)
- Additional I2C devices can be daisy-chained via STEMMA QT connectors

### UART Pins

| UART | TX Pin | RX Pin | Status | Connected To |
|------|--------|--------|--------|--------------|
| **UART0** | D1 (TX) | D0 (RX) | ✅ OCCUPIED | MIDI FeatherWing #1 (note I/O) |
| **UART1** | D10 | D11 | ✅ OCCUPIED | MIDI FeatherWing #2 (clock in) |

### GPIO Pins

| Pin | Status | Function | Connected To |
|-----|--------|----------|--------------|
| **D5** | ✅ OCCUPIED | Button C | OLED FeatherWing |
| **D6** | ✅ OCCUPIED | Button B | OLED FeatherWing |
| **D9** | ✅ OCCUPIED | Button A | OLED FeatherWing |
| **D13** | 🟢 AVAILABLE | Onboard LED | (optional, can disable) |

### Analog/DAC Pins

| Pin | Status | Function | Notes |
|-----|--------|----------|-------|
| **A0** | 🟢 AVAILABLE | DAC0 | Future: 2nd CV output or S-Trigger |
| **A1** | 🟢 AVAILABLE | DAC1 | Future: 2nd CV output or Velocity CV |

### Power Rails

| Rail | Voltage | Current Available | Consumers |
|------|---------|-------------------|-----------|
| **USB 5V** | 5.0V | ~500mA | M4 (via regulator), MCP4728 DAC (VCC) |
| **3.3V** | 3.3V | ~500mA | M4 logic, OLED, MIDI FeatherWings |
| **BAT** | 3.7V | Varies | M4 (via JST SH connector - future) |
| **GND** | 0V | - | Common ground for all devices |

### MCP4728 DAC Channels

| Channel | Pin Name | Status | Function | Notes |
|---------|----------|--------|----------|-------|
| **Channel A** | VA | 🔴 RESERVED | CV Pitch | 1V/octave or 1.035V/octave, 0-5V range |
| **Channel B** | VB | 🔴 RESERVED | Gate/Trigger | V-trig (0V=off, 5V=on) or S-trig (inverted) |
| **Channel C** | VC | 🟢 AVAILABLE | - | Future: Velocity CV, Modulation CV, etc. |
| **Channel D** | VD | 🟢 AVAILABLE | - | Future: Clock out, 2nd trigger, etc. |

### Physical Outputs (3.5mm TRS Jacks)

| Jack | Status | Signal Source | Notes |
|------|--------|---------------|-------|
| **CV Pitch** | 🔴 RESERVED | MCP4728 Channel A (VA) | 1V/octave, 0-5V |
| **Gate** | 🔴 RESERVED | MCP4728 Channel B (VB) | 0V or 5V (V-trig) |
| **MIDI IN** | ✅ OCCUPIED | MIDI FeatherWing #1 | DIN-5 or TRS Type A |
| **MIDI OUT** | ✅ OCCUPIED | MIDI FeatherWing #1 | DIN-5 or TRS Type A |

### Expansion Capacity

**Available for future expansion:**
- 🟢 **2x MCP4728 DAC channels** (C, D) - can add 2 more CV outputs
- 🟢 **2x I2C STEMMA QT connectors** - can daisy-chain more I2C devices
- 🟢 **2x DAC pins on M4** (A0, A1) - alternative CV outputs (0-3.3V native)
- 🟢 **Multiple GPIO pins** - encoders, additional buttons, LEDs
- 🟢 **Analog inputs** - potentiometers for tempo, swing, etc.

### Important Notes

1. **JST SH on M4 is RESERVED for battery** - do NOT use for I2C, use OLED's STEMMA QT instead
2. **I2C is shared** - OLED and MCP4728 both use D21/D22, daisy-chained via STEMMA QT
3. **UART pins are fully occupied** - both UART0 (MIDI I/O) and UART1 (MIDI clock) in use
4. **MCP4728 channels C/D are free** - can add velocity CV, modulation, 2nd gate, etc.
5. **Update this document** whenever adding new hardware connections

---

## Additional Resources

- CircuitPython UART Guide: https://learn.adafruit.com/circuitpython-essentials/circuitpython-uart-serial
- FeatherWing Stacking: https://learn.adafruit.com/featherwings
- M4 Express Pinout: https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/pinouts
- MCP4728 DAC Guide: https://learn.adafruit.com/adafruit-mcp4728-i2c-quad-dac
- STEMMA QT Guide: https://learn.adafruit.com/introducing-adafruit-stemma-qt
