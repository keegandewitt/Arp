# Latency Compensation

**Automatic latency detection and compensation for VintageCapture workflow**

---

## Overview

When routing MIDI through a computer (DAW → USB → Arp → Synth), latency is introduced at multiple points. VintageCapture includes automatic latency calibration to ensure playback timing matches the original performance.

---

## The Latency Problem

### Sources of Latency

```
DAW Playback
    ↓ [Audio Engine: 0-20ms depending on buffer size]
USB MIDI Out
    ↓ [USB Driver: 1-5ms, can have jitter]
Arp Hardware
    ↓ [Processing: <1ms]
UART MIDI Out
    ↓ [Transmission: 0.3ms per message]
Vintage Synth
    ↓ [Attack Time: 10-200ms depending on patch]
Audio Output
```

**Total System Latency:** Typically 15-50ms

### Why It Matters

During **Stage 3 (Playback)**:
- Your captured performance has precise timing
- System latency shifts all notes forward in time
- Without compensation, playback won't match the DAW timeline
- Especially critical for:
  - Sync with other tracks
  - Punch-ins and edits
  - Multiple takes that need to align

---

## The Solution: Automatic Calibration

### One-Button Calibration

**User clicks [Fix Latency] button:**

1. **VST sends calibration ping** via USB MIDI
2. **Arp immediately echoes** a test note to synth
3. **DAW records** the resulting audio
4. **VST analyzes** audio onset time
5. **Calculates offset** and applies to future playback

**Result:** Playback is automatically shifted earlier to compensate for system latency.

---

## How It Works (Technical)

### Calibration Sequence

```
T=0ms:    VST sends CC 104 (Calibrate) + timestamp
T=2ms:    Arp receives via USB
T=2.5ms:  Arp sends C4 NoteOn to MIDI OUT
T=2.8ms:  Synth receives note
T=15ms:   Synth audio begins (attack time)
T=17ms:   Audio reaches DAW input
T=17ms:   VST detects audio onset

Calculated Latency = 17ms - 0ms = 17ms
Compensation Offset = -17ms (shift playback earlier)
```

### MIDI Protocol

**Calibration Request (VST → Arp):**
```
CC 104, Value 127  // Start latency calibration
```

**Arp Response:**
```
1. Immediately send NoteOn(C4, 127) to MIDI OUT
2. Wait 100ms
3. Send NoteOff(C4, 0)
4. Send SysEx acknowledgment back to VST
```

**SysEx Acknowledgment (Arp → VST):**
```
F0 7D 02 [timestamp MSB] [timestamp] [timestamp] [timestamp LSB] F7

Command 02 = Calibration ACK
Timestamp = When Arp received the calibration request (microseconds)
```

### Audio Onset Detection

**VST analyzes incoming audio to detect note start:**

```cpp
// Simplified algorithm
float detectAudioOnset(AudioBuffer& buffer) {
    float threshold = 0.1;  // -20dB
    float rmsWindowSize = 512;  // samples

    for (int i = 0; i < buffer.getNumSamples(); i++) {
        float rms = calculateRMS(buffer, i, rmsWindowSize);

        if (rms > threshold) {
            // Found onset - convert sample position to milliseconds
            return (i / sampleRate) * 1000.0;
        }
    }

    return -1;  // No onset found
}
```

---

## Usage Guide

### Quick Start

1. **Load VintageCapture** in your DAW
2. **Connect Arp** via USB
3. **Arm audio track** to record from synth
4. **Set synth to middle C patch** (for consistent results)
5. **Click [Fix Latency]**
6. **Wait 1 second** while calibration runs
7. **Done!** Latency is now compensated

### When to Calibrate

**Recalibrate when:**
- ✅ First time using VintageCapture
- ✅ DAW buffer size changes
- ✅ USB interface changes (different hub, port, etc.)
- ✅ Computer performance changes (other apps running)
- ✅ Synth patch changes dramatically (different attack time)

**Don't need to recalibrate:**
- ❌ Between sessions (stored in project)
- ❌ Between different performances on same synth
- ❌ When just tweaking filter/envelope during playback

### Advanced Options

