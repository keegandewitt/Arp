# Bill of Materials (BOM)
## MIDI Arpeggiator with CV Output - Desktop Enclosure

---

## Electronics - Core Components

| Item | Qty | Unit Price | Total | Source | Notes |
|------|-----|------------|-------|--------|-------|
| **Adafruit Feather M4 CAN Express** | 1 | $24.95 | $24.95 | Adafruit #4759 | Main microcontroller with built-in USB-C charging |
| **Adafruit OLED FeatherWing** (128x32) | 1 | $14.95 | $14.95 | Adafruit #4650 | Display + 3 buttons (A, B, C) |
| **Adafruit MIDI FeatherWing** | 1 | $9.95 | $9.95 | Adafruit #4740 | MIDI In/Out with DIN-5 jacks |
| **Adafruit MCP4728 Quad DAC** | 1 | $8.95 | $8.95 | Adafruit #4470 | 4-channel 12-bit DAC with EEPROM (I2C: 0x60) |
| **LiPo Battery** (500-1200mAh, 3.7V) | 1 | $7.95 | $7.95 | Adafruit #258 or #328 | JST connector, capacity based on runtime needs |

**Subtotal (Core):** $66.75

---

## Power & Control Components

| Item | Qty | Unit Price | Total | Source | Notes |
|------|-----|------------|-------|--------|-------|
| **Teyleten Multi-Function Boost Module** | 1 | $0.70 | $0.70 | Amazon (pack of 10 for ~$7) | 3.7V→5V @ 1.5A boost converter |
| **Slide Switch Model 805** | 1 | $1.50 | $1.50 | Manufacturer/supplier TBD | Power distribution hub (battery → M4 + boost) |

**Subtotal (Power):** $2.20

---

## Connectors & Panel Hardware

| Item | Qty | Unit Price | Total | Source | Notes |
|------|-----|------------|-------|--------|-------|
| **3.5mm TRS Panel Mount Jacks** (Lsgoodcare 20-pack) | 2 | $0.50 | $1.00 | Amazon B01DBOBRHQ | CV Pitch + Gate outputs (mono wiring: Tip=signal, Ring+Sleeve=GND) - purchased as 20-pack (~$10) |
| **DIN-5 Panel Mount Jacks** | 2 | $2.50 | $5.00 | Generic | MIDI In/Out passthrough |
| **USB-C Panel Mount Extension** | 0 | $0.00 | $0.00 | N/A | Direct cutout in rear panel for M4's onboard USB-C |

**Subtotal (Connectors):** $6.00

---

## CV/Gate Output Components (Best Practice)

| Item | Qty | Unit Price | Total | Source | Notes |
|------|-----|------------|-------|--------|-------|
| **0.1µF Ceramic Capacitor** (50V) | 1 | $0.05 | $0.05 | Generic | Power decoupling for MCP4728 VCC |
| **100Ω Resistor** (1/4W) | 2 | $0.02 | $0.04 | Generic | Series protection on DAC OUT A and OUT B |

**Subtotal (CV/Gate Best Practice):** $0.09

**Purpose:**
- **Capacitor:** Filters 5V power noise, stabilizes DAC output voltage
- **Resistors:** Limit fault current if outputs shorted, protect DAC from damaged cables

**Note:** These components are optional but highly recommended for reliable CV/Gate operation.

---

## Fasteners & Hardware

| Item | Qty | Unit Price | Total | Source | Notes |
|------|-----|------------|-------|--------|-------|
| **M2.5 Screws** (6-10mm) | 10-20 | $0.10 | $1.00-2.00 | Generic hardware | FeatherWing stack mounting |
| **M3 Screws** (various lengths) | 10-15 | $0.15 | $1.50-2.25 | Generic hardware | Case assembly, module mounting |
| **M2.5/M3 Standoffs** | 10-15 | $0.20 | $2.00-3.00 | Generic hardware | Board spacing and support |
| **M2.5/M3 Nuts** | 10-15 | $0.05 | $0.50-0.75 | Generic hardware | Securing components |

**Subtotal (Hardware):** $5.00-8.00

---

## Enclosure Components (3D Printed)

| Item | Qty | Material Cost | Notes |
|------|-----|---------------|-------|
| **Main Enclosure Body** | 1 | ~$2-5 | PLA filament, Bambu A1 Mini, raw finish |
| **Top Lid/Cover** | 1 | ~$1-3 | Access to OLED and buttons |
| **Module Mounting Brackets/Trays** | 2-4 | ~$0.50-2 | DAC, boost module, switch mounting |
| **Connector Panel Inserts** | 2-3 | ~$0.50-1.50 | CV jacks, MIDI jacks, USB-C cutouts |

**Subtotal (3D Printed):** $4.00-11.50

---

## Wire & Cabling

| Item | Qty | Unit Price | Total | Notes |
|------|-----|------------|-------|-------|
| **22-24 AWG Stranded Wire** | 1m | $0.50/m | $0.50 | Power distribution wiring |
| **Heat Shrink Tubing** (assorted) | 1 pack | $3.00 | $3.00 | Insulating solder joints |
| **Jumper Wires** (F/F, M/F) | 10-15 | $0.10 | $1.00-1.50 | I2C, power connections |

