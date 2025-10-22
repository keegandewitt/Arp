"""
MIDI Input Test
Tests MIDI FeatherWing input functionality

Hardware: Adafruit MIDI FeatherWing #4740
Pins: RX (D0) for MIDI IN
"""

import board
import busio
import time
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

print("\n=== MIDI Input Test ===\n")

# Initialize UART MIDI (31250 baud for MIDI)
print("[1] Initializing UART MIDI IN...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi_in = adafruit_midi.MIDI(midi_in=uart, in_channel=0)
print("OK - MIDI IN on RX (D0)")

print("\n[2] Listening for MIDI Input...")
print("Connect a MIDI controller/keyboard to MIDI IN")
print("Watch for MIDI IN LED on FeatherWing")
print("Play some notes!\n")

note_count = 0

while True:
    msg = midi_in.receive()

    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            note_count += 1
            print(f"[{note_count}] Note ON:  Note #{msg.note:3d}  Velocity: {msg.velocity:3d}")

        elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            print(f"      Note OFF: Note #{msg.note:3d}")

    time.sleep(0.001)  # Small delay to prevent overwhelming CPU