**Manual Offset:**
```
If automatic calibration fails or you want fine-tuning:

1. Disable auto-calibration
2. Enter manual offset in milliseconds
3. Positive = delay playback (unusual)
4. Negative = advance playback (typical: -10 to -30ms)
```

**Multi-point Calibration:**
```
For maximum accuracy:

1. Calibrate with slow attack patch
2. Calibrate with fast attack patch
3. VST averages the results
4. More consistent across different sounds
```

---

## UI Design

### Latency Panel

```
┌─────────────────────────────────────────┐
│  ⏱ Latency Compensation                 │
├─────────────────────────────────────────┤
│                                         │
│  System Latency: 16.4ms                 │
│                                         │
│  Breakdown:                             │
│    USB MIDI:         3.2ms              │
│    Arp Processing:   0.8ms              │
│    UART TX:          0.3ms              │
│    Synth Attack:    12.1ms              │
│                                         │
│  [Calibrate Latency]                    │
│                                         │
│  ☑ Auto-compensate playback             │
│                                         │
│  Manual Offset: [______] ms             │
│                                         │
│  Last Calibrated: 2 minutes ago         │
│                                         │
└─────────────────────────────────────────┘
```

### Status Messages

**During calibration:**
```
⏱ Calibrating latency...
  1/3 Sending test ping
  2/3 Listening for audio
  3/3 Calculating offset
✓ Calibration complete! (16.4ms)
```

**Errors:**
```
⚠ Calibration failed: No audio detected
  → Check synth is connected and powered on
  → Check audio input is armed in DAW
  → Try manual calibration

⚠ Calibration unstable: High variance
  → System may have jitter issues
  → Try closing background apps
  → Consider using lower buffer size
```

---

## Implementation Details

### VintageCapture VST (C++/JUCE)

```cpp
class LatencyCalibrator {
public:
    void startCalibration() {
        // 1. Send calibration request to Arp
        midiOut.sendControlChange(1, 104, 127);
        calibrationStartTime = Time::getMillisecondCounter();

        // 2. Start listening for audio
        listeningForOnset = true;
        audioOnsetTime = -1;
    }

    void processAudioBlock(AudioBuffer<float>& buffer) {
        if (!listeningForOnset) return;

        // Detect audio onset
        for (int i = 0; i < buffer.getNumSamples(); i++) {
            float sample = buffer.getSample(0, i);

            if (abs(sample) > 0.1 && audioOnsetTime < 0) {
                // Found onset!
                audioOnsetTime = Time::getMillisecondCounter();
                latencyMs = audioOnsetTime - calibrationStartTime;

                // Apply compensation
                compensationOffset = -latencyMs;
                listeningForOnset = false;

                DBG("Latency calibrated: " + String(latencyMs) + "ms");
                break;
            }
        }
    }

    void applyCompensation(MidiBuffer& buffer, int numSamples) {
        if (!autoCompensate) return;

        // Shift all MIDI events by compensation offset
        MidiBuffer shifted;
        for (auto metadata : buffer) {
            int newPosition = metadata.samplePosition +
                             (compensationOffset * sampleRate / 1000);
            shifted.addEvent(metadata.getMessage(), newPosition);
        }
        buffer = shifted;
    }

private:
    bool listeningForOnset = false;
    int64 calibrationStartTime = 0;
    int64 audioOnsetTime = -1;
    float latencyMs = 0;
    float compensationOffset = 0;
    bool autoCompensate = true;
};
```

### Arp Firmware (CircuitPython)

