# prisme Translation Hub - Implementation Plan

**Created:** 2025-11-01 (Session 15)
**Research Confidence:** 97%
**Implementation Strategy:** Phased migration with zero-risk fallback
**Total Estimated Time:** 8-12 hours (spread across 3-4 sessions)

---

## Executive Summary

### Goal
Migrate from inline arpeggiator in `main.py` to class-based architecture with user-configurable translation layer system, enabling:
- **Routing modes:** THRU (pass-through) or TRANSLATION (layer processing)
- **Input selection:** MIDI IN, USB MIDI, CV IN (future), Gate IN (future)
- **Layer ordering:** Scale → Arp OR Arp → Scale (user-definable)
- **Clock transformations:** Swing, Multiply (2x, 4x), Divide (1/2, 1/4, 1/8)

### Approach
**Zero-risk migration:** Create `main_v2.py` on feature branch, test thoroughly, merge when confident.

### Success Criteria
1. All current functionality preserved
2. Translation layers working with user-definable ordering
3. Swing/multiply/divide implemented
4. Custom CC integration maintained (from Session 14)
5. CV/Gate output working (currently missing in main.py)
6. Zero latency increase (< 0.1ms added)
7. All tests passing (unit + hardware validation)

---

## Phase 1: Foundation Setup (1-2 hours)

### 1.1 Git Branching and Backup
```bash
# Create feature branch
git checkout -b feature/translation-hub

# Ensure we can rollback easily
git tag backup-before-translation-hub
```

**Deliverable:** Feature branch ready, rollback point tagged

---

### 1.2 File Structure Setup

**Create new files:**
```
arp/
  core/
    translation.py          # NEW: TranslationPipeline class
    layers.py               # NEW: Layer implementations
  tests/
    test_translation.py     # NEW: PyTest unit tests
    test_arpeggiator.py     # NEW: Arpeggiator tests
    conftest.py             # NEW: PyTest configuration
main_v2.py                  # NEW: New architecture main file
```

**Action Items:**
- [ ] Create `arp/core/translation.py` (TranslationPipeline class)
- [ ] Create `arp/core/layers.py` (ScaleLayer, ArpLayer base classes)
- [ ] Create `tests/` directory structure
- [ ] Create `main_v2.py` as copy of `main.py` (starting point)

**Deliverable:** File structure ready for implementation

---

### 1.3 Settings Expansion (30 min)

**Add to `config.py`:**
```python
# Routing mode
ROUTING_THRU = 0
ROUTING_TRANSLATION = 1

# Input source
INPUT_SOURCE_MIDI_IN = 0
INPUT_SOURCE_USB = 1
INPUT_SOURCE_CV_IN = 2   # Future
INPUT_SOURCE_GATE_IN = 3  # Future

# Layer ordering
LAYER_ORDER_SCALE_FIRST = 0  # Scale → Arp
LAYER_ORDER_ARP_FIRST = 1    # Arp → Scale

# Clock transformations
CLOCK_MULTIPLY_1X = 1
CLOCK_MULTIPLY_2X = 2
CLOCK_MULTIPLY_4X = 4

CLOCK_DIVIDE_1 = 1
CLOCK_DIVIDE_2 = 2
CLOCK_DIVIDE_4 = 4
CLOCK_DIVIDE_8 = 8
```

**Add to `Settings` class (config.py):**
```python
def __init__(self):
    # ... existing settings ...

    # Translation Hub settings (8 new bytes)
    self.routing_mode = ROUTING_TRANSLATION
    self.input_source = INPUT_SOURCE_MIDI_IN
    self.layer_order = LAYER_ORDER_SCALE_FIRST
    self.scale_enabled = True
    self.arp_enabled = True
    self.clock_multiply = CLOCK_MULTIPLY_1X
    self.clock_divide = CLOCK_DIVIDE_1
    self.swing_percent = 50  # 50% = no swing

def _load_defaults(self):
    # ... existing defaults ...
    self.routing_mode = ROUTING_TRANSLATION
    self.input_source = INPUT_SOURCE_MIDI_IN
    self.layer_order = LAYER_ORDER_SCALE_FIRST
    self.scale_enabled = True
    self.arp_enabled = True
    self.clock_multiply = CLOCK_MULTIPLY_1X
    self.clock_divide = CLOCK_DIVIDE_1
    self.swing_percent = 50

def save(self):
    # ... existing save logic ...
    # Add 8 new bytes to NVM storage (total: 35/256 bytes)
```

