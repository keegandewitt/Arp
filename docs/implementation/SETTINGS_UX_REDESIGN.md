# Settings UX Redesign
## prisme Translation Hub - Intuitive Settings Philosophy

**Date:** 2025-11-01
**Status:** Design Phase
**Inspiration:** "Option B" - Timing Feel unified control

---

## Design Philosophy

**Core Principle:** The value of a setting should naturally determine its behavior. Users shouldn't need to enable/disable features separately when the value itself can indicate intent.

**"Option B" Example:**
```
BAD:  Swing Enabled: On/Off + Swing Amount: 50-75%
      Humanize Enabled: On/Off + Humanize Amount: 0-100%

GOOD: Timing Feel: 50% (robot) → 65% (swing) → 85% (humanize)
      Single control, behavior adapts to range
```

---

## Current Settings Analysis

### Current Structure (8 categories, 27+ settings)

```
Clock (5 settings)
├── Source: Internal / External
├── BPM: 30-300
├── Swing: 50-75%
├── Multiply: 1x / 2x / 4x
└── Divide: /1 / /2 / /4 / /8

Translation (4 settings)
├── Mode: THRU / TRANSLATION
├── Input: MIDI IN / USB / CV / GATE
├── Clock Enabled: On / Off
└── [Vintage Mode: On / Off] (new)

Arp (2 settings)
├── Pattern: 16 types
└── Octaves: 1-4

Scale (2 settings)
├── Type: Chromatic / Major / Minor / etc.
└── Root: C / C# / D / etc.

Triggers (1 setting)
└── Gate Length: 0.1-1.0

CV (2 settings)
├── Enabled: On / Off
└── Scale: 1V/oct / Moog

Custom CC (3 settings)
├── Source: Disabled / CC / Aftertouch / Pitch / Velocity
├── CC Number: 0-127
└── Smoothing: Off / Low / Mid / High

Firmware (1 setting)
└── Version: (display only)
```

---

## Proposed Redesigns

### 🔴 HIGH IMPACT CHANGES

#### 1. Clock: Combine Multiply & Divide → **Clock Rate**

**Current Problem:**
- Two separate settings: Multiply (1x/2x/4x) and Divide (/1/2/4/8)
- Confusing: Do they stack? Which one to use?
- 3 multiply × 4 divide = 12 combinations (but only 7 unique rates)

**Proposed Solution: Clock Rate**
```
Single setting with values: /8, /4, /2, 1x, 2x, 4x, 8x

Range behavior:
- Left of 1x (< 100%) = Division (slower)
- 1x (100%) = No transformation (transparent)
- Right of 1x (> 100%) = Multiplication (faster)

Display: "Clock Rate: /4" or "Clock Rate: 2x"
```

**Benefits:**
- One control, intuitive direction
- Clear mental model: left = slower, right = faster
- Values map to musical divisions naturally

**Implementation:**
```python
# New unified setting
self.clock_rate = 1.0  # Multiplier: 0.125=/8, 0.25=/4, 0.5=/2, 1.0=1x, 2.0=2x, 4.0=4x, 8.0=8x

# Or as enum for menu navigation:
CLOCK_RATE_DIV_8 = 0
CLOCK_RATE_DIV_4 = 1
CLOCK_RATE_DIV_2 = 2
CLOCK_RATE_1X = 3  # Default
CLOCK_RATE_2X = 4
CLOCK_RATE_4X = 5
CLOCK_RATE_8X = 6

self.clock_rate = CLOCK_RATE_1X

def get_clock_multiply_divide(self):
    """Convert clock_rate to multiply/divide for clock engine"""
    if self.clock_rate <= CLOCK_RATE_1X:
        # Division
        divide = 2 ** (CLOCK_RATE_1X - self.clock_rate)
        return 1, int(divide)
    else:
        # Multiplication
        multiply = 2 ** (self.clock_rate - CLOCK_RATE_1X)
        return int(multiply), 1
```

**Storage:** 1 byte (enum) vs 2 bytes (multiply + divide)
**Saves:** 1 byte

