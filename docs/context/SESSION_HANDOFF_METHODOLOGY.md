# Session Handoff Methodology

**Purpose:** Ensures smooth continuity between Claude Code sessions through systematic documentation updates.

---

## When to Execute Handoff

Execute this protocol when:
- Token usage reaches ~180K / 200K (90%)
- Session is ending for any reason
- Major milestone completed
- Switching to different task/focus area

---

## Session End Protocol

### 1. Create Manual Backup FIRST

**Before any commits or documentation updates:**

```bash
cd /Users/keegandewitt/Cursor.ai
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
zip -r "_Backups/Arp_manual_$TIMESTAMP.zip" Arp \
  -x "*/.git/*" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x "*.DS_Store"
```

**Why first:** Captures current state before any final changes.

---

### 2. Verify All Code Changes Are Committed

```bash
cd /Users/keegandewitt/Cursor.ai/Arp
git status
```

**If there are uncommitted changes:**
- Review with `git diff`
- Decide: commit, stash, or document why uncommitted
- If committing: Follow git workflow from METHODOLOGY.md

---

### 3. Check Git Status and Recent Commits

```bash
git status
git log -5 --oneline
git branch
```

**Record:**
- Current branch
- Last commit hash and message
- Working tree status (clean / has changes)

---

### 4. Update docs/context/CONTEXT.md

Update the **Session Handoff** section with:

#### a) Header Metadata
```markdown
**Last Updated:** [Current timestamp]
**Session Status:** ✅ COMPLETE / ⏳ IN PROGRESS / ⚠️ BLOCKED
**Token Usage:** [XXK / 200K]
```

#### b) Current Session Summary
```markdown
### Current Session Summary (Session N)
**What was accomplished:**
- [Key accomplishment 1]
- [Key accomplishment 2]
- [Key accomplishment 3]

**Git Status:**
- **Branch:** [branch name]
- **Last Commit:** [hash] - [message]
- **Working Tree:** [clean / has changes]

**What's Next:**
1. [Next priority task]
2. [Second priority task]
3. [Third priority task]
```

#### c) Add to Session History
Add entry to the Session History section:
```markdown
### Session N (YYYY-MM-DD)
- **Focus:** [What was the main focus]
- **Outcome:** [What was accomplished]
- **Status:** ✅ Complete / ⏳ In Progress / ⚠️ Blocked
```

#### d) Update Active Work Section
- Mark completed tasks as done
- Add new tasks discovered during session
- Update priorities based on current state

#### e) Update Recently Modified Files
```markdown
### This Session (Session N)
- **file.py:line** - [What changed and why]
- **doc.md** - [What was updated]
```

#### f) Document Important Decisions
If any key decisions were made, add to "Important Decisions Made":
```markdown
### [Category] Decisions
- **[Decision Topic]:** [What was decided and why]
```

#### g) Update/Clear Blockers
- Remove resolved blockers
- Add new blockers discovered
- Update blocker status

---

### 5. Commit CONTEXT.md Update

```bash
git add docs/context/CONTEXT.md
git commit -m "docs: Update session handoff (Session N complete)"
```

**Optional:** If other documentation was updated, include in same commit:
```bash
git add START_HERE.md PROJECT_STATUS.md
git commit -m "docs: Update session handoff and project status (Session N complete)"
```

---

### 6. Verify Git Status Matches Documentation

```bash
git status
git log -1 --oneline
```

**Verify:**
- Working tree is clean (unless intentionally left uncommitted)
- Last commit includes CONTEXT.md update
- Git status matches what's documented in CONTEXT.md

---

### 7. Push to Remote (Optional)

**Only if ready to push:**
```bash
# Create backup first (automated)
python3 scripts/backup.py

# Push
git push origin main
```

**Note:** It's okay to NOT push if work is incomplete. Just document in CONTEXT.md that commits are local only.

---

### 8. Send Completion Notification (macOS)

```bash
osascript -e 'display notification "Session handoff complete. CONTEXT.md updated." with title "Arp Project"'
```

---

### 9. Summarize for User

Provide clear summary to user:

```
Session handoff complete!

This session (Session N):
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

Updated: docs/context/CONTEXT.md
Committed: [commit hash]

Next session should focus on:
1. [Priority 1]
2. [Priority 2]

Git status: [clean / has uncommitted changes]
Token usage: ~XXK / 200K
```

---

## Starting a New Session (Handoff Receipt)

When a new Claude instance starts:

### 1. Read START_HERE.md
Quick 30-second orientation.

### 2. Read docs/context/CONTEXT.md
**Focus on "Session Handoff" section:**
- What did previous session accomplish?
- What's the current git state?
- What are the next priorities?

### 3. Verify Git State
```bash
git status
git log -5 --oneline
```

Compare to what's documented in CONTEXT.md.

### 4. Check for Uncommitted Changes
If working tree is not clean:
- Review with `git diff`
- Understand why (should be documented in CONTEXT.md)
- Ask user if unsure

### 5. Review Active Work
Check CONTEXT.md "Active Work" section:
- What task is in progress?
- What's the current status?
- Are there blockers?

### 6. Ask User for Direction
Even with full context, **always ask user:**
- "I've reviewed the session context. What would you like to focus on today?"
- Offer the priorities from CONTEXT.md as options
- Be ready to pivot to different task if needed

---

## Best Practices

### DO:
- ✅ Update CONTEXT.md EVERY session end
- ✅ Be specific with file paths and line numbers
- ✅ Explain WHY decisions were made
- ✅ Document blockers and challenges
- ✅ Note incomplete work clearly
- ✅ Create backup before any documentation commits

### DON'T:
- ❌ Skip handoff updates (causes context loss)
- ❌ Use vague language ("fixed some stuff")
- ❌ Forget to commit CONTEXT.md updates
- ❌ Assume next instance has your context
- ❌ Leave uncommitted changes without explanation
- ❌ Update docs without committing them

---

## Emergency Handoff

If session is interrupted unexpectedly (crash, must stop immediately):

### User Action:
Tell next Claude instance:
> "Previous session was interrupted. Check git log, git diff, and docs/context/CONTEXT.md for context."

### Next Claude Action:
1. Read docs/context/CONTEXT.md (may be outdated)
2. Check `git log -10 --oneline` for recent commits
3. Check `git diff` for uncommitted changes
4. Check `todo` file
5. Check backups in `/Users/keegandewitt/Cursor/_Backups/`
6. Ask user to explain what was happening

---

## Handoff Quality Checklist

Before ending session, verify:

- [ ] Manual backup created
- [ ] All meaningful code changes committed (or documented why not)
- [ ] CONTEXT.md "Session Handoff" section updated
- [ ] Session added to "Session History"
- [ ] "Active Work" reflects current state
- [ ] "Recently Modified Files" is current
- [ ] Any new blockers documented
- [ ] "What's Next" priorities clear and actionable
- [ ] CONTEXT.md changes committed to git
- [ ] Git status matches documentation
- [ ] User informed of session status and next steps

---

## Version History

- **v1.0** (2025-10-22) - Initial methodology created for Arp project
  - Adapted from METHODOLOGY.md handoff protocol
  - Streamlined for CONTEXT.md living document approach
  - Added emergency handoff procedures

---

**This methodology ensures no context is lost between sessions and maintains project momentum.**
