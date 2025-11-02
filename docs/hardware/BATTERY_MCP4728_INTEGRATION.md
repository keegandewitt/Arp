# Battery + MCP4728 Integration Guide
## Safe Simultaneous Integration Plan

**Date:** 2025-10-23
**Purpose:** Safely integrate LiPo battery AND MCP4728 DAC at the same time
**Hardware:** Feather M4 CAN + OLED FeatherWing + MIDI FeatherWing + MCP4728 + Powerboost + LiPo Battery

---

## Table of Contents

1. [Safety First - LiPo Battery Precautions](#safety-first)
2. [Hardware Inventory Check](#hardware-inventory-check)
3. [Pre-Integration Preparation](#pre-integration-preparation)
4. [Integration Plan Overview](#integration-plan-overview)
5. [Step-by-Step Wiring Instructions](#step-by-step-wiring)
6. [Testing & Verification](#testing-verification)
7. [Troubleshooting](#troubleshooting)
8. [Software Integration](#software-integration)

---

## Safety First - LiPo Battery Precautions {#safety-first}

### ⚠️ CRITICAL SAFETY RULES

**LiPo batteries can be dangerous if mishandled. Follow these rules absolutely:**

1. **Never Short Circuit**
   - Keep positive and negative terminals separate at all times
   - Use heat shrink tubing on exposed connections
   - Double-check polarity before connecting ANYTHING

2. **Never Overcharge**
   - Feather M4's built-in charger is rated at 100mA (safe)
   - Charge only via USB connection to Feather
   - Never exceed 4.2V per cell
   - Disconnect if battery feels warm during charging

3. **Never Over-Discharge**
   - Do not drain below 3.0V (CircuitPython has no built-in protection)
   - Monitor battery voltage via A5 pin (we'll implement this)
   - Add low-battery warning to display

4. **Never Physically Damage**
   - Do not puncture, crush, or bend battery
   - Store in fireproof LiPo bag when not in use
   - Dispose of damaged batteries properly (do NOT throw in trash)

5. **Never Use Damaged Battery**
   - Inspect for:
     - Swelling (puffy appearance)
     - Discoloration
     - Tears in wrapper
     - Bent/corroded connector
   - **If any damage detected: DO NOT USE**

6. **Work Area Safety**
   - Keep fire extinguisher nearby (ABC or Class D)
   - Work on non-flammable surface (metal, ceramic, concrete)
   - Have LiPo safety bag available
   - Keep away from flammable materials

### Emergency Procedures

**If Battery Swells/Smokes:**
1. Immediately disconnect power
2. Move battery to fireproof container (LiPo bag, metal tin, ceramic pot)
3. Take outdoors to open area
4. Let battery cool completely (30+ minutes)
5. Dispose properly at hazardous waste facility or battery recycling center

**If Battery Catches Fire:**
1. DO NOT use water extinguisher
2. Use ABC fire extinguisher or sand
3. Evacuate area if fire spreads
4. Call fire department if unable to control

### Safe Storage

- **Short-term (daily use):** Store at 40-60% charge in LiPo bag
- **Long-term (>1 week):** Store at 3.7-3.8V (50% charge) in cool, dry place
- **Temperature:** 15-25°C (60-77°F) ideal, avoid freezing or >60°C (140°F)
- **Location:** Fireproof container (LiPo bag, ammo can, metal toolbox)

---

## Hardware Inventory Check {#hardware-inventory-check}

### Required Components

**Check that you have ALL of these before starting:**

#### Core Components
- [ ] Feather M4 CAN Express (with USB-C cable)
- [ ] OLED FeatherWing 128x64 (Product #4650)
- [ ] MIDI FeatherWing (already stacked)
- [ ] MCP4728 Quad DAC Breakout (Adafruit #4470)
- [ ] LiPo Battery (500-1200mAh, 3.7V with JST connector)
- [ ] Powerboost Module (configured for 5V output: A=0, B=0)

#### Cables & Connectors
- [ ] STEMMA QT cable (4-wire: 3.3V, GND, SDA, SCL) - for I2C
- [ ] JST connector cable (if battery doesn't have one)
- [ ] 22-24 AWG stranded wire (red and black, ~20cm each)
- [ ] Heat shrink tubing (various sizes)

#### Tools
- [ ] Soldering iron + solder (if connections needed)
- [ ] Wire strippers
- [ ] Multimeter (CRITICAL for voltage checks)
- [ ] Small screwdriver
- [ ] Heat gun or lighter (for heat shrink)
- [ ] Helping hands or PCB holder
- [ ] Safety glasses

#### Safety Equipment
- [ ] LiPo safety bag (fireproof charging bag)
- [ ] Fire extinguisher (ABC or Class D)
- [ ] Non-flammable work surface
- [ ] Good lighting
- [ ] Well-ventilated workspace

### Optional But Recommended
- [ ] LiPo voltage alarm/monitor (3.7V cutoff)
- [ ] Fuse holder + 2A fuse (for battery protection)
- [ ] Switch (SPST) for power control
- [ ] Label maker or tape (for marking polarity)

---

## Pre-Integration Preparation {#pre-integration-preparation}

### Step 1: Inspect All Components

**LiPo Battery Inspection (CRITICAL):**
1. Visual check:
   - [ ] No swelling or puffiness
   - [ ] No tears in wrapper
   - [ ] No discoloration
   - [ ] Connector intact and not bent
2. Voltage check:
   - [ ] Use multimeter to measure voltage
   - [ ] Should read 3.7V-4.2V (nominal 3.7V, fully charged 4.2V)
   - [ ] If below 3.0V or above 4.3V: **DO NOT USE**
3. Polarity check:
   - [ ] Verify JST connector polarity matches Feather M4
   - [ ] **Adafruit standard:** Red = +, Black = -
   - [ ] If reversed, **DO NOT CONNECT** without fixing

**Powerboost Module Inspection:**
1. Solder pad check:
   - [ ] Verify Pad A = OPEN (disconnected)
   - [ ] Verify Pad B = OPEN (disconnected)
   - [ ] **Result:** A=0, B=0 → 5V output
2. Visual check:
   - [ ] No damaged components
   - [ ] No solder bridges
   - [ ] Pads/traces intact

**MCP4728 DAC Inspection:**
1. Visual check:
   - [ ] No damaged pins
   - [ ] STEMMA QT connector intact
   - [ ] No solder bridges
2. I2C address check:
   - [ ] Default address: 0x60
   - [ ] Check if A0/A1/A2 jumpers changed address

**Feather M4 + FeatherWing Stack:**
1. Power off and disconnect USB
2. Visual inspection:
   - [ ] All pins properly seated
   - [ ] No bent pins
   - [ ] OLED displays properly when USB powered (test before proceeding)
3. JST battery connector check:
   - [ ] No bent pins
   - [ ] Clean contacts
   - [ ] Polarity marking visible

### Step 2: Prepare Workspace

1. **Clear workspace** of flammable materials
2. **Place LiPo safety bag** nearby
3. **Test multimeter:**
   - Set to DC voltage mode (20V range)
   - Verify battery reads 3.7-4.2V
4. **Label wires:**
   - Red = Positive (+)
   - Black = Negative (-)
   - Use tape/labels if needed

### Step 3: Plan Wire Routing

**Before connecting anything, plan your layout:**

```
Physical Layout (Top View):

┌─────────────────────────────────┐
│  Feather Stack                  │
│  ┌─────────────────┐            │
│  │ OLED FeatherWing│            │
│  ├─────────────────┤            │
│  │ MIDI FeatherWing│            │
│  ├─────────────────┤            │
│  │ Feather M4 CAN  │            │
│  │   [JST BAT]     │◄───────────┼─── LiPo Battery (JST)
│  │   [USB-C]       │            │
│  └────────┬────────┘            │
│           │ STEMMA QT           │
│           ↓                     │
│   ┌──────────────┐              │
│   │  MCP4728 DAC │              │
│   │  VCC  GND    │              │
│   └───┬────┬─────┘              │
│       │    │                    │
│  ┌────┴────┴────────┐           │
│  │  Powerboost      │           │
│  │  VIN: from BAT   │           │
│  │  VOUT: to DAC    │           │
│  └──────────────────┘           │
└─────────────────────────────────┘
```

### Step 4: Test Powerboost BEFORE Connecting

**Do this with a separate power source first:**

1. **Test input (without battery):**
   - Use multimeter leads to apply 3.7V to powerboost VIN/GND
   - **OR** use a spare AA battery pack (3x AA = 4.5V) as test input
   - Do NOT use USB 5V (too high for 5V output mode)

2. **Measure output:**
   - Set multimeter to DC voltage (20V range)
   - Probe powerboost VOUT and GND
   - Should read: **5.0V ± 0.2V**
   - If incorrect, check pad configuration again

3. **Load test (optional but recommended):**
   - Connect 100Ω resistor across VOUT/GND
   - Current draw: ~50mA (5V / 100Ω)
   - Voltage should remain stable at 5.0V
   - Powerboost should not overheat

---

## Integration Plan Overview {#integration-plan-overview}

### Power Flow Diagram

```
                ┌──────────────────────────────────┐
                │  LiPo Battery (3.7V nominal)     │
                │  Capacity: 500-1200mAh           │
                └───────────┬──────────────────────┘
                            │ JST Connector
                            ↓
         ┌──────────────────────────────────────────┐
         │  SPLIT POWER (Junction Point)            │
         │  - Option A: Feather BAT pin distributes │
         │  - Option B: Physical wire splice/switch │
         └─────┬────────────────────┬────────────────┘
               │                    │
               ↓                    ↓
    ┌──────────────────┐   ┌──────────────────┐
    │  Feather M4 BAT  │   │  Powerboost VIN  │
    │  3.7V Input      │   │  3.7V Input      │
    │  ↓               │   │  ↓               │
    │  Internal 3.3V   │   │  Boost to 5V     │
    │  Regulator       │   │  (1.2A max)      │
    └─────┬────────────┘   └────────┬─────────┘
          │                         │
          ↓                         ↓
   ┌──────────────┐         ┌──────────────┐
   │  3.3V Rail   │         │  5V Rail     │
   │  - Feather   │         │  - MCP4728   │
   │  - OLED      │         │    DAC       │
   │  - MIDI      │         │              │
   └──────────────┘         └──────────────┘

I2C Bus: Shared across all devices (SDA, SCL, GND)
```

### Integration Sequence (Safe Order)

**We'll integrate in this order to test incrementally:**

1. **Phase 1:** Battery → Feather Only (test basic charging)
2. **Phase 2:** Battery → Powerboost (test 5V generation)
3. **Phase 3:** MCP4728 → I2C Only (no power yet)
4. **Phase 4:** MCP4728 → 5V Power (full integration)
5. **Phase 5:** Software Integration (voltage monitoring, CV output)

### Why This Order?

- **Incremental:** Test each subsystem before combining
- **Safe:** Battery tested alone first
- **Reversible:** Each phase can be undone if problems arise
- **Debuggable:** Isolate failures to specific component

---

## Step-by-Step Wiring Instructions {#step-by-step-wiring}

### Phase 1: Battery → Feather Integration

**Goal:** Connect LiPo battery to Feather M4 and verify charging works.

#### Step 1.1: Final Battery Inspection

**Before connecting battery:**
1. **Voltage Check:**
   ```
   Multimeter Settings: DC Voltage, 20V range
   Black probe → Battery negative (black wire)
   Red probe   → Battery positive (red wire)
   Expected: 3.7V - 4.2V
   ```
   - If voltage < 3.0V: **Battery dead, charge with external charger first**
   - If voltage > 4.3V: **Battery overcharged, DO NOT USE**
   - If voltage 3.0-3.7V: Safe but needs charging
   - If voltage 3.7-4.2V: Good, ready to use

2. **Polarity Check:**
   - JST connector polarity (looking at connector from wire side):
   ```
   Standard Adafruit JST Connector:
   ┌────┐
   │ ○ ○│
   └─┬─┬┘
     │ └── Red wire = Positive (+)
     └──── Black wire = Negative (-)
   ```
   - **Verify with multimeter:**
     - Black probe to black wire
     - Red probe to red wire
     - Should read positive voltage (+3.7V to +4.2V)
     - If negative reading: **REVERSED POLARITY - DO NOT CONNECT**

#### Step 1.2: Connect Battery to Feather

**Physical Connection:**
1. **Power OFF:**
   - Unplug USB from Feather M4
   - Verify OLED is dark (no power)

2. **Orient Feather:**
   - Place Feather on non-conductive surface (cardboard, wood, plastic)
   - Locate JST battery connector (near USB-C port)

3. **Connect Battery:**
   - **CRITICAL:** Double-check polarity one last time
   - Align JST connector (keyed, should only fit one way)
   - **Gently** push connector until fully seated
   - **DO NOT FORCE** - If resistance, check orientation

4. **Visual Check:**
   - Connector fully inserted
   - No exposed metal
   - Wires not stressed or bent sharply

#### Step 1.3: Test Battery Power

1. **Power On Test:**
   - Battery connected, USB disconnected
   - Observe:
     - [ ] OLED should light up (showing Arp menu)
     - [ ] Red onboard LED may blink briefly (boot)
     - [ ] No smoke, no unusual smells
     - [ ] Battery not warm to touch

   - **If OLED does not light up:**
     - Check battery voltage with multimeter
     - Check JST connection seated properly
     - Verify battery voltage > 3.0V

2. **USB Charging Test:**
   - Connect USB-C cable to Feather
   - Observe:
     - [ ] Orange/yellow LED lights up (charging indicator)
     - [ ] OLED continues to work
     - [ ] Battery starts charging (will take 5-10 hours for 500mAh battery at 100mA)

   - **Charging Current:**
     - Feather M4's built-in charger: 100mA
     - Safe for all LiPo batteries (even small 150mAh)
     - Charging time: Capacity (mAh) / 100mA
       - 500mAh battery: ~5 hours
       - 1200mAh battery: ~12 hours

3. **Charge Completion:**
   - Orange LED turns OFF when fully charged
   - Battery voltage should be 4.2V (check with multimeter after disconnecting USB)

#### Step 1.4: Battery Voltage Monitoring (Software)

**We'll implement this in Phase 5, but prepare now:**

- Feather M4 can read battery voltage via **analog pin A5** (labeled VBAT on some boards)
- Voltage divider: Reads 0-4.2V battery as 0-3.3V analog input
- Resolution: 3.3V / 4096 steps = 0.8mV per ADC unit (12-bit)

**Expected Voltages:**
- **4.2V** = Fully charged
- **3.7V** = Nominal voltage (~50% capacity)
- **3.3V** = Low battery warning (discharge cutoff)
- **3.0V** = Critical - shutdown immediately

**Test Plan (Later):**
```python
import board
import analogio

# Read battery voltage
vbat_pin = analogio.AnalogIn(board.VOLTAGE_MONITOR)  # A5 / VBAT
raw_value = vbat_pin.value  # 0-65535 (16-bit read)
voltage = (raw_value / 65535.0) * 3.3 * 2  # Scale to battery voltage
print(f"Battery: {voltage:.2f}V")
```

---

### Phase 2: Battery → Powerboost Integration

**Goal:** Connect battery to powerboost and generate stable 5V for MCP4728.

#### Step 2.1: Powerboost Wiring Plan

**We have two options for powering the powerboost from the battery:**

**Option A: Tap Feather's BAT Pin (Recommended)**
- **Pros:** Clean integration, uses Feather's existing battery connection
- **Cons:** Adds load to Feather's JST connector (but well within spec)

**Option B: Wire Splitter from Battery**
- **Pros:** Separate power paths (diagnostic isolation)
- **Cons:** Requires soldering or splitter cable

**We'll use Option A for simplicity.**

#### Step 2.2: Wire Powerboost to Feather BAT Pin

**Materials Needed:**
- 22 AWG red wire (~10cm)
- 22 AWG black wire (~10cm)
- Heat shrink tubing
- Soldering iron + solder

**Wiring:**
1. **Power OFF:**
   - Disconnect USB
   - Disconnect battery JST connector
   - Verify OLED is dark

2. **Identify Feather BAT and GND Pins:**
   - **BAT Pin:** Labeled "BAT" on Feather M4 (outputs battery voltage directly)
   - **GND Pin:** Any ground pin (labeled "GND")

3. **Solder Wires to Powerboost:**
   ```
   Powerboost Connections:
   VIN  ←── Red wire   (to Feather BAT pin)
   GND  ←── Black wire (to Feather GND pin)
   VOUT → (unconnected for now)
   GND  → (will connect to MCP4728 later)
   ```

4. **Solder Wires to Feather:**
   - **Option 1:** Solder directly to BAT and GND header pins
   - **Option 2:** Use female jumper wires (if available)

5. **Insulate Connections:**
   - Slide heat shrink tubing over each solder joint
   - Heat with heat gun or lighter (carefully!)
   - Ensure no exposed metal

#### Step 2.3: Test Powerboost Output

1. **Reconnect Battery:**
   - Plug JST connector back into Feather
   - OLED should light up

2. **Measure Powerboost Output:**
   ```
   Multimeter Settings: DC Voltage, 20V range
   Black probe → Powerboost GND
   Red probe   → Powerboost VOUT
   Expected: 5.0V ± 0.2V
   ```

   - **If 5.0V:** ✅ Success! Powerboost working correctly
   - **If 0V:** Check wiring (VIN connected to BAT? GND connected?)
   - **If < 4.5V:** Battery may be too low, check battery voltage
   - **If > 5.5V:** **STOP - Powerboost misconfigured**, re-check pads A=0, B=0

3. **Load Test (Optional):**
   - Connect 100Ω resistor across VOUT/GND
   - Current draw: ~50mA
   - Voltage should remain 5.0V ± 0.1V

---

### Phase 3: MCP4728 I2C Connection (No Power Yet)

**Goal:** Connect MCP4728 to I2C bus via STEMMA QT, but don't power it yet.

#### Step 3.1: STEMMA QT Cable Preparation

**Standard STEMMA QT pinout:**
```
Connector (looking at cable end):
┌─────────┐
│ ● ● ● ● │
└─────────┘
  │ │ │ │
  │ │ │ └─ SCL (I2C Clock) - Yellow wire
  │ │ └─── SDA (I2C Data)  - Blue wire
  │ └───── 3.3V (Power)    - Red wire  ← DO NOT USE for MCP4728 power
  └─────── GND (Ground)    - Black wire
```

**For MCP4728, we'll use STEMMA QT for I2C ONLY:**
- SDA, SCL, GND are needed
- **3.3V line will NOT power the MCP4728** (we'll use 5V from powerboost instead)

#### Step 3.2: Connect STEMMA QT Cable

1. **Power OFF:**
   - Disconnect USB
   - Disconnect battery (pull JST connector)

2. **Connect Cable:**
   - **OLED FeatherWing STEMMA QT** → **MCP4728 STEMMA QT**
   - Cable is keyed, should only fit one way
   - Push until fully seated (you'll feel a click)

3. **Verify Connection:**
   - Cable firmly attached on both ends
   - No bent pins
   - Connectors aligned properly

---

### Phase 4: MCP4728 Power Connection (Full Integration)

**Goal:** Power MCP4728 from powerboost 5V output.

#### Step 4.1: Wire MCP4728 to Powerboost 5V

**Materials:**
- 22 AWG red wire (~10cm) - for VCC
- 22 AWG black wire (~10cm) - for GND

**Wiring Plan:**
```
Powerboost VOUT → MCP4728 VCC pin
Powerboost GND  → MCP4728 GND pin (in addition to STEMMA QT GND)
```

**Important:** MCP4728 will have TWO ground connections:
1. Via STEMMA QT cable (I2C ground reference)
2. Via powerboost GND (power supply ground)

This is **correct and safe** - all grounds are common.

#### Step 4.2: Solder Power Wires

1. **Identify MCP4728 Power Pins:**
   - **VCC Pin:** Labeled "VCC" or "V+" on breakout
   - **GND Pin:** Labeled "GND" or "-" (may have multiple)

2. **Solder Wires:**
   - Red wire: Powerboost VOUT → MCP4728 VCC
   - Black wire: Powerboost GND → MCP4728 GND

3. **Insulate:**
   - Heat shrink tubing on each connection
   - Verify no shorts between VCC and GND

#### Step 4.3: Pre-Power Final Check

**CRITICAL: Check these before powering on:**

- [ ] **Powerboost Configuration:**
  - Pads A=0, B=0 (both open)
  - VIN connected to Feather BAT
  - GND connected to Feather GND
  - VOUT connected to MCP4728 VCC
  - GND connected to MCP4728 GND

- [ ] **MCP4728 Connections:**
  - VCC connected to Powerboost VOUT
  - GND connected to Powerboost GND
  - STEMMA QT connected to OLED FeatherWing
  - No shorts between VCC and GND (use multimeter continuity test)

- [ ] **Battery:**
  - Voltage 3.0V - 4.2V (checked with multimeter)
  - JST connector ready to plug into Feather
  - No damage, swelling, or discoloration

- [ ] **Workspace:**
  - LiPo safety bag nearby
  - Fire extinguisher accessible
  - Non-flammable work surface
  - Good lighting and ventilation

#### Step 4.4: Power On - Full System Test

**This is the moment of truth!**

1. **Connect Battery:**
   - Plug JST connector into Feather M4
   - Observe (look for ANY signs of problems):
     - [ ] OLED lights up (displays Arp menu)
     - [ ] No smoke or unusual smells
     - [ ] No components getting hot
     - [ ] No sparks or crackling sounds

2. **Measure Voltages:**
   ```
   Checkpoint 1: Battery Voltage
   Multimeter → Battery terminals (can read at Feather BAT pin)
   Expected: 3.7V - 4.2V

   Checkpoint 2: Powerboost Output
   Multimeter → Powerboost VOUT to GND
   Expected: 5.0V ± 0.2V

   Checkpoint 3: MCP4728 VCC
   Multimeter → MCP4728 VCC pin to GND
   Expected: 5.0V ± 0.2V (same as powerboost)
   ```

3. **Connect USB (Charging Test):**
   - Plug USB-C into Feather
   - Observe:
     - [ ] Orange charge LED lights up
     - [ ] OLED still working
     - [ ] All voltages remain stable

4. **I2C Bus Scan Test:**
   - Deploy test code to scan I2C bus
   - Expected devices:
     - **0x3C** - OLED Display (SH1107)
     - **0x60** - MCP4728 DAC

   - We'll do this in next section (Testing & Verification)

---

## Testing & Verification {#testing-verification}

### Test 1: I2C Bus Scan

**Deploy test code to verify all I2C devices detected:**

1. **Create test file:**
   ```python
   # /Volumes/CIRCUITPY/code.py
   import board
   import time

   print("\n" + "="*50)
   print("Battery + MCP4728 Integration Test")
   print("="*50)

   # Test 1: I2C Bus Scan
   print("\n[TEST 1] I2C Bus Scan...")

   try:
       i2c = board.I2C()
       while not i2c.try_lock():
           pass

       devices = i2c.scan()
       i2c.unlock()

       print(f"  Found {len(devices)} device(s):")

       oled_found = False
       dac_found = False

       for addr in devices:
           name = "Unknown"
           if addr == 0x3C:
               name = "OLED Display (SH1107)"
               oled_found = True
           elif addr == 0x60:
               name = "MCP4728 DAC"
               dac_found = True
           elif addr == 0x64:
               name = "MCP4728A4 DAC (alt address)"
               dac_found = True

           marker = "✓" if addr in [0x3C, 0x60, 0x64] else " "
           print(f"    [{marker}] 0x{addr:02X} - {name}")

       if oled_found and dac_found:
           print("\n  ✅ SUCCESS: Both OLED and DAC detected!")
       elif oled_found:
           print("\n  ⚠ OLED found, but DAC NOT detected")
           print("  Check MCP4728 power (should be 5V)")
       elif dac_found:
           print("\n  ⚠ DAC found, but OLED NOT detected")
           print("  Check OLED power and I2C connection")
       else:
           print("\n  ❌ ERROR: No devices found")
           print("  Check I2C wiring (SDA, SCL, GND)")

   except Exception as e:
       print(f"\n  ❌ I2C scan failed: {e}")

   print("\n" + "="*50)

   while True:
       time.sleep(1)
   ```

2. **Deploy and monitor:**
   ```bash
   # Copy to device
   cp test_battery_integration.py /Volumes/CIRCUITPY/code.py

   # Monitor output
   python3 scripts/monitor_serial.py --duration 10
   ```

3. **Expected Output:**
   ```
   ==================================================
   Battery + MCP4728 Integration Test
   ==================================================

   [TEST 1] I2C Bus Scan...
     Found 2 device(s):
       [✓] 0x3C - OLED Display (SH1107)
       [✓] 0x60 - MCP4728 DAC

     ✅ SUCCESS: Both OLED and DAC detected!

   ==================================================
   ```

### Test 2: Battery Voltage Reading

**Read battery voltage via analog input:**

```python
import board
import analogio
import time

# Initialize battery voltage monitor
vbat = analogio.AnalogIn(board.VOLTAGE_MONITOR)  # A5/VBAT pin

print("\n[TEST 2] Battery Voltage Reading...")

for i in range(5):
    # Read raw ADC value (0-65535)
    raw = vbat.value

    # Convert to voltage
    # Feather M4 has voltage divider: VBAT → 1MΩ → A5 → 1MΩ → GND
    # So A5 reads VBAT / 2
    voltage = (raw / 65535.0) * 3.3 * 2

    print(f"  Reading {i+1}: {voltage:.2f}V (raw: {raw})")
    time.sleep(1)

print("\n  ✅ Battery voltage readings complete")
```

**Expected Output:**
```
[TEST 2] Battery Voltage Reading...
  Reading 1: 3.98V (raw: 39845)
  Reading 2: 3.98V (raw: 39840)
  Reading 3: 3.97V (raw: 39820)
  Reading 4: 3.98V (raw: 39850)
  Reading 5: 3.98V (raw: 39855)

  ✅ Battery voltage readings complete
```

**Interpretation:**
- **4.2V:** Fully charged
- **3.7-4.0V:** Good charge
- **3.5-3.7V:** Moderate charge (50-70%)
- **3.3-3.5V:** Low battery warning
- **< 3.3V:** Critical - display warning and reduce power usage

### Test 3: MCP4728 DAC Initialization

**Initialize DAC and test basic output:**

```python
import board
import busio
import adafruit_mcp4728
import time

print("\n[TEST 3] MCP4728 DAC Initialization...")

try:
    # Initialize I2C
    i2c = board.I2C()

    # Initialize DAC
    dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
    print("  ✓ DAC initialized at 0x60")

    # Configure all channels
    for idx, channel in enumerate([dac.channel_a, dac.channel_b,
                                   dac.channel_c, dac.channel_d]):
        channel.vref = adafruit_mcp4728.Vref.INTERNAL
        channel.gain = 1  # 1x gain
        channel.value = 0  # Start at 0V

        ch_name = chr(65 + idx)  # A, B, C, D
        print(f"  ✓ Channel {ch_name}: Vref=INTERNAL, Gain=1x, Value=0")

    print("\n  Testing Channel A output (0V → 2.5V → 5V)...")

    # Test voltage sequence
    for voltage in [0.0, 2.5, 5.0]:
        dac_value = int((voltage / 5.0) * 4095)
        dac.channel_a.value = dac_value
        print(f"    Set {voltage:.1f}V (DAC value = {dac_value})")
        print(f"    → Measure Channel A (VA pin) with multimeter")
        time.sleep(3)

    # Reset to 0V
    dac.channel_a.value = 0
    print(f"\n  ✓ Channel A reset to 0V")

    print("\n  ✅ MCP4728 DAC test complete")

except Exception as e:
    print(f"\n  ❌ DAC test failed: {e}")
    print(f"  Check power (VCC should be 5V)")
```

**Use multimeter to verify voltages match expected values (±0.1V).**

### Test 4: OLED Display Test

**Verify OLED still works with full system powered:**

```python
import board
import displayio
import i2cdisplaybus
import adafruit_displayio_sh1107
from adafruit_display_text import label
import terminalio

print("\n[TEST 4] OLED Display Test...")

# Initialize display
i2c = board.I2C()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)

# Create text
splash = displayio.Group()
text = label.Label(
    terminalio.FONT,
    text="Battery + DAC\\nIntegration\\nSUCCESS!",
    color=0xFFFFFF,
    x=10,
    y=10
)
splash.append(text)
display.root_group = splash

print("  ✓ OLED displaying test message")
print("  → Verify 'Battery + DAC Integration SUCCESS!' on screen")
print("\n  ✅ OLED display test complete")
```

### Test 5: Current Draw Measurement

**Measure system current draw to estimate battery life:**

**Method 1: USB Current Meter (if available)**
- Insert USB current meter between USB cable and Feather
- Read current draw in mA
- Typical values:
  - Idle (OLED on, no MIDI): 50-80mA
  - Active (arpeggiating): 80-120mA
  - Peak (MIDI + DAC + display updates): 120-150mA

**Method 2: Multimeter in Series**
- **CAUTION:** Requires breaking battery connection
- Set multimeter to current mode (200mA range)
- Connect in series: Battery + → Multimeter → Feather BAT
- Read current draw

**Battery Life Estimate:**
```
Battery Capacity (mAh) / Current Draw (mA) = Runtime (hours)

Example:
500mAh battery / 100mA average = 5 hours
1200mAh battery / 100mA average = 12 hours

With safety margin (discharge to 3.3V only, not fully drained):
Usable capacity ≈ 80% of rated capacity
500mAh × 0.8 = 400mAh → 4 hours runtime
1200mAh × 0.8 = 960mAh → 9.6 hours runtime
```

---

## Troubleshooting {#troubleshooting}

### OLED Not Displaying

**Symptom:** OLED blank after connecting MCP4728

**Possible Causes:**
1. **Power overload on 3.3V rail**
   - Check: Is MCP4728 VCC connected to 5V powerboost (NOT 3.3V STEMMA QT)?
   - Fix: Verify MCP4728 VCC wired to Powerboost VOUT

2. **I2C bus conflict**
   - Check: Run I2C scan, verify both 0x3C and 0x60 detected
   - Fix: Reseat STEMMA QT cable

3. **Low battery voltage**
   - Check: Measure battery voltage (should be > 3.3V)
   - Fix: Charge battery via USB

### MCP4728 Not Detected on I2C

**Symptom:** I2C scan shows 0x3C but not 0x60

**Possible Causes:**
1. **No power to MCP4728**
   - Check: Measure MCP4728 VCC pin (should be 5V)
   - Fix: Check powerboost wiring, verify VOUT = 5V

2. **STEMMA QT cable loose**
   - Check: Verify cable seated on both ends
   - Fix: Reseat cable, check for bent pins

3. **Wrong I2C address**
   - Check: Some MCP4728 boards use 0x64 instead of 0x60
   - Fix: Try `dac = adafruit_mcp4728.MCP4728(i2c, address=0x64)`

### Powerboost Not Outputting 5V

**Symptom:** Powerboost VOUT reads 0V or < 4.5V

**Possible Causes:**
1. **Input voltage too low**
   - Check: Measure battery voltage (should be > 2.5V)
   - Fix: Charge battery

2. **Input voltage too high**
   - Check: If using USB 5V, this exceeds max input (4.5V) for 5V output mode
   - Fix: Use battery (3.7V) instead of USB 5V

3. **Pad configuration wrong**
   - Check: Verify pads A=0, B=0 (both open)
   - Fix: Desolder any bridges on pads A or B

4. **Powerboost damaged**
   - Check: Visual inspection for burnt components
   - Fix: Replace powerboost module

### Battery Not Charging

**Symptom:** Orange LED doesn't light when USB connected

**Possible Causes:**
1. **Battery already full**
   - Check: Measure battery voltage (if 4.2V, it's full)
   - Fix: None needed - this is normal

2. **USB cable bad**
   - Check: Try different USB cable
   - Fix: Use USB cable that supports data + power

3. **Feather charging circuit fault**
   - Check: Measure USB voltage at Feather USB pin (should be 5V)
   - Fix: If 0V, Feather may have damaged USB protection circuit

### Battery Drains Too Fast

**Symptom:** Battery goes from 4.2V to 3.3V in < 2 hours

**Possible Causes:**
1. **High current draw**
   - Check: Measure current with multimeter (should be 50-150mA)
   - Fix: If > 200mA, check for shorts or faulty components

2. **Battery capacity lower than expected**
   - Check: Battery label (actual vs rated capacity)
   - Fix: Use larger battery (1200mAh instead of 500mAh)

3. **Old/damaged battery**
   - Check: Battery age (LiPo capacity degrades over time)
   - Fix: Replace battery if > 2 years old or shows swelling

---

## Software Integration {#software-integration}

### Step 1: Add Battery Voltage Monitoring

**Create `arp/utils/battery.py`:**

```python
"""
Battery Monitor
Monitors LiPo battery voltage and provides low-battery warnings
"""

import board
import analogio

class BatteryMonitor:
    """Monitors battery voltage via VBAT pin (A5)"""

    # Voltage thresholds
    VBAT_FULL = 4.2      # Fully charged
    VBAT_NOMINAL = 3.7   # Normal operating voltage
    VBAT_LOW = 3.5       # Low battery warning
    VBAT_CRITICAL = 3.3  # Critical - shutdown soon
    VBAT_MIN = 3.0       # Absolute minimum (damage risk)

    def __init__(self):
        """Initialize battery monitor"""
        try:
            self.vbat_pin = analogio.AnalogIn(board.VOLTAGE_MONITOR)
            self.available = True
        except Exception as e:
            print(f"Warning: Battery monitor not available: {e}")
            self.available = False
            self.vbat_pin = None

        self.last_voltage = 0.0
        self.voltage_history = []  # For averaging

    def read_voltage(self):
        """
        Read battery voltage

        Returns:
            float: Battery voltage (0.0 if unavailable)
        """
        if not self.available:
            return 0.0

        try:
            # Read raw ADC value (0-65535)
            raw = self.vbat_pin.value

            # Convert to voltage
            # Feather M4 voltage divider: VBAT/2 → A5
            voltage = (raw / 65535.0) * 3.3 * 2.0

            # Store for averaging
            self.voltage_history.append(voltage)
            if len(self.voltage_history) > 10:
                self.voltage_history.pop(0)

            # Return averaged voltage
            self.last_voltage = sum(self.voltage_history) / len(self.voltage_history)
            return self.last_voltage

        except Exception as e:
            print(f"Error reading battery: {e}")
            return 0.0

    def get_percentage(self):
        """
        Get battery charge percentage (rough estimate)

        Returns:
            int: 0-100 percentage
        """
        voltage = self.last_voltage or self.read_voltage()

        # Linear approximation (not accurate, but simple)
        # 3.3V = 0%, 4.2V = 100%
        percentage = ((voltage - self.VBAT_MIN) / (self.VBAT_FULL - self.VBAT_MIN)) * 100
        return max(0, min(100, int(percentage)))

    def get_status(self):
        """
        Get battery status string

        Returns:
            str: "FULL", "GOOD", "LOW", "CRITICAL", or "UNKNOWN"
        """
        voltage = self.last_voltage or self.read_voltage()

        if voltage >= self.VBAT_FULL:
            return "FULL"
        elif voltage >= self.VBAT_NOMINAL:
            return "GOOD"
        elif voltage >= self.VBAT_LOW:
            return "LOW"
        elif voltage >= self.VBAT_CRITICAL:
            return "CRITICAL"
        else:
            return "UNKNOWN"

    def is_low(self):
        """Check if battery is low"""
        return self.last_voltage < self.VBAT_LOW

    def is_critical(self):
        """Check if battery is critical"""
        return self.last_voltage < self.VBAT_CRITICAL
```

### Step 2: Update Display to Show Battery Status

**Modify `arp/ui/display.py`:**

Add battery indicator to status line:
```python
# In update_status() method:
def update_status(self, pattern, bpm, battery_voltage=0.0):
    """
    Update status line with pattern, BPM, and battery

    Args:
        pattern: Current pattern name
        bpm: Current BPM
        battery_voltage: Battery voltage (0.0 if unavailable)
    """
    # Existing code...

    # Add battery indicator
    if battery_voltage > 0:
        if battery_voltage >= 4.0:
            battery_icon = "█"  # Full
        elif battery_voltage >= 3.7:
            battery_icon = "▓"  # Good
        elif battery_voltage >= 3.5:
            battery_icon = "▒"  # Low
        else:
            battery_icon = "!"  # Critical

        status_text = f"{pattern} {bpm}BPM {battery_icon}{battery_voltage:.1f}V"
    else:
        status_text = f"{pattern} {bpm}BPM [USB]"

    # Update display...
```

### Step 3: Integrate into Main Loop

**Modify `main.py`:**

```python
# Add battery monitor
from prisme.utils.battery import BatteryMonitor

# Initialize
battery = BatteryMonitor()

# In main loop:
while True:
    # Read battery periodically (every 10 seconds)
    if time.monotonic() - last_battery_check > 10.0:
        voltage = battery.read_voltage()
        last_battery_check = time.monotonic()

        # Update display with battery info
        display.update_status(pattern, bpm, voltage)

        # Check for low battery
        if battery.is_critical():
            display.show_warning("LOW BATTERY\\nSHUTDOWN SOON")
            # TODO: Reduce power usage (dim display, lower update rate)
```

---

## Integration Complete! 🎉

**If all tests pass, you now have:**

✅ LiPo battery integrated and charging
✅ Battery voltage monitoring via software
✅ Powerboost generating stable 5V from battery
✅ MCP4728 DAC powered and detected on I2C
✅ OLED display working alongside DAC
✅ Complete system running on battery power

**Next Steps:**

1. **Run Full MCP4728 Test:** Deploy `tests/test_mcp4728_dac.py` and verify CV/Gate outputs
2. **Integrate CV/Gate into Main App:** Update `main.py` to output CV pitch and gate
3. **Test Battery Life:** Run arpeggiator for 1 hour, measure battery drain rate
4. **Update Documentation:** Record final wiring configuration and test results

---

**Document Version:** 1.0
**Last Updated:** 2025-10-23
**Status:** Ready for implementation
