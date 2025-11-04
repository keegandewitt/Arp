# Diode Installation - Visual Breadboard Guide

**Date:** 2025-11-03 (Session 25)
**Purpose:** Show exactly where to install protection diodes on breadboard

---

## Current Breadboard Layout (CV IN Example)

**What you have now (voltage divider only):**

```
Breadboard Row Layout:
┌─────────────────────────────────────────────────────┐
│ Row 1:  [CV IN Jack TIP wire]                       │
│           │                                          │
│ Row 2:  [10kΩ R1 leg 1] ← connected to Row 1        │
│           │                                          │
│ Row 3:  [10kΩ R1 leg 2] ← TAP POINT                 │
│           │                                          │
│           ├──→ [Wire to M4 pin A3]                  │
│           │                                          │
│ Row 4:  [10kΩ R2 leg 1] ← connected to Row 3        │
│           │                                          │
│ Row 5:  [10kΩ R2 leg 2] ← connected to GND rail     │
└─────────────────────────────────────────────────────┘
```

**Voltage scaling:**
- 5V at Jack → 2.5V at TAP → 2.5V to M4 ADC ✅
- 10V at Jack → 5.0V at TAP → 💥 DAMAGE

---

## After Adding Diode Protection

**New circuit (with BAT85 or 1N4148 diode):**

```
Breadboard Row Layout:
┌──────────────────────────────────────────────────────┐
│ Row 1:  [CV IN Jack TIP wire]                        │
│           │                                           │
│ Row 2:  [10kΩ R1 leg 1]                              │
│           │                                           │
│ Row 3:  [10kΩ R1 leg 2] ← TAP POINT (Modified)       │
│           │                                           │
│           ├──→ [Wire to M4 pin A3]                   │
│           │                                           │
│           ├──→ [Diode ANODE (non-banded end)]        │
│           │                                           │
│           └──→ [100nF cap leg] (optional)            │
│                                                       │
│ Row 4:  [Diode CATHODE (banded end)] ────→ 3.3V rail│
│                                                       │
│ Row 5:  [100nF cap leg] ────→ GND rail (optional)    │
│                                                       │
│ Row 6:  [10kΩ R2 leg 1]                              │
│           │                                           │
│ Row 7:  [10kΩ R2 leg 2] ────→ GND rail               │
└──────────────────────────────────────────────────────┘
```

**Voltage scaling with diode protection:**
- 5V at Jack → 2.5V at TAP → diode OFF → 2.5V to M4 ADC ✅
- 10V at Jack → 5.0V at TAP → diode ON → clamps to 3.7V (BAT85) or 4.0V (1N4148)

---

## Physical Diode Identification

### BAT85 Schottky Diode
```
Visual appearance:
┌─────────────────────────┐
│  [▓▓▓]═══════════[   ]  │  ← Glass body, tiny diode
│   ↑                ↑    │
│ Cathode          Anode  │
│ (banded)        (plain) │
│                         │
│ Black or silver band    │
│ marking cathode end     │
└─────────────────────────┘

Markings:
- May have "BAT85" printed on glass (very tiny)
- Single band on cathode end
- Glass body, axial leads
```

### 1N4148 Silicon Diode
```
Visual appearance:
┌─────────────────────────┐
│  [███]═══════════[   ]  │  ← Glass body, similar size
│   ↑                ↑    │
│ Cathode          Anode  │
│ (banded)        (plain) │
│                         │
│ Black band marking      │
│ cathode end             │
└─────────────────────────┘

Markings:
- May have "1N4148" printed on glass
- Single black band on cathode end
- Looks almost identical to BAT85
```

**CRITICAL: The band ALWAYS marks the CATHODE, which goes to 3.3V!**

---

## Step-by-Step Installation

### Step 1: Power OFF
```
[ ] Disconnect M4 USB power
[ ] Wait 10 seconds for capacitors to discharge
```

### Step 2: Identify TAP Point
```
Current breadboard:
  CV IN Jack → 10kΩ → [TAP] → M4 pin A3
                        ↓
                      10kΩ
                        ↓
                       GND

TAP is where the wire to A3 connects (between the two resistors)
```

### Step 3: Identify Diode Orientation
```
Hold diode with band on RIGHT:
  [     body     ][▓]  ← Band on right
   Anode      Cathode

Remember: "Band goes to 3.3V rail"
```

