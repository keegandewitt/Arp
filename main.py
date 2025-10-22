"""
Arp - Hardware Arpeggiator (Phase 1: MIDI Core)
Main application entry point

Hardware:
- Adafruit Feather M4 CAN Express
- Adafruit MIDI FeatherWing (UART TX/RX)
- Adafruit OLED FeatherWing 128x64 (I2C)

Phase 1 Features:
- MIDI IN/OUT via DIN-5 jacks
- Basic arpeggiator patterns (Up, Down, Random)
- OLED display with pattern/tempo
- Button controls for pattern selection
- Internal clock (120 BPM default)
"""

import board
import busio
import time
import digitalio
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# Import our modules
from arp.ui.display import Display
from arp.ui.buttons import ButtonHandler

print("\n" + "="*60)
print("ARP - Hardware Arpeggiator v1.0")
print("="*60)

# =============================================================================
# Hardware Initialization
# =============================================================================

print("[1/3] Initializing MIDI...")
# MIDI FeatherWing on UART (TX=D1, RX=D0)
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("      ✓ MIDI ready (31250 baud)")

print("[2/3] Initializing Display...")
# OLED FeatherWing on I2C
i2c = board.I2C()
display = Display(i2c)
display.show_startup()
print("      ✓ Display ready (SH1107 128x64)")

print("[3/3] Initializing Buttons...")
# Buttons on OLED FeatherWing (D9=A, D6=B, D5=C)
buttons = ButtonHandler(board.D9, board.D6, board.D5)
print("      ✓ Buttons ready (A, B, C)")

print("\n" + "="*60)
print("SYSTEM READY")
print("="*60)
print("Button A: Previous pattern")
print("Button B: Play C major chord arpeggio (demo)")
print("Button C: Next pattern")
print("MIDI IN: Send notes to arpeggiate")
print("-"*60 + "\n")

# =============================================================================
# Arpeggiator State
# =============================================================================

# Pattern definitions
PATTERNS = ['UP', 'DOWN', 'UP/DOWN', 'RANDOM']
current_pattern_index = 0

# Note buffer (stores held notes)
note_buffer = []  # List of (note, velocity) tuples

# Arpeggiator state
current_step = 0
arp_sequence = []
last_note_time = 0
note_interval = 0.125  # 1/8 note at 120 BPM = 125ms
bpm = 120

# Currently playing note (for note-off)
current_playing_note = None

def get_current_pattern():
    """Get the current pattern name"""
    return PATTERNS[current_pattern_index]

def generate_arp_sequence(notes):
    """Generate arpeggiated sequence from note buffer"""
    if not notes:
        return []

    pattern = get_current_pattern()
    note_nums = sorted([n for n, v in notes])  # Just note numbers, sorted

    if pattern == 'UP':
        return note_nums
    elif pattern == 'DOWN':
        return list(reversed(note_nums))
    elif pattern == 'UP/DOWN':
        return note_nums + list(reversed(note_nums[1:-1])) if len(note_nums) > 2 else note_nums
    elif pattern == 'RANDOM':
        import random
        shuffled = note_nums.copy()
        random.shuffle(shuffled)
        return shuffled

    return note_nums

# Update display with initial state
time.sleep(1)  # Let startup message show
display.update_display(bpm, get_current_pattern(), True, "INT")

# =============================================================================
# Main Loop
# =============================================================================

loop_count = 0

while True:
    loop_count += 1
    current_time = time.monotonic()

    # -------------------------------------------------------------------------
    # MIDI Input Processing
    # -------------------------------------------------------------------------
    msg = midi.receive()
    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            # Add note to buffer
            if not any(n == msg.note for n, v in note_buffer):
                note_buffer.append((msg.note, msg.velocity))
                arp_sequence = generate_arp_sequence(note_buffer)
                current_step = 0  # Reset step on new note
                print(f"Note ON: {msg.note} (velocity {msg.velocity}) - Buffer: {[n for n,v in note_buffer]}")

        elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            # Remove note from buffer
            note_buffer = [(n, v) for n, v in note_buffer if n != msg.note]
            arp_sequence = generate_arp_sequence(note_buffer)
            if not note_buffer:
                current_step = 0
                # Send note off if we were playing
                if current_playing_note is not None:
                    midi.send(NoteOff(current_playing_note, 0))
                    current_playing_note = None
            print(f"Note OFF: {msg.note} - Buffer: {[n for n,v in note_buffer]}")

    # -------------------------------------------------------------------------
    # Arpeggiator Clock & Step
    # -------------------------------------------------------------------------
    if arp_sequence and (current_time - last_note_time >= note_interval):
        # Send note off for previous note
        if current_playing_note is not None:
            midi.send(NoteOff(current_playing_note, 0))

        # Get next note in sequence
        note_to_play = arp_sequence[current_step]
        velocity = 100  # Could use velocity from buffer

        # Send note on
        midi.send(NoteOn(note_to_play, velocity))
        current_playing_note = note_to_play

        # Advance step
        current_step = (current_step + 1) % len(arp_sequence)
        last_note_time = current_time

    # -------------------------------------------------------------------------
    # Button Input
    # -------------------------------------------------------------------------
    button_a, button_b, button_c, button_ac_combo, a_long, b_long = buttons.check_buttons()

    if button_a:
        # Previous pattern
        current_pattern_index = (current_pattern_index - 1) % len(PATTERNS)
        arp_sequence = generate_arp_sequence(note_buffer)
        print(f"Pattern: {get_current_pattern()}")
        display.update_display(bpm, get_current_pattern(), True, "INT")

    if button_c:
        # Next pattern
        current_pattern_index = (current_pattern_index + 1) % len(PATTERNS)
        arp_sequence = generate_arp_sequence(note_buffer)
        print(f"Pattern: {get_current_pattern()}")
        display.update_display(bpm, get_current_pattern(), True, "INT")

    if button_b:
        # Demo: Play C major chord arpeggio
        print("Button B: Playing C major arpeggio demo")
        note_buffer = [(60, 100), (64, 100), (67, 100)]  # C, E, G
        arp_sequence = generate_arp_sequence(note_buffer)
        current_step = 0

        # Play for 4 beats then stop
        for i in range(4):
            if current_step < len(arp_sequence):
                note = arp_sequence[current_step]
                midi.send(NoteOn(note, 100))
                time.sleep(0.12)
                midi.send(NoteOff(note, 0))
                time.sleep(0.005)
                current_step = (current_step + 1) % len(arp_sequence)

        # Clear buffer after demo
        note_buffer = []
        arp_sequence = []
        current_step = 0

    # Small delay to prevent CPU spinning
    time.sleep(0.001)
