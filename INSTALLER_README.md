# Auto-Installer for MIDI Arpeggiator

## Overview

The auto-installer automatically detects when your Feather board is connected and syncs missing or outdated files, including `test_commands.py`. No more manual file copying!

## Features

✅ **Auto-detects** CIRCUITPY drive when connected
✅ **Smart sync** - only copies missing/outdated files
✅ **Safe** - won't overwrite newer files without `--force`
✅ **Watch mode** - monitors for board connection and auto-installs
✅ **Cross-platform** - macOS, Linux, Windows
✅ **Verification** - checks file hashes to avoid unnecessary copies

## Quick Start

### One-Time Install

Plug in your board and run:

```bash
python3 install.py
```

**Output:**
```
==============================================================
          MIDI Arpeggiator - Auto-Installer
==============================================================

ℹ Searching for CIRCUITPY drive...
✓ Found CIRCUITPY at: /Volumes/CIRCUITPY
ℹ Device: Adafruit CircuitPython 9.0.0 on 2024-01-01; Feather M4 CAN

  code.py                        → Up to date
  settings.py                    → Up to date
  test_commands.py               → Copying (missing)
  ...

==============================================================
                Installation Summary
==============================================================

✓ Copied 1 file(s)
ℹ Skipped 7 file(s)

✓ Installation complete!
```

### Watch Mode (Recommended for Development)

**Start watch mode:**
```bash
python3 install.py --watch
```

Or use the shortcut:
```bash
./watch.sh
```

**What happens:**
1. Script monitors for CIRCUITPY drive
2. When you plug in the board → auto-installs missing files
3. When you unplug → waits for next connection
4. Press Ctrl+C to exit

**Perfect for:**
- Enclosure assembly (test each component as you install it)
- Rapid development (edit code, plug in board, auto-sync)
- Multiple boards (swap boards and auto-sync to each)

## Usage Examples

### Check Installation Status

See what's missing without copying anything:

```bash
python3 install.py --check
```

**Output:**
```
✓ Up to date: code.py
✓ Up to date: settings.py
✗ Missing: test_commands.py
⚠ Outdated: display.py

Summary: 6 up to date, 1 outdated, 1 missing
```

### Force Reinstall Everything

Overwrite all files regardless of status:

```bash
python3 install.py --force
```

**Use when:**
- Recovering from corrupted files
- Resetting to known good state
- Deploying to a new board

### Dry Run (Preview Changes)

See what would be copied without actually copying:

```bash
python3 install.py --dry-run
```

**Output shows:**
```
Would copy test_commands.py (missing)
Would copy display.py (outdated)
```

## Files Managed by Installer

### Required Files (Always Synced)

| File | Description |
|------|-------------|
| `code.py` | Main application |
| `settings.py` | Configuration |
| `midi_io.py` | MIDI input/output handler |
| `clock_handler.py` | Clock synchronization |
| `arpeggiator.py` | Arpeggiator engine |
| `display.py` | OLED display manager |
| `button_handler.py` | Button input handler |
| `test_commands.py` | **Hardware test suite** ⭐ |

### Optional Files (Synced if Present)

| File | Description |
|------|-------------|
| `TESTING_GUIDE.md` | Test documentation |
| `README.md` | Project documentation |
| `HARDWARE_PINOUT.md` | Hardware reference |

## How It Works

### 1. Drive Detection

Checks common mount points:
- macOS: `/Volumes/CIRCUITPY`
- Linux: `/media/CIRCUITPY`
- Windows: `D:/`, `E:/`, etc.

Verifies drive by checking for `boot_out.txt` (unique to CircuitPython devices)

### 2. File Status Check

For each file, compares:
- **MD5 hash** (are contents identical?)
- **Modification time** (which is newer?)

**Status values:**
- `same` - Files are identical (skip)
- `missing` - File doesn't exist on device (copy)
- `outdated` - Device file is older (copy)
- `newer` - Device file is newer (skip, unless `--force`)

