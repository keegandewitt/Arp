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

### I2C Address
- **OLED Display:** 0x3C (default, auto-detected)

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

## Additional Resources

- CircuitPython UART Guide: https://learn.adafruit.com/circuitpython-essentials/circuitpython-uart-serial
- FeatherWing Stacking: https://learn.adafruit.com/featherwings
- M4 Express Pinout: https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/pinouts
