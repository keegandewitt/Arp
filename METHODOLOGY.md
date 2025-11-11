# Project Methodology & Workflow Guide

**Last Updated:** 2025-10-22 (v1.3 - Added comprehensive dependency management)
**Project:** Arp - CircuitPython MIDI Arpeggiator
**Purpose:** This document guides all development, git workflows, and collaboration practices for this project.

---

## Table of Contents
1. [Git Workflow & Version Control](#git-workflow--version-control)
2. [Backup Strategy](#backup-strategy)
3. [Development Session Handoff Protocol](#development-session-continuity-protocol)
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
python scripts/backup.py
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

## Development Session Handoff Protocol

### Session budget Management
the development environment sessions have a token budget that auto-compacts when exceeded. To ensure smooth continuity:

**When session progress reaches 90% (90% of session capacity):**

1. **Stop at a Clean Checkpoint**
   - Complete current task if nearly done
   - Otherwise, pause at a logical stopping point
   - Commit and push any uncommitted work (following the git workflow above)
   - Run backup: `python3 scripts/backup.py`

2. **Create Handoff Document**
   Create `HANDOFF.md` in the project root with the following sections:

   ```markdown
   # Development Session Handoff

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
   Critical information the next the assistant needs to know:
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
   git commit -m "docs: Add development session handoff document"
   git push origin main
   ```

5. **Inform User**
   Tell the user:
   - Session budget is at 90%
   - Handoff document has been created
   - Current work status (complete, paused, blocked)
   - What the next instance should do first

### Starting a New Session (After Handoff)

When a new development session begins and finds a `HANDOFF.md`:

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

The user can ask the next development session to check:
- Latest commit message (often contains context)
- Git diff for uncommitted changes
- The `todo` file
- Recent backups in `/Users/keegandewitt/Cursor/_Backups/`

---

## Development Guidelines

### CRITICAL: Deployment Workflow (main.py vs code.py)

**The Problem:**
- CircuitPython devices run `code.py` on boot
- Our repository uses `main.py` as the source of truth
- Editing one without deploying causes version mismatches and confusion

**The Solution:**
1. **ALWAYS** edit `main.py` in the repository (never edit `code.py` on device)
2. **ALWAYS** deploy using the deployment script (never manually copy files)
3. **VERIFY** deployment succeeded before testing

**Deployment Commands:**
```bash
# Deploy all changed files
python3 scripts/deploy.py

# Check what needs deployment (dry run)
python3 scripts/deploy.py --check

# Force deploy everything
python3 scripts/deploy.py --force

# Watch for changes and auto-deploy
python3 scripts/deploy.py --watch
```

**What Gets Deployed:**
- `main.py` → `/Volumes/CIRCUITPY/code.py` (main entry point)
- `arp/core/*.py` → `/Volumes/CIRCUITPY/arp/core/*.py` (core modules)
- `arp/ui/*.py` → `/Volumes/CIRCUITPY/arp/ui/*.py` (UI modules)
- `arp/utils/*.py` → `/Volumes/CIRCUITPY/arp/utils/*.py` (utilities)

**Important Notes:**
- Both files have warning comments at the top
- Device auto-reloads after deployment (~2-3 seconds)
- Deploy script checks file hashes to avoid unnecessary copies
- Use `--check` to see what's out of sync without deploying

**Never:**
- ❌ Edit `code.py` directly on the device
- ❌ Manually copy files with `cp` command
- ❌ Forget to deploy after editing `main.py`
- ❌ Assume changes are live without deploying

**Always:**
- ✅ Edit `main.py` in repository
- ✅ Use `python3 scripts/deploy.py` to deploy
- ✅ Wait for auto-reload (watch serial output)
- ✅ Test on hardware after deployment

---

### Core Development Philosophy: Verify-Then-Act Protocol

**Principle:** Be extremely detailed and rigorous. Validate assumptions before acting on them.

**The Protocol:**
1. **Verify** - Check specifications, read documentation, examine existing code
2. **Assess** - Do you have sufficient information to proceed confidently?
3. **Gather** - If information is missing or unclear, gather more context
4. **Reassess** - With new information, do you now understand fully?
5. **Act** - Only proceed when verification is complete

**Key Behavior:** If you need more information or context, GET IT, then reassess before acting.

**In Practice:**
- **Verify before implementing** - Check specifications, read documentation, examine existing code
- **Test assumptions** - Don't assume compatibility, behavior, or state - verify it
- **Read first, code second** - Understand the full context before making changes
- **Gather when uncertain** - Missing information? Read more files, check docs, search the codebase
- **Reassess continuously** - New information may change your approach
- **Document findings** - Record what you verified so others don't repeat the work
- **Ask when blocked** - If context isn't available in the codebase, ask the user

**Examples:**
- Before using a library: Check its compatibility with your platform version
- Before modifying code: Read the surrounding context and understand the current behavior
- Before assuming a feature exists: Search the codebase or documentation
- Before deploying: Test in isolation first

**Anti-patterns to Avoid:**
- ❌ Assuming library X works with platform Y without checking
- ❌ Making changes based on partial information
- ❌ Skipping validation steps to "save time"
- ❌ Implementing solutions before fully understanding the problem
- ❌ Guessing at specifications instead of looking them up

**Time Investment:**
- 5 minutes verifying specifications vs. 2 hours debugging wrong assumptions
- 10 minutes reading existing code vs. breaking working functionality
- 2 minutes checking documentation vs. implementing the wrong solution

This principle applies to ALL development activities: hardware selection, software design, testing, integration, and debugging.

---

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

## Dependency Compatibility Validation

### CRITICAL: Verify Compatibility BEFORE Installing or Deploying

**The most important lesson: Library compatibility issues can brick your workflow, crash your device, and waste hours of debugging.**

**NEW CORE PRINCIPLE: Test compatibility in a safe environment BEFORE deploying to hardware.**

### The Problem We Experienced

- Installed libraries without checking CircuitPython version compatibility
- Libraries crashed the M4 with hard faults (memory access errors)
- Multiple safe mode crashes required recovery
- Wasted significant time debugging incompatible libraries
- Could have been prevented with upfront compatibility checking

### Compatibility Validation Workflow

**BEFORE installing ANY library, follow these steps:**

#### 1. Check CircuitPython Version on Device

```bash
# Always know what version you're running
cat /Volumes/CIRCUITPY/boot_out.txt | grep "CircuitPython"
# Example output: Adafruit CircuitPython 10.0.3
```

**Record this version** - it determines which library bundle you need.

#### 2. Research Library Compatibility

**For each library you need:**

1. **Check Adafruit Learn Guides** - Look for "compatible with CircuitPython X.x" notes
2. **Check GitHub Issues** - Search for your CP version + library name + "crash" or "incompatible"
3. **Check CircuitPython Bundle Release Notes** - See what changed between versions
4. **Look for Known Issues** - Check if others have reported crashes

**Red Flags:**
- Library hasn't been updated in over a year
- GitHub issues mentioning crashes with your CP version
- API changes between CP major versions (9.x → 10.x)
- Libraries requiring `displayio.I2CDisplay` (removed in CP 10.x)

#### 3. Create a Safe Test Environment

**NEVER test untrusted libraries directly in your project code.**

Create a minimal test file first:

```python
# test_library_import.py
"""
Safe library import test
Tests if library loads without crashing
"""

import time

print("Starting safe library test...")

try:
    print("Importing library...")
    import library_name_here
    print("✓ Import successful!")

    # Try basic initialization if applicable
    print("Testing basic usage...")
    # obj = library_name_here.ClassName(...)

    print("✓✓✓ Library appears compatible!")

except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("Library not installed or wrong name")

except Exception as e:
    print(f"✗ Runtime error: {type(e).__name__}: {e}")
    print("Library may be incompatible with this CP version")

print("\nTest complete - board still stable")
while True:
    time.sleep(1)
```

**Deploy this test FIRST** before integrating into your main code.

#### 4. Test Library Incrementally

When testing a new library:

1. **Import only** - Does it load without crashing?
2. **Initialize with minimal params** - Can you create an object?
3. **Test basic operations** - Does the simple API work?
4. **Test your use case** - Does your specific function work?

**Stop at the first failure** and investigate before proceeding.

#### 5. Document Working Configurations

When you find a working library version:

```bash
# Freeze the working configuration
circup freeze > requirements_circuitpy.txt
```

This creates a **locked dependency list** you can restore later.

**Commit this file to git:**
```bash
git add requirements_circuitpy.txt
git commit -m "docs: Add working library versions for CP 10.0.3"
```

### Pre-Deployment Compatibility Checklist

**Before deploying code that uses external libraries:**

- [ ] **CircuitPython version verified** - `cat /Volumes/CIRCUITPY/boot_out.txt`
- [ ] **Library compatibility researched** - Checked Learn guides, GitHub issues
- [ ] **Safe import test created** - Minimal test file prepared
- [ ] **Import test passed** - Library loads without errors
- [ ] **Basic usage tested** - Simple operations work
- [ ] **No crashes in safe mode** - Board remains stable
- [ ] **Dependencies documented** - `circup freeze` output saved
- [ ] **Recovery code ready** - Know how to exit safe mode if crash occurs

### Recovery from Incompatible Libraries

**If a library causes a hard crash (safe mode):**

1. **Don't panic** - The device is recoverable
2. **Deploy safe code immediately:**
   ```bash
   cat > /Volumes/CIRCUITPY/code.py << 'EOF'
   import time
   print("Recovery mode - board stable")
   while True:
       time.sleep(1)
   EOF
   ```
3. **Press RESET button** - Exit safe mode
4. **Remove problematic library:**
   ```bash
   circup uninstall library_name
   ```
5. **Verify board is stable** - Should see "Recovery mode" message
6. **Research alternative** - Find compatible library or different approach

### Known Compatibility Issues

#### CircuitPython 10.x Breaking Changes

**Libraries that DON'T work with CP 10.0.3 (from our testing):**

| Library | Version | Issue | Alternative |
|---------|---------|-------|-------------|
| `adafruit_ssd1306` | 2.x | Hard crash - memory fault | Use raw I2C commands or older CP version |
| `adafruit_displayio_ssd1306` | 3.0.4 | Wrong driver for 128x64 FeatherWing | Use `adafruit_displayio_sh1107` instead |

**API Changes to Watch For:**
- `displayio.I2CDisplay()` - **Removed** in CP 10.x (use direct bus passing)
- Display initialization signatures changed
- Some bus creation methods deprecated

#### Working Configurations (Verified)

**CircuitPython 10.0.3 + Feather M4 CAN:**

| Library | Version | Status | Notes |
|---------|---------|--------|-------|
| `neopixel` | 6.3.18 | ✅ Working | No issues |
| `adafruit_pixelbuf` | 2.0.10 | ✅ Working | Dependency for neopixel |
| `adafruit_ssd1306` | Latest | ❌ Crashes | Hard fault - avoid |
| `adafruit_displayio_ssd1306` | 3.0.4 | ❌ Wrong driver | For 128x32 FeatherWing only |
| `adafruit_displayio_sh1107` | Latest | ✅ Working | For 128x64 FeatherWing (#4650) |

### Compatibility Testing Script

Use `scripts/test_library_compatibility.py` to safely test libraries:

```bash
# Test a specific library
python3 scripts/test_library_compatibility.py library_name

# Deploy to device for hardware-specific testing
cp scripts/safe_library_test.py /Volumes/CIRCUITPY/code.py
# Edit code.py to test your specific library
```

---

## Dependency Management

### Core Principle: ALWAYS Check Dependencies First

**Never deploy code without verifying all required libraries are installed AND compatible.**

This applies to:
- Deploying to hardware
- Running tests
- Using any script that imports external libraries
- After any git pull or code update

### CircuitPython Library Management

#### Tool: circup (CircuitPython Library Manager)

**Installation:**
```bash
# Install circup (one-time setup)
pip3 install --upgrade circup

# Add to PATH if needed (check installation warnings)
# macOS: Add to ~/.zshrc or ~/.bash_profile:
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

**Usage:**
```bash
# Check what's installed on connected device
circup list

# Check for required libraries
circup freeze

# Install a library
circup install <library_name>

# Install multiple libraries
circup install neopixel adafruit_midi adafruit_displayio_ssd1306

# Update all libraries to latest compatible versions
circup update --all
```

### Dependency Checking Workflow

#### Before Every Deployment:

1. **Identify Required Libraries**
   - Check all `import` statements in the code
   - Check for external dependencies (not built-in CircuitPython modules)
   - Review code comments or requirements files

2. **Verify CircuitPython Built-ins vs External**

   **Built-in (no installation needed):**
   - `board`, `digitalio`, `analogio`, `busio`, `time`, `json`, `sys`, `os`
   - `pwmio`, `microcontroller`, `storage`, `supervisor`

   **External (require installation):**
   - `neopixel` - NeoPixel/RGB LED control
   - `adafruit_midi` - MIDI input/output
   - `adafruit_displayio_ssd1306` - OLED display driver
   - `adafruit_display_text` - Text rendering on displays
   - `adafruit_debouncer` - Button debouncing
   - Any library starting with `adafruit_*`

3. **Check Installed Libraries**
   ```bash
   # Connect device, then:
   circup list

   # Or manually check:
   ls /Volumes/CIRCUITPY/lib/
   ```

4. **Install Missing Dependencies**
   ```bash
   # Use circup to install missing libraries
   circup install <library_name>

   # Or use our helper script:
   scripts/install_libs.py
   ```

5. **Verify Installation**
   ```bash
   # List installed libraries again
   circup list

   # Check file sizes (should be > 0 bytes)
   ls -lh /Volumes/CIRCUITPY/lib/
   ```

### Automated Dependency Checking

**Use helper scripts that check dependencies automatically:**

```bash
# Before deploying pin test:
scripts/deploy_pin_test.sh  # Should auto-check dependencies

# Before deploying main code:
scripts/install.py  # Should verify all libs before copying files
```

**All deployment scripts MUST:**
1. Check for CIRCUITPY mount point
2. Verify required libraries are installed
3. Install missing libraries automatically (with user confirmation)
4. Report what was installed
5. Only proceed with deployment after dependencies are satisfied

### Dependency Documentation

**Every Python file that requires external libraries MUST include:**

At the top of the file (after docstring):
```python
"""
Module description here.

Required CircuitPython Libraries:
- neopixel (install via: circup install neopixel)
- adafruit_midi (install via: circup install adafruit_midi)

Built-in Dependencies:
- board, digitalio, time
"""
```

**In README or installation docs:**
- List ALL external library dependencies
- Provide circup install command for all dependencies at once
- Note CircuitPython version compatibility

### Common Pitfall: "ImportError: no module named X"

**When you see this error:**

1. **DO NOT ignore it** - Fix it immediately
2. **Identify the missing library**
3. **Check if it's external or a typo**
4. **Install via circup**
5. **Verify installation**
6. **Test again**

**Example Fix:**
```bash
# Error: ImportError: no module named 'neopixel'

# Fix:
circup install neopixel

# Verify:
circup list | grep neopixel
# Should show: neopixel

# Device auto-reloads, test again
```

### Version Compatibility

**CircuitPython Library Bundles:**
- Libraries are version-specific to CircuitPython major version
- 9.x libraries for CircuitPython 9.x
- 10.x libraries for CircuitPython 10.x
- circup handles this automatically

**Check Your Version:**
```bash
cat /Volumes/CIRCUITPY/boot_out.txt | grep "CircuitPython"
# Example: Adafruit CircuitPython 10.0.3
```

circup will download the correct bundle (e.g., 10.x-mpy) automatically.

### Project-Specific Requirements

**For Arp Project:**

**Required External Libraries:**
- `adafruit_midi` - MIDI communication
- `adafruit_displayio_sh1107` - OLED display (128x64 FeatherWing #4650)
- `adafruit_display_text` - Text on display
- `adafruit_debouncer` - Button handling
- `neopixel` - Status LED (for testing)

**Install All At Once:**
```bash
circup install adafruit_midi adafruit_displayio_sh1107 adafruit_display_text adafruit_debouncer neopixel
```

**Or use project installer:**
```bash
python3 scripts/install_libs.py
```

---

## Testing Procedures

### Pre-Deployment Testing
Before deploying to hardware:

1. **Check Dependencies FIRST:**
   ```bash
   circup list
   # Verify all required libraries are installed
   ```

2. **Hardware Tests:** `python tests/hardware_tests.py` or load on device
3. **Functionality Tests:**
   - MIDI input/output
   - Button responsiveness
   - Display updates
   - Settings persistence
   - Arpeggiator patterns
4. **Integration Tests:**
   - Full workflow from boot to arpeggiating
   - Settings changes and persistence across reboots

### Hardware Testing
See `docs/features/TESTING_GUIDE.md` for comprehensive hardware validation procedures.

---

## Documentation Standards

### Required Documentation
Every significant feature or hardware change requires documentation:

- **Code Comments:** Complex logic should have inline comments
- **Module Docstrings:** Every `.py` file should have a module-level docstring
- **Function Docstrings:** Public functions should document parameters and return values
- **README Updates:** Keep `docs/installation/INSTALLER_README.md` current
- **Hardware Docs:** Update `docs/hardware/HARDWARE_BUILD_GUIDE.md` for any hardware changes

### Documentation Files
- `README.md` - Project overview (create if needed)
- `docs/installation/INSTALLER_README.md` - Installation instructions
- `docs/hardware/HARDWARE_BUILD_GUIDE.md` - Hardware assembly
- `docs/features/TESTING_GUIDE.md` - Testing procedures
- `docs/features/CV_GATE_INTEGRATION.md` - CV/Gate feature documentation
- `docs/features/ENCLOSURE_ROADMAP.md` - Enclosure design plans
- `docs/hardware/BOM.md` - Bill of materials
- `METHODOLOGY.md` - This document

---

## Hardware Development

### ⚠️ CRITICAL HARDWARE CONFIGURATION NOTE

**MIDI FeatherWing is NEVER stacked on the M4!**

The physical configuration is:
- **STACKED:** OLED FeatherWing (128x64) on top of Feather M4 CAN
- **BREADBOARD:** MIDI I/O (DIN-5 jacks) connected via jumper wires to D0/D1

**DO NOT suggest stacking the MIDI FeatherWing.** It stays on the breadboard for prototyping flexibility. Only the OLED is stacked.

---

### CRITICAL LESSON: Verify Requirements Match Implementation

**Date Learned:** 2025-11-01
**Context:** CV output implemented with 2V/octave instead of 1V/octave standard

**What Happened:**
- User specified "1V/octave" requirement (industry standard) for weeks
- Implementation used LM358N with 2× gain: DAC (0-5V) → Op-amp → Jack (0-10V)
- Result: 2V/octave at output jack (non-standard, incompatible with most VCOs)
- Issue went undetected for multiple sessions

**Root Cause:**
- Assumption that "more voltage is better" (0-10V vs 0-5V)
- Did not verify that 2× gain breaks 1V/octave standard
- Focused on achieving 10V maximum rather than correct tracking

**The Correct Implementation:**
- **1V/octave Standard:** MIDI note number / 12 = voltage in volts
- **DAC direct output:** 0-5V from MCP4728 Channel A → 1V/octave ✓
- **No op-amp needed:** Direct connection to 1/8" jack
- **5 octaves range:** C0-C4 (MIDI 12-60) = 0-5V = sufficient for arpeggiator

**Key Learning:**
- **Standards exist for a reason** - 1V/octave is universal in modular synthesis
- **More voltage ≠ better** - 5V with correct scaling > 10V with wrong scaling
- **Verify math against specs** - 2× gain means 2V/octave, not 1V/octave
- **Question "improvements"** - Adding complexity should solve a real problem

**Time Cost:**
- 2 weeks of sessions with incorrect implementation
- LM358N op-amp circuit unnecessary (wasted effort)
- Could have been caught by verifying: "Does 2× gain preserve 1V/octave?" (No!)

**New Protocol - CV Implementation:**
1. ✅ **Verify voltage standard FIRST** (1V/octave for modular)
2. ✅ **Calculate output range** (MIDI → voltage formula)
3. ✅ **Verify gain doesn't break standard** (1× gain only for 1V/octave)
4. ✅ **Question added complexity** (Do we need op-amp? Why?)
5. ✅ **Test with VCO** (Real-world verification)

---

### CRITICAL LESSON: Always Verify Hardware Specifications FIRST

**Date Learned:** 2025-10-22
**Context:** OLED FeatherWing 128x64 displaying garbled output

**What Happened:**
- Spent hours troubleshooting garbled OLED display output
- Tried multiple library versions, initialization sequences, COM configurations
- Problem: Using SSD1306 driver for a display that has SH1107 chip

**Root Cause:**
- Did NOT check the actual hardware specifications first
- Assumed OLED FeatherWing used SSD1306 (like the 128x32 version)
- Product #4650 (128x64) actually uses **SH1107 driver**

**What Should Have Been Done:**
1. **Go to the product page FIRST:** adafruit.com/product/[ID]
2. **Read the specifications carefully:** Look for "Driver:", "Chip:", etc.
3. **Verify before coding:** Confirm chip model matches library
4. **Then proceed with code**

**The Fix:**
- Checked product page → Found "Driver: SH1107"
- Installed correct library: `circup install adafruit_displayio_sh1107`
- Changed one line in display.py: `SSD1306` → `SH1107`
- **Display worked immediately**

**Time Saved by This Approach:**
- Previous approach: 2+ hours of troubleshooting
- Correct approach: 5 minutes to identify and fix

**New Protocol - Hardware Troubleshooting:**

When hardware doesn't work:
1. ✅ **Check product page specifications FIRST**
2. ✅ **Verify chip/driver model**
3. ✅ **Confirm library matches hardware**
4. ✅ **Search for product-specific guides/examples**
5. ✅ **Only then try code variations**

**DO NOT:**
- ❌ Assume specifications based on similar products
- ❌ Try random code variations without understanding root cause
- ❌ Test library updates before confirming correct library
- ❌ Spend hours on initialization parameters when using wrong driver

**This lesson applies to ALL hardware integration:**
- Displays (check driver chip)
- Sensors (check communication protocol)
- Motors (check voltage/current requirements)
- Any component (check actual specs vs. assumptions)

---

### Rigorous Hardware Validation Philosophy

**Core Principle:** Test EVERYTHING, not just what we're using.

When bringing up new hardware or validating soldering/assembly:

1. **Complete Pin Testing**
   - Test ALL pins on the microcontroller, not just pins used by the project
   - Validate every GPIO, analog input, communication bus, power pin
   - Document which pins pass/fail testing
   - Rationale: Verifies assembly quality, catches cold solder joints, identifies damaged components

2. **Systematic Test Approach**
   - Follow a methodical, pin-by-pin testing sequence
   - Test basic functionality first (GPIO toggle, analog read, pull-up/down)
   - Progress to advanced functions (PWM, I2C, SPI, UART, DAC, ADC)
   - Document every test result in a test log

3. **Test Before Integration**
   - Validate hardware independently before running application code
   - Use dedicated test scripts that exercise individual subsystems
   - Verify power rails, voltage levels, current draw
   - Check for shorts, opens, and intermittent connections

4. **Documentation Requirements**
   - Create comprehensive test scripts that others can replicate
   - Log all test results with pass/fail status
   - Note any anomalies, even if they don't cause immediate failure
   - Include scope traces or multimeter readings for critical signals

5. **Failure Analysis**
   - If ANY pin fails, investigate thoroughly before proceeding
   - Use continuity testing, voltage measurements, scope traces
   - Check solder joints under magnification
   - Don't assume "it's probably fine" - verify and document

**Benefits of This Approach:**
- Catches manufacturing/assembly defects early
- Builds confidence in hardware reliability
- Creates reusable test infrastructure
- Provides baseline for troubleshooting future issues
- Documents hardware capabilities comprehensively

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

## Onboarding New the assistant Instances

When starting a new the development environment session:

1. **Check for `HANDOFF.md`** - If present, read it FIRST (see [Development Session Handoff Protocol](#development-session-continuity-protocol))
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

- **v1.4** (2025-10-23) - Added Verify-Then-Act Protocol
  - **Core Philosophy:** Established explicit 5-step verification protocol
  - Replaced metaphorical language with clear, actionable instructions
  - Added iterative "Gather → Reassess" loop for incomplete information
  - Emphasized getting context before acting, not making assumptions
  - Key addition: "If you need more information or context, GET IT, then reassess"

- **v1.3** (2025-10-22) - Added Comprehensive Dependency Management
  - **Core Principle:** ALWAYS check dependencies before deployment
  - Documented circup installation and usage
  - Created dependency checking workflow (5-step process)
  - Distinguished built-in vs external CircuitPython libraries
  - Added project-specific library requirements
  - Created automated dependency checker script (`scripts/check_dependencies.py`)
  - Updated deployment scripts to auto-check/install dependencies
  - Documented dependency headers for all Python files
  - Updated testing procedures to include dependency verification

- **v1.2** (2025-10-22) - Added Rigorous Hardware Validation Philosophy
  - Established "test everything" principle for hardware bring-up
  - Defined systematic pin-by-pin testing approach
  - Documented comprehensive validation requirements
  - Added failure analysis procedures

- **v1.1** (2025-10-21) - Added development session handoff protocol
  - Session budget management at 90% threshold
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
- All team members (and the assistant instances) should follow these guidelines
- When in doubt, refer to this document or ask for clarification
- Consistency is key to maintainable code and smooth collaboration
