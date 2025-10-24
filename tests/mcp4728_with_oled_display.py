"""MCP4728 Test with OLED Display Feedback"""
import board
import digitalio
import displayio
import time

# LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Initialize I2C
i2c = board.I2C()

# Initialize OLED
displayio.release_displays()

from i2cdisplaybus import I2CDisplayBus
import adafruit_displayio_sh1107
from adafruit_display_text import label
import terminalio

display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(
    display_bus,
    width=128,
    height=64,
    rotation=90
)

splash = displayio.Group()

text1 = label.Label(terminalio.FONT, text="MCP4728 Test", color=0xFFFFFF, x=5, y=8)
text2 = label.Label(terminalio.FONT, text="Status:", color=0xFFFFFF, x=5, y=24)
text3 = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=5, y=40)
text4 = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=5, y=56)

splash.append(text1)
splash.append(text2)
splash.append(text3)
splash.append(text4)
display.root_group = splash

def update_display(line2="", line3="", line4=""):
    text2.text = line2
    text3.text = line3
    text4.text = line4
    display.refresh()

# Blink start
for i in range(3):
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)

# Scan I2C
update_display("Scanning I2C...", "", "")
time.sleep(0.5)

while not i2c.try_lock():
    pass
devices = i2c.scan()
i2c.unlock()

oled_found = 0x3C in devices
mcp_addr = None
for addr in [0x60, 0x61, 0x64, 0x66]:
    if addr in devices:
        mcp_addr = addr
        break

if mcp_addr:
    update_display(f"OLED: 0x3C", f"MCP: 0x{mcp_addr:02X}", "Initializing...")
    led.value = True
    time.sleep(1)
    led.value = False
else:
    update_display("ERROR:", "MCP4728 not", "detected!")
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

# Initialize MCP4728
import adafruit_mcp4728

try:
    dac = adafruit_mcp4728.MCP4728(i2c, address=mcp_addr)
    update_display("DAC Init OK", "Configuring", "for 5V...")
    time.sleep(1)

    # Configure for 5V external reference
    for channel in [dac.channel_a, dac.channel_b, dac.channel_c, dac.channel_d]:
        channel.vref = adafruit_mcp4728.Vref.VDD
        channel.gain = 1

    update_display("Config OK", "VDD ref, 1x", "Ready!")
    time.sleep(1)

except Exception as e:
    update_display("ERROR:", "Init failed", str(e)[:12])
    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)

# Test voltage sweep on Channel A
update_display("Voltage Sweep", "Channel A", "0V -> 5V")
time.sleep(1)

steps = [
    (0, "0.00V"),
    (1024, "1.25V"),
    (2048, "2.50V"),
    (3072, "3.75V"),
    (4095, "5.00V"),
]

for value, voltage in steps:
    dac.channel_a.value = value
    update_display("Channel A", voltage, f"Val: {value}")
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(1.5)

# Zero
dac.channel_a.value = 0
update_display("Sweep Done!", "Ch A -> 0V", "")
time.sleep(1)

# Test all channels
update_display("Testing all", "channels at", "2.5V...")
time.sleep(1)

channels = [
    (dac.channel_a, "Ch A"),
    (dac.channel_b, "Ch B"),
    (dac.channel_c, "Ch C"),
    (dac.channel_d, "Ch D"),
]

for channel, name in channels:
    dac.channel_a.value = 0
    dac.channel_b.value = 0
    dac.channel_c.value = 0
    dac.channel_d.value = 0

    channel.value = 2048
    update_display(f"{name}: 2.5V", "Measure output", "")
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(1.5)

# Zero all
dac.channel_a.value = 0
dac.channel_b.value = 0
dac.channel_c.value = 0
dac.channel_d.value = 0

# Gate test
update_display("Gate Test", "Channel B", "5 cycles")
time.sleep(1)

for i in range(5):
    dac.channel_b.value = 4095
    update_display(f"Gate {i+1}/5", "HIGH (5V)", "")
    led.value = True
    time.sleep(0.5)

    dac.channel_b.value = 0
    update_display(f"Gate {i+1}/5", "LOW (0V)", "")
    led.value = False
    time.sleep(0.5)

# Success!
update_display("ALL TESTS", "PASSED!", "CV Ready!")
time.sleep(2)

# Heartbeat mode
count = 0
while True:
    count += 1
    update_display("MCP4728 OK", f"Heartbeat {count}", "Ready for CV")
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(1.9)
