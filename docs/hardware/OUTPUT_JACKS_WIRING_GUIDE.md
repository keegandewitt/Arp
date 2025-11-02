# Output Jacks Wiring & Testing Guide

**Date:** 2025-11-02
**Purpose:** Step-by-step guide for wiring and testing all CV/Gate/Trigger outputs
**Hardware:** Feather M4 + MCP4728 DAC + Output jacks

---

## Overview

**Output Configuration:**

| Output | Hardware Source | Voltage Range | Jack Type | Purpose |
|--------|----------------|---------------|-----------|---------|
| **CV Pitch** | MCP4728 Channel A | 0-5V (1V/octave) | 1/8" TS mono | Pitch control |
| **V-Trig Gate** | MCP4728 Channel C | 0V/5V | 1/8" TS mono | Modern gate/trigger |
| **S-Trig** | GPIO D10 + NPN | Open/Short to GND | 1/4" TS mono | Vintage trigger |
| **Custom CC** | MCP4728 Channel D | 0-5V | 1/8" TS mono | Modulation/CC |

**Optional Enhancement:**
- **CV Pitch (0-10V)** - Add LM358N op-amp for extended range (eurorack)

---

## Tools & Materials Needed

### Required
- [ ] **Output Jacks:**
  - 3× 1/8" (3.5mm) TS mono jacks (CV Pitch, V-Trig, Custom CC)
  - 1× 1/4" TS mono jack (S-Trig - vintage compatibility)
- [ ] **Hookup Wire:**
  - **RED** wire (signal/tip - hot)
  - **WHITE** wire (ground/sleeve - return)
  - Various colors for identification (optional)
- [ ] **Color Convention:** 🔴 RED = Tip | ⚪ WHITE = Sleeve (see `WIRING_COLOR_CONVENTION.md`)
- [ ] **Transistor Circuit (for S-Trig):**
  - 1× 2N3904 NPN transistor (or 2N2222)
  - 1× 1kΩ resistor (brown-black-red)
- [ ] **Testing Equipment:**
  - Digital multimeter
  - Breadboard and jumper wires
  - MIDI controller or keyboard
  - (Optional) Oscilloscope for waveform verification

### Optional (for 0-10V CV)
- [ ] 1× LM358N op-amp (dual, DIP-8)
- [ ] 2× 100kΩ resistors (for 2× gain circuit)
- [ ] 12V power supply (from Powerboost or similar)

---

## Pre-Flight Checklist

**Before wiring anything:**

1. [ ] **Verify MCP4728 is working:**
   - Run `circup list` - confirm `adafruit_mcp4728` is installed
   - Check I2C devices: Should see address 0x60
   - Deploy simple test: `cp tests/mcp4728_voltage_test.py /Volumes/CIRCUITPY/code.py`

2. [ ] **Check available pins:**
   - Review `docs/hardware/PIN_ALLOCATION_MATRIX.md`
   - Verify D10 is available for S-Trig
   - Confirm I2C bus (D21/D22) is shared with OLED + DAC

3. [ ] **Organize workspace:**
   - Clear breadboard area
   - Label all wires with tape/marker
   - Have documentation open (this guide + MCP4728_CV_GUIDE.md)

4. [ ] **Safety check:**
   - Feather M4 powered off
   - All power supplies disconnected
   - Multimeter on hand for continuity checks

---

## Phase 1: Wire CV Pitch Output (Simplest First)

### What We're Building
MCP4728 Channel A → 1/8" Jack → Eurorack/Synth Pitch Input

**Voltage:** 0-5V (1V/octave standard)
**Range:** 5 octaves (MIDI notes 0-60)

### Wiring Steps

1. **Identify MCP4728 Channel A output pin:**
   - MCP4728 breakout board: Look for pin labeled "VOUTA" or "CHA"
   - This is the analog voltage output (0-5V)

2. **Wire signal path:**
   ```
   MCP4728 VOUTA (Channel A) → RED wire   → Jack TIP
   MCP4728 GND              → WHITE wire → Jack SLEEVE
   ```

3. **Physical connections:**
   - Solder RED wire to MCP4728 Channel A output pin
   - Solder WHITE wire to MCP4728 GND pin
   - Solder RED wire to jack TIP terminal
   - Solder WHITE wire to jack SLEEVE terminal

4. **Verify with multimeter (POWER OFF):**
   - Continuity check: MCP4728 VOUTA → Jack TIP (should beep)
   - Continuity check: MCP4728 GND → Jack SLEEVE (should beep)
   - Check for shorts: TIP to SLEEVE should be OPEN (no beep)

### Testing CV Pitch Output

