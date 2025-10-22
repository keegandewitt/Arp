# Session Start: Onboarding Protocol

You are beginning a new session on the **Arp** project. This command provides comprehensive context about the project, recent work, and current status.

---

## Project Overview

**Name:** Arp - CircuitPython MIDI Arpeggiator
**Platform:** CircuitPython 9.x on RP2040-based boards (Raspberry Pi Pico, Adafruit M4 Express)
**Purpose:** Hardware MIDI arpeggiator with OLED display, button controls, and multiple pattern modes

### Core Features
- 6 arpeggiator patterns (Up, Down, Up-Down, Down-Up, Random, As Played)
- Internal/External MIDI clock synchronization
- OLED display with real-time BPM and pattern display
- Button-based UI for pattern and clock source selection
- Settings persistence to flash storage
- CV/Gate output support (in development)
- Low-latency MIDI processing (<1ms)
- Battery power management with deep sleep

### Hardware Components
- RP2040-based MCU (M4 Express or similar)
- SSD1306 OLED display (128x32, I2C)
- 2x MIDI FeatherWings (one for I/O, one for clock sync)
- 3 buttons (A, B, C) for UI control
- Optional CV/Gate output circuitry

---

## Critical First Steps

### 1. Check for HANDOFF.md
```bash
ls -la HANDOFF.md
```

If `HANDOFF.md` exists:
- **READ IT IMMEDIATELY** - Contains context from previous Claude instance
- Follow the handoff protocol in METHODOLOGY.md section "Claude Instance Handoff Protocol"
- Delete or archive HANDOFF.md once context is absorbed

### 2. Read METHODOLOGY.md
```bash
cat METHODOLOGY.md
```

This document contains:
- Git workflow and pre-commit checklist
- Backup strategy (ALWAYS backup before pushing)
- Claude instance handoff protocol
- Development guidelines and code style
- Testing procedures
- Documentation standards

**KEY REQUIREMENT:** Before ANY git push, run `python backup.py` to create a backup

### 3. Check Current Git Status
```bash
git status
git log -5 --oneline
```

Understand:
- What branch you're on
- Any uncommitted changes
- Recent commit history and what was worked on

### 4. Check for Active Tasks
```bash
cat todo 2>/dev/null || echo "No todo file found"
```

If a `todo` file exists, review active tasks.

### 5. Review Recent Commits for Context
```bash
git log --oneline -10 --graph
```

This shows the recent development timeline and helps you understand what's been worked on.

---

## MCP Server for Documentation Access

**Recommended:** This project is configured to use **mcp-server-docs** for efficient documentation access.

### What is MCP?

Model Context Protocol (MCP) allows you to search and retrieve documentation instantly, reducing token usage by ~80-90% compared to reading files directly.

### Check if MCP is Available

Try searching the documentation:
```
"Search the Arp documentation for MIDI clock information"
```

If MCP is working, you'll get instant results. If not, you'll need to read files manually.

### Setup Instructions

If MCP is not configured, see **MCP_SETUP.md** for complete setup instructions:
```bash
cat MCP_SETUP.md
```

**Key benefits with MCP:**
- Search all markdown files simultaneously
- ~90% reduction in documentation-reading tokens
- Faster context gathering during onboarding
- More token budget available for actual work

**Without MCP:** You can still read files directly using the Read tool, but it will be slower and use more tokens.

---

## Project Architecture

### Key Files & Modules

**Core Application:**
- `code.py` - Main entry point, hardware initialization, main loop
- `arpeggiator.py` - Arpeggiator engine, pattern generation logic
- `settings.py` - Global configuration, settings persistence
- `settings_menu.py` - Settings UI and menu system

**Hardware Interfaces:**
- `midi_io.py` - MIDI input/output handling (FeatherWing 1)
- `clock_handler.py` - MIDI clock sync and BPM calculation (FeatherWing 2)
- `cv_output.py` - CV/Gate output for modular synth integration
- `display.py` - OLED display management, UI rendering, auto-sleep
- `button_handler.py` - Button input, debouncing, pattern selection

**Utilities:**
- `install.py` - Installation and setup script
- `install_libs.py` - Library installation helper
- `hardware_tests.py` - Hardware validation test suite
- `connection_test.py` - Connection diagnostic tool
- `backup.py` - Backup automation script (RUN BEFORE EVERY PUSH)

### Documentation Files

**User Documentation:**
- `README.md` - Project overview, features, usage guide
- `INSTALLER_README.md` - Installation instructions
- `HARDWARE_BUILD_GUIDE.md` - Hardware assembly guide
- `TESTING_GUIDE.md` - Testing procedures
- `BOM.md` - Bill of materials

**Technical Documentation:**
- `METHODOLOGY.md` - Development workflow, git practices, handoff protocol
- `MCP_SETUP.md` - MCP server configuration for efficient doc access
- `CV_GATE_INTEGRATION.md` - CV/Gate feature documentation
- `HARDWARE_PINOUT.md` - Pin assignments
- `ENCLOSURE_ROADMAP.md` - Enclosure design plans

