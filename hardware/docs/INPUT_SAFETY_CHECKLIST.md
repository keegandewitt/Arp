# CV/TRIG Input Safety - Critical Checklist

**Date:** 2025-11-03 (Session 25)
**Priority:** 🔥 CRITICAL - Can permanently damage M4 if wrong
**Purpose:** Ensure your breadboard inputs won't destroy the Feather M4

---

## 🚨 THE DANGER

**Feather M4 ADC Specifications:**
- **Maximum Safe Input:** 3.3V
- **Absolute Maximum:** 3.6V (brief spikes only)
- **Above 3.6V:** Permanent damage to ADC pin, possibly entire chip

**What Eurorack Modules Send:**
- **Standard CV:** 0-5V (1V/octave pitch control)
- **Some modules:** Can output up to 10V
- **Hot-patching mistakes:** Could send full power rail voltage

**Without Protection:**
```
Eurorack 5V → A3/A4 pin → 💥 INSTANT DAMAGE
```

---

## ✅ IMMEDIATE SAFETY CHECK

### Step 1: Check What You Have RIGHT NOW

**Look at your breadboard and trace the wires:**

1. **Find CV IN jack** (if connected)
   - Follow the wire from jack TIP
   - Does it go DIRECTLY to M4 pin A3?
   - OR does it go through resistors first?

2. **Find TRIG IN jack** (if connected)
   - Follow the wire from jack TIP
   - Does it go DIRECTLY to M4 pin A4?
   - OR does it go through resistors first?

**CRITICAL QUESTION:**
**Are there ANY resistors between the input jacks and the M4 ADC pins?**

---

## 🔍 What to Look For

### SAFE Configuration (What You SHOULD Have):

```
Input Jack TIP
    ↓
  [Resistor 1] ← 10kΩ (brown-black-orange)
    ↓
  [TAP POINT] ← Wire to M4 pin A3 or A4 comes from here
    ↓
  [Resistor 2] ← 10kΩ (brown-black-orange)
    ↓
   GND
```

**This is a voltage divider:**
- Divides input voltage in half
- 5V input → 2.5V to ADC ✅ SAFE
- 10V input → 5V to ADC ⚠️ Still too high, but less dangerous

### UNSAFE Configuration (What You Should NOT Have):

```
Input Jack TIP → Wire → Directly to M4 pin A3 or A4
                         💥 DANGER ZONE
```

**No resistors = NO PROTECTION = DAMAGE ON 5V INPUT**

---

## 📋 Your Action Plan

### If You Have Voltage Dividers Already: ✅ YOU'RE SAFE (mostly)

1. **Verify the values:**
   - Should be two 10kΩ resistors in series
   - Color code: brown-black-orange-gold

2. **Optional improvement - Add smoothing cap:**
   ```
   From tap point (between the two resistors)
       ↓
   100nF capacitor (104 marking)
       ↓
   GND
   ```
   Purpose: Filters noise from long patch cables

3. **Optional extra safety - Add clamp diode:**
   ```
   From tap point
       ↓
   BAT85 Schottky diode (cathode to 3.3V rail)
   ```
   Purpose: Clamps any voltage above ~3.9V

### If You DON'T Have Voltage Dividers: 🔥 STOP TESTING NOW

**DO NOT CONNECT EXTERNAL CV SOURCES UNTIL YOU ADD PROTECTION!**

**Quick Fix (5 minutes):**

**Parts needed:**
- 4× 10kΩ resistors (brown-black-orange) - $0.10 each
- 2× 100nF capacitors (optional but recommended) - $0.10 each

**For CV IN (A3):**
```
1. Remove direct wire from jack to A3
2. Wire jack TIP to one end of R1 (10kΩ)
3. Wire other end of R1 to TAP POINT
4. Wire TAP POINT to M4 pin A3
5. Wire TAP POINT to one end of R2 (10kΩ)
6. Wire other end of R2 to GND
7. [Optional] Wire 100nF cap from TAP POINT to GND
```

**For TRIG IN (A4):**
```
Same as above, but use A4 instead of A3
```

**Visual diagram:**
```
CV IN Jack               TRIG IN Jack
    TIP                      TIP
     │                        │
   [10kΩ] R1              [10kΩ] R1
     │                        │
   [TAP]──→ A3            [TAP]──→ A4
     │                        │
 [100nF]                  [100nF]
     │                        │
   [10kΩ] R2              [10kΩ] R2
     │                        │
    GND                      GND
```

---

## 🧪 Testing Your Protection Circuit