1. **Deploy test code:**
   ```bash
   cp tests/cv_pitch_test.py /Volumes/CIRCUITPY/code.py
   ```

2. **Test procedure:**
   - Connect multimeter to jack (red probe=TIP, black probe=SLEEVE)
   - Set multimeter to DC voltage (20V range)
   - Power on Feather M4

3. **Expected voltages (1V/octave):**

   | MIDI Note | Note Name | Expected Voltage | Tolerance |
   |-----------|-----------|------------------|-----------|
   | 0 | C-1 | 0.00V | ±0.02V |
   | 12 | C0 | 1.00V | ±0.02V |
   | 24 | C1 | 2.00V | ±0.02V |
   | 36 | C2 | 3.00V | ±0.02V |
   | 48 | C3 | 4.00V | ±0.02V |
   | 60 | C4 | 5.00V | ±0.02V |

4. **Interactive test:**
   - Press Button A to cycle through notes
   - Measure voltage at each step
   - Verify voltages match table above

5. **Pass criteria:**
   - All voltages within ±0.05V (±5 cents tuning accuracy)
   - No noise or fluctuation (steady readings)
   - Smooth transitions between notes

### Troubleshooting CV Pitch

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No voltage at all | MCP4728 not initialized | Check I2C connection, run init code |
| Very low voltage (0.3V max) | Using `.value` instead of `.raw_value` | Fix in code (see MCP4728_CV_GUIDE.md) |
| Voltage not changing | DAC not receiving commands | Check serial output for errors |
| Voltage unstable/noisy | Poor ground connection | Re-check GND continuity |

---

## Phase 2: Wire V-Trig Gate Output

### What We're Building
MCP4728 Channel C → 1/8" Jack → Eurorack/Synth Gate Input

**Voltage:** 0V (idle) / 5V (active)
**Type:** Standard positive gate (V-Trig)

### Wiring Steps

1. **Identify MCP4728 Channel C output pin:**
   - MCP4728 breakout board: Pin labeled "VOUTC" or "CHC"

2. **Wire signal path:**
   ```
   MCP4728 VOUTC (Channel C) → RED wire   → Jack TIP
   MCP4728 GND               → WHITE wire → Jack SLEEVE
   ```

3. **Label the jack:**
   - Use tape/label: "V-TRIG GATE" or "GATE (Modern)"
   - This helps distinguish from S-Trig output

4. **Verify with multimeter (POWER OFF):**
   - Continuity check: MCP4728 VOUTC → Jack TIP
   - Check for shorts: TIP to SLEEVE should be OPEN

### Testing V-Trig Gate

1. **Deploy test code:**
   ```bash
   cp tests/gate_vtrig_test.py /Volumes/CIRCUITPY/code.py
   ```

2. **Test procedure:**
   - Connect multimeter to V-Trig jack
   - Power on Feather M4
   - Press Button B to toggle gate

3. **Expected behavior:**
   - **Idle:** 0.00V (±0.05V)
   - **Active:** 5.00V (±0.05V) - or VDD voltage (4.83V typical)
   - **Transition time:** <1ms (instant switching)

4. **Visual test with LED:**
   - Connect LED + resistor (1kΩ) across jack
   - LED should light up when gate is HIGH
   - LED should turn off when gate is LOW

5. **Pass criteria:**
   - Clean 0V/5V switching
   - No voltage droop during sustained gates
   - Works with modular synth (if available)

---

## Phase 3: Wire S-Trig Output (Vintage Compatibility)

### What We're Building
GPIO D10 → NPN Transistor → 1/4" Jack → Vintage Synth Trigger

**Type:** Switch closure (open/short to ground)
**Idle:** Open circuit (floating)
**Active:** Short to ground (<1Ω)

### Circuit Schematic
```
    D10 (3.3V GPIO)
         │
         ├─── 1kΩ resistor ───┐
         │                    │
         │                   BASE
         │                    │
         │              ┌─────┴─────┐
         │              │  2N3904   │
         │              │    NPN    │
         │              └─────┬─────┘
         │                    │
         │                COLLECTOR ──── Jack TIP (S-Trig output)
         │                    │
         │                 EMITTER
         │                    │
        GND ──────────────────┴──────── Jack SLEEVE (Ground)
```

### Wiring Steps

1. **Insert NPN transistor on breadboard:**
   - 2N3904 or 2N2222
   - Flat side facing you, leads down:
     ```
     E   B   C
     │   │   │
     ```
   - Emitter (left) → Ground rail
   - Base (middle) → Empty row (for resistor)
   - Collector (right) → Empty row (for output)

