"""
Connection Test Script for M4 Express + OLED FeatherWing

This script tests:
- I2C connection to OLED display (address 0x3C)
- OLED display functionality
- Button A, B, C functionality
- Basic hardware setup verification

Press each button to test it. Press all three buttons simultaneously to exit.
"""

import board
import busio
import digitalio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import time

print("\n" + "="*50)
print("M4 Express + OLED FeatherWing Connection Test")
print("="*50 + "\n")

# Test 1: I2C Bus Initialization
print("[1/4] Testing I2C bus initialization...")
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("  ✓ I2C bus initialized successfully")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    print("  Check: SCL and SDA connections")
    raise

# Test 2: I2C Device Scan
print("\n[2/4] Scanning I2C bus for devices...")
try:
    while not i2c.try_lock():
        pass
    devices = i2c.scan()
    i2c.unlock()

    print(f"  Found {len(devices)} device(s) at address(es): ", end="")
    for device in devices:
        print(f"0x{device:02X} ", end="")
    print()

    if 0x3C in devices:
        print("  ✓ OLED display found at 0x3C")
    else:
        print("  ✗ OLED display NOT found at expected address 0x3C")
        print("  Check: OLED FeatherWing is properly seated")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    raise

# Test 3: OLED Display Initialization
print("\n[3/4] Initializing OLED display...")
try:
    displayio.release_displays()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(
        display_bus,
        width=128,
        height=32
    )
    display.brightness = 0.8  # Bright for testing
    print("  ✓ OLED display initialized (128x32)")

    # Create display group
    group = displayio.Group()

    # Title
    title_label = label.Label(
        terminalio.FONT,
        text="Connection Test",
        color=0xFFFFFF,
        x=0,
        y=4
    )

    # Status line
    status_label = label.Label(
        terminalio.FONT,
        text="Press buttons...",
        color=0xFFFFFF,
        x=0,
        y=16
    )

    # Button status line
    button_label = label.Label(
        terminalio.FONT,
        text="A:_ B:_ C:_",
        color=0xFFFFFF,
        x=0,
        y=28
    )

    group.append(title_label)
    group.append(status_label)
    group.append(button_label)
    display.root_group = group

    print("  ✓ Display test pattern shown")
    time.sleep(2)

except Exception as e:
    print(f"  ✗ FAILED: {e}")
    print("  Check: OLED FeatherWing connections and seating")
    raise

# Test 4: Button Initialization and Testing
print("\n[4/4] Testing buttons...")
try:
    # Initialize buttons (active low with pullup)
    button_a = digitalio.DigitalInOut(board.D9)
    button_a.direction = digitalio.Direction.INPUT
    button_a.pull = digitalio.Pull.UP

    button_b = digitalio.DigitalInOut(board.D6)
    button_b.direction = digitalio.Direction.INPUT
    button_b.pull = digitalio.Pull.UP

    button_c = digitalio.DigitalInOut(board.D5)
    button_c.direction = digitalio.Direction.INPUT
    button_c.pull = digitalio.Pull.UP

    print("  ✓ Buttons initialized (D9=A, D6=B, D5=C)")

    # Track which buttons have been tested
    button_a_tested = False
    button_b_tested = False
    button_c_tested = False

    status_label.text = "Press each button"

    print("\n  Interactive button test:")
    print("  - Press Button A (leftmost)")
    print("  - Press Button B (middle)")
    print("  - Press Button C (rightmost)")
    print("  - Press all 3 together to exit")
    print()

    # Interactive test loop
    last_a = True
    last_b = True
    last_c = True

    while True:
        # Read button states (inverted because active low)
        a_pressed = not button_a.value
        b_pressed = not button_b.value
        c_pressed = not button_c.value

        # Detect button presses (falling edge)
        if a_pressed and last_a is False:
            if not button_a_tested:
                print("  ✓ Button A working")
                button_a_tested = True

        if b_pressed and last_b is False:
            if not button_b_tested:
                print("  ✓ Button B working")
                button_b_tested = True

        if c_pressed and last_c is False:
            if not button_c_tested:
                print("  ✓ Button C working")
                button_c_tested = True

        # Update display
        button_label.text = f"A:{'X' if a_pressed else '_'} B:{'X' if b_pressed else '_'} C:{'X' if c_pressed else '_'}"

        # Check if all buttons tested
        if button_a_tested and button_b_tested and button_c_tested:
            status_label.text = "All buttons OK!"

            # Check for all 3 pressed to exit
            if a_pressed and b_pressed and c_pressed:
                break

        # Save states for edge detection
        last_a = a_pressed
        last_b = b_pressed
        last_c = c_pressed

        time.sleep(0.05)  # 50ms debounce

    print("\n  ✓ All buttons tested successfully")

except Exception as e:
    print(f"  ✗ FAILED: {e}")
    print("  Check: Button pins D9, D6, D5")
    raise

# Final success message
print("\n" + "="*50)
print("✓ ALL TESTS PASSED - Hardware is ready!")
print("="*50)

status_label.text = "Tests PASSED!"
time.sleep(2)

# Clean shutdown message
title_label.text = "Ready for"
status_label.text = "main program!"
button_label.text = ""
time.sleep(2)

print("\nYou can now upload your main code (code.py)")
print("Connection test complete.\n")
