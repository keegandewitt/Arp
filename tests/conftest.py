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
    """Mock Settings object for testing (v3 format)

    Returns:
        Mock Settings with default v3 values
    """
    from unittest.mock import MagicMock

    settings = MagicMock()

    # V3 settings (unified controls)
    settings.scale_type = 1  # SCALE_MAJOR (enabled)
    settings.octave_range = 1  # Arp enabled (octaves > 0)
    settings.routing_mode = 1  # ROUTING_TRANSLATION
    settings.input_source = 0  # INPUT_SOURCE_MIDI_IN
    settings.clock_rate = 3  # CLOCK_RATE_1X
    settings.timing_feel = 50  # No swing

    # V3 helper methods (must return actual booleans)
    def is_scale_enabled():
        """V3: Scale enabled when scale_type != CHROMATIC (0)"""
        return settings.scale_type != 0

    def is_arp_enabled():
        """V3: Arp enabled when octave_range > 0"""
        return settings.octave_range > 0

    def is_clock_active():
        """V3: Clock active when rate != 1x OR timing_feel != 50%"""
        return settings.clock_rate != 3 or settings.timing_feel != 50

    settings.is_scale_enabled = is_scale_enabled
    settings.is_arp_enabled = is_arp_enabled
    settings.is_clock_active = is_clock_active

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