---

#### 2. Clock: Unified **Timing Feel** (Replaces Swing + Humanize)

**Current Problem:**
- Swing: 50-75% (consistent delay)
- Humanize: 0-100% (random variation) [proposed feature]
- Two settings for timing modification

**Proposed Solution: Timing Feel**
```
Single setting: 50-100%

Range behavior:
- 50% = Perfect robot timing (quantized grid)
- 51-75% = Swing (consistent groove, Roger Linn method)
  * 50% = no swing
  * 66% = triplet feel (sweet spot)
  * 75% = maximum swing
- 76-100% = Humanize (increasing randomness)
  * 76% = subtle variation (±10ms)
  * 90% = moderate variation (±30ms)
  * 100% = maximum human feel (±50ms)

Display:
- "Feel: 50%" = Robot
- "Feel: 66%" = Swing
- "Feel: 85%" = Human
```

**Benefits:**
- Intuitive progression: Robot → Groove → Human
- One control for all timing feel
- Natural mapping: more = more feel

**Implementation:**
```python
# New unified setting
self.timing_feel = 50  # 50-100%

def apply_timing_feel(self, note_time, bpm):
    """Apply timing feel to scheduled note time"""
    if self.timing_feel == 50:
        return note_time  # Perfect timing

    if self.timing_feel <= 75:
        # Swing range (51-75%)
        # Map 51-75 to swing 1-75%
        swing_amount = (self.timing_feel - 50) * 3  # 51→3%, 75→75%
        return self.apply_swing(note_time, swing_amount, bpm)
    else:
        # Humanize range (76-100%)
        # Map 76-100 to humanize 1-100%
        humanize_amount = (self.timing_feel - 75) * 4  # 76→4%, 100→100%
        return self.apply_humanize(note_time, humanize_amount, bpm)

def apply_swing(self, note_time, swing_percent, bpm):
    """Roger Linn swing method (existing)"""
    # Existing swing implementation
    pass

def apply_humanize(self, note_time, humanize_percent, bpm):
    """Random timing variation"""
    import random
    max_variation = min(0.050, sixty_fourth_note)
    variation = max_variation * (humanize_percent / 100.0)
    offset = random.uniform(-variation, variation)
    return note_time + offset
```

**Storage:** 1 byte (timing_feel) vs 2 bytes (swing + humanize)
**Saves:** 1 byte

**Display on Main Screen:**
```
Before: "CLK SRC: Int  BPM: 120 (sw:66% H40%)"
After:  "CLK SRC: Int  BPM: 120 (Feel:66%)"
```

---

#### 3. Clock: Remove "Clock Enabled" - Make Automatic

**Current Problem:**
- "Clock Enabled: On/Off" - what does this even mean?
- If disabled, does clock still run? Do transformations apply?
- Confusing user mental model

**Proposed Solution: Auto-Detect Based on Values**
```
Clock transformations are "enabled" when values differ from defaults:
- Clock Rate ≠ 1x → Clock is active
- Timing Feel ≠ 50% → Clock is active
- Otherwise → Clock is transparent (1:1 pass-through)

No separate "enabled" toggle needed!
```

**Benefits:**
- One less setting to think about
- Behavior is obvious from values
- Clock display shows active transformations automatically

**Implementation:**
```python
def is_clock_active(self):
    """Check if clock transformations are active"""
    return (self.clock_rate != CLOCK_RATE_1X or
            self.timing_feel != 50)

def get_clock_display_name(self):
    """Get clock layer display name"""
    if not self.is_clock_active():
        return "Clk"  # Transparent

    # Show active transformations
    parts = []
    if self.clock_rate != CLOCK_RATE_1X:
        parts.append(self.get_clock_rate_short())
    if self.timing_feel != 50:
        parts.append(f"F{self.timing_feel}%")

    return "Clk(" + ",".join(parts) + ")"
```

**Storage:** Remove 1 byte (clock_enabled)
**Saves:** 1 byte

