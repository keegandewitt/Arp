# Project Status & Roadmap

**Last Updated:** 2025-11-01 (Session 15 - Translation Hub Research Complete)
**Project:** prisme - MIDI/CV Translation Hub
**Current Version:** Hardware v1.0, Software v3.0 (Translation Hub architecture planned)

> **Purpose:** This is a living document that tracks project state, key decisions, and roadmap. Update this regularly to ensure continuity across Claude instances and recovery from crashes/compacts.

---

## Quick Reference

| Item | Status | Notes |
|------|--------|-------|
| **Hardware Platform** | Adafruit Feather M4 CAN Express | CircuitPython 10.0.3 |
| **Core Functionality** | ✅ Working | MIDI arp, display, buttons, settings |
| **OLED Display** | ✅ Working | CP 10.x API, fully integrated |
| **CV/Gate Output** | 🚧 In Progress | DAC on A0/A1, see docs/features/CV_GATE_INTEGRATION.md |
| **VintageCapture VST** | 🚧 In Progress | VST plugin for vintage synth workflow, see VintageCapture/ |
| **Vintage Mode Firmware** | 📋 Planned | USB MIDI control for VintageCapture integration |
| **Hardware Testing** | ✅ Complete | Comprehensive pin test suite created |
| **Enclosure** | 📋 Planned | See docs/features/ENCLOSURE_ROADMAP.md |
| **Battery Integration** | 📋 Planned | LiPo charging, monitoring needed |

**Legend:** ✅ Complete | 🚧 In Progress | 📋 Planned | ⚠️ Blocked | ❌ Cancelled

---

## Current Hardware Configuration

### Microcontroller: Adafruit Feather M4 CAN Express
- **Processor:** ATSAMD51J19 (ARM Cortex M4, 120MHz)
- **RAM:** 192KB
- **Flash:** 512KB
- **CircuitPython Version:** 10.0.3 (October 2025 release)
- **USB:** Native USB for MIDI and serial

### Physical Configuration
- **Stacked:** OLED FeatherWing on top of Feather M4 CAN
- **Breadboard:** MIDI I/O (DIN-5 jacks) connected via jumper wires to D0/D1
- ⚠️ **IMPORTANT:** MIDI FeatherWing is NOT stacked - stays on breadboard for prototyping

