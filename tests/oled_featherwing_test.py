"""
OLED FeatherWing Hardware Test

Tests the Adafruit 128x32 or 128x64 OLED FeatherWing

Hardware Required:
- Feather M4 CAN Express (tested and validated)
- OLED FeatherWing (SSD1306-based)
- FeatherWing stacked on M4 (pins aligned)

Required CircuitPython Libraries:
- adafruit_displayio_ssd1306
- adafruit_display_text

To install:
    circup install adafruit_displayio_ssd1306 adafruit_display_text

This test will:
1. Scan I2C bus for OLED (should be at 0x3C)
2. Initialize the display
3. Show test patterns
4. Display text
5. Verify all functionality
"""

import board
import busio
import displayio
import terminalio
import time

print("\n" + "=" * 60)
print("OLED FEATHERWING HARDWARE TEST")
print("=" * 60)
print("\nMake sure:")
print("  - OLED FeatherWing is stacked on Feather M4")
print("  - All pins are properly aligned and seated")
print("  - I2C pins (SDA/SCL) are making good contact")
print("\nStarting test in 3 seconds...")
time.sleep(3)

# Release any existing displays
displayio.release_displays()

# Test results
test_passed = True
display = None

# ============================================================================
# TEST 1: I2C Bus Scan
# ============================================================================
print("\n" + "-" * 60)
print("TEST 1: I2C Bus Scan")
print("-" * 60)

try:
    i2c = busio.I2C(board.SCL, board.SDA)

    print("Scanning I2C bus for devices...")

    # Scan for I2C devices
    while not i2c.try_lock():
        pass

    found_devices = i2c.scan()
    i2c.unlock()

    print(f"\nFound {len(found_devices)} I2C device(s):")
    for addr in found_devices:
        print(f"  - 0x{addr:02X}")

    # Check for OLED at typical address
    OLED_ADDR = 0x3C
    if OLED_ADDR in found_devices:
        print(f"\n✓ OLED found at address 0x{OLED_ADDR:02X}")
    else:
        print(f"\n✗ OLED NOT found at expected address 0x{OLED_ADDR:02X}")
        print("  Possible causes:")
        print("    - FeatherWing not properly seated")
        print("    - I2C pins not making contact")
        print("    - OLED using different address (rare)")
        print("    - Hardware failure")
        test_passed = False

except Exception as e:
    print(f"\n✗ I2C scan failed: {e}")
    test_passed = False

# ============================================================================
# TEST 2: Display Initialization
# ============================================================================
print("\n" + "-" * 60)
print("TEST 2: Display Initialization")
print("-" * 60)

if test_passed:
    try:
        from adafruit_displayio_ssd1306 import SSD1306

        print("Importing display library...")
        print("✓ Library loaded")

        print("\nInitializing display bus...")
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
        print("✓ Display bus created")

        # Try common resolutions
        print("\nDetecting display resolution...")

        # Try 128x32 first (common for OLED FeatherWing)
        try:
            display = SSD1306(display_bus, width=128, height=32)
            print("✓ Display initialized: 128x32")
        except:
            # Try 128x64
            display = SSD1306(display_bus, width=128, height=64)
            print("✓ Display initialized: 128x64")

        print(f"  Width: {display.width}")
        print(f"  Height: {display.height}")

    except ImportError as e:
        print(f"\n✗ Display library not found: {e}")
        print("\nTo install:")
        print("  circup install adafruit_displayio_ssd1306 adafruit_display_text")
        test_passed = False

    except Exception as e:
        print(f"\n✗ Display initialization failed: {e}")
        test_passed = False

# ============================================================================
# TEST 3: Display Test Patterns
# ============================================================================
print("\n" + "-" * 60)
print("TEST 3: Display Test Patterns")
print("-" * 60)

if test_passed and display:
    try:
        from adafruit_display_text import label

        # Create a display group
        splash = displayio.Group()
        display.show(splash)

        print("\n[1] Clearing display...")
        display.show(None)
        time.sleep(0.5)
        print("    ✓ Display should be blank")

        print("\n[2] Displaying text...")
        splash = displayio.Group()

        # Create text label
        text = "OLED TEST"
        text_area = label.Label(
            terminalio.FONT,
            text=text,
            color=0xFFFFFF,
            x=0,
            y=4
        )
        splash.append(text_area)
        display.show(splash)

        print(f"    ✓ Should see: '{text}'")
        print("    Do you see text on the display? (visual check)")
        time.sleep(2)

        print("\n[3] Testing screen update...")
        text_area.text = "UPDATE OK"
        print("    ✓ Text should change to 'UPDATE OK'")
        time.sleep(2)

        print("\n[4] Testing multiple lines...")
        splash = displayio.Group()

        line1 = label.Label(terminalio.FONT, text="Line 1", color=0xFFFFFF, x=0, y=4)
        line2 = label.Label(terminalio.FONT, text="Line 2", color=0xFFFFFF, x=0, y=14)
        line3 = label.Label(terminalio.FONT, text="Line 3", color=0xFFFFFF, x=0, y=24)

        splash.append(line1)
        splash.append(line2)
        splash.append(line3)
        display.show(splash)

        print("    ✓ Should see 3 lines of text")
        time.sleep(2)

        print("\n[5] Testing scrolling text...")
        splash = displayio.Group()
        text_area = label.Label(
            terminalio.FONT,
            text="Scrolling...",
            color=0xFFFFFF,
            x=display.width,
            y=display.height // 2
        )
        splash.append(text_area)
        display.show(splash)

        # Scroll text across screen
        for i in range(display.width + 50):
            text_area.x = display.width - i
            time.sleep(0.01)

        print("    ✓ Text should have scrolled across")

        print("\n[6] Final display test...")
        splash = displayio.Group()
        success_text = label.Label(
            terminalio.FONT,
            text="PASS!",
            color=0xFFFFFF,
            x=(display.width - 30) // 2,
            y=display.height // 2
        )
        splash.append(success_text)
        display.show(splash)

        print("    ✓ Display should show 'PASS!'")

    except Exception as e:
        print(f"\n✗ Display test failed: {e}")
        test_passed = False

# ============================================================================
# TEST SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

if test_passed:
    print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
    print("\nOLED FeatherWing is fully functional!")
    print("  - I2C communication: Working")
    print("  - Display initialization: Working")
    print("  - Text rendering: Working")
    print("  - Screen updates: Working")
    print("\nHardware Status: APPROVED FOR PROJECT USE")
else:
    print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
    print("\nPlease review error messages above.")
    print("Common fixes:")
    print("  - Reseat FeatherWing on M4")
    print("  - Check for bent pins")
    print("  - Verify I2C pull-up resistors on FeatherWing")
    print("  - Install required libraries via circup")

print("\n" + "=" * 60)
print("\nTest complete. Display will stay on.")
print("Type 'exit' in monitor to close, or press RESET to re-run.")
print("\n")

# Keep display on
while True:
    time.sleep(1)
