"""
CV Output Handler
Manages CV pitch output and trigger/gate signals via MCP4728 DAC
"""

import time
import busio
import adafruit_mcp4728


class CVOutput:
    """Handles CV pitch and trigger output via MCP4728 DAC"""

    # DAC channel assignments
    CH_PITCH = 0      # Channel A: CV pitch (1V/octave or 1.035V/octave)
    CH_TRIGGER = 1    # Channel B: Trigger/gate output
    CH_UNUSED_C = 2   # Channel C: Reserved for future use
    CH_UNUSED_D = 3   # Channel D: Reserved for future use

    # Voltage constants for 5V reference
    DAC_MAX_VALUE = 4095  # 12-bit DAC
    DAC_VREF = 5.0  # 5V reference

    # CV pitch reference point: C3 (MIDI note 60) = 1V
    MIDI_REFERENCE_NOTE = 60  # C3
    CV_REFERENCE_VOLTAGE = 1.0  # 1V at C3

    # Trigger voltage levels
    TRIGGER_HIGH = 4095  # ~5V (full scale)
    TRIGGER_LOW = 0      # 0V

    def __init__(self, i2c, settings):
        """
        Initialize CV output handler

        Args:
            i2c: I2C bus object
            settings: Global settings object
        """
        self.settings = settings

        try:
            # Initialize MCP4728 DAC (address 0x60 by default)
            self.dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)

            # Set all channels to use internal 5V reference
            # This provides stable, accurate CV output
            for channel in [self.dac.channel_a, self.dac.channel_b,
                           self.dac.channel_c, self.dac.channel_d]:
                channel.vref = adafruit_mcp4728.Vref.INTERNAL
                channel.gain = 1  # 1x gain for 0-5V output
                channel.value = 0  # Start at 0V

            self.dac_available = True

        except Exception as e:
            print(f"Warning: MCP4728 DAC not found: {e}")
            print("CV output will be disabled")
            self.dac_available = False
            self.dac = None

        # Trigger state tracking
        self.trigger_active = False
        self.current_note = None

    def note_to_voltage(self, midi_note):
        """
        Convert MIDI note number to CV voltage

        Args:
            midi_note: MIDI note number (0-127)

        Returns:
            Voltage value (float)
        """
        # Calculate semitones from reference note
        semitones_from_reference = midi_note - self.MIDI_REFERENCE_NOTE

        # Get voltage per octave based on settings
        if self.settings.cv_scale == self.settings.CV_SCALE_STANDARD:
            volts_per_octave = 1.0  # Standard 1V/octave
        else:
            volts_per_octave = 1.035  # Moog Source 1.035V/octave

        # Calculate voltage (12 semitones = 1 octave)
        volts_per_semitone = volts_per_octave / 12.0
        voltage = self.CV_REFERENCE_VOLTAGE + (semitones_from_reference * volts_per_semitone)

        # Clamp to valid range (0-5V)
        return max(0.0, min(self.DAC_VREF, voltage))

    def voltage_to_dac_value(self, voltage):
        """
        Convert voltage to DAC value

        Args:
            voltage: Desired voltage (0.0-5.0)

        Returns:
            DAC value (0-4095)
        """
        # Scale voltage to DAC range
        dac_value = int((voltage / self.DAC_VREF) * self.DAC_MAX_VALUE)

        # Clamp to valid range
        return max(0, min(self.DAC_MAX_VALUE, dac_value))

    def set_pitch_cv(self, midi_note):
        """
        Set CV pitch output for a MIDI note

        Args:
            midi_note: MIDI note number (0-127)
        """
        if not self.dac_available or not self.settings.cv_enabled:
            return

        try:
            voltage = self.note_to_voltage(midi_note)
            dac_value = self.voltage_to_dac_value(voltage)
            self.dac.channel_a.value = dac_value
            self.current_note = midi_note

        except Exception as e:
            print(f"Error setting pitch CV: {e}")

    def trigger_on(self):
        """Activate the trigger output (gate mode)"""
        if not self.dac_available or not self.settings.cv_enabled:
            return

        try:
            # Determine trigger voltage based on polarity
            if self.settings.trigger_polarity == self.settings.TRIGGER_VTRIG:
                # V-trig: high = active
                trigger_value = self.TRIGGER_HIGH
            else:
                # S-trig: low = active
                trigger_value = self.TRIGGER_LOW

            self.dac.channel_b.value = trigger_value
            self.trigger_active = True

        except Exception as e:
            print(f"Error setting trigger on: {e}")

    def trigger_off(self):
        """Deactivate the trigger output (gate mode)"""
        if not self.dac_available or not self.settings.cv_enabled:
            return

        try:
            # Determine trigger voltage based on polarity
            if self.settings.trigger_polarity == self.settings.TRIGGER_VTRIG:
                # V-trig: low = inactive
                trigger_value = self.TRIGGER_LOW
            else:
                # S-trig: high = inactive
                trigger_value = self.TRIGGER_HIGH

            self.dac.channel_b.value = trigger_value
            self.trigger_active = False

        except Exception as e:
            print(f"Error setting trigger off: {e}")

    def note_on(self, midi_note):
        """
        Handle note-on event: set CV pitch and activate trigger

        Args:
            midi_note: MIDI note number
        """
        if not self.dac_available or not self.settings.cv_enabled:
            return

        # Set pitch CV
        self.set_pitch_cv(midi_note)

        # Activate trigger
        self.trigger_on()

    def note_off(self):
        """Handle note-off event: deactivate trigger"""
        if not self.dac_available or not self.settings.cv_enabled:
            return

        # Turn off trigger (gate mode)
        self.trigger_off()
        self.current_note = None

    def process(self):
        """
        Process CV output (call in main loop)
        Reserved for future use - gate mode doesn't require timing
        """
        pass

    def reset(self):
        """Reset all CV outputs to 0V"""
        if not self.dac_available:
            return

        try:
            self.dac.channel_a.value = 0  # Pitch CV to 0V
            self.trigger_off()  # Trigger to inactive state
            self.current_note = None

        except Exception as e:
            print(f"Error resetting CV: {e}")

    def test_cv_output(self, midi_note, duration=1.0):
        """
        Test CV output by playing a specific note

        Args:
            midi_note: MIDI note to test
            duration: How long to hold the note (seconds)
        """
        if not self.dac_available:
            print("DAC not available")
            return False

        print(f"\nTesting CV output with note {midi_note}:")

        voltage = self.note_to_voltage(midi_note)
        print(f"  Target voltage: {voltage:.3f}V")
        print(f"  CV scale: {self.settings.get_cv_scale_name()}")
        print(f"  Trigger polarity: {self.settings.get_trigger_polarity_name()}")

        # Send note on
        print(f"\n  Note ON...")
        self.note_on(midi_note)
        time.sleep(duration)

        # Send note off
        print(f"  Note OFF...")
        self.note_off()

        return True

    def get_status(self):
        """
        Get current CV output status

        Returns:
            Dictionary with status information
        """
        return {
            'dac_available': self.dac_available,
            'cv_enabled': self.settings.cv_enabled,
            'current_note': self.current_note,
            'current_voltage': self.note_to_voltage(self.current_note) if self.current_note else 0.0,
            'trigger_active': self.trigger_active,
            'cv_scale': self.settings.get_cv_scale_name(),
            'trigger_polarity': self.settings.get_trigger_polarity_name()
        }
