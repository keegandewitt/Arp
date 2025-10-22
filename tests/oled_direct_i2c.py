"""OLED Test - Direct I2C method (like oled_working_version.py) for 128x64"""

import board
import busio
import displayio
import terminalio
import time

print("\n" + "=" * 60)
print("OLED 128x64 TEST - Direct I2C Method")
print("=" * 60)

displayio.release_displays()

print("\n[1] Creating I2C bus...")
i2c = busio.I2C(board.SCL, board.SDA)
print("  ✓ I2C created")

print("\n[2] Importing SSD1306 driver...")
from adafruit_displayio_ssd1306 import SSD1306
print("  ✓ Driver imported")

print("\n[3] Creating display (128x64) with DIRECT I2C...")
# Pass I2C directly (NOT using display bus)
display = SSD1306(i2c, width=128, height=64, addr=0x3C)
print(f"  ✓ Display created: {display.width}x{display.height}")

# Set brightness to MAX
display.brightness = 1.0
print("  ✓ Brightness = 100%")

print("\n[4] Creating splash group...")
from adafruit_display_text import label

splash = displayio.Group()
print("  ✓ Group created")

print("\n[5] Adding text...")
text = label.Label(
    terminalio.FONT,
    text="HELLO WORLD!",
    color=0xFFFFFF,
    x=10,
    y=32  # Middle of 64px display
)
splash.append(text)
print("  ✓ Text added")

print("\n[6] Showing on display...")
display.root_group = splash
print("  ✓ DISPLAYED!")

print("\n" + "=" * 60)
print("CHECK OLED - Should show 'HELLO WORLD!' clearly")
print("=" * 60)

while True:
    time.sleep(1)
