"""Translation pipeline - configurable layer chain

Part of prisme Translation Hub architecture.
Manages the ordered chain of translation layers based on user settings.
"""

from .layers import ScaleQuantizeLayer, ArpeggiatorLayer


# Layer ordering constants (imported from config.py)
LAYER_ORDER_SCALE_FIRST = 0  # Scale → Arp
LAYER_ORDER_ARP_FIRST = 1    # Arp → Scale


class TranslationPipeline:
    """Manages the translation layer chain

    Builds and maintains a dynamic chain of translation layers
    based on user configuration. Supports two layer orderings:
    - Scale → Arp: Quantize notes first, then arpeggiate
    - Arp → Scale: Arpeggiate first, then quantize output

    Each layer can be independently enabled/disabled.
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
        """Build layer chain based on user settings

        Creates layer instances in the order specified by
        settings.layer_order. Only enabled layers are added.
        """
        self.layers = []

        if self.settings.layer_order == LAYER_ORDER_SCALE_FIRST:
            # Scale → Arp ordering
            if self.settings.scale_enabled:
                self.layers.append(ScaleQuantizeLayer(self.settings))
            if self.settings.arp_enabled:
                self.layers.append(ArpeggiatorLayer(self.settings, self.arpeggiator))
        else:
            # Arp → Scale ordering (LAYER_ORDER_ARP_FIRST)
            if self.settings.arp_enabled:
                self.layers.append(ArpeggiatorLayer(self.settings, self.arpeggiator))
            if self.settings.scale_enabled:
                self.layers.append(ScaleQuantizeLayer(self.settings))

    def reconfigure(self):
        """Reconfigure layers after settings change

        Call this method when user changes layer order or
        enables/disables layers via menu system.
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
