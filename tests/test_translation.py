"""Unit tests for translation pipeline

Tests the TranslationPipeline and layer system with fixed layer ordering.
Layer order is FIXED: Scale → Arp (cannot be changed).
"""

import pytest
import sys
import os

# Add parent directory to path so we can import arp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prisme.core.translation import TranslationPipeline
from prisme.core.layers import ScaleQuantizeLayer, ArpeggiatorLayer


def test_fixed_layer_ordering(mock_settings, mock_arpeggiator):
    """Test fixed Scale → Arp layer ordering (v3)"""
    mock_settings.scale_type = 1  # SCALE_MAJOR (enabled)
    mock_settings.octave_range = 1  # Arp enabled (octaves > 0)

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Verify layer chain (fixed order: Scale → Arp)
    assert pipeline.get_layer_count() == 2
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ScaleQuantizeLayer'
    assert layer_names[1] == 'ArpeggiatorLayer'


def test_scale_disabled(mock_settings, mock_arpeggiator):
    """Test with scale layer disabled (v3: scale_type = CHROMATIC)"""
    mock_settings.scale_type = 0  # SCALE_CHROMATIC = disabled
    mock_settings.octave_range = 1  # Arp enabled (octaves > 0)

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Should only have arpeggiator layer
    assert pipeline.get_layer_count() == 1
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ArpeggiatorLayer'


def test_arp_disabled(mock_settings, mock_arpeggiator):
    """Test with arpeggiator layer disabled (v3: octave_range = 0)"""
    mock_settings.scale_type = 1  # SCALE_MAJOR (enabled)
    mock_settings.octave_range = 0  # Arp disabled (octaves = 0)

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Should only have scale layer
    assert pipeline.get_layer_count() == 1
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ScaleQuantizeLayer'


def test_both_layers_disabled(mock_settings, mock_arpeggiator):
    """Test with all layers disabled (v3: CHROMATIC + octaves=0)"""
    mock_settings.scale_type = 0  # SCALE_CHROMATIC = disabled
    mock_settings.octave_range = 0  # Arp disabled (octaves = 0)

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Should have no layers (pass-through)
    assert pipeline.get_layer_count() == 0


def test_process_note(mock_settings, mock_arpeggiator):
    """Test note processing through pipeline"""
    mock_settings.scale_type = 1  # SCALE_MAJOR (enabled)
    mock_settings.octave_range = 1  # Arp enabled

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
    """Test pipeline reconfiguration after settings change (v3)"""
    mock_settings.scale_type = 1  # SCALE_MAJOR (enabled)
    mock_settings.octave_range = 1  # Arp enabled (octaves > 0)

    pipeline = TranslationPipeline(mock_settings, mock_arpeggiator)

    # Initial state: 2 layers
    assert pipeline.get_layer_count() == 2

    # Change settings (disable scale in v3: set to CHROMATIC)
    mock_settings.scale_type = 0  # SCALE_CHROMATIC = disabled

    # Reconfigure
    pipeline.reconfigure()

    # Should now have 1 layer
    assert pipeline.get_layer_count() == 1
    layer_names = pipeline.get_layer_names()
    assert layer_names[0] == 'ArpeggiatorLayer'


def test_scale_quantize_layer(mock_settings):
    """Test ScaleQuantizeLayer directly (v3)"""
    layer = ScaleQuantizeLayer(mock_settings)

    # Mock quantization
    def quantize_to_scale(note):
        # C major scale: C=60, D=62, E=64, F=65, G=67, A=69, B=71
        # F# (66) should quantize to G (67)
        if note == 66:
            return 67
        return note

    mock_settings.quantize_to_scale = quantize_to_scale
    mock_settings.scale_type = 1  # SCALE_MAJOR (enabled)

    # Test quantization
    result = layer.transform(66, 100)  # F# should become G
    assert result == 67

    # Test with scale disabled (v3: CHROMATIC)
    mock_settings.scale_type = 0  # SCALE_CHROMATIC = disabled
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
