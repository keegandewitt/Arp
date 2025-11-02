# UX Redesign Implementation Plan
## prisme Translation Hub - Settings Overhaul

**Date:** 2025-11-01
**Status:** Ready to Implement
**Approved By:** User
**Estimated Time:** 4-5 days

---

## Goals

Transform prisme's settings from 27 verbose controls to 24 intuitive, self-explanatory controls.

**Key Principles:**
1. Value determines behavior (no redundant enable/disable toggles)
2. Ranges adapt behavior naturally (Timing Feel: Robot → Swing → Humanize)
3. Neutral values = disabled (Clock Rate 1x = off, Octaves 0 = off)
4. Smarter display (only show active features)

---

## Changes Summary

### Removed (6 settings):
1. ❌ `clock_multiply` - Merged into clock_rate
2. ❌ `clock_divide` - Merged into clock_rate
3. ❌ `swing_percent` - Merged into timing_feel
4. ❌ `clock_enabled` - Auto-detect from clock_rate + timing_feel
5. ❌ `scale_enabled` - Auto-detect from scale_type != CHROMATIC
6. ❌ `cv_enabled` - Always on (hardware output)

### Added (4 settings):
1. ✅ `clock_rate` - Unified /8 to 8x (replaces multiply + divide)
2. ✅ `timing_feel` - Unified 50-100% (replaces swing + humanize)
3. ✅ `midi_filter` - Presets: Off/Vintage/Minimal (replaces vintage boolean)
4. ✅ `likelihood` - 0-100% (100 = disabled)

### Modified (2 settings):
1. 🔄 `octave_range` - Changed from 1-4 to 0-4 (0 = disabled)
2. 🔄 `custom_cc_source` - Removed "Disabled" enum value (use smoothing=off)

**Net Result:** 27 → 24 settings, 35 → 30 bytes

---

## Implementation Phases

### Phase 1: Add New Controls (Backward Compatible)
**Goal:** Add new settings alongside old without breaking anything
**Time:** 1 day

#### 1.1 Update config.py - Add New Settings
```python
# Add new unified controls
self.clock_rate = 3  # 0=/8, 1=/4, 2=/2, 3=1x, 4=2x, 5=4x, 6=8x (default: 1x)
self.timing_feel = 50  # 50-100 (50=robot, 51-75=swing, 76-100=humanize)
self.midi_filter = 0  # 0=Off, 1=Vintage, 2=Minimal, 3=Custom(future)
self.likelihood = 100  # 0-100 (100=disabled)

# Strum settings (for future feature)
self.strum_speed = 1  # 0=/64, 1=/32, 2=/16, 3=/8, 4=/4, 5=/2
self.strum_octaves = 1  # 1-4
self.strum_repeat = False  # One-shot or loop
self.strum_direction = 0  # 0=Up, 1=Down, 2=UpDown

# Keep old settings for now (will remove in Phase 3)
# self.clock_multiply, self.clock_divide, self.swing_percent, etc.
```

#### 1.2 Add Helper Methods
```python
def get_clock_multiply_divide(self):
    """Convert clock_rate to multiply/divide for backward compat"""
    rates = [
        (1, 8),  # /8
        (1, 4),  # /4
        (1, 2),  # /2
        (1, 1),  # 1x
        (2, 1),  # 2x
        (4, 1),  # 4x
        (8, 1),  # 8x
    ]
    return rates[self.clock_rate]

def get_swing_percent(self):
    """Convert timing_feel to swing_percent"""
    if self.timing_feel <= 50:
        return 50  # No swing
    elif self.timing_feel <= 75:
        return self.timing_feel  # Swing range
    else:
        return 50  # Humanize mode (no swing)

def get_humanize_amount(self):
    """Extract humanize amount from timing_feel"""
    if self.timing_feel <= 75:
        return 0  # No humanize
    else:
        # Map 76-100 to 0-100% humanize
        return (self.timing_feel - 75) * 4

def is_clock_active(self):
    """Check if clock transformations are active"""
    return self.clock_rate != 3 or self.timing_feel != 50  # 3 = 1x

def is_scale_enabled(self):
    """Check if scale quantization is active"""
    return self.scale_type != self.SCALE_CHROMATIC

def is_arp_enabled(self):
    """Check if arpeggiator is active"""
    return self.octave_range > 0

def should_filter_message(self, msg):
    """Check if MIDI message should be filtered"""
    if self.midi_filter == 0:  # Off
        return False

    if self.midi_filter == 1:  # Vintage
        from adafruit_midi import (ActiveSensing, ChannelPressure,
                                    PolyphonicKeyPressure, ProgramChange)
        return isinstance(msg, (ActiveSensing, ChannelPressure,
                                PolyphonicKeyPressure, ProgramChange))

    # Future: Minimal, Custom
    return False
```

