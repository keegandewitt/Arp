# System Occupancy Reference

**A comprehensive map of all hardware, software, and conceptual resources in the Arp project**

**Last Updated:** 2025-10-23

---

## Philosophy

**Occupancy** tracks not just physical pins, but the entire system architecture:
- Physical connections (pins, connectors, buses)
- Data flows (MIDI routing, signal paths)
- Conceptual resources (processing loops, interrupts, timing)
- Output capabilities (jacks, triggers, signals)

**Purpose:** Prevent conflicts, plan expansions, and maintain a clear mental model of the system.

---

## 1. Physical Hardware Occupancy

### 1.1 Connector Occupancy

#### JST SH (STEMMA QT) Connectors

| Connector Location | Status | Connected To | Purpose |
|-------------------|--------|--------------|---------|
| **M4 Feather JST SH** | 🔴 RESERVED | Battery (future) | LiPo power integration |
| **OLED FeatherWing JST SH #1** | ✅ OCCUPIED | MCP4728 DAC | I2C to CV/Gate DAC |
| **OLED FeatherWing JST SH #2** | 🟢 AVAILABLE | - | Daisy-chain expansion |
| **MCP4728 DAC JST SH #1** | ✅ OCCUPIED | OLED FeatherWing | I2C from OLED |
| **MCP4728 DAC JST SH #2** | 🟢 AVAILABLE | - | Daisy-chain expansion |

**Status Key:**
- 🔴 RESERVED = Intentionally saved for specific future use
- ✅ OCCUPIED = Currently in use
- 🟢 AVAILABLE = Free for expansion

---

### 1.2 I2C Bus Occupancy

**Bus:** Shared communication line (SDA/SCL on D21/D22)

| Device | I2C Address | Connection Method | Data Purpose |
|--------|-------------|-------------------|--------------|
| **OLED FeatherWing** | 0x3C | Stacked headers | Display rendering, UI updates |
| **MCP4728 DAC** | 0x60 or 0x64* | STEMMA QT cable from OLED | CV pitch + Gate/Trigger output |

**Notes:**
- I2C is a shared bus - multiple devices coexist
- *Check actual address with I2C scan (varies by DAC variant)
- Bus speed: 100kHz (standard) or 400kHz (fast mode)
- Additional I2C devices can be added via STEMMA QT daisy-chain

---

### 1.3 UART Pin Occupancy

| UART | TX Pin | RX Pin | Status | Purpose | Data Flow |
|------|--------|--------|--------|---------|-----------|
| **UART0** | D1 (TX) | D0 (RX) | ✅ OCCUPIED | MIDI I/O (note data) | Bidirectional MIDI messages |
| **UART1** | D10 | D11 | ✅ OCCUPIED | MIDI Clock In | External clock reception |

**UART0 Data Flow:**
- RX (D0): Receives MIDI from keyboard/controller
- TX (D1): Sends arpeggiated MIDI to synth

**UART1 Data Flow:**
- RX (D11): Receives MIDI clock ticks from DAW/sequencer
- TX (D10): Unused (could send clock out in future)

---

### 1.4 GPIO Pin Occupancy

| Pin | Status | Function | Connected To | Signal Type |
|-----|--------|----------|--------------|-------------|
| **D5** | ✅ OCCUPIED | Button C (Next) | OLED FeatherWing | Digital input (pull-up) |
| **D6** | ✅ OCCUPIED | Button B (Confirm) | OLED FeatherWing | Digital input (pull-up) |
| **D9** | ✅ OCCUPIED | Button A (Previous) | OLED FeatherWing | Digital input (pull-up) |
| **D13** | 🟢 AVAILABLE | Onboard LED | M4 Feather | Digital output (optional) |

---

### 1.5 Analog/DAC Pin Occupancy

| Pin | Status | Function | Notes |
|-----|--------|----------|-------|
| **A0** | 🟢 AVAILABLE | DAC0 (12-bit) | Future: S-Trigger output (0-3.3V) |
| **A1** | 🟢 AVAILABLE | DAC1 (12-bit) | Future: Velocity CV or 2nd pitch CV (0-3.3V) |
| **A2-A5** | 🟢 AVAILABLE | Analog inputs | Future: Potentiometers (tempo, swing, gate length) |

