"""MCP4728 Simple Output Test - 3.3V Operation

Tests basic DAC output. Watch the LED and use a multimeter on the DAC outputs.

LED Patterns:
- 3 quick blinks: Starting
- 1 blink per test step
- Fast heartbeat (0.5s): Test running, outputs active
- Slow error blink (1s): Something failed

Hardware Check:
- Use multimeter on MCP4728 Channel A (VA) output
- Should sweep from 0V to 3.3V in steps
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
    print("    ✗ ERROR - entering error mode")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

print("\n" + "=" * 50)
print("MCP4728 DAC Output Test - 3.3V")
print("=" * 50)
blink(3)  # Starting

# Step 1: Get I2C bus
print("\n[1] Getting shared I2C bus...")
try:
    i2c = board.I2C()
    print("    ✓ I2C ready")
    blink(1)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 2: Import MCP4728 library
print("\n[2] Importing adafruit_mcp4728...")
try:
    import adafruit_mcp4728
    print("    ✓ Library imported")
    blink(1)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    print("    → Run: circup install adafruit_mcp4728")
    error()

# Step 3: Initialize MCP4728
print("\n[3] Initializing MCP4728 at 0x60...")
try:
    dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
    print("    ✓ DAC initialized")
    blink(1)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    print("    → Check DAC power and I2C connection")
    error()

# Step 4: Configure for 3.3V operation
print("\n[4] Configuring DAC for 3.3V...")
try:
    # Use VDD (3.3V) as reference with 1x gain
    # Max output = 3.3V when value = 4095
    for channel in [dac.channel_a, dac.channel_b, dac.channel_c, dac.channel_d]:
        channel.vref = adafruit_mcp4728.Vref.VDD
        channel.gain = 1

    print("    ✓ DAC configured (VDD ref, 1x gain)")
    print("    → Max output: 3.3V @ value=4095")
    blink(1)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 5: Zero all channels
print("\n[5] Zeroing all channels...")
try:
    dac.channel_a.value = 0
    dac.channel_b.value = 0
    dac.channel_c.value = 0
    dac.channel_d.value = 0
    print("    ✓ All channels at 0V")
    print("    → Check multimeter: should read ~0V")
    blink(1)
    time.sleep(2)
except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 6: Voltage sweep on Channel A
print("\n[6] Voltage sweep on Channel A...")
print("    → Place multimeter on VA (Channel A) output")
print()

try:
    # Sweep in 5 steps: 0V, 0.825V, 1.65V, 2.475V, 3.3V
    steps = [
        (0, "0.00V"),
        (1024, "0.82V"),
        (2048, "1.65V"),
        (3072, "2.48V"),
        (4095, "3.30V"),
    ]

    for value, expected in steps:
        dac.channel_a.value = value
        print(f"    Value {value:4d} → {expected}")
        blink(1, 0.1)
        time.sleep(2.5)

    print("\n    ✓ Sweep complete!")
    print("    → Did voltages match on multimeter?")
    blink(3)

except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 7: Test all channels at mid-range
print("\n[7] Testing all 4 channels at 1.65V...")
try:
    mid_value = 2048  # 1.65V

    print("    Testing each channel (2 seconds each):")
    channels = [
        (dac.channel_a, "A (VA)"),
        (dac.channel_b, "B (VB)"),
        (dac.channel_c, "C (VC)"),
        (dac.channel_d, "D (VD)"),
    ]

    for channel, name in channels:
        # Zero all first
        dac.channel_a.value = 0
        dac.channel_b.value = 0
        dac.channel_c.value = 0
        dac.channel_d.value = 0

        # Set target
        channel.value = mid_value
        print(f"      Channel {name}: 1.65V")
        blink(1, 0.1)
        time.sleep(2.5)

    # Zero all
    dac.channel_a.value = 0
    dac.channel_b.value = 0
    dac.channel_c.value = 0
    dac.channel_d.value = 0

    print("\n    ✓ All channels tested!")
    blink(3)

except Exception as e:
    print(f"    ✗ Failed: {e}")
    error()

# Step 8: Gate test on Channel B
print("\n[8] Gate/trigger test on Channel B...")
print("    → Measure Channel B (VB)")
try:
    for i in range(5):
        # Gate HIGH (3.3V)
        dac.channel_b.value = 4095
        print(f"      [{i+1}/5] Gate HIGH (3.3V)")
        led.value = True
        time.sleep(0.5)

        # Gate LOW (0V)
        dac.channel_b.value = 0
        print(f"      [{i+1}/5] Gate LOW  (0V)")
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
print("\nMCP4728 DAC is working correctly!")
print("Hardware is ready for CV/Gate integration.")
print("\nNext steps:")
print("  1. Verify multimeter readings matched expected")
print("  2. Test with oscilloscope if available")
print("  3. Integrate into main arpeggiator code")
print("\nEntering heartbeat mode (fast pulse)...")
print("=" * 50)
print()

# Fast heartbeat = success
while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.4)
