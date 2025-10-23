# Arp - Start Here

**Last Updated:** 2025-10-22
**Quick Read:** 30 seconds to orientation

---

## Project Identity

- **Name:** Arp (Hardware MIDI Arpeggiator)
- **Platform:** Adafruit Feather M4 CAN Express
- **Language:** CircuitPython 10.0.3
- **Current Phase:** Phase 1 - MIDI Core Development

---

## Current Status Snapshot

| Component | Status | Notes |
|-----------|--------|-------|
| **Hardware** | ✅ Validated | M4 + MIDI FeatherWing + OLED FeatherWing |
| **OLED Display** | ✅ Working | SH1107 128x64, fully integrated |
| **MIDI I/O** | ✅ Working | USB MIDI + UART loopback tested |
| **Buttons** | ✅ Working | Debounced, long-press support |
| **Arpeggiator Core** | ⏳ TODO | Main engine needs implementation |

---

## Start Sequence (Run in Order)

### 1. Read Session Context FIRST
```bash
cat docs/context/CONTEXT.md
```
**Look for:** "Session Handoff" section - what did the last session accomplish?

### 2. Check Git Status
```bash
git status
git log -5 --oneline
```
**Look for:** Uncommitted changes, recent commits

### 3. Read Project Roadmap
```bash
cat PROJECT_STATUS.md
```
**Look for:** Current features, known issues, next steps

### 4. Read Development Methodology
```bash
cat METHODOLOGY.md
```
**Look for:** Git workflow, testing procedures, hardware protocols

### 5. Check Active Tasks
```bash
cat todo
```

### 6. Ask User
**Prompt:** "I've reviewed the project context. What should we work on today?"

---

## Key Project Files (Reference)

### Core Documentation
- **PROJECT_STATUS.md** - Living roadmap, feature status, milestones
- **METHODOLOGY.md** - Git workflow, testing, dependency management
- **docs/ARCHITECTURE.md** - System design, pin allocation, data flow
- **docs/context/CONTEXT.md** - Session-to-session context (read this FIRST!)

### Hardware Documentation
- **docs/hardware/HARDWARE_PINOUT.md** - Pin assignments
- **docs/hardware/BOM.md** - Bill of materials
- **docs/hardware/HARDWARE_TEST_RESULTS.md** - Validation test results

### Code Structure
```
arp/
├── core/               # ⏳ TODO - Arpeggiator engine
├── drivers/            # ⏳ TODO - Output drivers (MIDI/CV)
├── ui/                 # ✅ Working - Display & buttons
└── utils/              # ⏳ TODO - Helpers

main.py                 # Entry point (needs arp core integration)
```

---

## Critical Context Items

### Hardware: OLED FeatherWing
- **Product:** Adafruit #4650 (128x64)
- **Driver:** SH1107 (NOT SSD1306!)
- **Library:** `adafruit_displayio_sh1107`
- **I2C Address:** 0x3C

### CircuitPython 10.x Breaking Changes
- **Old API (deprecated):** `displayio.I2CDisplay`
- **New API (required):** `i2cdisplaybus.I2CDisplayBus`
- **Impact:** All display code updated to CP 10.x

### Next Steps from Previous Session
See `docs/context/CONTEXT.md` for detailed next steps.

**Immediate priorities:**
1. Create `arp/core/arpeggiator.py` - Main engine
2. Create `arp/core/note_buffer.py` - Note storage
3. Create `arp/core/patterns.py` - Pattern library
4. Create `arp/drivers/midi_output.py` - MIDI driver
5. Integrate with `main.py`

---

## Emergency Recovery

### If Previous Session Crashed/Compacted
1. Check `docs/context/CONTEXT.md` for session handoff
2. Check `_archive/HANDOFF_*.md` for older handoffs
3. Review recent backups: `/Users/keegandewitt/Cursor/_Backups/`
4. Check git history: `git log -10 --oneline`

### Backup Locations
- **Automated:** `/Users/keegandewitt/Cursor/_Backups/Arp_YYYYMMDD_HHMMSS.tar.gz`
- **Git Remote:** `origin/main` (check `git remote -v`)

---

## Quick Commands Reference

```bash
# Check hardware connection
ls /Volumes/CIRCUITPY/

# List installed libraries
circup list

# Check CircuitPython version
cat /Volumes/CIRCUITPY/boot_out.txt | grep CircuitPython

# Monitor serial output
python3 scripts/monitor_serial.py

# Deploy test code
cp tests/[test_name].py /Volumes/CIRCUITPY/code.py
```

---

**You're ready! Check CONTEXT.md for session handoff, then ask the user what to work on.**
