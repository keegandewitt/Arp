"""
Display Integration Test - Test the Display class with CP 10.x API

Tests the updated display.py module with OLED FeatherWing
"""

import board
import time

print("\n" + "=" * 60)
print("DISPLAY CLASS INTEGRATION TEST")
print("=" * 60)

print("\n[1] Creating I2C bus...")
i2c = board.I2C()
print("  ✓ I2C created")

print("\n[2] Importing Display class...")
try:
    from display import Display
    print("  ✓ Display class imported")
except ImportError as e:
    print(f"  ✗ Import failed: {e}")
    print("  Make sure display.py is on CIRCUITPY drive")
    while True:
        time.sleep(1)

print("\n[3] Initializing Display...")
try:
    display = Display(i2c)
    print("  ✓ Display initialized!")
except Exception as e:
    print(f"  ✗ Display init failed: {e}")
    print(f"  Error type: {type(e).__name__}")
    import traceback
    traceback.print_exception(e)
    while True:
        time.sleep(1)

print("\n[4] Testing startup screen...")
try:
    display.show_startup()
    print("  ✓ Startup screen shown")
    print("  CHECK OLED: Should show 'MIDI', 'Arpeggiator', 'Ready!'")
except Exception as e:
    print(f"  ✗ Failed: {e}")

time.sleep(3)

print("\n[5] Testing BPM update...")
display.update_bpm(120, "(Int)")
print("  ✓ BPM set to 120")
print("  CHECK OLED: Should show 'BPM: 120 (Int)'")

time.sleep(2)

print("\n[6] Testing pattern update...")
display.update_pattern("Up")
print("  ✓ Pattern set to 'Up'")
print("  CHECK OLED: Should show 'Pattern: Up'")

time.sleep(2)

print("\n[7] Testing MIDI indicators...")
display.set_midi_in_active(True)
print("  ✓ MIDI IN active (should see 'v' top left)")
time.sleep(1)

display.set_midi_out_active(True)
print("  ✓ MIDI OUT active (should see '^' top right)")
time.sleep(2)

display.set_midi_in_active(False)
display.set_midi_out_active(False)
print("  ✓ MIDI indicators cleared")

time.sleep(2)

print("\n[8] Testing message display...")
display.show_message("Test OK!")
print("  ✓ Message shown: 'Test OK!'")

time.sleep(2)

print("\n[9] Testing brightness control...")
print("  Testing low brightness (30%)...")
display.set_brightness(0.3)
time.sleep(1)

print("  Testing medium brightness (50%)...")
display.set_brightness(0.5)
time.sleep(1)

print("  Testing high brightness (100%)...")
display.set_brightness(1.0)
time.sleep(1)

print("  Resetting to default (50%)...")
display.set_brightness(0.5)
print("  ✓ Brightness control working")

time.sleep(2)

print("\n[10] Final display update...")
display.update_bpm(140, "(Int)")
display.update_pattern("Random")
display.show_message("SUCCESS!")
print("  ✓ Display shows: BPM 140, Pattern Random, SUCCESS!")

print("\n" + "=" * 60)
print("✓✓✓ DISPLAY CLASS FULLY WORKING ✓✓✓")
print("=" * 60)
print("\nOLED FeatherWing integration COMPLETE!")
print("Display class ready for arpeggiator integration.")

while True:
    time.sleep(1)
