# LM358N Op-Amp Wiring Guide

**Purpose:** 2× gain circuit to convert MCP4728 0-5V output to 0-10V eurorack range

**Last Updated:** 2025-10-31

**IC Used:** LM358N (dual op-amp, rail-to-rail inputs)

---

## ⚠️ CRITICAL: Why LM358N and NOT TL072

**DO NOT USE TL072 for this circuit!**

The TL072 was initially attempted but **cannot handle 0V inputs** in single-supply (ground-referenced) operation:

- **TL072 limitation:** Common-mode input range = V- + 4V minimum
- **Our circuit:** V- = 0V (ground), so TL072 requires inputs ≥ 4V
- **Problem:** At 0V input, TL072 experiences "phase inversion" and outputs ~12V (saturated high)
- **Result:** Works at 1-5V but fails at 0V - unusable for 0-10V CV output

**LM358N solves this:**
- Rail-to-rail input range (works down to 0V!)
- Single-supply operation (3V to 32V)
- Same pinout as TL072 (drop-in replacement)
- Perfect for precision DC voltage amplification

**Lesson learned:** Always verify op-amp input common-mode range for single-supply applications!

---

## LM358N Pinout (STANDARD ORIENTATION - NOTCH AT TOP)

```
View: Looking at chip from TOP, with notch at TOP CENTER

              ╭─╮                    ← Notch at top
         ┌────╯ ╰────┐
         │           │
    1 ───┤           ├─── 8
         │           │
    2 ───┤           ├─── 7
         │           │
    3 ───┤           ├─── 6
         │           │
    4 ───┤           ├─── 5
         │           │
         └───────────┘

Pin Numbers (from datasheet):
  1: OUT A (top-left)           8: V+ (12V power) (top-right)
  2: IN- A                      7: OUT B (unused)
  3: IN+ A                      6: IN- B (unused)
  4: GND (bottom-left)          5: IN+ B (unused)
```

**Note:** LM358N has identical pinout to TL072 - drop-in replacement!

---

## Circuit Schematic

```
Op-Amp A (Non-Inverting Amplifier, Gain = 2×)

MCP4728 CH-A ────────┐
 (0-5V input)        │
                     │
                   [Pin 3]
                    IN+
                     │
                 ┌───┴───┐
                 │       │
                 │LM358N │
                 │  (A)  │
                 └───┬───┘
                     │
                   [Pin 1]     R2 (100kΩ)
                    OUT  ──────┬────────── Output (0-10V)
                               │
                   [Pin 2]     │
                    IN-  ──────┤
                               │
                             R1 (100kΩ)
                               │
                              GND

[Pin 8] V+   ─────── 12V (from Powerboost)
[Pin 4] GND  ─────── GND (common ground)

Gain Formula: Vout = Vin × (1 + R2/R1) = Vin × 2
```

**Tested with actual resistor values:**
- R1: 86kΩ (measured)
- R2: 78.7kΩ (measured)
- Gain: 1 + (78.7/86) = 1.92× (close enough to 2×)

---

## Breadboard Wiring (Step-by-Step)

### Power Connections

1. **LM358N Pin 8 (V+) → 12V rail**
   - Source: Powerboost 12V output
   - Wire: Red wire to positive power rail

2. **LM358N Pin 4 (GND) → GND rail**
   - Source: Common ground
   - Wire: Black wire to ground rail

3. **MCP4728 VDD → 5V rail**
   - Source: LM7805 output (Pin 3)
   - Wire: Red wire

4. **MCP4728 GND → GND rail**
   - Wire: Black wire to common ground

### Signal Connections

5. **MCP4728 Channel A (VA pin) → LM358N Pin 3 (IN+)**
   - This is your DAC output: 0-5V
   - Wire: Orange/yellow signal wire

6. **Feedback Network (R1 and R2):**
   - R1 (100kΩ): LM358N Pin 2 (IN-) to GND
   - R2 (100kΩ): LM358N Pin 1 (OUT) to Pin 2 (IN-)
   - Creates ~2× gain

7. **LM358N Pin 1 (OUT) → Multimeter/Eurorack output**
   - This is your amplified output: 0-10V
   - Wire: Green wire to output jack

---

## Physical Layout (Breadboard)

