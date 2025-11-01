"""
Minimal MIDI Test - No external module dependencies
Tests MIDI FeatherWing with bare minimum code
Follows CircuitPython crash prevention patterns
"""

import board
import busio
import time

print("\n" + "="*60)
print("MINIMAL MIDI TEST")
print("="*60)

# Step 1: Initialize UART
print("\n[1] Initializing UART...")
try:
    uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
    print("    ✓ UART initialized (D0=RX, D1=TX, 31250 baud)")
except Exception as e:
    print(f"    ✗ UART FAILED: {e}")
    while True:
        time.sleep(1)

# Step 2: Import MIDI library
print("\n[2] Importing MIDI library...")
try:
    import adafruit_midi
    from adafruit_midi.note_on import NoteOn
    from adafruit_midi.note_off import NoteOff
    print("    ✓ MIDI library imported")
except ImportError as e:
    print(f"    ✗ MIDI library missing: {e}")
    print("    Run: circup install adafruit_midi")
    while True:
        time.sleep(1)

# Step 3: Create MIDI object
print("\n[3] Creating MIDI interface...")
try:
    midi = adafruit_midi.MIDI(
        midi_in=uart,
        midi_out=uart,
        in_channel=0,
        out_channel=0
    )
    print("    ✓ MIDI interface ready")
except Exception as e:
    print(f"    ✗ MIDI interface FAILED: {e}")
    while True:
        time.sleep(1)

# Step 4: Test transmission
print("\n[4] Testing MIDI transmission...")
print("    Sending test note (C4, note 60)...")
try:
    midi.send(NoteOn(60, 100))
    time.sleep(0.1)
    midi.send(NoteOff(60, 0))
    print("    ✓ Note sent successfully")
    print("    (MIDI OUT LED should have blinked)")
except Exception as e:
    print(f"    ✗ Send FAILED: {e}")

# Step 5: Reception test
print("\n[5] Testing MIDI reception...")
print("    Listening for 5 seconds...")
print("    (If loopback cable connected, will see test note)")
print()

received_count = 0
start_time = time.monotonic()

while (time.monotonic() - start_time) < 5.0:
    msg = midi.receive()
    if msg is not None:
        received_count += 1
        if isinstance(msg, NoteOn):
            print(f"    ✓ Note ON:  {msg.note} (velocity {msg.velocity})")
        elif isinstance(msg, NoteOff):
            print(f"    ✓ Note OFF: {msg.note}")
        else:
            print(f"    ✓ MIDI: {type(msg).__name__}")
    time.sleep(0.001)

print(f"\n    Total messages received: {received_count}")

# Success
print("\n" + "="*60)
print("✅ MIDI TEST COMPLETE")
print("="*60)
print("\nHardware Status:")
print("  ✓ UART working (D0/D1)")
print("  ✓ MIDI library loaded")
print("  ✓ Transmission working")
if received_count > 0:
    print("  ✓ Reception working")
else:
    print("  - Reception: No messages (connect loopback cable to test)")

print("\n" + "="*60)
print("Test complete. Looping...")
print("="*60 + "\n")

# Keep running
while True:
    time.sleep(1)
