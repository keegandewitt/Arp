"""
Integration Test with Debug Output
Tests M4 + OLED + MIDI + Buttons step by step

Debug version that reports each initialization step
"""

import board
import busio
import time
import digitalio

print("\n" + "="*60)
print("INTEGRATION TEST - DEBUG MODE")
print("="*60 + "\n")

# Step 1: Initialize Buttons
try:
    print("[1/4] Initializing buttons...")
    button_a = digitalio.DigitalInOut(board.D9)
    button_a.direction = digitalio.Direction.INPUT
    button_a.pull = digitalio.Pull.UP

    button_b = digitalio.DigitalInOut(board.D6)
    button_b.direction = digitalio.Direction.INPUT
    button_b.pull = digitalio.Pull.UP

    button_c = digitalio.DigitalInOut(board.D5)
    button_c.direction = digitalio.Direction.INPUT
    button_c.pull = digitalio.Pull.UP
    print("      ✓ Buttons ready (D9, D6, D5)")
except Exception as e:
    print(f"      ✗ BUTTON ERROR: {e}")
    raise

# Step 2: Initialize MIDI
try:
    print("[2/4] Initializing MIDI UART...")
    uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
    print("      ✓ UART ready (31250 baud)")
except Exception as e:
    print(f"      ✗ UART ERROR: {e}")
    raise

try:
    print("[3/4] Initializing MIDI library...")
    import adafruit_midi
    from adafruit_midi.note_on import NoteOn
    from adafruit_midi.note_off import NoteOff
    from adafruit_midi.timing_clock import TimingClock

    midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
    print("      ✓ MIDI library ready")
except Exception as e:
    print(f"      ✗ MIDI LIBRARY ERROR: {e}")
    raise

# Step 4: Initialize OLED (if possible)
oled_available = False
try:
    print("[4/4] Initializing OLED display...")
    import displayio
    import terminalio
    from i2cdisplaybus import I2CDisplayBus
    import adafruit_displayio_sh1107
    from adafruit_display_text import label

    displayio.release_displays()
    i2c = board.I2C()
    display_bus = I2CDisplayBus(i2c, device_address=0x3C)
    display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)
    display.brightness = 0.8

    # Create display group
    splash = displayio.Group()

    title = label.Label(terminalio.FONT, text="INTEGRATION", color=0xFFFFFF, x=20, y=10)
    splash.append(title)

    status_label = label.Label(terminalio.FONT, text="Ready!", color=0xFFFFFF, x=0, y=25)
    splash.append(status_label)

    midi_label = label.Label(terminalio.FONT, text="MIDI: ---", color=0xFFFFFF, x=0, y=40)
    splash.append(midi_label)

    btn_label = label.Label(terminalio.FONT, text="BTN: ---", color=0xFFFFFF, x=0, y=55)
    splash.append(btn_label)

    display.root_group = splash
    oled_available = True
    print("      ✓ OLED ready (SH1107 128x64)")
except Exception as e:
    print(f"      ⚠ OLED not available: {e}")
    print("      → Continuing without OLED...")

print("\n" + "="*60)
print("SYSTEM READY - Starting main loop")
print("="*60)
print("Commands:")
print("  Button A: Send C4 (60)")
print("  Button B: Send E4 (64)")
print("  Button C: Send G4 (67) + MIDI Clock")
print("  MIDI IN: Receives and displays notes")
print("-"*60 + "\n")

# Main loop
loop_count = 0
clock_count = 0

while True:
    loop_count += 1
    current_time = time.monotonic()

    # Heartbeat every 5 seconds
    if loop_count % 500 == 0:
        print(f"[Heartbeat] Loop {loop_count}, Time: {current_time:.1f}s")

    # Check MIDI input
    msg = midi.receive()
    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            print(f"MIDI IN → Note {msg.note:3d}  Velocity: {msg.velocity:3d}")
            if oled_available:
                midi_label.text = f"IN: {msg.note}"
        elif isinstance(msg, TimingClock):
            clock_count += 1
            if clock_count % 24 == 0:  # 24 clocks per quarter note
                print(f"MIDI IN → Clock (quarter note #{clock_count//24})")

    # Button A: Send Note
    if not button_a.value:
        midi.send(NoteOn(60, 100))
        print("Button A → MIDI OUT: C4 (60)")
        if oled_available:
            btn_label.text = "BTN: A"
            midi_label.text = "OUT: 60"
        time.sleep(0.15)
        midi.send(NoteOff(60, 0))
        time.sleep(0.05)
        if oled_available:
            btn_label.text = "BTN: ---"

    # Button B: Send Note
    if not button_b.value:
        midi.send(NoteOn(64, 100))
        print("Button B → MIDI OUT: E4 (64)")
        if oled_available:
            btn_label.text = "BTN: B"
            midi_label.text = "OUT: 64"
        time.sleep(0.15)
        midi.send(NoteOff(64, 0))
        time.sleep(0.05)
        if oled_available:
            btn_label.text = "BTN: ---"

    # Button C: Send Note + Clock signals
    if not button_c.value:
        midi.send(NoteOn(67, 100))
        print("Button C → MIDI OUT: G4 (67) + Clock signals")
        if oled_available:
            btn_label.text = "BTN: C"
            midi_label.text = "OUT: 67+CLK"

        # Send 24 clock pulses (1 quarter note worth)
        for i in range(24):
            midi.send(TimingClock())
            time.sleep(0.005)  # 5ms between clocks (~120 BPM)

        midi.send(NoteOff(67, 0))
        time.sleep(0.05)
        if oled_available:
            btn_label.text = "BTN: ---"

    time.sleep(0.01)  # 10ms loop delay
