# MIDI LED Tap Guide - External Activity Indicators

**Purpose:** Tap the MIDI IN/OUT LED signals from the MIDI FeatherWing to drive external panel-mount LEDs.

**Hardware:** Adafruit MIDI FeatherWing #4740

---

## Overview

The MIDI FeatherWing has onboard activity LEDs:
- **MIDI IN LED** (red) - Blinks when receiving MIDI
- **MIDI OUT LED** (red) - Blinks when sending MIDI

We'll tap these signals to drive larger, panel-mount LEDs for better visibility (especially through semi-transparent enclosure).

---

## Components Needed

**LEDs:**
- 2× LEDs (your choice - red, amber, blue, RGB, etc.)
- Recommend: 5mm or 3mm standard LEDs
- Forward voltage: 2.0-2.2V (red), 3.0-3.4V (blue/white)

**Resistors:**
- 2× Current-limiting resistors (see calculations below)
- Typical: 330Ω - 470Ω for standard brightness

**Wire:**
- 22-26 AWG hookup wire
- 4 wires total (2 per LED: anode + cathode)

**Optional:**
- Heat shrink tubing
- LED bezels/holders for panel mounting

---

## MIDI FeatherWing LED Circuit Analysis

### MIDI OUT LED Circuit

**Signal source:** UART TX line (D1 from Feather M4)

**Circuit path:**
```
D1 (TX) → [Resistor R3: 220Ω] → LED D2 (anode) → LED D2 (cathode) → GND
```

**Behavior:**
- TX line HIGH (idle): LED OFF
- TX line LOW (transmitting): LED ON
- Blinks during MIDI transmission

**Tap point:** LED D2 anode (resistor side) or cathode (GND side)

### MIDI IN LED Circuit

**Signal source:** Optocoupler (6N138) output

**Circuit path:**
```
Optocoupler Pin 6 → [Resistor R2: 220Ω] → LED D1 (anode) → LED D1 (cathode) → GND
```

**Behavior:**
- No MIDI: LED OFF
- Receiving MIDI: LED ON
- Blinks during MIDI reception

**Tap point:** LED D1 anode (resistor side) or cathode (GND side)

---

## Current Limiting Resistor Calculation

**Given:**
- Supply voltage: 3.3V (from Feather M4)
- LED forward voltage (Vf): 2.0V (red), 3.0V (blue)
- Desired current (If): 10-20mA (standard LED)

**Formula:**
```
R = (Vsupply - Vf) / If
```

**Examples:**

**Red LED @ 15mA:**
```
R = (3.3V - 2.0V) / 0.015A = 87Ω
Nearest standard: 100Ω (brighter) or 150Ω (dimmer)
```

**Blue LED @ 15mA:**
```
R = (3.3V - 3.0V) / 0.015A = 20Ω
Nearest standard: 22Ω or 33Ω
```

**For safety and longer LED life, use 330Ω - 470Ω (results in ~5-10mA, plenty bright).**

---

## Wiring Method 1: Parallel Tap (Recommended)

**Concept:** Connect external LED in parallel with onboard LED.

**Advantages:**
- ✅ Onboard LED still works (useful for troubleshooting)
- ✅ Same signal, perfect sync
- ✅ Simple wiring

**Wiring:**

### MIDI OUT LED Tap

**Breadboard connections:**
1. **Find D1 (TX) on breadboard** - This is the signal wire from M4 to MIDI FeatherWing
2. **Tap signal:** Connect external LED anode to TX line (D1)
3. **Tap ground:** Connect external LED cathode to GND

**Circuit:**
```
D1 (TX) ──┬─[R3: 220Ω]─→ Onboard LED D2 → GND
          │
          └─[R: 330Ω]──→ External LED → GND
```

**Steps:**
1. Cut 2 wires (red for signal, black for GND)
2. Connect red wire to D1 (TX) breadboard row
3. Connect black wire to GND breadboard row
4. External LED anode → through 330Ω resistor → red wire
5. External LED cathode → black wire

### MIDI IN LED Tap

