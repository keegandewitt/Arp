# MIDI FeatherWing Pre-Flight Checklist

**Date:** 2025-10-22
**Purpose:** Systematic verification before connecting MIDI FeatherWing
**Philosophy:** "Measure twice, cut once"

---

## ✅ Verified Hardware Specifications

### MIDI FeatherWing
- [ ] **Product Number Confirmed:** #4740 (check physical board)
- [ ] **MIDI Jacks:** 2x DIN-5 jacks (IN and OUT)
- [ ] **LEDs:** 2x indicator LEDs (IN activity, OUT activity)
- [ ] **Connection Method:** Stacks on Feather headers
- [ ] **Isolation:** Optical isolator for 3.3V logic compatibility

### Feather M4 CAN Express
- [ ] **Model Confirmed:** Adafruit #4759
- [ ] **UART Pins Verified:**
  - TX = **D1** (board.TX, GPIO #1)
  - RX = **D0** (board.RX, GPIO #0)
- [ ] **CircuitPython Version:** 10.0.3 (verified via boot_out.txt)

---

## 📋 Pre-Stacking Physical Verification

### Current System State
- [ ] **M4 working:** Baseline test passed
- [ ] **OLED working:** Display shows clear text (SH1107 driver)
- [ ] **Buttons working:** All 3 buttons responsive
- [ ] **USB connection stable:** No brownouts or disconnects

### MIDI FeatherWing Physical Inspection
- [ ] **No bent header pins** on MIDI FeatherWing
- [ ] **No bent pins** on M4 female headers (where MIDI will stack)
- [ ] **MIDI jacks secure:** Not loose or damaged
- [ ] **Solder joints clean:** No bridges or cold joints visible
- [ ] **Board clean:** No debris or flux residue

---

## 🔧 Stacking Configuration Verified

### Planned Stack Order (Bottom to Top)
```
Layer 3: OLED FeatherWing (top) - buttons accessible
Layer 2: MIDI FeatherWing (middle) - jacks facing outward
Layer 1: Feather M4 CAN (bottom) - USB accessible
```

### Pin Conflict Check
- [ ] **UART pins:** RX(D0) and TX(D1) - Used by MIDI ✓
- [ ] **I2C pins:** SDA(D21) and SCL(D22) - Used by OLED ✓
- [ ] **Button pins:** D5, D6, D9 - Used by OLED ✓
- [ ] **NO CONFLICTS DETECTED**

**Critical:** MIDI uses hardware UART. Confirm no other code uses `board.TX` or `board.RX`.

---

## 📚 Library Verification

### Required Library
- **Name:** `adafruit_midi`
- **Latest Version:** 1.5.6 (October 2025)
- **CircuitPython Compatibility:** Works with CP 10.x (no known breaking changes)
- **Dependencies:** None (standalone library)

### Installation Command
```bash
circup install adafruit_midi
```

### Verify Installation
```bash
# Check if installed
ls /Volumes/CIRCUITPY/lib/ | grep midi

# Should see:
# adafruit_midi/
```

---

## 🧪 Test Plan

### Test 1: MIDI Output
**Goal:** Verify MIDI OUT jack sends data

**Test Script:** `tests/midi_output_test.py`

**Expected Results:**
- ✅ MIDI OUT LED blinks on FeatherWing
- ✅ Serial output shows "Sending Note ON: C4..."
- ✅ UART initializes without errors
- ✅ No crashes or freezes

**How to Verify:**
1. Watch MIDI OUT LED (should blink rhythmically)
2. Connect MIDI OUT to synth/device (optional, should hear notes)
3. Serial output shows clean messages

---

### Test 2: MIDI Input
**Goal:** Verify MIDI IN jack receives data

**Test Script:** `tests/midi_input_test.py`

**Required Hardware:** MIDI keyboard or controller

**Expected Results:**
- ✅ MIDI IN LED blinks when receiving
- ✅ Serial output shows "Note ON: Note #XX Velocity: XXX"
- ✅ All notes from keyboard detected
- ✅ No dropped messages

**How to Verify:**
1. Connect MIDI keyboard to MIDI IN jack
2. Play notes on keyboard
3. Watch MIDI IN LED blink
4. Serial output shows each note

---

### Test 3: MIDI Loopback
**Goal:** Verify both jacks work simultaneously

**Test Script:** `tests/midi_loopback_test.py`

**Required Hardware:** MIDI cable (DIN-5 to DIN-5)

**Setup:** Connect MIDI OUT jack to MIDI IN jack with cable

**Expected Results:**
- ✅ 100% of sent notes received back
- ✅ Both LEDs blink in sync
- ✅ No dropped messages
- ✅ Statistics show 100% success rate

---

### Test 4: Full System Integration
**Goal:** Verify M4 + OLED + MIDI all work together

**Test Script:** `tests/full_system_test.py`

**Expected Results:**
- ✅ OLED displays MIDI activity
- ✅ Button A sends test note
- ✅ MIDI IN/OUT indicators update on display
- ✅ System stable for 5+ minutes
- ✅ No memory errors or crashes

---

## 🚨 Known Gotchas & Common Issues

### Issue 1: UART Already in Use
**Symptom:** `ValueError: UART in use`

**Cause:** Another part of code using TX/RX pins

**Solution:**
- Check for serial debugging on UART
- Ensure only MIDI uses `board.TX` and `board.RX`
- USB serial is separate - it won't conflict

### Issue 2: Wrong Baud Rate
**Symptom:** Garbled MIDI or no communication

**Cause:** UART not at 31250 baud (MIDI standard)

**Critical Code:**
```python
uart = busio.UART(board.TX, board.RX, baudrate=31250)
```

**NOT 9600, NOT 115200 - MUST BE 31250!**

### Issue 3: MIDI IN LED Never Blinks
**Symptom:** No activity on MIDI IN

**Check:**
1. MIDI cable connected correctly (OUT → IN)
2. MIDI device sending on correct channel
3. Cable not damaged
4. FeatherWing fully seated on headers

### Issue 4: Both LEDs Blink Constantly
**Symptom:** LEDs stay lit or blink continuously

**Cause:** Possible UART feedback loop or noise

**Solution:**
- Disconnect MIDI cables
- Re-deploy test code
- Check for wiring shorts

---

## ✅ Pre-Flight Checklist Summary

Before stacking MIDI FeatherWing:

- [ ] MIDI FeatherWing product # verified (#4740)
- [ ] Physical inspection complete (no bent pins)
- [ ] Pin conflict check complete (no conflicts)
- [ ] M4 + OLED currently working
- [ ] Stack order planned (M4 → MIDI → OLED)
- [ ] Test scripts ready
- [ ] MIDI cable available (for loopback test)
- [ ] MIDI keyboard available (for input test, optional)

**If ALL boxes checked:** Ready to proceed with stacking!

---

## 📝 Assembly Steps (When Ready)

1. **Power off:** Disconnect USB from M4
2. **Remove OLED:** Gently pull OLED FeatherWing off M4
3. **Inspect pins:** Check M4 headers for bent pins
4. **Stack MIDI:**
   - Align MIDI FeatherWing headers with M4
   - MIDI jacks facing outward (same side as USB)
   - Press down firmly and evenly
   - Verify all pins seated
5. **Re-stack OLED:** Place OLED on top of MIDI
6. **Visual check:** Ensure stack is straight and aligned
7. **Power on:** Reconnect USB
8. **Verify mount:** Check `/Volumes/CIRCUITPY` appears
9. **Deploy test:** Start with `midi_output_test.py`

---

## 📊 Success Criteria

System is validated when:

✅ MIDI OUT test passes (LED blinks, notes send)
✅ MIDI IN test passes (LED blinks, notes receive)
✅ Loopback test passes (100% success rate)
✅ Full system test passes (OLED + MIDI integrated)
✅ No errors in serial output
✅ System stable for 5+ minutes

**After validation:** Ready for actual arpeggiator application!

---

**Version:** 1.0
**Last Updated:** 2025-10-22
**Status:** Ready for hardware stacking
