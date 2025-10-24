"""I2C Scanner with LED Blink Confirmation"""
import board
import busio
import digitalio
import time

# Setup LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Blink 3 times to show we're starting
print("Starting... (watch LED)")
for i in range(3):
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)

print("\n=== I2C SCANNER ===")

try:
    print("Init I2C...")
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C OK")

    # Blink once for success
    led.value = True
    time.sleep(0.5)
    led.value = False

    print("Scanning...")
    while not i2c.try_lock():
        pass

    devices = i2c.scan()
    i2c.unlock()

    print(f"\nFound {len(devices)} devices:")
    for addr in devices:
        name = ""
        if addr == 0x3C:
            name = " - OLED"
        elif addr == 0x60:
            name = " - MCP4728"
        print(f"  0x{addr:02X}{name}")

        # Blink for each device found
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)

    print("\nDone!")

    # Blink pattern: Success = 5 quick blinks
    for i in range(5):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)

except Exception as e:
    print(f"ERROR: {e}")
    # Error pattern: Slow blinks
    for i in range(10):
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

# Keep alive with slow heartbeat
print("Heartbeat mode...")
while True:
    led.value = True
    time.sleep(2)
    led.value = False
    time.sleep(2)
