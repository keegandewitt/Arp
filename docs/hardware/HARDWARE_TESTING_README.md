# Comprehensive Hardware Testing Guide

## Overview

This guide explains how to perform rigorous, comprehensive hardware validation on your Feather M4 CAN Express board.

**Philosophy:** Test EVERYTHING, not just what you're using. This approach:
- Validates soldering quality
- Catches manufacturing defects early
- Builds confidence in hardware reliability
- Creates baseline for troubleshooting future issues
- Documents complete hardware capabilities

---

## What You'll Need

### Required
- Feather M4 CAN Express (the board you're testing)
- USB-C cable
- Computer with CircuitPython serial monitor

### Recommended
- Multimeter (for voltage verification)
- Magnifying glass or macro lens (for solder joint inspection)
- Good lighting

### Optional
- Jumper wire (for UART loopback test)
- Oscilloscope (for advanced signal verification)

---

## Testing Process

### Step 1: Prepare the Board

1. **Visual Inspection**
   - Inspect all solder joints under magnification
   - Look for:
     - Cold solder joints (dull, grainy appearance)
     - Solder bridges between pins
     - Damaged pads or traces
     - Missing components

2. **Continuity Check** (with multimeter)
   - Check that adjacent pins are NOT shorted together
   - Verify GND pins are connected to ground
   - Verify 3V pins are connected to 3.3V rail

### Step 2: Load the Test Script

1. **Connect the board via USB**
   ```bash
   # Check that board is detected
   ls /dev/cu.usbmodem*
   ```

2. **Mount the CIRCUITPY drive**
   - Board should appear as a USB drive named `CIRCUITPY`
   - If not, double-tap the reset button to enter bootloader mode

3. **Backup existing code** (if any)
   ```bash
   # If you have existing code on the board
   cp /Volumes/CIRCUITPY/code.py /Volumes/CIRCUITPY/code.py.backup
   ```

4. **Copy test script to board**
   ```bash
   cp comprehensive_pin_test.py /Volumes/CIRCUITPY/code.py
   ```

5. **The board will automatically reset and start running the test**

### Step 3: Monitor the Test

1. **Open serial monitor**

   **Option A: Using `screen` (built into macOS/Linux)**
   ```bash
   screen /dev/cu.usbmodem1143101 115200
   ```
   - Press `Ctrl+A` then `K` to exit
   - Or press `Ctrl+A` then `D` to detach (keeps running)

   **Option B: Using Mu Editor**
   - Open Mu Editor (recommended for beginners)
   - Click "Serial" button
   - Watch the output

   **Option C: Using `tio`** (if installed)
   ```bash
   tio /dev/cu.usbmodem1143101
   ```

2. **Watch the test progress**
   - Tests run automatically
   - Each pin is tested systematically
   - Results are displayed in real-time

### Step 4: Document Results

1. **Copy the output**
   - Save all serial monitor output to a text file
   - Or take screenshots of the results

2. **Fill out the test results template**
   - Open `HARDWARE_TEST_RESULTS.md`
   - Make a copy for your specific board:
     ```bash
     cp HARDWARE_TEST_RESULTS.md HARDWARE_TEST_RESULTS_$(date +%Y%m%d).md
     ```
   - Fill in all sections with your test results

3. **Perform manual tests**
   - Use multimeter to verify power pins (3V, BAT, USB, GND)
   - Record measured voltages in the test results document

4. **Optional: UART Loopback Test**
   - Connect a jumper wire from D0 (RX) to D1 (TX)
   - Reset the board to re-run the test
   - The UART loopback test should now pass

### Step 5: Analyze Results

#### If All Tests Pass ✓
Congratulations! Your hardware is fully validated and ready for use.

#### If Any Tests Fail ✗

**DO NOT PROCEED** until failures are investigated and resolved.

1. **Note which pins failed**
   - GPIO failures: Check solder joints, look for bridges
   - Analog failures: Check reference voltage, power rails
   - PWM failures: Check solder quality, test adjacent pins
   - Communication bus failures: Check SCL/SDA or MISO/MOSI/SCK

2. **Visual re-inspection**
   - Use magnifying glass to examine failed pins
   - Look for cold solder joints, bridges, or damaged pads

3. **Electrical testing**
   - Use multimeter in continuity mode
   - Check pin-to-pad connection
   - Check for shorts to adjacent pins or ground

4. **Rework if needed**
   - Reflow cold solder joints
   - Remove solder bridges with desoldering braid
   - Replace damaged components

5. **Retest**
   - After rework, run the test again
   - Document the rework and retest results

### Step 6: Restore Original Code

Once testing is complete and all tests pass:

```bash
# Option 1: Restore backup (if you had existing code)
cp /Volumes/CIRCUITPY/code.py.backup /Volumes/CIRCUITPY/code.py

# Option 2: Install your project code
cp code.py /Volumes/CIRCUITPY/code.py
```

---

## Understanding Test Results

### GPIO Test
- **What it tests:** Digital input/output, pull-up/pull-down resistors
- **Pass criteria:** Pin can toggle high/low, pull-up reads high, pull-down reads low
- **Common failures:**
  - Cold solder joint: Cannot toggle
  - Damaged GPIO: Stuck high or stuck low
  - Pull resistor issue: Both read same value

### Analog Test
- **What it tests:** ADC (analog-to-digital converter) on pins A0-A5
- **Pass criteria:** Can read voltage between 0-3.3V
- **Common failures:**
  - Open circuit: Reads extremely noisy value
  - Short to ground: Always reads ~0V
  - Short to 3V: Always reads ~3.3V

### DAC Test
- **What it tests:** True analog output on A0 and A1
- **Pass criteria:** Can generate 0V, 1.65V, and 3.3V outputs
- **Verification:** Use multimeter to measure voltage on A0/A1 during test
- **Common failures:**
  - No output: Solder joint issue
  - Wrong voltage: Reference voltage problem

### PWM Test
- **What it tests:** Pulse width modulation capability
- **Pass criteria:** Can generate PWM signal at 1kHz
- **Common failures:**
  - GPIO passes but PWM fails: Timer conflict or damaged PWM hardware

### I2C/SPI Test
- **What it tests:** Communication bus initialization
- **Pass criteria:** Bus can be initialized without errors
- **Verification:** Run I2C scan or SPI transfer with actual devices
- **Common failures:**
  - Bus init fails: Check pull-up resistors (for I2C), check pin connections

### UART Test
- **What it tests:** Serial communication with loopback
- **Pass criteria:** Data sent on TX is received on RX
- **Note:** Requires jumper wire from D0 to D1
- **Common failures:**
  - Fails without jumper: Normal (expected)
  - Fails with jumper: Check jumper connection, check GPIO functionality

### Special Functions
- **NeoPixel:** RGB LED should cycle through red, green, blue
- **Onboard LED:** Red LED on D13 should blink 3 times
- **Visual confirmation required:** You must see these with your eyes

---

## Troubleshooting

### Board Not Detected
```bash
# Check USB connection
system_profiler SPUSBDataType | grep -A 10 "Feather"

# Try different USB cable (some cables are charge-only)
# Try different USB port
# Double-tap reset button to enter bootloader
```

### Serial Monitor Shows Nothing
- Ensure baud rate is set correctly (115200)
- Try unplugging and replugging USB
- Press Ctrl+C in serial monitor, then Ctrl+D to soft reboot

### Test Crashes or Hangs
- Press Ctrl+C to interrupt
- Check for hardware shorts (especially power pins)
- Reset board and try again

### Some Pins Pass, Some Fail
- This is normal for assembly defects
- Follow failure analysis procedure above
- Focus on failed pins first

### All Pins Fail
- Check power supply (is 3V rail at 3.3V?)
- Check GND connections
- May indicate board is not functioning at all

---

## Advanced Testing (Optional)

### Oscilloscope Verification

If you have an oscilloscope, you can verify:

1. **PWM signals**
   - Connect scope probe to any PWM-capable pin during PWM test
   - Should see 1kHz square wave with 50% duty cycle

2. **I2C signals**
   - Connect to SDA/SCL
   - Should see clock on SCL, data on SDA during I2C init

3. **DAC output**
   - Connect to A0 or A1
   - Should see clean voltage steps: 0V → 1.65V → 3.3V → 0V

### Load Testing

After basic pin testing passes:

1. **Current draw test**
   - Measure current at USB or BAT pin
   - Idle current should be 20-40mA (approximate)
   - Running full project should be <150mA

2. **Thermal testing**
   - Run for 30 minutes
   - Check for hot spots (especially voltage regulator)
   - Nothing should exceed ~50°C in normal operation

---

## Test Results Archive

Keep completed test results in this directory:

```
/
├── HARDWARE_TEST_RESULTS_20251022.md  <- Your filled-out test log
├── HARDWARE_TEST_RESULTS_20251023.md  <- After rework (if needed)
└── test_photos/
    ├── board_top.jpg
    ├── board_bottom.jpg
    └── failed_pin_closeup.jpg
```

---

## References

- [Feather M4 CAN Pinout](https://learn.adafruit.com/adafruit-feather-m4-can-express/pinouts)
- [CircuitPython Basics](https://learn.adafruit.com/welcome-to-circuitpython)
- [Adafruit Soldering Tutorial](https://learn.adafruit.com/adafruit-guide-excellent-soldering)
- Project Methodology: `METHODOLOGY.md` - Section "Rigorous Hardware Validation Philosophy"

---

## Questions or Issues?

If you encounter problems not covered in this guide:

1. Check the project `METHODOLOGY.md` for troubleshooting procedures
2. Review Adafruit's learning guides for your specific board
3. Document the issue thoroughly with photos and error messages
4. Open an issue on the project repository (if applicable)

---

## Revision History

- **v1.0** (2025-10-22) - Initial hardware testing guide
  - Comprehensive testing procedure
  - Troubleshooting section
  - Advanced testing methods
  - Follows rigorous validation methodology
