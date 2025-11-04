# Power System Simplification - Removing Battery & Powerboost

**Date:** 2025-11-04 (Session 27)
**Decision:** Remove battery and powerboost from design
**Rationale:** Simplify hardware, reduce cost, eliminate complexity

---

## 🎯 CHANGE SUMMARY

### What We're Removing:
- ❌ LiPo battery (500-2000mAh)
- ❌ Powerboost 1000C module
- ❌ Battery monitoring circuits
- ❌ Battery-related pin allocations
- ❌ Power switch for battery
- ❌ JST battery connectors

### What We're Keeping:
- ✅ **USB-C power input only**
- ✅ Feather M4's onboard 5V USB pin
- ✅ Feather M4's onboard 3.3V regulator
- ✅ All existing CV/Gate/MIDI functionality

---

## 📐 NEW POWER ARCHITECTURE

### Power Distribution (USB-only):

```
USB-C Connector (5V)
    ↓
Feather M4 USB pin (5V)
    ↓
    ├──→ M4 onboard 3.3V regulator
    │       ↓
    │    3.3V Rail:
    │       ├─→ OLED FeatherWing (I2C 0x3C)
    │       ├─→ MIDI FeatherWing circuits
    │       ├─→ 4× White status LEDs
    │       ├─→ 3× RGB LED channels (6 channels total)
    │       └─→ BAT85 input clamp diodes (if > 3.3V)
    │
    └──→ 5V Rail (direct from USB pin):
            ├─→ MCP4728 DAC (VDD = 5V)
            ├─→ CV/Gate output circuits
            └─→ Optional future 5V devices
```

### Power Specifications:

**USB-C Input:**
- Voltage: 5V DC
- Current: Typically 500mA (USB 2.0), up to 3A (USB 3.0 / USB-PD)
- Sufficient for all circuits

**5V Rail:**
- Source: Feather M4 USB pin (direct from USB-C)
- Max load: MCP4728 (~1-5mA) + future devices
- Total estimated: <50mA

**3.3V Rail:**
- Source: Feather M4 onboard regulator (from USB 5V)
- Regulator capacity: 500mA (more than sufficient)
- Current load:
  - OLED FeatherWing: ~20mA
  - MIDI FeatherWing: ~15mA
  - 7 LED channels @ 2-8mA each: ~30mA
  - Total: ~65mA typical

**Margin:** Plenty of headroom, no thermal concerns

---

## 📋 AFFECTED DOCUMENTATION

### Files That Need Updates:

1. **hardware/ACTUAL_HARDWARE_TRUTH.md**
   - Section 1: Power Supply System
   - Remove battery/powerboost references
   - Document USB-only architecture

2. **hardware/EASYEDA_PCB_DESIGN_GUIDE.md**
   - BOM: Remove battery, powerboost, JST connectors, power switch
   - Pin connections table: Update power section (USB pin instead of BAT)
   - Power distribution schematic references

3. **hardware/enclosure/POWER_DISTRIBUTION.svg**
   - Regenerate schematic showing USB-only power
   - Remove battery and powerboost components
   - Show USB-C → M4 USB pin → 5V/3.3V rails

4. **docs/hardware/PIN_ALLOCATION_MATRIX.md**
   - Remove any battery monitoring pin allocations
   - Clarify USB pin usage

5. **docs/hardware/BOM.md**
   - Remove LiPo battery line items
   - Remove powerboost module
   - Remove slide switch (if power-related)

6. **docs/ARCHITECTURE.md**
   - Update power system section
   - Remove battery life estimates

7. **Other affected files:**
   - docs/SESSION_13_HANDOFF.md (historical, archive only)
   - docs/hardware/MCP4728_WORKING_SETUP.md (may need power section update)
   - docs/hardware/CV_OPAMP_CIRCUIT.md (referenced 12V from powerboost - obsolete)
   - docs/hardware/BREADBOARD_WALKTHROUGH.md (referenced powerboost config)

---

## ✅ BENEFITS OF THIS CHANGE

1. **Simplified Design:**
   - No battery charging circuitry
   - No power switch needed
   - No battery level monitoring

2. **Reduced Cost:**
   - No LiPo battery ($8-13)
   - No powerboost module (~$20-25)
   - No JST connectors
   - No power switch

