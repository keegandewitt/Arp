"""
⚠️  DEPLOYMENT WARNING ⚠️
=======================
This file (main_v2.py) is the Translation Hub VERSION.
Once tested, this will replace main.py as the SOURCE OF TRUTH.

To deploy changes:
    python3 scripts/deploy.py

=======================

prisme - MIDI/CV Translation Hub
Main application entry point (Translation Hub Architecture)

Hardware:
- Adafruit Feather M4 CAN Express
- Adafruit MIDI FeatherWing (UART TX/RX)
- Adafruit OLED FeatherWing 128x64 (I2C)
- MCP4728 DAC (CV Output)

Translation Hub Features:
- Multiple input sources (MIDI IN, USB MIDI)
- Configurable layer ordering (Scale → Arp OR Arp → Scale)
- Routing modes (THRU = pass-through, TRANSLATION = layer processing)
- Clock transformations (swing, multiply, divide)
- CV/Gate output with custom CC mapping
- Zero-latency MIDI pass-through for non-note messages
"""

# =============================================================================
# Version Information
# =============================================================================
__version__ = "1.0.0-alpha"
__build_date__ = "2025-11-01"
__hardware_version__ = "1.0"

import board
import busio
import time
import digitalio
import usb_midi
import gc
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
from arp.drivers.cv_gate import CVOutput
from arp.drivers.midi_custom_cc import CustomCCHandler
from arp.drivers.midi_output import MidiIO
from arp.core.arpeggiator import Arpeggiator
from arp.core.translation import TranslationPipeline
from arp.core.input_router import InputRouter

print("\n" + "="*60)
print(f"prisme - MIDI/CV Translation Hub v{__version__}")
print(f"Build: {__build_date__} | Hardware: v{__hardware_version__}")
print("="*60)

# =============================================================================
# Configuration
# =============================================================================

# Enable memory monitoring for debugging
DEBUG_MEMORY = False

if DEBUG_MEMORY:
    print(f"[DEBUG] Startup memory: {gc.mem_free()} bytes free")

# =============================================================================
# Hardware Initialization
# =============================================================================

print("[1/8] Initializing MIDI UART...")
# MIDI FeatherWing on UART (TX=D1, RX=D0)
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi_uart = MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("      ✓ MIDI UART ready (31250 baud)")

print("[2/8] Initializing USB MIDI...")
# USB MIDI for notes and clock
midi_usb = MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], in_channel=0, out_channel=0)
print("      ✓ USB MIDI ready")

print("[3/8] Initializing Display...")
# OLED FeatherWing on I2C
i2c = board.I2C()
display = Display(i2c)
display.show_startup(version=__version__)
print("      ✓ Display ready (SH1107 128x64)")

print("[4/8] Initializing Buttons...")
# Buttons on OLED FeatherWing (D9=A, D6=B, D5=C)
buttons = ButtonHandler(board.D9, board.D6, board.D5)
print("      ✓ Buttons ready (A, B, C)")

print("[5/8] Initializing Settings...")
# Global settings object
settings = Settings()
settings.load()
menu = SettingsMenu(settings)
print("      ✓ Settings ready")

print("[6/8] Initializing Clock...")
# Clock handler with configurable transformations (swing, multiply, divide)
# USB MIDI used for external clock
clock = ClockHandler(
    midi_in_port=usb_midi.ports[0],
    swing_percent=settings.swing_percent,
    multiply=settings.clock_multiply,
    divide=settings.clock_divide
)
clock.set_internal_bpm(settings.internal_bpm)
print(f"      ✓ Clock ready (Internal: {settings.internal_bpm} BPM)")
print(f"      ✓ Swing: {settings.swing_percent}%, Multiply: {settings.clock_multiply}x, Divide: 1/{settings.clock_divide}")

print("[7/8] Initializing CV Output...")
# CV Output via MCP4728 DAC on I2C
cv_output = CVOutput(i2c, settings)
print("      ✓ CV Output ready (MCP4728 on I2C)")

print("[8/8] Initializing Custom CC Handler...")
# Custom CC MIDI-to-CV handler
custom_cc = CustomCCHandler(cv_output, settings)
print("      ✓ Custom CC Handler ready")

# =============================================================================
# Translation Hub Components
# =============================================================================

print("\n" + "-"*60)
print("INITIALIZING TRANSLATION HUB...")
print("-"*60)

print("[Hub 1/4] Initializing MIDI I/O...")
# MidiIO wrapper for UART output
midi_io = MidiIO(uart, uart)
print("      ✓ MIDI I/O ready")

print("[Hub 2/4] Initializing Arpeggiator...")
# Class-based arpeggiator
arpeggiator = Arpeggiator(settings, midi_io, cv_output)
print("      ✓ Arpeggiator ready")

