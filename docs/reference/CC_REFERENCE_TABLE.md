# MIDI CC to CV Voltage Reference Table

**Purpose:** Maps all 128 MIDI CC numbers to their expected voltage polarity and behavior for accurate CV output.

**Last Updated:** 2025-11-01
**For:** prisme MIDI/CV Translation Hub

---

## Overview

When prisme outputs a MIDI CC as CV voltage, it needs to know:
1. **Polarity** - Unipolar (0-5V), Bipolar (±5V), or Binary (on/off)
2. **Behavior** - How the MIDI value maps to voltage
3. **Center Point** - For bipolar CCs, what value = 0V

This table provides the reference for all 128 MIDI CC numbers.

---

## Voltage Polarity Types

| Type | Voltage Range | MIDI Mapping | Example Use Cases |
|------|---------------|--------------|-------------------|
| **Unipolar** | 0-5V | 0 = 0V, 127 = 5V (linear) | Mod wheel, filter cutoff, volume |
| **Bipolar** | ±5V | 0 = -5V, 64 = 0V, 127 = +5V | Pan, detune, pitch offset |
| **Binary** | 0V or 5V | <64 = 0V, e64 = 5V (threshold) | Sustain pedal, portamento on/off |

---

## Complete CC Reference Table

### High Resolution Controllers (0-31)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 0 | Bank Select MSB | Unipolar | 0-5V | Linear | Not typically used for CV |
| 1 | Mod Wheel | Unipolar | 0-5V | Linear | Most common modulation source |
| 2 | Breath Controller | Unipolar | 0-5V | Linear | Wind instrument control |
| 3 | Undefined | Unipolar | 0-5V | Linear | Available for custom use |
| 4 | Foot Controller | Unipolar | 0-5V | Linear | Expression pedal |
| 5 | Portamento Time | Unipolar | 0-5V | Linear | Glide rate |
| 6 | Data Entry MSB | Unipolar | 0-5V | Linear | RPN/NRPN parameter |
| 7 | Channel Volume | Unipolar | 0-5V | Linear | Main volume control |
| 8 | Balance | Bipolar | ±5V | Center @ 64 | Left/right balance |
| 9 | Undefined | Unipolar | 0-5V | Linear | Available for custom use |
| 10 | Pan | Bipolar | ±5V | Center @ 64 | Stereo position |
| 11 | Expression | Unipolar | 0-5V | Linear | Secondary volume |
| 12 | Effect Control 1 | Unipolar | 0-5V | Linear | General purpose |
| 13 | Effect Control 2 | Unipolar | 0-5V | Linear | General purpose |
| 14-15 | Undefined | Unipolar | 0-5V | Linear | Available for custom use |
| 16-19 | General Purpose 1-4 | Unipolar | 0-5V | Linear | User-assignable |
| 20-31 | Undefined | Unipolar | 0-5V | Linear | Available for custom use |

### Low Resolution (LSB) Controllers (32-63)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 32-63 | LSB for CC 0-31 | Same as MSB | Same as MSB | Fine control | Rarely used, follow MSB polarity |

### Switch Controllers (64-69)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 64 | Sustain Pedal | Binary | 0V or 5V | <64 = 0V, e64 = 5V | Most common switch CC |
| 65 | Portamento On/Off | Binary | 0V or 5V | <64 = 0V, e64 = 5V | Enable glide |
| 66 | Sostenuto | Binary | 0V or 5V | <64 = 0V, e64 = 5V | Hold sustain pedal variant |
| 67 | Soft Pedal | Binary | 0V or 5V | <64 = 0V, e64 = 5V | Piano soft pedal |
| 68 | Legato Footswitch | Binary | 0V or 5V | <64 = 0V, e64 = 5V | Smooth note transitions |
| 69 | Hold 2 | Binary | 0V or 5V | <64 = 0V, e64 = 5V | Secondary sustain |