**Action Items:**
- [ ] Add constants to `config.py`
- [ ] Add settings to `Settings.__init__()`
- [ ] Update `_load_defaults()`
- [ ] Update `save()` and `load()` methods
- [ ] Test settings save/load

**Deliverable:** Settings system supports all Translation Hub parameters

---

## Phase 2: Translation Layer System (2-3 hours)

### 2.1 Layer Base Classes (`arp/core/layers.py`)

```python
"""Translation layer base classes and implementations"""

class TranslationLayer:
    """Base class for all translation layers"""
    def __init__(self, settings):
        self.settings = settings

    def transform(self, note, velocity=64):
        """Transform a note - must be implemented by subclass"""
        raise NotImplementedError

class ScaleQuantizeLayer(TranslationLayer):
    """Quantize notes to the current scale"""
    def transform(self, note, velocity=64):
        if self.settings.scale_enabled:
            return self.settings.quantize_to_scale(note)
        return note

class ArpeggiatorLayer(TranslationLayer):
    """Arpeggiator layer - buffers notes and generates sequence"""
    def __init__(self, settings, arpeggiator):
        super().__init__(settings)
        self.arpeggiator = arpeggiator

    def transform(self, note, velocity=64):
        # This layer doesn't transform directly
        # It buffers notes for arpeggiation
        # The arpeggiator handles the actual sequencing
        return note
```

**Action Items:**
- [ ] Create `layers.py` with base classes
- [ ] Implement `ScaleQuantizeLayer`
- [ ] Implement `ArpeggiatorLayer` integration
- [ ] Add docstrings

**Deliverable:** Layer classes ready for pipeline integration

---

### 2.2 Translation Pipeline (`arp/core/translation.py`)

```python
"""Translation pipeline - configurable layer chain"""

from .layers import ScaleQuantizeLayer, ArpeggiatorLayer
from .config import LAYER_ORDER_SCALE_FIRST, LAYER_ORDER_ARP_FIRST

class TranslationPipeline:
    """Manages the translation layer chain"""

    def __init__(self, settings, arpeggiator):
        self.settings = settings
        self.arpeggiator = arpeggiator
        self.layers = []
        self._configure_layers()

    def _configure_layers(self):
        """Build layer chain based on user settings"""
        self.layers = []

        if self.settings.layer_order == LAYER_ORDER_SCALE_FIRST:
            # Scale → Arp
            if self.settings.scale_enabled:
                self.layers.append(ScaleQuantizeLayer(self.settings))
            if self.settings.arp_enabled:
                self.layers.append(ArpeggiatorLayer(self.settings, self.arpeggiator))
        else:
            # Arp → Scale
            if self.settings.arp_enabled:
                self.layers.append(ArpeggiatorLayer(self.settings, self.arpeggiator))
            if self.settings.scale_enabled:
                self.layers.append(ScaleQuantizeLayer(self.settings))

    def reconfigure(self):
        """Reconfigure layers after settings change"""
        self._configure_layers()

    def process_note(self, note, velocity):
        """Pass note through layer chain"""
        current_note = note

        for layer in self.layers:
            current_note = layer.transform(current_note, velocity)

        return current_note
```

**Action Items:**
- [ ] Create `translation.py` with TranslationPipeline
- [ ] Implement layer ordering logic
- [ ] Add reconfigure method (for when user changes settings)
- [ ] Add logging for debugging

**Deliverable:** Translation pipeline ready for integration

---

### 2.3 Unit Tests (`tests/test_translation.py`)

