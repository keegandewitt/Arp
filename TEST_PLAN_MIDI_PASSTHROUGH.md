# MIDI Pass-Through Test Plan

**Date:** 2025-10-22
**Test Subject:** MIDI Pass-Through Implementation
**Hardware:** Feather M4 CAN + MIDI FeatherWing + OLED FeatherWing
**CircuitPython Version:** 10.0.3
**adafruit_midi Version:** 1.5.6

---

## Test Objectives

Verify that ALL non-note MIDI messages pass through the arpeggiator transparently, enabling full expressive control over arpeggiated notes.

---

## Pre-Test Checklist

- [x] M4 connected and recognized
- [x] CircuitPython 10.0.3 running
- [x] adafruit_midi 1.5.6 installed
- [x] Backup created (Arp_20251022_165526.tar.gz)
- [x] main.py deployed to M4
- [ ] Serial console connected
- [ ] MIDI keyboard connected to MIDI IN
- [ ] MIDI OUT connected to hardware synth
- [ ] Synth set to "Local Control OFF" (if available)

---

## Test Categories

### 1. Boot Sequence Test
**Objective:** Verify clean startup with no import errors

**Expected Output:**
```
============================================================
ARP - Hardware Arpeggiator v1.0
============================================================
[1/3] Initializing MIDI...
      ✓ MIDI ready (31250 baud)
[2/3] Initializing Display...
      ✓ Display ready (SH1107 128x64)
[3/3] Initializing Buttons...
      ✓ Buttons ready (A, B, C)

============================================================
SYSTEM READY
============================================================
Button A: Previous pattern
Button B: Play C major chord arpeggio (demo)
Button C: Next pattern
MIDI IN → Arpeggiator → MIDI OUT
Now listening for MIDI...
```

**Pass Criteria:**
- No `ImportError` or `ModuleNotFoundError`
- All three initialization steps complete with ✓
- "SYSTEM READY" displayed
- No exceptions or crashes

---

### 2. Note On/Off Arpeggiator Test
**Objective:** Verify basic arpeggiator functionality

**Test Steps:**
1. Play single note (e.g., C4/60) and hold
2. Observe arpeggiated output
3. Play chord (e.g., C major: C4, E4, G4)
4. Observe arpeggiated chord
5. Release notes one by one
6. Verify clean note-off handling

**Expected Serial Output:**
```
Note ON: 60 (velocity 100) - Buffer: [60]
Note ON: 64 (velocity 100) - Buffer: [60, 64]
Note ON: 67 (velocity 100) - Buffer: [60, 64, 67]
Note OFF: 60 - Buffer: [64, 67]
Note OFF: 64 - Buffer: [67]
Note OFF: 67 - Buffer: []
```

**Pass Criteria:**
- Notes added to buffer correctly
- Arpeggio plays at correct tempo (120 BPM default)
- No index errors when releasing notes
- Arpeggio stops when all notes released

---

### 3. Pitch Bend Pass-Through Test
**Objective:** Verify pitch bend messages pass through to synth

**Test Steps:**
1. Play and hold a chord
2. Move pitch bend wheel up
3. Move pitch bend wheel down
4. Return to center
5. Listen for pitch bend on arpeggiated notes

**Expected Serial Output:**
```
Note ON: 60 (velocity 100) - Buffer: [60, 64, 67]
Pass-through: PitchBend 8192  # Center
Pass-through: PitchBend 12288 # Up
Pass-through: PitchBend 4096  # Down
Pass-through: PitchBend 8192  # Center
```

**Pass Criteria:**
- Pitch bend values logged correctly
- Arpeggiated notes bend in real-time
- No "Failed to send" errors
- Smooth pitch bend response

---

### 4. Control Change (CC) Pass-Through Test
**Objective:** Verify CC messages (mod wheel, sustain, etc.) pass through

