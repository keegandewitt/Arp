# Arp - Hardware Arpeggiator

A powerful hardware arpeggiator built on CircuitPython that bridges the MIDI and modular synthesis worlds.

```
┌─────────────────────────────┐
│  OLED FeatherWing           │  ← UI + Buttons
├─────────────────────────────┤
│  MIDI FeatherWing           │  ← DIN MIDI IN/OUT
├─────────────────────────────┤
│  Feather M4 CAN Express     │  ← Brain (120MHz ARM)
└─────────────────────────────┘
         ↓ USB-C
    [Computer/DAW]
```

---

## What It Does

**Input:** MIDI notes from keyboards, sequencers, or DAW
**Processing:** Real-time arpeggiation with multiple patterns
**Output:** MIDI, CV/Gate, S-Trigger (phase-dependent)

### Phase 1: MIDI Core (NOW)
- ✅ MIDI IN/OUT via DIN-5 jacks
- ✅ USB MIDI clock sync from DAW
- ⏳ Arpeggiator patterns (Up/Down/Random/Up-Down)
- ⏳ Clock divisions (1/4, 1/8, 1/16 notes)
- ⏳ 1-4 octave range
- ⏳ OLED UI with button control

### Phase 2: CV/Gate Output (FUTURE)
- 📋 CV Pitch (1V/octave) for modular synths
- 📋 Gate/Trigger out
- 📋 Output mode switching (MIDI vs. CV)

### Phase 3: S-Trigger (FUTURE)
- 📋 S-Trigger support for vintage gear (ARP, Korg MS, Yamaha CS)

---

## Project Status

**Current Phase:** Hardware Validated ✅ | Software In Development ⏳

See [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) for detailed progress.

---

## 🎹 NEW: VintageCapture VST Plugin

**Bonus Project:** We've also built a complete VST plugin that solves the vintage synth "Local Control Off" problem!

### The Problem
Vintage synths (Moog Source, ARP Odyssey, Korg MS-20) don't have MIDI Local Control Off, making them incompatible with external arpeggiators.

### The Solution
**VintageCapture** is a VST plugin with a two-stage workflow:
1. **Calibration:** "Press C3" - learns synth timing (attack/release)
2. **Keystroke Capture:** Record your performance (notes, velocity, timing)
3. **Playback:** Arp hardware plays back via MIDI while you tweak synth parameters

**Benefits:**
- ✅ Separate performance from sound design
- ✅ Zero-latency monitoring during capture
- ✅ Repeatable playback for multiple takes
- ✅ Works with ANY vintage synth

See [VintageCapture/README.md](VintageCapture/README.md) for full details.

---

## Documentation

### Overview
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Complete system design
- **[PROJECT_STATUS.md](docs/PROJECT_STATUS.md)** - Current progress and next steps
- **[METHODOLOGY.md](docs/METHODOLOGY.md)** - Development approach

### Hardware
- **[ASSEMBLY_PROTOCOL.md](docs/hardware/ASSEMBLY_PROTOCOL.md)** - Step-by-step build guide
- **[MIDI_PREFLIGHT_CHECKLIST.md](docs/hardware/MIDI_PREFLIGHT_CHECKLIST.md)** - Pre-flight validation
- **[MIDI_BREADBOARD_WIRING.md](docs/hardware/MIDI_BREADBOARD_WIRING.md)** - Breadboard testing guide

### Software
- **[UI_ARCHITECTURE.md](docs/UI_ARCHITECTURE.md)** - Button interaction standards

---

## Hardware

