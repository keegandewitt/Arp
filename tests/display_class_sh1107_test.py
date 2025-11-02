"""
Test the full Display class with correct SH1107 driver
"""

import board
import time

print("\n=== Display Class Integration Test (SH1107) ===\n")

# Import the Display class
import sys
sys.path.insert(0, '/Users/keegandewitt/Cursor/prisme')
from display import Display

print("[1] Creating I2C bus...")
i2c = board.I2C()
print("OK")

print("[2] Initializing Display class...")
display = Display(i2c)
print("OK")

print("[3] Testing startup screen...")
display.show_startup()
time.sleep(2)
print("OK")

print("[4] Testing BPM update...")
display.update_bpm(120, "(Int)")
time.sleep(2)
print("OK")

print("[5] Testing pattern update...")
display.update_pattern("Up/Down")
time.sleep(2)
print("OK")

print("[6] Testing status message...")
display.show_message("All systems GO!")
time.sleep(2)
print("OK")

print("[7] Testing brightness control...")
display.set_brightness(0.3)
time.sleep(1)
display.set_brightness(1.0)
time.sleep(1)
display.set_brightness(0.5)
print("OK")

print("\n=== All Display Class Tests Passed! ===\n")
print("Display should show:")
print("  BPM: 120 (Int)")
print("  Pattern: Up/Down")
print("  All systems GO!")
print("\nDisplay class is fully functional!")

while True:
    time.sleep(1)
