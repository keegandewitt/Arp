# PRISME Hardware Board Designs - Comprehensive Audit Report

**Generated:** 2025-11-03
**Project:** PRISME Translation Hub (MIDI Arpeggiator with CV/Gate Output)
**Purpose:** Complete hardware specification for production-ready schematics
**Thoroughness Level:** VERY THOROUGH - All component values, connections, and positions documented

---

## EXECUTIVE SUMMARY

The PRISME hardware consists of a **two-board vertical stack** plus a **Feather M4 stack** (top), with a rear-panel connector arrangement. The design uses professional-grade protection circuits, activity LEDs, and dual gate output modes (V-Trig and S-Trig).

### Key Specifications
- **Boards:** 2× custom-cut ElectroCookie protoboards (90mm × 55mm each)
- **Main MCU:** Adafruit Feather M4 CAN Express
- **DAC:** MCP4728 (4-channel 12-bit I2C)
- **Connectors:** 2 MIDI IN/OUT, USB-C, 2 CV IN, 1 TRIG IN, 3 CV OUT, 1 RGB TRIG OUT, 1 CC OUT
- **LEDs:** 5× white activity indicators + 2× RGB mode indicators
- **Total GPIO:** 21 pins in use out of 26 available

---

## SECTION 1: BOARD STRUCTURE & PHYSICAL LAYOUT

### Board Stack Overview

```
┌─────────────────────────────────────────────────────┐
│  FEATHER STACK (Top - M4 + OLED + MIDI wings)       │
│  - Feather M4 CAN Express                           │
│  - OLED FeatherWing (128×64 SH1107 @ 0x3C)          │
│  - MIDI FeatherWing (DIN-5 MIDI @ 0x60)             │
├─────────────────────────────────────────────────────┤
│  INPUT BOARD (90mm × 55mm)                          │
│  - Position: Below Feather, above OUTPUT board      │
│  - Rear jacks: CV IN, TRIG IN (top row)            │
│  - Mounted on 10mm M3 standoffs                     │
├─────────────────────────────────────────────────────┤
│  OUTPUT BOARD (90mm × 55mm)                         │
│  - Position: Bottom of stack                        │
│  - Rear jacks: CV OUT, TRIG OUT, CC OUT,           │
│    MIDI IN/OUT, USB-C (rear bottom row)             │
│  - Mounted on 10mm M3 standoffs to enclosure        │
└─────────────────────────────────────────────────────┘

Board Spacing:
- Feather to INPUT: 15mm gap (wire routing)
- INPUT to OUTPUT: 10mm (board thickness + standoff)
- OUTPUT to enclosure base: 10mm
- Total height: ~35mm

Rear Edge Layout:
TOP ROW (INPUT board):
  [CV IN]  [TRIG IN]
   20mm      32mm
   ●LED      ●RGB

BOTTOM ROW (OUTPUT board):
  [USB-C]  [CV OUT]  [TRIG OUT]  [CC OUT]  [MIDI OUT]  [MIDI IN]
   8mm      20mm       32mm        44mm      65mm        85mm
            ●LED       ●RGB        ●LED      ●LED        ●LED
```

---

## SECTION 2: COMPLETE PIN ALLOCATION MATRIX

### M4 CAN Express - All 21 Pins In Use

#### GPIO - Control & Signals (11 pins)
| Pin | Function | Hardware | Notes |
|-----|----------|----------|-------|
| **D4** | CV IN LED | 3mm white LED | Activity indicator |
| **D5** | Button C | OLED FeatherWing | Fire gate pulse |
| **D6** | Button B | OLED FeatherWing | Toggle V/S-Trig |
| **D9** | Button A | OLED FeatherWing | Pattern select |
| **D10** | S-Trig GPIO | NPN transistor base | True S-Trig output |
| **D11** | TRIG IN LED R | RGB LED (red channel) | S-Trig indicator |
| **D12** | CV OUT LED | 3mm white LED | Activity indicator |
| **D13** | Status LED | Onboard LED | Visual feedback |

#### Analog - Inputs (2 pins)
| Pin | Function | Hardware | Voltage Range |
|-----|----------|----------|----------------|
| **A3** | CV Pitch IN | Voltage divider 20k/22k | 0-5V → 0-2.62V |
| **A4** | Gate IN | Voltage divider 20k/22k | 0-5V → 0-2.62V |

#### I2C Bus (2 pins) - Shared
| Pin | Function | Connected Devices |
|-----|----------|-------------------|
| **D21 (SDA)** | I2C Data | OLED (0x3C), MCP4728 (0x60) |
| **D22 (SCL)** | I2C Clock | OLED (0x3C), MCP4728 (0x60) |

#### RGB LED Channels (4 pins)
| Pin | Function | LED | Color |
|-----|----------|-----|-------|
| **D23 (MOSI)** | TRIG IN LED G | RGB LED channel | V-Trig indicator |
| **D24 (MISO)** | TRIG IN LED B | RGB LED channel | Reserved |
| **A0** | TRIG OUT LED R | RGB LED channel | S-Trig indicator |
| **A1** | TRIG OUT LED G | RGB LED channel | V-Trig indicator |

#### Activity Indicators (2 pins)
| Pin | Function | LED |
|-----|----------|-----|
| **D25 (SCK)** | CC OUT LED | 3mm white LED |
| **A5** | MIDI IN LED | 3mm white LED |

#### Special Functions (2 pins)
| Pin | Function | Hardware |
|-----|----------|----------|
| **CAN_TX** | MIDI OUT LED | 3mm white LED |
| **NEOPIXEL** | Onboard RGB | Status indicator |

#### Reserved (2 pins)
| Pin | Function | Hardware | Status |
|-----|----------|----------|--------|
| **D0 (RX)** | MIDI In (UART) | MIDI FeatherWing | Reserved for future |
| **D1 (TX)** | MIDI Out (UART) | MIDI FeatherWing | Reserved for future |

### MCP4728 DAC Channel Allocation

| Channel | Function | Output Type | Voltage | Current Use |
|---------|----------|-------------|---------|-------------|
| **A** | CV Pitch (1V/octave) | 0-5V DAC | 0-5V | ACTIVE |
| **B** | CC/Velocity (future) | 0-5V DAC | 0-5V | AVAILABLE |
| **C** | V-Trig Gate | 0-5V DAC | 0V/5V | ACTIVE |
| **D** | Trigger/Accent (future) | 0-5V DAC | 0-5V | AVAILABLE |

**I2C Address:** 0x60 (default, configurable 0x60-0x67)

---

## SECTION 3: OUTPUT BOARD (BOTTOM) - COMPONENT DETAILS

### Physical Position & Jacks

```
REAR EDGE (Back panel):
  8mm      20mm     32mm      44mm       65mm       85mm
  ↓        ↓         ↓         ↓          ↓          ↓
[USB-C]  [CV OUT]  [TRIG OUT] [CC OUT]  [MIDI OUT] [MIDI IN]
         ●LED      ●RGB       ●LED      ●LED       ●LED
```

### Jack Wiring Specifications

