#!/usr/bin/env python3
"""
MIDI Arpeggiator - Auto-Installer
==================================

Automatically detects when the Feather board is connected and syncs missing files.

Features:
- Detects CIRCUITPY drive automatically
- Checks for missing/outdated files
- Uploads only what's needed
- Verifies installation
- Safe - won't overwrite newer files without confirmation

Usage:
    python3 install.py                    # One-time install
    python3 install.py --watch            # Monitor and auto-install on connect
    python3 install.py --force            # Force reinstall all files
    python3 install.py --check            # Just check what's missing
"""

import os
import sys
import time
import shutil
import hashlib
from pathlib import Path

# Configuration
PROJECT_DIR = Path(__file__).parent.absolute()
CIRCUITPY_MOUNT_POINTS = [
    "/Volumes/CIRCUITPY",  # macOS
    "/media/CIRCUITPY",     # Linux
    "D:/",                  # Windows (may vary)
    "E:/",                  # Windows alternate
]

# Files to sync (source_file: destination_path_on_device)
FILES_TO_SYNC = {
    "code.py": "code.py",
    "settings.py": "settings.py",
    "midi_io.py": "midi_io.py",
    "clock_handler.py": "clock_handler.py",
    "arpeggiator.py": "arpeggiator.py",
    "display.py": "display.py",
    "button_handler.py": "button_handler.py",
    "cv_output.py": "cv_output.py",  # CV/trigger output handler
    "settings_menu.py": "settings_menu.py",  # Hierarchical settings menu
    "test_commands.py": "test_commands.py",  # Hardware test commands
}

# Optional files (won't fail if missing)
OPTIONAL_FILES = {
    "TESTING_GUIDE.md": "TESTING_GUIDE.md",
    "README.md": "README.md",
    "HARDWARE_PINOUT.md": "HARDWARE_PINOUT.md",
}


