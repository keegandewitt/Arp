"""
Dual Gate Output Test - V-TRIG and True S-TRIG

Button A: Fire gate pulse
Button B: Toggle between V-TRIG and S-TRIG modes

V-TRIG Output: MCP4728 Channel C (voltage-based)
  - Idle: 0V, Active: 5V
  - Use for: Modern synths, Eurorack

S-TRIG Output: GPIO D10 + NPN transistor (switch-based)
  - Idle: Open circuit, Active: Short to GND
  - Use for: ARP 2600, Korg MS-20, Yamaha CS series

Hardware Required:
- MCP4728 DAC on I2C (for V-TRIG)
- NPN transistor circuit on D10 (for S-TRIG)
- OLED display
- Buttons A and B
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

# Setup S-Trig GPIO (D10)
strig_gpio = digitalio.DigitalInOut(board.D10)
strig_gpio.direction = digitalio.Direction.OUTPUT
strig_gpio.value = False  # Start with S-Trig idle (open circuit)

print("\n" + "="*60)
print("DUAL GATE OUTPUT TEST - V-TRIG & TRUE S-TRIG")
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

# STEP 3: Initialize MCP4728 for V-TRIG
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
print("[3] MCP4728 detected")

# STEP 4: Wake and configure DAC Channel C for V-TRIG
dac.wakeup()
time.sleep(0.1)

dac.channel_c.vref = adafruit_mcp4728.Vref.VDD
dac.channel_c.gain = 1
time.sleep(0.1)

dac.save_settings()
time.sleep(0.3)
print("[4] V-TRIG output configured (MCP4728 Ch C)")
print("[5] S-TRIG output configured (GPIO D10)")

# STEP 6: Setup display
splash = displayio.Group()
display.root_group = splash

title = label.Label(terminalio.FONT, text="Gate Test", x=10, y=5, color=0xFFFFFF)
line1 = label.Label(terminalio.FONT, text="V-TRIG", x=5, y=25, color=0xFFFFFF)
line2 = label.Label(terminalio.FONT, text="MCP Ch C", x=5, y=40, color=0xFFFFFF)
line3 = label.Label(terminalio.FONT, text="0V/5V", x=5, y=55, color=0xFFFFFF)

splash.append(title)
splash.append(line1)
splash.append(line2)
splash.append(line3)

print("[6] Display ready")
print("\n" + "="*60)
print("Button A: Fire gate pulse")
print("Button B: Toggle V-TRIG/S-TRIG")
print("="*60)
print("\nOutputs:")
print("  V-TRIG: MCP4728 Channel C (voltage)")
print("  S-TRIG: GPIO D10 (transistor switch)")
print("="*60)

# Gate mode state
gate_mode = "V-TRIG"
pulse_count = 0

# Set both outputs to idle
dac.channel_c.raw_value = 0        # V-TRIG idle = 0V
strig_gpio.value = False            # S-TRIG idle = open circuit

print("\nReady! Starting in V-TRIG mode\n")

while True:
    # Button B: Toggle mode
    if not button_b.value:
        if gate_mode == "V-TRIG":
            gate_mode = "S-TRIG"
            line1.text = "S-TRIG"
            line2.text = "GPIO D10"
            line3.text = "Open/Short"
            print("Mode: S-TRIG (GPIO D10, open/short)")
        else:
            gate_mode = "V-TRIG"
            line1.text = "V-TRIG"
            line2.text = "MCP Ch C"
            line3.text = "0V/5V"
            print("Mode: V-TRIG (MCP4728 Ch C, 0V/5V)")

        # Ensure both outputs are idle when switching
        dac.channel_c.raw_value = 0
        strig_gpio.value = False

        # Wait for button release
        while not button_b.value:
            time.sleep(0.05)
        time.sleep(0.2)

    # Button A: Fire gate pulse
    if not button_a.value:
        pulse_count += 1

        if gate_mode == "V-TRIG":
            # V-TRIG: Voltage pulse on MCP4728 Channel C
            print(f"[{pulse_count}] V-TRIG pulse (0V → 5V → 0V)")
            dac.channel_c.raw_value = 4095  # 5V active
            led.value = True
            time.sleep(0.1)  # 100ms pulse
            dac.channel_c.raw_value = 0     # 0V idle
            led.value = False
        else:
            # S-TRIG: Transistor switch on D10
            print(f"[{pulse_count}] S-TRIG pulse (Open → Short → Open)")
            strig_gpio.value = True   # Short to ground (active)
            led.value = True
            time.sleep(0.1)  # 100ms pulse
            strig_gpio.value = False  # Open circuit (idle)
            led.value = False

        # Wait for button release
        while not button_a.value:
            time.sleep(0.05)
        time.sleep(0.1)

    time.sleep(0.05)
