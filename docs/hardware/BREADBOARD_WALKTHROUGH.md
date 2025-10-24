# TL072 Op-Amp Breadboard Walkthrough

**Date:** 2025-10-24
**Purpose:** Build a 2× gain amplifier to convert 0-5V to 0-10V for Eurorack CV pitch control
**Skill Level:** Beginner-friendly with component explanations

---

## What You'll Need

| Qty | Part | Notes |
|-----|------|-------|
| 1 | TL072 op-amp chip | 8-pin DIP package |
| 2 | 100kΩ resistors | Brown-Black-Yellow bands |
| 3 | 100nF (0.1µF) ceramic capacitors | Small disc or rectangular |
| 1 | LM7805 voltage regulator | TO-220 package (3 pins) |
| 1 | Breadboard | Standard size |
| - | Jumper wires | Various colors/lengths |
| 1 | Feather M4 | Your microcontroller |
| 1 | MCP4728 DAC | Already set up from previous steps |
| 1 | Powerboost | Needs reconfiguration to 12V |
| 1 | Multimeter | For testing voltages |

---

## Before You Start: Reconfigure Powerboost to 12V

**Why:** The TL072 needs 12V power to output 10V. Currently your Powerboost outputs 5V.

**How to change it:**

1. **Locate solder pads A and B** on the Powerboost board
2. **Bridge pad A** with a small blob of solder (connecting the two sides)
3. **Bridge pad B** with solder (same thing)
4. **Test:** Power on and measure VOUT with multimeter - should read ~12V (not 5V)

**Settings:**
- A=0, B=0 → 5V (old setting)
- A=1, B=1 → 12V (new setting) ✅

---

## Power Architecture Overview

```
LiPo Battery (3.7V)
    ↓
Feather M4 BAT pin
    ↓
Powerboost (12V output)
    ├──→ TL072 Op-Amp (needs 12V to output 10V)
    │
    └──→ LM7805 Regulator (12V → 5V)
         └──→ MCP4728 VDD (max 5.5V rating)
```

**Important:**
- TL072 requires 12V to output full 0-10V range
- MCP4728 requires 5V (max 5.5V rating)
- LM7805 converts 12V down to 5V for the MCP4728
- **Note:** Feather M4 CAN does NOT have a 5V pin on headers, so LM7805 is required

---

## Step 1: Insert the TL072 into the Breadboard

### What you're doing
Placing the op-amp chip on the breadboard so we can connect wires to its pins.

### What is an op-amp?
An **operational amplifier (op-amp)** is a chip that amplifies voltage. Think of it like a volume knob for electrical signals - we're using it to double our voltage from 5V to 10V.

### How to do it

1. **Find the TL072 chip** - it's a small black rectangle with 8 metal legs (pins)
2. **Look for the notch or dot** on one end - this marks Pin 1
3. **Orient the chip** so the notch faces left (or up - your choice, just remember)
4. **Straddle the center gap** - place the chip so its legs go into holes on BOTH sides of the breadboard's center divider

### Pin numbering reference
```
     ← Notch points this way
        ┌───────┐
   Pin 1│●      │Pin 8  (VCC+ power)
   Pin 2│       │Pin 7  (not used)
   Pin 3│       │Pin 6  (not used)
   Pin 4│  TL072│Pin 5  (not used)
        └───────┘
          (GND power)
```

**Pins we'll use:**
- Pin 1: Output (amplified signal)
- Pin 2: Inverting input (-)
- Pin 3: Non-inverting input (+)
- Pin 4: Ground (GND)
- Pin 8: Positive power (VCC+)

---

## Step 2: Connect Power to Pin 8 (VCC+)

### What you're doing
Giving the op-amp its positive 12V power supply.

### What is VCC+?
**VCC+** (or V+) is the positive voltage rail that powers the chip. The op-amp needs this to function. Think of it like plugging in an appliance.

### How to do it

1. **Take a jumper wire** (red is conventional for positive power)
2. **Connect one end to the +12V rail** on your breadboard (the red line running along the side)
3. **Connect the other end to Pin 8** (top right pin of the TL072)

**Don't power on yet!** Wait until all connections are complete.

---

## Step 3: Connect Ground to Pin 4 (GND)

### What you're doing
Completing the power circuit by connecting ground.

### What is ground (GND)?
**Ground** is the reference point for all voltages - it's 0V. Every circuit needs a ground connection to complete the electrical circuit. Think of it like the return path for electricity.

### How to do it

1. **Take a jumper wire** (black is conventional for ground)
2. **Connect one end to the GND rail** on your breadboard (the blue/black line)
3. **Connect the other end to Pin 4** (bottom left pin of the TL072)

---

## Step 4: Add Bypass Capacitor for TL072 Power

