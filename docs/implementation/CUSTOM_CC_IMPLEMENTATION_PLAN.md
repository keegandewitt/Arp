# Custom CC Output - Sequential Implementation Plan

**Date:** 2025-11-01
**Status:** 🎯 Implementation Ready
**Complexity:** High (Multi-component integration)

---

## Executive Summary

Implement a third 1/8" TRS jack that outputs user-selectable MIDI CC values as CV voltage (0-5V). Users can choose which incoming MIDI message (CC, Aftertouch, Pitch Bend, or Velocity) outputs to this jack via menu. All MIDI messages pass through to MIDI OUT with imperceptible latency.

**Scope:** Phase 1 - 0-5V unipolar output (no hardware modifications required)

---

## Feature Requirements

### Core Functionality:
1. ✅ **Third output jack** - Uses MCP4728 Channel D (currently available)
2. ✅ **User-selectable source** - Menu to choose: CC (0-127), Aftertouch, Pitch Bend, Velocity, or Disabled
3. ✅ **MIDI pass-through** - All messages forward to MIDI OUT (imperceptible latency)
4. ✅ **CC name display** - Show human-readable names in menu (e.g., "CC 74: Filter Cutoff")
5. ✅ **Arpeggiator disable** - Key function to toggle arp mode (device becomes MIDI hub + CV converter)
6. ✅ **Monophonic warning** - UI and documentation clarify CV output is monophonic

### Out of Scope (Future Phases):
- ❌ LFO transmission (too much latency)
- ❌ 0-10V output (requires op-amp + 12V supply)
- ❌ ±5V bipolar output (requires ±12V bipolar supply)

---

## Implementation Phases

### Phase 1: Core Infrastructure (Foundation)
**Goal:** Set up data structures, settings, and voltage conversion without touching UI

**Tasks:**
1. Add Custom CC settings to `arp/utils/config.py`
2. Create voltage conversion functions for each message type
3. Extend `CVOutput` class to support Custom CC on Channel D
4. Write unit tests for voltage conversion accuracy

**Dependencies:** None
**Risk:** Low
**Estimated Time:** 2-3 hours

---

### Phase 2: MIDI Message Handling (Data Flow)
**Goal:** Capture incoming MIDI messages and route to Custom CC output

**Tasks:**
1. Extend `MidiIO.read_messages()` to capture CC, Aftertouch, Pitch Bend, Velocity
2. Create `CustomCCHandler` class to process selected message type
3. Extend MIDI pass-through to forward ALL message types (not just NoteOn/NoteOff)
4. Add latency monitoring (measure time from USB IN to MIDI OUT)

**Dependencies:** Phase 1 complete
**Risk:** Medium (pass-through latency critical)
**Estimated Time:** 3-4 hours

---

### Phase 3: Menu System (User Interface)
**Goal:** Allow users to configure Custom CC source and CC number

**Tasks:**
1. Add "Custom CC" menu page to `arp/ui/menu_manager.py`
2. Integrate CC name lookup from `midi_cc_names.py`
3. Create submenu for CC number selection (0-127 with names)
4. Add visual indicator for current Custom CC source (OLED status line)
5. Save/load settings to NVM

**Dependencies:** Phase 1 & 2 complete
**Risk:** Medium (menu navigation UX)
**Estimated Time:** 4-5 hours

---

### Phase 4: Arpeggiator Disable Function (Mode Switching)
**Goal:** Allow toggling between Arp Mode and MIDI Hub Mode

**Tasks:**
1. Add key handler for long-press or double-press encoder button
2. Create `MIDIHubMode` state (arp disabled, all notes pass through)
3. Update UI to show current mode ("ARP" vs "MIDI HUB")
4. Ensure CV outputs still work in MIDI Hub mode (monophonic last-note priority)
5. Document mode switching in user manual

**Dependencies:** Phase 2 complete
**Risk:** Low
**Estimated Time:** 2-3 hours

---

### Phase 5: Testing and Validation (Quality Assurance)
**Goal:** Verify all functionality works correctly with real hardware

**Tasks:**
1. Create `tests/custom_cc_hardware_test.py` (cycles through all message types)
2. Test with multimeter: verify voltage accuracy for CC (0-5V), Aftertouch, Velocity
3. Test MIDI pass-through latency with MIDI monitor tool
4. Test menu navigation and settings persistence
5. Test arpeggiator disable mode with external synth
6. Document monophonic limitation with test cases

