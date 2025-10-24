"""Super Simple I2C Scanner"""
print("Starting I2C scan...")

try:
    import board
    import busio
    import time

    print("Imports successful")

    print("Creating I2C bus...")
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C bus created")

    print("Locking I2C...")
    while not i2c.try_lock():
        pass
    print("I2C locked")

    print("Scanning...")
    devices = i2c.scan()
    i2c.unlock()

    print(f"Found {len(devices)} devices:")
    for addr in devices:
        print(f"  0x{addr:02X}")

    print("Scan complete!")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exception(type(e), e, e.__traceback__)

print("Keeping board alive...")
while True:
    import time
    time.sleep(1)
