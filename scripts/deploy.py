#!/usr/bin/env python3
"""
Arp - Deployment Script
=======================

CRITICAL: This script ensures main.py from the repository is always deployed as code.py on hardware.

The Problem:
- CircuitPython devices run code.py
- Our repository uses main.py
- Editing one without deploying causes version mismatches

The Solution:
- Always edit main.py in the repository
- This script syncs main.py -> code.py automatically
- Also syncs all arp/ modules

Usage:
    python3 scripts/deploy.py              # Deploy all files
    python3 scripts/deploy.py --check      # Check what needs updating
    python3 scripts/deploy.py --force      # Force overwrite all files
    python3 scripts/deploy.py --watch      # Watch for changes and auto-deploy

Required CircuitPython Libraries:
- See METHODOLOGY.md for complete list
"""

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime

# Color output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END}  {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.END}  {msg}")

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
CIRCUITPY_MOUNT = Path("/Volumes/CIRCUITPY")

# File mapping: {source: destination}
FILES_TO_DEPLOY = {
    # Main entry point: main.py -> code.py (CRITICAL!)
    "main.py": "code.py",

    # Boot configuration (runs before code.py)
    "boot.py": "boot.py",

    # Core modules
    "arp/core/clock.py": "arp/core/clock.py",

    # UI modules
    "arp/ui/display.py": "arp/ui/display.py",
    "arp/ui/buttons.py": "arp/ui/buttons.py",
    "arp/ui/menu.py": "arp/ui/menu.py",

    # Utils
    "arp/utils/config.py": "arp/utils/config.py",
}

def check_circuitpy_mounted():
    """Check if CIRCUITPY drive is mounted"""
    if not CIRCUITPY_MOUNT.exists():
        print_error(f"CIRCUITPY not found at {CIRCUITPY_MOUNT}")
        print_info("Please connect your Feather M4 via USB")
        return False
    return True

def get_file_hash(filepath):
    """Get SHA256 hash of a file"""
    if not filepath.exists():
        return None
    import hashlib
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        sha256.update(f.read())
    return sha256.hexdigest()

def needs_update(source_path, dest_path):
    """Check if destination needs updating"""
    if not dest_path.exists():
        return True, "missing"

    source_hash = get_file_hash(source_path)
    dest_hash = get_file_hash(dest_path)

    if source_hash != dest_hash:
        return True, "outdated"

    return False, "up-to-date"

def deploy_file(source_rel, dest_rel, force=False):
    """Deploy a single file"""
    source_path = PROJECT_ROOT / source_rel
    dest_path = CIRCUITPY_MOUNT / dest_rel

    if not source_path.exists():
        print_error(f"Source file not found: {source_rel}")
        return False

    # Create destination directory if needed
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if update needed
    needs_update_flag, reason = needs_update(source_path, dest_path)

    if not needs_update_flag and not force:
        print_info(f"Skipping {source_rel} (up-to-date)")
        return True

    # Copy file
    try:
        shutil.copy2(source_path, dest_path)
        if source_rel == "main.py":
            print_success(f"Deployed {Colors.BOLD}main.py → code.py{Colors.END} ({reason})")
        else:
            print_success(f"Deployed {source_rel} ({reason})")
        return True
    except Exception as e:
        print_error(f"Failed to deploy {source_rel}: {e}")
        return False

def deploy_all(force=False, check_only=False):
    """Deploy all files to hardware"""
    print(f"\n{Colors.BOLD}Arp Deployment{Colors.END}")
    print("=" * 60)

    if not check_circuitpy_mounted():
        return False

    print_info(f"Repository: {PROJECT_ROOT}")
    print_info(f"Target: {CIRCUITPY_MOUNT}")
    print()

    if check_only:
        print(f"{Colors.BOLD}Checking files...{Colors.END}")
        needs_deployment = []
        for source_rel, dest_rel in FILES_TO_DEPLOY.items():
            source_path = PROJECT_ROOT / source_rel
            dest_path = CIRCUITPY_MOUNT / dest_rel
            needs_update_flag, reason = needs_update(source_path, dest_path)

            if needs_update_flag:
                needs_deployment.append((source_rel, reason))
                print_warning(f"{source_rel} → {dest_rel} ({reason})")
            else:
                print_success(f"{source_rel} (up-to-date)")

        print()
        if needs_deployment:
            print_warning(f"{len(needs_deployment)} file(s) need deployment")
            print_info("Run 'python3 scripts/deploy.py' to deploy")
        else:
            print_success("All files are up-to-date!")
        return True

    # Deploy files
    print(f"{Colors.BOLD}Deploying files...{Colors.END}")
    success_count = 0
    fail_count = 0

    for source_rel, dest_rel in FILES_TO_DEPLOY.items():
        if deploy_file(source_rel, dest_rel, force=force):
            success_count += 1
        else:
            fail_count += 1

    print()
    print("=" * 60)
    if fail_count == 0:
        print_success(f"Deployment complete! ({success_count} files)")
        print_info("Device will auto-reload in a few seconds...")
    else:
        print_error(f"Deployment completed with errors: {success_count} succeeded, {fail_count} failed")
        return False

    return True

def watch_and_deploy():
    """Watch for file changes and auto-deploy"""
    print(f"\n{Colors.BOLD}Arp Deployment - Watch Mode{Colors.END}")
    print("=" * 60)
    print_info("Watching for changes... (Ctrl+C to stop)")
    print()

    last_hashes = {}

    # Get initial hashes
    for source_rel in FILES_TO_DEPLOY.keys():
        source_path = PROJECT_ROOT / source_rel
        if source_path.exists():
            last_hashes[source_rel] = get_file_hash(source_path)

    try:
        while True:
            time.sleep(2)  # Check every 2 seconds

            if not check_circuitpy_mounted():
                print_warning("CIRCUITPY unmounted, waiting...")
                time.sleep(5)
                continue

            # Check for changes
            changed_files = []
            for source_rel in FILES_TO_DEPLOY.keys():
                source_path = PROJECT_ROOT / source_rel
                if not source_path.exists():
                    continue

                current_hash = get_file_hash(source_path)
                if current_hash != last_hashes.get(source_rel):
                    changed_files.append(source_rel)
                    last_hashes[source_rel] = current_hash

            # Deploy changed files
            if changed_files:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Changes detected:")
                for source_rel in changed_files:
                    dest_rel = FILES_TO_DEPLOY[source_rel]
                    deploy_file(source_rel, dest_rel, force=True)
                print()

    except KeyboardInterrupt:
        print("\n")
        print_info("Watch mode stopped")

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Deploy Arp to CircuitPython hardware")
    parser.add_argument("--check", action="store_true", help="Check what needs deployment")
    parser.add_argument("--force", action="store_true", help="Force deploy all files")
    parser.add_argument("--watch", action="store_true", help="Watch for changes and auto-deploy")

    args = parser.parse_args()

    if args.watch:
        watch_and_deploy()
    else:
        success = deploy_all(force=args.force, check_only=args.check)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
