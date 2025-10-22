"""OLED Test - Step by Step with detailed output"""

import board
import busio
import time

print("\n" + "=" * 60)
print("OLED DISPLAY TEST - STEP BY STEP")
print("=" * 60)

print("\n[STEP 1] Creating I2C bus...")
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("  ✓ I2C bus created")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 2] Importing displayio...")
try:
    import displayio
    print("  ✓ displayio imported")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 3] Releasing any existing displays...")
try:
    displayio.release_displays()
    print("  ✓ Displays released")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 4] Importing SSD1306 driver...")
try:
    from adafruit_displayio_ssd1306 import SSD1306
    print("  ✓ SSD1306 driver imported")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    print("  Library may be corrupted or wrong version")
    while True:
        time.sleep(1)

print("\n[STEP 5] Creating I2C display bus...")
try:
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    print("  ✓ Display bus created at 0x3C")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 6] Initializing display (trying 128x32)...")
try:
    display = SSD1306(display_bus, width=128, height=32)
    print("  ✓ Display initialized as 128x32")
except Exception as e:
    print(f"  ⚠ 128x32 failed: {e}")
    print("\n[STEP 6b] Trying 128x64 instead...")
    try:
        display = SSD1306(display_bus, width=128, height=64)
        print("  ✓ Display initialized as 128x64")
    except Exception as e2:
        print(f"  ✗ 128x64 also failed: {e2}")
        while True:
            time.sleep(1)

print(f"\n[STEP 7] Display info:")
print(f"  Width: {display.width}")
print(f"  Height: {display.height}")

print("\n[STEP 8] Importing text support...")
try:
    from adafruit_display_text import label
    import terminalio
    print("  ✓ Text libraries imported")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 9] Creating display group...")
try:
    splash = displayio.Group()
    print("  ✓ Display group created")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 10] Creating text label...")
try:
    text_area = label.Label(
        terminalio.FONT,
        text="HELLO!",
        color=0xFFFFFF,
        x=10,
        y=10
    )
    print("  ✓ Text label created")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 11] Adding text to group...")
try:
    splash.append(text_area)
    print("  ✓ Text added to group")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n[STEP 12] Showing on display...")
try:
    display.show(splash)
    print("  ✓ Display updated!")
    print("\n*** CHECK THE OLED - You should see 'HELLO!' ***")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    while True:
        time.sleep(1)

print("\n" + "=" * 60)
print("✓✓✓ ALL STEPS PASSED ✓✓✓")
print("=" * 60)
print("\nThe OLED should be showing 'HELLO!'")
print("\nTest complete!")

while True:
    time.sleep(1)
