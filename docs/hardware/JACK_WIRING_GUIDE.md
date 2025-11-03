# Jack Wiring Guide - Professional Assembly Reference

## Overview

This document provides complete wiring instructions for connecting all back panel jacks to the protoboards. All jacks are **soldered directly to the rear edges** of the boards - the jack barrels pass through the enclosure clearance holes and the internal boards provide all mechanical support.

**Board Stack (bottom to top):**
1. OUTPUT Board (75mm × 50mm) - Bottom row jacks
2. INPUT Board (75mm × 50mm) - Top row jacks
3. Feather Stack (M4 + MIDI FeatherWing + OLED FeatherWing)

---

## Wire Color Standard

Follow the **RED/WHITE convention** for consistency:

- **RED** = Signal/hot wire
- **WHITE** = Ground wire
- **BLACK** = GND rail connections
- **YELLOW** = 5V power
- **GREEN** = I2C SDA
- **BLUE** = I2C SCL

---

## OUTPUT BOARD (Bottom Board) - Rear Panel Bottom Row

### Board Rear Edge Layout
```
  13mm      23mm      33mm
   ↓         ↓         ↓
[CV OUT] [V/S-TRIG] [CUSTOM CC]

All 1/8" (3.5mm) mono jacks, 10mm spacing
```

---

### 1. CV OUT Jack (13mm from left edge)

**Jack Type:** 1/8" (3.5mm) mono jack, panel mount

**Circuit Path:**
```
MCP4728 CH A → [100Ω R1] → [100nF C6] → CV OUT Jack TIP
                                           │
                                         SLEEVE → GND
```

**Wiring Instructions:**
1. **TIP (signal):**
   - Solder **RED** wire from jack TIP to the junction of R1/C6
   - Junction point is after the 100Ω protection resistor

2. **SLEEVE (ground):**
   - Solder **WHITE** wire from jack SLEEVE to GND rail

**Component Locations (on OUTPUT board):**
- R1 (100Ω): Near MCP4728 Channel A output
- C6 (100nF): Between R1 and jack connection point
- MCP4728 position: Center of board on M2.5 standoffs

---

### 2. V-TRIG/S-TRIG OUT Jack (23mm from left edge)

**Jack Type:** 1/8" (3.5mm) mono jack, panel mount

**Special Note:** This jack carries **TWO different signals** depending on mode:
- **V-Trig mode:** Direct DAC output (0-5V gates)
- **S-Trig mode:** NPN transistor pulls to GND (active-low gates)

**Circuit Path:**
```
V-TRIG PATH:
MCP4728 CH C → [100Ω R3] ───────────────────┐
                                             ├→ TRIG Jack TIP
S-TRIG PATH:                                 │
D10 → [1kΩ R5] → NPN Base                    │
             NPN Collector → [100Ω R6] ──────┘
             NPN Emitter → GND

TRIG Jack SLEEVE → GND
```

**Wiring Instructions:**

1. **TIP (dual signal):**
   - Connect **RED** wire from jack TIP to the junction where V-Trig (R3) and S-Trig (R6) meet
   - This junction receives signals from BOTH paths

2. **SLEEVE (ground):**
   - Solder **WHITE** wire from jack SLEEVE to GND rail

**Component Locations (on OUTPUT board):**
- R3 (100Ω): From MCP4728 Channel C to junction
- R6 (100Ω): From NPN collector to junction
- R5 (1kΩ): From D10 header pin to NPN base
- NPN (2N3904): Near D10 connection area
  - **Collector** → R6 → TIP junction
  - **Base** → R5 → D10
  - **Emitter** → GND

**NPN Transistor Pinout (2N3904, flat side facing you):**
```
   E  B  C
   │  │  │
  ───────
  │     │
  └─────┘
```

---

### 3. CUSTOM CC Jack (33mm from left edge)

**Jack Type:** 1/8" (3.5mm) mono jack, panel mount

