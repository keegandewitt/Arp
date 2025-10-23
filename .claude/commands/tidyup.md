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

### Step 2: Generate Commit Message
**AUTOMATICALLY** generate a commit message based on the changes you see. DO NOT ASK THE USER.

Follow this format:
- `feat: <description>` - New feature
- `fix: <description>` - Bug fix
- `docs: <description>` - Documentation changes
- `refactor: <description>` - Code refactoring
- `test: <description>` - Test changes
- `chore: <description>` - Maintenance tasks
- `hardware: <description>` - Hardware-related changes

Analyze the git diff and create a concise, descriptive commit message.
Show the user what commit message you generated.

### Step 3: Create Backup
Run: `python3 scripts/backup.py`

Verify backup succeeded before proceeding.

### Step 4: Commit and Push
```bash
git add .
git commit -m "<generated message>"
git push origin main
```

**STRICT RULE:** NEVER include any mention of "Claude", "Claude Code", "AI", or "Generated with" in commit messages.
Commit messages must be clean, professional, and contain ONLY the technical description of changes.

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