#### 1. USB-C (8mm from left edge)
- **Type:** Panel mount breakout (extension cable to Feather)
- **Size:** 9.5mm × 3.8mm cutout
- **Purpose:** Programming access, power supply
- **No LED indicator**

#### 2. CV OUT Jack (20mm from left edge)
**Jack Type:** 1/8" mono TRS (3.5mm), panel mount

**Signal Path:**
```
MCP4728 Channel A → [R1 100Ω] → [C6 100nF] → TIP
                                               │
                                    SLEEVE → GND
```

**Components:**
- R1: 100Ω 1/4W (series protection)
- C6: 100nF ceramic (output smoothing)

**LED:** D12 white activity indicator
- Control: GPIO pin D12
- Resistor: 150Ω current limiting
- Behavior: ON when DAC channel A active

#### 3. V-TRIG/S-TRIG OUT Jack (32mm from left edge)
**Jack Type:** 1/8" mono TRS (3.5mm), panel mount

**Dual-Mode Output (V-Trig OR S-Trig, software selectable):**

**V-Trig Path:**
```
MCP4728 Channel C → [R3 100Ω] ───────┐
                                     ├→ TIP
S-Trig Path:                         │
D10 GPIO → [R5 1kΩ] → NPN Base      │
                Collector → [R6 100Ω]┘
                Emitter → GND

SLEEVE → GND
```

**Components:**
- R3: 100Ω 1/4W (V-Trig protection)
- R5: 1kΩ 1/4W (transistor base limiting)
- R6: 100Ω 1/4W (S-Trig collector resistor)
- Q1: 2N3904 NPN transistor

**NPN Transistor Pinout (2N3904, flat side down):**
```
  E   B   C
  │   │   │
 Emitter Base Collector
```
- **Emitter:** → GND
- **Base:** → 1kΩ resistor → D10 GPIO
- **Collector:** → 100Ω → Jack TIP junction

**LED:** A0/A1/A2 RGB LED (mode indicator)
- Red (A0): S-Trig mode active
- Green (A1): V-Trig mode active
- Blue (A2): Reserved/unused
- Current limiting: 150Ω per channel
- Behavior: Shows which mode is active

#### 4. CC OUT Jack (44mm from left edge)
**Jack Type:** 1/8" mono TRS (3.5mm), panel mount

**Signal Path:**
```
MCP4728 Channel B → [R2 100Ω] → [C7 100nF] → TIP
                                              │
                                   SLEEVE → GND
```

**Components:**
- R2: 100Ω 1/4W (series protection)
- C7: 100nF ceramic (output smoothing)

**LED:** D25 white activity indicator
- Control: GPIO pin D25
- Resistor: 150Ω current limiting
- Behavior: ON when DAC channel B active

#### 5. MIDI OUT Jack (65mm from left edge)
**Jack Type:** 5-pin DIN panel mount

**Pinout (DIN-5, 180° orientation):**
```
    2
  ┌───┐
 5│   │1
  │ O │  (O = center hole)
 4│   │3
  └───┘
```

**Wiring (MIDI current loop):**
- **Pin 5:** MIDI Signal OUT → MIDI FeatherWing TX OUT
- **Pin 4:** Return (current loop) → MIDI FeatherWing TX RETURN
- **Pins 1-3:** Unconnected (legacy shield ground, not used)

**LED:** CAN_TX white activity indicator
- Control: GPIO CAN_TX pin
- Resistor: 150Ω current limiting
- Behavior: 50ms pulse on MIDI TX activity

#### 6. MIDI IN Jack (85mm from left edge)
**Jack Type:** 5-pin DIN panel mount

**Pinout (DIN-5, 180° orientation, same as OUT):**

**Wiring (MIDI current loop with optocoupler isolation):**
- **Pin 5:** MIDI Signal IN → MIDI FeatherWing RX IN
- **Pin 4:** Return (current loop) → MIDI FeatherWing RX RETURN
- **Pins 1-3:** Unconnected

**LED:** A5 white activity indicator
- Control: GPIO pin A5
- Resistor: 150Ω current limiting
- Behavior: 50ms pulse on MIDI RX activity

### Power Distribution - OUTPUT Board

**Input:** Feather USB 5V + GND

**Distribution:**
```
Feather 5V ──→ [C1 47µF electrolytic] ──→ 5V Rail
              [C2 0.1µF ceramic bypass]
                                    ├→ MCP4728 VCC (5V)
                                    ├→ MIDI FeatherWing VCC
                                    └→ Output stage

All grounds tied to common GND rail
```

**Decoupling Capacitors:**
- C1: 47µF 16V electrolytic (bulk power supply)
- C2: 0.1µF 50V ceramic (high-frequency bypass)
- C3: 0.1µF 50V ceramic (MCP4728 VCC decoupling, very close to pin)
- C4: 0.1µF 50V ceramic (spare)
- C6, C7: 100nF 50V ceramic (output low-pass filters)
- C8: 100nF 50V ceramic (future expansion)

**Current Budget:**
- MCP4728 DAC: ~10mA
- MIDI FeatherWing: ~15mA
- Output resistors/LEDs: <10mA
- **Total typical: <50mA** (well under USB 500mA limit)

### OUTPUT Board BOM

| Qty | Component | Value | Purpose |
|-----|-----------|-------|---------|
| 1 | MCP4728 Module | I2C DAC, 4-channel | CV/Gate output generation |
| 1 | MIDI FeatherWing | Adafruit #4740 | MIDI I/O (stacked on Feather) |
| 1 | USB-C Breakout | Panel mount | Extension to Feather USB port |
| 1 | Electrolytic Cap | 47µF 16V | Bulk power supply |
| 4 | Ceramic Cap | 0.1µF 50V | Bypass/decoupling |
| 3 | Ceramic Cap | 100nF 50V | Output smoothing (CV OUT, TRIG OUT, CC OUT) |
| 1 | Ceramic Cap | 100nF 50V | Spare |
| 4 | Resistor | 100Ω 1/4W | Output protection (R1-R4) |
| 1 | Resistor | 1kΩ 1/4W | NPN base limiting (R5) |
| 4 | Resistor | 150Ω 1/4W | White LED current limiting (R7-R10) |
| 3 | Resistor | 150Ω 1/4W | RGB LED channels (R11-R13) |
| 1 | NPN Transistor | 2N3904 | S-Trig switching |
| 1 | 1/8" mono jack | Panel mount | CV OUT |
| 1 | 1/8" mono jack | Panel mount | TRIG OUT (V/S-Trig) |
| 1 | 1/8" mono jack | Panel mount | CC OUT |
| 2 | 5-pin DIN jack | Panel mount | MIDI IN/OUT |
| 4 | LED | 3mm white flat-top | Activity indicators |
| 1 | RGB LED | 3mm common cathode | TRIG OUT mode indicator |
| 1 | 12-pin header | Male 0.1" | Connection to Feather stack |
| 4 | Standoffs | M2.5 × 10mm | MCP4728 module mounting |

---

## SECTION 4: INPUT BOARD (TOP) - COMPONENT DETAILS

### Physical Position & Jacks

