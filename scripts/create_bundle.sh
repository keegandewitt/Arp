#!/bin/bash
#
# Arp Firmware Bundle Creator
#
# Creates a firmware bundle (.arpfw file) containing:
# - main.py (source code)
# - arp/ directory (core modules)
# - lib/ directory (required CircuitPython libraries)
# - manifest.json (version info, checksums)
# - CHANGELOG.md (user-facing changes)
#
# Usage:
#   ./scripts/create_bundle.sh [version]
#
# Example:
#   ./scripts/create_bundle.sh 1.0.0
#

set -e  # Exit on error

# Get version from command line or extract from main.py
if [ -n "$1" ]; then
    VERSION="$1"
else
    # Extract version from main.py
    VERSION=$(grep '^__version__ = ' main.py | cut -d'"' -f2)
    if [ -z "$VERSION" ]; then
        echo "Error: Could not extract version from main.py"
        echo "Usage: $0 [version]"
        exit 1
    fi
fi

BUILD_DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="arp-firmware-v${VERSION}.arpfw"
TEMP_DIR="arp-firmware-v${VERSION}"

echo "=================================================="
echo "Arp Firmware Bundle Creator"
echo "=================================================="
echo "Version: ${VERSION}"
echo "Build Date: ${BUILD_DATE}"
echo "Output: ${OUTPUT_FILE}"
echo ""

# Create temporary directory
echo "[1/5] Creating temporary directory..."
rm -rf "${TEMP_DIR}"
mkdir -p "${TEMP_DIR}"

# Copy main.py
echo "[2/5] Copying main.py..."
cp main.py "${TEMP_DIR}/"

# Copy arp/ directory
echo "[3/5] Copying arp/ modules..."
if [ -d "arp" ]; then
    cp -r arp "${TEMP_DIR}/"
else
    echo "Warning: arp/ directory not found (may not exist yet)"
fi

# Copy lib/ directory from device (if mounted)
echo "[4/5] Copying libraries..."
if [ -d "/Volumes/CIRCUITPY/lib" ]; then
    cp -r /Volumes/CIRCUITPY/lib "${TEMP_DIR}/"
    echo "      ✓ Copied from /Volumes/CIRCUITPY/lib"
else
    echo "Warning: /Volumes/CIRCUITPY not mounted - bundle will not include libraries"
    echo "         Connect device to include libraries in bundle"
fi

# Create manifest.json
echo "[5/5] Creating manifest.json..."
cat > "${TEMP_DIR}/manifest.json" << EOF
{
  "version": "${VERSION}",
  "build_date": "${BUILD_DATE}",
  "circuitpython_version": "10.0.3",
  "hardware": ["feather_m4_can"],
  "description": "Arp Hardware Arpeggiator Firmware",
  "files": {
    "main.py": "Main entry point (deploys as code.py)",
    "arp/": "Core modules",
    "lib/": "Required CircuitPython libraries"
  },
  "required_libraries": [
    "adafruit_midi",
    "adafruit_displayio_sh1107",
    "adafruit_display_text",
    "adafruit_debouncer"
  ]
}
EOF

# Copy or create CHANGELOG.md
if [ -f "CHANGELOG.md" ]; then
    cp CHANGELOG.md "${TEMP_DIR}/"
else
    echo "Creating placeholder CHANGELOG.md..."
    cat > "${TEMP_DIR}/CHANGELOG.md" << EOF
# Changelog

## v${VERSION} (${BUILD_DATE})

- Firmware bundle created
- See git history for detailed changes

EOF
fi

# Create zip archive
echo ""
echo "Creating bundle archive..."
rm -f "${OUTPUT_FILE}"
cd "${TEMP_DIR}"
zip -r "../${OUTPUT_FILE}" . > /dev/null
cd ..

# Cleanup
echo "Cleaning up temporary files..."
rm -rf "${TEMP_DIR}"

# Show result
FILE_SIZE=$(ls -lh "${OUTPUT_FILE}" | awk '{print $5}')
echo ""
echo "=================================================="
echo "✓ Bundle created successfully!"
echo "=================================================="
echo "File: ${OUTPUT_FILE}"
echo "Size: ${FILE_SIZE}"
echo ""
echo "To deploy this bundle:"
echo "  1. Extract the .arpfw file (it's a zip)"
echo "  2. Copy main.py to /Volumes/CIRCUITPY/code.py"
echo "  3. Copy arp/ to /Volumes/CIRCUITPY/arp/"
echo "  4. Copy lib/ to /Volumes/CIRCUITPY/lib/"
echo ""
echo "Or use the Arp Firmware Updater app (coming soon)"
echo "=================================================="
