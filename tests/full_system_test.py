"""
Full System Integration Test
Tests M4 + OLED + MIDI together

Displays MIDI activity on OLED, responds to buttons
"""

import board
import busio
import time
import digitalio
import displayio
import terminalio
from i2cdisplaybus import I2CDisplayBus
import adafruit_displayio_sh1107
from adafruit_display_text import label
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

print("\n=== Full System Integration Test ===\n")

# Initialize I2C for display
print("[1] Initializing I2C...")
i2c = board.I2C()
print("OK")

# Initialize OLED display
print("[2] Initializing OLED (SH1107 128x64)...")
displayio.release_displays()
display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)
display.brightness = 0.8
print("OK")

# Initialize buttons
print("[3] Initializing buttons...")
button_a = digitalio.DigitalInOut(board.D9)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.D6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

button_c = digitalio.DigitalInOut(board.D5)
button_c.direction = digitalio.Direction.INPUT
button_c.pull = digitalio.Pull.UP
print("OK")

# Initialize MIDI
print("[4] Initializing MIDI...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("OK")

# Create display group
splash = displayio.Group()

# Title
title = label.Label(terminalio.FONT, text="SYSTEM TEST", color=0xFFFFFF, x=20, y=10)
splash.append(title)

# MIDI IN/OUT indicators
midi_in_label = label.Label(terminalio.FONT, text="IN: ---", color=0xFFFFFF, x=0, y=25)
splash.append(midi_in_label)

midi_out_label = label.Label(terminalio.FONT, text="OUT: ---", color=0xFFFFFF, x=0, y=38)
splash.append(midi_out_label)

# Button status
button_label = label.Label(terminalio.FONT, text="BTN: ---", color=0xFFFFFF, x=0, y=51)
splash.append(button_label)

display.root_group = splash

print("\n[5] System running!")
print("- Play MIDI notes → see IN activity")
print("- Press Button A → sends test note")
print("- Press Button B/C → changes display")
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
        print(f"MIDI IN: Note {msg.note}")

    # Update MIDI IN display (fade after 0.5s)
    if last_note_in and (current_time - note_in_time) < 0.5:
        midi_in_label.text = f"IN: {last_note_in:3d}"
    else:
        midi_in_label.text = "IN: ---"

    # Update MIDI OUT display (fade after 0.5s)
    if last_note_out and (current_time - note_out_time) < 0.5:
        midi_out_label.text = f"OUT: {last_note_out:3d}"
    else:
        midi_out_label.text = "OUT: ---"

    # Check buttons
    btn_text = ""

    if not button_a.value:  # Pressed
        btn_text = "A"
        # Send test note
        midi.send(NoteOn(60, 100))
        last_note_out = 60
        note_out_time = current_time
        print("Button A: Sent Note 60")
        time.sleep(0.2)
        midi.send(NoteOff(60, 0))

    if not button_b.value:
        btn_text += "B"
        display.brightness = 0.3 if display.brightness > 0.5 else 1.0
        time.sleep(0.2)

    if not button_c.value:
        btn_text += "C"
        time.sleep(0.2)

    button_label.text = f"BTN: {btn_text if btn_text else '---'}"

    time.sleep(0.01)  # 10ms loop
