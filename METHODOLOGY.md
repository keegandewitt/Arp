# Project Methodology & Workflow Guide

**Last Updated:** 2025-10-21
**Project:** Arp - CircuitPython MIDI Arpeggiator
**Purpose:** This document guides all development, git workflows, and collaboration practices for this project.

---

## Table of Contents
1. [Git Workflow & Version Control](#git-workflow--version-control)
2. [Backup Strategy](#backup-strategy)
3. [Development Guidelines](#development-guidelines)
4. [Testing Procedures](#testing-procedures)
5. [Documentation Standards](#documentation-standards)
6. [Hardware Development](#hardware-development)

---

## Git Workflow & Version Control

### Pre-Commit Checklist
Before every commit and push to the remote repository, **ALWAYS**:

1. **Backup First** - Create archived backup to `/Users/keegandewitt/Cursor/_Backups/`
   - Maintain only the last 5 backups (automatically rotate older ones)
   - Backups should be timestamped tar.gz archives
   - Run backup script before ANY push operation

2. **Review Changes** - Check git status and diff
   - `git status` - Review all modified and untracked files
   - `git diff` - Review all changes line-by-line
   - Ensure no sensitive data, credentials, or temporary files are included

3. **Stage Files Appropriately**
   - Add modified files: `git add <file>`
   - Add new files deliberately (no blanket `git add .` without review)
   - Verify staging: `git status`

4. **Commit with Clear Messages**
   - Follow format: `<type>: <concise description>`
   - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `hardware`
   - Example: `feat: Add CV/Gate output support for modular synth integration`

5. **Push to Remote**
   - `git push origin main`
   - Verify push succeeded

### Backup Script Usage
```bash
# Run before every push
python backup.py
```

The backup script will:
- Create timestamped archive of entire project
- Store in `/Users/keegandewitt/Cursor/_Backups/Arp_YYYYMMDD_HHMMSS.tar.gz`
- Automatically remove backups older than the last 5
- Exclude `.git/` directory and Python cache files

---

## Backup Strategy

### Automated Backups
- **When:** Before every `git push` operation
- **Where:** `/Users/keegandewitt/Cursor/_Backups/`
- **Format:** `Arp_YYYYMMDD_HHMMSS.tar.gz`
- **Retention:** Last 5 backups only (older ones auto-deleted)
- **Tool:** `backup.py` script in project root

### Manual Backups
For major milestones or before significant refactoring:
```bash
# Create a named milestone backup
python backup.py --milestone "pre-cv-gate-integration"
```

### Backup Exclusions
The following are excluded from backups:
- `.git/` directory
- `__pycache__/` directories
- `*.pyc` files
- `.DS_Store` files
- Virtual environments (if any)

---

## Development Guidelines

### Code Style
- **Language:** CircuitPython 9.x
- **Style Guide:** PEP 8 (where applicable to CircuitPython)
- **Line Length:** 100 characters max
- **Indentation:** 4 spaces (no tabs)

### File Organization
```
/
├── code.py                 # Main entry point
├── arpeggiator.py         # Arpeggiator engine
├── button_handler.py      # UI button logic
├── display.py             # OLED display management
├── settings.py            # Settings persistence
├── settings_menu.py       # Settings UI
├── cv_output.py           # CV/Gate output (if applicable)
├── hardware_tests.py      # Hardware validation tests
├── install.py             # Installation/setup script
├── _hardware_files/       # KiCad, Gerbers, BOM, schematics
├── *.md                   # Documentation
└── todo                   # Task tracking
```

### Module Design Principles
- **Single Responsibility:** Each module handles one aspect (arp logic, display, buttons, etc.)
- **Minimal Dependencies:** Keep imports minimal for CircuitPython memory constraints
- **Error Handling:** Always handle hardware exceptions gracefully
- **State Management:** Centralize state in `settings.py`

### Hardware Constraints
- **RAM:** CircuitPython has limited memory - be mindful of allocations
- **Performance:** OLED updates should be throttled to avoid lag
- **Pin Limitations:** Document all pin assignments clearly

---

## Testing Procedures

### Pre-Deployment Testing
Before deploying to hardware:

1. **Hardware Tests:** `python hardware_tests.py` or load on device
2. **Functionality Tests:**
   - MIDI input/output
   - Button responsiveness
   - Display updates
   - Settings persistence
   - Arpeggiator patterns
3. **Integration Tests:**
   - Full workflow from boot to arpeggiating
   - Settings changes and persistence across reboots

### Hardware Testing
See `TESTING_GUIDE.md` for comprehensive hardware validation procedures.

---

## Documentation Standards

### Required Documentation
Every significant feature or hardware change requires documentation:

- **Code Comments:** Complex logic should have inline comments
- **Module Docstrings:** Every `.py` file should have a module-level docstring
- **Function Docstrings:** Public functions should document parameters and return values
- **README Updates:** Keep `INSTALLER_README.md` current
- **Hardware Docs:** Update `HARDWARE_BUILD_GUIDE.md` for any hardware changes

### Documentation Files
- `README.md` - Project overview (create if needed)
- `INSTALLER_README.md` - Installation instructions
- `HARDWARE_BUILD_GUIDE.md` - Hardware assembly
- `TESTING_GUIDE.md` - Testing procedures
- `CV_GATE_INTEGRATION.md` - CV/Gate feature documentation
- `ENCLOSURE_ROADMAP.md` - Enclosure design plans
- `BOM.md` - Bill of materials
- `METHODOLOGY.md` - This document

---

## Hardware Development

### Design Process
1. **Schematic Design:** Use KiCad, store in `_hardware_files/`
2. **PCB Layout:** Export Gerbers to `_hardware_files/gerbers/`
3. **BOM Management:** Update `BOM.md` with all components
4. **Version Tracking:** Tag hardware versions in git (e.g., `hw-v1.0`)

### Enclosure Design
See `ENCLOSURE_ROADMAP.md` for current enclosure development status and plans.

### Component Selection
- Prioritize availability (avoid rare/discontinued parts)
- Document suppliers and part numbers in `BOM.md`
- Consider hobbyist-friendly options (through-hole where possible)

---

## Onboarding New Claude Instances

When starting a new Claude Code session:

1. **Read this document first** - Understand our methodologies
2. **Check `git status`** - Understand current state
3. **Review `todo`** - See active tasks
4. **Read recent commits** - `git log -5 --oneline`
5. **Ask clarifying questions** - Don't assume, ask the user

### Key Commands to Run
```bash
git status              # Current state
git log -5 --oneline    # Recent history
cat todo               # Active tasks
ls -la                 # Project structure
```

---

## Current Project Status

### Active Features
- MIDI arpeggiator with multiple patterns
- OLED display UI
- Button-based settings control
- Settings persistence
- Installation script
- Hardware testing suite

### In Development
- CV/Gate output integration (see `CV_GATE_INTEGRATION.md`)
- Enclosure design (see `ENCLOSURE_ROADMAP.md`)

### Hardware Platform
- **MCU:** RP2040-based board (e.g., Raspberry Pi Pico, KB2040)
- **Display:** SSD1306 OLED (I2C)
- **MIDI:** TRS or DIN MIDI I/O
- **Storage:** CircuitPython filesystem for settings

---

## Emergency Procedures

### If Something Goes Wrong
1. **Don't Panic** - Backups exist in `/Users/keegandewitt/Cursor/_Backups/`
2. **Check Git History** - `git log` to see what changed
3. **Restore from Backup** - Extract latest backup if needed
4. **Git Reset if Needed** - `git reset --hard origin/main` (CAUTION)

### Recovery Commands
```bash
# List available backups
ls -lt /Users/keegandewitt/Cursor/_Backups/

# Extract a backup
cd /Users/keegandewitt/Cursor/_Backups/
tar -xzf Arp_YYYYMMDD_HHMMSS.tar.gz

# Reset to remote state (DESTRUCTIVE)
git fetch origin
git reset --hard origin/main
```

---

## Version History

- **v1.0** (2025-10-21) - Initial methodology document created
  - Established git workflow
  - Defined backup strategy
  - Documented project structure
  - Created onboarding guide

---

## Notes

- This document should be updated as the project evolves
- All team members (and Claude instances) should follow these guidelines
- When in doubt, refer to this document or ask for clarification
- Consistency is key to maintainable code and smooth collaboration
