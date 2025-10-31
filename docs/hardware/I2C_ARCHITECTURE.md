# I2C Bus Architecture for Arp

## Overview
The Arp project uses a single shared I2C bus for multiple devices. Proper management is critical to prevent conflicts, crashes, and communication errors.

## Hardware Configuration

**I2C Bus:**
- **SCL**: board.SCL (shared clock line)
- **SDA**: board.SDA (shared data line)
- **Frequency**: 100kHz (safe for all devices)
- **Pull-ups**: Built into OLED FeatherWing (4.7kΩ)

**Connected Devices:**
| Device | Address | Purpose |
|--------|---------|---------|
| OLED FeatherWing (SH1107) | 0x3C | 128x64 display |
| MCP4728 DAC | 0x60 | 4-channel 12-bit CV output |
| MIDI FeatherWing | 0x4D | UART MIDI interface (I2C config only) |

## Critical I2C Rules (from CircuitPython Mastery)

### 1. Single I2C Bus Instance
```python
# BAD - Creates multiple I2C buses
i2c1 = busio.I2C(board.SCL, board.SDA)
i2c2 = busio.I2C(board.SCL, board.SDA)  # CONFLICT!

# GOOD - Use board.I2C() singleton
i2c = board.I2C()  # Returns shared I2C bus
```

**Why:** `board.I2C()` returns a singleton - the same bus instance every time. Creating multiple `busio.I2C()` instances causes hardware conflicts.

### 2. Initialize in Setup, Not in Loop
```python
# BAD - Allocates memory in loop
while True:
    i2c = board.I2C()  # Memory leak!

# GOOD - Initialize once at top
i2c = board.I2C()
display = init_display(i2c)
dac = init_dac(i2c)
# Now use in loop
```

### 3. Lock/Unlock Pattern
```python
# For device libraries (adafruit_mcp4728, etc):
#   Libraries handle locking internally - DON'T manually lock

# For raw I2C access only:
if i2c.try_lock():
    try:
        devices = i2c.scan()
    finally:
        i2c.unlock()
```

### 4. Device Initialization Order
Order matters for reliability:
```python
# 1. Release any existing displays first
displayio.release_displays()
time.sleep(0.2)  # Let hardware settle

# 2. Create shared I2C bus
i2c = board.I2C()

# 3. Initialize devices (order doesn't matter after displayio.release)
display = init_display(i2c)
dac = init_dac(i2c)
midi = init_midi(i2c)
```

## Implementation Pattern

### Initialization (code.py)
```python
import board
import busio
import time
import displayio
import adafruit_mcp4728
from adafruit_displayio_sh1107 import SH1107
import adafruit_midi

# Release any previous display resources
displayio.release_displays()
time.sleep(0.2)

# Create shared I2C bus (singleton)
i2c = board.I2C()

# Initialize OLED Display
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = SH1107(display_bus, width=128, height=64)

# Initialize MCP4728 DAC
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)

# Wake DAC from power-down (if needed)
dac.wakeup()

# Configure DAC for 5V reference
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
dac.channel_b.vref = adafruit_mcp4728.Vref.VDD
dac.channel_c.vref = adafruit_mcp4728.Vref.VDD
dac.channel_d.vref = adafruit_mcp4728.Vref.VDD
dac.save_settings()  # Persist to EEPROM

# Initialize MIDI (UART, not I2C communication)
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart)

# Now all devices ready for main loop
```

### Main Loop Usage
```python
while True:
    # Update display (uses I2C internally)
    update_display(display, current_data)

    # Set DAC outputs (uses I2C internally)
    dac.channel_a.value = cv_value

    # Read MIDI (uses UART, not I2C)
    msg = midi.receive()

    # Collect garbage periodically
    gc.collect()

    time.sleep(0.001)
```

## Common I2C Errors and Solutions

### Error: "No pull up found on SDA or SCL"
**Cause:** Missing pull-up resistors or I2C bus conflict
**Solution:**
- Use `board.I2C()` singleton, not `busio.I2C()`
- Call `displayio.release_displays()` before initializing
- Verify OLED FeatherWing is properly stacked (has built-in pull-ups)

### Error: "RuntimeError: Function requires lock"
**Cause:** Trying to use I2C without locking
**Solution:** Device libraries handle locking automatically. Only lock manually for raw `i2c.scan()` calls.

### Error: "Hard fault: memory access"
**Cause:** I2C device in bad state or hardware damaged
**Solution:**
- Call `dac.wakeup()` to clear power-down mode
- Power cycle the M4
- Check for shorts or damaged hardware

### Error: Device outputs wrong values (e.g., MCP4728 low voltage)
**Cause:** Device in power-down mode or wrong reference voltage
**Solution:**
```python
dac.wakeup()  # Clear power-down
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD  # Use VDD (5V)
dac.channel_a.gain = 1  # 1x gain
dac.save_settings()  # Persist configuration
```

## Testing and Verification

### I2C Bus Scan
```python
i2c = board.I2C()
while not i2c.try_lock():
    pass
devices = i2c.scan()
i2c.unlock()

expected = [0x3C, 0x4D, 0x60]  # OLED, MIDI, DAC
for addr in expected:
    if addr in devices:
        print(f"✓ Found device at 0x{addr:02X}")
    else:
        print(f"✗ Missing device at 0x{addr:02X}")
```

### Device-Specific Tests
See `tests/` directory:
- `tests/i2c_debug_scan.py` - Comprehensive I2C scanner
- `tests/mcp4728_simple_test.py` - DAC verification
- `tests/oled_heartbeat_simple.py` - Display test

## References
- CircuitPython busio documentation: https://docs.circuitpython.org/en/latest/shared-bindings/busio/
- MCP4728 library: https://docs.circuitpython.org/projects/mcp4728/
- SH1107 display library: https://docs.circuitpython.org/projects/displayio-sh1107/
- `~/.claude/references/CIRCUITPYTHON_MASTERY.md` - Section "busio Module"