print("[Hub 3/4] Initializing Translation Pipeline...")
# Translation pipeline for layer processing
pipeline = TranslationPipeline(settings, arpeggiator)
print(f"      ✓ Pipeline ready ({pipeline.get_layer_count()} layers)")
print(f"      ✓ Layer order: {' → '.join(pipeline.get_layer_names())}")

print("[Hub 4/4] Initializing Input Router...")
# Input router for source selection
input_router = InputRouter(settings, midi_uart, midi_usb)
print(f"      ✓ Input router ready (Source: {input_router.get_current_source_name()})")

print("-"*60)
print(f"Routing Mode: {settings.get_routing_mode_name()}")
print(f"Input Source: {input_router.get_current_source_name()}")
print(f"Layer Order: {' → '.join(pipeline.get_layer_names())}")
print("-"*60)

# Configure clock handler
def on_clock_step():
    """Clock callback - triggers arpeggiator step"""
    arpeggiator.step()

clock.set_step_callback(on_clock_step)
clock.set_clock_division(settings.clock_division)
clock.set_clock_source(settings.clock_source)

# Start clock if internal
if settings.clock_source == Settings.CLOCK_INTERNAL:
    clock.start()

print("\n" + "="*60)
print("SYSTEM READY")
print("="*60)
print("Button A (short):  Previous pattern")
print("Button A+C (long): Settings menu")
print("Button B:          Demo arpeggio")
print("Button C (short):  Next pattern")
print("MIDI IN:           Send notes to process")
print("Routing Mode:      " + settings.get_routing_mode_name())
print("Input Source:      " + input_router.get_current_source_name())
print("Clock:             " + settings.get_clock_source_name())
if DEBUG_MEMORY:
    print(f"[DEBUG] Post-init memory: {gc.mem_free()} bytes free")
print("-"*60 + "\n")

# Update display with initial state
time.sleep(1)
display.update_translation_display(settings)

# =============================================================================
# Main Loop
# =============================================================================

loop_count = 0
last_display_update = time.monotonic()
display_update_interval = 0.1
gc_counter = 0
gc_interval = 100
button_cooldown_end = 0.0

# Pre-allocate demo chord (C major: C, E, G)
DEMO_CHORD = [(60, 100), (64, 100), (67, 100)]

