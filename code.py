"""
MIDI Arpeggiator - Main Application
For Adafruit M4 Express with two MIDI FeatherWings and OLED FeatherWing
"""

import board
import busio
import time
import digitalio
import supervisor
import alarm

# Import our modules
from settings import settings
from midi_io import MidiIO
from clock_handler import ClockHandler
from arpeggiator import Arpeggiator
from display import Display
from button_handler import ButtonHandler, PatternSelector, ClockSourceSelector


# Hardware Setup
# =============================================================================

# Configure UART for first MIDI FeatherWing (MIDI In/Out)
# Standard MIDI baud rate is 31250
# Timeout set to 0 for non-blocking immediate reads (minimal latency)
uart_midi = busio.UART(
    board.TX, board.RX,
    baudrate=31250,
    timeout=0  # Non-blocking for minimum latency
)

# Configure UART for second MIDI FeatherWing (MIDI Clock In)
# Using alternate pins - adjust based on your M4 Express pin configuration
# You may need to change these pins based on your wiring
uart_clock = busio.UART(
    board.D10, board.D11,  # TX, RX - adjust as needed
    baudrate=31250,
    timeout=0  # Non-blocking for minimum latency
)

# Configure I2C for OLED display
i2c = busio.I2C(board.SCL, board.SDA)

# Optional: Configure LED for visual feedback (disabled to save power)
# led = digitalio.DigitalInOut(board.D13)
# led.direction = digitalio.Direction.OUTPUT


# Initialize System Components
# =============================================================================

print("Initializing MIDI Arpeggiator...")

# Create MIDI I/O handler
midi_io = MidiIO(uart_midi, uart_midi)

# Create clock handler
clock = ClockHandler(uart_clock)

# Create arpeggiator
arp = Arpeggiator(settings, midi_io)

# Set clock division from settings
clock.set_clock_division(settings.clock_division)

# Set initial clock source and start if internal
clock.set_clock_source(settings.clock_source)
clock.set_internal_bpm(settings.internal_bpm)

# Connect clock to arpeggiator
clock.set_step_callback(arp.step)

# Initialize OLED display
display = Display(i2c)
display.show_startup()
time.sleep(1)  # Show startup message briefly

# Initialize buttons (FeatherWing OLED uses D9, D6, D5 for A, B, C)
buttons = ButtonHandler(board.D9, board.D6, board.D5)

# Initialize pattern selector
pattern_selector = PatternSelector(settings)

# Initialize clock source selector
clock_source_selector = ClockSourceSelector(settings)

print("Arpeggiator ready!")
print(f"Pattern: {settings.get_pattern_name()}")
print(f"Clock Division: {settings.clock_division} ticks")
print(f"Channel: {settings.midi_channel + 1}")
print("-" * 40)


# Main Loop
# =============================================================================
# OPTIMIZED FOR MINIMAL LATENCY
# - No sleep delays in main loop
# - Display updates only every 5000 loops (~5 seconds)
# - Debug prints only on user interactions
# - MIDI activity tracking uses flag instead of time.monotonic() in critical path
# - Power management checks happen outside MIDI processing loop

display_update_count = 0
display_sleep_check_count = 0
midi_indicator_update_count = 0

# Power management
battery_sleep_timeout = 60.0  # Sleep after 60 seconds of inactivity on battery
last_activity_time = time.monotonic()
power_check_count = 0
midi_activity_flag = False  # Track MIDI activity without time.monotonic() overhead

