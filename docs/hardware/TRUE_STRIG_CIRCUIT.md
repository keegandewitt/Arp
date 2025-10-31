# True S-Trig Circuit Design

**Date:** 2025-10-31
**Purpose:** Implement real S-Trig (Short-Trigger) for vintage synth compatibility

---

## What is True S-Trig?

**S-Trig = "Short Trigger"**
- **Idle State:** Open circuit (tip floating, no connection to ground)
- **Active State:** Tip shorted to ground/sleeve via transistor
- **NOT voltage-based** - it's a physical switch

**Used By:**
- ARP 2600
- Korg MS-20
- Yamaha CS series
- Other vintage gear from 1970s-1980s

---

## Circuit Design

### Components Needed

| Component | Value/Type | Purpose | Notes |
|-----------|------------|---------|-------|
| NPN Transistor | 2N3904, 2N2222, or similar | Switching element | Any general-purpose NPN works |
| Base Resistor | 1kΩ | Limit current to transistor base | Can use 470Ω - 2.2kΩ |
| (Optional) Pull-up | 10kΩ | Ensure clean open circuit | Only if receiving synth needs it |
| TS Jack | 1/4" mono | S-Trig output connector | Tip = signal, Sleeve = ground |

### Schematic

```
Feather M4
  GPIO Pin (D10) ──┬─── 1kΩ ───┬─── NPN Base (2N3904)
                   │            │
                   │            │
                   │         Collector ──── S-Trig Output (Tip)
                   │            │
                   │         Emitter ──── Ground (Sleeve)
                   │
              (Optional)
              10kΩ Pull-up to +5V
              (only if synth needs it)
```

### How It Works

**GPIO LOW (0V):**
- Transistor is OFF
- Collector-Emitter is OPEN (high impedance)
- S-Trig output is FLOATING (idle state)
- **Result:** No trigger

**GPIO HIGH (3.3V):**
- Transistor is ON (saturated)
- Collector-Emitter is SHORTED (low resistance, ~0.2Ω)
- S-Trig output is SHORTED TO GROUND
- **Result:** Trigger active!

---

## Breadboard Wiring

### Pin Assignments

| M4 Pin | Connection | Notes |
|--------|------------|-------|
| D10 | S-Trig control GPIO | Available, not used by OLED/DAC |
| GND | Common ground | Share with transistor emitter and jack sleeve |

### Transistor Pinout (2N3904 / 2N2222)

```
   Flat side facing you, leads down:

    E   B   C
    │   │   │
   Emitter Base Collector
```

**Connections:**
- **Emitter (E):** → Ground
- **Base (B):** → 1kΩ resistor → M4 D10
- **Collector (C):** → S-Trig jack TIP

### Step-by-Step Breadboard Assembly

1. **Insert NPN transistor** (2N3904) into breadboard
   - Flat side facing you
   - Emitter (left pin) → Ground rail
   - Base (middle pin) → empty row
   - Collector (right pin) → empty row

2. **Base resistor** (1kΩ, brown-black-red)
   - One end → M4 pin D10 (via jumper wire)
   - Other end → Transistor BASE pin

3. **S-Trig output connection**
   - Transistor COLLECTOR → S-Trig jack TIP
   - Ground rail → S-Trig jack SLEEVE

4. **Common ground**
   - M4 GND → Breadboard ground rail
   - Transistor EMITTER → Same ground rail
   - S-Trig jack SLEEVE → Same ground rail

---

## Testing the Circuit

### Test 1: Multimeter Resistance Check

**Setup:**
- Disconnect M4 power
- Set multimeter to resistance mode (Ω)
- Measure between S-Trig TIP and GND

**Test Procedure:**

1. **GPIO Floating (M4 off):**
   - Measure TIP to GND
   - **Expected:** Open circuit (OL or >10MΩ)

2. **GPIO manually grounded:**
   - Connect D10 to GND with jumper
   - Measure TIP to GND
   - **Expected:** Open circuit (OL)

3. **GPIO manually to 3.3V:**
   - Connect D10 to 3.3V pin with jumper
   - Measure TIP to GND
   - **Expected:** SHORT (<1Ω, should beep on continuity)

**If measurements don't match:**
- Check transistor orientation
- Verify base resistor connections
- Test transistor with multimeter (diode mode, check B-E and B-C junctions)

### Test 2: Software Control Test

Upload test code (see `tests/strig_transistor_test.py`):
- Toggles GPIO HIGH/LOW every second
- Monitor with multimeter on S-Trig output
- Should alternate: OPEN → SHORT → OPEN → SHORT

---

## Output Comparison Table

| Mode | Hardware | Idle State | Active State | Output Type | Compatible With |
|------|----------|------------|--------------|-------------|-----------------|
| **V-TRIG** | MCP4728 DAC | 0V | 5V | Voltage source | Modern synths, Eurorack |
| **Inverted Gate** | MCP4728 DAC | 5V | 0V | Voltage source | Some gear (not true S-Trig) |
| **True S-TRIG** | GPIO + Transistor | OPEN (floating) | SHORT to GND | Switch/relay | ARP, Korg MS-20, Yamaha CS |

---

## Safety Notes

1. **Never short V-Trig outputs** - they are voltage sources, will draw excessive current
2. **True S-Trig expects a short** - safe because it's designed for switch closure
3. **Don't mix modes** - use V-Trig OR S-Trig, never both simultaneously on same input
4. **Check your synth's manual** - verify which trigger type it expects

---

## Pin Usage Summary

After implementing S-Trig:

| M4 Pin | Function | Used By |
|--------|----------|---------|
| D21, D22 | I2C (SDA/SCL) | OLED, MCP4728 |
| D5, D6, D9 | Buttons A, B, C | User input |
| D10 | **S-Trig GPIO** | **True S-Trig output** |
| D13 | LED | Status indicator |
| MCP4728 Ch A | CV Pitch | 1V/octave CV output |
| MCP4728 Ch B | CV Velocity | (Future use) |
| MCP4728 Ch C | **V-Trig Gate** | **Standard gate output** |
| MCP4728 Ch D | Trigger | (Future use) |

**User Selects:**
- V-Trig output → Use MCP4728 Channel C (TS cable)
- S-Trig output → Use GPIO D10 transistor circuit (TS cable)
- **Different physical jacks** for each mode

---

## Next Steps

1. ✅ Build transistor circuit on breadboard
2. ✅ Test with multimeter (resistance check)
3. ✅ Write test code (`tests/strig_transistor_test.py`)
4. ✅ Verify switching behavior
5. ⏳ Update gate mode test to use D10 for S-Trig
6. ⏳ Test with actual vintage synth
7. ⏳ Design PCB with both V-Trig and S-Trig outputs

---

**End of Document**
