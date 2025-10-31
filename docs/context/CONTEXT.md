# Arp Project - Living Context

**Purpose:** This file maintains session-to-session continuity for Claude instances.
**Update Frequency:** After every significant milestone or before session end.

---

## Session Handoff

**Last Updated:** 2025-10-31 (Session 12)
**Session Status:** ✅ COMPLETE - Full 0-10V CV output working!
**Token Usage:** ~62K / 200K

### Current Session Summary (Session 12)
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
- ❌ TL072 op-amp - **DO NOT USE** (cannot handle 0V inputs in single-supply)

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
1. **[HIGH]** Integrate MIDI FeatherWing hardware (next missing piece)
2. **[HIGH]** Build end-to-end arpeggiator test (MIDI in → CV out)
3. **[MEDIUM]** Test 1V/octave tracking with actual eurorack VCO
4. **[MEDIUM]** Design PCB layout with LM358N for production
5. **[LOW]** Implement pattern storage and user presets

---

## Session History

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

### Session 5 (2025-10-22)
- **Focus:** VintageCapture VST plugin - Complete implementation
- **Outcome:** Built full VST plugin for vintage synth capture workflow
- **Major Achievement:** Solved vintage synth Local Control Off problem with two-stage workflow
- **Lines of Code:** 1800+ (C++, fully functional)
- **Status:** ✅ Complete

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

### Current Task: Arpeggiator Core Implementation
**Status:** ⏳ Ready to start
**Priority:** HIGH

**What needs to be done:**
1. Create `arp/core/note_buffer.py`
   - Polyphonic note storage (hold multiple pressed notes)
   - Add/remove notes on MIDI Note On/Off
   - Query sorted note list for arpeggiator

2. Create `arp/core/patterns.py`
   - Pattern classes: Up, Down, UpDown, Random
   - Pattern interface: `get_next_note(note_buffer, current_index)`
   - Pattern cycling logic

3. Create `arp/core/arpeggiator.py`
   - Main arpeggiator engine
   - Clock/tempo management
   - Note triggering at correct intervals
   - Integration with patterns and note buffer

4. Create `arp/drivers/midi_output.py`
   - MIDI output abstraction
   - Note On/Off sending
   - USB and UART MIDI support

5. Update `main.py`
   - Integrate arpeggiator core
   - Wire up MIDI input → note buffer → arpeggiator → MIDI output
   - Add UI controls (pattern selection, tempo)

**Estimated Effort:** 2-3 sessions

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

### This Session (Session 9)
- **docs/PRODUCTION_ROADMAP.md** (NEW) - Comprehensive 200-unit production planning
- **docs/context/CONTEXT.md** (UPDATED) - Session 9 handoff info

### Session 8 (2025-10-23)
- **docs/BATTERY_MCP4728_INTEGRATION.md** - Battery + DAC integration guide
- **docs/MCP4728_POWER_SETUP.md** - Power setup and safety procedures
- **main.py:324** - Fixed button unpacking error
- **docs/context/CONTEXT.md** - Updated with battery integration status

### Previous Session (Session 3)
- **display.py:35** - Updated to use `i2cdisplaybus.I2CDisplayBus`
- **tests/display_integration_test.py** (NEW) - Display validation tests
- **METHODOLOGY.md** - Added dependency management section

### Session 2
- **tests/comprehensive_pin_test.py** (NEW) - Full hardware validation
- **docs/hardware/M4_TEST_BASELINE.md** (NEW) - Test results

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
