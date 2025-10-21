# Project Methodology & Workflow Guide

**Last Updated:** 2025-10-21 (v1.1 - Added handoff protocol)
**Project:** Arp - CircuitPython MIDI Arpeggiator
**Purpose:** This document guides all development, git workflows, and collaboration practices for this project.

---

## Table of Contents
1. [Git Workflow & Version Control](#git-workflow--version-control)
2. [Backup Strategy](#backup-strategy)
3. [Claude Instance Handoff Protocol](#claude-instance-handoff-protocol)
4. [Development Guidelines](#development-guidelines)
5. [Testing Procedures](#testing-procedures)
6. [Documentation Standards](#documentation-standards)
7. [Hardware Development](#hardware-development)

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

## Claude Instance Handoff Protocol

### Token Budget Management
Claude Code sessions have a token budget that auto-compacts when exceeded. To ensure smooth continuity:

**When token usage reaches 90% (180,000 of 200,000 tokens):**

1. **Stop at a Clean Checkpoint**
   - Complete current task if nearly done
   - Otherwise, pause at a logical stopping point
   - Commit and push any uncommitted work (following the git workflow above)
   - Run backup: `python3 backup.py`

2. **Create Handoff Document**
   Create `HANDOFF.md` in the project root with the following sections:

   ```markdown
   # Claude Instance Handoff

   **Date:** YYYY-MM-DD HH:MM
   **Token Usage at Handoff:** XXX,XXX / 200,000
   **Last Commit:** [commit hash] - [commit message]

   ## Session Summary
   Brief overview of what was accomplished in this session (3-5 bullet points)

   ## Current Context
   What we were working on and why:
   - Primary task/goal
   - Approach being taken
   - Key decisions made

   ## Progress Made
   Detailed list of what was completed:
   - Feature X implemented (files: a.py, b.py)
   - Bug Y fixed in module Z
   - Documentation updated (files: DOC1.md, DOC2.md)

   ## In-Progress Work
   What's partially done (if applicable):
   - Task description
   - What's complete vs. what remains
   - Files being modified
   - Any blockers or challenges encountered

   ## Next Steps
   Clear, prioritized list of what to do next:
   1. [High priority task]
   2. [Medium priority task]
   3. [Nice to have]

   ## Important Context for Next Instance
   Critical information the next Claude needs to know:
   - Architectural decisions and rationale
   - Gotchas or tricky areas to be aware of
   - Dependencies between components
   - Testing considerations

   ## Files Modified This Session
   List of all files touched:
   - `file1.py` - [what changed]
   - `file2.md` - [what changed]

   ## Open Questions/Decisions Needed
   Things that require user input or clarification:
   - Question 1?
   - Decision needed on approach X vs Y?

   ## Git Status
   ```
   [paste output of `git status`]
   ```

   ## Recent Commits
   ```
   [paste output of `git log -5 --oneline`]
   ```
   ```

3. **Verify Handoff Quality**
   - Read through `HANDOFF.md` - would YOU understand what to do next?
   - Ensure all context is clear and unambiguous
   - Include specific file paths and line numbers where relevant
   - Don't assume knowledge - be explicit

4. **Stage and Commit Handoff**
   ```bash
   git add HANDOFF.md
   git commit -m "docs: Add Claude instance handoff document"
   git push origin main
   ```

5. **Inform User**
   Tell the user:
   - Token budget is at 90%
   - Handoff document has been created
   - Current work status (complete, paused, blocked)
   - What the next instance should do first

### Starting a New Session (After Handoff)

When a new Claude instance begins and finds a `HANDOFF.md`:

1. **Read `HANDOFF.md` FIRST** - Before doing anything else
2. **Read `METHODOLOGY.md`** - Understand the project workflows
3. **Verify git state** - Run `git status` and compare to handoff
4. **Review recent commits** - Run `git log -5 --oneline`
5. **Check `todo` file** - See if there are active tasks
6. **Ask clarifying questions** - If anything is unclear, ask the user
7. **Delete or archive `HANDOFF.md`** - Once context is absorbed, remove it or move to `_archive/`

### Handoff Best Practices

**DO:**
- Be specific with file paths (e.g., `settings.py:127`)
- Explain WHY decisions were made, not just WHAT was done
- Include code snippets for complex logic
- List any new dependencies or requirements
- Document any workarounds or temporary solutions
- Note any performance or memory concerns

**DON'T:**
- Assume the next instance has your context
- Use vague language ("fix the thing", "update that file")
- Skip documenting in-progress work
- Leave uncommitted changes without explanation
- Forget to push the handoff document

### Emergency Handoffs

If a session is interrupted unexpectedly (crash, user needs to stop immediately):

The user can ask the next Claude instance to check:
- Latest commit message (often contains context)
- Git diff for uncommitted changes
- The `todo` file
- Recent backups in `/Users/keegandewitt/Cursor/_Backups/`

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

1. **Check for `HANDOFF.md`** - If present, read it FIRST (see [Claude Instance Handoff Protocol](#claude-instance-handoff-protocol))
2. **Read this document** - Understand our methodologies
3. **Check `git status`** - Understand current state
4. **Review `todo`** - See active tasks
5. **Read recent commits** - `git log -5 --oneline`
6. **Ask clarifying questions** - Don't assume, ask the user

### Key Commands to Run
```bash
ls -la                 # Check for HANDOFF.md first
cat HANDOFF.md         # If present, read handoff context
git status             # Current state
git log -5 --oneline   # Recent history
cat todo              # Active tasks
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

- **v1.1** (2025-10-21) - Added Claude instance handoff protocol
  - Token budget management at 90% threshold
  - Detailed handoff document template
  - Best practices for session continuity
  - Emergency handoff procedures

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
