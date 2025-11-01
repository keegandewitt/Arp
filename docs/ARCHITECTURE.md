# prisme - MIDI/CV Translation Hub Architecture

**Version:** 2.0
**Last Updated:** 2025-11-01
**Status:** Architecture Definition

---

## Mission Statement

**prisme** is a full-service USB-C powered MIDI/CV translation hub with imperceptible latency. It bridges the gap between MIDI controllers, DAWs, hardware synthesizers, and Eurorack modular systems by applying real-time transformations to musical data.

### What Makes prisme Special

1. **Translation Layers**: Apply musical transformations (Scale Quantization, Arpeggiation, Clock Manipulation) to incoming MIDI/CV data in real-time
2. **Loopback Mode**: Hardware synths can connect their MIDI OUT → prisme IN → prisme OUT → Synth IN, adding features like arpeggiation and scale quantization without a DAW
3. **Universal Output**: Simultaneously outputs to MIDI OUT, USB MIDI, CV (pitch), Gate/Trigger, and Custom CC - no configuration needed
4. **Zero-Latency Design**: Sub-millisecond processing ensures imperceptible lag
5. **Flexible Routing**: Switch between Thru (passthrough) and Translation (transform) modes

---

## Signal Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INPUT SELECTION                              │
│                         (User selects ONE)                           │
│                                                                       │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │ MIDI IN  │   │  USB-C   │   │  CV IN   │   │ GATE IN  │        │
│  │  (DIN)   │   │  (MIDI)  │   │ (1/8" TRS)│  │(1/8" TRS)│        │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘        │
│       │              │              │              │                │
│       └──────────────┴──────────────┴──────────────┘                │
│                          │                                           │
│                          ▼                                           │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ROUTING MODE SWITCH                             │
│                                                                       │
│         ┌────────────┐                    ┌──────────────┐          │
│         │   THRU     │                    │ TRANSLATION  │          │
│         │ (Bypass)   │◄──── User ────────►│  (Transform) │          │
│         └─────┬──────┘    Setting         └──────┬───────┘          │
│               │                                   │                  │
│               │                                   ▼                  │
│               │                    ┌──────────────────────────┐     │
│               │                    │   TRANSLATION LAYERS     │     │
│               │                    │   (User-Defined Order)   │     │
│               │                    │                          │     │
│               │                    │  ┌────────────────────┐ │     │
│               │                    │  │  Layer Priority:   │ │     │
│               │                    │  │  1. [Scale/Arp]    │ │     │
│               │                    │  │  2. [Arp/Scale]    │ │     │
│               │                    │  │  3. Clock          │ │     │
│               │                    │  └────────────────────┘ │     │
│               │                    │                          │     │
│               │                    │  Each layer can be       │     │
│               │                    │  enabled/disabled        │     │
│               │                    └────────────┬─────────────┘     │
│               │                                 │                   │
│               └─────────────┬───────────────────┘                   │
│                             ▼                                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    OUTPUT TO ALL DESTINATIONS                        │
│                      (Simultaneous, Always)                          │
│                                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ MIDI OUT │  │  USB-C   │  │  CV OUT  │  │ GATE OUT │           │
│  │  (DIN)   │  │  (MIDI)  │  │(1/8" TRS)│  │(1/8" TRS)│           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                       │
│                    ┌──────────────┐                                  │
│                    │ CUSTOM CC OUT│                                  │
│                    │  (1/8" TRS)  │                                  │
│                    └──────────────┘                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Input Sources (Exclusive Selection)

User selects **ONE** active input source at a time:

| Input | Hardware | Format | Notes |
|-------|----------|--------|-------|
| **MIDI IN** | DIN-5 jack (via MIDI FeatherWing) | Standard MIDI | Most common, hardware synths/controllers |
| **USB-C** | USB MIDI device class | USB MIDI | DAW, MIDI controllers, iPad |
| **CV IN** | 1/8" TRS jack → ADC (A2) | 0-10V → 0-3.3V (scaled) | Modular CV sources (future) |
| **GATE IN** | 1/8" TRS jack → GPIO (D4) | 5V/12V gate (protected) | Modular trigger/clock (future) |

**Why Exclusive?**
- Prevents accidental signal merging (user confusion)
- Reduces CPU overhead
- Clear signal path (easier to debug)

---

## Routing Modes

### 1. THRU Mode (Passthrough)
- Input data is sent **directly** to all outputs
- No translation layers applied
- Zero-latency bypass
- Use case: prisme acts as a simple MIDI/CV hub

### 2. TRANSLATION Mode (Transform)
- Input data passes through **enabled translation layers**
- Layers applied in **user-defined order**
- Output is transformed musical data
- Use case: Add arpeggiation, scale quantization, swing, etc.

**User Controls:**
- Toggle between modes via menu (or dedicated button)
- Visual feedback on OLED (e.g., "THRU" vs "XLATE")

---

## Translation Layers

### Layer System Architecture

Each translation layer is:
- **Independently enabled/disabled** (bypass if disabled)
- **User-orderable** (priority 1, 2, 3...)
- **Stateless** (doesn't affect other layers)

### Available Layers

#### 1. Scale Quantization Layer
**Function:** Quantizes incoming notes to a selected musical scale

**Parameters:**
- Root note (C, C#, D, ..., B)
- Scale type (Major, Minor, Dorian, Phrygian, etc.)
- Enabled/Disabled

**Data Flow:**
```
Input: MIDI note 61 (C#)
Scale: C Major (C, D, E, F, G, A, B)
Output: MIDI note 60 (C) - quantized down to nearest scale note
```

**Current Status:** ✅ Implemented (`arp/processors/scale_quantizer.py`)

---

#### 2. Arpeggiation Layer
**Function:** Converts held chords into arpeggiated note sequences

**Parameters:**
- Pattern (Up, Down, Up/Down, Random, etc.)
- Rate (1/4, 1/8, 1/16, 1/32 notes)
- Octave range (1-4 octaves)
- Gate length (10%-100%)
- Enabled/Disabled

**Data Flow:**
```
Input: Notes [C3, E3, G3] held simultaneously
Pattern: Up
Rate: 1/16
Output: C3 → E3 → G3 → C3 → E3 → G3... (repeating)
```

**Current Status:** ✅ Implemented (`arp/processors/arpeggiator.py`)

---

#### 3. Clock Layer
**Function:** Manipulates timing and groove of MIDI clock and arpeggiator

**Parameters:**
- Clock source (Internal, External MIDI, External Gate, USB)
- Tempo multiply/divide (2x, 1x, 1/2, 1/4, 1/8...)
- Swing percentage (0%-75%)
- Enabled/Disabled

**Data Flow:**
```
Input: External MIDI clock at 120 BPM
Settings: Divide by 2, Swing 50%
Output: Arpeggiator runs at 60 BPM with swing applied
```

**Current Status:** 🟡 Partially implemented (clock source selection exists, swing/multiply not yet implemented)

**Implementation Notes:**
- Swing: Delay every 2nd clock tick by X% (16th note swing)
- Multiply: Send N clock ticks for every 1 received
- Divide: Send 1 clock tick for every N received

---

### Translation Layer Ordering

**User-Definable Priority:**

The user can choose which layer is applied first:

**Option A: Scale → Arp**
1. Quantize incoming notes to scale
2. Arpeggiate the quantized notes
3. Apply clock timing/swing

**Example:**
```
Input: [C#3, E3, G#3] (not in C Major scale)
After Scale: [C3, E3, G3] (quantized to C Major)
After Arp: C3 → E3 → G3 → C3... (arpeggiated)
```

**Option B: Arp → Scale**
1. Arpeggiate incoming notes (as-is)
2. Quantize each arpeggiated note to scale
3. Apply clock timing/swing

**Example:**
```
Input: [C#3, E3, G#3]
After Arp: C#3 → E3 → G#3 → C#3... (arpeggiated first)
After Scale: C3 → E3 → G3 → C3... (then quantized)
```

**Why This Matters:**
- Different creative results
- Arp → Scale can create unexpected melodic patterns
- Scale → Arp ensures strict scale adherence

**Implementation:**
- User setting: "Translation Order" (Scale First / Arp First)
- Code applies layers in specified order
- Clock layer always applied last (affects timing, not notes)

---

## Output Destinations (Simultaneous)

All outputs are **active simultaneously** with no user configuration required.

| Output | Hardware | Format | Latency |
|--------|----------|--------|---------|
| **MIDI OUT** | DIN-5 jack | Standard MIDI | ~320 μs |
| **USB-C** | USB MIDI device class | USB MIDI | ~50 μs |
| **CV OUT** | 1/8" TRS (MCP4728 Ch A) | 1V/octave or 1.035V/octave | ~20 μs |
| **GATE OUT** | 1/8" TRS (MCP4728 Ch B or GPIO D10) | V-trig (5V) or S-trig (GND) | ~20 μs |
| **CUSTOM CC OUT** | 1/8" TRS (MCP4728 Ch D) | 0-5V (unipolar) or ±5V (bipolar) | ~20 μs |

**Total Output Latency:** < 0.5 milliseconds (imperceptible)

**Why Send Everywhere?**
- Zero configuration for user
- Negligible CPU/battery cost
- Simplified code architecture
- User can connect/disconnect outputs freely

---

## Clock System Architecture

### Clock Sources (User Selectable)

| Source | Input | Priority | Notes |
|--------|-------|----------|-------|
| **Internal** | Software timer | User set (20-300 BPM) | Default, always available |
| **MIDI Clock** | MIDI IN or USB | External device | 24 PPQN standard |
| **Gate/Trig** | GPIO D4 (future) | External modular | Rising edge detection |
| **USB Clock** | USB MIDI clock | External DAW | 24 PPQN standard |

### Clock Transformations

#### 1. Tempo Multiply/Divide
- **Multiply** (2x, 3x, 4x): Speed up clock
  - Example: 120 BPM × 2 = 240 BPM
- **Divide** (1/2, 1/4, 1/8): Slow down clock
  - Example: 120 BPM ÷ 2 = 60 BPM

**Use Cases:**
- Sync arpeggiator to half-time or double-time of external clock
- Create polyrhythms

#### 2. Swing/Groove
- **Swing Percentage** (0%-75%)
- Delays every 2nd 16th note by specified percentage
- Example: 50% swing = classic shuffle feel

**Formula:**
```python
if tick % 2 == 1:  # Every 2nd 16th note
    delay_ms = (tick_interval * swing_percent / 100)
    time.sleep(delay_ms)
```

### Clock Display
OLED shows:
- Current tempo (BPM)
- Clock source (Int/Ext/Gate/USB)
- Multiply/divide factor (e.g., "×2" or "÷4")
- Swing percentage (e.g., "Swing: 50%")

---

## Custom CC Reference System

### Problem
Different MIDI CCs expect different voltage behaviors:
- **Unipolar** (0-5V): Mod wheel, filter cutoff, volume
- **Bipolar** (±5V): Pan (center = 0V), pitch bend
- **Binary** (0V or 5V): Sustain pedal (on/off)

### Solution: CC Reference Table
A lookup table maps each CC number (0-127) to:
- **Name** (e.g., "Mod Wheel")
- **Polarity** (Unipolar, Bipolar, Binary)
- **Voltage range** (0-5V, ±5V, etc.)
- **Common usage** (brief description)

**Implementation:**
```python
CC_REFERENCE = {
    1: {
        "name": "Mod Wheel",
        "polarity": "unipolar",
        "range": "0-5V",
        "behavior": "linear"
    },
    10: {
        "name": "Pan",
        "polarity": "bipolar",
        "range": "±5V",
        "behavior": "center_zero"  # 64 = 0V
    },
    64: {
        "name": "Sustain Pedal",
        "polarity": "binary",
        "range": "0V or 5V",
        "behavior": "threshold"  # <64 = 0V, ≥64 = 5V
    }
}
```

**Usage:**
When user selects CC #10 (Pan):
1. Lookup in reference table → "bipolar", "±5V"
2. Apply voltage conversion: `voltage = ((value - 64) / 64) * 5.0`
3. Output: CC value 0 = -5V, 64 = 0V, 127 = +5V

**Document:** `docs/reference/CC_REFERENCE_TABLE.md`

---

## Hardware I/O Summary

### Inputs (User selects ONE)
- 🔌 **MIDI IN** (DIN-5 jack)
- 🔌 **USB-C** (MIDI device class)
- 🔌 **CV IN** (1/8" TRS) - *Future*
- 🔌 **GATE IN** (1/8" TRS) - *Future*

### Outputs (All active simultaneously)
- 🔌 **MIDI OUT** (DIN-5 jack)
- 🔌 **USB-C** (MIDI device class)
- 🔌 **CV OUT** (1/8" TRS, 1V/octave)
- 🔌 **GATE OUT** (1/8" TRS, V-trig or S-trig)
- 🔌 **CUSTOM CC OUT** (1/8" TRS, 0-5V or ±5V)

### Control Interface
- 🖥️ **OLED Display** (128x64 SH1107)
- 🔘 **Button A** (Pattern/Navigation)
- 🔘 **Button B** (Confirm/Long-press features)
- 🔘 **Button C** (Settings/Navigation)

---

## Technical Specifications

### Performance
- **Latency:** < 0.5ms (sub-millisecond)
- **Clock Jitter:** < ±50μs (tight timing)
- **MIDI Throughput:** ~3,000 messages/sec
- **Power Consumption:** ~150mA @ 5V (USB-C powered)
- **Battery Life:** 6-7 hours continuous (500mAh LiPo)

### Hardware Platform
- **MCU:** Adafruit Feather M4 CAN Express
  - ATSAMD51J19A (120MHz Cortex-M4)
  - 192KB RAM, 512KB Flash
  - Hardware floating-point unit
- **DAC:** MCP4728 (4-channel, 12-bit, I2C)
- **Display:** SH1107 OLED (128x64, I2C)
- **MIDI I/O:** MIDI FeatherWing (optocoupler isolated)

### Software
- **Language:** CircuitPython 9.x
- **Architecture:** Event-driven, non-blocking
- **Libraries:**
  - `adafruit_midi` (MIDI parsing)
  - `adafruit_mcp4728` (DAC control)
  - `adafruit_displayio_sh1107` (OLED)

---

## Loopback Mode Use Case

**Scenario:** User has a hardware synth without built-in arpeggiation or scale quantization.

**Setup:**
1. Connect synth **MIDI OUT** → prisme **MIDI IN**
2. Connect prisme **MIDI OUT** → synth **MIDI IN**
3. Connect synth **AUDIO OUT** → Speakers/Interface
4. Enable Translation mode on prisme
5. Enable Arp + Scale layers

**Data Flow:**
```
Synth plays notes → MIDI OUT → prisme MIDI IN
                                    ↓
                    [Translation Layers Applied]
                                    ↓
                    prisme MIDI OUT → Synth MIDI IN
                                    ↓
                    Synth plays arpeggiated, quantized notes
```

**Result:** The synth now has arpeggiation and scale quantization without any DAW or external computer!

**Additional Uses:**
- Add swing to a rigid hardware sequencer
- Quantize an "out of tune" MIDI keyboard
- Transform MIDI from a DAW before it hits hardware

---

## Future Expansion Possibilities

### Translation Layers (Future)
- **Velocity Curve** (compress/expand velocity)
- **Note Delay** (humanization)
- **Chord Generator** (harmonize single notes)
- **MIDI FX** (transpose, channel filter, etc.)

### Hardware Expansion
- **Analog CV IN** (modulate tempo, swing, etc.)
- **Gate IN** (external clock/reset)
- **Expression Pedal Input** (real-time control)
- **Multiple CV Outputs** (use MCP4728 Channel C)

### Software Features
- **Preset System** (save/recall settings)
- **MIDI Learn** (assign CCs to parameters)
- **Pattern Sequencer** (step sequencer mode)
- **LFO/Modulation** (CV modulation sources)

---

## Related Documentation

- **Hardware Wiring:** `docs/hardware/MASTER_BREADBOARD_LAYOUT.md`
- **Pin Allocation:** `docs/hardware/PIN_ALLOCATION_MATRIX.md`
- **CV Standards:** `docs/hardware/MIDI_TO_CV_VOLTAGE_STANDARDS.md`
- **Software Architecture:** `docs/software/` (coming soon)
- **User Manual:** `docs/USER_GUIDE.md` (coming soon)

---

**Last Updated:** 2025-11-01
**Version:** 2.0 - Architecture Reframe ("prisme" MIDI/CV Translation Hub)
**Status:** Living Document - Update as system evolves
