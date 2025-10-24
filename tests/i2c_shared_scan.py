"""I2C Scanner - Using Shared Bus (board.I2C())"""
import board
import digitalio
import time

# Setup LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

def blink(count=1, delay=0.2):
    for _ in range(count):
        led.value = True
        time.sleep(delay)
        led.value = False
        time.sleep(delay)

print("=== I2C Shared Bus Scanner ===")
print()

# Start
blink(2)

# Step 1: Use board.I2C() instead of busio.I2C()
# This returns a shared I2C bus that multiple devices can use
print("[1] Getting shared I2C bus...")
try:
    i2c = board.I2C()  # This is the KEY - returns shared singleton
    print("    ✓ Got shared I2C bus")
    blink(1)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

# Step 2: Lock and scan
print("\n[2] Scanning I2C bus...")
try:
    while not i2c.try_lock():
        pass

    devices = i2c.scan()
    i2c.unlock()

    print(f"    ✓ Found {len(devices)} device(s):")
    print()

    mcp_found = False
    oled_found = False

    for addr in devices:
        name = "Unknown"
        if addr == 0x3C:
            name = "OLED Display (SH1107)"
            oled_found = True
        elif addr == 0x60:
            name = "MCP4728 DAC ★"
            mcp_found = True
        elif addr == 0x61:
            name = "MCP4728 DAC (Alt 0x61) ★"
            mcp_found = True
        elif addr == 0x64:
            name = "MCP4728 DAC (Alt 0x64) ★"
            mcp_found = True

        print(f"      0x{addr:02X} - {name}")
        blink(1, 0.1)

    print()

    # Report findings
    if oled_found:
        print("    ✓ OLED detected at 0x3C")
    else:
        print("    ⚠ OLED not detected")

    if mcp_found:
        print("    ✓✓✓ MCP4728 DETECTED!")
        print("\n    → Hardware is ready for CV/Gate output!")
        blink(5, 0.1)  # Success!
    else:
        print("    ✗ MCP4728 NOT detected")
        print("\n    Troubleshooting:")
        print("      1. Check VCC → M4 3V pin (3.3V)")
        print("      2. Check GND → M4 GND")
        print("      3. Check STEMMA QT cable connected")
        print("      4. Verify MCP4728 board has power")
        blink(3, 0.5)

except Exception as e:
    print(f"    ✗ Scan failed: {e}")
    try:
        i2c.unlock()
    except:
        pass

# Heartbeat
print("\n[3] Test complete - heartbeat mode")
print("    (Quick pulse every 2 seconds)")
print()

while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(1.9)