**Subtotal (Wire):** $4.50-5.00

---

## Optional Components

| Item | Qty | Unit Price | Total | Source | Notes |
|------|-----|------------|-------|--------|-------|
| **Second MIDI FeatherWing** | 1 | $9.95 | $9.95 | Adafruit #4740 | For second MIDI clock input (if needed) |
| **Larger LiPo Battery** (2000mAh) | 1 | $12.95 | $12.95 | Adafruit #2011 | Extended runtime (12-14 hours) |
| **Rubber Feet** (adhesive) | 4 | $0.25 | $1.00 | Generic | Desktop stability |
| **Acrylic Window** (for OLED) | 1 | $2.00 | $2.00 | Cut to size | Optional display protection |

**Subtotal (Optional):** $0-25.90

---

## Cost Summary

| Category | Estimated Cost |
|----------|----------------|
| **Core Electronics** | $66.75 |
| **Power & Control** | $2.20 |
| **Connectors & Panel Hardware** | $7.50 |
| **CV/Gate Best Practice Components** | $0.09 |
| **Fasteners & Hardware** | $5.00-8.00 |
| **3D Printed Parts** | $4.00-11.50 |
| **Wire & Cabling** | $4.50-5.00 |
| **Optional Components** | $0-25.90 |
| **TOTAL (without optional)** | **$88.54-104.04** |
| **TOTAL (with all optional)** | **$88.54-129.94** |

---

## Cost Savings vs Original Design

| Original Plan | Current Plan | Savings |
|---------------|--------------|---------|
| PowerBoost 500C: $14.95 | Teyleten Boost: $0.70 | **$14.25** |
| JST Splitter Cable: $2.95 | None (slide switch distributes power) | **$2.95** |
| **Total Savings:** | | **$17.20** |

---

## Purchasing Notes

### Adafruit Components (Single Order)
- M4 Feather CAN Express ($24.95)
- OLED FeatherWing ($14.95)
- MIDI FeatherWing ($9.95)
- MCP4728 Quad DAC ($8.95)
- LiPo Battery 500mAh ($7.95)

**Adafruit Subtotal:** $66.75 (before shipping)

### Amazon/Generic Components
- Teyleten Boost Modules (pack of 10: ~$7.00)
- **Lsgoodcare 3.5mm TRS jacks** (pack of 20: ~$10) - Amazon B01DBOBRHQ
- Wire, heat shrink, hardware (various)

### 3D Printing Costs
- Filament usage: ~50-100g PLA (~$1-3)
- Print time: 3-6 hours total
- Machine: Bambu Labs A1 Mini

---

## Assembly Cost Estimate

| Phase | Estimated Time |
|-------|----------------|
| CAD Design (Fusion 360) | 6-8 hours |
| 3D Printing | 3-6 hours (mostly unattended) |
| Electronics Assembly | 2-3 hours |
| Wiring & Soldering | 2-3 hours |
| Testing & Debugging | 1-2 hours |
| **Total Build Time:** | **14-22 hours** |

---

## Procurement Strategy

### Phase 1: Core Components (Start Development)
Order immediately:
- All Adafruit components
- Teyleten boost modules (10-pack)
- Basic wire and hardware

**Cost:** ~$75-80

### Phase 2: Enclosure Components (After CAD Design)
Order after finalizing dimensions:
- Panel mount connectors (exact quantities)
- Specific fasteners (M2.5/M3 sizes confirmed)
- 3D printing filament (if needed)

**Cost:** ~$20-30

### Phase 3: Optional Enhancements (Post-Testing)
Order based on testing results:
- Second MIDI FeatherWing (if clock input needed)
- Larger battery (if runtime insufficient)
- Cosmetic additions (rubber feet, acrylic window)

**Cost:** $0-25

---

## Vendor Links (Reference)

### Adafruit
- M4 Feather CAN: https://www.adafruit.com/product/4759
- OLED FeatherWing: https://www.adafruit.com/product/4650
- MIDI FeatherWing: https://www.adafruit.com/product/4740
- MCP4728 DAC: https://www.adafruit.com/product/4470
- LiPo 500mAh: https://www.adafruit.com/product/258

### Amazon
- Teyleten Boost Modules: Search "Teyleten Multi-Function Boost Module"
- Generic hardware, connectors, wire: Search by specification

### 3D Printing
- Bambu Labs A1 Mini: https://bambulab.com/
- PLA Filament: Various vendors (Bambu, Overture, Hatchbox, etc.)

---

## Bill of Materials Version

**Version:** 1.0
**Date:** 2025-10-15
**Project:** MIDI Arpeggiator Desktop Enclosure
**Hardware Revision:** M4 CAN + OLED + MIDI + MCP4728 DAC + Teyleten Boost

---

## Notes

- All prices are estimates as of 2025-10-15
- Shipping costs not included
- Generic component prices may vary by supplier
- 3D printing costs assume PLA filament at ~$20/kg
- Optional components can be added later without redesign
- Slide switch model number (805) to be verified with supplier
- Heat shrink and wire can be purchased in bulk for cost savings
- Consider buying extra fasteners (M2.5/M3) for future modifications
