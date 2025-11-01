"""
MIDI + OLED Integration Test
Shows real-time MIDI activity on OLED display
"""

import board
import busio
import time
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1107
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

print("\n" + "="*60)
print("MIDI + OLED INTEGRATION TEST")
print("="*60)

# Initialize OLED
print("[1/2] Initializing OLED...")
i2c = board.I2C()
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)
display.brightness = 0.8
print("      ✓ OLED ready")

# Initialize MIDI
print("[2/2] Initializing MIDI...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("      ✓ MIDI ready")

print("\n" + "="*60)
print("DISPLAY + MIDI READY!")
print("="*60)
print("\nSending test notes + showing on OLED...")
print("Watch the OLED screen for real-time updates!")
print("="*60 + "\n")

# Create display layout
group = displayio.Group()

# Title
title = label.Label(terminalio.FONT, text="MIDI Monitor", color=0xFFFFFF, x=20, y=5)
group.append(title)

# Separator line (using dashes)
sep = label.Label(terminalio.FONT, text="-" * 21, color=0xFFFFFF, x=0, y=15)
group.append(sep)

# Status line
status = label.Label(terminalio.FONT, text="Sending...", color=0xFFFFFF, x=25, y=25)
group.append(status)

# Current note line
note_line = label.Label(terminalio.FONT, text="Note: ---", color=0xFFFFFF, x=25, y=38)
group.append(note_line)

# Counter line
counter_line = label.Label(terminalio.FONT, text="Count: 0", color=0xFFFFFF, x=25, y=51)
group.append(counter_line)

display.root_group = group

# Test data
test_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
note_names = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
note_index = 0
count = 0

last_send_time = time.monotonic()
send_interval = 0.8  # Send note every 800ms

print("Starting MIDI test loop...")
print("(Watch both serial output AND OLED display)\n")

while True:
    current_time = time.monotonic()

    # Send notes periodically
    if current_time - last_send_time >= send_interval:
        note = test_notes[note_index]
        name = note_names[note_index]

        # Send MIDI
        midi.send(NoteOn(note, 100))
        time.sleep(0.1)
        midi.send(NoteOff(note, 0))

        count += 1

        # Update display
        status.text = f"Sent: {name}"
        note_line.text = f"Note: {note}"
        counter_line.text = f"Count: {count}"

        # Print to serial
        print(f"[{count:3d}] Sent {name:3s} (MIDI {note:3d}) → Check OLED!")

        # Next note
        note_index = (note_index + 1) % len(test_notes)
        last_send_time = current_time

    # Check for received MIDI (from loopback)
    msg = midi.receive()
    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            note_line.text = f"RCV: {msg.note}"
            print(f"      ← Received Note {msg.note}")

    time.sleep(0.05)