**Circuit Path:**
```
MCP4728 CH B → [100Ω R2] → [100nF C7] → CUSTOM CC Jack TIP
                                           │
                                         SLEEVE → GND
```

**Wiring Instructions:**

1. **TIP (signal):**
   - Solder **RED** wire from jack TIP to the junction of R2/C7

2. **SLEEVE (ground):**
   - Solder **WHITE** wire from jack SLEEVE to GND rail

**Component Locations (on OUTPUT board):**
- R2 (100Ω): Near MCP4728 Channel B output
- C7 (100nF): Between R2 and jack connection point

---

### 4. MCP4728 Module Connections

**Module Type:** 4-channel 12-bit I2C DAC breakout board

**Mounting:** 4× M2.5 standoffs to OUTPUT board (center position)

**Pin Connections:**

| MCP4728 Pin | Wire Color | Destination | Notes |
|-------------|------------|-------------|-------|
| VCC | YELLOW | +5V rail | Power supply |
| GND | BLACK | GND rail | Ground reference |
| SDA | GREEN | SDA header pin | I2C data to Feather |
| SCL | BLUE | SCL header pin | I2C clock to Feather |
| CH A (VOUT A) | - | R1 (100Ω) | CV Out path |
| CH B (VOUT B) | - | R2 (100Ω) | Custom CC path |
| CH C (VOUT C) | - | R3 (100Ω) | V-Trig path |
| CH D (VOUT D) | - | R4 (100Ω) | Future expansion |

---

### 5. OUTPUT Board Header to Feather Stack

**Header Type:** 5-pin male 0.1" header

**Pin Assignments (left to right):**

| Pin # | Signal | Wire Color | Destination | Purpose |
|-------|--------|------------|-------------|---------|
| 1 | SDA | GREEN | Feather SDA | MCP4728 I2C data |
| 2 | SCL | BLUE | Feather SCL | MCP4728 I2C clock |
| 3 | +5V | YELLOW | Feather 5V | Power from Feather |
| 4 | GND | BLACK | Feather GND | Ground return |
| 5 | D10 | ORANGE | Feather D10 | S-Trig control signal |

---

## INPUT BOARD (Top Board) - Rear Panel Top Row

### Board Rear Edge Layout
```
  13mm     23mm       35.5mm      55.5mm
   ↓        ↓           ↓           ↓
[CV IN] [GATE IN]  [MIDI IN]  [MIDI OUT]

         58.5mm (bottom row)
           ↓
        [USB-C]
```

---

### 6. CV IN Jack (13mm from left edge, top row)

**Jack Type:** 1/8" (3.5mm) mono jack, panel mount

**Circuit Path:**
```
CV IN Jack TIP → [R1 10kΩ] → [R2 10kΩ] → [R4 22kΩ] → GND
                                  ↓
                            Tap Point
                                  ↓
                         [R3 10kΩ] → [C3 100nF] → [D1 BAT85] → A3
                                         │             │
                                        GND         +3.3V

CV IN Jack SLEEVE → GND
```

**Voltage Scaling:** External 0-5V → Internal 0-2.62V (safe for 3.3V ADC)

**Wiring Instructions:**

1. **TIP (signal input):**
   - Solder **RED** wire from jack TIP to start of voltage divider (R1)

2. **SLEEVE (ground):**
   - Solder **WHITE** wire from jack SLEEVE to GND rail

**Component Locations (on INPUT board, left area):**
- R1, R2 (10kΩ each): Series voltage divider
- R4 (22kΩ): Divider to ground
- Tap point: Junction of R2/R3/R4
- R3 (10kΩ): Series protection to ADC
- C3 (100nF): Low-pass filter capacitor to GND
- D1 (BAT85): Schottky diode clamp to +3.3V rail
- Output: Connect to A3 header pin

**Protection Features:**
- 10kΩ series resistor limits current if ADC shorts
- 100nF capacitor filters RF noise (cutoff ~160Hz)
- BAT85 diode clamps overvoltage to 3.3V

---

