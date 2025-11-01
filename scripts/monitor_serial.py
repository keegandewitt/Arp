#!/usr/bin/env python3
"""
Clean Serial Monitor Utility
Kills existing serial connections and provides clean monitoring
Automatically detects CircuitPython devices
"""

import serial
import serial.tools.list_ports
import time
import sys
import subprocess
import signal

BAUD_RATE = 115200

def find_circuitpython_port():
    """
    Automatically detect CircuitPython device port

    Returns:
        str: Serial port path or None if not found
    """
    # Look for CircuitPython devices by checking:
    # 1. Product description contains "CircuitPython" or "Adafruit"
    # 2. Common vendor IDs for Adafruit boards (0x239A)
    # 3. Port name patterns (tty.usbmodem*)

    ports = serial.tools.list_ports.comports()

    # First pass: Look for explicit CircuitPython/Adafruit devices
    for port in ports:
        description = port.description.lower() if port.description else ""
        product = port.product.lower() if port.product else ""
        manufacturer = port.manufacturer.lower() if port.manufacturer else ""

        # Check for Adafruit vendor ID (0x239A)
        if port.vid == 0x239A:
            print(f"✓ Found Adafruit device: {port.device}")
            print(f"  Description: {port.description}")
            return port.device

        # Check for CircuitPython in description/product
        if "circuitpython" in description or "circuitpython" in product:
            print(f"✓ Found CircuitPython device: {port.device}")
            print(f"  Description: {port.description}")
            return port.device

        # Check for Adafruit in manufacturer
        if "adafruit" in manufacturer:
            print(f"✓ Found Adafruit device: {port.device}")
            print(f"  Description: {port.description}")
            return port.device

    # Second pass: Look for typical USB modem ports
    usb_modems = [p for p in ports if 'usbmodem' in p.device.lower()]
    if len(usb_modems) == 1:
        port = usb_modems[0]
        print(f"✓ Found USB modem device: {port.device}")
        print(f"  Description: {port.description}")
        return port.device
    elif len(usb_modems) > 1:
        print("⚠ Multiple USB modem devices found:")
        for i, port in enumerate(usb_modems, 1):
            print(f"  {i}. {port.device} - {port.description}")
        return usb_modems[0].device  # Use first one as default

    return None

def cleanup_serial_connections(port):
    """Kill any existing processes using the serial port"""
    if not port:
        return

    print("Cleaning up existing serial connections...")
    try:
        # Kill any python processes using the serial port
        subprocess.run(
            f"ps aux | grep '{port}' | grep -v grep | awk '{{print $2}}' | xargs kill -9 2>/dev/null",
            shell=True,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.5)
        print("✓ Cleanup complete")
    except Exception as e:
        print(f"Cleanup warning: {e}")

def trigger_reload(ser):
    """Send CTRL+D to trigger code reload"""
    print("Triggering code reload (CTRL+D)...")
    ser.write(b'\x04')
    time.sleep(1.5)
    # Clear any buffered data
    if ser.in_waiting:
        ser.read(ser.in_waiting)
    print("✓ Reload triggered\n")

def monitor_serial(duration=None, reload=False, port=None):
    """
    Monitor serial output cleanly

    Args:
        duration: Seconds to monitor (None = indefinite)
        reload: Whether to trigger reload first
        port: Specific port to use (None = auto-detect)
    """
    # Auto-detect port if not specified
    if not port:
        print("Detecting CircuitPython device...")
        port = find_circuitpython_port()

        if not port:
            print("\n✗ No CircuitPython device found!")
            print("\nTroubleshooting:")
            print("  1. Check USB cable is connected")
            print("  2. Check CIRCUITPY drive is mounted: ls /Volumes/CIRCUITPY")
            print("  3. List all serial ports: ls /dev/tty.usb*")
            print("  4. Specify port manually: --port /dev/tty.usbmodemXXXX")
            sys.exit(1)
        print()

    cleanup_serial_connections(port)

    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        time.sleep(0.5)

        if reload:
            trigger_reload(ser)

        print("=== Serial Monitor Started ===")
        print(f"Port: {port} @ {BAUD_RATE} baud")
        print("Press CTRL+C to stop\n")
        print("-" * 60)

        start_time = time.time()

        while True:
            if duration and (time.time() - start_time) > duration:
                break

            if ser.in_waiting:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                print(data, end='', flush=True)

            time.sleep(0.05)

        print("\n" + "-" * 60)
        print("=== Monitor Stopped ===")
        ser.close()

    except KeyboardInterrupt:
        print("\n" + "-" * 60)
        print("=== Monitor Stopped (CTRL+C) ===")
        if 'ser' in locals():
            ser.close()
    except Exception as e:
        print(f"\nError: {e}")
        if 'ser' in locals():
            ser.close()
        sys.exit(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Clean serial monitor for CircuitPython')
    parser.add_argument('-d', '--duration', type=int, help='Monitor duration in seconds')
    parser.add_argument('-r', '--reload', action='store_true', help='Trigger code reload first')
    parser.add_argument('-p', '--port', type=str, help='Specific serial port (auto-detect if not specified)')

    args = parser.parse_args()

    monitor_serial(duration=args.duration, reload=args.reload, port=args.port)
