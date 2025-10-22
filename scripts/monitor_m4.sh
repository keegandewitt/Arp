#!/bin/bash
# Monitor Feather M4 CAN Express via serial console
#
# Usage:
#   ./scripts/monitor_m4.sh           # Auto-detect and connect
#   ./scripts/monitor_m4.sh <device>  # Connect to specific device

set -e

echo "==================================================================="
echo "Feather M4 Serial Monitor"
echo "==================================================================="
echo ""

# Find the device
if [ -z "$1" ]; then
    echo "Searching for connected Feather M4..."
    DEVICE=$(ls /dev/tty.usbmodem* 2>/dev/null | head -n1)

    if [ -z "$DEVICE" ]; then
        echo "❌ No USB serial device found!"
        echo ""
        echo "Troubleshooting:"
        echo "  1. Ensure Feather M4 is connected via USB"
        echo "  2. Check if CircuitPython is installed"
        echo "  3. Try pressing the RESET button"
        echo "  4. Run 'ls /dev/tty.*' to see all devices"
        exit 1
    fi
else
    DEVICE="$1"
fi

echo "✓ Found device: $DEVICE"
echo ""

# Check if CIRCUITPY is mounted
if [ -d "/Volumes/CIRCUITPY" ]; then
    echo "✓ CIRCUITPY drive mounted at /Volumes/CIRCUITPY"
else
    echo "⚠ CIRCUITPY drive not found (board may be in bootloader mode)"
fi

echo ""
echo "Connecting to serial console..."
echo "-------------------------------------------------------------------"
echo "Tips:"
echo "  • Ctrl+C: Stop running code"
echo "  • Ctrl+D: Reload/restart CircuitPython"
echo "  • Ctrl+A then K: Exit screen (then press Y to confirm)"
echo "  • Type 'help()' in REPL for CircuitPython help"
echo "-------------------------------------------------------------------"
echo ""
echo "Press any key to connect..."
read -n 1 -s

# Connect via screen
screen "$DEVICE" 115200