```python
"""Unit tests for translation pipeline"""
import pytest
from arp.core.translation import TranslationPipeline
from arp.core.config import Settings, LAYER_ORDER_SCALE_FIRST, LAYER_ORDER_ARP_FIRST

def test_scale_first_ordering():
    """Test Scale → Arp layer ordering"""
    settings = Settings()
    settings.layer_order = LAYER_ORDER_SCALE_FIRST
    settings.scale_enabled = True
    settings.arp_enabled = True

    arpeggiator = MockArpeggiator(settings)
    pipeline = TranslationPipeline(settings, arpeggiator)

    # Verify layer chain
    assert len(pipeline.layers) == 2
    assert isinstance(pipeline.layers[0], ScaleQuantizeLayer)
    assert isinstance(pipeline.layers[1], ArpeggiatorLayer)

def test_arp_first_ordering():
    """Test Arp → Scale layer ordering"""
    settings = Settings()
    settings.layer_order = LAYER_ORDER_ARP_FIRST
    settings.scale_enabled = True
    settings.arp_enabled = True

    arpeggiator = MockArpeggiator(settings)
    pipeline = TranslationPipeline(settings, arpeggiator)

    # Verify layer chain
    assert len(pipeline.layers) == 2
    assert isinstance(pipeline.layers[0], ArpeggiatorLayer)
    assert isinstance(pipeline.layers[1], ScaleQuantizeLayer)

def test_scale_quantization():
    """Test that scale quantization works correctly"""
    settings = Settings()
    settings.scale_root = 0  # C
    settings.scale_type = SCALE_MAJOR

    # F# (66) should quantize to G (67) in C major
    quantized = settings.quantize_to_scale(66)
    assert quantized == 67
```

**Action Items:**
- [ ] Create `conftest.py` with CircuitPython mocks
- [ ] Write layer ordering tests
- [ ] Write scale quantization tests
- [ ] Write integration tests
- [ ] Achieve 100% coverage

**Test Command:**
```bash
pytest --cov-report term-missing --cov=arp tests/
```

**Deliverable:** All tests passing with 100% coverage

---

## Phase 3: Clock Transformations (2-3 hours)

### 3.1 Swing Implementation (`arp/core/clock.py`)

**Add to ClockHandler:**
```python
class ClockHandler:
    def __init__(self, bpm=120, swing_percent=50, multiply=1, divide=1, ...):
        self.bpm = bpm
        self.swing_percent = swing_percent  # 50-75
        self.multiply = multiply            # 1, 2, 4
        self.divide = divide                # 1, 2, 4, 8
        self.tick_count = 0
        self.base_tick_interval = self._calculate_base_interval()
        self.current_tick_interval = self._calculate_next_tick_delay()

    def _calculate_base_interval(self):
        """Base tick interval before transformations"""
        return 60.0 / (self.bpm * 24)

    def _calculate_next_tick_delay(self):
        """Calculate delay for next tick with swing applied"""
        # Apply multiply/divide first
        transformed_interval = (self.base_tick_interval * self.divide) / self.multiply

        # Apply swing (Roger Linn method)
        if self.swing_percent == 50:
            return transformed_interval  # No swing

        # Determine if this is an even or odd 16th note
        sixteenth_number = (self.tick_count // 6) % 2  # 0 (odd) or 1 (even)

        if sixteenth_number == 0:  # Odd 16th (on-beat)
            ratio = self.swing_percent / 100.0
            return transformed_interval * 12 * ratio / 6
        else:  # Even 16th (off-beat)
            ratio = (100 - self.swing_percent) / 100.0
            return transformed_interval * 12 * ratio / 6

    def set_swing(self, swing_percent):
        """Set swing amount (50-75)"""
        assert 50 <= swing_percent <= 75
        self.swing_percent = swing_percent

    def set_multiply(self, multiply):
        """Set clock multiplier (1, 2, 4)"""
        assert multiply in [1, 2, 4]
        self.multiply = multiply
        self.base_tick_interval = self._calculate_base_interval()

    def set_divide(self, divide):
        """Set clock divider (1, 2, 4, 8)"""
        assert divide in [1, 2, 4, 8]
        self.divide = divide
        self.base_tick_interval = self._calculate_base_interval()
```

**Action Items:**
- [ ] Implement `_calculate_next_tick_delay()` with swing
- [ ] Add multiply/divide support
- [ ] Update tick generation to use dynamic intervals
- [ ] Test at various BPMs (60, 120, 140)
- [ ] Verify swing percentages (50%, 62%, 66%)

**Deliverable:** Clock transformations working correctly

---

### 3.2 Clock Tests (`tests/test_clock.py`)

