# Custom CC Output - Professional Implementation (Revised)

**Date:** 2025-11-01
**Status:** 🎯 Ready to Implement (Based on Industry Best Practices)
**Complexity:** Medium (Simplified using proven patterns)

---

## Research Summary: What the Pros Do

After researching **Expert Sleepers FH-2**, **Polyend Poly 2**, and **Intellijel MIDI 1U**, we've identified proven patterns that eliminate our custom implementation challenges:

### ✅ Key Professional Solutions:

1. **LEARN MODE** (FH-2) - Users move a physical controller, device captures CC number automatically
2. **CC SMOOTHING** (Poly 2) - Off/Low/Mid/High options prevent stepping artifacts
3. **12-bit DAC** (Poly 2) - Same as our MCP4728, confirms our hardware is professional-grade
4. **Real-time MIDI display** (FH-2) - Show incoming MIDI messages during configuration
5. **Common CC presets** - Quick access to CC 1, 74, 71, 11, 7

---

## Simplified Feature Requirements

### Core Functionality (Revised):
1. ✅ **Third output jack** - MCP4728 Channel D (0-5V)
2. ✅ **Manual CC selection** - Scroll through 0-127 with names OR use Learn Mode
3. ✅ **LEARN MODE** - Automatic CC capture (hold encoder → move controller → done!)
4. ✅ **CC Smoothing** - Off/Low/Mid/High to prevent stepping
5. ✅ **Real-time MIDI feedback** - Display last MIDI message (Custom CC menu only)
6. ✅ **MIDI pass-through** - All messages forwarded (imperceptible latency)
7. ✅ **Arpeggiator disable** - Toggle between Arp Mode and MIDI Hub Mode

### Out of Scope (Future Phases):
- ❌ LFO transmission (bandwidth issues)
- ❌ 0-10V output (requires 12V supply + op-amp)
- ❌ ±5V bipolar (requires ±12V bipolar supply)
- ❌ Scrolling CC menu (LEARN MODE replaces this!)

---

## Implementation Phases (Revised)

### Phase 1: Core Infrastructure + Learn Mode
**Goal:** Voltage conversion + automatic CC capture

**Tasks:**
1. Add Custom CC settings to `arp/utils/config.py`
   - Source type (Disabled, CC Learn, Aftertouch, Pitch Bend, Velocity)
   - CC smoothing level (Off, Low, Mid, High)
   - Last learned CC number
2. Create voltage conversion with smoothing in `cv_gate.py`
3. Implement CC Learn Mode in MIDI handler
4. Add real-time MIDI message display

**Professional Pattern:** FH-2 learn mode workflow
**Estimated Time:** 3-4 hours

---

### Phase 2: CC Smoothing Implementation
**Goal:** Prevent audible stepping artifacts

**Tasks:**
1. Implement low-pass filter for CC values
2. Add smoothing coefficients (Off=1.0, Low=0.9, Mid=0.7, High=0.5)
3. Apply smoothing only when enabled
4. Test with rapid CC changes (mod wheel sweep)

**Professional Pattern:** Polyend Poly 2 smoothing levels
**Estimated Time:** 2-3 hours

---

### Phase 3: Menu System (Simplified)
**Goal:** Simple, intuitive configuration UI

**Tasks:**
1. Add "Custom CC" menu page
2. Source selection: [Disabled / CC Learn / Aftertouch / Pitch Bend / Velocity]
3. If "CC Learn" selected:
   - Show "Press LEARN button"
   - Enter learn mode on encoder press
   - Display captured CC with name
4. Add smoothing selector (Off/Low/Mid/High)
5. Show real-time voltage output

**Professional Pattern:** FH-2 menu navigation + Poly 2 status display
**Estimated Time:** 3-4 hours

---

### Phase 4: MIDI Pass-Through Extension
**Goal:** Forward ALL MIDI message types