#### 1.3 Update Clock Handler
```python
# In clock.py - add method to apply timing feel
def apply_timing_feel(self, note_time, bpm):
    """Apply timing feel (swing or humanize)"""
    feel = self.settings.timing_feel

    if feel == 50:
        return note_time  # Perfect timing

    if feel <= 75:
        # Swing mode (51-75%)
        swing_amount = feel
        return self._apply_swing(note_time, swing_amount, bpm)
    else:
        # Humanize mode (76-100%)
        humanize_amount = (feel - 75) * 4  # Map to 0-100%
        return self._apply_humanize(note_time, humanize_amount, bpm)

def _apply_swing(self, note_time, swing_percent, bpm):
    """Apply Roger Linn swing (existing implementation)"""
    # Existing swing code...
    pass

def _apply_humanize(self, note_time, humanize_percent, bpm):
    """Apply random timing variation"""
    import random

    # Calculate max variation (smaller of 50ms or 1/64 note)
    sixteenth_note = 60.0 / (bpm * 4)
    sixty_fourth = sixteenth_note / 4
    max_variation = min(0.050, sixty_fourth)

    # Scale by humanize amount
    variation_range = max_variation * (humanize_percent / 100.0)

    # Random offset
    offset = random.uniform(-variation_range, variation_range)

    return note_time + offset
```

**Deliverables:**
- ✅ New settings added to config.py
- ✅ Helper methods for backward compatibility
- ✅ Clock handler supports timing_feel
- ✅ All existing code still works

---

### Phase 2: Update Menu & Display
**Goal:** Show new controls in UI, hide old ones
**Time:** 1 day

#### 2.1 Update menu.py - New Menu Structure

```python
# Clock category (4 settings)
CLOCK_SOURCE = 0
CLOCK_BPM = 1
CLOCK_RATE = 2  # NEW
CLOCK_TIMING_FEEL = 3  # NEW

# Translation category (4 settings)
TRANSLATION_MODE = 0
TRANSLATION_INPUT = 1
TRANSLATION_MIDI_FILTER = 2  # NEW
TRANSLATION_LIKELIHOOD = 3  # NEW

# Arp category (2-7 settings)
ARP_PATTERN = 0
ARP_OCTAVES = 1  # Now 0-4 instead of 1-4
# If pattern == STRUM:
ARP_STRUM_SPEED = 2
ARP_STRUM_OCTAVES = 3
ARP_STRUM_REPEAT = 4
ARP_STRUM_DIRECTION = 5
```

#### 2.2 Update display.py - Compact Notation