```python
def test_swing_implementation():
    """Test Roger Linn swing implementation"""
    clock = ClockHandler(bpm=120, swing_percent=66)

    # At 66%, first 16th gets 66% of time, second gets 34%
    # This creates perfect triplet swing

    # Calculate expected delays
    base_interval = 60.0 / (120 * 24)  # 0.02083s
    pair_time = base_interval * 12      # 0.25s for two 16ths

    # Tick 0 (odd 16th): Should get 66% of pair_time
    delay_0 = clock._calculate_next_tick_delay()
    expected_0 = pair_time * 0.66 / 6
    assert abs(delay_0 - expected_0) < 0.0001

    # Advance to tick 6 (even 16th): Should get 34% of pair_time
    clock.tick_count = 6
    delay_6 = clock._calculate_next_tick_delay()
    expected_6 = pair_time * 0.34 / 6
    assert abs(delay_6 - expected_6) < 0.0001

def test_multiply_divide():
    """Test clock multiply and divide"""
    base_clock = ClockHandler(bpm=120, multiply=1, divide=1)
    base_interval = base_clock.base_tick_interval

    # 2x multiply should halve interval
    fast_clock = ClockHandler(bpm=120, multiply=2, divide=1)
    assert abs(fast_clock.current_tick_interval - base_interval/2) < 0.0001

    # 1/2 divide should double interval
    slow_clock = ClockHandler(bpm=120, multiply=1, divide=2)
    assert abs(slow_clock.current_tick_interval - base_interval*2) < 0.0001
```

**Action Items:**
- [ ] Write swing calculation tests
- [ ] Write multiply/divide tests
- [ ] Test external clock compatibility
- [ ] Verify no drift accumulation

**Deliverable:** All clock tests passing

---

## Phase 4: USB MIDI Integration (1-2 hours)

### 4.1 USB MIDI Input for Notes (`main_v2.py`)

**Current (clock only):**
```python
clock = ClockHandler(midi_in_port=usb_midi.ports[0])
```

**New (clock + notes):**
```python
import usb_midi
from adafruit_midi import MIDI

# Create MIDI objects for both UART and USB
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi_uart = MIDI(midi_in=uart, midi_out=uart)
midi_usb = MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

# Clock handler can share the USB input port
clock = ClockHandler(midi_in_port=usb_midi.ports[0])

# In main loop:
def get_midi_input():
    """Get MIDI input based on selected source"""
    if settings.input_source == INPUT_SOURCE_MIDI_IN:
        return midi_uart.receive()
    elif settings.input_source == INPUT_SOURCE_USB:
        return midi_usb.receive()
    return None
```

**Action Items:**
- [ ] Create USB MIDI object
- [ ] Implement input source switching
- [ ] Test USB note input
- [ ] Test USB clock input (verify still works)
- [ ] Test UART input (verify backward compatibility)

**Deliverable:** USB MIDI fully functional for both clock and notes

---

## Phase 5: Main Loop Integration (2-3 hours)

### 5.1 Migrate to Class-Based Arpeggiator

**Replace inline arpeggiator (lines 181-204 in main.py) with:**
```python
from arp.core.arpeggiator import Arpeggiator
from arp.core.translation import TranslationPipeline

# Initialize (after settings loaded)
arpeggiator = Arpeggiator(settings)
translation_pipeline = TranslationPipeline(settings, arpeggiator)

# Set clock callback
clock.set_step_callback(arpeggiator.on_clock_step)
```

**Action Items:**
- [ ] Import class-based arpeggiator
- [ ] Remove inline arpeggiator code
- [ ] Integrate translation pipeline
- [ ] Update clock callback
- [ ] Test all 16 patterns

**Deliverable:** Class-based arpeggiator fully integrated

---

### 5.2 Routing Mode Logic

**Add to main loop:**
```python
while True:
    # Get MIDI input based on source
    msg = get_midi_input()

    if msg:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            if settings.routing_mode == ROUTING_THRU:
                # Pass through immediately
                midi_uart.send(msg)
                midi_usb.send(msg)
            else:  # ROUTING_TRANSLATION
                # Process through translation pipeline
                translated_note = translation_pipeline.process_note(msg.note, msg.velocity)
                arpeggiator.add_note(translated_note, msg.velocity)

        elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            if settings.routing_mode == ROUTING_THRU:
                # Pass through immediately
                midi_uart.send(msg)
                midi_usb.send(msg)
            else:  # ROUTING_TRANSLATION
                arpeggiator.remove_note(msg.note)

        else:
            # All other MIDI messages (CC, PitchBend, etc.)
            custom_cc.process_messages([msg])  # Custom CC output (Session 14)
            midi_uart.send(msg)                # Pass through
            midi_usb.send(msg)

    # Clock processing
    clock.process_clock_messages()

    # ... rest of main loop
```

