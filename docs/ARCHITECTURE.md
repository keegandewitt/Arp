# Arp - Hardware Arpeggiator Architecture

**Vision:** A powerful hardware arpeggiator that bridges the MIDI and modular CV/Gate worlds, with flexible output routing and clock synchronization.

---

## Core Concept

**Input:** MIDI notes from keyboards, sequencers, or DAW
**Processing:** Real-time arpeggiation with multiple patterns and modes
**Output:** MIDI, CV/Gate, and S-Trigger (selectable per session)

---

## Hardware Architecture

### Main Board: Adafruit Feather M4 CAN Express
- **MCU:** SAMD51 (120MHz ARM Cortex-M4)
- **RAM:** 192KB
- **Flash:** 512KB
- **DACs:** 2x 12-bit (A0, A1)
- **USB:** Native USB MIDI support
- **UART:** Hardware UART on D0/D1

### FeatherWing Stack (Bottom to Top)
```
┌─────────────────────────────┐
│  OLED FeatherWing (128x64)  │  ← UI + 3 Buttons
├─────────────────────────────┤
│  MIDI FeatherWing           │  ← MIDI IN/OUT (DIN-5)
├─────────────────────────────┤
│  Feather M4 CAN Express     │  ← Main processor
└─────────────────────────────┘
         ↓ USB-C
    [Computer/DAW]
```

### Pin Allocation

#### Currently Used (Phase 1)
```
D0  (RX)     → MIDI FeatherWing RX
D1  (TX)     → MIDI FeatherWing TX
D5           → OLED Button C
D6           → OLED Button B
D9           → OLED Button A
D21 (SDA)    → OLED I2C Data
D22 (SCL)    → OLED I2C Clock
3V           → Shared power rail
GND          → Shared ground
```

#### Reserved for Future (Phase 2 & 3)
```
A0  (DAC0)   → CV Pitch Out (1V/octave)
A1  (DAC1)   → CV Velocity/Mod Out
A2           → Gate/Trigger Out (standard)
A3           → S-Trigger Out (alternative mode)
A4           → Future: Gate 2 / Accent Out
A5           → Future: Clock Out
D10-D13      → Future: Additional triggers/gates
```

#### Available for Expansion
```
CAN_TX, CAN_RX → Future: Multi-unit networking
D11, D12, D13  → Future: External controls
```

---

## Software Architecture

### Modular Design Principle
**Core Engine** is independent of output method
→ Output drivers are pluggable modules

```
┌──────────────────────────────────────────┐
│           MIDI Input Layer               │
│  - USB MIDI (DAW/Computer)              │
│  - DIN MIDI IN (Hardware Keyboards)     │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│         Arpeggiator Engine               │
│  - Note Buffer (polyphonic input)       │
│  - Pattern Generator (Up/Down/Random)   │
│  - Clock Sync (Internal/External)       │
│  - Rhythm Patterns (1/4, 1/8, 1/16)     │
└──────────────────┬───────────────────────┘
                   ↓
┌──────────────────────────────────────────┐
│         Output Router                    │
│  - Mode Selection (MIDI/CV/S-Trig)      │
│  - Routing Logic                        │
└─────┬────────────┬────────────┬──────────┘
      ↓            ↓            ↓
┌─────────┐  ┌─────────┐  ┌─────────┐
│  MIDI   │  │ CV/Gate │  │ S-Trig  │
│ Driver  │  │ Driver  │  │ Driver  │
└─────────┘  └─────────┘  └─────────┘
```

### Directory Structure
```
arp/
├── core/
│   ├── arpeggiator.py      # Main arp engine
│   ├── note_buffer.py      # Polyphonic note storage
│   ├── clock.py            # Clock sync engine
│   └── patterns.py         # Arp pattern library
├── drivers/
│   ├── midi_output.py      # MIDI OUT driver
│   ├── cv_gate.py          # CV/Gate driver (Phase 2)
│   └── s_trigger.py        # S-Trigger driver (Phase 3)
├── ui/
│   ├── display.py          # OLED display manager
│   ├── buttons.py          # Button input handler
│   └── menu.py             # UI menu system
├── utils/
│   ├── config.py           # User settings
│   └── midi_helpers.py     # MIDI utilities
└── main.py                 # Application entry point
```

