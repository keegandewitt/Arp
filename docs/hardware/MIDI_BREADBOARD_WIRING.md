# MIDI FeatherWing Breadboard Testing Guide

**Purpose:** Test MIDI FeatherWing on breadboard WITHOUT unstacking OLED
**Benefit:** Safe testing - keep working OLED + M4 intact!

---

## ⚡ Power Flow

**CRITICAL:** Power comes from USB-C → M4 → MIDI FeatherWing

```
[USB-C Cable] → [M4 USB-C Port] → [M4 3V regulator] → [M4 3V pin] → [MIDI 3V pin]
```

**Only ONE power source:** USB-C connected to M4
**NO separate power** needed for MIDI FeatherWing!

---

## 🔌 Required Connections

The MIDI FeatherWing needs only **4 wires** to function:

| Connection | M4 Pin | MIDI FeatherWing Pin | Wire Color (suggest) | Purpose |
|------------|--------|----------------------|----------------------|---------|
| **Power** | 3V | 3V | Red | 3.3V from M4 regulator |
| **Ground** | GND | GND | Black | Common ground |
| **UART TX** | D1 (TX) | TX | Yellow | MIDI data out |
| **UART RX** | D0 (RX) | RX | Orange | MIDI data in |

---

## 📍 Feather M4 CAN Pin Locations

**Looking at M4 with USB on LEFT:**

```
        USB-C
         ___
        |   |
Left    |   |    Right
Side    |___|    Side

LEFT SIDE (top to bottom):
- RESET
- 3V      ← Connect to MIDI 3V (RED wire)
- AREF
- GND     ← Connect to MIDI GND (BLACK wire)
- A0
- A1
- A2
- A3
- A4
- A5
- SCK
- MOSI
- MISO
- RX (D0) ← Connect to MIDI RX (ORANGE wire)
- TX (D1) ← Connect to MIDI TX (YELLOW wire)

RIGHT SIDE:
[Other pins not needed for MIDI]
```

---

## 🎯 Step-by-Step Breadboard Wiring

### What You Need:
- Breadboard
- 4x male-to-male jumper wires
- MIDI FeatherWing (not stacked, separate)
- M4 + OLED stack (stays intact!)

### Wiring Procedure:

**1. Power Off M4**
```bash
# Disconnect USB-C cable from M4
# This is your ONLY power source
```

**2. Insert MIDI FeatherWing into Breadboard**
- Place MIDI FeatherWing across center gap of breadboard
- Headers should plug into breadboard rows
- MIDI jacks facing outward (easy access)

**3. Identify MIDI FeatherWing Pins**

On the MIDI FeatherWing headers (same layout as Feather):
- Find **TX** pin (usually marked, or count from end)
- Find **RX** pin (next to TX)
- Find **3V** pin (near top)
- Find **GND** pin (near top, next to 3V)

**4. Wire Connections**

**CRITICAL: Double-check each connection before powering on!**

```
Connection 1: Power
[M4 3V pin] ----RED WIRE----> [MIDI 3V pin]

Connection 2: Ground
[M4 GND pin] ---BLACK WIRE--> [MIDI GND pin]

Connection 3: UART TX
[M4 TX (D1)] ---YELLOW WIRE--> [MIDI TX pin]

Connection 4: UART RX
[M4 RX (D0)] ---ORANGE WIRE--> [MIDI RX pin]
```

**5. Visual Verification**

Before powering on, check:
- [ ] 3V to 3V (RED wire)
- [ ] GND to GND (BLACK wire)
- [ ] TX to TX (YELLOW wire)
- [ ] RX to RX (ORANGE wire)
- [ ] No wires crossed
- [ ] All wires firmly seated

**6. Power On**
- Reconnect USB-C to M4 (this powers EVERYTHING)
- M4 3V regulator provides power to MIDI via 3V wire
- Check `/Volumes/CIRCUITPY` mounts
- MIDI FeatherWing LEDs may flash briefly on power-up

---

## 🔍 Troubleshooting Breadboard Setup

### MIDI FeatherWing Not Powering
**Check:**
- 3V wire connected correctly
- GND wire connected correctly
- Breadboard connections are firm

**Test:**
- Use multimeter to check 3.3V at MIDI FeatherWing 3V pin

### UART Not Working
**Check:**
- TX → TX connection (not crossed)
- RX → RX connection (not crossed)
- Wires not loose in breadboard

### Serial Errors
**Common Issue:** Swapped TX/RX

**If you see UART errors:**
1. Power off
2. Swap TX and RX wires
3. Power on and test again

---

## 🧪 Testing Sequence

### Test 1: Power Verification
```bash
# Just check MIDI FeatherWing powers up
# Look for LEDs to light up briefly on power-on
```

### Test 2: MIDI Output Test
```bash
# Install library first
circup install adafruit_midi

# Deploy test
cp tests/midi_output_test.py /Volumes/CIRCUITPY/code.py

# Watch for:
# - MIDI OUT LED blinking on FeatherWing
# - Serial output showing "Sending Note ON..."
```

**Expected:**
- ✅ MIDI OUT LED blinks rhythmically
- ✅ No UART errors in serial output
- ✅ Code runs continuously

### Test 3: MIDI Input Test
```bash
# Deploy input test
cp tests/midi_input_test.py /Volumes/CIRCUITPY/code.py

# Connect MIDI keyboard to MIDI IN jack
# Play notes

# Watch for:
# - MIDI IN LED blinking when you play
# - Serial output showing note numbers
```

**Expected:**
- ✅ MIDI IN LED blinks on key presses
- ✅ Serial shows "Note ON: Note #60..."
- ✅ All notes detected

### Test 4: Loopback Test
```bash
# Connect MIDI OUT to MIDI IN with cable

# Deploy loopback test
cp tests/midi_loopback_test.py /Volumes/CIRCUITPY/code.py

# Watch for:
# - 100% success rate in serial output
# - Both LEDs blinking in sync
```

---

## ✅ Success Criteria

Breadboard testing is successful when:

- ✅ MIDI FeatherWing powers from M4 3V
- ✅ MIDI OUT test passes (LED blinks)
- ✅ MIDI IN test passes (receives notes)
- ✅ Loopback test shows 100% success rate
- ✅ No UART errors in serial output
- ✅ OLED + buttons still work (M4 unaffected)

**Once breadboard tests pass:**
- We know MIDI FeatherWing works!
- We know the code is correct!
- Safe to stack into final configuration!

---

## 🎯 Advantages of Breadboard Testing

1. **OLED stays intact** - No unstacking needed
2. **Easy debugging** - Can swap wires easily
3. **Visual verification** - See all connections clearly
4. **Safe** - No risk to working M4 + OLED
5. **Educational** - Understand connections better

---

## ⚡ Quick Reference Card

**Pin Connections:**
```
M4 → MIDI FeatherWing

3V  → 3V  (power)
GND → GND (ground)
TX  → TX  (UART transmit)
RX  → RX  (UART receive)
```

**Test Order:**
1. Power verification
2. MIDI output test
3. MIDI input test
4. Loopback test

**Success = All 4 tests pass!**

---

**Version:** 1.0
**Date:** 2025-10-22
**Status:** Ready for breadboard assembly
