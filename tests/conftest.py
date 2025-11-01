"""PyTest configuration - CircuitPython mocks

Automatically mocks CircuitPython-specific modules so tests can run
on conventional computers without CircuitPython hardware.

Based on Nicholas Tollervey's CircuitPython testing guide.
"""

import sys
from unittest.mock import MagicMock


# Mock CircuitPython modules BEFORE any imports happen
# This runs at module load time, before pytest collection
sys.modules['board'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['digitalio'] = MagicMock()
sys.modules['usb_midi'] = MagicMock()
sys.modules['adafruit_midi'] = MagicMock()
sys.modules['adafruit_midi.timing_clock'] = MagicMock()
sys.modules['adafruit_midi.start'] = MagicMock()
sys.modules['adafruit_midi.stop'] = MagicMock()
sys.modules['adafruit_midi.midi_continue'] = MagicMock()
sys.modules['adafruit_midi.note_on'] = MagicMock()
sys.modules['adafruit_midi.note_off'] = MagicMock()
sys.modules['adafruit_midi.control_change'] = MagicMock()
sys.modules['adafruit_midi.pitch_bend'] = MagicMock()
sys.modules['microcontroller'] = MagicMock()
sys.modules['displayio'] = MagicMock()
sys.modules['i2cdisplaybus'] = MagicMock()
sys.modules['adafruit_displayio_sh1107'] = MagicMock()
sys.modules['adafruit_display_text'] = MagicMock()
sys.modules['adafruit_display_text.label'] = MagicMock()
sys.modules['terminalio'] = MagicMock()
sys.modules['adafruit_mcp4728'] = MagicMock()
sys.modules['analogio'] = MagicMock()
sys.modules['pwmio'] = MagicMock()


def pytest_runtest_setup(item):
    """Called before each test (kept for compatibility)

    Args:
        item: Test item being run
    """
    # Mocks are already set up at module load time
    pass


# Pytest fixtures can be added here
import pytest


@pytest.fixture
def mock_settings():
    """Mock Settings object for testing

    Returns:
        Mock Settings with default values
    """
    from unittest.mock import MagicMock

    settings = MagicMock()
    settings.scale_enabled = True
    settings.arp_enabled = True
    settings.layer_order = 0  # LAYER_ORDER_SCALE_FIRST
    settings.routing_mode = 1  # ROUTING_TRANSLATION
    settings.input_source = 0  # INPUT_SOURCE_MIDI_IN
    settings.clock_multiply = 1
    settings.clock_divide = 1
    settings.swing_percent = 50

    # Mock quantize_to_scale method
    def quantize_to_scale(note):
        """Mock quantization - just return the note"""
        return note

    settings.quantize_to_scale = quantize_to_scale

    return settings


@pytest.fixture
def mock_arpeggiator(mock_settings):
    """Mock Arpeggiator object for testing

    Args:
        mock_settings: Mock settings fixture

    Returns:
        Mock Arpeggiator instance
    """
    from unittest.mock import MagicMock

    arp = MagicMock()
    arp.settings = mock_settings
    arp.note_buffer = []

    def add_note(note, velocity):
        """Mock add_note method"""
        arp.note_buffer.append((note, velocity))

    def remove_note(note):
        """Mock remove_note method"""
        arp.note_buffer = [(n, v) for n, v in arp.note_buffer if n != note]

    arp.add_note = add_note
    arp.remove_note = remove_note

    return arp
