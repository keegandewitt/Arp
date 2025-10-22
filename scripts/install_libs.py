#!/usr/bin/env python3
"""
CircuitPython Library Installation Helper
Automatically downloads and installs required libraries for the MIDI Arpeggiator

Usage:
    python3 install_libs.py [OPTIONS]

Options:
    --bundle-path PATH    Path to downloaded CircuitPython bundle (if already downloaded)
    --circuitpy-path PATH Path to CIRCUITPY drive (auto-detected if not specified)
    --download            Download the latest bundle automatically
    --help                Show this help message
"""

import os
import sys
import argparse
import shutil
import zipfile
import urllib.request
from pathlib import Path

# Required libraries for this project
REQUIRED_LIBS = [
    {"type": "folder", "name": "adafruit_midi"},
    {"type": "file", "name": "adafruit_displayio_ssd1306.mpy"},
    {"type": "folder", "name": "adafruit_display_text"},
]

# CircuitPython bundle URL (version 10.x)
BUNDLE_URL = "https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest/download/adafruit-circuitpython-bundle-10.x-mpy-latest.zip"


def find_circuitpy_drive():
    """Auto-detect CIRCUITPY drive on macOS, Linux, or Windows"""
    possible_paths = [
        "/Volumes/CIRCUITPY",  # macOS
        "/media/*/CIRCUITPY",  # Linux
        "D:/",  # Windows (common)
        "E:/",  # Windows (common)
        "F:/",  # Windows (common)
    ]

    for path_pattern in possible_paths:
        if "*" in path_pattern:
            # Handle wildcard paths (Linux)
            import glob
            matches = glob.glob(path_pattern)
            if matches:
                return Path(matches[0])
        else:
            path = Path(path_pattern)
            if path.exists():
                # Verify it's actually CIRCUITPY by checking for boot_out.txt
                boot_file = path / "boot_out.txt"
                if boot_file.exists():
                    return path

    return None


def download_bundle(download_dir):
    """Download the latest CircuitPython bundle"""
    print(f"📥 Downloading CircuitPython bundle from GitHub...")
    print(f"   URL: {BUNDLE_URL}")

    zip_path = download_dir / "circuitpython_bundle.zip"

    try:
        urllib.request.urlretrieve(BUNDLE_URL, zip_path)
        print(f"✓ Downloaded to: {zip_path}")
        return zip_path
    except Exception as e:
        print(f"✗ Failed to download bundle: {e}")
        print("\nPlease download manually from:")
        print("https://circuitpython.org/libraries")
        return None


def extract_bundle(zip_path, extract_dir):
    """Extract the CircuitPython bundle"""
    print(f"\n📦 Extracting bundle...")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Find the lib folder in extracted contents
        for root, dirs, files in os.walk(extract_dir):
            if 'lib' in dirs:
                lib_path = Path(root) / 'lib'
                print(f"✓ Found library folder: {lib_path}")
                return lib_path

        print("✗ Could not find 'lib' folder in bundle")
        return None

    except Exception as e:
        print(f"✗ Failed to extract bundle: {e}")
        return None


def copy_libraries(bundle_lib_path, circuitpy_path):
    """Copy required libraries from bundle to CIRCUITPY"""
    dest_lib = circuitpy_path / "lib"

    # Create lib folder if it doesn't exist
    dest_lib.mkdir(exist_ok=True)

    print(f"\n📚 Installing libraries to: {dest_lib}")
    print("-" * 60)

    success_count = 0

    for lib in REQUIRED_LIBS:
        lib_name = lib["name"]
        lib_type = lib["type"]
        source = bundle_lib_path / lib_name
        dest = dest_lib / lib_name

        print(f"\n  {lib_name}:")

        if not source.exists():
            print(f"    ✗ Not found in bundle: {source}")
            continue

        try:
            if dest.exists():
                print(f"    ⚠ Already exists, removing old version...")
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()

            if lib_type == "folder":
                shutil.copytree(source, dest)
                print(f"    ✓ Copied folder ({count_files(dest)} files)")
            else:
                shutil.copy2(source, dest)
                size_kb = dest.stat().st_size / 1024
                print(f"    ✓ Copied file ({size_kb:.1f} KB)")

            success_count += 1

        except Exception as e:
            print(f"    ✗ Failed to copy: {e}")

    print("\n" + "-" * 60)
    print(f"✓ Successfully installed {success_count}/{len(REQUIRED_LIBS)} libraries")

    return success_count == len(REQUIRED_LIBS)