**Display Example:**
```
Clock Rate: 1x, Feel: 50% → "Clk" (transparent)
Clock Rate: 2x, Feel: 50% → "Clk(2x)"
Clock Rate: 1x, Feel: 66% → "Clk(F66%)"
Clock Rate: 2x, Feel: 85% → "Clk(2x,F85%)"
```

---

#### 4. Arp: Octaves 0-4 (0 = Arp Disabled)

**Current Problem:**
- Octave Range: 1-4
- Separate "Arp Enabled" boolean in code
- Two ways to disable arp

**Proposed Solution: Octaves 0-4**
```
Octave Range: 0-4

Range behavior:
- 0 = Arp disabled (notes pass through)
- 1 = Single octave arpeggio (current default)
- 2-4 = Multi-octave arpeggios

Natural mental model: 0 octaves = no arp
```

**Benefits:**
- No separate "enabled" boolean needed
- Zero is intuitive for "off"
- Still have all arp ranges (1-4)

**Implementation:**
```python
self.octave_range = 1  # Default: 0-4 (0=disabled)

def is_arp_enabled(self):
    """Check if arp is active"""
    return self.octave_range > 0

# In arpeggiator.py:
if not settings.is_arp_enabled():
    # Pass through notes directly
    self.output_note(note, velocity)
else:
    # Add to arp buffer
    self.add_note(note, velocity)
```

**Storage:** No change (still 1 byte)
**Saves:** Conceptual clarity

**Display:**
```
Octaves: 0 → Arp layer disappears from display
Octaves: 1-4 → "Arp(Up)" shown
```

---

#### 5. Scale: Auto-Detect Enabled (Chromatic = Disabled)

**Current Problem:**
- Scale Type: Chromatic / Major / Minor / etc.
- Separate "Scale Enabled" boolean
- Chromatic = "all notes allowed" = effectively disabled

**Proposed Solution: Auto-Detect**
```
Scale is "enabled" when:
- scale_type != SCALE_CHROMATIC

Chromatic scale means "no quantization" = disabled behavior

No separate "enabled" toggle needed!
```

**Benefits:**
- One less setting
- Chromatic is natural "off" state
- Behavior matches user mental model

**Implementation:**
```python
def is_scale_enabled(self):
    """Check if scale quantization is active"""
    return self.scale_type != self.SCALE_CHROMATIC

# In translation.py:
if settings.is_scale_enabled():
    self.layers.append(ScaleQuantizeLayer(settings))
```

**Storage:** Remove 1 byte (scale_enabled)
**Saves:** 1 byte

**Display:**
```
Scale: Chromatic → Scale layer disappears from display
Scale: Major/Minor/etc → "Scale(Maj)" shown
```

---

#### 6. CV: Remove "CV Enabled" Toggle

**Current Problem:**
- CV Enabled: On / Off
- CV Scale: 1V/oct / Moog
- Why toggle off CV output? Just don't plug anything in!

**Proposed Solution: Always Enabled**
```
CV output is always active (hardware always outputs voltage)

If user doesn't want CV:
- Don't plug a cable into CV jack
- Output still works, just goes nowhere

Remove the "Enabled" toggle entirely
```

**Benefits:**
- One less setting
- CV is a hardware output - it's always "on"
- Simpler mental model

**Implementation:**
```python
# Remove self.cv_enabled

# In cv_gate.py:
# Always output CV (no enable check)
self.set_cv_output(note, voltage)
```

**Storage:** Remove 1 byte (cv_enabled)
**Saves:** 1 byte

---

#### 7. Custom CC: Source "Disabled" → Remove, Use CC#0

**Current Problem:**
- Source: Disabled / CC / Aftertouch / Pitch / Velocity
- "Disabled" is first option - extra enum value

**Proposed Solution: Automatic Detection**
```
Custom CC is "disabled" when:
- Source = CC AND CC Number = 0

OR simpler:
- Just remove "Disabled" option entirely
- If user doesn't want Custom CC, set Smoothing = Off
- Smoothing Off = no output (alpha = 1.0 → no change)

No separate "Disabled" enum needed!
```

