#!/usr/bin/env python3
"""
CircuitPython Dependency Checker

Checks if required CircuitPython libraries are installed on a connected device.
Can auto-install missing libraries via circup.

Usage:
    python3 scripts/check_dependencies.py <library1> <library2> ...
    python3 scripts/check_dependencies.py --file requirements_circuitpy.txt
    python3 scripts/check_dependencies.py --auto-install neopixel adafruit_midi

Examples:
    # Check if neopixel is installed
    python3 scripts/check_dependencies.py neopixel

    # Check multiple libraries
    python3 scripts/check_dependencies.py neopixel adafruit_midi

    # Auto-install if missing
    python3 scripts/check_dependencies.py --auto-install neopixel adafruit_midi

    # Read from requirements file
    python3 scripts/check_dependencies.py --file requirements_circuitpy.txt
"""

import sys
import subprocess
import argparse
from pathlib import Path

# CIRCUITPY mount point (macOS default)
CIRCUITPY_PATH = Path("/Volumes/CIRCUITPY")

# Find circup command
def find_circup():
    """Find circup executable."""
    # Check common locations
    locations = [
        "circup",  # In PATH
        Path.home() / "Library/Python/3.9/bin/circup",  # macOS user install
        "/usr/local/bin/circup",  # Homebrew install
    ]

    for loc in locations:
        try:
            result = subprocess.run(
                [str(loc), "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return str(loc)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return None


def check_circuitpy_connected():
    """Check if CIRCUITPY drive is mounted."""
    if not CIRCUITPY_PATH.exists():
        print(f"❌ CIRCUITPY drive not found at {CIRCUITPY_PATH}")
        print("\nTroubleshooting:")
        print("  1. Connect your CircuitPython device via USB")
        print("  2. Wait for CIRCUITPY drive to mount (~2-3 seconds)")
        print("  3. If it doesn't appear, press RESET button on device")
        print("  4. Check 'ls /Volumes/' to see all mounted drives")
        return False
    return True


def get_installed_libraries(circup_path):
    """Get list of installed libraries from device."""
    try:
        result = subprocess.run(
            [circup_path, "list"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"⚠ Warning: circup list returned error: {result.stderr}")
            return []

        # Parse circup list output (format: "library_name")
        installed = []
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith("Found device"):
                # Extract library name (first word)
                lib_name = line.split()[0]
                installed.append(lib_name)

        return installed

    except subprocess.TimeoutExpired:
        print("⚠ Warning: circup list timed out")
        return []
    except Exception as e:
        print(f"⚠ Warning: Error checking installed libraries: {e}")
        return []


def install_library(circup_path, library):
    """Install a library using circup."""
    print(f"  Installing {library}...")
    try:
        result = subprocess.run(
            [circup_path, "install", library],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print(f"    ✓ {library} installed successfully")
            return True
        else:
            print(f"    ✗ Failed to install {library}")
            print(f"       Error: {result.stderr.strip()}")
            return False

    except subprocess.TimeoutExpired:
        print(f"    ✗ Installation of {library} timed out")
        return False
    except Exception as e:
        print(f"    ✗ Error installing {library}: {e}")
        return False


def check_dependencies(libraries, auto_install=False):
    """Check if required libraries are installed."""

    # Check if device is connected
    if not check_circuitpy_connected():
        return False

    # Find circup
    circup_path = find_circup()
    if not circup_path:
        print("❌ circup not found")
        print("\nTo install circup:")
        print("  pip3 install --upgrade circup")
        print("\nOr add to PATH if already installed:")
        print("  export PATH=\"$HOME/Library/Python/3.9/bin:$PATH\"")
        return False

    print(f"✓ Found circup: {circup_path}\n")

    # Get installed libraries
    print("Checking installed libraries...")
    installed = get_installed_libraries(circup_path)

    # Check each required library
    missing = []
    for lib in libraries:
        if lib in installed:
            print(f"  ✓ {lib} (installed)")
        else:
            print(f"  ✗ {lib} (missing)")
            missing.append(lib)

    # Handle missing libraries
    if not missing:
        print("\n✓ All required libraries are installed")
        return True

    print(f"\n⚠ Missing libraries: {', '.join(missing)}")

    if auto_install:
        print("\nInstalling missing libraries...")
        all_success = True
        for lib in missing:
            success = install_library(circup_path, lib)
            if not success:
                all_success = False

        if all_success:
            print("\n✓ All missing libraries installed successfully")
            return True
        else:
            print("\n✗ Some libraries failed to install")
            return False
    else:
        print("\nTo install missing libraries:")
        print(f"  circup install {' '.join(missing)}")
        print("\nOr run with --auto-install flag:")
        print(f"  {' '.join(sys.argv)} --auto-install")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Check CircuitPython library dependencies"
    )
    parser.add_argument(
        "libraries",
        nargs="*",
        help="Libraries to check (e.g., neopixel adafruit_midi)"
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Read library list from file (one per line)"
    )
    parser.add_argument(
        "--auto-install",
        "-i",
        action="store_true",
        help="Automatically install missing libraries"
    )

    args = parser.parse_args()

    # Get library list
    libraries = list(args.libraries)

    if args.file:
        # Read from file
        try:
            with open(args.file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        libraries.append(line)
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            return 1

    if not libraries:
        parser.print_help()
        print("\nError: No libraries specified")
        return 1

    print("=" * 70)
    print("CircuitPython Dependency Checker")
    print("=" * 70)
    print(f"\nRequired libraries: {', '.join(libraries)}\n")

    success = check_dependencies(libraries, auto_install=args.auto_install)

    if success:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
