"""
Gate Trigger Mode Test - V-TRIG vs S-TRIG

Button A: Fire gate pulse
Button B: Toggle between V-TRIG and S-TRIG

Based on working mcp4728_correct_voltage_test.py baseline
"""

import time
import board
import digitalio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_sh1107 import SH1107
import adafruit_mcp4728

# Setup LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Setup Button A (fire gate pulse)
button_a = digitalio.DigitalInOut(board.D5)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

# Setup Button B (toggle mode)
button_b = digitalio.DigitalInOut(board.D6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

print("\n" + "="*60)
print("GATE TRIGGER MODE TEST")
print("="*60)

# STEP 1: I2C Bus Setup
displayio.release_displays()
time.sleep(0.2)
i2c = board.I2C()
print("\n[1] I2C bus ready")

# STEP 2: Initialize OLED
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = SH1107(display_bus, width=128, height=64)
print("[2] OLED initialized")

# STEP 3: Initialize MCP4728
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
print("[3] MCP4728 detected")

# STEP 4: Wake and configure DAC
dac.wakeup()
time.sleep(0.1)

# Configure Channel C for gate output
dac.channel_c.vref = adafruit_mcp4728.Vref.VDD
dac.channel_c.gain = 1
time.sleep(0.1)

dac.save_settings()
time.sleep(0.3)
print("[4] DAC configured (Channel C for gate)")

# STEP 5: Setup display
splash = displayio.Group()
display.root_group = splash

title = label.Label(terminalio.FONT, text="Gate Test", x=10, y=5, color=0xFFFFFF)
line1 = label.Label(terminalio.FONT, text="V-TRIG", x=5, y=25, color=0xFFFFFF)
line2 = label.Label(terminalio.FONT, text="Idle: 0V", x=5, y=40, color=0xFFFFFF)
line3 = label.Label(terminalio.FONT, text="Active: 5V", x=5, y=55, color=0xFFFFFF)

splash.append(title)
splash.append(line1)
splash.append(line2)
splash.append(line3)

print("[5] Display ready")
print("\n" + "="*60)
print("Button A: Fire gate pulse")
print("Button B: Toggle V-TRIG/S-TRIG")
print("="*60)

# Gate mode state
gate_mode = "V-TRIG"
pulse_count = 0

# Set gate to idle (V-TRIG starts at 0V)
dac.channel_c.raw_value = 0

print("\nReady! Press buttons to test\n")

while True:
    # Button B: Toggle mode
    if not button_b.value:
        if gate_mode == "V-TRIG":
            gate_mode = "S-TRIG"
            line1.text = "S-TRIG"
            line2.text = "Idle: 5V"
            line3.text = "Active: 0V"
            dac.channel_c.raw_value = 4095  # S-TRIG idle = 5V
            print("Mode: S-TRIG (idle 5V, active 0V)")
        else:
            gate_mode = "V-TRIG"
            line1.text = "V-TRIG"
            line2.text = "Idle: 0V"
            line3.text = "Active: 5V"
            dac.channel_c.raw_value = 0  # V-TRIG idle = 0V
            print("Mode: V-TRIG (idle 0V, active 5V)")

        # Wait for button release
        while not button_b.value:
            time.sleep(0.05)
        time.sleep(0.2)

    # Button A: Fire gate pulse
    if not button_a.value:
        pulse_count += 1

        if gate_mode == "V-TRIG":
            # V-TRIG: 0V -> 5V -> 0V
            print(f"[{pulse_count}] V-TRIG pulse")
            dac.channel_c.raw_value = 4095  # Active = 5V
            led.value = True
            time.sleep(0.1)  # 100ms pulse
            dac.channel_c.raw_value = 0     # Back to 0V
            led.value = False
        else:
            # S-TRIG: 5V -> 0V -> 5V
            print(f"[{pulse_count}] S-TRIG pulse")
            dac.channel_c.raw_value = 0     # Active = 0V
            led.value = True
            time.sleep(0.1)  # 100ms pulse
            dac.channel_c.raw_value = 4095  # Back to 5V
            led.value = False

        # Wait for button release
        while not button_a.value:
            time.sleep(0.05)
        time.sleep(0.1)

    time.sleep(0.05)
