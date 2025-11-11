# Creative Features Design
## prisme Translation Hub - Phase 6 Enhancements

**Date:** 2025-11-01
**Status:** Design Phase
**Purpose:** Add creative performance features to prisme Translation Hub

---

## Philosophy

prisme is a **creative translation hub**, not a generic MIDI processor. We focus on features that enable musical expression and creative experimentation, not utility routing.

**Design Principles:**
- Features should be musically expressive
- Simple to use, deep to master
- Work together to create emergent behavior
- No feature bloat - only what serves the music

---

## Feature 1: Vintage Synth Auto-Filter

### Problem Statement
User's Juno 60 (and many vintage synths) get confused when receiving all MIDI messages from DAW. Only Clock + Note messages work reliably.

### Research Findings

**Problematic MIDI Messages for Vintage Synths:**
1. **Active Sensing (0xFE)** - Most common culprit
   - Sent every 300ms by some devices
   - Many vintage synths don't implement it properly
   - Can cause hanging notes, confusion

2. **Aftertouch** - Channel Pressure (0xD0) & Polyphonic (0xA0)
   - Not implemented on many vintage synths
   - Can cause unwanted modulation if wired wrong

3. **Program Change (0xC0)**
   - Can cause unexpected patch changes

4. **Continuous Controllers (0xB0)**
   - Some vintage synths only understand specific CCs
   - Others can be confused by unknown CC numbers

**Safe Messages for Vintage Synths:**
- ✅ Note On/Off (0x80, 0x90)
- ✅ Pitch Bend (0xE0)
- ✅ Timing Clock (0xF8)
- ✅ Start/Stop/Continue (0xFA, 0xFC, 0xFB)
- ✅ System Exclusive (0xF0) - if synth supports it

### Implementation Design

**Setting: `vintage_mode`** (Boolean, default: False)
- Add to Translation category in menu
- "Vintage Mode: Off / On"

**When Enabled:**
```python
# Auto-filter these message types:
FILTER_LIST = [
    ActiveSensing,           # 0xFE - Most problematic
    ChannelPressure,         # 0xD0 - Aftertouch
    PolyphonicKeyPressure,   # 0xA0 - Poly Aftertouch
    ProgramChange,           # 0xC0 - Patch changes
]

# ALLOW these messages (safe for vintage):
ALLOW_LIST = [
    NoteOn,                  # 0x90
    NoteOff,                 # 0x80
    PitchBend,               # 0xE0
    TimingClock,             # 0xF8
    Start, Stop, Continue,   # 0xFA, 0xFC, 0xFB
    # SystemExclusive,       # 0xF0 - controversial, maybe optional?
]

# ControlChange - selective filtering
# Allow: Mod Wheel (CC1), Volume (CC7), Pan (CC10), Expression (CC11)
# Filter: Everything else
SAFE_CC_NUMBERS = [1, 7, 10, 11]
```

**Display:**
- Show "VINTAGE" indicator on main screen when enabled
- Maybe replace "MODE: XLAT" with "MODE: XLAT (VINTAGE)"

**Benefits:**
- Automatic - user doesn't need to know what to filter
- Based on research and real-world usage (Juno 60)
- Can be toggled on/off quickly

**Testing:**
- User's Juno 60 (real-world test)
- Other vintage synths if available

---

## Feature 2: Strum Arpeggiator Mode

### Concept
Like strumming a guitar - play chord notes sequentially with configurable speed and range.

### Use Cases
- Guitar-like performance on synths
- Harp glissandos
- Rapid arpeggios
- Expressive chord voicings

### Parameters

#### 1. **Pattern:** `STRUM` (Pattern 16)
- Add to existing 16 arpeggiator patterns
- Direction sub-modes:
  - Strum Up (low to high)
  - Strum Down (high to low)
  - Strum UpDown (alternate)

#### 2. **Speed:** Clock Division (new setting)
- How fast to strum through notes
- Values: 1/64, 1/32, 1/16, 1/8, 1/4
- Default: 1/32 (fast strum)
- Smaller = faster strum, larger = slower/more deliberate

#### 3. **Octaves:** Note Range Multiplier (new setting)
- How many octaves to strum across
- Values: 1, 2, 3, 4
- Default: 1 (just the chord notes as played)
- Example: Play C-E-G with Octaves=2 → C3, E3, G3, C4, E4, G4, C5

#### 4. **Repeat:** One-shot vs Loop (new setting)
- One-shot: Strum once when chord changes, then stop
- Loop: Continuously strum (like existing arp patterns)
- Default: One-shot (more guitar-like)

### Implementation

**Data Structure:**
```python
# New settings (add to Settings class)
self.strum_speed = 5      # Index: 0=/64, 1=/32, 2=/16, 3=/8, 4=/4, 5=/2
self.strum_octaves = 1    # 1-4 octaves
self.strum_repeat = False # One-shot or loop
self.strum_direction = 0  # 0=Up, 1=Down, 2=UpDown
```

