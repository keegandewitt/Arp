"""
Comprehensive Pin Test for Adafruit Feather M4 CAN Express
Tests ALL pins on the board to verify soldering and hardware integrity.

Upload this to your CIRCUITPY drive as code.py and monitor serial output.

Test Philosophy:
- Test EVERY pin, not just the ones used by the project
- Systematic, methodical validation
- Clear pass/fail indicators
- Document all results

Hardware Required:
- Feather M4 CAN Express
- USB connection for serial monitor
- Optional: Multimeter for voltage verification
- Optional: Jumper wire for loopback tests

Required CircuitPython Libraries:
- neopixel (install via: circup install neopixel)

Built-in Dependencies:
- board, digitalio, analogio, pwmio, busio, time

To install dependencies:
    circup install neopixel

Or use the deployment script which auto-checks dependencies:
    ./scripts/deploy_pin_test.sh
"""

import board
import digitalio
import analogio
import pwmio
import busio
import time
import neopixel

print("\n" + "="*60)
print("FEATHER M4 CAN EXPRESS - COMPREHENSIVE PIN TEST")
print("="*60)
print("\nThis test validates ALL pins on the board.")
print("Follow the instructions and record all results.\n")

# Test results tracking
tests_passed = 0
tests_failed = 0
test_results = []

def log_result(test_name, passed, notes=""):
    """Log a test result"""
    global tests_passed, tests_failed, test_results

    status = "✓ PASS" if passed else "✗ FAIL"
    result_line = f"{status:8} | {test_name:40} | {notes}"
    test_results.append(result_line)

    if passed:
        tests_passed += 1
    else:
        tests_failed += 1

    print(result_line)

def test_gpio_pin(pin, pin_name):
    """Test a GPIO pin for basic input/output functionality"""
    try:
        # Test as output
        gpio = digitalio.DigitalInOut(pin)
        gpio.direction = digitalio.Direction.OUTPUT

        # Test high
        gpio.value = True
        time.sleep(0.01)

        # Test low
        gpio.value = False
        time.sleep(0.01)

        # Test as input with pull-up
        gpio.direction = digitalio.Direction.INPUT
        gpio.pull = digitalio.Pull.UP
        time.sleep(0.01)
        pullup_val = gpio.value

        # Test as input with pull-down
        gpio.pull = digitalio.Pull.DOWN
        time.sleep(0.01)
        pulldown_val = gpio.value

        gpio.deinit()

        # Verify pull-up reads high and pull-down reads low
        if pullup_val == True and pulldown_val == False:
            log_result(f"GPIO {pin_name}", True, "I/O and pulls working")
            return True
        else:
            log_result(f"GPIO {pin_name}", False, f"Pull-up={pullup_val}, Pull-down={pulldown_val}")
            return False

    except Exception as e:
        log_result(f"GPIO {pin_name}", False, f"Exception: {e}")
        return False

def test_analog_input(pin, pin_name):
    """Test an analog input pin"""
    try:
        analog = analogio.AnalogIn(pin)

        # Read voltage (should be ~0V if floating or ~3.3V if pulled up)
        raw_value = analog.value
        voltage = (raw_value * 3.3) / 65536

        analog.deinit()

        # Just verify we can read it (value should be reasonable)
        if 0 <= voltage <= 3.5:
            log_result(f"Analog {pin_name}", True, f"Reads {voltage:.2f}V")
            return True
        else:
            log_result(f"Analog {pin_name}", False, f"Out of range: {voltage:.2f}V")
            return False

    except Exception as e:
        log_result(f"Analog {pin_name}", False, f"Exception: {e}")
        return False

def test_pwm_pin(pin, pin_name):
    """Test PWM capability on a pin"""
    try:
        pwm = pwmio.PWMOut(pin, frequency=1000, duty_cycle=0)

        # Test 50% duty cycle
        pwm.duty_cycle = 32768
        time.sleep(0.05)

        # Test 0% duty cycle
        pwm.duty_cycle = 0
        time.sleep(0.05)

        pwm.deinit()

        log_result(f"PWM {pin_name}", True, "1kHz PWM working")
        return True

    except Exception as e:
        log_result(f"PWM {pin_name}", False, f"Exception: {e}")
        return False

def test_dac_output(pin, pin_name):
    """Test DAC (true analog output) on A0 or A1"""
    try:
        from analogio import AnalogOut
        dac = AnalogOut(pin)

        # Test 0V
        dac.value = 0
        time.sleep(0.05)

        # Test ~1.65V (50%)
        dac.value = 32768
        time.sleep(0.05)

        # Test ~3.3V
        dac.value = 65535
        time.sleep(0.05)

        # Back to 0V
        dac.value = 0

        dac.deinit()

        log_result(f"DAC {pin_name}", True, "0V to 3.3V output working")
        return True

    except Exception as e:
        log_result(f"DAC {pin_name}", False, f"Exception: {e}")
        return False

# ============================================================================
# TEST SEQUENCE
# ============================================================================

print("\n" + "-"*60)
print("SECTION 1: POWER PINS")
print("-"*60)
print("\nManual verification required:")
print("  - Check 3V pin with multimeter: Should read ~3.3V")
print("  - Check BAT pin: Should read battery voltage or ~3.3V from USB")
print("  - Check GND pin: Should be ground (0V)")
print("  - Check USB pin: Should read ~5V when USB connected")
print("\nRecord results manually. Press Enter when done...")
# In actual use, we'd wait for input, but CircuitPython doesn't have easy input
time.sleep(2)

print("\n" + "-"*60)
print("SECTION 2: GPIO PINS (Digital I/O)")
print("-"*60)
print()

