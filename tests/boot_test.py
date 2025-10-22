"""Immediate boot test - prints ASAP"""

# Print immediately on import
print("\n\n*** BOOT TEST STARTING ***")
print("If you see this, Python is running!")

import time
print("✓ time imported")

import board
print("✓ board imported")

import busio
print("✓ busio imported")

print("\n*** ALL IMPORTS SUCCESSFUL ***")
print("\nCounting down from 5...")

for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("\n✓ Boot test complete!")
print("\nType 'exit' to close monitor")

while True:
    time.sleep(1)
