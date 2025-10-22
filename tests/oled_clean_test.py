"""
Clean OLED Test - Simple static text display for 128x64
"""

import board
import displayio
import terminalio
import time
from adafruit_display_text import label

print("\n" + "=" * 60)
print("CLEAN OLED TEST - 128x64")
print("=" * 60)

# Release and initialize
displayio.release_displays()
i2c = board.I2C()

print("\nInitializing display...")
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

import adafruit_displayio_ssd1306
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Set brightness
display.brightness = 0.8
print("✓ Display initialized (128x64)")

# Create clean display group
splash = displayio.Group()

# Title at top
title = label.Label(
    terminalio.FONT,
    text="OLED Working!",
    color=0xFFFFFF,
    x=10,
    y=10
)
splash.append(title)

# Line 2
line2 = label.Label(
    terminalio.FONT,
    text="128x64 Display",
    color=0xFFFFFF,
    x=10,
    y=25
)
splash.append(line2)

# Line 3
line3 = label.Label(
    terminalio.FONT,
    text="CP 10.0.3",
    color=0xFFFFFF,
    x=10,
    y=40
)
splash.append(line3)

# Line 4
line4 = label.Label(
    terminalio.FONT,
    text="SUCCESS!",
    color=0xFFFFFF,
    x=10,
    y=55
)
splash.append(line4)

# Display it
display.root_group = splash
print("✓ Text displayed")

print("\n" + "=" * 60)
print("CHECK OLED - Should show:")
print("  OLED Working!")
print("  128x64 Display")
print("  CP 10.0.3")
print("  SUCCESS!")
print("=" * 60)

# Keep it on screen
while True:
    time.sleep(1)
