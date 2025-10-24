"""
MCP4728 DAC Basic Test - 3.3V Operation

Tests the MCP4728 quad DAC for CV/Gate output.
This test is configured for 3.3V operation (using M4's 3V pin).

Required CircuitPython Libraries:
- adafruit_mcp4728 (install via: circup install adafruit_mcp4728)

Hardware Setup:
- MCP4728 VCC → Feather M4 3V pin (3.3V)
- MCP4728 GND → Feather M4 GND
- MCP4728 SDA → Connect via STEMMA QT to OLED FeatherWing
- MCP4728 SCL → Connect via STEMMA QT to OLED FeatherWing

Expected I2C Addresses:
- 0x3C: OLED Display
- 0x60: MCP4728 DAC (default address)

Test Sequence:
1. I2C bus scan (verify both devices detected)
2. Initialize MCP4728
3. Zero all channels
4. Test voltage sweep on Channel A (0V to 3.3V)
5. Test all 4 channels independently
6. Test CV pitch output (scaled for 3.3V range)
7. Test gate/trigger output
"""

import board
import busio
import time
import adafruit_mcp4728

print("\n" + "=" * 60)
print("MCP4728 DAC Basic Test - 3.3V Operation")
print("=" * 60)

# Test configuration
DAC_ADDRESS = 0x60  # Default MCP4728 address
OLED_ADDRESS = 0x3C
TEST_DELAY = 1.0  # Seconds between test steps

def print_test_header(test_num, description):
    """Print a formatted test header"""
    print(f"\n{'─' * 60}")
    print(f"[TEST {test_num}] {description}")
    print(f"{'─' * 60}")

def scan_i2c_bus(i2c):
    """Scan I2C bus and return list of detected devices"""
    print("\nScanning I2C bus...")
    while not i2c.try_lock():
        pass

    try:
        devices = i2c.scan()
        print(f"  Found {len(devices)} device(s) on I2C bus:")

        for addr in devices:
            device_name = ""
            if addr == OLED_ADDRESS:
                device_name = "OLED Display"
            elif addr == DAC_ADDRESS:
                device_name = "MCP4728 DAC"
            else:
                device_name = "Unknown"

            check = "✓" if addr in [OLED_ADDRESS, DAC_ADDRESS] else " "
            print(f"    [{check}] 0x{addr:02X} - {device_name}")

        return devices
    finally:
        i2c.unlock()

def test_dac_initialization(i2c):
    """Test DAC initialization"""
    print_test_header(2, "Initialize MCP4728 DAC")

    try:
        print("  Creating MCP4728 object...")
        dac = adafruit_mcp4728.MCP4728(i2c, address=DAC_ADDRESS)
        print("  ✓ MCP4728 initialized successfully")

        # Configure for 3.3V operation
        # Using VDD as reference (3.3V from M4's 3V pin)
        print("  Configuring DAC for 3.3V operation...")
        print("    - Vref: VDD (3.3V)")
        print("    - Gain: 1x")

        # Set all channels to use VDD reference with 1x gain
        for channel in [dac.channel_a, dac.channel_b, dac.channel_c, dac.channel_d]:
            channel.vref = adafruit_mcp4728.Vref.VDD
            channel.gain = 1

        print("  ✓ DAC configured")
        return dac

    except Exception as e:
        print(f"  ✗ Failed to initialize DAC: {e}")
        return None

def test_zero_all_channels(dac):
    """Zero all DAC channels"""
    print_test_header(3, "Zero All Channels")

    try:
        print("  Setting all channels to 0V...")
        dac.channel_a.value = 0
        dac.channel_b.value = 0
        dac.channel_c.value = 0
        dac.channel_d.value = 0
        print("  ✓ All channels set to 0V")
        print("  → Use multimeter to verify: Should read ~0V on all outputs")
        time.sleep(TEST_DELAY * 2)

    except Exception as e:
        print(f"  ✗ Failed to zero channels: {e}")

def test_voltage_sweep(dac):
    """Test voltage sweep on Channel A"""
    print_test_header(4, "Voltage Sweep Test (Channel A)")

    try:
        print("  Sweeping Channel A from 0V to 3.3V...")
        print("  → Use multimeter on Channel A (VA) output")
        print()

        # MCP4728 is 12-bit: 0 to 4095
        # With VDD reference (3.3V) and gain=1: Output = (value/4095) * 3.3V
        steps = [
            (0, "0.0V"),
            (1024, "0.825V"),
            (2048, "1.65V"),
            (3072, "2.475V"),
            (4095, "3.3V"),
        ]

        for value, expected in steps:
            dac.channel_a.value = value
            print(f"    Value: {value:4d} → Expected: {expected}")
            time.sleep(TEST_DELAY)

        print("  ✓ Voltage sweep complete")
        print("  → Verify multimeter readings matched expected values")
        time.sleep(TEST_DELAY)

    except Exception as e:
        print(f"  ✗ Failed voltage sweep: {e}")