**Tasks:**
1. Extend `midi_output.py` pass-through for CC, Pitch Bend, Aftertouch
2. Add latency monitoring (target < 1ms)
3. Test with MIDI monitor tool

**Professional Pattern:** Universal pass-through (all devices)
**Estimated Time:** 2 hours

---

### Phase 5: Testing and Documentation
**Goal:** Verify professional-grade accuracy

**Tasks:**
1. Create `tests/custom_cc_learn_mode_test.py`
2. Test voltage accuracy with multimeter (target: ±20mV, same as Poly 2)
3. Test CC smoothing effectiveness (visual stepping test)
4. Test MIDI latency (< 1ms)
5. Document learn mode workflow

**Professional Standard:** Polyend Poly 2 accuracy (~20mV for CC outputs)
**Estimated Time:** 3 hours

---

## Detailed Technical Design

### 1. Settings Architecture (Revised)

**File:** `arp/utils/config.py`

```python
class Settings:
    # Custom CC source types
    CC_SOURCE_DISABLED = 0
    CC_SOURCE_CC = 1            # NEW: Manual selection OR Learn mode
    CC_SOURCE_AFTERTOUCH = 2
    CC_SOURCE_PITCH_BEND = 3
    CC_SOURCE_VELOCITY = 4

    # CC Smoothing levels (Polyend Poly 2 pattern)
    CC_SMOOTH_OFF = 0
    CC_SMOOTH_LOW = 1
    CC_SMOOTH_MID = 2
    CC_SMOOTH_HIGH = 3

    def __init__(self):
        # ... existing settings ...

        # Custom CC settings
        self.custom_cc_source = self.CC_SOURCE_DISABLED
        self.custom_cc_number = 1  # Default: CC 1 (Mod Wheel) - can be changed manually or via learn
        self.custom_cc_smoothing = self.CC_SMOOTH_LOW  # Default: Low smoothing

        # Learn mode state (transient, not saved to NVM)
        self.custom_cc_learn_active = False

        # Arpeggiator mode
        self.arpeggiator_enabled = True
```

---

### 2. Voltage Conversion with Smoothing (FH-2 + Poly 2 Pattern)

**File:** `arp/drivers/cv_gate.py` (extend `CVOutput` class)

```python
class CVOutput:
    # ... existing code ...

    CH_CUSTOM_CC = 3  # Channel D

    def __init__(self, dac, settings):
        # ... existing init ...
        self.custom_cc_smoothed_value = 0.0  # Smoothing state

    def cc_to_voltage_smoothed(self, cc_value):
        """
        Convert MIDI CC (0-127) to 0-5V with smoothing.
        Implements Polyend Poly 2 smoothing pattern.
        """
        target_voltage = (cc_value / 127.0) * 5.0

        # Smoothing coefficients (higher = less smoothing)
        smoothing_map = {
            Settings.CC_SMOOTH_OFF: 1.0,   # No smoothing
            Settings.CC_SMOOTH_LOW: 0.9,   # Light smoothing
            Settings.CC_SMOOTH_MID: 0.7,   # Moderate smoothing
            Settings.CC_SMOOTH_HIGH: 0.5,  # Heavy smoothing
        }

        alpha = smoothing_map[self.settings.custom_cc_smoothing]

        # Exponential moving average (low-pass filter)
        # New value = (alpha × target) + ((1 - alpha) × current)
        self.custom_cc_smoothed_value = (alpha * target_voltage) + \
                                        ((1 - alpha) * self.custom_cc_smoothed_value)

        return max(0.0, min(5.0, self.custom_cc_smoothed_value))

    def aftertouch_to_voltage(self, aftertouch_value):
        """Convert Channel Aftertouch (0-127) to 0-5V"""
        voltage = (aftertouch_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def velocity_to_voltage(self, velocity_value):
        """Convert Note Velocity (0-127) to 0-5V"""
        voltage = (velocity_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def pitch_bend_to_voltage(self, bend_value):
        """
        Convert Pitch Bend (0-16383, center=8192) to 0-5V
        WARNING: Unipolar approximation (true pitch bend needs ±5V bipolar)
        """
        voltage = (bend_value / 16383.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def set_custom_cc_voltage(self, voltage):
        """Set Custom CC output voltage (Channel D)"""
        dac_value = self.voltage_to_dac_value(voltage)
        self.dac.channel_d.raw_value = dac_value
```