```
REAR EDGE (Back panel, top row):
      20mm      32mm
       ↓         ↓
     [CV IN]  [TRIG IN]
      ●LED      ●RGB
```

### Precision Input Protection Circuits

Both input circuits use **identical voltage divider + protection topology** for professional-grade overvoltage protection:

#### Circuit Architecture

**Stage 1: Voltage Divider (Input Protection)**
```
External 0-5V Jack
         ↓
    [R1 10kΩ]  ← Series
         ↓
    [R2 10kΩ]  ← Series
         ├──────→ Tap Point (scaled voltage)
         ↓
    [R3 22kΩ]  ← To ground
         ↓
        GND

Scaling Formula: Vout = Vin × (22kΩ / (20kΩ + 22kΩ))
                Vout = Vin × 0.524
Example: 5V input → 2.62V at tap
```

**Stage 2: Protection Chain (Per Input)**
```
Tap Point → [R series] → [C filter] → [D clamp] → ADC Pin
             10kΩ         100nF       BAT85      (3.3V)
                            ↓
                           GND
                           
            Diode cathode also to 3.3V rail (clamp)
```

**Protection Features:**
1. **10kΩ Series Resistors:** Current limiting (prevents ADC shorts)
2. **100nF Capacitor:** Low-pass filter (removes RF, cutoff ~160Hz)
3. **BAT85 Schottky Diode:** Overvoltage clamp (protects to 3.3V max)

#### 1. CV IN Jack (20mm from left edge)
**Jack Type:** 1/8" mono TRS (3.5mm), panel mount

**Full Circuit:**
```
CV IN TIP ──[R1 10kΩ]──[R2 10kΩ]──[R4 22kΩ to GND]
                            ↓ (Tap)
                       [R3 10kΩ]──[C3 100nF]──[D1 BAT85]──→ A3 ADC Pin
                                      ↓             ↓
                                     GND         3.3V (clamp)

CV IN SLEEVE → GND
```

**Components (Left section of INPUT board):**
- R1, R2: 10kΩ 1/4W (voltage divider series)
- R4: 22kΩ 1/4W (divider to ground)
- R3: 10kΩ 1/4W (series protection to ADC)
- C3: 100nF 50V ceramic (low-pass filter)
- D1: BAT85 Schottky diode (overvoltage clamp)

**Voltage Scaling:**
- 5V input → 2.62V at A3 ✓ (safe for 3.3V ADC)
- Prevents overvoltage damage
- Maintains CV signal integrity (DC to ~150Hz)

**LED:** D4 white activity indicator
- Control: GPIO pin D4
- Resistor: 150Ω current limiting
- Behavior: ON when voltage > 0.1V (activity detect)

#### 2. TRIG IN Jack (32mm from left edge)
**Jack Type:** 1/8" mono TRS (3.5mm), panel mount

**Full Circuit:**
```
TRIG IN TIP ──[R5 10kΩ]──[R6 10kΩ]──[R8 22kΩ to GND]
                             ↓ (Tap)
                        [R7 10kΩ]──[C4 100nF]──[D2 BAT85]──→ A4 ADC Pin
                                       ↓             ↓
                                      GND         3.3V (clamp)

TRIG IN SLEEVE → GND
```

**Components (Center section of INPUT board):**
- R5, R6: 10kΩ 1/4W (voltage divider series)
- R8: 22kΩ 1/4W (divider to ground)
- R7: 10kΩ 1/4W (series protection to ADC)
- C4: 100nF 50V ceramic (low-pass filter)
- D2: BAT85 Schottky diode (overvoltage clamp)

**Voltage Scaling:** Same as CV IN
- 5V input → 2.62V at A4 ✓
- Protects ADC from external trigger sources (may be 5V, 12V, or higher)

**Detection Modes (Software-selectable):**
| Mode | Detection | Voltage Threshold | Use Case |
|------|-----------|-------------------|----------|
| **V-Trig** | Gate HIGH | >2.0V | Modern modular (Eurorack) |
| **S-Trig** | Gate HIGH | <1.0V (inverted) | Vintage modular (Moog, ARP) |

**LED:** D11/D23/D24 RGB LED (mode indicator + activity)
- Red (D11): S-Trig mode detected (voltage <1.0V)
- Green (D23): V-Trig mode detected (voltage >2.0V)
- Blue (D24): Reserved/unused
- Current limiting: 150Ω per channel
- Brightness varies with input signal strength

### Power Distribution - INPUT Board

**Input:** Feather 5V + GND via header

**Distribution:**
```
Feather 5V ──→ [C1 47µF electrolytic] ──→ 5V Rail
              [C2 0.1µF ceramic bypass]
                                    ├→ Protection circuit supplies
                                    └→ 3.3V clamp references
```

**Decoupling Capacitors:**
- C1: 47µF 16V electrolytic (bulk power supply)
- C2: 0.1µF 50V ceramic (high-frequency bypass)
- C3, C4: 100nF 50V ceramic (input filtering)

**Current Budget:**
- Protection circuits: <1mA (mostly passive)
- LEDs: <10mA total
- **Total typical: <15mA**

### INPUT Board BOM

| Qty | Component | Value | Purpose |
|-----|-----------|-------|---------|
| 1 | Electrolytic Cap | 47µF 16V | Bulk power supply |
| 1 | Ceramic Cap | 0.1µF 50V | High-frequency bypass |
| 2 | Ceramic Cap | 100nF 50V | Input filtering (CV IN, TRIG IN) |
| 4 | Resistor | 10kΩ 1/4W | Voltage divider (series, 2 per input) |
| 2 | Resistor | 22kΩ 1/4W | Voltage divider (to ground, 1 per input) |
| 2 | Resistor | 10kΩ 1/4W | Series input protection (1 per input) |
| 4 | Resistor | 150Ω 1/4W | LED current limiting (1 white + 3 RGB) |
| 2 | Schottky Diode | BAT85 | Overvoltage clamp to 3.3V |
| 2 | 1/8" mono jack | Panel mount | CV IN, TRIG IN |
| 1 | LED | 3mm white flat-top | CV IN activity indicator |
| 1 | RGB LED | 3mm common cathode | TRIG IN mode indicator |
| 1 | 8-pin header | Male 0.1" | Connection to Feather stack |

---

## SECTION 5: CIRCUIT DESIGN DETAILS

### Input Voltage Divider (Both A3 & A4)

**Purpose:** Scale external 0-5V to safe 0-2.62V for 3.3V ADC

**Formula:**
```
Vout = Vin × (R_to_ground) / (R_total)
Vout = Vin × 22kΩ / (20kΩ + 22kΩ)
Vout = Vin × 0.524
```

**Example Conversions:**
- 0V input → 0V output ✓
- 2.5V input → 1.31V output ✓
- 5V input → 2.62V output ✓
- 10V input → 5.24V output ✗ (clipped by BAT85 diode to 3.3V)

**Filtering Characteristics:**
- Cutoff Frequency (with 10kΩ + 100nF): ~160Hz
- Removes RF interference
- Preserves DC and slow CV signals
- Roll-off: -20dB/decade above cutoff

### CV Output Stage (0-5V DAC + Protection)

