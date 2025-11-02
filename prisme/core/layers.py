"""Translation layer base classes and implementations

Part of prisme Translation Hub architecture.
Provides pluggable layer system for user-configurable processing order.
"""


class TranslationLayer:
    """Base class for all translation layers"""

    def __init__(self, settings):
        """Initialize layer with settings reference

        Args:
            settings: Settings object with configuration
        """
        self.settings = settings

    def transform(self, note, velocity=64):
        """Transform a note - must be implemented by subclass

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)

        Returns:
            Transformed note number
        """
        raise NotImplementedError("Subclasses must implement transform()")


class ScaleQuantizeLayer(TranslationLayer):
    """Quantize notes to the current scale (v3)

    Uses settings.quantize_to_scale() to snap incoming notes
    to the nearest note in the selected scale and root.

    V3: Enabled when scale_type != CHROMATIC (checked via is_scale_enabled())
    """

    def transform(self, note, velocity=64):
        """Quantize note to current scale

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (ignored for quantization)

        Returns:
            Quantized note number (snapped to scale)
        """
        if self.settings.is_scale_enabled():
            return self.settings.quantize_to_scale(note)
        return note


class ArpeggiatorLayer(TranslationLayer):
    """Arpeggiator layer - buffers notes for sequence generation

    This layer doesn't directly transform notes in real-time.
    Instead, it integrates with the Arpeggiator class to buffer
    incoming notes and generate arpeggiated sequences.

    The actual arpeggiation happens via the arpeggiator's
    clock-driven step callback.
    """

    def __init__(self, settings, arpeggiator):
        """Initialize arpeggiator layer

        Args:
            settings: Settings object with configuration
            arpeggiator: Arpeggiator instance for note buffering
        """
        super().__init__(settings)
        self.arpeggiator = arpeggiator

    def transform(self, note, velocity=64):
        """Pass note through (actual arpeggiation is clock-driven)

        The arpeggiator buffers notes and generates sequences
        based on clock ticks, not on note input.

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)

        Returns:
            Original note (no transformation at input)
        """
        # Note: The arpeggiator handles note buffering and
        # sequence generation internally via add_note() and
        # the clock callback system.
        return note