### 7. GATE IN Jack (23mm from left edge, top row)

**Jack Type:** 1/8" (3.5mm) mono jack, panel mount

**Circuit Path:**
```
GATE IN Jack TIP → [R5 10kΩ] → [R6 10kΩ] → [R8 22kΩ] → GND
                                   ↓
                             Tap Point
                                   ↓
                          [R7 10kΩ] → [C4 100nF] → [D2 BAT85] → A4
                                          │             │
                                         GND         +3.3V

GATE IN Jack SLEEVE → GND
```

**Voltage Scaling:** External 0-5V → Internal 0-2.62V (safe for 3.3V ADC)

**Wiring Instructions:**

1. **TIP (signal input):**
   - Solder **RED** wire from jack TIP to start of voltage divider (R5)

2. **SLEEVE (ground):**
   - Solder **WHITE** wire from jack SLEEVE to GND rail

**Component Locations (on INPUT board, left area):**
- R5, R6 (10kΩ each): Series voltage divider
- R8 (22kΩ): Divider to ground
- Tap point: Junction of R6/R7/R8
- R7 (10kΩ): Series protection to ADC
- C4 (100nF): Low-pass filter capacitor to GND
- D2 (BAT85): Schottky diode clamp to +3.3V rail
- Output: Connect to A4 header pin

---

### 8. MIDI IN Jack (35.5mm from left edge, top row)

**Jack Type:** 5-pin DIN jack, panel mount (only pins 4 and 5 used)

**Circuit Path:**
```
MIDI IN Jack Pin 5 → MIDI FeatherWing RX IN (via optocoupler)
MIDI IN Jack Pin 4 → MIDI FeatherWing Current Loop Return

(Pins 1, 2, 3 not connected - standard MIDI DIN wiring)
```

**5-Pin DIN Pinout (looking at back of jack):**
```
     2
   ┌───┐
  5│   │1
   │ O │     O = center hole (mechanical)
  4│   │3
   └───┘
```

**Wiring Instructions:**

1. **Pin 5 (MIDI signal):**
   - Solder wire to MIDI FeatherWing **RX IN** terminal

2. **Pin 4 (current loop return):**
   - Solder wire to MIDI FeatherWing **RX RETURN** terminal

3. **Pins 1, 2, 3:**
   - Leave unconnected (standard MIDI specification)

**MIDI FeatherWing Connection:**
- The MIDI FeatherWing has built-in optocoupler isolation
- No external components needed
- FeatherWing RX connects to Feather D0 (Serial RX) internally

---

### 9. MIDI OUT Jack (55.5mm from left edge, top row)

**Jack Type:** 5-pin DIN jack, panel mount (only pins 4 and 5 used)

**Circuit Path:**
```
MIDI FeatherWing TX OUT → MIDI OUT Jack Pin 5
MIDI FeatherWing TX Current Loop → MIDI OUT Jack Pin 4

(Pins 1, 2, 3 not connected - standard MIDI DIN wiring)
```

**Wiring Instructions:**

1. **Pin 5 (MIDI signal):**
   - Solder wire from MIDI FeatherWing **TX OUT** terminal

2. **Pin 4 (current loop):**
   - Solder wire from MIDI FeatherWing **TX CURRENT** terminal

3. **Pins 1, 2, 3:**
   - Leave unconnected (standard MIDI specification)

**MIDI FeatherWing Connection:**
- The MIDI FeatherWing provides buffered MIDI output
- Built-in current limiting resistor (220Ω)
- FeatherWing TX connects to Feather D1 (Serial TX) internally

**MIDI DIN Standard:**
- MIDI uses a current loop, NOT voltage signaling
- Pin 5 = Signal
- Pin 4 = Current return
- Pins 1-3 unused in modern MIDI (legacy shield ground)

---

### 10. USB-C Panel Mount (58.5mm from left edge, bottom row)

**Jack Type:** USB-C panel mount breakout board

**Connection Method:** USB-C extension cable