**Each CV output (A, B, C):**
```
DAC Channel → [100Ω Resistor] → [100nF Capacitor] → Output Jack
                                        ↓
                                       GND
```

**Protection Features:**
- **100Ω Series Resistor:** 
  - Limits fault current (50mA max at 5V)
  - Prevents DAC damage if jack shorted
  - Safe for all typical cables

- **100nF Capacitor:** 
  - Low-pass filter (cutoff ~160Hz at 100Ω)
  - Smooths DAC switching noise
  - Reduces EMI

**NOT used on Gate outputs** (V-Trig) because capacitor slows rise/fall times (gates need fast edges for drum triggers)

### S-Trig Circuit (True Short-to-Ground Output)

**Purpose:** Vintage synth compatibility (ARP, Korg MS-20, Yamaha CS)

**How it works:**
- **Idle State:** Transistor OFF, output open circuit (floating)
- **Active State:** Transistor ON, output shorted to ground (<0.2Ω)

**Switching Control:**
```
GPIO D10 (3.3V)
    ↓
[1kΩ Resistor] ← Base current limiting
    ↓
2N3904 Base
    ├─ Collector (pulled low when ON)
    └─ Emitter (tied to GND)
```

**Transistor Operation:**
| GPIO Level | Transistor State | S-Trig Output | Use |
|------------|------------------|---------------|-----|
| LOW (0V) | OFF | Open circuit | Idle (no trigger) |
| HIGH (3.3V) | ON (saturated) | Shorted to GND | Active (trigger) |

**2N3904 Characteristics:**
- General-purpose NPN switching transistor
- Acceptable alternatives: 2N2222, BC337, or similar
- Safe with 3.3V GPIO (Vbe = 0.6V, max Ic = 200mA)

### LED Current Calculations (3.3V GPIO Supply)

**White LEDs (3mm flat-top high-efficiency):**
```
Forward voltage: ~3.0V
Current limiting resistor: 150Ω
Current = (3.3V - 3.0V) / 150Ω = 0.003V / 150Ω = 20mA
Wait, recalculate: (3.3V - 3.0V) / 150Ω = 0.3V / 150Ω = 2mA ✓
Power per LED: 3.3V × 2mA = 6.6mW ≈ 7mW
Brightness: Visible, moderate
```

**RGB LED Channels (common cathode):**
- Red (Vf ~2.0V): (3.3V - 2.0V) / 150Ω = 8.7mA (bright)
- Green (Vf ~3.0V): (3.3V - 3.0V) / 150Ω = 2mA (dimmer but visible)
- Blue (Vf ~3.0V): (3.3V - 3.0V) / 150Ω = 2mA (dimmer but visible)

**Only one RGB channel active at a time** (V-Trig=Green, S-Trig=Red)

**Total Power Budget:**
- 5 white LEDs: 5 × 2mA = 10mA
- 2 RGB LEDs (one channel each): 2 × 3mA = 6mA
- **Total typical: 16-20mA** (negligible for 500mAh battery)

### DAC Configuration (MCP4728)

**Power & Reference:**
- VDD: 5V from Feather (LM7805 regulator or direct USB)
- VSS: Ground
- Vref: VDD (use 5V as reference, not internal 2.048V)
- Gain: 1× (no amplification)

**Output Characteristics (with VDD = 4.83V):**
- Resolution: 12-bit (4096 steps)
- Output range: 0V to 4.83V
- Settling time: 6 microseconds
- Accuracy: ±2 LSB typical

**Initialization Sequence (Critical):**
1. Call `dac.wakeup()` (clear power-down mode)
2. Set `vref = Vref.VDD` (use 5V reference)
3. Set `gain = 1` (no amplification)
4. Call `dac.save_settings()` (persist to EEPROM)
5. Set all channels to 0V initially

**1V/Octave Calculation (Channel A):**
```
MIDI Note → Voltage Conversion:
voltage = (MIDI_note / 12.0)  [volts]
raw_value = int((voltage / 5.0) * 4095)  [12-bit value]

Or simplified:
raw_value = int(MIDI_note × 68.27)  [steps per semitone]

Example conversions:
MIDI 12 (C0)  → 1.00V → raw 819
MIDI 24 (C1)  → 2.00V → raw 1639
MIDI 36 (C2)  → 3.00V → raw 2458
MIDI 48 (C3)  → 4.00V → raw 3277
MIDI 60 (C4)  → 5.00V → raw 4095 (max)
```

**Maximum Range:** 5 octaves (C0 to C4) with 5V reference
- Sufficient for 61-key keyboard
- Sufficient for typical arpeggiator patterns (2-3 octaves)

---

## SECTION 6: CONNECTOR SPECIFICATIONS

### Rear Panel Connector Layout

```
Top Row (INPUT board):
[CV IN]      [TRIG IN]
  ●LED        ●RGB
  20mm        32mm

Bottom Row (OUTPUT board):
[USB-C]  [CV OUT]  [TRIG OUT]  [CC OUT]  [MIDI OUT]  [MIDI IN]
          ●LED      ●RGB       ●LED      ●LED       ●LED
  8mm      20mm     32mm       44mm      65mm        85mm
```

### Jack Specifications

#### 1/8" Mono TRS Jacks (CV/Gate)
- **Count:** 3 output (CV OUT, TRIG OUT, CC OUT) + 2 input (CV IN, TRIG IN)
- **Type:** Thonkiconn PJ301M-12 (Eurorack standard)
- **Hole Size:** 6mm diameter
- **Jack Depth:** ~12mm behind panel
- **Wiring:** Tip = Signal, Ring = N/C, Sleeve = Ground
- **LED Position:** 7mm to right of jack center
- **LED Hole Size:** 3.2mm (press-fit for 3mm LED)

#### 5-pin DIN Jacks (MIDI)
- **Count:** 2 (MIDI IN, MIDI OUT)
- **Type:** Panel-mount DIN-5 180° (standard MIDI orientation)
- **Hole Size:** 14mm diameter
- **Jack Depth:** ~35mm behind panel
- **Pins Used:** 4 and 5 only (signal + return)
- **Pins Unused:** 1, 2, 3 (legacy shield ground)
- **Current Loop:** MIDI uses current loop, not voltage
  - Pin 5: Signal
  - Pin 4: Return
- **Isolation:** Optional, but optocoupler isolation recommended on RX
- **LED Position:** 7mm to right of jack center
- **LED Hole Size:** 3.2mm

#### USB-C Port
- **Type:** Feather M4 onboard port (extension via cable)
- **Cutout:** 9.5mm × 3.8mm rectangular opening
- **Extension:** USB-C male to female extension cable
- **Purpose:** Programming, power, serial console
- **No LED indicator** (unlike signal jacks)

---

## SECTION 7: I2C BUS ARCHITECTURE

### Shared I2C Bus Configuration

**Hardware Setup:**
```
M4 SDA (D21) ──┬─→ OLED FeatherWing (0x3C)
               └─→ MCP4728 DAC (0x60)

M4 SCL (D22) ──┬─→ OLED FeatherWing (0x3C)
               └─→ MCP4728 DAC (0x60)

Pull-ups: 4.7kΩ built into OLED FeatherWing
Bus Speed: 100kHz (safe for all devices)
```

