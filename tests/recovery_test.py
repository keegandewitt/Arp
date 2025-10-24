"""Recovery Test - No MCP4728 required"""
import board
import digitalio
import time

# LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

print("\n=== RECOVERY TEST ===")
print("Board is alive!")
print("LED should blink 5 times fast...")

# 5 quick blinks
for i in range(5):
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)
    print(f"  Blink {i+1}/5")

print("\nChecking I2C bus...")
try:
    i2c = board.I2C()
    while not i2c.try_lock():
        pass

    devices = i2c.scan()
    i2c.unlock()

    print(f"Found {len(devices)} device(s):")
    for addr in devices:
        name = ""
        if addr == 0x3C:
            name = " - OLED"
        elif addr == 0x60:
            name = " - MCP4728"
        print(f"  0x{addr:02X}{name}")

except Exception as e:
    print(f"I2C error: {e}")

print("\nEntering slow heartbeat...")
print("(LED pulses every 2 seconds = board OK)")

# Slow heartbeat
while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(1.9)
