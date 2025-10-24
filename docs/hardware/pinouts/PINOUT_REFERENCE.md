# Hardware Pinout Reference

Quick reference for all hardware pinouts in the Arp project.

---

## Feather M4 CAN Express

**Pinout Diagram:**
![Feather M4 CAN Pinout](https://cdn-learn.adafruit.com/assets/assets/000/111/275/medium800/adafruit_products_Adafruit_Feather_M4_CAN_Pinout.png?1651520615)

**Direct Link:** https://cdn-learn.adafruit.com/assets/assets/000/111/275/original/adafruit_products_Adafruit_Feather_M4_CAN_Pinout.png

**Key Pins for This Project:**
- **D21 (SDA)** - I2C Data (OLED, MCP4728)
- **D22 (SCL)** - I2C Clock (OLED, MCP4728)
- **D0 (RX)** - MIDI In (UART)
- **D1 (TX)** - MIDI Out (UART)
- **D4-D6** - Buttons (Pattern, Tempo, Settings)
- **3V** - 3.3V output (can power MCP4728 at 3.3V)
- **GND** - Ground
- **BAT** - Battery voltage (for Powerboost input)
- **USB** - 5V from USB (for Powerboost input - NOT RECOMMENDED, see notes)

**Important Notes:**
- NeoPixel is on Digital Pin 8 (not shown correctly in older diagrams)
- 3V pin provides 3.3V regulated output
- BAT pin provides LiPo voltage (3.0V-4.2V)

**Learn Guide:** https://learn.adafruit.com/adafruit-feather-m4-can-express

---

## MIDI FeatherWing

**Pinout Diagram (Top):**
![MIDI FeatherWing Top](https://cdn-learn.adafruit.com/assets/assets/000/095/281/medium800/adafruit_products_MIDI_FW_pinouts.jpg?1601489783)

**Pinout Diagram (Bottom):**
![MIDI FeatherWing Bottom](https://cdn-learn.adafruit.com/assets/assets/000/095/283/medium800/adafruit_products_MIDI_FW_pinouts_bottom.jpg?1601491249)

**Direct Links:**
- Top: https://cdn-learn.adafruit.com/assets/assets/000/095/281/original/adafruit_products_MIDI_FW_pinouts.jpg
- Bottom: https://cdn-learn.adafruit.com/assets/assets/000/095/283/original/adafruit_products_MIDI_FW_pinouts_bottom.jpg

**Key Connections:**
- **D0 (RX)** - MIDI In data
- **D1 (TX)** - MIDI Out data
- **GND** - Ground
- **VBUS** - 5V power from USB (powers MIDI circuit)

**Important Notes:**
- Uses UART Serial1 on Feather
- MIDI jacks are DIN-5 female connectors
- Activity LEDs for MIDI In/Out

**Learn Guide:** https://learn.adafruit.com/adafruit-midi-featherwing

---

## OLED FeatherWing 128x64 (Product #4650)

**Pinout Diagram:**
See Adafruit Learn guide for detailed pinout

**Key Connections:**
- **D21 (SDA)** - I2C Data (via stacking headers)
- **D22 (SCL)** - I2C Clock (via stacking headers)
- **D5** - Button A
- **D6** - Button B
- **D9** - Button C
- **3V** - 3.3V power
- **GND** - Ground
- **STEMMA QT** - I2C connector (3.3V, GND, SDA, SCL)

**Important Notes:**
- Uses **SH1107 driver** (NOT SSD1306!)
- I2C Address: **0x3C**
- 128x64 pixel resolution
- STEMMA QT provides 3.3V power - NOT suitable for powering 5V devices

**Learn Guide:** https://learn.adafruit.com/adafruit-128x64-oled-featherwing

---

## MCP4728 Quad DAC Breakout

**Pinout:**

```
        MCP4728
    ┌─────────────┐
VDD │●            │ VA  (DAC Channel A output)
GND │             │ VB  (DAC Channel B output)
SDA │  STEMMA QT  │ VC  (DAC Channel C output)
SCL │  ┌────┐     │ VD  (DAC Channel D output)
    │  └────┘     │
    └─────────────┘
```

**Key Connections:**
- **VDD** - Power supply (2.7V-5.5V)
  - **3.3V:** 0-3.3V output range
  - **5V:** 0-5V output range (REQUIRED for full CV range)
- **GND** - Ground
- **SDA** - I2C Data
- **SCL** - I2C Clock
- **VA, VB, VC, VD** - DAC outputs (0 to VDD voltage)

**I2C Addresses:**
- Default: **0x60**
- Alternate: 0x61, 0x64, 0x66 (via address pins)

**Important Notes:**
- I2C logic levels match VDD voltage
- If VDD = 5V, SDA/SCL expect 5V logic (needs level shifter from 3.3V Feather)
- If VDD = 3.3V, SDA/SCL work directly with Feather (no level shifter needed)
- 12-bit resolution (0-4095)
- STEMMA QT connector: **Do NOT use for power** if MCP4728 is at different voltage than STEMMA QT source

**Learn Guide:** https://learn.adafruit.com/adafruit-mcp4728-i2c-quad-dac

---

## Current Wiring (Arp Project)

### Power
```
LiPo Battery (3.7V)
    ↓
Feather M4 (charges battery, provides BAT pin)
    ↓
Powerboost (boosts to 5V)
    ↓
MCP4728 VDD (5V for full CV range)
```

### I2C Bus (3.3V logic)
```
Feather M4 (D21=SDA, D22=SCL)
    ↓ (stacking headers)
OLED FeatherWing (0x3C)
    ↓ (jumper wires from M4 headers)
MCP4728 (0x60) - powered at 5V but I2C at 3.3V
```

**CRITICAL:** MCP4728 powered at 5V expects 5V I2C logic, but Feather provides 3.3V.
- **Current approach:** Testing if 3.3V logic works with 5V-powered MCP4728 (may work but out of spec)
- **Proper solution:** Use BSS138 level shifters for SDA/SCL (see MCP4728_POWER_SETUP.md)

### MIDI
```
Feather M4 D0/D1 (UART)
    ↓ (stacking headers)
MIDI FeatherWing (DIN-5 jacks)
```

---

## Quick Pin Reference Table

| Function | M4 Pin | OLED Wing | MIDI Wing | MCP4728 |
|----------|--------|-----------|-----------|---------|
| I2C SDA | D21 | SDA (0x3C) | - | SDA (0x60) |
| I2C SCL | D22 | SCL | - | SCL |
| UART RX | D0 | - | MIDI In | - |
| UART TX | D1 | - | MIDI Out | - |
| Button A | D5 | Button A | - | - |
| Button B | D6 | Button B | - | - |
| Button C | D9 | Button C | - | - |
| Power 3.3V | 3V | 3V | - | VDD (alt) |
| Power 5V | USB | - | VBUS | VDD (current) |
| Ground | GND | GND | GND | GND |
| CV Out A | - | - | - | VA |
| CV Out B | - | - | - | VB |
| CV Out C | - | - | - | VC |
| CV Out D | - | - | - | VD |

---

**Last Updated:** 2025-10-24
**Project:** Arp MIDI Arpeggiator