---

## Data Flow

### 1. Input Processing
```
[MIDI Keyboard] → [MIDI IN] → Note Buffer
         OR
[USB MIDI]      → [USB IN]  → Note Buffer
```

### 2. Arpeggiation
```
Note Buffer → Arpeggiator Engine
              ├─ Select pattern (Up/Down/Random)
              ├─ Apply clock division (1/4, 1/8, 1/16)
              ├─ Generate note sequence
              └─ Sync to clock (USB/MIDI/Internal)
```

### 3. Output Routing
```
Arpeggiator → Output Router → [Selected Driver]
                               ├─ MIDI Driver → DIN OUT
                               ├─ CV Driver → A0 (pitch) + A2 (gate)
                               └─ S-Trig Driver → A3 (inverted gate)
```

---

## Feature Implementation Phases

### Phase 1: MIDI Core (NOW)
**Status:** In Development
**Goal:** Fully functional MIDI arpeggiator

Features:
- ✅ MIDI IN: Receive notes from keyboard/controller
- ✅ MIDI OUT: Send arpeggiated notes to synths
- ✅ USB MIDI: Receive clock from DAW
- ⏳ Arp Patterns: Up, Down, Up/Down, Random
- ⏳ Clock Division: 1/4, 1/8, 1/16 notes
- ⏳ Note Range: 1-4 octaves
- ⏳ OLED UI: Pattern selection, tempo display
- ⏳ Button Control: Pattern, octave, tempo

**Output:** MIDI notes via DIN-5 jack

---

### Phase 2: CV/Gate Output (FUTURE)
**Status:** Hardware Reserved, Not Implemented
**Goal:** Control modular synthesizers

Features:
- ⬜ CV Pitch: 1V/octave on A0 (with optional op-amp)
- ⬜ Gate Out: Standard 5V gate on A2
- ⬜ CV Velocity: Velocity → CV on A1
- ⬜ Output Mode Selection: MIDI vs. CV/Gate
- ⬜ Pitch calibration routine
- ⬜ Gate length control

**Output:** CV pitch + Gate trigger via 3.5mm jacks

**Hardware Needs:**
- 3.5mm mono jacks (3x minimum)
- Op-amp for 1V/octave scaling (optional)
- Protection circuitry

---

### Phase 3: S-Trigger Output (FUTURE)
**Status:** Hardware Reserved, Not Implemented
**Goal:** Support vintage gear (Yamaha CS-series, ARP, Korg MS-series)

Features:
- ⬜ S-Trigger: Inverted gate (normally HIGH, pulse LOW)
- ⬜ Mode toggle: Standard Gate vs. S-Trigger
- ⬜ Shared jack with standard trigger (user selectable)

**Output:** S-Trigger via same gate jack (mode switched)

**Hardware Needs:**
- Same 3.5mm jack as Phase 2 gate
- Software mode switching only

---

## Clock Synchronization

### Input Sources (Priority Order)
1. **USB MIDI Clock** (from DAW) - Highest priority
2. **DIN MIDI Clock** (from hardware sequencer)
3. **Internal Clock** (free-running, user adjustable)

### Clock Processing
```python
# Pseudocode
if usb_midi_clock_detected:
    sync_to_usb_clock()
elif din_midi_clock_detected:
    sync_to_din_clock()
else:
    use_internal_clock(bpm=120)
```

### Clock Division
- **Quarter Notes:** 6 clocks (24 PPQN ÷ 4)
- **Eighth Notes:** 3 clocks (24 PPQN ÷ 8)
- **Sixteenth Notes:** 1.5 clocks (24 PPQN ÷ 16)

---

## User Interface Design

