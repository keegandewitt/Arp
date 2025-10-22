#!/bin/bash
# Deploy comprehensive pin test to Feather M4
#
# This script:
# 1. Checks for CIRCUITPY mount
# 2. Verifies and installs required dependencies
# 3. Backs up existing code.py
# 4. Deploys the pin test

set -e

CIRCUITPY="/Volumes/CIRCUITPY"
TEST_FILE="tests/comprehensive_pin_test.py"
REQUIRED_LIBS=("neopixel")

# Find circup (may be in user Python bin)
CIRCUP=""
if command -v circup &> /dev/null; then
    CIRCUP="circup"
elif [ -f "$HOME/Library/Python/3.9/bin/circup" ]; then
    CIRCUP="$HOME/Library/Python/3.9/bin/circup"
elif [ -f "/usr/local/bin/circup" ]; then
    CIRCUP="/usr/local/bin/circup"
fi

echo "==================================================================="
echo "Deploy Comprehensive Pin Test to Feather M4"
echo "==================================================================="
echo ""

# Check if CIRCUITPY is mounted
if [ ! -d "$CIRCUITPY" ]; then
    echo "❌ CIRCUITPY drive not found at $CIRCUITPY"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Connect Feather M4 via USB"
    echo "  2. Wait for CIRCUITPY drive to mount"
    echo "  3. If it doesn't appear, double-tap RESET button"
    echo "  4. Check 'ls /Volumes/' to see mounted drives"
    exit 1
fi

echo "✓ CIRCUITPY drive found"

# Check if test file exists
if [ ! -f "$TEST_FILE" ]; then
    echo "❌ Test file not found: $TEST_FILE"
    exit 1
fi

echo "✓ Test file found: $TEST_FILE"
echo ""

# Check for circup
echo "-------------------------------------------------------------------"
echo "STEP 1: Dependency Check"
echo "-------------------------------------------------------------------"

if [ -z "$CIRCUP" ]; then
    echo "⚠ circup not found - cannot auto-install dependencies"
    echo ""
    echo "To install circup:"
    echo "  pip3 install --upgrade circup"
    echo ""
    echo "Required libraries for this test:"
    for lib in "${REQUIRED_LIBS[@]}"; do
        echo "  - $lib"
    done
    echo ""
    read -p "Continue without dependency check? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
else
    echo "✓ Found circup: $CIRCUP"
    echo ""

    # Check installed libraries
    echo "Checking installed libraries..."
    INSTALLED=$($CIRCUP list 2>/dev/null || echo "")

    MISSING_LIBS=()
    for lib in "${REQUIRED_LIBS[@]}"; do
        if echo "$INSTALLED" | grep -q "^$lib"; then
            echo "  ✓ $lib (installed)"
        else
            echo "  ✗ $lib (missing)"
            MISSING_LIBS+=("$lib")
        fi
    done

    # Install missing libraries
    if [ ${#MISSING_LIBS[@]} -gt 0 ]; then
        echo ""
        echo "Missing libraries: ${MISSING_LIBS[*]}"
        echo "Installing missing dependencies..."

        for lib in "${MISSING_LIBS[@]}"; do
            echo "  Installing $lib..."
            $CIRCUP install "$lib"
            if [ $? -eq 0 ]; then
                echo "    ✓ $lib installed"
            else
                echo "    ✗ Failed to install $lib"
                exit 1
            fi
        done

        echo ""
        echo "✓ All dependencies installed"
    else
        echo ""
        echo "✓ All dependencies already installed"
    fi
fi

echo ""
echo "-------------------------------------------------------------------"
echo "STEP 2: Deploy Test Script"
echo "-------------------------------------------------------------------"
echo ""

# Backup existing code.py if it exists
if [ -f "$CIRCUITPY/code.py" ]; then
    BACKUP_NAME="code_backup_$(date +%Y%m%d_%H%M%S).py"
    echo "📦 Backing up existing code.py to $BACKUP_NAME"
    cp "$CIRCUITPY/code.py" "$CIRCUITPY/$BACKUP_NAME"
fi

# Copy test file as code.py
echo "📋 Copying pin test to CIRCUITPY/code.py"
cp "$TEST_FILE" "$CIRCUITPY/code.py"

echo ""
echo "✓ Pin test deployed successfully!"
echo ""
echo "-------------------------------------------------------------------"
echo "The M4 will auto-reload and start the test in ~2 seconds."
echo ""
echo "To view test output:"
echo "  ./scripts/monitor_m4.sh"
echo ""
echo "To restore your original code:"
echo "  cp $CIRCUITPY/code_backup_*.py $CIRCUITPY/code.py"
echo "-------------------------------------------------------------------"
echo ""
