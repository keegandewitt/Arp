"""
Clean button test with static display and long press detection
- Shows button states on one line (no scrolling)
- Detects long presses (3 seconds)
- Shows combinations
"""

import board
import digitalio
import time

# Initialize buttons
button_a = digitalio.DigitalInOut(board.D9)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.D6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

button_c = digitalio.DigitalInOut(board.D5)
button_c.direction = digitalio.Direction.INPUT
button_c.pull = digitalio.Pull.UP

print("=== Button Test: Long Press & Combinations ===")
print("A=D9, B=D6, C=D5")
print("Long press threshold: 0.5 seconds")
print("")

# Track press times and states
press_times = {'A': None, 'B': None, 'C': None}
last_states = {'A': True, 'B': True, 'C': True}
long_press_detected = {'A': False, 'B': False, 'C': False}
LONG_PRESS_THRESHOLD = 0.5  # Standard long press: 0.5 seconds

while True:
    # Read current button states
    current_states = {
        'A': button_a.value,
        'B': button_b.value,
        'C': button_c.value
    }

    current_time = time.monotonic()

    # Build status line
    status_parts = []
    pressed_buttons = []
    long_presses = []

    for btn_name in ['A', 'B', 'C']:
        is_pressed = not current_states[btn_name]  # Inverted: False = pressed
        was_pressed = not last_states[btn_name]

        # Button just pressed
        if is_pressed and not was_pressed:
            press_times[btn_name] = current_time
            long_press_detected[btn_name] = False

        # Button released
        elif not is_pressed and was_pressed:
            press_times[btn_name] = None
            long_press_detected[btn_name] = False

        # Button being held
        if is_pressed:
            pressed_buttons.append(btn_name)

            if press_times[btn_name]:
                hold_time = current_time - press_times[btn_name]

                # Check for long press
                if hold_time >= LONG_PRESS_THRESHOLD and not long_press_detected[btn_name]:
                    long_presses.append(btn_name)
                    long_press_detected[btn_name] = True

                status_parts.append(f"{btn_name}:PRESS({hold_time:.1f}s)")
            else:
                status_parts.append(f"{btn_name}:PRESS")
        else:
            status_parts.append(f"{btn_name}:---")

        last_states[btn_name] = current_states[btn_name]

    # Build display line
    line = " | ".join(status_parts)

    # Add combination indicator
    if len(pressed_buttons) > 1:
        line += f" | COMBO: {'+'.join(pressed_buttons)}"

    # Add long press indicator
    if long_presses:
        line += f" | LONG: {'+'.join(long_presses)}"

    # Print with carriage return (overwrites same line)
    print(f"\r{line}                    ", end='')

    time.sleep(0.1)
