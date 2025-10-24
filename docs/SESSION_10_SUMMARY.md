# Session 10 Summary - CV Output Op-Amp Design

**Date:** 2025-10-24
**Status:** Paused - Waiting for LM7805 voltage regulator to arrive

---

## What We Accomplished

### 1. Identified CV Output Voltage Requirement
- **Problem:** MCP4728 outputs 0-5V, but Eurorack 1V/octave standard requires 0-10V
- **Solution:** Add TL072 op-amp with 2× gain stage (0-5V → 0-10V)
- **Rationale:** Industry-standard approach, no alternative I2C DACs output 10V natively

### 2. Designed Op-Amp Circuit
- **Created:** `docs/hardware/CV_OPAMP_CIRCUIT.md` - Complete 2× gain circuit design
- **Components:** TL072 op-amp, 2× 100kΩ resistors, bypass capacitors
- **Circuit type:** Non-inverting amplifier with Gain = 1 + (R2/R1) = 2×

### 3. Discovered Power Architecture Issue
- **Problem:** TL072 needs 12V to output 10V, but MCP4728 max is 5.5V
- **Initial mistake:** Assumed M4 CAN had a 5V pin (it doesn't!)
- **Correct solution:**
  - Powerboost reconfigured to 12V (A=1, B=1)
  - LM7805 regulator to step 12V → 5V for MCP4728
  - TL072 powered directly from 12V

### 4. Created Comprehensive Breadboard Guide
- **Created:** `docs/hardware/BREADBOARD_WALKTHROUGH.md`
- **Features:**
  - Step-by-step assembly instructions
  - Component education (what resistors, caps, op-amps do)
  - Complete testing procedures
  - Troubleshooting guide
  - Beginner-friendly with clear explanations

---

## Current Hardware Status

### ✅ Components Confirmed Available
- TL072 dual op-amp (using 1 channel)
- 2× 100kΩ resistors
- 3× 100nF (0.1µF) ceramic capacitors
- Breadboard and jumper wires
- Feather M4 CAN Express
- MCP4728 DAC (working at 5V)
- OLED display (working)
- Powerboost module (currently at 5V)

### ❌ Components Needed (Ordered)
- **LM7805 voltage regulator** (TO-220 package)
  - Quantity: 2-5 units
  - Purpose: Convert 12V → 5V for MCP4728
  - No heatsink needed (only 1mA draw)

### 📋 Optional Components to Order
- MOSFET variety kit (for future projects)
  - 2N7000, BS170, BS250, IRLZ44N
  - Not needed for this CV project

---

## Power Architecture (Final Design)

```
LiPo Battery (3.7V)
    ↓
Feather M4 BAT pin
    ↓
Powerboost (reconfigure to 12V: A=1, B=1)
    ├──→ TL072 Pin 8 (VCC+) - needs 12V for 10V output
    │    + 100nF bypass cap to GND
    │
    └──→ LM7805 Voltage Regulator
         Pin 1 (IN): 12V + 100nF cap
         Pin 2 (GND): Common ground
         Pin 3 (OUT): 5V + 100nF cap
              ↓
         MCP4728 VDD (5V, max 5.5V)
```

**Key insight:** Feather M4 CAN has NO 5V pin on headers, so LM7805 is required (not optional).

---

## Signal Path (Complete CV Chain)

```
MIDI Note (USB or DIN)
    ↓
Feather M4 (CircuitPython)
    ↓
MIDI → Voltage conversion (1V/octave)
    ↓
MCP4728 DAC Channel A (0-5V, 12-bit)
    ↓
TL072 Op-Amp (2× gain)
    ↓
CV Output (0-10V, 1V/octave)
    ↓
Eurorack Oscillator (V/Oct input)
```

**Voltage scaling:**
- C0 (MIDI 12) = 0V
- C1 (MIDI 24) = 1V
- C4 (Middle C, MIDI 60) = 4V
- C10 (MIDI 132) = 10V

---

## Next Steps (When LM7805 Arrives)

### 1. Hardware Assembly
- [ ] Reconfigure Powerboost to 12V (solder jumpers A and B)
- [ ] Verify 12V output with multimeter
- [ ] Build LM7805 regulator circuit on breadboard
- [ ] Verify 5V output from LM7805
- [ ] Assemble TL072 op-amp circuit
- [ ] Connect all power and signal paths
- [ ] Test with multimeter (0V → 10V range)

**Estimated time:** 1-2 hours for careful assembly and testing

### 2. Software Development
- [ ] Create CV driver module (`lib/cv_driver.py`)
- [ ] Implement MIDI → CV conversion functions
- [ ] Add 1V/octave scaling
- [ ] Create Gate output functions (MCP4728 Channel B)
- [ ] Integrate into arpeggiator code

**Estimated time:** 2-3 hours

### 3. System Integration
- [ ] Test CV output with modular synthesizer
- [ ] Verify 1V/octave tracking across octaves
- [ ] Test Gate/trigger timing
- [ ] Integrate with arpeggiator patterns
- [ ] Full system test (MIDI → Arp → CV/Gate → Synth)

**Estimated time:** 2-3 hours

---

## Files Created This Session

### Documentation
- `docs/hardware/CV_OPAMP_CIRCUIT.md` - Op-amp circuit design (2× gain)
- `docs/hardware/BREADBOARD_WALKTHROUGH.md` - Complete assembly guide
- `docs/SESSION_10_SUMMARY.md` - This document

### Code
- No new code this session (waiting for hardware)

### Updated
- `docs/hardware/MCP4728_WORKING_SETUP.md` - Clarified 5V operation
- `docs/hardware/pinouts/PINOUT_REFERENCE.md` - Referenced for M4 pins

---

## Key Learnings

### 1. Voltage Requirements for Eurorack CV
- **Standard:** 1V/octave, 0-10V range (10 octaves)
- **Cannot compromise** on this - modular synths expect it
- Op-amp gain stage is industry-standard solution

### 2. M4 CAN Pinout Differences
- **No 5V pin** on Feather M4 CAN Express headers
- Only has 3.3V (3V pin) and BAT (3.0-4.2V)
- Must use voltage regulator for 5V needs

### 3. Power Architecture Planning
- Always verify pin availability before designing circuits
- Voltage regulators are cheap and solve multi-voltage problems
- LM7805 needs minimal components (just bypass caps)

### 4. Component Education Value
- Beginner-friendly documentation helps user learn
- Explaining "what" and "why" prevents future mistakes
- Visual diagrams and step-by-step crucial for hardware

---

## Questions Answered

**Q: Can we use the M4's USB pin for 5V power?**
A: No - M4 CAN doesn't have a USB pin on headers (only 3V and BAT)

**Q: Do we need MOSFETs for level shifting?**
A: No - MCP4728 works with 3.3V I2C at 5V power (already tested)

**Q: Will LM7805 need a heatsink?**
A: No - MCP4728 only draws ~1mA, dissipates only 7mW

**Q: Why not use a 10V DAC directly?**
A: No I2C DACs output 10V natively. Op-amp solution is standard.

**Q: What op-amp should we use?**
A: TL072 (dual) or TL074 (quad) - Eurorack industry standard

---

## When to Resume

**Prerequisites:**
1. ✅ LM7805 voltage regulator arrives
2. ✅ Soldering iron available
3. ✅ Multimeter available
4. ✅ 2-3 hours of uninterrupted time

**Starting point:**
- Follow `docs/hardware/BREADBOARD_WALKTHROUGH.md` from Step 1
- Reconfigure Powerboost first
- Then build regulator circuit
- Then build op-amp circuit
- Test thoroughly before software work

---

## Git Status

**Current branch:** main
**Last commit:** (to be created after this session)

**Files to commit:**
- `docs/hardware/CV_OPAMP_CIRCUIT.md`
- `docs/hardware/BREADBOARD_WALKTHROUGH.md`
- `docs/SESSION_10_SUMMARY.md`
- Updated todo list

---

**Session End:** 2025-10-24
**Next Session:** When LM7805 arrives
**Estimated Assembly Time:** 1-2 hours hardware + 2-3 hours software
