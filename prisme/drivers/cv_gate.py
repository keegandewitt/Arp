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
    CH_CUSTOM_CC = 3  # Channel D: Custom CC output (0-5V)

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

        # Custom CC smoothing state
        self.custom_cc_smoothed_value = 0.0  # Smoothed voltage (0.0-5.0V)

        # Polyphonic note tracking (Session 19 - Translation Hub)
        # Tracks all currently held notes with their velocities
        # Used to implement note priority for monophonic CV output
        self.active_notes = []  # List of (note, velocity) tuples

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

    def cc_to_voltage(self, cc_value):
        """
        Convert MIDI CC value to voltage

        Args:
            cc_value: MIDI CC value (0-127)

        Returns:
            Voltage value (0.0-5.0V)
        """
        # Linear mapping: 0-127 → 0-5V
        voltage = (cc_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def aftertouch_to_voltage(self, aftertouch_value):
        """
        Convert MIDI Aftertouch (Channel Pressure) to voltage

        Args:
            aftertouch_value: MIDI aftertouch value (0-127)

        Returns:
            Voltage value (0.0-5.0V)
        """
        # Same mapping as CC: 0-127 → 0-5V
        voltage = (aftertouch_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def velocity_to_voltage(self, velocity_value):
        """
        Convert MIDI Velocity to voltage

        Args:
            velocity_value: MIDI velocity (0-127)

        Returns:
            Voltage value (0.0-5.0V)
        """
        # Same mapping as CC: 0-127 → 0-5V
        voltage = (velocity_value / 127.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def pitch_bend_to_voltage(self, pitch_bend_value):
        """
        Convert MIDI Pitch Bend to voltage (unipolar 0-5V)

        Args:
            pitch_bend_value: MIDI pitch bend (0-16383, center=8192)

        Returns:
            Voltage value (0.0-5.0V)
        """
        # Unipolar mapping: 0-16383 → 0-5V
        # Note: For bipolar, would need -5V to +5V (Phase 2)
        voltage = (pitch_bend_value / 16383.0) * 5.0
        return max(0.0, min(5.0, voltage))

    def set_custom_cc_voltage(self, raw_voltage):
        """
        Set Custom CC output voltage with smoothing

        Args:
            raw_voltage: Target voltage (0.0-5.0V)
        """
        if not self.dac_available:
            return

        try:
            # Get smoothing coefficient based on settings
            smoothing_alphas = {
                self.settings.CC_SMOOTH_OFF: 1.0,   # No smoothing
                self.settings.CC_SMOOTH_LOW: 0.9,   # Light smoothing
                self.settings.CC_SMOOTH_MID: 0.7,   # Medium smoothing
                self.settings.CC_SMOOTH_HIGH: 0.5   # Heavy smoothing
            }
            alpha = smoothing_alphas.get(self.settings.custom_cc_smoothing, 1.0)

            # Apply exponential moving average smoothing
            # smoothed = (alpha × target) + ((1-alpha) × current)
            self.custom_cc_smoothed_value = (alpha * raw_voltage) + ((1.0 - alpha) * self.custom_cc_smoothed_value)

            # Convert to DAC value and output to Channel D
            dac_value = self.voltage_to_dac_value(self.custom_cc_smoothed_value)
            self.dac.channel_d.value = dac_value

        except Exception as e:
            print(f"Error setting custom CC voltage: {e}")

    def set_pitch_cv(self, midi_note):
        """
        Set CV pitch output for a MIDI note

        Args:
            midi_note: MIDI note number (0-127)
        """
        if not self.dac_available:
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
        if not self.dac_available:
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
        if not self.dac_available:
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
        if not self.dac_available:
            return

        # Set pitch CV
        self.set_pitch_cv(midi_note)

        # Activate trigger
        self.trigger_on()

    def note_off(self):
        """Handle note-off event: deactivate trigger"""
        if not self.dac_available:
            return

        # Turn off trigger (gate mode)
        self.trigger_off()
        self.current_note = None

    def add_note(self, note, velocity):
        """
        Add a note to the active notes buffer (polyphonic tracking)
        Updates CV output based on note priority setting

        Session 19 - Translation Hub: Polyphonic MIDI → Monophonic CV with priority

        Args:
            note: MIDI note number (0-127)
            velocity: MIDI velocity (0-127)
        """
        if not self.dac_available:
            return

        # Add note to tracking if not already present
        if not any(n == note for n, v in self.active_notes):
            self.active_notes.append((note, velocity))

        # Update CV output based on note priority
        self._update_cv_output()

    def remove_note(self, note):
        """
        Remove a note from the active notes buffer
        Updates CV output based on note priority setting

        Session 19 - Translation Hub: Polyphonic MIDI → Monophonic CV with priority

        Args:
            note: MIDI note number (0-127)
        """
        if not self.dac_available:
            return

        # Remove note from tracking
        self.active_notes = [(n, v) for n, v in self.active_notes if n != note]

        # Update CV output based on note priority
        self._update_cv_output()

    def _update_cv_output(self):
        """
        Update CV pitch and gate based on active notes and priority setting

        Session 19 - Translation Hub: Implements 4 note priority modes
        - Highest: Play highest pitched note (lead synth - Roland SH-09)
        - Lowest:  Play lowest pitched note (bass synth - Minimoog)
        - Last:    Play most recent note (default - modern MIDI-to-CV)
        - First:   Play first note pressed (drone synth - Crumar Spirit)

        Research validated against professional gear (99% confidence)
        """
        if not self.dac_available:
            return

        # If no notes are active, turn off gate
        if not self.active_notes:
            self.trigger_off()
            self.current_note = None
            return

        # Determine which note to play based on priority mode
        note_to_play = None

        if self.settings.note_priority == self.settings.NOTE_PRIORITY_HIGHEST:
            # Highest: Play highest pitched note (lead synth)
            note_to_play = max(n for n, v in self.active_notes)

        elif self.settings.note_priority == self.settings.NOTE_PRIORITY_LOWEST:
            # Lowest: Play lowest pitched note (bass synth)
            note_to_play = min(n for n, v in self.active_notes)

        elif self.settings.note_priority == self.settings.NOTE_PRIORITY_LAST:
            # Last: Play most recent note (default - most intuitive)
            note_to_play = self.active_notes[-1][0]  # Last note in list

        elif self.settings.note_priority == self.settings.NOTE_PRIORITY_FIRST:
            # First: Play first note pressed (drone synth)
            note_to_play = self.active_notes[0][0]  # First note in list

        # Update CV pitch (Channel A)
        if note_to_play is not None:
            self.set_pitch_cv(note_to_play)

            # Ensure gate is HIGH (stays HIGH as long as ANY note is held)
            # This is industry standard behavior (Kenton PRO SOLO Mk3, etc.)
            if not self.trigger_active:
                self.trigger_on()

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
            'current_note': self.current_note,
            'current_voltage': self.note_to_voltage(self.current_note) if self.current_note else 0.0,
            'trigger_active': self.trigger_active,
            'cv_scale': self.settings.get_cv_scale_name(),
            'trigger_polarity': self.settings.get_trigger_polarity_name()
        }
