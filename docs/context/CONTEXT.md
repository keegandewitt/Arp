# prisme - MIDI/CV Translation Hub - Living Context

**Purpose:** This file maintains session-to-session continuity for Claude instances.
**Update Frequency:** After every significant milestone or before session end.

**Project Vision:** prisme is a full-service USB-C powered MIDI/CV translation hub that applies real-time transformations (Scale, Arp, Clock) to musical data, bridging DAWs, hardware synths, and Eurorack modular systems with imperceptible latency.

---

## ⚠️ CRITICAL RULE: NO BLAME-SHIFTING TO TOOLS

**NEVER claim a tool has "limitations" or "shortcomings" to excuse your own failures unless you can provide multi-point verification:**

1. **Documentation from the tool's official sources** stating the limitation
2. **Multiple independent third-party sources** confirming the limitation
3. **Concrete technical reasons** why the limitation exists (not just "it's hard")

**Example of BANNED blame-shifting:**
- ❌ "schemdraw is fundamentally inadequate for complex layouts"
- ❌ "this tool isn't suitable for multi-component diagrams"
- ❌ "the library has limitations that prevent..."

**What you MUST say instead:**
- ✅ "I failed to calculate proper coordinates for component positioning"
- ✅ "I used improvisational placement instead of planned layout"
- ✅ "I didn't understand how to use the spacing parameters correctly"

**Your failures are YOUR failures.** Own them. Document what you didn't figure out, not what the tool "can't do."

---

## Session Handoff

**Last Updated:** 2025-11-03 20:10 PST (Session 26 - Unified Schematic Work)
**Session Status:** ⏳ IN PROGRESS - Need to solve coordinate-based layout for unified schematic
**Token Usage:** ~82K / 200K

### Current Session Summary (Session 26 - Unified Schematic Work)
**What was attempted:**
- ⏳ **IN PROGRESS: Unified system schematic for EasyEDA**
  - User requested: "if i'm going to begin in EasyEDA, what do i need from you?"
  - Goal: Single complete schematic showing all hardware interconnections
  - **Technical challenge:** Right-side outputs (4 LEDs + S-Trig) from 5 vertically stacked M4 pins
  - Multiple iterations with overlapping components
  - **Actual problem:** Failed to calculate and use proper absolute coordinates for component placement
  - Used improvisational `.right()` and `.down()` instead of planned `.at(x, y)` positioning

**What needs to be solved:**
1. Calculate exact Y-coordinates for M4 pins based on IC spacing parameter
2. Plan horizontal X positions for each output component to prevent overlap
3. Use absolute coordinate positioning instead of relative positioning
4. Verify layout mathematically before generating

**Files created this session:**
- Multiple generate_*.py scripts (coordinate planning needed)
- UNIFIED_SYSTEM_SCHEMATIC.svg (needs proper layout)

### Previous Session Summary (Session 25 - HARDWARE DOCUMENTATION OVERHAUL & PCB SCHEMATICS)
**What was accomplished:**
- ✅ **SEPARATED DOCUMENTATION TRUTH FROM FICTION**
  - User discovered: Previous Claudes added BAT85 diodes + op-amp to docs (never built)
  - Created ACTUAL_HARDWARE_TRUTH.md as single source of truth
  - Created HARDWARE_AUDIT_CORRECTIONS.md to fix polluted documentation
  - User quote: "this is the first i'm hearing of BAT85 clamps"

- ✅ **FOUND OPTIMAL BAT85 SOURCE**
  - User found Amazon: ALLECIN 100pcs for ~$8-10 (vs Digi-Key 10pcs $7.30)
  - Updated all 10+ docs with Amazon link as primary recommendation
  - User ordered diodes, arriving in 1-2 days

- ✅ **GENERATED PRODUCTION-READY PCB SCHEMATICS**
  - TOP_BOARD_FINAL.svg (32.4 KB) - Input protection circuits
  - BOTTOM_BOARD_FINAL.svg (42.0 KB) - DAC outputs + S-Trig
  - EASYEDA_PCB_DESIGN_GUIDE.md - Complete BOM, layout guidelines
  - Both 5V and 3.3V power rails properly documented (3.3V was missing!)

- ✅ **REDESIGNED SCHEMATICS FOR CLARITY (User: "come on let's clean this up")**
  - **Problem:** Initial COMPLETE_SYSTEM_SCHEMATIC.svg was cluttered, hard to read
  - **Lesson learned:** Don't try to show everything in one schematic
  - **Solution:** Break into 6 focused schematics, one per functional block
  - **New schematics:**
    1. M4_PIN_ASSIGNMENTS.svg - Pin reference table (text-based)
    2. TOP_PCB_CV_IN.svg - CV input circuit only
    3. TOP_PCB_TRIG_IN.svg - TRIG input circuit only
    4. BOTTOM_PCB_DAC_OUTPUTS.svg - DAC output circuits
    5. BOTTOM_PCB_STRIG.svg - S-Trig transistor circuit
    6. POWER_DISTRIBUTION.svg - Power decoupling (both boards)
  - **Result:** Each schematic is clean, focused, easy to read

**Schemdraw Best Practices (Lessons Learned):**
```python
# ❌ DON'T: Try to show everything in one giant schematic
d = schemdraw.Drawing()
# ... add M4, MIDI, OLED, DAC, inputs, outputs, power, LEDs all in one drawing
# Result: Cluttered, overlapping elements, hard to read

# ✅ DO: Break into focused schematics, one per functional block
# Schematic 1: M4 pin assignments (text-based reference)
# Schematic 2: CV IN circuit only
# Schematic 3: TRIG IN circuit only
# Schematic 4: DAC outputs only
# Schematic 5: S-Trig circuit only
# Schematic 6: Power distribution only

# ❌ DON'T: Use schemdraw for complex multi-component system diagrams
# schemdraw is best for individual circuits, not system overviews

# ✅ DO: Use generous spacing between elements
d += elm.Resistor().right(2)  # Use 2 units, not 0.5
d += elm.Line().down(1)       # Clear vertical separation

# ✅ DO: Group related components visually
# Power section at top
# Input circuits in middle
# Output circuits at bottom

# ✅ DO: Use clear labels with context
d += elm.Dot().label('To M4\nPin A3\n(ADC)', fontsize=10, halign='left')
# Not just: .label('A3')

# ✅ DO: Add component values directly on schematic
d += elm.Resistor().right(2).label('R1\n10kΩ', fontsize=9, loc='top')

# ✅ DO: Include notes sections for context
d += elm.Label().at((0, -5)).label('COMPONENT VALUES:', fontsize=11, halign='left', font='bold')
d += elm.Label().at((0, -5.5)).label('R1, R2: 10kΩ ±5% 1/4W', fontsize=9, halign='left')
```

**Files Created (Session 25):**
- ACTUAL_HARDWARE_TRUTH.md (~4,800 lines) - Single source of truth
- HARDWARE_AUDIT_CORRECTIONS.md - Corrections to old docs
- FINAL_PROTECTION_RECOMMENDATION.md - Amazon BAT85 decision
- EASYEDA_PCB_DESIGN_GUIDE.md (updated with M4 pin tables)
- TOP_BOARD_FINAL.svg, BOTTOM_BOARD_FINAL.svg - Initial schematics
- **Clean schematics (final set):**
  - M4_PIN_ASSIGNMENTS.svg - Pin reference
  - TOP_PCB_CV_IN.svg - CV input circuit
  - TOP_PCB_TRIG_IN.svg - TRIG input circuit
  - BOTTOM_PCB_DAC_OUTPUTS.svg - DAC outputs
  - BOTTOM_PCB_STRIG.svg - S-Trig circuit
  - POWER_DISTRIBUTION.svg - Power decoupling

**Key Learnings:**
1. **Documentation pollution is real** - Previous AI sessions added components never built
2. **User verification is critical** - Always confirm components exist on breadboard
3. **Schematic clarity matters** - Break complex systems into focused diagrams
4. **Missing power rails** - 3.3V rail was completely undocumented but in use
5. **schemdraw limitations** - Not suitable for complex multi-component system diagrams

**Next Steps (Session 26):**
1. **[HIGH]** Use clean schematics in EasyEDA to design PCBs
2. **[MEDIUM]** Test BAT85 diodes on breadboard when they arrive
3. **[LOW]** Order PCBs from JLCPCB/PCBWay after EasyEDA design complete

### Previous Session Summary (Session 23 - FUSION 360 AUTOMATION)
**What was accomplished:**
- ⚠️ **OPENSCAD VISUALIZATION ABANDONED - FUNDAMENTALLY INADEQUATE**
  - Attempted to create accurate 3D hardware visualization using OpenSCAD
  - Multiple failures revealed OpenSCAD cannot handle complex spatial positioning
  - Key issue: "shockingly bad" renders showing no concept of physical reality
  - User feedback: "you have no concept of the physical world"
  - Root cause: Coding 3D positions without visual feedback is inherently error-prone
- ✅ **FUSION 360 API CHOSEN AS PROFESSIONAL SOLUTION**
  - Researched proper CAD tools for hardware assembly
  - Fusion 360: Best for electronics enclosures, supports STEP/STL, visual positioning
  - FreeCAD: Open-source alternative but steeper learning curve
  - OpenSCAD: Confirmed NOT suitable for complex multi-part assemblies