**Benefits:**
- One less enum value to cycle through
- Smoothing Off is natural "disabled" state
- Faster to navigate (4 sources instead of 5)

**Implementation:**
```python
# Remove CC_SOURCE_DISABLED

# Source options: CC, Aftertouch, Pitch, Velocity (4 values)
CC_SOURCE_CC = 0
CC_SOURCE_AFTERTOUCH = 1
CC_SOURCE_PITCHBEND = 2
CC_SOURCE_VELOCITY = 3

def is_custom_cc_enabled(self):
    """Check if Custom CC output is active"""
    return self.custom_cc_smoothing != self.CC_SMOOTH_OFF
```

**Storage:** No change (still 1 byte)
**Saves:** Menu navigation time

---

### 🟡 MEDIUM IMPACT CHANGES

#### 8. Translation: Vintage Mode → **MIDI Filter Preset**

**Current Proposal:**
- Vintage Mode: On / Off (filters Active Sensing, Aftertouch, Program Change)

**Better Idea: MIDI Filter Presets**
```
MIDI Filter: Off / Vintage / Minimal / Custom

Presets:
- Off: All messages pass through (current behavior)
- Vintage: Safe for old synths (filter Active Sensing, Aftertouch, Prog Change)
- Minimal: Only Note + Clock (ultra-safe)
- Custom: User picks individual message types (future feature)

Range determines filter aggressiveness
```

**Benefits:**
- More flexible than binary on/off
- "Vintage" is just one preset
- Room to grow (Minimal, Custom, etc.)

**Implementation:**
```python
# MIDI filter presets
MIDI_FILTER_OFF = 0      # Pass everything
MIDI_FILTER_VINTAGE = 1  # Safe for vintage synths
MIDI_FILTER_MINIMAL = 2  # Only Note + Clock (future)
MIDI_FILTER_CUSTOM = 3   # User-defined (future)

self.midi_filter = MIDI_FILTER_OFF  # Default

def should_filter_message(self, msg):
    """Check if message should be filtered"""
    if self.midi_filter == MIDI_FILTER_OFF:
        return False

    if self.midi_filter == MIDI_FILTER_VINTAGE:
        # Filter problematic messages for vintage synths
        return isinstance(msg, (ActiveSensing, ChannelPressure,
                                PolyphonicKeyPressure, ProgramChange))

    # Future: MIDI_FILTER_MINIMAL, MIDI_FILTER_CUSTOM
    return False
```

**Storage:** 1 byte (same as vintage_mode boolean)
**Future:** Can expand to custom filters without changing storage

---

#### 9. Likelihood: 100% = Disabled (No Separate Toggle)

**Current Proposal:**
- Likelihood: 0-100%
- Likelihood Mode: All Notes / Arp Only

**Better Idea: 100% = Off**
```
Likelihood: 0-100%

Range behavior:
- 100% = All notes play (disabled, current behavior)
- 50% = Half notes play (moderate)
- 0% = No notes play (extreme)

No "mode" toggle - just apply to all post-translation notes

When at 100% → Feature is transparent (disabled)
```

**Benefits:**
- No separate enabled/disabled state
- 100% is natural "off"
- One control, clear behavior

**Implementation:**
```python
self.likelihood = 100  # Default: 0-100 (100 = disabled)

def should_trigger_note(self):
    """Check if note should play based on likelihood"""
    if self.likelihood >= 100:
        return True  # Always play (disabled)

    if self.likelihood <= 0:
        return False  # Never play

    return random.randint(1, 100) <= self.likelihood
```

**Storage:** 1 byte (remove likelihood_mode)
**Saves:** 1 byte

---

### 🟢 LOW IMPACT / KEEP AS-IS

#### 10. Routing Mode: THRU / TRANSLATION (Keep)
- Clear binary choice
- Fundamentally different behaviors
- No room for range-based logic
- **KEEP AS-IS**

#### 11. Input Source: MIDI IN / USB / CV / GATE (Keep)
- Discrete hardware sources
- Not a range/spectrum
- **KEEP AS-IS**

