"""Unit tests for CV output note priority system

Session 19 - Translation Hub: Tests polyphonic note tracking with monophonic CV output

Tests the 4 note priority modes:
- Highest: Play highest pitched note (lead synth)
- Lowest: Play lowest pitched note (bass synth)
- Last: Play most recent note (default)
- First: Play first note pressed (drone synth)

Run with: pytest tests/test_cv_priority.py -v
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prisme.utils.config import Settings


class MockDAC:
    """Mock MCP4728 DAC for testing"""
    def __init__(self):
        self.channel_a = MockChannel()  # CV pitch
        self.channel_b = MockChannel()  # Gate/trigger
        self.channel_c = MockChannel()  # Unused
        self.channel_d = MockChannel()  # Custom CC


class MockChannel:
    """Mock DAC channel"""
    def __init__(self):
        self.value = 0
        self.vref = None
        self.gain = 1


class MockI2C:
    """Mock I2C bus for testing"""
    pass


class MockCVOutput:
    """
    Mock CVOutput for testing note priority logic
    Simulates the behavior of prisme.drivers.cv_gate.CVOutput
    """

    def __init__(self, settings):
        self.settings = settings
        self.dac_available = True
        self.active_notes = []
        self.current_note = None
        self.trigger_active = False

        # Track CV output for testing
        self.cv_note_history = []  # List of notes sent to CV output

    def add_note(self, note, velocity):
        """Add note to tracking and update CV output based on priority"""
        if not any(n == note for n, v in self.active_notes):
            self.active_notes.append((note, velocity))
        self._update_cv_output()

    def remove_note(self, note):
        """Remove note from tracking and update CV output based on priority"""
        self.active_notes = [(n, v) for n, v in self.active_notes if n != note]
        self._update_cv_output()

    def _update_cv_output(self):
        """Update CV pitch and gate based on active notes and priority setting"""
        if not self.active_notes:
            self.trigger_active = False
            self.current_note = None
            return

        # Determine which note to play based on priority mode
        note_to_play = None

        if self.settings.note_priority == self.settings.NOTE_PRIORITY_HIGHEST:
            note_to_play = max(n for n, v in self.active_notes)
        elif self.settings.note_priority == self.settings.NOTE_PRIORITY_LOWEST:
            note_to_play = min(n for n, v in self.active_notes)
        elif self.settings.note_priority == self.settings.NOTE_PRIORITY_LAST:
            note_to_play = self.active_notes[-1][0]
        elif self.settings.note_priority == self.settings.NOTE_PRIORITY_FIRST:
            note_to_play = self.active_notes[0][0]

        if note_to_play is not None:
            self.current_note = note_to_play
            self.cv_note_history.append(note_to_play)
            self.trigger_active = True


# =============================================================================
# Priority Mode Tests
# =============================================================================

def test_priority_highest():
    """Test HIGHEST note priority (lead synth mode)"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_HIGHEST
    cv = MockCVOutput(settings)

    # Play C3, E3, G3 (C major chord)
    cv.add_note(60, 100)  # C3
    assert cv.current_note == 60  # Only note, so C3

    cv.add_note(64, 100)  # E3
    assert cv.current_note == 64  # E3 is higher, so switches to E3

    cv.add_note(67, 100)  # G3
    assert cv.current_note == 67  # G3 is highest, so switches to G3

    # Release G3 - should return to E3
    cv.remove_note(67)
    assert cv.current_note == 64  # E3 is now highest

    # Release E3 - should return to C3
    cv.remove_note(64)
    assert cv.current_note == 60  # C3 is now highest

    # Release C3 - should turn off
    cv.remove_note(60)
    assert cv.current_note is None
    assert cv.trigger_active is False


def test_priority_lowest():
    """Test LOWEST note priority (bass synth mode - Minimoog style)"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_LOWEST
    cv = MockCVOutput(settings)

    # Play G3, E3, C3 (reverse order)
    cv.add_note(67, 100)  # G3
    assert cv.current_note == 67  # Only note, so G3

    cv.add_note(64, 100)  # E3
    assert cv.current_note == 64  # E3 is lower, so switches to E3

    cv.add_note(60, 100)  # C3
    assert cv.current_note == 60  # C3 is lowest, so switches to C3

    # Release C3 - should return to E3
    cv.remove_note(60)
    assert cv.current_note == 64  # E3 is now lowest

    # Release E3 - should return to G3
    cv.remove_note(64)
    assert cv.current_note == 67  # G3 is now lowest

    # Release G3 - should turn off
    cv.remove_note(67)
    assert cv.current_note is None
    assert cv.trigger_active is False


def test_priority_last():
    """Test LAST note priority (default - modern MIDI-to-CV style)"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_LAST
    cv = MockCVOutput(settings)

    # Play C3, E3, G3 (order matters!)
    cv.add_note(60, 100)  # C3
    assert cv.current_note == 60  # Most recent

    cv.add_note(64, 100)  # E3
    assert cv.current_note == 64  # Most recent

    cv.add_note(67, 100)  # G3
    assert cv.current_note == 67  # Most recent

    # Release E3 (middle note) - should stay on G3 (still most recent)
    cv.remove_note(64)
    assert cv.current_note == 67  # G3 still most recent

    # Release G3 - should return to C3 (now most recent of remaining)
    cv.remove_note(67)
    assert cv.current_note == 60  # C3 is most recent remaining

    # Release C3 - should turn off
    cv.remove_note(60)
    assert cv.current_note is None


