"""OLED Test - Using Framebuffer Library"""

import board
import busio
import time

print("\n" + "=" * 60)
print("OLED TEST - Framebuffer Library")
print("=" * 60)

print("\n[1] Creating I2C bus...")
i2c = busio.I2C(board.SCL, board.SDA)
print("  ✓ I2C created")

print("\n[2] Importing SSD1306 library...")
import adafruit_ssd1306
print("  ✓ Library imported")

print("\n[3] Creating display object (128x32)...")
try:
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    print(f"  ✓ Display created: {oled.width}x{oled.height}")
except Exception as e:
    print(f"  ✗ 128x32 failed: {e}")
    print("\n[3b] Trying 128x64...")
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
    print(f"  ✓ Display created: {oled.width}x{oled.height}")

print("\n[4] Clearing display...")
oled.fill(0)
oled.show()
print("  ✓ Display cleared (should be blank)")

time.sleep(1)

print("\n[5] Drawing text 'HELLO!'...")
oled.text('HELLO!', 0, 0, 1)
oled.show()
print("  ✓ Text drawn")

print("\n*** CHECK THE OLED - You should see 'HELLO!' ***")

time.sleep(2)

print("\n[6] Adding more text...")
oled.text('Line 2', 0, 10, 1)
oled.text('Line 3', 0, 20, 1)
oled.show()
print("  ✓ Multiple lines displayed")

time.sleep(2)

print("\n[7] Clearing and showing 'PASS!'...")
oled.fill(0)
oled.text('PASS!', 40, 12, 1)
oled.show()
print("  ✓ PASS displayed")

print("\n" + "=" * 60)
print("✓✓✓ OLED WORKING! ✓✓✓")
print("=" * 60)
print("\nOLED FeatherWing is fully functional!")
print("Display shows 'PASS!'")

while True:
    time.sleep(1)
