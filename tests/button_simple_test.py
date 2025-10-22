"""
Simple button test - just prints when buttons change state
"""

import board
import digitalio
import time

print("=== Simple Button Test ===")
print("Starting...")

# Try buttons on D9, D6, D5
button_a = digitalio.DigitalInOut(board.D9)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.D6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

button_c = digitalio.DigitalInOut(board.D5)
button_c.direction = digitalio.Direction.INPUT
button_c.pull = digitalio.Pull.UP

print("Buttons initialized")
print("A=D9, B=D6, C=D5")
print("Monitoring... press buttons!")
print("")

while True:
    a_val = button_a.value
    b_val = button_b.value
    c_val = button_c.value

    print(f"A:{a_val} B:{b_val} C:{c_val}")
    time.sleep(0.5)
