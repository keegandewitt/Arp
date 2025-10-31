# True S-Trig Breadboard Wiring Guide

**Step-by-step assembly guide for the S-Trig transistor circuit**

---

## Parts You'll Need

From your parts bin:
- [ ] 1× NPN transistor (2N3904, 2N2222, or similar)
- [ ] 1× 1kΩ resistor (brown-black-red, or 470Ω-2.2kΩ works)
- [ ] Jumper wires
- [ ] Breadboard (if not already using one)

Tools:
- [ ] Multimeter (for testing)

---

## Transistor Identification

### 2N3904 / 2N2222 Pinout

```
Looking at the FLAT side, leads pointing DOWN:

     ┌─────────┐
     │  FLAT   │
     │  SIDE   │
     └─────────┘
        │ │ │
        E B C

    E = Emitter   (left)
    B = Base      (middle)
    C = Collector (right)
```

**How to identify the flat side:**
- The transistor body has one flat side and one rounded side
- Hold it so the flat side faces you
- Leads should point downward
- Left to right: **E-B-C**

---

## Breadboard Layout

```
Feather M4 CAN
┌─────────────────────┐
│                     │
│  D10 ●──────────────┼──→ To 1kΩ resistor
│  GND ●──────────────┼──→ To ground rail
│                     │
└─────────────────────┘


Breadboard:
═══════════════════════════════════════════
 + Rail (not used)
───────────────────────────────────────────
 - Rail (GROUND) ◄────── M4 GND
═══════════════════════════════════════════

Row 10:  [1kΩ]─[1kΩ]   (resistor)
              │
Row 11:       └─────[B]  (base)
                    [E]  (emitter) ──→ GND rail
                    [C]  (collector) ──→ S-Trig TIP

═══════════════════════════════════════════

Where:
  [1kΩ] = 1kΩ resistor (one end to D10, one end to Base)
  [E]   = Transistor Emitter
  [B]   = Transistor Base
  [C]   = Transistor Collector
```

---

## Step-by-Step Assembly

### Step 1: Ground Connection

```bash
Connect M4 GND to breadboard ground rail
```

- Use a jumper wire
- One end: M4 GND pin
- Other end: Blue/Black ground rail on breadboard

---

### Step 2: Insert Transistor

```
Insert 2N3904 into breadboard:
- FLAT SIDE facing you
- Leads pointing down into breadboard
- Use 3 adjacent holes in the same row
```

**Recommended position:** Row 15, columns E-F-G

```
    E    B    C
    │    │    │
   15e  15f  15g  ← Breadboard holes
```

---

### Step 3: Connect Emitter to Ground

```bash
Transistor EMITTER (left pin) → Ground rail
```

- Use a short jumper wire
- One end: Same row as Emitter (e.g., hole 15e)
- Other end: Ground rail (blue/black stripe)

---

### Step 4: Install Base Resistor

```
1kΩ resistor (brown-black-red):
- One leg: Same row as Base (e.g., hole 15f)
- Other leg: Empty row for D10 connection (e.g., hole 10f)
```

The resistor bridges between:
- Transistor BASE row → Empty row for GPIO

---

### Step 5: Connect D10 to Base Resistor

```bash
M4 Pin D10 → Base resistor (empty leg)
```

- Jumper wire from M4 D10
- To the resistor leg that's NOT connected to the base
- This controls the transistor ON/OFF

---

### Step 6: S-Trig Output Connection

```bash
Transistor COLLECTOR (right pin) → S-Trig jack TIP
```

**For testing (no jack yet):**
- Just leave collector available for multimeter probing
- Probe between: Collector pin and Ground

**For final assembly (with jack):**
- Jumper from Collector → TS jack TIP terminal
- Ground rail → TS jack SLEEVE terminal

---

## Final Wiring Checklist

Double-check these connections:

