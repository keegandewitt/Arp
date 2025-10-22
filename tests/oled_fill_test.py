"""
OLED Fill Test - Fill entire screen white to verify display is working
"""

import board
import displayio
import time

print("\n" + "=" * 60)
print("OLED FILL TEST - Fill entire screen")
print("=" * 60)

displayio.release_displays()
i2c = board.I2C()

print("\nInitializing display...")
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

import adafruit_displayio_ssd1306
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

print("✓ Display created")

# Set brightness to absolute MAX
display.brightness = 1.0
print("✓ Brightness set to 100%")

# Create a bitmap that fills the entire screen with white
import displayio
import terminalio
from adafruit_display_text import label

# Method 1: Try with a large text label
splash = displayio.Group()

# Fill with multiple lines of text
for y_pos in range(5, 30, 10):
    text = label.Label(
        terminalio.FONT,
        text="X" * 20,  # Fill with X characters
        color=0xFFFFFF,
        x=0,
        y=y_pos
    )
    splash.append(text)

display.root_group = splash
print("✓ Screen filled with text")

print("\n" + "=" * 60)
print("CHECK THE OLED NOW - Should be FILLED with X characters")
print("If you see NOTHING:")
print("  1. Check FeatherWing is seated properly")
print("  2. Check I2C connections (SDA/SCL)")
print("  3. Try reseating the FeatherWing")
print("  4. Check for bent or missing header pins")
print("=" * 60)

while True:
    time.sleep(1)
