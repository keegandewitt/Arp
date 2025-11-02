# Polyphony vs Monophony Handling Design

**Created:** 2025-11-02 (Session 19)
**Purpose:** Define how prisme handles polyphonic MIDI input vs monophonic CV output
**Status:** Design Complete - Ready for Implementation

---

## Executive Summary

**Problem:** prisme receives MIDI input (polyphonic - up to 16 simultaneous notes per channel) but outputs to both:
- **MIDI OUT** - Polyphonic capable (16+ notes)
- **CV/Gate OUT** - Monophonic only (1 note at a time)

**Solution:** Implement dual routing paths with note priority strategies for monophonic outputs.

---

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Routing Scenarios](#routing-scenarios)
3. [Note Priority Strategies](#note-priority-strategies)
4. [Architecture Design](#architecture-design)
5. [Implementation Details](#implementation-details)
6. [Settings & UI](#settings--ui)
7. [Testing Strategy](#testing-strategy)

---

## Core Concepts

### Polyphonic vs Monophonic

**Polyphonic:**
- Multiple notes can play simultaneously
- MIDI protocol supports 128 notes across 16 channels (theoretically unlimited)
- Examples: MIDI OUT, USB MIDI, multi-timbral synths

**Monophonic:**
- Only one note can play at a time
- CV/Gate outputs: 1 pitch voltage + 1 gate signal = 1 note
- Examples: CV OUT, most vintage analog synths, monosynths

### Why This Matters

**Scenario 1 - Polyphonic MIDI → Polyphonic MIDI:**
```
Input:  C + E + G (chord)
Scale:  C Major (no change)
Arp:    OFF (disabled)
Output: C + E + G (all 3 notes simultaneously)
```
✅ **Works:** All notes pass through with scale quantization

**Scenario 2 - Polyphonic MIDI → Monophonic CV:**
```
Input:  C + E + G (chord)
Arp:    OFF (disabled)
CV OUT: ??? Which note? All 3 can't play at once!
```
❌ **Problem:** Need note priority strategy

**Scenario 3 - Polyphonic MIDI → Arpeggiator → MIDI:**
```
Input:  C + E + G (chord held)
Arp:    UP pattern, enabled
Output: C → E → G → C → E → G (sequential)
```
✅ **Works:** Arpeggiator buffers notes and plays sequentially (already monophonic)

---

## Routing Scenarios

### Scenario Matrix

| Arp Enabled | Scale Enabled | Output Type | Behavior | Polyphony |
|-------------|---------------|-------------|----------|-----------|
| ✅ ON | ✅ ON | MIDI | Arpeggio of quantized notes | Mono (arped) |
| ✅ ON | ✅ ON | CV/Gate | Arpeggio of quantized notes | Mono (arped) |
| ✅ ON | ❌ OFF | MIDI | Arpeggio of input notes | Mono (arped) |
| ✅ ON | ❌ OFF | CV/Gate | Arpeggio of input notes | Mono (arped) |
| ❌ OFF | ✅ ON | MIDI | Quantized notes pass-through | **Poly** |
| ❌ OFF | ✅ ON | CV/Gate | Quantized notes **→ NEED PRIORITY** | **Mono** |
| ❌ OFF | ❌ OFF | MIDI | Direct pass-through | **Poly** |
| ❌ OFF | ❌ OFF | CV/Gate | Direct notes **→ NEED PRIORITY** | **Mono** |

### Critical Insight

**When Arpeggiator is ENABLED:** Already monophonic (buffer → sequential output)
**When Arpeggiator is DISABLED:** Need note priority for CV/Gate output

---

## Note Priority Strategies

### 1. Highest Note Priority (Most Common for Lead)

**Behavior:** Play the highest pitched note
**Use Case:** Lead synth lines, solos, melodies
**Example:**
```
Hold C3 → CV outputs C3
Add E3  → CV outputs E3 (higher)
Add G3  → CV outputs G3 (highest)
Release G3 → CV outputs E3 (now highest)
Release E3 → CV outputs C3 (only remaining)
```

**Implementation:**
```python
selected_note = max(active_notes, key=lambda x: x[0])
```

---

### 2. Lowest Note Priority (Bass Lines)

**Behavior:** Play the lowest pitched note
**Use Case:** Bass synth, sub-oscillators, foundation notes
**Example:**
```
Hold E3 → CV outputs E3
Add C3  → CV outputs C3 (lower)
Add G3  → CV outputs C3 (still lowest)
Release C3 → CV outputs E3 (now lowest)
```

**Implementation:**
```python
selected_note = min(active_notes, key=lambda x: x[0])
```

---

### 3. Last Note Priority (Most Recent)

**Behavior:** Play the most recently pressed note
**Use Case:** Expressive playing, monophonic synth feel, legato
**Example:**
```
Hold C3 → CV outputs C3
Hold E3 → CV outputs E3 (most recent)
Hold G3 → CV outputs G3 (most recent)
Release G3 → CV outputs E3 (last remaining held)
```

**Why this is different from Highest:**
```
Play C3 → E3 → C4 (high) → C3 again
- Highest priority: C4 (highest pitch)
- Last priority: C3 (most recently pressed)
```

**Implementation:**
```python
selected_note = active_notes[-1]  # Last in list
```

---

### 4. First Note Priority (Earliest)

**Behavior:** Play the first note pressed, ignore additional notes
**Use Case:** Drone synth, sustained pedal tones
**Example:**
```
Hold C3 → CV outputs C3
Hold E3 → CV outputs C3 (still first)
Hold G3 → CV outputs C3 (still first)
Release C3 → CV outputs E3 (now first of remaining)
```

**Implementation:**
```python
selected_note = active_notes[0]  # First in list
```

---

### Default Recommendation

**Default:** **Last Note Priority**
- Most natural for monophonic synth playing
- Matches behavior of most analog monosynths (Minimoog, SH-101, etc.)
- Allows expressive playing without fighting the priority logic

---

## Architecture Design

### Component Responsibilities

#### 1. **Input Router** (main.py)
- Receives MIDI from USB or UART
- Routes to appropriate processing path based on settings
- **New:** Detects polyphonic vs monophonic output requirements

#### 2. **Translation Pipeline** (translation.py)
- Processes notes through Scale → Arp or Arp → Scale layers
- **Current:** Designed for monophonic (arp buffering)
- **New:** Add polyphonic pass-through when Arp OFF

#### 3. **CV Output Driver** (cv_gate.py)
- Outputs to MCP4728 DAC (CV pitch) and GPIO (gate)
- **Current:** Receives single note at a time
- **New:** Maintain active notes list, apply priority

#### 4. **Arpeggiator** (arpeggiator.py)
- Buffers notes and generates sequences
- **Current:** Already monophonic by design
- **New:** No changes needed (already correct)

---

### Routing Path Decision Tree

```
MIDI Input (Note On/Off)
│
├─ ROUTING_THRU mode?
│  └─ YES → Pass through immediately (polyphonic)
│
└─ ROUTING_TRANSLATION mode
   │
   ├─ Arpeggiator ENABLED?
   │  └─ YES → Buffer note for arpeggiation (monophonic)
   │     │
   │     └─ On arp step:
   │        ├─ Send to MIDI OUT (monophonic arped sequence)
   │        └─ Send to CV OUT (monophonic arped sequence)
   │
   └─ Arpeggiator DISABLED
      │
      ├─ Scale quantization ENABLED?
      │  └─ YES → Quantize note
      │
      └─ Output routing:
         ├─ MIDI OUT → Send immediately (polyphonic)
         └─ CV OUT → Apply note priority (monophonic)
```

---

## Implementation Details

### 1. Settings (config.py)

**Add note priority constants:**
```python
# Note priority strategies (for monophonic CV output)
NOTE_PRIORITY_HIGHEST = 0  # Play highest note (lead)
NOTE_PRIORITY_LOWEST = 1   # Play lowest note (bass)
NOTE_PRIORITY_LAST = 2     # Play most recent note (default)
NOTE_PRIORITY_FIRST = 3    # Play first note (drone)

NOTE_PRIORITY_NAMES = [
    "Highest",
    "Lowest",
    "Last",
    "First"
]
```

**Add to Settings class:**
```python
class Settings:
    def __init__(self):
        # ... existing settings ...

        # CV/Gate monophonic note priority
        self.note_priority = NOTE_PRIORITY_LAST  # Default: Last note

    def _load_defaults(self):
        # ... existing defaults ...
        self.note_priority = NOTE_PRIORITY_LAST

    def get_note_priority_name(self):
        """Get human-readable note priority name"""
        return NOTE_PRIORITY_NAMES[self.note_priority]
```

**NVM Storage:** +1 byte (total: 36/256 bytes)

---

### 2. CV Output Driver (cv_gate.py)

**Expand CVOutput class:**
```python
class CVOutput:
    def __init__(self, mcp4728, settings):
        self.mcp4728 = mcp4728
        self.settings = settings

        # Active notes tracking for priority
        self.active_notes = []  # List of (note, velocity) tuples
        self.current_cv_note = None

        # Gate output state
        self.gate_high = False

    def add_note(self, note, velocity):
        """
        Add note to active buffer, apply priority
        Used when arpeggiator is OFF
        """
        # Add to active notes if not already present
        if not any(n[0] == note for n in self.active_notes):
            self.active_notes.append((note, velocity))

        # Apply priority and output
        self._update_cv_output()

    def remove_note(self, note):
        """
        Remove note from active buffer, recalculate priority
        """
        # Remove from active notes
        self.active_notes = [(n, v) for n, v in self.active_notes if n != note]

        # If note was playing, update
        if self.current_cv_note == note:
            self._update_cv_output()

    def _update_cv_output(self):
        """
        Apply note priority strategy and output to CV/Gate
        """
        if not self.active_notes:
            # No notes held - gate off
            self.note_off()
            return

        # Apply priority strategy
        if self.settings.note_priority == NOTE_PRIORITY_HIGHEST:
            selected = max(self.active_notes, key=lambda x: x[0])
        elif self.settings.note_priority == NOTE_PRIORITY_LOWEST:
            selected = min(self.active_notes, key=lambda x: x[0])
        elif self.settings.note_priority == NOTE_PRIORITY_LAST:
            selected = self.active_notes[-1]  # Most recent
        else:  # NOTE_PRIORITY_FIRST
            selected = self.active_notes[0]   # Earliest

        note, velocity = selected

        # Output to CV/Gate (existing method)
        self.note_on(note, velocity)

    def note_on(self, note, velocity=64):
        """
        Output note to CV/Gate
        (Existing method - no changes)
        """
        # Convert MIDI note to CV voltage (1V/octave)
        cv_voltage = self._note_to_voltage(note)

        # Set MCP4728 Channel A (CV Pitch)
        self.mcp4728.channel_a.raw_value = cv_voltage

        # Set gate high (Channel B or GPIO depending on mode)
        if self.settings.gate_mode == GATE_MODE_VTRIG:
            # V-Trig: 0V/5V via MCP4728 Channel B
            self.mcp4728.channel_b.raw_value = 4095  # Full 5V
        else:
            # S-Trig: Open/Short via GPIO D10
            self.gate_pin.value = True  # Short to ground

        self.current_cv_note = note
        self.gate_high = True

    def note_off(self):
        """
        Turn off gate
        (Existing method - no changes)
        """
        # Gate low
        if self.settings.gate_mode == GATE_MODE_VTRIG:
            self.mcp4728.channel_b.raw_value = 0  # 0V
        else:
            self.gate_pin.value = False  # Open circuit

        self.current_cv_note = None
        self.gate_high = False

    def clear_all_notes(self):
        """Clear all tracked notes (e.g., on panic)"""
        self.active_notes = []
        self.note_off()
```

---

### 3. Main Loop Routing (main.py)

**Update MIDI input handling:**
```python
# In main loop
while True:
    msg = get_midi_input()

    if msg:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            # ============================================
            # NOTE ON HANDLING
            # ============================================

            if settings.routing_mode == ROUTING_THRU:
                # THRU mode: Pass through immediately (polyphonic)
                midi_uart.send(msg)
                midi_usb.send(msg)

            else:  # ROUTING_TRANSLATION
                if settings.arp_enabled:
                    # ========================================
                    # MONOPHONIC PATH: Arpeggiator buffering
                    # ========================================
                    # Quantize if scale enabled
                    note = msg.note
                    if settings.scale_enabled:
                        note = settings.quantize_to_scale(note)

                    # Add to arpeggiator buffer
                    arpeggiator.add_note(note, msg.velocity)
                    # (Arpeggiator will output sequentially via clock)

                else:
                    # ========================================
                    # POLYPHONIC PATH: Direct translation
                    # ========================================
                    # Quantize if scale enabled
                    note = msg.note
                    if settings.scale_enabled:
                        note = settings.quantize_to_scale(note)

                    # MIDI OUT: Send immediately (polyphonic)
                    midi_uart.send(NoteOn(note, msg.velocity))
                    midi_usb.send(NoteOn(note, msg.velocity))

                    # CV OUT: Add to priority buffer (monophonic)
                    cv_output.add_note(note, msg.velocity)

        elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            # ============================================
            # NOTE OFF HANDLING
            # ============================================

            if settings.routing_mode == ROUTING_THRU:
                # THRU mode: Pass through immediately
                midi_uart.send(msg)
                midi_usb.send(msg)

            else:  # ROUTING_TRANSLATION
                if settings.arp_enabled:
                    # Remove from arpeggiator buffer
                    arpeggiator.remove_note(msg.note)

                else:
                    # Quantize to match what was added
                    note = msg.note
                    if settings.scale_enabled:
                        note = settings.quantize_to_scale(note)

                    # MIDI OUT: Send immediately (polyphonic)
                    midi_uart.send(NoteOff(note))
                    midi_usb.send(NoteOff(note))

                    # CV OUT: Remove from priority buffer (monophonic)
                    cv_output.remove_note(note)

        else:
            # All other MIDI messages (CC, PitchBend, etc.)
            custom_cc.process_messages([msg])
            midi_uart.send(msg)
            midi_usb.send(msg)
```

---

### 4. Arpeggiator Integration (No Changes Needed)

**Current arpeggiator.step() already correct:**
- Outputs one note at a time (monophonic by design)
- Sends to both MIDI OUT and CV OUT simultaneously
- No polyphonic handling needed (already sequential)

```python
# In arpeggiator.py - EXISTING CODE (no changes)
def step(self):
    """Advance arpeggiator by one step"""
    # ... existing logic ...

    # Get next note
    note, velocity = self.step_sequence[self.current_step]

    # Send to MIDI (monophonic sequence)
    self.midi_io.send_note_on(note, velocity)

    # Send to CV (monophonic sequence)
    if self.cv_output:
        self.cv_output.note_on(note, velocity)
```

---

## Settings & UI

### Menu Structure

**Add "CV/Gate" category to menu.py:**
```python
{
    'name': 'CV/Gate',
    'items': [
        {
            'name': 'Gate Mode',
            'type': 'options',
            'options': ['V-Trig', 'S-Trig'],
            'setting': 'gate_mode',
            'values': [GATE_MODE_VTRIG, GATE_MODE_STRIG]
        },
        {
            'name': 'Priority',
            'type': 'options',
            'options': ['Highest', 'Lowest', 'Last', 'First'],
            'setting': 'note_priority',
            'values': [
                NOTE_PRIORITY_HIGHEST,
                NOTE_PRIORITY_LOWEST,
                NOTE_PRIORITY_LAST,
                NOTE_PRIORITY_FIRST
            ]
        }
    ]
}
```

**Menu Categories (New Total: 8):**
1. Arpeggiator (pattern, octave range, etc.)
2. Scale (root, type, enable)
3. Clock (source, division, swing, multiply, divide)
4. Routing (mode, input source, layer order)
5. Custom CC (source, number, smoothing)
6. **CV/Gate** ← NEW
7. MIDI (channel, velocity)
8. Firmware (rotation, about, reset)

---

### Display Feedback

**Show note priority on main screen when Arp OFF:**
```
┌────────────────────┐
│ SCALE: C Major     │
│ ARP:   OFF         │
│ CV:    Last Note   │  ← NEW: Show priority mode
│ Notes: C E G (3)   │  ← NEW: Show held notes
└────────────────────┘
```

**When Arp ON (existing):**
```
┌────────────────────┐
│ UP      C Major    │
│ ♩=120   16th       │
│ Notes: C E G (3)   │
└────────────────────┘
```

---

## Testing Strategy

### Unit Tests (PyTest)

**Test note priority logic:**
```python
# tests/test_cv_priority.py

def test_highest_note_priority():
    """Test highest note priority strategy"""
    cv = CVOutput(mock_dac, settings)
    settings.note_priority = NOTE_PRIORITY_HIGHEST

    cv.add_note(60, 64)  # C3
    assert cv.current_cv_note == 60

    cv.add_note(64, 64)  # E3
    assert cv.current_cv_note == 64  # Higher note takes priority

    cv.add_note(67, 64)  # G3
    assert cv.current_cv_note == 67  # Highest

    cv.remove_note(67)
    assert cv.current_cv_note == 64  # E3 now highest

    cv.remove_note(64)
    assert cv.current_cv_note == 60  # C3 only remaining

def test_last_note_priority():
    """Test last note priority strategy"""
    cv = CVOutput(mock_dac, settings)
    settings.note_priority = NOTE_PRIORITY_LAST

    cv.add_note(60, 64)  # C3
    assert cv.current_cv_note == 60

    cv.add_note(64, 64)  # E3 (last)
    assert cv.current_cv_note == 64

    cv.add_note(67, 64)  # G3 (last)
    assert cv.current_cv_note == 67

    cv.add_note(55, 64)  # G2 (last, even though lower)
    assert cv.current_cv_note == 55  # Last note wins

    cv.remove_note(55)
    assert cv.current_cv_note == 67  # G3 now last remaining

def test_polyphonic_midi_passthrough():
    """Test polyphonic pass-through when arp OFF"""
    settings.arp_enabled = False
    settings.scale_enabled = True

    # Send chord (C, E, G)
    process_note_on(60, 64)
    process_note_on(64, 64)
    process_note_on(67, 64)

    # Verify all 3 notes sent to MIDI OUT
    assert len(midi_out_buffer) == 3
    assert 60 in midi_out_buffer
    assert 64 in midi_out_buffer
    assert 67 in midi_out_buffer

    # Verify only 1 note sent to CV OUT (using priority)
    assert cv_output.current_cv_note in [60, 64, 67]
```

---

### Hardware Tests

**Manual Test Procedure:**

**Test 1: Polyphonic MIDI Pass-Through (Arp OFF)**
```
Setup:
- Arp: OFF
- Scale: C Major, ON
- Note Priority: Last

Input: Play C-E-G chord simultaneously
Expected:
- MIDI OUT: All 3 notes playing (polyphonic)
- CV OUT: G (last note pressed) at correct voltage
```

**Test 2: Highest Note Priority**
```
Setup:
- Arp: OFF
- Note Priority: Highest

Input:
1. Play C3 → CV = C3
2. Add E3  → CV = E3 (higher)
3. Add G3  → CV = G3 (highest)
4. Release G3 → CV = E3
5. Release E3 → CV = C3

Verify with oscilloscope: Voltage steps correctly
```

**Test 3: Last Note Priority (Expressive Playing)**
```
Setup:
- Arp: OFF
- Note Priority: Last

Input: Play melody while holding bass note
1. Hold C2 (bass) → CV = C2
2. Play E3 → CV = E3 (last)
3. Play G3 → CV = G3 (last)
4. Release E3 → CV = G3 (still last)
5. Release G3 → CV = C2 (back to bass)

Expected: Expressive monophonic playing over drone
```

**Test 4: Arpeggiator with Polyphonic Input**
```
Setup:
- Arp: UP pattern, ON
- Scale: C Major

Input: Hold C-E-G chord
Expected:
- MIDI OUT: C → E → G → C (sequential)
- CV OUT: Same sequence (already monophonic)
```

---

## Edge Cases & Gotchas

### 1. Quantization + Priority Interaction
**Scenario:** Two different input notes quantize to same note
```
Input:  F# (66) + G (67) simultaneously
Scale:  C Major (both quantize to G)
Result: Only one G in active_notes buffer
```
**Solution:** Check for duplicates when adding to active_notes

### 2. Velocity Handling
**Question:** Which velocity to use when multiple notes held?
**Answer:** Use velocity of the selected priority note
```python
selected = max(active_notes, key=lambda x: x[0])
note, velocity = selected  # Use this note's velocity
```

### 3. Note Off Matching
**Problem:** Note off for quantized note
```
Input: F# note on → quantizes to G → CV plays G
Input: F# note off → must remove G from buffer
```
**Solution:** Quantize note offs the same way as note ons

### 4. MIDI Channel Filtering
**Current:** Arpeggiator filters by MIDI channel
**New:** CV priority must also filter by channel
```python
# In main loop - only process configured MIDI channel
if hasattr(msg, 'channel') and msg.channel != settings.midi_channel:
    # Pass through to MIDI OUT (other channels)
    midi_uart.send(msg)
    midi_usb.send(msg)
    # Don't send to CV OUT (wrong channel)
    continue
```

---

## Performance Considerations

### Memory Impact
- Active notes list: ~20 bytes per note × 16 max = 320 bytes worst case
- Priority calculation: O(n) where n = number of held notes (negligible)
- Total impact: < 0.5% of available RAM

### Latency Impact
- Priority calculation: ~50µs for 16 notes (negligible)
- No impact on MIDI pass-through (still zero latency)
- CV output update: ~200µs (same as before)

### CPU Impact
- Note priority on add/remove: O(n) linear search
- For typical 3-note chord: < 10µs
- Well within 10ms main loop budget

---

## Migration Path

### Phase 1: Update Settings
- Add note priority constants to config.py
- Add note_priority to Settings class
- Update NVM save/load

### Phase 2: Update CV Output
- Add active_notes tracking to CVOutput
- Implement _update_cv_output() with priority logic
- Add add_note() and remove_note() methods

### Phase 3: Update Main Loop
- Add polyphonic pass-through path (Arp OFF)
- Route Note On/Off to cv_output.add_note() / remove_note()
- Maintain monophonic path for arpeggiator (existing)

### Phase 4: Add Menu
- Add CV/Gate category to menu
- Add Note Priority setting
- Test all 4 priority modes

### Phase 5: Testing
- Unit tests for all priority strategies
- Hardware tests with oscilloscope
- Integration tests (poly MIDI, mono CV)

---

## Future Enhancements

### Paraphonic Mode (Future)
**Concept:** Multiple CV outputs (requires more DAC channels)
- CV OUT 1: Highest note
- CV OUT 2: Middle note
- CV OUT 3: Lowest note
**Requirement:** 3× MCP4728 channels or additional DAC

### Unison Mode (Future)
**Concept:** Layer multiple notes at same time (same CV)
- Play chord → all notes trigger same CV (first note)
- Use for detuned unison effects
**Requirement:** Custom oscillator with multiple VCOs

### Note Stealing (Future)
**Concept:** Limit polyphony to N voices
- Steal oldest voice when exceeding limit
- For multi-timbral MIDI OUT expansion

---

## Conclusion

**Summary:**
- Polyphonic MIDI → Polyphonic MIDI ✓ (with scale quantization)
- Polyphonic MIDI → Monophonic CV ✓ (with note priority)
- Arpeggiator → Always monophonic ✓ (no changes needed)

**Default Configuration:**
- Note Priority: **Last** (most natural for monophonic playing)
- Gate Mode: **V-Trig** (most common for modern Eurorack)

**Implementation Effort:**
- 2-3 hours (settings + CV output updates + main loop routing)
- Low risk (isolated to CV output path)
- Backward compatible (existing arp behavior unchanged)

**Ready for implementation in Translation Hub Phase 5!**

---

**Document Status:** ✅ Complete - Ready for Review
**Next Step:** Update Translation Hub Implementation Plan
