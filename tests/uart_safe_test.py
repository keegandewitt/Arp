"""Safe UART test with detailed error catching"""

import board
import busio
import time

print("\n" + "=" * 60)
print("SAFE UART LOOPBACK TEST")
print("=" * 60)

print("\nMake sure:")
print("  - D0 (RX) and D1 (TX) are connected with a jumper")
print("  - No other devices using UART pins")
print("\nStarting in 3 seconds...")
time.sleep(3)

uart = None

try:
    print("\n[1] Attempting to initialize UART...")
    print(f"    TX pin: board.TX = {board.TX}")
    print(f"    RX pin: board.RX = {board.RX}")

    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=1.0)
    print("    ✓ UART initialized successfully!")

except ValueError as e:
    print(f"    ✗ ValueError: {e}")
    print("    This usually means: pins already in use or wrong pins")
    uart = None

except RuntimeError as e:
    print(f"    ✗ RuntimeError: {e}")
    print("    This usually means: hardware issue or peripheral unavailable")
    uart = None

except Exception as e:
    print(f"    ✗ Unexpected error: {type(e).__name__}: {e}")
    uart = None

if uart is not None:
    try:
        print("\n[2] Clearing RX buffer...")
        time.sleep(0.1)
        if uart.in_waiting:
            discarded = uart.in_waiting
            uart.reset_input_buffer()
            print(f"    ✓ Cleared {discarded} old bytes")
        else:
            print("    ✓ Buffer already clear")

        print("\n[3] Sending test message...")
        test_msg = b"HELLO"
        bytes_written = uart.write(test_msg)
        print(f"    ✓ Wrote {bytes_written} bytes: {test_msg}")

        print("\n[4] Waiting for loopback (1 second)...")
        time.sleep(1.0)

        print("\n[5] Checking RX buffer...")
        waiting = uart.in_waiting
        print(f"    Bytes in buffer: {waiting}")

        if waiting > 0:
            print("\n[6] Reading data...")
            received = uart.read(waiting)
            print(f"    ✓ Received: {received}")

            print("\n[7] Comparing...")
            if received == test_msg:
                print("    ✓✓✓ SUCCESS! Loopback working!")
            else:
                print("    ✗ MISMATCH!")
                print(f"    Expected: {test_msg}")
                print(f"    Got:      {received}")
        else:
            print("\n    ✗ NO DATA RECEIVED")
            print("    Possible causes:")
            print("      - Jumper not connected")
            print("      - Bad solder joint on D0 or D1")
            print("      - Wrong pins connected")

        print("\n[8] Cleaning up...")
        uart.deinit()
        print("    ✓ UART closed")

    except Exception as e:
        print(f"\n✗ Error during test: {type(e).__name__}: {e}")
        if uart:
            try:
                uart.deinit()
            except:
                pass
else:
    print("\n✗ UART initialization failed - skipping loopback test")
    print("\nThis might be normal - UART pins may conflict with USB serial.")
    print("You can skip the UART test for now.")

print("\n" + "=" * 60)
print("Test complete")
print("=" * 60)
print("\nType 'exit' to close monitor")

while True:
    time.sleep(1)