**Algorithm:**
```python
def generate_strum_pattern(self, chord_notes, octaves):
    """Generate strum pattern from chord notes"""
    pattern = []

    # Sort notes (lowest to highest)
    sorted_notes = sorted(chord_notes)

    # Multiply across octaves
    for octave in range(octaves):
        for note in sorted_notes:
            extended_note = note + (octave * 12)
            if extended_note <= 127:  # MIDI note range
                pattern.append(extended_note)

    # Apply direction
    if self.strum_direction == 1:  # Down
        pattern.reverse()
    elif self.strum_direction == 2:  # UpDown
        pattern = pattern + pattern[-2:0:-1]  # Up, then down (no repeat of ends)

    return pattern

def step_strum(self):
    """Step through strum pattern at configured speed"""
    if not self.strum_pattern or self.strum_index >= len(self.strum_pattern):
        if self.strum_repeat:
            self.strum_index = 0  # Loop
        else:
            return  # One-shot complete

    current_note = self.strum_pattern[self.strum_index]
    self.output_note(current_note)
    self.strum_index += 1
```

**Clock Integration:**
- Strum speed determines step rate
- Independent of main clock division setting
- Could be 1/32 while main arp is 1/16

**Menu Structure:**
```
Arp
├── Pattern: [UP, DOWN, ..., STRUM] ← Add STRUM as pattern 16
├── Octaves: [1, 2, 3, 4]
├── Strum Speed: [/64, /32, /16, /8, /4, /2]
├── Strum Repeat: [One-shot, Loop]
└── Strum Dir: [Up, Down, UpDn]
```

**Display:**
- Pattern shows as "Strum"
- Maybe show speed/octaves: "Strum(/32,x2)"

---

## Feature 3: Humanize

### Concept
Add subtle timing and velocity variations to make performance less robotic and more human.

### NOT Swing
- **Swing** = Consistent, predictable timing offset (even notes delayed)
- **Humanize** = Random, subtle variations around the beat
- Both can coexist!

### Use Cases
- Less mechanical arpeggiator playback
- Groove that breathes
- Analog-feel timing
- Live performance realism

### Parameters

#### 1. **Humanize Amount:** Timing Variation
- Range: 0-100%
- 0% = Perfect timing (current behavior)
- 100% = Maximum variation (±50ms or ±1/64 note, whichever is smaller)
- Default: 0% (off)

#### 2. **Humanize Type:** What to Randomize
- **Timing Only** - Just note timing
- **Velocity Only** - Just note velocity
- **Both** - Timing + Velocity (most human)
- Default: Both

### Implementation

**Data Structure:**
```python
# New settings
self.humanize_amount = 0     # 0-100%
self.humanize_type = 2       # 0=Timing, 1=Velocity, 2=Both
```

**Algorithm:**
```python
import random

def apply_humanize_timing(self, note_time, bpm):
    """Add random timing variation around scheduled time"""
    if self.humanize_amount == 0:
        return note_time

    # Calculate max variation based on BPM
    # At 120 BPM: 1/64 note = 31.25ms
    # Use smaller of: 50ms or 1/64 note
    sixteenth_note = 60.0 / (bpm * 4)  # seconds
    sixty_fourth = sixteenth_note / 4
    max_variation = min(0.050, sixty_fourth)  # 50ms or 1/64 note

    # Scale by humanize amount
    variation_range = max_variation * (self.humanize_amount / 100.0)

    # Random offset: ±variation_range
    offset = random.uniform(-variation_range, variation_range)

    return note_time + offset

def apply_humanize_velocity(self, velocity):
    """Add random velocity variation"""
    if self.humanize_amount == 0 or velocity == 0:
        return velocity

    # Velocity variation: ±10% of humanize amount
    # At 100% humanize, ±10 velocity units
    max_variation = 10 * (self.humanize_amount / 100.0)

    # Random offset
    offset = random.uniform(-max_variation, max_variation)

    # Clamp to MIDI range
    new_velocity = int(velocity + offset)
    return max(1, min(127, new_velocity))  # Keep in 1-127 range

def output_humanized_note(self, note, velocity, scheduled_time):
    """Output note with humanization applied"""
    if self.humanize_type in [0, 2]:  # Timing or Both
        scheduled_time = self.apply_humanize_timing(scheduled_time, self.current_bpm)

    if self.humanize_type in [1, 2]:  # Velocity or Both
        velocity = self.apply_humanize_velocity(velocity)

    # Schedule note output at humanized time
    self.schedule_note(note, velocity, scheduled_time)
```

