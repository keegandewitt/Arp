# Custom CC Implementation - Prep Doc
**Date:** 2025-11-01
**Purpose:** Eliminate uncertainties before implementation

---

## ✅ Research Complete - All Questions Answered!

### 1. How Menu System Works

**File:** `arp/ui/menu.py`

**Architecture:**
- **Three-level hierarchy:** Category → Setting → Value
- **Current categories:** 6 (Clock, Arp, Scale, Triggers, CV, Firmware)
- **Display format:** 3 lines of text on OLED

**Pattern to Add Custom CC:**
```python
# Step 1: Add category constant
CATEGORY_CUSTOM_CC = 6  # 7th category

# Step 2: Add to category_names dict (line 62)
self.category_names = {
    # ... existing ...
    self.CATEGORY_CUSTOM_CC: "Custom CC"
}

# Step 3: Add setting names
self.custom_cc_setting_names = {
    0: "Source",
    1: "CC Number",
    2: "Smoothing"
}

# Step 4: Handle in navigate_next/previous (lines 146-171)
# Step 5: Handle in _increase_value/_decrease_value (lines 227-303)
# Step 6: Add to get_display_text() (lines 311-516)
```

**Auto-save:** Settings automatically saved after each change (lines 264, 303) ✓

---

### 2. How NVM Settings Storage Works

**File:** `arp/utils/config.py`

**Current Storage:**
- **Format:** Binary struct using `struct.pack()`
- **Magic bytes:** `ARP2` for validation
- **Current size:** 24 bytes / 256 bytes available (9% usage)
- **Struct format:** `'BBBHBBBBBBBBBBBf'` (mostly bytes)

**Adding Custom CC Settings:**
```python
# Current struct (line 25):
SETTINGS_STRUCT_FORMAT = 'BBBHBBBBBBBBBBBf'  # 16 values, 24 bytes

# Add 3 new bytes for Custom CC:
SETTINGS_STRUCT_FORMAT = 'BBBHBBBBBBBBBBBfBBB'  # 19 values, 27 bytes
# Added: ^^^ custom_cc_source, custom_cc_number, custom_cc_smoothing

# Still only 27 / 256 bytes (10%) - plenty of room! ✓
```

**Save/Load Pattern:**
```python
def save(self):  # Line 306
    packed_data = struct.pack(
        SETTINGS_STRUCT_FORMAT,
        # ... existing 16 values ...
        self.custom_cc_source,     # B (byte) - NEW
        self.custom_cc_number,     # B (byte) - NEW
        self.custom_cc_smoothing   # B (byte) - NEW
    )
    nvm_data = NVM_SETTINGS_MAGIC + packed_data
    microcontroller.nvm[NVM_SETTINGS_START:...] = nvm_data

def load(self):  # Line 349
    unpacked = struct.unpack(SETTINGS_STRUCT_FORMAT, packed_data)
    # ... assign existing 16 values ...
    self.custom_cc_source = unpacked[16]     # NEW
    self.custom_cc_number = unpacked[17]     # NEW
    self.custom_cc_smoothing = unpacked[18]  # NEW
```

**Memory impact:** +3 bytes (negligible) ✓

---

### 3. How Button Handling Works

**File:** `arp/ui/buttons.py`

**Long Press Detection Already Implemented!**

```python
# Line 47: Long press threshold
self.long_press_time = 0.8  # 800ms

# Line 126-140: Button B long press tracking
if not current_b:  # Button B pressed
    if self.b_press_start_time is None:
        self.b_press_start_time = current_time
        self.b_long_press_triggered = False
    elif not self.b_long_press_triggered:
        if current_time - self.b_press_start_time >= self.long_press_time:
            b_long_press = True
            self.b_long_press_triggered = True

# Line 64: Returns tuple including b_long_press
return (a_pressed, b_pressed, c_pressed, ac_combo, a_long_press, b_long_press, ac_long_press)
```

**For Learn Mode:**
- Check `b_long_press` when in Custom CC menu
- No new code needed - infrastructure exists! ✓

---

### 4. How CV Output Works

**File:** `arp/drivers/cv_gate.py`

**MCP4728 Channel Allocation:**
```python
# Line 14-18: Channel assignments
CH_PITCH = 0      # Channel A: CV pitch (IN USE)
CH_TRIGGER = 1    # Channel B: Trigger/gate (IN USE)
CH_UNUSED_C = 2   # Channel C: Reserved
CH_UNUSED_D = 3   # Channel D: Reserved ← USE THIS FOR CUSTOM CC
```

**Initialization Already Done:**
```python
# Line 48-52: All channels configured with 5V internal reference
for channel in [dac.channel_a, dac.channel_b, dac.channel_c, dac.channel_d]:
    channel.vref = adafruit_mcp4728.Vref.INTERNAL
    channel.gain = 1  # 1x gain for 0-5V output
    channel.value = 0  # Start at 0V
```

