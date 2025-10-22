"""
CORRECT TEST: OLED FeatherWing 128x64 uses SH1107, NOT SSD1306!
Product #4650 has the SH1107 driver chip
"""

import board
import displayio
import terminalio
import time
from i2cdisplaybus import I2CDisplayBus
import adafruit_displayio_sh1107
from adafruit_display_text import label

print("\n=== OLED 128x64 SH1107 Test (CORRECT DRIVER!) ===\n")

displayio.release_displays()

print("[1] Getting I2C...")
i2c = board.I2C()
print("OK")

print("[2] Creating display bus...")
display_bus = I2CDisplayBus(i2c, device_address=0x3C)
print("OK")

print("[3] Creating SH1107 display (128x64)...")
display = adafruit_displayio_sh1107.SH1107(
    display_bus,
    width=128,
    height=64
)
print(f"OK - {display.width}x{display.height}")

print("[4] Setting brightness to MAX...")
display.brightness = 1.0
print("OK")

print("[5] Creating text...")
splash = displayio.Group()

text1 = label.Label(
    terminalio.FONT,
    text="IT WORKS!",
    color=0xFFFFFF,
    x=25,
    y=20
)

text2 = label.Label(
    terminalio.FONT,
    text="SH1107 Driver",
    color=0xFFFFFF,
    x=15,
    y=40
)

splash.append(text1)
splash.append(text2)
print("OK")

print("[6] Displaying...")
display.root_group = splash
print("OK")

print("\n=== CHECK SCREEN ===")
print("Should show:")
print("  IT WORKS!")
print("  SH1107 Driver")
print("\nClear and readable!\n")

while True:
    time.sleep(1)
