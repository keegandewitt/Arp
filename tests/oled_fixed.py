"""OLED Test - Fixed parameter name"""

import board
import busio
import displayio
import terminalio
import time

print("\n" + "=" * 60)
print("OLED DISPLAY TEST - Parameter Fix")
print("=" * 60)

displayio.release_displays()

print("\n[1] Creating I2C bus...")
i2c = busio.I2C(board.SCL, board.SDA)
print("  ✓ I2C created")

print("\n[2] Importing SSD1306 driver...")
from adafruit_displayio_ssd1306 import SSD1306
print("  ✓ Driver imported")

print("\n[3] Creating display (128x32)...")
try:
    display = SSD1306(i2c, width=128, height=32, address=0x3C)
    print(f"  ✓ Display created: {display.width}x{display.height}")
except Exception as e:
    print(f"  ✗ 128x32 failed: {e}")
    print("\n[3b] Trying 128x64...")
    try:
        display = SSD1306(i2c, width=128, height=64, address=0x3C)
        print(f"  ✓ Display created: {display.width}x{display.height}")
    except Exception as e2:
        print(f"  ✗ Both sizes failed!")
        print(f"     Error: {e2}")
        print("\n[3c] Trying without address parameter...")
        try:
            display = SSD1306(i2c, width=128, height=32)
            print(f"  ✓ Display created: {display.width}x{display.height}")
        except Exception as e3:
            print(f"  ✗ That failed too: {e3}")
            print("\nStopping - check library version")
            while True:
                time.sleep(1)

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

print("\n*** CHECK THE OLED SCREEN NOW! ***")

time.sleep(2)

print("\n[7] Testing text update...")
text.text = "IT WORKS!"
print("  ✓ Text changed to 'IT WORKS!'")

time.sleep(2)

print("\n[8] Final 'PASS!'...")
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
print("✓✓✓ OLED WORKING! ✓✓✓")
print("=" * 60)

while True:
    time.sleep(1)