**BEFORE connecting any external CV source:**

1. **Voltage test with multimeter:**
   ```
   - Power off M4
   - Set multimeter to resistance mode
   - Measure from jack TIP to GND
   - Should read ~20kΩ (two 10kΩ in series)
   ```

2. **Voltage division test:**
   ```
   - Power on M4
   - Connect 5V from M4 USB pin to input jack TIP (via jumper wire)
   - Measure voltage at TAP POINT (where wire goes to A3/A4)
   - Should read ~2.5V
   - If it reads 5V → DIVIDER NOT WORKING, FIX BEFORE PROCEEDING
   ```

3. **Safe voltage test:**
   ```
   - With 5V connected to jack (through divider)
   - Measure voltage at M4 pin A3 or A4
   - Should read ~2.5V (safe for 3.3V ADC)
   ```

---

## 🎯 Long-Term Solution for PCB

**For production PCB design, use this proven circuit:**

```
Input Jack TIP
    ↓
  [10kΩ] Series protection
    ↓
  [10kΩ] Voltage divider (to GND)
    ↓ (TAP)
  [100nF] Low-pass filter (to GND)
    ↓
  [BAT85] Overvoltage clamp (cathode to 3.3V)
    ↓
  M4 ADC Pin (A3 or A4)
```

**Protection layers:**
1. **Voltage divider:** Scales 5V → 2.5V (primary protection)
2. **Low-pass filter:** Removes noise and RF interference
3. **Clamp diode:** Backup protection against voltage spikes
4. **Series resistor:** Current limiting if ADC shorts

**BOM per input:**
- 2× 10kΩ resistors (1/4W)
- 1× 100nF ceramic capacitor (50V)
- 1× BAT85 Schottky diode
- Total cost: ~$0.50 per input

---

## ⚠️ What Voltage Range Are You Planning to Receive?

**This determines your protection needs:**

### Option 1: Only 0-5V Input (Most Eurorack)
**Protection needed:**
- 2× 10kΩ voltage divider ✅ Sufficient
- 100nF smoothing cap ✅ Recommended
- BAT85 clamp diode ⚪ Optional (nice-to-have)

### Option 2: Possible 0-10V Input (Some Modules)
**Protection needed:**
- Different divider ratio (3:1 instead of 2:1)
- Example: 20kΩ + 10kΩ (scales 10V → 3.3V)
- BAT85 clamp diode ✅ REQUIRED for safety margin

### Option 3: Unknown/Varied Voltage
**Protection needed:**
- Conservative divider ratio (3:1 or 4:1)
- BAT85 clamp diode ✅ REQUIRED
- Consider adding adjustable trimmer for calibration

---

## 🔧 Quick Reference - Resistor Values

**For different input voltage ranges:**

| Max Input | R1 (Series) | R2 (to GND) | Output to ADC | Status |
|-----------|-------------|-------------|---------------|--------|
| 5V | 10kΩ | 10kΩ | 2.5V | ✅ Safe |
| 8V | 15kΩ | 10kΩ | 3.2V | ✅ Safe (just under limit) |
| 10V | 20kΩ | 10kΩ | 3.3V | ⚠️ At limit (add diode!) |
| 10V | 10kΩ | 10kΩ | 5.0V | 💥 DAMAGE |

**Formula:**
```
Output Voltage = Input Voltage × (R2 / (R1 + R2))
```

---

## 📞 Immediate Action Required

**Please tell me:**

1. **Do you have resistors between input jacks and A3/A4 pins on your breadboard?**
   - YES → What values? (read color codes)
   - NO → STOP testing, we need to add them

2. **Have you connected any external CV sources to these inputs yet?**
   - YES → Did the M4 survive? (test ADC functionality)
   - NO → GOOD, don't connect until protected

3. **What voltage range will you be receiving?**
   - 0-5V only (most common)
   - Possibly 0-10V (some modules)
   - Unknown/varied

**Once I know this, I can give you exact parts and wiring instructions to make it safe!**

---

## 💡 Good News

**If you haven't connected external CV yet:**
- M4 is still safe
- Easy to add protection (5 minutes, $0.50 in parts)
- Will work perfectly once protected

**The 100Ω output resistors you already have:**
- Those protect the MCP4728 DAC outputs ✅
- Different circuit (output protection, not input)
- Already done correctly!

**Your S-Trig circuit:**
- Already safe ✅
- Uses GPIO output, not ADC input
- No voltage protection needed

---

**Bottom line: We just need to verify/add input protection on A3 and A4, then you're 100% safe!**