#### 12. Clock Source: Internal / External (Keep)
- Discrete hardware sources
- Not a range/spectrum
- **KEEP AS-IS**

#### 13. BPM: 30-300 (Keep)
- Already a range control
- Direct value, no abstraction needed
- **KEEP AS-IS**

#### 14. Arp Pattern: 16 Types + Strum (Keep)
- Discrete algorithms
- Not a range/spectrum
- **KEEP AS-IS**

#### 15. Scale Type: Chromatic / Major / Minor / etc. (Keep)
- Discrete musical scales
- Not a range/spectrum
- **KEEP AS-IS** (but auto-detect enabled via Chromatic)

#### 16. Scale Root: C / C# / D / etc. (Keep)
- Discrete notes
- Not a range/spectrum
- **KEEP AS-IS**

#### 17. Gate Length: 0.1-1.0 (Keep)
- Already a range control
- Direct value, clear meaning
- **KEEP AS-IS**

#### 18. CV Scale: 1V/oct / Moog (Keep)
- Two hardware standards
- Not a range/spectrum
- **KEEP AS-IS** (but remove CV enabled toggle)

#### 19. Trigger Polarity: V-trig / S-trig (Keep)
- Two hardware standards
- Not a range/spectrum
- **KEEP AS-IS**

#### 20. Strum Settings (Keep - if we implement)
- Speed: Clock divisions (discrete)
- Octaves: 1-4 (already a range)
- Repeat: One-shot / Loop (binary choice)
- Direction: Up / Down / UpDown (discrete)
- **KEEP AS-IS** (all make sense)

---

## Summary of Changes

### Settings Before Redesign: 27 values, 35 bytes

### Settings After Redesign: 24 values, 30 bytes

**Removed:**
1. ~~clock_multiply~~ → Merged into clock_rate
2. ~~clock_divide~~ → Merged into clock_rate
3. ~~swing_percent~~ → Merged into timing_feel
4. ~~clock_enabled~~ → Auto-detect from clock_rate + timing_feel
5. ~~scale_enabled~~ → Auto-detect from scale_type != CHROMATIC
6. ~~cv_enabled~~ → Always on (hardware output)

**Added:**
1. clock_rate (1 byte) - Replaces multiply + divide
2. timing_feel (1 byte) - Replaces swing + humanize
3. midi_filter (1 byte) - Replaces vintage_mode boolean
4. likelihood (1 byte)

**Net Change:** -6 removed, +1 combined, +3 new = 27 → 24 values
**Storage:** 35 → 30 bytes (5 bytes saved)

---

## New Menu Structure

### Clock (4 settings) ← Was 5
1. Source: Internal / External
2. BPM: 30-300
3. **Clock Rate: /8 / /4 / /2 / 1x / 2x / 4x / 8x** (NEW - replaces multiply/divide)
4. **Timing Feel: 50-100%** (NEW - replaces swing/humanize)

### Translation (4 settings) ← Was 4
1. Mode: THRU / TRANSLATION
2. Input: MIDI IN / USB / CV / GATE
3. **MIDI Filter: Off / Vintage / Minimal** (NEW - replaces vintage boolean)
4. **Likelihood: 0-100%** (NEW)

### Arp (2-7 settings) ← Was 2
1. Pattern: [UP, DOWN, ..., STRUM]
2. **Octaves: 0-4** (CHANGED - was 1-4, now 0=disabled)
3. [Strum settings only if Pattern=STRUM]

### Scale (2 settings) ← Was 2
1. Type: Chromatic / Major / Minor / etc. (Chromatic = disabled)
2. Root: C / C# / D / etc.

### Triggers (1 setting) ← Was 1
1. Gate Length: 0.1-1.0

### CV (1 setting) ← Was 2
1. Scale: 1V/oct / Moog *(CV always enabled)*

### Custom CC (3 settings) ← Was 3
1. Source: CC / Aftertouch / Pitch / Velocity *(Disabled removed)*
2. CC Number: 0-127
3. Smoothing: Off / Low / Mid / High *(Off = disabled)*

