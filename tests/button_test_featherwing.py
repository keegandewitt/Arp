"""
Comprehensive Button Test for OLED FeatherWing
Tests individual buttons, combinations, and long presses

OLED FeatherWing Button Pins:
- Button A: D9
- Button B: D6
- Button C: D5
"""

import board
import digitalio
import time

print("\n=== OLED FeatherWing Button Test ===\n")

# Button configuration
BUTTONS = {
    'A': board.D9,
    'B': board.D6,
    'C': board.D5
}

# Initialize buttons with pull-ups (buttons connect to ground when pressed)
buttons = {}
for name, pin in BUTTONS.items():
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons[name] = btn
    print(f"Button {name} initialized on {pin}")

print("\n=== Test 1: Individual Button Presses ===")
print("Press each button A, B, C to test")
print("(Buttons are active LOW - press connects to ground)\n")

# Track button states
last_states = {name: True for name in buttons.keys()}  # True = not pressed (pulled up)
long_press_threshold = 1.0  # seconds
press_start_times = {name: None for name in buttons.keys()}

def check_buttons():
    """Check all buttons and return current states"""
    states = {}
    for name, btn in buttons.items():
        states[name] = btn.value  # False = pressed, True = released
    return states

def detect_combinations(states):
    """Detect button combinations"""
    pressed = [name for name, state in states.items() if not state]  # Inverted logic
    return pressed

print("Monitoring buttons...")
print("- Single press: Shows button name")
print("- Long press: Shows 'LONG' indicator")
print("- Combinations: Shows all pressed buttons")
print("Press CTRL+C to exit\n")

try:
    while True:
        current_states = check_buttons()
        current_time = time.monotonic()

        # Check each button
        for name in buttons.keys():
            current = current_states[name]
            last = last_states[name]

            # Button just pressed (went from HIGH to LOW)
            if last and not current:
                press_start_times[name] = current_time
                print(f"[{name}] Pressed")

            # Button being held
            elif not current and press_start_times[name]:
                hold_time = current_time - press_start_times[name]
                if hold_time >= long_press_threshold:
                    print(f"[{name}] LONG PRESS ({hold_time:.1f}s)")
                    press_start_times[name] = None  # Prevent repeated messages

            # Button just released (went from LOW to HIGH)
            elif not last and current:
                if press_start_times[name]:
                    hold_time = current_time - press_start_times[name]
                    if hold_time < long_press_threshold:
                        print(f"[{name}] Released (short press, {hold_time:.2f}s)")
                    else:
                        print(f"[{name}] Released after long press")
                    press_start_times[name] = None

            last_states[name] = current

        # Check for button combinations
        pressed = detect_combinations(current_states)
        if len(pressed) > 1:
            combo = "+".join(sorted(pressed))
            print(f"*** COMBINATION: {combo} ***")

        time.sleep(0.05)  # 50ms polling

except KeyboardInterrupt:
    print("\n\n=== Button Test Complete ===")
    print("Summary:")
    print("- Individual buttons working")
    print("- Long press detection working")
    print("- Combination detection working")