**Dependencies:** All phases complete
**Risk:** Low
**Estimated Time:** 3-4 hours

---

## Detailed Technical Design

### 1. Settings Architecture

**File:** `arp/utils/config.py`

```python
class Settings:
    # Custom CC source types
    CC_SOURCE_DISABLED = 0
    CC_SOURCE_CC = 1
    CC_SOURCE_AFTERTOUCH = 2
    CC_SOURCE_PITCH_BEND = 3
    CC_SOURCE_VELOCITY = 4

    def __init__(self):
        # ... existing settings ...

        # Custom CC settings
        self.custom_cc_source = self.CC_SOURCE_DISABLED
        self.custom_cc_number = 74  # Default: Filter Cutoff (common)

        # Arpeggiator mode
        self.arpeggiator_enabled = True  # New: toggle arp on/off
```

**Storage:** Use existing NVM storage mechanism in `config.py`

---

### 2. Voltage Conversion Functions

**File:** `arp/drivers/cv_gate.py` (extend `CVOutput` class)

```python
class CVOutput:
    # ... existing code ...

    CH_CUSTOM_CC = 3  # Channel D for Custom CC output

    def cc_to_voltage(self, cc_value):
        """
        Convert MIDI CC (0-127) to 0-5V
        Linear scaling: 0 → 0V, 127 → 5V
        """
        voltage = (cc_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def aftertouch_to_voltage(self, aftertouch_value):
        """
        Convert Channel Aftertouch (0-127) to 0-5V
        Identical to CC conversion
        """
        voltage = (aftertouch_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def velocity_to_voltage(self, velocity_value):
        """
        Convert Note Velocity (0-127) to 0-5V
        0 = silent (0V), 127 = max velocity (5V)
        """
        voltage = (velocity_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def pitch_bend_to_voltage(self, bend_value):
        """
        Convert Pitch Bend (0-16383, center=8192) to 0-5V
        WARNING: This is unipolar approximation!
        Center (8192) → 2.5V
        Min (0) → 0V
        Max (16383) → 5V

        NOTE: True pitch bend should be ±5V bipolar.
        This is a compromise for Phase 1 (0-5V only).
        """
        voltage = (bend_value / 16383.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def set_custom_cc_voltage(self, voltage):
        """Set Custom CC output voltage (Channel D)"""
        dac_value = self.voltage_to_dac_value(voltage)
        self.dac.channel_d.raw_value = dac_value
```

**Reference:** See `docs/hardware/MIDI_TO_CV_VOLTAGE_STANDARDS.md` for voltage formulas

---

### 3. MIDI Message Handler

**File:** `arp/drivers/midi_custom_cc.py` (NEW FILE)

