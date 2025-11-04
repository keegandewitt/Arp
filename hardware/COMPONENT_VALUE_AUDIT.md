# Component Value Audit & Standardization

**Date:** 2025-11-04 (Session 27)
**Purpose:** Fix inconsistent component values across ALL documentation
**Issue:** Found LED resistor values varying between 150Ω, 220Ω, 330Ω, and 1kΩ

---

## 🔍 AUDIT FINDINGS

### ❌ INCONSISTENT: LED Current Limiting Resistors

**Found in documentation:**
- 150Ω (most common - in PIN_ALLOCATION_MATRIX, COMPREHENSIVE_HARDWARE_AUDIT, JACK_WIRING_GUIDE, etc.)
- 220Ω (in PRODUCTION_ROADMAP, user preference)
- 330Ω (in EASYEDA_PCB_DESIGN_GUIDE for RGB LEDs, my unified schematic)
- 1kΩ (in EASYEDA_PCB_DESIGN_GUIDE for white LEDs, my unified schematic)

**Electrical analysis:**
- 150Ω @ 3.3V = ~2mA (white), ~8.7mA (RGB red)
- 220Ω @ 3.3V = ~1.4mA (white), ~5.9mA (RGB red)
- 330Ω @ 3.3V = ~0.9mA (white), ~3.9mA (RGB red)
- 1kΩ @ 3.3V = ~0.3mA (white) - TOO DIM!

**Decision:** **220Ω for ALL LEDs**
- Most common resistor value (E12/E24 series, in every kit)
- Good brightness for indicators
- Single BOM line item
- User explicitly requested this value

### ✅ CONSISTENT: Voltage Dividers (Input Protection)

**Value:** 2× 10kΩ (for each input)
**Usage:** CV IN (A3), TRIG IN (A4)
**Documented in:** ACTUAL_HARDWARE_TRUTH, EASYEDA_PCB_DESIGN_GUIDE, all schematics
**Status:** ✓ No changes needed

### ✅ CONSISTENT: DAC Output Protection

**Value:** 100Ω series resistors
**Usage:** CV OUT, CC OUT, all DAC outputs
**Documented in:** ACTUAL_HARDWARE_TRUTH, EASYEDA_PCB_DESIGN_GUIDE
**Status:** ✓ No changes needed

### ✅ CONSISTENT: S-Trig Transistor Circuit

**Base resistor:** 1kΩ (GPIO D10 → 2N3904 base)
**Collector resistor:** 100Ω (protection)
**Documented in:** ACTUAL_HARDWARE_TRUTH, EASYEDA_PCB_DESIGN_GUIDE
**Status:** ✓ No changes needed

### ✅ CONSISTENT: Power Rails

**5V rail:** USB-C → M4 USB pin → devices
**3.3V rail:** M4 3V3 pin (onboard LDO, 500mA capacity)
**Documented in:** POWER_DISTRIBUTION.svg, ACTUAL_HARDWARE_TRUTH, EASYEDA_PCB_DESIGN_GUIDE
**Status:** ✓ No changes needed (Session 27 removed battery/powerboost)

---

## 📝 STANDARDIZED VALUES (Official BOM)

### Resistors

| Value | Quantity | Purpose | Designators | Notes |
|-------|----------|---------|-------------|-------|
| **100Ω** | 5 | DAC output protection + S-Trig | R_OUT1-4, R_STRIG | Series protection |
| **220Ω** | 11 | **LED current limiting (ALL)** | **R_LED1-11** | **STANDARDIZED VALUE** |
| **1kΩ** | 1 | S-Trig transistor base | R_BASE | Current limiting |
| **10kΩ** | 4 | Input voltage dividers | R1-R5 | 2 per input (CV, TRIG) |

**Total resistors:** 21

### LEDs

| Type | Quantity | Current | Resistor | Pins |
|------|----------|---------|----------|------|
| White 3mm | 5 | ~1.4mA | 220Ω | D4, D12, D25, CAN_TX, A5 |
| RGB 5mm (common cathode) | 2 | ~6mA (red), ~1.4mA (green/blue) | 220Ω (×6 channels) | D11/D23/D24, A0/A1/A2 |

**Total resistors for LEDs:** 11× 220Ω

---

## 🔧 FILES THAT NEED UPDATES

### High Priority (User-facing, PCB design):

1. **hardware/EASYEDA_PCB_DESIGN_GUIDE.md**
   - Change: 1kΩ → 220Ω for white LEDs
   - Change: 330Ω → 220Ω for RGB LEDs
   - Update BOM table

2. **hardware/ACTUAL_HARDWARE_TRUTH.md**
   - Add explicit LED resistor values (currently TBD)
   - Standardize on 220Ω

3. **docs/hardware/PIN_ALLOCATION_MATRIX.md**
   - Change: 150Ω → 220Ω throughout

4. **hardware/enclosure/CURRENT_SCHEMATICS/README.md**
   - Change: 1kΩ → 220Ω for white LEDs
   - Change: 330Ω → 220Ω for RGB LEDs

5. **hardware/enclosure/generate_unified_system_schematic_v2.py**
   - Regenerate schematic with 220Ω values

### Medium Priority (Reference docs):

6. **docs/hardware/COMPREHENSIVE_HARDWARE_AUDIT.md**
   - Change: 150Ω → 220Ω throughout

7. **docs/hardware/JACK_WIRING_GUIDE.md**
   - Change: 150Ω → 220Ω throughout

8. **docs/hardware/PROTOBOARD_LAYOUT.md**
   - Change: 150Ω → 220Ω throughout

9. **hardware/SCHEMATIC_STATUS.md**
   - Change: 150Ω → 220Ω throughout

### Low Priority (Archive/historical):

10. Various other docs with 150Ω, 330Ω, 1kΩ references
    - Update for consistency but less critical

---

## ✅ VERIFICATION CHECKLIST

After updates:
- [ ] All LED resistors = 220Ω
- [ ] All voltage dividers = 10kΩ + 10kΩ
- [ ] All DAC protection = 100Ω
- [ ] S-Trig base = 1kΩ
- [ ] S-Trig collector = 100Ω
- [ ] Power rails = USB 5V, M4 3.3V (no battery)
- [ ] BOM updated in EASYEDA_PCB_DESIGN_GUIDE.md
- [ ] Schematics regenerated with correct values

---

## 📊 IMPACT SUMMARY

**Before standardization:**
- 4 different LED resistor values in docs (150Ω, 220Ω, 330Ω, 1kΩ)
- Confusion about which to use
- Possible wrong values on breadboard/PCB

**After standardization:**
- Single value: 220Ω for ALL LEDs
- Clear, consistent documentation
- Simpler BOM (one resistor value for all 11 LED resistors)
- Common value, easy to source

---

**Status:** ✅ Audit complete, ready to implement fixes
**Next:** Update all 9 high/medium priority files with 220Ω LED resistors