3. **Improved Reliability:**
   - No battery degradation over time
   - No charging failures
   - Simpler troubleshooting

4. **Cleaner PCB Layout:**
   - Fewer components to route
   - More space for other features
   - Simpler power plane design

5. **Safer:**
   - No LiPo fire/swelling risk
   - No battery overcharge concerns

---

## ⚠️ TRADE-OFFS

**What We Lose:**
- ❌ Portable/mobile operation (must be plugged in)
- ❌ Battery backup during power interruption

**Why It's Acceptable:**
- Device is intended for studio/desktop use
- USB power is ubiquitous (laptops, USB chargers, power banks)
- Most MIDI/CV gear is powered, not battery-operated
- Reduces complexity significantly

**User Can Still Use Portable Power:**
- USB power bank (if needed)
- Laptop USB port (when mobile)
- USB wall adapter (studio setup)

---

## 📊 POWER BUDGET (USB-Only)

| Rail | Source | Consumers | Typical Current | Max Current | Headroom |
|------|--------|-----------|-----------------|-------------|----------|
| **5V** | USB-C (500mA min) | MCP4728 DAC | 1-5mA | 10mA | 98% free |
| **3.3V** | M4 Regulator (500mA) | OLED, MIDI, LEDs | 65mA | 100mA | 80% free |

**Total USB Load:** ~75mA typical, ~120mA max
**USB 2.0 Minimum:** 500mA
**Margin:** 4× safety factor

---

## 🔧 IMPLEMENTATION NOTES

### PCB Design Changes:

1. **Remove Components:**
   - No JST battery connector pads
   - No powerboost mounting holes/traces
   - No power switch footprint

2. **USB-C Connection:**
   - Use Adafruit USB-C breakout board (or equivalent)
   - 4 pins: VBUS (5V), GND, D+, D- (data not used for power)
   - Route VBUS to Feather M4 USB pin
   - Route GND to common ground plane

3. **Power Decoupling (Still Required):**
   - 5V rail: 47µF + 0.1µF near MCP4728
   - 3.3V rail: 10µF + 0.1µF near high-speed digital (OLED, MIDI)

4. **Schematic Simplification:**
   - Power section becomes trivial: USB → M4 → 5V/3.3V rails
   - No voltage boost/buck circuits
   - No battery monitoring

---

## 📝 SCHEMATIC UPDATES REQUIRED

### POWER_DISTRIBUTION.svg Needs:

**Remove:**
- Battery symbol
- Powerboost module block
- Power switch
- JST connector

**Add/Keep:**
- USB-C connector symbol
- Feather M4 USB pin
- M4 3.3V pin
- Decoupling capacitors (both rails)
- Clean 5V and 3.3V distribution buses

**Layout:**
```
USB-C Connector (5V, GND)
    ↓
[Feather M4]
    ├─ USB pin → 5V rail (+ decoupling)
    └─ 3V3 pin → 3.3V rail (+ decoupling)
```

---

## 🎯 NEXT STEPS

1. ✅ Create this documentation (POWER_SYSTEM_SIMPLIFICATION.md)
2. ⏳ Update ACTUAL_HARDWARE_TRUTH.md (Power Supply System section)
3. ⏳ Update EASYEDA_PCB_DESIGN_GUIDE.md (BOM + pin connections)
4. ⏳ Regenerate POWER_DISTRIBUTION.svg schematic
5. ⏳ Update PIN_ALLOCATION_MATRIX.md (remove battery monitoring)
6. ⏳ Update BOM.md (remove battery items)
7. ⏳ Update ARCHITECTURE.md (power section)
8. ⏳ Commit all changes with clear message
9. ⏳ Update CONTEXT.md session handoff

---

## 📚 REFERENCES

**Feather M4 CAN Express Power Pins:**
- **USB:** 5V power input when connected via USB-C
- **3V3:** Regulated 3.3V output from onboard regulator (500mA max)
- **GND:** Common ground
- **EN:** Enable pin (not used in our design)

**Datasheet:** https://learn.adafruit.com/adafruit-feather-m4-can-express

---

**Status:** ✅ Architecture defined, ready to update documentation
**Session:** 27 (2025-11-04)
**Next:** Update all affected hardware documentation files
