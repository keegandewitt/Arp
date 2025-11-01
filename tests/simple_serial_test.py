"""
Simple Serial Output Test
Just prints to verify serial communication works
No complex imports - just basic output
"""

import time

print("\n" + "="*60)
print("SIMPLE SERIAL TEST")
print("="*60)
print()
print("If you can see this, serial communication is working!")
print()
print("Counting to 10...")
print()

for i in range(1, 11):
    print(f"  Count: {i}")
    time.sleep(0.5)

print()
print("="*60)
print("Serial test complete - everything is working!")
print("="*60)
print()

while True:
    time.sleep(1)
