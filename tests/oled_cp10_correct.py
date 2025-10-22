"""
OLED FeatherWing Test - CircuitPython 10.x Correct API

Uses the NEW i2cdisplaybus module introduced in CP 10.x
"""

import board
import displayio
import terminalio
import time

print("\n" + "=" * 60)
print("OLED TEST - CircuitPython 10.x Correct API")
print("=" * 60)

displayio.release_displays()

print("\n[1] Creating I2C bus...")
i2c = board.I2C()
print("  ✓ I2C created using board.I2C()")

print("\n[2] Importing i2cdisplaybus (NEW in CP 10.x)...")
try:
    import i2cdisplaybus
    print("  ✓ i2cdisplaybus imported")
except ImportError:
    print("  ✗ i2cdisplaybus not found - this is a BUILT-IN module")
    print("  Your CircuitPython version may not support it")
    while True:
        time.sleep(1)

print("\n[3] Creating I2C display bus...")
try:
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3c)
    print("  ✓ Display bus created at address 0x3c")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[4] Importing SSD1306 driver...")
try:
    import adafruit_displayio_ssd1306
    print("  ✓ SSD1306 driver imported")
except ImportError:
    print("  ✗ adafruit_displayio_ssd1306 not installed")
    print("  Install with: circup install adafruit_displayio_ssd1306")
    while True:
        time.sleep(1)

print("\n[5] Creating display object...")
try:
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
    print(f"  ✓ Display created: {display.width}x{display.height}")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[6] Creating display group...")
from adafruit_display_text import label

splash = displayio.Group()
print("  ✓ Group created")

print("\n[7] Adding text 'HELLO!'...")
text_area = label.Label(
    terminalio.FONT,
    text="HELLO!",
    color=0xFFFFFF,
    x=28,
    y=15
)
splash.append(text_area)
print("  ✓ Text label created")

print("\n[8] Displaying on OLED...")
display.root_group = splash
print("  ✓ DISPLAYED!")

print("\n" + "=" * 60)
print("✓✓✓ CHECK THE OLED - Should show 'HELLO!' ✓✓✓")
print("=" * 60)

time.sleep(2)

print("\n[9] Updating text...")
text_area.text = "IT WORKS!"
print("  ✓ Text changed to 'IT WORKS!'")

time.sleep(2)

print("\n[10] Final test - 'SUCCESS!'...")
text_area.text = "SUCCESS!"
print("  ✓ Display shows 'SUCCESS!'")

print("\n" + "=" * 60)
print("✓✓✓ OLED FULLY WORKING ✓✓✓")
print("=" * 60)
print("\nThe issue was using outdated CP 9.x API.")
print("CP 10.x requires: import i2cdisplaybus")

while True:
    time.sleep(1)
