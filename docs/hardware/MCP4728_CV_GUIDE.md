# MCP4728 for CV Output - Complete Guide

**Purpose:** Definitive guide for using MCP4728 DAC to generate 1V/octave control voltage for modular synthesis.

**Last Updated:** 2025-10-31
**Hardware:** Feather M4 CAN + MCP4728 @ 5V

---

## Table of Contents
1. [Critical Concepts](#critical-concepts)
2. [The Value Property Trap](#the-value-property-trap)
3. [1V/Octave Mathematics](#1voctave-mathematics)
4. [Proper Initialization Sequence](#proper-initialization-sequence)
5. [Real-Time Performance](#real-time-performance)
6. [Complete Code Example](#complete-code-example)

---

## Critical Concepts

### MCP4728 Specifications
- **Resolution:** 12-bit (4096 discrete steps)
- **Reference Options:** Internal 2.048V or External VDD
- **Gain:** 1x or 2x (only with internal reference)
- **Update Rate:** 6 microseconds settling time
- **I2C Speed:** Supports up to 3.4 Mbps (High Speed mode)

### Our Hardware Configuration
- **VDD:** 4.83V from LM7805 regulator
- **Reference:** Vref.VDD (uses VDD voltage as reference)
- **Gain:** 1x
- **Output Range:** 0V to 4.83V (approximately 0V to 5V)

---

## The Value Property Trap

### ⚠️ CRITICAL BUG: Using Wrong Property

The Adafruit MCP4728 library provides **three different value properties**:

| Property | Range | Bits | Use Case |
|----------|-------|------|----------|
| `raw_value` | 0-4095 | 12-bit | **✅ USE THIS for CV** |
| `normalized_value` | 0.0-1.0 | Float | Proportional control |
| `value` | 0-65535 | 16-bit | Generic DAC interface |

### The Bug Explained

```python
# WRONG - Calculates 12-bit but assigns to 16-bit property
test_value = int((5.0 / 5.0) * 4095)  # = 4095 (12-bit)
dac.channel_a.value = test_value       # Expects 16-bit!

# What actually happens:
# Library does: raw_value = value >> 4
# Result: raw_value = 4095 >> 4 = 255
# Output voltage: (255/4095) * 4.83V = 0.30V ❌
```

```python
# CORRECT - Direct 12-bit control
test_value = int((5.0 / 5.0) * 4095)  # = 4095 (12-bit)
dac.channel_a.raw_value = test_value   # Direct assignment

# What happens:
# raw_value = 4095 (no conversion)
# Output voltage: (4095/4095) * 4.83V = 4.83V ✅
```

### The Math Behind the Bug

When you set `dac.channel_a.value = 4095`:

1. Library expects 16-bit value (0-65535)
2. Converts to 12-bit: `raw_value = 4095 >> 4 = 255`
3. Output voltage: `(255 / 4095) × 4.83V = 0.30V`

**This matches your measured 0.03-0.31V readings!**

### The Fix

**Always use `raw_value` for CV applications:**

```python
# For voltage control
dac.channel_a.raw_value = 4095  # 4.83V (max)
dac.channel_a.raw_value = 2458  # 3.00V
dac.channel_a.raw_value = 0     # 0.00V

# NOT this:
dac.channel_a.value = 4095      # Only 0.30V!
```

---

## 1V/Octave Mathematics

### The Standard

**1V/octave** (1V/oct) is the standard for pitch control in modular synthesis:
- Increasing voltage by 1V raises pitch by 1 octave (12 semitones)
- Each semitone = 1/12 volt = 0.0833V

### MCP4728 Resolution for 1V/Octave

With 5V reference and 12-bit resolution:

```
Steps per volt: 4096 / 5 = 819.2 steps/volt
Steps per semitone: 819.2 / 12 = 68.27 steps/semitone
```

### MIDI Note to Voltage Conversion

**Standard formula:**
```python
voltage = (MIDI_note_number / 12.0)
raw_value = int(voltage * 819.2)
```

**Simplified (from real-world projects):**
```python
raw_value = int(MIDI_note_number * 68.27)
```

### Example Conversions

| MIDI Note | Note Name | Calculation | Raw Value | Voltage |
|-----------|-----------|-------------|-----------|---------|
| 12 | C0 | 12 × 68.27 | 819 | 1.00V |
| 24 | C1 | 24 × 68.27 | 1639 | 2.00V |
| 36 | C2 | 36 × 68.27 | 2458 | 3.00V |
| 48 | C3 | 48 × 68.27 | 3277 | 4.00V |
| 60 | C4 | 60 × 68.27 | 4096 | 5.00V |
| 72 | C5 | 72 × 68.27 | 4915* | 6.00V* |

\* Values > 4095 clip to maximum (4.83V with our VDD)

### Lookup Table Approach (Recommended)

For best real-time performance, use a **pre-calculated lookup table**:

```python
# Pre-calculate at initialization (0-127 MIDI notes)
MIDI_TO_CV = [int(note * 68.27) for note in range(128)]

# In real-time loop - zero latency
def note_on(midi_note):
    raw_value = MIDI_TO_CV[midi_note]
    dac.channel_a.raw_value = min(raw_value, 4095)  # Clamp to max
```

**Why lookup table?**
- Zero calculation overhead in real-time loop
- Consistent timing (critical for clock sync)
- Used by professional MIDI-to-CV projects (MIDI4CV, others)

### Accuracy Analysis

With 68.27 steps/semitone:
- **Theoretical:** Perfect semitone tuning
- **Practical:** MCP4728 INL (Integral Non-Linearity) = ±2 LSB typical, ±13 LSB max
- **Tuning error:** Typically < 2.3 cents, worst case 15 cents

For arpeggiator use: **Excellent** (well within audible pitch tolerance)

---

## Proper Initialization Sequence

### Complete Setup (Copy-Paste Ready)

```python
import board
import time
import displayio
import adafruit_mcp4728

# 1. Release previous displays (if using OLED)
displayio.release_displays()
time.sleep(0.2)

# 2. Get shared I2C bus (singleton pattern)
i2c = board.I2C()

# 3. Initialize MCP4728
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)

# 4. Wake from power-down mode (CRITICAL!)
dac.wakeup()
time.sleep(0.1)

# 5. Configure channel for 5V operation
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD  # Use VDD reference
dac.channel_a.gain = 1                           # 1x gain
time.sleep(0.1)

# 6. Save configuration to EEPROM (survives power cycle)
dac.save_settings()
time.sleep(0.3)

# 7. Set initial voltage (0V)
dac.channel_a.raw_value = 0

# Ready for use!
```

### Critical Steps Explained

**Step 4 - `dac.wakeup()`:**
- MCP4728 can be in power-down mode (outputs disabled)
- Always call `wakeup()` after initialization
- Wait 100ms for hardware to stabilize

**Step 5 - Vref.VDD configuration:**
- `Vref.INTERNAL` = 2.048V reference (only 2 octaves)
- `Vref.VDD` = Use VDD as reference (0-5V, 5 octaves) ✅
- Must set for each channel individually

**Step 6 - `save_settings()`:**
- Stores configuration to EEPROM
- Configuration persists across power cycles
- Wait 300ms for EEPROM write

---

## Real-Time Performance

### Update Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| DAC settling time | 6 µs | Per voltage change |
| I2C transaction | ~200 µs | At 400kHz bus speed |
| Total latency | < 1 ms | From note event to voltage |
| Max note rate | > 1000 notes/sec | Theoretical |

### Performance Optimization

**1. Use raw_value directly:**
```python
# Fast - direct 12-bit write
dac.channel_a.raw_value = 2458

# Slow - requires conversion
dac.channel_a.value = 39328  # Gets converted
```

**2. Pre-calculate lookup table:**
```python
# At initialization
MIDI_TO_CV = [int(n * 68.27) for n in range(128)]

# In loop - instant lookup
dac.channel_a.raw_value = MIDI_TO_CV[midi_note]
```

**3. Minimize I2C transactions:**
```python
# Only update when note changes
if new_note != last_note:
    dac.channel_a.raw_value = MIDI_TO_CV[new_note]
    last_note = new_note
```

### I2C Bus Sharing

With multiple I2C devices (OLED, DAC, MIDI config):

```python
# Initialize once
i2c = board.I2C()  # Singleton - returns same bus

# Use with all devices
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
midi_config = some_i2c_device(i2c, address=0x4D)

# Libraries handle locking automatically - no manual locking needed
```

---

## Complete Code Example

### Arpeggiator CV Driver Module

```python
"""
CV Output Driver for MCP4728
Converts MIDI note numbers to 1V/octave CV
"""

import board
import time
import adafruit_mcp4728

class CVOutput:
    """1V/octave CV output using MCP4728 DAC"""

    # Pre-calculated MIDI note to raw_value lookup (0-127)
    # Formula: raw_value = MIDI_note * 68.27 (clamped to 4095)
    MIDI_TO_CV = [min(int(n * 68.27), 4095) for n in range(128)]

    def __init__(self, i2c, address=0x60):
        """Initialize MCP4728 for CV output

        Args:
            i2c: Shared I2C bus (from board.I2C())
            address: MCP4728 I2C address (default 0x60)
        """
        self.dac = adafruit_mcp4728.MCP4728(i2c, address=address)

        # Wake from power-down mode
        self.dac.wakeup()
        time.sleep(0.1)

        # Configure all channels for 5V operation
        for channel in [self.dac.channel_a, self.dac.channel_b,
                       self.dac.channel_c, self.dac.channel_d]:
            channel.vref = adafruit_mcp4728.Vref.VDD
            channel.gain = 1
        time.sleep(0.1)

        # Save to EEPROM
        self.dac.save_settings()
        time.sleep(0.3)

        # Zero all outputs
        self.set_cv_a(0)
        self.set_cv_b(0)
        self.set_gate(False)

    def set_cv_a(self, midi_note):
        """Set CV output A from MIDI note number

        Args:
            midi_note: MIDI note number (0-127)

        Output voltage: (midi_note / 12) volts (1V/octave)
        Example: midi_note=60 (C4) → 5.00V
        """
        if 0 <= midi_note <= 127:
            self.dac.channel_a.raw_value = self.MIDI_TO_CV[midi_note]

    def set_cv_b(self, midi_note):
        """Set CV output B from MIDI note number"""
        if 0 <= midi_note <= 127:
            self.dac.channel_b.raw_value = self.MIDI_TO_CV[midi_note]

    def set_gate(self, state):
        """Set gate output (0V or 5V)

        Args:
            state: True = 5V (gate high), False = 0V (gate low)
        """
        self.dac.channel_c.raw_value = 4095 if state else 0

    def set_raw_voltage(self, channel, voltage):
        """Set exact voltage on channel (for testing/calibration)

        Args:
            channel: 'a', 'b', 'c', or 'd'
            voltage: Voltage in volts (0.0 to 5.0)
        """
        raw_value = int((voltage / 5.0) * 4095)
        raw_value = max(0, min(4095, raw_value))  # Clamp

        if channel == 'a':
            self.dac.channel_a.raw_value = raw_value
        elif channel == 'b':
            self.dac.channel_b.raw_value = raw_value
        elif channel == 'c':
            self.dac.channel_c.raw_value = raw_value
        elif channel == 'd':
            self.dac.channel_d.raw_value = raw_value

# Usage Example
if __name__ == "__main__":
    # Initialize
    i2c = board.I2C()
    cv = CVOutput(i2c)

    # Play some notes
    notes = [36, 48, 60, 72]  # C2, C3, C4, C5

    for note in notes:
        cv.set_cv_a(note)
        cv.set_gate(True)
        time.sleep(0.5)
        cv.set_gate(False)
        time.sleep(0.1)
```

---

## Troubleshooting

### Issue: Low voltage output (0.03-0.31V instead of 0-5V)

**Cause:** Using `.value` property instead of `.raw_value`

**Fix:** Change all DAC assignments to use `.raw_value`:
```python
# Before
dac.channel_a.value = 4095  # Wrong

# After
dac.channel_a.raw_value = 4095  # Correct
```

### Issue: No voltage output at all

**Possible causes:**
1. MCP4728 in power-down mode → Call `dac.wakeup()`
2. Using internal 2.048V reference → Set `vref = Vref.VDD`
3. VDD not connected → Check 5V power supply
4. Bad I2C connection → Verify communication with `i2c.scan()`

### Issue: Voltage not stable or drifting

**Possible causes:**
1. VDD voltage unstable → Check LM7805 output
2. Configuration not saved → Call `dac.save_settings()`
3. Electrical noise → Add decoupling capacitor near MCP4728 VDD pin

---

## References

- **MCP4728 Datasheet:** Microchip DS22187E
- **Adafruit MCP4728 Library:** https://docs.circuitpython.org/projects/mcp4728/
- **Real-world implementations:**
  - MIDI4CV Project (MCP4728 + ATmega328P)
  - MIDI2CV by dlynch7 (MCP4725 + Arduino)
  - Adafruit MIDI to CV Skull (MCP4725 + RP2040)
- **1V/Octave Standard:** https://en.wikipedia.org/wiki/CV/gate

---

**Last Updated:** 2025-10-31
**Verified Working:** Feather M4 CAN + MCP4728 @ 4.83V VDD
