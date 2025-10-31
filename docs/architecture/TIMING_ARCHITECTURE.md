# Arpeggiator Timing Architecture

**Purpose:** Ensure CV output timing accuracy is never compromised by I2C bus contention.

**Last Updated:** 2025-10-31
**Critical Priority:** BLOCKING ISSUE for production quality

---

## Executive Summary

**Problem:** OLED display updates on shared I2C bus can block CPU and introduce timing jitter in CV output, causing audible pitch instability.

**Impact:** Display updates can take 50-280ms, completely blocking real-time CV/Gate output during that period.

**Solution:** Implement priority-based I2C access with display throttling and separation of critical vs. non-critical paths.

---

## The Problem: I2C Blocking

### Real-World Evidence

From production audio/synth projects using I2C OLED + DAC:

| Platform | Issue | Measured Impact |
|----------|-------|----------------|
| Teensy 4.1 + Audio | "Audio cuts out when updating I2C OLED" | 50-280ms blocking |
| HiFiBerry DAC + OLED | "Rhythmic noise proportionate to display refresh" | Audio artifacts |
| Arduino + Audio | "Audio glitches every time buffer sent to OLED" | Audible dropouts |

**Root Cause:**
- I2C is **synchronous** - CPU waits for each byte transfer
- OLED updates send **1024 bytes** (128×64 pixels) over slow I2C
- CircuitPython/MicroPython **do not support I2C DMA** on most platforms
- Result: **CPU completely blocked** during OLED update

### Our Hardware Timing Budget

**Arpeggiator Requirements:**

| Tempo | Note Division | Time per Note | Jitter Tolerance |
|-------|---------------|---------------|------------------|
| 120 BPM | 16th notes | 125 ms | ±5 ms |
| 200 BPM | 16th notes | 75 ms | ±3 ms |
| 300 BPM | 16th notes | 50 ms | ±2 ms |

**I2C Operation Times (typical):**

| Operation | Bus Time | Blocking? | Impact |
|-----------|----------|-----------|--------|
| MCP4728 DAC write | 0.2-1 ms | ✓ Yes | ✓ Acceptable |
| OLED partial update | 10-30 ms | ✓ Yes | ⚠️ Marginal |
| OLED full refresh | 50-280 ms | ✓ Yes | ❌ **CRITICAL** |

**Verdict:** Full OLED updates can **completely miss** note timing at fast tempos.

---

## Solution Architecture

### Priority Tiers

```
┌─────────────────────────────────────────┐
│ TIER 1: REAL-TIME CRITICAL              │
│ - MIDI input processing                 │
│ - CV/Gate output (MCP4728)              │
│ - Note event timing                     │
│ - Clock sync                            │
│ Target: < 5ms latency, < 2ms jitter     │
└─────────────────────────────────────────┘
          ↓ NO BLOCKING ALLOWED ↓
┌─────────────────────────────────────────┐
│ TIER 2: USER INTERFACE                  │
│ - OLED display updates                  │
│ - Button scanning                       │
│ - LED feedback                          │
│ Target: 10-30Hz update rate             │
└─────────────────────────────────────────┘
```

### Implementation Strategy

#### 1. **Display Throttling Pattern**

Never update display in the same loop iteration as CV output:

```python
# BAD - Display blocks CV output
def main_loop():
    if midi_note_event:
        dac.channel_a.raw_value = cv_lookup[note]
        display.text = f"Note: {note}"  # BLOCKS FOR 50ms!
        display.refresh()

# GOOD - Separate update schedules
last_display_update = 0
DISPLAY_UPDATE_INTERVAL = 100  # 10Hz max

def main_loop():
    now = supervisor.ticks_ms()

    # TIER 1: Always run (real-time critical)
    if midi_note_event:
        dac.channel_a.raw_value = cv_lookup[note]  # < 1ms

    # TIER 2: Throttled updates only
    if (now - last_display_update) >= DISPLAY_UPDATE_INTERVAL:
        display.text = f"Note: {note}"
        display.refresh()  # 50ms, but infrequent
        last_display_update = now
```

#### 2. **Double-Buffered Display Updates**

Prepare display content without refreshing, batch updates:

```python
# Track what needs display update
display_dirty = False
pending_note = None

def on_note_event(note):
    # Critical path: Update CV immediately
    dac.channel_a.raw_value = cv_lookup[note]

    # Non-critical: Flag for later display
    pending_note = note
    display_dirty = True

def display_update_task():
    if display_dirty and (time_since_last > 100):
        display.text = f"Note: {pending_note}"
        display.refresh()  # Blocking, but scheduled
        display_dirty = False
```

#### 3. **Performance Mode (Display-Free)**

