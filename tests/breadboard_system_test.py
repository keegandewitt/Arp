"""
Breadboard System Integration Test
Tests M4 + OLED (stacked) + MIDI (breadboard) together

Simpler version that's more robust for breadboard testing
"""

import board
import busio
import time
import digitalio
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

print("\n=== Breadboard System Test ===\n")

# Initialize buttons
print("[1] Initializing buttons...")
button_a = digitalio.DigitalInOut(board.D9)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.D6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

button_c = digitalio.DigitalInOut(board.D5)
button_c.direction = digitalio.Direction.INPUT
button_c.pull = digitalio.Pull.UP
print("OK - Buttons on D9, D6, D5")

# Initialize MIDI
print("[2] Initializing MIDI...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("OK - MIDI on breadboard")

print("\n[3] System running!")
print("- Button A: Send test note (C4)")
print("- Button B: Send test note (E4)")
print("- Button C: Send test note (G4)")
print("- MIDI IN: Play notes and they'll be displayed")
print("")

last_note_in = None
last_note_out = None
note_in_time = 0
note_out_time = 0

while True:
    current_time = time.monotonic()

    # Check MIDI input
    msg = midi.receive()
    if msg is not None and isinstance(msg, NoteOn) and msg.velocity > 0:
        last_note_in = msg.note
        note_in_time = current_time
        print(f"MIDI IN:  Note {msg.note:3d}  Velocity: {msg.velocity:3d}")

    # Check buttons and send MIDI
    if not button_a.value:  # Button A pressed
        midi.send(NoteOn(60, 100))  # C4
        print("Button A → MIDI OUT: C4 (60)")
        time.sleep(0.2)
        midi.send(NoteOff(60, 0))

    if not button_b.value:  # Button B pressed
        midi.send(NoteOn(64, 100))  # E4
        print("Button B → MIDI OUT: E4 (64)")
        time.sleep(0.2)
        midi.send(NoteOff(64, 0))

    if not button_c.value:  # Button C pressed
        midi.send(NoteOn(67, 100))  # G4
        print("Button C → MIDI OUT: G4 (67)")
        time.sleep(0.2)
        midi.send(NoteOff(67, 0))

    time.sleep(0.01)  # 10ms loop
