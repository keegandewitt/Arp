# Unified System Schematic - Coordinate Plan

**Date:** 2025-11-04 (Session 27)
**Purpose:** Mathematical coordinate planning BEFORE generating schematic
**Lesson:** Session 26 failed due to improvisational placement - this time we calculate first!

---

## LAYOUT STRATEGY

### Horizontal Sections (X-axis):
```
X = 0-4:    Power system (USB-C → M4 → Rails)
X = 5-10:   Feather M4 block (center, large)
X = 11-15:  Input circuits (TOP PCB)
X = 16-20:  Output circuits (BOTTOM PCB)
```

### Vertical Sections (Y-axis):
```
Y = 16-20:  Title and notes
Y = 11-15:  Power distribution
Y = 6-10:   Input circuits (CV IN, TRIG IN)
Y = 1-5:    Output circuits (CV OUT, TRIG OUT, CC OUT)
Y = -4-0:   MIDI circuits (IN/OUT)
Y = -9--5:  Component values table
```

---

## DETAILED COORDINATES

### 1. TITLE SECTION (Y = 16-20)
- (0, 19): Title "PRISME UNIFIED SYSTEM SCHEMATIC"
- (0, 18): Subtitle "Complete Hardware Interconnection Diagram"
- (0, 17): Date and session info

### 2. POWER SYSTEM (X = 0-4, Y = 11-15)
- (0, 15): USB-C connector symbol
- (0, 14): USB +5V line
- (0, 13): USB GND line
- (2, 14): M4 USB pin connection point
- (2, 13): 5V rail distribution
- (2, 12): 3.3V rail distribution
- (0, 12): Ground symbol

### 3. FEATHER M4 BLOCK (X = 5-10, Y = 6-15)
**Box coordinates:**
- Top-left: (5, 15)
- Top-right: (10, 15)
- Bottom-left: (5, 6)
- Bottom-right: (10, 6)

**Pin labels inside box (Y = 14 down to Y = 7):**
- (7.5, 14): "Feather M4 CAN"
- (7.5, 13.5): "USB → 5V"
- (7.5, 13): "3V3 → 3.3V"
- (7.5, 12): "SDA/SCL → I2C"
- (7.5, 11): "RX/TX → MIDI"
- (7.5, 10): "A3 ← CV IN"
- (7.5, 9): "A4 ← TRIG IN"
- (7.5, 8): "D4 → CV IN LED"
- (7.5, 7): "D11/D23/D24 → TRIG IN RGB"

**Connection points (dots):**
- Left side (power): (5, 13), (5, 12.5), (5, 12)
- Right side (inputs): (10, 10), (10, 9), (10, 8), (10, 7)
- Bottom side (outputs): (7, 6), (8, 6), (9, 6)

### 4. INPUT CIRCUITS - TOP PCB (X = 11-15, Y = 6-10)

**CV IN circuit (Y = 9-10):**
- (11, 10): CV IN jack symbol
- (11.5, 10): R1 (10kΩ) series
- (12, 10): Voltage divider TAP
- (12, 9.5): R2 (10kΩ) to GND
- (12.5, 10): BAT85 diode to 3.3V
- (13, 10): Line to A3
- (13.5, 10): R3 (1kΩ) for LED
- (14, 10): LED1 (white) symbol
- (14.5, 10): Label "D4 → CV IN LED"

**TRIG IN circuit (Y = 7-8):**
- (11, 8): TRIG IN jack symbol
- (11.5, 8): R4 (10kΩ) series
- (12, 8): Voltage divider TAP
- (12, 7.5): R5 (10kΩ) to GND
- (12.5, 8): BAT85 diode to 3.3V
- (13, 8): Line to A4
- (13.5, 8): R6 (330Ω) for RGB
- (14, 8): RGB LED2 symbol (3 channels)
- (14, 7.8): Red channel (D11)
- (14, 7.6): Green channel (D23)
- (14, 7.4): Blue channel (D24)