- [ ] M4 GND → Breadboard ground rail
- [ ] Transistor EMITTER → Ground rail
- [ ] Transistor BASE → 1kΩ resistor → M4 D10
- [ ] Transistor COLLECTOR → S-Trig output (or test point)
- [ ] Transistor orientation: FLAT SIDE toward you, E-B-C left-to-right

---

## Testing the Circuit

### Test 1: Visual Inspection

Before applying power:
- [ ] Transistor flat side facing correct direction?
- [ ] Emitter connected to ground?
- [ ] Base has resistor to D10?
- [ ] Collector going to output?
- [ ] No shorts between adjacent pins?

### Test 2: Multimeter Resistance Check (Powered Off)

**M4 powered OFF, multimeter in resistance mode:**

1. **Check Base-Emitter junction:**
   - Multimeter: Red → Base, Black → Emitter
   - Should read: ~600-700Ω (diode junction)
   - Reverse probes: Should read OPEN (OL)

2. **Check Base-Collector junction:**
   - Multimeter: Red → Base, Black → Collector
   - Should read: ~600-700Ω (diode junction)
   - Reverse probes: Should read OPEN (OL)

3. **Check Collector-Emitter:**
   - Either polarity
   - Should read: OPEN (OL) when transistor is OFF

**If readings don't match:** Transistor is damaged or incorrectly oriented

### Test 3: Deploy Test Code

1. **Deploy the test:**
   ```bash
   cp tests/strig_transistor_test.py /Volumes/CIRCUITPY/code.py
   ```

2. **Watch for LED pattern:**
   - LED ON for 1 second = S-Trig ACTIVE (short to GND)
   - LED OFF for 1 second = S-Trig IDLE (open circuit)

3. **Measure with multimeter (resistance mode):**
   - Probes: Collector to Ground
   - When LED ON: Should read < 1Ω (SHORT)
   - When LED OFF: Should read OL (OPEN)

**Expected console output:**
```
============================================================
TRUE S-TRIG TRANSISTOR TEST
============================================================

[1] S-Trig ACTIVE (GPIO HIGH)
    → Multimeter should read: SHORT (<1Ω)
    → LED: ON

[1] S-Trig IDLE (GPIO LOW)
    → Multimeter should read: OPEN (OL)
    → LED: OFF
```

---

## Troubleshooting

### LED blinks but multimeter always reads OPEN
**Problem:** Transistor not conducting
**Fixes:**
- Check transistor orientation (flat side correct?)
- Verify base resistor is connected to D10
- Test transistor with diode mode (see Test 2 above)
- Try a different transistor

### LED blinks but multimeter always reads SHORT
**Problem:** Transistor stuck ON or shorted
**Fixes:**
- Check for solder bridges or wire shorts
- Verify emitter is connected to ground (not base!)
- Try a different transistor

### Multimeter reads ~300Ω when "shorted"
**Problem:** Not fully saturated
**Note:** This is still acceptable for S-Trig (< 500Ω is fine)
**Optional improvement:** Reduce base resistor to 470Ω for deeper saturation

### Nothing happens (LED doesn't blink)
**Problem:** Code not running or pin issue
**Fixes:**
- Check serial console for errors
- Verify D10 is not already used by something else
- Press RESET button on M4
- Re-deploy test code

---

## Success Criteria

Your circuit is working correctly if:

- ✅ LED blinks every second (ON/OFF pattern)
- ✅ When LED is ON: Multimeter reads < 1Ω (short to ground)
- ✅ When LED is OFF: Multimeter reads OL (open circuit)
- ✅ Pattern is stable and repeats consistently

**If all checks pass: You have a working true S-Trig circuit!** 🎉

---

## Next Steps

Once the circuit is verified:

1. Integrate into gate mode test (update code to use D10 for S-Trig)
2. Add physical TS jack for S-Trig output
3. Label jacks clearly: "V-TRIG" and "S-TRIG"
4. Test with actual vintage synth!

---

**End of Guide**
