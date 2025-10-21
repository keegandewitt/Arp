# Hardware Testing Guide

## Overview

Your MIDI Arpeggiator now has **built-in hardware tests** that run alongside the main application without interrupting it. Tests are triggered via serial commands while the arpeggiator is running.

## How to Access Tests

### 1. Connect to Serial Console

**macOS/Linux:**
```bash
screen /dev/tty.usbmodem* 115200
# Press Ctrl+A then K to exit
```

**Windows:**
- Use PuTTY, TeraTerm, or Arduino Serial Monitor
- Baud rate: 115200
- Port: COM port of your Feather

### 2. Type Test Commands

Once connected, simply type a command and press Enter:

```
test i2c
test oled
test dac
help
```

## Available Test Commands

| Command | Duration | Description |
|---------|----------|-------------|
| `test i2c` | 1s | Scan I2C bus, identify OLED (0x3C) and DAC (0x60) |
| `test oled` | 3s | Flash test message on display, verify brightness |
| `test buttons` | 10s | Press buttons A, B, C to verify functionality |
| `test midi` | 10s | Listen for MIDI input, echo received messages |
| `test dac` | 8s | Output test voltages (0V-5V) + 1V/octave test |
| `test all` | ~30s | Run all tests in sequence with summary |
| `help` | - | Show command list |

## Test Details

### `test i2c` - I2C Bus Scan

**Purpose:** Verify both I2C devices are connected and communicating

**Expected Output:**
```
Found 2 device(s):
  0x3C - OLED Display
  0x60 - MCP4728 DAC
✓ OLED found
✓ DAC found
```

**Troubleshooting:**
- ✗ OLED missing → Check FeatherWing is seated properly
- ⚠ DAC missing → Normal if DAC not yet installed

---

### `test oled` - OLED Display Test

**Purpose:** Verify display is working and responsive

**What Happens:**
1. Shows "Test OK!" message for 2 seconds
2. Flashes brightness 3 times
3. Returns to normal operation

**Expected:** See text on physical OLED display

**Troubleshooting:**
- No display → Check I2C connections (SCL/SDA)
- Dim display → Normal, brightness set to 0.5 (50%)

---

### `test buttons` - Button Test

**Purpose:** Verify all three OLED buttons are responding

**Instructions:**
1. Type `test buttons` and press Enter
2. Press Button A (left)
3. Press Button B (center)
4. Press Button C (right)
5. Test completes after 10 seconds or when all buttons pressed

**Expected Output:**
```
Press buttons A, B, C within 10 seconds...
  ✓ Button A
  ✓ Button B
  ✓ Button C
✓ All buttons working!
```

**Troubleshooting:**
- Button not responding → Check pins D9, D6, D5 connections
- False presses → Check for loose connections

---

### `test midi` - MIDI Input/Output Test

**Purpose:** Verify MIDI FeatherWing is receiving data

**Requirements:**
- MIDI device connected to MIDI IN
- Device actively sending MIDI data

**Instructions:**
1. Connect MIDI keyboard/controller to MIDI IN
2. Type `test midi` and press Enter
3. Play notes or move controls within 10 seconds

**Expected Output:**
```
Play MIDI notes within 10 seconds...
  MIDI IN: Note 60 ON (vel=100)
  MIDI IN: Note 60 OFF
  MIDI IN: Note 62 ON (vel=95)
✓ Received 4 MIDI messages
```

**Troubleshooting:**
- ⚠ No MIDI messages → Check MIDI cable and device is powered
- No output → Check TX/RX pin connections (board.TX, board.RX)

---

### `test dac` - MCP4728 DAC Test

**Purpose:** Verify DAC is outputting CV correctly

**What Happens:**
1. Cycles all channels through: 0V → 1.25V → 2.5V → 3.75V → 5V
2. Tests 1V/octave conversion: C1=1V, C2=2V, C3=3V, C4=4V
3. Resets all channels to 0V

**Equipment Needed:**
- Multimeter to verify voltages on CV outputs

**Expected:** Voltages match displayed values (±0.1V)

**Troubleshooting:**
- ✗ DAC not found → Check I2C connection
- Max voltage 3.3V instead of 5V → DAC powered by 3.3V instead of 5V boost
- No voltage output → Check VCC connection to Teyleten boost 5V output

---

### `test all` - Full Test Suite

**Purpose:** Run all tests in sequence to verify complete system

**Duration:** ~30 seconds

**Output:** Summary showing pass/fail for each component

**Expected:**
```
TEST SUMMARY
  ✓ PASS - I2C Scan
  ✓ PASS - OLED Display
  ✓ PASS - Buttons
  ✓ PASS - MIDI I/O
  ✓ PASS - DAC

Total: 5/5 tests passed
```

---

## Testing Workflow

### Initial Hardware Bring-Up

When assembling the enclosure for the first time:

```bash
1. Power on device
2. Connect to serial console
3. Type: test all
4. Verify all tests pass
```

### Adding New Component (e.g., DAC)

When adding the MCP4728 DAC:

```bash
1. Connect DAC to I2C (SCL/SDA) and 5V power
2. Type: test i2c         # Verify DAC appears at 0x60
3. Type: test dac         # Verify CV outputs work
4. Use multimeter to check voltages
```

### Troubleshooting Connection Issues

If something stops working:

```bash
1. Type: test i2c         # Check what devices are visible
2. Type: test [component] # Test specific component
3. Check physical connections based on output
```

---

## Integration with Main Code

The test system is **non-invasive**:

- ✓ Tests run in the main loop (no separate mode)
- ✓ Arpeggiator continues operating
- ✓ MIDI processing not interrupted
- ✓ Tests complete quickly (1-10 seconds each)
- ✓ Hardware resources properly cleaned up after tests

**Note:** Some tests (buttons, MIDI) briefly pause the main loop during their 10-second windows. MIDI messages during this time may be captured by the test instead of the arpeggiator.

---

## Files

- **`test_commands.py`** - Test function implementations
- **`code.py`** - Main application (imports and calls tests)
- **`hardware_tests.py`** - Standalone test suite (legacy, for reference)

---

## Quick Reference Card

Print this and keep near your workstation:

```
╔════════════════════════════════════════╗
║   MIDI ARPEGGIATOR TEST COMMANDS      ║
╠════════════════════════════════════════╣
║                                        ║
║  test i2c      → I2C bus scan          ║
║  test oled     → Display test          ║
║  test buttons  → Button test (10s)     ║
║  test midi     → MIDI I/O test (10s)   ║
║  test dac      → CV output test        ║
║  test all      → Run all tests         ║
║  help          → Show commands         ║
║                                        ║
║  Serial: 115200 baud                   ║
║  macOS: screen /dev/tty.usbmodem* ...  ║
║                                        ║
╚════════════════════════════════════════╝
```

---

## Advanced: Custom Tests

To add your own tests, edit `test_commands.py`:

```python
def test_my_feature():
    """Test description"""
    print("Testing my feature...")
    # Your test code here
    return True  # or False if failed
```

Then add to `code.py` in `check_serial_commands()`:

```python
elif command == "test myfeature":
    test_my_feature()
    return True
```

---

## Tips

1. **Keep serial console open** during assembly for instant testing
2. **Run `test all` after any hardware change** to catch issues early
3. **Use `test i2c` frequently** - quick sanity check for connections
4. **Test DAC with multimeter** - visual confirmation prevents mistakes
5. **Document test results** if troubleshooting intermittent issues

---

**Happy Testing!** 🎛️🎹
