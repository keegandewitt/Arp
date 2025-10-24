# CV Output Op-Amp Circuit - 2× Gain Stage

**Purpose:** Amplify MCP4728 DAC output from 0-5V to 0-10V for proper 1V/octave CV
**Date:** 2025-10-24
**Status:** Design complete, ready for breadboard testing

---

## Overview

The MCP4728 outputs 0-5V, but Eurorack CV standard requires 0-10V for a full 10-octave range at 1V/octave.

**Solution:** Non-inverting op-amp amplifier with 2× gain.

```
MCP4728 (0-5V) → Op-Amp (2× gain) → CV Output (0-10V)
```

---

## Circuit Design

### Non-Inverting Amplifier (2× Gain)

```
                    R2 (100kΩ)
                    ┌────────┐
                    │        │
    MCP4728 ────────┤+       │
    VA (0-5V)       │   OP   ├───────→ CV OUT (0-10V)
                    │        │
         ┌──────────┤-       │
         │          └────────┘
         │              │
         │          R1 (100kΩ)
         │              │
         └──────────────┴─────── GND
```

### Gain Formula
```
Gain = 1 + (R2 / R1)
     = 1 + (100kΩ / 100kΩ)
     = 1 + 1
     = 2×
```

**Result:**
- 0V input → 0V output
- 2.5V input → 5V output
- 5V input → 10V output

---

## Component Selection

### Op-Amp Chip Options

**Recommended: TL072 or TL074**
- **TL072:** Dual op-amp (2 channels per chip)
- **TL074:** Quad op-amp (4 channels per chip)
- Low noise, rail-to-rail output
- Single supply operation: 9V to 36V
- Perfect for Eurorack CV applications
- **Very common and cheap** (~$1-2)

