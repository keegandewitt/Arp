"""OLED Test - Try all possible initialization methods"""

import board
import busio
import displayio
import time

print("\n" + "=" * 60)
print("OLED INIT - Trying All Methods")
print("=" * 60)

displayio.release_displays()

print("\n[1] Creating I2C...")
i2c = busio.I2C(board.SCL, board.SDA)
print("  ✓ I2C created")

print("\n[2] Importing library...")
from adafruit_displayio_ssd1306 import SSD1306
print("  ✓ Imported")

print("\n[3] Trying Method 1: Direct I2C, no kwargs...")
try:
    display = SSD1306(i2c, 128, 32)
    print("  ✓✓✓ METHOD 1 WORKED!")
    print(f"  Display: {display.width}x{display.height}")
except Exception as e:
    print(f"  ✗ Method 1 failed: {e}")

    print("\n[4] Trying Method 2: With width/height kwargs...")
    try:
        display = SSD1306(i2c, width=128, height=32)
        print("  ✓✓✓ METHOD 2 WORKED!")
        print(f"  Display: {display.width}x{display.height}")
    except Exception as e2:
        print(f"  ✗ Method 2 failed: {e2}")

        print("\n[5] Trying Method 3: FourWire SPI approach...")
        try:
            from displayio import FourWire
            display_bus = FourWire(i2c, command=0, chip_select=None)
            display = SSD1306(display_bus, width=128, height=32)
            print("  ✓✓✓ METHOD 3 WORKED!")
        except Exception as e3:
            print(f"  ✗ Method 3 failed: {e3}")

            print("\n[6] Trying Method 4: I2CDisplayBus...")
            try:
                from displayio import I2CDisplay as I2CDisplayBus
                display_bus = I2CDisplayBus(i2c, device_address=0x3C)
                display = SSD1306(display_bus, width=128, height=32)
                print("  ✓✓✓ METHOD 4 WORKED!")
            except Exception as e4:
                print(f"  ✗ Method 4 failed: {e4}")

                print("\n✗ ALL METHODS FAILED")
                print("This library version is incompatible.")
                while True:
                    time.sleep(1)

# If we got here, one method worked!
print("\n[SUCCESS] Now testing display...")

from adafruit_display_text import label
import terminalio

splash = displayio.Group()
text = label.Label(terminalio.FONT, text="WORKS!", color=0xFFFFFF, x=30, y=15)
splash.append(text)

display.root_group = splash

print("\n✓✓✓ CHECK OLED - Should show 'WORKS!' ✓✓✓")

while True:
    time.sleep(1)