### Pin Assignments (Active)
| Pin | Function | Notes |
|-----|----------|-------|
| D21 (SDA) | OLED Display | I2C SH1107 128x64 (Product #4650) - STACKED |
| D22 (SCL) | OLED Display | I2C bus - STACKED |
| D0 (RX) | MIDI In | UART RX - BREADBOARD via jumper wires |
| D1 (TX) | MIDI Out | UART TX - BREADBOARD via jumper wires |
| D4-D6 | Button Inputs | Pattern, Tempo, Settings (pull-up) |
| A0 | CV Output 1 | DAC, 0-3.3V (planned scaling to 0-5V or 0-10V) |
| A1 | Gate Output | DAC or GPIO, triggers on note |
| D13 | Status LED | Onboard red LED |
| NEOPIXEL | RGB Status | Onboard NeoPixel |

### Pin Assignments (Reserved/Future)
| Pin | Reserved For | Notes |
|-----|--------------|-------|
| A2-A5 | Analog Controls | Potentiometers for tempo, swing, gate length |
| D9-D12 | Additional I/O | Encoders, extra buttons, triggers |
| D23-D25 | SPI Bus | Future expansion (SD card, etc.) |

### Power
- **USB:** 5V via USB-C
- **Battery:** LiPo (not yet integrated, see todo)
- **Charging:** Onboard LiPo charger (500mA)
- **Voltage Regulators:** 3.3V onboard

---

## Architecture Overview

### File Structure
```
/
├── code.py                     # Main entry point, boots system
├── arpeggiator.py              # Arpeggiator engine (patterns, timing)
├── button_handler.py           # Button debouncing and UI logic
├── clock_handler.py            # Clock/tempo management
├── cv_output.py                # CV/Gate output (in progress)
├── display.py                  # OLED display management
├── midi_io.py                  # MIDI input/output handling
├── settings.py                 # Settings persistence (JSON on flash)
├── settings_menu.py            # Settings menu UI
│
├── VintageCapture/             # VST plugin for vintage synth workflow
│   ├── Source/                 # C++ source (JUCE framework)
│   ├── Resources/              # UI assets
│   ├── Builds/                 # Build output (VST3, AU, AAX)
│   ├── README.md               # VST overview
│   ├── WORKFLOW.md             # User workflow guide
│   └── ARP_FIRMWARE_SPEC.md    # Arp firmware integration spec
│
├── scripts/                    # Utilities and installation
│   ├── backup.py               # Backup script
│   ├── install.py              # Installation/setup script
│   ├── install_libs.py         # Library installer
│   └── watch.sh                # File watcher utility
│
├── tests/                      # Hardware validation tests
│   ├── comprehensive_pin_test.py  # Complete pin validation suite
│   ├── hardware_tests.py       # Hardware validation (legacy)
│   └── connection_test.py      # Connection/MIDI tests
│
├── docs/                       # Documentation
│   ├── hardware/               # Hardware docs
│   │   ├── BOM.md
│   │   ├── HARDWARE_BUILD_GUIDE.md
│   │   ├── HARDWARE_PINOUT.md
│   │   ├── HARDWARE_TESTING_README.md
│   │   └── HARDWARE_TEST_RESULTS.md
│   ├── installation/           # Installation guides
│   │   ├── INSTALL.md
│   │   └── INSTALLER_README.md
│   └── features/               # Feature documentation
│       ├── CV_GATE_INTEGRATION.md
│       ├── ENCLOSURE_ROADMAP.md
│       └── TESTING_GUIDE.md
│
├── _hardware_files/            # KiCad, Gerbers, Fusion360
├── _archive/                   # Archived docs and old code
├── README.md                   # Main project README
├── PROJECT_STATUS.md           # This file (living roadmap)
├── METHODOLOGY.md              # Development methodology
├── requirements.txt            # Python dependencies
└── todo                        # Task tracking (plain text)
```

### Key Design Decisions

1. **CircuitPython over C/Arduino**
   - Rationale: Faster iteration, easier USB MIDI, filesystem for settings
   - Trade-off: Slightly higher memory usage, but manageable on M4

2. **Settings Persistence via JSON**
   - File: `settings.json` on CIRCUITPY drive
   - Approach: Load on boot, save on change
   - Rationale: Human-readable, debuggable, no EEPROM needed

3. **OLED Display over LCD**
   - I2C SH1107 128x64 (OLED FeatherWing Product #4650)
   - **CRITICAL:** Uses SH1107 driver, NOT SSD1306! (128x32 FeatherWing uses SSD1306, 128x64 uses SH1107)
   - Rationale: Low power, high contrast, easy library support
   - **CP 10.x Migration:** Updated to use `i2cdisplaybus.I2CDisplayBus` (new API)
   - Old CP 9.x `displayio.I2CDisplay` deprecated and incompatible

4. **DAC for CV Output**
   - Using SAMD51's built-in DACs on A0/A1
   - Output: 0-3.3V native, external op-amp for 0-5V or 0-10V
   - Rationale: True analog, no PWM filtering needed

5. **Button Interface (No Encoder Yet)**
   - Current: 3 buttons (Pattern, Tempo, Settings)
   - Future: Rotary encoder for faster navigation
   - Rationale: Simple, reliable, low pin count

---

## Feature Status

### ✅ Complete Features
- [x] **MIDI Input/Output** - USB and UART MIDI working
- [x] **Arpeggiator Engine** - Up, Down, Up/Down, Random patterns
- [x] **Tempo Control** - BPM adjustable via buttons
- [x] **Note Division** - Quarter, 8th, 16th notes
- [x] **Settings Menu** - Navigate and save settings
- [x] **Settings Persistence** - JSON-based, survives reboots
- [x] **OLED Display** - Real-time status and menus (CP 10.x API, fully tested)
- [x] **Button Handling** - Debounced, responsive UI
- [x] **Installation Script** - `install.py` for easy deployment
- [x] **Hardware Test Suite** - Comprehensive pin validation

### 🚧 In Progress
- [ ] **CV/Gate Output** (70% complete)
  - DAC code written, needs testing
  - V/Oct scaling implementation needed
  - Gate timing needs refinement
  - See: `docs/features/CV_GATE_INTEGRATION.md`

- [ ] **Startup Error Check Protocol** (todo item #1)
  - Validate hardware on boot
  - Display errors on OLED if detected
  - Safe mode or limited functionality on failure

- [ ] **Connection Debug Verification** (todo item #4)
  - Need to test serial prompt mechanism
  - Verify debug output is accessible

### 📋 Planned Features

#### Vintage Synth Integration
- [ ] **Vintage Mode Firmware**
  - USB MIDI control protocol (CC commands for pattern, division, etc.)
  - SysEx buffer transfer for note sequences
  - Timeline-locked playback engine
  - Integration with VintageCapture VST
  - See `VintageCapture/ARP_FIRMWARE_SPEC.md` for complete specification

#### Hardware & Enclosure
- [ ] **Battery Integration** (todo item #2)
  - LiPo monitoring (voltage readout)
  - Battery level indicator on display
  - Low battery warning
  - Charging status LED/display

- [ ] **Hardware Migration** (todo item #3)
  - Migrate to new Feather M4 board
  - Re-run comprehensive pin tests
  - Validate all functionality on new hardware

- [ ] **Enclosure Design**
  - See `docs/features/ENCLOSURE_ROADMAP.md` for details
  - Laser-cut or 3D-printed case
  - Panel-mount jacks and controls

#### Performance Features
- [ ] **Swing/Humanize**
  - Timing variations for groove
  - Adjustable swing percentage

- [ ] **Latch Mode**
  - Hold notes without holding keys
  - Toggle on/off via button

- [ ] **Octave Transpose**
  - Shift arp up/down by octaves
  - +/- 2 octave range

- [ ] **Clock Sync**
  - MIDI clock input/output
  - External sync for modular integration

---

## Recent Milestones

### 2025-11-01 (Latest - Session 15)
- **Translation Hub Architecture Research Complete** ✅
  - **Rebranding:** Project renamed to "prisme" - reflects Translation Hub concept
  - **Research Methodology:** Used FireCrawl MCP to gather authoritative documentation
  - **Confidence Achieved:** 97% confidence (exceeded 95% target)
  - **Key Findings:**
    - Class-based arpeggiator recommended (official Adafruit design patterns)
    - USB MIDI can handle both clock AND notes on same port
    - Swing implementation from Roger Linn himself (inventor of swing!)
    - PyTest + mocking for CircuitPython testing
    - Clock multiply/divide by modifying tick interval
  - **Deliverables:**
    - `TRANSLATION_HUB_QUESTIONS.md` - 10 critical questions identified
    - `TRANSLATION_HUB_ANSWERS.md` - Complete answers with evidence
    - `TRANSLATION_HUB_IMPLEMENTATION_PLAN.md` - Phased 8-phase plan (12-19 hours estimated)
  - **Next Steps:** Begin Phase 1 implementation (Session 16+)

### 2025-10-23
- **VintageCapture VST Project Initiated** 🚧
  - **Problem Solved:** Vintage synths without "Local Control Off" are incompatible with external arpeggiators (doubled notes)
  - **Solution:** Two-stage VST plugin workflow that separates performance from sound design
  - **Architecture:**
    - Stage 1: Calibration ("Press C3") - learns synth timing characteristics
    - Stage 2: Keystroke Capture - records MIDI performance with zero-latency monitoring
    - Stage 3: Playback - Arp hardware plays back captured notes while user tweaks synth parameters
  - **Innovation:** Uses Arp as USB-controlled MIDI playback engine
  - **Status:** VST Phase 1 in progress (core analysis), Arp firmware spec complete
  - **Files:** `VintageCapture/` directory with README, WORKFLOW, and ARP_FIRMWARE_SPEC
  - **Next Steps:** Implement Vintage Mode firmware on Arp hardware

### 2025-10-22
- **OLED FeatherWing Integration Complete** ✅
  - **Problem:** OLED not working with CircuitPython 10.0.3 due to API changes
  - **Root Cause:** CP 10.x deprecated `displayio.I2CDisplay`, requires new `i2cdisplaybus` module
  - **Solution:** Updated `display.py` to use `i2cdisplaybus.I2CDisplayBus` (display.py:35)
  - **Testing:** Created `tests/display_integration_test.py` - all tests passed
  - **Status:** Display class fully functional with CP 10.x
  - **Files Modified:** display.py (added i2cdisplaybus import and updated initialization)

- **Dependency Management & Compatibility Validation**
  - Added comprehensive dependency section to METHODOLOGY.md (v1.3)
  - Documented CircuitPython library compatibility validation workflow
  - Created safe library testing procedures
  - Documented CP 10.x breaking changes and known incompatibilities
  - Added recovery procedures for incompatible libraries

- **Hardware Testing Infrastructure**
  - Created `tests/comprehensive_pin_test.py` with systematic validation
  - Added `docs/hardware/M4_TEST_BASELINE.md` with complete test results
  - Added `docs/hardware/HARDWARE_TESTING_README.md` documentation
  - Follows "test EVERYTHING" philosophy from methodology
  - All GPIO, I2C, SPI, UART, ADC, DAC, PWM validated and working

- **Methodology Enhancement**
  - Added rigorous hardware validation section (v1.2)
  - Documented pin-by-pin testing approach

### 2025-10-21
- **Claude Instance Handoff Protocol**
  - Added handoff procedure to METHODOLOGY.md (v1.1)
  - Token budget management at 90% threshold
  - Ensures continuity across sessions

- **CV/Gate Integration**
  - Documented CV/Gate approach in docs/features/CV_GATE_INTEGRATION.md
  - Planned DAC usage for true analog output

### 2025-10-20
- **Settings Menu System**
  - Implemented multi-page settings UI
  - Persistent storage via JSON
  - Clean separation of concerns

### 2025-10-19
- **Initial Release**
  - Core arpeggiator functionality complete
  - MIDI I/O working
  - Display and button UI functional
  - Installation package created

---

## Known Issues & Blockers

### Active Issues
1. **Connection Debug Needs Verification** (todo #4)
   - Issue: Not sure how to prompt from serial in CircuitPython
   - Impact: Debug logging may not be interactive as expected
   - Next Step: Test with actual hardware, may need polling approach

2. **CV/Gate Untested on Hardware**
   - Issue: DAC code written but not validated
   - Impact: Feature incomplete
   - Next Step: Deploy to hardware, measure output with multimeter/scope

### Resolved Issues
- ✅ **OLED FeatherWing not working with CP 10.x** (2025-10-22)
  - Fixed by migrating to `i2cdisplaybus.I2CDisplayBus` API
  - Replaced deprecated `displayio.I2CDisplay`
  - Created comprehensive test suite (7 test files, display_integration_test.py validates)
- ✅ Button debouncing (fixed with proper timing)
- ✅ Display flickering (throttled updates)
- ✅ Settings not persisting (JSON file permissions)

---

## Dependencies & Tools

### Hardware
- Adafruit Feather M4 CAN Express (or compatible SAMD51 board)
- Adafruit OLED FeatherWing 128x64 (Product #4650, uses SH1107 driver)
- MIDI TRS jacks or DIN connectors
- Push buttons (3 minimum)
- LiPo battery (optional, not yet integrated)

### Software
- CircuitPython 10.0.3
- Libraries:
  - `adafruit_midi` (MIDI handling)
  - `adafruit_displayio_sh1107` (OLED display - SH1107 driver for 128x64 FeatherWing)
  - `adafruit_debouncer` (button handling)
  - `adafruit_display_text` (text rendering)
  - Built-in: `board`, `digitalio`, `busio`, `analogio`, `json`, `time`, `i2cdisplaybus`

### Development Tools
- CircuitPython serial console (screen, minicom, Mu editor)
- Git for version control
- Python 3.x for backup script and utilities
- Multimeter and/or oscilloscope (for CV/Gate validation)

---

## Testing Strategy

### Unit Testing
- Each module tested independently via `import` in REPL
- Hardware validation via `tests/comprehensive_pin_test.py`

### Integration Testing
- Full boot sequence to arpeggiating
- Settings persistence across reboots
- MIDI loopback tests

### Hardware Validation
- Power rail verification (3.3V, BAT, USB)
- Pin-by-pin GPIO testing
- I2C, SPI, UART bus initialization
- Analog input/output (ADC/DAC)
- PWM capability
- Visual confirmation (LEDs, display)

See: `docs/hardware/HARDWARE_TESTING_README.md` and `METHODOLOGY.md` Section 7

---

## Git Workflow Reminders

### Before Every Push
1. **Backup:** `python3 scripts/backup.py` (stores to `/Users/keegandewitt/Cursor/_Backups/`)
2. **Review:** `git status` and `git diff`
3. **Stage:** `git add <files>`
4. **Commit:** `git commit -m "<type>: <description>"`
5. **Push:** `git push origin main`

### Commit Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code restructuring
- `test:` Testing changes
- `chore:` Maintenance
- `hardware:` Hardware-related changes

See: `METHODOLOGY.md` for complete workflow

---

## Emergency Recovery

### If Claude Instance Crashes/Compacts
1. Run `/start` command (or manually read this file)
2. Check for `HANDOFF.md` in root (created at 90% token usage)
3. Review `git status` and recent commits
4. Check `todo` file for active tasks
5. Review recent backups in `/Users/keegandewitt/Cursor/_Backups/`

### Backup Locations
- **Automated:** `/Users/keegandewitt/Cursor/_Backups/Arp_YYYYMMDD_HHMMSS.tar.gz`
- **Retention:** Last 5 backups (auto-rotated)
- **Git Remote:** GitHub/GitLab (check git remote -v)

---

## Communication Conventions

### When Asking User for Decisions
Use clear, specific questions with options:
- Hardware approach (e.g., "DAC vs PWM for CV output?")
- Feature priority (e.g., "Battery integration or clock sync first?")
- Design trade-offs (e.g., "Encoder vs buttons?")

### When Reporting Progress
- ✅ Mark completed items clearly
- 🚧 Show in-progress work with percentage
- ⚠️ Flag blockers immediately
- Provide file:line references for code locations

---

## Next Session Checklist

When starting a new Claude instance:
- [ ] Run `/start` (or read this file + METHODOLOGY.md)
- [ ] Check for HANDOFF.md
- [ ] Review git status
- [ ] Read todo file
- [ ] Ask user what to prioritize

---

## Version History

### v1.0 (2025-10-22)
- Initial PROJECT_STATUS.md created
- Comprehensive roadmap with hardware config, architecture, features, milestones
- Emergency recovery procedures documented
- Crash/compact recovery strategy established

---

## Notes

- Update this file whenever:
  - Hardware configuration changes
  - Major features complete or added
  - Architectural decisions are made
  - Blockers arise or are resolved
  - Migration or major refactoring occurs

- Keep this document under 500 lines for quick readability
- Archive old status info to `_archive/` if it grows too large
- This is a LIVING DOCUMENT - keep it current!