class Colors:
    """Terminal colors for pretty output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓{Colors.ENDC} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠{Colors.ENDC} {text}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗{Colors.ENDC} {text}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ{Colors.ENDC} {text}")


def find_circuitpy():
    """Find CIRCUITPY mount point"""
    for mount_point in CIRCUITPY_MOUNT_POINTS:
        if os.path.exists(mount_point):
            # Verify it's actually a CircuitPython device
            boot_out = os.path.join(mount_point, "boot_out.txt")
            if os.path.exists(boot_out):
                return mount_point
    return None


def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    if not os.path.exists(filepath):
        return None

    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()


def check_file_status(source_file, dest_file):
    """
    Check if file needs to be synced.
    Returns: 'missing', 'outdated', 'same', or 'newer'
    """
    if not os.path.exists(dest_file):
        return 'missing'

    source_hash = get_file_hash(source_file)
    dest_hash = get_file_hash(dest_file)

    if source_hash == dest_hash:
        return 'same'

    # Compare modification times
    source_mtime = os.path.getmtime(source_file)
    dest_mtime = os.path.getmtime(dest_file)

    if source_mtime > dest_mtime:
        return 'outdated'
    else:
        return 'newer'


def sync_files(circuitpy_path, force=False, dry_run=False):
    """
    Sync files to CIRCUITPY drive.
    Returns: (success_count, skip_count, error_count)
    """
    success_count = 0
    skip_count = 0
    error_count = 0

    print_info(f"Syncing to: {circuitpy_path}")
    print()

    # Combine required and optional files
    all_files = {**FILES_TO_SYNC, **OPTIONAL_FILES}

    for source_name, dest_name in all_files.items():
        source_path = PROJECT_DIR / source_name
        dest_path = Path(circuitpy_path) / dest_name

        # Check if source exists
        if not source_path.exists():
            if source_name in OPTIONAL_FILES:
                print_warning(f"Optional file not found: {source_name} (skipping)")
                skip_count += 1
                continue
            else:
                print_error(f"Required file not found: {source_name}")
                error_count += 1
                continue

        # Check file status
        status = check_file_status(source_path, dest_path)

        if status == 'same' and not force:
            print(f"  {source_name:30} → {Colors.OKBLUE}Up to date{Colors.ENDC}")
            skip_count += 1
            continue

        if status == 'newer' and not force:
            print(f"  {source_name:30} → {Colors.WARNING}Device version newer (skipping){Colors.ENDC}")
            skip_count += 1
            continue

        # Copy file
        action = "Would copy" if dry_run else "Copying"
        if status == 'missing':
            print(f"  {source_name:30} → {Colors.OKGREEN}{action} (missing){Colors.ENDC}")
        elif status == 'outdated':
            print(f"  {source_name:30} → {Colors.WARNING}{action} (outdated){Colors.ENDC}")
        elif force:
            print(f"  {source_name:30} → {Colors.OKCYAN}{action} (forced){Colors.ENDC}")

        if not dry_run:
            try:
                # Create destination directory if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(source_path, dest_path)
                success_count += 1
            except Exception as e:
                print_error(f"Failed to copy {source_name}: {e}")
                error_count += 1
        else:
            success_count += 1

    return success_count, skip_count, error_count


def check_installation(circuitpy_path):
    """Check what files are missing or outdated"""
    print_header("Installation Check")

    missing = []
    outdated = []
    up_to_date = []

    for source_name, dest_name in FILES_TO_SYNC.items():
        source_path = PROJECT_DIR / source_name
        dest_path = Path(circuitpy_path) / dest_name

        if not source_path.exists():
            print_error(f"{source_name} not found in project directory!")
            continue

        status = check_file_status(source_path, dest_path)

        if status == 'missing':
            missing.append(source_name)
            print_error(f"Missing: {source_name}")
        elif status == 'outdated':
            outdated.append(source_name)
            print_warning(f"Outdated: {source_name}")
        elif status == 'same':
            up_to_date.append(source_name)
            print_success(f"Up to date: {source_name}")

    print()
    print(f"Summary: {len(up_to_date)} up to date, {len(outdated)} outdated, {len(missing)} missing")

    return len(missing) == 0 and len(outdated) == 0


def install(force=False, dry_run=False):
    """Main installation function"""
    print_header("MIDI Arpeggiator - Auto-Installer")

    # Find CIRCUITPY drive
    print_info("Searching for CIRCUITPY drive...")
    circuitpy_path = find_circuitpy()

    if not circuitpy_path:
        print_error("CIRCUITPY drive not found!")
        print()
        print("Please check:")
        print("  1. Feather board is connected via USB")
        print("  2. CircuitPython is installed on the board")
        print("  3. Drive is mounted (check Finder/Explorer)")
        print()
        return False

    print_success(f"Found CIRCUITPY at: {circuitpy_path}")
    print()

    # Read boot_out.txt for device info
    boot_out = Path(circuitpy_path) / "boot_out.txt"
    if boot_out.exists():
        with open(boot_out, 'r') as f:
            boot_info = f.read().strip()
            print_info(f"Device: {boot_info}")
            print()

    # Sync files
    if dry_run:
        print_info("DRY RUN MODE - No files will be copied")
        print()

    success, skipped, errors = sync_files(circuitpy_path, force=force, dry_run=dry_run)

    # Summary
    print()
    print_header("Installation Summary")

    if not dry_run:
        if success > 0:
            print_success(f"Copied {success} file(s)")
        if skipped > 0:
            print_info(f"Skipped {skipped} file(s)")
        if errors > 0:
            print_error(f"Failed {errors} file(s)")
    else:
        print_info(f"Would copy {success} file(s), skip {skipped} file(s)")

    print()

    if errors == 0:
        if not dry_run:
            print_success("Installation complete!")
            print()
            print("Next steps:")
            print("  1. Board will auto-restart")
            print("  2. Connect to serial console:")
            print(f"     screen /dev/tty.usbmodem* 115200")
            print("  3. Type 'help' to see test commands")
        return True
    else:
        print_error("Installation completed with errors")
        return False


def watch_mode():
    """Watch for CIRCUITPY drive and auto-install when detected"""
    print_header("Watch Mode - Auto-Install on Connect")
    print_info("Monitoring for CIRCUITPY drive...")
    print_info("Press Ctrl+C to exit")
    print()

    last_state = None

    try:
        while True:
            circuitpy_path = find_circuitpy()
            current_state = circuitpy_path is not None

            # State changed: disconnected → connected
            if current_state and not last_state:
                print()
                print_success("CIRCUITPY connected!")
                print()
                install(force=False, dry_run=False)
                print()
                print_info("Monitoring for next connection...")

            # State changed: connected → disconnected
            elif not current_state and last_state:
                print_warning("CIRCUITPY disconnected")

            last_state = current_state
            time.sleep(2)  # Check every 2 seconds

    except KeyboardInterrupt:
        print()
        print_info("Watch mode stopped")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="MIDI Arpeggiator Auto-Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 install.py              # Install missing files
  python3 install.py --force      # Reinstall all files
  python3 install.py --check      # Check installation status
  python3 install.py --watch      # Auto-install when board connects
        """
    )

    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force reinstall all files'
    )

    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='Check installation status without copying'
    )

    parser.add_argument(
        '--watch', '-w',
        action='store_true',
        help='Watch mode - auto-install when board connects'
    )

    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be copied without copying'
    )

    args = parser.parse_args()

    try:
        if args.watch:
            watch_mode()
        elif args.check:
            circuitpy_path = find_circuitpy()
            if circuitpy_path:
                check_installation(circuitpy_path)
            else:
                print_error("CIRCUITPY drive not found!")
                sys.exit(1)
        else:
            success = install(force=args.force, dry_run=args.dry_run)
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print()
        print_info("Cancelled by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
