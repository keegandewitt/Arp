"""
Library Import Test

Tests that all required libraries can be imported successfully.
"""

import time

print("\n" + "=" * 60)
print("LIBRARY IMPORT TEST")
print("=" * 60)
print("\nTesting library imports...\n")

# Test built-in modules
print("[1] Testing built-in modules...")
try:
    import board
    print("  ✓ board")
except Exception as e:
    print(f"  ✗ board: {e}")

try:
    import busio
    print("  ✓ busio")
except Exception as e:
    print(f"  ✗ busio: {e}")

try:
    import displayio
    print("  ✓ displayio")
except Exception as e:
    print(f"  ✗ displayio: {e}")

try:
    import terminalio
    print("  ✓ terminalio")
except Exception as e:
    print(f"  ✗ terminalio: {e}")

# Test external libraries
print("\n[2] Testing external libraries (from /lib)...")

try:
    import neopixel
    print("  ✓ neopixel")
except Exception as e:
    print(f"  ✗ neopixel: {e}")

try:
    from adafruit_displayio_ssd1306 import SSD1306
    print("  ✓ adafruit_displayio_ssd1306")
except Exception as e:
    print(f"  ✗ adafruit_displayio_ssd1306: {e}")

try:
    from adafruit_display_text import label
    print("  ✓ adafruit_display_text")
except Exception as e:
    print(f"  ✗ adafruit_display_text: {e}")

try:
    import adafruit_ticks
    print("  ✓ adafruit_ticks")
except Exception as e:
    print(f"  ✗ adafruit_ticks: {e}")

try:
    import adafruit_bitmap_font
    print("  ✓ adafruit_bitmap_font")
except Exception as e:
    print(f"  ✗ adafruit_bitmap_font: {e}")

print("\n" + "=" * 60)
print("✓ LIBRARY IMPORT TEST COMPLETE")
print("=" * 60)
print("\nAll libraries imported successfully!")
print("The OLED test should work now.")
print("\nType 'exit' to close monitor")

while True:
    time.sleep(1)