### Device Addresses

| Device | Address | Configurable? | Purpose |
|--------|---------|---------------|---------|
| **OLED Display (SH1107)** | 0x3C | No (hardwired) | 128×64 display |
| **MCP4728 DAC** | 0x60 | Yes (A0-A2 pins) | 4-channel CV output |
| **MIDI FeatherWing** | 0x4D | Yes (jumpers) | UART, not I2C config |

### Initialization Order (Critical)

```python
1. displayio.release_displays()  # Clear previous display
   time.sleep(0.2)               # Let hardware settle

2. i2c = board.I2C()             # Get shared I2C bus (singleton)

3. # Initialize devices in any order after this
   display = init_display(i2c)   # OLED @ 0x3C
   dac = init_dac(i2c)           # MCP4728 @ 0x60

4. dac.wakeup()                  # Clear power-down mode
   time.sleep(0.1)

5. # Configure DAC for 5V operation
   dac.channel_a.vref = Vref.VDD
   dac.channel_b.vref = Vref.VDD
   dac.channel_c.vref = Vref.VDD
   dac.channel_d.vref = Vref.VDD
   dac.save_settings()            # Persist to EEPROM
   time.sleep(0.3)
```

**Why this order matters:**
- `board.I2C()` is a singleton (returns same bus instance)
- `displayio.release_displays()` clears previous bus conflicts
- Wait times allow hardware to stabilize
- DAC EEPROM write takes 300ms

---

## SECTION 8: LED INDICATOR SYSTEM (Complete)

### LED Summary Table

| Jack | LED Type | GPIO Pin(s) | Board | Detection | Behavior |
|------|----------|-------------|-------|-----------|----------|
| **CV IN** | White 3mm | D4 | INPUT | Monitor A3 ADC | ON when voltage > 0.1V |
| **TRIG IN** | RGB 3mm | D11 (R), D23 (G), D24 (B) | INPUT | Monitor A4 ADC + mode | GREEN (V-Trig), RED (S-Trig) |
| **CV OUT** | White 3mm | D12 | OUTPUT | Software controlled | ON when DAC Ch A active |
| **TRIG OUT** | RGB 3mm | A0 (R), A1 (G), A2 (B) | OUTPUT | Software + mode | GREEN (V-Trig), RED (S-Trig) |
| **CC OUT** | White 3mm | D25 | OUTPUT | Software controlled | ON when DAC Ch B active |
| **MIDI OUT** | White 3mm | CAN_TX | OUTPUT | Monitor UART TX | 50ms pulse on TX activity |
| **MIDI IN** | White 3mm | A5 | OUTPUT | Monitor UART RX | 50ms pulse on RX activity |

### Physical Mounting

**LED Hole Positions on Back Panel:**
```
Top Row:
[CV IN]       [TRIG IN]
 27mm         39mm (from left edge)

Bottom Row:
[CV OUT]      [TRIG OUT]      [CC OUT]      [MIDI OUT]      [MIDI IN]
 27mm         39mm            51mm          72mm            92mm
```

**Installation:**
1. Insert LED from OUTSIDE through 3.2mm back panel hole
2. LED sits flush or slightly recessed (flat-top style)
3. Bend leads 90° inside enclosure
4. Solder leads to protoboard traces
5. **Polarity:** Longer lead = Anode (+), Short lead = Cathode (-)

### White LED Wiring (5 total)

**Standard Circuit (all white LEDs identical):**
```
GPIO Pin → [150Ω resistor] → LED Anode (+)
LED Cathode (-) → GND
```

**Individual Mappings:**
1. **CV IN (INPUT board):** D4 → 150Ω → LED → GND
2. **CV OUT (OUTPUT board):** D12 → 150Ω → LED → GND
3. **CC OUT (OUTPUT board):** D25 → 150Ω → LED → GND
4. **MIDI OUT (OUTPUT board):** CAN_TX → 150Ω → LED → GND
5. **MIDI IN (OUTPUT board):** A5 → 150Ω → LED → GND

### RGB LED Wiring (2 total - Common Cathode)

**Standard Circuit (both RGB LEDs identical):**
```
GPIO Red → [150Ω] → RED anode
GPIO Green → [150Ω] → GREEN anode
GPIO Blue → [150Ω] → BLUE anode
All cathodes → Common cathode → GND
```

**RGB LED Pinout (flat side up):**
```
[R]  [G]  [B]  [Common Cathode]
 1    2    3         4 (longest pin)
```

**TRIG IN RGB (INPUT board):**
- D11 → 150Ω → Red anode
- D23 → 150Ω → Green anode
- D24 → 150Ω → Blue anode
- Common cathode → GND

**Color Behavior:**
- **GREEN:** V-Trig mode detected (A4 > 2.0V)
- **RED:** S-Trig mode detected (A4 < 1.0V)
- **OFF:** No gate signal present
- **Brightness:** Varies with input signal strength

**TRIG OUT RGB (OUTPUT board):**
- A0 → 150Ω → Red anode
- A1 → 150Ω → Green anode
- A2 → 150Ω → Blue anode
- Common cathode → GND

**Color Behavior:**
- **GREEN:** V-Trig mode active (software selected)
- **RED:** S-Trig mode active (software selected)
- **OFF:** No gate output
- **Brightness:** Varies with gate activity

### Software Detection Logic

**Input Monitoring (CV IN, TRIG IN):**
```python
Sample A3/A4 at 100Hz
if A3 > 0.1V: turn_on_led(D4)   # CV IN activity
if A4 > 2.0V: turn_on_led(D23, green)   # V-Trig
if A4 < 1.0V: turn_on_led(D11, red)     # S-Trig
```

**Output Status (CV OUT, TRIG OUT, CC OUT):**
```python
if dac_a_active: turn_on_led(D12)   # CV OUT
if dac_b_active: turn_on_led(D25)   # CC OUT
if gate_mode == vtrig: turn_on_led(A1, green)
if gate_mode == strig: turn_on_led(A0, red)
```

**MIDI Activity (UART monitoring):**
```python
if uart_tx_activity: pulse_led(CAN_TX, 50ms)
if uart_rx_activity: pulse_led(A5, 50ms)
```

---

## SECTION 9: POWER DISTRIBUTION & DECOUPLING

### Power Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│ Power Source                                        │
│ - USB-C (primary, 5V 500mA)                        │
│ - LiPo Battery (secondary, 3.7V via boost)         │
└────────────────────┬────────────────────────────────┘
                     │
                     ├─→ Feather M4 (USB or BAT input)
                     │     ├─→ 3.3V rail (logic)
                     │     └─→ 5V rail (peripherals)
                     │
                     ├─→ OUTPUT Board (5V + GND from Feather)
                     │     ├─→ C1: 47µF bulk
                     │     ├─→ C2: 0.1µF bypass
                     │     ├─→ MCP4728 (VCC=5V, GND)
                     │     ├─→ MIDI FeatherWing (VCC=5V, GND)
                     │     └─→ Output stage (100Ω + 100nF filters)
                     │
                     └─→ INPUT Board (5V + GND from Feather)
                           ├─→ C1: 47µF bulk
                           ├─→ C2: 0.1µF bypass
                           └─→ Protection circuits (passive)