```python
def _format_clock_modifiers(self, settings):
    """Format clock modifiers - NEW COMPACT FORMAT"""
    if not settings.is_clock_active():
        return ""

    parts = []

    # Clock rate (only if not 1x)
    if settings.clock_rate != 3:  # 3 = 1x
        rate_names = ["/8", "/4", "/2", "1x", "2x", "4x", "8x"]
        parts.append(rate_names[settings.clock_rate])

    # Timing feel (only if not 50%)
    if settings.timing_feel != 50:
        parts.append(f"F{settings.timing_feel}%")

    if parts:
        return " (" + " ".join(parts) + ")"
    return ""

def _format_active_layers(self, settings):
    """Format active layers - AUTO-HIDE DISABLED"""
    layers = []

    # Scale (only if not Chromatic)
    if settings.is_scale_enabled():
        scale_short = self._get_scale_short_name(settings.scale_type)
        layers.append(f"Scale({scale_short})")

    # Arp (only if octaves > 0)
    if settings.is_arp_enabled():
        pattern_short = self._get_pattern_short_name(settings.pattern)

        # Add likelihood if active
        likelihood_suffix = ""
        if settings.likelihood < 100:
            likelihood_suffix = f",L{settings.likelihood}%"

        layers.append(f"Arp({pattern_short}{likelihood_suffix})")

    # Clock (only if active)
    if settings.is_clock_active() and layers:
        clk_src = "Int" if settings.clock_source == settings.CLOCK_INTERNAL else "Ext"

        # Build clock display with modifiers
        clock_parts = [clk_src]
        if settings.clock_rate != 3:
            rate_names = ["/8", "/4", "/2", "1x", "2x", "4x", "8x"]
            clock_parts.append(rate_names[settings.clock_rate])
        if settings.timing_feel != 50:
            clock_parts.append(f"F{settings.timing_feel}%")

        return " -> ".join(layers) + f" - Clk({','.join(clock_parts)})"

    elif settings.is_clock_active():
        # Only clock enabled
        return "Clk(...)"

    elif layers:
        return " -> ".join(layers)

    else:
        return "No layers active"

def update_translation_display(self, settings):
    """Update main display with Translation Hub info"""
    # Line 1: MODE and INPUT (+ MIDI Filter indicator)
    mode_text = "THRU" if settings.routing_mode == settings.ROUTING_THRU else "XLAT"
    input_text = self._format_input_source(settings.input_source)

    # Add MIDI filter indicator
    filter_indicator = ""
    if settings.midi_filter == 1:  # Vintage
        filter_indicator = " [VINTAGE]"
    elif settings.midi_filter == 2:  # Minimal
        filter_indicator = " [MINIMAL]"

    self.line1_label.text = f"MODE: {mode_text}  IN: {input_text}{filter_indicator}"

    # Line 2: CLOCK SOURCE, BPM, modifiers (compact)
    clk_src = "Int" if settings.clock_source == settings.CLOCK_INTERNAL else "Ext"
    bpm_text = str(settings.internal_bpm) if settings.clock_source == settings.CLOCK_INTERNAL else "---"

    # Compact modifiers
    modifiers = []
    if settings.clock_rate != 3:
        rate_names = ["/8", "/4", "/2", "1x", "2x", "4x", "8x"]
        modifiers.append(rate_names[settings.clock_rate])
    if settings.timing_feel != 50:
        modifiers.append(f"F{settings.timing_feel}%")

    modifier_str = " (" + " ".join(modifiers) + ")" if modifiers else ""

    self.line2_label.text = f"CLK SRC: {clk_src}  BPM: {bpm_text}{modifier_str}"

    # Line 3: TRANSLATION layers (auto-hide disabled)
    if settings.routing_mode == settings.ROUTING_TRANSLATION:
        layers_text = self._format_active_layers(settings)
        self.line3_label.text = f"XLAT: {layers_text}"
    else:
        self.line3_label.text = "PASS-THROUGH (no translation)"
```

**Deliverables:**
- ✅ Menu shows new controls
- ✅ Display uses compact notation
- ✅ Disabled layers auto-hide
- ✅ Visual feedback for all states

---

### Phase 3: Remove Old Controls & Update NVM
**Goal:** Clean up redundant settings, update storage format
**Time:** 1 day

#### 3.1 Update Settings Struct Format

```python
# OLD FORMAT (35 bytes):
# SETTINGS_STRUCT_FORMAT = 'BBBHBBBBBBBBBBBfBBBBBBBBBBB'  # 27 values

# NEW FORMAT (37 bytes): Add 4 new, remove 6 old = net +2 bytes temporarily
# Then optimize to 30 bytes after removing old settings
SETTINGS_STRUCT_FORMAT_V3 = 'BBBHBBBBBBBBBBfBBBBBBBBBBBBBBB'  # 30 values

# New magic bytes for v3 format
NVM_SETTINGS_MAGIC_V3 = b'ARP3'
```

#### 3.2 Remove Old Settings from config.py

```python
# REMOVE these:
# self.clock_multiply
# self.clock_divide
# self.swing_percent
# self.clock_enabled
# self.scale_enabled
# self.cv_enabled

# REMOVE backward compat helpers:
# get_clock_multiply_divide()
# get_swing_percent()
# (Keep is_* methods - they're useful!)
```

#### 3.3 Update save() Method