**Interaction with Swing:**
- Applied AFTER swing calculation
- Swing = predictable groove
- Humanize = subtle imperfection on top
- Order: Base timing → Swing → Humanize

**Menu Structure:**
```
Arp
├── ...
├── Humanize: [0-100%]
└── Humanize Type: [Timing, Velocity, Both]
```

**OR in Translation category:**
```
Translation
├── ...
├── Humanize: [0-100%]
└── Humanize Type: [Timing, Velocity, Both]
```

**Display:**
- Show on main screen: "XLAT: Scale(Maj) -> Arp(Up,H50%) - Clk(Int)"
- "H50%" = Humanize 50%

---

## Feature 4: Likelihood (Random Note Probability)

### Concept
Each note has a probability of actually being triggered - creates sparse, evolving patterns.

### Use Cases
- Euclidean-style rhythms
- Generative music
- Living patterns that evolve
- Controlled randomness

### Parameters

#### 1. **Likelihood:** Probability Percentage
- Range: 0-100%
- 0% = No notes play
- 50% = Half the notes play (on average)
- 100% = All notes play (default, current behavior)

#### 2. **Apply To:** What Gets Affected
- **All Notes** - Every note has X% chance
- **Arp Only** - Only affects arpeggiated notes (not direct input)
- **Specific Patterns** - Maybe only certain arp patterns?

### Implementation

**Data Structure:**
```python
# New settings
self.likelihood = 100   # 0-100% (100 = always play)
self.likelihood_mode = 0  # 0=All, 1=Arp Only
```

**Algorithm:**
```python
import random

def should_trigger_note(self):
    """Determine if note should actually play based on likelihood"""
    if self.likelihood >= 100:
        return True  # Always play

    if self.likelihood <= 0:
        return False  # Never play

    # Roll the dice
    roll = random.randint(1, 100)
    return roll <= self.likelihood

def output_note_with_likelihood(self, note, velocity):
    """Output note only if likelihood dice roll succeeds"""

    # Check mode
    if self.likelihood_mode == 1 and not self.is_arpeggiated:
        # Arp Only mode, but this is a direct note - always play
        self.output_note(note, velocity)
        return

    # Apply likelihood
    if self.should_trigger_note():
        self.output_note(note, velocity)
    else:
        # Note was rejected by likelihood - don't play
        # Could optionally send gate-off for CV output
        pass
```

**Where It Applies:**
- **AFTER** all translation layers (Scale → Arp → Clock)
- This is the final gate before note output
- Applies to both MIDI and CV/Gate outputs

**Timing:**
- Note is "scheduled" but not triggered
- Clock still advances (so pattern stays in time)
- Creates "holes" in the pattern

**Interaction with Strum:**
- Each strum note individually checked
- Creates interesting random strums
- Example: 50% likelihood on 8-note strum = ~4 notes play

**Menu Structure:**
```
Translation
├── ...
├── Likelihood: [0-100%]
└── Likelihood Mode: [All Notes, Arp Only]
```

**Display:**
- Show on main screen: "XLAT: Scale(Maj) -> Arp(Up,L75%) - Clk(Int)"
- "L75%" = 75% Likelihood

---

## Feature Integration

### How They Work Together

**Example 1: Humanized Strum with Likelihood**
```
Settings:
- Pattern: Strum
- Strum Speed: /32
- Strum Octaves: 2
- Humanize: 40% (Both)
- Likelihood: 70%

Result:
- Strum through 2 octaves of chord
- Each note slightly off-time and varied velocity (human feel)
- ~30% of notes randomly skip (sparse, interesting)
- Every strum is different!
```

**Example 2: Euclidean-Style Arp**
```
Settings:
- Pattern: Up
- Clock Division: /16
- Likelihood: 60%
- Humanize: 20%

Result:
- Classic up arpeggio pattern
- But only ~60% of notes play (creates rhythm)
- Slight timing variation (groove)
- Almost like Euclidean rhythm generator
```

**Example 3: Vintage Synth + Creative Layers**
```
Settings:
- Vintage Mode: On (safe for Juno 60)
- Scale: Major
- Pattern: Up-Down
- Humanize: 30%
- Likelihood: 80%

Result:
- No problematic MIDI messages sent
- Notes quantized to Major scale
- Up-down arpeggio with subtle humanization
- Occasional note drops for interest
- Juno 60 stays happy!
```

### Display Format

**Main Screen with All Features Active:**
```
MODE: XLAT (VINTAGE)  IN: MIDI
CLK SRC: Int  BPM: 120 (sw:66%)
XLAT: Scale(Maj) -> Arp(Strum,H40%,L70%) - Clk(Int)
```

**Abbreviations:**
- `H40%` = Humanize 40%
- `L70%` = Likelihood 70%
- `(VINTAGE)` = Vintage mode enabled

---

## Settings Storage Impact

