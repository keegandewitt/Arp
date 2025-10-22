"""
Simple test to verify serial output is working

Deploy this temporarily to test if serial communication is working.
"""

import time

print("\n" + "=" * 60)
print("SIMPLE SERIAL OUTPUT TEST")
print("=" * 60)
print("\nIf you can see this, serial output is working!")
print("\nCounting to 10...")

for i in range(1, 11):
    print(f"  {i}...")
    time.sleep(0.5)

print("\n✓ Test complete!")
print("\nSerial communication is working correctly.")
print("\n" + "=" * 60)

# Keep running so we can see the output
print("\nPress Ctrl+C (or type 'stop' in monitor) to exit")
while True:
    time.sleep(1)
