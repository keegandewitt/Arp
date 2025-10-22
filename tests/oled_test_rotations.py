"""
Test different rotation values to see if that affects the garbled display
"""

import board
import displayio
import terminalio
import time
import i2cdisplaybus
import adafruit_displayio_ssd1306
from adafruit_display_text import label

print("\n=== Testing Display Rotations ===\n")

displayio.release_displays()

i2c = board.I2C()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

# Test different rotations
rotations = [0, 90, 180, 270]

for rot in rotations:
    print(f"\n--- Testing rotation={rot} ---")

    # Create display with specific rotation
    display = adafruit_displayio_ssd1306.SSD1306(
        display_bus,
        width=128,
        height=64,
        rotation=rot
    )

    display.brightness = 1.0

    # Create simple text
    splash = displayio.Group()
    text = label.Label(
        terminalio.FONT,
        text=f"ROT {rot}",
        color=0xFFFFFF,
        x=30,
        y=32
    )
    splash.append(text)

    display.root_group = splash

    print(f"Displaying with rotation={rot}")
    print("Check display for 5 seconds...")
    time.sleep(5)

print("\n=== Test Complete ===")
print("Which rotation looked best?")

while True:
    time.sleep(1)
