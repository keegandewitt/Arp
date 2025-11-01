"""Unit tests for clock transformations

Tests swing, multiply, and divide functionality to ensure
correct timing calculations based on Roger Linn's swing method.
"""

import pytest
import sys
import os

# Add parent directory to path so we can import arp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arp.core.clock import ClockHandler


def test_base_interval_calculation():
    """Test basic tick interval calculation"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=1, divide=1)
    clock.set_internal_bpm(120)

    # At 120 BPM: 60 / (120 * 24) = 0.02083s per tick
    expected = 60.0 / (120 * 24)
    assert abs(clock.base_tick_interval - expected) < 0.0001


def test_clock_multiply_2x():
    """Test 2x clock multiplier (faster ticks)"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=2, divide=1)
    clock.set_internal_bpm(120)

    # At 120 BPM with 2x multiply: half the base interval
    base = 60.0 / (120 * 24)
    expected = base / 2
    assert abs(clock.base_tick_interval - expected) < 0.0001


def test_clock_multiply_4x():
    """Test 4x clock multiplier (4x faster)"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=4, divide=1)
    clock.set_internal_bpm(120)

    # At 120 BPM with 4x multiply: quarter the base interval
    base = 60.0 / (120 * 24)
    expected = base / 4
    assert abs(clock.base_tick_interval - expected) < 0.0001


def test_clock_divide_2():
    """Test 1/2 clock divider (slower ticks)"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=1, divide=2)
    clock.set_internal_bpm(120)

    # At 120 BPM with 1/2 divide: double the base interval
    base = 60.0 / (120 * 24)
    expected = base * 2
    assert abs(clock.base_tick_interval - expected) < 0.0001


def test_clock_divide_4():
    """Test 1/4 clock divider (4x slower)"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=1, divide=4)
    clock.set_internal_bpm(120)

    # At 120 BPM with 1/4 divide: quadruple the base interval
    base = 60.0 / (120 * 24)
    expected = base * 4
    assert abs(clock.base_tick_interval - expected) < 0.0001


def test_multiply_and_divide_cancel():
    """Test that 2x multiply + 1/2 divide cancel out"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=2, divide=2)
    clock.set_internal_bpm(120)

    # Should equal base interval
    base = 60.0 / (120 * 24)
    assert abs(clock.base_tick_interval - base) < 0.0001