while True:
    loop_count += 1
    current_time = time.monotonic()

    # -------------------------------------------------------------------------
    # MIDI Input Processing (Translation Hub Architecture)
    # -------------------------------------------------------------------------
    msg = input_router.get_midi_message()
    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            # Note On received
            if settings.routing_mode == Settings.ROUTING_THRU:
                # THRU mode: Pass through directly
                midi_io.send_note_on(msg.note, msg.velocity, settings.midi_channel)
            else:
                # TRANSLATION mode: Process through pipeline
                pipeline.process_note_on(msg.note, msg.velocity)

            print(f"Note ON: {msg.note} (velocity {msg.velocity})")

        elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            # Note Off received
            if settings.routing_mode == Settings.ROUTING_THRU:
                # THRU mode: Pass through directly
                midi_io.send_note_off(msg.note, settings.midi_channel)
            else:
                # TRANSLATION mode: Process through pipeline
                pipeline.process_note_off(msg.note)

            print(f"Note OFF: {msg.note}")

        else:
            # Process for Custom CC output FIRST
            custom_cc.process_messages([msg])

            # Pass through all other MIDI messages (zero latency)
            # This includes: Pitch Bend, Mod Wheel, CC, Aftertouch, etc.

            if isinstance(msg, (TimingClock, Start, Stop, Continue, ActiveSensing, MtcQuarterFrame)):
                # Real-time messages
                try:
                    midi_uart.send(msg)
                    if isinstance(msg, Start):
                        print(f"Pass-through: MIDI Start")
                    elif isinstance(msg, Stop):
                        print(f"Pass-through: MIDI Stop")
                    elif isinstance(msg, Continue):
                        print(f"Pass-through: MIDI Continue")
                except Exception as e:
                    print(f"⚠️  Failed real-time pass: {type(msg).__name__}: {e}")

            elif isinstance(msg, (MIDIUnknownEvent, MIDIBadEvent)):
                # Unknown/bad events - raw byte pass-through
                try:
                    if isinstance(msg, MIDIUnknownEvent):
                        uart.write(bytes([msg.status]))
                        print(f"Pass-through (raw): Unknown MIDI 0x{msg.status:02X}")
                    else:
                        uart.write(msg.data)
                        print(f"Pass-through (raw): Bad MIDI event ({len(msg.data)} bytes)")
                except Exception as e:
                    print(f"⚠️  Failed raw pass-through: {e}")
            else:
                # Normal MIDI messages
                try:
                    midi_uart.send(msg)
                    if isinstance(msg, PitchBend):
                        print(f"Pass-through: PitchBend {msg.pitch_bend}")
                    elif isinstance(msg, ControlChange):
                        print(f"Pass-through: CC#{msg.control} = {msg.value}")
                    elif isinstance(msg, ProgramChange):
                        print(f"Pass-through: Program Change {msg.patch}")
                except (TypeError, AttributeError) as e:
                    print(f"⚠️  Failed to send {type(msg).__name__}: {e}")

    # -------------------------------------------------------------------------
    # Clock Processing
    # -------------------------------------------------------------------------
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
            if not menu.menu_active:
                display.exit_settings_menu()
                if menu.show_saved_confirmation:
                    display.show_status("SETTINGS SAVED!", 2.0)
                    menu.show_saved_confirmation = False
                    button_cooldown_end = current_time + 0.5

                # Apply settings changes
                pipeline.reconfigure()
                clock.set_swing(settings.swing_percent)
                clock.set_multiply(settings.clock_multiply)
                clock.set_divide(settings.clock_divide)

                display.update_translation_display(settings)
                print("Settings saved and exited menu")

        if ac_long:
            menu.exit_menu()
            display.exit_settings_menu()
            display.update_translation_display(settings)
            print("Exited settings menu")
        elif a_long:
            menu.back()
            if not menu.menu_active:
                display.exit_settings_menu()
                display.update_translation_display(settings)

        if b_long and menu.current_category == menu.CATEGORY_CUSTOM_CC:
            custom_cc.enter_learn_mode()
            print("[Learn Mode] Activated - send a CC message to capture")

        if menu.menu_active:
            line1, line2, line3 = menu.get_display_text()
            display.enter_settings_menu(line1, line2, line3)

        # Apply settings changes to clock handler
        if clock.get_clock_source() != settings.clock_source:
            clock.set_clock_source(settings.clock_source)
            if settings.clock_source == Settings.CLOCK_INTERNAL:
                clock.start()
            print(f"Clock source: {settings.get_clock_source_name()}")

        if clock.internal_bpm != settings.internal_bpm:
            clock.set_internal_bpm(settings.internal_bpm)
            print(f"BPM: {settings.internal_bpm}")

    else:
        # Normal mode (not in menu)
        if ac_long:
            menu.enter_menu()
            print("Entered settings menu")
        elif button_a:
            settings.pattern = (settings.pattern - 1) % 16
            print(f"Pattern: {settings.get_pattern_name()}")
            display.update_translation_display(settings)
            settings.save()

        if button_c:
            settings.next_pattern()
            print(f"Pattern: {settings.get_pattern_name()}")
            display.update_translation_display(settings)
            settings.save()

    # Button B: Demo arpeggio
    if button_b and not menu.menu_active and current_time >= button_cooldown_end:
        print("Button B: Playing C major arpeggio demo")

        if settings.routing_mode == Settings.ROUTING_TRANSLATION:
            # Use arpeggiator in TRANSLATION mode
            for note, velocity in DEMO_CHORD:
                arpeggiator.add_note(note, velocity)

            # Play for 4 beats then clear
            demo_start = time.monotonic()
            while time.monotonic() - demo_start < 2.0:
                clock.process_clock_messages()
                time.sleep(0.001)

            # Clear demo notes
            arpeggiator.clear_notes()
        else:
            # THRU mode: Play chord directly
            for note, velocity in DEMO_CHORD:
                midi_io.send_note_on(note, velocity, settings.midi_channel)
                time.sleep(0.12)
                midi_io.send_note_off(note, settings.midi_channel)
                time.sleep(0.005)

    # -------------------------------------------------------------------------
    # Periodic Display Updates
    # -------------------------------------------------------------------------
    if not menu.menu_active and (current_time - last_display_update >= display_update_interval):
        display.update_translation_display(settings)
        last_display_update = current_time

    # -------------------------------------------------------------------------
    # Periodic Garbage Collection
    # -------------------------------------------------------------------------
    gc_counter += 1
    if gc_counter >= gc_interval:
        if DEBUG_MEMORY:
            mem_before = gc.mem_free()
        gc.collect()
        if DEBUG_MEMORY:
            mem_after = gc.mem_free()
            mem_freed = mem_after - mem_before
            if mem_freed > 0:
                print(f"[DEBUG] GC freed {mem_freed} bytes ({mem_after} bytes free)")
        gc_counter = 0

    # Small delay to prevent CPU spinning
    time.sleep(0.001)