while True:
    # CRITICAL PATH: MIDI processing first for minimal latency
    # Process clock (internal generation or external MIDI clock)
    # Already optimized: external UART only polled when using external clock
    clock.process_clock_messages()

    # Read incoming MIDI messages
    messages = midi_io.read_messages()

    # Flag MIDI activity before processing (minimal overhead)
    if messages:
        midi_activity_flag = True

    # Process each message immediately
    for msg in messages:
        if settings.enabled:
            # Pass to arpeggiator
            arp.process_midi_message(msg)
        else:
            # Pass through directly when arp is disabled
            midi_io.process_passthrough([msg], settings.midi_channel)

    # NON-CRITICAL PATH: UI handling (lower priority)
    # Button handling
    button_a, button_b, button_c, button_ac_combo = buttons.check_buttons()

    # Track button activity for display wake/sleep and power management
    button_activity = button_a or button_b or button_c or button_ac_combo
    if button_activity:
        current_time = time.monotonic()
        display.record_activity(current_time)
        last_activity_time = current_time  # Update power management activity

    # Priority 1: Clock source selection mode
    if clock_source_selector.selection_active:
        if button_a or button_c:
            # Toggle clock source selection
            clock_source_selector.toggle_source()
            display.update_clock_source_selection(clock_source_selector.get_selected_source_name())

        if button_b:
            # Confirm clock source selection
            clock_source_selector.confirm_selection()

            # Apply clock source change
            clock.set_clock_source(settings.clock_source)
            if settings.clock_source == settings.CLOCK_INTERNAL:
                clock.set_internal_bpm(settings.internal_bpm)

            display.exit_clock_source_selection(confirmed=True)
            # Force display update on next loop
            display_update_count = 5000

    # Priority 2: Pattern selection mode
    elif pattern_selector.selection_active:
        if button_a:
            # Previous pattern
            pattern_selector.previous_pattern()
            display.update_pattern(pattern_selector.get_selected_pattern_name())

        if button_c:
            # Next pattern
            pattern_selector.next_pattern()
            display.update_pattern(pattern_selector.get_selected_pattern_name())

        if button_b:
            # Confirm selection
            pattern_selector.confirm_selection()
            arp._generate_sequence()  # Regenerate with new pattern
            display.exit_selection_mode(confirmed=True)
            # Force display update on next loop
            display_update_count = 5000

    # Priority 3: Normal mode
    else:
        # Check for A+C combo to enter clock source selection
        if button_ac_combo:
            clock_source_selector.start_selection()
            display.enter_clock_source_selection(clock_source_selector.get_selected_source_name())

        # Individual buttons enter pattern selection
        elif button_a or button_c:
            pattern_selector.start_selection()
            display.enter_selection_mode(pattern_selector.get_selected_pattern_name())

        # Button B also enters pattern selection
        elif button_b:
            pattern_selector.start_selection()
            display.enter_selection_mode(pattern_selector.get_selected_pattern_name())

    # Update MIDI activity indicators (every ~500 loops for responsiveness)
    # These are lightweight updates (just two small labels)
    midi_indicator_update_count += 1
    if midi_indicator_update_count >= 500:
        has_midi_in, has_midi_out = midi_io.get_and_clear_midi_activity()
        display.update_midi_indicators(has_midi_in, has_midi_out)
        midi_indicator_update_count = 0

    # Check display sleep status (every ~1000 loops = ~1 second)
    # Only check periodically to avoid constant time.monotonic() calls
    display_sleep_check_count += 1
    if display_sleep_check_count >= 1000:
        display.check_sleep(time.monotonic())
        display_sleep_check_count = 0

    # Power management: deep sleep on battery when inactive (every ~2000 loops)
    power_check_count += 1
    if power_check_count >= 2000:
        # Update activity timestamp if there was MIDI activity
        if midi_activity_flag:
            last_activity_time = time.monotonic()
            midi_activity_flag = False

        # Check if running on battery power
        if not supervisor.runtime.usb_connected:
            current_time = time.monotonic()
            inactive_time = current_time - last_activity_time

            # Enter deep sleep if inactive for too long
            if inactive_time >= battery_sleep_timeout:
                print(f"Battery powered, inactive for {inactive_time:.1f}s - entering deep sleep")

                # Stop all MIDI notes before sleeping
                midi_io.stop_all_notes(settings.midi_channel)

                # Put display to sleep
                display.sleep()

                # Create pin alarms for any button press to wake
                button_a_alarm = alarm.pin.PinAlarm(pin=board.D9, value=False, pull=True)
                button_b_alarm = alarm.pin.PinAlarm(pin=board.D6, value=False, pull=True)
                button_c_alarm = alarm.pin.PinAlarm(pin=board.D5, value=False, pull=True)

                # Enter deep sleep - will wake on button press
                # This drastically reduces power consumption to <1mA
                alarm.exit_and_deep_sleep_until_alarms(button_a_alarm, button_b_alarm, button_c_alarm)
                # After wake, the board will restart from the beginning

        power_check_count = 0

    # Update display much less frequently (every ~5000 loops = ~5 seconds)
    # Display updates are SLOW due to I2C communication
    # Skipped entirely if display is sleeping
    display_update_count += 1
    if display_update_count >= 5000:
        if not pattern_selector.selection_active and not clock_source_selector.selection_active:
            display.update_display(
                clock.get_bpm(),
                settings.get_pattern_name(),
                clock.is_running(),
                settings.get_clock_source_short()
            )
        display_update_count = 0

    # LED heartbeat disabled to save power (~2.5-5mA)
    # Extends battery life by approximately 10-15%

    # NO SLEEP DELAY - run as fast as possible for minimal MIDI latency
