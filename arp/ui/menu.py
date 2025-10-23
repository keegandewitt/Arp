"""
Settings Menu Handler
Manages hierarchical settings menu navigation with three categories: BPM, Triggers, CV
"""


class SettingsMenu:
    """Handles hierarchical settings menu navigation"""

    # Menu levels
    LEVEL_CATEGORY = 0  # Top level: Arp Mode, BPM, Triggers, CV
    LEVEL_SETTING = 1   # Setting level: specific settings within a category
    LEVEL_VALUE = 2     # Value level: adjusting a specific value

    # Categories
    CATEGORY_ARP = 0
    CATEGORY_SCALE = 1
    CATEGORY_CLOCK = 2
    CATEGORY_TRIGGERS = 3
    CATEGORY_CV = 4
    CATEGORY_FIRMWARE = 5

    # Arp settings
    ARP_PATTERN = 0       # Up, Down, Up-Down, etc.
    ARP_OCTAVES = 1       # Octave range (1-4)

    # Scale settings
    SCALE_TYPE = 0        # Scale type (Major, Minor, etc.)
    SCALE_ROOT = 1        # Root note (C, C#, D, etc.)

    # Clock settings
    CLOCK_SOURCE = 0      # Internal or External
    CLOCK_BPM = 1         # BPM (only shown if Internal)

    # Trigger settings (only polarity now - always gate mode)
    TRIGGER_POLARITY = 0  # V-trig vs S-trig

    # CV settings
    CV_SCALE = 0  # 1V/octave vs 1.035V/octave (Moog)

    # Firmware settings
    FIRMWARE_INFO = 0     # Show firmware info
    FIRMWARE_UPDATE = 1   # Update firmware option

    def __init__(self, settings):
        """
        Initialize settings menu

        Args:
            settings: Global settings object
        """
        self.settings = settings
        self.menu_active = False

        # Navigation state
        self.current_level = self.LEVEL_CATEGORY
        self.current_category = self.CATEGORY_ARP
        self.current_setting = 0

        # Category names
        self.category_names = {
            self.CATEGORY_ARP: "Arp Mode",
            self.CATEGORY_SCALE: "Scale",
            self.CATEGORY_CLOCK: "Clock",
            self.CATEGORY_TRIGGERS: "Triggers",
            self.CATEGORY_CV: "CV",
            self.CATEGORY_FIRMWARE: "Firmware"
        }

        # Arp setting names
        self.arp_setting_names = {
            self.ARP_PATTERN: "Pattern",
            self.ARP_OCTAVES: "Octaves"
        }

        # Scale setting names
        self.scale_setting_names = {
            self.SCALE_TYPE: "Type",
            self.SCALE_ROOT: "Root"
        }

        # Clock setting names
        self.clock_setting_names = {
            self.CLOCK_SOURCE: "Source",
            self.CLOCK_BPM: "BPM"
        }

        # Trigger setting names
        self.trigger_setting_names = {
            self.TRIGGER_POLARITY: "Polarity"
        }

        # CV setting names
        self.cv_setting_names = {
            self.CV_SCALE: "Scale"
        }

        # Firmware setting names
        self.firmware_setting_names = {
            self.FIRMWARE_INFO: "Info",
            self.FIRMWARE_UPDATE: "Update"
        }

    def enter_menu(self):
        """Enter settings menu"""
        self.menu_active = True
        self.current_level = self.LEVEL_CATEGORY
        self.current_category = self.CATEGORY_ARP
        self.current_setting = 0

    def exit_menu(self):
        """Exit settings menu"""
        self.menu_active = False
        self.current_level = self.LEVEL_CATEGORY
        self.current_category = self.CATEGORY_ARP
        self.current_setting = 0

    def navigate_previous(self):
        """Navigate to previous item at current level"""
        if self.current_level == self.LEVEL_CATEGORY:
            # Cycle through categories
            self.current_category = (self.current_category - 1) % 6

        elif self.current_level == self.LEVEL_SETTING:
            # Cycle through settings within category
            if self.current_category == self.CATEGORY_ARP:
                self.current_setting = (self.current_setting - 1) % 2
            elif self.current_category == self.CATEGORY_SCALE:
                self.current_setting = (self.current_setting - 1) % 2
            elif self.current_category == self.CATEGORY_CLOCK:
                self.current_setting = (self.current_setting - 1) % 2
            elif self.current_category == self.CATEGORY_TRIGGERS:
                # Triggers only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_CV:
                # CV only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_FIRMWARE:
                self.current_setting = (self.current_setting - 1) % 2

        elif self.current_level == self.LEVEL_VALUE:
            # Decrease value
            self._decrease_value()

    def navigate_next(self):
        """Navigate to next item at current level"""
        if self.current_level == self.LEVEL_CATEGORY:
            # Cycle through categories
            self.current_category = (self.current_category + 1) % 6

        elif self.current_level == self.LEVEL_SETTING:
            # Cycle through settings within category
            if self.current_category == self.CATEGORY_ARP:
                self.current_setting = (self.current_setting + 1) % 2
            elif self.current_category == self.CATEGORY_SCALE:
                self.current_setting = (self.current_setting + 1) % 2
            elif self.current_category == self.CATEGORY_CLOCK:
                self.current_setting = (self.current_setting + 1) % 2
            elif self.current_category == self.CATEGORY_TRIGGERS:
                # Triggers only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_CV:
                # CV only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_FIRMWARE:
                self.current_setting = (self.current_setting + 1) % 2

        elif self.current_level == self.LEVEL_VALUE:
            # Increase value
            self._increase_value()

    def select(self):
        """Select/enter current item (drill down or toggle)"""
        if self.current_level == self.LEVEL_CATEGORY:
            # Enter category
            if self.current_category == self.CATEGORY_CLOCK:
                # Clock has multiple settings, go to setting selection
                self.current_level = self.LEVEL_SETTING
                self.current_setting = 0
            elif self.current_category == self.CATEGORY_TRIGGERS:
                # Triggers goes directly to polarity adjustment (only one setting)
                self.current_level = self.LEVEL_VALUE
                self.current_setting = self.TRIGGER_POLARITY
            elif self.current_category == self.CATEGORY_CV:
                # CV goes directly to scale adjustment (only one setting)
                self.current_level = self.LEVEL_VALUE
                self.current_setting = self.CV_SCALE
            elif self.current_category == self.CATEGORY_FIRMWARE:
                # Firmware goes directly to info display
                self.current_level = self.LEVEL_VALUE
                self.current_setting = self.FIRMWARE_INFO
            else:
                # Arp and Scale have multiple settings, go to setting selection
                self.current_level = self.LEVEL_SETTING
                self.current_setting = 0

        elif self.current_level == self.LEVEL_SETTING:
            # Enter value adjustment
            self.current_level = self.LEVEL_VALUE

        elif self.current_level == self.LEVEL_VALUE:
            # Toggle value (for settings with discrete options)
            self._toggle_value()

    def back(self):
        """Go back to previous level"""
        if self.current_level == self.LEVEL_VALUE:
            # Go back to setting selection (or category for single-setting categories)
            if (self.current_category == self.CATEGORY_TRIGGERS or
                self.current_category == self.CATEGORY_CV or
                self.current_category == self.CATEGORY_FIRMWARE):
                self.current_level = self.LEVEL_CATEGORY
            else:
                self.current_level = self.LEVEL_SETTING

        elif self.current_level == self.LEVEL_SETTING:
            # Go back to category selection
            self.current_level = self.LEVEL_CATEGORY

        elif self.current_level == self.LEVEL_CATEGORY:
            # Exit menu
            self.exit_menu()

    def _increase_value(self):
        """Increase current setting value"""
        if self.current_category == self.CATEGORY_ARP:
            if self.current_setting == self.ARP_PATTERN:
                # Cycle to next pattern
                self.settings.next_pattern()
            elif self.current_setting == self.ARP_OCTAVES:
                # Increase octave range
                self.settings.octave_range = min(4, self.settings.octave_range + 1)

        elif self.current_category == self.CATEGORY_SCALE:
            if self.current_setting == self.SCALE_TYPE:
                # Cycle to next scale
                self.settings.next_scale()
            elif self.current_setting == self.SCALE_ROOT:
                # Cycle to next root note
                self.settings.next_root_note()

        elif self.current_category == self.CATEGORY_CLOCK:
            if self.current_setting == self.CLOCK_SOURCE:
                # Toggle clock source
                self.settings.toggle_clock_source()
            elif self.current_setting == self.CLOCK_BPM:
                # Increase BPM by 1
                self.settings.internal_bpm = min(300, self.settings.internal_bpm + 1)

        elif self.current_category == self.CATEGORY_TRIGGERS:
            if self.current_setting == self.TRIGGER_POLARITY:
                self.settings.toggle_trigger_polarity()

        elif self.current_category == self.CATEGORY_CV:
            if self.current_setting == self.CV_SCALE:
                self.settings.toggle_cv_scale()

    def _decrease_value(self):
        """Decrease current setting value"""
        if self.current_category == self.CATEGORY_ARP:
            if self.current_setting == self.ARP_PATTERN:
                # Cycle to previous pattern
                self.settings.pattern = (self.settings.pattern - 1) % 16
            elif self.current_setting == self.ARP_OCTAVES:
                # Decrease octave range
                self.settings.octave_range = max(1, self.settings.octave_range - 1)

        elif self.current_category == self.CATEGORY_SCALE:
            if self.current_setting == self.SCALE_TYPE:
                # Cycle to previous scale
                self.settings.previous_scale()
            elif self.current_setting == self.SCALE_ROOT:
                # Cycle to previous root note
                self.settings.previous_root_note()

        elif self.current_category == self.CATEGORY_CLOCK:
            if self.current_setting == self.CLOCK_SOURCE:
                # Toggle clock source
                self.settings.toggle_clock_source()
            elif self.current_setting == self.CLOCK_BPM:
                # Decrease BPM by 1
                self.settings.internal_bpm = max(30, self.settings.internal_bpm - 1)

        elif self.current_category == self.CATEGORY_TRIGGERS:
            if self.current_setting == self.TRIGGER_POLARITY:
                self.settings.toggle_trigger_polarity()

        elif self.current_category == self.CATEGORY_CV:
            if self.current_setting == self.CV_SCALE:
                self.settings.toggle_cv_scale()

    def _toggle_value(self):
        """Toggle current setting value (for discrete options)"""
        # For now, toggle is same as increase
        # This is used for discrete settings like trigger type
        self._increase_value()

    def get_display_text(self):
        """
        Get text to display for current menu state

        Returns:
            Tuple of (line1, line2, line3) strings for display
        """
        if self.current_level == self.LEVEL_CATEGORY:
            # Show category selection with current value
            category_name = self.category_names[self.current_category]

            # Add current value preview for each category
            if self.current_category == self.CATEGORY_ARP:
                preview = f"{self.settings.get_pattern_name()}/{self.settings.octave_range}oct"
                display_text = f"{category_name} ({preview})"
            elif self.current_category == self.CATEGORY_SCALE:
                preview = f"{self.settings.get_root_note_name()} {self.settings.get_scale_name()}"
                display_text = f"{category_name} ({preview})"
            elif self.current_category == self.CATEGORY_CLOCK:
                preview = f"{self.settings.get_clock_source_name()}/{self.settings.internal_bpm}"
                display_text = f"{category_name} ({preview})"
            elif self.current_category == self.CATEGORY_TRIGGERS:
                preview = f"{self.settings.get_trigger_polarity_name()}"
                display_text = f"{category_name} ({preview})"
            elif self.current_category == self.CATEGORY_CV:
                preview = f"{self.settings.get_cv_scale_name()}"
                display_text = f"{category_name} ({preview})"
            elif self.current_category == self.CATEGORY_FIRMWARE:
                # Import firmware version
                from settings import FIRMWARE_VERSION
                preview = f"v{FIRMWARE_VERSION}"
                display_text = f"{category_name} ({preview})"
            else:
                display_text = category_name

            return (
                "Settings Menu:",
                f"> {display_text} <",
                "A/C:Nav B:Select"
            )

        elif self.current_level == self.LEVEL_SETTING:
            # Show setting selection within category
            category_name = self.category_names[self.current_category]

            if self.current_category == self.CATEGORY_ARP:
                setting_name = self.arp_setting_names[self.current_setting]
            elif self.current_category == self.CATEGORY_SCALE:
                setting_name = self.scale_setting_names[self.current_setting]
            elif self.current_category == self.CATEGORY_CLOCK:
                setting_name = self.clock_setting_names[self.current_setting]
            elif self.current_category == self.CATEGORY_TRIGGERS:
                setting_name = self.trigger_setting_names[self.current_setting]
            elif self.current_category == self.CATEGORY_CV:
                setting_name = self.cv_setting_names[self.current_setting]
            elif self.current_category == self.CATEGORY_FIRMWARE:
                setting_name = self.firmware_setting_names[self.current_setting]
            else:
                setting_name = "Unknown"

            return (
                f"{category_name}:",
                f"> {setting_name} <",
                "A/C:Nav B:Select"
            )

        elif self.current_level == self.LEVEL_VALUE:
            # Show value adjustment
            if self.current_category == self.CATEGORY_ARP:
                if self.current_setting == self.ARP_PATTERN:
                    value = self.settings.get_pattern_name()
                    return (
                        "Arp Pattern:",
                        f"> {value} <",
                        "A/C:Change B:Done"
                    )
                elif self.current_setting == self.ARP_OCTAVES:
                    value = self.settings.octave_range
                    return (
                        "Octave Range:",
                        f"> {value} <",
                        "A/C:Adj B:Done"
                    )

            elif self.current_category == self.CATEGORY_SCALE:
                if self.current_setting == self.SCALE_TYPE:
                    value = self.settings.get_scale_name()
                    return (
                        "Scale Type:",
                        f"> {value} <",
                        "A/C:Change B:Done"
                    )
                elif self.current_setting == self.SCALE_ROOT:
                    value = self.settings.get_root_note_name()
                    return (
                        "Root Note:",
                        f"> {value} <",
                        "A/C:Change B:Done"
                    )

            elif self.current_category == self.CATEGORY_CLOCK:
                if self.current_setting == self.CLOCK_SOURCE:
                    value = self.settings.get_clock_source_name()
                    return (
                        "Clock Source:",
                        f"> {value} <",
                        "A/C:Toggle B:Done"
                    )
                elif self.current_setting == self.CLOCK_BPM:
                    return (
                        "BPM (Internal):",
                        f"> {self.settings.internal_bpm} <",
                        "A/C:Adj B:Done"
                    )

            elif self.current_category == self.CATEGORY_TRIGGERS:
                if self.current_setting == self.TRIGGER_POLARITY:
                    value = self.settings.get_trigger_polarity_name()
                    return (
                        "Trigger Polarity:",
                        f"> {value} <",
                        "A/C:Toggle B:Done"
                    )

            elif self.current_category == self.CATEGORY_CV:
                if self.current_setting == self.CV_SCALE:
                    value = self.settings.get_cv_scale_name()
                    return (
                        "CV Scale:",
                        f"> {value} <",
                        "A/C:Toggle B:Done"
                    )

            elif self.current_category == self.CATEGORY_FIRMWARE:
                if self.current_setting == self.FIRMWARE_INFO:
                    from settings import FIRMWARE_VERSION, FIRMWARE_DATE
                    return (
                        f"v{FIRMWARE_VERSION}",
                        f"{FIRMWARE_DATE}",
                        "B:Back"
                    )
                elif self.current_setting == self.FIRMWARE_UPDATE:
                    return (
                        "Update Firmware:",
                        "Connect to PC",
                        "See docs B:Back"
                    )

        return ("Settings", "Error", "")

    def get_current_category_name(self):
        """Get name of current category"""
        return self.category_names.get(self.current_category, "Unknown")

    def is_at_top_level(self):
        """Check if we're at the top level (category selection)"""
        return self.current_level == self.LEVEL_CATEGORY
