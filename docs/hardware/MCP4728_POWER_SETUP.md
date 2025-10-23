# MCP4728 DAC Power Setup Guide

**Date:** 2025-10-23
**Issue:** OLED display stops working when MCP4728 connected via STEMMA QT
**Root Cause:** MCP4728 needs external 5V power, cannot be powered from OLED FeatherWing's 3.3V STEMMA QT

---

## Hardware Inventory

### Components Available
1. **Adafruit OLED FeatherWing 128x64** (Product #4650)
   - STEMMA QT connector provides: 3.3V, GND, SDA, SCL
   - Cannot supply enough current for both OLED + MCP4728

2. **Adafruit MCP4728 Quad DAC Breakout**
   - Power Requirements: 2.7V - 5.5V on VCC pin
   - Needs 5V for full 0-5V CV output range
   - STEMMA QT connector: I2C only (does NOT power the board alone)

3. **Powerboost Module** (22×11×3.6mm)
   - **Input:** 2.5V to (VOUT - 0.5V)
   - **Output Options:** 5V / 8V / 9V / 12V (configurable via solder pads)
   - **Current Capacity:**
     - 5V: 1.2A max (from 3.7V Li-ion input)
     - 8V: 0.7A max
     - 9V: 0.6A max
     - 12V: 0.5A max
   - **Max Input/Output Current:** 1.5A
   - **Size:** 22 × 11 × 3.6mm

### Voltage Configuration (Powerboost)

**Solder Pad Configuration:**
```
Pad A | Pad B | Output Voltage
------|-------|---------------
  0   |   0   |     5V     ← USE THIS FOR MCP4728
  0   |   1   |     8V
  1   |   0   |     9V
  1   |   1   |    12V

0 = Pad disconnected (open)
1 = Pad connected (soldered bridge)
```

**Current Configuration Needed:** **A=0, B=0 → 5V Output**

---

## Problem Diagnosis

### What Happened
1. MCP4728 connected to OLED FeatherWing via STEMMA QT cable only
2. MCP4728 tried to draw power from OLED's 3.3V STEMMA QT line
3. Combined current draw (OLED + MCP4728) exceeded 3.3V rail capacity
4. OLED browned out and stopped displaying

### Why It Happened
- **STEMMA QT Standard:** Provides 3.3V, GND, SDA, SCL
- **OLED FeatherWing:** Sources 3.3V from Feather's 3.3V regulator
- **MCP4728 Power Needs:**
  - Chip operation: ~1-2mA (negligible)
  - DAC outputs: Up to 25mA per channel × 4 = 100mA max
  - **Total:** Can draw 50-100mA+ depending on load

- **OLED Power Budget:**
  - OLED display: ~15-30mA (typical)
  - STEMMA QT power delivery: Limited by Feather's 3.3V regulator
  - **Problem:** Not enough headroom for OLED + MCP4728

### Correct Solution
**MCP4728 needs separate 5V power supply via its VCC pin.**

---

## Wiring Plan - Option A: Powerboost Module (RECOMMENDED)

### Step 1: Configure Powerboost for 5V Output

**Check Solder Pads A and B:**
1. Locate pads marked "A" and "B" on front of powerboost PCB
2. Verify configuration:
   - **Pad A:** Should be OPEN (disconnected) = 0
   - **Pad B:** Should be OPEN (disconnected) = 0
   - **Result:** A=0, B=0 → 5V output

**If pads are already configured differently:**
1. Heat solder bridge with soldering iron
2. Use solder wick to remove solder and open the connection
3. Confirm pads are disconnected with multimeter (continuity test)

**Optional - Disable LED Indicator:**
- If you want to save power, desolder the pad next to the LED indicator
- This turns off the power LED on the powerboost

### Step 2: Connect Powerboost Input Power

**Power Source Options:**

**Option 1: USB 5V (Testing/Development)**
```
Feather M4 USB Pin → Powerboost VIN
Feather M4 GND    → Powerboost GND
```
- Simple, no battery needed
- Good for bench testing
- **Note:** Powerboost input range is 2.5V to (VOUT - 0.5V)
  - For 5V output: Input must be 2.5V to 4.5V
  - **WARNING:** USB 5V is ABOVE the max input (4.5V) for 5V output mode!
  - **DO NOT USE USB 5V DIRECTLY** - It will damage the powerboost or not regulate properly

**Option 2: LiPo Battery (3.7V nominal, recommended)**
```
LiPo Battery + → Powerboost VIN
LiPo Battery - → Powerboost GND
```
- **Recommended:** 3.7V Li-ion/LiPo battery
- Input range: 2.5V (dead battery) to 4.2V (fully charged)
- Well within safe input range for 5V output
- Powerboost output: 5V @ 1.2A max

**Option 3: Feather M4 BAT Pin (If LiPo connected to Feather)**
```
Feather M4 BAT Pin → Powerboost VIN
Feather M4 GND     → Powerboost GND
```
- Uses Feather's LiPo battery connection
- Clean integration
- **Best option for final assembly**

### Step 3: Connect MCP4728 DAC

**Power Connections:**
```
Powerboost VOUT (5V) → MCP4728 VCC pin
Powerboost GND       → MCP4728 GND pin
```

**I2C Connections (via STEMMA QT):**
```
OLED FeatherWing STEMMA QT → MCP4728 STEMMA QT
  - SDA (I2C Data)
  - SCL (I2C Clock)
  - GND (Common ground - connects to powerboost GND too)
  - 3.3V (NOT CONNECTED to MCP4728 VCC - leave floating!)
```

**Important:** The STEMMA QT cable's 3.3V wire should be left unconnected on the MCP4728 side, or cut/taped. Only SDA, SCL, and GND are needed for I2C communication.

### Step 4: Complete Wiring Diagram

```
┌─────────────────────────────────────┐
│  Feather M4 CAN Express             │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  OLED FeatherWing 128x64    │   │
│  │  (Stacked on Feather)       │   │
│  │                              │   │
│  │  STEMMA QT OUT              │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│         BAT Pin ────────┐           │
│         GND Pin ────┐   │           │
└─────────────────────┼───┼───────────┘
                      │   │
                      │   │ ┌──────────────────────┐
                      │   │ │  Powerboost Module   │
                      │   └→│  VIN (3.7V LiPo)     │
                      └────→│  GND                 │
                           │  VOUT (5V)           │──┐
                           │  GND                 │──┼─┐
                           └──────────────────────┘  │ │
                                                     │ │
         STEMMA QT Cable (4-wire)                    │ │
                      │                              │ │
         ┌────────────┴──────────┐                   │ │
         │                       │                   │ │
         ↓ SDA, SCL, GND only    ↓                   │ │
    ┌────────────────────────────────┐               │ │
    │  MCP4728 Quad DAC Breakout     │               │ │
    │                                │               │ │
    │  VCC ←──────────────────────────────────────────┘ │
    │  GND ←────────────────────────────────────────────┘
    │  SDA ←──┐                      │
    │  SCL ←──┼── (via STEMMA QT)    │
    │  GND ←──┘                      │
    │                                │
    │  VA, VB, VC, VD (CV Outputs)   │ → To synth/module
    └────────────────────────────────┘
```

### Step 5: Verification Before Power-On

**Pre-Power Checklist:**
- [ ] Powerboost configured for 5V (A=0, B=0)
- [ ] Powerboost VIN connected to 3.7V LiPo or Feather BAT pin
- [ ] Powerboost GND connected to Feather GND
- [ ] MCP4728 VCC connected to Powerboost VOUT (5V)
- [ ] MCP4728 GND connected to Powerboost GND
- [ ] MCP4728 STEMMA QT connected for I2C only (SDA, SCL, GND)
- [ ] No shorts between power rails (use multimeter continuity test)

**Voltage Verification (Use Multimeter):**
1. Power on Feather M4 via USB
2. Measure Powerboost VOUT: Should read **5.0V ± 0.1V**
3. Measure MCP4728 VCC pin: Should read **5.0V ± 0.1V**
4. If voltage incorrect, power off immediately and check wiring

---

## Alternative Wiring - Option B: Direct 5V from Feather USB Pin

**⚠️ WARNING:** This option has limitations and is NOT recommended for production use.

### When to Use This
- Quick testing only
- No LiPo battery available
- USB-powered operation only (no portability)

### Wiring
```
Feather M4 USB Pin (5V) → MCP4728 VCC
Feather M4 GND          → MCP4728 GND
OLED STEMMA QT          → MCP4728 STEMMA QT (I2C only)
```

### Limitations
1. **No Battery Operation:** Requires USB connection at all times
2. **Voltage Drop:** USB 5V may sag under load
3. **Noise:** USB power is noisier than regulated battery power
4. **CV Accuracy:** Voltage fluctuations affect CV pitch accuracy

### Pre-Connection Check
- Use multimeter to verify Feather's USB pin outputs 5V
- If voltage < 4.9V, USB port may not supply enough current

---

## Testing Procedure After Wiring

### Test 1: Power-On Verification
1. Power on Feather M4 via USB
2. **Check OLED Display:**
   - Should display startup screen
   - If blank, check OLED power and I2C connections
3. **Check Powerboost:**
   - LED indicator should be lit (if not disabled)
   - Measure VOUT with multimeter: 5.0V ± 0.1V
4. **Check MCP4728 VCC:**
   - Measure VCC pin: 5.0V ± 0.1V

### Test 2: I2C Bus Scan
Run the quick MCP4728 import test:
```bash
cp tests/test_mcp4728_dac.py /Volumes/CIRCUITPY/code.py
python3 scripts/monitor_serial.py --duration 30
```

Expected output:
```
[TEST 1] Scanning I2C bus...
  Found 2 device(s) on I2C bus:
    [ ] 0x3C - OLED Display
    [✓] 0x60 - MCP4728 DAC

  ✓ MCP4728 DAC found at address 0x60
```

If DAC not found:
- Check STEMMA QT cable connection (SDA, SCL, GND)
- Verify MCP4728 VCC is 5V
- Check I2C pullup resistors (STEMMA QT usually has them)

### Test 3: DAC Output Test
The full test will run through:
1. I2C bus scan
2. DAC initialization
3. Zero all channels
4. Voltage ramp (0V → 5V)
5. CV pitch accuracy (1V/octave)
6. Gate/trigger test

**Use a multimeter to verify voltages during test.**

### Test 4: OLED + MCP4728 Together
Deploy main.py and verify both work simultaneously:
```bash
python3 scripts/deploy.py
python3 scripts/monitor_serial.py --reload
```

Expected:
- OLED displays menu/status
- No brownouts or flickering
- MCP4728 responds to I2C commands
- Both devices stable

---

## Current Draw Analysis

### Power Budget (3.7V LiPo Input, 5V Output)

**Feather M4 CAN + OLED (3.3V rail):**
- Feather M4 (active): ~50-80mA
- OLED display (active): ~15-30mA
- **Total 3.3V rail:** ~70-110mA

**MCP4728 DAC (5V rail, separate from powerboost):**
- MCP4728 chip: ~1-2mA
- DAC outputs (under load): Up to 25mA/channel × 4 = 100mA max
- **Total 5V rail:** ~50-100mA (typical)

**Powerboost Module Capacity:**
- Input: 3.7V LiPo @ 1.5A max
- Output: 5V @ 1.2A max
- **Headroom:** Plenty for MCP4728 (only 50-100mA typical)

**Result:** Clean power separation, no brownouts, stable operation.

---

## Troubleshooting

### OLED Not Displaying After Connection
1. **Check OLED Power:**
   - Measure 3.3V at OLED I2C header: Should be 3.3V
   - If 0V, check Feather's 3.3V regulator
2. **Check I2C Bus:**
   - Run I2C scan (see Test 2 above)
   - Verify both 0x3C (OLED) and 0x60 (DAC) detected
3. **Check for Shorts:**
   - Power off
   - Use multimeter continuity mode
   - Check 5V rail not shorted to 3.3V rail

### MCP4728 Not Detected on I2C
1. **Check VCC Voltage:**
   - Measure MCP4728 VCC pin: Should be 5.0V ± 0.1V
   - If 0V, check powerboost wiring
   - If < 4.5V, check powerboost configuration (A=0, B=0)
2. **Check STEMMA QT Connection:**
   - Verify SDA, SCL, GND connected
   - Try reseating cable
3. **Check I2C Address:**
   - Default: 0x60
   - Some boards ship with 0x64
   - Try scanning for both addresses

### DAC Outputs Wrong Voltage
1. **Check Vref Configuration:**
   - Code should set `channel.vref = adafruit_mcp4728.Vref.INTERNAL`
   - Internal reference: 2.048V base × 2 (gain) = 4.096V max
   - For 5V output, use EXTERNAL reference (VCC = 5V)
2. **Check Gain:**
   - Code should set `channel.gain = 1` for 0-5V range
3. **Measure VCC:**
   - If VCC < 5V, DAC output will be proportionally lower
   - Example: VCC = 4.5V → Max output = 4.5V (not 5V)

### Powerboost Not Outputting 5V
1. **Check Input Voltage:**
   - Measure VIN: Should be 2.5V to 4.5V for 5V output mode
   - If > 4.5V (e.g., USB 5V), powerboost may shutdown or not regulate
2. **Check Solder Pads:**
   - Verify A=0, B=0 (both pads open)
   - Use continuity tester to confirm pads not bridged
3. **Check Current Draw:**
   - If output current > 1.2A, powerboost will current-limit
   - Typical draw should be < 200mA total

---

## Power Supply Comparison

| Power Source | Input V | Output V | Current | Pros | Cons |
|--------------|---------|----------|---------|------|------|
| **Powerboost + LiPo** | 3.7V | 5.0V | 1.2A | Clean, stable, portable | Extra component |
| **Feather USB Pin** | 5.0V | 5.0V | Varies | Simple, no extra parts | USB-only, noise |
| **Separate 5V Supply** | N/A | 5.0V | 1A+ | High current, clean | Extra power brick |

**Recommendation:** Powerboost + LiPo for best results.

---

## Bill of Materials (Power Supply)

### Required Components
- [✓] Powerboost module (22×11mm, 5V/8V/9V/12V configurable) - **IN INVENTORY**
- [✓] LiPo battery (3.7V, 500mAh or larger) - Check if in inventory
- [ ] JST connector or wire leads for LiPo (if not included)
- [ ] Wire (22-24 AWG) for power connections
- [ ] Breadboard or perfboard for mounting powerboost

### Optional Components
- [ ] Switch (SPST) for power control
- [ ] Indicator LED (3mm) + 1kΩ resistor
- [ ] Heat shrink tubing for wire insulation
- [ ] Mounting standoffs/screws for powerboost

---

## Next Steps

1. **Configure Powerboost:** Set A=0, B=0 for 5V output
2. **Connect LiPo Battery:** To powerboost VIN/GND (or use Feather BAT pin)
3. **Wire MCP4728:** VCC to powerboost VOUT, GND to powerboost GND
4. **Test I2C:** Run test_mcp4728_dac.py and verify detection
5. **Test OLED:** Verify OLED still displays correctly
6. **Measure Voltages:** Use multimeter to confirm 5V on MCP4728 outputs

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
**Status:** Ready for implementation
