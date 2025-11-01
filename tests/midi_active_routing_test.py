"""
Active MIDI Routing Test
Sends test notes + echoes received notes (for loopback testing)
"""

import board
import busio
import time
import gc
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

print("\n" + "="*60)
print("ACTIVE MIDI ROUTING TEST")
print("="*60)
print("\nWith loopback cable: Sends notes, receives them back")
print("Without loopback: Sends notes out to synth")
print("="*60 + "\n")

# Initialize MIDI
print("[1/2] Initializing MIDI...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("      ✓ MIDI ready")

# Memory
gc.collect()
print(f"[2/2] Memory: {gc.mem_free()} bytes free")
print("\n" + "="*60)
print("STARTING TEST - Sending notes every 500ms...")
print("="*60 + "\n")

# Test notes (C major scale)
test_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
note_index = 0
received_count = 0
sent_count = 0

last_send_time = time.monotonic()
send_interval = 0.5  # Send note every 500ms

while True:
    current_time = time.monotonic()

    # Check for received MIDI (from loopback or external)
    msg = midi.receive()
    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            received_count += 1
            print(f"  ← Received: Note ON  {msg.note:3d} (vel {msg.velocity:3d}) [{received_count} total]")
        elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            print(f"  ← Received: Note OFF {msg.note:3d}")

    # Send test note periodically
    if current_time - last_send_time >= send_interval:
        # Get next test note
        note = test_notes[note_index]

        # Send note on
        print(f"  → Sending:  Note ON  {note:3d} (vel 100)")
        midi.send(NoteOn(note, 100))
        sent_count += 1

        time.sleep(0.05)  # Short delay

        # Send note off
        print(f"  → Sending:  Note OFF {note:3d}")
        midi.send(NoteOff(note, 0))

        # Advance to next note
        note_index = (note_index + 1) % len(test_notes)

        # Stats every 8 notes
        if sent_count % 8 == 0:
            print(f"\n--- Sent: {sent_count} | Received: {received_count} ---\n")
            gc.collect()

        last_send_time = current_time

    time.sleep(0.001)