```

### Current Budget (Typical Operation)

| Circuit | Component | Current | Notes |
|---------|-----------|---------|-------|
| **M4 Core** | Feather M4 | 30-50mA | Active processing |
| **Display** | OLED FeatherWing | 20-30mA | Display + buttons |
| **MIDI** | MIDI FeatherWing | 10-15mA | I/O buffering |
| **DAC** | MCP4728 | ~10mA | Generating CV |
| **Protection** | Passive circuits | <1mA | Voltage dividers |
| **Activity LEDs** | 5× white + 2× RGB | ~20mA | When active |
| | | | |
| **TOTAL TYPICAL** | | **~100-150mA** | Well under 500mA |
| **TOTAL MAXIMUM** | | **<200mA** | All LEDs + CPU full load |

**Battery Runtime (500mAh LiPo):**
- Typical: 500mAh / 100mA = 5 hours
- Optimized (LEDs dimmed): 500mAh / 70mA = 7 hours
- Sleep mode (GPIO only): 500mAh / 10mA = 50 hours

### Decoupling Strategy

**Purpose:** Remove high-frequency noise from power supply

**Topology:**
```
Ferrite bead (optional) ──→ Bulk capacitor ──→ IC VCC
                                            ↓
                                        Bypass capacitor
                                            ↓
                                           GND
```

**Placement Rules:**
- Bulk caps: Within 1 inch of power input to board
- Bypass caps: Within 0.25 inch of IC power pin
- Multiple caps: Better than single large cap (reduces impedance)

**Our Implementation:**

**OUTPUT Board:**
- C1 (47µF): Near USB-C input or power header
- C2 (0.1µF): Nearby, high-frequency bypass
- C3 (0.1µF): **Very close to MCP4728 VCC pin** (critical)
- C4 (0.1µF): Spare, near other high-impedance nodes

**INPUT Board:**
- C1 (47µF): Near 5V input header
- C2 (0.1µF): Nearby, high-frequency bypass
- C3, C4 (100nF): With protection circuit capacitors

**Why 47µF + 0.1µF combination?**
- 47µF: Low impedance at medium frequencies (100Hz-1kHz)
- 0.1µF: Very low impedance at high frequencies (10kHz+)
- Together: Covers full audio spectrum (20Hz-20kHz)

---

## SECTION 10: EXTERNAL INPUT SIGNAL COMPATIBILITY

### CV Pitch Input (A3) - Specification

**Accepted Voltage Range:** 0V to 5V (maps to 0V-2.62V internally)

**Standard CV Sources:**
| Source | Output | Scaling | Notes |
|--------|--------|---------|-------|
| **Eurorack Oscillator** | 0-10V | 1V/octave | Hardware scales to 0-5V |
| **Synthesizer Keyboard** | 0-5V | 1V/octave | Direct connection |
| **Sequencer** | 0-5V | Variable | Check spec sheet |
| **LFO (modular)** | -5 to +5V | Bipolar | Will read as 0V (negative clipped) |

**ADC Scaling (Internal):**
```
External Voltage → Divider × 0.524 → BAT85 clamp (3.3V max) → ADC
5V input → 2.62V at A3 ✓
```

### Gate Input (A4) - Specification

**Accepted Voltage Range:** 0V to 5V

**Signal Types:**
| Type | Standard | Detection | Voltage |
|------|----------|-----------|---------|
| **V-Trig** | Eurorack/Modern | HIGH = voltage > 2.0V | 0-5V |
| **S-Trig** | Vintage (ARP, Korg) | HIGH = voltage < 1.0V | 0-5V or 0-12V |

**Why Voltage Divider Essential:**
- Vintage synths may output 5V, 12V, or higher
- Divider scales any input to safe 0-2.62V
- BAT85 diode provides additional safety
- **Can accept even 24V inputs** (would be scaled to ~12.6V, clamped to 3.3V)

**Software Detects:**
```python
if gate_voltage > 2.0V: "V-Trig detected"
elif gate_voltage < 1.0V: "S-Trig detected"
else: "No gate signal"
```

### MIDI Input (DIN-5 Jack) - Specification

**Standard:** MIDI 1.0 (31.25 kbaud, current loop)

**Supported Messages:**
- **Note On/Off:** Full 0-127 range
- **CC (Control Change):** MIDI Learn for parameter mapping
- **Pitch Bend:** Modulation CV output
- **Clock:** MIDI Clock sync (MIDI FeatherWing future)
- **All other messages:** Pass-through

**MIDI FeatherWing Specs:**
- Optocoupler isolation on input (protects M4 from ground loops)
- Buffered output on TX
- Address: 0x4D (not currently used, UART-based)
- Baud rate: 31250 (MIDI standard)

---

## SECTION 11: ENCLOSURE PHYSICAL LAYOUT

### Dimensions Summary

| Dimension | Value | Notes |
|-----------|-------|-------|
| **Enclosure Width** | 70mm | Accommodates Feather + wings |
| **Enclosure Depth** | 100mm | Rear clearance for DIN-5 jacks |
| **Enclosure Height** | 35mm | Desktop form factor |
| **Protoboard Width** | 90mm | Custom-cut (with ~7mm overhang) |
| **Protoboard Depth** | 55mm | Custom-cut from ElectroCookie |
| **Internal Stack Height** | ~27mm | M4 + OLED + headers |

### Component Physical Positions

**Vertical Stack (front to back view):**
```
Feather M4 stack (top)
├─ OLED FeatherWing (display visible through top window)
├─ Feather M4 (USB-C facing rear)
└─ MIDI FeatherWing (MIDI jacks at rear)
        ↓ (15mm gap)
INPUT Board (middle)
├─ CV IN jack (20mm from left edge)
├─ TRIG IN jack (32mm from left edge)
└─ Protection circuits (underneath, toward rear)
        ↓ (10mm gap)
OUTPUT Board (bottom)
├─ USB-C breakout (8mm from left edge)
├─ CV OUT jack (20mm)
├─ TRIG OUT jack (32mm)
├─ CC OUT jack (44mm)
├─ MIDI OUT jack (65mm)
├─ MIDI IN jack (85mm)
├─ MCP4728 DAC (center, on standoffs)
└─ S-Trig transistor circuit (near TRIG OUT jack)
        ↓ (10mm gap)
Enclosure Base
├─ Battery pocket (front-left)
├─ Boost module (front-center)
└─ Slide switch mount (left side)
```

### Back Panel Rear Edge Positions

**All measurements from left edge (horizontal):**

```
TOP ROW (INPUT board rear):
CV IN jack: 20mm from left
TRIG IN jack: 32mm from left

BOTTOM ROW (OUTPUT board rear):
USB-C cutout: 8mm from left
CV OUT jack: 20mm from left
TRIG OUT jack: 32mm from left
CC OUT jack: 44mm from left
MIDI OUT jack: 65mm from left
MIDI IN jack: 85mm from left
```

**LED Positions (7mm to right of jack center):**
```
TOP ROW:
CV IN LED: 27mm
TRIG IN RGB: 39mm