```python
def save(self):
    """Save settings to NVM - V3 FORMAT"""
    try:
        packed_data = struct.pack(
            SETTINGS_STRUCT_FORMAT_V3,
            self.pattern,
            int(self.enabled),
            self.clock_source,
            self.internal_bpm,
            self.clock_division,
            self.octave_range,  # Now 0-4 instead of 1-4
            self.midi_channel,
            int(self.velocity_passthrough),
            self.fixed_velocity,
            int(self.latch),
            self.cv_scale,  # cv_enabled removed
            self.trigger_polarity,
            self.scale_type,
            self.scale_root,
            self.gate_length,
            self.custom_cc_source,  # Disabled enum removed
            self.custom_cc_number,
            self.custom_cc_smoothing,
            # Translation Hub (v2 settings)
            self.routing_mode,
            self.input_source,
            # v3 NEW SETTINGS:
            self.clock_rate,      # Replaces multiply + divide
            self.timing_feel,     # Replaces swing + humanize
            self.midi_filter,     # Replaces vintage boolean
            self.likelihood,      # NEW
            self.strum_speed,     # NEW (for future Strum feature)
            self.strum_octaves,   # NEW
            int(self.strum_repeat),  # NEW
            self.strum_direction  # NEW
        )

        nvm_data = NVM_SETTINGS_MAGIC_V3 + packed_data
        microcontroller.nvm[NVM_SETTINGS_START:NVM_SETTINGS_START + len(nvm_data)] = nvm_data

        print(f"Settings saved to NVM ({len(packed_data)} bytes, v3 format)")
        return True

    except Exception as e:
        print(f"Failed to save settings: {e}")
        return False
```

#### 3.4 Update load() with Migration

```python
def load(self):
    """Load settings from NVM with format migration"""
    try:
        # Try v3 format first
        struct_size_v3 = struct.calcsize(SETTINGS_STRUCT_FORMAT_V3)
        total_size_v3 = len(NVM_SETTINGS_MAGIC_V3) + struct_size_v3
        nvm_data = bytes(microcontroller.nvm[NVM_SETTINGS_START:NVM_SETTINGS_START + total_size_v3])

        if nvm_data.startswith(NVM_SETTINGS_MAGIC_V3):
            # V3 format - newest
            packed_data = nvm_data[len(NVM_SETTINGS_MAGIC_V3):]
            unpacked = struct.unpack(SETTINGS_STRUCT_FORMAT_V3, packed_data)
            self._load_v3(unpacked)
            print(f"Settings loaded (v3 format, {struct_size_v3} bytes)")
            return True

        # Try v2 format (current)
        elif nvm_data.startswith(NVM_SETTINGS_MAGIC):
            print("Migrating settings from v2 to v3 format...")
            struct_size_v2 = struct.calcsize(SETTINGS_STRUCT_FORMAT)
            packed_data = nvm_data[len(NVM_SETTINGS_MAGIC):len(NVM_SETTINGS_MAGIC) + struct_size_v2]
            unpacked = struct.unpack(SETTINGS_STRUCT_FORMAT, packed_data)
            self._load_v2_and_migrate(unpacked)
            self.save()  # Save in new format
            print("Settings migrated to v3 format")
            return True

        else:
            print("No saved settings found, using defaults")
            return False

    except Exception as e:
        print(f"Failed to load settings: {e}")
        print("Using default settings")
        return False

def _load_v3(self, unpacked):
    """Load v3 format settings"""
    self.pattern = unpacked[0]
    self.enabled = bool(unpacked[1])
    self.clock_source = unpacked[2]
    self.internal_bpm = unpacked[3]
    self.clock_division = unpacked[4]
    self.octave_range = unpacked[5]  # Now 0-4
    self.midi_channel = unpacked[6]
    self.velocity_passthrough = bool(unpacked[7])
    self.fixed_velocity = unpacked[8]
    self.latch = bool(unpacked[9])
    self.cv_scale = unpacked[10]
    self.trigger_polarity = unpacked[11]
    self.scale_type = unpacked[12]
    self.scale_root = unpacked[13]
    self.gate_length = unpacked[14]
    self.custom_cc_source = unpacked[15]
    self.custom_cc_number = unpacked[16]
    self.custom_cc_smoothing = unpacked[17]
    self.routing_mode = unpacked[18]
    self.input_source = unpacked[19]
    # v3 new settings:
    self.clock_rate = unpacked[20]
    self.timing_feel = unpacked[21]
    self.midi_filter = unpacked[22]
    self.likelihood = unpacked[23]
    self.strum_speed = unpacked[24]
    self.strum_octaves = unpacked[25]
    self.strum_repeat = bool(unpacked[26])
    self.strum_direction = unpacked[27]

def _load_v2_and_migrate(self, unpacked):
    """Load v2 format and migrate to v3"""
    # Load old values
    self.pattern = unpacked[0]
    self.enabled = bool(unpacked[1])
    self.clock_source = unpacked[2]
    self.internal_bpm = unpacked[3]
    self.clock_division = unpacked[4]
    self.octave_range = max(0, unpacked[5])  # Ensure 0-4 range
    self.midi_channel = unpacked[6]
    self.velocity_passthrough = bool(unpacked[7])
    self.fixed_velocity = unpacked[8]
    self.latch = bool(unpacked[9])
    # Skip cv_enabled (unpacked[10])
    self.cv_scale = unpacked[11]
    self.trigger_polarity = unpacked[12]
    self.scale_type = unpacked[13]
    self.scale_root = unpacked[14]
    self.gate_length = unpacked[15]
    self.custom_cc_source = unpacked[16]
    self.custom_cc_number = unpacked[17]
    self.custom_cc_smoothing = unpacked[18]
    self.routing_mode = unpacked[19]
    self.input_source = unpacked[20]
    # Skip scale_enabled (unpacked[21])
    # Skip arp_enabled (unpacked[22])

    # Migrate clock settings
    clock_multiply = unpacked[23]
    clock_divide = unpacked[24]
    swing_percent = unpacked[25]
    # clock_enabled = unpacked[26]

    # Convert multiply/divide to clock_rate
    if clock_divide == 8:
        self.clock_rate = 0  # /8
    elif clock_divide == 4:
        self.clock_rate = 1  # /4
    elif clock_divide == 2:
        self.clock_rate = 2  # /2
    elif clock_multiply == 1:
        self.clock_rate = 3  # 1x
    elif clock_multiply == 2:
        self.clock_rate = 4  # 2x
    elif clock_multiply == 4:
        self.clock_rate = 5  # 4x
    else:
        self.clock_rate = 3  # Default 1x

    # Convert swing to timing_feel
    self.timing_feel = swing_percent if swing_percent >= 50 else 50

    # Default new settings
    self.midi_filter = 0  # Off
    self.likelihood = 100  # All notes
    self.strum_speed = 1  # /32
    self.strum_octaves = 1
    self.strum_repeat = False
    self.strum_direction = 0  # Up
```

