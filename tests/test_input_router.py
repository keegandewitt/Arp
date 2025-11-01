"""Unit tests for input router

Tests MIDI input source selection and routing logic.
"""

import pytest
import sys
import os

# Add parent directory to path so we can import arp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arp.core.input_router import InputRouter


def test_midi_in_source(mock_settings):
    """Test MIDI IN (UART) source selection"""
    from unittest.mock import MagicMock

    # Create mock MIDI objects
    mock_midi_uart = MagicMock()
    mock_midi_usb = MagicMock()

    # Set up mock messages
    uart_msg = MagicMock()
    usb_msg = MagicMock()
    mock_midi_uart.receive.return_value = uart_msg
    mock_midi_usb.receive.return_value = usb_msg

    # Create router with MIDI IN source
    mock_settings.input_source = mock_settings.INPUT_SOURCE_MIDI_IN
    router = InputRouter(mock_settings, mock_midi_uart, mock_midi_usb)

    # Should receive from UART
    msg = router.get_midi_message()
    assert msg == uart_msg
    mock_midi_uart.receive.assert_called_once()
    mock_midi_usb.receive.assert_not_called()


def test_usb_midi_source(mock_settings):
    """Test USB MIDI source selection"""
    from unittest.mock import MagicMock

    # Create mock MIDI objects
    mock_midi_uart = MagicMock()
    mock_midi_usb = MagicMock()

    # Set up mock messages
    uart_msg = MagicMock()
    usb_msg = MagicMock()
    mock_midi_uart.receive.return_value = uart_msg
    mock_midi_usb.receive.return_value = usb_msg

    # Create router with USB source
    mock_settings.input_source = mock_settings.INPUT_SOURCE_USB
    router = InputRouter(mock_settings, mock_midi_uart, mock_midi_usb)

    # Should receive from USB
    msg = router.get_midi_message()
    assert msg == usb_msg
    mock_midi_usb.receive.assert_called_once()
    mock_midi_uart.receive.assert_not_called()


def test_source_switching(mock_settings):
    """Test switching between input sources"""
    from unittest.mock import MagicMock

    # Create mock MIDI objects
    mock_midi_uart = MagicMock()
    mock_midi_usb = MagicMock()

    # Set up mock messages
    uart_msg = MagicMock()
    usb_msg = MagicMock()
    mock_midi_uart.receive.return_value = uart_msg
    mock_midi_usb.receive.return_value = usb_msg

    # Start with MIDI IN
    mock_settings.input_source = mock_settings.INPUT_SOURCE_MIDI_IN
    router = InputRouter(mock_settings, mock_midi_uart, mock_midi_usb)

    # Get message from UART
    msg = router.get_midi_message()
    assert msg == uart_msg

    # Switch to USB
    mock_settings.input_source = mock_settings.INPUT_SOURCE_USB

    # Get message from USB
    msg = router.get_midi_message()
    assert msg == usb_msg


def test_no_midi_objects(mock_settings):
    """Test router with no MIDI objects (returns None)"""
    mock_settings.input_source = mock_settings.INPUT_SOURCE_MIDI_IN
    router = InputRouter(mock_settings, midi_uart=None, midi_usb=None)

    # Should return None when no MIDI objects available
    msg = router.get_midi_message()
    assert msg is None


def test_source_name_midi_in(mock_settings):
    """Test source name for MIDI IN"""
    mock_settings.input_source = mock_settings.INPUT_SOURCE_MIDI_IN
    router = InputRouter(mock_settings)

    assert router.get_current_source_name() == "MIDI IN (DIN-5)"


def test_source_name_usb(mock_settings):
    """Test source name for USB MIDI"""
    mock_settings.input_source = mock_settings.INPUT_SOURCE_USB
    router = InputRouter(mock_settings)

    assert router.get_current_source_name() == "USB MIDI"


def test_source_name_cv_in(mock_settings):
    """Test source name for CV IN (future)"""
    mock_settings.input_source = mock_settings.INPUT_SOURCE_CV_IN
    router = InputRouter(mock_settings)

    assert router.get_current_source_name() == "CV IN (Future)"


def test_source_name_gate_in(mock_settings):
    """Test source name for Gate IN (future)"""
    mock_settings.input_source = mock_settings.INPUT_SOURCE_GATE_IN
    router = InputRouter(mock_settings)

    assert router.get_current_source_name() == "Gate IN (Future)"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