BOTTOM ROW:
CV OUT LED: 27mm
TRIG OUT RGB: 39mm
CC OUT LED: 51mm
MIDI OUT LED: 72mm
MIDI IN LED: 92mm
```

---

## SECTION 12: ASSEMBLY CRITICAL NOTES

### Soldering & Construction

**Component Quality:**
- All resistors: 1% metal film (for precision in voltage dividers)
- All capacitors: Ceramic X7R/C0G or low-ESR electrolytic
- Diodes: BAT85 Schottky (fast switching, low forward drop)
- Transistor: 2N3904 (or 2N2222) general-purpose NPN

**Key Solder Points (Check twice):**
1. MCP4728 power pins (VCC, VSS) - touching both pads
2. Voltage divider tap points (must have clean junction)
3. BAT85 diode polarity (cathode marking must be correct)
4. LED polarities (longer lead = anode)
5. Jack sleeve connections (GND rail)

### Testing Sequence (Before Integration)

1. **Continuity Test:**
   - Verify 5V rail is connected throughout
   - Verify all GND connections are clean
   - No shorts between 5V and GND

2. **Voltage Divider Test (INPUT board):**
   - Apply 5V to CV IN jack
   - Measure at tap point: should be ~2.62V
   - Measure at ADC pin (A3): should be ~2.62V (with BAT85 clamp)

3. **MCP4728 Test (OUTPUT board):**
   - Power on, verify I2C scan detects 0x60
   - Set channel A to max: measure 4.8-5.0V at CV OUT jack
   - Set channel C to max: measure 4.8-5.0V at TRIG OUT jack

4. **S-Trig Test:**
   - Set D10 LOW: measure open circuit at TRIG OUT jack
   - Set D10 HIGH: measure <0.2Ω resistance to GND

5. **LED Test:**
   - Drive each GPIO HIGH: verify LED illuminates
   - Verify correct color for RGB LEDs
   - Check for dim or non-lighting LEDs

### Key Schematic Points for CAD Import

**Critical dimensions for schematic layout:**

**OUTPUT Board:**
```
Front (component side):
[+5V RAIL] ════════════════════════════════════
  C1(47µF) C2(0.1µF)
  
  MCP4728 Module (centered, 35-50mm from front)
  ├─ VCC to +5V
  ├─ GND to GND rail
  ├─ SDA, SCL to headers
  └─ Outputs: Ch A→R1, Ch B→R2, Ch C→R3, Ch D→R4
  
  MIDI FeatherWing (right side, ~65mm from front)
  
[GND RAIL] ═════════════════════════════════════
```

**INPUT Board:**
```
Front (component side):
[+5V RAIL] ════════════════════════════════════
  C1(47µF) C2(0.1µF)
  
  Left section (CV IN):
  R1-R2 (voltage divider)
  R3 (series to ADC)
  C3 (filter)
  D1 (BAT85 clamp)
  
  Center section (TRIG IN):
  R5-R6 (voltage divider)
  R7 (series to ADC)
  C4 (filter)
  D2 (BAT85 clamp)
  