### 5. OUTPUT CIRCUITS - BOTTOM PCB (X = 16-20, Y = 1-5)

**CV OUT circuit (Y = 5):**
- (16, 5): From M4 via I2C label
- (16.5, 5): MCP4728 Ch A block
- (17, 5): R7 (100Ω) series protection
- (17.5, 5): CV OUT jack symbol
- (18, 5): R8 (1kΩ) for LED
- (18.5, 5): LED3 (white) symbol
- (19, 5): Label "D12 → CV OUT LED"

**TRIG OUT circuit (Y = 3-4):**
- (16, 4): MCP4728 Ch C block (V-Trig)
- (16, 3): GPIO D10 + transistor block (S-Trig)
- (17, 3.5): Mode switch symbol
- (17.5, 3.5): TRIG OUT jack symbol
- (18, 3.5): R9 (330Ω) for RGB
- (18.5, 3.5): RGB LED4 symbol
- (18.5, 3.3): Red (A0) S-Trig mode
- (18.5, 3.1): Green (A1) V-Trig mode
- (18.5, 2.9): Blue (A2) reserved

**CC OUT circuit (Y = 2):**
- (16, 2): MCP4728 Ch D block
- (17, 2): R10 (100Ω) series protection
- (17.5, 2): CC OUT jack symbol
- (18, 2): R11 (1kΩ) for LED
- (18.5, 2): LED5 (white) symbol
- (19, 2): Label "D25 → CC OUT LED"

### 6. MIDI CIRCUITS (X = 16-20, Y = -1 to -3)

**MIDI OUT (Y = -1):**
- (16, -1): From M4 TX label
- (16.5, -1): MIDI FeatherWing block
- (17.5, -1): MIDI OUT DIN jack
- (18, -1): R12 (1kΩ) for LED
- (18.5, -1): LED6 (white) symbol
- (19, -1): Label "CAN_TX → MIDI OUT LED"

**MIDI IN (Y = -2):**
- (16, -2): To M4 RX label
- (16.5, -2): MIDI FeatherWing block
- (17.5, -2): MIDI IN DIN jack
- (18, -2): R13 (1kΩ) for LED
- (18.5, -2): LED7 (white) symbol
- (19, -2): Label "A5 → MIDI IN LED"

### 7. COMPONENT VALUES TABLE (Y = -5 to -9)
- (0, -5): "COMPONENT VALUES"
- (0, -6): "Resistors: 10kΩ (voltage dividers), 100Ω (output protection)"
- (0, -7): "          1kΩ (white LED), 330Ω (RGB LED)"
- (0, -8): "Diodes: BAT85 Schottky (30V, 200mA)"
- (0, -9): "LEDs: 5× white 3mm, 2× RGB 5mm common cathode"

### 8. NOTES SECTION (Y = -10 to -12)
- (0, -10): "NOTES:"
- (0, -11): "• All 7 LEDs included (4 white input/output, 2 RGB mode indicators, 1 white MIDI)"
- (0, -12): "• Power: USB-C only (no battery) - See POWER_DISTRIBUTION.svg"

---

## SPACING RULES

1. **Minimum horizontal spacing:** 0.5 units between adjacent components
2. **Minimum vertical spacing:** 0.5 units between circuit rows
3. **LED offset from jack:** 1.0 unit to the right
4. **Text label offset:** 0.5 units from component
5. **Ground symbols:** Always 0.5 units below lowest component

---

## VERIFICATION CHECKLIST

Before generating:
- [ ] All X coordinates unique per component (no overlap)
- [ ] All Y coordinates allow 0.5 unit minimum spacing
- [ ] All 7 LEDs positioned and labeled
- [ ] All resistor values documented
- [ ] Power connections clear
- [ ] M4 pin connections labeled
- [ ] MCP4728 channels identified
- [ ] MIDI FeatherWing shown separately (breadboard)

---

**Status:** ✅ Coordinate plan complete - ready to generate schematic
**Next:** Create `generate_unified_system_schematic_v2.py` using these exact coordinates
