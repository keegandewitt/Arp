"""
Custom CC Output Handler
Manages Custom CC output via CV DAC Channel D
Supports CC, Aftertouch, Pitch Bend, Velocity with Learn Mode
"""

from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.channel_pressure import ChannelPressure
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff


class CustomCCHandler:
    """Handles Custom CC MIDI-to-CV conversion with Learn Mode"""

    def __init__(self, cv_output, settings):
        """
        Initialize Custom CC handler

        Args:
            cv_output: CVOutput instance for DAC access
            settings: Global settings object
        """
        self.cv_output = cv_output
        self.settings = settings

        # Learn Mode state
        self.learn_mode_active = False

        # Last MIDI message tracking (for display feedback)
        self.last_message_type = None
        self.last_message_value = None
        self.last_cc_number = None

    def enter_learn_mode(self):
        """Enter Learn Mode - next CC received will be captured"""
        self.learn_mode_active = True
        print("[Learn Mode] Active - send a CC message to capture")

    def exit_learn_mode(self, captured_cc=None):
        """Exit Learn Mode"""
        self.learn_mode_active = False
        if captured_cc is not None:
            print(f"[Learn Mode] Captured CC #{captured_cc}")
        else:
            print("[Learn Mode] Cancelled")

    def process_messages(self, messages):
        """
        Process incoming MIDI messages for Custom CC output

        Args:
            messages: List of MIDI message objects
        """
        # If Custom CC is disabled, do nothing
        if self.settings.custom_cc_source == self.settings.CC_SOURCE_DISABLED:
            return

        for msg in messages:
            # Handle Learn Mode (only for CC messages)
            if self.learn_mode_active and isinstance(msg, ControlChange):
                # Capture CC number and exit learn mode
                self.settings.custom_cc_number = msg.control
                self.settings.custom_cc_source = self.settings.CC_SOURCE_CC
                self.settings.save()  # Auto-save
                self.exit_learn_mode(captured_cc=msg.control)
                # Fall through to process the message

            # Route message based on source type
            if self.settings.custom_cc_source == self.settings.CC_SOURCE_CC:
                self._process_cc(msg)

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_AFTERTOUCH:
                self._process_aftertouch(msg)

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_PITCHBEND:
                self._process_pitch_bend(msg)

            elif self.settings.custom_cc_source == self.settings.CC_SOURCE_VELOCITY:
                self._process_velocity(msg)

    def _process_cc(self, msg):
        """Process Control Change messages"""
        if isinstance(msg, ControlChange):
            # Only process the CC number we're listening to
            if msg.control == self.settings.custom_cc_number:
                voltage = self.cv_output.cc_to_voltage(msg.value)
                self.cv_output.set_custom_cc_voltage(voltage)

                # Update display tracking
                self.last_message_type = "CC"
                self.last_message_value = msg.value
                self.last_cc_number = msg.control

    def _process_aftertouch(self, msg):
        """Process Channel Pressure (Aftertouch) messages"""
        if isinstance(msg, ChannelPressure):
            voltage = self.cv_output.aftertouch_to_voltage(msg.pressure)
            self.cv_output.set_custom_cc_voltage(voltage)

            # Update display tracking
            self.last_message_type = "AT"  # Aftertouch
            self.last_message_value = msg.pressure
            self.last_cc_number = None

    def _process_pitch_bend(self, msg):
        """Process Pitch Bend messages"""
        if isinstance(msg, PitchBend):
            voltage = self.cv_output.pitch_bend_to_voltage(msg.pitch_bend)
            self.cv_output.set_custom_cc_voltage(voltage)

            # Update display tracking
            self.last_message_type = "PB"  # Pitch Bend
            self.last_message_value = msg.pitch_bend
            self.last_cc_number = None

    def _process_velocity(self, msg):
        """Process Note Velocity messages (NoteOn only)"""
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            voltage = self.cv_output.velocity_to_voltage(msg.velocity)
            self.cv_output.set_custom_cc_voltage(voltage)

            # Update display tracking
            self.last_message_type = "VEL"
            self.last_message_value = msg.velocity
            self.last_cc_number = None

        elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
            # Note off - reset to 0V
            self.cv_output.set_custom_cc_voltage(0.0)

            # Update display tracking
            self.last_message_type = "VEL"
            self.last_message_value = 0
            self.last_cc_number = None

    def get_last_midi_display(self):
        """
        Get last MIDI message for display feedback

        Returns:
            String formatted for OLED display (e.g., "CC#74 V:64")
        """
        if self.last_message_type is None:
            return "No MIDI yet"

        if self.last_message_type == "CC" and self.last_cc_number is not None:
            return f"CC#{self.last_cc_number} V:{self.last_message_value}"
        elif self.last_message_type == "AT":
            return f"AT V:{self.last_message_value}"
        elif self.last_message_type == "PB":
            return f"PB V:{self.last_message_value}"
        elif self.last_message_type == "VEL":
            return f"VEL V:{self.last_message_value}"
        else:
            return "Unknown"

    def get_learn_mode_status(self):
        """
        Get learn mode status for display

        Returns:
            String indicating learn mode state
        """
        if self.learn_mode_active:
            return "LEARN MODE"
        else:
            return ""