- ✅ **AUTOMATED ASSEMBLY SCRIPT CREATED**
  - `PRISME_Hardware_Assembly.py` - 301-line Fusion 360 Python API script
  - Imports all CAD files: STL (Feather, OLED, MIDI), STEP (MCP4728, Battery, jacks)
  - Positions components with EXACT coordinates from CORRECT_STACK_LAYOUT.md
  - Key fix: OLED correctly stacked ON TOP of Feather (not parallel!)
  - All dimensions verified against manufacturer specifications
- ✅ **COMPLETE FUSION 360 WORKFLOW DOCUMENTED**
  - `FUSION360_ASSEMBLY_GUIDE.md` - Setup, installation, troubleshooting guide
  - Script installed to Fusion 360 Scripts folder
  - Manual installation instructions provided
  - Component position reference table included
- ✅ **ENCLOSURE FOLDER CLEANED AND ORGANIZED**
  - Archived 36 OpenSCAD files (all .scad files and renders)
  - Moved obsolete documentation to archive
  - Created clean README.md with current status
  - Production files organized and ready
- ✅ **ALL CAD MODELS INVENTORIED AND VERIFIED**
  - 3× STL files (Adafruit boards) ✓
  - 6× STEP files (components) ✓
  - 8× SLDPRT files (passives) ✓
  - All files confirmed present in FINAL_CAD_STATUS.md

**Key Technical Decisions:**
1. **Fusion 360 over OpenSCAD:** Visual CAD tool required for precision hardware assembly
2. **API Automation:** Python script eliminates manual positioning errors
3. **Documentation-Driven:** Every dimension from CORRECT_STACK_LAYOUT.md and PROTOBOARD_LAYOUT.md
4. **Archive Strategy:** Keep failed attempts for reference, but separate from production

**Component Stack (Verified Correct):**
```
Z=50.2mm: OLED FeatherWing top (STACKED on Feather)
Z=43.2mm: OLED FeatherWing base
Z=33.2mm: Feather M4 top
Z=25.2mm: Feather M4 base (on TOP board)
Z=15.2mm: TOP protoboard top
Z=13.6mm: TOP protoboard base
Z=5.6mm:  BOTTOM protoboard top
Z=4.0mm:  BOTTOM protoboard base
Z=-6.0mm: Battery (under BOTTOM board)
```

**Files Created (Session 23):**
- `hardware/enclosure/PRISME_Hardware_Assembly.py` (NEW) - Fusion 360 API script
- `hardware/enclosure/FUSION360_ASSEMBLY_GUIDE.md` (NEW) - Complete workflow guide
- `hardware/enclosure/README.md` (NEW) - Enclosure folder overview
- `hardware/enclosure/archive_openscad_attempts/` (NEW) - 40 archived files
- Installed script to: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/PRISME_Assembly/`

**Methodology Lessons Learned:**
1. **Visual feedback essential:** Cannot code 3D positions accurately without seeing results
2. **Right tool for job:** Professional CAD (Fusion 360) >>> Programmer CAD (OpenSCAD) for assemblies
3. **Research before implementation:** Should have evaluated tools before attempting OpenSCAD
4. **User patience finite:** Multiple failed iterations damage trust and waste time

**Next Steps (Session 24):**
1. **[IMMEDIATE]** Run Fusion 360 assembly script (Shift+S → PRISME_Assembly → Run)
2. **[HIGH]** Verify all components positioned correctly in Fusion 360
3. **[HIGH]** Design enclosure around assembled hardware with proper clearances
4. **[MEDIUM]** Export enclosure for 3D printing (STL) or manufacturing (STEP)
5. **[MEDIUM]** Create mounting features (standoffs, screw posts)

### Previous Session Summary (Session 22 - COLLISION FIX)
**What was accomplished:**
- ⚠️  **DISCOVERED AND FIXED CRITICAL LED/MIDI COLLISION**
  - User identified LED holes overlapping with MIDI DIN jacks in screenshots
  - Previous Session 21 design had 15.5mm MIDI holes with LEDs placed only 7mm away
  - LED holes were INSIDE the MIDI jack holes (72mm + 7mm = 79mm, but MIDI extends to 79.75mm!)
  - MIDI IN LED was positioned PAST the 90mm board edge (92mm)
- ✅ **ENCLOSURE DIMENSIONS INCREASED (MAJOR CHANGE)**
  - Internal width: 110mm (was 95mm, originally 83mm)
  - Protoboard size: 105mm × 55mm (was 90mm × 55mm, originally 75mm × 50mm)
  - External dimensions: 117mm × 72mm × 66.5mm
  - User approved: "if it needs to be wider, that's fine"
- ✅ **COMPLETE BACK PANEL LAYOUT REDESIGN**
  - All jack and LED positions recalculated with proper 2mm+ clearances
  - USB-C: 10mm | CV OUT: 22mm | TRIG OUT: 36mm | CC OUT: 50mm | MIDI OUT: 72mm | MIDI IN: 95mm
  - LEDs at: 29mm, 43mm, 57mm, 79mm, 102mm (all 7mm offset from jacks)
  - Verified NO collisions: minimum clearance 2.4mm between all holes
  - Created `BACK_PANEL_LAYOUT.md` with detailed measurements and clearance verification table
- ✅ **ALL DOCUMENTATION UPDATED WITH CORRECTED MEASUREMENTS**
  - `prisme_enclosure.scad`: Updated dimensions (110mm width) and all jack/LED positions
  - `PROTOBOARD_LAYOUT.md`: Updated board size to 105mm, all rear edge jack positions corrected
  - `JACK_WIRING_GUIDE.md`: Updated LED positions and added note about dimension increase
  - `BACK_PANEL_LAYOUT.md`: NEW file with clearance calculations and visual layout
- ✅ **METHODOLOGY LESSON LEARNED**
  - User feedback: "This is not just about the enclosure but the board designs TOO!"
  - Must verify physical clearances for ALL components, especially large MIDI DIN jacks
  - LED positioning requires accounting for full jack diameter, not just center-to-center spacing
  - Always generate verification renders to catch collisions before manufacturing

**Design Errors Fixed:**
1. **LED/MIDI Overlap:** MIDI OUT LED was inside MIDI jack hole (79mm LED vs 79.75mm jack edge)
2. **Board Overrun:** MIDI IN LED extended past 90mm board edge (92mm position)
3. **Insufficient Clearances:** Only 0.75mm between some holes (needed 2mm minimum)

**New Correct Dimensions:**
- **Enclosure Internal:** 110mm × 65mm × 60mm
- **Protoboards:** 105mm × 55mm (custom cut)
- **Jack Spacing:** 14mm (1/8" jacks with LEDs), 23mm (MIDI jacks with LEDs)
- **Verified Clearances:** All holes have 2.4mm - 13.4mm clearance ✓

### Previous Session Summary (Session 21 - **FLAWED DESIGN, FIXED IN SESSION 22**)
**What was accomplished:**
- ✅ **LED INDICATOR SYSTEM FULLY INTEGRATED**
  - 7 LED activity indicators added to hardware design:
    - 5× white 3mm flat-top LEDs: CV IN, CV OUT, CC OUT, MIDI OUT, MIDI IN
    - 2× RGB 3mm flat-top LEDs: TRIG IN, TRIG OUT (mode + activity indication)
  - RGB LEDs show V-Trig (green) vs S-Trig (red) mode visually
  - All LEDs positioned 7mm to right of respective jacks
  - 11× 150Ω current limiting resistors (total power: ~16-20mA)
- ✅ **ENCLOSURE DESIGN UPDATED WITH LED HOLES**
  - `hardware/enclosure/prisme_enclosure.scad` completely rewritten
  - Internal dimensions increased: 95mm × 65mm × 60mm (from 83mm × 58mm × 50mm)
  - NEW back panel layout: 2 rows (TOP: CV IN, TRIG IN | BOTTOM: USB-C, CV OUT, TRIG OUT, CC OUT, MIDI OUT, MIDI IN)
  - 7× 3.2mm LED holes added (press-fit for flat-top 3mm LEDs)
  - All jack positions recalculated with exact 12mm/20mm spacing
  - New protoboard size: 90mm × 55mm (custom cut from ElectroCookie stock)
- ✅ **ALL HARDWARE DOCUMENTATION UPDATED**
  - `PROTOBOARD_LAYOUT.md`: Completely rewritten with LED circuits, updated BOMs, LED power budget
  - `PIN_ALLOCATION_MATRIX.md`: 11 GPIO pins allocated for LEDs (D4, D11-12, D23-25, A0-2, A5, CAN_TX)
  - `JACK_WIRING_GUIDE.md`: Added complete LED wiring section (white + RGB circuits, testing, troubleshooting)
  - `REBUILD_PLAN.md`: RGB LED specifications and mode indication documented
- ✅ **DETAILED MEASUREMENTS CALCULATED**
  - Exact jack X-positions from left edge: 8, 20, 32, 44, 65, 85mm (bottom row); 20, 32mm (top row)
  - Jack Y-heights from base: 15mm (bottom row), 27mm (top row)
  - LED positions: Jack X + 7mm offset
  - Verified all components fit within 95mm width (92mm + 3mm margin = 95mm internal)

### Previous Session Summary (Session 20)
**What was accomplished:**
- ✅ **COMPLETE 3D-PRINTABLE ENCLOSURE DESIGNED**
  - Parametric OpenSCAD design: `hardware/enclosure/prisme_enclosure.scad`
  - Semi-transparent PLA optimized (3.5mm walls for strength)
  - Compact 90mm × 65mm × 57.5mm external dimensions
  - Custom-cut 75mm × 50mm protoboards (from 97mm × 89mm ElectroCookie stock)
  - All 8 back panel connectors aligned in professional 2-row grid layout
- ✅ **STL FILES GENERATED (READY FOR 3D PRINTING)**
  - `prisme_box.stl` (414KB) - Main enclosure with jack holes, screw posts, ventilation
  - `prisme_lid.stl` (229KB) - Top cover with OLED window, button holes, countersinks
  - Designed for 0.2mm layer height, 20% infill, no supports needed
- ✅ **COMPREHENSIVE WIRING GUIDE CREATED**
  - `docs/hardware/JACK_WIRING_GUIDE.md` - Complete assembly reference (400+ lines)
  - All 10 jack connections documented with circuit paths and component values
  - Step-by-step assembly sequence (6 phases)
  - Power distribution strategy and current budget
  - Troubleshooting guide for each subsystem
- ✅ **PROTOBOARD LAYOUT FINALIZED**
  - `docs/hardware/PROTOBOARD_LAYOUT.md` - Physical component placement
  - OUTPUT Board (bottom): CV Out, V-Trig/S-Trig, Custom CC jacks at rear edge
  - INPUT Board (top): CV In, Gate In, MIDI In/Out, USB-C at rear edge
  - Professional-grade filtering and protection on all I/O
  - Complete BOM for both boards
- ✅ **ENCLOSURE DESIGN ITERATIONS**
  - Initial size too large → User wanted "1/3 smaller"
  - Fixed jack size error (1/4" → 1/8")
  - Fixed output jack naming (V-Trig and S-Trig are ONE jack, not two)
  - Added MIDI DIN connectors (user feedback: "where's our MIDI?")
  - **Critical methodology change:** Design protoboards FIRST, then enclosure (user correction)
  - Aligned USB-C with MIDI Out to form clean grid (user feedback)
  - Dark colors for OpenSCAD visibility (dimgray/slategray)

**Design Evolution:**
- **Problem:** Initial enclosure design created jack overlaps, didn't match physical reality
- **User Feedback:** "Ports are overlapping and you're not being diligent and considering the physical reality of our breadboards. This is a mess. Let's take a step back."
- **Solution:** Complete redesign from protoboards up
  - Calculated exact component footprints
  - Positioned all jacks on protoboard rear edges with precise measurements
  - Made enclosure holes EXACTLY match protoboard positions
  - Result: Clean 2-row grid layout with all connectors aligned

**Back Panel Layout (Final):**
```
TOP ROW:    [CV In] [Gate In] [MIDI In] [MIDI Out]
             13mm    23mm      35.5mm    55.5mm

