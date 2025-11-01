"""
LED Blink Test - Visual confirmation code is running
No serial output needed - just watch the LED
"""

import board
import digitalio
import time

# Initialize onboard LED (D13)
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Blink pattern: 3 fast blinks = code is running
# If you see this pattern, CircuitPython is working

while True:
    # 3 fast blinks
    for _ in range(3):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)

    # Longer pause
    time.sleep(1.0)
