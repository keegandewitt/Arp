#!/usr/bin/env python3
"""
Clean Serial Monitor Utility
Kills existing serial connections and provides clean monitoring
"""

import serial
import time
import sys
import subprocess
import signal

SERIAL_PORT = '/dev/tty.usbmodem1143101'
BAUD_RATE = 115200

def cleanup_serial_connections():
    """Kill any existing processes using the serial port"""
    print("Cleaning up existing serial connections...")
    try:
        # Kill any python processes using the serial port
        subprocess.run(
            f"ps aux | grep '{SERIAL_PORT}' | grep -v grep | awk '{{print $2}}' | xargs kill -9 2>/dev/null",
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

def monitor_serial(duration=None, reload=False):
    """
    Monitor serial output cleanly

    Args:
        duration: Seconds to monitor (None = indefinite)
        reload: Whether to trigger reload first
    """
    cleanup_serial_connections()

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(0.5)

        if reload:
            trigger_reload(ser)

        print("=== Serial Monitor Started ===")
        print(f"Port: {SERIAL_PORT} @ {BAUD_RATE} baud")
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

    args = parser.parse_args()

    monitor_serial(duration=args.duration, reload=args.reload)