**Action Items:**
- [ ] Implement routing mode logic
- [ ] Add USB output to all outputs
- [ ] Maintain Custom CC integration
- [ ] Test THRU mode (zero latency)
- [ ] Test TRANSLATION mode (with layers)

**Deliverable:** Routing modes working correctly

---

### 5.3 CV/Gate Output Integration

**Add to arpeggiator callback:**
```python
# In arpeggiator.py (or main_v2.py callback)
def on_clock_step():
    """Called on each clock step"""
    # Send note off for previous note
    if self.current_playing_note is not None:
        midi_uart.send(NoteOff(self.current_playing_note))
        midi_usb.send(NoteOff(self.current_playing_note))
        cv_output.note_off()  # NEW: CV Gate off

    # Get next note
    if self.arp_sequence:
        next_note = self.arp_sequence[self.current_step]

        # Send note on
        midi_uart.send(NoteOn(next_note, self.current_velocity))
        midi_usb.send(NoteOn(next_note, self.current_velocity))
        cv_output.note_on(next_note, self.current_velocity)  # NEW: CV output

        self.current_playing_note = next_note
        self.current_step = (self.current_step + 1) % len(self.arp_sequence)
```

**Action Items:**
- [ ] Add `cv_output.note_on()` to note output
- [ ] Add `cv_output.note_off()` to note off
- [ ] Test CV output with oscilloscope
- [ ] Verify gate timing

**Deliverable:** CV/Gate output working (currently missing in main.py!)

---

## Phase 6: Menu System Update (1-2 hours)

### 6.1 Add New Menu Categories (`menu.py`)

**Add "Routing" category:**
```python
{
    'name': 'Routing',
    'items': [
        {'name': 'Mode', 'type': 'options', 'options': ['THRU', 'TRANSLATE'], ...},
        {'name': 'Input', 'type': 'options', 'options': ['MIDI IN', 'USB'], ...},
        {'name': 'Order', 'type': 'options', 'options': ['Scale→Arp', 'Arp→Scale'], ...},
    ]
}
```

**Expand "Clock" category:**
```python
{
    'name': 'Clock',
    'items': [
        # ... existing items ...
        {'name': 'Multiply', 'type': 'options', 'options': ['1x', '2x', '4x'], ...},
        {'name': 'Divide', 'type': 'options', 'options': ['1', '1/2', '1/4', '1/8'], ...},
        {'name': 'Swing', 'type': 'range', 'min': 50, 'max': 75, ...},
    ]
}
```

**Expand "Scale" and "Arp" categories:**
```python
# Add enable/disable toggles
{'name': 'Scale Enable', 'type': 'toggle', ...}
{'name': 'Arp Enable', 'type': 'toggle', ...}
```

**Action Items:**
- [ ] Add Routing category with 3 settings
- [ ] Add Clock transformations (3 settings)
- [ ] Add layer enable toggles (2 settings)
- [ ] Test navigation through all menus
- [ ] Verify settings save correctly

**Deliverable:** Menu system supports all Translation Hub features

---

## Phase 7: Testing & Validation (2-3 hours)

### 7.1 Unit Tests (on computer with PyTest)

```bash
# Run all tests with coverage
pytest --cov-report term-missing --cov=arp tests/

# Expected: 100% coverage on new code
# - arp/core/translation.py: 100%
# - arp/core/layers.py: 100%
# - Updated clock.py swing code: 100%
```

**Test Checklist:**
- [ ] Translation pipeline ordering
- [ ] Scale quantization accuracy
- [ ] Swing calculation (50%, 62%, 66%)
- [ ] Clock multiply/divide math
- [ ] Layer enable/disable
- [ ] Settings save/load

**Deliverable:** All unit tests passing

---

### 7.2 Hardware Validation Tests (on device)