```python
# arp/modes/vintage_mode.py

def handle_calibration_request(self):
    """
    Handle CC 104 latency calibration request
    Immediately send test note to MIDI OUT
    """
    import time

    # Record timestamp when we received the request
    receive_time = time.monotonic_ns() // 1000  # microseconds

    # Send test note immediately (C4 = middle C)
    self.midi_out.send(NoteOn(60, 127))

    # Hold for 100ms
    time.sleep(0.1)

    # Send note off
    self.midi_out.send(NoteOff(60, 0))

    # Send acknowledgment back to VST
    self.send_calibration_ack(receive_time)

    print(f"Latency calibration: Sent test note at {receive_time}µs")

def send_calibration_ack(self, timestamp):
    """
    Send SysEx acknowledgment with timestamp
    Format: F0 7D 02 [timestamp(4 bytes)] F7
    """
    sysex_data = bytearray([
        0xF0,  # SysEx start
        0x7D,  # Manufacturer ID
        0x02,  # Command: Calibration ACK
        (timestamp >> 24) & 0xFF,  # Timestamp MSB
        (timestamp >> 16) & 0xFF,
        (timestamp >> 8) & 0xFF,
        timestamp & 0xFF,           # Timestamp LSB
        0xF7   # SysEx end
    ])

    self.usb_midi.send(SystemExclusive(sysex_data))
```

---

## Accuracy & Limitations

### Expected Accuracy

- **Typical variance:** ±2ms
- **Best case:** ±0.5ms (low buffer, fast system)
- **Worst case:** ±5ms (high buffer, busy system)

### Factors Affecting Accuracy

**✅ Good:**
- Low DAW buffer size (64-128 samples)
- Fast computer with low CPU usage
- Direct USB connection (no hubs)
- Consistent synth attack time

**❌ Bad:**
- High DAW buffer size (512+ samples)
- USB hub chain (adds jitter)
- Background apps consuming CPU
- Synth with slow/variable attack

### Limitations

**Cannot compensate for:**
- ❌ **Jitter** - random variation in latency (only average)
- ❌ **Synth attack time variation** - if envelope changes between calibration and playback
- ❌ **Audio interface latency changes** - if recording different tracks at different buffer sizes

**Best practice:** Calibrate at the buffer size you'll use for recording.

---

## Troubleshooting

### "No audio detected"

**Cause:** VST isn't receiving audio from synth

**Solutions:**
1. Check synth is powered on and making sound
2. Check audio cable is connected
3. Check DAW input is armed and receiving signal
4. Try manual test: play a note and verify you see levels

### "High variance detected"

**Cause:** System latency is inconsistent (jitter)

**Solutions:**
1. Close background applications
2. Reduce DAW buffer size
3. Use different USB port (avoid hubs)
4. Check CPU usage in Activity Monitor/Task Manager

### "Calibration result seems wrong"

**Cause:** Detection algorithm may have false trigger

**Solutions:**
1. Ensure room is quiet (no background noise)
2. Increase detection threshold in settings
3. Use manual offset as fallback
4. Recalibrate multiple times and average

---

## Future Enhancements

### Planned Features

- [ ] **Multi-note calibration** - Send chord, average results
- [ ] **Continuous monitoring** - Detect if latency changes mid-session
- [ ] **Per-synth profiles** - Store calibration for different synths
- [ ] **Jitter analysis** - Report stability metrics
- [ ] **Auto-recalibrate** - Prompt when buffer size changes

### Research Ideas

- [ ] **Predictive compensation** - Use machine learning to predict latency
- [ ] **Phase-coherent alignment** - Align to waveform phase
- [ ] **MIDI clock sync** - Alternative timing reference

---

## Technical References

### Sample Rates & Latency

| Buffer Size | @ 44.1kHz | @ 48kHz | @ 96kHz |
|-------------|-----------|---------|---------|
| 64 samples  | 1.5ms     | 1.3ms   | 0.7ms   |
| 128 samples | 2.9ms     | 2.7ms   | 1.3ms   |
| 256 samples | 5.8ms     | 5.3ms   | 2.7ms   |
| 512 samples | 11.6ms    | 10.7ms  | 5.3ms   |

### USB MIDI Timing

- **USB Full Speed:** 1ms polling interval
- **Class Compliant:** No driver overhead
- **Typical jitter:** ±1-3ms on macOS/Windows

### UART MIDI Timing

- **Baud rate:** 31250 bps
- **3-byte message:** 0.96ms
- **Jitter:** <0.01ms (deterministic)

---

## Version History

**v1.0 (2025-10-23)**
- Initial specification
- Basic calibration protocol
- Audio onset detection
- Manual offset option

---

**Status:** Specification Complete - Ready for Implementation
**Next Steps:** Implement in VintageCapture VST and Arp firmware
