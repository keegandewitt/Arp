# Session 11 Handoff Summary

**Date:** 2025-10-31
**Duration:** Extended troubleshooting and architecture redesign
**Status:** Ready for hardware verification testing

---

## Session Overview

This session focused on recovering from hardware failures caused by a reversed LM7805 voltage regulator (which sent 12V to the 5V rail), and establishing a robust I2C architecture for multiple devices.

---

## Hardware Status

### Damaged Components (Replaced)
1. **Original Feather M4 CAN** - Overheating and crash-looping after 12V exposure
2. **Original OLED FeatherWing** - Static display and power-dip crashes after 12V exposure
3. **Original MCP4728 DAC** (potentially) - Exhibited strange behavior, replaced with new unit

### Working Components
1. **New Feather M4 CAN** - Running CircuitPython 10.0.3, stable
2. **New OLED FeatherWing** - 128x64 SH1107 display, tested and working
3. **New MCP4728 DAC** - 4-channel 12-bit DAC, I2C communication verified
4. **LM7805 Voltage Regulator** - Now correctly installed (plastic side toward user, metal away)
5. **Powerboost 1000C** - Providing 12V rail
6. **TL072 Op-Amp** - Circuit wired, awaiting final verification

---

## Key Achievements

### 1. I2C Architecture Documentation
Created comprehensive I2C management guide: `docs/hardware/I2C_ARCHITECTURE.md`

**Key Principles:**
- Use `board.I2C()` singleton instead of `busio.I2C()` to prevent conflicts
- Initialize with proper sequence: `displayio.release_displays()` → `board.I2C()` → devices
- Call `dac.wakeup()` to clear power-down mode on MCP4728
- Configure MCP4728 with `Vref.VDD` for 5V reference voltage

### 2. MCP4728 Configuration Discovery
Found critical MCP4728 power-down issue:
- MCP4728 can enter power-down mode (outputs disabled)
- Must call `mcp.wakeup()` after initialization
- Must set `vref = adafruit_mcp4728.Vref.VDD` to use external 5V reference
- Configuration persists to EEPROM with `mcp.save_settings()`

### 3. Hardware Verification Tests
Multiple diagnostic tests created in `tests/` directory for isolated component verification.

---

## Current System State

### Hardware Connections
```
Feather M4 CAN (New)
├── USB-C: Computer (power + programming)
├── Stacked: OLED FeatherWing (New)
├── I2C (STEMMA QT): MCP4728 DAC (New)
│   └── VDD: 5V from LM7805
│   └── GND: Common ground
└── Breadboard: TL072 op-amp circuit

Power Rails:
├── 12V: Powerboost → TL072 Pin 8
├── 5V: LM7805 output → MCP4728 VDD
└── GND: Common ground (all components)
```

### Software State
**Current code.py on CIRCUITPY:**
```python
# MCP4728 + OLED Test - Proper I2C Architecture
# Uses board.I2C() singleton
# Includes dac.wakeup() and Vref.VDD configuration
# Button B cycles through 0V, 1V, 2V, 3V, 4V, 5V on Channel A
```

**Libraries Installed:**
- `adafruit_mcp4728` - DAC control
- `adafruit_displayio_sh1107` - OLED display
- `adafruit_display_text` - Text rendering
- `i2cdisplaybus` - Display bus interface

---

## Outstanding Issues

### Critical: MCP4728 Voltage Output Verification
**Status:** Code ready, hardware testing incomplete

**Last Known Readings (Pre-Session End):**
- VDD pin: 4.93V ✓ (correct)
- VA output: 0.03-0.31V ✗ (should be 0-5V range)

**Possible Causes:**
1. Power-down mode still active (wakeup() may need hardware reset to take effect)
2. MCP4728 damaged from 12V exposure
3. Configuration not properly saved to EEPROM
4. Hardware connection issue (VA pin to ground short?)

**Next Steps:**
1. **Power cycle the M4** (unplug USB, wait 5 seconds, plug back in)
2. Run current `code.py` test
3. Press Button B to cycle through voltage steps
4. Measure VA pin with multimeter for each step:
   - Step 1: Should read ~0.00V
   - Step 2: Should read ~1.00V
   - Step 3: Should read ~2.00V
   - Step 4: Should read ~3.00V
   - Step 5: Should read ~4.00V
   - Step 6: Should read ~4.93V (VDD level)

5. **If readings are still wrong:**
   - Try another new MCP4728 (may be damaged)
   - Check for shorts between VA and GND
   - Verify VDD is actually 5V during measurement

---

## File Structure Changes

### New Documentation
```
docs/hardware/I2C_ARCHITECTURE.md  - Comprehensive I2C guide
docs/SESSION_11_HANDOFF.md          - This file
```

### Test Files (64 total in tests/)
Key diagnostic tests:
- `tests/i2c_debug_scan.py` - I2C device scanner with LED feedback
- `tests/mcp4728_simple_test.py` - MCP4728 configuration test
- `tests/oled_heartbeat_simple.py` - OLED verification
- `tests/led_only_test.py` - Bare M4 verification

