# VintageCapture Workflow Guide

**Complete step-by-step guide to capturing vintage synthesizer performances**

---

## Overview

VintageCapture solves the problem of using vintage synths (without MIDI Local Control Off) with external arpeggiators. It uses a two-stage workflow that separates **performance** from **sound design**.

### The Problem
Vintage synths like:
- Moog Source
- ARP Odyssey
- Korg MS-20
- Yamaha CS series

...don't have MIDI Local Control Off, so you can't intercept keyboard notes before they trigger the sound.

### The Solution
1. **Stage 1**: Capture your performance (notes, timing, velocity)
2. **Stage 2**: Play it back via Arp hardware to the vintage synth
3. During playback: Tweak synth parameters while DAW records audio

---

## Setup

### Hardware Required
1. **Vintage Synth** - The synth you want to capture
2. **Arp Hardware** - MIDI arpeggiator (connected via USB)
3. **Audio Interface** - For recording synth audio
4. **MIDI Keyboard** or use synth's keyboard

### Software Required
1. **DAW** - Ableton, Logic, Cubase, etc.
2. **VintageCapture VST** - This plugin

### Connections
```
[MIDI Keyboard] ──MIDI──> [Vintage Synth]
                             │
                             │ Audio Out
                             ↓
                       [Audio Interface] ──> [DAW]

[Arp Hardware] ──USB──> [Computer]
               ──MIDI OUT──> [Vintage Synth MIDI IN]
```

---

## Workflow

### Step 1: Calibration ("Press C3")

**Purpose:** Learn the synth's timing characteristics.

1. Load VintageCapture in your DAW
2. Set your synth to the sound you want
3. Click **[● REC C3]** in the calibration section
4. Press and hold **C3** for 2-3 seconds
5. Release the key
6. Click **[■ STOP]**

**What happens:**
- Plugin records the C3 note
- Analyzes attack time (how long to "speak")
- Analyzes release time (tail after key release)
- Creates reference sample for monitoring

**Display shows:**
```
Attack:  0.150s    Release: 0.800s
```

This tells the plugin: "This synth has a 150ms attack and 800ms release tail"

---

### Step 2: Keystroke Capture (Performance)

**Purpose:** Record your musical performance.

1. **Optional:** Enable **□ Enable Monitoring** for zero-latency playback
   - Monitoring uses the C3 sample, pitched to match each note
   - Instant feedback while playing

2. Click **[● REC]** in keystroke capture section

3. **Perform your part** on the vintage synth keyboard
   - Play naturally - timing and feel matter here
   - Don't worry about perfect sound yet
   - Focus on the right notes and rhythm

4. Click **[■ STOP]** when done

**Display shows:**
```
Recording: 47 notes, 16.32s
```

**What's captured:**
- Every note you played
- Note velocities
- Precise timing
- Note durations

**What's NOT captured:**
- Synth parameter positions (that's Stage 3!)
- Audio (not yet)

---

### Step 3: Playback & Capture (Sound Design)

**Purpose:** Perfect the sound while DAW records audio.

#### 3A: Prepare DAW
1. Arm an audio track to record from your interface
2. Optional: Enable loop mode for the section you want

#### 3B: Start Playback
1. Click **[▶ PLAY]** in playback section
2. VST sends MIDI buffer → Arp hardware → Vintage synth
3. Synth plays back your exact performance

#### 3C: Tweak Parameters
While it plays back (and DAW records):
- **Turn filter cutoff** - Sweeps are now perfectly repeatable
- **Adjust resonance** - Can do multiple takes
- **Tweak envelope** - No performance pressure
- **Modulate LFO** - Focus entirely on sound

#### 3D: Multiple Takes
- Try different filter sweeps on different passes
- DAW records each take as separate audio
- Comp the best moments together

4. Click **[■ STOP]** when you have your take

---

## Example Session

### Scenario: Capturing a Moog Source Bass Line

**Stage 1: Calibration**
```
1. Set Moog to: Square wave, Filter=50%, Resonance=30%
2. Record C3 for 2 seconds
3. Result: Attack=0.1s, Release=0.6s
```

**Stage 2: Keystroke Capture**
```
1. Enable monitoring ✓
2. Record
3. Play bass line: C2→E2→G2→C3 (16 bars)
4. Stop
5. Result: 64 notes captured, 32.0s
```

**Stage 3: Playback & Capture**
```
Take 1: Slow filter opening (bar 1-8)
  - Start: Filter=20%
  - End:   Filter=80%
  - DAW records → "bass_take1.wav"

Take 2: Resonance sweep on bar 12
  - Bar 1-11:  Resonance=30%
  - Bar 12-16: Resonance=70%
  - DAW records → "bass_take2.wav"

Take 3: LFO modulation on last 4 bars
  - Bar 1-12:  LFO off
  - Bar 13-16: LFO rate=0.5Hz, depth=50%
  - DAW records → "bass_take3.wav"

Final: Comp best parts of each take
```

---

## Tips & Tricks

### Monitoring Latency
- Enable monitoring for instant feedback
- If you hear latency, check audio interface buffer size
- Lower buffer = lower latency (but higher CPU)

### Calibration
- Calibrate once per synth preset
- If you change filter/envelope drastically, recalibrate
- Store multiple calibrations for different sounds

### Performance Tips
- Don't worry about being perfect in Stage 2
- You can loop playback in Stage 3 and fix timing issues
- Focus on feel and musicality in Stage 2

### Sound Design Tips
- Start with subtle parameter changes
- Record multiple takes with different approaches
- Use DAW automation to blend takes

### Arp Settings
- Arp pattern controls are sent via USB MIDI
- Set pattern/division/octaves in your DAW or Arp UI
- Arp just arpeggiates what you performed

---

## Troubleshooting

### "No sound during monitoring"
- Check: Did you complete calibration?
- Check: Is monitoring enabled?
- Check: DAW monitoring setup

### "Playback sounds different from performance"
- This is normal! You can now tweak parameters
- If timing is wrong, re-record Stage 2

### "Calibration failed"
- Make sure you held C3 for full 2+ seconds
- Check audio is actually reaching the plugin
- Try again with different synth settings

### "Arp not responding"
- Check USB connection to Arp hardware
- Verify MIDI output is set to Arp
- Check Arp is in "Vintage Mode"

---

## Advanced Techniques

### Multi-Scene Calibration
1. Calibrate once for verse sound
2. Capture performance
3. Re-calibrate for chorus sound (brighter)
4. Assign sections to different calibrations

### Hybrid Workflow
- Capture main performance in Stage 2
- Manually play additional parts in Stage 3
- Layer multiple performances

### Automation
- Use DAW to send automation to VintageCapture
- Automate monitoring on/off
- Automate playback start/stop

---

## Keyboard Shortcuts (Future)

```
Space       - Start/Stop current stage
R           - Start Recording
P           - Start Playback
M           - Toggle Monitoring
Esc         - Stop and Reset
```

---

## Next Steps

After mastering the workflow:
1. Build a library of calibrated synth presets
2. Create templates in your DAW
3. Experiment with arpeggiator patterns
4. Combine with other effects processing

---

**Version:** 0.1.0
**Last Updated:** 2025-10-22
**Status:** Initial Release