### Firmware (1 setting) ← Was 1
1. Version: (display only)

**Total Categories:** 8 (unchanged)
**Total Settings:** 18-23 (down from 27)

---

## Display Updates

### Main Screen Format (3 lines)

**Before:**
```
MODE: XLAT  IN: MIDI
CLK SRC: Int  BPM: 120 (sw:66% x2)
XLAT: Scale(Maj) -> Arp(Up) - Clk(Int)
```

**After:**
```
MODE: XLAT  IN: MIDI [VINTAGE]
CLK SRC: Int  BPM: 120 (2x F66%)
XLAT: Scale(Maj) -> Arp(Up,L80%) - Clk(2x,F66%)
```

**Legend:**
- `[VINTAGE]` = MIDI Filter: Vintage mode
- `2x` = Clock Rate: 2x (multiply)
- `F66%` = Timing Feel: 66% (swing)
- `L80%` = Likelihood: 80%

**Advantages:**
- More compact notation
- All active features visible
- No redundant information

---

## Implementation Strategy

### Phase 1: No Breaking Changes (1-2 days)
1. Add new unified controls (clock_rate, timing_feel, midi_filter, likelihood)
2. Keep old controls, map them internally
3. Test everything still works

### Phase 2: Menu Updates (1 day)
4. Update menu.py to show new controls
5. Update display.py with new format

### Phase 3: Remove Old Controls (1 day)
6. Remove: multiply, divide, swing, clock_enabled, scale_enabled, cv_enabled
7. Update save/load format (NVM migration)
8. Update tests

### Phase 4: Documentation (1 day)
9. Update user manual
10. Update design docs

**Total Time:** 4-5 days

---

## User Experience Benefits

### Before Redesign:
```
User: "I want faster clock"
Settings: Clock → Multiply: 1x / 2x / 4x
         Clock → Divide: /1 / /2 / /4 / /8
User: "Which one do I change? Do they stack?"
```

### After Redesign:
```
User: "I want faster clock"
Settings: Clock → Clock Rate: [... 1x | 2x | 4x ...]
User: "Oh, just turn it right. Easy!"
```

---

### Before Redesign:
```
User: "I want some groove"
Settings: Clock → Swing: 50-75%
User: "Is 66% good? Let me try... yeah!"

Later...

User: "Now I want it more human/random"
Settings: Arp → Humanize: 0-100%
User: "Wait, is this separate from swing? Do they work together?"
```

### After Redesign:
```
User: "I want some groove"
Settings: Clock → Timing Feel: 50-100%
User: "Turn it up... 66% nice swing!
      Turn it more... 85% oh cool, it's getting random/human now!
      This is intuitive!"
```

---

## Questions for User

1. **Clock Rate:** Does the unified /8 → 8x range make sense? Or too radical?

2. **Timing Feel:** Love the 50-100% unified control? Or prefer separate Swing + Humanize?

3. **Auto-Detect Disabled:** Comfortable with settings auto-disabling based on values? Or prefer explicit toggles?

4. **MIDI Filter Presets:** Better than binary Vintage On/Off? Room to grow?

5. **Octaves 0-4:** Does 0 octaves = disabled make sense? Or too weird?

6. **CV Always On:** OK to remove CV Enabled toggle? Just don't plug cable if not needed?

7. **Priority:** Implement these UX improvements before or after new features (Strum, Likelihood)?

---

## Recommendation

**My Vote: Implement ALL of these changes!**

Why:
- Users will love the intuitive controls
- Saves 5 bytes of NVM (room for future features)
- Reduces cognitive load (fewer settings)
- More room on display (compact notation)
- Feels professional and polished

**Timeline:**
- 4-5 days to implement all UX improvements
- Then implement new features (Strum, Likelihood, etc.)
- Result: Fewer settings, more features, better UX

---

**Next Step:** Get your feedback, then start implementing! 🎛️✨

---

**Generated:** 2025-11-01
**Author:** the development environment (Session 16)
**Status:** Design Complete - Awaiting User Approval
