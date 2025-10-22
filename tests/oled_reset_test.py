"""
OLED Reset Test - Properly initialize and clear display
"""

import board
import displayio
import terminalio
import time
from adafruit_display_text import label

print("\n" + "=" * 60)
print("OLED RESET AND INITIALIZATION TEST")
print("=" * 60)

# CRITICAL: Release displays first
print("\n[1] Releasing displays...")
displayio.release_displays()
time.sleep(0.5)  # Give it time to release
print("  ✓ Released")

# Get I2C
print("\n[2] Getting I2C bus...")
i2c = board.I2C()
print("  ✓ I2C obtained")

# Create display bus
print("\n[3] Creating display bus...")
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
print("  ✓ Bus created")

# Initialize display
print("\n[4] Initializing SSD1306 (128x64)...")
import adafruit_displayio_ssd1306
display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=128,
    height=64,
    rotation=0  # Ensure no rotation
)
print("  ✓ Display initialized")

# Turn on display (in case it was sleeping)
print("\n[5] Waking display...")
display.sleep = False
print("  ✓ Display awake")

# Set brightness to max
print("\n[6] Setting brightness to maximum...")
display.brightness = 1.0
print("  ✓ Brightness = 100%")

# Create EMPTY group first to clear screen
print("\n[7] Clearing display...")
empty_group = displayio.Group()
display.root_group = empty_group
time.sleep(0.5)  # Let it clear
print("  ✓ Display cleared")

# Now create content
print("\n[8] Creating text...")
splash = displayio.Group()

# Single line of text in the middle
text = label.Label(
    terminalio.FONT,
    text="HELLO OLED!",
    color=0xFFFFFF,
    x=20,
    y=32  # Middle of 64-pixel display
)
splash.append(text)

print("  ✓ Text created")

# Display it
print("\n[9] Showing text on display...")
display.root_group = splash
print("  ✓ DISPLAYED")

print("\n" + "=" * 60)
print("CHECK OLED NOW - Should show 'HELLO OLED!' clearly")
print("If still garbled, there may be a hardware reset issue")
print("=" * 60)

while True:
    time.sleep(1)