### 3. Smart Sync

- Only copies what's needed
- Creates directories as needed
- Preserves modification times
- Handles errors gracefully

## Typical Workflows

### Workflow 1: Initial Setup

```bash
# 1. Clone/download project
cd /path/to/Arp

# 2. Plug in Feather board

# 3. Install all files
python3 install.py

# 4. Connect to serial to verify
screen /dev/tty.usbmodem* 115200

# 5. Test hardware
>>> test all
```

### Workflow 2: Adding test_commands.py to Existing Board

```bash
# Board already has code.py, settings.py, etc.
# Just missing test_commands.py

python3 install.py

# Output:
#   code.py         → Up to date
#   settings.py     → Up to date
#   test_commands.py → Copying (missing)  ← Only copies this!

# Done! Test commands now available
```

### Workflow 3: Development Cycle

**Terminal 1 - Watch mode:**
```bash
./watch.sh
```

**Terminal 2 - Code editor:**
```bash
# Edit display.py locally
code display.py

# Save changes
# Unplug board
# Plug in board → auto-syncs display.py
```

**Terminal 3 - Serial console:**
```bash
screen /dev/tty.usbmodem* 115200

# Test changes immediately
>>> test oled
```

### Workflow 4: Multi-Board Deployment

```bash
# Start watch mode
python3 install.py --watch

# Plug in board #1 → auto-syncs
# Unplug board #1

# Plug in board #2 → auto-syncs
# Unplug board #2

# Plug in board #3 → auto-syncs
# ...
```

## Troubleshooting

### "CIRCUITPY drive not found"

**Check:**
1. Board is connected via USB (data cable, not charge-only)
2. CircuitPython is installed (not Arduino/etc.)
3. Drive is mounted:
   - macOS: Check Finder sidebar
   - Linux: `ls /media`
   - Windows: Check File Explorer

**Fix:**
- Replug USB cable
- Try different USB port
- Reinstall CircuitPython

### "Permission denied" on Linux

CircuitPython drives may need special permissions:

```bash
# Option 1: Run with sudo (not recommended)
sudo python3 install.py

# Option 2: Add udev rule (better)
sudo nano /etc/udev/rules.d/99-circuitpython.rules
# Add: SUBSYSTEM=="usb", ATTRS{idVendor}=="239a", MODE="0666"
sudo udevadm control --reload-rules
```

### Files Keep Getting Overwritten

If you edit files directly on the device and the installer keeps overwriting:

**Solution 1:** Edit source files locally instead
```bash
# Edit in project directory
nano /Users/keegandewitt/Cursor.ai/Arp/test_commands.py

# Then sync
python3 install.py --force
```

**Solution 2:** Use `--check` mode to see status without copying
```bash
python3 install.py --check
```

### Watch Mode Not Detecting Board

**macOS:** May need to grant Terminal permissions
- System Preferences → Security & Privacy → Files and Folders
- Allow Terminal to access Removable Volumes

**Linux:** May need to mount drive manually
```bash
sudo mount /dev/sdb1 /media/CIRCUITPY
```

## Advanced Usage

### Custom File List

Edit `install.py` to add your own files:

```python
FILES_TO_SYNC = {
    "code.py": "code.py",
    "settings.py": "settings.py",
    # ... existing files ...
    "my_module.py": "my_module.py",  # Add this
}
```

### Deploy to Different Drive Name

If your board shows up as something other than `CIRCUITPY`:

```python
# Edit CIRCUITPY_MOUNT_POINTS in install.py
CIRCUITPY_MOUNT_POINTS = [
    "/Volumes/CIRCUITPY",
    "/Volumes/MYBOARD",  # Add custom name
]
```

### Integration with Git Hooks

Auto-sync on git commit:

```bash
# .git/hooks/post-commit
#!/bin/bash
if [ -d "/Volumes/CIRCUITPY" ]; then
    python3 install.py
fi
```