**Hardware Files:**
- `_hardware_files/` - KiCad files, Gerbers, Fusion360 scripts, enclosure generation

### Signal Flow
```
MIDI In → midi_io.py → arpeggiator.py → midi_io.py → MIDI Out
                            ↓
MIDI Clock → clock_handler.py (triggers steps + calculates BPM)
                            ↓
Buttons → button_handler.py → settings → display.py
```

---

## Recent Development Timeline

Run this command to see recent work:
```bash
git log --oneline --all -15 --format="%h - %s (%ar)"
```

### Key Milestones (from git history)
- **Most Recent:** Claude instance handoff protocol added to methodology
- **Recent:** Comprehensive documentation, CV/Gate output, settings menu
- **Earlier:** Installation package and hardware testing features
- **Initial:** CircuitPython MIDI Arpeggiator core implementation

### Current Development Focus
Based on recent commits, the project is in active development with focus on:
1. Documentation and methodology improvements
2. CV/Gate integration for modular synth compatibility
3. Hardware testing and validation
4. Installation/setup automation

---

## Git Workflow Requirements

### CRITICAL: Pre-Push Checklist

Before **EVERY** `git push`, you MUST:

1. **Run backup script:**
   ```bash
   python backup.py
   ```
   - Creates timestamped backup to `/Users/keegandewitt/Cursor/_Backups/`
   - Keeps only last 5 backups
   - This is NON-NEGOTIABLE

2. **Review changes:**
   ```bash
   git status
   git diff
   ```

3. **Stage files deliberately** (avoid `git add .` without review)

4. **Commit with clear message:**
   - Format: `<type>: <description>`
   - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `hardware`

5. **Push to remote:**
   ```bash
   git push origin main
   ```

### Current Branch Information
You should be on one of these branches:
- `main` - Production branch
- `claude/*` - Claude-specific development branches (created per session)

Check your current branch and recent commits:
```bash
git branch --show-current
git log -3 --oneline
```

---

## Development Guidelines

### Code Style
- **Language:** CircuitPython 9.x
- **Style:** PEP 8 (where applicable)
- **Line Length:** 100 characters max
- **Indentation:** 4 spaces (no tabs)

### CircuitPython Constraints
- **RAM:** Limited memory - be mindful of allocations
- **Performance:** OLED I2C is slow (~10-20ms) - throttle updates
- **Pins:** Document all pin assignments clearly
- **Error Handling:** Always handle hardware exceptions gracefully

### Module Design Principles
- Single Responsibility - Each module has one clear purpose
- Minimal Dependencies - Keep imports light for memory constraints
- State Management - Centralize in `settings.py`

---

## Testing Before Deployment

Before deploying code to hardware:

1. **Hardware Tests:**
   ```bash
   python hardware_tests.py
   ```

2. **Functionality Tests:**
   - MIDI input/output
   - Button responsiveness
   - Display updates
   - Settings persistence
   - Arpeggiator patterns

3. **Integration Tests:**
   - Full boot-to-arpeggiating workflow
   - Settings persistence across reboots

See `TESTING_GUIDE.md` for comprehensive procedures.

---

## Token Budget Management

This session has a 200,000 token budget. Monitor usage and follow handoff protocol:

**When token usage reaches 90% (180,000 tokens):**
1. Complete current task or pause at logical stopping point
2. Commit and push any work (with backup!)
3. Create `HANDOFF.md` (see METHODOLOGY.md for template)
4. Stage, commit, and push `HANDOFF.md`
5. Inform user of handoff

---

## Common Tasks

### Creating a Commit
```bash
# Review changes
git status
git diff

# Backup first (REQUIRED)
python backup.py

# Stage and commit
git add <files>
git commit -m "type: description"
git push origin main
```

### Checking System Status
```bash
# Git status
git status
git log -5 --oneline

# Check for handoff document
ls -la HANDOFF.md

# Check active tasks
cat todo

# View recent backups
ls -lt /Users/keegandewitt/Cursor/_Backups/ | head -6
```

### Reading Key Documentation
```bash
# Methodology (workflow, git, handoff)
cat METHODOLOGY.md

# Project overview
cat README.md

# Hardware setup
cat HARDWARE_BUILD_GUIDE.md
```

---

## Questions to Ask User

If context is unclear after reading HANDOFF.md (if present), ask:

1. What are we working on in this session?
2. Are there any blockers or issues from the previous session?
3. What's the priority for today's work?
4. Should I continue previous work or start something new?

---

## Your Next Steps

After running this `/start` command:

1. **Check for HANDOFF.md** - If present, read it thoroughly
2. **Read METHODOLOGY.md** - Understand workflows
3. **Run git status** - See current state
4. **Check todo file** - Any active tasks?
5. **Review recent commits** - Context from git history
6. **Ask user** - What should we work on?

---

## Session Initialized

You now have comprehensive context about the Arp project. You understand:
- The project's purpose and architecture
- Git workflow requirements (especially backup before push)
- Recent development timeline
- Where to find documentation
- How to check for handoff documents
- Token budget management

**Ready to begin!** Ask the user what they'd like to work on, or if there's a specific task to complete.
