# Arp Firmware - Vintage Mode Specification

**Requirements for Arp hardware to work with VintageCapture VST**

---

## Overview

The Arp hardware needs a "Vintage Mode" that receives commands from the VintageCapture VST via USB MIDI and plays back MIDI note sequences to vintage synths.

---

## USB MIDI Control Protocol

### MIDI CC Commands (from VST → Arp)

| CC Number | Function | Values | Description |
|-----------|----------|--------|-------------|
| **CC 20** | Pattern | 0-3 | 0=Up, 1=Down, 2=UpDown, 3=Random |
| **CC 21** | Clock Division | 0-2 | 0=1/4 notes, 1=1/8 notes, 2=1/16 notes |
| **CC 22** | Octave Range | 0-3 | 0=1 octave, 1=2 octaves, 2=3 octaves, 3=4 octaves |
| **CC 23** | Latch Mode | 0-1 | 0=Off, 1=On |
| **CC 100** | Start Playback | 127 | Begin playing buffer |
| **CC 101** | Stop Playback | 127 | Stop playback |
| **CC 102** | Enter Vintage Mode | 127 | Disable local UI, accept USB control |
| **CC 103** | Exit Vintage Mode | 127 | Re-enable local UI |
| **CC 104** | Calibrate Latency | 127 | Send test note for latency measurement |

### MIDI Note Buffer Transfer (SysEx)

```
F0 7D [Manufacturer ID]
   01 [Command: Load Buffer]
   [Length MSB] [Length LSB]
   [Event 1: Timestamp(4), Note(1), Velocity(1), NoteOn(1)]
   [Event 2: ...]
   [...]
   F7
```

**Format:**
- Timestamp: 4 bytes (microseconds from start)
- Note: 1 byte (MIDI note 0-127)
- Velocity: 1 byte (0-127)
- NoteOn: 1 byte (1=Note On, 0=Note Off)

**Example Event:**
```
00 00 03 E8  // Timestamp: 1000 microseconds (1ms)
3C           // Note: C3 (60)
50           // Velocity: 80
01           // Note On
```

### Latency Calibration Response (SysEx)

**Arp → VST acknowledgment after CC 104:**

```
F0 7D 02 [Timestamp MSB] [Timestamp] [Timestamp] [Timestamp LSB] F7

Command 02 = Latency Calibration ACK
Timestamp  = 4 bytes (microseconds when Arp received CC 104)
```

**Example Response:**
```
F0 7D 02 00 00 27 10 F7  // Received at 10,000µs (10ms)
```

**Behavior:**
1. Arp receives CC 104
2. Records timestamp (microseconds since boot)
3. Immediately sends NoteOn(60, 127) to MIDI OUT (C4, forte)
4. Waits 100ms
5. Sends NoteOff(60, 0)
6. Sends SysEx ACK with timestamp back to VST via USB

**Purpose:** Allows VST to measure round-trip latency and compensate playback timing.
See `LATENCY_COMPENSATION.md` for complete details.

---

## Vintage Mode Behavior

### When Entering Vintage Mode (CC 102)
1. Disable OLED display updates (show "VINTAGE MODE - USB CTRL")
2. Disable button inputs
3. Disable internal arpeggiator engine
4. Enable USB MIDI listener
5. Clear any existing note buffer

### In Vintage Mode
1. **USB MIDI In** → Parse CC commands, update internal state
2. **Receive Buffer** → Store in RAM (up to 1000 events = ~7KB)
3. **On CC 100 (Start):**
   - Begin playback at index 0
   - Send MIDI notes to DIN OUT at correct timestamps
   - Use current pattern/division settings from USB CC
4. **On CC 101 (Stop):**
   - Stop playback
   - Send All Notes Off to DIN OUT

### When Exiting Vintage Mode (CC 103)
1. Re-enable OLED display
2. Re-enable button inputs
3. Re-enable internal arpeggiator
4. Clear buffer
5. Resume normal operation

---

## Implementation (CircuitPython)

### File Structure
```
arp/
└── modes/
    └── vintage_mode.py    # NEW - Vintage Mode implementation
```

### Core Class

