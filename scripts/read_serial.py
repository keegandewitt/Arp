#!/usr/bin/env python3
"""
Interactive Serial Monitor for CircuitPython devices

Features:
- Real-time serial output display
- Type commands to control the device
- No need for complex keyboard shortcuts

Commands:
    reset   - Send Ctrl+D to soft reload CircuitPython
    stop    - Send Ctrl+C to interrupt running code
    exit    - Close serial monitor and exit
    help    - Show available commands

Usage:
    python3 scripts/read_serial.py
"""

import serial
import sys
import time
import threading
import select

DEVICE = "/dev/tty.usbmodem1143101"
BAUDRATE = 115200

# Global flag for clean exit
running = True

def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print("Interactive CircuitPython Serial Monitor")
    print("=" * 70)
    print("\nConnected to:", DEVICE)
    print("Baudrate:", BAUDRATE)
    print("\nAvailable Commands:")
    print("  reset   - Soft reload CircuitPython (Ctrl+D)")
    print("  stop    - Interrupt running code (Ctrl+C)")
    print("  exit    - Close monitor and exit")
    print("  help    - Show this help message")
    print("\nType a command and press Enter, or just watch the output.")
    print("=" * 70)
    print()


def serial_reader(ser):
    """Thread function to read from serial port."""
    global running
    while running:
        try:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
                print(data, end='', flush=True)
            time.sleep(0.01)
        except Exception as e:
            if running:  # Only print error if we haven't intentionally stopped
                print(f"\n[Serial Read Error: {e}]")
            break


def process_command(ser, command):
    """Process user commands."""
    cmd = command.strip().lower()

    if cmd == "exit" or cmd == "quit":
        print("\n[Closing serial monitor...]")
        return False

    elif cmd == "reset" or cmd == "reload":
        print("\n[Sending soft reload (Ctrl+D)...]")
        ser.write(b'\x04')  # Ctrl+D
        time.sleep(0.1)

    elif cmd == "stop" or cmd == "interrupt":
        print("\n[Sending interrupt (Ctrl+C)...]")
        ser.write(b'\x03')  # Ctrl+C
        time.sleep(0.1)

    elif cmd == "help" or cmd == "?":
        print("\n--- Available Commands ---")
        print("  reset     - Soft reload CircuitPython (restarts code.py)")
        print("  stop      - Interrupt running code (stops execution)")
        print("  exit      - Close this monitor and exit")
        print("  help      - Show this help message")
        print("-" * 70 + "\n")

    elif cmd == "":
        # Empty command, just ignore
        pass

    else:
        # Send as literal text to REPL (for when in REPL mode)
        print(f"\n[Sending: {command}]")
        ser.write((command + '\r').encode('utf-8'))

    return True


def input_reader_unix(ser):
    """Read user input (Unix/macOS version using select)."""
    global running

    print("\n[Monitor started - type 'help' for commands or 'exit' to quit]\n")

    while running:
        # Use select to check if input is available (non-blocking)
        if select.select([sys.stdin], [], [], 0.1)[0]:
            try:
                command = sys.stdin.readline()
                if not process_command(ser, command):
                    running = False
                    break
            except EOFError:
                # Handle Ctrl+D from terminal
                running = False
                break
            except Exception as e:
                print(f"\n[Input Error: {e}]")
                running = False
                break


def main():
    """Main entry point."""
    global running

    try:
        # Connect to serial port
        print(f"Connecting to {DEVICE} at {BAUDRATE} baud...\n")
        ser = serial.Serial(DEVICE, BAUDRATE, timeout=1)
        time.sleep(0.1)  # Wait for connection to establish

        print_banner()

        # Start serial reader thread
        reader_thread = threading.Thread(target=serial_reader, args=(ser,), daemon=True)
        reader_thread.start()

        # Send initial Ctrl+D to reload
        print("[Sending initial reload to restart CircuitPython...]\n")
        ser.write(b'\x04')
        time.sleep(0.5)

        # Start input reader (main thread)
        input_reader_unix(ser)

        # Cleanup
        running = False
        time.sleep(0.2)  # Give reader thread time to finish
        ser.close()
        print("\n✓ Serial monitor closed\n")
        return 0

    except serial.SerialException as e:
        print(f"✗ Serial error: {e}")
        print("\nTroubleshooting:")
        print("  - Is the device connected?")
        print("  - Is another program using the serial port?")
        print("  - Try unplugging and replugging the USB cable")
        return 1

    except KeyboardInterrupt:
        running = False
        print("\n\n✓ Interrupted by user\n")
        try:
            ser.close()
        except:
            pass
        return 0

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
