# CV Output: Correct 1V/Octave Implementation

**Date:** 2025-11-01
**Status:** ✅ CORRECTED - Was incorrectly implemented as 2V/octave for 2 weeks

---

## ⚠️ CRITICAL: 1V/Octave is the ONLY Standard

**Industry Standard:** 1 volt per octave (1V/oct)
- Universal in modular synthesis (Eurorack, Serge, Buchla)
- Expected by ALL voltage-controlled oscillators (VCOs)
- MIDI note / 12 = voltage in volts

**Non-negotiable:** Any other scaling (2V/oct, 0.5V/oct, etc.) is incompatible with standard VCOs.

---

## ❌ What Was Wrong (Sessions 10-13)

### Incorrect Implementation:
```
MCP4728 DAC (0-5V) → LM358N Op-Amp (2× gain) → 1/8" Jack (0-10V)
```

**Problems:**
- 2× gain = 2V/octave (WRONG!)
- VCOs track at half speed
- C4 on MIDI = C3 on VCO (one octave low)
- Requires per-VCO calibration (defeats purpose of standard)

**Why it happened:**
- Assumption: "More voltage = better" (0-10V vs 0-5V)
- Goal: Match Eurorack 10V maximum
- **Missed:** 2× gain breaks 1V/octave standard

---

## ✅ Correct Implementation

### Simple Direct Connection:
```
MCP4728 DAC Channel A → 1/8" Jack
```

**Benefits:**
- ✅ Standard 1V/octave (works with ALL VCOs)
- ✅ 5 octaves range (C0-C4: 0-5V)
- ✅ Simpler circuit (no op-amp, fewer components)
- ✅ No calibration needed
- ✅ Lower noise (fewer amplification stages)

**Configuration:**
```python
# MCP4728 setup (arp/drivers/cv_output.py)
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD  # 5V reference
dac.channel_a.gain = 1  # 1× gain (NO amplification)

# 1V/octave formula
voltage = midi_note / 12.0
raw_value = int((voltage / 5.0) * 4095)
dac.channel_a.raw_value = raw_value
```

**Output Range:**
| MIDI Note | Note Name | Voltage | Octave |
|-----------|-----------|---------|--------|
| 0         | C-1       | 0.00V   | -1     |
| 12        | C0        | 1.00V   | 0      |
| 24        | C1        | 2.00V   | 1      |
| 36        | C2        | 3.00V   | 2      |
| 48        | C3        | 4.00V   | 3      |
| 60        | C4        | 5.00V   | 4      |

**Maximum:** MIDI 60 (C4) = 5.00V = 5 octaves

---

## 🎹 Is 5 Octaves Enough?

**Yes!** 5 octaves is standard for arpeggiators:

**Commercial Examples:**
- **Make Noise 0-Coast:** 0-5V, 5 octaves
- **Pittsburgh Modular Lifeforms:** 0-5V, 5 octaves
- **Korg SQ-1:** 0-8V, 8 octaves (but patterns use 3-4)
- **Arturia Keystep:** 0-10V, 10 octaves (full keyboard range)

**Practical Use:**
- 49-key keyboard = 4 octaves
- 61-key keyboard = 5 octaves ✓
- Arp patterns = 2-3 octaves typically
- Octave transpose: +1/-1 octave fits in 5-octave range

**Conclusion:** 5 octaves (0-5V) is perfect for arpeggiator use.

---

## 🔧 Hardware Wiring

### Direct Connection (No Op-Amp):
```
MCP4728 Pin Connections:
  VDD  → 5V rail (from M4 or external)
  VSS  → Ground
  SDA  → M4 D21 (I2C data)
  SCL  → M4 D22 (I2C clock)

  OUTA → 1/8" Jack Tip (CV Pitch Output)
         1/8" Jack Sleeve → Ground
```

**That's it!** No op-amp, no gain circuit, no extra components.

### What to Remove:
- ❌ LM358N op-amp circuit
- ❌ 2× gain resistor network
- ❌ 12V power supply (if only used for op-amp)

---

## 📝 Testing 1V/Octave

### Verification Procedure:

1. **Set multimeter to DC voltage**
2. **Measure at 1/8" jack:**
   - Black probe → Ground (jack sleeve)
   - Red probe → Signal (jack tip)

3. **Test notes:**
   ```
   C0 (MIDI 12)  → 1.00V ± 0.05V
   C1 (MIDI 24)  → 2.00V ± 0.05V
   C2 (MIDI 36)  → 3.00V ± 0.05V
   C3 (MIDI 48)  → 4.00V ± 0.05V
   C4 (MIDI 60)  → 5.00V ± 0.05V
   ```

4. **Verify with VCO:**
   - Connect CV output to VCO 1V/oct input
   - Play chromatic scale
   - Each semitone = 1/12V step (83.33mV)
   - Each octave doubles frequency

**Pass criteria:**
- ✅ Voltage matches note (±50mV)
- ✅ VCO tracks chromatically
- ✅ Octaves are true octaves (frequency doubles)

---

## 📚 References

**CV/Gate Standards:**
- 1V/octave: https://en.wikipedia.org/wiki/CV/gate
- Eurorack standard: 0-10V maximum, 1V/octave required
- Gate: 5V high, 0V low (separate signal)

**MCP4728 Datasheet:**
- 12-bit DAC (4096 steps)
- 0-5V output with VDD reference
- Formula: `voltage = (raw_value / 4095) × 5.0`

---

## 🎯 Key Takeaways

1. **1V/octave is NON-NEGOTIABLE** - Industry standard since 1960s
2. **More voltage ≠ better** - Correct scaling > maximum voltage
3. **Simpler is better** - Direct DAC output > amplified output
4. **5 octaves is sufficient** - Covers full arpeggiator use cases
5. **Always verify math** - 2× gain = 2V/octave (breaks standard)

---

**Next Steps:**
1. Remove LM358N op-amp circuit from breadboard
2. Connect MCP4728 OUTA directly to 1/8" jack
3. Run `tests/cv_1v_octave_test.py` to verify
4. Test with actual VCO for tracking verification
5. Update all documentation to reflect correct implementation

**Test File:** `tests/cv_1v_octave_test.py` (direct output, no gain)