BOTTOM ROW: [CV Out] [V/S-Trig] [Custom CC]        [USB-C]
             13mm      23mm       33mm            58.5mm
                                                  (aligned)
```

**Files Created (This Session):**
- `hardware/enclosure/prisme_enclosure.scad` (NEW) - Parametric 3D model (404 lines)
- `hardware/enclosure/prisme_box.stl` (NEW) - Print-ready box STL (414KB)
- `hardware/enclosure/prisme_lid.stl` (NEW) - Print-ready lid STL (229KB)
- `docs/hardware/JACK_WIRING_GUIDE.md` (NEW) - Complete wiring reference (400+ lines)
- `docs/hardware/PROTOBOARD_LAYOUT.md` (UPDATED) - Finalized with rear edge jack positions
- `docs/context/CONTEXT.md` (UPDATED) - This session handoff

**Next Steps (Session 21 - Hardware Fabrication):**
1. **[HIGH]** 3D print enclosure (box + lid) using semi-transparent PLA
2. **[HIGH]** Order components from PROTOBOARD_LAYOUT.md BOM:
   - 2× ElectroCookie protoboards (97mm × 89mm, will cut to 75mm × 50mm)
   - 5× 1/8" (3.5mm) mono jacks (panel mount)
   - 2× 5-pin DIN MIDI jacks (panel mount)
   - 1× USB-C panel mount breakout
   - Resistors, capacitors, diodes per BOM
   - NPN transistor (2N3904) for S-Trig
3. **[MEDIUM]** Cut protoboards to exact dimensions (75mm × 50mm)
4. **[MEDIUM]** Populate OUTPUT board following JACK_WIRING_GUIDE.md
5. **[MEDIUM]** Populate INPUT board following JACK_WIRING_GUIDE.md
6. **[MEDIUM]** Test circuits before enclosure assembly
7. **[LOW]** Final assembly and hardware integration testing

**Git Status:**
- **Branch:** feature/translation-hub
- **Last Commit:** c15ec61 - docs: Update session handoff (Session 19 - OLED split-screen bug blocking)
- **Working Tree:** Has uncommitted changes
  - Modified: Multiple files from Sessions 19-20
  - New: Complete hardware/ directory with enclosure design and STL files
  - New: Comprehensive wiring and layout documentation
- **Remote:** Behind origin/main (will commit after handoff)

**Important Context for Next Session:**
- Session 19 display bug still unresolved but no longer blocking
- Hardware fabrication now takes priority (physical prototyping phase)
- Once hardware assembled, can debug display on actual device
- All software features complete (polyphonic routing, menu UI, CV/Gate)
- Next phase: Build physical prototype, test with real hardware

---

### Previous Session Summary (Session 19)
**What was accomplished:**
- ✅ **DEPLOYMENT SCRIPT UPDATED FOR PRISME RENAME**
  - Fixed `scripts/deploy.py` file mapping from `arp/` → `prisme/` paths
  - Successfully deployed 14 files to Feather M4 hardware
  - Deployment automation now working correctly
- ✅ **POLYPHONIC ROUTING COMPLETE (Phase 5 from Session 18)**
  - Note priority implementation: Highest, Lowest, Last, First
  - Polyphonic → Monophonic CV conversion working in code
  - Ready for hardware testing (blocked by display bug)
- ✅ **MENU UI COMPLETE (Phase 6 from Session 18)**
  - Added CV category to menu with note priority selection
  - Menu navigation structure in place
  - Ready for testing (blocked by display bug)
- ⚠️ **CRITICAL BLOCKER: OLED SPLIT-SCREEN BUG NOT FIXED**
  - **Issue:** Display shows BOTH portrait and landscape content simultaneously
  - **User reported:** "still broken the exact same way" after all fix attempts
  - **Multiple fix attempts ALL FAILED:**
    1. Changed display rotation from 0° to 180° and back - no effect
    2. Added gc.collect() and delays - no effect
    3. Switched between .show() and .root_group - no effect
    4. Tried .fill(0) method - caused crash (invalid method)
    5. Added empty group initialization - no effect
    6. Double rotation initialization - no effect
    7. Rewrote display.py to match official Adafruit docs - **STILL BROKEN**
  - **Research conducted:**
    - Used Context7 MCP to search for SH1107 libraries
    - Used Firecrawl MCP to scrape official Adafruit tutorial
    - Found correct initialization pattern from https://learn.adafruit.com/adafruit-128x64-oled-featherwing/circuitpython
    - Implemented exactly as documented - still didn't fix it
  - **Root cause unknown** - needs deeper investigation

**Critical User Feedback:**
- User became frustrated with trial-and-error approach
- Demanded documentation-based solution (not "hacker" random fixes)
- Explicitly requested using MCPs to get official documentation
- After using MCPs and implementing correctly, display STILL broken

**Hardware Testing Blocked:**
- Cannot test menu navigation (display unreadable)
- Cannot test polyphonic MIDI loopback
- Cannot test note priority modes on CV output
- All Phase 7 hardware testing tasks blocked

**Files Modified (This Session):**
- `scripts/deploy.py` - Updated file mapping for prisme rename (arp → prisme)
- `prisme/ui/display.py` - Multiple rewrites attempting to fix split-screen bug
- `prisme/utils/config.py` - Changed display_rotation default (0° ↔ 180°)
- `docs/context/CONTEXT.md` - This session handoff update

**Next Steps (Session 20 - URGENT):**
1. **[CRITICAL - BLOCKER]** Investigate OLED split-screen bug deeper:
   - Check `boot.py` for display initialization conflicts
   - Verify I2C bus initialization sequence in main.py
   - Look for existing display state not being cleared
   - Test with minimal display code (eliminate all other factors)
   - Consider hardware issue (try different OLED FeatherWing?)
   - Check if previous display configuration is cached somewhere
   - Review CircuitPython 10.x display initialization best practices
2. **[HIGH]** Once display fixed: Test menu navigation for note priority
3. **[HIGH]** Test polyphonic MIDI loopback (Arp OFF mode)
4. **[HIGH]** Test note priority modes on CV output
5. **[MEDIUM]** Complete hardware integration testing

**Git Status:**
- **Branch:** feature/translation-hub
- **Last Commit:** 06c6f00 - feat: Add note priority selection to CV menu (Phase 6)
- **Working Tree:** Has uncommitted changes
  - Modified: `docs/context/CONTEXT.md`, `docs/hardware/PIN_ALLOCATION_MATRIX.md`, `docs/hardware/WIRING_COLOR_CONVENTION.md`, `prisme/ui/display.py`, `prisme/utils/config.py`, `scripts/deploy.py`
  - Untracked: Many test files and new hardware docs
- **Remote:** Behind origin/main (need to resolve blocker before committing)

**Important Context for Next Session:**
- This is a recurring bug from previous sessions
- User mentioned "we've had this issue in the past"
- Previous solution might exist in git history
- Display WAS working in earlier sessions
- Something changed that broke display initialization
- Need to find what changed and revert or fix properly

---

### Previous Session Summary (Session 18)
**What was accomplished:**
- ✅ **ROOT CAUSE IDENTIFIED: Jack Wiring Pinout Incorrect**
  - Comprehensive diagnostic tested all 4 MCP4728 channels at chip pins
  - Initial finding: Channel A showed 0V when connected to jack
  - **Actual cause:** Wrong jack pin used for signal (created short circuit)
  - **Conclusion:** ALL 4 channels working perfectly - no hardware damage
  - **Solution:** Correct Xiaoyztan jack pinout documented
- ✅ **JACK WIRING ISSUE DIAGNOSED AND RESOLVED**
  - **Problem:** Any VOUT pin connected to jack dropped to 0V
  - **Root cause:** Jack pinout misidentified - signal on wrong pin
  - **Discovery:** Plugging TS cable into jack created short circuit
  - **Solution:** Correct pinout documented for Xiaoyztan TS jacks
- ✅ **XIAOYZTAN JACK PINOUT DOCUMENTED**
  - TOP PIN (nearest jack) = SLEEVE (ground) ← WHITE wire
  - MIDDLE PIN = Mounting lug (ignore, not connected)
  - FAR LEFT PIN = TIP (signal) ← RED wire
  - Updated `docs/hardware/WIRING_COLOR_CONVENTION.md` with correct pinout
  - Simple 2-wire connection, no jumpers needed (true TS mono jacks)
- ✅ **CV PITCH OUTPUT VERIFIED WORKING (Channel A)**
  - MCP4728 Channel A (pin 4, VOUTA) → Jack FAR LEFT PIN (correct pinout)
  - 1V/octave standard confirmed: C0=1V, C1=2V, C2=3V, C3=4V, C4=5V
  - No voltage drop when cable plugged in with correct wiring
  - All 4 MCP4728 channels verified healthy - no hardware damage!

**Key Technical Learnings:**
1. **Hardware diagnosis:** Isolate by testing all channels, not just one
2. **Jack types:** Xiaoyztan "3 pins" are TS mono (pin 3 = mounting lug)
3. **Short circuit detection:** Voltage drops to 0V when output shorted to ground
4. **I2C singleton:** Always use `board.I2C()`, never create new instances
5. **Channel reassignment:** MCP4728 channels are interchangeable (A→B seamless)

**Updated Channel Allocation:**
- **Channel A (pin 4, VOUTA)** - CV Pitch (1V/octave) ✅ WORKING
- **Channel B (pin 5, VOUTB)** - V-Trig Gate (ready to wire)
- **Channel C (pin 6, VOUTC)** - Reserved for future expansion
- **Channel D (pin 7, VOUTD)** - Custom CC (ready to wire)

**All Outputs Verified Working:**
- ✅ **Jack #1 - CV Pitch** (Channel A, pin 4) - 1V/octave, 0-5V range
- ✅ **Jack #2 - Dual Gate** (Channel B + GPIO D10) - V-Trig (0V/5V) and S-Trig (open/short)
- ✅ **Jack #3 - Custom CC** (Channel C, pin 6) - 0-5V modulation output

**Files Created (This Session):**
- `docs/hardware/WIRING_COLOR_CONVENTION.md` - Updated with Xiaoyztan jack pinout and final channel allocation
- `tests/mcp4728_channel_a_debug.py` (NEW) - Quick diagnostic test
- `tests/mcp4728_full_diagnostic.py` (NEW) - All-channel voltage test
- `tests/dual_gate_test.py` (NEW) - V-Trig/S-Trig switchable test
- `tests/strig_simple_test.py` (NEW) - S-Trig GPIO toggle test
- `tests/strig_scope_test.py` (NEW) - S-Trig with pull-high for scope visibility
- `tests/custom_cc_test.py` (NEW) - Custom CC sweep test

**Next Steps (Session 19):**
1. **[HIGH]** Test all outputs with actual synthesizer/VCO
2. **[HIGH]** Integrate CV/Gate outputs into main.py (production code)
3. **[MEDIUM]** Create menu settings for gate mode selection (V-Trig/S-Trig)
4. **[MEDIUM]** Test arpeggiator → CV/Gate pipeline end-to-end
5. **[LOW]** Optional: Wire LM358N op-amp for 0-10V CV (if specific VCO needs it)

**Git Status:**
- **Branch:** feature/translation-hub
- **Last Commit:** 22c6608 - docs: Add comprehensive output jack wiring guides with RED/WHITE color standard
- **Working Tree:** Modified (CONTEXT.md, WIRING_COLOR_CONVENTION.md updates pending)
- **Untracked:** New diagnostic test files
- **Remote:** Behind origin/main (will commit and push after session)

---

### Previous Session Summary (Session 17)
**What was accomplished:**
- ✅ **WIRING COLOR CONVENTION ESTABLISHED**
  - Official standard: RED = Tip (signal), WHITE = Sleeve (ground)
  - Created `docs/hardware/WIRING_COLOR_CONVENTION.md` - authoritative reference
  - Updated all wiring guides to use RED/WHITE convention
  - Cleaner, more consistent than previous black ground approach
- ✅ **COMPREHENSIVE WIRING DOCUMENTATION CREATED**
  - `docs/hardware/OUTPUT_JACKS_WIRING_GUIDE.md` - Complete 6-phase guide (2,800+ lines)
  - `docs/hardware/QUICK_START_JACK_WIRING.md` - Fast-track guide for first output
  - Covers: CV Pitch, V-Trig Gate, S-Trig, Custom CC, optional 0-10V op-amp
  - Each phase: wiring steps, schematics, testing, troubleshooting
- ✅ **CV PITCH OUTPUT JACK WIRED**
  - MCP4728 Channel A (VOUTA) → 1/8" TS jack
  - RED wire to Tip, WHITE wire to Sleeve
  - Continuity tests passed (3/3)
  - Ready for voltage testing
- ⚠️ **TESTING BLOCKED - NO VOLTAGE AT CHANNEL A**
  - Deployed working test code from Session 12 (`cv_1v_octave_test.py`)
  - Code runs without errors, cycles through notes C0-C4
  - MCP4728 has power (VDD = 5V measured)
  - **Problem:** Measuring 0V at Channel A output pin (expected 0-5V)
  - Wiring verified correct via continuity tests
  - **Root cause unknown** - needs hardware investigation

**Research Conducted:**
- Deep search confirmed MCP4728 Channel A was working in Sessions 12-13
- Found exact working code and test files
- Session 12: Full 0-5V range verified with multimeter
- Session 13: Dual gate output (Ch C) verified on scope
- Critical bug fix history: `.value` vs `.raw_value` property (Session 12)

**Blocker Details:**
- Issue: MCP4728 Channel A not outputting voltage
- Tests tried: `cv_1v_octave_test.py`, `mcp4728_correct_voltage_test.py`
- Hardware checks: VDD power confirmed, continuity verified
- Next action needed: Verify I2C communication, check MCP4728 physical connections

**Files Created (This Session):**
- `docs/hardware/OUTPUT_JACKS_WIRING_GUIDE.md` (NEW)
- `docs/hardware/QUICK_START_JACK_WIRING.md` (NEW)
- `docs/hardware/WIRING_COLOR_CONVENTION.md` (NEW)

**Next Steps (Session 18):**
1. **[IMMEDIATE - BLOCKER]** Debug MCP4728 Channel A voltage output issue
   - Run I2C scan to verify MCP4728 is responding (0x60)
   - Check SDA/SCL physical connections to M4 (D21/D22)
   - Verify MCP4728 wakeup and configuration sequence
   - Test with oscilloscope if multimeter shows 0V
   - Consider reseating MCP4728 or checking for hardware damage
2. **[HIGH]** Once CV Pitch working: Wire V-Trig Gate output (Channel C)
3. **[HIGH]** Wire S-Trig output circuit (GPIO D10 + NPN transistor)
4. **[MEDIUM]** Wire Custom CC output (Channel D)
5. **[LOW]** Optional: Wire LM358N op-amp for 0-10V CV

**Git Status:**
- **Branch:** feature/translation-hub
- **Last Commit:** 22c6608 - docs: Add comprehensive output jack wiring guides with RED/WHITE color standard
- **Working Tree:** Clean
- **Untracked:** None
- **Remote:** Behind origin/main (will push after resolving blocker)

---

### Previous Session Summary (Session 16)
**What was accomplished:**
- ✅ **TRANSLATION HUB IMPLEMENTATION COMPLETE (Phases 1-5)**
  - **Phase 1-2:** Created class-based translation layer system with Scale→Arp pipeline
  - **Phase 3:** Implemented clock transformations (swing, multiply, divide) using Roger Linn's formula
  - **Phase 4:** Integrated USB MIDI for note input alongside existing clock sync
  - **Phase 5:** Migrated to class-based arpeggiator with 16 patterns including new Strum mode
  - **NVM v3 Format:** Expanded settings from 19 to 28 values (40 bytes/256)
  - **All 30 unit tests passing:** test_translation.py (8), test_clock.py (14), test_input_router.py (8)
- ✅ **NEW FEATURE: STRUM ARPEGGIATOR MODE (Pattern 16)**
  - Plays held notes sequentially with configurable strum speed (fast→slow)
  - Perfect for guitar-style chord strumming on synths
  - Implemented in `arp/core/arpeggiator.py:224-246`
- ✅ **NEW FEATURE: DISPLAY ROTATION FOR LEFT/RIGHT-HANDED USERS**
  - Software-based 180° rotation with automatic button remapping (A↔C swap)
  - Added to Firmware settings menu (0° = right-handed, 180° = left-handed)
  - Single enclosure design accommodates both orientations
  - Changes: `config.py` (NVM v3→29 values), `display.py`, `buttons.py`, `menu.py`, `main.py`
- ✅ **PROJECT CLEANUP - REMOVED VINTAGECAPTURE**
  - Deleted entire `VintageCapture/` directory (19 files, C++ VST plugin)
  - Cleaned all references from README.md, PROJECT_STATUS.md, CONTEXT.md, OCCUPANCY.md
  - Focused project scope: MIDI/CV Translation Hub only
- ✅ **SESSION END PROTOCOL EXECUTED**
  - Manual backup created: `_Backups/Arp_manual_20251101_210929.zip`
  - All changes staged and ready to commit
  - Documentation updated

**Key Technical Achievements:**
1. **Translation Layer Architecture:** Modular layer system (Scale, Arp, Clock) with fixed ordering
2. **Class-Based Arpeggiator:** 16 patterns with scale quantization and configurable octave range
3. **Unified Clock System:** Single rate control (±8× multiply/divide) + timing feel (50-100%)
4. **Input Routing:** Support for MIDI IN, USB MIDI, CV IN, Gate IN sources
5. **Display Rotation:** Hardware-agnostic enclosure design with software orientation control

**Files Modified (This Session):**
- **Core Implementation:**
  - `arp/core/translation.py` (NEW) - Translation layer pipeline
  - `arp/core/layers.py` (NEW) - ScaleQuantizeLayer + ArpeggiatorLayer classes
  - `arp/core/arpeggiator.py` - Added Strum mode, updated all 16 patterns
  - `arp/core/input_router.py` (NEW) - Input source abstraction
  - `arp/core/clock.py` - Timing feel + unified rate transformations
- **Display Rotation:**
  - `arp/utils/config.py` - Added display_rotation (NVM v3: 28→29 values)
  - `arp/ui/display.py` - Apply rotation from settings
  - `arp/ui/buttons.py` - Button remapping for 180° rotation
  - `arp/ui/menu.py` - Added rotation toggle in Firmware category
  - `main.py` - Reordered initialization (settings before display)
- **Documentation:**
  - `README.md` - Removed VintageCapture section
  - `PROJECT_STATUS.md` - Removed VintageCapture references
  - `docs/OCCUPANCY.md` - Removed VintageCapture references
  - `docs/context/CONTEXT.md` - This session handoff
  - `docs/hardware/ENCLOSURE_DESIGN.md` - Updated for display rotation

**Next Steps (Session 17+):**
1. **[IMMEDIATE]** Test display rotation on hardware (Settings → Firmware → Display Rotation)
2. **[HIGH]** Test Translation Hub on hardware (THRU vs TRANSLATION routing modes)
3. **[HIGH]** Verify all 16 arpeggiator patterns work correctly
4. **[HIGH]** Test Strum mode with different strum speeds
5. **[MEDIUM]** Complete enclosure design (3D printed case with display rotation in mind)
6. **[MEDIUM]** Implement CV/Gate output driver for MCP4728
7. **[LOW]** Add velocity curves and latch mode

**Git Status:**
- **Branch:** feature/translation-hub
- **Last Commit:** 3ea4985 - docs: Add comprehensive 3D printed enclosure design spec
- **Staged Changes:** VintageCapture deletion + all implementation files
- **Working Tree:** All changes staged, ready to commit
- **Remote:** Behind origin/main (need to push after commit)

---

### Previous Session Summary (Session 15)
**What was accomplished:**
- ✅ **TRANSLATION HUB RESEARCH COMPLETE (97% CONFIDENCE)**
  - Created comprehensive prep document via deep codebase analysis
  - Identified 10 critical implementation questions (including 1 blocker)
  - Used FireCrawl MCP to research authoritative documentation sources
  - Answered all 10 questions with evidence and code examples
  - Created detailed 8-phase implementation plan (12-19 hours estimated)
- ✅ **RESEARCH DELIVERABLES CREATED (4 documents, 1,883 lines)**
  - `TRANSLATION_HUB_PREP_DOC.md` (500 lines) - Deep codebase analysis
  - `TRANSLATION_HUB_QUESTIONS.md` (341 lines) - 10 critical questions
  - `TRANSLATION_HUB_ANSWERS.md` (605 lines) - Complete research findings
  - `TRANSLATION_HUB_IMPLEMENTATION_PLAN.md` (437 lines) - Phased implementation plan
- ✅ **PROJECT REBRANDED TO "prisme"**
  - Updated README.md to reflect Translation Hub architecture
  - Updated PROJECT_STATUS.md with Session 15 milestone
  - Committed and pushed all documentation updates to origin/main

**Key Research Findings:**
1. **Class-based architecture recommended** - Official Adafruit CircuitPython design patterns
2. **USB MIDI can handle both clock AND notes** - Same port supports multiple MIDI objects
3. **Swing implementation from Roger Linn** - Inventor of swing! Delay even 16th notes by percentage
4. **PyTest + mocking for testing** - CircuitPython modules can be mocked for unit tests
5. **Clock transformations via tick interval** - Clean formula: `(base_interval * divide) / multiply`

---

### Session 14 Summary
**What was accomplished:**
- ✅ **CUSTOM CC OUTPUT SYSTEM - COMPLETE SOFTWARE IMPLEMENTATION**
  - Complete MIDI-to-CV conversion system for MCP4728 Channel D
  - 5 source types: Disabled, CC (0-127), Aftertouch, Pitch Bend, Velocity
  - 4 smoothing levels: Off, Low, Mid, High (exponential moving average)
  - Learn Mode: Hold Button B in Custom CC menu to capture CC number
  - Human-readable CC names (e.g., "CC 74: Filter Cutoff")
  - Real-time MIDI processing before pass-through (lowest latency)
- ✅ **COMPREHENSIVE IMPLEMENTATION (3,715 lines added!)**
  - `config.py`: Custom CC settings + NVM storage (19 values, 27 bytes/256)
  - `cv_gate.py`: Voltage conversion for all 4 sources + smoothing
  - `midi_custom_cc.py` (NEW): 169-line CustomCCHandler with Learn Mode
  - `main.py`: CV Output initialization + Custom CC integration
  - `menu.py`: 7th category added with 3 settings
  - `midi_cc_names.py` (NEW): Database of 128 MIDI CC names
- ✅ **EXTENSIVE DOCUMENTATION CREATED**
  - `MIDI_TO_CV_VOLTAGE_STANDARDS.md` (721 lines) - Comprehensive voltage reference
  - `CUSTOM_CC_IMPLEMENTATION_PLAN.md` (638 lines) - Complete implementation plan
  - `CUSTOM_CC_PREP_DOC.md` (463 lines) - Codebase analysis for planning
  - `CUSTOM_CC_FINAL_QUESTIONS.md` (358 lines) - 10 critical questions identified
  - `CUSTOM_CC_ANSWERS.md` (325 lines) - All questions answered via research
  - `CUSTOM_CC_PROFESSIONAL_APPROACH.md` (569 lines) - Hybrid manual+learn design

**Implementation Highlights:**
- **Methodology Success:** User requested thorough planning before implementation
  - Created prep doc by reading entire codebase (87% confidence achieved)
  - Identified 10 critical questions (including 1 blocker: CV not initialized)
  - Used Perplexity MCP to research M4 specs and CircuitPython best practices
  - Answered all 10 questions with evidence and specific line numbers
  - Implemented with 95% confidence and ~2 hours (as estimated!)
- **Technical Excellence:**
  - Exponential moving average smoothing: `(alpha × target) + ((1-alpha) × current)`
  - Alpha coefficients: Off=1.0, Low=0.9, Mid=0.7, High=0.5
  - Auto-save after every setting change (matches existing pattern)
  - Button B long press unused - perfect for Learn Mode
  - Memory impact: ~500 bytes (0.36% of available RAM)
- **Menu Integration:**
  - Category navigation (7 categories now)
  - 3 settings: Source, CC Number, Smoothing
  - CC number display with human names when source is CC
  - Graceful handling when CC Number not applicable (shows "N/A")

**Hardware Requirements (Still Pending):**
- ⏳ Wire third 1/8" TRS jack to MCP4728 Channel D
- ⏳ Create hardware test (`tests/custom_cc_test.py`)
- ⏳ Verify voltage accuracy with multimeter (±20mV target)

**Git Status:**
- **Branch:** main
- **Last Commit:** 106df84 - feat: Add Custom CC output system with Learn Mode and smoothing
- **Working Tree:** Clean
- **Ahead of origin:** 2 commits (needs push)

**Next Steps:**
1. **[HIGH]** Create `tests/custom_cc_test.py` for voltage verification
2. **[HIGH]** Wire third TRS jack for Custom CC output (Channel D)
3. **[MEDIUM]** Test with multimeter (verify ±20mV accuracy like Polyend Poly 2)
4. **[MEDIUM]** Test Learn Mode workflow with actual MIDI controller
5. **[LOW]** Consider Phase 2: Bipolar voltage for pitch bend (±5V)

### Previous Session Summary (Session 13)
**What was accomplished:**
- ✅ **TRUE S-TRIG CIRCUIT IMPLEMENTED AND VERIFIED**
  - NPN transistor (2N3904) switching circuit on GPIO D10
  - Idle state: Open circuit (floating, >10MΩ) - verified with multimeter
  - Active state: Short to ground (<1Ω) - verified with multimeter
  - **Real switch-based triggering** for vintage synth compatibility
- ✅ **DUAL GATE OUTPUT SYSTEM INTEGRATED**
  - V-TRIG: MCP4728 Channel C (voltage-based, 0V/5V)
  - S-TRIG: GPIO D10 + NPN transistor (switch-based, open/short)
  - Single test with button toggle between modes
  - OLED display shows active mode
  - Both outputs verified working on hardware!
- ✅ **PIN ALLOCATION MATRIX CREATED**
  - `docs/hardware/PIN_ALLOCATION_MATRIX.md` - AUTHORITATIVE pin reference
  - Documents all current and planned pin usage
  - Prevents conflicts and enables future planning
  - D10 permanently assigned to S-Trig GPIO
  - D0/D1 reserved for MIDI FeatherWing
- ✅ **COMPLETE DOCUMENTATION**
  - `docs/hardware/TRUE_STRIG_CIRCUIT.md` - Circuit theory and design
  - `docs/hardware/STRIG_BREADBOARD_GUIDE.md` - Step-by-step wiring guide
  - `docs/SESSION_13_HANDOFF.md` - Complete session handoff
  - `tests/gate_dual_output_test.py` - Working dual output test

**Critical Hardware Discovery:**
- **1kΩ base resistor required** - Initially used 100kΩ which prevented transistor saturation
- Once corrected to 1kΩ, circuit worked perfectly
- Verified switching behavior: LED ON → Short (<1Ω), LED OFF → Open (OL)

**Universal Synth Compatibility Achieved:**
- Modern synths (V-TRIG): Eurorack, modern hardware, MIDI-to-CV converters
- Vintage synths (S-TRIG): ARP 2600, Korg MS-20, Yamaha CS series
- **50+ years of synthesizer compatibility in one device!**

### Previous Session Summary (Session 12)
**What was accomplished:**
- ✅ **CRITICAL BUG DISCOVERED AND FIXED: MCP4728 `.value` vs `.raw_value`**
  - Root cause: Using `.value` property (16-bit) with 12-bit calculated values
  - Library was bit-shifting: `raw_value = value >> 4` causing 1/16th voltage output
  - This perfectly explained 0.30V readings: `(255/4095) × 4.83V = 0.30V`
  - **Solution:** Use `.raw_value` property for direct 12-bit DAC control
  - Verified full 0-5V output range working perfectly
- ✅ **RESEARCH: I2C BUS CONTENTION AND DISPLAY THROTTLING**
  - Investigated I2C bus sharing impact on CV timing accuracy
  - Measured: DAC update = 0.7ms, OLED update = 86.6ms (blocking!)
  - At 200 BPM 16th notes (75ms budget), OLED completely misses timing
  - **Solution:** Display throttling (10Hz max) + existing sleep mode optimizations
  - Created `TIMING_ARCHITECTURE.md` with TIER 1 (real-time) vs TIER 2 (non-critical) patterns
- ✅ **CV OUTPUT DRIVER CREATED**
  - `arp/drivers/cv_output.py` - Production CV driver with throttling
  - Pre-calculated 128-note MIDI lookup table (zero-latency)
  - Built-in display update throttling (100ms intervals)
  - 1V/octave formula: `raw_value = MIDI_note × 68.27`
- ✅ **CRITICAL DISCOVERY: TL072 LIMITATION**
  - TL072 **CANNOT handle 0V inputs** in single-supply operation
  - Common-mode input range: V- + 4V minimum (requires ≥4V inputs)
  - At 0V input: TL072 saturated to ~12V (phase inversion)
  - **Hours wasted** troubleshooting before researching op-amp limitations
  - **Lesson learned:** Research component specs immediately when behavior is anomalous
- ✅ **LM358N SOLUTION VERIFIED WORKING!**
  - Replaced TL072 with LM358N (rail-to-rail inputs, same pinout)
  - Tested unity gain: 0V→0V, 5V→5V ✓ (works at 0V!)
  - Tested 2× gain circuit: 0V→0V, 5V→9.5V ✓ (full range working!)
  - **ACHIEVEMENT:** Complete 0-10V CV output chain verified end-to-end
- ✅ **COMPREHENSIVE DOCUMENTATION UPDATED**
  - `docs/hardware/LM358_WIRING_GUIDE.md` - Complete wiring guide with TL072 warning
  - `docs/hardware/MCP4728_CV_GUIDE.md` - DAC implementation guide
  - `docs/architecture/TIMING_ARCHITECTURE.md` - I2C timing analysis
  - `tests/tl072_gain_circuit_test.py` - Voltage stepping test (works with LM358N)

**Critical Bug Details:**
**The `.value` vs `.raw_value` Property Trap:**
```python
# WRONG (what previous session did)
dac.channel_a.value = 4095      # Expects 16-bit, gets bit-shifted
# Result: raw_value = 4095 >> 4 = 255 → Only 0.30V