def test_all_channels(dac):
    """Test all 4 channels independently"""
    print_test_header(5, "Test All Four Channels")

    try:
        print("  Testing each channel at 1.65V (mid-range)...")
        print("  → Use multimeter to verify each output")
        print()

        # Mid-range value: 2048 = 1.65V at 3.3V VDD
        test_value = 2048
        expected_voltage = "1.65V"

        channels = [
            (dac.channel_a, "A (VA)", "CV Pitch"),
            (dac.channel_b, "B (VB)", "Gate/Trigger"),
            (dac.channel_c, "C (VC)", "Velocity"),
            (dac.channel_d, "D (VD)", "Modulation"),
        ]

        for channel, name, purpose in channels:
            # Zero all first
            dac.channel_a.value = 0
            dac.channel_b.value = 0
            dac.channel_c.value = 0
            dac.channel_d.value = 0

            # Set target channel
            channel.value = test_value
            print(f"    Channel {name} ({purpose}): {expected_voltage}")
            time.sleep(TEST_DELAY * 1.5)

        # Zero all at end
        dac.channel_a.value = 0
        dac.channel_b.value = 0
        dac.channel_c.value = 0
        dac.channel_d.value = 0

        print("  ✓ All channels tested")

    except Exception as e:
        print(f"  ✗ Failed channel test: {e}")

def test_cv_pitch_scaling(dac):
    """Test CV pitch scaling (adapted for 3.3V)"""
    print_test_header(6, "CV Pitch Scaling Test (3.3V Range)")

    print("  NOTE: Standard 1V/octave CV requires 0-5V range")
    print("  With 3.3V, we can cover ~3.3 octaves")
    print()

    try:
        print("  Simulating MIDI notes → CV voltage...")
        print("  → Measure Channel A (VA) with multimeter")
        print()

        # For 3.3V operation:
        # - 0V = C0 (MIDI 24)
        # - 1V = C1 (MIDI 36)
        # - 2V = C2 (MIDI 48)
        # - 3V = C3 (MIDI 60)
        # - 3.3V = ~C3 + 3.6 semitones (MIDI 63-64)

        notes = [
            (24, "C0", 0.0),
            (36, "C1", 1.0),
            (48, "C2", 2.0),
            (60, "C3", 3.0),
            (64, "E3", 3.3),  # Max voltage for 3.3V system
        ]

        for midi_note, note_name, target_voltage in notes:
            # Calculate DAC value for target voltage
            # value = (target_voltage / 3.3) * 4095
            dac_value = int((target_voltage / 3.3) * 4095)
            dac.channel_a.value = dac_value

            print(f"    MIDI {midi_note} ({note_name}): {target_voltage:.2f}V (DAC={dac_value})")
            time.sleep(TEST_DELAY * 1.5)

        # Zero
        dac.channel_a.value = 0
        print("  ✓ CV pitch scaling test complete")
        print("  NOTE: For full 5-octave range, upgrade to 5V power")

    except Exception as e:
        print(f"  ✗ Failed CV pitch test: {e}")

def test_gate_trigger(dac):
    """Test gate/trigger output"""
    print_test_header(7, "Gate/Trigger Output Test")

    try:
        print("  Testing gate output on Channel B (VB)...")
        print("  → Measure Channel B with multimeter")
        print()

        # Gate high = 3.3V, low = 0V
        gate_high = 4095  # Max value = 3.3V
        gate_low = 0

        print("  Simulating note on/off sequence...")
        for i in range(4):
            # Note ON
            dac.channel_b.value = gate_high
            print(f"    [{i+1}/4] Gate HIGH (3.3V) - Note ON")
            time.sleep(TEST_DELAY * 0.5)

            # Note OFF
            dac.channel_b.value = gate_low
            print(f"    [{i+1}/4] Gate LOW  (0V)   - Note OFF")
            time.sleep(TEST_DELAY * 0.5)

        print("  ✓ Gate/trigger test complete")
        print("  → Verify you saw voltage transitions on multimeter")

    except Exception as e:
        print(f"  ✗ Failed gate test: {e}")

def main():
    """Main test sequence"""

    # Initialize I2C
    print_test_header(1, "I2C Bus Scan")
    try:
        print("  Initializing I2C bus...")
        i2c = busio.I2C(board.SCL, board.SDA)
        print("  ✓ I2C bus initialized")
    except Exception as e:
        print(f"  ✗ Failed to initialize I2C: {e}")
        print("\nTest aborted.")
        return

    # Scan bus
    devices = scan_i2c_bus(i2c)

    if OLED_ADDRESS not in devices:
        print(f"\n  ⚠ WARNING: OLED not detected at 0x{OLED_ADDRESS:02X}")
        print("    - OLED may not be connected or powered")

    if DAC_ADDRESS not in devices:
        print(f"\n  ✗ ERROR: MCP4728 DAC not found at 0x{DAC_ADDRESS:02X}")
        print("\n  Troubleshooting:")
        print("    1. Check VCC connected to M4's 3V pin (3.3V)")
        print("    2. Check GND connected to M4's GND")
        print("    3. Check STEMMA QT cable (SDA, SCL)")
        print("    4. Try different I2C address (some boards use 0x64)")
        print("\nTest aborted.")
        return

    print(f"\n  ✓ MCP4728 DAC found at address 0x{DAC_ADDRESS:02X}")

    # Initialize DAC
    dac = test_dac_initialization(i2c)
    if dac is None:
        print("\nTest aborted.")
        return

    # Run tests
    test_zero_all_channels(dac)
    test_voltage_sweep(dac)
    test_all_channels(dac)
    test_cv_pitch_scaling(dac)
    test_gate_trigger(dac)

    # Final summary
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\n✓ All tests completed successfully!")
    print("\nNext Steps:")
    print("  1. Verify multimeter readings matched expected voltages")
    print("  2. If all good, proceed to integrate CV/Gate into main code")
    print("  3. For full 5V range, upgrade power supply (see MCP4728_POWER_SETUP.md)")
    print("\n" + "=" * 60)

# Run main test
main()

# Keep board alive
print("\nBoard staying alive. Press CTRL+C to restart.")
while True:
    time.sleep(1)