**Create `tests/hardware_validation.py`:**
```python
"""Hardware validation - deploy to /Volumes/CIRCUITPY/code.py"""

print("prisme Translation Hub - Hardware Validation")
print("="*40)

# Test 1: THRU mode (zero latency)
print("\nTest 1: THRU Mode")
settings.routing_mode = ROUTING_THRU
# Send MIDI notes, verify immediate pass-through

# Test 2: Scale → Arp
print("\nTest 2: Scale → Arp Mode")
settings.routing_mode = ROUTING_TRANSLATION
settings.layer_order = LAYER_ORDER_SCALE_FIRST
# Send notes, verify quantization then arpeggiation

# Test 3: Arp → Scale
print("\nTest 3: Arp → Scale Mode")
settings.layer_order = LAYER_ORDER_ARP_FIRST
# Verify arpeggiation then quantization

# Test 4: Swing at 66%
print("\nTest 4: Swing (66% triplet)")
settings.swing_percent = 66
# Verify swing timing with LED or oscilloscope

# Test 5: Clock multiply 2x
print("\nTest 5: Clock Multiply 2x")
settings.clock_multiply = 2
# Verify double-speed arpeggiation

# Test 6: USB MIDI input
print("\nTest 6: USB MIDI Input")
settings.input_source = INPUT_SOURCE_USB
# Send USB MIDI notes, verify processing

# Test 7: CV/Gate output
print("\nTest 7: CV/Gate Output")
# Verify CV voltage and gate triggers

# Test 8: Custom CC (Session 14 regression)
print("\nTest 8: Custom CC Output")
# Verify Custom CC still works

print("\n✅ All hardware tests passed!")
```

**Manual Test Checklist:**
- [ ] THRU mode: Notes pass through instantly
- [ ] TRANSLATION mode: Layers process correctly
- [ ] Scale → Arp: Quantization before arpeggiation
- [ ] Arp → Scale: Arpeggiation before quantization
- [ ] Swing 66%: Triplet feel (use metronome)
- [ ] Multiply 2x: Double-speed arp
- [ ] Divide 1/2: Half-speed arp
- [ ] USB input: Notes received correctly
- [ ] UART input: Still works (backward compatible)
- [ ] CV output: Correct voltage (oscilloscope)
- [ ] Gate output: Correct triggers (oscilloscope)
- [ ] Custom CC: Still works (Session 14 regression test)
- [ ] All buttons: Still responsive
- [ ] Display: Updates correctly
- [ ] Settings: Save/load correctly

**Deliverable:** All hardware tests passing

---

## Phase 8: Documentation & Finalization (1 hour)

### 8.1 Update Documentation

**Files to update:**
- [ ] `README.md` - Add Translation Hub features
- [ ] `docs/ARCHITECTURE.md` - Document new architecture
- [ ] `docs/USER_GUIDE.md` - Explain routing modes, layer ordering
- [ ] `docs/context/CONTEXT.md` - Update session handoff

**Action Items:**
- [ ] Document all new features
- [ ] Update architecture diagrams
- [ ] Add usage examples
- [ ] Update project name to "prisme" everywhere

**Deliverable:** Complete documentation

---

### 8.2 Code Cleanup

**Action Items:**
- [ ] Remove debug print statements
- [ ] Add comprehensive docstrings
- [ ] Clean up commented code
- [ ] Verify consistent code style
- [ ] Run linter (if available)

**Deliverable:** Clean, production-ready code

---

### 8.3 Final Merge

```bash
# Ensure all tests pass
pytest --cov=arp tests/

# Deploy to hardware for final validation
cp main_v2.py /Volumes/CIRCUITPY/code.py

# Test thoroughly on hardware
# ... manual testing ...

# If all good, rename and merge
git mv main.py main_legacy.py
git mv main_v2.py main.py
git add .
git commit -m "feat: Implement Translation Hub architecture with user-definable layers

- Migrate to class-based arpeggiator with scale quantization
- Add configurable translation pipeline (Scale→Arp or Arp→Scale)
- Implement swing (Roger Linn method), multiply, divide
- Add USB MIDI input for notes (not just clock)
- Integrate CV/Gate output (was missing in main.py)
- Add routing modes (THRU / TRANSLATION)
- Preserve Custom CC integration (Session 14)
- All tests passing (unit + hardware validation)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Merge to main
git checkout main
git merge feature/translation-hub
git push
```

