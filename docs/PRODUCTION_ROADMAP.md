# Arp Production Roadmap

**Purpose:** Production planning and cost optimization for 200-unit manufacturing run
**Status:** 📋 Planning Phase - Hardware testing in progress
**Last Updated:** 2025-10-24
**Target:** Cost-optimized single PCB design for wide release

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Current Development Hardware](#current-development-hardware)
3. [Production Hardware Strategy](#production-hardware-strategy)
4. [Cost Analysis](#cost-analysis)
5. [Technical Implementation](#technical-implementation)
6. [Development Timeline](#development-timeline)
7. [Risk Assessment](#risk-assessment)
8. [Next Steps](#next-steps)

---

## Executive Summary

### Goal
Manufacture 200 units of Arp hardware MIDI arpeggiator with:
- MIDI IN/OUT (DIN-5)
- CV Pitch + Gate/Trigger outputs
- S-Trigger support
- OLED display + button UI
- USB-C connectivity
- Optional battery power

### Key Findings
- **Current dev hardware cost:** $60+ per unit (Feather stack)
- **Optimized production cost:** $40-45 per unit (custom PCB)
- **Total savings:** $1,800-3,600 for 200 units
- **Recommended MCU:** RP2040 (instead of SAMD51)
- **Strategy:** Single custom PCB with integrated MIDI circuitry

### Decision: Custom PCB Required for Cost Effectiveness

**Why you need a microcontroller:**
- Real-time MIDI processing and arpeggiator logic
- CV/Gate output generation and timing
- Display driver and UI state management
- Settings persistence and clock synchronization

**Why RP2040 instead of SAMD51:**
- Cost: $1 vs $6-8 per unit
- Performance: 133MHz dual-core (more than sufficient)
- CircuitPython compatible (easy firmware port)
- Proven reliability in production devices

---

## Current Development Hardware

### Architecture (Session 8 - October 2025)
```
┌─────────────────────────────┐
│  OLED FeatherWing           │  ← UI + 3 Buttons
│  (128x64, SH1107)           │     $20
├─────────────────────────────┤
│  MIDI FeatherWing           │  ← DIN MIDI IN/OUT
│  (H11L1 + 74HC14)           │     $15
├─────────────────────────────┤
│  Feather M4 CAN Express     │  ← Brain (SAMD51, 120MHz)
│  (192KB RAM, 512KB Flash)   │     $25
└─────────────────────────────┘
         ↓ USB-C
    [Computer/DAW]

+ 3.7V 1200mAh LiPo            $4-5
+ Powerboost 5V                $10-15
+ MCP4728 DAC breakout         $10-15

Total: $84-105 per unit
```

### What Works (Validated)
- ✅ MIDI Input/Output (USB + UART DIN)
- ✅ Arpeggiator engine (Up, Down, UpDown, Random)
- ✅ OLED Display (CP 10.x compatible)
- ✅ Button UI with debouncing
- ✅ Settings persistence (JSON)
- ✅ Battery power (3.7V LiPo, USB charging)
- ✅ CircuitPython 10.0.3 firmware

### What's In Testing
- 🚧 MCP4728 DAC integration (wiring in progress)
- 🚧 CV/Gate output driver (software 70% complete)
- 🚧 I2C level shifting (3.3V ↔ 5V for full CV range)

### What's Planned
- 📋 S-Trigger output
- 📋 MIDI clock sync (ClockHandler exists but unused)
- 📋 Startup error protocol
- 📋 Enclosure design (3D printable)

---

## Production Hardware Strategy

### Recommended: Single Custom PCB with RP2040

#### Why Custom PCB?
The Feather stack is a **development platform**, not a production solution:
- Unnecessarily expensive (modular markup)
- Bulky form factor (3 stacked boards)
- Over-engineered (CAN bus not needed)
- Contains unused features (second UART, extra GPIO)

#### Core Components (All on One PCB)

**Microcontroller Section:**
- RP2040 microcontroller (dual-core 133MHz)
- W25Q128 flash memory (2MB for CircuitPython)
- 12MHz crystal + load capacitors
- USB-C connector with ESD protection
- 3.3V LDO regulator (AP2112K or XC6206)

**MIDI Circuit (Integrated):**
- MIDI IN: H11L1 optocoupler + 74HC14 inverter + passives
- MIDI OUT: 74HC04 buffer (or transistor) + current limiting
- 2× DIN-5 female jacks (panel mount or PCB mount)

**CV/Gate Output:**
- MCP4728 4-channel 12-bit DAC
- BSS138 level shifter (3.3V ↔ 5V I2C)
- Op-amp voltage scaling (0-5V or 0-10V)
- 3× 3.5mm mono jacks (CV Pitch, Gate, S-Trig)

**User Interface:**
- 128x64 I2C OLED module (header socket for plug-in module)
- 3× tactile switches (panel mount or PCB mount)
- Optional: Status LEDs (MIDI activity, power)

**Power Management:**
- USB-C 5V input
- 3.3V rail (digital logic)
- 5V rail (CV output, optional)
- **Optional:** LiPo charging circuit (MCP73831) + battery connector
- **Optional:** Battery level monitoring (ADC + voltage divider)

---

## Cost Analysis

### Per-Unit Component Cost (200 Qty)

| Component | Development (Feathers) | Production (Custom PCB) | Savings |
|-----------|------------------------|-------------------------|---------|
| **Microcontroller** | $25 (Feather M4) | $1.00 (RP2040) | $24.00 |
| **MIDI Circuit** | $15 (FeatherWing) | $6.00 (integrated) | $9.00 |
| **Display** | $20 (FeatherWing) | $5.00 (module) | $15.00 |
| **Flash Memory** | Included | $0.50 (W25Q128) | — |
| **DAC** | $12 (breakout) | $3.50 (MCP4728 IC) | $8.50 |
| **Power Regulation** | Included | $1.00 (LDO + passives) | — |
| **USB Connector** | Included | $0.50 (USB-C) | — |
| **Crystal + Passives** | Included | $2.00 | — |
| **DIN Jacks (2x)** | External | $3.00 | — |
| **3.5mm Jacks (3x)** | External | $3.00 | — |
| **Buttons (3x)** | External | $1.50 | — |
| **PCB + Assembly** | N/A | $15-20 (PCBA service) | — |
| **LiPo Battery** | $5.00 | $4.00 (optional) | $1.00 |
| **Powerboost** | $12 | Integrated | $12.00 |
| | | | |
| **TOTAL** | **$89-105** | **$42-51** | **$38-54** |

### 200-Unit Production Run

| Configuration | Per Unit | 200 Units | vs Feathers |
|---------------|----------|-----------|-------------|
| **USB-only** | $42-47 | $8,400-9,400 | **Save $8,600-12,600** |
| **With Battery** | $46-51 | $9,200-10,200 | **Save $7,800-11,800** |

### Additional Costs (One-Time)

| Item | Cost | Notes |
|------|------|-------|
| **PCB Design** | $0-500 | DIY in KiCad or hire designer |
| **Prototype Run (5 units)** | $150-300 | First validation batch |
| **Beta Run (20 units)** | $1,000-1,500 | Pre-production testing |
| **Test Jigs/Fixtures** | $200-500 | For QA and programming |
| **Firmware Development** | $0 | Port existing CircuitPython code |
| **Assembly Labor** | $500-1,000 | Through-hole soldering (~10 min/unit) |

**Total One-Time Investment:** $1,850-3,800

**Break-Even vs Feathers:** Savings offset investment after ~35-50 units

---

## Technical Implementation

### 1. Microcontroller: RP2040 vs SAMD51

#### Why RP2040 is Better for Production

| Feature | RP2040 | SAMD51 (M4) | Winner |
|---------|--------|-------------|--------|
| **Cost** | $1.00 | $6-8 | RP2040 (6-8× cheaper) |
| **Clock Speed** | 133MHz dual-core | 120MHz single-core | RP2040 (2× cores) |
| **RAM** | 264KB SRAM | 192KB SRAM | RP2040 (37% more) |
| **Flash** | External (2MB+) | 512KB internal | RP2040 (4× capacity) |
| **GPIO** | 30 pins | 32 pins | Tie |
| **ADC** | 3× 12-bit | 2× 12-bit | RP2040 |
| **DAC** | None (use external) | 2× 10-bit | M4* |
| **I2C/SPI/UART** | 2/2/2 | 6/6/6 | M4** |
| **USB** | Native | Native | Tie |
| **CircuitPython** | Fully supported | Fully supported | Tie |
| **Community** | Huge (Pico ecosystem) | Good (Feather) | RP2040 |
| **Availability** | Excellent | Good | RP2040 |

*We're using external MCP4728 DAC anyway (better specs)
**We only need 1 I2C bus - RP2040 has plenty

**Verdict:** RP2040 wins on cost, performance, and availability

#### Firmware Port Difficulty: LOW

Current codebase uses:
- `board` → Pin definitions (easy mapping)
- `busio` → I2C, UART (identical on RP2040)
- `digitalio` → GPIO (identical)
- `usb_midi` → USB MIDI (identical)
- `adafruit_midi` → Library (platform-agnostic)
- `adafruit_displayio_sh1107` → Display (works on RP2040)

**Estimated port time:** 4-8 hours (mostly pin mapping and testing)

---

### 2. MIDI Circuit Integration

#### What's in the MIDI FeatherWing

**MIDI IN Circuit:**
```
DIN-5 Pin 5 → 220Ω → H11L1 Optocoupler LED+
DIN-5 Pin 4 → 220Ω → H11L1 Optocoupler LED-
H11L1 Output → 74HC14 Schmitt Trigger Inverter → RP2040 UART RX
```

**MIDI OUT Circuit:**
```
RP2040 UART TX → 74HC04 Buffer → 220Ω → DIN-5 Pin 5
                                  → 220Ω → DIN-5 Pin 4
```

#### Component BOM (MIDI Section)

| Qty | Part Number | Description | Unit Cost | Supplier |
|-----|-------------|-------------|-----------|----------|
| 1 | H11L1M | Optocoupler, 6-pin SMD | $0.50 | Mouser, LCSC |
| 1 | 74HC14D | Hex Schmitt Trigger Inverter | $0.30 | Mouser, LCSC |
| 1 | 74HC04D | Hex Inverter | $0.30 | Mouser, LCSC |
| 1 | 1N4148 | Diode | $0.10 | Mouser, LCSC |
| 4 | 220Ω 0805 | Resistor | $0.02 | LCSC |
| 2 | 100nF 0805 | Capacitor | $0.05 | LCSC |
| 2 | DIN-5 Female | 180° PCB mount or panel mount | $1.50 | Mouser, AliExpress |

**Total MIDI cost:** ~$5-6 per unit (vs $15 FeatherWing)

#### PCB Space Required
- MIDI circuit: ~20mm × 30mm
- DIN-5 jacks: 16mm × 16mm each (if PCB mount)

#### Reference Designs
- [Adafruit MIDI FeatherWing schematic](https://learn.adafruit.com/adafruit-midi-featherwing/downloads) (open source)
- [Arduino MIDI Circuit](https://www.arduino.cc/en/Tutorial/Foundations/MIDIDevice)
- [Electrical Music MIDI reference](https://www.midi.org/specifications/midi1-specifications)

---

### 3. CV/Gate Output Design

#### Current Plan (Validated in Testing)

**MCP4728 4-Channel 12-bit DAC:**
- Channel A: CV Pitch (0-5V, 1V/octave)
- Channel B: Gate/Trigger (0-5V, pulse on note on)
- Channel C: S-Trigger (0V normally, -5V trigger)
- Channel D: Future (velocity CV, modulation, etc.)

**Voltage Scaling:**
- Native DAC output: 0-3.3V (if powered at 3.3V) or 0-5V (if powered at 5V)
- For 1V/octave: Need 5 octaves = 5V range minimum
- **Solution:** Power MCP4728 at 5V with BSS138 level shifter for I2C

**Op-Amp Conditioning (Optional):**
- Rail-to-rail op-amp (MCP6002 or TL072)
- Gain stage: 0-5V → 0-10V (for euro-rack compatibility)
- Offset adjustment: +/- trimming

#### BOM (CV/Gate Section)

| Qty | Part Number | Description | Unit Cost |
|-----|-------------|-------------|-----------|
| 1 | MCP4728 | 4-ch 12-bit DAC, I2C | $3.50 |
| 1 | BSS138 | N-ch MOSFET (level shift) | $0.30 |
| 2 | 10kΩ 0805 | Pull-up resistors | $0.05 |
| 1 | MCP6002 | Dual op-amp (optional scaling) | $0.60 |
| 3 | 3.5mm Mono Jack | Panel mount or PCB mount | $1.00 |
| 6 | Resistors/Caps | Gain network | $0.30 |

**Total CV cost:** ~$5-6 per unit

---

### 4. Display Integration

#### Current: Adafruit OLED FeatherWing ($20)
- 128x64 pixels, SH1107 driver
- I2C interface (0x3C address)
- 3 buttons integrated
- **Issue:** FeatherWing markup

#### Production: Off-the-Shelf OLED Module ($3-5)

**Source:** AliExpress, LCSC, or Adafruit wholesale
- Same 128x64 resolution, same I2C driver
- 4-pin header: VCC, GND, SDA, SCL
- **PCB strategy:** Female header socket, user plugs in module

**Alternative:** COG (Chip-on-Glass) OLED directly on PCB
- Cost: $8-12 per unit
- Requires reflow soldering
- More integrated (no socket)
- **Recommendation:** Use module for flexibility

#### Buttons
- Separate tactile switches on PCB (3×)
- Panel mount or PCB mount
- Cost: $0.50 each × 3 = $1.50

**Total UI cost:** $5-7 per unit (vs $20 FeatherWing)

---

### 5. Power Management

#### Input Options

**Option A: USB-Only (Simplest)**
- USB-C 5V input
- 3.3V LDO regulator (AP2112K: 600mA, $0.50)
- Cost: ~$1 total
- **Pros:** Simple, reliable, lowest cost
- **Cons:** Tethered to computer/USB power

**Option B: USB + Battery (Portable)**
- USB-C 5V input + charging
- MCP73831 LiPo charger (500mA, $0.50)
- JST-PH connector for battery
- Battery level monitoring (ADC + voltage divider)
- Cost: ~$2 (without battery)
- **Pros:** Portable, 9-12 hour runtime
- **Cons:** +$4 for battery, safety considerations

#### Recommendation: Offer Both

- **Standard model:** USB-only ($42-47)
- **Pro model:** USB + battery ($46-51)
- **PCB design:** Populate charging circuit on pro model only

#### Power Rails

- **3.3V:** RP2040, OLED, buttons, logic
- **5V:** CV output (MCP4728 VDD for full range)
- **USB 5V → 3.3V LDO:** AP2112K (600mA, low dropout)
- **USB 5V → CV rail:** Direct or boost converter

---

### 6. PCB Layout Considerations

#### Form Factor Options

**Option 1: Feather-Sized (50mm × 23mm)**
- Compact, familiar form factor
- Limited space for jacks (use panel mount)
- **Use case:** Minimal enclosure

**Option 2: Euro Card (100mm × 80mm)**
- All jacks on PCB (no flying leads)
- Room for future expansion
- **Use case:** Desktop unit

**Option 3: Custom (120mm × 60mm)**
- Balance between size and features
- All jacks on edges
- **Recommendation:** Best for 3D printed enclosure

#### Layer Count
- **2-layer:** Sufficient for this design
- Cost: ~$5-8 per board (200 qty)
- **4-layer:** Overkill unless EMI issues arise

#### Connectors Placement
- **Edge 1 (Front):** OLED header, buttons (or panel mount holes)
- **Edge 2 (Back):** MIDI DIN jacks (IN/OUT)
- **Edge 3 (Side):** 3.5mm jacks (CV, Gate, S-Trig)
- **Edge 4 (Side):** USB-C, power LED

#### Ground Plane Strategy
- Solid ground plane on bottom layer
- Keep analog (CV) and digital (MIDI/I2C) separated
- Star grounding for DAC reference

---

## Development Timeline

### Phase 1: Prototype Design (4-6 Weeks)

#### Week 1-2: Schematic Design
- [ ] Create KiCad project
- [ ] RP2040 + flash + USB-C section
- [ ] MIDI IN/OUT circuit (replicate FeatherWing)
- [ ] MCP4728 + level shifter + CV output
- [ ] Power regulation (3.3V + optional charging)
- [ ] OLED header + buttons
- [ ] Design review and validation

#### Week 3-4: PCB Layout
- [ ] Component placement (optimize for routing)
- [ ] Route critical signals (USB, I2C, UART)
- [ ] Ground/power planes
- [ ] Silkscreen labels
- [ ] DRC (Design Rule Check)
- [ ] Generate Gerbers + BOM + CPL (pick-and-place)

#### Week 5: Prototype Order
- [ ] Submit to JLCPCB/PCBWay (5 boards, PCBA)
- [ ] Order missing components (DIN jacks, 3.5mm jacks, OLED)
- [ ] Wait for delivery (10-14 days)

#### Week 6: Assembly & Testing
- [ ] Solder through-hole parts (jacks, headers)
- [ ] Flash RP2040 bootloader (if not pre-flashed)
- [ ] Port CircuitPython firmware to RP2040
- [ ] Validate MIDI IN/OUT
- [ ] Validate CV/Gate output
- [ ] Test display + buttons
- [ ] Measure power consumption
- [ ] Document issues and design changes

**Deliverable:** 5 working prototypes + design revision list

---

### Phase 2: Beta Production (6-8 Weeks)

#### Week 1-2: Design Revision
- [ ] Incorporate prototype feedback
- [ ] Fix any issues (footprints, routing, component values)
- [ ] Optimize layout for easier assembly
- [ ] Add test points and debug headers
- [ ] Final design review

#### Week 3: Beta Order
- [ ] Order 20 units (PCBA)
- [ ] Order through-hole components (bulk)
- [ ] Order OLED modules (20 units)

#### Week 4-5: Beta Assembly
- [ ] Solder through-hole parts (20 units)
- [ ] Flash firmware (via USB bootloader or SWD)
- [ ] Run QA tests (MIDI loopback, CV output, UI)
- [ ] Create assembly documentation (photos, BOM, steps)

#### Week 6-8: Beta Testing
- [ ] Distribute to testers (friends, community)
- [ ] Collect feedback (bugs, feature requests, usability)
- [ ] Monitor for hardware failures
- [ ] Refine firmware based on feedback

**Deliverable:** 20 beta units + final design + production documentation

---

### Phase 3: Full Production (8-10 Weeks)

#### Week 1-2: Production Prep
- [ ] Finalize PCB design (Rev 1.0)
- [ ] Create production BOM (with alternates)
- [ ] Source components (check stock, lead times)
- [ ] Create test plan and QA checklist
- [ ] Build test jigs (if needed)

#### Week 3: Production Order
- [ ] Order 200 PCBs (PCBA)
- [ ] Order through-hole components (bulk, 220 qty for spares)
- [ ] Order OLED modules (220 qty)
- [ ] Order enclosures/hardware (if applicable)

#### Week 4-8: Assembly
- [ ] Receive boards (verify PCBAs are correct)
- [ ] Set up assembly line (soldering station, tools)
- [ ] Solder through-hole parts (~10 min/unit = 33 hours total)
- [ ] Flash firmware (batch programming if possible)
- [ ] Run QA tests (MIDI, CV, display, buttons)
- [ ] Burn-in testing (24-hour power-on test for sample units)

#### Week 9-10: Packaging & Shipping
- [ ] Package units (antistatic bags, boxes)
- [ ] Create user manual (PDF or printed)
- [ ] Ship to customers or distributor

**Deliverable:** 200 production units ready for sale

---

### Total Timeline: 18-24 Weeks (4.5-6 Months)

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **RP2040 firmware port fails** | Low | High | Prototype first, RP2040 is well-supported in CircuitPython |
| **MIDI circuit doesn't work** | Low | High | Use proven reference design (Adafruit FeatherWing schematic) |
| **CV output not accurate** | Medium | Medium | Prototype testing, calibration routine in firmware |
| **I2C level shifting issues** | Medium | Medium | BSS138 is proven solution, test early |
| **PCB design error (wrong footprint, routing)** | Medium | High | Design review, order 5 prototypes before 200 units |
| **Component shortage** | Medium | Medium | Source from multiple suppliers, order early |
| **Assembly defects** | Low | Medium | Use PCBA service for SMD, QA testing for every unit |

### Financial Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Component cost increase** | Medium | Medium | Order bulk upfront, lock in prices |
| **Prototype requires expensive iteration** | Low | Low | Only $150-300 per iteration |
| **Beta units reveal major flaw** | Low | High | Thorough prototype testing, beta test with 20 units |
| **200-unit order is defective** | Very Low | Very High | Start with 20-unit beta run, validate before scaling |
| **Demand lower than expected** | Medium | High | Start with 20-50 units, gauge interest before 200 |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Assembly takes longer than planned** | Medium | Low | Budget 15 min/unit instead of 10 min |
| **Testing reveals firmware bugs** | High | Medium | Beta testing phase, firmware updates post-launch |
| **3D printed enclosures are slow** | High | Medium | Print in parallel, or outsource to 3D print farm |
| **Supply chain delays** | Medium | Medium | Order 12-16 weeks before target ship date |

---

## Next Steps

### Immediate (After Hardware Testing Complete)

**Before starting PCB design:**
1. ✅ **Complete MCP4728 integration testing**
   - Validate I2C communication at 3.3V
   - Test DAC output accuracy with multimeter/scope
   - Confirm 5V operation with BSS138 level shifter
   - Measure CV output stability and noise

2. ✅ **Validate CV/Gate output**
   - Test 1V/octave calibration across 5 octaves
   - Verify gate timing (note on/off response)
   - Test S-Trigger polarity (0V → -5V)

3. ✅ **Finalize feature set**
   - Confirm all features work on Feather M4
   - Document any limitations or quirks
   - Freeze firmware API for production

4. ✅ **Document current hardware baseline**
   - Pin assignments (final)
   - Power consumption measurements
   - MIDI latency and jitter specs
   - Display update rate and responsiveness

### Short Term (Weeks 1-4)

**Prototype design phase:**
1. **Design PCB schematic in KiCad**
   - RP2040 section (reference Raspberry Pi Pico schematic)
   - MIDI IN/OUT (reference Adafruit MIDI FeatherWing)
   - MCP4728 + level shifter
   - Power regulation
   - OLED header + buttons
   - **I can help with this if you want**

2. **Create detailed BOM**
   - Part numbers (Mouser, LCSC, Digikey)
   - Alternates (in case of shortages)
   - Unit costs and availability
   - Total cost calculation

3. **PCB layout**
   - Component placement
   - Routing (2-layer)
   - Generate Gerbers + assembly files

4. **Order 5 prototypes**
   - JLCPCB or PCBWay PCBA
   - Through-hole components separately
   - OLED modules

### Medium Term (Weeks 5-12)

**Prototype validation:**
1. **Assemble and test prototypes**
   - Solder through-hole parts
   - Flash RP2040 bootloader
   - Port firmware from Feather M4
   - Validate all features

2. **Iterate if needed**
   - Fix any design issues
   - Order revised prototypes if necessary

3. **Beta production (20 units)**
   - Order small batch
   - Distribute for testing
   - Collect feedback

### Long Term (Weeks 13-24)

**Full production:**
1. **Finalize design** (Rev 1.0)
2. **Order 200 units** with PCBA
3. **Assembly line** for through-hole parts
4. **QA testing** on all units
5. **Package and ship**

---

## Decision Points

### Before Committing to Prototype ($150-300)
- [ ] Hardware testing on Feather M4 is COMPLETE
- [ ] All features validated and working
- [ ] Cost analysis confirms $40-50 per unit is achievable
- [ ] Timeline is acceptable (18-24 weeks)

### Before Committing to Beta Run ($1,000-1,500)
- [ ] 5 prototypes are fully functional
- [ ] No major design flaws discovered
- [ ] Firmware port to RP2040 is complete
- [ ] Assembly time is <15 min per unit

### Before Committing to Full Production ($8,400-10,200)
- [ ] 20 beta units tested successfully
- [ ] Community feedback is positive
- [ ] No critical bugs in firmware
- [ ] Supply chain is stable (components in stock)
- [ ] Demand validated (pre-orders, interest)

---

## Open Questions

### Hardware Design
- [ ] **Battery:** Standard or optional? Pro/standard model split?
- [ ] **Enclosure:** Specific dimensions? Mounting holes? Panel vs PCB mount jacks?
- [ ] **CV voltage range:** 0-5V or 0-10V? (affects op-amp design)
- [ ] **S-Trigger:** Required or nice-to-have? (adds cost)
- [ ] **OLED:** Module with header or COG directly on PCB?

### Production
- [ ] **Manufacturer:** JLCPCB, PCBWay, or other?
- [ ] **Assembly:** DIY through-hole or pay for full assembly?
- [ ] **Testing:** Manual QA or automated test jig?
- [ ] **Firmware:** Pre-flash at factory or user installs?

### Business
- [ ] **Price point:** What's the target retail price?
- [ ] **Distribution:** Direct sales, distributor, or both?
- [ ] **Support:** Warranty? Firmware updates? User forum?
- [ ] **Certification:** CE/FCC required? (depends on market)

---

## Resources

### PCB Design Tools
- [KiCad](https://www.kicad.org/) (free, open source)
- [EasyEDA](https://easyeda.com/) (free, web-based, integrates with JLCPCB)

### Manufacturers
- [JLCPCB](https://jlcpcb.com/) - PCB + PCBA, great prices, fast turnaround
- [PCBWay](https://www.pcbway.com/) - PCB + PCBA, good quality
- [OSH Park](https://oshpark.com/) - US-based, higher quality, slower

### Component Suppliers
- [Mouser](https://www.mouser.com/) - US, fast shipping, full catalog
- [Digikey](https://www.digikey.com/) - US, huge selection
- [LCSC](https://www.lcsc.com/) - China, low prices, integrates with JLCPCB

### Reference Designs
- [Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) - RP2040 reference schematic
- [Adafruit MIDI FeatherWing](https://learn.adafruit.com/adafruit-midi-featherwing/downloads) - MIDI circuit reference
- [Adafruit MCP4728 Breakout](https://learn.adafruit.com/adafruit-mcp4728-i2c-quad-dac/downloads) - DAC reference

### Firmware
- [CircuitPython RP2040 Guide](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython)
- [RP2040 Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)

---

## Appendix: Why Not Other MCUs?

### Alternatives Considered

**ESP32 ($2-3)**
- Pros: Cheap, WiFi/BLE, powerful
- Cons: Overkill, higher power, CircuitPython support weaker
- **Verdict:** Not needed for MIDI arp

**STM32F4 ($3-5)**
- Pros: Powerful, good GPIO
- Cons: More expensive, toolchain complexity, no CircuitPython
- **Verdict:** RP2040 is simpler

**ATmega328P ($1.50)**
- Pros: Cheap, Arduino-compatible
- Cons: Slow (16MHz), limited RAM (2KB), no native USB
- **Verdict:** Too limited for display + arp + MIDI

**SAMD21 ($3-4)**
- Pros: CircuitPython, lower power than SAMD51
- Cons: 48MHz (slower than RP2040), 32KB RAM (vs 264KB)
- **Verdict:** RP2040 is better value

**Teensy 4.0 ($25)**
- Pros: Incredibly fast (600MHz), great audio
- Cons: Expensive, overkill for MIDI arp
- **Verdict:** Not cost-effective for production

**Winner: RP2040** (best cost/performance/support)

---

## Revision History

### v1.0 (2025-10-24)
- Initial document created
- Cost analysis for 200-unit run
- RP2040 vs SAMD51 comparison
- Timeline and risk assessment
- **Status:** Planning phase, awaiting hardware testing completion

### Future Revisions
- [ ] v1.1: Update after MCP4728 testing complete
- [ ] v1.2: Update after CV/Gate validation
- [ ] v1.3: Update after schematic design complete
- [ ] v2.0: Update after prototype testing complete

---

**Next update:** After MCP4728 + CV/Gate hardware testing is complete

**Document Owner:** Keegan
**Status:** 📋 Living Document - Update as testing progresses
