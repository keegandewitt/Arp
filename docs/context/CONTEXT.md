# Arp Project - Living Context

**Purpose:** This file maintains session-to-session continuity for Claude instances.
**Update Frequency:** After every significant milestone or before session end.

---

## Session Handoff

**Last Updated:** 2025-10-22 20:10
**Session Status:** ✅ COMPLETE - Session optimization and documentation
**Token Usage:** ~60K / 200K

### Current Session Summary (Session 4)
**What was accomplished:**
- Created START_HERE.md for quick onboarding
- Created docs/context/CONTEXT.md (this file) for session continuity
- Analyzed existing /start and /handoff commands in ~/.claude/commands/
- Identified that commands were referencing non-existent files
- Established optimized context file structure

**Git Status:**
- **Branch:** main
- **Last Commit:** aac0f45 - feat: Add comprehensive zero-latency MIDI pass-through
- **Working Tree:** Clean (after creating START_HERE.md and CONTEXT.md)

**What's Next:**
1. Update ~/.claude/commands/start.md to reflect Arp project (not Phil)
2. Begin implementing Phase 1 arpeggiator core (`arp/core/`)
3. Create note_buffer.py, patterns.py, arpeggiator.py modules

---

## Session History

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

### This Session (Session 4)
- **START_HERE.md** (NEW) - Quick onboarding guide
- **docs/context/CONTEXT.md** (NEW) - This file, living session context

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
