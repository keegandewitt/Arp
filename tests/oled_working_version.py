"""OLED Test - Working version for CircuitPython 10.x"""

import board
import busio
import displayio
import terminalio
import time

print("\n" + "=" * 60)
print("OLED DISPLAY TEST - CircuitPython 10.x Compatible")
print("=" * 60)

displayio.release_displays()

print("\n[1] Creating I2C bus...")
i2c = busio.I2C(board.SCL, board.SDA)
print("  ✓ I2C created")

print("\n[2] Importing SSD1306 driver...")
from adafruit_displayio_ssd1306 import SSD1306
print("  ✓ Driver imported")

print("\n[3] Creating display (128x32)...")
# For CircuitPython 10.x, pass I2C directly to SSD1306
try:
    display = SSD1306(i2c, width=128, height=32, addr=0x3C)
    print(f"  ✓ Display created: {display.width}x{display.height}")
except Exception as e:
    print(f"  ✗ 128x32 failed: {e}")
    print("\n[3b] Trying 128x64...")
    display = SSD1306(i2c, width=128, height=64, addr=0x3C)
    print(f"  ✓ Display created: {display.width}x{display.height}")

print("\n[4] Creating splash group...")
from adafruit_display_text import label

splash = displayio.Group()
print("  ✓ Group created")

print("\n[5] Adding text 'HELLO OLED!'...")
text = label.Label(
    terminalio.FONT,
    text="HELLO OLED!",
    color=0xFFFFFF,
    x=5,
    y=15
)
splash.append(text)
print("  ✓ Text added")

print("\n[6] Showing on display...")
display.root_group = splash
print("  ✓ DISPLAYED!")

print("\n*** CHECK THE OLED SCREEN - Should show 'HELLO OLED!' ***")

time.sleep(2)

print("\n[7] Testing text update...")
text.text = "UPDATE OK!"
print("  ✓ Text changed to 'UPDATE OK!'")

time.sleep(2)

print("\n[8] Testing multiple lines...")
splash = displayio.Group()

line1 = label.Label(terminalio.FONT, text="Line 1", color=0xFFFFFF, x=5, y=5)
line2 = label.Label(terminalio.FONT, text="Line 2", color=0xFFFFFF, x=5, y=15)
line3 = label.Label(terminalio.FONT, text="Line 3", color=0xFFFFFF, x=5, y=25)

splash.append(line1)
splash.append(line2)
splash.append(line3)

display.root_group = splash
print("  ✓ Multiple lines displayed")

time.sleep(2)

print("\n[9] Final test - 'PASS!'...")
splash = displayio.Group()
pass_text = label.Label(
    terminalio.FONT,
    text="PASS!",
    color=0xFFFFFF,
    x=40,
    y=15
)
splash.append(pass_text)
display.root_group = splash
print("  ✓ PASS displayed")

print("\n" + "=" * 60)
print("✓✓✓ OLED TEST COMPLETE ✓✓✓")
print("=" * 60)
print("\nOLED FeatherWing is WORKING!")
print("Display will stay on showing 'PASS!'")

while True:
    time.sleep(1)
