"""
⚠️  DEPLOYMENT WARNING ⚠️
=======================
This file (main.py) is the SOURCE OF TRUTH in the repository.
It is deployed as code.py on the CircuitPython device.

ALWAYS EDIT: main.py (in repository)
NEVER EDIT:  code.py (on device) - it will be overwritten!

To deploy changes:
    python3 scripts/deploy.py

=======================

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
- Zero-latency MIDI pass-through (pitch bend, CC, etc.)

MIDI Routing:
- Note On/Off → Buffered for arpeggiator, NOT echoed back
- All other MIDI → Passed through immediately (zero latency)
  * Pitch Bend, Mod Wheel, Aftertouch, CC, Program Change, etc.
- Arpeggiated notes → Sent as new Note On/Off messages

Setup for Modern Synths (Prophet 5 Rev 4, etc.):
1. Synth MIDI OUT → Arp MIDI IN
2. Arp MIDI OUT → Synth MIDI IN
3. Set synth to "Local Control OFF" (disconnects keyboard from sound engine)
4. You'll only hear Arp's arpeggiated output, with full expression control

Setup for Vintage Synths (Moog Source, etc.):
- Same wiring as above
- Note: Vintage synths may not have "Local Control OFF"
- You may hear doubled notes (local keyboard + Arp output)
- This is a hardware limitation - use external MIDI filtering if needed
"""

# =============================================================================
# Version Information
# =============================================================================
__version__ = "0.95.0"
__build_date__ = "2025-10-23"
__hardware_version__ = "1.0"

import board
import busio
import time
import digitalio
import usb_midi
import gc
import random
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.channel_pressure import ChannelPressure
from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure
from adafruit_midi.system_exclusive import SystemExclusive
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.midi_continue import Continue
from adafruit_midi.active_sensing import ActiveSensing
from adafruit_midi.mtc_quarter_frame import MtcQuarterFrame
from adafruit_midi.midi_message import MIDIUnknownEvent, MIDIBadEvent

# Import our modules
from arp.ui.display import Display
from arp.ui.buttons import ButtonHandler
from arp.core.clock import ClockHandler
from arp.ui.menu import SettingsMenu
from arp.utils.config import Settings

print("\n" + "="*60)
print(f"ARP - Hardware Arpeggiator v{__version__}")
print(f"Build: {__build_date__} | Hardware: v{__hardware_version__}")
print("="*60)

# =============================================================================
# Configuration
# =============================================================================

# Enable memory monitoring for debugging (set to True to see memory stats)
DEBUG_MEMORY = False

if DEBUG_MEMORY:
    print(f"[DEBUG] Startup memory: {gc.mem_free()} bytes free")

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
display.show_startup(version=__version__)
print("      ✓ Display ready (SH1107 128x64)")

print("[3/3] Initializing Buttons...")
# Buttons on OLED FeatherWing (D9=A, D6=B, D5=C)
buttons = ButtonHandler(board.D9, board.D6, board.D5)
print("      ✓ Buttons ready (A, B, C)")

print("[4/5] Initializing Settings...")
# Global settings object
settings = Settings()
settings.load()  # Load saved settings from file (or use defaults if no file exists)
menu = SettingsMenu(settings)
print("      ✓ Settings ready")

print("[5/5] Initializing Clock...")
# Clock handler with USB MIDI input for external clock
# Note: MIDI FeatherWing (UART) is exclusive to Arpeggio Translation Loop
clock = ClockHandler(midi_in_port=usb_midi.ports[0])  # USB MIDI IN
clock.set_internal_bpm(settings.internal_bpm)  # Use settings BPM
print(f"      ✓ Clock ready (Internal: {settings.internal_bpm} BPM, External: USB)")

