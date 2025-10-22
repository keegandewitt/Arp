"""
MIDI Loopback Test
Tests MIDI FeatherWing by connecting MIDI OUT to MIDI IN

Hardware: Adafruit MIDI FeatherWing #4740
Setup: Connect MIDI OUT jack to MIDI IN jack with MIDI cable
"""

import board
import busio
import time
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

print("\n=== MIDI Loopback Test ===\n")
print("SETUP: Connect MIDI OUT to MIDI IN with a MIDI cable")
print("This tests that both MIDI jacks work\n")

# Initialize UART MIDI (31250 baud for MIDI)
print("[1] Initializing UART MIDI...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("OK - MIDI IN/OUT on RX/TX (D0/D1)")

print("\n[2] Starting loopback test...")
print("Sending notes and checking if they loop back\n")

test_note = 60  # Middle C
sent_count = 0
received_count = 0
errors = 0

while True:
    # Send note
    sent_count += 1
    print(f"Sending Note #{test_note}... ", end='')
    midi.send(NoteOn(test_note, 100))

    # Wait for loopback
    start_time = time.monotonic()
    received = False

    while (time.monotonic() - start_time) < 0.1:  # 100ms timeout
        msg = midi.receive()
        if msg is not None and isinstance(msg, NoteOn):
            if msg.note == test_note:
                received_count += 1
                print(f"✓ Received! (velocity: {msg.velocity})")
                received = True
                break
        time.sleep(0.001)

    if not received:
        errors += 1
        print(f"✗ NOT RECEIVED (timeout)")

    # Send note off
    midi.send(NoteOff(test_note, 0))

    # Clear any remaining messages
    while midi.receive() is not None:
        pass

    # Stats
    if sent_count % 10 == 0:
        success_rate = (received_count / sent_count) * 100
        print(f"\n--- Stats: {sent_count} sent, {received_count} received ({success_rate:.1f}%), {errors} errors ---\n")

    # Change note for next test
    test_note += 1
    if test_note > 72:  # C to C (one octave)
        test_note = 60

    time.sleep(0.5)
