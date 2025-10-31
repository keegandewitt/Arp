"""
CV Output Scope Test

Generates stepped CV output pattern for oscilloscope verification.
Tests the complete chain: M4 → MCP4728 (0-5V) → LM358N (0-10V)

Connect oscilloscope:
- Probe 1: LM358N Pin 1 (CV output, 0-10V)
- Probe 2: MCP4728 Channel C (Gate output, 0-5V)
- Ground: Common ground

Expected waveform:
- CV: Staircase pattern (chromatic scale)
- Gate: Pulses synchronized with CV steps
"""

import time
import board
import digitalio
from arp.drivers.cv_output import CVOutput

# Setup LED for visual feedback
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

print("\n" + "="*60)
print("CV OUTPUT SCOPE TEST")
print("="*60)
print("\nConnect oscilloscope:")
print("  CH1: LM358N Pin 1 (CV output, 0-10V)")
print("  CH2: MCP4728 Channel C (Gate, 0-5V)")
print("  GND: Common ground")
print("\n" + "="*60)

# Initialize I2C and CV output
i2c = board.I2C()
cv = CVOutput(i2c, display=None)
print("[✓] CV output initialized\n")

# Test patterns
print("Test patterns:")
print("  1. Chromatic scale (C2 → C4) - 2 octaves")
print("  2. Octave steps (C1, C2, C3, C4, C5)")
print("  3. Voltage ramp (0V → 10V in 1V steps)")
print("\n" + "="*60)

def chromatic_scale_test():
    """Chromatic scale: 12 semitones per octave"""
    print("\n[1] CHROMATIC SCALE TEST")
    print("Pattern: C2 → C4 (24 semitones)")
    print("Duration: 200ms per note\n")

    start_note = 36  # C2
    end_note = 60    # C4

    for midi_note in range(start_note, end_note + 1):
        note_name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][midi_note % 12]
        octave = (midi_note // 12) - 1
        voltage = midi_note / 12.0

        print(f"  Note {midi_note:3d} ({note_name:2s}{octave}) → {voltage:.2f}V")

        # Set CV and gate high
        cv.set_cv_a(midi_note)
        cv.set_gate(True)
        led.value = True
        time.sleep(0.15)  # Note on

        # Gate low (brief gap)
        cv.set_gate(False)
        led.value = False
        time.sleep(0.05)  # Note off

    # Reset
    cv.set_cv_a(0)
    cv.set_gate(False)
    print("  [Complete]\n")
    time.sleep(1.0)

def octave_steps_test():
    """Octave steps: 1V jumps"""
    print("\n[2] OCTAVE STEPS TEST")
    print("Pattern: C1, C2, C3, C4, C5 (1V/octave)")
    print("Duration: 500ms per octave\n")

    octave_notes = [24, 36, 48, 60, 72]  # C1 through C5

    for midi_note in octave_notes:
        octave = (midi_note // 12) - 1
        voltage = midi_note / 12.0

        print(f"  C{octave} (MIDI {midi_note}) → {voltage:.2f}V")

        # Set CV and gate
        cv.set_cv_a(midi_note)
        cv.set_gate(True)
        led.value = True
        time.sleep(0.4)  # Hold

        cv.set_gate(False)
        led.value = False
        time.sleep(0.1)  # Gap

    # Reset
    cv.set_cv_a(0)
    cv.set_gate(False)
    print("  [Complete]\n")
    time.sleep(1.0)

def voltage_ramp_test():
    """Direct voltage ramp: 0-10V in 1V steps"""
    print("\n[3] VOLTAGE RAMP TEST")
    print("Pattern: 0V → 10V in 1V steps")
    print("Duration: 500ms per step\n")

    # Use raw voltage control for precise 1V steps
    for volts in range(0, 11):  # 0V to 10V
        print(f"  {volts:2d}V")

        # Convert to DAC voltage (before 2× gain)
        dac_voltage = volts / 2.0  # Divide by 2 because LM358N has 2× gain

        # Set voltage and gate
        cv.set_raw_voltage('a', dac_voltage)
        cv.set_gate(True)
        led.value = True
        time.sleep(0.4)  # Hold

        cv.set_gate(False)
        led.value = False
        time.sleep(0.1)  # Gap

    # Reset
    cv.set_raw_voltage('a', 0.0)
    cv.set_gate(False)
    print("  [Complete]\n")
    time.sleep(1.0)

# Run all tests in loop
print("\nStarting test sequence...\n")
time.sleep(2.0)

try:
    while True:
        chromatic_scale_test()
        octave_steps_test()
        voltage_ramp_test()

        print("="*60)
        print("Sequence complete. Repeating in 3 seconds...")
        print("="*60 + "\n")
        time.sleep(3.0)

except KeyboardInterrupt:
    print("\n\n[!] Test stopped by user")
    cv.set_cv_a(0)
    cv.set_gate(False)
    led.value = False
    print("[✓] Outputs reset to 0V\n")
