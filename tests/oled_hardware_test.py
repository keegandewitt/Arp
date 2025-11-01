"""
Simple OLED Hardware Test
Verifies OLED FeatherWing is connected and working
"""

import board
import time
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1107

print("\n" + "="*60)
print("OLED HARDWARE TEST")
print("="*60)
print("\nTesting OLED FeatherWing 128x64 (SH1107)")
print("="*60 + "\n")

# Step 1: Initialize I2C
print("[1/4] Initializing I2C bus...")
try:
    i2c = board.I2C()
    print("      ✓ I2C initialized")
except Exception as e:
    print(f"      ✗ FAILED: {e}")
    print("\n⚠️ Check I2C connections (D21=SDA, D22=SCL)")
    while True:
        time.sleep(1)

# Step 2: Create display
print("[2/4] Creating display...")
try:
    displayio.release_displays()
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
    display = adafruit_displayio_sh1107.SH1107(
        display_bus,
        width=128,
        height=64
    )
    display.brightness = 0.8
    print("      ✓ Display created (SH1107 @ 0x3C)")
except Exception as e:
    print(f"      ✗ FAILED: {e}")
    print("\n⚠️ Possible issues:")
    print("   - OLED not connected")
    print("   - Wrong I2C address (should be 0x3C)")
    print("   - Library not installed: circup install adafruit_displayio_sh1107")
    while True:
        time.sleep(1)

# Step 3: Create simple display group
print("[3/4] Creating display content...")
group = displayio.Group()

# Title
title = label.Label(
    terminalio.FONT,
    text="OLED TEST",
    color=0xFFFFFF,
    x=30,
    y=10
)
group.append(title)

# Status
status = label.Label(
    terminalio.FONT,
    text="Hardware OK!",
    color=0xFFFFFF,
    x=20,
    y=30
)
group.append(status)

# Info line
info = label.Label(
    terminalio.FONT,
    text="SH1107 128x64",
    color=0xFFFFFF,
    x=15,
    y=50
)
group.append(info)

display.root_group = group
print("      ✓ Content created")

# Step 4: Test display updates
print("[4/4] Testing display updates...")
print("      CHECK OLED: Should show 'OLED TEST'")
time.sleep(2)

# Animate a counter
print("\n" + "="*60)
print("✓ OLED WORKING!")
print("="*60)
print("\nAnimating counter on display...")
print("(Watch the OLED screen)")

counter_label = label.Label(
    terminalio.FONT,
    text="Count: 0",
    color=0xFFFFFF,
    x=30,
    y=50
)
group.append(counter_label)

for i in range(10):
    counter_label.text = f"Count: {i}"
    print(f"  Display updated: {i}")
    time.sleep(0.5)

# Final success message
print("\n" + "="*60)
print("✓✓✓ OLED HARDWARE TEST PASSED ✓✓✓")
print("="*60)
print("\nOLED FeatherWing is working correctly!")
print("Ready for integration with arpeggiator code.")

# Show final success screen
group = displayio.Group()
success1 = label.Label(terminalio.FONT, text="TEST PASSED!", color=0xFFFFFF, x=15, y=20)
success2 = label.Label(terminalio.FONT, text="OLED Ready", color=0xFFFFFF, x=20, y=40)
group.append(success1)
group.append(success2)
display.root_group = group

print("\nKeeping display on... (press CTRL+C to exit)")
while True:
    time.sleep(1)