### Bill of Materials
- [Adafruit Feather M4 CAN Express](https://www.adafruit.com/product/4759) - Main board
- [Adafruit MIDI FeatherWing](https://www.adafruit.com/product/4740) - MIDI IN/OUT
- [Adafruit OLED FeatherWing 128x64](https://www.adafruit.com/product/4650) - Display + 3 buttons
- USB-C cable
- MIDI cables (DIN-5)

**Future (Phase 2):**
- 3x 3.5mm mono jacks (CV, Gate, Velocity)
- Op-amp circuit (for 1V/octave scaling)

### Pin Usage

**Currently Used:**
```
D0, D1     → MIDI FeatherWing (UART)
D5, D6, D9 → OLED Buttons
D21, D22   → OLED Display (I2C)
```

**Reserved for Future:**
```
A0  → CV Pitch Out (DAC)
A1  → CV Velocity Out (DAC)
A2  → Gate/Trigger Out
A3  → S-Trigger Out
```

See [ARCHITECTURE.md - Pin Allocation](docs/ARCHITECTURE.md#pin-allocation) for complete details.

---

## Software Architecture

### Modular Design
```
[MIDI Input] → [Arpeggiator Engine] → [Output Router]
                                           ↓
                                  ┌────────┼────────┐
                                  ↓        ↓        ↓
                               MIDI    CV/Gate  S-Trig
                              Driver   Driver   Driver
```

### Directory Structure
```
arp/
├── core/                # Arpeggiator engine (TODO)
├── drivers/             # Output drivers (TODO)
├── ui/                  # Display & buttons (WIP)
├── utils/               # Helpers (TODO)
└── main.py              # Entry point (TODO)
```

### Dependencies
- CircuitPython 10.0.3
- `adafruit_displayio_sh1107` - OLED driver
- `adafruit_midi` - MIDI protocol
- `i2cdisplaybus` - I2C management

---

## Development

### Setup
1. Install CircuitPython 10.0.3 on Feather M4
2. Install libraries:
   ```bash
   circup install adafruit_displayio_sh1107 adafruit_midi
   ```
3. Clone repository:
   ```bash
   git clone https://github.com/keegandewitt/Arp.git
   ```

### Testing
Use the comprehensive test suite:
```bash
# MIDI tests
python3 scripts/monitor_serial.py --reload &
cp tests/midi_loopback_test.py /Volumes/CIRCUITPY/code.py

# Integration test
cp tests/integration_test_debug.py /Volumes/CIRCUITPY/code.py
```

See [tests/](tests/) directory for all test scripts.

### Serial Monitoring
Clean serial port monitoring with automatic cleanup:
```bash
python3 scripts/monitor_serial.py --reload --duration 60
```

---

## Features

### Arpeggiator Patterns (Phase 1)
- **Up:** Ascending notes
- **Down:** Descending notes
- **Up/Down:** Ascending then descending
- **Random:** Random note selection

### Clock Division (Phase 1)
- Quarter notes (1/4)
- Eighth notes (1/8)
- Sixteenth notes (1/16)

### Clock Sources (Phase 1)
1. USB MIDI Clock (from DAW) - Priority 1
2. DIN MIDI Clock (from hardware) - Priority 2
3. Internal Clock (free-running) - Fallback

### UI Controls (Phase 1)
**Single Press:**
- Button A: Cycle pattern
- Button B: Cycle clock division
- Button C: Cycle octave range

**Long Press (0.5s):**
- Button A: Settings menu
- Button B: Tap tempo
- Button C: Output mode

---

## Performance

- **MIDI Latency:** <5ms (input to output)
- **Clock Jitter:** <1ms
- **Loop Rate:** 100Hz (10ms)
- **Display Update:** 30Hz (33ms)
- **Stability:** 25+ minutes validated

---

## Repository

- **GitHub:** https://github.com/keegandewitt/Arp
- **License:** MIT (TBD)
- **Issues:** [Report bugs](https://github.com/keegandewitt/Arp/issues)

---

## Resources

### Datasheets
- [Feather M4 CAN](https://learn.adafruit.com/adafruit-feather-m4-can-express)
- [MIDI FeatherWing](https://learn.adafruit.com/adafruit-midi-featherwing)
- [OLED FeatherWing](https://learn.adafruit.com/adafruit-128x64-oled-featherwing)

### CircuitPython
- [CircuitPython Docs](https://docs.circuitpython.org/)
- [CircuitPython MIDI Guide](https://learn.adafruit.com/circuitpython-midi-projects)

### Standards
- [MIDI 1.0 Specification](https://www.midi.org/specifications)
- [CV/Gate Standards](https://en.wikipedia.org/wiki/CV/gate)

---

## Development Philosophy

> **"Measure twice, cut once"**

This project emphasizes:
1. ✅ **Thorough planning** before implementation
2. ✅ **Hardware validation** before software development
3. ✅ **Comprehensive testing** at each stage
4. ✅ **Clear documentation** for maintainability
5. ✅ **Modular architecture** for future expansion

See [METHODOLOGY.md](docs/METHODOLOGY.md) for our development approach.

---

## Roadmap

### Immediate (This Week)
- ⏳ Build arpeggiator engine core
- ⏳ Implement pattern library (Up/Down/Random)
- ⏳ Create basic main.py with simple arpeggio

### Short Term (Next 2 Weeks)
- ⏳ Clock synchronization (USB/DIN/Internal)
- ⏳ UI menu system
- ⏳ Pattern/tempo controls
- ⏳ Settings persistence

### Long Term (Months)
- 📋 CV/Gate output driver
- 📋 S-Trigger support
- 📋 Calibration routine
- 📋 Advanced features (swing, velocity curves)

---

## Contributing

This is currently a personal project, but contributions and suggestions are welcome!

1. Check [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) for current work
2. Review [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
3. Open an issue to discuss your ideas

---

## Acknowledgments

- **Adafruit** - Amazing hardware and CircuitPython
- **CircuitPython Community** - Excellent documentation and libraries

---

**Version:** 2.0
**Status:** Hardware validated, software in development
**Last Updated:** 2025-10-22