---

### 3. LEARN MODE Implementation (FH-2 Pattern)

**File:** `arp/drivers/midi_custom_cc.py` (NEW FILE)

```python
"""
Custom CC Output Handler with LEARN MODE
Based on Expert Sleepers FH-2 implementation pattern.
"""

from arp.data.midi_cc_names import get_cc_short_name
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.channel_pressure import ChannelPressure
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.note_on import NoteOn

class CustomCCHandler:
    def __init__(self, cv_output, settings):
        self.cv_output = cv_output
        self.settings = settings
        self.last_received_midi = None  # For real-time display (FH-2 pattern)

    def enter_learn_mode(self):
        """
        Enter LEARN MODE (FH-2 pattern).
        Next CC message received will be captured.
        """
        self.settings.custom_cc_learn_active = True
        print("[LEARN MODE] Active - move a controller to capture CC number")

    def exit_learn_mode(self):
        """Exit LEARN MODE"""
        self.settings.custom_cc_learn_active = False
        print("[LEARN MODE] Exited")

    def process_messages(self, messages):
        """
        Process incoming MIDI messages.
        If learn mode active, capture CC number.
        Otherwise, output to Custom CC jack.
        """
        for msg in messages:
            # Store for real-time display (FH-2 pattern)
            self.last_received_midi = msg

            # LEARN MODE: Capture CC number
            if self.settings.custom_cc_learn_active:
                if isinstance(msg, ControlChange):
                    self.settings.custom_cc_number = msg.control
                    self.settings.custom_cc_source = self.settings.CC_SOURCE_CC_LEARN
                    self.settings.custom_cc_learn_active = False
                    cc_name = get_cc_short_name(msg.control)
                    print(f"[LEARNED] {cc_name}")
                    return  # Exit after learning

            # NORMAL MODE: Output to Custom CC jack
            if self.settings.custom_cc_source == self.settings.CC_SOURCE_DISABLED:
                continue

            if self.settings.custom_cc_source == self.settings.CC_SOURCE_CC_LEARN:
                if isinstance(msg, ControlChange):
                    if msg.control == self.settings.custom_cc_number:
                        voltage = self.cv_output.cc_to_voltage_smoothed(msg.value)
                        self.cv_output.set_custom_cc_voltage(voltage)

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_AFTERTOUCH:
                if isinstance(msg, ChannelPressure):
                    voltage = self.cv_output.aftertouch_to_voltage(msg.pressure)
                    self.cv_output.set_custom_cc_voltage(voltage)

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_PITCH_BEND:
                if isinstance(msg, PitchBend):
                    voltage = self.cv_output.pitch_bend_to_voltage(msg.pitch_bend)
                    self.cv_output.set_custom_cc_voltage(voltage)

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_VELOCITY:
                if isinstance(msg, NoteOn):
                    voltage = self.cv_output.velocity_to_voltage(msg.velocity)
                    self.cv_output.set_custom_cc_voltage(voltage)

    def get_last_midi_display(self):
        """
        Get last received MIDI message for display (FH-2 pattern).
        Returns: "CC#74 Value:64" or "Pitch Bend: 8192"
        """
        if self.last_received_midi is None:
            return "No MIDI received"

        msg = self.last_received_midi

        if isinstance(msg, ControlChange):
            cc_name = get_cc_short_name(msg.control)
            return f"{cc_name[:15]} V:{msg.value}"

        elif isinstance(msg, ChannelPressure):
            return f"Aftertouch: {msg.pressure}"

        elif isinstance(msg, PitchBend):
            return f"Pitch: {msg.pitch_bend}"

        elif isinstance(msg, NoteOn):
            return f"Note:{msg.note} V:{msg.velocity}"

        return "Unknown MIDI"
```

