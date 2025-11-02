# Arp Firmware Update Guide

This guide explains how to update your Arp hardware arpeggiator firmware manually.

> **Note:** An automated updater app is in development. Until then, follow this manual process.

---

## Before You Start

### Check Current Firmware Version

1. Connect your Arp device via USB
2. Open a serial console (see [Serial Connection](#serial-connection))
3. Press the reset button on the device
4. Look for the startup message:
   ```
   ARP - Hardware Arpeggiator v0.95.0
   Build: 2025-10-23 | Hardware: v1.0
   ```

### What You'll Need

- **Arp device** connected via USB
- **Firmware bundle** file (`.arpfw` - it's a zip file)
- **Backup** of your current settings (optional but recommended)

---

## Step 1: Backup Your Settings

Your Arp saves settings to `settings.json` on the device. To preserve your settings:

1. Connect Arp via USB (it appears as `CIRCUITPY` drive)
2. Copy `settings.json` to your computer as a backup
3. Keep this file safe - you'll restore it after the update

---

## Step 2: Download Firmware

1. Go to the [Arp Releases](https://github.com/keegandewitt/prisme/releases) page
2. Download the latest `arp-firmware-vX.X.X.arpfw` file
3. Save it to your Downloads folder

---

## Step 3: Extract Firmware Bundle

The `.arpfw` file is a ZIP archive. Extract it:

**macOS:**
```bash
cd ~/Downloads
unzip arp-firmware-v1.0.0.arpfw -d arp-firmware-v1.0.0
```

**Windows:**
- Right-click the `.arpfw` file
- Select "Extract All..."
- Choose a destination folder

**Linux:**
```bash
cd ~/Downloads
unzip arp-firmware-v1.0.0.arpfw -d arp-firmware-v1.0.0
```

You should now have a folder with:
```
arp-firmware-v1.0.0/
├── manifest.json       # Version info
├── main.py            # Main firmware file
├── arp/               # Core modules
├── lib/               # CircuitPython libraries
└── CHANGELOG.md       # What's new
```

---

## Step 4: Connect Device

1. Connect your Arp via USB
2. Wait for the `CIRCUITPY` drive to appear
3. Verify it's mounted:
   - **macOS:** `/Volumes/CIRCUITPY`
   - **Windows:** `D:` or `E:` (varies)
   - **Linux:** `/media/USERNAME/CIRCUITPY`

---

## Step 5: Install Firmware

### 5a. Copy Main Firmware

**IMPORTANT:** The file `main.py` from the bundle must be renamed to `code.py` on the device.

**macOS/Linux:**
```bash
cp arp-firmware-v1.0.0/main.py /Volumes/CIRCUITPY/code.py
```

**Windows:**
```cmd
copy arp-firmware-v1.0.0\main.py D:\code.py
```

### 5b. Copy Modules

**macOS/Linux:**
```bash
# Remove old modules (if they exist)
rm -rf /Volumes/CIRCUITPY/arp

# Copy new modules
cp -r arp-firmware-v1.0.0/arp /Volumes/CIRCUITPY/
```

**Windows:**
```cmd
rmdir /s /q D:\arp
xcopy /E /I arp-firmware-v1.0.0\arp D:\arp
```

### 5c. Copy Libraries

**macOS/Linux:**
```bash
# Remove old libraries
rm -rf /Volumes/CIRCUITPY/lib

# Copy new libraries
cp -r arp-firmware-v1.0.0/lib /Volumes/CIRCUITPY/
```

**Windows:**
```cmd
rmdir /s /q D:\lib
xcopy /E /I arp-firmware-v1.0.0\lib D:\lib
```

---

## Step 6: Restore Settings (Optional)

If you backed up your `settings.json`:

**macOS/Linux:**
```bash
cp ~/Desktop/settings.json.backup /Volumes/CIRCUITPY/settings.json
```

**Windows:**
```cmd
copy C:\Users\YourName\Desktop\settings.json.backup D:\settings.json
```

---

## Step 7: Reboot Device

The device should auto-reload after copying files. If not:

1. Press the **RESET** button on the Arp device
2. Wait 3-5 seconds for it to boot
3. The OLED display should show:
   ```
   MIDI Arpeggiator
   v1.0.0
   Ready!
   ```

---

## Step 8: Verify Update

### Check Serial Output

Open a serial console and verify the version:

```
ARP - Hardware Arpeggiator v1.0.0
Build: 2025-10-23 | Hardware: v1.0
```

### Test Functionality

1. Press **Button B** - Should play demo arpeggio
2. Press **Button C** - Should cycle patterns
3. Send MIDI notes - Should arpeggiate correctly
4. Check display - Should show BPM and pattern

---

## Troubleshooting

### Device Shows "Safe Mode"

**Symptom:** Red LED blinking, display shows "Safe mode!"

**Cause:** Firmware crashed on boot (usually syntax error or missing library)

**Fix:**
1. Connect to serial console to see error message
2. Check that all files were copied correctly
3. Verify CircuitPython version is 10.0.3 (`boot_out.txt` on device)
4. Re-copy firmware files

### "ImportError: no module named X"

**Symptom:** Serial output shows `ImportError`

**Cause:** Missing library in `lib/` folder

**Fix:**
1. Verify `lib/` folder was copied completely
2. Check that `.arpfw` bundle included libraries
3. Manually install missing library:
   ```bash
   circup install library_name
   ```

### Display Not Working

**Symptom:** OLED display is blank

**Cause:** Library mismatch or I2C issue

**Fix:**
1. Press reset button
2. Check serial output for errors
3. Verify `adafruit_displayio_sh1107` is in `lib/` folder
4. Check hardware connections (OLED FeatherWing seated properly)

### Settings Lost After Update

**Symptom:** Arp resets to default settings

**Cause:** Forgot to backup `settings.json` before update

**Fix:**
- Unfortunately settings are lost
- Reconfigure via Settings menu (long-press A+C)
- Next time, backup `settings.json` first!

---

## Serial Connection

To monitor serial output during update:

### macOS/Linux

**Using screen:**
```bash
screen /dev/tty.usbmodem* 115200
```
(Press `Ctrl+A` then `K` to exit)

**Using Python script:**
```bash
python3 scripts/monitor_serial.py
```

### Windows

**Using PuTTY:**
1. Download [PuTTY](https://www.putty.org/)
2. Select "Serial" connection type
3. Set COM port (check Device Manager)
4. Set speed: 115200
5. Click "Open"

**Using Mu Editor:**
1. Download [Mu Editor](https://codewith.mu/)
2. Click "Serial" button at top
3. Device output appears in console

---

## Rolling Back

If the update causes problems, you can roll back to the previous version:

1. Download the previous firmware version from [Releases](https://github.com/keegandewitt/prisme/releases)
2. Follow the same update procedure above
3. Restore your backed-up `settings.json`

---

## Getting Help

If you encounter issues:

1. **Check the logs:** Connect to serial console to see error messages
2. **Report a bug:** [Open an issue](https://github.com/keegandewitt/prisme/issues) with:
   - Current firmware version
   - Target firmware version
   - Full serial output
   - Steps to reproduce the problem
3. **Community support:** [Join the discussion](https://github.com/keegandewitt/prisme/discussions)

---

## Next: Automated Updater

We're building a desktop app that will automate this entire process:

- ✅ Auto-detect device
- ✅ Download firmware automatically
- ✅ Backup settings
- ✅ Install firmware with one click
- ✅ Verify installation
- ✅ Restore settings
- ✅ No command line required

**Coming soon!** Follow the project for updates.

---

**Last Updated:** 2025-10-23
**Applies to:** Arp v0.95.0 and later