### Sound Controllers (70-79)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 70 | Sound Variation | Unipolar | 0-5V | Linear | Timbre/character |
| 71 | Resonance (Timbre) | Unipolar | 0-5V | Linear | Filter resonance/Q |
| 72 | Release Time | Unipolar | 0-5V | Linear | Envelope release |
| 73 | Attack Time | Unipolar | 0-5V | Linear | Envelope attack |
| 74 | Brightness (Cutoff) | Unipolar | 0-5V | Linear | **Most common filter cutoff CC** |
| 75 | Decay Time | Unipolar | 0-5V | Linear | Envelope decay |
| 76 | Vibrato Rate | Unipolar | 0-5V | Linear | LFO speed |
| 77 | Vibrato Depth | Unipolar | 0-5V | Linear | LFO amount |
| 78 | Vibrato Delay | Unipolar | 0-5V | Linear | LFO delay time |
| 79 | Sound Controller 10 | Unipolar | 0-5V | Linear | General purpose |

### General Purpose Controllers (80-83)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 80 | General Purpose 5 | Unipolar | 0-5V | Linear | User-assignable |
| 81 | General Purpose 6 | Unipolar | 0-5V | Linear | User-assignable |
| 82 | General Purpose 7 | Unipolar | 0-5V | Linear | User-assignable |
| 83 | General Purpose 8 | Unipolar | 0-5V | Linear | User-assignable |

### Effects Controllers (84-95)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 84 | Portamento Control | Unipolar | 0-5V | Linear | Glide source note |
| 85-90 | Undefined | Unipolar | 0-5V | Linear | Available for custom use |
| 91 | Reverb Send | Unipolar | 0-5V | Linear | Reverb amount |
| 92 | Tremolo Depth | Unipolar | 0-5V | Linear | Amplitude modulation |
| 93 | Chorus Send | Unipolar | 0-5V | Linear | Chorus amount |
| 94 | Detune Depth | Bipolar | ±5V | Center @ 64 | Pitch offset |
| 95 | Phaser Depth | Unipolar | 0-5V | Linear | Phaser amount |

### Data Increment/Decrement (96-97)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 96 | Data Increment | Unipolar | 0-5V | Linear | RPN/NRPN control |
| 97 | Data Decrement | Unipolar | 0-5V | Linear | RPN/NRPN control |

### Parameter Controllers (98-101)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 98 | NRPN LSB | Unipolar | 0-5V | Linear | Non-registered parameter |
| 99 | NRPN MSB | Unipolar | 0-5V | Linear | Non-registered parameter |
| 100 | RPN LSB | Unipolar | 0-5V | Linear | Registered parameter |
| 101 | RPN MSB | Unipolar | 0-5V | Linear | Registered parameter |

### Undefined Controllers (102-119)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 102-119 | Undefined | Unipolar | 0-5V | Linear | Available for custom use, default to unipolar |

### Channel Mode Messages (120-127)

| CC# | Name | Polarity | Range | Behavior | Notes |
|-----|------|----------|-------|----------|-------|
| 120 | All Sound Off | Binary | 0V or 5V | e64 = 5V pulse | Immediate silence |
| 121 | Reset All Controllers | Binary | 0V or 5V | e64 = 5V pulse | Reset to defaults |
| 122 | Local Control | Binary | 0V or 5V | <64 = 0V, e64 = 5V | Enable/disable local keyboard |
| 123 | All Notes Off | Binary | 0V or 5V | e64 = 5V pulse | Release all notes |
| 124 | Omni Mode Off | Binary | 0V or 5V | e64 = 5V pulse | Mono mode |
| 125 | Omni Mode On | Binary | 0V or 5V | e64 = 5V pulse | Poly mode |
| 126 | Mono Mode On | Binary | 0V or 5V | e64 = 5V pulse | Monophonic |
| 127 | Poly Mode On | Binary | 0V or 5V | e64 = 5V pulse | Polyphonic |

---

## Most Commonly Used CCs (for Quick Reference)

