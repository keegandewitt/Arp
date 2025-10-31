"""
MCP4728 Correct Voltage Test - Using raw_value Property

This test demonstrates the CORRECT way to set MCP4728 output voltages
for 1V/octave CV applications.

KEY INSIGHT: Use raw_value (12-bit), NOT value (16-bit)

Hardware:
- MCP4728 VDD: 4.83V from LM7805
- Reference: Vref.VDD (uses VDD as voltage reference)
- Gain: 1x
- Expected output range: 0V to 4.83V

Math for 1V/octave CV (assuming 5V reference for standard tuning):
- 12-bit DAC: 4096 steps
- 5V range: 4096 / 5 = 819.2 steps per volt
- Per semitone: 819.2 / 12 = 68.27 steps/semitone
- Formula: raw_value = MIDI_note * 68.27

Example MIDI notes:
- C1 (24): 24 * 68.27 = 1639 → 2.00V
- C2 (36): 36 * 68.27 = 2458 → 3.00V
- C3 (48): 48 * 68.27 = 3277 → 4.00V
- C4 (60): 60 * 68.27 = 4096 → 5.00V (will be 4.83V with our VDD)
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

# Setup Button B for stepping through voltages
button_b = digitalio.DigitalInOut(board.D6)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

print("\n" + "="*60)
print("MCP4728 CORRECT VOLTAGE TEST")
print("Using raw_value (12-bit) for direct DAC control")
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

# Use VDD reference (4.83V) with 1x gain
dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
dac.channel_a.gain = 1
time.sleep(0.1)

dac.save_settings()
time.sleep(0.3)
print("[4] DAC configured (VDD ref, 1x gain, woken up)")

# STEP 5: Setup display
splash = displayio.Group()
display.root_group = splash

title = label.Label(terminalio.FONT, text="CV Test (raw)", x=10, y=5, color=0xFFFFFF)
line1 = label.Label(terminalio.FONT, text="Press B", x=5, y=25, color=0xFFFFFF)
line2 = label.Label(terminalio.FONT, text="", x=5, y=40, color=0xFFFFFF)
line3 = label.Label(terminalio.FONT, text="", x=5, y=55, color=0xFFFFFF)

splash.append(title)
splash.append(line1)
splash.append(line2)
splash.append(line3)

print("[5] Display ready")
print("\n" + "="*60)
print("TEST VOLTAGES - Using raw_value property")
print("="*60)

# Test voltages with exact 12-bit values
test_cases = [
    # (description, raw_value, expected_voltage, midi_note_equiv)
    ("Zero",      0,    0.00, ""),
    ("1 Volt",    819,  1.00, "≈C0 (12)"),
    ("2 Volts",   1639, 2.00, "C1 (24)"),
    ("3 Volts",   2458, 3.00, "C2 (36)"),
    ("4 Volts",   3277, 4.00, "C3 (48)"),
    ("Max (4.83V)", 4095, 4.83, "≈C4 (60)"),
]

current_step = 0
led.value = False

print("\nReady! Press Button B to cycle through voltages")
print("Measure Channel A (VA) output pin with multimeter\n")

while True:
    if not button_b.value:  # Button pressed
        desc, raw_val, expected_v, midi_note = test_cases[current_step]

        # CRITICAL: Use raw_value for direct 12-bit control
        dac.channel_a.raw_value = raw_val

        # Update display
        line1.text = f"{desc}"
        line2.text = f"raw: {raw_val}"
        line3.text = f"→ {expected_v:.2f}V {midi_note}"

        # Print to serial
        print(f"Step {current_step + 1}/6: {desc}")
        print(f"  raw_value = {raw_val}")
        print(f"  Expected voltage: {expected_v:.2f}V")
        print(f"  MIDI equivalent: {midi_note}")
        print(f"  → Measure VA pin now!\n")

        # LED feedback
        led.value = True
        time.sleep(0.1)
        led.value = False

        # Next step
        current_step = (current_step + 1) % len(test_cases)

        # Wait for button release
        while not button_b.value:
            time.sleep(0.05)
        time.sleep(0.2)

    time.sleep(0.05)