def test_priority_first():
    """Test FIRST note priority (drone synth mode - Crumar Spirit style)"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_FIRST
    cv = MockCVOutput(settings)

    # Play C3, E3, G3
    cv.add_note(60, 100)  # C3 - first note
    assert cv.current_note == 60  # First note

    cv.add_note(64, 100)  # E3
    assert cv.current_note == 60  # C3 still first

    cv.add_note(67, 100)  # G3
    assert cv.current_note == 60  # C3 still first

    # Release G3 - should stay on C3
    cv.remove_note(67)
    assert cv.current_note == 60  # C3 still first

    # Release E3 - should stay on C3
    cv.remove_note(64)
    assert cv.current_note == 60  # C3 still first

    # Release C3 - should turn off
    cv.remove_note(60)
    assert cv.current_note is None


# =============================================================================
# Edge Case Tests
# =============================================================================

def test_duplicate_note_ignored():
    """Test that duplicate notes are ignored (no double-add)"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_LAST
    cv = MockCVOutput(settings)

    cv.add_note(60, 100)
    assert len(cv.active_notes) == 1

    # Add same note again - should be ignored
    cv.add_note(60, 100)
    assert len(cv.active_notes) == 1  # Still only 1 note


def test_remove_nonexistent_note():
    """Test that removing a note that doesn't exist is safe"""
    settings = Settings()
    cv = MockCVOutput(settings)

    cv.add_note(60, 100)
    cv.remove_note(64)  # Note that was never added
    assert len(cv.active_notes) == 1  # Still has C3


def test_gate_stays_high():
    """Test that gate stays HIGH as long as ANY note is held"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_LAST
    cv = MockCVOutput(settings)

    cv.add_note(60, 100)
    assert cv.trigger_active is True

    cv.add_note(64, 100)
    assert cv.trigger_active is True  # Still high

    cv.remove_note(64)
    assert cv.trigger_active is True  # Still high (C3 held)

    cv.remove_note(60)
    assert cv.trigger_active is False  # Now low (no notes)


def test_all_priority_modes_cycle():
    """Test cycling through all 4 priority modes"""
    settings = Settings()

    # Test next_note_priority()
    settings.note_priority = Settings.NOTE_PRIORITY_HIGHEST
    settings.next_note_priority()
    assert settings.note_priority == Settings.NOTE_PRIORITY_LOWEST

    settings.next_note_priority()
    assert settings.note_priority == Settings.NOTE_PRIORITY_LAST

    settings.next_note_priority()
    assert settings.note_priority == Settings.NOTE_PRIORITY_FIRST

    settings.next_note_priority()
    assert settings.note_priority == Settings.NOTE_PRIORITY_HIGHEST  # Wraps

    # Test previous_note_priority()
    settings.note_priority = Settings.NOTE_PRIORITY_HIGHEST
    settings.previous_note_priority()
    assert settings.note_priority == Settings.NOTE_PRIORITY_FIRST  # Wraps backward


def test_priority_mode_names():
    """Test that priority mode names are correct"""
    settings = Settings()

    settings.note_priority = Settings.NOTE_PRIORITY_HIGHEST
    assert settings.get_note_priority_name() == "Highest"

    settings.note_priority = Settings.NOTE_PRIORITY_LOWEST
    assert settings.get_note_priority_name() == "Lowest"

    settings.note_priority = Settings.NOTE_PRIORITY_LAST
    assert settings.get_note_priority_name() == "Last"

    settings.note_priority = Settings.NOTE_PRIORITY_FIRST
    assert settings.get_note_priority_name() == "First"


# =============================================================================
# Trill & Musical Performance Tests
# =============================================================================

def test_trill_effect_last_priority():
    """Test trill effect (rapid note alternation) with LAST priority"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_LAST
    cv = MockCVOutput(settings)

    # Trill between C3 and E3 (Keith Emerson style)
    cv.add_note(60, 100)  # C3
    cv.add_note(64, 100)  # E3
    assert cv.current_note == 64  # E3 (last)

    cv.remove_note(64)  # Release E3
    assert cv.current_note == 60  # Returns to C3

    cv.add_note(64, 100)  # E3 again
    assert cv.current_note == 64  # Back to E3

    cv.remove_note(64)
    assert cv.current_note == 60  # Back to C3


def test_bass_pedal_lowest_priority():
    """Test bass pedal technique with LOWEST priority"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_LOWEST
    cv = MockCVOutput(settings)

    # Hold low C2 (bass pedal), then play melody above
    cv.add_note(36, 100)  # C2 (bass pedal)
    assert cv.current_note == 36

    cv.add_note(60, 100)  # C3 (melody)
    assert cv.current_note == 36  # Still on bass pedal

    cv.add_note(64, 100)  # E3 (melody)
    assert cv.current_note == 36  # Still on bass pedal

    cv.add_note(67, 100)  # G3 (melody)
    assert cv.current_note == 36  # Still on bass pedal

    # Release melody notes - bass pedal continues
    cv.remove_note(67)
    cv.remove_note(64)
    cv.remove_note(60)
    assert cv.current_note == 36  # Bass pedal still held

    # Release bass pedal
    cv.remove_note(36)
    assert cv.current_note is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
