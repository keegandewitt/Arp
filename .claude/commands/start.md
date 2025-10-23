# Start - Comprehensive Session Onboarding

Bring a new Claude instance up to speed with complete project context, methodology, current status, and exactly where we left off.

## Your Task:

Provide a comprehensive briefing by reading and synthesizing information from key project files. Present the information in a clear, organized way.

## Instructions for Claude:

### Step 1: Read Core Documentation (in parallel)
Read these files to understand the project:
- `docs/context/CONTEXT.md` - Living context and session handoff
- `METHODOLOGY.md` - Development philosophy and workflows
- `PROJECT_STATUS.md` - Current project state and roadmap
- `README.md` - Project overview (if exists)
- `todo` - Active task list

### Step 2: Check Project State
Run these commands to understand current state:
```bash
git status
git log -5 --oneline
git branch -a
```

### Step 3: Present Briefing

Present the following information to the user in a well-organized format:

#### 🎯 Project Overview
- What is this project? (Brief 2-3 sentence summary)
- What hardware platform?
- What's the current development stage?

#### 📍 Where We Are Now
- **Current Session Status**: From CONTEXT.md "Session Handoff" section
- **Last Session Summary**: What was accomplished last time
- **Git Status**: Clean or uncommitted changes?
- **Last Commit**: Hash and message
- **Current Branch**: Which branch are we on

#### 🎨 What We're Building
- Core features and their status (Complete ✅ / In Progress 🚧 / Planned 📋)
- Current architecture overview
- Hardware configuration summary

#### 🔨 How We Work Here
Brief summary of key methodology points:
- **Verify-Then-Act Protocol**: Always verify specs before implementation
- **Git Workflow**: Backup → Review → Commit → Push → Update CONTEXT
- **Dependency Management**: Always check libraries before deploying
- **Hardware Testing**: Test everything systematically
- **Available Commands**: List any /tidyup or other custom commands

#### 📋 Active Tasks
From the `todo` file - what's on the current task list?

#### 🚀 What's Next (Priority Order)
From CONTEXT.md "What's Next" section - immediate priorities

#### ⚠️ Known Issues
Any active blockers or important gotchas from PROJECT_STATUS.md

#### 📚 Quick Reference
Key file locations:
- Main entry: `main.py`
- Core modules: `arp/core/`
- Hardware tests: `tests/`
- Documentation: `docs/`
- Scripts: `scripts/`

Key commands:
```bash
# Deploy to hardware
cp main.py /Volumes/CIRCUITPY/code.py

# Check dependencies
circup list

# Monitor serial output
python3 scripts/monitor_serial.py

# Create backup
python3 scripts/backup.py

# Run tidyup workflow
/tidyup
```

#### 💡 Recent Learnings
Highlight 2-3 key lessons learned from METHODOLOGY.md (like the OLED driver discovery, dependency checking importance, etc.)

### Step 4: Ask the User
End with: "I'm up to speed! What would you like to work on?"

## Important Notes:
- **Be concise but comprehensive** - user needs the full picture quickly
- **Use visual markers** (✅ 🚧 📋 ⚠️) to make scanning easy
- **Highlight critical info** - blockers, uncommitted changes, active work
- **Don't assume** - if CONTEXT.md says we're mid-task, mention it clearly
- **Focus on continuity** - help user pick up exactly where they left off

## If Files Are Missing:
- If CONTEXT.md doesn't exist, check for `HANDOFF.md` in root
- If documentation is incomplete, note what's missing
- If todo file is empty, check git log for recent activity clues
