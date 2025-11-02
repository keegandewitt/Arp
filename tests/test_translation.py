"""Unit tests for translation pipeline

Tests the TranslationPipeline class and layer ordering.
Run with: pytest tests/test_translation.py -v
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prisme.core.translation import TranslationPipeline
from prisme.core.layers import ScaleQuantizeLayer, ArpeggiatorLayer
from prisme.utils.config import Settings


class MockArpeggiator:
    """Mock arpeggiator for testing"""
    def __init__(self, settings):
        self.settings = settings
        self.notes_added = []

    def add_note(self, note, velocity):
        self.notes_added.append((note, velocity))


def test_pipeline_creation():
    """Test that pipeline can be created"""
    settings = Settings()
    arp = MockArpeggiator(settings)
    pipeline = TranslationPipeline(settings, arp)

    assert pipeline is not None
    assert pipeline.settings == settings
    assert pipeline.arpeggiator == arp


def test_layer_order_fixed_scale_then_arp():
    """Test that layers are in FIXED order: Scale → Arp"""
    settings = Settings()
    settings.scale_type = Settings.SCALE_MAJOR  # Scale enabled
    settings.octave_range = 1  # Arp enabled
    arp = MockArpeggiator(settings)

    pipeline = TranslationPipeline(settings, arp)

    layer_names = pipeline.get_layer_names()
    assert len(layer_names) == 2
    assert layer_names[0] == 'ScaleQuantizeLayer'  # Scale FIRST (FIXED)
    assert layer_names[1] == 'ArpeggiatorLayer'    # Arp SECOND (FIXED)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