---

### 4. Menu System (Simplified)

**File:** `arp/ui/menu_manager.py` (MODIFY)

```python
def render_custom_cc_menu(self):
    """
    Render Custom CC configuration menu.
    Hybrid approach: Manual selection OR Learn Mode (best of both!)
    """
    source_names = ["Disabled", "CC", "Aftertouch", "Pitch Bend", "Velocity"]
    smooth_names = ["Off", "Low", "Mid", "High"]

    current_source = self.settings.custom_cc_source
    current_smooth = self.settings.custom_cc_smoothing

    lines = [
        "CUSTOM CC OUTPUT",
        "-" * 21,
        f"Source: {source_names[current_source]}",
    ]

    # If CC mode selected
    if current_source == Settings.CC_SOURCE_CC:
        cc_name = get_cc_short_name(self.settings.custom_cc_number)
        lines.append(cc_name[:21])  # "CC 74: Filter Cutoff"

        # Show LEARN prompt or LEARNING status
        if self.settings.custom_cc_learn_active:
            lines.append("LEARNING... move ctrl")
        else:
            lines.append("Turn to change/Hold=LEARN")

    # Show smoothing setting
    lines.append(f"Smooth: {smooth_names[current_smooth]}")

    # Real-time MIDI feedback (only in Custom CC menu)
    last_midi = self.custom_cc_handler.get_last_midi_display()
    lines.append(last_midi[:21])

    self.display_lines(lines)

# Encoder interaction:
# - Turn encoder: Scroll CC number 0-127 (shows name)
# - Hold encoder: Enter LEARN MODE (next CC received sets the number)
# - Press encoder: (navigate menu as usual)
```

---

### 5. MIDI Pass-Through Extension

**File:** `arp/drivers/midi_output.py` (MODIFY)

```python
def process_passthrough(self, messages, channel=0):
    """
    Pass ALL MIDI messages through unchanged.
    Professional pattern: Universal pass-through.
    """
    for msg in messages:
        self.midi_out.send(msg, channel=channel)
        self.has_sent_midi = True
```

**That's it!** No complex filtering, just send everything.

---

## Hardware Integration

### MCP4728 Channel D Wiring:

```
MCP4728 Channel D (OUTD):
  └──→ TRS Jack Tip (Custom CC output, 0-5V)

TRS Jack Sleeve → Ground
TRS Jack Ring → Not connected (or duplicate Tip)
```

