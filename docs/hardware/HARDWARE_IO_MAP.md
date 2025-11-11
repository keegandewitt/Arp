# Hardware I/O Occupancy Map

**Last Updated:** 2025-10-23
**Purpose:** Track hardware resource allocation to prevent conflicts and confusion

---

## Port Occupancy Status

### Legend
- ✅ **OCCUPIED** - Currently in use, cannot be reassigned
- 🔒 **RESERVED** - Not yet used, but allocated for planned feature
- 🆓 **AVAILABLE** - Free for future use
- ⚠️ **SHARED** - Multiple functions on same physical port (software-switchable)

---

## Communication Buses

### UART0 (Hardware Serial)
| Resource | Pins | Status | Occupied By | Notes |
|----------|------|--------|-------------|-------|
| **TX** | board.TX (D1, GPIO #1) | ✅ OCCUPIED | **Arpeggio Translation Loop** | DIN MIDI OUT via MIDI FeatherWing |
| **RX** | board.RX (D0, GPIO #0) | ✅ OCCUPIED | **Arpeggio Translation Loop** | DIN MIDI IN via MIDI FeatherWing |

**CRITICAL:** This UART carries:
1. Note On/Off messages (arpeggiated output)
2. MIDI Clock messages (for sync)
3. All MIDI pass-through messages (CC, Pitch Bend, etc.)

**Why "Arpeggio Translation Loop"?**
MIDI IN → Arp Engine → MIDI OUT (all on same port)

---

### I2C Bus
| Resource | Pins | Status | Occupied By | Notes |
|----------|------|--------|-------------|-------|
| **SDA** | board.SDA (D21) | ✅ OCCUPIED | OLED FeatherWing Display | SH1107 128x64 @ 0x3C |
| **SCL** | board.SCL (D22) | ✅ OCCUPIED | OLED FeatherWing Display | Shared I2C bus |

**Future I2C Expansion:**
- 🔒 MCP4728 DAC (4-channel, 12-bit, 0-5V) for CV/Gate output
- Address: 0x60 (default) or 0x61-0x67 (configurable)

---

### SPI Bus
| Resource | Pins | Status | Occupied By | Notes |
|----------|------|--------|-------------|-------|
| **SCK** | board.SCK | 🆓 AVAILABLE | - | Future expansion (SD card, etc.) |
| **MOSI** | board.MOSI | 🆓 AVAILABLE | - | |
| **MISO** | board.MISO | 🆓 AVAILABLE | - | |

---

## GPIO Pins

### Digital I/O (Buttons)
| Pin | Status | Occupied By | Function | Notes |
|-----|--------|-------------|----------|-------|
| **D9** | ✅ OCCUPIED | OLED FeatherWing | Button A | Prev pattern, or long-press for menu |
| **D6** | ✅ OCCUPIED | OLED FeatherWing | Button B | Demo chord / tap tempo |
| **D5** | ✅ OCCUPIED | OLED FeatherWing | Button C | Next pattern |

### Digital I/O (Available)
| Pin | Status | Occupied By | Function | Notes |
|-----|--------|-------------|----------|-------|
| **D4** | 🆓 AVAILABLE | - | - | GPIO capable |
| **D10** | 🆓 AVAILABLE | - | - | GPIO, PWM capable |
| **D11** | 🆓 AVAILABLE | - | - | GPIO, PWM capable |
| **D12** | 🆓 AVAILABLE | - | - | GPIO, PWM capable |
| **D13** | 🆓 AVAILABLE | - | Onboard LED | Can be used for status |

### NEOPIXEL
| Pin | Status | Occupied By | Function | Notes |
|-----|--------|-------------|----------|-------|
| **NEOPIXEL** | 🆓 AVAILABLE | - | Onboard RGB LED | Can be used for status |

---

## Analog Pins

### DAC Outputs (Built-in SAMD51)
| Pin | Status | Occupied By | Function | Notes |
|-----|--------|-------------|----------|-------|
| **A0** | 🔒 RESERVED | - | CV Pitch Out (future) | 10-bit, 0-3.3V native |
| **A1** | 🔒 RESERVED | - | Gate/Trigger Out (future) | 10-bit, 0-3.3V native |

**Note:** Built-in DACs are 10-bit, 0-3.3V. For CV/Gate (0-5V, 12-bit), we'll use external MCP4728 DAC on I2C.

### ADC Inputs (Analog Read)
| Pin | Status | Occupied By | Function | Notes |
|-----|--------|-------------|----------|-------|
| **A2** | 🆓 AVAILABLE | - | - | Could be used for pot/CV input |
| **A3** | 🆓 AVAILABLE | - | - | Could be used for pot/CV input |
| **A4** | 🆓 AVAILABLE | - | - | Could be used for pot/CV input |
| **A5** | 🆓 AVAILABLE | - | - | Could be used for pot/CV input |

---

## Physical Jacks (External)

### Current (Phase 1)
| Jack Type | Pins | Status | Function | Notes |
|-----------|------|--------|----------|-------|
| **DIN-5 MIDI IN** | D0 (RX) | ✅ OCCUPIED | MIDI FeatherWing | Opto-isolated input |
| **DIN-5 MIDI OUT** | D1 (TX) | ✅ OCCUPIED | MIDI FeatherWing | Buffered output |
| **USB-C** | Native USB | ✅ OCCUPIED | USB MIDI + Serial | Power + Data |

### Planned (Phase 2 - CV/Gate)
| Jack Type | Source | Status | Function | Notes |
|-----------|--------|--------|----------|-------|
| **3.5mm TRS (CV1)** | MCP4728 Ch A | 🔒 RESERVED | CV Pitch (1V/oct) | 0-5V output |
| **3.5mm TRS (CV2)** | MCP4728 Ch B | 🔒 RESERVED | CV Velocity | 0-5V output |
| **3.5mm TRS (Gate)** | MCP4728 Ch C | 🔒 RESERVED | ⚠️ V-trig OR S-trig | Software-switchable |
| **3.5mm TRS (Aux)** | MCP4728 Ch D | 🔒 RESERVED | Auxiliary CV | 0-5V output |

**IMPORTANT - Software-Switchable Trigger:**
The Gate jack will support **both** V-trigger and S-trigger on the **same physical jack**, switched via software setting:
- **V-trigger:** 0V = off, 5V = on (modern standard)
- **S-trigger:** 5V = off, 0V = on (vintage Moog/ARP/Korg)

User selects mode in settings → DAC inverts output for S-trig mode.

---

## Power Pins

| Pin | Status | Occupied By | Function | Notes |
|-----|--------|-------------|----------|-------|
| **USB** | ✅ OCCUPIED | System Power | 5V power via USB-C | Primary power source |
| **BAT** | 🔒 RESERVED | LiPo Battery (future) | 3.7V LiPo input | Onboard charging circuit |
| **EN** | 🔒 RESERVED | Power Switch (future) | Enable pin | Can be used for power control |
| **3V3** | ✅ OCCUPIED | System Power | 3.3V rail | Powers all logic |
| **GND** | ✅ OCCUPIED | System Ground | Ground reference | |

---

## Summary of Occupied Resources

### Currently In Use (Phase 1)
- **UART (D0/D1):** Arpeggio Translation Loop (DIN MIDI IN/OUT + Clock)
- **I2C (D21/D22):** OLED Display (SH1107)
- **GPIO (D9, D6, D5):** OLED FeatherWing buttons
- **USB:** USB MIDI + Serial console

### Reserved for Phase 2 (CV/Gate)
- **I2C:** MCP4728 4-channel DAC (address 0x60)
- **4x 3.5mm jacks:** CV Pitch, CV Velocity, Gate (V-trig/S-trig switchable), Aux CV

### Available for Future Expansion
- **GPIO:** D4, D10, D11, D12, D13
- **ADC:** A2, A3, A4, A5
- **SPI Bus:** All pins available
- **NEOPIXEL:** Onboard RGB LED

---

## Conflict Prevention Rules

### 1. UART0 is Exclusive
- **Never** reassign D0/D1 (TX/RX) for other purposes
- UART handles both notes AND clock on same port
- This is the "Arpeggio Translation Loop" - it's a single logical unit

### 2. I2C is Shared
- Multiple devices can coexist on I2C if addresses don't conflict
- Current: OLED @ 0x3C
- Future: MCP4728 DAC @ 0x60 (no conflict)

### 3. Physical Jack Mapping
- Document which jack connects to which MCU pin/DAC channel
- Use labels on enclosure that match this document
- Example: "CV1 (Pitch)" = MCP4728 Ch A

### 4. Software-Switchable Functions
- When one physical port has multiple modes (V-trig/S-trig), document:
  - Which setting controls the mode
  - How to switch modes
  - Expected behavior in each mode
- Label physical jack with both functions: "GATE (V/S-trig)"

---

## Change Log

### 2025-10-23 (v1.0)
- Initial document created
- Established "Arpeggio Translation Loop" terminology for UART MIDI path
- Documented current Phase 1 occupancy
- Reserved pins for Phase 2 CV/Gate
- Documented V-trig/S-trig software-switchable gate concept

---

## Usage Notes

**When adding new features:**
1. Check this document FIRST before assigning pins
2. Update occupancy status when allocating resources
3. Document the function and purpose clearly
4. Note any shared resources or conflicts
5. Update the change log with date and description

**When troubleshooting:**
- If a feature isn't working, check if its pins are actually available
- Verify no other code is using the same UART/SPI/I2C bus
- Check for address conflicts on I2C

**When onboarding new the assistant instances:**
- Read this document to understand hardware allocation
- Refer to "Arpeggio Translation Loop" for MIDI note+clock path
- Check occupancy before suggesting pin assignments
