"""
TL072 2× Gain Circuit Test

Tests op-amp gain circuit to amplify MCP4728 0-5V output to 0-10V eurorack range.

CRITICAL: TL072 Pinout (DIP-8, looking at chip with notch at TOP)

              ╭─╮                    ← Notch at top
         ┌────╯ ╰────┐
         │           │
    1 ───┤           ├─── 8
         │           │
    2 ───┤           ├─── 7
         │           │
    3 ───┤           ├─── 6
         │           │
    4 ───┤           ├─── 5
         │           │
         └───────────┘

Pin 1: OUT A (top-left)        Pin 8: V+ (12V) (top-right)
Pin 2: IN- A                   Pin 7: OUT B
Pin 3: IN+ A                   Pin 6: IN- B
Pin 4: V- (GND) (bottom-left)  Pin 5: IN+ B

We're using Op-Amp A (pins 1, 2, 3) in non-inverting configuration with 2× gain:
- IN+ (pin 3): MCP4728 Channel A output (0-5V)
- IN- (pin 2): Connected to voltage divider (R1/R2)
- OUT (pin 1): Amplified output (0-10V)

Circuit:
                    R2 (100kΩ)
         OUT (Pin 1) ──────┬─────── Output to Eurorack (0-10V)
                           │
                           R1 (100kΩ)
                           │
         IN- (Pin 2) ──────┤
                           │
                          GND

         IN+ (Pin 3) ────── MCP4728 Channel A (0-5V)

         VCC+ (Pin 8) ───── 12V
         VCC- (Pin 4) ───── GND

Gain = 1 + (R2/R1) = 1 + (100k/100k) = 2×

Hardware:
- MCP4728 VDD: 5V from LM7805
- TL072 power: 12V from Powerboost
- All grounds connected (common ground)
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

# Setup Button B for stepping
button_b = digitalio.DigitalInOut(board.D6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

print("\n" + "="*60)
print("TL072 2× GAIN CIRCUIT TEST")
print("="*60)
print("\nHardware Setup:")
print("  MCP4728 Channel A (VA) → TL072 IN+ (Pin 3)")
print("  TL072 OUT (Pin 1) → Multimeter probe")
print("  TL072 VCC+ (Pin 8) → 12V rail")
print("  TL072 VCC- (Pin 4) → GND")
print("  All grounds connected (common ground)")
print("\n" + "="*60)

# Initialize I2C
displayio.release_displays()
time.sleep(0.2)
i2c = board.I2C()
print("\n[1] I2C bus ready")

# Initialize OLED
import i2cdisplaybus
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = SH1107(display_bus, width=128, height=64)
print("[2] OLED initialized")

# Initialize MCP4728
dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
print("[3] MCP4728 detected")

# Wake and configure
dac.wakeup()
time.sleep(0.1)
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
dac.channel_a.gain = 1
time.sleep(0.1)
dac.save_settings()
time.sleep(0.3)
print("[4] MCP4728 configured (VDD ref, 1x gain)")

# Setup display
splash = displayio.Group()
display.root_group = splash

title = label.Label(terminalio.FONT, text="TL072 Test", x=20, y=5, color=0xFFFFFF)
line1 = label.Label(terminalio.FONT, text="Press B", x=5, y=25, color=0xFFFFFF)
line2 = label.Label(terminalio.FONT, text="", x=5, y=40, color=0xFFFFFF)
line3 = label.Label(terminalio.FONT, text="", x=5, y=55, color=0xFFFFFF)

splash.append(title)
splash.append(line1)
splash.append(line2)
splash.append(line3)

print("[5] Display ready")
print("\n" + "="*60)
print("TEST VOLTAGES")
print("="*60)
print("\nButton B cycles through test voltages")
print("Measure TL072 Pin 1 (OUT) with multimeter\n")

# Test cases: (description, DAC_input_V, expected_output_V)
test_cases = [
    ("Zero",        0.0,  0.0),
    ("0.5V input",  0.5,  1.0),
    ("1.0V input",  1.0,  2.0),
    ("2.0V input",  2.0,  4.0),
    ("3.0V input",  3.0,  6.0),
    ("4.0V input",  4.0,  8.0),
    ("5.0V input",  5.0, 10.0),  # Max eurorack range
]

current_step = 0
led.value = False

print("Step | DAC In | Expected Out | Actual (measure)")
print("-----|--------|--------------|------------------")

while True:
    if not button_b.value:  # Button pressed
        desc, dac_in_v, expected_out_v = test_cases[current_step]

        # Calculate raw_value for DAC
        raw_value = int((dac_in_v / 5.0) * 4095)

        # CRITICAL: Use raw_value (not value)
        dac.channel_a.raw_value = raw_value

        # Update display
        line1.text = f"{desc}"
        line2.text = f"In: {dac_in_v:.1f}V"
        line3.text = f"Out: {expected_out_v:.1f}V?"

        # Print to serial
        print(f"  {current_step+1}  | {dac_in_v:5.1f}V | {expected_out_v:6.1f}V    | ________")
        print(f"       raw={raw_value}")

        # LED feedback
        led.value = True
        time.sleep(0.1)
        led.value = False

        # Next step
        current_step = (current_step + 1) % len(test_cases)

        # Wait for release
        while not button_b.value:
            time.sleep(0.05)
        time.sleep(0.2)

    time.sleep(0.05)
