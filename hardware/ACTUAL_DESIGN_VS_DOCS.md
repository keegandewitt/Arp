# ACTUAL DESIGN vs. DOCUMENTATION - Critical Review

**Date:** 2025-11-03 (Session 25)
**Purpose:** Identify what you ACTUALLY built vs. what's in the docs

---

## ✅ CONFIRMED - What You Actually Have

### Power Rails (CONFIRMED BY USER)
- **5V Rail:** From Feather M4 USB pin → MCP4728 DAC power
- **3.3V Rail:** From Feather M4 3V3 pin → MIDI FeatherWing + LEDs
- **Both rails need decoupling caps** (bulk + bypass on each board)

### CV/TRIG Outputs (FROM BREADBOARD DOCS)
- **CV OUT:** MCP4728 Channel A → 0-5V direct output
  - **No op-amp** (you eliminated it per Claude's advice)
  - **0-5V = 5 octaves at 1V/octave** (valid for Eurorack!)
  - **Works with:** Most Eurorack (limited to 5 octave range)

- **TRIG OUT:** MCP4728 Channel B (V-Trig) OR GPIO D10 via NPN (S-Trig)
  - **V-Trig:** 0-5V standard gate
  - **S-Trig:** Switch to GND (vintage gear)

### CV/TRIG Inputs (USER SAYS: "on breadboard")
- **CV IN → A3 ADC:** Direct? Or through voltage divider?
- **TRIG IN → A4 ADC:** Needs voltage divider (per user question)

**CRITICAL SAFETY:**
- M4 ADC max input: **3.3V**
- Eurorack can send: **0-5V or even 0-10V**
- **Without protection → you will destroy the M4!**

---

## ❌ DOCUMENTATION ERRORS - What Docs Say But You Don't Have

### 1. BAT85 Diode Clamps (USER: "Never heard of these")
**Docs say:**
```
CV IN → voltage divider → BAT85 diode → 3.3V clamp → A3 ADC
```

**Reality:**
- You have NO diodes on breadboard
- A previous Claude added this without your knowledge
- **Decision needed:** Keep the protection design, or remove it?

### 2. Op-Amp for 0-10V Output (USER: "Eliminated it")
**Docs say:**
```
MCP4728 0-5V → TL072 op-amp (2x gain) → 0-10V CV OUT
```

**Reality:**
- You eliminated the op-amp
- Direct 0-5V output from MCP4728
- **This is FINE!** 0-5V gives you 5 octaves (C0-C5) which is plenty

### 3. Missing Power Rail Documentation
**Docs show:**
- Only 5V rail with C1, C2
- Mentions "3.3V clamp references" but no actual 3.3V power caps

**Reality:**
- You definitely have 3.3V rail (MIDI + LEDs)
- Needs proper decoupling caps: C9, C10 (or C11, C12 depending on board)

---

## ⚠️ CRITICAL QUESTIONS TO RESOLVE

### Question 1: CV/TRIG Input Protection
**Current breadboard:** What do you ACTUALLY have right now?
- Option A: Direct CV IN jack → A3 ADC (DANGEROUS if Eurorack sends >3.3V)
- Option B: Voltage divider exists but no diodes
- Option C: Something else?

**Recommended:** Voltage divider (resistors) to scale incoming voltage to safe range
- Example: 5V input → voltage divider → 2.5V to ADC (safe!)

### Question 2: Do You Need 10V CV Output?
**Current:** 0-5V (5 octaves)
**Alternative:** Add op-amp back for 0-10V (10 octaves)

**Considerations:**
- 5 octaves is plenty for most use cases
- Most MIDI only spans ~5-7 octaves anyway
- Adding op-amp requires +12V power supply (more complexity)

**Recommendation:** **Keep 0-5V** unless you specifically need >5 octave range

### Question 3: Input Voltage Range
**What voltage will you receive on CV IN and TRIG IN jacks?**
- Eurorack standard: 0-5V (some modules go to 10V)
- Other modular: varies widely
- Need to know this to design protection circuit

---

## 🔧 RECOMMENDED FIXES

### Fix 1: Add Input Voltage Divider (CRITICAL FOR SAFETY)
**Purpose:** Scale 0-5V input → 0-3.3V safe for ADC

**Simple resistor divider:**
```
CV IN jack → 10kΩ → [tap point] → A3 ADC
                        ↓
                      10kΩ
                        ↓
                      GND

Math: 5V × (10k/(10k+10k)) = 2.5V (safe!)
```

**Add optional smoothing cap:**
- 100nF capacitor from tap point to GND
- Filters noise from long cables

### Fix 2: Document Actual Power Distribution
Create proper power section showing BOTH rails:

**TOP BOARD (Input):**
- 5V: C11 (10µF bulk) + C12 (0.1µF bypass)
- 3.3V: C13 (10µF bulk) + C14 (0.1µF bypass)

**BOTTOM BOARD (Output):**
- 5V: C1 (47µF bulk) + C2 (0.1µF bypass)
- 3.3V: C9 (10µF bulk) + C10 (0.1µF bypass)

### Fix 3: Remove BAT85 Diodes from Documentation
**They're not on your breadboard, so remove from schematics**

Unless you decide you want overvoltage protection (valid choice!), in which case:
- BAT85 cathode to 3.3V rail
- Clamps any voltage spike above ~3.9V
- Extra safety margin

---

## 📋 IMMEDIATE ACTION ITEMS

1. **USER: Tell me what's on your breadboard RIGHT NOW for CV/TRIG inputs**
   - Direct connection to ADC pins?
   - Any resistors?
   - Any capacitors?

2. **USER: What voltage range do you expect on CV IN and TRIG IN?**
   - Just 0-5V?
   - Possibly 0-10V?
   - Unknown/varied?

3. **USER: Are you happy with 5 octave range (0-5V CV OUT)?**
   - Yes → keep current design
   - No → need to add op-amp back + 12V power

4. **CLAUDE: Based on answers, create accurate schematics**
   - Remove fictional components (BAT85 if not wanted)
   - Add actual power distribution (both 5V and 3.3V)
   - Add actual input protection (if exists)

---

## 💡 MY RECOMMENDATION

**For CV/TRIG Inputs (Protection):**
- Add simple voltage divider: 10kΩ + 10kΩ (scales 5V → 2.5V)
- Add 100nF smoothing cap
- Skip BAT85 diodes (simple is better)

**For CV Output (Range):**
- Keep 0-5V (5 octaves is plenty)
- Eliminates need for 12V power supply
- Simpler, fewer components, lower cost

**For Documentation:**
- Fix power distribution to show BOTH 5V and 3.3V rails
- Remove BAT85 references (or mark as "optional future upgrade")
- Match schematics to what you actually built

---

**NEXT STEP:** Please answer the 3 critical questions above, then I'll create accurate documentation!