[GND RAIL] ═════════════════════════════════════
```

---

## SECTION 13: BILL OF MATERIALS - COMPLETE

### PROTOBOARD COMPONENTS ONLY (excludes Feather stack)

| Qty | Component | Value/Part | Unit Cost | Total | Purpose |
|-----|-----------|------------|-----------|-------|---------|
| **OUTPUT BOARD** |
| 1 | MCP4728 Module | I2C DAC Breakout | $8.95 | $8.95 | 4-channel CV output |
| 1 | Electrolytic Cap | 47µF 16V | $0.15 | $0.15 | Bulk power supply |
| 4 | Ceramic Cap | 0.1µF 50V | $0.05 | $0.20 | Bypass/decoupling |
| 3 | Ceramic Cap | 100nF 50V | $0.05 | $0.15 | Output filters (CV, TRIG, CC) |
| 1 | Ceramic Cap | 100nF 50V | $0.05 | $0.05 | Spare/future |
| 4 | Resistor | 100Ω 1/4W | $0.02 | $0.08 | Output protection |
| 1 | Resistor | 1kΩ 1/4W | $0.02 | $0.02 | Transistor base limiting |
| 7 | Resistor | 150Ω 1/4W | $0.02 | $0.14 | LED current limiting |
| 1 | NPN Trans | 2N3904 | $0.10 | $0.10 | S-Trig switching |
| 3 | 1/8" Mono Jack | Panel mount | $0.50 | $1.50 | CV OUT, TRIG OUT, CC OUT |
| 2 | DIN-5 Jack | Panel mount | $2.50 | $5.00 | MIDI IN/OUT |
| 1 | USB-C Breakout | Panel mount | $1.00 | $1.00 | Power/programming extension |
| 4 | LED | 3mm white | $0.15 | $0.60 | Activity indicators |
| 1 | RGB LED | 3mm common cathode | $0.30 | $0.30 | TRIG OUT mode indicator |
| 1 | Header | 12-pin male 0.1" | $0.30 | $0.30 | To Feather stack |
| 4 | Standoff | M2.5 × 10mm | $0.20 | $0.80 | MCP4728 mounting |
| | **OUTPUT Subtotal** | | | **$19.44** | |
| | | | | | |
| **INPUT BOARD** |
| 1 | Electrolytic Cap | 47µF 16V | $0.15 | $0.15 | Bulk power supply |
| 1 | Ceramic Cap | 0.1µF 50V | $0.05 | $0.05 | Bypass |
| 2 | Ceramic Cap | 100nF 50V | $0.05 | $0.10 | Input filtering |
| 4 | Resistor | 10kΩ 1/4W | $0.02 | $0.08 | Voltage dividers |
| 2 | Resistor | 22kΩ 1/4W | $0.02 | $0.04 | Voltage dividers |
| 2 | Resistor | 10kΩ 1/4W | $0.02 | $0.04 | Series protection |
| 4 | Resistor | 150Ω 1/4W | $0.02 | $0.08 | LED current limiting |
| 2 | Diode | BAT85 Schottky | $0.10 | $0.20 | Overvoltage clamps |
| 2 | 1/8" Mono Jack | Panel mount | $0.50 | $1.00 | CV IN, TRIG IN |
| 1 | LED | 3mm white | $0.15 | $0.15 | CV IN activity |
| 1 | RGB LED | 3mm common cathode | $0.30 | $0.30 | TRIG IN mode indicator |
| 1 | Header | 8-pin male 0.1" | $0.20 | $0.20 | To Feather stack |
| | **INPUT Subtotal** | | | **$2.39** | |
| | | | | | |
| **WIRING & HARDWARE** |
| | Wire | 22-24 AWG | $0.50/m | $1.00 | Internal connections |
| | Solder | Solder | bulk | $0.50 | Assembly |
| 20 | Screw | M3 various | $0.10 | $2.00 | Board & standoff mounting |
| 8 | Standoff | M3 × 10mm | $0.20 | $1.60 | Board-to-board spacing |
| | **HARDWARE Subtotal** | | | **$5.10** | |
| | | | | | |
| | **PROTOBOARD TOTAL** | | | **$26.93** | |

### Full System BOM (with Feather Stack)

**Add to above:**
- Feather M4 CAN Express: $24.95
- OLED FeatherWing: $14.95
- MIDI FeatherWing: $9.95
- LiPo Battery (500-1200mAh): $7.95
- USB-C extension cable: $2.00

**System Total: ~$100-110** (including enclosure printing ~$3-5)

---

## SECTION 14: VERIFICATION CHECKLIST

### Pre-Assembly (Design Review)

- [ ] All resistor values verified (voltage dividers: 10k/10k/22k)
- [ ] All capacitor voltages adequate (≥16V electrolytic, ≥50V ceramic)
- [ ] DAC channel assignments correct (A=CV, B=CC, C=V-Trig, D=spare)
- [ ] LED GPIO pins don't conflict with I2C or buttons
- [ ] Voltage divider scaling confirmed (0.524× factor)
- [ ] BAT85 diode orientation marked (cathode to 3.3V)
- [ ] 2N3904 transistor pinout verified (E/B/C from left)
- [ ] Jack wiring diagram complete
- [ ] LED current calculations done (150Ω resistors adequate)
- [ ] Power budget reviewed (<200mA total)

### During Assembly

- [ ] Solder joints visually inspected (shiny, not dull)
- [ ] No cold solder joints (visually inspect)
- [ ] No solder bridges between pads
- [ ] Capacitor polarities correct (stripe side on electrolytic)
- [ ] Diode polarities marked (cathode = black stripe)
- [ ] Resistor bands read (brown-black-red = 1k, etc.)
- [ ] All header pins soldered cleanly
- [ ] MCP4728 sits firmly on standoffs
- [ ] Jacks aligned perpendicular to board
- [ ] Wire runs don't cross high-voltage areas unnecessarily

### Post-Assembly - Electrical Tests

- [ ] Multimeter: 5V rail = 5.0V ±0.2V
- [ ] Multimeter: GND rail = 0V (reference)
- [ ] Multimeter: No short between 5V and GND (<10MΩ)
- [ ] Multimeter: Voltage divider tap ≈ 2.62V when jack has 5V
- [ ] I2C scan detects 0x60 (MCP4728)
- [ ] MCP4728 responds to I2C commands
- [ ] All GPIO pins output 3.3V when HIGH
- [ ] All GPIO pins read ~0V when LOW
- [ ] ADC pins read ~2.62V with 5V at jack

### Post-Assembly - Functional Tests

- [ ] Set DAC Channel A to max: verify CV OUT reads 4.8-5.0V
- [ ] Set DAC Channel C to max: verify TRIG OUT reads 4.8-5.0V
- [ ] Drive D10 HIGH: verify S-Trig pulls to <0.2Ω
- [ ] Drive D10 LOW: verify S-Trig is open circuit
- [ ] All 5 white LEDs illuminate when GPIO driven HIGH
- [ ] RGB TRIG IN LED shows GREEN with 3V+ on gate input
- [ ] RGB TRIG IN LED shows RED with <1V on gate input
- [ ] RGB TRIG OUT LED shows GREEN in V-Trig mode
- [ ] RGB TRIG OUT LED shows RED in S-Trig mode
- [ ] No flickering or unstable behavior

---

## SECTION 15: TROUBLESHOOTING REFERENCE

### Symptom: No voltage on CV OUT jack

**Checklist:**
1. Verify MCP4728 I2C communication (`i2c.scan()` detects 0x60)
2. Verify `dac.wakeup()` was called (clears power-down mode)
3. Verify `vref = Vref.VDD` set (not using internal 2.048V)
4. Check R1, R2 100Ω resistors for cold solder joints
5. Check C6, C7 filter capacitors are connected
6. Measure voltage at MCP4728 Channel A output pin directly
7. If all else fails: check power to MCP4728 VCC (should be 5V)

### Symptom: CV output reads 0.03-0.31V (wrong scaling)

**Cause:** Using `.value` property instead of `.raw_value`
```python
# WRONG
dac.channel_a.value = 4095  # Gets divided by 16!

# CORRECT
dac.channel_a.raw_value = 4095  # Direct 12-bit control
```

### Symptom: Voltage divider not scaling correctly

**Checklist:**
1. Verify R1, R2 are 10kΩ (not 1kΩ or 100kΩ)
2. Verify R3 (or R4 for TRIG) is 22kΩ (not 20kΩ or 24kΩ)
3. Measure tap point voltage with multimeter
4. Apply known 5V source (USB power supply)
5. Verify scaling: Vout = 5V × 0.524 = 2.62V

### Symptom: S-Trig not switching

**Checklist:**
1. Verify 2N3904 transistor orientation (E/B/C)
2. Verify base resistor R5 is 1kΩ (not 10kΩ)
3. Measure D10 GPIO output: should be 3.3V when HIGH
4. Test transistor directly with multimeter (diode mode)
5. Check R6 collector resistor is 100Ω

### Symptom: LED doesn't light up

**Checklist:**
1. Verify GPIO pin can source 3.3V (test with multimeter)
2. Verify 150Ω resistor installed in series
3. Check LED polarity (longer lead = anode, to resistor)
4. Verify GND connection is solid
5. Try replacing LED (may be defective)
6. Check for cold solder joints on LED leads

### Symptom: MIDI not working

**Checklist:**
1. Verify DIN-5 jack pins 4 and 5 are connected
2. Verify MIDI FeatherWing is stacked correctly
3. Test with known MIDI device (controller or sequencer)
4. Check MIDI baud rate is 31250
5. Verify pin 4/5 wiring matches standard (pin 5 = signal, pin 4 = return)

---

## SUMMARY: COMPLETE COMPONENT LIST FOR SCHEMATICS

### Schematic Symbols Required

**Resistors:**
- 100Ω (×5)
- 150Ω (×11)
- 1kΩ (×1)
- 10kΩ (×8)
- 22kΩ (×2)

**Capacitors:**
- 47µF 16V electrolytic (×2)
- 0.1µF 50V ceramic (×6)
- 100nF 50V ceramic (×5)

**Diodes:**
- BAT85 Schottky (×2)

**ICs:**
- MCP4728 (12-bit DAC)
- 2N3904 NPN transistor (×1)

**Connectors:**
- 1/8" TRS mono jacks (×5)
- 5-pin DIN jacks (×2)
- USB-C breakout (×1)
- Pin headers (various)

**LEDs:**
- 3mm white flat-top (×5)
- 3mm RGB common cathode (×2)

**Feather Stack (not on protoboards):**
- Feather M4 CAN Express
- OLED FeatherWing
- MIDI FeatherWing

---

**END OF COMPREHENSIVE AUDIT REPORT**

**Generated:** 2025-11-03
**Status:** Complete - All information for production-ready schematics
**Next Steps:** Import into EDA tool (KiCAD, Eagle, Altium) and route PCB