**Breadboard connections:**
1. **Find the optocoupler output** or tap at onboard LED D1 anode
2. **Tap signal:** Connect external LED anode to same point
3. **Tap ground:** Connect external LED cathode to GND

**Circuit:**
```
Opto Pin 6 ──┬─[R2: 220Ω]─→ Onboard LED D1 → GND
             │
             └─[R: 330Ω]──→ External LED → GND
```

**Steps:**
1. Cut 2 wires (red for signal, black for GND)
2. Locate LED D1 anode on breadboard (resistor R2 side)
3. Connect red wire to same breadboard row as LED D1 anode
4. Connect black wire to GND breadboard row
5. External LED anode → through 330Ω resistor → red wire
6. External LED cathode → black wire

---

## Wiring Method 2: Series Tap (Alternative)

**Concept:** Wire external LED in series with onboard LED (shares current).

**Advantages:**
- ✅ No additional current draw
- ✅ Both LEDs guaranteed same brightness/timing

**Disadvantages:**
- ⚠️ Voltage drop may dim both LEDs
- ⚠️ Requires cutting traces or removing onboard LED

**Not recommended unless you need ultra-low power.**

---

## Physical Wiring Steps

**Tools needed:**
- Multimeter (for continuity checks)
- Soldering iron (if soldering resistors to LED leads)
- Wire strippers

### Step 1: Prepare External LEDs

1. **Identify LED polarity:**
   - Anode: Longer lead, larger internal element
   - Cathode: Shorter lead, flat side on LED body

2. **Solder resistors to LED anodes:**
   - 330Ω resistor to anode lead
   - Heat shrink over solder joint

3. **Add wire leads:**
   - Red wire to resistor free end (signal)
   - Black wire to LED cathode (ground)
   - Length: Depends on enclosure layout (6-12 inches typical)

### Step 2: Locate Tap Points on Breadboard

**MIDI OUT LED (easier):**
- **Signal:** D1 (TX) breadboard row
- **Ground:** Any GND breadboard row

**MIDI IN LED (slightly harder):**
- **Signal:** Find onboard LED D1 anode connection on breadboard
- **Ground:** Any GND breadboard row

**Use multimeter continuity mode to verify connections.**

### Step 3: Connect External LEDs

1. **MIDI OUT LED:**
   - Insert red wire into D1 breadboard row
   - Insert black wire into GND breadboard row

2. **MIDI IN LED:**
   - Insert red wire into LED D1 anode breadboard row
   - Insert black wire into GND breadboard row

3. **Secure connections:**
   - Ensure wires are fully inserted
   - Consider small dab of hot glue for strain relief

---

## Testing Procedure

### Visual Test (No Equipment)

1. **Deploy active MIDI routing test:**
   ```bash
   cp tests/midi_active_routing_test.py /Volumes/CIRCUITPY/code.py
   ```

2. **Observe LEDs:**
   - External MIDI OUT LED should blink every 500ms (sending notes)
   - If loopback cable connected: External MIDI IN LED blinks too

3. **Success criteria:**
   - External LEDs blink in sync with onboard LEDs
   - Brightness is acceptable
   - No flickering when idle

### Multimeter Test (Before Powering)

1. **Check polarity:**
   - Set multimeter to diode test mode
   - Touch probes to external LED leads
   - LED should light dimly in correct polarity

2. **Check continuity:**
   - Verify signal wire connects to correct breadboard row
   - Verify ground wire connects to GND

3. **Check for shorts:**
   - Measure resistance between signal and GND
   - Should read >100Ω (resistor value)
   - Not 0Ω (short) or OL (open/no connection)

---

## Troubleshooting

### External LED Not Lighting

**Check:**
1. LED polarity (anode to signal, cathode to GND)
2. Resistor value (too high? Try 220Ω)
3. Breadboard connections fully inserted
4. Onboard LED working? (If not, tap point is wrong)

### External LED Always On

**Check:**
1. Tap point - may be on wrong side of resistor
2. Short circuit - check for solder bridges
3. LED connected to 3.3V instead of signal

