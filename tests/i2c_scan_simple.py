"""Simple I2C Scanner - Find the OLED"""

import board
import busio
import time

print("\n" + "=" * 60)
print("I2C SCANNER - Looking for OLED FeatherWing")
print("=" * 60)

print("\nInitializing I2C bus...")
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("✓ I2C bus initialized")
except Exception as e:
    print(f"✗ Failed to init I2C: {e}")
    print("Stopping here.")
    while True:
        time.sleep(1)

print("\nScanning I2C bus...")
print("(This may take a few seconds...)")

try:
    while not i2c.try_lock():
        pass

    print("\nScanning addresses 0x00 to 0x7F...")
    devices = i2c.scan()
    i2c.unlock()

    print(f"\nFound {len(devices)} device(s):")

    if len(devices) == 0:
        print("  (No I2C devices detected)")
        print("\n✗ OLED NOT FOUND!")
        print("\nPossible causes:")
        print("  - FeatherWing not making contact with I2C pins")
        print("  - Check SDA (D21) and SCL (D22) connection")
        print("  - Try reseating the FeatherWing")
        print("  - Verify FeatherWing has power")
    else:
        for addr in devices:
            device_name = ""
            if addr == 0x3C:
                device_name = " <- OLED (FOUND!)"
            elif addr == 0x3D:
                device_name = " <- OLED at alternate address"

            print(f"  0x{addr:02X}{device_name}")

        if 0x3C in devices:
            print("\n✓✓✓ OLED DETECTED AT 0x3C ✓✓✓")
            print("Hardware connection is GOOD!")
            print("The OLED should work.")
        elif 0x3D in devices:
            print("\n✓ OLED found at 0x3D (alternate address)")
            print("You may need to adjust the test script.")
        else:
            print("\n⚠ Devices found, but not the OLED")
            print("Expected OLED at 0x3C or 0x3D")

except Exception as e:
    print(f"\n✗ I2C scan failed: {e}")

print("\n" + "=" * 60)
print("Scan complete")
print("=" * 60)

while True:
    time.sleep(1)
