"""I2C Debug Scanner - Detailed Error Reporting"""
import board
import digitalio
import time

# Setup LED for visual feedback
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

def blink_pattern(count, delay=0.2):
    """Blink LED a specific number of times"""
    for i in range(count):
        led.value = True
        time.sleep(delay)
        led.value = False
        time.sleep(delay)

def error_blink():
    """Slow error blink pattern"""
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

# Start indication
print("=== I2C Debug Scanner ===")
blink_pattern(2)  # 2 blinks = starting

# Step 1: Try to import busio
print("\n[1] Importing busio...")
try:
    import busio
    print("    ✓ busio imported")
    blink_pattern(1)  # Success
except Exception as e:
    print(f"    ✗ Failed to import busio: {e}")
    error_blink()

# Step 2: Check if SCL/SDA pins are available
print("\n[2] Checking I2C pins...")
try:
    print(f"    SCL: {board.SCL}")
    print(f"    SDA: {board.SDA}")
    print("    ✓ I2C pins available")
    blink_pattern(1)
except Exception as e:
    print(f"    ✗ I2C pins not available: {e}")
    error_blink()

# Step 3: Try to create I2C bus
print("\n[3] Creating I2C bus...")
i2c = None
try:
    # Create I2C with explicit timeout
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    print("    ✓ I2C bus created (100kHz)")
    blink_pattern(1)
    time.sleep(0.5)
except Exception as e:
    print(f"    ✗ Failed to create I2C: {e}")
    print(f"    Error type: {type(e).__name__}")
    error_blink()

# Step 4: Try to lock I2C
print("\n[4] Locking I2C bus...")
try:
    timeout = 0
    while not i2c.try_lock():
        time.sleep(0.1)
        timeout += 1
        if timeout > 50:  # 5 second timeout
            print("    ✗ Timeout waiting for I2C lock")
            print("    → Another device may have I2C locked")
            error_blink()

    print("    ✓ I2C locked")
    blink_pattern(1)
except Exception as e:
    print(f"    ✗ Failed to lock I2C: {e}")
    error_blink()

# Step 5: Scan for devices
print("\n[5] Scanning I2C bus...")
try:
    devices = i2c.scan()
    print(f"    ✓ Scan complete: {len(devices)} devices found")

    if len(devices) == 0:
        print("\n    ⚠ NO DEVICES FOUND")
        print("    Possible causes:")
        print("      - MCP4728 not powered (check VCC = 3.3V)")
        print("      - STEMMA QT cable not connected")
        print("      - Wrong I2C address")
        blink_pattern(3, 0.5)  # Warning pattern
    else:
        print("\n    Devices:")
        for addr in devices:
            name = "Unknown"
            if addr == 0x3C:
                name = "OLED Display"
            elif addr == 0x60:
                name = "MCP4728 DAC (DEFAULT)"
            elif addr == 0x61:
                name = "MCP4728 DAC (Alt)"
            elif addr == 0x64:
                name = "MCP4728 DAC (Alt 2)"

            print(f"      0x{addr:02X} - {name}")
            blink_pattern(1, 0.1)  # Quick blink per device

        # Check specifically for MCP4728
        if 0x60 in devices:
            print("\n    ✓✓✓ MCP4728 FOUND at 0x60!")
            blink_pattern(5, 0.1)  # Success!
        elif 0x61 in devices or 0x64 in devices:
            print("\n    ✓ MCP4728 found at alternate address")
            blink_pattern(4, 0.1)
        else:
            print("\n    ⚠ MCP4728 NOT detected")
            print("    Check:")
            print("      - VCC connected to M4's 3V pin")
            print("      - GND connected to M4's GND")
            print("      - STEMMA QT cable for SDA/SCL")
            blink_pattern(3, 0.5)

    i2c.unlock()

except Exception as e:
    print(f"    ✗ Scan failed: {e}")
    try:
        i2c.unlock()
    except:
        pass
    error_blink()

# Success - heartbeat pattern
print("\n[6] Test complete - entering heartbeat mode")
print("    (LED will pulse every 2 seconds)")

while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(1.9)
