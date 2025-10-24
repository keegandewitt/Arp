"""I2C Scanner - Find OLED and MCP4728 DAC"""

import board
import busio
import time

print("\n" + "=" * 60)
print("I2C SCANNER - Looking for OLED and MCP4728 DAC")
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
    else:
        for addr in devices:
            device_name = ""
            if addr == 0x3C:
                device_name = " <- OLED Display (SH1107)"
            elif addr == 0x3D:
                device_name = " <- OLED at alternate address"
            elif addr == 0x60:
                device_name = " <- MCP4728 DAC (DEFAULT ADDRESS)"
            elif addr == 0x64:
                device_name = " <- MCP4728 DAC (Alternate)"
            elif addr == 0x61:
                device_name = " <- MCP4728 DAC (Alt 2)"

            print(f"  0x{addr:02X}{device_name}")

        print()
        if 0x3C in devices:
            print("✓ OLED found at 0x3C")
        if 0x60 in devices:
            print("✓ MCP4728 DAC found at 0x60")
        elif 0x61 in devices:
            print("✓ MCP4728 DAC found at 0x61 (alternate)")
        elif 0x64 in devices:
            print("✓ MCP4728 DAC found at 0x64 (alternate)")
        else:
            print("⚠ MCP4728 DAC not detected")
            print("\nTroubleshooting:")
            print("  1. Check VCC → M4's 3V pin (3.3V)")
            print("  2. Check GND → M4's GND")
            print("  3. Check STEMMA QT cable connected")
            print("  4. Verify MCP4728 has power (LED on breakout?)")

except Exception as e:
    print(f"\n✗ I2C scan failed: {e}")

print("\n" + "=" * 60)
print("Scan complete")
print("=" * 60)

while True:
    time.sleep(1)
