# CV/Gate Output Integration Guide
## Hardware Specifications & Enclosure Integration

---

## Overview

This guide covers the hardware integration of CV Pitch and Gate outputs for the MIDI Arpeggiator, using the MCP4728 Quad DAC and 3.5mm TRS panel-mount jacks.

---

## Jack Specifications

### Recommended Part: **Thonkiconn PJ301M-12**

**Why Thonkiconn PJ301M-12?**
- Industry standard for Eurorack and modular synth DIY
- Reliable mechanical construction
- Proper dimensions for 3.5mm (1/8") cables
- Isolated sleeve (prevents ground loops)
- Affordable (~$1.25 each)

**Specifications:**
- **Type:** 3.5mm TRS (stereo) panel-mount jack
- **Contacts:** Tip, Ring, Sleeve (switched)
- **Panel Hole:** 6mm (0.236") diameter
- **Mounting:** Threaded bushing with nut
- **Material:** Plastic body with metal contacts
- **Insulation:** Isolated sleeve terminal

**Alternative Options (if Thonkiconn unavailable):**
- Switchcraft 35RAPC4BH (~$3.50) - Premium quality
- Lumberg/Rean NYS226 (~$1.50) - Good quality
- Qingpu WQP-PJ301M-12 (~$0.80) - Budget clone

---

## Wiring Configuration

### TRS Jack Wiring for Mono CV/Gate Signals

Even though CV and Gate are **mono signals**, we use **TRS jacks** for compatibility and reliability.

**Standard Wiring (per jack):**
```
TIP (T)     ──→  Signal wire from MCP4728 DAC output
RING (R)    ──→  Connect to SLEEVE (tie to ground) *
SLEEVE (S)  ──→  Ground (common GND)

* Critical: Ring MUST be tied to Sleeve for TS cable compatibility
```

**Why tie Ring to Sleeve?**
- Ensures compatibility with both TS (mono) and TRS (stereo) cables
- Prevents floating/open Ring terminal (which can cause noise)
- Standard practice in modular synth world

---

## MCP4728 DAC Channel Assignment

The MCP4728 has 4 channels (A, B, C, D). We're using 2 for CV/Gate:

| DAC Channel | Output Function | Jack Label | Voltage Range | Purpose |
|-------------|----------------|------------|---------------|---------|
| **Channel A** | CV Pitch | "CV PITCH" or "CV" | 0-5V | 1V/octave pitch control |
| **Channel B** | Gate/Trigger | "GATE" or "TRIG" | 0V or 5V | Note on/off (gate mode) |
| Channel C | (Reserved) | - | - | Future expansion |
| Channel D | (Reserved) | - | - | Future expansion |

**Polarity Settings:**
- V-trig (standard): 0V = off, 5V = on
- S-trig (Moog vintage): 5V = off, 0V = on (inverted in software)

---

## Wiring Diagram

```
MCP4728 Quad DAC Breakout
┌─────────────────────────┐
│  VCC ──→ 5V (Boost)     │
│  GND ──→ Common GND     │
│  SCL ──→ M4 SCL         │
│  SDA ──→ M4 SDA         │
│                         │
│  OUT A ─────────────────┼──→ Wire 1
│  OUT B ─────────────────┼──→ Wire 2
│  OUT C (unused)         │
│  OUT D (unused)         │
└─────────────────────────┘
           │
           ↓
   Wire 1 & 2 go to rear panel jacks

Rear Panel - CV/Gate Jacks
┌──────────────────────────────────┐
│  Jack 1: CV PITCH                │
│  ┌─────┐                         │
│  │ T ──── Wire 1 (DAC OUT A)     │
│  │ R ──┐                         │
│  │ S ──┴─ Common GND             │
│  └─────┘                         │
│                                  │
│  Jack 2: GATE                    │
│  ┌─────┐                         │
│  │ T ──── Wire 2 (DAC OUT B)     │
│  │ R ──┐                         │
│  │ S ──┴─ Common GND             │
│  └─────┘                         │
└──────────────────────────────────┘

Note: Ring (R) and Sleeve (S) are soldered together
      on EACH jack for TS/TRS cable compatibility
```

---

## Physical Integration into Enclosure

### Rear Panel Layout

**Suggested arrangement (left to right):**
```
┌────────────────────────────────────────────┐
│  [MIDI IN]  [MIDI OUT]    [CV]    [GATE]  │
│    DIN-5      DIN-5       3.5mm   3.5mm   │
└────────────────────────────────────────────┘
```

**Note:** All jacks are mounted on the rear panel for a cleaner front appearance and consolidated I/O.

**Dimensions:**
- **DIN-5 MIDI jacks:** 14mm mounting holes, ~25mm center-to-center spacing
- **3.5mm CV/Gate jacks:** 6mm mounting holes, ~15mm center-to-center spacing
- **Minimum edge clearance:** 10mm from panel edge to jack center

### Panel Hole Specifications

| Component | Hole Diameter | Tolerance | Notes |
|-----------|---------------|-----------|-------|
| DIN-5 MIDI Jack | 14mm | ±0.2mm | Snug fit, secured with nut |
| 3.5mm TRS Jack | 6mm | ±0.2mm | Threaded bushing with nut |
| USB-C Cutout (rear) | 9mm × 4mm | +0.5mm | Rectangular cutout, allow cable clearance |
| Slide Switch (side) | See `805 slide switch.f3d` | - | Reference CAD model for exact dimensions |

---

## Assembly Instructions

### Step 1: Prepare TRS Jacks (× 2)

**For each jack:**
1. **Identify terminals:**
   - Tip: Usually longest lug
   - Ring: Middle lug
   - Sleeve: Shortest lug (or threaded body if isolated)

2. **Solder Ring to Sleeve:**
   - Cut a short piece of bare wire (~10mm)
   - Solder one end to Ring terminal
   - Solder other end to Sleeve terminal
   - Use heat shrink to insulate the connection
   - **Critical:** This must be done on BOTH jacks

3. **Prepare signal wire:**
   - Cut 22-24 AWG stranded wire (~6-8 inches)
   - Strip 3mm from one end
   - Tin the wire end with solder
   - Solder to Tip terminal

4. **Prepare ground wire:**
   - Cut 22-24 AWG black wire (~6-8 inches)
   - Strip and tin one end
   - Solder to Sleeve terminal (common point with Ring)

### Step 2: Mount Jacks to Rear Panel

1. **Drill/3D-print panel holes:**
   - 2× 6mm holes for CV/Gate jacks
   - Spacing: 15mm center-to-center
   - Check hole alignment with calipers

2. **Install jacks:**
   - Insert jack from outside of panel
   - Thread retaining nut from inside
   - Tighten with small wrench or pliers
   - Ensure jack is seated flush and straight

### Step 3: Wire to MCP4728 DAC

**Wiring from jacks to DAC breakout:**

**Jack 1 (CV Pitch):**
- Tip wire → MCP4728 OUT A pad (solder or screw terminal)
- Sleeve wire → MCP4728 GND pad

**Jack 2 (Gate):**
- Tip wire → MCP4728 OUT B pad (solder or screw terminal)
- Sleeve wire → MCP4728 GND pad (same common ground)

**Ground wire management:**
- Both Sleeve wires can share a single connection to GND
- Use a common GND bus bar or wire splice if needed
- Keep ground wires short and direct

### Step 4: Secure DAC in Enclosure

**Mounting options:**
1. **Double-sided foam tape** (easiest):
   - Clean mounting surface
   - Apply foam tape to bottom of DAC breakout
   - Press firmly onto enclosure floor near rear panel
   - Ensure wires have slack for strain relief

2. **Standoffs/screws** (more secure):
   - Use M2.5 or M3 standoffs if DAC has mounting holes
   - Secure with small screws from bottom of enclosure

**Wire routing:**
- Route CV/Gate wires neatly from DAC to rear panel
- Avoid crossing power wires (keep 5-10mm separation)
- Use cable ties or wire clips to secure bundle
- Leave ~10mm slack for serviceability

### Step 5: Label Panel

**Recommended labeling:**
- Jack 1: "CV" or "PITCH" (with 1V/oct symbol if desired)
- Jack 2: "GATE" or "TRIG"
- Optional: Add polarity indicator (e.g., "V-TRIG" below Gate jack)
- Optional: Voltage range label "0-5V"

**Labeling methods:**
- Vinyl label maker
- Laser engraving (if enclosure material supports it)
- Permanent marker (simple but effective for prototypes)

---

## Electrical Specifications

### Output Characteristics

**CV Pitch (Channel A):**
- **Voltage Range:** 0-5V
- **Resolution:** 12-bit (4096 steps) = ~1.22mV per step
- **Scaling:** 1V/octave (configurable via software)
- **Reference:** C3 (MIDI 60) = typically 1V or 2V (user configurable)
- **Accuracy:** ±0.5% (with 5V reference from boost module)

**Gate (Channel B):**
- **Voltage Levels:**
  - HIGH (note on): 5V
  - LOW (note off): 0V
- **Polarity:** V-trig (standard) or S-trig (inverted via software)
- **Mode:** Gate (stays high during note, low when note ends)
- **Output Impedance:** ~1kΩ (suitable for most modular inputs)

### Power Requirements

- **MCP4728 Supply:** 5V @ ~10mA (from Teyleten Boost Module)
- **Total CV/Gate current:** Negligible (<1mA per channel)
- **Ground reference:** Common ground with M4 Feather and boost module

---

## Testing Procedure

### Initial Testing (Before Enclosure Assembly)

1. **Continuity Test:**
   - Use multimeter in continuity mode
   - Verify Ring and Sleeve are connected on each jack
   - Verify Tip is isolated from Ring/Sleeve (no short)

2. **Resistance Test:**
   - Measure Tip to Sleeve: should be high impedance (>100kΩ)
   - Measure Ring to Sleeve: should be ~0Ω (direct connection)

3. **Voltage Test (DAC powered, code running):**
   - Insert voltmeter probes into jack (Tip = positive, Sleeve = negative)
   - CV Jack: Should read 0-5V when playing notes
   - Gate Jack: Should toggle between 0V (off) and 5V (on)

### Functional Testing (After Assembly)

1. **Cable Compatibility Test:**
   - Test with TS (mono) cable: Should work normally
   - Test with TRS (stereo) cable: Should work normally
   - Verify no ground loops or hum

2. **CV Pitch Accuracy:**
   - Send MIDI note C3 (MIDI 60)
   - Measure CV output (should be 1V or 2V depending on reference)
   - Send C4 (MIDI 72) → Should be 1V higher than C3
   - Verify 1V/octave scaling

3. **Gate Timing:**
   - Send MIDI note on → Gate should go HIGH (5V or 0V if S-trig)
   - Send MIDI note off → Gate should go LOW (0V or 5V if S-trig)
   - Verify gate follows arpeggiated notes correctly

4. **Polarity Test:**
   - Test V-trig mode: 0V off, 5V on
   - Test S-trig mode: 5V off, 0V on (inverted)
   - Verify setting changes correctly in menu

---

## Troubleshooting

### Problem: No voltage on CV output

**Possible causes:**
- MCP4728 not powered (check 5V from boost module)
- I2C communication failure (check SCL/SDA connections)
- Wire not soldered to Tip terminal
- Code not running or DAC not initialized

**Solution:**
1. Check 5V power at MCP4728 VCC pin
2. Run `test dac` command in serial console
3. Verify DAC address (0x60) with I2C scan
4. Check wire connections with continuity test

### Problem: Gate stuck HIGH or LOW

**Possible causes:**
- Wire shorted to ground (stuck LOW)
- Wire floating/disconnected (may read HIGH)
- Code not sending gate off command
- Wrong polarity setting

**Solution:**
1. Check wire continuity from DAC OUT B to jack Tip
2. Toggle polarity setting (V-trig ↔ S-trig)
3. Monitor serial console for gate on/off messages
4. Test DAC directly: `dac.channel_b.value = 0` (LOW) or `4095` (HIGH)

### Problem: Voltage inaccurate (not 1V/octave)

**Possible causes:**
- Boost module not outputting exactly 5V (check with multimeter)
- Software calibration needed
- Incorrect MIDI reference note setting

**Solution:**
1. Measure boost module output (should be 5.0V ±0.1V)
2. Adjust boost module trim pot if needed
3. Verify `MIDI_REFERENCE_NOTE = 60` in `cv_output.py`
4. Calibrate with known voltage reference (1V, 2V, 3V)

### Problem: Ground loop hum/noise

**Possible causes:**
- Ground wire not connected to Sleeve
- Ring terminal floating (not tied to Sleeve)
- Ground loop with external synth

**Solution:**
1. Verify Ring-Sleeve connection on both jacks
2. Check common ground between M4, DAC, and jacks
3. Use ground lift adapter on external synth power supply
4. Add ferrite bead on CV cable if interference persists

### Problem: Works with TS cable but not TRS cable

**Possible causes:**
- Ring not tied to Sleeve (TRS cable shorts Ring to ground)
- Faulty TRS cable

**Solution:**
1. Double-check Ring-Sleeve solder joint on each jack
2. Test with known-good TRS cable
3. Verify no opens or shorts on TRS cable with multimeter

---

## Compatible Synthesizers

### Tested Compatible (1V/octave standard):

**Vintage:**
- Moog Minimoog, Source, Prodigy
- ARP Odyssey, 2600
- Roland SH-101, SH-09, Juno-60
- Korg MS-20, MS-10, MS-50
- Sequential Circuits Prophet-5, Pro-One

**Modern:**
- Arturia MiniBrute, MicroBrute, MatrixBrute
- Moog Mother-32, DFAM, Subsequent 37
- Make Noise 0-Coast, Strega
- Behringer Neutron, Model D
- Any Eurorack modular system

**Note:** Moog S-trig compatibility requires S-trig polarity setting in menu (5V=off, 0V=on).

---

## Future Expansion (Channels C & D)

The MCP4728 has 2 additional channels (C, D) available for expansion:

**Possible uses:**
- **Velocity CV:** 0-5V proportional to MIDI velocity
- **Modulation CV:** LFO or envelope follower output
- **Second Gate:** For drum triggers or additional voice
- **Clock Output:** Pulse on each arpeggio step

**To add jacks later:**
1. Follow same wiring procedure as CV/Gate
2. Update panel labels (drill new 6mm holes)
3. Update firmware to assign functions to channels C/D
4. No hardware changes needed (DAC already supports it)

---

## Bill of Materials - CV/Gate Hardware Only

| Item | Qty | Unit Price | Total | Source |
|------|-----|------------|-------|--------|
| Thonkiconn PJ301M-12 (3.5mm TRS jack) | 2 | $1.25 | $2.50 | Thonkiconn, Tayda, Mouser |
| 22-24 AWG stranded wire (6 inches per jack) | 1 foot | $0.50 | $0.50 | Generic |
| Heat shrink tubing (assorted sizes) | 4 pieces | $0.10 | $0.40 | Generic |
| Solder | ~1 gram | - | - | (Included in tools) |

**Total CV/Gate Hardware Cost:** ~$3.40

---

## Tools Required

- Soldering iron (15-30W)
- Solder (60/40 or lead-free)
- Wire strippers (22-24 AWG)
- Multimeter (voltage and continuity testing)
- Small wrench or pliers (for jack nuts)
- Heat gun or lighter (for heat shrink)
- Drill with 6mm bit (if hand-drilling panel holes)

---

## Safety Notes

- Always power off before making connections
- Double-check polarity before applying power
- Use heat shrink on all exposed solder joints
- Avoid shorts between Tip and Ring/Sleeve
- Test with multimeter before connecting to expensive synthesizers
- Keep CV voltages within 0-5V range (MCP4728 cannot exceed supply voltage)

---

## Software Configuration

See `cv_output.py` for full implementation details. Key settings:

```python
# CV Output Configuration
MIDI_REFERENCE_NOTE = 60  # C3 = reference point
CV_REFERENCE_VOLTAGE = 1.0  # Voltage at reference note

# Channel assignments
CH_PITCH = 0    # Channel A: CV pitch (1V/octave)
CH_TRIGGER = 1  # Channel B: Gate/trigger output

# Polarity (user-configurable in settings menu)
TRIGGER_VTRIG = 0  # V-trig: 0V=off, 5V=on
TRIGGER_STRIG = 1  # S-trig: 5V=off, 0V=on (Moog)
```

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-15 | Initial CV/Gate integration guide |

---

**Questions or issues?** See `TESTING_GUIDE.md` for hardware troubleshooting or run `test dac` via serial console.