print("\n" + "="*60)
print("SYSTEM READY")
print("="*60)
print("Button A (short):  Previous pattern")
print("Button A+C (long): Settings menu")
print("Button B:          Demo arpeggio")
print("Button C (short):  Next pattern")
print("MIDI IN:           Send notes to arpeggiate")
print("Clock:             " + settings.get_clock_source_name())
if DEBUG_MEMORY:
    print(f"[DEBUG] Post-init memory: {gc.mem_free()} bytes free")
print("-"*60 + "\n")

# =============================================================================
# Arpeggiator State
# =============================================================================

# Note buffer (stores held notes)
note_buffer = []  # List of (note, velocity) tuples

# Arpeggiator state
current_step = 0
arp_sequence = []

# Currently playing note (for note-off)
current_playing_note = None

# Pre-allocate demo chord (C major: C, E, G) - avoid allocations in button handler
DEMO_CHORD = [(60, 100), (64, 100), (67, 100)]

def generate_arp_sequence(notes):
    """Generate arpeggiated sequence from note buffer based on current pattern"""
    if not notes:
        return []

    note_nums = sorted([n for n, v in notes])  # Just note numbers, sorted

    # Use settings pattern
    if settings.pattern == Settings.ARP_UP:
        return note_nums
    elif settings.pattern == Settings.ARP_DOWN:
        return list(reversed(note_nums))
    elif settings.pattern == Settings.ARP_UP_DOWN:
        return note_nums + list(reversed(note_nums[1:-1])) if len(note_nums) > 2 else note_nums
    elif settings.pattern == Settings.ARP_DOWN_UP:
        return list(reversed(note_nums)) + note_nums[1:-1] if len(note_nums) > 2 else list(reversed(note_nums))
    elif settings.pattern == Settings.ARP_RANDOM:
        # random imported at module level - no memory allocation here
        shuffled = note_nums.copy()
        random.shuffle(shuffled)
        return shuffled
    else:
        # Default to UP for any unhandled pattern
        return note_nums

def on_clock_step():
    """
    Callback function triggered by ClockHandler on each arpeggiator step
    Plays the next note in the sequence
    """
    global current_step, current_playing_note

    if not arp_sequence:
        return

    # Bounds check: ensure current_step is valid
    if current_step >= len(arp_sequence):
        current_step = 0

    # Send note off for previous note
    if current_playing_note is not None:
        midi.send(NoteOff(current_playing_note, 0))

    # Get next note in sequence
    try:
        note_to_play = arp_sequence[current_step]
        velocity = 100  # Could use velocity from buffer

        # Send note on
        midi.send(NoteOn(note_to_play, velocity))
        current_playing_note = note_to_play

        # Advance step
        current_step = (current_step + 1) % len(arp_sequence)

    except IndexError as e:
        print(f"ERROR: Index out of range - step:{current_step} len:{len(arp_sequence)}")
        current_step = 0  # Reset on error

# Configure clock handler
clock.set_step_callback(on_clock_step)
clock.set_clock_division(settings.clock_division)  # Use settings division
clock.set_clock_source(settings.clock_source)  # Use settings clock source

# Start clock if internal
if settings.clock_source == Settings.CLOCK_INTERNAL:
    clock.start()

# Update display with initial state
time.sleep(1)  # Let startup message show
clock_src_label = settings.get_clock_source_short()
display.update_display(clock.get_bpm(), settings.get_pattern_name(), clock.is_running(), clock_src_label)

# =============================================================================
# Main Loop
# =============================================================================

