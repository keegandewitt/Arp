# Tidy Up - Commit, Backup, and Push Workflow

Execute the full "Commit, Backup Archive, Push, and Update Context" routine for the Arp project.

## Workflow Steps:

1. **Review changes** - Run `git status` and `git diff` to show what will be committed
2. **Create backup** - Run `python3 scripts/backup.py` to create timestamped archive
3. **Stage and commit** - Add files and create commit with AI-generated message
4. **Push to remote** - Push to origin/main
5. **Update CONTEXT.md** - Update the "Session Handoff" section with latest commit info

## Instructions for Claude:

Follow this procedure:

### Step 1: Review Changes
Run `git status` and `git diff` to see what's changed. Present a summary to the user.

### Step 2: Ask for Commit Message
Ask the user: "What commit message would you like?"

Suggest a message based on the changes you see, following the format:
- `feat: <description>` - New feature
- `fix: <description>` - Bug fix
- `docs: <description>` - Documentation changes
- `refactor: <description>` - Code refactoring
- `test: <description>` - Test changes
- `chore: <description>` - Maintenance tasks
- `hardware: <description>` - Hardware-related changes

### Step 3: Create Backup
Run: `python3 scripts/backup.py`

Verify backup succeeded before proceeding.

### Step 4: Commit and Push
```bash
git add .
git commit -m "<user's message>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin main
```

### Step 5: Update CONTEXT.md
Update the "Session Handoff" section in `docs/context/CONTEXT.md`:
- Update "Last Updated" date
- Update "Git Status" with clean working tree
- Update "Last Commit" with the new commit hash and message
- Do NOT update session summary unless user requests it

### Step 6: Confirm Completion
Report to user:
- ✅ Backup created: [filename]
- ✅ Committed: [commit hash] - [commit message]
- ✅ Pushed to origin/main
- ✅ CONTEXT.md updated

**IMPORTANT:** Follow the Verify-Then-Act Protocol - check that each step succeeds before proceeding to the next.
