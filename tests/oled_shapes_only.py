"""
Test OLED with shapes only (no text library) to rule out text rendering issues
"""

import board
import displayio
import time
import i2cdisplaybus
import adafruit_displayio_ssd1306

print("\n=== OLED Shapes Test ===\n")

displayio.release_displays()

i2c = board.I2C()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

# Create display
display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=128,
    height=64
)

display.brightness = 1.0

# Create a simple bitmap pattern
bitmap = displayio.Bitmap(128, 64, 2)
palette = displayio.Palette(2)
palette[0] = 0x000000  # Black
palette[1] = 0xFFFFFF  # White

# Draw a pattern:
# - Border around the edge
# - Horizontal line at y=32 (middle)
# - Vertical line at x=64 (middle)

# Top and bottom borders
for x in range(128):
    bitmap[x, 0] = 1    # Top edge
    bitmap[x, 63] = 1   # Bottom edge

# Left and right borders
for y in range(64):
    bitmap[0, y] = 1    # Left edge
    bitmap[127, y] = 1  # Right edge

# Middle lines
for x in range(128):
    bitmap[x, 32] = 1  # Horizontal middle

for y in range(64):
    bitmap[64, y] = 1  # Vertical middle

# Create tile grid
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create group and show
splash = displayio.Group()
splash.append(tile_grid)

display.root_group = splash

print("Display should show:")
print("- Border around all 4 edges")
print("- Cross through the middle")
print("- This tests the full 128x64 area")
print("")
print("=== CHECK DISPLAY ===")

while True:
    time.sleep(1)
