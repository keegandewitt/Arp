"""
OLED Maximum Brightness Test
Tests display at full brightness with high-contrast pattern
"""

import board
import time
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1107

print("\n" + "="*60)
print("OLED MAXIMUM BRIGHTNESS TEST")
print("="*60)

# Initialize
print("Initializing display at MAXIMUM brightness...")
i2c = board.I2C()
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)

# MAX BRIGHTNESS
display.brightness = 1.0
print("✓ Display brightness set to 100%")

# Create LARGE, BRIGHT text
group = displayio.Group()

# Big text at top
line1 = label.Label(terminalio.FONT, text="* HELLO! *", color=0xFFFFFF, x=20, y=10)
line2 = label.Label(terminalio.FONT, text="CAN YOU", color=0xFFFFFF, x=28, y=25)
line3 = label.Label(terminalio.FONT, text="SEE THIS?", color=0xFFFFFF, x=20, y=40)
line4 = label.Label(terminalio.FONT, text=">>><<<", color=0xFFFFFF, x=35, y=55)

group.append(line1)
group.append(line2)
group.append(line3)
group.append(line4)

display.root_group = group

print("\n" + "="*60)
print("OLED SHOULD BE SHOWING:")
print("  * HELLO! *")
print("  CAN YOU")
print("  SEE THIS?")
print("  >>><<<")
print("="*60)
print("\nBrightness: 100% (MAXIMUM)")
print("\nIf you STILL can't see anything:")
print("  1. Check OLED FeatherWing is stacked on M4")
print("  2. Check all pins are making contact")
print("  3. Look at display from different angles")
print("  4. OLED should glow blue/white")
print("\nFlashing display in 3 seconds...")
time.sleep(3)

# Flash on/off to make it obvious
print("\nFLASHING DISPLAY (watch for any light)...")
for i in range(10):
    if i % 2 == 0:
        display.brightness = 1.0
        print(f"  Flash {i//2 + 1}: ON")
    else:
        display.brightness = 0.0
        print(f"  Flash {i//2 + 1}: OFF")
    time.sleep(0.5)

# Leave at full brightness
display.brightness = 1.0
print("\n✓ Display now at full brightness")
print("\nPress CTRL+C to exit")

while True:
    time.sleep(1)
