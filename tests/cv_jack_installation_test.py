"""
CV 1/8" Jack Installation Test
Tests CV pitch output with 1V/octave scaling

HARDWARE SETUP:
1. MCP4728 DAC on I2C bus (address 0x60)
2. MCP4728 Channel A → LM358N op-amp (2× gain)
3. LM358N output → 1/8" jack (CV pitch output)
4. OLED display shows current note and expected voltage

MEASUREMENT POINTS:
- DAC output (Channel A): 0-5V (measure at MCP4728 pin)
- 1/8" jack: 0-10V (measure with multimeter at jack tip)

VERIFICATION:
- C0 (MIDI 12) = 1.00V
- C1 (MIDI 24) = 2.00V
- C2 (MIDI 36) = 3.00V
- C3 (MIDI 48) = 4.00V
- C4 (MIDI 60) = 5.00V
- C5 (MIDI 72) = 6.00V
- C6 (MIDI 84) = 7.00V
- C7 (MIDI 96) = 8.00V
"""

import board
import time
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1107

print("\n" + "="*60)
print("CV 1/8\" JACK INSTALLATION TEST")
print("="*60)
print("\nTests 1V/octave CV output on Channel A")
print("Verify voltage with multimeter at 1/8\" jack")
print("="*60 + "\n")

# Initialize OLED
print("[1/3] Initializing OLED display...")
i2c = board.I2C()
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(display_bus, width=128, height=64)
display.brightness = 0.8
print("      ✓ OLED ready")

# Initialize MCP4728 DAC
print("[2/3] Initializing MCP4728 DAC...")
import adafruit_mcp4728

try:
    dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
    dac.wakeup()
    time.sleep(0.1)

    # Configure Channel A for 5V operation
    dac.channel_a.vref = adafruit_mcp4728.Vref.VDD  # Use VDD (5V) reference
    dac.channel_a.gain = 1  # 1× gain
    time.sleep(0.1)

    dac.save_settings()
    time.sleep(0.3)

    # Initialize to 0V
    dac.channel_a.raw_value = 0

    print("      ✓ MCP4728 initialized (Channel A)")
except Exception as e:
    print(f"      ✗ FAILED: {e}")
    print("\n⚠️ Check I2C connections and MCP4728 address (0x60)")
    while True:
        time.sleep(1)

# Create display layout
group = displayio.Group()

title = label.Label(terminalio.FONT, text="CV Jack Test", color=0xFFFFFF, x=20, y=5)
group.append(title)

sep = label.Label(terminalio.FONT, text="-" * 21, color=0xFFFFFF, x=0, y=15)
group.append(sep)

note_label = label.Label(terminalio.FONT, text="Note: ---", color=0xFFFFFF, x=5, y=28)
group.append(note_label)

dac_voltage = label.Label(terminalio.FONT, text="DAC: 0.00V", color=0xFFFFFF, x=5, y=41)
group.append(dac_voltage)

jack_voltage = label.Label(terminalio.FONT, text="Jack: 0.00V", color=0xFFFFFF, x=5, y=54)
group.append(jack_voltage)

display.root_group = group

print("[3/3] Starting CV output test...")
print("\n" + "="*60)
print("MEASURE WITH MULTIMETER AT 1/8\" JACK")
print("="*60)
print("\nTesting octaves C0-C4 (MIDI 12-60)")
print("DAC range: 0-5V → Jack range: 0-10V (2× gain)")
print("Expected: 1V/octave at jack")
print("\n" + "-"*60)

# Test notes: C0 through C4 (5 octaves = 0-10V range)
# DAC outputs 0-5V, LM358N amplifies 2× to 0-10V
test_notes = [
    (12, "C0", 1.00, 2.00),   # 1.00V DAC → 2.00V jack
    (24, "C1", 2.00, 4.00),   # 2.00V DAC → 4.00V jack
    (36, "C2", 3.00, 6.00),   # 3.00V DAC → 6.00V jack
    (48, "C3", 4.00, 8.00),   # 4.00V DAC → 8.00V jack
    (60, "C4", 5.00, 10.00)   # 5.00V DAC → 10.00V jack (maximum)
]

print("\nNote | MIDI | DAC Out | Jack Out (2× gain)")
print("-" * 60)

for midi_note, note_name, dac_expected, jack_expected in test_notes:
    # Calculate DAC voltage (0-5V)
    dac_volts = midi_note / 12.0

    # Calculate expected jack voltage (2× gain from LM358N)
    jack_volts = jack_expected

    # Set DAC output (clamp to 4095 max)
    raw_value = int((dac_volts / 5.0) * 4095)
    raw_value = min(raw_value, 4095)  # Safety clamp
    dac.channel_a.raw_value = raw_value

    # Update display
    note_label.text = f"Note: {note_name}"
    dac_voltage.text = f"DAC: {dac_volts:.2f}V"
    jack_voltage.text = f"Jack: {jack_volts:.2f}V"

    # Print to serial
    print(f"{note_name:4s} | {midi_note:4d} | {dac_volts:5.2f}V  | {jack_volts:5.2f}V (expected)")

    # Hold for measurement
    time.sleep(2.5)

print("-" * 60)
print("\n" + "="*60)
print("✓ CV OUTPUT TEST COMPLETE")
print("="*60)

# Hold final display
group = displayio.Group()
done1 = label.Label(terminalio.FONT, text="Test Complete!", color=0xFFFFFF, x=10, y=20)
done2 = label.Label(terminalio.FONT, text="Measure jack", color=0xFFFFFF, x=15, y=40)
group.append(done1)
group.append(done2)
display.root_group = group

print("\nVERIFICATION CHECKLIST:")
print("  □ DAC output stepped from 1.00V to 8.00V")
print("  □ Jack output matches expected voltages (±0.1V)")
print("  □ 1V/octave tracking verified")
print("  □ No distortion or noise on output")
print("\nIf voltages are off:")
print("  - Check LM358N wiring (2× gain circuit)")
print("  - Verify 12V power supply to op-amp")
print("  - Check ground connections")
print("\nTest will loop through notes continuously...")
print("Press CTRL+C to exit\n")

# Continuous test loop
while True:
    for midi_note, note_name, dac_expected, jack_expected in test_notes:
        dac_volts = midi_note / 12.0
        jack_volts = jack_expected

        raw_value = int((dac_volts / 5.0) * 4095)
        raw_value = min(raw_value, 4095)  # Safety clamp
        dac.channel_a.raw_value = raw_value

        # Update display
        group = displayio.Group()
        title = label.Label(terminalio.FONT, text="CV Jack Test", color=0xFFFFFF, x=20, y=5)
        sep = label.Label(terminalio.FONT, text="-" * 21, color=0xFFFFFF, x=0, y=15)
        note_label = label.Label(terminalio.FONT, text=f"Note: {note_name}", color=0xFFFFFF, x=5, y=28)
        dac_voltage = label.Label(terminalio.FONT, text=f"DAC: {dac_volts:.2f}V", color=0xFFFFFF, x=5, y=41)
        jack_voltage = label.Label(terminalio.FONT, text=f"Jack: {jack_volts:.2f}V", color=0xFFFFFF, x=5, y=54)

        group.append(title)
        group.append(sep)
        group.append(note_label)
        group.append(dac_voltage)
        group.append(jack_voltage)
        display.root_group = group

        print(f"[LOOP] {note_name:4s} → DAC: {dac_volts:.2f}V, Jack: {jack_volts:.2f}V")

        time.sleep(2.0)