**Note:** M4 internal DACs output 0-3.3V (not 0-5V like MCP4728)

---

### 1.6 MCP4728 DAC Channel Occupancy

| Channel | Pin Name | Status | Function | Voltage Range | Purpose |
|---------|----------|--------|----------|---------------|---------|
| **Channel A** | VA | 🔴 RESERVED | CV Pitch | 0-5V | 1V/octave or 1.035V/octave pitch control |
| **Channel B** | VB | 🔴 RESERVED | Gate/Trigger | 0-5V | V-trig (0V=off, 5V=on) or S-trig (inverted) |
| **Channel C** | VC | 🟢 AVAILABLE | - | 0-5V | Future: Velocity CV, Modulation, Clock out |
| **Channel D** | VD | 🟢 AVAILABLE | - | 0-5V | Future: 2nd gate, LFO out, envelope follower |

---

### 1.7 Physical Output Jack Occupancy

| Jack Type | Location | Status | Signal Source | Signal Type | Notes |
|-----------|----------|--------|---------------|-------------|-------|
| **MIDI IN (DIN-5)** | Rear panel | ✅ OCCUPIED | MIDI FeatherWing #1 RX | MIDI (31250 baud) | Receives notes from keyboard |
| **MIDI OUT (DIN-5)** | Rear panel | ✅ OCCUPIED | MIDI FeatherWing #1 TX | MIDI (31250 baud) | Sends arpeggiated notes to synth |
| **CV Pitch (3.5mm TRS)** | Rear panel | 🔴 RESERVED | MCP4728 Channel A | 0-5V analog | 1V/octave pitch CV |
| **Gate (3.5mm TRS)** | Rear panel | 🔴 RESERVED | MCP4728 Channel B | 0-5V digital | V-trig or S-trig |
| **S-Trigger (3.5mm TRS)** | Rear panel | 🟡 PLANNED | M4 A0 (DAC0) or MCP4728 Ch C | 0-5V inverted | Moog-style S-trigger (future) |

**Status Key:**
- ✅ OCCUPIED = Currently implemented and wired
- 🔴 RESERVED = Hardware allocated, software integration pending
- 🟡 PLANNED = Design specified, hardware not yet allocated
- 🟢 AVAILABLE = No allocation

---

## 2. Data Flow Occupancy

### 2.1 MIDI Message Routing

**Arpeggiation Translation Loop** (Core concept - OCCUPIED)

```
MIDI IN (Keyboard)
    ↓
[UART RX Buffer]
    ↓
[Note On/Off Detection]
    ↓
[Note Buffer (held notes)]
    ↓
[Arpeggiator Engine]
    ↓ (on clock tick)
[Generate Sequence] → Pattern (Up/Down/Random/etc.)
    ↓
[Arpeggiated Note Output]
    ↓
[UART TX Buffer]
    ↓
MIDI OUT (Synth)
```

**MIDI Pass-Through** (OCCUPIED - for non-note messages)

```
MIDI IN
    ↓
[UART RX Buffer]
    ↓
[Message Type Detection]
    ↓
If NOT Note On/Off:
    ↓
[Immediate Pass-Through] → Zero latency
    ↓
[UART TX Buffer]
    ↓
MIDI OUT
```

