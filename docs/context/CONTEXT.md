# Arp Project - Living Context

**Purpose:** This file maintains session-to-session continuity for Claude instances.
**Update Frequency:** After every significant milestone or before session end.

---

## Session Handoff

**Last Updated:** 2025-10-24
**Session Status:** 📋 PLANNING - Production Roadmap Complete
**Token Usage:** ~55K / 200K

### Current Session Summary (Session 9)
**What was accomplished:**
- ✅ **PRODUCTION ROADMAP COMPLETE**
  - Created comprehensive PRODUCTION_ROADMAP.md (800+ lines)
  - Analyzed cost optimization for 200-unit manufacturing run
  - Documented single custom PCB strategy with RP2040
  - Cost breakdown: $42-51/unit (vs $89-105 with Feathers)
  - Total savings: $7,800-12,600 for 200 units
- ✅ **Technical Analysis**
  - RP2040 vs SAMD51 comparison (6-8× cheaper, dual-core, better specs)
  - MIDI circuit integration ($6 vs $15 FeatherWing)
  - Display optimization ($5 vs $20 FeatherWing)
  - Power management options (USB-only vs battery)
- ✅ **Timeline & Risk Assessment**
  - 18-24 week production timeline documented
  - Technical, financial, and operational risks identified
  - Decision point checklists created
  - Phase breakdown: Prototype → Beta → Production

**Key Decisions Made:**
1. **Custom PCB Required:** Single board integration saves $38-54 per unit
2. **RP2040 Microcontroller:** $1 vs $6-8 (SAMD51), dual-core 133MHz, excellent CircuitPython support
3. **Integrated MIDI Circuit:** Replicate FeatherWing schematic on custom PCB
4. **Off-the-Shelf OLED:** Use $3-5 module instead of $20 FeatherWing
5. **PCBA Service:** Use JLCPCB/PCBWay for SMD assembly, hand-solder through-hole
6. **Two Product Tiers:** USB-only standard ($42-47) and battery pro model ($46-51)

**Git Status:**
- **Branch:** main
- **Last Commit:** c10b22d - docs: Add comprehensive production planning roadmap for 200-unit manufacturing
- **Working Tree:** Clean

**What's Next (Priority Order):**
1. **[HARDWARE]** Complete MCP4728 DAC testing (in progress from Session 8)
   - Wire MCP4728 to 3.3V power (M4's 3V pin)
   - Connect I2C via STEMMA QT to OLED FeatherWing
   - Run I2C scanner to verify devices (0x3C, 0x60)
   - Test DAC outputs at 3.3V
2. **[HARDWARE]** Validate CV/Gate output with multimeter/scope
3. **[HARDWARE]** Test BSS138 level shifter for 5V operation
4. **[DOCUMENTATION]** Update PRODUCTION_ROADMAP.md after testing complete
5. **[DESIGN]** Begin PCB schematic design in KiCad (when ready)
6. **[SOFTWARE]** Integrate CV/Gate output into main arpeggiator code

---

## Session History

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
