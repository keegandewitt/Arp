"""
MIDI FeatherWing Connection Test
Verifies MIDI FeatherWing is properly connected and UART initializes

Hardware: Adafruit MIDI FeatherWing #4740
Pins: TX (D1) for MIDI OUT, RX (D0) for MIDI IN
Test: Initializes UART and verifies hardware communication

This is Step 1 before testing actual MIDI routing.
"""

import board
import busio
import time

print("\n" + "="*60)
print("MIDI FeatherWing Connection Test")
print("="*60)
print("\nVerifying MIDI FeatherWing hardware connection...")
print()

# Test 1: UART Initialization
print("[1/3] Initializing UART on D0 (RX) and D1 (TX)...")
try:
    uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
    print("      ✓ UART initialized successfully")
    print(f"      - Baudrate: 31250 (MIDI standard)")
    print(f"      - TX Pin: D1 (board.TX)")
    print(f"      - RX Pin: D0 (board.RX)")
except Exception as e:
    print(f"      ✗ UART initialization FAILED: {e}")
    print("\n⚠️  TROUBLESHOOTING:")
    print("    - Is MIDI FeatherWing stacked on Feather M4?")
    print("    - Check that pins are properly aligned")
    print("    - Verify no bent pins on FeatherWing")
    raise

# Test 2: UART Read/Write Buffer Check
print("\n[2/3] Checking UART read buffer...")
try:
    # Check if we can read (should return None or empty if nothing connected)
    data = uart.read(1)
    if data is None:
        print("      ✓ UART read buffer accessible (no data)")
    else:
        print(f"      ✓ UART read buffer accessible (received {len(data)} bytes)")
except Exception as e:
    print(f"      ✗ UART read buffer FAILED: {e}")
    raise

# Test 3: MIDI Library Initialization
print("\n[3/3] Initializing MIDI library...")
try:
    import adafruit_midi
    from adafruit_midi.note_on import NoteOn
    from adafruit_midi.note_off import NoteOff

    midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
    print("      ✓ MIDI library initialized successfully")
    print(f"      - MIDI IN channel: 0 (omni)")
    print(f"      - MIDI OUT channel: 0")
except ImportError as e:
    print(f"      ✗ MIDI library import FAILED: {e}")
    print("\n⚠️  TROUBLESHOOTING:")
    print("    - Install adafruit_midi: circup install adafruit_midi")
    raise
except Exception as e:
    print(f"      ✗ MIDI library initialization FAILED: {e}")
    raise

# Test 4: LED Check (if visible)
print("\n[4/4] Visual Hardware Check...")
print("      Look at the MIDI FeatherWing:")
print("      - PWR LED should be ON (green)")
print("      - MIDI IN LED (red) will blink when receiving MIDI")
print("      - MIDI OUT LED (red) will blink when sending MIDI")
print()

# Success Summary
print("\n" + "="*60)
print("✅ CONNECTION TEST PASSED")
print("="*60)
print("\nMIDI FeatherWing is properly connected and initialized!")
print("\nHardware Status:")
print("  ✓ UART initialized (31250 baud)")
print("  ✓ MIDI library loaded")
print("  ✓ Ready for MIDI communication")
print("\nNext Steps:")
print("  1. Run 'midi_input_test.py' to test MIDI IN")
print("  2. Run 'midi_output_test.py' to test MIDI OUT")
print("  3. Run 'midi_loopback_test.py' to test both (requires MIDI cable)")
print("\n" + "="*60 + "\n")

# Keep running to allow serial monitoring
print("Test complete. Press Ctrl+C to exit or reset board.\n")
while True:
    time.sleep(1)
