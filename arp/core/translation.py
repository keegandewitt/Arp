"""Translation pipeline - fixed layer chain

Part of prisme Translation Hub architecture.
Manages the ordered chain of translation layers.

LAYER ORDER IS FIXED: Scale → Arp → Clock
- Scale corrects pitch BEFORE musical processing (not an effect)
- Arp generates sequences from corrected notes
- Clock (external to pipeline) transforms timing globally

This order cannot be changed because Scale is a correction layer,
not a creative effect. It must process notes before Arp.
"""

from .layers import ScaleQuantizeLayer, ArpeggiatorLayer


class TranslationPipeline:
    """Manages the translation layer chain

    Builds a fixed-order chain of translation layers:
    Scale → Arp

    Each layer can be independently enabled/disabled via settings.
    """

    def __init__(self, settings, arpeggiator):
        """Initialize translation pipeline

        Args:
            settings: Settings object with layer configuration
            arpeggiator: Arpeggiator instance for ArpeggiatorLayer
        """
        self.settings = settings
        self.arpeggiator = arpeggiator
        self.layers = []
        self._configure_layers()

    def _configure_layers(self):
        """Build layer chain in fixed order: Scale → Arp

        Only enabled layers are added to the chain.
        Layer order is FIXED and cannot be changed.

        V3: Layers are auto-enabled based on settings values:
        - Scale: enabled when scale_type != CHROMATIC
        - Arp: enabled when octave_range > 0
        """
        self.layers = []

        # Fixed order: Scale → Arp
        if self.settings.is_scale_enabled():
            self.layers.append(ScaleQuantizeLayer(self.settings))
        if self.settings.is_arp_enabled():
            self.layers.append(ArpeggiatorLayer(self.settings, self.arpeggiator))

    def reconfigure(self):
        """Reconfigure layers after settings change

        Call this method when user enables/disables layers
        via menu system.
        """
        self._configure_layers()

    def process_note(self, note, velocity):
        """Pass note through layer chain

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)

        Returns:
            Transformed note number after passing through all layers
        """
        current_note = note

        for layer in self.layers:
            current_note = layer.transform(current_note, velocity)

        return current_note

    def get_layer_count(self):
        """Get number of active layers

        Returns:
            Number of layers currently in the chain
        """
        return len(self.layers)

    def get_layer_names(self):
        """Get names of active layers in order

        Returns:
            List of layer class names
        """
        return [layer.__class__.__name__ for layer in self.layers]
