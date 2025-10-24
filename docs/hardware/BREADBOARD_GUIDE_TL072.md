# TL072 Op-Amp Breadboard Assembly Guide

**Date:** 2025-10-24
**Purpose:** Build 2× gain amplifier for CV pitch (0-5V → 0-10V)
**Status:** Ready to build

---

## Bill of Materials

| Qty | Part | Value | Notes |
|-----|------|-------|-------|
| 1 | TL072 | Dual op-amp (DIP-8) | Using channel 1 only |
| 2 | Resistor | 100kΩ | 1/4W, ±5% or ±1% |
| 1 | Capacitor | 0.1µF (100nF) ceramic | Non-polarized, bypass cap |
| 1 | Breadboard | Standard | - |
| - | Jumper wires | - | Various lengths |
| 1 | Powerboost | 12V output | Reconfigure A=1, B=1 |

**Optional:**
- 1× 1kΩ resistor (output protection - can add later)
- Multimeter for voltage testing

---

## TL072 Pinout (DIP-8)

```
        TL072
      ┌───────┐
OUT1 ─┤1    8├─ VCC+ (+12V)
 -1  ─┤2    7├─ OUT2  (not used)
 +1  ─┤3    6├─ -2    (not used)
GND  ─┤4    5├─ +2    (not used)
      └───────┘
```