**Deliverables:**
- ✅ Old settings removed from code
- ✅ New NVM format (v3) with migration
- ✅ Automatic migration from v2 to v3
- ✅ Tests updated for new format

---

### Phase 4: Update All Code References
**Goal:** Update all files that reference old settings
**Time:** 1 day

#### Files to Update:
1. **main_v2.py** - Update clock/menu initialization
2. **arp/core/clock.py** - Use timing_feel instead of swing_percent
3. **arp/core/translation.py** - Use is_scale_enabled() instead of scale_enabled
4. **arp/core/arpeggiator.py** - Use is_arp_enabled() instead of arp_enabled
5. **arp/drivers/cv_gate.py** - Remove cv_enabled checks
6. **arp/drivers/midi_custom_cc.py** - Update source enum (remove Disabled)
7. **tests/*.py** - Update all test files

#### Example Updates:

**main_v2.py:**
```python
# OLD:
clock.set_swing(settings.swing_percent)
clock.set_multiply(settings.clock_multiply)
clock.set_divide(settings.clock_divide)

# NEW:
clock.set_timing_feel(settings.timing_feel, settings.internal_bpm)
multiply, divide = settings.get_clock_multiply_divide()
clock.set_multiply(multiply)
clock.set_divide(divide)
```

**translation.py:**
```python
# OLD:
if self.settings.scale_enabled:
    self.layers.append(ScaleQuantizeLayer(self.settings))

# NEW:
if self.settings.is_scale_enabled():
    self.layers.append(ScaleQuantizeLayer(self.settings))
```

**Deliverables:**
- ✅ All code updated to use new settings
- ✅ No references to removed settings
- ✅ Clean compile

---

### Phase 5: Testing & Validation
**Goal:** Ensure everything works, no regressions
**Time:** 1 day

#### 5.1 Unit Tests
```bash
# Update existing tests
tests/test_translation.py  # Use is_scale_enabled()
tests/test_clock.py        # Use timing_feel
tests/test_input_router.py # No changes needed

# Add new tests
tests/test_timing_feel.py  # Test swing → humanize transition
tests/test_clock_rate.py   # Test unified clock rate
tests/test_midi_filter.py  # Test vintage/minimal filtering
tests/test_likelihood.py   # Test note probability

pytest tests/ -v
```

#### 5.2 Integration Tests
- [ ] Settings save/load correctly (v3 format)
- [ ] Migration from v2 to v3 works
- [ ] Menu navigation shows new controls
- [ ] Display shows correct compact notation
- [ ] Disabled layers auto-hide
- [ ] Clock Rate changes tempo correctly
- [ ] Timing Feel transitions smoothly (50% → 66% → 85%)
- [ ] MIDI Filter blocks correct messages
- [ ] Likelihood probability distribution correct

#### 5.3 Hardware Tests (if available)
- [ ] Load settings from NVM on boot
- [ ] Juno 60 with MIDI Filter Vintage mode
- [ ] Clock Rate multiply/divide timing
- [ ] Timing Feel swing and humanize
- [ ] Display updates in real-time

**Deliverables:**
- ✅ All tests passing
- ✅ No regressions
- ✅ Settings persist correctly
- ✅ Migration works

---

## After UX Redesign: New Features

Once UX redesign is complete, implement new creative features:

### Feature 1: Strum Arpeggiator Mode (3-4 days)
- Already have settings: strum_speed, strum_octaves, strum_repeat, strum_direction
- Implement pattern generation algorithm
- Add to arpeggiator.py

### Feature 2: Likelihood (Already Done!)
- Setting already added: likelihood (0-100%)
- Already have auto-detect: 100% = disabled
- Just implement probability check in arpeggiator output

### Feature 3: Timing Feel (Already Done!)
- Implemented as part of UX redesign!
- Swing (51-75%) and Humanize (76-100%) in one control

### Feature 4: MIDI Filter (Already Done!)
- Implemented as part of UX redesign!
- Vintage mode solves Juno 60 issue

**Total New Features Time:** 3-4 days (just Strum mode)

---

## Risk Management

### Potential Issues:
1. **NVM Migration Bugs** - Could lose user settings
   - Mitigation: Thorough testing of v2→v3 migration
   - Fallback: Keep old format reader for emergency

2. **Menu Navigation Confusion** - Users used to old menu
   - Mitigation: Clear names, intuitive defaults
   - Fallback: Documentation

3. **Display Overflow** - Compact notation too long
   - Mitigation: Test max-length strings
   - Fallback: Truncate or rotate display

4. **Breaking Changes** - Existing user workflows
   - Mitigation: This is v1.0-alpha, breaking changes OK
   - Fallback: Document migration path

---

## Timeline

**Total Estimated Time: 4-5 days**

| Phase | Task | Days | Done |
|-------|------|------|------|
| 1 | Add new controls (backward compat) | 1 | ☐ |
| 2 | Update menu & display | 1 | ☐ |
| 3 | Remove old controls & NVM | 1 | ☐ |
| 4 | Update all code references | 1 | ☐ |
| 5 | Testing & validation | 1 | ☐ |

---

## Success Criteria

✅ **Phase 1 Complete When:**
- New settings exist in config.py
- Helper methods work
- Backward compat verified
- All tests pass

✅ **Phase 2 Complete When:**
- Menu shows new controls
- Display uses compact notation
- Auto-hide works for disabled layers
- Visual feedback correct

✅ **Phase 3 Complete When:**
- Old settings removed
- NVM format updated (v3)
- Migration works (v2 → v3)
- All tests pass

✅ **Phase 4 Complete When:**
- No references to old settings
- All code uses new API
- Clean compile
- All tests pass

✅ **Phase 5 Complete When:**
- All unit tests pass
- Integration tests pass
- Hardware tests pass (if available)
- No regressions found

---

## Next Steps

1. **Get final approval** - Confirm this plan with user
2. **Start Phase 1** - Add new controls
3. **Daily check-ins** - Report progress
4. **Celebrate success** - Better UX unlocked! 🎉

---

**Generated:** 2025-11-01
**Author:** Claude Code (Session 16)
**Status:** Ready to Implement
**Approved:** YES - User confirmed "this kicks ass. yes! let's do it!"