### OLED Display Layout (128x64)
```
┌────────────────────────┐
│ ARP  UP   ♩=120  Oct:2 │  ← Status line
├────────────────────────┤
│ [C] [E] [G]            │  ← Active notes
├────────────────────────┤
│ MIDI OUT: Ch 1         │  ← Output mode
│ ▶ C4  E4  G4  C5       │  ← Arp preview
└────────────────────────┘
```

### Button Functions

#### Single Press
- **Button A:** Cycle arp pattern (Up → Down → Up/Down → Random)
- **Button B:** Cycle clock division (1/4 → 1/8 → 1/16)
- **Button C:** Cycle octave range (1 → 2 → 3 → 4)

#### Long Press (0.5s)
- **Button A:** Enter settings menu
- **Button B:** Tap tempo
- **Button C:** Output mode (MIDI → CV/Gate → S-Trig)

#### Combinations
- **A + B:** Latch mode on/off
- **B + C:** Reset to defaults

---

## Configuration System

### Settings Storage
Use CircuitPython's `microcontroller.nvm` for persistent settings:

```python
# settings.py
class Settings:
    def __init__(self):
        self.pattern = "up"          # up, down, updown, random
        self.clock_div = 8           # 4, 8, 16
        self.octave_range = 2        # 1-4
        self.output_mode = "midi"    # midi, cv_gate, s_trigger
        self.midi_channel = 1        # 1-16
        self.tempo = 120             # BPM (internal clock)

    def save(self):
        # Serialize to NVM
        pass

    def load(self):
        # Deserialize from NVM
        pass
```

---

## Performance Requirements

### Timing Constraints
- **MIDI Clock Response:** < 1ms jitter
- **Note Latency:** < 5ms (input to output)
- **Gate Pulse Width:** 15ms minimum (adjustable)
- **CV Settling Time:** < 2ms (for pitch changes)

### CPU Budget
- **Main Loop:** 100Hz (10ms cycle)
- **MIDI Processing:** Event-driven (non-blocking)
- **Display Update:** 30Hz (33ms)
- **Button Polling:** 100Hz (10ms)

---

## Future Expansion Ideas

### Networking (CAN Bus)
- Multiple Arp units synchronized via CAN
- One master clock, multiple arp voices
- Distributed polyphony

### External Control
- CV input for tempo modulation
- Gate input for step advance
- Expression pedal for arp speed

### Advanced Features
- **Swing:** Shuffle timing
- **Velocity Curves:** Dynamic expression
- **MIDI Learn:** Map parameters to CC
- **Pattern Memory:** Save/recall 8 presets

---

## Hardware BOM (Current + Reserved)

### Phase 1 (Current)
- [x] Feather M4 CAN Express
- [x] MIDI FeatherWing
- [x] OLED FeatherWing 128x64
- [x] USB-C cable
- [x] MIDI cables (DIN-5)

### Phase 2 (Future - CV/Gate)
- [ ] 3x 3.5mm mono jacks (Pitch, Velocity, Gate)
- [ ] Op-amp circuit (MCP6002 or similar) for 1V/octave
- [ ] Protection diodes
- [ ] Enclosure with panel cutouts

### Phase 3 (Future - S-Trigger)
- [ ] No additional hardware (software toggle only)

---

## Testing Strategy

### Phase 1 Tests
- [x] MIDI loopback (100% message success)
- [x] Button debouncing and long press
- [x] OLED rendering (SH1107 driver)
- [x] Integration test (M4 + OLED + MIDI)
- [ ] Arpeggiator engine (pattern generation)
- [ ] Clock sync (USB MIDI clock)
- [ ] Full UI flow

### Phase 2 Tests (Future)
- [ ] CV calibration (1V/octave accuracy)
- [ ] Gate timing (pulse width verification)
- [ ] CV slew rate (pitch stability)

### Phase 3 Tests (Future)
- [ ] S-Trigger polarity (inverted gate)
- [ ] Mode switching (gate ↔ s-trigger)

---

**Version:** 2.0
**Date:** 2025-10-22
**Status:** Architecture defined, Phase 1 in progress