```python
"""
Custom CC Output Handler
Monitors incoming MIDI messages and outputs selected message to Custom CC jack.
"""

from arp.data.midi_cc_names import get_cc_short_name, get_cc_full_name

class CustomCCHandler:
    def __init__(self, cv_output, settings):
        self.cv_output = cv_output
        self.settings = settings
        self.last_cc_values = {}  # Store last value per CC number
        self.last_velocity = 0
        self.last_aftertouch = 0
        self.last_pitch_bend = 8192  # Center position

    def process_messages(self, messages):
        """
        Process incoming MIDI messages and update Custom CC output.
        This does NOT consume messages - they still pass through to MIDI OUT.
        """
        if self.settings.custom_cc_source == self.settings.CC_SOURCE_DISABLED:
            return

        for msg in messages:
            if self.settings.custom_cc_source == self.settings.CC_SOURCE_CC:
                if isinstance(msg, adafruit_midi.ControlChange):
                    if msg.control == self.settings.custom_cc_number:
                        voltage = self.cv_output.cc_to_voltage(msg.value)
                        self.cv_output.set_custom_cc_voltage(voltage)
                        self.last_cc_values[msg.control] = msg.value

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_AFTERTOUCH:
                if isinstance(msg, adafruit_midi.ChannelPressure):
                    voltage = self.cv_output.aftertouch_to_voltage(msg.pressure)
                    self.cv_output.set_custom_cc_voltage(voltage)
                    self.last_aftertouch = msg.pressure

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_PITCH_BEND:
                if isinstance(msg, adafruit_midi.PitchBend):
                    voltage = self.cv_output.pitch_bend_to_voltage(msg.pitch_bend)
                    self.cv_output.set_custom_cc_voltage(voltage)
                    self.last_pitch_bend = msg.pitch_bend

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_VELOCITY:
                if isinstance(msg, adafruit_midi.NoteOn):
                    voltage = self.cv_output.velocity_to_voltage(msg.velocity)
                    self.cv_output.set_custom_cc_voltage(voltage)
                    self.last_velocity = msg.velocity

    def get_current_value_display(self):
        """
        Get current Custom CC value for UI display.
        Returns: (value, voltage) tuple
        """
        source = self.settings.custom_cc_source

        if source == self.settings.CC_SOURCE_DISABLED:
            return ("Off", 0.0)

        elif source == self.settings.CC_SOURCE_CC:
            cc_num = self.settings.custom_cc_number
            value = self.last_cc_values.get(cc_num, 0)
            voltage = self.cv_output.cc_to_voltage(value)
            return (f"{value}", voltage)

        elif source == self.settings.CC_SOURCE_AFTERTOUCH:
            voltage = self.cv_output.aftertouch_to_voltage(self.last_aftertouch)
            return (f"{self.last_aftertouch}", voltage)

        elif source == self.settings.CC_SOURCE_PITCH_BEND:
            voltage = self.cv_output.pitch_bend_to_voltage(self.last_pitch_bend)
            return (f"{self.last_pitch_bend}", voltage)

        elif source == self.settings.CC_SOURCE_VELOCITY:
            voltage = self.cv_output.velocity_to_voltage(self.last_velocity)
            return (f"{self.last_velocity}", voltage)

        return ("?", 0.0)
```

---

### 4. MIDI Pass-Through Extension

**File:** `arp/drivers/midi_output.py` (MODIFY)

**Current implementation only passes NoteOn/NoteOff. Must extend for all message types.**

```python
# BEFORE (current code):
def process_passthrough(self, messages, channel=0):
    """Pass MIDI messages through unchanged"""
    for msg in messages:
        if isinstance(msg, NoteOn):
            self.midi_out.send(msg, channel=channel)
        elif isinstance(msg, NoteOff):
            self.midi_out.send(msg, channel=channel)

# AFTER (new code):
def process_passthrough(self, messages, channel=0):
    """
    Pass ALL MIDI messages through unchanged.
    Supports: NoteOn, NoteOff, CC, PitchBend, Aftertouch, etc.
    """
    for msg in messages:
        # Pass through ALL message types
        self.midi_out.send(msg, channel=channel)
        self.has_sent_midi = True
```

**Critical:** This change enables imperceptible latency pass-through for all MIDI data.

---

### 5. Menu System Integration

**File:** `arp/ui/menu_manager.py` (MODIFY)

**Add new menu page:** "Custom CC"

```python
# Menu structure:
# Main Menu
#   ├─ Settings
#   ├─ CV/Gate
#   ├─ Custom CC ← NEW
#   │   ├─ Source: [Disabled/CC/Aftertouch/Pitch Bend/Velocity]
#   │   └─ CC Number: [0-127 with names] (only shown if Source = CC)
#   └─ About

class MenuPage:
    # ... existing pages ...
    CUSTOM_CC = 5  # New page ID

# In menu rendering:
def render_custom_cc_menu(self):
    """Render Custom CC configuration menu"""
    source_names = ["Disabled", "CC", "Aftertouch", "Pitch Bend", "Velocity"]
    current_source = self.settings.custom_cc_source

    lines = [
        "CUSTOM CC OUTPUT",
        "-" * 21,
        f"Source: {source_names[current_source]}",
    ]

    # If CC selected, show CC number with name
    if current_source == Settings.CC_SOURCE_CC:
        cc_num = self.settings.custom_cc_number
        cc_name = get_cc_short_name(cc_num)
        lines.append(cc_name[:21])  # Truncate to OLED width

    # Show current value and voltage
    value, voltage = self.custom_cc_handler.get_current_value_display()
    lines.append(f"Value: {value} ({voltage:.2f}V)")

    self.display_lines(lines)
```

**CC Number Selection Submenu:**
- Use rotary encoder to scroll through 0-127
- Display: "CC 74: Filter Cutoff" (from `midi_cc_names.py`)
- Highlight commonly used CCs (1, 7, 10, 11, 64, 71, 74)

---