### Step 4: Insert Diode
```
Breadboard insertion:
  Row 3 (TAP): Insert diode ANODE (non-banded end)
  Row 4 (new): Insert diode CATHODE (banded end)

Then connect Row 4 to 3.3V rail with jumper wire
```

### Step 5: Optional - Add Smoothing Cap
```
100nF ceramic capacitor (marked "104"):
  One leg: Row 3 (TAP point)
  Other leg: Row 5 (GND rail)

This filters noise from long patch cables
```

### Step 6: Verify Wiring
```
Visual check:
  [ ] Diode anode (non-banded) connected to TAP
  [ ] Diode cathode (banded) connected to 3.3V
  [ ] Original divider resistors still in place
  [ ] Wire from TAP to M4 pin A3 still connected
```

---

## Testing Procedure

### Test 1: Diode Polarity Check (MUST DO!)
```
Equipment: Multimeter in diode mode
Power: OFF

Steps:
1. Red probe on TAP point (Row 3)
2. Black probe on 3.3V rail (Row 4)
3. Should read: 0.4V-0.5V (forward voltage)

4. Swap probes
5. Should read: OL or >1V (reverse blocking)

If both directions read low → DIODE BACKWARD! Fix it!
```

### Test 2: Power-On Voltage Check
```
Equipment: Multimeter on DC voltage
Power: ON (USB connected)

Steps:
1. Measure 3.3V rail → should read 3.3V ±0.1V
2. Measure TAP point with nothing connected → should read ~0V
3. Apply 5V to input jack (jumper from M4 USB pin)
4. Measure TAP point → should read ~2.5V
5. If reads 3.3V → diode conducting (bad), check wiring
```

### Test 3: ADC Functionality
```
Equipment: M4 running CircuitPython
Power: ON

Code:
import board
import analogio

cv_in = analogio.AnalogIn(board.A3)
voltage = cv_in.value * 3.3 / 65535
print(f"CV IN: {voltage:.2f}V")

Expected:
- Nothing connected: ~0V
- 5V jumper connected: ~2.5V
- If reads 3.3V: diode may be conducting, investigate
```

### Test 4: Protection Verification (Optional)
```
WARNING: Only do this if confident in wiring!

Equipment: Variable power supply or 9V battery
Power: ON

Steps:
1. Connect 9V to input jack
2. Measure at TAP point
3. Should NOT exceed 4.0V (1N4148) or 3.7V (BAT85)
4. If exceeds → diode not working, check orientation

DO NOT test with >10V unless you're certain diode is correct!
```

---

## Complete Circuit for Both Inputs

**CV IN (A3) and TRIG IN (A4) - identical circuits:**

```
Schematic (each input):
                        ┌─── M4 pin A3 (or A4)
                        │
Input Jack ── 10kΩ ── [TAP] ── Diode ── 3.3V
                        │
                      100nF
                        │
                       GND
```

**Breadboard physical layout:**

```
Left side (CV IN):              Right side (TRIG IN):
Row 1: CV Jack                  Row 1: TRIG Jack
Row 2: 10kΩ R1                  Row 2: 10kΩ R1
Row 3: TAP + diode anode        Row 3: TAP + diode anode
       + 100nF cap              + 100nF cap
       + wire to A3             + wire to A4
Row 4: Diode cathode → 3.3V    Row 4: Diode cathode → 3.3V
Row 5: 100nF cap → GND          Row 5: 100nF cap → GND
Row 6: 10kΩ R2                  Row 6: 10kΩ R2
Row 7: 10kΩ R2 → GND            Row 7: 10kΩ R2 → GND
```

---

## Common Mistakes and How to Avoid

### Mistake 1: Diode Backward
**Symptoms:**
- TAP point always reads 3.3V (even with no input)
- ADC always reads max value
- Diode gets warm

**Fix:**
- Power OFF
- Flip diode around (band to 3.3V, not to TAP)

### Mistake 2: Diode on Wrong Rail
**Symptoms:**
- No protection (TAP can still reach 5V+)
- Diode never conducts

**Fix:**
- Cathode (banded end) MUST go to 3.3V
- NOT to 5V, NOT to GND

### Mistake 3: TAP Point Wrong
**Symptoms:**
- Voltage division doesn't work
- Full input voltage reaches ADC

**Fix:**
- TAP must be BETWEEN the two 10kΩ resistors
- Verify with multimeter: TAP should read 1/2 input voltage

### Mistake 4: No Voltage Divider
**Symptoms:**
- Diode always conducting (TAP always at 3.3V)
- ADC always reads max

