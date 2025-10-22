"""
MIDI Output Test
Tests MIDI FeatherWing output functionality

Hardware: Adafruit MIDI FeatherWing #4740
Pins: TX (D1) for MIDI OUT
"""

import board
import busio
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

print("\n=== MIDI Output Test ===\n")

# Initialize UART MIDI (31250 baud for MIDI)
print("[1] Initializing UART MIDI OUT...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi_out = adafruit_midi.MIDI(midi_out=uart, out_channel=0)
print("OK - MIDI OUT on TX (D1)")

# Test notes (C major chord: C4, E4, G4)
notes = [60, 64, 67]  # MIDI note numbers
note_names = ["C4", "E4", "G4"]

print("\n[2] Testing MIDI Output...")
print("Connect MIDI OUT to a MIDI device/synth")
print("Watch for MIDI OUT LED on FeatherWing")
print("You should hear notes C-E-G repeating\n")

count = 0
while True:
    for i, note in enumerate(notes):
        # Send Note On
        print(f"Sending Note ON: {note_names[i]} (note #{note})")
        midi_out.send(NoteOn(note, 100))  # velocity 100

        time.sleep(0.3)

        # Send Note Off
        print(f"Sending Note OFF: {note_names[i]}")
        midi_out.send(NoteOff(note, 0))

        time.sleep(0.2)

    count += 1
    print(f"\n--- Cycle {count} complete ---\n")
    time.sleep(1)
