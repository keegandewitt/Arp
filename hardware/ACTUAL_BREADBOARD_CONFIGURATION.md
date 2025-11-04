# ACTUAL Breadboard Configuration - What You Really Have

**Date:** 2025-11-03 (Session 25)
**Source:** Breadboard photo analysis + documentation research
**Purpose:** Document REALITY, not fiction

---

## What's Actually Built (Verified)

### 1. ✅ S-Trig Output Circuit (CONFIRMED)
**Purpose:** True S-Trig for vintage synths (ARP, Korg MS-20, Yamaha CS)

**Circuit:**
```
GPIO D10 → 1kΩ resistor → 2N3904 NPN Base
                           Collector → 100Ω → TRIG OUT Jack Tip
                           Emitter → GND
```

**Operation:**
- D10 LOW (0V) = Transistor OFF = Jack tip OPEN (idle)
- D10 HIGH (3.3V) = Transistor ON = Jack tip SHORTED TO GND (active trigger)

**Components on breadboard:**
- 1× 2N3904 NPN transistor
- 1× 1kΩ resistor (base current limiting)
- 1× 100Ω resistor (collector series protection)

**Files:** `docs/hardware/TRUE_STRIG_CIRCUIT.md`

---

### 2. ✅ MCP4728 DAC Output with Series Resistor (CONFIRMED)
**Purpose:** Short-circuit protection on DAC outputs

**VB (Channel B) Output - What you're testing:**
```
MCP4728 Channel B (VB pin) → 100Ω resistor → White jack (bottom of breadboard)
                                             GND → Jack sleeve
```

**Why 100Ω resistor?**
- **Short-circuit protection:** If jack accidentally shorts, limits current from DAC
- **DAC protection:** MCP4728 max output current is 25mA
  - Without resistor: Short circuit draws excessive current → DAC damage
  - With 100Ω: Max current = 5V / 100Ω = 50mA (still safe, resistor limits damage)
- **Standard practice:** All professional CV interfaces use series resistors (100Ω-1kΩ typical)

**All DAC channels should have this:**
- Channel A (CV OUT): 100Ω series resistor
- Channel B (TRIG OUT / currently testing): 100Ω series resistor  ✅ ON BREADBOARD
- Channel C (CC OUT): 100Ω series resistor
- Channel D (future): 100Ω series resistor

**Files:** `docs/hardware/PROTOBOARD_LAYOUT.md` (R1, R2, R3, R4)

---

### 3. ✅ Power Rails (CONFIRMED BY USER)
**5V Rail:**
- Source: Feather M4 USB pin (or Powerboost 5V)
- Powers: MCP4728 DAC
- Decoupling: C1 (47µF bulk) + C2 (0.1µF bypass)

**3.3V Rail:**
- Source: Feather M4 3V3 pin
- Powers: MIDI FeatherWing, All LEDs (7 total)
- Decoupling: **NEEDED BUT NOT DOCUMENTED** - should be C9 (10µF) + C10 (0.1µF)

---

### 4. ⚠️ CV/TRIG Inputs - UNCLEAR

**User said:** "I believe there is a resistor between one of the ADC outputs"

**Documentation says:**
- A3 (CV IN) and A4 (TRIG IN) both have voltage divider + protection
- But user has never heard of BAT85 diodes

**CRITICAL SAFETY ISSUE:**
- Feather M4 ADC max input: **3.3V** (anything above = permanent damage)
- Eurorack can send: **0-5V or 0-10V**
- **You MUST have voltage division to protect the M4!**

**Likely reality based on docs:**
```
CV IN Jack → Voltage divider (2× 10kΩ) → A3 ADC
TRIG IN Jack → Voltage divider (2× 10kΩ) → A4 ADC
```

**Voltage scaling:**
- 5V input × (10k / 20k) = 2.5V to ADC ✅ SAFE
- 10V input × (10k / 20k) = 5V to ADC ⚠️ WOULD DAMAGE M4

**Optional smoothing cap:** 100nF from ADC pin to GND (filters noise)

**BAT85 diodes:** Documentation shows them, but you don't have them. They would provide backup overvoltage protection by clamping to 3.3V rail.

---

## What's NOT on Breadboard (Confirmed Removed)

### ❌ Op-Amp for 0-10V Output
**User:** "We eliminated the op amp because Claude told me I only needed 5V for the DAC"

**Correct!** You don't NEED an op-amp. Here's why:

**0-5V Output (current design):**
- 5 octaves range (MIDI notes 0-60, C0 to C5)
- Still 1V/octave Eurorack compliant! ✅
- Most MIDI music uses <5 octaves anyway
- Simpler circuit, fewer components

**0-10V Output (requires op-amp):**
- 10 octaves range (MIDI notes 0-120, C0 to C10)
- Needs TL072 or LM358N op-amp with 2× gain
- Needs +12V power supply (adds complexity)
- **Only needed if you specifically want >5 octave range**