### Current NVM Usage: 35/256 bytes (13.7%)

### New Settings (8 bytes total):
```python
# Vintage Mode (1 byte)
vintage_mode: bool = False

# Strum (3 bytes)
strum_speed: uint8 = 5       # 0-5 (6 values)
strum_octaves: uint8 = 1     # 1-4
strum_repeat: bool = False

# Humanize (2 bytes)
humanize_amount: uint8 = 0   # 0-100
humanize_type: uint8 = 2     # 0-2 (3 values)

# Likelihood (2 bytes)
likelihood: uint8 = 100      # 0-100
likelihood_mode: uint8 = 0   # 0-1 (2 values)
```

**New Total:** 43/256 bytes (16.8%)
**Remaining:** 213 bytes

Still plenty of room!

---

## Menu Structure Updates

### Translation Category (4 → 5 settings):
1. Mode: THRU / TRANSLATION
2. Input: MIDI IN / USB / CV IN / GATE IN
3. Clock: Enabled / Disabled
4. **Vintage Mode: Off / On** ← NEW
5. **Likelihood: 0-100%** ← NEW

### Arp Category (2 → 7 settings):
1. Pattern: [UP, DOWN, ..., **STRUM**] ← Add STRUM
2. Octaves: 1-4
3. **Strum Speed: [/64, /32, /16, /8, /4, /2]** ← NEW (only if Pattern=STRUM)
4. **Strum Repeat: [One-shot, Loop]** ← NEW (only if Pattern=STRUM)
5. **Strum Direction: [Up, Down, UpDown]** ← NEW (only if Pattern=STRUM)
6. **Humanize: 0-100%** ← NEW
7. **Humanize Type: [Timing, Velocity, Both]** ← NEW

**Total Categories:** Still 8
**Total Settings:** 27 → 35 (+8)

---

## Implementation Priority

### Phase 6a: Vintage Mode (Highest Priority)
**Why First:** Solves user's immediate problem (Juno 60)
**Complexity:** Low
**Time Estimate:** 1 day
**Files:**
- `arp/utils/config.py` - Add vintage_mode setting
- `main_v2.py` - Add filter logic to pass-through section
- `arp/ui/menu.py` - Add to Translation category

### Phase 6b: Likelihood (Quick Win)
**Why Second:** Simple, high creative impact
**Complexity:** Low
**Time Estimate:** 1 day
**Files:**
- `arp/utils/config.py` - Add likelihood settings
- `arp/core/arpeggiator.py` - Add probability check before output
- `arp/ui/menu.py` - Add to Translation category
- `arp/ui/display.py` - Show likelihood on display

### Phase 6c: Humanize (Medium Complexity)
**Why Third:** More complex timing, needs testing
**Complexity:** Medium
**Time Estimate:** 2-3 days
**Files:**
- `arp/utils/config.py` - Add humanize settings
- `arp/core/arpeggiator.py` - Add timing/velocity variation
- `arp/core/clock.py` - May need scheduled note support
- `arp/ui/menu.py` - Add to Arp category
- `tests/test_humanize.py` - New test file

### Phase 6d: Strum Mode (Most Complex)
**Why Last:** Most complex, needs new pattern type
**Complexity:** High
**Time Estimate:** 3-4 days
**Files:**
- `arp/utils/config.py` - Add strum settings
- `arp/core/arpeggiator.py` - New strum pattern generator
- `arp/ui/menu.py` - Add strum sub-settings
- `tests/test_strum.py` - New test file

**Total Time:** 7-9 days

---

## Testing Strategy

### Unit Tests
- Vintage filter correctly blocks/allows messages
- Likelihood probability distribution (100 iterations)
- Humanize timing stays within bounds
- Strum pattern generation
- Feature interactions (humanize + likelihood)

### Integration Tests
- All features work together
- Display shows correct abbreviations
- Settings save/load correctly
- No performance degradation

### Hardware Tests
- **Juno 60 with Vintage Mode** - User's real-world test
- Latency measurement with all features
- CV/Gate output with likelihood (gate still triggers?)
- Strum timing accuracy

---

## User Feedback Questions

1. **Vintage Mode:** Is auto-filtering the right approach? Or should user pick which messages?

2. **Humanize vs Swing:** Should we replace swing with humanize, or keep both?
   - My recommendation: Keep both - they serve different purposes

3. **Strum Sub-Settings:** Too many settings for one pattern? Or is granular control good?

4. **Likelihood Display:** "L70%" clear enough? Or show as "70%" somewhere?

5. **Priority:** Does this order make sense?
   - Vintage Mode → Likelihood → Humanize → Strum

---

**Next Step:** Get user feedback, then implement in priority order!

---

**Generated:** 2025-11-01
**Author:** the development environment (Session 16)
**Status:** Design Complete - Awaiting User Approval
