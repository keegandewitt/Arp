"""Unit tests for translation pipeline

Tests the TranslationPipeline and layer system to ensure
correct behavior of user-configurable layer ordering.
"""

import pytest
import sys
import os

# Add parent directory to path so we can import arp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arp.core.translation import TranslationPipeline, LAYER_ORDER_SCALE_FIRST, LAYER_ORDER_ARP_FIRST
from arp.core.layers import ScaleQuantizeLayer, ArpeggiatorLayer


def test_scale_first_ordering(mock_settings, mock_arpeggiator):
    """Test Scale → Arp layer ordering"""
    mock_settings.layer_order = LAYER_ORDER_SCALE_FIRST
    mock_settings.scale_enabled = True
    mock_settings.arp_enabled = True

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Verify layer chain
    assert pipeline.get_layer_count() == 2
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ScaleQuantizeLayer'
    assert layer_names[1] == 'ArpeggiatorLayer'


def test_arp_first_ordering(mock_settings, mock_arpeggiator):
    """Test Arp → Scale layer ordering"""
    mock_settings.layer_order = LAYER_ORDER_ARP_FIRST
    mock_settings.scale_enabled = True
    mock_settings.arp_enabled = True

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Verify layer chain
    assert pipeline.get_layer_count() == 2
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ArpeggiatorLayer'
    assert layer_names[1] == 'ScaleQuantizeLayer'


def test_scale_disabled(mock_settings, mock_arpeggiator):
    """Test with scale layer disabled"""
    mock_settings.layer_order = LAYER_ORDER_SCALE_FIRST
    mock_settings.scale_enabled = False
    mock_settings.arp_enabled = True

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Should only have arpeggiator layer
    assert pipeline.get_layer_count() == 1
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ArpeggiatorLayer'


def test_arp_disabled(mock_settings, mock_arpeggiator):
    """Test with arpeggiator layer disabled"""
    mock_settings.layer_order = LAYER_ORDER_SCALE_FIRST
    mock_settings.scale_enabled = True
    mock_settings.arp_enabled = False

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Should only have scale layer
    assert pipeline.get_layer_count() == 1
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ScaleQuantizeLayer'


def test_both_layers_disabled(mock_settings, mock_arpeggiator):
    """Test with all layers disabled (pass-through)"""
    mock_settings.layer_order = LAYER_ORDER_SCALE_FIRST
    mock_settings.scale_enabled = False
    mock_settings.arp_enabled = False

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Should have no layers (pass-through)
    assert pipeline.get_layer_count() == 0


def test_process_note(mock_settings, mock_arpeggiator):
    """Test note processing through pipeline"""
    mock_settings.layer_order = LAYER_ORDER_SCALE_FIRST
    mock_settings.scale_enabled = True
    mock_settings.arp_enabled = True

    # Mock quantization to shift note by 1 semitone
    def quantize_to_scale(note):
        return note + 1

    mock_settings.quantize_to_scale = quantize_to_scale

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Process note
    result = pipeline.process_note(60, 100)  # Middle C

    # Should be quantized (+1 semitone)
    assert result == 61


def test_reconfigure(mock_settings, mock_arpeggiator):
    """Test pipeline reconfiguration after settings change"""
    mock_settings.layer_order = LAYER_ORDER_SCALE_FIRST
    mock_settings.scale_enabled = True
    mock_settings.arp_enabled = True

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Initial state: 2 layers
    assert pipeline.get_layer_count() == 2

    # Change settings
    mock_settings.scale_enabled = False

    # Reconfigure
    pipeline.reconfigure()

    # Should now have 1 layer
    assert pipeline.get_layer_count() == 1
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ArpeggiatorLayer'


def test_scale_quantize_layer(mock_settings):
    """Test ScaleQuantizeLayer directly"""
    layer = ScaleQuantizeLayer(mock_settings)

    # Mock quantization
    def quantize_to_scale(note):
        # C major scale: C=60, D=62, E=64, F=65, G=67, A=69, B=71
        # F# (66) should quantize to G (67)
        if note == 66:
            return 67
        return note

    mock_settings.quantize_to_scale = quantize_to_scale
    mock_settings.scale_enabled = True

    # Test quantization
    result = layer.transform(66, 100)  # F# should become G
    assert result == 67

    # Test with scale disabled
    mock_settings.scale_enabled = False
    result = layer.transform(66, 100)  # Should pass through
    assert result == 66


def test_arpeggiator_layer(mock_settings, mock_arpeggiator):
    """Test ArpeggiatorLayer directly"""
    layer = ArpeggiatorLayer(mock_settings, mock_arpeggiator)

    # Arpeggiator layer passes through notes
    # (actual arpeggiation is clock-driven)
    result = layer.transform(60, 100)
    assert result == 60


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