**Messages that bypass arpeggiator:**
- ✅ Pitch Bend
- ✅ Modulation (CC #1)
- ✅ Control Change (all CCs)
- ✅ Program Change
- ✅ Aftertouch (Channel Pressure)
- ✅ Polyphonic Key Pressure
- ✅ System Exclusive (SysEx)

**Messages processed by arpeggiator:**
- 🎹 Note On (velocity > 0)
- 🎹 Note Off (velocity = 0 or explicit Note Off)

---

### 2.2 CV/Gate Signal Path

**CV Pitch Output** (RESERVED - hardware allocated, software pending integration)

```
Arpeggiated Note
    ↓
[MIDI Note Number] (0-127)
    ↓
[Note-to-Voltage Conversion]
    ↓
voltage = CV_REF + ((note - 60) / 12) * V_PER_OCTAVE
    ↓
[DAC Value Calculation]
    ↓
dac_value = (voltage / 5.0) * 4095
    ↓
[MCP4728 Channel A Write]
    ↓
CV Pitch Jack (0-5V, 1V/octave)
```

**Gate/Trigger Output** (RESERVED - hardware allocated, software pending integration)

```
Note On Event
    ↓
[Gate State = HIGH]
    ↓
If V-trig: 5V
If S-trig: 0V (inverted)
    ↓
[MCP4728 Channel B Write]
    ↓
Gate Jack Output

Note Off Event
    ↓
[Gate State = LOW]
    ↓
If V-trig: 0V
If S-trig: 5V (inverted)
    ↓
[MCP4728 Channel B Write]
    ↓
Gate Jack Output
```

---

### 2.3 Clock Sync Flow

**External Clock (UART1)** (OCCUPIED)

```
DAW/Sequencer MIDI Clock
    ↓
MIDI FeatherWing #2 (UART1 RX)
    ↓
[UART1 RX Buffer - D11]
    ↓
[Timing Clock Message Detection] (0xF8)
    ↓
[BPM Calculation] (24 PPQN)
    ↓
[Clock Tick Distribution]
    ↓
Arpeggiator Step Callback
```

**Internal Clock** (OCCUPIED - fallback mode)

```
[Free-Running Timer]
    ↓
[BPM-to-Interval Calculation]
    ↓
interval = 60.0 / (BPM * clock_division)
    ↓
[Clock Tick Generation]
    ↓
Arpeggiator Step Callback
```

---

## 3. Trigger/Gate Output Occupancy

### 3.1 Gate Output Modes

| Mode | Status | Output Jack | Polarity | Behavior |
|------|--------|-------------|----------|----------|
| **V-Trigger (Standard)** | 🔴 RESERVED | Gate (MCP4728 Ch B) | 0V=off, 5V=on | Gate high during note, low on release |
| **S-Trigger (Moog)** | 🔴 RESERVED | Gate (MCP4728 Ch B) | 5V=off, 0V=on | Inverted gate (vintage Moog compatibility) |
| **Dedicated S-Trigger** | 🟡 PLANNED | S-Trig (M4 A0 or MCP4728 Ch C) | 5V=off, 0V=on | Separate jack for S-trigger (future) |

**Current Implementation Status:**
- ✅ V-trig/S-trig polarity switching: Software complete (arp/drivers/cv_gate.py)
- 🔴 Gate jack wiring: Hardware allocated (MCP4728 Ch B), not yet wired
- 🔴 Integration: Not yet integrated into main.py
- 🟡 Dedicated S-trig jack: Planned for future (separate output)

---

### 3.2 Trigger Types & Use Cases

| Trigger Type | Jack | Use Case | Compatible Synths |
|--------------|------|----------|-------------------|
| **V-Trigger** | Gate (Ch B) | Modern modular, eurorack | Arturia, Moog (modern), Make Noise, etc. |
| **S-Trigger** | Gate (Ch B, inverted) | Vintage Moog gear | Minimoog, Moog Source, ARP 2600 (S-trig mode) |
| **Dedicated S-Trig** | S-Trig (future) | Vintage compatibility without polarity switching | Moog, ARP, Korg MS-20 |

---

## 4. Processing Loop Occupancy

### 4.1 Main Loop Responsibilities

**Current main loop tasks** (main.py):

| Task | Frequency | Priority | Purpose |
|------|-----------|----------|---------|
| **MIDI Input Processing** | Every loop (~100Hz) | HIGH | Read UART, detect Note On/Off, update note buffer |
| **Button Polling** | Every loop (~100Hz) | MEDIUM | Debounce buttons, detect short/long press |
| **Clock Tick Processing** | On clock event | HIGH | Trigger arpeggiator step callback |
| **Display Update** | 10Hz (100ms) | LOW | Refresh OLED with BPM, pattern, status |
| **Sleep Check** | 1Hz (1000ms) | LOW | Check for inactivity timeout |
| **Garbage Collection** | Every 100 loops | LOW | Free unused memory |

**Future additions (pending):**
| Task | Frequency | Priority | Purpose |
|------|-----------|----------|---------|
| **CV Output Update** | On note change | HIGH | Update MCP4728 CV pitch + gate |

---

### 4.2 Interrupt/Callback Occupancy

| Interrupt/Callback | Trigger | Handler | Purpose |
|-------------------|---------|---------|---------|
| **Clock Step Callback** | Clock tick (internal or external) | `on_clock_step()` | Play next arpeggiated note |
| **UART RX Interrupt** | MIDI byte received | CircuitPython UART driver | Buffer incoming MIDI |
| **USB MIDI Callback** | USB MIDI message | (future for Vintage Mode) | Receive VST control commands |

---

## 5. Conceptual Resource Occupancy

### 5.1 Software Modules

| Module | Status | Purpose | Dependencies |
|--------|--------|---------|--------------|
| **arp/core/clock.py** | ✅ COMPLETE | Clock management (internal + external) | usb_midi, time |
| **arp/ui/display.py** | ✅ COMPLETE | OLED rendering and UI | adafruit_displayio_sh1107 |
| **arp/ui/buttons.py** | ✅ COMPLETE | Button debouncing and press detection | digitalio, time |
| **arp/ui/menu.py** | ✅ COMPLETE | Settings menu navigation | Settings |
| **arp/utils/config.py** | ✅ COMPLETE | Settings persistence (NVM) | struct, microcontroller.nvm |
| **arp/drivers/cv_gate.py** | 🔴 RESERVED | CV/Gate output driver | adafruit_mcp4728, i2c |

---

### 5.2 Memory Budget (SAMD51 - 192KB RAM)

| Resource | Usage | Allocated | Purpose |
|----------|-------|-----------|---------|
| **CircuitPython Runtime** | ~40KB | Fixed | Interpreter, libraries |
| **MIDI Buffers** | ~2KB | Fixed | UART RX/TX buffers (2x 1KB) |
| **Display Framebuffer** | ~1KB | Fixed | OLED bitmap (128x64 / 8) |
| **Note Buffer** | ~256 bytes | Dynamic | Held notes (max 16 notes × 16 bytes) |
| **Arp Sequence** | ~128 bytes | Dynamic | Arpeggiated sequence |
| **Settings** | 20 bytes | Fixed | NVM settings (struct packed) |
| **Vintage Mode Buffer** | ~7KB | Future | 1000 MIDI events (7 bytes each) |
| **Free RAM** | ~140KB | Available | Expansion, fragmentation overhead |

---

### 5.3 Timing Budget (Main Loop @ ~100Hz = 10ms per iteration)

| Task | Time Budget | Actual | Notes |
|------|-------------|--------|-------|
| **MIDI RX Processing** | 1ms | <0.5ms | Fast, interrupt-driven |
| **Button Polling** | 1ms | <0.5ms | Simple GPIO reads |
| **Clock Processing** | 2ms | <1ms | Only on clock tick |
| **Display Update** | 5ms | ~3ms | I2C write (only every 10 loops) |
| **CV Output** | 1ms | <0.5ms | I2C write to MCP4728 |
| **Slack Time** | 5ms | - | Overhead, variability |

**Total:** ~10ms maximum per loop (100Hz sustained)

---

## 6. Expansion Planning

### 6.1 Available Resources

**Hardware:**
- 🟢 2x MCP4728 DAC channels (C, D) → Velocity CV, modulation, 2nd gate
- 🟢 2x M4 internal DACs (A0, A1) → S-trigger, 2nd CV (0-3.3V)
- 🟢 Multiple GPIO pins → Encoders, extra buttons, LEDs
- 🟢 Analog inputs (A2-A5) → Potentiometers for live control
- 🟢 I2C STEMMA QT expansion → More DACs, displays, sensors

**Software:**
- 🟢 ~140KB free RAM → Larger buffers, more patterns, audio processing
- 🟢 ~5ms loop time slack → Additional processing tasks
- 🟢 NVM storage → More settings, user presets

**Conceptual:**
- 🟢 Unused interrupt capacity → Faster response to events
- 🟢 UART1 TX (D10) → MIDI clock out, MIDI merge

---

### 6.2 Future Expansion Possibilities

| Expansion | Resources Required | Complexity | Priority |
|-----------|-------------------|------------|----------|
| **Velocity CV** | MCP4728 Ch C, 1x TRS jack | Low | Medium |
| **2nd Gate (for drums)** | MCP4728 Ch D, 1x TRS jack | Low | Low |
| **Dedicated S-Trigger** | M4 A0, 1x TRS jack | Low | Medium |
| **Swing/Humanize** | Software only | Medium | High |
| **Tempo Pot** | A2 analog input | Low | High |
| **Gate Length Pot** | A3 analog input | Low | Medium |
| **Rotary Encoder** | 2x GPIO (D7, D8) | Medium | High |
| **MIDI Clock Out** | UART1 TX (D10) | Low | Medium |
| **Vintage Mode** | USB MIDI, 7KB RAM | High | High |
| **LiPo Battery** | M4 JST SH, voltage monitor | Medium | High |

---

## 7. Conflict Prevention

### 7.1 Pin Conflict Matrix

| Resource | Conflict With | Resolution |
|----------|---------------|------------|
| **M4 JST SH** | I2C devices needing STEMMA QT | Use OLED's STEMMA QT instead |
| **D0/D1 (UART0)** | Any GPIO use | Exclusively reserved for MIDI I/O |
| **D10/D11 (UART1)** | Any GPIO use | Exclusively reserved for MIDI Clock |
| **D21/D22 (I2C)** | Multiple I2C devices | Safe - bus is shared, use daisy-chain |
| **MCP4728 Ch A/B** | CV/Gate outputs | Reserved - do not reassign |

---

### 7.2 Conceptual Conflicts

| Concept | Conflict With | Resolution |
|---------|---------------|------------|
| **Arpeggiation Loop** | MIDI pass-through | Separate logic: arpeggiator only processes Note On/Off |
| **Internal Clock** | External Clock | Priority system: external overrides internal |
| **V-trig** | S-trig | User setting, single jack with polarity toggle |
| **Vintage Mode** | Normal Arp Mode | Exclusive modes: disable local UI when in Vintage Mode |

---

## 8. Occupancy Update Protocol

**When adding new hardware or features:**

1. ✅ **Check this document** for available resources
2. ✅ **Update relevant occupancy tables** (pins, connectors, data flows)
3. ✅ **Document new conflicts** in conflict matrix
4. ✅ **Update expansion capacity** section
5. ✅ **Commit changes** with clear description
6. ✅ **Update date** at top of document

**Example commit message:**
```
docs: Update OCCUPANCY.md for CV pitch integration

- Marked MCP4728 Ch A as RESERVED for CV pitch
- Added CV pitch signal flow diagram
- Updated I2C bus occupancy (added MCP4728)
- Documented CV jack allocation (rear panel 3.5mm TRS)
```

---

## 9. Quick Reference

### Active Data Flows (OCCUPIED)
- ✅ MIDI IN → Note buffer → Arpeggiator → MIDI OUT
- ✅ MIDI IN → Pass-through (non-notes) → MIDI OUT (zero latency)
- ✅ UART1 RX → External clock → Arpeggiator timing
- ✅ Button presses → Menu navigation → Settings changes
- ✅ OLED display ← UI updates ← System state

### Reserved/Pending (HARDWARE ALLOCATED)
- 🔴 Arpeggiated notes → CV pitch → MCP4728 Ch A → CV jack
- 🔴 Note On/Off → Gate logic → MCP4728 Ch B → Gate jack

### Planned (FUTURE)
- 🟡 USB MIDI → Vintage Mode → Buffer playback → MIDI OUT
- 🟡 S-trigger logic → M4 A0 or MCP4728 Ch C → S-Trig jack

---

**This document is the single source of truth for system resource allocation.**

**Update it religiously as the project evolves!**