# CORRECT (what works)
dac.channel_a.raw_value = 4095  # Direct 12-bit control → Full 4.83V
```

**Key Technical Discoveries:**
1. **raw_value vs value:** Always use `raw_value` for CV applications (direct 12-bit)
2. **1V/Octave Formula:** `raw_value = MIDI_note × 68.27` (for 5V reference)
3. **Lookup Table Best Practice:** Pre-calculate all 128 MIDI notes at init
4. **MCP4728 Performance:** 6µs settling, 200µs I2C transaction = excellent for real-time
5. **Real-World Validation:** Multiple production projects confirm this approach

**Hardware Status:**
- ✅ New Feather M4 CAN - stable, CircuitPython 10.0.3
- ✅ New OLED FeatherWing - tested, working
- ✅ **MCP4728 DAC - FULLY WORKING! Full 0-5V output verified**
- ✅ LM7805 regulator - correctly installed (5V output verified)
- ✅ **LM358N op-amp circuit - VERIFIED WORKING! Full 0-10V output**
- ✅ **S-Trig transistor circuit - DESIGNED (D10 + NPN transistor)**
- ❌ TL072 op-amp - **DO NOT USE** (cannot handle 0V inputs in single-supply)
- 🔶 MIDI FeatherWing - **BREADBOARDED, NOT STACKED** (D0/D1 via jumper wires)
  - ⚠️ **IMPORTANT:** MIDI FeatherWing will NEVER be stacked on M4
  - MIDI I/O stays on breadboard, connected via jumper wires to D0/D1
  - Only OLED FeatherWing is stacked on the M4

**📌 PIN ALLOCATION:** See `docs/hardware/PIN_ALLOCATION_MATRIX.md` (AUTHORITATIVE SOURCE)

**Git Status:**
- **Branch:** main
- **Last Commit:** 1ce728e - docs: Update CONTEXT.md with Session 10 summary
- **Working Tree:**
  - Modified: `docs/context/CONTEXT.md`
  - New: `docs/hardware/LM358_WIRING_GUIDE.md` (renamed from TL072)
  - New: `docs/hardware/MCP4728_CV_GUIDE.md`
  - New: `docs/architecture/TIMING_ARCHITECTURE.md`
  - New: `arp/drivers/cv_output.py`
  - New: Multiple test files in `tests/`

**Critical Next Steps:**
1. **[HIGH]** Wire 1/8" output jacks (CV pitch + Gate + S-Trig)
2. **[HIGH]** Create end-to-end test: MIDI In → CV/Gate Out
3. **[MEDIUM]** Build arpeggiator core (note buffer, patterns)
4. **[MEDIUM]** Test with actual eurorack VCO for 1V/octave tracking
5. **[LOW]** Consider enclosure design (MIDI stays breadboarded for prototyping)

---

## Session History

### Session 20 (2025-11-02)
- **Focus:** Complete 3D enclosure design and comprehensive wiring documentation
- **Outcome:** ✅ **FULL SUCCESS** - Hardware design ready for fabrication!
- **Major Achievements:**
  - Created parametric OpenSCAD enclosure (90mm × 65mm × 57.5mm)
  - Generated print-ready STL files (box + lid)
  - Wrote complete wiring guide for all 10 connectors
  - Finalized protoboard layout with exact jack positions
  - Fixed multiple design issues through iterative user feedback
- **Key Learning:** Design protoboards FIRST, then enclosure (don't guess connector positions)
- **Deliverables:**
  - `prisme_enclosure.scad` - Parametric 3D model
  - `prisme_box.stl` + `prisme_lid.stl` - Print-ready files
  - `JACK_WIRING_GUIDE.md` - 400+ line assembly reference
  - `PROTOBOARD_LAYOUT.md` - Component placement with BOM
- **Design Iterations:** 7 major revisions based on user feedback
  - Size reduction (1/3 smaller than initial)
  - Jack size correction (1/4" → 1/8")
  - Output naming fix (V-Trig/S-Trig = ONE jack)
  - Added MIDI DIN connectors
  - Methodology change (protoboards before enclosure)
  - Grid alignment (USB-C aligned with MIDI Out)
  - Dark colors for visibility
- **Status:** ✅ Complete - Ready for 3D printing and hardware assembly
- **Documentation:** CONTEXT.md updated, JACK_WIRING_GUIDE.md created, PROTOBOARD_LAYOUT.md finalized

### Session 19 (2025-11-02)
- **Focus:** Testing Translation Hub on hardware (polyphonic routing + menu UI)
- **Outcome:** ⚠️ **BLOCKED** - OLED split-screen bug preventing all hardware testing
- **Major Issue:**
  - Display shows portrait and landscape content simultaneously (split-screen)
  - Attempted 7 different fixes, all failed
  - Followed official Adafruit documentation exactly - still broken
  - User frustrated with trial-and-error approach
- **Accomplishments:**
  - Fixed deployment script for prisme rename (arp → prisme)
  - Successfully deployed code to hardware (14 files)
  - Phases 5-6 complete in code (polyphonic routing + menu UI)
- **Key Learning:** When multiple fix attempts fail, issue may be elsewhere (boot.py, I2C conflicts, hardware)
- **Blocker:** Display initialization preventing all Phase 7 hardware testing
- **Status:** ⚠️ Blocked - Needs deeper investigation of display initialization chain
- **Documentation:** Updated CONTEXT.md with comprehensive failure analysis

### Session 18 (2025-11-02)
- **Focus:** CV/Gate output jack wiring and MCP4728 debugging
- **Outcome:** ✅ **FULL SUCCESS** - All 3 output jacks verified working!
- **Major Achievement:** Root cause identified - jack pinout was incorrect (not hardware failure)
- **Status:** ✅ Complete - All CV/Gate outputs working

### Session 13 (2025-10-31)
- **Focus:** True S-Trig implementation and dual gate output system
- **Outcome:** ✅ **FULL SUCCESS** - Universal synth compatibility achieved!
- **Major Achievements:**
  - Implemented true S-Trig using NPN transistor switching circuit (GPIO D10)
  - Integrated V-TRIG and S-TRIG into single toggle-able test
  - Created PIN_ALLOCATION_MATRIX.md (authoritative pin reference)
  - Both gate outputs verified working on hardware (scope + multimeter)
- **Key Learning:** 1kΩ base resistor required (100kΩ won't saturate transistor)
- **Hardware Discovery:** True S-Trig is switch-based (open/short), not voltage-based
- **Breakthrough:** Complete gate/trigger compatibility - works with ANY synth from 1970s-present
- **Status:** ✅ Complete - Ready for MIDI integration and output jack wiring
- **Documentation:** SESSION_13_HANDOFF.md, TRUE_STRIG_CIRCUIT.md, STRIG_BREADBOARD_GUIDE.md, PIN_ALLOCATION_MATRIX.md

### Session 12 (2025-10-31)
- **Focus:** Complete 0-10V CV output chain (DAC + op-amp amplification)
- **Outcome:** ✅ **FULL SUCCESS** - End-to-end 0-10V CV output working!
- **Major Achievements:**
  - Fixed MCP4728 `.value` vs `.raw_value` bug (0-5V verified working)
  - Researched I2C bus contention, created display throttling solution
  - Created CVOutput driver with lookup table and throttling
  - **Discovered TL072 limitation** (cannot handle 0V in single-supply)
  - **Verified LM358N solution** (full 0-10V range working!)
- **Key Learning:** Research component specs immediately when behavior is anomalous (wasted hours on TL072)
- **Breakthrough:** Complete CV output chain verified: M4 → MCP4728 (0-5V) → LM358N (0-10V) → Eurorack
- **Status:** ✅ Complete - Ready for MIDI integration and end-to-end testing
- **Documentation:** LM358_WIRING_GUIDE.md, MCP4728_CV_GUIDE.md, TIMING_ARCHITECTURE.md, cv_output.py

### Session 11 (2025-10-31)
- **Focus:** Hardware recovery from 12V damage, I2C architecture design
- **Outcome:** New hardware installed, I2C documentation created, proper patterns established
- **Major Achievement:** Comprehensive I2C_ARCHITECTURE.md with multi-device best practices
- **Key Learning:** `board.I2C()` singleton pattern critical, MCP4728 power-down mode exists
- **Blocker:** MCP4728 voltage output verification (reading wrong values)
- **Status:** ⚠️ Blocked - Needs hardware power cycle and voltage verification test
- **Documentation:** SESSION_11_HANDOFF.md, I2C_ARCHITECTURE.md

### Session 10 (2025-10-24)
- **Focus:** CV output voltage requirements and op-amp circuit design
- **Outcome:** Complete 2× gain circuit designed, power architecture corrected
- **Major Achievement:** Discovered M4 CAN has no 5V pin (LM7805 regulator required)
- **Key Learning:** Always verify pinout availability before circuit design
- **Blocker:** LM7805 voltage regulator needed (ordered)
- **Status:** ⏸️ Paused - Resume when LM7805 arrives

### Session 9 (2025-10-24)
- **Focus:** Production planning and cost optimization for 200-unit run
- **Outcome:** Comprehensive PRODUCTION_ROADMAP.md created (800+ lines)
- **Major Achievement:** Custom PCB strategy saves $7,800-12,600 for 200 units
- **Key Decision:** RP2040-based custom PCB ($42-51/unit vs $89-105 with Feathers)
- **Status:** ✅ Complete - Ready for prototyping phase

### Session 8 (2025-10-23)
- **Focus:** Battery integration and MCP4728 DAC library setup
- **Outcome:** Battery power working, powerboost configured, comprehensive documentation created
- **Major Achievement:** Discovered voltage level requirements for MCP4728 (BSS138 level shifter needed)
- **Lesson Learned:** Powerboost schematic on one side, actual solder pads on the other
- **Status:** ✅ Complete - Ready for MCP4728 hardware testing

### Session 7 (2025-10-23)
- **Focus:** Session handoff and documentation review
- **Outcome:** Context review, planning for next steps
- **Status:** ✅ Complete

### Session 6 (2025-10-23)
- **Focus:** CV/Gate hardware planning and MIDI clock sync investigation
- **Outcome:** Discovered MIDI clock not integrated, clarified hardware constraints
- **Major Realization:** ClockHandler exists but unused - external sync is critical for vintage users
- **Status:** 🔄 In Progress - Ready for clock integration

### Session 4 (2025-10-22)
- **Focus:** Documentation optimization and /start command improvement
- **Outcome:** Created START_HERE.md and CONTEXT.md structure
- **Status:** ✅ Complete

### Session 3 (2025-10-22)
- **Focus:** OLED FeatherWing integration with CircuitPython 10.x
- **Outcome:** Fixed display driver (SH1107), updated to CP 10.x API
- **Lesson Learned:** Always verify hardware specs (SH1107 vs SSD1306)
- **Status:** ✅ Complete

### Session 2 (2025-10-21)
- **Focus:** Hardware validation and testing infrastructure
- **Outcome:** Created comprehensive_pin_test.py, validated all M4 pins
- **Status:** ✅ Complete

### Session 1 (2025-10-20)
- **Focus:** Initial setup, MIDI integration, breadboard testing
- **Outcome:** Hardware fully validated, MIDI pass-through working
- **Status:** ✅ Complete

---

## Active Work

### Current Task: Translation Hub Implementation (Phase 1)
**Status:** ⏳ Ready to start (Research complete - 97% confidence)
**Priority:** HIGH

**What needs to be done (Phase 1 - Foundation Setup):**
1. Create feature branch: `feature/translation-hub`
2. Create file structure:
   - `arp/core/translation.py` - TranslationPipeline class
   - `arp/core/layers.py` - Layer implementations (Scale, Arp)
   - `tests/test_translation.py` - PyTest unit tests
   - `tests/conftest.py` - PyTest configuration with CircuitPython mocks
   - `main_v2.py` - New architecture main file (keep main.py intact)
3. Expand Settings in `config.py`:
   - Routing mode (THRU / TRANSLATION)
   - Input source (MIDI IN / USB / CV IN / Gate IN)
   - Layer ordering (Scale→Arp or Arp→Scale)
   - Layer enables (scale_enabled, arp_enabled)
   - Clock transformations (multiply, divide, swing_percent)
4. Update NVM storage to accommodate 8 new settings bytes

**Implementation Plan:** See `docs/implementation/TRANSLATION_HUB_IMPLEMENTATION_PLAN.md`
**Estimated Effort:** 3-4 sessions @ 4-5 hours each (12-19 hours total)

---

## Important Decisions Made

### Hardware Decisions
- **OLED Driver:** Using SH1107 (not SSD1306) for 128x64 FeatherWing #4650
- **CircuitPython Version:** 10.0.3 (requires new i2cdisplaybus API)
- **Platform:** Feather M4 CAN Express (SAMD51, 120MHz, 192KB RAM)

### Software Architecture Decisions
- **Modular Design:** Separate core engine from output drivers
- **Pattern Library:** Pluggable pattern system (easy to add new patterns)
- **Settings Persistence:** JSON-based (settings.json on CIRCUITPY drive)
- **Button UI:** 3 buttons minimum (Pattern, Tempo, Settings)

### Development Workflow Decisions
- **Backup Before Push:** Always run `python3 scripts/backup.py` before `git push`
- **Test Hardware First:** Use comprehensive_pin_test.py to validate hardware
- **Dependency Checking:** Always verify libraries with `circup list` before deployment
- **Documentation First:** Update docs before/during implementation, not after

---

## Known Blockers

### Current Blockers
**None** - Ready to proceed with arpeggiator core implementation

### Resolved Blockers
- ✅ OLED not working → Fixed by using SH1107 driver and CP 10.x API
- ✅ Button debouncing → Fixed with proper timing
- ✅ Display flickering → Fixed by throttling updates

---

## Recently Modified Files

### This Session (Session 15 - Translation Hub Research)
- **docs/implementation/TRANSLATION_HUB_PREP_DOC.md** (NEW) - Deep codebase analysis (500 lines)
- **docs/implementation/TRANSLATION_HUB_QUESTIONS.md** (NEW) - 10 critical questions (341 lines)
- **docs/implementation/TRANSLATION_HUB_ANSWERS.md** (NEW) - Research findings (605 lines)
- **docs/implementation/TRANSLATION_HUB_IMPLEMENTATION_PLAN.md** (NEW) - 8-phase plan (437 lines)
- **README.md** (UPDATED) - Rebranded to "prisme", updated features/roadmap
- **PROJECT_STATUS.md** (UPDATED) - Added Session 15 milestone
- **docs/context/CONTEXT.md** (UPDATED) - Session 15 handoff

### Session 14 (2025-10-31)
- **arp/drivers/midi_custom_cc.py** (NEW) - CustomCCHandler with Learn Mode (169 lines)
- **arp/data/midi_cc_names.py** (NEW) - Database of 128 MIDI CC names
- **arp/utils/config.py** (UPDATED) - Custom CC settings + NVM storage
- **arp/drivers/cv_gate.py** (UPDATED) - Voltage conversion for all sources + smoothing
- **main.py** (UPDATED) - CV Output initialization + Custom CC integration
- **arp/ui/menu.py** (UPDATED) - 7th category added (Custom CC)
- **docs/hardware/MIDI_TO_CV_VOLTAGE_STANDARDS.md** (NEW) - Voltage reference (721 lines)
- **docs/implementation/CUSTOM_CC_*.md** (NEW) - 5 comprehensive planning documents

### Session 13 (2025-10-31)
- **docs/hardware/TRUE_STRIG_CIRCUIT.md** (NEW) - S-Trig transistor circuit
- **docs/hardware/PIN_ALLOCATION_MATRIX.md** (NEW) - Authoritative pin reference
- **docs/SESSION_13_HANDOFF.md** (NEW) - Session handoff documentation
- **tests/gate_dual_output_test.py** (NEW) - V-Trig + S-Trig validation

### Session 12 (2025-10-31)
- **arp/drivers/cv_output.py** (NEW) - CVOutput driver with lookup table
- **docs/hardware/LM358_WIRING_GUIDE.md** (NEW) - 0-10V amplification circuit
- **docs/hardware/MCP4728_CV_GUIDE.md** (NEW) - DAC usage guide
- **docs/architecture/TIMING_ARCHITECTURE.md** (NEW) - I2C throttling design
- **docs/SESSION_12_HANDOFF.md** (NEW) - Session handoff documentation

---

## Code Context

### Arpeggiator Core (To Be Implemented)

**Expected Flow:**
```
MIDI Input → Note Buffer → Arpeggiator Engine → Output Router → MIDI/CV Drivers
```

**Key Classes:**
```python
# arp/core/note_buffer.py
class NoteBuffer:
    def add_note(self, note, velocity)
    def remove_note(self, note)
    def get_sorted_notes(self) -> list

