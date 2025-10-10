# Installation Guide - CircuitPython MIDI Arpeggiator

This guide will walk you through setting up your M4 Express board with all required libraries for the MIDI Arpeggiator.

## Prerequisites

### Hardware Required
- Adafruit M4 Express board (Feather M4, Metro M4, or compatible)
- 2× Adafruit MIDI FeatherWings (for MIDI I/O and Clock input)
- 1× Adafruit OLED FeatherWing (128×32, SSD1306-based)
- Stacking headers for connecting FeatherWings
- USB cable for programming and power

### Software Required
- CircuitPython 10.0.1 or later
- Adafruit CircuitPython Bundle (matching your CircuitPython version)

---

## Step 1: Install CircuitPython on Your M4 Express

### 1.1 Download CircuitPython
1. Visit the CircuitPython downloads page for your board:
   - **Feather M4 Express**: https://circuitpython.org/board/feather_m4_express/
   - **Metro M4 Express**: https://circuitpython.org/board/metro_m4_express/
   - Other M4 boards: https://circuitpython.org/downloads

2. Download the **latest stable release** (10.0.1 or newer)
   - Look for the `.UF2` file

### 1.2 Install CircuitPython
1. Connect your M4 Express to your computer via USB
2. Double-click the **RESET** button on the board
   - The board will appear as a drive named `FEATHERBOOT` or `METROBOOT`
3. Drag and drop the `.UF2` file onto the boot drive
4. The board will automatically reboot
5. A new drive named `CIRCUITPY` should appear
   - If you see this drive, CircuitPython is installed successfully!

---

## Step 2: Install Required Libraries

### 2.1 Download the CircuitPython Library Bundle
1. Visit: https://circuitpython.org/libraries
2. Download the **Bundle for Version 10.x** (must match your CircuitPython version)
3. Extract the `.zip` file

### 2.2 Copy Required Libraries
From the extracted bundle, copy these files/folders to `CIRCUITPY/lib/`:

```
CIRCUITPY/
└── lib/
    ├── adafruit_midi/              (entire folder)
    ├── adafruit_displayio_ssd1306.mpy
    └── adafruit_display_text/      (entire folder)
```

**Files to copy:**
- `adafruit_midi/` - **Entire folder** (MIDI encoding/decoding)
- `adafruit_displayio_ssd1306.mpy` - Single file (OLED display driver)
- `adafruit_display_text/` - **Entire folder** (Text rendering)

### 2.3 Verify Library Installation
Your `CIRCUITPY/lib/` folder should look like this:
```
lib/
├── adafruit_midi/
│   ├── __init__.py
│   ├── note_on.py
│   ├── note_off.py
│   ├── control_change.py
│   ├── timing_clock.py
│   └── ... (other MIDI message types)
├── adafruit_display_text/
│   ├── __init__.py
│   ├── label.py
│   └── ... (other display text modules)
└── adafruit_displayio_ssd1306.mpy
```

---

## Step 3: Install the Arpeggiator Code

### 3.1 Copy Project Files
Copy all `.py` files from this project to the root of `CIRCUITPY`:

```bash
# From your project directory
cp *.py /Volumes/CIRCUITPY/
```

**Required files:**
- `code.py` - Main application (runs on boot)
- `arpeggiator.py` - Arpeggiator engine
- `midi_io.py` - MIDI input/output handling
- `clock_handler.py` - MIDI clock and timing
- `display.py` - OLED display management
- `button_handler.py` - Button input handling
- `settings.py` - Configuration and settings
- `connection_test.py` - Hardware testing utility (optional)

### 3.2 Verify Installation
Your `CIRCUITPY` drive should contain:
```
CIRCUITPY/
├── code.py
├── arpeggiator.py
├── midi_io.py
├── clock_handler.py
├── display.py
├── button_handler.py
├── settings.py
├── connection_test.py
└── lib/
    ├── adafruit_midi/
    ├── adafruit_display_text/
    └── adafruit_displayio_ssd1306.mpy
```

---

## Step 4: Hardware Assembly

### 4.1 Stack the FeatherWings
**Order from bottom to top:**
1. **Bottom**: M4 Express board (Feather/Metro)
2. **Layer 2**: First MIDI FeatherWing (MIDI I/O - uses TX/RX pins)
3. **Layer 3**: Second MIDI FeatherWing (MIDI Clock - uses D10/D11 pins)
4. **Top**: OLED FeatherWing (I2C - uses SCL/SDA pins)