def test_swing_50_percent_no_swing():
    """Test that 50% swing equals no swing (equal timing)"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=1, divide=1)
    clock.set_internal_bpm(120)
    clock.tick_count = 0

    # At 50% swing, delay should equal base interval
    delay = clock._calculate_next_tick_delay()
    assert abs(delay - clock.base_tick_interval) < 0.0001


def test_swing_66_percent_triplet():
    """Test 66% swing (perfect triplet swing)"""
    clock = ClockHandler(midi_in_port=None, swing_percent=66, multiply=1, divide=1)
    clock.set_internal_bpm(120)

    base_interval = 60.0 / (120 * 24)
    pair_time = base_interval * 12  # Two 16th notes = 12 ticks

    # First 16th (odd, tick_count=0): Should get 66% of pair time
    clock.tick_count = 0
    delay_odd = clock._calculate_next_tick_delay()
    expected_odd = pair_time * 0.66 / 6
    assert abs(delay_odd - expected_odd) < 0.0001

    # Second 16th (even, tick_count=6): Should get 34% of pair time
    clock.tick_count = 6
    delay_even = clock._calculate_next_tick_delay()
    expected_even = pair_time * 0.34 / 6
    assert abs(delay_even - expected_even) < 0.0001

    # Total time should equal pair_time (timing preserved)
    total_time = (delay_odd * 6) + (delay_even * 6)
    assert abs(total_time - pair_time) < 0.001


def test_swing_62_percent():
    """Test 62% swing (common laid-back groove)"""
    clock = ClockHandler(midi_in_port=None, swing_percent=62, multiply=1, divide=1)
    clock.set_internal_bpm(120)

    base_interval = 60.0 / (120 * 24)
    pair_time = base_interval * 12

    # First 16th: 62% of pair time
    clock.tick_count = 0
    delay_odd = clock._calculate_next_tick_delay()
    expected_odd = pair_time * 0.62 / 6
    assert abs(delay_odd - expected_odd) < 0.0001

    # Second 16th: 38% of pair time
    clock.tick_count = 6
    delay_even = clock._calculate_next_tick_delay()
    expected_even = pair_time * 0.38 / 6
    assert abs(delay_even - expected_even) < 0.0001


def test_swing_alternates_correctly():
    """Test that swing alternates between odd and even 16th notes"""
    clock = ClockHandler(midi_in_port=None, swing_percent=66, multiply=1, divide=1)
    clock.set_internal_bpm(120)

    base_interval = 60.0 / (120 * 24)
    pair_time = base_interval * 12

    # tick_count 0, 1, 2, 3, 4, 5 → odd 16th (first note)
    for tick in range(6):
        clock.tick_count = tick
        delay = clock._calculate_next_tick_delay()
        expected = pair_time * 0.66 / 6
        assert abs(delay - expected) < 0.0001

    # tick_count 6, 7, 8, 9, 10, 11 → even 16th (second note)
    for tick in range(6, 12):
        clock.tick_count = tick
        delay = clock._calculate_next_tick_delay()
        expected = pair_time * 0.34 / 6
        assert abs(delay - expected) < 0.0001

    # tick_count 12, 13, ... → back to odd 16th
    for tick in range(12, 18):
        clock.tick_count = tick
        delay = clock._calculate_next_tick_delay()
        expected = pair_time * 0.66 / 6
        assert abs(delay - expected) < 0.0001


def test_set_swing():
    """Test setting swing dynamically"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=1, divide=1)

    # Initial swing
    assert clock.swing_percent == 50

    # Set to 66%
    clock.set_swing(66)
    assert clock.swing_percent == 66

    # Test clamping (too high)
    clock.set_swing(90)
    assert clock.swing_percent == 75  # Clamped to max

    # Test clamping (too low)
    clock.set_swing(30)
    assert clock.swing_percent == 50  # Clamped to min


def test_set_multiply():
    """Test setting multiply dynamically"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=1, divide=1)
    clock.set_internal_bpm(120)

    base = 60.0 / (120 * 24)

    # Set to 2x
    clock.set_multiply(2)
    assert clock.multiply == 2
    assert abs(clock.base_tick_interval - base / 2) < 0.0001

    # Set to 4x
    clock.set_multiply(4)
    assert clock.multiply == 4
    assert abs(clock.base_tick_interval - base / 4) < 0.0001


def test_set_divide():
    """Test setting divide dynamically"""
    clock = ClockHandler(midi_in_port=None, swing_percent=50, multiply=1, divide=1)
    clock.set_internal_bpm(120)

    base = 60.0 / (120 * 24)

    # Set to 1/2
    clock.set_divide(2)
    assert clock.divide == 2
    assert abs(clock.base_tick_interval - base * 2) < 0.0001

    # Set to 1/4
    clock.set_divide(4)
    assert clock.divide == 4
    assert abs(clock.base_tick_interval - base * 4) < 0.0001


def test_different_bpms():
    """Test clock transformations at various BPMs"""
    bpms = [60, 120, 140, 180]

    for bpm in bpms:
        clock = ClockHandler(midi_in_port=None, swing_percent=66, multiply=2, divide=1)
        clock.set_internal_bpm(bpm)

        # Base interval with 2x multiply
        base = 60.0 / (bpm * 24)
        expected_base = base / 2
        assert abs(clock.base_tick_interval - expected_base) < 0.0001

        # Swing should still work correctly
        pair_time = clock.base_tick_interval * 12
        clock.tick_count = 0
        delay_odd = clock._calculate_next_tick_delay()
        expected_odd = pair_time * 0.66 / 6
        assert abs(delay_odd - expected_odd) < 0.0001


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
