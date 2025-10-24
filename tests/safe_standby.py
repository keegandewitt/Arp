"""Safe Standby - No I2C activity, safe for hot-plugging"""
import digitalio
import board
import time

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

print("\n=== SAFE STANDBY MODE ===")
print("No I2C activity")
print("Safe to connect/disconnect STEMMA QT cable")
print("LED will pulse slowly")
print()

# Slow pulse = standby
while True:
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)