For critical live use:

```python
class ArpSettings:
    performance_mode = False  # User toggle

def main_loop():
    if midi_note_event:
        dac.channel_a.raw_value = cv_lookup[note]

    # Skip display entirely in performance mode
    if not settings.performance_mode:
        throttled_display_update()
```

#### 4. **I2C Manager Class**

Centralize all I2C access with priority scheduling:

```python
class I2CManager:
    def __init__(self, i2c_bus):
        self.bus = i2c_bus
        self.dac = adafruit_mcp4728.MCP4728(i2c_bus)
        self.display = init_display(i2c_bus)
        self.last_display_update = 0

    def update_cv(self, midi_note):
        """TIER 1: Real-time critical - always execute"""
        raw_value = self.midi_to_cv_lookup[midi_note]
        self.dac.channel_a.raw_value = raw_value
        # Returns immediately (< 1ms)

    def update_gate(self, state):
        """TIER 1: Real-time critical"""
        self.dac.channel_c.raw_value = 4095 if state else 0

    def update_display(self, text, force=False):
        """TIER 2: Throttled, non-blocking"""
        now = supervisor.ticks_ms()
        if force or (now - self.last_display_update > 100):
            self.display.text = text
            self.display.refresh()  # Blocking
            self.last_display_update = now
```

---

## Testing Protocol

### 1. Measure Actual Timing

Run `tests/i2c_timing_test.py` to measure:
- DAC update time (should be < 1ms)
- OLED update time (expect 10-280ms)
- Combined operation time

### 2. Stress Test

```python
# Worst case: Fast arpeggio with display updates
# Run for 5 minutes at 200 BPM, 16th notes
# Monitor for:
# - Missed note events
# - CV voltage jitter (oscilloscope)
# - Audio artifacts (listen to VCO)
```

### 3. Acceptance Criteria

| Metric | Target | Critical Threshold |
|--------|--------|--------------------|
| CV update latency | < 1ms | < 5ms |
| CV update jitter | < 0.5ms | < 2ms |
| Note timing accuracy | ±0ms | ±3ms |
| Display update rate | 10Hz | 3Hz minimum |
| Missed notes | 0 | 0 (absolute) |

---

## Implementation Phases

### Phase 1: Measure Current State ✅ (This session)
- [x] Create timing test
- [ ] Run test and collect data
- [ ] Identify actual blocking times
- [ ] Determine if problem exists

### Phase 2: Implement Display Throttling
- [ ] Add display update scheduling
- [ ] Separate TIER 1 and TIER 2 paths
- [ ] Test timing improvements

### Phase 3: Create I2C Manager
- [ ] Centralize I2C device access
- [ ] Implement priority-based updates
- [ ] Add performance mode toggle

### Phase 4: Stress Testing
- [ ] 5-minute continuous arpeggio test
- [ ] Oscilloscope CV jitter analysis
- [ ] Audio quality verification

---

## Alternative Solutions (If Needed)

If CircuitPython I2C blocking proves insurmountable:

### Option A: SPI Display

| Pros | Cons |
|------|------|
| Much faster (10-20x) | Requires more pins |
| Non-blocking capable | Different display library |
| Better for real-time | Hardware change required |

### Option B: Dual MCU Architecture

| Pros | Cons |
|------|------|
| Complete separation | Added complexity |
| Zero I2C contention | Extra hardware cost |
| Proven in pro gear | Communication overhead |

```
┌─────────────────┐     Serial/SPI      ┌─────────────────┐
│  MCU 1: Audio   │ ←─────────────────→ │  MCU 2: Display │
│  - CV/Gate      │    Status updates   │  - OLED         │
│  - MIDI         │                     │  - Buttons      │
│  - Timing       │                     │  - LEDs         │
└─────────────────┘                     └─────────────────┘
```

### Option C: No Display Mode

Simplest solution for pro use:
- Remove OLED entirely
- Use USB serial for status
- CV/Gate only (zero latency)

---

## References

- [Teensy Forum: Audio cuts out with OLED](https://forum.pjrc.com/index.php?threads/audio-cuts-out-when-updating-i2c-oled-display.67141/)
- [Non-blocking I2C discussion](https://forum.pjrc.com/index.php?threads/non-blocking-i2c-library-or-i2c-oled-display-alternative.71909/)
- CircuitPython I2C clock stretching issues
- HiFiBerry DAC + OLED interference report

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-10-31 | Investigate I2C timing | User raised accuracy concerns |
| 2025-10-31 | Create timing test | Need empirical data |
| TBD | Select mitigation strategy | Based on test results |

---

**Next Action:** Run `i2c_timing_test.py` and analyze results before proceeding.