```python
# arp/modes/vintage_mode.py

import time
import usb_midi
import adafruit_midi

class VintageMode:
    """
    USB MIDI controlled mode for VintageCapture VST integration.
    Receives commands and MIDI buffer from VST, plays back to hardware synth.
    """

    def __init__(self, midi_out):
        self.active = False
        self.midi_out = midi_out
        self.midi_buffer = []
        self.playback_active = False
        self.playback_index = 0
        self.playback_start_time = 0

        # Arp settings (controlled via USB MIDI CC)
        self.pattern = 0        # 0=Up, 1=Down, 2=UpDown, 3=Random
        self.division = 1       # 0=1/4, 1=1/8, 2=1/16
        self.octave_range = 1   # 0=1 oct, 1=2 oct, etc.
        self.latch = False

    def enter(self):
        """Enter Vintage Mode - disable local UI"""
        self.active = True
        self.midi_buffer = []
        self.playback_active = False
        print("Entered Vintage Mode - awaiting USB MIDI")

    def exit(self):
        """Exit Vintage Mode - restore local UI"""
        self.active = False
        self.midi_buffer = []
        self.playback_active = False
        print("Exited Vintage Mode")

    def handle_cc(self, cc_num, cc_val):
        """Handle MIDI CC from USB"""
        if not self.active:
            return

        if cc_num == 20:  # Pattern
            self.pattern = min(cc_val, 3)
        elif cc_num == 21:  # Division
            self.division = min(cc_val, 2)
        elif cc_num == 22:  # Octave Range
            self.octave_range = min(cc_val, 3)
        elif cc_num == 23:  # Latch
            self.latch = (cc_val > 0)
        elif cc_num == 100:  # Start Playback
            self.start_playback()
        elif cc_num == 101:  # Stop Playback
            self.stop_playback()
        elif cc_num == 102:  # Enter Vintage Mode
            self.enter()
        elif cc_num == 103:  # Exit Vintage Mode
            self.exit()

    def handle_sysex(self, sysex_data):
        """Handle SysEx buffer load"""
        if not self.active:
            return

        # Parse SysEx and load buffer
        # Format: F0 7D 01 [length_msb] [length_lsb] [events...] F7
        if len(sysex_data) < 5:
            return

        if sysex_data[0:2] != bytes([0xF0, 0x7D]):
            return  # Wrong manufacturer

        if sysex_data[2] != 0x01:
            return  # Wrong command (not Load Buffer)

        # TODO: Parse events and store in self.midi_buffer
        print(f"Loaded {len(self.midi_buffer)} events into buffer")

    def start_playback(self):
        """Begin playback of buffer"""
        if not self.midi_buffer:
            print("Error: No buffer loaded")
            return

        self.playback_active = True
        self.playback_index = 0
        self.playback_start_time = time.monotonic_ns() // 1000  # microseconds
        print("Started playback")

    def stop_playback(self):
        """Stop playback"""
        self.playback_active = False
        # Send All Notes Off
        for note in range(128):
            self.midi_out.send(NoteOff(note, 0))
        print("Stopped playback")

    def tick(self):
        """Call this in main loop to process playback"""
        if not self.playback_active:
            return

        current_time = time.monotonic_ns() // 1000  # microseconds
        elapsed = current_time - self.playback_start_time

        # Send any events that are due
        while self.playback_index < len(self.midi_buffer):
            event = self.midi_buffer[self.playback_index]

            if event['timestamp'] <= elapsed:
                # Send this event
                if event['note_on']:
                    self.midi_out.send(NoteOn(event['note'], event['velocity']))
                else:
                    self.midi_out.send(NoteOff(event['note'], 0))

                self.playback_index += 1
            else:
                break  # Not yet time for this event

        # Check if playback finished
        if self.playback_index >= len(self.midi_buffer):
            self.stop_playback()
```

### Integration into main.py

```python
# main.py

from arp.modes.vintage_mode import VintageMode

# Initialize
vintage_mode = VintageMode(midi_out)

# Main loop
while True:
    # Check USB MIDI
    msg = usb_midi.ports[0].read()
    if msg:
        if msg.type == CONTROL_CHANGE:
            vintage_mode.handle_cc(msg.control, msg.value)
        elif msg.type == SYSTEM_EXCLUSIVE:
            vintage_mode.handle_sysex(msg.data)

    # Tick playback
    vintage_mode.tick()

    # ... rest of main loop
```

---

## Testing Plan

### Test 1: Enter/Exit Vintage Mode
1. Send CC 102 (Enter Vintage Mode)
2. Verify OLED shows "VINTAGE MODE"
3. Verify buttons disabled
4. Send CC 103 (Exit Vintage Mode)
5. Verify UI restored

### Test 2: CC Control
1. Enter Vintage Mode
2. Send CC 20 (Pattern = 2)
3. Verify pattern updated internally
4. Send CC 21 (Division = 1)
5. Verify division updated

### Test 3: Buffer Playback
1. Enter Vintage Mode
2. Send SysEx with 3-note sequence: C3, E3, G3
3. Send CC 100 (Start Playback)
4. Verify MIDI OUT sends C3, E3, G3 at correct times
5. Send CC 101 (Stop Playback)
6. Verify All Notes Off sent

### Test 4: Integration with VST
1. Load VintageCapture in DAW
2. Connect Arp via USB
3. Calibrate C3
4. Record 4-note performance
5. Click Playback
6. Verify Arp plays back notes to synth

---

## Memory Considerations

### RAM Usage
```
Each event: 7 bytes (timestamp=4, note=1, velocity=1, note_on=1)
Max events: 1000
Total: ~7KB (well within M4's 192KB RAM)
```

### Optimization
- Use CircuitPython arrays for efficiency
- Limit buffer to 1000 events (about 30 seconds at 1/16 notes)
- Clear buffer when entering Vintage Mode

---

## Next Steps

1. Implement `arp/modes/vintage_mode.py`
2. Add USB MIDI listener to `main.py`
3. Test with simple buffer
4. Integrate with VintageCapture VST
5. Test full workflow with real vintage synth

---

**Status:** Specification Complete - Ready for Implementation
**Target:** Tomorrow after fixing Arp MIDI thru
