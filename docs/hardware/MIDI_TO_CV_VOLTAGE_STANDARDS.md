# MIDI to CV Voltage Standards - Complete Reference

**Created:** 2025-11-01
**Purpose:** Comprehensive reference for MIDI to CV conversion voltage standards
**Scope:** Industry standards, manufacturer implementations, practical guidelines

---

## Executive Summary

This document provides definitive voltage conversion standards for MIDI to CV applications in Eurorack and modular synthesis. Use this as the **single source of truth** when implementing MIDI to CV conversion.

**Quick Reference:**
- **MIDI CC (0-127)**: 0-10V unipolar (standard) OR ±5V bipolar (advanced)
- **Pitch Bend**: ±5V bipolar, centered at 0V (14-bit resolution)
- **Aftertouch/Pressure**: 0-5V unipolar OR ±5V bipolar (manufacturer-dependent)
- **LFO Outputs**: ±5V bipolar (standard for modulation)
- **Gate/Trigger**: 0-5V or 0-10V (unipolar positive)

---

## Table of Contents

1. [MIDI CC to CV Conversion](#midi-cc-to-cv-conversion)
2. [Pitch Bend Conversion](#pitch-bend-conversion)
3. [Aftertouch/Channel Pressure](#aftertouchchannel-pressure)
4. [LFO Voltage Standards](#lfo-voltage-standards)
5. [Velocity Conversion](#velocity-conversion)
6. [Manufacturer Implementations](#manufacturer-implementations)
7. [Hardware Requirements](#hardware-requirements)
8. [Conversion Formulas](#conversion-formulas)
9. [Practical Implementation Guide](#practical-implementation-guide)

---

## MIDI CC to CV Conversion

### Standard: Unipolar 0-10V

**Most Common Implementation:**
- **MIDI Range:** 0-127 (7-bit)
- **Voltage Range:** 0-10V (unipolar positive)
- **Formula:** `voltage = (cc_value / 127) * 10.0`
- **Step Size:** ~0.0787V per MIDI value

**Example Implementation (Applied Acoustics Multiphonics CV-1):**
- MIDI CC 0 → 0.0V
- MIDI CC 64 → 5.04V (midpoint)
- MIDI CC 127 → 10.0V

**Use Cases:**
- Filter cutoff modulation
- Resonance control
- Pulse width modulation
- Any unidirectional parameter control

### Alternative: Bipolar ±5V

**Advanced Implementation:**
- **MIDI Range:** 0-127
- **Voltage Range:** -5V to +5V (bipolar)
- **Formula:** `voltage = ((cc_value - 64) / 63.5) * 5.0`
- **Center Point:** MIDI CC 64 = 0V

**Why Bipolar?**
- Symmetrical modulation around current parameter value
- Additive patching without rebalancing
- More intuitive for bidirectional modulation

**Example:**
- MIDI CC 0 → -5.0V
- MIDI CC 64 → 0.0V (neutral/no modulation)
- MIDI CC 127 → +5.0V

### 0-5V Compact Range (Less Common)

**Cherry Audio Implementation:**
- **MIDI Range:** 0-127
- **Voltage Range:** 0-5V
- **Formula:** `voltage = (cc_value / 127) * 5.0`

**Use Cases:**
- Compact 5V systems
- Digital CV inputs (0-5V only)
- Lower voltage modular systems

---

## Pitch Bend Conversion

### Standard: Bipolar ±5V (or ±2 semitones)

**MIDI Specification:**
- **Resolution:** 14-bit (0-16383)
- **Center Point:** 8192 = no pitch bend
- **Range:** 0-8191 = bend down, 8193-16383 = bend up
- **Default Range:** ±2 semitones (configurable)

**Voltage Conversion (1V/octave standard):**
- **Voltage Range:** Typically ±0.167V for ±2 semitones
- **Formula:** `voltage = ((bend_value - 8192) / 8192) * bend_range_volts`
- **Center:** 0V = no pitch bend

**Example (±2 semitones = ±0.167V):**
- Bend Value 0 → -0.167V (2 semitones down)
- Bend Value 8192 → 0.0V (no bend)
- Bend Value 16383 → +0.167V (2 semitones up)

**Configurable Ranges:**
- ±2 semitones: ±0.167V (default)
- ±12 semitones (1 octave): ±1.0V
- ±24 semitones (2 octaves): ±2.0V
- ±48 semitones (4 octaves): ±4.0V (Kenton Pro CV)

**Key Points:**
- **Always bipolar** (pitch can bend up or down)
- **Always centered at 0V**
- **Additive with base pitch CV** (voltages sum)
- **High resolution** (14-bit vs 7-bit for CC)

---

## Aftertouch/Channel Pressure

### Two Standard Implementations

#### Implementation A: Bipolar ±5V (Applied Acoustics)

- **MIDI Range:** 0-127
- **Voltage Range:** -5V to +5V
- **Formula:** `voltage = ((pressure - 64) / 63.5) * 5.0`
- **Center:** MIDI 64 = 0V

**Advantages:**
- Symmetrical modulation (add/subtract from parameter)
- No patch rebalancing needed
- Intuitive for additive modulation

#### Implementation B: Unipolar 0-5V (Cherry Audio)

- **MIDI Range:** 0-127
- **Voltage Range:** 0-5V
- **Formula:** `voltage = (pressure / 127) * 5.0`

**Advantages:**
- Simple unidirectional modulation
- Matches velocity-style behavior
- Compatible with unipolar-only inputs

### Recommendation

**For additive modulation:** Use bipolar ±5V (like Applied Acoustics)
**For direct parameter control:** Use unipolar 0-5V

---

## LFO Voltage Standards

### Standard: Bipolar ±5V

**Why LFOs Must Be Bipolar:**

1. **Symmetrical Modulation**
   - Oscillates equally above and below center point
   - Creates natural vibrato, tremolo, filter sweeps
   - Example: 0V pitch + ±5V LFO = pitch oscillates symmetrically

2. **Voltage Additivity**
   - LFO voltage adds to parameter's base voltage
   - Negative LFO values lower the parameter
   - Positive LFO values raise the parameter
   - Result: Bidirectional modulation around current setting

3. **Unipolar LFO Problem**
   - 0-5V unipolar LFO only modulates upward
   - Creates asymmetric modulation (parameter only increases)
   - Requires offset/attenuverter to center the waveform

**Standard LFO Voltage Range:**
- **Triangle/Sine:** -5V to +5V (smooth bipolar)
- **Square:** -5V or +5V (hard switching)
- **Saw:** -5V to +5V (ramp up or down)

**Example: Filter Cutoff Modulation**
```
Filter Cutoff CV: 2V (base setting)
LFO Output: -5V to +5V (triangle wave)
Result: Filter sweeps from -3V to +7V
```

### Special Cases: Unipolar LFO

**When Unipolar Is Used:**
- Digital CV inputs (can't accept negative voltage)
- Gate/trigger generation (0V = off, 5V = on)
- Envelope followers (0V = silence, 5V = maximum)

**Converting Bipolar to Unipolar:**
```
unipolar_voltage = (bipolar_voltage + 5.0) / 2.0
// Example: -5V to +5V → 0V to 5V
```

**Converting Unipolar to Bipolar:**
```
bipolar_voltage = (unipolar_voltage * 2.0) - 5.0
// Example: 0V to 5V → -5V to +5V
```

---

## Velocity Conversion

### Two Philosophies

#### Traditional: Unipolar 0-5V

- **MIDI Range:** 0-127 (note: 0 = note off)
- **Voltage Range:** 0-5V
- **Formula:** `voltage = (velocity / 127) * 5.0`
- **Logic:** Harder hit = higher voltage

**Use Cases:**
- VCA control (0V = silent, 5V = loud)
- Envelope intensity scaling
- Traditional synthesizer behavior

#### Modern: Bipolar ±5V (Applied Acoustics Philosophy)

- **MIDI Range:** 1-127 (practical playing range)
- **Voltage Range:** -5V to +5V
- **Formula:** `voltage = ((velocity - 64) / 63.5) * 5.0`
- **Center:** MIDI velocity 64 = 0V

**Why Bipolar Velocity?**

Quote from Applied Acoustics documentation:
> "In many modular synths, velocity is unipolar with MIDI velocity 1 at 0V. This is annoying when adding velocity modulation to an existing patch since we almost never play notes at velocity 1, so the velocity output is always too high and the patch must be re-balanced. With bipolar output, MIDI velocity 64 is at 0V. Playing at medium volume has minimal impact on the patch, playing louder results in positive modulation, playing softer results in negative modulation. You can try adding velocity modulation anywhere without breaking everything."

**Practical Example:**
- Soft hit (velocity 32): -2.5V → reduces filter cutoff
- Medium hit (velocity 64): 0V → no change to filter
- Hard hit (velocity 96): +2.5V → increases filter cutoff

---

## Manufacturer Implementations

### Expert Sleepers (FH-2, General CV)

**Voltage Ranges:**
- Software-selectable: ±5V, 0-10V, or 0-1V per output
- Maximum output: ±8V (16V peak-to-peak)
- Input ranges: Bipolar ±5V, Unipolar 0-5V

**Philosophy:**
- Maximum flexibility through software configuration
- Each output individually configurable
- Supports both modern and legacy voltage standards

**Key Products:**
- **FH-2 Factotum:** 8 configurable outputs, bidirectional MIDI/CV
- **General CV:** 9 inputs (digital, unipolar, bipolar), ±8V outputs
- **CVM-8:** ±10.24V range, 16-bit ADC

### Doepfer (A-190-3)

**Voltage Ranges:**
- Pitch CV: 0-5V (1V/octave)
- Gate: +5V or +12V (jumper selectable)
- Velocity: 0-5V (unipolar)
- CC: 0-5V (unipolar)

**Philosophy:**
- Simple, fixed output assignments
- Minimal configuration (jumpers only)
- Straightforward MIDI-to-CV translation

**Key Feature:**
- Assignable CC output (choose any CC number)
- Direct 1V/octave implementation
- No menu diving required

### Kenton Electronics (Pro CV to MIDI)

**Voltage Ranges:**
- Input: -3V to +10.65V (wide range for legacy gear)
- Pitch Bend Range: ±48 semitones configurable
- 16-bit ADC conversion

**Philosophy:**
- Support multiple pitch standards (1V/Oct, Hz/V, 1.2V/Oct)
- Intelligent learn mode for calibration
- Wide voltage acceptance for vintage equipment

**Key Features:**
- Adaptive CV scaling (auto-detects 1V/Oct vs Hz/V)
- Aux inputs for custom CC mapping
- Comprehensive voltage range support

### Intellijel (MIDI 1U + CVx Expanders)

**Voltage Ranges:**
- Pitch: ±5V (1V/octave)
- Clock: 0-5V or ±5V (user configurable)
- CVx outputs: Fully programmable voltage ranges

**Philosophy:**
- Modular expansion (add CVx modules as needed)
- Software configuration via Intellijel Config app
- Up to 32 assignable outputs (4× CVx expanders)

**Key Features:**
- Polarity assignment (unipolar vs bipolar per output)
- 10 synths × 10 MIDI channels supported
- Compact 1U form factor

### Polyend (Poly 2)

**Voltage Ranges:**
- Gate: 0-5V or 0-10V
- Pitch: 0-10V (V/Oct, Hz/V, or Buchla 1.2V/Oct)
- CV outputs: Configurable 0-5V, 0-10V, ±5V

**Philosophy:**
- Multiple pitch standards support
- Factory calibration for precision
- Configurable output ranges

**Technical Specs:**
- 12-bit DAC (4096 steps)
- Accuracy: 2.5mV to 5mV (calibrated outputs)
- 20 configurable outputs total

---

## Hardware Requirements

### For MCP4728 DAC (0-5V native output)

**Native Capabilities:**
- **Maximum Voltage:** 5V (with VDD reference)
- **Resolution:** 12-bit (4096 steps = 1.22mV per step)
- **Channels:** 4 independent outputs

**Voltage Ranges Achievable (Direct Output):**
- ✅ 0-5V unipolar (native)
- ✅ MIDI CC → 0-5V
- ✅ Velocity → 0-5V
- ✅ Aftertouch → 0-5V
- ❌ 0-10V (requires op-amp)
- ❌ ±5V bipolar (requires op-amp with bipolar supply)
- ❌ LFO ±5V (requires op-amp with bipolar supply)

### To Achieve 0-10V Output (Unipolar)

**Hardware Needed:**
- Op-amp (LM358N, TL072, etc.)
- 2× gain configuration
- 12V power supply (for op-amp headroom)

**Circuit:**
```
MCP4728 (0-5V) → Op-amp (2× gain) → Output (0-10V)
```

**Achievable:**
- ✅ 0-10V unipolar
- ✅ MIDI CC → 0-10V
- ❌ Still can't do bipolar (no negative supply)

### To Achieve ±5V Bipolar Output

**Hardware Needed:**
- Op-amp with dual supply (TL072, OPA2134, etc.)
- ±12V power supply (or ±5V minimum)
- Offset/summing circuit
- Reference voltage (2.5V for offset)

**Circuit Options:**

**Option A: Offset + Amplify**
```
MCP4728 (0-5V) → Offset (-2.5V) → Op-amp → ±5V bipolar
```

**Option B: Differential Amplifier**
```
MCP4728 Ch1 (0-5V) → \
                      Diff Amp → ±5V bipolar
MCP4728 Ch2 (inverted) → /
```

**Achievable:**
- ✅ ±5V bipolar
- ✅ LFO modulation
- ✅ Bipolar CC/velocity/aftertouch
- ✅ Symmetrical pitch bend

### For Our Project (Current Capabilities)

**Available:**
- MCP4728 DAC (4 channels, 0-5V each)
- 5V power supply (PowerBoost 1000C)

**Can Do (No Additional Hardware):**
- ✅ MIDI CC → 0-5V (Channels C or D)
- ✅ Pitch CV → 0-5V (Channel A - currently used)
- ✅ Gate → 0-5V (Channel B or software-selected)

**Need Op-amp + 12V for:**
- ❌ 0-10V unipolar (CC, velocity, etc.)
- ❌ ±5V bipolar (LFO, bipolar modulation)

**Recommendation for Custom CC Jack:**
- **Phase 1:** Use 0-5V output (MCP4728 direct) → Works with most modules
- **Phase 2:** Add op-amp + 12V rail → Unlock 0-10V and ±5V capabilities

---

## Conversion Formulas

### MIDI CC (0-127) → Voltage

**To 0-5V (Direct MCP4728):**
```python
def cc_to_voltage_5v(cc_value):
    """Convert MIDI CC to 0-5V"""
    return (cc_value / 127.0) * 5.0
```

**To 0-10V (With 2× Op-Amp):**
```python
def cc_to_voltage_10v(cc_value):
    """Convert MIDI CC to 0-10V"""
    return (cc_value / 127.0) * 10.0
```

**To ±5V Bipolar (With Op-Amp + Bipolar Supply):**
```python
def cc_to_voltage_bipolar(cc_value):
    """Convert MIDI CC to ±5V (centered at CC 64)"""
    return ((cc_value - 64) / 63.5) * 5.0
```

### Pitch Bend (0-16383) → Voltage

**Standard ±2 Semitones:**
```python
def pitch_bend_to_voltage(bend_value, bend_range_semitones=2):
    """
    Convert 14-bit pitch bend to voltage

    Args:
        bend_value: 0-16383 (8192 = center)
        bend_range_semitones: ±semitones (default ±2)

    Returns:
        Voltage (bipolar, centered at 0V)
    """
    # Normalize to -1.0 to +1.0
    normalized = (bend_value - 8192) / 8192.0

    # Convert semitones to volts (1V/octave standard)
    volts_per_octave = 1.0
    bend_range_volts = (bend_range_semitones / 12.0) * volts_per_octave

    return normalized * bend_range_volts
```

**Example:**
- Bend Value 0 (max down): -0.167V (-2 semitones)
- Bend Value 8192 (center): 0.0V
- Bend Value 16383 (max up): +0.167V (+2 semitones)

### Aftertouch/Pressure (0-127) → Voltage

**Unipolar 0-5V:**
```python
def aftertouch_to_voltage_unipolar(pressure):
    """Convert MIDI aftertouch to 0-5V"""
    return (pressure / 127.0) * 5.0
```

**Bipolar ±5V:**
```python
def aftertouch_to_voltage_bipolar(pressure):
    """Convert MIDI aftertouch to ±5V (centered at pressure 64)"""
    return ((pressure - 64) / 63.5) * 5.0
```

### Voltage → DAC Value (MCP4728)

**For 0-5V Output:**
```python
def voltage_to_dac(voltage, vref=5.0, max_value=4095):
    """
    Convert voltage to 12-bit DAC value

    Args:
        voltage: 0.0 to vref (5.0V for MCP4728)
        vref: Reference voltage (5.0V)
        max_value: 12-bit max (4095)

    Returns:
        DAC value (0-4095)
    """
    dac_value = int((voltage / vref) * max_value)
    return max(0, min(max_value, dac_value))  # Clamp to valid range
```

**Example:**
- 0.0V → DAC 0
- 2.5V → DAC 2048 (midpoint)
- 5.0V → DAC 4095 (maximum)

---

## Practical Implementation Guide

### Design Decision: Unipolar vs Bipolar

**Choose Unipolar 0-5V or 0-10V When:**
- Parameter is inherently unidirectional (filter cutoff, resonance)
- Voltage represents an absolute value (not modulation)
- Target modules expect positive-only CV
- Simpler hardware (no bipolar power supply needed)

**Choose Bipolar ±5V When:**
- Modulation source (LFO, envelope, aftertouch as modulation)
- Parameter should modulate around current setting
- Additive patching is desired (voltage summing)
- Need symmetrical modulation (pitch bend, vibrato)

### Implementation Steps for Custom CC Output

**Phase 1: Basic (0-5V with MCP4728)**

1. **Use MCP4728 Channel D** (available)
2. **Output Range:** 0-5V (direct DAC output)
3. **MIDI Sources:** CC, Aftertouch, Velocity (all unipolar)
4. **Hardware:** None needed (use existing DAC)

**Code Example:**
```python
def set_custom_cc(self, cc_value):
    """Send MIDI CC value to Custom CC jack (0-5V)"""
    voltage = (cc_value / 127.0) * 5.0
    dac_value = int((voltage / 5.0) * 4095)
    self.dac.channel_d.value = dac_value
```

**Phase 2: Extended (0-10V with Op-Amp)**

1. **Add op-amp circuit** (2× gain, single supply)
2. **Power:** Add 12V rail (LM7805 or PowerBoost with buck converter)
3. **Output Range:** 0-10V
4. **Benefits:** Industry-standard CC voltage range

**Circuit:**
```
MCP4728 Ch D (0-5V) → LM358N (2× gain) → Custom CC Jack (0-10V)
```

**Phase 3: Advanced (±5V Bipolar with Dual Supply)**

1. **Add bipolar power supply** (±12V or ±5V)
2. **Op-amp circuit:** Offset + differential amplifier
3. **Output Range:** ±5V (bipolar)
4. **Benefits:** LFO generation, symmetrical modulation

**Circuit:**
```
MCP4728 → Offset (-2.5V ref) → Op-amp → ±5V bipolar
```

### Menu Design for Custom CC Selection

**Hierarchy:**
```
Settings > CV Output > Custom CC Source
  ├─ MIDI CC (0-127)
  │   └─ Select CC Number (0-127)
  ├─ Pitch Bend
  ├─ Aftertouch
  └─ Disabled
```

**Implementation:**
```python
# In settings
CC_SOURCE_DISABLED = 0
CC_SOURCE_MIDI_CC = 1
CC_SOURCE_PITCH_BEND = 2
CC_SOURCE_AFTERTOUCH = 3

custom_cc_source = CC_SOURCE_DISABLED
custom_cc_number = 1  # If MIDI CC selected, which CC?
```

### Voltage Range Documentation for Users

**Label on Hardware:**
```
CUSTOM CC
0-5V
(0-10V with mod)
```

**User Manual Entry:**
```
Custom CC Jack - Voltage Range
- Stock Configuration: 0-5V (unipolar)
- Hardware Mod: 0-10V (with op-amp upgrade)
- Compatible: Most Eurorack CV inputs

Maps selected MIDI message to CV:
- MIDI CC 0-127 → 0-5V (or 0-10V)
- Pitch Bend → 0-5V centered (or ±2.5V with mod)
- Aftertouch → 0-5V (or 0-10V)
```

---

## Appendix A: Complete MIDI CC List

### Standard MIDI CC Assignments (0-127)

**High-Resolution Controllers (0-31) + LSB (32-63):**

| CC# | Name | Typical Use | Voltage Type |
|-----|------|-------------|--------------|
| 0 | Bank Select MSB | Patch selection | N/A (discrete) |
| 1 | **Modulation Wheel** | Vibrato, tremolo | 0-5V or 0-10V |
| 2 | Breath Controller | Wind synth expression | 0-5V or 0-10V |
| 4 | Foot Controller | Pedal control | 0-5V or 0-10V |
| 5 | Portamento Time | Glide rate | 0-5V |
| 7 | **Channel Volume** | Master volume | 0-5V or 0-10V |
| 10 | **Pan** | Stereo position | ±5V bipolar |
| 11 | **Expression** | Dynamic control | 0-5V or 0-10V |

**Single-Byte Controllers (64-127):**

| CC# | Name | Typical Use | Voltage Type |
|-----|------|-------------|--------------|
| 64 | **Sustain Pedal** | Hold notes | Gate (0V/5V) |
| 65 | Portamento On/Off | Enable glide | Gate (0V/5V) |
| 71 | **Resonance** | Filter resonance | 0-5V or 0-10V |
| 74 | **Brightness/Cutoff** | Filter cutoff | 0-5V or 0-10V |

**Undefined CCs (Available for Custom Use):**
- CC 3, 9, 14-15, 20-31, 85-87, 89-90, 102-119

**Recommendation:**
Use undefined CCs for custom parameters to avoid conflicts with standard controllers.

---

## Appendix B: Voltage Range Quick Reference Table

| MIDI Message | Standard Range | Alternative Range | Hardware Needed |
|--------------|----------------|-------------------|-----------------|
| **CC (0-127)** | 0-10V unipolar | ±5V bipolar | Op-amp + 12V |
| **Pitch Bend** | ±0.167V (±2 semi) | ±1V to ±4V | Bipolar supply |
| **Aftertouch** | 0-5V unipolar | ±5V bipolar | Bipolar supply |
| **Velocity** | 0-5V unipolar | ±5V bipolar | Bipolar supply |
| **LFO** | ±5V bipolar | 0-10V unipolar | Bipolar supply |
| **Gate/Trigger** | 0-5V or 0-10V | 5V S-Trig | Transistor circuit |

---

## Appendix C: Op-Amp Circuits

### 2× Gain (0-5V → 0-10V)

**Single Supply Configuration:**
```
       R2 (10kΩ)
        |
In ----R1(10kΩ)---+--- Op-Amp (+)
                  |
                  +--- Op-Amp (-)
                  |
                  +--- Out (0-10V)

Op-Amp (+) to Vref (5V) via 10kΩ
Op-Amp (-) to Out via 10kΩ (feedback)
Supply: +12V, GND
```

### Bipolar Offset (0-5V → ±5V)

**Dual Supply Configuration:**
```
In (0-5V) → Offset (-2.5V) → ±2.5V → Gain (2×) → ±5V

Supply: +12V, -12V, GND
Reference: 2.5V (voltage divider or precision ref)
```

---

## References & Sources

- Applied Acoustics Systems Multiphonics CV-1 Manual
- Expert Sleepers FH-2 User Manual (v1.18)
- Kenton Electronics Pro CV to MIDI Documentation
- Doepfer A-190-3 Specifications
- Intellijel MIDI 1U Manual
- Polyend Poly 2 User Manual
- Perfect Circuit: "MIDI to CV Conversion Guide"
- Control Voltage: "LFO Variables and Destinations"
- MIDI Specification 1.0 (MIDI Manufacturers Association)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-01
**Maintained By:** Arpeggiator Project Team

**END OF REFERENCE**
