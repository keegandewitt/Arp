# prisme - MIDI/CV Translation Hub

A powerful MIDI/CV translation hub built on CircuitPython that bridges the MIDI and modular synthesis worlds with user-configurable layer processing.

```
┌─────────────────────────────┐
│  OLED FeatherWing           │  ← UI + Buttons (STACKED)
├─────────────────────────────┤
│  Feather M4 CAN Express     │  ← Brain (120MHz ARM)
└─────────────────────────────┘
         ↓ USB-C
    [Computer/DAW]

[BREADBOARD]
  MIDI I/O (DIN-5 jacks) ──jumpers──> D0/D1 on M4
  CV/Gate circuits
  Op-amp circuits

⚠️ IMPORTANT: MIDI FeatherWing is NOT stacked - stays on breadboard
```

---

## What It Does

**Concept:** User-definable MIDI/CV processing pipeline with configurable layer ordering

**Input:** MIDI IN (DIN-5), USB MIDI, CV IN (future), Gate IN (future)
**Processing:** Translation layers (Scale Quantization → Arpeggiation, or vice versa)
**Output:** MIDI OUT (DIN-5), USB MIDI, CV/Gate, Custom CC mapping

### Core Features (Working)
- ✅ **Routing Modes:** THRU (zero-latency pass-through) or TRANSLATION (layer processing)
- ✅ **Translation Layers:** Scale quantization, Arpeggiation (user-definable order)
- ✅ **Arpeggiator:** 16 patterns (Up, Down, Up/Down, Random, As-Played, etc.)
- ✅ **Clock System:** Internal/External sync, clock division (16th, 8th, quarter notes)
- ✅ **Custom CC Mapping:** Learn mode for flexible CC output (Session 14)
- ✅ **Settings Persistence:** NVM storage with auto-save
- ✅ **OLED UI:** Real-time display with 3-button navigation

### Translation Hub Features (Planned - Session 15+)
- ⏳ **Layer Ordering:** Scale → Arp OR Arp → Scale (user choice)
- ⏳ **Clock Transformations:** Swing (Roger Linn method), Multiply (2x, 4x), Divide (1/2, 1/4, 1/8)
- ⏳ **Input Selection:** MIDI IN, USB MIDI, CV IN, Gate IN
- ⏳ **CV/Gate Output:** 1V/octave pitch + gate triggers (MCP4728 DAC)
- ⏳ **USB MIDI Notes:** Full USB MIDI input (currently clock only)

### Future Expansions
- 📋 S-Trigger support for vintage gear (ARP, Korg MS, Yamaha CS)
- 📋 Advanced arpeggiator features (latch mode, velocity passthrough)
- 📋 CV IN: Analog voltage input for pitch control

---

## Project Status

**Current Phase:** Translation Hub Architecture - Research Complete ✅ | Implementation Planned ⏳

**Latest:**
- Session 15: Translation Hub architecture research complete (97% confidence)
- Session 14: Custom CC output system implemented and working
- Session 13: CV/Gate output hardware tested and validated
- Core arpeggiator working with 16 patterns, clock sync, settings persistence

See [docs/context/CONTEXT.md](docs/context/CONTEXT.md) for detailed session history and [docs/implementation/TRANSLATION_HUB_IMPLEMENTATION_PLAN.md](docs/implementation/TRANSLATION_HUB_IMPLEMENTATION_PLAN.md) for next steps.

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
/
├── main.py                      # Main entry point (current inline arpeggiator)
├── arp/
│   ├── core/
│   │   ├── arpeggiator.py       # Class-based arpeggiator (16 patterns, scale quantization)
│   │   ├── clock.py             # Clock handler (internal/external sync)
│   │   ├── config.py            # Settings with NVM persistence
│   │   ├── custom_cc.py         # Custom CC mapping with Learn Mode (Session 14)
│   │   └── cv_gate.py           # CV/Gate output driver (MCP4728)
│   ├── ui/
│   │   ├── display.py           # OLED display manager (SH1107)
│   │   ├── menu.py              # Menu system
│   │   └── buttons.py           # Button handler
│   └── lib/                     # CircuitPython libraries
├── docs/
│   ├── context/                 # Session handoffs and project context
│   ├── implementation/          # Implementation plans and research
│   ├── hardware/                # Hardware documentation, tests, schematics
│   └── ARCHITECTURE.md          # System architecture
└── tests/                       # Hardware validation and unit tests
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
   git clone https://github.com/keegandewitt/Arp.git prisme
   cd prisme
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

### Translation Hub Architecture
- **Routing Modes:** THRU (zero-latency) or TRANSLATION (layer processing)
- **Layer Ordering:** User-configurable (Scale → Arp OR Arp → Scale)
- **Layer Enable/Disable:** Independent control of each translation layer

### Arpeggiator Engine (16 Patterns)
- **Up:** Ascending notes
- **Down:** Descending notes
- **Up/Down:** Ascending then descending (palindrome)
- **Down/Up:** Descending then ascending
- **Random:** Random note selection
- **As-Played:** Remembers input order
- **+ 10 more patterns** in class-based arpeggiator

### Scale Quantization
- **Scales:** Major, Minor, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian
- **Root Note:** Chromatic selection (C through B)
- **Real-time quantization:** Notes snap to scale during performance

### Clock System
- **Sources:** USB MIDI Clock, DIN MIDI Clock, Internal (free-running)
- **Divisions:** 16th notes, 8th notes, Quarter notes
- **Transformations (Planned):** Swing (50-75%), Multiply (2x, 4x), Divide (1/2, 1/4, 1/8)

### Custom CC Mapping (Session 14)
- **Learn Mode:** Button B long press to capture CC assignments
- **Smoothing:** Configurable smoothing for jitter reduction
- **Flexible Routing:** Map any input CC to any output CC

### UI Controls
**Single Press:**
- Button A: Navigate menu / Cycle pattern
- Button B: Navigate menu / Cycle clock division
- Button C: Navigate menu / Select option

**Long Press (0.5s):**
- Button A: Enter/exit menu system
- Button B: **Learn Mode** (Custom CC mapping)
- Button C: Context-specific action

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

### Completed (Sessions 1-14)
- ✅ Arpeggiator engine core (16 patterns)
- ✅ Clock synchronization (USB/DIN/Internal)
- ✅ UI menu system (7 categories)
- ✅ Settings persistence (NVM storage)
- ✅ Custom CC mapping with Learn Mode
- ✅ CV/Gate output driver (MCP4728 DAC)
- ✅ OLED display integration (SH1107)

### Current Focus (Session 15)
- ⏳ Translation Hub architecture research (97% complete)
- ⏳ Implementation plan finalized
- ⏳ Documentation updates to reflect "prisme" rebranding

### Next Session (Session 16+)
- 📋 Migrate to class-based arpeggiator architecture
- 📋 Implement translation layer pipeline
- 📋 Add swing/multiply/divide to clock system
- 📋 Enable USB MIDI for note input (currently clock only)
- 📋 Implement configurable layer ordering (Scale→Arp or Arp→Scale)
- 📋 Add routing mode selection (THRU / TRANSLATION)
- 📋 Comprehensive testing (PyTest + hardware validation)

### Long Term
- 📋 Input source selection (CV IN, Gate IN)
- 📋 S-Trigger support for vintage gear
- 📋 Advanced arpeggiator features (latch, velocity curves)

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

**Project:** prisme - MIDI/CV Translation Hub
**Version:** 3.0 (Translation Hub Architecture)
**Status:** Core features working, Translation Hub implementation planned
**Last Updated:** 2025-11-01 (Session 15)