**Wiring Instructions:**

1. **Feather M4 Side:**
   - Connect USB-C extension cable **male end** to Feather M4 USB-C port
   - Route cable through internal enclosure space

2. **Panel Mount Side:**
   - Connect USB-C extension cable **female end** to panel mount breakout
   - Panel mount breakout passes through enclosure cutout (9.5mm × 3.8mm)

3. **Mechanical Mounting:**
   - Panel mount breakout may have screw holes - if so, secure to INPUT board
   - If no screw holes, use hot glue or double-sided tape to secure breakout to board

**Purpose:**
- Programming access to Feather M4
- Serial console via USB CDC
- Power supply (when not using external 5V)

**Alignment Note:**
- USB-C positioned at BOTTOM ROW height (same as OUTPUT board jacks)
- Right edge aligns with MIDI Out right edge (forms clean grid)

---

### 11. INPUT Board Header to Feather Stack

**Header Type:** 5-pin male 0.1" header

**Pin Assignments (left to right):**

| Pin # | Signal | Wire Color | Destination | Purpose |
|-------|--------|------------|-------------|---------|
| 1 | A3 | RED | Feather A3 | CV Pitch input (0-2.62V) |
| 2 | A4 | ORANGE | Feather A4 | Gate input (0-2.62V) |
| 3 | GND | BLACK | Feather GND | Ground return |
| 4 | MIDI TX | PURPLE | MIDI Wing D1 | MIDI Out data (internal) |
| 5 | MIDI RX | GRAY | MIDI Wing D0 | MIDI In data (internal) |

**Note:** MIDI TX/RX pins connect internally within the Feather stack - the MIDI FeatherWing sits between the Feather M4 and the OLED FeatherWing, and uses D0/D1 pins via the stacking headers.

---

## Power Distribution

### Power Flow Diagram
```
Feather M4 USB-C
      ↓ (5V, GND)
      ├→ OLED FeatherWing (via stacking headers)
      ├→ MIDI FeatherWing (via stacking headers)
      ├→ OUTPUT Board 5-pin header
      │     ↓
      │   MCP4728 module (VCC, GND)
      │     ↓
      │   OUTPUT Board local caps (47µF + 0.1µF)
      │
      └→ INPUT Board 5-pin header
            ↓
          INPUT Board local caps (47µF + 0.1µF)
```

### Current Budget
| Component | Typical Current | Notes |
|-----------|----------------|-------|
| Feather M4 | 30-50mA | Active processing |
| OLED FeatherWing | 20-30mA | Display + buttons |
| MIDI FeatherWing | 10-15mA | MIDI I/O buffering |
| MCP4728 | 10mA | 4-channel DAC |
| Protection circuits | <5mA | Passive components |
| **TOTAL** | **<100mA** | Well under USB 500mA limit |

### Decoupling Strategy
- **OUTPUT Board:** 47µF + 0.1µF at 5V rail
- **INPUT Board:** 47µF + 0.1µF at 5V rail
- **MCP4728:** 0.1µF decoupling cap at VCC pin (very close to IC)

---

## Assembly Sequence

### Step 1: Populate OUTPUT Board
1. Solder all resistors (R1-R6)
2. Solder all capacitors (C1-C8)
3. Solder NPN transistor (2N3904) - watch orientation!
4. Mount MCP4728 module on M2.5 standoffs
5. Solder 5-pin header (for Feather connection)
6. Solder power rails (5V and GND traces)

### Step 2: Populate INPUT Board
1. Solder all resistors (R1-R8)
2. Solder all capacitors (C1-C4)
3. Solder Schottky diodes (D1, D2) - **watch polarity!**
4. Solder 5-pin header (for Feather connection)
5. Solder power rails (5V and GND traces)

### Step 3: Mount Jacks to OUTPUT Board
1. Position OUTPUT board at rear edge of enclosure
2. Insert jack barrels through enclosure holes:
   - CV OUT (13mm position)
   - V-TRIG/S-TRIG (23mm position)
   - CUSTOM CC (33mm position)
