# VintageCapture VST Plugin

**A revolutionary workflow for capturing vintage synthesizer performances**

## The Problem
Vintage synths (Moog Source, ARP Odyssey, Korg MS-20, etc.) lack MIDI Local Control Off, making them incompatible with external arpeggiators.

## The Solution
Two-stage capture workflow that separates performance from sound design:

### Stage 1: Keystroke Capture
- Capture MIDI notes, velocity, timing from performance
- Provide zero-latency sample-based monitoring
- Record performance data to buffer

### Stage 2: Parameter Playback
- Play back MIDI buffer via Arp hardware to vintage synth
- Timeline-locked, repeatable playback
- User tweaks synth parameters while DAW records audio
- Multiple takes, punch-ins possible

## Key Innovation: "Press C3" Calibration
Instead of complex parameter detection, we analyze ONE note to learn:
- Attack time (note startup duration)
- Release time (tail after key release)
- Reference sample for monitoring

This tells us sonic duration = MIDI duration + release tail.

## Tech Stack
- **Framework:** JUCE
- **Plugin Formats:** VST3, AU, AAX
- **Language:** C++17
- **Hardware:** Arp MIDI Arpeggiator (USB MIDI control)

## Project Structure
```
VintageCapture/
├── Source/
│   ├── PluginProcessor.h/cpp      # Audio processing & state
│   ├── PluginEditor.h/cpp         # UI
│   ├── DurationAnalyzer.h/cpp     # C3 analysis (attack/release)
│   ├── KeystrokeCapture.h/cpp     # MIDI recording
│   ├── PlaybackEngine.h/cpp       # Timeline-locked playback
│   ├── MonitoringEngine.h/cpp     # Sample playback with pitch shift
│   └── ArpInterface.h/cpp         # USB MIDI to Arp hardware
├── Resources/
│   └── UI assets
└── Builds/
    ├── MacOSX/
    └── VisualStudio2022/
```

## Development Roadmap

### Phase 1: Core Analysis (NOW)
- [x] RMS envelope analyzer
- [ ] Attack/release time detection
- [ ] C3 calibration workflow
- [ ] Sample storage

### Phase 2: Monitoring
- [ ] Sample pitch shifting
- [ ] Zero-latency playback
- [ ] MIDI note triggering

### Phase 3: Playback
- [ ] Timeline synchronization
- [ ] Arp hardware interface
- [ ] Playback engine

### Phase 4: Polish
- [ ] UI design
- [ ] Preset management
- [ ] Documentation

## Building

### Prerequisites
- JUCE Framework 7.x
- Xcode (macOS) or Visual Studio 2022 (Windows)
- CMake 3.22+

### Build Instructions
```bash
cd VintageCapture
cmake -B Builds -G Xcode  # macOS
# or
cmake -B Builds -G "Visual Studio 17 2022"  # Windows

cmake --build Builds --config Release
```

## Usage

### Quick Start
1. Load VintageCapture in your DAW
2. Connect vintage synth audio output to DAW input
3. Connect Arp hardware via USB
4. Click "Calibrate" → Press C3 for 2 seconds
5. Click "Record" → Perform on vintage synth keyboard
6. Click "Playback" → Tweak synth parameters while DAW records

### Detailed Workflow
See [WORKFLOW.md](WORKFLOW.md) for complete walkthrough.

## License
TBD

## Credits
- Concept & Design: Keegan DeWitt
- Implementation: Claude Code + Keegan DeWitt
- Inspired by the limitations and beauty of vintage synthesizers

---

**Status:** In Development
**Version:** 0.1.0-alpha
**Last Updated:** 2025-10-22
