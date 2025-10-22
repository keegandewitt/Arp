"""
UART Loopback Debugging Test

This is a more detailed UART test with extra diagnostics.
Use this to debug UART loopback issues.

Connect D0 (RX) to D1 (TX) with a jumper wire.
"""

import board
import busio
import time

print("\n" + "=" * 60)
print("UART LOOPBACK DEBUG TEST")
print("=" * 60)
print("\nMake sure D0 (RX) and D1 (TX) are connected with a jumper wire.")
print("\nStarting test in 3 seconds...")
time.sleep(3)

try:
    print("\n1. Initializing UART...")
    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=1.0)
    print("   ✓ UART initialized at 9600 baud")

    # Clear any existing data in buffers
    time.sleep(0.1)
    if uart.in_waiting:
        uart.reset_input_buffer()
        print(f"   Cleared {uart.in_waiting} bytes from RX buffer")

    print("\n2. Sending test data...")
    test_msg = b"HELLO"
    bytes_written = uart.write(test_msg)
    print(f"   ✓ Wrote {bytes_written} bytes: {test_msg}")

    # Give time for data to transmit and loop back
    print("\n3. Waiting for loopback (1 second)...")
    time.sleep(1.0)

    print("\n4. Checking RX buffer...")
    waiting = uart.in_waiting
    print(f"   Bytes waiting in RX buffer: {waiting}")

    if waiting > 0:
        print("\n5. Reading received data...")
        received = uart.read(waiting)
        print(f"   ✓ Read {len(received)} bytes: {received}")

        print("\n6. Comparing data...")
        if received == test_msg:
            print("   ✓✓✓ SUCCESS! Data matches!")
            print(f"   Sent:     {test_msg}")
            print(f"   Received: {received}")
        else:
            print("   ✗✗✗ MISMATCH!")
            print(f"   Sent:     {test_msg}")
            print(f"   Received: {received}")
            print("\n   Possible causes:")
            print("   - Loose jumper wire connection")
            print("   - Cold solder joint on D0 or D1")
            print("   - Damaged pins")
    else:
        print("   ✗✗✗ NO DATA RECEIVED!")
        print("\n   Troubleshooting:")
        print("   1. Check jumper wire is firmly connected")
        print("   2. Verify D0 (RX) is connected to D1 (TX)")
        print("   3. Check solder joints on D0 and D1")
        print("   4. Try a different jumper wire")
        print("   5. Verify D0 and D1 passed the GPIO test earlier")

    uart.deinit()
    print("\n" + "=" * 60)
    print("Test complete")
    print("=" * 60)

except Exception as e:
    print(f"\n✗✗✗ ERROR: {e}")
    print("\nThis usually means:")
    print("- UART peripheral is not available")
    print("- Pins are already in use by another function")
    print("- Hardware issue with the UART pins")

print("\nPress Ctrl+C to exit")
while True:
    time.sleep(1)
