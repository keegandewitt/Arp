# Wiring Color Convention

**Project Standard:** Consistent color coding for all audio/CV connections

**Date Established:** 2025-11-02

---

## Standard Color Code

### TS (Tip-Sleeve) Mono Jacks

**All CV/Gate outputs use this standard:**

| Color | Connection | Purpose |
|-------|------------|---------|
| **RED** | **TIP** | Signal (hot) - CV voltage or gate signal |
| **WHITE** | **SLEEVE** | Ground (return) - common reference |

```
TS Jack (Mono):

    ┌─── TIP (signal)    → RED wire
    │
    │
    └─── SLEEVE (ground) → WHITE wire
```

### Why This Convention?

- **Red = Hot/Signal** - Universal standard in audio/electronics
- **White = Ground** - Cleaner appearance than black, easy to see
- **Consistency** - Same colors across all outputs
- **Debugging** - Easy to trace connections on breadboard
- **Documentation** - Photos/diagrams are clearer

---

## Application to prisme Outputs

### CV Pitch Output (MCP4728 Channel A)
```
MCP4728 VOUTA (Channel A) → RED wire   → Jack TIP
MCP4728 GND               → WHITE wire → Jack SLEEVE
```

### V-Trig Gate Output (MCP4728 Channel C)
```
MCP4728 VOUTC (Channel C) → RED wire   → Jack TIP
MCP4728 GND               → WHITE wire → Jack SLEEVE
```

### Custom CC Output (MCP4728 Channel D)
```
MCP4728 VOUTD (Channel D) → RED wire   → Jack TIP
MCP4728 GND               → WHITE wire → Jack SLEEVE
```

### S-Trig Output (GPIO D10 + Transistor)
```
Transistor COLLECTOR → RED wire   → Jack TIP
Common Ground        → WHITE wire → Jack SLEEVE
```

---

## For TRS (Tip-Ring-Sleeve) Stereo Jacks

**If used in future (not currently planned):**

| Color | Connection | Purpose |
|-------|------------|---------|
| **RED** | **TIP** | Signal 1 (Left channel or positive) |
| **WHITE** | **RING** | Signal 2 (Right channel or negative) |
| **BLACK** | **SLEEVE** | Ground (common reference) |

```
TRS Jack (Stereo):

    ┌─── TIP          → RED wire
    │
    ├─── RING         → WHITE wire
    │
    └─── SLEEVE       → BLACK wire
```

**Note:** TRS jacks are NOT currently used in prisme. All outputs are mono (TS).

---

## Special Cases

### LM358N Op-Amp Circuit (0-10V CV)
```
MCP4728 Channel A → LM358N input (internal wiring)
LM358N Pin 1 OUT  → RED wire   → Jack TIP (0-10V)
Common Ground     → WHITE wire → Jack SLEEVE
```

### MIDI Connections (If TRS MIDI Used)
```
MIDI over TRS Type A standard:
  Tip (RED)   → Current Source
  Ring (WHITE) → Current Sink
  Sleeve (BLACK) → Ground/Shield

Note: prisme uses DIN-5 MIDI, not TRS MIDI
```

---

## Wire Gauge Recommendations

| Application | Wire Gauge | Type |
|-------------|------------|------|
| CV/Gate signals | 22-24 AWG | Solid core (breadboard) |
| CV/Gate signals | 22-24 AWG | Stranded (soldered) |
| MIDI signals | 24-26 AWG | Stranded |
| Power (5V/12V) | 20-22 AWG | Stranded |
| I2C bus | 22-24 AWG | Solid core |

---

## Labeling Standards

**Physical Labels:**
- Use white electrical tape or label maker
- Format: `[Signal Name] - [Pin]`
- Examples:
  - "CV PITCH - MCP CH-A"
  - "V-TRIG GATE - MCP CH-C"
  - "S-TRIG - D10"
  - "GND - WHITE"

**Breadboard Organization:**
- **Top rail:** +5V (red wire from power)
- **Bottom rail:** GND (white wire, common ground)
- Signal wires: Red for hot, white for return

---

## Continuity Testing Color Reference

**When checking connections with multimeter:**

✅ **Correct connections:**
```
MCP4728 VOUTA ←→ Jack TIP (RED wire should beep)
MCP4728 GND   ←→ Jack SLEEVE (WHITE wire should beep)
```

❌ **Should NOT beep (open circuit):**
```
Jack TIP ←→ Jack SLEEVE (red to white should be open)
```

---

## Migration from Previous Black Ground Convention

**Old convention (used in some docs):**
- Red = Tip (signal)
- **Black** = Sleeve (ground)

**New convention (current standard):**
- Red = Tip (signal)
- **White** = Sleeve (ground)

**Action items:**
- Update all wiring guides to use WHITE for ground
- Update test procedures to reference WHITE wires
- Photos/diagrams should show white ground wires

---

## Quick Reference Card

```
┌─────────────────────────────────────┐
│   prisme WIRING COLOR CONVENTION    │
├─────────────────────────────────────┤
│                                     │
│  TS Mono Jacks (CV/Gate):          │
│    🔴 RED   = TIP (signal)          │
│    ⚪ WHITE = SLEEVE (ground)       │
│                                     │
│  Common Ground:                     │
│    All WHITE wires connect to       │
│    common ground rail               │
│                                     │
│  Never Mix:                         │
│    ❌ Red-to-White = SHORT          │
│    ✅ Always verify with multimeter │
│                                     │
└─────────────────────────────────────┘
```

---

## Exceptions & Notes

1. **Power wiring:** May use red (+) and black (-) for clarity
2. **Existing breadboards:** Can have black grounds until rewired
3. **Commercial cables:** Often use black for sleeve (that's OK for external cables)
4. **Internal wiring:** MUST follow RED/WHITE convention

---

**Status:** ACTIVE STANDARD as of 2025-11-02

All new wiring must follow this convention.
All documentation updates should reference RED/WHITE colors.

---

**Approved by:** Project team
**Last Updated:** 2025-11-02
