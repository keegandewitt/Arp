"""
Test different SSD1306 COM pin configurations
The garbled bottom half might be due to wrong COM pin config

SSD1306 Command 0xDA (Set COM Pins Hardware Configuration):
- 0x02: Sequential, no left/right remap
- 0x12: Alternative, no left/right remap (default in library)
- 0x22: Sequential, enable left/right remap
- 0x32: Alternative, enable left/right remap
"""

import board
import busio
import time
import displayio

print("\n=== SSD1306 Raw Init Test ===\n")

displayio.release_displays()

# Create I2C
i2c = board.I2C()
while not i2c.try_lock():
    pass

# SSD1306 I2C address
ADDR = 0x3C

def send_command(cmd):
    """Send a command byte to SSD1306"""
    i2c.writeto(ADDR, bytes([0x00, cmd]))  # 0x00 = command mode

def init_ssd1306_128x64(com_pins_config=0x12):
    """Initialize SSD1306 with specific COM pins config"""
    print(f"Initializing with COM config: 0x{com_pins_config:02X}")

    # Display OFF
    send_command(0xAE)

    # Set memory addressing mode to horizontal (0x00)
    send_command(0x20)
    send_command(0x00)

    # Set contrast
    send_command(0x81)
    send_command(0xCF)

    # Segment remap (column 127 mapped to SEG0)
    send_command(0xA1)

    # Normal display (not inverted)
    send_command(0xA6)

    # COM output scan direction (remapped mode, scan from COM[N-1] to COM0)
    send_command(0xC8)

    # Set multiplex ratio for 64 lines (0x3F = 63, meaning 64 lines)
    send_command(0xA8)
    send_command(0x3F)

    # Set display clock divide ratio
    send_command(0xD5)
    send_command(0x80)

    # Set pre-charge period
    send_command(0xD9)
    send_command(0xF1)

    # **Set COM pins hardware configuration** (THIS IS WHAT WE'RE TESTING)
    send_command(0xDA)
    send_command(com_pins_config)  # Try different values!

    # Set VCOMH deselect level
    send_command(0xDB)
    send_command(0x40)

    # Enable charge pump
    send_command(0x8D)
    send_command(0x14)

    # Display ON
    send_command(0xAF)

    time.sleep(0.1)

def clear_display():
    """Clear the display by writing zeros"""
    # Set column address range (0-127)
    send_command(0x21)
    send_command(0x00)
    send_command(0x7F)

    # Set page address range (0-7 for 64 rows)
    send_command(0x22)
    send_command(0x00)
    send_command(0x07)

    # Write zeros (128 columns * 8 pages = 1024 bytes)
    for page in range(8):
        data = bytes([0x40] + [0x00] * 128)  # 0x40 = data mode
        i2c.writeto(ADDR, data)

def draw_test_pattern():
    """Draw a simple test pattern"""
    # Set address range
    send_command(0x21)  # Column address
    send_command(0x00)
    send_command(0x7F)

    send_command(0x22)  # Page address
    send_command(0x00)
    send_command(0x07)

    # Draw pattern: alternating lines
    for page in range(8):
        if page % 2 == 0:
            data = bytes([0x40] + [0xFF] * 128)  # Solid line
        else:
            data = bytes([0x40] + [0xAA] * 128)  # Dotted line
        i2c.writeto(ADDR, data)

# Test different COM configurations
configs_to_test = [
    (0x02, "Sequential, no remap"),
    (0x12, "Alternative, no remap (library default)"),
    (0x22, "Sequential, with remap"),
    (0x32, "Alternative, with remap"),
]

print("Testing different COM pin configurations...")
print("Each will display for 10 seconds\n")

for com_config, description in configs_to_test:
    print(f"\n--- Testing 0x{com_config:02X}: {description} ---")

    init_ssd1306_128x64(com_config)
    clear_display()
    draw_test_pattern()

    print(f"Check display now! (10 seconds)")
    print("Pattern should be clear horizontal stripes")
    print("If garbled, this COM config is wrong\n")
    time.sleep(10)

print("\n=== Test Complete ===")
print("Which COM configuration looked best?")
print("Note the number and we'll update the library config")

i2c.unlock()

while True:
    time.sleep(1)
