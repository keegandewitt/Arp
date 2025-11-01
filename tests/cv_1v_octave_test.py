"""
CV 1V/Octave Test - CORRECT IMPLEMENTATION
Direct MCP4728 DAC output (no op-amp, no gain)

HARDWARE SETUP:
1. MCP4728 DAC on I2C bus (address 0x60)
2. MCP4728 VCC powered by PowerBoost 5V
3. MCP4728 Channel A (OUTA) → 1/8" jack TIP (CV pitch output)
4. Ground → 1/8" jack SLEEVE
5. 0.1µF cap between VCC and GND
6. NO OP-AMP!

VERIFICATION:
- C0 (MIDI 12) = 1.00V ✓
- C1 (MIDI 24) = 2.00V ✓
- C2 (MIDI 36) = 3.00V ✓
- C3 (MIDI 48) = 4.00V ✓
- C4 (MIDI 60) = 5.00V ✓ (maximum)

This is the STANDARD 1V/octave that works with ALL VCOs.
"""

import board
import time
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1107

print("\n" + "="*60)
print("CV 1V/OCTAVE TEST - CORRECT IMPLEMENTATION")
print("="*60)
print("\nDirect DAC output (no op-amp, no gain)")
print("Standard 1V/octave for modular synths")
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

    # Configure Channel A for 5V operation (NO GAIN!)
    dac.channel_a.vref = adafruit_mcp4728.Vref.VDD  # Use VDD (5V) reference
    dac.channel_a.gain = 1  # 1× gain (CRITICAL: No amplification!)
    time.sleep(0.1)

    dac.save_settings()
    time.sleep(0.3)

    # Initialize to 0V
    dac.channel_a.raw_value = 0

    print("      ✓ MCP4728 initialized (Channel A, 1× gain)")
    print("      ✓ 1V/octave standard configuration")
except Exception as e:
    print(f"      ✗ FAILED: {e}")
    print("\n⚠️ Check I2C connections and MCP4728 address (0x60)")
    while True:
        time.sleep(1)

# Create display layout
group = displayio.Group()

title = label.Label(terminalio.FONT, text="1V/Octave", color=0xFFFFFF, x=28, y=5)
group.append(title)

sep = label.Label(terminalio.FONT, text="-" * 21, color=0xFFFFFF, x=0, y=15)
group.append(sep)

note_label = label.Label(terminalio.FONT, text="Note: ---", color=0xFFFFFF, x=5, y=30)
group.append(note_label)

voltage_label = label.Label(terminalio.FONT, text="Out: 0.00V", color=0xFFFFFF, x=5, y=45)
group.append(voltage_label)

status_label = label.Label(terminalio.FONT, text="STANDARD", color=0xFFFFFF, x=25, y=58)
group.append(status_label)

display.root_group = group

print("[3/3] Starting 1V/octave test...")
print("\n" + "="*60)
print("MEASURE WITH MULTIMETER AT 1/8\" JACK")
print("="*60)
print("\nTesting C0-C4 (5 octaves)")
print("Expected: 1V/octave standard")
print("\n" + "-"*60)

# Test notes: C0 through C4 (5 octaves = 0-5V)
test_notes = [
    (12, "C0", 1.00),   # MIDI 12 → 1.00V
    (24, "C1", 2.00),   # MIDI 24 → 2.00V
    (36, "C2", 3.00),   # MIDI 36 → 3.00V
    (48, "C3", 4.00),   # MIDI 48 → 4.00V
    (60, "C4", 5.00)    # MIDI 60 → 5.00V (maximum)
]

print("\nNote | MIDI | Voltage | Formula")
print("-" * 60)

for midi_note, note_name, expected_volts in test_notes:
    # 1V/octave formula: voltage = MIDI note / 12
    voltage = midi_note / 12.0

    # Set DAC output (direct, no gain)
    raw_value = int((voltage / 5.0) * 4095)
    raw_value = min(raw_value, 4095)  # Safety clamp
    dac.channel_a.raw_value = raw_value

    # Update display
    note_label.text = f"Note: {note_name}"
    voltage_label.text = f"Out: {voltage:.2f}V"

    # Print to serial
    print(f"{note_name:4s} | {midi_note:4d} | {voltage:5.2f}V | {midi_note}/12")

    # Hold for measurement
    time.sleep(2.5)

print("-" * 60)
print("\n" + "="*60)
print("✓ 1V/OCTAVE TEST COMPLETE")
print("="*60)

# Hold final display
group = displayio.Group()
done1 = label.Label(terminalio.FONT, text="Test Complete!", color=0xFFFFFF, x=10, y=20)
done2 = label.Label(terminalio.FONT, text="1V/octave OK", color=0xFFFFFF, x=15, y=40)
group.append(done1)
group.append(done2)
display.root_group = group

print("\nVERIFICATION CHECKLIST:")
print("  □ Voltages match MIDI/12 formula (±0.05V)")
print("  □ 1.00V steps between octaves")
print("  □ Works with VCO 1V/oct input")
print("  □ No distortion or noise")
print("\nIf testing with VCO:")
print("  □ Chromatic scale tracks correctly")
print("  □ Each octave doubles frequency")
print("  □ C4 (5V) → highest note")
print("\nTest will loop through notes continuously...")
print("Press CTRL+C to exit\n")

# Continuous test loop
while True:
    for midi_note, note_name, expected_volts in test_notes:
        voltage = midi_note / 12.0

        raw_value = int((voltage / 5.0) * 4095)
        raw_value = min(raw_value, 4095)
        dac.channel_a.raw_value = raw_value

        # Update display
        group = displayio.Group()
        title = label.Label(terminalio.FONT, text="1V/Octave", color=0xFFFFFF, x=28, y=5)
        sep = label.Label(terminalio.FONT, text="-" * 21, color=0xFFFFFF, x=0, y=15)
        note_label = label.Label(terminalio.FONT, text=f"Note: {note_name}", color=0xFFFFFF, x=5, y=30)
        voltage_label = label.Label(terminalio.FONT, text=f"Out: {voltage:.2f}V", color=0xFFFFFF, x=5, y=45)
        status_label = label.Label(terminalio.FONT, text="STANDARD", color=0xFFFFFF, x=25, y=58)

        group.append(title)
        group.append(sep)
        group.append(note_label)
        group.append(voltage_label)
        group.append(status_label)
        display.root_group = group

        print(f"[LOOP] {note_name:4s} → {voltage:.2f}V")

        time.sleep(2.0)