2. **Wire base resistor:**
   - 1kΩ resistor (brown-black-red)
   - One end → M4 pin D10 (via jumper wire)
   - Other end → Transistor BASE pin

3. **Wire output to jack:**
   - Transistor COLLECTOR → 1/4" Jack TIP (RED wire)
   - Ground rail → 1/4" Jack SLEEVE (WHITE wire)

4. **Connect grounds:**
   - M4 GND → Breadboard ground rail
   - Transistor EMITTER → Same ground rail
   - Jack SLEEVE → Same ground rail

5. **Label the jack:**
   - Use tape: "S-TRIG (Vintage)" or "S-TRIG ARP/Korg"

### Testing S-Trig Output

**Test 1: Resistance Check (Multimeter)**

1. **Power OFF** - Disconnect M4
2. Set multimeter to resistance (Ω) or continuity mode
3. Measure between S-Trig jack TIP and SLEEVE

4. **Manual LOW test:**
   - Jumper D10 → GND
   - Measure TIP to SLEEVE
   - **Expected:** OPEN (OL or >10MΩ) - Transistor OFF

5. **Manual HIGH test:**
   - Jumper D10 → 3.3V pin
   - Measure TIP to SLEEVE
   - **Expected:** SHORT (<1Ω, continuity beep) - Transistor ON

6. **If readings are wrong:**
   - Check transistor orientation (flat side reference)
   - Verify 1kΩ resistor is in base circuit
   - Test transistor with diode check

**Test 2: Software Control Test**

1. **Deploy test code:**
   ```bash
   cp tests/strig_transistor_test.py /Volumes/CIRCUITPY/code.py
   ```

2. **Test procedure:**
   - Connect multimeter in continuity mode
   - Power on M4
   - Code toggles D10 every 1 second
   - Watch multimeter readings

3. **Expected behavior:**
   - Pattern: OPEN → SHORT → OPEN → SHORT (repeating)
   - Audible beeps when SHORT
   - Steady open circuit when OPEN

4. **Visual test with vintage synth:**
   - Connect to ARP 2600, Korg MS-20, or similar
   - Should trigger envelope on each pulse
   - No issues with voltage incompatibility

---

## Phase 4: Wire Custom CC Output

### What We're Building
MCP4728 Channel D → 1/8" Jack → Modulation Input

**Voltage:** 0-5V (user-configurable source: CC, Aftertouch, Pitch Bend, Velocity)
**Features:** Smoothing, Learn Mode (Button B long press)

### Wiring Steps

1. **Identify MCP4728 Channel D output pin:**
   - MCP4728 breakout board: Pin labeled "VOUTD" or "CHD"

2. **Wire signal path:**
   ```
   MCP4728 VOUTD (Channel D) → RED wire   → Jack TIP
   MCP4728 GND               → WHITE wire → Jack SLEEVE
   ```

3. **Label the jack:**
   - "CUSTOM CC" or "MOD OUT"

### Testing Custom CC Output

1. **Deploy main firmware** (has Custom CC already implemented):
   ```bash
   cp main.py /Volumes/CIRCUITPY/code.py
   ```

2. **Configure Custom CC:**
   - Navigate to Settings → Custom CC
   - Set source (e.g., "CC 74: Filter Cutoff")
   - Set smoothing level (Off/Low/Mid/High)

3. **Test with MIDI controller:**
   - Connect MIDI controller to MIDI IN
   - Move a CC knob (e.g., mod wheel = CC 1)
   - Measure voltage on Custom CC jack
   - Should vary 0-5V proportionally

4. **Test Learn Mode:**
   - Long press Button B (0.5s) in Custom CC menu
   - Move a CC knob on controller
   - CC number should be captured automatically
   - Test that newly learned CC controls voltage

---

## Phase 5: Optional - 0-10V CV with LM358N Op-Amp

**Why?** Extended range for eurorack (10 octaves instead of 5)

### Circuit Overview

```
MCP4728 CH-A (0-5V) → LM358N (2× gain) → 0-10V Output
```

**Refer to:** `docs/hardware/LM358_WIRING_GUIDE.md` for complete details

### Quick Setup

1. **Power LM358N:**
   - Pin 8 (V+) → 12V rail
   - Pin 4 (GND) → Ground

2. **Input from DAC:**
   - MCP4728 Channel A → LM358N Pin 3 (IN+)

3. **Feedback network (2× gain):**
   - R1 (100kΩ): Pin 2 → GND
   - R2 (100kΩ): Pin 1 → Pin 2

4. **Output:**
   - LM358N Pin 1 (OUT) → New jack "CV 0-10V"

5. **Test:**
   - Deploy `tests/lm358_gain_circuit_test.py`
   - Verify 2× gain: 0V→0V, 5V→10V