**Channel 1 (we're using this):**
- Pin 1: Output
- Pin 2: Inverting input (-)
- Pin 3: Non-inverting input (+)

**Power:**
- Pin 8: VCC+ (connect to +12V)
- Pin 4: GND (connect to ground)

---

## Step 1: Power the TL072

### What You're Doing
Powering the op-amp with 12V from Powerboost

### Connections
```
Powerboost +12V ──────┬──────→ TL072 Pin 8 (VCC+)
                      │
                  [0.1µF Cap]
                      │
Powerboost GND ───────┴──────→ TL072 Pin 4 (GND)
```

### Breadboard Steps
1. **Insert TL072** into breadboard (straddle the center gap)
2. **Connect Pin 8** to +12V rail with jumper wire
3. **Connect Pin 4** to GND rail with jumper wire
4. **Add bypass cap:** Place 100nF (0.1µF) ceramic cap between +12V and GND rails **as close to the chip as possible**
5. **Verify power:** Use multimeter to check ~12V between Pin 8 and Pin 4

⚠️ **IMPORTANT:** Do NOT power on until all connections are complete!

---

## Step 2: Build the Gain Circuit

### What You're Doing
Creating 2× gain with two 100kΩ resistors

### Gain Formula
```
Gain = 1 + (R2 / R1) = 1 + (100k / 100k) = 2×
```

### Circuit Topology
```
MCP4728 VA (0-5V) ──────────→ TL072 Pin 3 (+IN)

         ┌──────────────────────────┤ TL072 Pin 2 (-IN)
         │                          │
         │                      [100kΩ R2]
         │                          │
         └──────────────────────────┤ TL072 Pin 1 (OUT)
                                    │
                                [100kΩ R1]
                                    │
                                   GND
```

### Breadboard Steps
1. **R1 (Feedback):** Connect 100kΩ resistor between Pin 2 and Pin 1
2. **R2 (Ground):** Connect 100kΩ resistor between Pin 2 and GND rail
3. **Verify:** Pin 2 should have two resistors connected (one to Pin 1, one to GND)

---

## Step 3: Connect Input and Output

### Input Connection (from MCP4728)
```
MCP4728 Channel A (VA) ───→ TL072 Pin 3 (+IN)
MCP4728 GND ───────────────→ Common GND rail
```

### Output Connection (to CV jack)
```
TL072 Pin 1 (OUT) ───→ CV Output Jack (0-10V)
```

**Optional:** Add 1kΩ resistor in series with output for short-circuit protection

---

## Complete Circuit Diagram

```
                    +12V (Powerboost)
                      │
               0.1µF  │
        ┌────────┤├───┤
        │              │
        │       ┌──────┴──────┐
        │       │  8   TL072  │
        │       │             │
MCP VA ─┼───────┤3 (+)        │
(0-5V)  │       │             │
        │   ┌───┤2 (-)      1 ├───→ CV OUT
        │   │   │             │     (0-10V)
        │   │   │  4          │
        │   │   └──────┬──────┘
        │   │          │
        │   │     [100kΩ R2]
        │   │          │
        │   └──────────┴───────┐
        │                      │
        │                  [100kΩ R1]
        │                      │
       GND ────────────────────┴────── GND
```

---

## Step 4: Testing Procedure

### Before Power-On Checklist
- [ ] TL072 Pin 8 connected to +12V
- [ ] TL072 Pin 4 connected to GND
- [ ] 0.1µF bypass cap between +12V and GND (near chip)
- [ ] 100kΩ R1 between Pin 2 and Pin 1
- [ ] 100kΩ R2 between Pin 2 and GND
- [ ] MCP4728 Channel A ready to connect to Pin 3
- [ ] Common ground between MCP4728, Powerboost, and TL072

### Test 1: Power Rails
1. **Power on** Powerboost (12V mode)
2. **Measure** voltage between TL072 Pin 8 and Pin 4
3. **Expected:** ~12V

### Test 2: Zero Offset
1. **Connect** MCP4728 Channel A to TL072 Pin 3
2. **Set** MCP4728 Channel A to 0V (DAC value = 0)
3. **Measure** voltage at TL072 Pin 1 (output)
4. **Expected:** 0V (or very close, ±0.05V)

### Test 3: Gain Verification
Use MCP4728 test code to sweep voltages:

| MCP Input | Expected Output | Test Point |
|-----------|-----------------|------------|
| 0V | 0V | Zero |
| 1V | 2V | Low scale |
| 2.5V | 5V | Mid scale |
| 5V | 10V | Full scale |

**Tolerance:** ±0.2V is acceptable for breadboard

### Test 4: Stability
1. Leave powered for 5 minutes
2. Check output voltage drift
3. **Expected:** ±0.1V max drift

---

## Troubleshooting

### Output is 0V (no signal)
- Check power rails (Pin 8 = +12V, Pin 4 = GND)
- Verify MCP4728 is outputting voltage (measure VA pin directly)
- Check R1 resistor connection (Pin 2 to Pin 1)

### Output is stuck at 12V (rail)
- Check R2 resistor connection (Pin 2 to GND)
- Verify Pin 2 is NOT shorted to +12V

### Output is correct but noisy
- Move bypass cap closer to op-amp pins
- Add second 0.1µF cap on opposite power rail
- Check for loose breadboard connections

### Gain is incorrect (not 2×)
- Measure resistance of both resistors (should be ~100kΩ)
- Verify R1 is between Pin 2 and Pin 1
- Verify R2 is between Pin 2 and GND

---

## Next Steps After Breadboard Success

1. ✅ Breadboard circuit built
2. ✅ Voltage tests passed (0V → 10V)
3. 📋 Create CV driver Python module
4. 📋 Implement MIDI → CV conversion (1V/octave)
5. 📋 Integrate into arpeggiator code
6. 📋 Test with modular synth

---

## Powerboost Reconfiguration (12V Output)

**IMPORTANT:** Powerboost must be set to 12V output for op-amp to reach 10V

### Current Setting
- **A=0, B=0** → 5V output (current)

### Required Setting
- **A=1, B=1** → 12V output (needed for 10V CV)

### How to Change
1. Locate solder pads A and B on Powerboost
2. Bridge pad A with solder
3. Bridge pad B with solder
4. Verify output voltage with multimeter (~12V)

**Note:** After changing to 12V, MCP4728 VDD must use a separate 5V regulator (or powered from M4's 5V pin if available)

---

## Safety Notes

- ⚠️ **Do not short** +12V to GND (will damage Powerboost)
- ⚠️ **Do not exceed 12V** on TL072 VCC (max rating is typically 36V, but keep it safe)
- ⚠️ **Do not connect** 12V to MCP4728 VDD (max 5.5V!)
- ✅ **Always use common ground** between all circuits

---

**Document Version:** 1.0
**Last Updated:** 2025-10-24
**Status:** Ready for breadboard assembly
