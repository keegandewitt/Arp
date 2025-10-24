"""OLED Recovery Test - Get display working again"""
import board
import digitalio
import displayio
import time

# LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

print("\n=== OLED Recovery Test ===")

# Blink to show starting
for i in range(3):
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)

print("Initializing I2C...")
try:
    i2c = board.I2C()
    print("I2C OK")
    led.value = True
    time.sleep(0.5)
    led.value = False
except Exception as e:
    print(f"I2C failed: {e}")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

print("Importing OLED library...")
try:
    import adafruit_displayio_sh1107
    print("Library OK")
except Exception as e:
    print(f"Import failed: {e}")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

print("Initializing display...")
try:
    displayio.release_displays()

    from i2cdisplaybus import I2CDisplayBus
    display_bus = I2CDisplayBus(i2c, device_address=0x3C)

    WIDTH = 128
    HEIGHT = 64
    display = adafruit_displayio_sh1107.SH1107(
        display_bus,
        width=WIDTH,
        height=HEIGHT,
        rotation=90
    )

    print("Display initialized!")
    led.value = True
    time.sleep(0.5)
    led.value = False

except Exception as e:
    print(f"Display init failed: {e}")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

print("Creating text...")
try:
    from adafruit_display_text import label
    import terminalio

    splash = displayio.Group()

    text1 = label.Label(
        terminalio.FONT,
        text="OLED Working!",
        color=0xFFFFFF,
        x=10,
        y=10
    )

    text2 = label.Label(
        terminalio.FONT,
        text="Ready for MCP",
        color=0xFFFFFF,
        x=10,
        y=30
    )

    splash.append(text1)
    splash.append(text2)
    display.root_group = splash

    print("Text displayed!")
    print("\nOLED should show:")
    print("  OLED Working!")
    print("  Ready for MCP")

except Exception as e:
    print(f"Text failed: {e}")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

print("\nSuccess! Entering heartbeat mode...")

# Fast heartbeat = success
while True:
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.4)