3. Solder jack pins to board rear edge pads
4. Wire jack TIP/SLEEVE to component circuits (see individual jack sections)

### Step 4: Mount Jacks to INPUT Board
1. Stack INPUT board above OUTPUT board (10mm M3 standoffs)
2. Insert jack barrels through enclosure holes:
   - CV IN (13mm position, top row)
   - GATE IN (23mm position, top row)
   - MIDI IN (35.5mm position, top row)
   - MIDI OUT (55.5mm position, top row)
   - USB-C breakout (58.5mm position, bottom row)
3. Solder jack pins to board rear edge pads
4. Wire jack connections to component circuits

### Step 5: Connect Boards to Feather Stack
1. Wire OUTPUT board 5-pin header to Feather stack
2. Wire INPUT board 5-pin header to Feather stack
3. Wire MIDI DIN jacks to MIDI FeatherWing terminals
4. Connect USB-C extension cable from Feather to panel mount

### Step 6: Testing
1. **Visual inspection:** Check for solder bridges, cold joints
2. **Continuity test:** Verify all jack connections
3. **Power test:** Measure 5V rail, check for shorts
4. **I2C test:** Verify MCP4728 responds (I2C scan)
5. **Input test:** Apply 5V to CV IN, verify 2.62V at A3
6. **Output test:** Set DAC channels, measure jack outputs
7. **MIDI test:** Send/receive MIDI messages

---

## Troubleshooting

### No CV Output
- Check MCP4728 power (VCC = 5V)
- Verify I2C communication (I2C scan detects 0x60)
- Check output resistors (R1-R4) for cold solder joints
- Measure DAC channel outputs directly at MCP4728 pins

### CV Input Reads Wrong Voltage
- Verify voltage divider resistor values (10kΩ/10kΩ/22kΩ)
- Check divider formula: Vout = Vin × (22kΩ / 42kΩ) = Vin × 0.524
- Measure tap point voltage with multimeter
- Check BAT85 diode orientation (cathode to 3.3V)

### S-Trig Not Switching
- Verify NPN transistor orientation (2N3904 pinout)
- Check base resistor (R5 = 1kΩ)
- Measure D10 output (should be 3.3V HIGH when active)
- Check collector resistor (R6 = 100Ω)
- Verify emitter connected to GND

### MIDI Not Working
- Check DIN jack pin assignments (5 = signal, 4 = return)
- Verify MIDI FeatherWing connections (RX IN/OUT, TX IN/OUT)
- Test with known-good MIDI device
- Check MIDI activity LEDs on FeatherWing

### USB-C Not Detected
- Verify USB-C extension cable is **data capable** (not charge-only)
- Check cable connection to Feather M4
- Try different USB cable to computer
- Verify Feather M4 power LED illuminates

---

## Safety Notes

1. **Electrostatic Discharge (ESD):**
   - Use ESD wrist strap when handling boards
   - MCP4728 and Feather M4 are ESD-sensitive

2. **Soldering Safety:**
   - Use proper ventilation
   - Don't exceed 350°C tip temperature (damages components)
   - Allow components to cool before handling

3. **Power Safety:**
   - Never apply >5.5V to input jacks (exceeds protection limits)
   - Check 5V rail polarity before powering on
   - Disconnect power before making circuit changes

4. **Mechanical Safety:**
   - Jack barrels can be sharp - handle carefully
   - Use proper standoff heights to avoid board shorts
   - Ensure no loose wire strands that could short

---

**Last Updated:** 2025-11-02
**Status:** Complete Wiring Reference
**Revision:** 1.0

**Related Documents:**
- `PROTOBOARD_LAYOUT.md` - Component placement maps
- `CV_INPUT_SYSTEM.md` - Input circuit specifications
- `PIN_ALLOCATION_MATRIX.md` - Feather pin assignments
- `OUTPUT_JACK_WIRING.md` - Output jack color conventions