# arp/core/patterns.py
class Pattern(ABC):
    def get_next_note(self, notes, index) -> (note, new_index)

class UpPattern(Pattern):
    # Ascending notes

class DownPattern(Pattern):
    # Descending notes

# arp/core/arpeggiator.py
class Arpeggiator:
    def __init__(self, note_buffer, pattern, tempo)
    def tick(self) -> note_event
    def set_pattern(self, pattern)
    def set_tempo(self, bpm)
```

### Current main.py Structure
```python
# main.py (current state - needs arp integration)
- Initializes display, buttons, MIDI I/O
- Has MIDI pass-through working
- Needs: Integration with arpeggiator core
```

---

## Next Steps (Priority Order)

### Immediate (This/Next Session)
1. **[HIGH]** Implement `arp/core/note_buffer.py`
2. **[HIGH]** Implement `arp/core/patterns.py` (at least Up/Down)
3. **[HIGH]** Implement `arp/core/arpeggiator.py`
4. **[MEDIUM]** Create `arp/drivers/midi_output.py` wrapper
5. **[MEDIUM]** Integrate arpeggiator into `main.py`

### Short Term (Next 1-2 Weeks)
- [ ] Add clock sync (USB MIDI clock from DAW)
- [ ] Implement clock divisions (1/4, 1/8, 1/16 notes)
- [ ] Add octave range control (1-4 octaves)
- [ ] Build UI menu system for pattern/tempo selection
- [ ] Implement settings persistence (save pattern/tempo to settings.json)

### Long Term (Phase 2+)
- [ ] CV/Gate output driver (Phase 2)
- [ ] S-Trigger support (Phase 3)
- [ ] Enclosure design and fabrication

---

## Dependencies & Environment

### CircuitPython Expertise

**🎓 CRITICAL:** Before writing ANY CircuitPython code, read:
- **`~/.claude/references/CIRCUITPYTHON_MASTERY.md`** - Comprehensive crash prevention guide
- **Local copy:** `docs/context/CIRCUITPYTHON_MASTERY.md`

This 600+ line reference covers:
- Memory management & crash prevention
- Safe mode debugging
- MIDI programming patterns
- busio (I2C, UART, SPI) best practices
- SAMD51 specifics
- Common pitfalls with solutions

**Previous sessions struggled with basic CircuitPython issues causing crashes.** This reference makes you a CircuitPython ninja.

### Hardware
- Feather M4 CAN Express
- MIDI FeatherWing (UART on D0/D1)
- OLED FeatherWing 128x64 (I2C on D21/D22, SH1107 driver)
- 3 Buttons (D4-D6)

### Software
- CircuitPython 10.0.3
- Libraries (installed via circup):
  - `adafruit_midi`
  - `adafruit_displayio_sh1107`
  - `adafruit_display_text`
  - `adafruit_debouncer`
  - `neopixel`

### Development Tools
- `circup` - Library manager
- `scripts/monitor_serial.py` - Serial debugging
- `scripts/backup.py` - Pre-push backups

---

## Quick Reference Commands

```bash
# Check git status
git status
git log -5 --oneline