## Command Reference

```
usage: install.py [-h] [--force] [--check] [--watch] [--dry-run]

Options:
  -h, --help     Show help message
  -f, --force    Force reinstall all files
  -c, --check    Check installation status only
  -w, --watch    Watch mode - auto-install on connect
  -n, --dry-run  Preview changes without copying

Examples:
  python3 install.py              # Install missing files
  python3 install.py --force      # Reinstall everything
  python3 install.py --check      # Check status
  python3 install.py --watch      # Auto-install on connect
  ./watch.sh                      # Shortcut for watch mode
```

## Verifying Installation with Hardware Tests

After installing files, verify everything works using the built-in test commands via serial:

### Connecting to Serial Console

**macOS/Linux:**
```bash
# Find device
ls /dev/tty.usb*

# Connect
screen /dev/tty.usbmodem14201 115200

# Exit: Ctrl+A, then K, then Y
```

**Windows (PowerShell):**
```powershell
# List COM ports
Get-WmiObject Win32_SerialPort | Select Name,DeviceID

# Use PuTTY or other terminal at 115200 baud
```

### Running Tests

Once connected to serial, type these commands:

| Command | What It Tests | Duration |
|---------|---------------|----------|
| `help` | Show command list | Instant |
| `test i2c` | I2C bus and device scan | ~1s |
| `test oled` | OLED display | 2s |
| `test buttons` | Button A, B, C inputs | 10s |
| `test midi` | MIDI input/output | 10s |
| `test dac` | MCP4728 DAC | ~1s |
| `test all` | Complete hardware suite | ~25s |

### Example Test Session

```
Initializing MIDI Arpeggiator...
Arpeggiator ready!
Pattern: Up
Clock Division: 6 ticks
Channel: 1
----------------------------------------

help                           <-- Type this and press Enter

==================================================
AVAILABLE TEST COMMANDS
==================================================
  test i2c      - Scan I2C bus
  test oled     - Quick OLED display test
  test buttons  - Test buttons (10s)
  test midi     - Test MIDI I/O (10s)
  test dac      - Test MCP4728 DAC
  test all      - Run all tests
  help          - Show this menu
==================================================

test all                       <-- Run full hardware test

==================================================
I2C Bus Scan
==================================================
Found 2 device(s):
  0x3C (OLED Display - SSD1306)
  0x60 (MCP4728 DAC)
==================================================

[Additional test output...]

✓ ALL TESTS PASSED
```

### Recommended Test Flow After Installation

```bash
# 1. Install files
python3 install.py

# 2. Connect to serial
screen /dev/tty.usbmodem* 115200

# 3. Run quick verification
>>> test i2c        # Verify I2C devices detected
>>> test oled       # Verify display works

# 4. Full hardware test (if assembling enclosure)
>>> test all        # Complete component verification
```

### Troubleshooting Tests

**No response to commands:**
- Verify baud rate is 115200
- Check correct serial port is selected
- Try unplugging and reconnecting

**Tests fail:**
- Run `test i2c` first to see which devices are detected
- Check hardware connections (see `TESTING_GUIDE.md`)
- Verify all FeatherWing boards are properly seated

**Display shows "Connection Test OK" on startup:**
- This means a test recently ran - normal behavior
- Display will return to normal operation after 2 seconds

## Tips

1. **Keep watch mode running** during enclosure assembly
2. **Use --check frequently** to verify what's on the board
3. **Commit changes to git** before forcing reinstall (safety net)
4. **Test after syncing** with `test all` command
5. **Unplug/replug** if device isn't detected immediately
6. **Use serial tests** to verify each component as you assemble

## Safety Features

✅ **Hash verification** - Only copies if content differs
✅ **Timestamp check** - Won't overwrite newer files
✅ **Dry-run mode** - Preview before copying
✅ **Error handling** - Continues even if one file fails
✅ **Optional files** - Won't fail if documentation missing

---

**Happy Hacking!** 🚀