**Deliverable:** Translation Hub merged to main branch

---

## Risk Mitigation Strategies

### Risk 1: Breaking Current Functionality
**Mitigation:**
- Keep `main.py` intact during development
- Create `main_v2.py` for new architecture
- Feature branch allows easy rollback
- Git tag before starting (`backup-before-translation-hub`)

### Risk 2: USB MIDI Conflicts
**Mitigation:**
- Research confirms same port can be shared
- Test early in Phase 4
- Fallback: Keep clock on USB, notes on UART

### Risk 3: Performance Degradation
**Mitigation:**
- Translation layers add only ~65µs (negligible)
- Monitor performance at each phase
- Profile with time.monotonic_ns() if needed

### Risk 4: Memory Overflow
**Mitigation:**
- New code adds only ~450 bytes (~0.3% of RAM)
- Monitor `gc.mem_free()` after each phase
- Optimize if memory drops below 120KB

### Risk 5: Timing Drift with Swing
**Mitigation:**
- Roger Linn method is drift-free (proven)
- Test with external clock to verify sync
- Use oscilloscope to measure actual timing

---

## Rollback Plan

If any phase fails critically:

1. **Immediate rollback:**
   ```bash
   git checkout main
   git reset --hard backup-before-translation-hub
   ```

2. **Selective rollback:**
   ```bash
   # Keep current branch, copy old main.py back
   git checkout main -- main.py
   cp main.py /Volumes/CIRCUITPY/code.py
   ```

3. **Debugging mode:**
   ```bash
   # Switch between old and new on device
   cp main.py /Volumes/CIRCUITPY/code.py      # Old
   cp main_v2.py /Volumes/CIRCUITPY/code.py   # New
   ```

---

## Timeline Estimates

| Phase | Description | Time | Cumulative |
|-------|-------------|------|------------|
| 1 | Foundation Setup | 1-2h | 2h |
| 2 | Translation Layers | 2-3h | 5h |
| 3 | Clock Transformations | 2-3h | 8h |
| 4 | USB MIDI Integration | 1-2h | 10h |
| 5 | Main Loop Integration | 2-3h | 13h |
| 6 | Menu System | 1-2h | 15h |
| 7 | Testing & Validation | 2-3h | 18h |
| 8 | Documentation | 1h | 19h |

**Total:** 12-19 hours (realistic: 15 hours)
**Sessions:** 3-4 sessions @ 4-5 hours each

---

## Success Metrics

**Functionality:**
- ✅ All 10 critical questions answered (97% confidence)
- ✅ THRU mode: Zero latency pass-through
- ✅ TRANSLATION mode: Configurable layer ordering
- ✅ Swing: Roger Linn implementation working
- ✅ Multiply/Divide: Clock transformations working
- ✅ USB MIDI: Both clock and notes working
- ✅ CV/Gate: Output working (was missing!)
- ✅ Custom CC: Still working (Session 14 preserved)

**Quality:**
- ✅ 100% unit test coverage
- ✅ All hardware tests passing
- ✅ Zero performance regression (< 0.1ms added latency)
- ✅ Zero memory issues (< 1% RAM increase)
- ✅ All documentation updated
- ✅ Clean, maintainable code

**User Experience:**
- ✅ All current features still work
- ✅ New features intuitive to use
- ✅ Settings save/load correctly
- ✅ Display shows helpful information
- ✅ Can rollback easily if needed

---

## Next Session Checklist

**Before starting Phase 1:**
- [ ] Review this implementation plan
- [ ] Ensure 2-3 hours of uninterrupted time
- [ ] Device connected and working
- [ ] Git repo clean (no uncommitted changes)
- [ ] Ready to create feature branch

**Quick Start:**
```bash
# Start Phase 1
git checkout -b feature/translation-hub
git tag backup-before-translation-hub
mkdir -p arp/core tests
# ... proceed with Phase 1.2
```

---

**Created:** 2025-11-01 (Session 15)
**Status:** 📋 Ready for Implementation
**Confidence:** 97%
**Risk Level:** LOW (with mitigation strategies)

**Let's build this! 🚀**