# Check hardware connection
ls /Volumes/CIRCUITPY/

# Check installed libraries
circup list

# Deploy test code
cp tests/[test_name].py /Volumes/CIRCUITPY/code.py

# Monitor serial output
python3 scripts/monitor_serial.py

# Create backup before push
python3 scripts/backup.py
```

---

## Communication Notes

### User Preferences
- Methodical, systematic approach
- Documentation-first workflow
- Test hardware before software integration
- Clear handoffs between sessions
- Ask for clarification on ambiguous specs

### What User Values
- Learning from mistakes (e.g., hardware spec verification)
- Comprehensive documentation
- Reusable test infrastructure
- Clean git history with good commit messages

---

## Emergency Recovery

### If This Session Was Interrupted
1. Read this file (CONTEXT.md) from top to bottom
2. Check `git status` and `git log -5 --oneline`
3. Check `todo` file for active tasks
4. Review backups in `/Users/keegandewitt/Cursor/_Backups/`
5. Check `_archive/` for older handoff documents

### Backup Locations
- **Automated:** `/Users/keegandewitt/Cursor/_Backups/Arp_*.tar.gz`
- **Retention:** Last 5 backups (auto-rotated)
- **Git Remote:** origin/main

---

**End of Context Document**

**Next Claude Instance:** Read START_HERE.md first, then this file's "Session Handoff" section.