**Parts:**
- 1× Switchcraft 112BX or equivalent TRS jack (1/8" / 3.5mm)
- Wire: 22 AWG solid core

---

## Testing Strategy

### Professional Accuracy Standard (Polyend Poly 2):
- **Target:** ±20mV accuracy for non-calibrated CC outputs
- **Method:** Multimeter measurement at CC 0, 64, 127
- **Expected:**
  - CC 0 → 0.000V ± 0.020V
  - CC 64 → 2.520V ± 0.020V
  - CC 127 → 5.000V ± 0.020V

### Smoothing Test:
- Send rapid CC changes (0 → 127 → 0 repeated)
- Observe with oscilloscope or multimeter
- Off: Immediate stepping
- Low: Slight smoothing
- Mid: Moderate smoothing
- High: Heavy smoothing (slow response)

### Learn Mode Test:
```
1. Enter Custom CC menu
2. Select "CC Learn" source
3. Hold encoder button → LEARN MODE active
4. Move mod wheel on MIDI controller
5. Device displays "CC 1: Mod Wheel" ✓
6. Move mod wheel again → voltage changes on jack ✓
```

---

## User Workflow (Hybrid: Manual + Learn Mode)

### Scenario: User wants to control filter cutoff with mod wheel

**WORKFLOW 1: Manual Selection (Power User)**
1. Enter Custom CC menu
2. Select "CC" as source
3. Turn encoder to scroll CC numbers
4. See "CC 74: Filter Cutoff"
5. Press to confirm
6. Done! ✓

**WORKFLOW 2: Learn Mode (Beginner-Friendly)**
1. Enter Custom CC menu
2. Select "CC" as source
3. Hold encoder button → LEARN MODE
4. Move mod wheel on controller
5. Device displays "CC 1: Mod Wheel" (auto-captured)
6. Done! ✓

**WORKFLOW 3: Quick Setup (No Controller Connected)**
1. Enter Custom CC menu
2. Select "CC" as source
3. Manually set to CC 74 (you know what you want)
4. Connect controller later
5. Done! ✓

**Best of all worlds!** Manual control + automatic learn + offline configuration.

---

## Success Criteria (Professional Standards)

✅ **Voltage Accuracy:**
- ±20mV tolerance (matches Polyend Poly 2)
- 12-bit resolution verified

✅ **LEARN MODE:**
- One-button CC capture
- Instant visual feedback
- Display CC name after learning

✅ **Smoothing:**
- Off/Low/Mid/High options
- No audible stepping at Mid/High settings
- Immediate response at Off

✅ **Latency:**
- MIDI pass-through < 1ms
- No audible delay

✅ **UI/UX:**
- Real-time MIDI message display
- Clear learn mode prompts
- Simple menu navigation

---

## Implementation Checklist

### Phase 1: Core Infrastructure + Learn Mode ✅
- [ ] Add settings to `config.py` (source, smoothing, learn mode state)
- [ ] Implement smoothing in `cv_gate.py`
- [ ] Create `CustomCCHandler` with learn mode
- [ ] Test learn mode capture

### Phase 2: CC Smoothing ✅
- [ ] Implement exponential moving average filter
- [ ] Add smoothing coefficients (Off/Low/Mid/High)
- [ ] Test with rapid CC changes

### Phase 3: Menu System ✅
- [ ] Add "Custom CC" menu page
- [ ] Implement learn mode UI workflow
- [ ] Add real-time MIDI display
- [ ] Add smoothing selector

### Phase 4: MIDI Pass-Through ✅
- [ ] Extend pass-through for all message types
- [ ] Measure latency

### Phase 5: Testing ✅
- [ ] Voltage accuracy test (±20mV target)
- [ ] Smoothing effectiveness test
- [ ] Learn mode workflow test
- [ ] MIDI latency test

---

## References

### Professional Implementations:
- **Expert Sleepers FH-2:** Learn mode, real-time MIDI display, 384 mappings
- **Polyend Poly 2:** 12-bit DAC, CC smoothing (Off/Low/Mid/High), ~20mV accuracy
- **Intellijel MIDI 1U:** Modular approach, computer configuration tool

### Technical Resources:
- FH-2 Manual: https://www.expert-sleepers.co.uk/downloads/manuals/fh2_user_manual_1.3.pdf
- Poly 2 Manual: https://polyend.com/manuals/poly2-manual/
- CircuitPython MIDI: https://learn.adafruit.com/circuitpython-midi-to-cv-skull

### Our Documentation:
- `docs/hardware/MIDI_TO_CV_VOLTAGE_STANDARDS.md`
- `arp/data/midi_cc_names.py`
- `arp/drivers/cv_gate.py`

---

## Estimated Total Time: 13-16 hours

**Compared to original plan:** -1 to -3 hours savings by eliminating CC scrolling menu!

**Next Steps:**
1. Review with user for approval
2. Begin Phase 1 (Core + Learn Mode)
3. Test incrementally
4. Deploy to hardware

---

**Key Insight:** By adopting proven professional patterns (LEARN MODE, CC smoothing, real-time MIDI display), we eliminate complexity, reduce implementation time, and deliver a better user experience. No need to reinvent the wheel!