### 6. Arpeggiator Disable Function

**File:** `arp/ui/button_handler.py` (MODIFY)

**Add long-press detection for encoder button:**

```python
class ButtonHandler:
    def __init__(self):
        self.last_press_time = 0
        self.long_press_threshold = 1000  # 1 second long press

    def check_long_press(self):
        """Detect long press to toggle arpeggiator mode"""
        current_time = time.monotonic_ns() // 1_000_000

        if button_pressed and not button_was_pressed:
            self.last_press_time = current_time

        if button_pressed and (current_time - self.last_press_time) > self.long_press_threshold:
            # Toggle arpeggiator enabled/disabled
            self.settings.arpeggiator_enabled = not self.settings.arpeggiator_enabled
            return True

        return False
```

**UI Feedback:**
- Show "ARP MODE" or "MIDI HUB" in status line
- Brief message: "Arpeggiator Disabled" / "Arpeggiator Enabled"

---

## Hardware Integration

### MCP4728 Channel Allocation:

| Channel | Function | Voltage Range | Status |
|---------|----------|---------------|--------|
| A | CV Pitch (1V/oct or 1.035V/oct) | 0-5V | ✅ In Use |
| B | **Available** (future: CV Velocity) | 0-5V | ⚪ Reserved |
| C | V-Trig Gate (standard gate) | 0V idle, 5V active | ✅ In Use |
| D | **Custom CC Output** | 0-5V | 🟢 Implement Here |

### Physical Jack Wiring:

