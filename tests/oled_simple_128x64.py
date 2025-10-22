"""
Simplest possible OLED test for 128x64 with CP 10.x
Based on oled_cp10_correct.py but simplified
"""

import board
import displayio
import terminalio
import time

print("\n=== OLED 128x64 Simple Test ===\n")

displayio.release_displays()

print("[1] Getting I2C...")
i2c = board.I2C()
print("OK")

print("[2] Creating display bus...")
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3c)
print("OK")

print("[3] Creating SSD1306 display (128x64)...")
import adafruit_displayio_ssd1306
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
print(f"OK - {display.width}x{display.height}")

print("[4] Setting brightness to MAX...")
display.brightness = 1.0
print("OK")

print("[5] Creating text...")
from adafruit_display_text import label

splash = displayio.Group()
text = label.Label(
    terminalio.FONT,
    text="IT WORKS!",
    color=0xFFFFFF,
    x=30,
    y=32
)
splash.append(text)
print("OK")

print("[6] Displaying...")
display.root_group = splash
print("OK")

print("\n=== CHECK SCREEN - Should show 'IT WORKS!' ===\n")

while True:
    time.sleep(1)