loop_count = 0
last_display_update = time.monotonic()
display_update_interval = 0.1  # Update display every 100ms
gc_counter = 0
gc_interval = 100  # Run garbage collection every 100 loops (~100ms)
button_cooldown_end = 0.0  # Cooldown timer to prevent demo after settings exit

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

            # Reset step to prevent index errors when sequence shrinks
            if note_buffer:
                current_step = min(current_step, len(arp_sequence) - 1)
            else:
                current_step = 0
                # Send note off if we were playing
                if current_playing_note is not None:
                    midi.send(NoteOff(current_playing_note, 0))
                    current_playing_note = None

            print(f"Note OFF: {msg.note} - Buffer: {[n for n,v in note_buffer]}")

        else:
            # Pass through all other MIDI messages with zero latency
            # This includes: Pitch Bend, Mod Wheel, CC, Aftertouch, Program Change, etc.
            # Only Note On/Off are filtered (used for arpeggiator, not echoed back)

            # Handle real-time MIDI messages (now properly recognized by library)
            if isinstance(msg, (TimingClock, Start, Stop, Continue, ActiveSensing, MtcQuarterFrame)):
                # Real-time messages: Clock, Start, Stop, Continue, Active Sensing, MTC
                try:
                    midi.send(msg)
                    # Log only important transport messages (not chatty clock/sensing)
                    if isinstance(msg, Start):
                        print(f"Pass-through: MIDI Start")
                    elif isinstance(msg, Stop):
                        print(f"Pass-through: MIDI Stop")
                    elif isinstance(msg, Continue):
                        print(f"Pass-through: MIDI Continue")
                    elif isinstance(msg, MtcQuarterFrame):
                        print(f"Pass-through: MTC Quarter Frame")
                    # TimingClock and ActiveSensing are too frequent - don't log
                except Exception as e:
                    print(f"⚠️  Failed real-time pass: {type(msg).__name__}: {e}")

            elif isinstance(msg, (MIDIUnknownEvent, MIDIBadEvent)):
                # Unknown or unparseable MIDI events - fall back to raw byte pass-through
                try:
                    if isinstance(msg, MIDIUnknownEvent):
                        uart.write(bytes([msg.status]))
                        print(f"Pass-through (raw): Unknown MIDI 0x{msg.status:02X}")
                    else:  # MIDIBadEvent
                        uart.write(msg.data)
                        print(f"Pass-through (raw): Bad MIDI event ({len(msg.data)} bytes)")
                except Exception as e:
                    print(f"⚠️  Failed raw pass-through: {e}")
            else:
                # Normal MIDI messages - send via library
                try:
                    midi.send(msg)
                    # Verbose debug (can be removed later)
                    if isinstance(msg, PitchBend):
                        print(f"Pass-through: PitchBend {msg.pitch_bend}")
                    elif isinstance(msg, ControlChange):
                        print(f"Pass-through: CC#{msg.control} = {msg.value}")
                    elif isinstance(msg, ProgramChange):
                        print(f"Pass-through: Program Change {msg.patch}")
                    else:
                        print(f"Pass-through: {type(msg).__name__}")
                except (TypeError, AttributeError) as e:
                    # Some MIDI messages can be received but not sent by adafruit_midi library
                    print(f"⚠️  Failed to send {type(msg).__name__}: {e}")

    # -------------------------------------------------------------------------
    # Clock Processing
    # -------------------------------------------------------------------------
    # Process clock - will call on_clock_step() callback when it's time to play next note
    clock.process_clock_messages()

    # -------------------------------------------------------------------------
    # Button Input & Menu Handling
    # -------------------------------------------------------------------------
    button_a, button_b, button_c, button_ac_combo, a_long, b_long, ac_long = buttons.check_buttons()

    if menu.menu_active:
        # Menu navigation mode
        if button_a:
            menu.navigate_previous()
        if button_c:
            menu.navigate_next()
        if button_b:
            menu.select()
            # Check if we exited menu after selecting (B at VALUE level)
            if not menu.menu_active:
                display.exit_settings_menu()
                # Show "SETTINGS SAVED!" confirmation if flag is set
                if menu.show_saved_confirmation:
                    display.show_status("SETTINGS SAVED!", 2.0)  # Show for 2 seconds
                    menu.show_saved_confirmation = False
                    # Set cooldown to prevent demo from triggering if B still held
                    button_cooldown_end = current_time + 0.5  # 500ms cooldown
                # Refresh main display
                clock_src_label = settings.get_clock_source_short()
                display.update_display(clock.get_bpm(), settings.get_pattern_name(), clock.is_running(), clock_src_label)
                print("Settings saved and exited menu")
        if ac_long:
            # Long press A+C: Exit settings menu
            menu.exit_menu()
            display.exit_settings_menu()
            # Refresh main display
            clock_src_label = settings.get_clock_source_short()
            display.update_display(clock.get_bpm(), settings.get_pattern_name(), clock.is_running(), clock_src_label)
            print("Exited settings menu")
        elif a_long:
            menu.back()
            # Check if we exited the menu
            if not menu.menu_active:
                display.exit_settings_menu()
                # Refresh main display
                clock_src_label = settings.get_clock_source_short()
                display.update_display(clock.get_bpm(), settings.get_pattern_name(), clock.is_running(), clock_src_label)

        # Update display with menu
        if menu.menu_active:
            line1, line2, line3 = menu.get_display_text()
            display.enter_settings_menu(line1, line2, line3)

        # Apply settings changes to clock handler
        if clock.get_clock_source() != settings.clock_source:
            # Clock source changed
            clock.set_clock_source(settings.clock_source)
            if settings.clock_source == Settings.CLOCK_INTERNAL:
                clock.start()
            print(f"Clock source: {settings.get_clock_source_name()}")

        if clock.internal_bpm != settings.internal_bpm:
            # BPM changed
            clock.set_internal_bpm(settings.internal_bpm)
            print(f"BPM: {settings.internal_bpm}")

    else:
        # Normal mode (not in menu)
        if ac_long:
            # Long press A+C: Enter settings menu
            menu.enter_menu()
            print("Entered settings menu")
        elif button_a:
            # Short press A: Previous pattern
            settings.pattern = (settings.pattern - 1) % 16
            arp_sequence = generate_arp_sequence(note_buffer)
            print(f"Pattern: {settings.get_pattern_name()}")
            clock_src_label = settings.get_clock_source_short()
            display.update_display(clock.get_bpm(), settings.get_pattern_name(), clock.is_running(), clock_src_label)
            settings.save()  # Auto-save pattern change

        if button_c:
            # Next pattern
            settings.next_pattern()
            arp_sequence = generate_arp_sequence(note_buffer)
            print(f"Pattern: {settings.get_pattern_name()}")
            clock_src_label = settings.get_clock_source_short()
            display.update_display(clock.get_bpm(), settings.get_pattern_name(), clock.is_running(), clock_src_label)
            settings.save()  # Auto-save pattern change

    # Button B: Demo arpeggio (only on main screen, not in menu, and after cooldown)
    if button_b and not menu.menu_active and current_time >= button_cooldown_end:
        # Demo: Play C major chord arpeggio
        print("Button B: Playing C major arpeggio demo")
        note_buffer = list(DEMO_CHORD)  # Use pre-allocated demo chord
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

    # -------------------------------------------------------------------------
    # Periodic Display Updates
    # -------------------------------------------------------------------------
    if not menu.menu_active and (current_time - last_display_update >= display_update_interval):
        clock_src_label = settings.get_clock_source_short()
        bpm = clock.get_bpm()  # Get current BPM (internal or detected external)
        is_running = clock.is_running()

        # Update display
        display.update_display(bpm, settings.get_pattern_name(), is_running, clock_src_label)

        last_display_update = current_time

    # -------------------------------------------------------------------------
    # Periodic Garbage Collection
    # -------------------------------------------------------------------------
    gc_counter += 1
    if gc_counter >= gc_interval:
        if DEBUG_MEMORY:
            mem_before = gc.mem_free()
        gc.collect()  # Clean up phantom objects and reduce fragmentation
        if DEBUG_MEMORY:
            mem_after = gc.mem_free()
            mem_freed = mem_after - mem_before
            if mem_freed > 0:
                print(f"[DEBUG] GC freed {mem_freed} bytes ({mem_after} bytes free)")
        gc_counter = 0

    # Small delay to prevent CPU spinning
    time.sleep(0.001)
