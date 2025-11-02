"""Unit tests for CV Note Priority menu integration

Session 19 - Translation Hub: Tests menu UI for note priority selection

Tests that:
- CV category now has 2 settings (Scale + Note Priority)
- Navigation works correctly
- Display text shows current priority mode
- Category preview shows both scale and priority

Run with: pytest tests/test_menu_cv_priority.py -v
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prisme.utils.config import Settings
from prisme.ui.menu import SettingsMenu


def test_cv_category_has_two_settings():
    """Test that CV category now has 2 settings (Scale, Note Priority)"""
    settings = Settings()
    menu = SettingsMenu(settings)

    # Enter menu and navigate to CV category
    menu.enter_menu()

    # Navigate to CV category
    while menu.current_category != menu.CATEGORY_CV:
        menu.navigate_next()

    # CV category should now have 2 settings, so it goes to SETTING level (not directly to VALUE)
    menu.select()  # Enter CV category
    assert menu.current_level == menu.LEVEL_SETTING  # Should be at setting selection
    assert menu.current_setting == 0  # Should start at first setting (Scale)


def test_cv_setting_navigation():
    """Test navigation between CV Scale and Note Priority settings"""
    settings = Settings()
    menu = SettingsMenu(settings)

    # Enter menu and navigate to CV category
    menu.enter_menu()
    while menu.current_category != menu.CATEGORY_CV:
        menu.navigate_next()

    menu.select()  # Enter CV category (now at SETTING level)

    # Should be at CV_SCALE (0)
    assert menu.current_setting == menu.CV_SCALE

    # Navigate to next setting
    menu.navigate_next()
    assert menu.current_setting == menu.CV_NOTE_PRIORITY

    # Navigate back
    menu.navigate_previous()
    assert menu.current_setting == menu.CV_SCALE


def test_note_priority_display_text():
    """Test that note priority display text shows correct mode"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_LAST  # Default
    menu = SettingsMenu(settings)

    # Navigate to CV > Note Priority > VALUE level
    menu.enter_menu()
    while menu.current_category != menu.CATEGORY_CV:
        menu.navigate_next()

    menu.select()  # Enter CV category
    menu.navigate_next()  # Move to Note Priority setting
    menu.select()  # Enter value adjustment

    # Get display text
    line1, line2, line3 = menu.get_display_text()

    assert "Note Priority" in line1
    assert "Last" in line2  # Current mode
    assert "Hi/Lo/Last/First" in line3  # Options hint


def test_note_priority_cycling():
    """Test cycling through all 4 note priority modes"""
    settings = Settings()
    settings.note_priority = Settings.NOTE_PRIORITY_HIGHEST
    menu = SettingsMenu(settings)

    # Navigate to CV > Note Priority > VALUE level
    menu.enter_menu()
    while menu.current_category != menu.CATEGORY_CV:
        menu.navigate_next()

    menu.select()  # Enter CV
    menu.navigate_next()  # Move to Note Priority
    menu.select()  # Enter value adjustment

    # Test cycling forward
    assert settings.note_priority == Settings.NOTE_PRIORITY_HIGHEST

    menu.navigate_next()  # Increase
    assert settings.note_priority == Settings.NOTE_PRIORITY_LOWEST

    menu.navigate_next()  # Increase
    assert settings.note_priority == Settings.NOTE_PRIORITY_LAST

    menu.navigate_next()  # Increase
    assert settings.note_priority == Settings.NOTE_PRIORITY_FIRST

    menu.navigate_next()  # Increase (wraps)
    assert settings.note_priority == Settings.NOTE_PRIORITY_HIGHEST


def test_category_preview_shows_both():
    """Test that CV category preview shows both scale and priority"""
    settings = Settings()
    settings.cv_scale = Settings.CV_SCALE_STANDARD  # 1V/oct
    settings.note_priority = Settings.NOTE_PRIORITY_LAST
    menu = SettingsMenu(settings)

    menu.enter_menu()
    while menu.current_category != menu.CATEGORY_CV:
        menu.navigate_next()

    # Get display text at category level
    line1, line2, line3 = menu.get_display_text()

    # Should show both scale and priority in preview
    assert "CV" in line2  # Category name
    assert "1V/oct" in line2 or "Moog" in line2  # Scale
    assert "Last" in line2 or "Highest" in line2 or "Lowest" in line2 or "First" in line2  # Priority


def test_back_navigation_from_priority():
    """Test that back navigation works correctly from note priority"""
    settings = Settings()
    menu = SettingsMenu(settings)

    # Navigate to CV > Note Priority > VALUE level
    menu.enter_menu()
    while menu.current_category != menu.CATEGORY_CV:
        menu.navigate_next()

    menu.select()  # Enter CV (SETTING level)
    assert menu.current_level == menu.LEVEL_SETTING

    menu.navigate_next()  # Move to Note Priority
    menu.select()  # Enter value adjustment (VALUE level)
    assert menu.current_level == menu.LEVEL_VALUE

    # Back should go to SETTING level (not CATEGORY, since CV now has multiple settings)
    menu.back()
    assert menu.current_level == menu.LEVEL_SETTING

    # Back again should go to CATEGORY level
    menu.back()
    assert menu.current_level == menu.LEVEL_CATEGORY


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