**Alternative: MCP6002** (if you have it)
- Dual op-amp
- Lower voltage: 2.7V to 6V (won't work for 10V output!)
- ❌ **NOT suitable** - can't output 10V

**Alternative: LM358**
- Dual op-amp
- Single supply: 3V to 32V
- Slightly noisier than TL072
- ✅ Works, but TL072 is better

**What op-amps do you have?**

### Resistors
- **2× 100kΩ resistors** per channel
- 1/4W metal film resistors
- ±1% tolerance (precision) or ±5% (standard)

**Why 100kΩ?**
- High impedance (low current draw)
- Low noise
- Standard value

### Power Supply
Op-amp needs **at least 12V supply** to output 10V:
- Use **12V from Powerboost** (configure for 12V output)
- Or separate 12V power supply
- Requires reconfiguring Powerboost: A=1, B=1 → 12V

---

## Complete Circuit (1 Channel)

```
                    +12V (from Powerboost)
                      │
                      ├─────────┐
                      │         │
               0.1µF  │         │ 0.1µF
    Bypass ──┤├──────┤         ├──────┤├─── Bypass
    Caps     0.1µF    │         │      0.1µF
                      │         │
    MCP4728 VA ───────┤+        │
    (0-5V)            │   TL072 ├──────→ CV OUT
                      │    #1   │       (0-10V)
         ┌────────────┤-        │
         │            └─────────┘
         │                │
         │            100kΩ R2
         │                │
         └────────────────┤
                          │
                      100kΩ R1
                          │
                         GND
```

### Power Supply Decoupling
- **0.1µF ceramic capacitors** on +12V and GND near op-amp
- Reduces noise and stabilizes power
- Place as close to op-amp pins as possible

---

## Full 4-Channel Build

For all 4 MCP4728 channels, you need:

### Option 1: Two TL072 Chips (2 channels each)
```
TL072 #1:
  - Channel A (VA) → CV Pitch
  - Channel B (VB) → CV Velocity

TL072 #2:
  - Channel C (VC) → CV Modulation 1
  - Channel D (VD) → CV Modulation 2
```

### Option 2: One TL074 Chip (4 channels)
```
TL074:
  - Op-amp #1: Channel A (VA) → CV Pitch
  - Op-amp #2: Channel B (VB) → CV Velocity
  - Op-amp #3: Channel C (VC) → CV Mod 1
  - Op-amp #4: Channel D (VD) → CV Mod 2
```

**TL074 is cleaner** - single chip for all 4 channels!

---

## Bill of Materials

### For 4 Channels (Pitch + 3× Modulation)

| Qty | Part | Description | Est. Cost |
|-----|------|-------------|-----------|
| 1 | TL074 | Quad op-amp (or 2× TL072) | $1-2 |
| 8 | 100kΩ resistor | 1/4W metal film, ±1% | $0.50 |
| 4 | 0.1µF capacitor | Ceramic, power decoupling | $0.40 |
| 4 | 3.5mm jack | Eurorack CV output jacks | $4-8 |
| - | Breadboard | For testing | - |
| - | Jumper wires | Connections | - |

**Total:** ~$6-11 in parts

---

## Power Configuration

### Powerboost Reconfiguration

Currently: **5V output** (A=0, B=0)
Need: **12V output** (A=1, B=1)

**Steps:**
1. Locate solder pads A and B on Powerboost
2. Bridge pad A (solder connection)
3. Bridge pad B (solder connection)
4. Verify with multimeter: Output should be ~12V

**Voltage Budget:**
- MCP4728 VDD: Use separate 5V regulator from 12V
- Op-amps: Powered from 12V
- M4 + OLED: Powered from M4's onboard regulation

---

## Breadboard Layout

```
MCP4728 VA (0-5V)
    │
    └───────┐
            │
    [100kΩ R2]───[TL074 Pin 3 (+)]
            │
            └───[TL074 Pin 2 (-)]───[100kΩ R1]───GND
                           │
                           └────────┐
                                    │
                        [TL074 Pin 1 (OUT)]───→ CV Jack (0-10V)

Power:
  TL074 Pin 4:  +12V (via 0.1µF cap to GND)
  TL074 Pin 11: GND
```

### Pin Reference (TL074 DIP-14)
```
        ┌───────┐
 OUT1 ──┤ 1  14 ├── OUT4
  -1  ──┤ 2  13 ├── -4
  +1  ──┤ 3  12 ├── +4
 VCC+ ──┤ 4  11 ├── GND
  +2  ──┤ 5  10 ├── +3
  -2  ──┤ 6   9 ├── -3
 OUT2 ──┤ 7   8 ├── OUT3
        └───────┘
```

---

## Testing Procedure

### 1. Power Test
- Apply 12V to op-amp
- Measure voltage rails
- Should read ~12V between VCC and GND

### 2. DC Offset Test
- No input connected (or 0V input)
- Measure CV output
- Should read 0V (or very close)

### 3. Gain Test
Use MCP4728 test code to output known voltages:

| MCP4728 Input | Expected Output | Test Point |
|---------------|-----------------|------------|
| 0V | 0V | Zero |
| 1V | 2V | - |
| 2.5V | 5V | Mid-scale |
| 5V | 10V | Full scale |

**Tolerance:** ±0.1V is acceptable

### 4. Stability Test
- Leave circuit powered for 10 minutes
- Check for drift
- Should remain stable within ±0.05V

---

## Calibration (Optional)

For precision CV, you can add a **trimmer potentiometer**:

```
         R2 (100kΩ)
            │
            ├───[10kΩ Trim Pot]───┐
            │                     │
         [Op-Amp]                GND
```

Adjust trim pot to set exact 2× gain if needed.

---

## Gate Output (No Amplification Needed)

**Gate/Trigger** output doesn't need amplification:
- Eurorack gates: 0V (low) or 5V+ (high)
- MCP4728 Channel B outputs 0-5V
- **Use directly** - no op-amp needed!

```
MCP4728 VB (0-5V) ───→ Gate Jack (0-5V, works fine!)
```

Most Eurorack modules trigger at 2.5V, so 5V is plenty.

---

## Next Steps

1. ✅ Design complete
2. 📋 Verify you have TL074 or TL072 op-amps
3. 📋 Gather resistors and capacitors
4. 📋 Breadboard one channel
5. 📋 Test with multimeter
6. 📋 Build remaining 3 channels
7. 📋 Update CV driver code for 10V range

---

## MIDI → CV Conversion (Updated for 10V)

With 0-10V output, we can do proper 1V/octave over 10 octaves:

```python
# Standard 1V/octave conversion
# C0 (MIDI 12) = 0V
# C1 (MIDI 24) = 1V
# C2 (MIDI 36) = 2V
# ...
# C10 (MIDI 132) = 10V

def midi_to_cv_voltage(midi_note):
    """Convert MIDI note to CV voltage (1V/octave)"""
    # Reference: C0 (MIDI 12) = 0V
    cv_voltage = (midi_note - 12) / 12.0

    # Clamp to 0-10V range
    if cv_voltage < 0:
        cv_voltage = 0
    elif cv_voltage > 10:
        cv_voltage = 10

    return cv_voltage

# Convert to MCP4728 DAC value (0-4095 for 0-5V)
# Op-amp will double it to 0-10V
def cv_voltage_to_dac(cv_voltage):
    """Convert CV voltage to DAC value (op-amp doubles output)"""
    # DAC outputs 0-5V, op-amp doubles to 0-10V
    # So we need half the target voltage from DAC
    dac_voltage = cv_voltage / 2.0

    # Convert voltage to 12-bit DAC value
    dac_value = int((dac_voltage / 5.0) * 4095)

    # Clamp to valid range
    if dac_value < 0:
        dac_value = 0
    elif dac_value > 4095:
        dac_value = 4095

    return dac_value
```

**Example:**
- MIDI 60 (Middle C) = 4V CV
- DAC needs to output 2V (4V / 2)
- DAC value = 1638 (2V / 5V × 4095)
- Op-amp doubles to 4V

Perfect! 🎯

---

**Document Version:** 1.0
**Last Updated:** 2025-10-24
**Status:** Ready for breadboard testing