**Status:** Circuit already tested and verified working (Session 12)

---

## Phase 6: Integration Testing

### Full Arpeggiator Test

**Goal:** Verify all outputs work together in real arpeggiator use

1. **Deploy main firmware:**
   ```bash
   cp main.py /Volumes/CIRCUITPY/code.py
   ```

2. **Hardware setup:**
   - Connect MIDI keyboard to MIDI IN
   - Connect CV Pitch jack → VCO 1V/oct input
   - Connect V-Trig Gate jack → VCA gate input
   - (Optional) Connect Custom CC → VCF cutoff

3. **Test procedure:**
   - Play chord on MIDI keyboard (e.g., C-E-G)
   - Arpeggiator should activate
   - Watch oscilloscope or listen to audio:
     - CV Pitch should step through notes
     - Gate should pulse on each note
     - Custom CC should modulate filter (if configured)

4. **Verify timing:**
   - Set tempo (e.g., 120 BPM)
   - Set division (e.g., 16th notes)
   - Verify ~31.25ms between gates (120 BPM, 16th = 31.25ms)

5. **Verify patterns:**
   - Test UP pattern (ascending)
   - Test DOWN pattern (descending)
   - Test RANDOM pattern (unpredictable)
   - Test new STRUM pattern (Session 16!)

6. **Pass criteria:**
   - All patterns work correctly
   - CV tracking is accurate (in tune)
   - Gates trigger reliably
   - No crashes or glitches during performance

---

## Troubleshooting Guide

### CV Pitch Issues

| Symptom | Check | Fix |
|---------|-------|-----|
| No voltage | MCP4728 initialization | Re-run `dac.wakeup()` |
| Wrong voltage range | Using .value property | Switch to .raw_value |
| Out of tune | Calibration | Verify 68.27 steps/semitone |
| Noise on output | Ground loop | Use star ground topology |

### Gate Issues

| Symptom | Check | Fix |
|---------|-------|-----|
| Gate stuck HIGH | DAC not updating | Check gate control code |
| Gate stuck LOW | Wrong channel | Verify using Channel C |
| Voltage droop | Load too high | Add buffer op-amp |
| Slow rise time | Capacitive load | Check cable/input impedance |

### S-Trig Issues

| Symptom | Check | Fix |
|---------|-------|-----|
| Always open | Transistor dead | Replace 2N3904 |
| Always short | Transistor saturated | Check base resistor (1kΩ) |
| Weak trigger | Base current too low | Reduce base resistor to 470Ω |
| Vintage synth not responding | Wrong polarity | Verify S-Trig expects short-to-ground |

---

## Final Checklist

Before declaring success:

- [ ] All jacks labeled clearly
- [ ] All grounds connected to common ground
- [ ] All outputs tested with multimeter
- [ ] CV Pitch verified with 1V/octave tracking
- [ ] V-Trig gate switches cleanly (0V/5V)
- [ ] S-Trig opens and shorts correctly
- [ ] Custom CC responds to MIDI input
- [ ] Integration test passes (full arpeggiator works)
- [ ] Documentation updated (pin usage, etc.)
- [ ] Photos taken of breadboard layout
- [ ] Commit changes to git

---

## Next Steps After Wiring

1. **Enclosure design:**
   - Plan jack placement on front/back panel
   - See `docs/hardware/ENCLOSURE_DESIGN.md`

2. **PCB design:**
   - Capture breadboard circuit in KiCad
   - Route proper PCB with jack connectors

3. **Performance optimization:**
   - Measure actual latency (MIDI in → CV out)
   - Optimize for sub-5ms response time

4. **Advanced features:**
   - Velocity to CV (Channel B)
   - Accent/trigger output (pulse width modulation)

---

## Bill of Materials Summary

| Component | Quantity | Purpose | Approx Cost |
|-----------|----------|---------|-------------|
| 1/8" TS mono jack | 3 | CV Pitch, V-Trig, Custom CC | $0.50 each |
| 1/4" TS mono jack | 1 | S-Trig output | $0.60 |
| 2N3904 NPN transistor | 1 | S-Trig switching | $0.10 |
| 1kΩ resistor | 1 | Transistor base | $0.05 |
| LM358N op-amp (optional) | 1 | 0-10V gain | $0.50 |
| 100kΩ resistor (optional) | 2 | Op-amp gain circuit | $0.10 |
| Hookup wire | 10ft | Connections | $2.00 |
| **Total:** | | | **~$5-7** |

---

**Ready to start wiring!** 🔧

Begin with Phase 1 (CV Pitch) - it's the simplest and gives immediate feedback.