**Voltage Conversion Pattern:**
```python
# Line 92-106: Existing pattern to copy
def voltage_to_dac_value(self, voltage):
    dac_value = int((voltage / self.DAC_VREF) * self.DAC_MAX_VALUE)
    return max(0, min(self.DAC_MAX_VALUE, dac_value))

# For Custom CC, add:
def cc_to_voltage(self, cc_value):
    """Convert MIDI CC (0-127) to 0-5V"""
    voltage = (cc_value / 127.0) * 5.0
    return max(0.0, min(5.0, voltage))

def set_custom_cc(self, cc_value):
    """Set Custom CC output on Channel D"""
    voltage = self.cc_to_voltage(cc_value)
    dac_value = self.voltage_to_dac_value(voltage)
    self.dac.channel_d.value = dac_value  # ← Channel D!
```

**No hardware setup needed - just use existing DAC** ✓

---

### 5. How MIDI Pass-Through Works

**File:** `arp/drivers/midi_output.py`

**Current Implementation:**
```python
# Line 10: Already imports ControlChange
from adafruit_midi.control_change import ControlChange

# Line 121-144: Current pass-through (NoteOn/NoteOff only)
def process_passthrough(self, messages, channel=0):
    for msg in messages:
        if isinstance(msg, NoteOn):
            # ... handle note on ...
        elif isinstance(msg, NoteOff):
            # ... handle note off ...
```

**Extension Needed:**
```python
# Add imports (top of file):
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.channel_pressure import ChannelPressure

# Extend process_passthrough (line 121):
def process_passthrough(self, messages, channel=0):
    for msg in messages:
        if isinstance(msg, NoteOn):
            # ... existing code ...
        elif isinstance(msg, NoteOff):
            # ... existing code ...
        elif isinstance(msg, ControlChange):  # NEW
            self.send_cc(msg.control, msg.value, channel)
        elif isinstance(msg, PitchBend):  # NEW
            self.midi_out.send(msg, channel=channel)
        elif isinstance(msg, ChannelPressure):  # NEW
            self.midi_out.send(msg, channel=channel)
```

**Simple extension of existing pattern** ✓

---

## 📊 Implementation Complexity Analysis

### Lines of Code Estimate:

| Component | File | Lines | Complexity |
|-----------|------|-------|------------|
| Settings constants | config.py | +10 | Trivial |
| NVM save/load | config.py | +6 | Copy existing |
| Voltage conversion | cv_gate.py | +30 | Simple math |
| CC Smoothing | cv_gate.py | +15 | One formula |
| Menu category | menu.py | +50 | Copy pattern |
| MIDI pass-through | midi_output.py | +10 | Simple extension |
| Custom CC handler | midi_custom_cc.py (NEW) | +80 | New file |
| **TOTAL** | | **~200 lines** | **Low-Med** |

---

## 🎯 Revised Confidence Level

### Before Research: 40-50%
**Concerns:**
- ❌ Don't know menu system
- ❌ Don't know NVM storage
- ❌ Don't know button handling
- ❌ Don't know memory constraints

### After Research: 85-90%
**Why High Confidence:**
- ✅ Menu system follows clear 3-level pattern
- ✅ NVM storage is simple struct.pack()
- ✅ Long press detection already implemented!
- ✅ MCP4728 Channel D already initialized!
- ✅ Voltage conversion pattern exists
- ✅ MIDI library already imported
- ✅ Only 3 bytes of NVM needed (plenty of space)
- ✅ ~200 lines of straightforward code

**Remaining 10-15% Risk:**
- Integration bugs (always possible)
- Hardware testing iterations
- Edge cases in menu navigation

---

## 🚀 Implementation Order (Optimized)

### Phase 1: Settings + Core Voltage Conversion (30 min)
**Files:** `config.py`, `cv_gate.py`

1. Add constants to `config.py` (10 min)
   - Custom CC source types (3 constants)
   - Smoothing levels (4 constants)
   - Default values in `__init__()`

2. Update NVM struct (10 min)
   - Modify `SETTINGS_STRUCT_FORMAT`
   - Update `save()` method (+3 lines)
   - Update `load()` method (+3 lines)

3. Add voltage conversion to `cv_gate.py` (10 min)
   - `cc_to_voltage()` - one line of math
   - `set_custom_cc()` - call dac.channel_d.value
   - Copy existing pattern

**Test:** Settings save/load, basic voltage output

---

### Phase 2: CC Smoothing (20 min)
**File:** `cv_gate.py`

1. Add smoothing state variable (5 min)
   - `self.custom_cc_smoothed_value = 0.0`

2. Implement exponential moving average (15 min)
   - Smoothing coefficients dict
   - Apply formula: `(alpha × target) + ((1-alpha) × current)`

**Test:** Rapid CC changes with smoothing on/off

---

### Phase 3: Custom CC Handler + Learn Mode (45 min)
**File:** `arp/drivers/midi_custom_cc.py` (NEW)

1. Create `CustomCCHandler` class (20 min)
   - `process_messages()` - route by source type
   - `enter_learn_mode()` / `exit_learn_mode()`
   - `get_last_midi_display()` - for UI feedback

