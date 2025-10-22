# Arp - Project Status

**Last Updated:** 2025-10-22
**Current Phase:** Phase 1 - MIDI Core Development
**Overall Progress:** Hardware Validated ✅ | Software In Development ⏳

---

## Project Vision

A **hardware arpeggiator** that bridges MIDI and modular synthesis worlds:

- **Phase 1 (NOW):** MIDI IN/OUT with full arpeggiator features
- **Phase 2 (FUTURE):** CV/Gate output for modular synthesizers
- **Phase 3 (FUTURE):** S-Trigger support for vintage gear

**See:** [ARCHITECTURE.md](./ARCHITECTURE.md) for complete system design

---

## Hardware Status

### ✅ Validated and Working

| Component | Status | Notes |
|-----------|--------|-------|
| **Feather M4 CAN Express** | ✅ Working | CircuitPython 10.0.3 |
| **OLED FeatherWing 128x64** | ✅ Working | SH1107 driver, I2C 0x3C |
| **MIDI FeatherWing** | ✅ Working | UART 31250 baud, 100% loopback |
| **Buttons (A, B, C)** | ✅ Working | D9, D6, D5 with debouncing |
| **USB MIDI** | ✅ Working | Native USB MIDI support verified |
| **Power System** | ✅ Working | USB-C → M4 → FeatherWings |

### 🔧 Reserved for Future

| Component | Pin | Phase | Purpose |
|-----------|-----|-------|---------|
| **DAC 0** | A0 | Phase 2 | CV Pitch Out (1V/octave) |
| **DAC 1** | A1 | Phase 2 | CV Velocity/Mod Out |
| **GPIO** | A2 | Phase 2 | Gate/Trigger Out |
| **GPIO** | A3 | Phase 3 | S-Trigger Out |
| **GPIO** | A4, A5 | Future | Additional CV/Gates |

