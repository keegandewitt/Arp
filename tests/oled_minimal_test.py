"""
Minimal OLED Test - Absolute simplest test to get ANYTHING on screen
Try both 128x32 and 128x64, try both addresses 0x3C and 0x3D
"""

import board
import displayio
import terminalio
import time
from adafruit_display_text import label

print("\n" + "=" * 60)
print("MINIMAL OLED TEST")
print("=" * 60)

displayio.release_displays()
i2c = board.I2C()

print("\nTrying 128x32 at 0x3C...")
try:
    import i2cdisplaybus
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

    import adafruit_displayio_ssd1306
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

    # Set brightness to MAX
    display.brightness = 1.0

    # Create simple text
    splash = displayio.Group()
    text = label.Label(terminalio.FONT, text="HELLO!", color=0xFFFFFF, x=0, y=15)
    splash.append(text)
    display.root_group = splash

    print("✓✓✓ SUCCESS - 128x32 at 0x3C")
    print("CHECK THE SCREEN - Should show 'HELLO!'")

    while True:
        time.sleep(1)

except Exception as e:
    print(f"✗ Failed: {e}")

print("\nTrying 128x64 at 0x3C...")
try:
    displayio.release_displays()
    i2c = board.I2C()
    import i2cdisplaybus
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

    import adafruit_displayio_ssd1306
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

    display.brightness = 1.0

    splash = displayio.Group()
    text = label.Label(terminalio.FONT, text="HELLO!", color=0xFFFFFF, x=0, y=30)
    splash.append(text)
    display.root_group = splash

    print("✓✓✓ SUCCESS - 128x64 at 0x3C")
    print("CHECK THE SCREEN - Should show 'HELLO!'")

    while True:
        time.sleep(1)

except Exception as e:
    print(f"✗ Failed: {e}")

print("\nTrying 128x32 at 0x3D...")
try:
    displayio.release_displays()
    i2c = board.I2C()
    import i2cdisplaybus
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3D)

    import adafruit_displayio_ssd1306
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

    display.brightness = 1.0

    splash = displayio.Group()
    text = label.Label(terminalio.FONT, text="HELLO!", color=0xFFFFFF, x=0, y=15)
    splash.append(text)
    display.root_group = splash

    print("✓✓✓ SUCCESS - 128x32 at 0x3D")
    print("CHECK THE SCREEN - Should show 'HELLO!'")

    while True:
        time.sleep(1)

except Exception as e:
    print(f"✗ Failed: {e}")

print("\n⚠️  NONE OF THE CONFIGURATIONS WORKED")
print("Check:")
print("  - Is the OLED FeatherWing properly seated on headers?")
print("  - Is the display powered on?")
print("  - Are there any solder bridges or poor connections?")

while True:
    time.sleep(1)