2. Handle all message types (15 min)
   - CC → `cc_to_voltage()`
   - Aftertouch → `aftertouch_to_voltage()`
   - Pitch Bend → `pitch_bend_to_voltage()`
   - Velocity → `velocity_to_voltage()`

3. Learn mode logic (10 min)
   - If learn active + CC received → capture number
   - Exit learn mode automatically

**Test:** Learn mode capture, voltage output per source

---

### Phase 4: Menu Integration (40 min)
**File:** `menu.py`

1. Add Custom CC category (15 min)
   - Category constant
   - Category name
   - Setting names dict

2. Navigation handling (10 min)
   - Add to `navigate_next/previous()`
   - Add to `select()` / `back()`

3. Value adjustment (10 min)
   - Add to `_increase_value()` / `_decrease_value()`
   - Call settings save

4. Display rendering (5 min)
   - Add to `get_display_text()`
   - Format for 3-line OLED

**Test:** Navigate menu, change values, persistence

---

### Phase 5: MIDI Pass-Through Extension (15 min)
**File:** `midi_output.py`

1. Add imports (2 min)
   - `PitchBend`, `ChannelPressure`

2. Extend `process_passthrough()` (10 min)
   - Add elif for CC
   - Add elif for Pitch Bend
   - Add elif for Aftertouch

3. Test latency (3 min)
   - Profile with time.monotonic()

**Test:** MIDI messages pass through, latency < 1ms

---

### Phase 6: Hardware Test (20 min)
**File:** `tests/custom_cc_test.py` (NEW)

1. Create test script (15 min)
   - Cycle through all sources
   - Display on OLED
   - Output to Channel D

2. Multimeter verification (5 min)
   - CC 0 → 0.000V ± 0.020V
   - CC 64 → 2.520V ± 0.020V
   - CC 127 → 5.000V ± 0.020V

**Test:** Voltage accuracy within ±20mV (Polyend Poly 2 standard)

---

## ⏱️ Final Time Estimate

| Phase | Time | Confidence |
|-------|------|------------|
| Phase 1: Settings + Voltage | 30 min | 95% |
| Phase 2: CC Smoothing | 20 min | 90% |
| Phase 3: CC Handler + Learn | 45 min | 85% |
| Phase 4: Menu Integration | 40 min | 80% |
| Phase 5: MIDI Pass-Through | 15 min | 95% |
| Phase 6: Hardware Test | 20 min | 90% |
| **TOTAL** | **2h 50min** | **87% avg** |

**Buffer for debugging:** +1h 10min → **4 hours total**

---

## 🔑 Key Implementation Insights

### 1. Menu System is Copy-Paste Friendly
The menu system uses a clear repeating pattern. Adding Custom CC is nearly identical to existing Triggers/CV categories.

### 2. Button Long-Press Already Works
No need to implement long-press detection - it's already in `buttons.py` and works perfectly. Just check `b_long_press` flag!

### 3. MCP4728 Channel D is Ready
Channel D is already initialized with 5V internal reference. Just write to `dac.channel_d.value` - no setup needed!

### 4. NVM Has Tons of Space
Currently using 24 / 256 bytes (9%). Adding 3 bytes for Custom CC = 27 / 256 bytes (10%). Zero memory concerns.

### 5. Voltage Conversion is Trivial
```python
voltage = (cc_value / 127.0) * 5.0  # One line!
```

### 6. Smoothing is One Formula
```python
smoothed = (alpha * target) + ((1-alpha) * current)  # Exponential moving average
```

### 7. MIDI Library Does the Heavy Lifting
`adafruit_midi` handles all message parsing. We just check `isinstance()` and route.

---

## 🎓 Lessons from Existing Code

### Auto-Save Pattern (from menu.py)
```python
def _increase_value(self):
    # ... change value ...
    self.settings.save()  # Auto-save immediately! (line 264)
```
**Insight:** No need for explicit "Save" button - auto-save after each change.

### Long Press Pattern (from buttons.py)
```python
if button_pressed:
    if press_start_time is None:
        press_start_time = current_time  # Mark start
    elif current_time - press_start_time >= threshold:
        long_press_triggered = True  # Fire event
```
**Insight:** Simple state machine - track start time, check threshold.

### Voltage Conversion Pattern (from cv_gate.py)
```python
def note_to_voltage(self, midi_note):
    semitones = midi_note - REFERENCE_NOTE
    voltage = REFERENCE_VOLTAGE + (semitones * volts_per_semitone)
    return max(0.0, min(5.0, voltage))  # Clamp!
```
**Insight:** Always clamp to 0-5V range to protect hardware.

---

## ✅ Ready to Implement!

**All questions answered:**
- ✅ Menu system architecture understood
- ✅ NVM storage pattern clear
- ✅ Button handling exists
- ✅ CV output ready
- ✅ MIDI pass-through simple
- ✅ Memory constraints non-issue

**Confidence:** 87%
**Estimated Time:** 2h 50min (realistic), 4h (with buffer)

**Recommendation:** Proceed with Phase 1 implementation now!
