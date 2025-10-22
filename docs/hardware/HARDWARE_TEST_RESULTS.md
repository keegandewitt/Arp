# Hardware Test Results Log

**Board:** Adafruit Feather M4 CAN Express
**Serial Number:** _(from sticker or system_profiler)_
**Test Date:** _(YYYY-MM-DD)_
**Tested By:** _(Your name)_
**Test Script Version:** comprehensive_pin_test.py v1.0

---

## Purpose

This document records the results of comprehensive pin testing to validate:
- Soldering quality and connections
- Hardware functionality
- Pin integrity before project integration

Following our methodology: **Test EVERYTHING, not just what we're using.**

---

## Test Environment

- **USB Connection:** Yes / No
- **Battery Connected:** Yes / No
- **External Power:** Yes / No
- **Test Equipment:**
  - [ ] Multimeter (for voltage verification)
  - [ ] Oscilloscope (optional)
  - [ ] Jumper wire (for loopback tests)

---

## Section 1: Power Pins (Manual Verification)

| Pin | Expected | Measured | Pass/Fail | Notes |
|-----|----------|----------|-----------|-------|
| 3V  | ~3.3V    | _____ V  | ⬜ Pass ⬜ Fail | |
| BAT | 3.0-4.2V | _____ V  | ⬜ Pass ⬜ Fail | Battery or USB |
| USB | ~5.0V    | _____ V  | ⬜ Pass ⬜ Fail | When USB connected |
| GND | 0V       | _____ V  | ⬜ Pass ⬜ Fail | |

---

## Section 2: GPIO Pins (Digital I/O)

Copy results from serial monitor:

```
[Paste test output here]
```

### Individual Pin Results

| Pin | Function | Pass/Fail | Notes |
|-----|----------|-----------|-------|
| D0  | RX       | ⬜ Pass ⬜ Fail | |
| D1  | TX       | ⬜ Pass ⬜ Fail | |
| D4  | GPIO     | ⬜ Pass ⬜ Fail | |
| D5  | GPIO     | ⬜ Pass ⬜ Fail | |
| D6  | GPIO     | ⬜ Pass ⬜ Fail | |
| D9  | GPIO     | ⬜ Pass ⬜ Fail | |
| D10 | GPIO     | ⬜ Pass ⬜ Fail | |
| D11 | GPIO     | ⬜ Pass ⬜ Fail | |
| D12 | GPIO     | ⬜ Pass ⬜ Fail | |
| D13 | LED      | ⬜ Pass ⬜ Fail | |

---

## Section 3: I2C Pins

| Test | Pass/Fail | Notes |
|------|-----------|-------|
| D21 (SDA) GPIO | ⬜ Pass ⬜ Fail | |
| D22 (SCL) GPIO | ⬜ Pass ⬜ Fail | |
| I2C Bus Init   | ⬜ Pass ⬜ Fail | |

---

## Section 4: SPI Pins

| Test | Pass/Fail | Notes |
|------|-----------|-------|
| D23 (MISO) GPIO | ⬜ Pass ⬜ Fail | |
| D24 (MOSI) GPIO | ⬜ Pass ⬜ Fail | |
| D25 (SCK) GPIO  | ⬜ Pass ⬜ Fail | |
| SPI Bus Init    | ⬜ Pass ⬜ Fail | |

---

## Section 5: Analog Input Pins

| Pin | Voltage Read | Pass/Fail | Notes |
|-----|--------------|-----------|-------|
| A0  | _____ V      | ⬜ Pass ⬜ Fail | |
| A1  | _____ V      | ⬜ Pass ⬜ Fail | |
| A2  | _____ V      | ⬜ Pass ⬜ Fail | |
| A3  | _____ V      | ⬜ Pass ⬜ Fail | |
| A4  | _____ V      | ⬜ Pass ⬜ Fail | |
| A5  | _____ V      | ⬜ Pass ⬜ Fail | |

---

## Section 6: DAC Output Pins (Analog Output)

| Pin | Pass/Fail | Multimeter Verification |
|-----|-----------|-------------------------|
| A0  | ⬜ Pass ⬜ Fail | 0V: _____ V, 1.65V: _____ V, 3.3V: _____ V |
| A1  | ⬜ Pass ⬜ Fail | 0V: _____ V, 1.65V: _____ V, 3.3V: _____ V |

---

## Section 7: PWM Capability

| Pin | Pass/Fail | Notes |
|-----|-----------|-------|
| D0  | ⬜ Pass ⬜ Fail | |
| D1  | ⬜ Pass ⬜ Fail | |
| D4  | ⬜ Pass ⬜ Fail | |
| D5  | ⬜ Pass ⬜ Fail | |
| D6  | ⬜ Pass ⬜ Fail | |
| D9  | ⬜ Pass ⬜ Fail | |
| D10 | ⬜ Pass ⬜ Fail | |
| D11 | ⬜ Pass ⬜ Fail | |
| D12 | ⬜ Pass ⬜ Fail | |
| D13 | ⬜ Pass ⬜ Fail | |
| D21 (SDA) | ⬜ Pass ⬜ Fail | |
| D22 (SCL) | ⬜ Pass ⬜ Fail | |

---

## Section 8: Special Functions

| Test | Pass/Fail | Visual Confirmation |
|------|-----------|---------------------|
| NeoPixel LED | ⬜ Pass ⬜ Fail | Did you see Red, Green, Blue? |
| Onboard Red LED (D13) | ⬜ Pass ⬜ Fail | Did you see it blink 3 times? |

---

## Section 9: UART Loopback (Optional)

**Jumper connected D0 to D1?** ⬜ Yes ⬜ No ⬜ Skipped

| Test | Pass/Fail | Notes |
|------|-----------|-------|
| UART Loopback | ⬜ Pass ⬜ Fail | |

---

## Test Summary

```
[Paste test summary from serial monitor]

Total Tests: _____
Passed: _____
Failed: _____
Success Rate: _____%
```

---

## Failed Tests Analysis

If any tests failed, document investigation here:

### Pin: _______
- **Failure Mode:** _(e.g., pull-up not working, no PWM, etc.)_
- **Voltage Measurements:** _____
- **Continuity Check:** ⬜ Pass ⬜ Fail
- **Visual Inspection:** _(cold solder joint, bridge, damaged pad, etc.)_
- **Resolution:** _(reflow solder, replace component, etc.)_
- **Retest Result:** ⬜ Pass ⬜ Fail

---

## Photos/Documentation

Attach photos of:
- [ ] Assembled board (top view)
- [ ] Assembled board (bottom view - solder joints)
- [ ] Any problem areas or failed pins
- [ ] Multimeter readings for critical pins
- [ ] Serial monitor output (screenshot)

---

## Final Validation

- [ ] All critical pins tested and passed
- [ ] All power rails verified with multimeter
- [ ] No shorts detected between pins
- [ ] No cold solder joints observed
- [ ] Board ready for project integration

**Final Status:** ⬜ PASSED - Ready for Use  |  ⬜ FAILED - Rework Required

**Notes:**
_________________________________
_________________________________
_________________________________

---

## Sign-Off

**Tested By:** ___________________
**Date:** ___________________
**Signature:** ___________________

---

## Revision History

- **v1.0** (2025-10-22) - Initial test results template
  - Comprehensive pin testing coverage
  - Follows rigorous validation methodology
  - Includes failure analysis section