| CC# | Name | Typical Use | Polarity | Voltage Behavior |
|-----|------|-------------|----------|------------------|
| **1** | **Mod Wheel** | Vibrato, tremolo | Unipolar | 0 = 0V, 127 = 5V |
| **7** | **Volume** | Main volume control | Unipolar | 0 = 0V, 127 = 5V |
| **10** | **Pan** | Stereo position | **Bipolar** | **0 = -5V, 64 = 0V, 127 = +5V** |
| **11** | **Expression** | Secondary volume | Unipolar | 0 = 0V, 127 = 5V |
| **64** | **Sustain Pedal** | Hold notes | Binary | <64 = 0V, e64 = 5V |
| **71** | **Resonance** | Filter resonance/Q | Unipolar | 0 = 0V, 127 = 5V |
| **74** | **Filter Cutoff** | Brightness/timbre | Unipolar | 0 = 0V, 127 = 5V |
| **91** | **Reverb** | Reverb send amount | Unipolar | 0 = 0V, 127 = 5V |
| **93** | **Chorus** | Chorus send amount | Unipolar | 0 = 0V, 127 = 5V |

---

## Voltage Conversion Formulas

### Unipolar (0-5V)
```python
voltage = (cc_value / 127.0) * 5.0
# Example: CC value 64 ’ (64/127) * 5 = 2.52V
```

### Bipolar (±5V)
```python
voltage = ((cc_value - 64) / 64.0) * 5.0
# Example: CC value 0 ’ ((0-64)/64) * 5 = -5.0V
# Example: CC value 64 ’ ((64-64)/64) * 5 = 0.0V
# Example: CC value 127 ’ ((127-64)/64) * 5 = +4.92V
```

### Binary (0V or 5V)
```python
voltage = 5.0 if cc_value >= 64 else 0.0
# Example: CC value 0 ’ 0V
# Example: CC value 127 ’ 5V
```

---

## Implementation Notes

### Current Custom CC System
The current prisme Custom CC implementation (`arp/drivers/cv_gate.py:111-123`) uses **unipolar mapping only**:

```python
def cc_to_voltage(self, cc_value):
    """Convert MIDI CC value to voltage (0-5V unipolar)"""
    voltage = (cc_value / 127.0) * 5.0
    return max(0.0, min(5.0, voltage))
```

### Future Enhancement: Auto-Polarity Detection
To support bipolar CCs (like Pan CC#10), the system should:

1. **Lookup CC number** in this reference table
2. **Determine polarity** (unipolar/bipolar/binary)
3. **Apply correct voltage conversion** based on polarity

**Proposed Enhancement:**
```python
def cc_to_voltage_with_polarity(self, cc_number, cc_value):
    """Convert CC to voltage with auto-polarity detection"""
    # Lookup CC polarity from reference table
    polarity = CC_REFERENCE[cc_number]["polarity"]

    if polarity == "unipolar":
        return (cc_value / 127.0) * 5.0
    elif polarity == "bipolar":
        return ((cc_value - 64) / 64.0) * 5.0
    elif polarity == "binary":
        return 5.0 if cc_value >= 64 else 0.0
```

### Bipolar Output Requirement
**Hardware Limitation:** The MCP4728 DAC can only output **0-5V** (unipolar).

**To output bipolar (±5V):**
- Requires op-amp offset circuit (see `docs/hardware/CV_OPAMP_CIRCUIT.md`)
- Converts DAC 0-5V ’ ±5V output
- Circuit formula: `Vout = 2 × (Vin - 2.5V)`

**Current Status:** Bipolar CCs output as unipolar (0-5V) until op-amp circuit is added.

---

## Recommended Defaults for prisme

When user enables Custom CC output without specific configuration:

| Setting | Default Value | Reason |
|---------|---------------|--------|
| **CC Number** | 74 (Filter Cutoff) | Most universal modulation target |
| **Polarity** | Unipolar (0-5V) | Works with current hardware (no op-amp) |
| **Smoothing** | Low | Light smoothing prevents zipper noise |

---

## Related Documentation

- **Custom CC Implementation:** `docs/implementation/CUSTOM_CC_IMPLEMENTATION_PLAN.md`
- **Voltage Standards:** `docs/hardware/MIDI_TO_CV_VOLTAGE_STANDARDS.md`
- **Op-Amp Circuit:** `docs/hardware/CV_OPAMP_CIRCUIT.md`
- **MIDI CC Names:** `arp/data/midi_cc_names.py`

---

**Last Updated:** 2025-11-01
**Status:** Reference Document
**Maintainer:** Update when adding new CC support or voltage conversion methods
