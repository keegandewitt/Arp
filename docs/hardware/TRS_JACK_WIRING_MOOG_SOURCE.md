# TRS Jack Wiring - Moog Source Compatibility

**Date:** 2025-11-01
**Status:** 🎯 Design Specification

---

## Overview

We use **TRS (stereo) jacks** for CV and Gate/Trigger outputs. By wiring them to match the Moog Source's specific pinout, we allow users to use **standard TRS cables** without custom adapters.

---

## Moog Source TRS Jack Pinout

The Moog Source synthesizer uses TRS jacks with a specific pinout:

### CV INPUT Jack (KB-CV IN/OUT)
```
1/4" TRS Jack on Moog Source:
  Tip    → CV OUT (from Moog to external)
  Ring   → CV IN  (from external to Moog) ← WE SEND HERE
  Sleeve → Ground
```

**Voltage:** 1.035V/octave (Moog Source quirk - slightly wider than 1V/oct standard)

### TRIG INPUT Jack (TRIG IN/OUT)
```
1/4" TRS Jack on Moog Source:
  Tip    → TRIG IN  (from external to Moog) ← WE SEND HERE
  Ring   → TRIG OUT (from Moog to external)
  Sleeve → Ground
```

**Signal Type:** S-Trig (switch trigger, no pullup)
- High voltage (open circuit) = Note OFF
- Low voltage (short to ground) = Note ON

---

## Our Output Jack Wiring

### Option A: Moog Source Optimized (Recommended)

Wire our outputs to **exactly match** the Moog Source pinout:

**CV Pitch Output (TRS Jack #1):**
```
Our TRS Jack:
  Tip    → CV Pitch (duplicate for standard gear)
  Ring   → CV Pitch (primary - matches Moog Source)
  Sleeve → Ground

MCP4728 Channel A → Both Tip and Ring in parallel
```

**S-Trig Output (TRS Jack #2):**
```
Our TRS Jack:
  Tip    → S-Trig (primary - matches Moog Source)
  Ring   → Not connected (or V-Trig for dual compatibility)
  Sleeve → Ground

S-Trig Circuit → Tip
```

**Benefits:**
- ✅ Moog Source users: Use standard TRS cable, plug and play
- ✅ Standard users: Use TS mono cable on Tip, works perfectly
- ✅ No custom cables needed for anyone

### Option B: Dual Compatibility (Advanced)

Add both S-Trig and V-Trig on the same jack:

**Gate/Trigger Output (TRS Jack #2):**
```
Our TRS Jack:
  Tip    → S-Trig (for Moog Source)
  Ring   → V-Trig (for standard Eurorack)
  Sleeve → Ground

S-Trig Circuit → Tip (inverted logic)
V-Trig Circuit → Ring (standard 5V gate)
```

**Benefits:**
- ✅ One jack handles both Moog and standard gear
- ✅ Users select by cable type (TS tip vs TRS ring)

---

## Hardware Implementation

### CV Pitch Jack Wiring

```
MCP4728 Channel A (OUTA):
  ┌──→ TRS Jack Tip (CV for standard gear)
  │
  └──→ TRS Jack Ring (CV for Moog Source)

TRS Jack Sleeve → Ground
```

**Parts:**
- 1× Switchcraft 112BX or equivalent TRS jack (1/4" or 3.5mm)
- Wire: 22 AWG solid core for breadboard

### S-Trig Jack Wiring

```
S-Trig Output (from MCP4728 Channel B via transistor):
  └──→ TRS Jack Tip (S-Trig for Moog Source)

TRS Jack Sleeve → Ground
TRS Jack Ring → (optional V-Trig for dual mode)
```

**S-Trig Circuit:**
- See `docs/sessions/Session_13_Handoff.md` for verified S-Trig circuit
- Uses transistor to invert 5V gate to S-Trig (high → low on trigger)

---

## Cable Guide for Users

### For Moog Source Owners:

**CV Cable:**
- Use: Standard **TRS cable** (stereo)
- From: Our "CV Pitch" TRS jack
- To: Moog Source "KB-CV IN/OUT" jack
- Signal path: Our Ring → Moog Ring (CV IN)

**Trigger Cable:**
- Use: Standard **TRS cable** (stereo)
- From: Our "S-Trig" TRS jack
- To: Moog Source "TRIG IN/OUT" jack
- Signal path: Our Tip → Moog Tip (TRIG IN)

### For Standard Eurorack Owners:

**CV Cable:**
- Use: **TS cable** (mono) or TRS with tip
- From: Our "CV Pitch" TRS jack
- To: VCO "1V/Oct" input
- Signal path: Our Tip → VCO CV IN

**Gate Cable:**
- Use: **TS cable** (mono)
- From: Our "V-Trig" output (if using Option B)
- To: VCO/EG "Gate" input
- Signal path: Our Tip (or Ring if using TRS) → Gate IN

---

## Voltage Levels

### CV Pitch
- **Range:** 0-5V
- **Standard:** 1V/octave (C3 @ MIDI 60 = 1.0V)
- **Moog Source mode:** 1.035V/octave (C3 @ MIDI 60 = 1.0V)
- **Resolution:** 12-bit DAC = ~1.2mV per step

### S-Trig (Tip)
- **High (Note OFF):** ~5V (open circuit via pullup resistor)
- **Low (Note ON):** ~0V (transistor shorts to ground)
- **Inverted logic:** Opposite of standard gate

### V-Trig (Ring - Optional)
- **High (Note ON):** 5V
- **Low (Note OFF):** 0V
- **Standard logic:** Same as Eurorack gate

---

## Testing Procedure

### Verify CV on TRS Jack:

1. **Set multimeter to DC voltage**
2. **Measure Ring to Sleeve:**
   - Black probe → Sleeve (ground)
   - Red probe → Ring (CV IN for Moog)
   - Expected: 0-5V depending on note

3. **Measure Tip to Sleeve:**
   - Should match Ring voltage (parallel connection)

### Verify S-Trig on TRS Jack:

1. **Measure Tip to Sleeve (no note playing):**
   - Expected: ~5V (high state)

2. **Measure Tip to Sleeve (note playing):**
   - Expected: ~0V (shorted to ground)

3. **Verify inversion:**
   - Standard gate HIGH → S-Trig goes LOW ✓

---

## References

- **Moog Source Manual:** Pages 48-49 (CV/Trig specifications)
- **Kenton Electronics:** [Moog Source MIDI-CV Guide](https://kentonuk.com/ordering-info/what-kenton-products-do-i-need-to-work-with-my-synth/moog-source/)
- **S-Trig Circuit:** `docs/sessions/Session_13_Handoff.md` (verified working)
- **CV Implementation:** `docs/hardware/CV_OUTPUT_CORRECT_IMPLEMENTATION.md`

---

## Key Decisions

1. ✅ **Use TRS jacks** (not TS mono) for both CV and Trig outputs
2. ✅ **Wire Ring = CV IN** (matches Moog Source CV input)
3. ✅ **Wire Tip = S-Trig** (matches Moog Source Trig input)
4. ✅ **Duplicate CV to both Tip and Ring** (works with TS or TRS cables)
5. ⏳ **Decide:** Add V-Trig on Ring of Trig jack for dual compatibility?

---

**Next Steps:**
1. Wire TRS jacks according to Option A (Moog Source optimized)
2. Test with multimeter to verify pinout
3. Test with actual Moog Source (if available)
4. Document in user manual which cable types to use