### Temporary Files (Can Delete)
```
/tmp/safe_code.py
/tmp/minimal_safe.py
```

---

## I2C Device Map

| Address | Device | Status | Purpose |
|---------|--------|--------|---------|
| 0x3C | OLED FeatherWing (SH1107) | ✓ Working | 128x64 display |
| 0x60 | MCP4728 DAC | ⚠ Needs verification | 4-channel CV output |
| 0x4D | MIDI FeatherWing | Not yet installed | UART MIDI interface |

---

## Code Architecture Pattern

### Initialization Template
```python
import board
import displayio
import time

# 1. Release previous displays
displayio.release_displays()
time.sleep(0.2)

# 2. Get shared I2C bus (singleton)
i2c = board.I2C()

# 3. Initialize devices
display = init_display(i2c)
dac = init_dac(i2c)

# 4. Configure DAC
dac.wakeup()
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
dac.channel_a.gain = 1
dac.save_settings()

# 5. Main loop (no I2C re-initialization)
while True:
    # Use devices
    pass
```

---

## Next Session Goals

### Immediate (Session 12)
1. **Verify MCP4728 voltage outputs** - Critical blocker
2. If MCP4728 works: **Test TL072 2× gain circuit** (0-5V → 0-10V)
3. If MCP4728 fails: **Replace with another new unit** and retest

### Short Term
1. Integrate MIDI FeatherWing
2. Build complete arpeggiator test with all components
3. Design and order PCB for permanent installation

### Future
1. Migration to new M4 (better specs)
2. Battery integration
3. Back panel LEDs for MIDI activity
4. Startup error check protocol

---

## References Created This Session

### Documentation
- **I2C_ARCHITECTURE.md** - Essential reading for all future I2C work
  - Singleton pattern with `board.I2C()`
  - Device initialization order
  - Common errors and solutions
  - Testing procedures

### Code Patterns
- **Proper I2C initialization** - See `code.py` lines 23-49
- **MCP4728 configuration** - See `code.py` lines 38-49
- **Button-based testing** - See `code.py` lines 70-95

---

## Important Notes

### Do NOT Do These Things
1. ❌ Create multiple I2C buses (`busio.I2C()` repeatedly)
2. ❌ Skip `displayio.release_displays()` before initializing display
3. ❌ Forget `dac.wakeup()` after MCP4728 initialization
4. ❌ Use internal 2.048V reference (always use `Vref.VDD` for 5V)
5. ❌ Install LM7805 backwards (plastic side faces you, metal away)

### Always Do These Things
1. ✓ Use `board.I2C()` singleton for shared bus
2. ✓ Call `dac.wakeup()` on MCP4728 after init
3. ✓ Set `Vref.VDD` for 5V reference
4. ✓ Call `save_settings()` to persist configuration
5. ✓ Test each component in isolation before integration

---

## Session Lessons Learned

### Hardware
1. **LM7805 orientation is critical** - Reversed regulator sends 12V to 5V rail
2. **12V exposure damages components** - Killed M4, OLED, possibly MCP4728
3. **New components may arrive in power-down mode** - Always call `wakeup()`
4. **Power-dip safe mode is sticky** - Requires hardware reset, not soft reboot

### Software
1. **I2C conflicts cause hard faults** - Use singleton pattern religiously
2. **Device libraries handle locking** - Don't manually lock/unlock with libraries
3. **MCP4728 configuration is complex** - Reference voltage, gain, and power-down modes
4. **CircuitPython reference docs are incomplete** - Need to combine docs + datasheet + experimentation

### Debugging
1. **Isolate components** - Test each device separately before integration
2. **Serial monitor is unreliable** - Use LED patterns and OLED display
3. **Safe mode messages are cryptic** - "Power dip" can mean hardware damage
4. **Physical verification is essential** - Software says one thing, multimeter says another

---

## Handoff Checklist

- [x] Document I2C architecture
- [x] Create proper initialization code
- [x] Test OLED independently (working)
- [x] Test MCP4728 I2C communication (working)
- [ ] **Verify MCP4728 voltage outputs (0-5V range)** ← **CRITICAL BLOCKER**
- [ ] Test TL072 op-amp circuit (2× gain)
- [ ] Update CONTEXT.md with session summary
- [ ] Clean up unnecessary test files

---

## Quick Start for Next Session

1. **Power on system** - Unplug/replug M4 USB to ensure clean boot
2. **Check OLED** - Should show "MCP4728 Test" with "Ready! Press B"
3. **Test MCP4728:**
   ```
   Press Button B → OLED shows "Step 1/6 VA: 0V"
   Measure VA pin with multimeter
   Press B again → "Step 2/6 VA: 1V"
   Measure VA pin (should be ~1V)
   Continue through all 6 steps
   ```
4. **If voltages correct:** Proceed to TL072 testing
5. **If voltages wrong:** Replace MCP4728 or debug hardware connections

---

**End of Session 11 Handoff**