def count_files(directory):
    """Count files in a directory recursively"""
    return sum(1 for _, _, files in os.walk(directory) for _ in files)


def verify_installation(circuitpy_path):
    """Verify all required libraries are installed"""
    print("\n🔍 Verifying installation...")
    lib_path = circuitpy_path / "lib"

    all_present = True
    for lib in REQUIRED_LIBS:
        lib_name = lib["name"]
        path = lib_path / lib_name

        if path.exists():
            print(f"  ✓ {lib_name}")
        else:
            print(f"  ✗ {lib_name} - MISSING")
            all_present = False

    return all_present


def main():
    parser = argparse.ArgumentParser(
        description="Install CircuitPython libraries for MIDI Arpeggiator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bundle-path", type=Path, help="Path to CircuitPython bundle")
    parser.add_argument("--circuitpy-path", type=Path, help="Path to CIRCUITPY drive")
    parser.add_argument("--download", action="store_true", help="Download latest bundle")

    args = parser.parse_args()

    print("=" * 60)
    print("CircuitPython MIDI Arpeggiator - Library Installer")
    print("=" * 60)

    # Find CIRCUITPY drive
    if args.circuitpy_path:
        circuitpy_path = args.circuitpy_path
    else:
        print("\n🔍 Auto-detecting CIRCUITPY drive...")
        circuitpy_path = find_circuitpy_drive()

    if not circuitpy_path or not circuitpy_path.exists():
        print("✗ CIRCUITPY drive not found!")
        print("\nPlease ensure:")
        print("  1. Your M4 Express board is connected via USB")
        print("  2. CircuitPython is installed on the board")
        print("  3. The CIRCUITPY drive is mounted")
        print("\nOr specify the path manually with --circuitpy-path")
        return 1

    print(f"✓ Found CIRCUITPY at: {circuitpy_path}")

    # Get bundle path
    bundle_lib_path = None

    if args.download:
        # Download bundle
        download_dir = Path.home() / "Downloads"
        zip_path = download_bundle(download_dir)
        if not zip_path:
            return 1

        extract_dir = download_dir / "circuitpython_bundle"
        extract_dir.mkdir(exist_ok=True)
        bundle_lib_path = extract_bundle(zip_path, extract_dir)

    elif args.bundle_path:
        # Use provided bundle path
        if args.bundle_path.is_dir():
            bundle_lib_path = args.bundle_path / "lib"
        else:
            # Assume it's a zip file
            extract_dir = args.bundle_path.parent / "extracted_bundle"
            extract_dir.mkdir(exist_ok=True)
            bundle_lib_path = extract_bundle(args.bundle_path, extract_dir)

    else:
        # Look for bundle in common locations
        print("\n🔍 Looking for CircuitPython bundle...")
        common_locations = [
            Path.home() / "Downloads" / "adafruit-circuitpython-bundle-10.x-mpy-*" / "lib",
            Path.home() / "Downloads" / "circuitpython_bundle" / "*" / "lib",
        ]

        import glob
        for pattern in common_locations:
            matches = glob.glob(str(pattern))
            if matches:
                bundle_lib_path = Path(matches[0])
                print(f"✓ Found bundle at: {bundle_lib_path.parent}")
                break

        if not bundle_lib_path:
            print("✗ CircuitPython bundle not found")
            print("\nPlease either:")
            print("  1. Download with: python3 install_libs.py --download")
            print("  2. Specify path: python3 install_libs.py --bundle-path /path/to/bundle")
            print("  3. Download manually from: https://circuitpython.org/libraries")
            return 1

    if not bundle_lib_path or not bundle_lib_path.exists():
        print("✗ Could not locate bundle library folder")
        return 1

    # Copy libraries
    if not copy_libraries(bundle_lib_path, circuitpy_path):
        print("\n⚠ Some libraries failed to install")
        return 1

    # Verify installation
    if verify_installation(circuitpy_path):
        print("\n" + "=" * 60)
        print("✓ Installation complete! All libraries installed successfully.")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Copy project .py files to CIRCUITPY drive")
        print("  2. Reset your board or run: 'test m4 to oled'")
        print("\nSee INSTALL.md for detailed setup instructions.")
        return 0
    else:
        print("\n✗ Installation verification failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
