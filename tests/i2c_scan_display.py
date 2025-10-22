"""I2C Scanner - Find the OLED display address"""

import board
import displayio
import time

print("\n" + "=" * 60)
print("I2C BUS SCANNER - Finding OLED Display")
print("=" * 60)

print("\n[0] Releasing any displays...")
displayio.release_displays()
print("  ✓ Displays released")

print("\n[1] Getting I2C bus...")
i2c = board.I2C()  # Use board's I2C singleton
print("  ✓ I2C bus obtained")

print("\n[2] Waiting for I2C lock...")
while not i2c.try_lock():
    pass
print("  ✓ I2C locked")

print("\n[3] Scanning I2C bus...")
print("  Addresses found:")

devices_found = []
for address in range(0x00, 0x80):
    try:
        i2c.writeto(address, b'')
        print(f"    0x{address:02X} - Device detected!")
        devices_found.append(address)
    except OSError:
        pass  # No device at this address

i2c.unlock()

print(f"\n[4] Scan complete - Found {len(devices_found)} device(s)")

if devices_found:
    print("\n  Common I2C addresses:")
    for addr in devices_found:
        if addr == 0x3C:
            print(f"    0x{addr:02X} - OLED Display (typical address)")
        elif addr == 0x3D:
            print(f"    0x{addr:02X} - OLED Display (alternate address)")
        else:
            print(f"    0x{addr:02X} - Unknown device")
else:
    print("\n  ⚠️  NO I2C DEVICES FOUND!")
    print("  Check wiring:")
    print("    - SDA (D21) connected?")
    print("    - SCL (D22) connected?")
    print("    - Display powered?")

print("\n" + "=" * 60)

while True:
    time.sleep(1)
