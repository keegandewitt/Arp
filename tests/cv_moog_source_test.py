"""
CV Moog Source Test - 1.035V/octave
Tests the special Moog Source CV scaling (1.035V/oct vs standard 1.0V/oct)

MOOG SOURCE QUIRK:
The Moog Source synthesizer expects 1.035V/octave instead of the standard 1.0V/octave.
This test compares both scales side-by-side.

REFERENCE POINT:
C3 (MIDI 60) = 1.0V (same for both modes)

HARDWARE SETUP:
1. MCP4728 Channel A (OUTA) → 1/8" jack (CV pitch output)
2. Measure with multimeter to verify scaling
"""

import board
import time
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1107

print("\n" + "="*60)
print("MOOG SOURCE CV TEST - 1.035V/OCTAVE")
print("="*60)
print("\nCompares standard 1V/oct vs Moog Source 1.035V/oct")
print("Reference: C3 (MIDI 60) = 1.0V")
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
    dac.channel_a.vref = adafruit_mcp4728.Vref.VDD
    dac.channel_a.gain = 1
    time.sleep(0.1)

    dac.save_settings()
    time.sleep(0.3)
    dac.channel_a.raw_value = 0

    print("      ✓ MCP4728 initialized")
except Exception as e:
    print(f"      ✗ FAILED: {e}")
    while True:
        time.sleep(1)

# CV calculation functions (matching arp/drivers/cv_gate.py)
REFERENCE_NOTE = 60  # C3 (MIDI 60)
REFERENCE_VOLTAGE = 1.0  # 1V at C3

def voltage_standard(midi_note):
    """
    Standard 1V/octave with C3 reference
    Reference: C3 (MIDI 60) = 1.0V
    Octave spacing: 1.0V
    """
    VOLTS_PER_OCTAVE = 1.0

    semitones_from_ref = midi_note - REFERENCE_NOTE
    volts_per_semitone = VOLTS_PER_OCTAVE / 12.0
    voltage = REFERENCE_VOLTAGE + (semitones_from_ref * volts_per_semitone)

    return max(0.0, min(5.0, voltage))

def voltage_moog_source(midi_note):
    """
    Moog Source 1.035V/octave with C3 reference
    Reference: C3 (MIDI 60) = 1.0V
    Octave spacing: 1.035V instead of 1.0V
    """
    VOLTS_PER_OCTAVE = 1.035

    semitones_from_ref = midi_note - REFERENCE_NOTE
    volts_per_semitone = VOLTS_PER_OCTAVE / 12.0
    voltage = REFERENCE_VOLTAGE + (semitones_from_ref * volts_per_semitone)

    return max(0.0, min(5.0, voltage))

print("[3/3] Starting comparison test...")
print("\n" + "="*60)
print("STANDARD 1V/OCTAVE vs MOOG SOURCE 1.035V/OCTAVE")
print("="*60)

# Test notes around the reference point (C3 = MIDI 60)
# Range: C2 (MIDI 48) = 0.0V to C7 (MIDI 108) = 5.0V
test_notes = [
    (48, "C2"),   # 0.0V (one octave below reference)
    (60, "C3"),   # 1.0V (reference point - same in both modes)
    (72, "C4"),   # 2.0V standard, 2.035V Moog Source
    (84, "C5"),   # 3.0V standard, 3.070V Moog Source
    (96, "C6")    # 4.0V standard, 4.105V Moog Source
]

print("\nNote | MIDI | Standard | Moog Source | Difference")
print("-" * 60)

for midi_note, note_name in test_notes:
    v_std = voltage_standard(midi_note)
    v_moog = voltage_moog_source(midi_note)
    diff = v_moog - v_std

    print(f"{note_name:4s} | {midi_note:4d} | {v_std:7.3f}V | {v_moog:9.3f}V | {diff:+.3f}V")

print("-" * 60)

# Now test both modes on hardware
print("\n" + "="*60)
print("TESTING ON HARDWARE")
print("="*60)
print("\nWill cycle through: STANDARD → MOOG SOURCE → STANDARD...")
print("Watch OLED and measure voltage at 1/8\" jack\n")

# Create display function
def update_display(note_name, voltage, mode):
    group = displayio.Group()

    mode_text = "STANDARD" if mode == "std" else "MOOG SRC"

    title = label.Label(terminalio.FONT, text=mode_text, color=0xFFFFFF, x=25, y=5)
    sep = label.Label(terminalio.FONT, text="-" * 21, color=0xFFFFFF, x=0, y=15)
    note_label = label.Label(terminalio.FONT, text=f"Note: {note_name}", color=0xFFFFFF, x=5, y=30)
    voltage_label = label.Label(terminalio.FONT, text=f"Out: {voltage:.3f}V", color=0xFFFFFF, x=5, y=45)

    group.append(title)
    group.append(sep)
    group.append(note_label)
    group.append(voltage_label)

    display.root_group = group

# Test loop - cycles through standard vs Moog Source for each note
test_cycle = [
    ("C2", 48, "std"),
    ("C2", 48, "moog"),
    ("C3", 60, "std"),
    ("C3", 60, "moog"),  # Reference point: 1.0V in both modes
    ("C4", 72, "std"),
    ("C4", 72, "moog"),  # Standard: 2.000V, Moog Source: 2.035V
    ("C5", 84, "std"),
    ("C5", 84, "moog"),  # Standard: 3.000V, Moog Source: 3.070V
    ("C6", 96, "std"),
    ("C6", 96, "moog")   # Standard: 4.000V, Moog Source: 4.105V
]

print("Starting continuous test loop...\n")

while True:
    for note_name, midi_note, mode in test_cycle:
        # Calculate voltage based on mode
        if mode == "std":
            voltage = voltage_standard(midi_note)
            mode_name = "STANDARD 1V/oct"
        else:
            voltage = voltage_moog_source(midi_note)
            mode_name = "MOOG SOURCE 1.035V/oct"

        # Set DAC output
        raw_value = int((voltage / 5.0) * 4095)
        raw_value = min(raw_value, 4095)
        dac.channel_a.raw_value = raw_value

        # Update display
        update_display(note_name, voltage, mode)

        # Print to serial
        print(f"[{mode_name:24s}] {note_name:3s} → {voltage:.3f}V")

        time.sleep(2.0)
