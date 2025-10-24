"""MCP4728 Auto-Detect and Output Test

Automatically finds MCP4728 at any address (0x60, 0x61, 0x64, 0x66)
then tests DAC output.
"""

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

def error():
    print("    ✗ ERROR MODE")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

print("\n" + "=" * 50)
print("MCP4728 Auto-Detect Test")
print("=" * 50)
blink(3)

# Step 1: Get I2C and scan
print("\n[1] Scanning I2C bus for MCP4728...")
try:
    i2c = board.I2C()

    while not i2c.try_lock():
        pass
    devices = i2c.scan()
    i2c.unlock()

    print(f"    Found {len(devices)} device(s):")
    for addr in devices:
        name = ""
        if addr == 0x3C:
            name = "OLED"
        elif addr in [0x60, 0x61, 0x64, 0x66]:
            name = "MCP4728 (possible)"
        print(f"      0x{addr:02X} - {name}")

    blink(1)

except Exception as e:
    print(f"    ✗ Scan failed: {e}")
    error()

# Step 2: Find MCP4728 address
print("\n[2] Looking for MCP4728 at known addresses...")
MCP_ADDRESSES = [0x60, 0x61, 0x64, 0x66]
mcp_address = None

for addr in MCP_ADDRESSES:
    if addr in devices:
        mcp_address = addr
        print(f"    ✓ MCP4728 found at 0x{addr:02X}")
        blink(1)
        break

if mcp_address is None:
    print("    ✗ MCP4728 NOT FOUND at any address!")
    print("\n    Checked addresses:")
    for addr in MCP_ADDRESSES:
        print(f"      0x{addr:02X}")
    print("\n    Troubleshooting:")
    print("      1. Is MCP4728 powered? (VCC = 3.3V)")
    print("      2. Is GND connected?")
    print("      3. Is STEMMA QT cable connected for I2C?")
    print("      4. Try a different MCP4728 board")
    error()

# Step 3: Import library
print("\n[3] Importing adafruit_mcp4728...")
try:
    import adafruit_mcp4728
    print("    ✓ Library imported")
    blink(1)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 4: Initialize DAC
print(f"\n[4] Initializing MCP4728 at 0x{mcp_address:02X}...")
try:
    dac = adafruit_mcp4728.MCP4728(i2c, address=mcp_address)
    print("    ✓ DAC initialized!")
    blink(2)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 5: Configure for 3.3V
print("\n[5] Configuring for 3.3V operation...")
try:
    for channel in [dac.channel_a, dac.channel_b, dac.channel_c, dac.channel_d]:
        channel.vref = adafruit_mcp4728.Vref.VDD
        channel.gain = 1
    print("    ✓ Configured (VDD ref, 1x gain)")
    blink(1)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 6: Zero all channels
print("\n[6] Zeroing all channels...")
try:
    dac.channel_a.value = 0
    dac.channel_b.value = 0
    dac.channel_c.value = 0
    dac.channel_d.value = 0
    print("    ✓ All at 0V")
    print("    → Multimeter should read ~0V on all outputs")
    blink(1)
    time.sleep(2)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 7: Voltage sweep on Channel A
print("\n[7] Voltage sweep on Channel A (VA)...")
print("    → Connect multimeter to VA output")
print()

try:
    steps = [
        (0, "0.00V"),
        (1024, "0.82V"),
        (2048, "1.65V"),
        (3072, "2.48V"),
        (4095, "3.30V"),
    ]

    for value, expected in steps:
        dac.channel_a.value = value
        print(f"    {value:4d} → {expected}")
        blink(1, 0.1)
        time.sleep(2.5)

    dac.channel_a.value = 0
    print("\n    ✓ Sweep complete!")
    blink(3)

except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 8: Test all 4 channels
print("\n[8] Testing all 4 channels at 1.65V...")
try:
    mid = 2048
    channels = [
        (dac.channel_a, "A (VA)"),
        (dac.channel_b, "B (VB)"),
        (dac.channel_c, "C (VC)"),
        (dac.channel_d, "D (VD)"),
    ]

    for channel, name in channels:
        dac.channel_a.value = 0
        dac.channel_b.value = 0
        dac.channel_c.value = 0
        dac.channel_d.value = 0

        channel.value = mid
        print(f"    Channel {name}: 1.65V")
        blink(1, 0.1)
        time.sleep(2.5)

    dac.channel_a.value = 0
    dac.channel_b.value = 0
    dac.channel_c.value = 0
    dac.channel_d.value = 0

    print("\n    ✓ All channels tested!")
    blink(3)

except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 9: Gate test on Channel B
print("\n[9] Gate test on Channel B (VB)...")
print("    → Measure VB output")
try:
    for i in range(5):
        dac.channel_b.value = 4095
        print(f"    [{i+1}/5] HIGH (3.3V)")
        led.value = True
        time.sleep(0.5)

        dac.channel_b.value = 0
        print(f"    [{i+1}/5] LOW  (0V)")
        led.value = False
        time.sleep(0.5)

    print("\n    ✓ Gate test complete!")
    blink(5, 0.1)

except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Success!
print("\n" + "=" * 50)
print("✓✓✓ ALL TESTS PASSED! ✓✓✓")
print("=" * 50)
print(f"\nMCP4728 detected at 0x{mcp_address:02X}")
print("DAC is working correctly at 3.3V!")
print("\nReady for CV/Gate integration!")
print("\nEntering heartbeat mode...")
print("=" * 50)

# Fast heartbeat = success
while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.4)