```
Power Rails:
  Top    (+) ═══════════════════ 12V (Powerboost)
  Top    (−) ═══════════════════ GND (common ground)

LM358N Position (example):
  Row 10-13 (straddling center gap)

Connections:
  Row 10, col E: Pin 8 (V+)    → 12V rail
  Row 10, col F: Pin 1 (OUT)   → Output wire + R2
  Row 11, col E: Pin 7 (unused)
  Row 11, col F: Pin 2 (IN-)   → R1 to GND, R2 to Pin 1
  Row 12, col E: Pin 6 (unused)
  Row 12, col F: Pin 3 (IN+)   → MCP4728 CH-A
  Row 13, col E: Pin 5 (unused)
  Row 13, col F: Pin 4 (GND)   → GND rail

Resistors (~100kΩ each):
  R1: Pin 2 → GND (any row to GND rail)
  R2: Pin 1 → Pin 2 (across rows)
```

---

## Pre-Flight Checklist

Before powering on:

- [ ] LM358N oriented correctly (notch at top center)
- [ ] Pin 8 (top-right) connected to 12V
- [ ] Pin 4 (bottom-left) connected to GND
- [ ] Pin 3 (bottom-right) connected to MCP4728 CH-A
- [ ] Pin 1 (top-left) connected to R2 and output
- [ ] Pin 2 connected to both R1 (→GND) and R2 (→Pin 1)
- [ ] MCP4728 VDD at 5V
- [ ] All grounds connected (common ground)
- [ ] No shorts between power rails

---

## Power-On Sequence

1. **Verify power rails:**
   - Measure 12V rail with multimeter (should be ~12V)
   - Measure 5V rail (LM7805 output, should be ~5V)
   - Verify GND continuity

2. **Check LM358N power:**
   - Measure Pin 8 (V+): Should be ~12V
   - Measure Pin 4 (GND): Should be 0V

3. **Deploy test code:**
   ```bash
   cp tests/tl072_gain_circuit_test.py /Volumes/CIRCUITPY/code.py
   ```
   (Note: Test code still named tl072 but works with LM358N - same pinout!)

4. **Test procedure:**
   - Press Button B to cycle through test voltages
   - Measure LM358N Pin 1 (OUT) with multimeter
   - Verify ~2× gain: 0V→0V, 1V→~1.9V, 5V→~9.5V

---

## Expected Results (VERIFIED WORKING!)

| Step | DAC Input | LM358N Output | Notes |
|------|-----------|---------------|-------|
| 1 | 0.0V | 0.0V | ✅ Zero baseline (works!) |
| 2 | 0.5V | ~1.0V | 2× gain verified |
| 3 | 1.0V | ~1.9V | 1V/octave base |
| 4 | 2.0V | ~3.8V | 2 octaves |
| 5 | 3.0V | ~5.7V | 3 octaves |
| 6 | 4.0V | ~7.6V | 4 octaves |
| 7 | 5.0V | ~9.5V | Max eurorack |

**Tolerance:** ±0.2V is acceptable (resistor tolerance affects gain)

**Status:** ✅ Circuit verified working 2025-10-31

---

## Troubleshooting

### Output is 0V at all voltages

**Check:**
- LM358N Pin 8 has 12V
- LM358N Pin 4 is grounded
- MCP4728 CH-A is outputting voltage (test with multimeter)

### Output is same as input (no gain)

**Check:**
- R2 is connected between Pin 1 and Pin 2
- R1 is connected between Pin 2 and GND
- Measure resistance between Pin 1-2 (should be ~100kΩ with power OFF)

### Output is inverted or unstable

**Check:**
- Pin 3 (IN+) has signal from MCP4728
- Pin 2 (IN-) connected to feedback network (not signal)
- LM358N orientation (notch at top!)

### Output still saturates at ~12V at 0V input

**You probably have a TL072 instead of LM358N!**
- Verify chip marking says "LM358N"
- TL072 will NOT work for this circuit (see warning above)

---

## Safety Notes

⚠️ **IMPORTANT:**
- 12V can damage 5V logic if connected incorrectly
- Always verify connections before applying power
- Keep 12V circuit isolated from M4 3.3V pins
- MCP4728 runs at 5V, M4 I2C is 3.3V (voltage level compatible)

---

## Next Steps After Verification

Once you verify 0-10V output:

1. Connect to eurorack VCO oscillator input
2. Test chromatic scale (should track 1V/octave)
3. Verify audio quality (no noise or distortion)
4. Integrate into arpeggiator firmware
5. Design PCB with LM358N for production

---

## Bill of Materials (BOM)

| Part | Value | Notes |
|------|-------|-------|
| U1 | LM358N | Dual op-amp, DIP-8 package |
| R1 | 100kΩ | 1/4W, ±5% tolerance OK |
| R2 | 100kΩ | 1/4W, ±5% tolerance OK |

**Cost:** ~$0.80 total (LM358N ~$0.50, resistors ~$0.15 each)

---

**Circuit tested and verified working 2025-10-31!**
