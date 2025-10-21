#!/usr/bin/env python3
"""
Project Backup Script for Arp

This script creates timestamped archives of the project and maintains
only the last 5 backups. It should be run BEFORE every git push operation.

Usage:
    python backup.py                    # Create timestamped backup
    python backup.py --milestone "name" # Create named milestone backup
"""

import os
import sys
import tarfile
import argparse
from datetime import datetime
from pathlib import Path

# Configuration
PROJECT_NAME = "Arp"
PROJECT_DIR = Path(__file__).parent.resolve()
BACKUP_DIR = Path.home() / "Cursor" / "_Backups"
MAX_BACKUPS = 5

# Files and directories to exclude from backup
EXCLUDE_PATTERNS = [
    '.git',
    '__pycache__',
    '*.pyc',
    '.DS_Store',
    'venv',
    '.venv',
    'env',
    '.env',
    '*.swp',
    '*.swo',
    '*~',
]


def should_exclude(path, base_path):
    """Check if a path should be excluded from backup."""
    rel_path = path.relative_to(base_path)

    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            # Extension matching
            if str(rel_path).endswith(pattern[1:]):
                return True
        else:
            # Directory or file name matching
            if pattern in rel_path.parts:
                return True

    return False


def create_backup(milestone_name=None):
    """Create a timestamped backup archive of the project."""

    # Ensure backup directory exists
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Generate backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if milestone_name:
        backup_filename = f"{PROJECT_NAME}_{timestamp}_milestone_{milestone_name}.tar.gz"
    else:
        backup_filename = f"{PROJECT_NAME}_{timestamp}.tar.gz"

    backup_path = BACKUP_DIR / backup_filename

    print(f"Creating backup: {backup_filename}")
    print(f"Source: {PROJECT_DIR}")
    print(f"Destination: {backup_path}")

    # Create tar.gz archive
    file_count = 0
    with tarfile.open(backup_path, "w:gz") as tar:
        for item in PROJECT_DIR.rglob("*"):
            if item.is_file() and not should_exclude(item, PROJECT_DIR):
                arcname = item.relative_to(PROJECT_DIR.parent)
                tar.add(item, arcname=arcname)
                file_count += 1
                if file_count % 10 == 0:
                    print(f"  Added {file_count} files...", end='\r')

    print(f"\nBackup complete: {file_count} files archived")
    print(f"Backup size: {backup_path.stat().st_size / 1024 / 1024:.2f} MB")

    return backup_path


def cleanup_old_backups():
    """Remove old backups, keeping only the last MAX_BACKUPS."""

    if not BACKUP_DIR.exists():
        return

    # Get all backup files for this project (excluding milestone backups)
    backup_files = sorted(
        [f for f in BACKUP_DIR.glob(f"{PROJECT_NAME}_*.tar.gz")
         if "_milestone_" not in f.name],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    # Remove old backups beyond MAX_BACKUPS
    if len(backup_files) > MAX_BACKUPS:
        print(f"\nCleaning up old backups (keeping last {MAX_BACKUPS})...")
        for old_backup in backup_files[MAX_BACKUPS:]:
            print(f"  Removing: {old_backup.name}")
            old_backup.unlink()
        print(f"Removed {len(backup_files) - MAX_BACKUPS} old backup(s)")
    else:
        print(f"\nCurrent backups: {len(backup_files)} (max: {MAX_BACKUPS})")


def list_backups():
    """List all available backups."""

    if not BACKUP_DIR.exists():
        print("No backups directory found.")
        return

    backup_files = sorted(
        BACKUP_DIR.glob(f"{PROJECT_NAME}_*.tar.gz"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if not backup_files:
        print("No backups found.")
        return

    print(f"\nAvailable backups in {BACKUP_DIR}:")
    print("-" * 80)
    for backup in backup_files:
        stat = backup.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime)
        size_mb = stat.st_size / 1024 / 1024
        is_milestone = "_milestone_" in backup.name
        marker = " [MILESTONE]" if is_milestone else ""
        print(f"{backup.name:60s} {size_mb:6.2f} MB  {mtime.strftime('%Y-%m-%d %H:%M:%S')}{marker}")
    print("-" * 80)
    print(f"Total: {len(backup_files)} backup(s)")


def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description="Create project backups before git operations"
    )
    parser.add_argument(
        '--milestone',
        type=str,
        help='Create a named milestone backup (will not be auto-deleted)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available backups'
    )

    args = parser.parse_args()

    if args.list:
        list_backups()
        return 0

    try:
        # Create backup
        backup_path = create_backup(milestone_name=args.milestone)

        # Cleanup old backups (unless this is a milestone)
        if not args.milestone:
            cleanup_old_backups()
        else:
            print("\nMilestone backup created (will not be auto-deleted)")

        print(f"\n✓ Backup successful: {backup_path.name}")
        return 0

    except Exception as e:
        print(f"\n✗ Backup failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
