# Arp Hardware Assembly & Testing Protocol

**Version:** 1.0
**Date:** 2025-10-22
**Purpose:** Step-by-step protocol for assembling and validating an Arp unit

---

## ⚠️ CRITICAL: Follow This Order Exactly

This protocol ensures each component works before adding the next layer. **Do not skip steps.**

---

## Pre-Assembly Checklist

Before starting, verify you have:

- [ ] Adafruit Feather M4 CAN Express (#4759)
- [ ] Adafruit OLED FeatherWing 128x64 (#4650)
- [ ] Adafruit MIDI FeatherWing (#4740)
- [ ] USB-C cable
- [ ] Computer with CircuitPython 10.0.3+ installed on M4
- [ ] MIDI keyboard or controller (for MIDI testing)
- [ ] MIDI cable (DIN-5 to DIN-5)

### Verify CircuitPython Installation

```bash
cat /Volumes/CIRCUITPY/boot_out.txt
```

Should show: `Adafruit CircuitPython 10.0.3` (or later)

---

## Stage 1: Bare M4 Baseline Test

**Goal:** Verify the Feather M4 works before adding anything.

### 1.1 Connect M4 to Computer

1. Connect Feather M4 to computer via USB-C
2. Verify `/Volumes/CIRCUITPY` mounts
3. Verify serial port appears (e.g., `/dev/tty.usbmodem*`)

### 1.2 Run M4 Baseline Test

```bash
# Deploy baseline test
cp tests/comprehensive_pin_test.py /Volumes/CIRCUITPY/code.py

# Monitor output
screen /dev/tty.usbmodem* 115200
```

**Expected Results:**
- ✅ All GPIO pins toggle successfully
- ✅ I2C bus initializes (SDA=D21, SCL=D22)
- ✅ UART initializes (RX=D0, TX=D1)
- ✅ DAC outputs functional (A0, A1)
- ✅ NeoPixel responds (if installed)

**If any fail:** STOP. Debug M4 before proceeding.

### 1.3 Baseline Checklist

- [ ] GPIO pins working
- [ ] I2C bus initialized
- [ ] UART initialized
- [ ] Power stable (no brownouts)
- [ ] Serial output clean

**✅ Stage 1 Complete - M4 Validated**

---

## Stage 2: Add OLED FeatherWing

**Goal:** Verify display works before adding MIDI.

### 2.1 Physical Assembly

**CRITICAL: Check hardware specs FIRST!**

1. **Verify OLED model:**
   - Product #4650 = 128x64 = **SH1107 driver**
   - Product #2900 = 128x32 = **SSD1306 driver**
   - **DO NOT ASSUME!** Check your actual product number.

2. Stack OLED FeatherWing onto M4:
   - Align headers carefully
   - Press firmly until fully seated
   - Verify no bent pins

### 2.2 Install Required Libraries

```bash
circup install adafruit_displayio_sh1107 adafruit_display_text
```

**For 128x32 version (if you have #2900):**
```bash
circup install adafruit_displayio_ssd1306 adafruit_display_text
```

### 2.3 Test OLED Display

```bash
# Deploy OLED test (for 128x64 SH1107)
cp tests/oled_sh1107_test.py /Volumes/CIRCUITPY/code.py
```

**Expected Results:**
- ✅ Display shows "IT WORKS!"
- ✅ Display shows "SH1107 Driver"
- ✅ Text is clear and readable (NOT garbled)
- ✅ Brightness adjustable

### 2.4 Test OLED Buttons

```bash
# Deploy button test
cp tests/button_clean_test.py /Volumes/CIRCUITPY/code.py
```

**Expected Results:**
- ✅ Button A (D9) responds to press
- ✅ Button B (D6) responds to press
- ✅ Button C (D5) responds to press
- ✅ Long press detected after 0.5 seconds
- ✅ Combinations detected (A+B, B+C, etc.)

### 2.5 OLED Stage Checklist

- [ ] Display shows clear text (not garbled)
- [ ] Correct driver installed (SH1107 or SSD1306)
- [ ] All 3 buttons responsive
- [ ] Long press detection working
- [ ] No I2C errors in serial output

**✅ Stage 2 Complete - OLED Validated**

---

## Stage 3: Add MIDI FeatherWing

**Goal:** Verify MIDI input and output.

### 3.1 Physical Assembly

**Stack order (bottom to top):**
1. Feather M4 CAN (bottom)
2. MIDI FeatherWing (middle)
3. OLED FeatherWing (top)

**Stacking MIDI FeatherWing:**
1. Remove OLED FeatherWing temporarily
2. Stack MIDI FeatherWing onto M4
   - Align headers carefully
   - MIDI jacks should face outward
   - Press firmly until seated
3. Re-stack OLED FeatherWing on top

**Pin Usage:**
- MIDI OUT → UART TX (D1)
- MIDI IN → UART RX (D0)
- Both are hardware serial pins

### 3.2 Install MIDI Library

```bash
circup install adafruit_midi
```

### 3.3 Test MIDI Output

```bash
# Deploy MIDI output test
cp tests/midi_output_test.py /Volumes/CIRCUITPY/code.py
```

**What it does:**
- Sends MIDI notes C, E, G (C major chord)
- Repeats every 2 seconds
- Shows MIDI OUT LED activity

**Expected Results:**
- ✅ MIDI OUT LED blinks on MIDI FeatherWing
- ✅ Connect to MIDI device and hear notes
- ✅ Serial output shows "Sending note X"

### 3.4 Test MIDI Input

```bash
# Deploy MIDI input test
cp tests/midi_input_test.py /Volumes/CIRCUITPY/code.py
```

**What it does:**
- Listens for MIDI notes
- Displays received notes on serial
- Shows MIDI IN LED activity

**Expected Results:**
- ✅ MIDI IN LED blinks when receiving
- ✅ Serial output shows received notes
- ✅ Note velocities displayed correctly

### 3.5 Test MIDI Loopback

Connect MIDI OUT to MIDI IN with a cable for loopback test:

```bash
# Deploy MIDI loopback test
cp tests/midi_loopback_test.py /Volumes/CIRCUITPY/code.py
```

**Expected Results:**
- ✅ Notes sent on MIDI OUT received on MIDI IN
- ✅ No dropped notes
- ✅ Timing stable

### 3.6 MIDI Stage Checklist

- [ ] MIDI OUT LED blinks when sending
- [ ] MIDI IN LED blinks when receiving
- [ ] External MIDI device receives notes
- [ ] Can receive notes from MIDI keyboard
- [ ] Loopback test passes
- [ ] No UART errors in serial output

**✅ Stage 3 Complete - MIDI Validated**

---

## Stage 4: Integrated System Test

**Goal:** Verify all components work together.

### 4.1 Deploy Integration Test

```bash
# Copy display.py to device
cp display.py /Volumes/CIRCUITPY/display.py

# Deploy integrated test
cp tests/full_system_test.py /Volumes/CIRCUITPY/code.py
```

**Expected Results:**
- ✅ OLED displays system status
- ✅ Buttons control test parameters
- ✅ MIDI notes send/receive correctly
- ✅ Display updates in real-time
- ✅ No crashes or freezes

### 4.2 Full System Checklist

- [ ] Display shows MIDI activity indicators
- [ ] Buttons change modes on display
- [ ] MIDI IN/OUT both functional
- [ ] System stable for 5+ minutes
- [ ] No memory errors
- [ ] Temperature normal (M4 not hot)

**✅ Stage 4 Complete - Full System Validated**

---

## Final Validation

### Hardware Validation Complete

- [ ] M4 baseline test passed
- [ ] OLED display working (correct driver)
- [ ] All 3 buttons responsive
- [ ] MIDI IN working
- [ ] MIDI OUT working
- [ ] Integrated system stable

### Documentation

Record in hardware log:
- Date assembled: _______________
- M4 serial number: _______________
- OLED product #: _______________ (4650 or 2900?)
- MIDI product #: 4740
- Test results: PASS / FAIL
- Notes: _______________

---

## Troubleshooting Guide

### Display Shows Garbled Output

**Problem:** Using wrong driver chip

**Solution:**
1. Check OLED product number
2. Product #4650 → Use SH1107 driver
3. Product #2900 → Use SSD1306 driver
4. Reinstall correct library: `circup install adafruit_displayio_sh1107`

### MIDI Not Sending/Receiving

**Problem:** UART pins conflict or not initialized

**Check:**
1. Verify MIDI FeatherWing stacked correctly
2. Check for bent pins on headers
3. Verify `busio.UART(board.TX, board.RX, baudrate=31250)`
4. Check serial output for UART errors

### Buttons Not Responding

**Problem:** Pull-up resistors not configured

**Solution:**
```python
button.pull = digitalio.Pull.UP
```

### I2C Device Not Found (Display)

**Problem:** OLED not seated or wrong address

**Check:**
1. Run I2C scan: `tests/i2c_scan_display.py`
2. Should see 0x3C (OLED)
3. Re-seat OLED FeatherWing
4. Check for bent pins

---

## Success Criteria

An Arp unit is considered **validated** when:

✅ All Stage 1-4 tests pass
✅ System runs stable for 10+ minutes
✅ No errors in serial output
✅ All LEDs respond correctly
✅ MIDI communication bidirectional
✅ Display and buttons responsive

**If all criteria met:** Unit ready for application code deployment!

---

## Next Steps After Validation

1. Deploy main application code (`code.py`, `arpeggiator.py`, etc.)
2. Test arpeggiator patterns
3. Configure settings via UI
4. Test with actual MIDI keyboard
5. Enjoy your working Arp! 🎹

---

**Protocol Version:** 1.0
**Last Updated:** 2025-10-22
**Verified On:** Feather M4 CAN + OLED #4650 + MIDI #4740