**Fix:**
- You MUST have voltage divider (2× 10kΩ)
- Diode is backup protection, not primary!

---

## Parts Needed (Per Input)

**Minimum protection (current status):**
- 2× 10kΩ resistors (brown-black-orange) ✅ You already have

**Good protection (add diode):**
- Everything above, PLUS:
- 1× BAT85 or 1N4148 diode
- Cost: $0.25-0.50 per input

**Best protection (add diode + smoothing):**
- Everything above, PLUS:
- 1× 100nF (0.1µF) ceramic capacitor
- Cost: $0.35-0.60 per input

**For both inputs (CV + TRIG):**
- 4× 10kΩ resistors ✅ You have
- 2× BAT85 (or 1N4148) diodes ← Need to buy
- 2× 100nF capacitors ← Optional

**Total shopping:**
- BAT85 10-pack: $2 (Digi-Key)
- OR 1N4148 120-pack: $5 (Amazon)
- Capacitors: ~$1 for 10-pack

---

## Before/After Comparison

### BEFORE (Current Breadboard):
```
Protection: Voltage divider only
Safe up to: 6.6V input
Safety rating: ⭐⭐⭐ 60%
Risk: Damage from 7V+ inputs or voltage spikes
Cost: $0.40 (4 resistors)
```

### AFTER (With 1N4148 Diodes):
```
Protection: Divider + silicon diode clamp
Safe up to: ~8V input (clamps at 4.0V)
Safety rating: ⭐⭐⭐⭐ 80%
Risk: Slight overvoltage (0.2V over spec)
Cost: $0.40 + $0.10 = $0.50 per input
```

### AFTER (With BAT85 Diodes):
```
Protection: Divider + Schottky diode clamp
Safe up to: 40V+ input (clamps at 3.7V)
Safety rating: ⭐⭐⭐⭐⭐ 100%
Risk: None (industry standard)
Cost: $0.40 + $0.25 = $0.65 per input
```

### AFTER (With BAT85 + Smoothing Cap):
```
Protection: Divider + clamp + noise filter
Safe up to: 40V+ input, immune to RF interference
Safety rating: ⭐⭐⭐⭐⭐ 100% + clean signals
Risk: None
Cost: $0.40 + $0.25 + $0.10 = $0.75 per input
```

---

## Quick Reference Card

**Print this and keep by your breadboard:**

```
╔═══════════════════════════════════════════╗
║  DIODE INSTALLATION QUICK REFERENCE       ║
╠═══════════════════════════════════════════╣
║                                           ║
║  1. POWER OFF!                            ║
║                                           ║
║  2. Band = Cathode = to 3.3V              ║
║                                           ║
║  3. Anode (no band) = to TAP/ADC          ║
║                                           ║
║  4. TAP = between 10kΩ resistors          ║
║                                           ║
║  5. Test polarity before power on!        ║
║                                           ║
║  Correct orientation:                     ║
║   TAP ──→ [Diode anode]                  ║
║           [Diode cathode] ──→ 3.3V       ║
║                                           ║
║  Test: Multimeter diode mode              ║
║   Red on TAP, Black on 3.3V = 0.4V ✅     ║
║   Reversed probes = OL ✅                 ║
║                                           ║
╚═══════════════════════════════════════════╝
```

---

## What You'll See After Installation

**Normal operation (0-3.3V input):**
- Diode does nothing (invisible to circuit)
- Voltage divider scales input by 1/2
- ADC reads accurate voltages
- Everything works as before

**Overvoltage event (>3.3V input):**
- Diode turns ON instantly (<1ns for BAT85, ~4ns for 1N4148)
- TAP voltage clamped to 3.7V (BAT85) or 4.0V (1N4148)
- ADC protected from damage
- You might not even notice it happened!

**Indicator that diode saved you:**
- If you measure TAP and it's exactly 3.7V or 4.0V during high input
- That means diode is clamping (doing its job!)

---

## Ready to Install?

**Checklist before you start:**
- [ ] Diodes purchased (BAT85 or 1N4148)
- [ ] Optional: 100nF capacitors
- [ ] Multimeter ready (for testing)
- [ ] Breadboard clear and organized
- [ ] 3.3V rail location identified
- [ ] TAP points identified (between 10kΩ resistors)
- [ ] M4 powered OFF

**Estimated installation time:**
- First input: 10 minutes (learning)
- Second input: 5 minutes (you're a pro now!)

**You've got this! The hardest part is just remembering: band to 3.3V**