**See:** [ARCHITECTURE.md - Pin Allocation](./ARCHITECTURE.md#pin-allocation)

---

## Software Status

### Phase 1: MIDI Core (In Development)

| Feature | Status | Location | Notes |
|---------|--------|----------|-------|
| **MIDI Input** | ✅ Done | Integration test | Receiving notes via UART RX |
| **MIDI Output** | ✅ Done | Integration test | Sending notes via UART TX |
| **USB MIDI Clock** | ✅ Done | Integration test | Clock sync from DAW |
| **MIDI Clock Handling** | ✅ Done | Integration test | 24 PPQN timing |
| **Button Input** | ✅ Done | UI layer | Debounced, long press support |
| **OLED Display** | ✅ Done | UI layer | SH1107 rendering |
| **Arpeggiator Engine** | ⏳ TODO | `/arp/core/` | Pattern generation |
| **Note Buffer** | ⏳ TODO | `/arp/core/` | Polyphonic storage |
| **Pattern Library** | ⏳ TODO | `/arp/core/` | Up/Down/Random/etc. |
| **Clock Division** | ⏳ TODO | `/arp/core/` | 1/4, 1/8, 1/16 notes |
| **UI Menu System** | ⏳ TODO | `/arp/ui/` | Pattern selection, settings |
| **Settings Storage** | ⏳ TODO | `/arp/utils/` | NVM persistence |

### Phase 2: CV/Gate Output (Future)

| Feature | Status | Location | Notes |
|---------|--------|----------|-------|
| **CV Pitch Driver** | 📋 Planned | `/arp/drivers/cv_gate.py` | A0 DAC, 1V/octave |
| **Gate Driver** | 📋 Planned | `/arp/drivers/cv_gate.py` | A2 GPIO |
| **Pitch Calibration** | 📋 Planned | `/arp/core/calibration.py` | User-guided |
| **Output Router** | 📋 Planned | `/arp/core/router.py` | MIDI vs. CV mode |

### Phase 3: S-Trigger Output (Future)

| Feature | Status | Location | Notes |
|---------|--------|----------|-------|
| **S-Trigger Driver** | 📋 Planned | `/arp/drivers/s_trigger.py` | A3 GPIO, inverted |
| **Mode Switching** | 📋 Planned | UI layer | Gate ↔ S-Trigger |

---

## Current Architecture

### Hardware Stack
```
┌─────────────────────────────┐
│  OLED FeatherWing           │  128x64 SH1107 + 3 Buttons
├─────────────────────────────┤
│  MIDI FeatherWing           │  DIN-5 IN/OUT, UART
├─────────────────────────────┤
│  Feather M4 CAN Express     │  SAMD51 120MHz, 2x DAC
└─────────────────────────────┘
         ↓ USB-C
    [Computer/DAW]
```

### Software Modules (Planned)
```
arp/
├── core/                      # ⏳ TODO
│   ├── arpeggiator.py        # Main engine
│   ├── note_buffer.py        # Note storage
│   ├── clock.py              # Clock sync
│   └── patterns.py           # Pattern library
├── drivers/
│   ├── midi_output.py        # ⏳ TODO - MIDI driver
│   ├── cv_gate.py            # 📋 Phase 2
│   └── s_trigger.py          # 📋 Phase 3
├── ui/
│   ├── display.py            # ✅ Working
│   ├── buttons.py            # ✅ Working (basic)
│   └── menu.py               # ⏳ TODO
└── main.py                    # ⏳ TODO - Entry point
```

---

## Testing Status

### ✅ Completed Tests

| Test | File | Result | Date |
|------|------|--------|------|
| **MIDI Output** | `tests/midi_output_test.py` | ✅ Pass | 2025-10-22 |
| **MIDI Input** | `tests/midi_input_test.py` | ✅ Pass | 2025-10-22 |
| **MIDI Loopback** | `tests/midi_loopback_test.py` | ✅ 100% | 2025-10-22 |
| **MIDI Clock** | `tests/integration_test_debug.py` | ✅ Pass | 2025-10-22 |
| **Full Integration** | `tests/integration_test_debug.py` | ✅ Pass | 2025-10-22 |
| **Button Debouncing** | `tests/button_clean_test.py` | ✅ Pass | 2025-10-22 |
| **OLED Display** | All tests | ✅ Pass | 2025-10-22 |
| **25+ Min Stability** | Integration test | ✅ Pass | 2025-10-22 |

### ⏳ Pending Tests

| Test | Description | Phase |
|------|-------------|-------|
| **Arpeggiator Patterns** | Verify Up/Down/Random patterns | Phase 1 |
| **Clock Sync Accuracy** | Measure MIDI clock jitter | Phase 1 |
| **Polyphonic Input** | 4-note chord handling | Phase 1 |
| **CV Calibration** | 1V/octave accuracy ±5mV | Phase 2 |
| **Gate Timing** | Pulse width 15ms ±2ms | Phase 2 |

---

## Development Environment

### Hardware
- **Board:** Adafruit Feather M4 CAN Express
- **Bootloader:** UF2 bootloader
- **Connection:** USB-C

### Software
- **OS:** macOS Darwin 24.6.0
- **Python:** CircuitPython 10.0.3
- **Libraries:**
  - `adafruit_displayio_sh1107` (OLED driver)
  - `adafruit_midi` (MIDI protocol)
  - `i2cdisplaybus` (I2C bus management)
- **Tools:**
  - `circup` - Library management
  - `scripts/monitor_serial.py` - Serial debugging

### Repository
- **Git:** https://github.com/keegandewitt/Arp
- **Branch:** main
- **Latest Commit:** `5264711` - MIDI integration complete

---

## Known Issues

### Current
- None! Hardware fully validated.

### Future Considerations
- **CV Output:** M4's DAC is 3.3V (0-3.3V range)
  - For true 1V/octave over 10 octaves (0-10V), need external op-amp
  - Can do 0.55V/octave over 6 octaves natively (0-3.3V)
- **S-Trigger:** Requires mode switching (cannot do both simultaneously)

---

## Next Steps

### Immediate (This Week)
1. ⏳ Create `arp/core/arpeggiator.py` - Main engine
2. ⏳ Create `arp/core/note_buffer.py` - Note storage
3. ⏳ Create `arp/core/patterns.py` - Pattern library (Up/Down/Random)
4. ⏳ Create `arp/drivers/midi_output.py` - MIDI driver abstraction
5. ⏳ Create basic `main.py` with simple up arpeggio

### Short Term (Next 2 Weeks)
1. ⏳ Implement clock synchronization
2. ⏳ Build UI menu system
3. ⏳ Add pattern selection (button controls)
4. ⏳ Add tempo/clock division controls
5. ⏳ Implement settings persistence (NVM)

### Long Term (Phase 2)
1. 📋 Design CV/Gate hardware interface
2. 📋 Implement CV pitch driver (A0 DAC)
3. 📋 Implement gate driver (A2 GPIO)
4. 📋 Build calibration routine
5. 📋 Add output mode switching (MIDI vs. CV)

---

## Documentation

### Completed
- ✅ `ARCHITECTURE.md` - Complete system design
- ✅ `METHODOLOGY.md` - Development approach
- ✅ `UI_ARCHITECTURE.md` - Button standards
- ✅ `hardware/ASSEMBLY_PROTOCOL.md` - Build guide
- ✅ `hardware/MIDI_PREFLIGHT_CHECKLIST.md` - Validation checklist
- ✅ `hardware/MIDI_BREADBOARD_WIRING.md` - Breadboard testing

### TODO
- ⏳ `API.md` - Module interfaces
- ⏳ `USER_GUIDE.md` - End-user documentation
- ⏳ `CONTRIBUTING.md` - Developer guide

---

## Resources

### Hardware Datasheets
- [Feather M4 CAN Express](https://www.adafruit.com/product/4759)
- [MIDI FeatherWing](https://www.adafruit.com/product/4740)
- [OLED FeatherWing 128x64](https://www.adafruit.com/product/4650)

### Software References
- [CircuitPython 10.x Docs](https://docs.circuitpython.org/)
- [MIDI Specification](https://www.midi.org/specifications)
- [1V/Octave Standard](https://en.wikipedia.org/wiki/CV/gate)

---

**Version:** 2.0
**Maintainer:** Keegan DeWitt
**Status:** Hardware validated, beginning software development