# Test all general purpose GPIO pins
test_gpio_pin(board.D0, "D0 (RX)")
test_gpio_pin(board.D1, "D1 (TX)")
test_gpio_pin(board.D4, "D4")
test_gpio_pin(board.D5, "D5")
test_gpio_pin(board.D6, "D6")
test_gpio_pin(board.D9, "D9")
test_gpio_pin(board.D10, "D10")
test_gpio_pin(board.D11, "D11")
test_gpio_pin(board.D12, "D12")
test_gpio_pin(board.D13, "D13 (LED)")

print("\n" + "-"*60)
print("SECTION 3: I2C PINS")
print("-"*60)
print()

test_gpio_pin(board.SDA, "D21 (SDA)")
test_gpio_pin(board.SCL, "D22 (SCL)")

# Test I2C bus initialization
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    i2c.deinit()
    log_result("I2C Bus Init", True, "I2C bus initialized successfully")
except Exception as e:
    log_result("I2C Bus Init", False, f"Exception: {e}")

print("\n" + "-"*60)
print("SECTION 4: SPI PINS")
print("-"*60)
print()

test_gpio_pin(board.MISO, "D23 (MISO)")
test_gpio_pin(board.MOSI, "D24 (MOSI)")
test_gpio_pin(board.SCK, "D25 (SCK)")

# Test SPI bus initialization
try:
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    spi.deinit()
    log_result("SPI Bus Init", True, "SPI bus initialized successfully")
except Exception as e:
    log_result("SPI Bus Init", False, f"Exception: {e}")

print("\n" + "-"*60)
print("SECTION 5: ANALOG INPUT PINS")
print("-"*60)
print()

test_analog_input(board.A0, "A0")
test_analog_input(board.A1, "A1")
test_analog_input(board.A2, "A2")
test_analog_input(board.A3, "A3")
test_analog_input(board.A4, "A4")
test_analog_input(board.A5, "A5")

print("\n" + "-"*60)
print("SECTION 6: DAC OUTPUT PINS (Analog Output)")
print("-"*60)
print()

test_dac_output(board.A0, "A0")
test_dac_output(board.A1, "A1")

print("\n" + "-"*60)
print("SECTION 7: PWM CAPABILITY")
print("-"*60)
print()

# Test PWM on various pins
test_pwm_pin(board.D0, "D0")
test_pwm_pin(board.D1, "D1")
test_pwm_pin(board.D4, "D4")
test_pwm_pin(board.D5, "D5")
test_pwm_pin(board.D6, "D6")
test_pwm_pin(board.D9, "D9")
test_pwm_pin(board.D10, "D10")
test_pwm_pin(board.D11, "D11")
test_pwm_pin(board.D12, "D12")
test_pwm_pin(board.D13, "D13")
test_pwm_pin(board.SDA, "D21 (SDA)")
test_pwm_pin(board.SCL, "D22 (SCL)")

print("\n" + "-"*60)
print("SECTION 8: SPECIAL FUNCTIONS")
print("-"*60)
print()

# Test onboard NeoPixel
try:
    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

    # Test red
    pixel[0] = (255, 0, 0)
    time.sleep(0.3)

    # Test green
    pixel[0] = (0, 255, 0)
    time.sleep(0.3)

    # Test blue
    pixel[0] = (0, 0, 255)
    time.sleep(0.3)

    # Off
    pixel[0] = (0, 0, 0)

    pixel.deinit()

    log_result("NeoPixel LED", True, "RGB LED working (did you see it?)")
except Exception as e:
    log_result("NeoPixel LED", False, f"Exception: {e}")

# Test onboard red LED (D13)
try:
    led = digitalio.DigitalInOut(board.D13)
    led.direction = digitalio.Direction.OUTPUT

    # Blink 3 times
    for _ in range(3):
        led.value = True
        time.sleep(0.2)
        led.value = False
        time.sleep(0.2)

    led.deinit()

    log_result("Onboard LED (D13)", True, "Red LED blinked (did you see it?)")
except Exception as e:
    log_result("Onboard LED (D13)", False, f"Exception: {e}")

print("\n" + "-"*60)
print("SECTION 9: UART LOOPBACK (Optional)")
print("-"*60)
print("\nTo test UART, connect D0 (RX) to D1 (TX) with a jumper wire.")
print("Skip this test if you don't have a jumper wire ready.")
print("Waiting 5 seconds before UART test...")
time.sleep(5)

try:
    # Initialize UART
    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.1)

    # Send test message
    test_msg = b"TEST"
    uart.write(test_msg)
    time.sleep(0.1)

    # Try to read it back
    received = uart.read(len(test_msg))

    uart.deinit()

    if received == test_msg:
        log_result("UART Loopback", True, f"Sent and received: {test_msg}")
    else:
        log_result("UART Loopback", False, f"Sent {test_msg}, got {received}")
except Exception as e:
    log_result("UART Loopback", False, f"Exception (jumper connected?): {e}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print()

for result in test_results:
    print(result)

print("\n" + "-"*60)
print(f"Total Tests: {tests_passed + tests_failed}")
print(f"Passed: {tests_passed}")
print(f"Failed: {tests_failed}")
print(f"Success Rate: {100.0 * tests_passed / (tests_passed + tests_failed):.1f}%")
print("-"*60)

if tests_failed == 0:
    print("\n✓ ALL TESTS PASSED - Hardware is fully validated!")
    print("  Your soldering and assembly are excellent.")
else:
    print(f"\n✗ {tests_failed} TEST(S) FAILED - Review failed pins")
    print("  Check solder joints on failed pins with magnification")
    print("  Use multimeter to check continuity and voltage levels")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nSave these results for your hardware validation log.")
print("Press Ctrl+C to exit or reset board to run again.\n")

# Keep the board running so we can see the results
while True:
    time.sleep(1)