**Recommendation:** Keep 0-5V unless you have a specific need for 10 octaves.

---

## What's Documented But Uncertain (Needs Verification)

### ❓ BAT85 Diode Clamps
**Docs show:** BAT85 Schottky diodes on CV IN and TRIG IN for overvoltage protection

**User says:** "First I'm hearing of BAT85 clamps"

**Likely conclusion:** A previous Claude added these to documentation without building them.

**Purpose if you DID have them:**
- Clamp voltage spikes above 3.3V
- Backup protection if voltage divider fails
- Common in professional designs

**Do you need them?**
- **With proper voltage divider:** No, optional extra safety
- **Without voltage divider:** YES, mandatory to prevent damage

---

## 🔥 CRITICAL QUESTIONS - Must Answer Before PCB Design

### Question 1: Input Voltage Dividers
**Do you have voltage dividers on A3 and A4 inputs?**

Check your breadboard:
- Between CV IN jack and M4 pin A3, are there TWO resistors in series?
- Between TRIG IN jack and M4 pin A4, are there TWO resistors in series?

**If NO voltage dividers:**
- ⚠️ **DANGER!** Eurorack 5V input will damage M4 ADC (3.3V max)
- Must add before any testing with external CV sources

**If YES voltage dividers:**
- ✅ Safe for 0-5V input (with 2× 10kΩ divider)
- ⚠️ Still risky for 0-10V input (need BAT85 clamps or different divider)

### Question 2: Input Voltage Range
**What voltage will you send to CV IN and TRIG IN?**

- Option A: **0-5V only** (most Eurorack) → 2× 10kΩ divider is sufficient
- Option B: **0-10V possible** (some modules) → Need different divider ratio or clamp diodes
- Option C: **Unknown/varied** → Add BAT85 clamps for safety margin

### Question 3: Smoothing Capacitors
**Are there capacitors from ADC pins to GND?**

Check for 100nF (0.1µF) caps:
- From A3 to GND?
- From A4 to GND?

**Purpose:** Filter noise from long patch cables (typical in Eurorack)

**Recommendation:** Add them! Very cheap insurance against noise.

---

## Power Distribution - What You ACTUALLY Need

### Both Boards Need BOTH Rails

**BOTTOM BOARD (Output):**
```
5V Rail (from M4 USB pin):
  C1: 47µF electrolytic (bulk storage)
  C2: 0.1µF ceramic (high-frequency bypass)
  → Powers: MCP4728 DAC

3.3V Rail (from M4 3V3 pin):
  C9: 10µF electrolytic (bulk storage)
  C10: 0.1µF ceramic (high-frequency bypass)
  → Powers: MIDI FeatherWing, 4 white LEDs, 3 RGB LED channels (7 total LEDs)
```

**TOP BOARD (Input) - if you have one:**
```
5V Rail (from headers):
  C11: 10µF electrolytic
  C12: 0.1µF ceramic
  → Powers: Input protection circuits (if active)

3.3V Rail (from headers):
  C13: 10µF electrolytic
  C14: 0.1µF ceramic
  → Powers: Input LEDs (if any), clamp reference (if BAT85 diodes used)
```

**Currently documented:** Only 5V rails (C1, C2)
**Reality:** You use 3.3V for MIDI + LEDs, so you need 3.3V decoupling!

---

## Summary - Truth vs. Fiction

### ✅ TRUTH (Actually on breadboard):
1. MCP4728 DAC outputting 0-5V
2. 100Ω series resistor on VB (Channel B) output for protection
3. S-Trig circuit: D10 → 1kΩ → 2N3904 NPN → 100Ω → jack
4. 5V power rail with C1 (47µF) + C2 (0.1µF)
5. 3.3V power used for MIDI + LEDs

### ❌ FICTION (In docs but not on breadboard):
1. BAT85 diode clamps on inputs (you've never heard of them)
2. Op-amp for 0-10V CV output (you eliminated it)
3. 3.3V power rail decoupling caps (needed but not documented)

### ❓ UNCERTAIN (Needs verification):
1. Voltage dividers on A3/A4 inputs (likely exist, but confirm)
2. Smoothing caps on ADC inputs (should exist, but confirm)
3. Exact input voltage range you'll be receiving

---

## Next Steps for Accurate Documentation

1. **USER:** Please tell me:
   - Do you have resistors between CV/TRIG input jacks and A3/A4 pins?
   - What voltage will you send to those input jacks?
   - Do you want BAT85 overvoltage protection or skip it?

2. **CLAUDE:** Based on answers:
   - Remove BAT85 references if not wanted
   - Add proper 3.3V power rail documentation
   - Create accurate schematics matching ACTUAL breadboard

3. **TOGETHER:** Design PCBs that match what you ACTUALLY built and tested!

---

**Key Insight:** Don't trust documentation blindly. Multiple Claudes have added "improvements" without checking if they were actually built. Always verify against physical reality!