### What you're doing
Adding a capacitor to filter out electrical noise from the power supply.

### What is a capacitor?
A **capacitor** stores and releases electrical energy very quickly. Think of it like a tiny rechargeable battery that smooths out bumps in your power supply.

**Ceramic capacitors** (what we're using) are non-polarized - either leg can go to either side. They look like small discs or rectangles.

### Why do we need it?
Op-amps are sensitive to noise on their power supply. This capacitor "absorbs" high-frequency noise and keeps the power clean, preventing unwanted sounds or instability.

### How to do it

1. **Take your 100nF ceramic capacitor** (small disc or rectangle, marked "104" or "100nF")
2. **Plug one leg into the +12V rail** (red line)
3. **Plug the other leg into the GND rail** (blue/black line)
4. **Place it as close to the TL072 as possible** on the breadboard

**Note:** Ceramic caps have no polarity - either leg can go to either rail.

---

## Step 5: Add the First Resistor (Feedback Resistor)

### What you're doing
Connecting the output back to the input to control the gain (amplification amount).

### What is a resistor?
A **resistor** resists (limits) the flow of electrical current. Think of it like a narrow pipe that restricts water flow.

### What does this resistor do?
This **feedback resistor** tells the op-amp how much to amplify. By connecting output to input through this resistor, we're creating a feedback loop that controls the gain.

### How to do it

1. **Take one 100kΩ resistor** (color bands: Brown-Black-Yellow-Gold)
2. **Connect one leg to Pin 2** (second pin from top, left side)
3. **Connect the other leg to Pin 1** (top pin, left side)

**Visual:**
```
Pin 1 ●───[100kΩ]───● Pin 2
(Out)              (In-)
```

**Note:** Resistors have no polarity - either direction works.

---

## Step 6: Add the Second Resistor (Ground Resistor)

### What you're doing
Completing the gain-setting circuit by connecting the input to ground through another resistor.

### What does this resistor do?
This **ground resistor** works with the feedback resistor to set the exact gain. The ratio of these two resistors determines the amplification:
- Both 100kΩ → Gain = 2× (doubles the voltage)

### How to do it

1. **Take your second 100kΩ resistor**
2. **Connect one leg to Pin 2** (yes, same pin - it now has TWO resistors)
3. **Connect the other leg to the GND rail** (blue/black line)

**Visual:**
```
         To Pin 1 (Out)
              │
         [100kΩ R1]
              │
Pin 2 ────────┤
(In-)         │
         [100kΩ R2]
              │
             GND
```

**Pin 2 now has TWO resistors:**
- One going UP to Pin 1 (output)
- One going DOWN to GND

This creates a "voltage divider" that sets the gain to 2×.

---

## Step 7: Add LM7805 Voltage Regulator Circuit

### What you're doing
Creating a 5V power supply for the MCP4728 from the Powerboost's 12V output.

### What is a voltage regulator?
An **LM7805** is a chip that converts a higher voltage (12V) down to a fixed 5V output. Think of it like a step-down transformer for DC power.

### How to do it

**LM7805 Pinout (looking at front with metal tab up):**
```
  Metal tab (heatsink)
       │
   ┌───┴───┐
   │       │
   1   2   3
   │   │   │
  IN  GND OUT
```

1. **Insert LM7805** into breadboard
2. **Pin 1 (IN):** Connect to Powerboost +12V rail
3. **Pin 2 (GND):** Connect to GND rail
4. **Pin 3 (OUT):** This is your 5V output - connect to MCP4728 VDD

### Add bypass capacitors

4. **Input cap:** Place 100nF ceramic cap between Pin 1 (12V) and Pin 2 (GND)
5. **Output cap:** Place second 100nF ceramic cap between Pin 3 (5V) and GND rail
6. **Place both caps close to the LM7805**

**Why two caps:** Input cap smooths the 12V input, output cap smooths the 5V output.

**Circuit:**
```
Powerboost 12V ──┬──[100nF]──┬─→ GND
                 │           │
              LM7805 Pin 1   │
              LM7805 Pin 2 ──┘
              LM7805 Pin 3 ──┬──[100nF]──┬─→ GND
                             │           │
                             └───────────┴─→ MCP4728 VDD (5V)
```

---

## Step 8: Connect Input from MCP4728

### What you're doing
Bringing the 0-5V signal from the DAC into the op-amp to be amplified.

### What is this connection?
This is your **signal input** - the voltage you want to amplify. The MCP4728 outputs 0-5V on Channel A (VA pin), and we're feeding that into the op-amp's "+" input.

### How to do it

1. **Take a jumper wire**
2. **Connect MCP4728 Channel A (VA pin)** to **TL072 Pin 3** (third pin from top, left side)

**Visual:**
```
MCP4728 VA (0-5V) ────────→ TL072 Pin 3 (+IN)
```

### What happens
- When MCP outputs 0V → Op-amp receives 0V → Will output 0V
- When MCP outputs 2.5V → Op-amp receives 2.5V → Will output 5V
- When MCP outputs 5V → Op-amp receives 5V → Will output 10V

**The magic of 2× gain!**

---

## Step 9: Connect Output and Test Point

### What you're doing
Creating a place to measure the amplified output voltage.

### How to do it

1. **Pin 1** (top left pin) is your output - this is where the amplified signal comes out
2. **Use a jumper wire** from Pin 1 to an empty row on your breadboard
3. **This is your test point** - you'll measure voltage here with your multimeter

**Later:** This will connect to your CV output jack for connecting to your modular synth.

---

## Step 10: Double-Check All Connections

**Before powering on, verify:**

### Power connections
- [ ] Pin 8 → +12V rail (from Powerboost)
- [ ] Pin 4 → GND rail
- [ ] 100nF cap between +12V and GND (near TL072)
- [ ] LM7805 Pin 1 → +12V rail
- [ ] LM7805 Pin 2 → GND rail
- [ ] LM7805 Pin 3 → MCP4728 VDD (5V output)
- [ ] 100nF cap between LM7805 Pin 1 and GND (input side)
- [ ] 100nF cap between LM7805 Pin 3 and GND (output side)
- [ ] Common ground: M4, MCP4728, TL072, LM7805, Powerboost all share GND

### Signal connections
- [ ] MCP4728 VA → TL072 Pin 3
- [ ] 100kΩ resistor between Pin 2 and Pin 1
- [ ] 100kΩ resistor between Pin 2 and GND
- [ ] Test point wire from Pin 1

**Visual summary:**
```
                    +12V (Powerboost)
                      │
                      ├─────────────────────┐
                      │                     │
               100nF  │              LM7805 Regulator
        ┌────────┤├───┤              ┌──────┴──────┐
        │              │              │ IN  GND OUT │
        │       ┌──────┴──────┐       └──┬───┬───┬──┘
        │       │  8   TL072  │          │   │   │
        │       │             │      100nF  GND 100nF
MCP VA ─┼───────┤3 (+)        │          │       │
(0-5V)  │       │             │          GND      └──→ MCP4728 VDD (5V)
        │   ┌───┤2 (-)      1 ├───→ Test Point (0-10V)
        │   │   │             │
        │   │   │  4          │
        │   │   └──────┬──────┘
        │   │          │
        │   │     [100kΩ R2]
        │   │          │
        │   └──────────┴───────┐
        │                      │
        │                  [100kΩ R1]
        │                      │
       GND ────────────────────┴────── GND (Common to all)
```

---

## Step 11: Power On and Test

### Test 1: Check Power Rails

1. **Power on** your Feather M4 (this powers the MCP4728)
2. **Power on** the Powerboost (this powers the TL072)
3. **Set multimeter to DC voltage mode**
4. **Measure TL072 power:**
   - Black probe → Pin 4 (GND)
   - Red probe → Pin 8 (VCC+)
   - **Expected: ~12V**

5. **Measure MCP4728 power:**
   - Black probe → GND
   - Red probe → VDD
   - **Expected: ~5V**

**If wrong:** Double-check Powerboost jumpers and connections.

---

### Test 2: Zero Offset Test

**What you're testing:** With no input, output should be 0V.

1. **Set MCP4728 Channel A to 0V** (run test code with `dac.channel_a.value = 0`)
2. **Measure output:**
   - Black probe → GND
   - Red probe → Pin 1 (output test point)
   - **Expected: 0V (or very close, ±0.05V)**

**If wrong:** Check resistor connections to Pin 2.

---

### Test 3: Gain Verification Test

**What you're testing:** 2× amplification across the full range.

**Use your MCP4728 test code to set different voltages:**

| MCP4728 Value | MCP Voltage | Expected Output | What to Measure |
|---------------|-------------|-----------------|-----------------|
| 0 | 0V | 0V | Zero point |
| 1024 | 1.25V | 2.5V | Quarter scale |
| 2048 | 2.5V | 5V | Mid scale |
| 3072 | 3.75V | 7.5V | Three-quarter |
| 4095 | 5V | 10V | Full scale |

**How to test:**
1. Run your MCP4728 test script (from previous session)
2. For each test value, measure voltage at Pin 1 with multimeter
3. Compare to expected output

**Tolerance:** ±0.2V is acceptable for a breadboard circuit.

**Example test code:**
```python
import board
import adafruit_mcp4728

i2c = board.I2C()
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)

# Configure for 5V reference
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
dac.channel_a.gain = 1

# Test different voltages
test_values = [0, 1024, 2048, 3072, 4095]

for value in test_values:
    dac.channel_a.value = value
    voltage = (value / 4095.0) * 5.0
    print(f"Set DAC to {value} ({voltage:.2f}V) - measure output now")
    input("Press Enter for next value...")
```

---

### Test 4: Stability Test

**What you're testing:** Output voltage stays stable over time.

1. **Set MCP4728 to mid-scale:** `dac.channel_a.value = 2048` (should output 5V)
2. **Measure output** with multimeter
3. **Wait 5 minutes** (leave it powered on)
4. **Measure again** - should be within ±0.1V of first reading

**If drifting:** Check bypass capacitor placement (should be close to chip).

---

## Troubleshooting

### Problem: Output is 0V (no signal)

**Possible causes:**
1. No power to TL072
   - **Check:** Measure Pin 8 to Pin 4, should be ~12V
   - **Fix:** Verify Powerboost is on and configured to 12V

2. Missing feedback resistor
   - **Check:** Is there a 100kΩ resistor between Pin 2 and Pin 1?
   - **Fix:** Add or reseat the resistor

3. MCP4728 not outputting voltage
   - **Check:** Measure VA pin directly with multimeter
   - **Fix:** Run MCP4728 test code, verify it's powered at 5V

---

### Problem: Output stuck at 12V (rail voltage)

**Possible causes:**
1. Missing ground resistor
   - **Check:** Is there a 100kΩ resistor between Pin 2 and GND?
   - **Fix:** Add the resistor

2. Pin 2 shorted to +12V
   - **Check:** Visually inspect breadboard for misplaced wires
   - **Fix:** Remove any connections from Pin 2 to +12V

---

### Problem: Output is close but gain is wrong (not exactly 2×)

**Possible causes:**
1. Resistor values not exactly 100kΩ
   - **Check:** Measure resistors with multimeter (should be 95-105kΩ for 5% tolerance)
   - **Fix:** Use closer-matched resistors if needed (1% tolerance)

2. Breadboard contact issues
   - **Check:** Wiggle wires - does voltage change?
   - **Fix:** Move to fresh breadboard holes

---

### Problem: Output is noisy or unstable

**Possible causes:**
1. Bypass capacitor too far from chip
   - **Check:** Is 100nF cap within a few holes of the TL072?
   - **Fix:** Move it closer

2. Poor breadboard connections
   - **Check:** Reseat all wires firmly
   - **Fix:** Try different breadboard holes

3. Ground loop or missing common ground
   - **Check:** Verify all GND connections share the same rail
   - **Fix:** Ensure M4, MCP4728, TL072, Powerboost all connect to same GND point

---

## Success Criteria

**Your circuit is working correctly if:**

✅ TL072 powered at 12V (Pin 8 to Pin 4)
✅ MCP4728 powered at 5V (VDD to GND)
✅ Output is 0V when input is 0V
✅ Output is 5V when input is 2.5V
✅ Output is 10V when input is 5V
✅ Voltage stays stable over 5 minutes (±0.1V)

**Congratulations! You now have a working 0-10V CV output for 1V/octave control!**

---

## What's Next?

1. ✅ Breadboard circuit built and tested
2. 📋 Create Python CV driver module for MIDI → CV conversion
3. 📋 Implement 1V/octave scaling (MIDI note → voltage)
4. 📋 Integrate CV/Gate into arpeggiator code
5. 📋 Test with actual modular synthesizer
6. 📋 (Optional) Add LM7805 regulator to replace M4 USB power
7. 📋 Design PCB for permanent installation

---

## Component Education: Quick Reference

### Resistors
- **What they do:** Limit current flow (like a narrow pipe for water)
- **How to read:** Color bands (Brown-Black-Yellow = 100kΩ)
- **No polarity:** Can be inserted either direction

### Capacitors (Ceramic)
- **What they do:** Store and release energy quickly, filter noise
- **Markings:** "104" = 100nF, "103" = 10nF
- **No polarity:** Either leg to either side

### Capacitors (Electrolytic)
- **Different type:** Larger, cylindrical, polarized
- **HAS POLARITY:** Negative leg marked with stripe, must go to GND
- **Not used in this circuit**

### Op-Amps
- **What they do:** Amplify voltage signals
- **Two inputs:** (+) non-inverting, (-) inverting
- **Gain controlled by:** External resistors (feedback circuit)

### Voltage Regulators (LM7805)
- **What they do:** Convert higher voltage to fixed lower voltage
- **Example:** 12V → 5V
- **Three pins:** Input, Ground, Output

---

**Document Version:** 2.0
**Last Updated:** 2025-10-24
**Status:** Complete beginner-friendly walkthrough