### 4.2 Pin Connections
- **OLED Display**: I2C (SCL, SDA, 0x3C address)
  - Buttons: D9 (A), D6 (B), D5 (C)
- **MIDI FeatherWing #1**: UART (TX, RX at 31250 baud)
- **MIDI FeatherWing #2**: UART (D10=TX, D11=RX at 31250 baud)

See `HARDWARE_PINOUT.md` for detailed wiring information.

---

## Step 5: Testing

### 5.1 Initial Boot Test
1. Connect USB to the M4 Express
2. Open a serial terminal (9600 baud):
   - **Mac/Linux**: `screen /dev/tty.usbmodem* 115200`
   - **Windows**: Use PuTTY or Arduino Serial Monitor
   - **Any OS**: Use Mu Editor (built-in serial console)

3. You should see:
   ```
   Initializing MIDI Arpeggiator...
   Arpeggiator ready!
   Pattern: Up
   Clock Division: 6 ticks
   Channel: 1
   ```

### 5.2 Hardware Connection Test
To verify all hardware is working, type in the serial console:
```
test m4 to oled
```

This will run a diagnostic test checking:
- I2C bus initialization
- OLED display detection (0x3C)
- OLED display functionality
- Button states (A, B, C)

### 5.3 Expected Output
If all tests pass, you'll see:
```
==================================================
M4 Express + OLED FeatherWing Connection Test
==================================================

[1/4] Testing I2C bus initialization...
  ✓ I2C bus initialized successfully

[2/4] Scanning I2C bus for devices...
  Found 1 device(s) at address(es): 0x3C
  ✓ OLED display found at 0x3C

[3/4] Testing OLED display (showing test pattern for 2s)...
  ✓ OLED display working

[4/4] Testing buttons...
  ✓ Buttons initialized (D9=A, D6=B, D5=C)
  Current states: A=False, B=False, C=False

==================================================
✓ ALL TESTS PASSED - Hardware is ready!
==================================================
```

---

## Troubleshooting

### CircuitPython Not Appearing
- **Issue**: `CIRCUITPY` drive doesn't appear after installing
- **Solution**:
  1. Try double-clicking RESET button again
  2. Try a different USB cable (must be data cable, not charge-only)
  3. Reinstall CircuitPython UF2 file

### Import Errors
- **Issue**: `ImportError: no module named 'adafruit_midi'`
- **Solution**:
  1. Verify libraries are in `CIRCUITPY/lib/` folder
  2. Check CircuitPython version matches library bundle version
  3. Ensure you copied the entire `adafruit_midi/` folder, not just files

### OLED Not Detected
- **Issue**: Test shows "OLED display NOT found at expected address 0x3C"
- **Solution**:
  1. Check OLED FeatherWing is properly seated on headers
  2. Verify I2C pins (SCL/SDA) are making contact
  3. Try pressing down on OLED FeatherWing to ensure connection

### MIDI Not Working
- **Issue**: No MIDI input/output
- **Solution**:
  1. Check MIDI cables are connected correctly (In to In, Out to Out)
  2. Verify MIDI devices are powered and configured
  3. Check that MIDI FeatherWings are properly seated
  4. Verify UART pins (TX/RX and D10/D11) are configured correctly

### Code Doesn't Auto-Run
- **Issue**: Code doesn't run automatically on boot
- **Solution**:
  1. Ensure main file is named exactly `code.py` (lowercase)
  2. Check for syntax errors in serial output
  3. Try renaming to `main.py` if `code.py` doesn't work

---

## Advanced Configuration

### Changing Default Settings
Edit `settings.py` to customize:
- Default arpeggio pattern
- MIDI channel (1-16)
- Clock division
- Internal BPM
- Display timeout

### Debug Mode
To enable additional debug output, modify `code.py`:
```python
DEBUG = True  # Add at top of file
```

---

## Getting Help

- **Adafruit Forums**: https://forums.adafruit.com/
- **CircuitPython Discord**: https://adafru.it/discord
- **Project Issues**: Check the README.md for project-specific help

---

## Quick Reference

### Library Versions (Verified)
- **CircuitPython**: 10.0.1+
- **adafruit_midi**: 1.0+
- **adafruit_displayio_ssd1306**: 1.0+
- **adafruit_display_text**: 3.3.3+

### Serial Commands
- `test m4 to oled` - Run hardware connection test

### Button Controls
- **Button A/C**: Enter pattern selection mode
- **Button B**: Enter pattern selection mode
- **Buttons A+C (simultaneous)**: Enter clock source selection mode

See the README for full usage instructions!
