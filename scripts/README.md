# Arp Scripts

Utility scripts for development, deployment, and testing.

## 🚀 Deployment (MOST IMPORTANT!)

### `deploy.py` - Deploy Code to Hardware

**Use this EVERY TIME you edit main.py or any arp/ modules!**

```bash
# Deploy all changed files
python3 scripts/deploy.py

# Check what needs deployment (no changes made)
python3 scripts/deploy.py --check

# Force deploy everything
python3 scripts/deploy.py --force

# Watch for changes and auto-deploy (development mode)
python3 scripts/deploy.py --watch
```

**What it does:**
- Syncs `main.py` → `/Volumes/CIRCUITPY/code.py`
- Syncs all `arp/` modules to device
- Only copies changed files (checks SHA256 hashes)
- Shows color-coded status messages

**Why it exists:**
- CircuitPython runs `code.py`, but our repo uses `main.py`
- Manual copying with `cp` is error-prone
- Prevents version mismatches between repo and hardware

---

## 📦 Installation

### `install_libs.py` - Install CircuitPython Libraries

```bash
python3 scripts/install_libs.py
```

Installs required libraries via `circup`:
- adafruit_midi
- adafruit_displayio_sh1107
- adafruit_display_text
- adafruit_debouncer
- neopixel

---

## 🔍 Monitoring & Debugging

### `monitor_serial.py` - Clean Serial Monitor

```bash
# Monitor with auto-reload on changes
python3 scripts/monitor_serial.py --reload

# Monitor for 60 seconds then exit
python3 scripts/monitor_serial.py --duration 60

# Monitor with filtering
python3 scripts/monitor_serial.py --filter "ERROR"
```

**Features:**
- Automatic cleanup on exit
- Color-coded output
- Timestamp support
- Filter by regex

### `read_serial.py` - Simple Serial Reader

```bash
python3 scripts/read_serial.py
```

Basic serial port reader without fancy features.

---

## 💾 Backup

### `backup.py` - Create Project Backup

```bash
# Create timestamped backup
python3 scripts/backup.py

# Named milestone backup
python3 scripts/backup.py --milestone "pre-cv-gate"
```

**What it does:**
- Creates tar.gz archive in `/Users/keegandewitt/Cursor/_Backups/`
- Automatically rotates old backups (keeps last 5)
- Excludes `.git/`, `__pycache__/`, etc.

**When to use:**
- Before major refactoring
- Before `git push`
- Before hardware changes

---

## 🧪 Testing

### `check_dependencies.py` - Verify Library Installation

```bash
python3 scripts/check_dependencies.py
```

Checks if all required CircuitPython libraries are installed on device.

### `simple_test.py` - Basic Hardware Test

```bash
cp scripts/simple_test.py /Volumes/CIRCUITPY/code.py
```

Simple test to verify device boots and basic functionality works.

---

## 📋 Shell Scripts

### `deploy_pin_test.sh` - Deploy Pin Test

```bash
bash scripts/deploy_pin_test.sh
```

Deploys comprehensive pin test to hardware.

### `monitor_m4.sh` - M4-Specific Monitor

```bash
bash scripts/monitor_m4.sh
```

Serial monitor configured for Feather M4.

### `watch.sh` - File Watcher

```bash
bash scripts/watch.sh
```

Watches for file changes (legacy, use `deploy.py --watch` instead).

---

## 🎯 Workflow Examples

### Typical Development Session

```bash
# 1. Edit code in repository
vim main.py

# 2. Deploy to hardware
python3 scripts/deploy.py

# 3. Monitor serial output
python3 scripts/monitor_serial.py --reload
```

### Before Committing Changes

```bash
# 1. Create backup
python3 scripts/backup.py

# 2. Verify deployment is up-to-date
python3 scripts/deploy.py --check

# 3. Commit and push
git add .
git commit -m "feat: Add new feature"
git push
```

### Debugging Issues

```bash
# 1. Force redeploy everything
python3 scripts/deploy.py --force

# 2. Check libraries are installed
python3 scripts/check_dependencies.py

# 3. Monitor serial output
python3 scripts/monitor_serial.py --reload
```

---

## 📚 See Also

- `../METHODOLOGY.md` - Complete development methodology
- `../docs/` - Project documentation
- `../README.md` - Project overview