**Test Steps:**
1. Play and hold a chord
2. Move mod wheel (CC#1) from 0 to 127
3. Press sustain pedal (CC#64) on/off
4. Test other CC controls if available (expression, volume, etc.)

**Expected Serial Output:**
```
Note ON: 60 (velocity 100) - Buffer: [60, 64, 67]
Pass-through: CC#1 = 0    # Mod wheel at minimum
Pass-through: CC#1 = 64   # Mod wheel at 50%
Pass-through: CC#1 = 127  # Mod wheel at maximum
Pass-through: CC#64 = 127 # Sustain ON
Pass-through: CC#64 = 0   # Sustain OFF
```

**Pass Criteria:**
- CC values logged with correct controller numbers
- Arpeggiated notes respond to CC changes
- No "Failed to send" errors
- CC changes audible on synth output

---

### 5. Program Change Pass-Through Test
**Objective:** Verify program change messages update synth patch

**Test Steps:**
1. Send program change 0 (patch 1)
2. Play chord and listen
3. Send program change 5 (patch 6)
4. Play chord and listen for different sound

**Expected Serial Output:**
```
Pass-through: Program Change 0
Note ON: 60 (velocity 100) - Buffer: [60, 64, 67]
Pass-through: Program Change 5
Note ON: 60 (velocity 100) - Buffer: [60, 64, 67]
```

**Pass Criteria:**
- Program changes logged correctly
- Synth patch changes audible
- No "Failed to send" errors

---

### 6. Channel Pressure (Aftertouch) Pass-Through Test
**Objective:** Verify aftertouch passes through

**Test Steps:**
1. Play and hold a chord
2. Apply channel pressure (if keyboard supports)
3. Listen for modulation on arpeggiated notes

**Expected Serial Output:**
```
Note ON: 60 (velocity 100) - Buffer: [60, 64, 67]
Pass-through: ChannelPressure
```

**Pass Criteria:**
- Aftertouch logged
- Aftertouch affects arpeggiated notes
- No "Failed to send" errors

---

### 7. MIDI Real-Time Messages Test
**Objective:** Verify Clock, Start, Stop, Continue pass through

**Test Steps:**
1. If keyboard/sequencer sends MIDI clock, start playback
2. Observe clock messages (should NOT flood console - silent logging)
3. Send MIDI Start (if available)
4. Send MIDI Stop
5. Send MIDI Continue

**Expected Serial Output:**
```
Pass-through: MIDI Start
# (MIDI Clock messages pass silently - not logged)
Pass-through: MIDI Stop
Pass-through: MIDI Continue
```

**Pass Criteria:**
- Transport messages logged (Start, Stop, Continue)
- MIDI Clock passes but is NOT logged (too chatty)
- Active Sensing passes but is NOT logged
- No "Failed real-time pass" errors

---

### 8. System Exclusive (SysEx) Test
**Objective:** Verify SysEx messages pass through (if applicable)

**Test Steps:**
1. Send SysEx message from keyboard (if supported)
2. Observe pass-through

**Expected Serial Output:**
```
Pass-through: SystemExclusive
```

**Pass Criteria:**
- SysEx logged
- No errors
- (Optional: verify on synth if it has SysEx functionality)

---

### 9. Unknown/Bad MIDI Events Test
**Objective:** Verify graceful handling of unknown MIDI messages

**Expected Behavior:**
- Unknown events logged as: `Pass-through (raw): Unknown MIDI 0xXX`
- Bad events logged as: `Pass-through (raw): Bad MIDI event (N bytes)`
- No crashes or exceptions
- Raw bytes passed through via uart.write()

**Pass Criteria:**
- System remains stable
- Unknown messages logged with hex status byte
- No unhandled exceptions

---

### 10. Edge Case Testing

#### 10.1 Rapid Note Changes
- Play notes quickly while changing controls
- Verify no buffer overflow or index errors

#### 10.2 All Notes Off (CC#123)
- Send MIDI CC#123 (all notes off)
- Verify arpeggiator stops cleanly

#### 10.3 Simultaneous Messages
- Play chord + pitch bend + mod wheel simultaneously
- Verify all messages pass through correctly

#### 10.4 Long Sustained Arpeggio with Expression
- Hold chord for 30+ seconds
- Continuously modulate pitch bend and mod wheel
- Verify no memory leaks or degradation

---

## Test Results Log

### Boot Sequence
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### Arpeggiator Functionality
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### Pitch Bend
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### Control Change (CC)
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### Program Change
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### Aftertouch
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### Real-Time Messages
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### SysEx
- **Status:** [ ] Pass / [ ] Fail / [ ] N/A
- **Notes:**

### Unknown/Bad Events
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

### Edge Cases
- **Status:** [ ] Pass / [ ] Fail
- **Notes:**

---

## Success Criteria

**Test suite PASSES if:**
- ✅ All 10 test categories pass
- ✅ No unhandled exceptions or crashes
- ✅ All logged MIDI messages match expected output
- ✅ Arpeggiated notes respond to all expression controls
- ✅ No "MIDIUnknownEvent" errors for standard MIDI messages
- ✅ System remains stable during edge case testing

**Test suite FAILS if:**
- ❌ Any category fails
- ❌ Import errors on boot
- ❌ Crashes or safe mode errors
- ❌ MIDI messages not passing through
- ❌ Performance degradation or memory issues

---

## Post-Test Actions

If ALL tests pass:
1. ✅ Reduce logging verbosity (remove verbose debug prints)
2. ✅ Update PROJECT_STATUS.md with test results
3. ✅ Commit changes with comprehensive message
4. ✅ Update todo list

If ANY test fails:
1. ❌ Document failure in detail
2. ❌ Review code for bugs
3. ❌ Fix issues
4. ❌ Re-test failed category
5. ❌ Repeat until all tests pass

---

## Notes

- Keep this document updated as tests are performed
- Add any unexpected behavior to notes section
- Screenshot or record video of successful tests if needed
- Save serial console output for documentation