**Third Jack: "CUSTOM CC" (1/8" TRS)**
```
MCP4728 Channel D (OUTD):
  └──→ TRS Jack Tip (Custom CC output)

TRS Jack Sleeve → Ground
TRS Jack Ring → Not connected (or duplicate Tip for mono compatibility)
```

**Parts Required:**
- 1× Switchcraft 112BX or equivalent TRS jack (1/8" / 3.5mm)
- Wire: 22 AWG solid core for breadboard

---

## Testing Strategy

### Unit Tests (Software):

1. **Voltage Conversion Accuracy:**
   - CC 0 → 0.000V ✓
   - CC 64 → 2.520V ✓
   - CC 127 → 5.000V ✓
   - Aftertouch 0 → 0.000V ✓
   - Pitch Bend 8192 → 2.500V (center) ✓

2. **Message Routing:**
   - CC message routed to Custom CC output AND passed to MIDI OUT ✓
   - Latency < 1ms (imperceptible) ✓

### Hardware Tests:

**File:** `tests/custom_cc_hardware_test.py`

```python
"""
Custom CC Hardware Test
Cycles through all message types and displays voltage on OLED.
Measure with multimeter to verify accuracy.
"""

test_sequence = [
    ("CC 74 = 0", CC, 74, 0, 0.000),
    ("CC 74 = 64", CC, 74, 64, 2.520),
    ("CC 74 = 127", CC, 74, 127, 5.000),
    ("Aftertouch = 64", Aftertouch, None, 64, 2.520),
    ("Pitch Bend = 8192", PitchBend, None, 8192, 2.500),
    ("Velocity = 100", Velocity, None, 100, 3.937),
]

# Cycle through each test case, display on OLED, wait 3 seconds
```

### Integration Tests:

1. **MIDI Hub Mode Test:**
   - Disable arpeggiator via long-press
   - Play notes on MIDI keyboard
   - Verify notes pass through to MIDI OUT
   - Verify CV Pitch outputs last note (monophonic) ✓

2. **Custom CC Live Test:**
   - Connect MIDI controller with mod wheel (CC 1)
   - Set Custom CC source to CC 1
   - Move mod wheel, observe voltage change on multimeter ✓

---

## Risk Mitigation

### Risk 1: MIDI Pass-Through Latency
**Severity:** High
**Mitigation:**
- Profile `process_passthrough()` execution time
- Ensure < 1ms latency (imperceptible)
- Consider DMA if latency detected (unlikely with CircuitPython)

### Risk 2: Menu UX Complexity
**Severity:** Medium
**Mitigation:**
- Use hierarchical menu (Source selection → CC number selection)
- Highlight commonly used CCs (CC 1, 7, 74, etc.)
- Show real-time voltage feedback

### Risk 3: Monophonic CV Confusion
**Severity:** Medium
**Mitigation:**
- Display "MONO" indicator in UI when CV outputs active
- Document in user manual with clear examples
- Show last-note priority behavior in tests

---

## Documentation Requirements

### User Manual Updates:

1. **Custom CC Feature:**
   - Explanation of 0-5V output range
   - How to select MIDI CC source
   - Common CC assignments (filter, resonance, volume, etc.)
   - Monophonic limitation warning

2. **MIDI Hub Mode:**
   - How to disable arpeggiator (long-press encoder)
   - Use cases: MIDI routing, CV conversion for hardware synths
   - CV output behavior when arp disabled (last-note priority)

3. **Cable Guide:**
   - Use TS (mono) or TRS cable for Custom CC output
   - Voltage compatibility with Eurorack (0-5V standard)

### Code Documentation:

- Inline comments for all voltage conversion formulas
- Reference to `MIDI_TO_CV_VOLTAGE_STANDARDS.md`
- Docstrings for all new classes and methods

---

## Implementation Checklist

### Phase 1: Core Infrastructure ✅
- [ ] Add Custom CC settings to `config.py`
- [ ] Create voltage conversion functions in `cv_gate.py`
- [ ] Extend `CVOutput` class for Channel D
- [ ] Write unit tests for voltage accuracy

### Phase 2: MIDI Message Handling ✅
- [ ] Create `CustomCCHandler` class (`midi_custom_cc.py`)
- [ ] Extend MIDI pass-through for ALL message types
- [ ] Add latency monitoring
- [ ] Test with MIDI monitor tool

### Phase 3: Menu System ✅
- [ ] Add "Custom CC" menu page
- [ ] Integrate CC name lookup from `midi_cc_names.py`
- [ ] Create CC number selection submenu
- [ ] Add visual indicator for current source
- [ ] Save/load settings to NVM

### Phase 4: Arpeggiator Disable ✅
- [ ] Add long-press detection to button handler
- [ ] Create MIDI Hub mode state
- [ ] Update UI to show current mode
- [ ] Test CV output in MIDI Hub mode
- [ ] Document mode switching

### Phase 5: Testing ✅
- [ ] Create `custom_cc_hardware_test.py`
- [ ] Test voltage accuracy with multimeter
- [ ] Measure MIDI pass-through latency
- [ ] Test menu navigation and persistence
- [ ] Test arpeggiator disable with external synth
- [ ] Document monophonic behavior

---

## Success Criteria

✅ **Functional:**
- Custom CC jack outputs accurate voltage (±10mV tolerance)
- MIDI pass-through latency < 1ms (imperceptible)
- Menu allows source selection with CC names
- Arpeggiator disable mode works correctly
- All MIDI message types supported (CC, Aftertouch, Pitch Bend, Velocity)

✅ **User Experience:**
- Menu is intuitive and responsive
- Real-time voltage feedback visible on OLED
- Mode switching is clear and reliable
- Monophonic limitation is clearly communicated

✅ **Code Quality:**
- All functions have docstrings
- Unit tests pass with 100% coverage
- Hardware tests validate accuracy
- No performance regressions

---

## Future Enhancements (Post-Phase 1)

### Phase 2: 0-10V Output
- Add op-amp circuit with 2× gain
- Require 12V power supply
- Software: scale voltage formulas × 2

### Phase 3: ±5V Bipolar Output
- Add bipolar power supply (±12V)
- Add offset/invert op-amp circuit
- Software: implement true bipolar pitch bend
- Support LFO modulation (if latency acceptable)

### Phase 4: Polyphonic CV (Multiple Jacks)
- Use MCP4728 Channel B for second voice
- Allocate notes round-robin or by priority
- Document polyphonic vs monophonic modes

---

## References

- **Voltage Standards:** `docs/hardware/MIDI_TO_CV_VOLTAGE_STANDARDS.md`
- **MIDI CC Names:** `arp/data/midi_cc_names.py`
- **Existing CV Implementation:** `arp/drivers/cv_gate.py`
- **MIDI I/O:** `arp/drivers/midi_output.py`
- **Pin Allocation:** `docs/hardware/PIN_ALLOCATION_MATRIX.md`

---

**Next Steps:**
1. Review this plan with user for approval
2. Begin Phase 1 implementation (core infrastructure)
3. Test each phase incrementally before proceeding
4. Deploy to hardware and verify with multimeter

**Estimated Total Time:** 14-19 hours (spread across 5 phases)
