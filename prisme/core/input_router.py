"""Input Router - Handle MIDI input source selection

Part of prisme Translation Hub architecture.
Routes MIDI input based on user-selected source.
"""


class InputRouter:
    """Routes MIDI input from selected source

    Supports multiple input sources:
    - MIDI IN (UART DIN-5 jack)
    - USB MIDI
    - CV IN (future)
    - Gate IN (future)
    """

    def __init__(self, settings, midi_uart=None, midi_usb=None):
        """Initialize input router

        Args:
            settings: Settings object with input_source
            midi_uart: MIDI object for UART (DIN-5 jack)
            midi_usb: MIDI object for USB MIDI
        """
        self.settings = settings
        self.midi_uart = midi_uart
        self.midi_usb = midi_usb

    def get_midi_message(self):
        """Get next MIDI message from selected input source

        Returns:
            MIDI message object or None if no message available
        """
        # Get the appropriate MIDI object based on input source
        if self.settings.input_source == self.settings.INPUT_SOURCE_MIDI_IN:
            if self.midi_uart:
                return self.midi_uart.receive()
        elif self.settings.input_source == self.settings.INPUT_SOURCE_USB:
            if self.midi_usb:
                return self.midi_usb.receive()
        # Future: CV IN, Gate IN support

        return None

    def get_current_source_name(self):
        """Get human-readable name of current input source

        Returns:
            String name of input source
        """
        if self.settings.input_source == self.settings.INPUT_SOURCE_MIDI_IN:
            return "MIDI IN (DIN-5)"
        elif self.settings.input_source == self.settings.INPUT_SOURCE_USB:
            return "USB MIDI"
        elif self.settings.input_source == self.settings.INPUT_SOURCE_CV_IN:
            return "CV IN (Future)"
        elif self.settings.input_source == self.settings.INPUT_SOURCE_GATE_IN:
            return "Gate IN (Future)"
        return "Unknown"