### External LED Dim

**Check:**
1. Resistor value too high (try 220Ω or 150Ω)
2. Poor breadboard connection (intermittent contact)
3. LED forward voltage mismatch (blue LED on 3.3V = very dim)

### Both LEDs Dim After Adding External

**Cause:** Excessive current draw from parallel connection

**Solution:**
1. Increase external LED resistor (470Ω or 560Ω)
2. Use transistor buffer (see advanced section)

---

## Advanced: Transistor Buffer (For Multiple LEDs)

If you want to drive **multiple bright LEDs** or **high-power LEDs** without loading the circuit:

**Circuit:**
```
Signal → [1kΩ] → NPN Base (2N3904)
                  NPN Emitter → GND
                  NPN Collector → LED anode(s) → [Resistor] → 3.3V
```

**Advantages:**
- ✅ Can drive multiple LEDs from one signal
- ✅ No loading on original circuit
- ✅ Can switch higher currents

**Components:**
- 1× NPN transistor (2N3904, 2N2222, or similar)
- 1× 1kΩ base resistor
- Current-limiting resistors for each LED

**You already have 2N3904 from S-Trig circuit! Same transistor type.**

---

## Panel Mounting Considerations

### LED Positioning

**Recommended placement:**
- **Front panel:** Visible during performance
- **Back panel:** Visible during patching/setup
- **Top edge:** Visible from above when racked

**Spacing:**
- Separate MIDI IN and OUT LEDs by at least 10mm
- Label clearly: "MIDI IN" / "MIDI OUT"

### LED Colors

**Aesthetic options:**
- **Classic:** Both red (matches MIDI standard)
- **Differentiated:** IN = blue, OUT = amber/orange
- **RGB:** Can be software-controlled later (requires PWM pins)

**For semi-transparent enclosure:**
- Diffused LEDs look better (less "hot spot")
- Consider recessing LEDs 2-3mm for even glow
- Frosted/translucent PLA works great as diffuser

### Mounting Methods

**3D printed bezel:**
- Design LED holder in enclosure CAD
- Press-fit 5mm or 3mm LED
- Hot glue from inside for permanence

**Panel-mount LED holder:**
- Buy pre-made LED bezels (5mm or 3mm)
- Drill hole in panel
- Snap in holder

**Flush mount:**
- Drill hole slightly smaller than LED diameter
- LED presses through from inside
- Looks very clean from outside

---

## Example: Semi-Transparent Front Panel

**Design concept:**
```
┌─────────────────────────────┐
│  [   OLED DISPLAY   ]       │  ← Semi-transparent PLA
│                              │
│  ● MIDI IN    ● MIDI OUT    │  ← LEDs glow through
│                              │
│  [A]  [B]  [C]  Buttons     │
└─────────────────────────────┘
```

**LED placement:**
- Mount LEDs 2-3mm behind front panel
- Panel thickness: 2-3mm translucent PLA
- LEDs diffuse through panel (no visible LED body from outside)
- Creates professional "backlit indicator" look

---

## Testing Checklist

- [ ] External MIDI OUT LED blinks when sending MIDI
- [ ] External MIDI IN LED blinks when receiving MIDI (loopback test)
- [ ] External LEDs sync perfectly with onboard LEDs
- [ ] Brightness is acceptable (not too dim, not too bright)
- [ ] No flickering when idle
- [ ] Onboard LEDs still work (for troubleshooting)
- [ ] Wire strain relief in place
- [ ] LEDs positioned for final enclosure

---

## Documentation

**Record your wiring:**
- Take photos of breadboard connections
- Note which breadboard rows were used
- Document resistor values used
- Measure and record LED positions for enclosure CAD

**Update PIN_ALLOCATION_MATRIX.md if using GPIO version later.**

---

## Next Steps

Once external LEDs are working:
1. Test with actual MIDI keyboard/synth (not just loopback)
2. Finalize LED positions for enclosure design
3. Design LED bezels/mounts in CAD
4. Consider adding LED labels/legends to front panel

---

**Ready to wire? Let's do it!**
