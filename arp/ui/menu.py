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

    # Categories (ordered as they appear in menu)
    CATEGORY_CLOCK = 0      # Clock first - most commonly adjusted
    CATEGORY_TRANSLATION = 1  # Translation Hub settings
    CATEGORY_ARP = 2
    CATEGORY_SCALE = 3
    CATEGORY_TRIGGERS = 4
    CATEGORY_CV = 5
    CATEGORY_CUSTOM_CC = 6  # Custom CC output
    CATEGORY_FIRMWARE = 7

    # Arp settings
    ARP_PATTERN = 0       # Up, Down, Up-Down, etc.
    ARP_OCTAVES = 1       # Octave range (1-4)

    # Scale settings
    SCALE_TYPE = 0        # Scale type (Major, Minor, etc.)
    SCALE_ROOT = 1        # Root note (C, C#, D, etc.)

    # Translation settings
    TRANSLATION_ROUTING_MODE = 0  # THRU or TRANSLATION
    TRANSLATION_INPUT_SOURCE = 1  # MIDI IN or USB
    TRANSLATION_CLOCK_ENABLED = 2  # Clock layer enabled/disabled
    # NOTE: Layer order is fixed as Scale → Arp (no user config)

    # Clock settings (v3 unified controls)
    CLOCK_SOURCE = 0      # Internal or External
    CLOCK_BPM = 1         # BPM (only shown if Internal)
    CLOCK_RATE = 2        # Unified multiply/divide: /8 to 8x
    TIMING_FEEL = 3       # Unified swing/humanize: 50-100%

    # Trigger settings (only polarity now - always gate mode)
    TRIGGER_POLARITY = 0  # V-trig vs S-trig

    # CV settings
    CV_SCALE = 0  # 1V/octave vs 1.035V/octave (Moog)

    # Custom CC settings
    CUSTOM_CC_SOURCE = 0    # Source type (CC, Aftertouch, PitchBend, Velocity, Disabled)
    CUSTOM_CC_NUMBER = 1    # CC number (0-127, only shown if source is CC)
    CUSTOM_CC_SMOOTHING = 2 # Smoothing level (Off, Low, Mid, High)

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
        self.show_saved_confirmation = False  # Flag to show "Settings Saved!" message

        # Navigation state
        self.current_level = self.LEVEL_CATEGORY
        self.current_category = self.CATEGORY_ARP
        self.current_setting = 0

        # Category names (ordered by category constant)
        self.category_names = {
            self.CATEGORY_CLOCK: "Clock",
            self.CATEGORY_TRANSLATION: "Translation",
            self.CATEGORY_ARP: "Arp Mode",
            self.CATEGORY_SCALE: "Scale",
            self.CATEGORY_TRIGGERS: "Triggers",
            self.CATEGORY_CV: "CV",
            self.CATEGORY_CUSTOM_CC: "Custom CC",
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

        # Translation setting names
        self.translation_setting_names = {
            self.TRANSLATION_ROUTING_MODE: "Mode",
            self.TRANSLATION_INPUT_SOURCE: "Input",
            self.TRANSLATION_CLOCK_ENABLED: "Clock"
        }

        # Clock setting names (v3 unified controls)
        self.clock_setting_names = {
            self.CLOCK_SOURCE: "Source",
            self.CLOCK_BPM: "BPM",
            self.CLOCK_RATE: "Rate",
            self.TIMING_FEEL: "Feel"
        }

        # Trigger setting names
        self.trigger_setting_names = {
            self.TRIGGER_POLARITY: "Polarity"
        }

        # CV setting names
        self.cv_setting_names = {
            self.CV_SCALE: "Scale"
        }

        # Custom CC setting names
        self.custom_cc_setting_names = {
            self.CUSTOM_CC_SOURCE: "Source",
            self.CUSTOM_CC_NUMBER: "CC Number",
            self.CUSTOM_CC_SMOOTHING: "Smoothing"
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
        self.current_category = self.CATEGORY_CLOCK  # Start at Clock (now first)
        self.current_setting = 0

    def exit_menu(self):
        """Exit settings menu"""
        self.menu_active = False
        self.current_level = self.LEVEL_CATEGORY
        self.current_category = self.CATEGORY_CLOCK  # Reset to Clock (now first)
        self.current_setting = 0

    def navigate_previous(self):
        """Navigate to previous item at current level"""
        if self.current_level == self.LEVEL_CATEGORY:
            # Cycle through categories
            self.current_category = (self.current_category - 1) % 8  # 8 categories now

        elif self.current_level == self.LEVEL_SETTING:
            # Cycle through settings within category
            if self.current_category == self.CATEGORY_ARP:
                self.current_setting = (self.current_setting - 1) % 2
            elif self.current_category == self.CATEGORY_SCALE:
                self.current_setting = (self.current_setting - 1) % 2
            elif self.current_category == self.CATEGORY_TRANSLATION:
                self.current_setting = (self.current_setting - 1) % 3  # 3 settings (Mode, Input, Clock)
            elif self.current_category == self.CATEGORY_CLOCK:
                self.current_setting = (self.current_setting - 1) % 4  # 4 settings (v3: Source, BPM, Rate, Feel)
            elif self.current_category == self.CATEGORY_TRIGGERS:
                # Triggers only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_CV:
                # CV only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_CUSTOM_CC:
                self.current_setting = (self.current_setting - 1) % 3  # 3 settings
            elif self.current_category == self.CATEGORY_FIRMWARE:
                self.current_setting = (self.current_setting - 1) % 2

        elif self.current_level == self.LEVEL_VALUE:
            # Decrease value
            self._decrease_value()

    def navigate_next(self):
        """Navigate to next item at current level"""
        if self.current_level == self.LEVEL_CATEGORY:
            # Cycle through categories
            self.current_category = (self.current_category + 1) % 8  # 8 categories now

        elif self.current_level == self.LEVEL_SETTING:
            # Cycle through settings within category
            if self.current_category == self.CATEGORY_ARP:
                self.current_setting = (self.current_setting + 1) % 2
            elif self.current_category == self.CATEGORY_SCALE:
                self.current_setting = (self.current_setting + 1) % 2
            elif self.current_category == self.CATEGORY_TRANSLATION:
                self.current_setting = (self.current_setting + 1) % 3  # 3 settings (Mode, Input, Clock)
            elif self.current_category == self.CATEGORY_CLOCK:
                self.current_setting = (self.current_setting + 1) % 4  # 4 settings (v3: Source, BPM, Rate, Feel)
            elif self.current_category == self.CATEGORY_TRIGGERS:
                # Triggers only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_CV:
                # CV only has one setting, no cycle needed
                pass
            elif self.current_category == self.CATEGORY_CUSTOM_CC:
                self.current_setting = (self.current_setting + 1) % 3  # 3 settings
            elif self.current_category == self.CATEGORY_FIRMWARE:
                self.current_setting = (self.current_setting + 1) % 2

        elif self.current_level == self.LEVEL_VALUE:
            # Increase value
            self._increase_value()

    def select(self):
        """Select/enter current item (drill down or toggle)"""
        if self.current_level == self.LEVEL_CATEGORY:
            # Enter category
            if self.current_category == self.CATEGORY_TRIGGERS:
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
                # Clock, Translation, Arp, Scale, and Custom CC have multiple settings
                self.current_level = self.LEVEL_SETTING
                self.current_setting = 0

        elif self.current_level == self.LEVEL_SETTING:
            # Enter value adjustment
            self.current_level = self.LEVEL_VALUE

        elif self.current_level == self.LEVEL_VALUE:
            # B button at value level = confirm selection and exit to main screen
            self.exit_menu()
            # Set flag to show "Settings Saved!" confirmation
            self.show_saved_confirmation = True

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

        elif self.current_category == self.CATEGORY_TRANSLATION:
            if self.current_setting == self.TRANSLATION_ROUTING_MODE:
                # Toggle routing mode (THRU/TRANSLATION)
                self.settings.next_routing_mode()
            elif self.current_setting == self.TRANSLATION_INPUT_SOURCE:
                # Cycle input source (MIDI IN/USB/CV IN/GATE IN)
                self.settings.next_input_source()
            elif self.current_setting == self.TRANSLATION_CLOCK_ENABLED:
                # Toggle clock transformation layer (enabled/disabled)
                self.settings.clock_enabled = not self.settings.clock_enabled

        elif self.current_category == self.CATEGORY_CLOCK:
            if self.current_setting == self.CLOCK_SOURCE:
                # Cycle to next clock source
                self.settings.next_clock_source()
            elif self.current_setting == self.CLOCK_BPM:
                # Increase BPM by 1
                self.settings.internal_bpm = min(300, self.settings.internal_bpm + 1)
            elif self.current_setting == self.CLOCK_RATE:
                # Cycle unified clock rate: /8 -> /4 -> /2 -> 1x -> 2x -> 4x -> 8x -> /8
                self.settings.clock_rate = (self.settings.clock_rate + 1) % 7
            elif self.current_setting == self.TIMING_FEEL:
                # Increase timing feel (50-100%)
                self.settings.timing_feel = min(100, self.settings.timing_feel + 1)

        elif self.current_category == self.CATEGORY_TRIGGERS:
            if self.current_setting == self.TRIGGER_POLARITY:
                # Cycle to next trigger polarity
                self.settings.next_trigger_polarity()

        elif self.current_category == self.CATEGORY_CV:
            if self.current_setting == self.CV_SCALE:
                # Cycle to next CV scale
                self.settings.next_cv_scale()

        elif self.current_category == self.CATEGORY_CUSTOM_CC:
            if self.current_setting == self.CUSTOM_CC_SOURCE:
                # Cycle to next Custom CC source
                self.settings.next_custom_cc_source()
            elif self.current_setting == self.CUSTOM_CC_NUMBER:
                # Increase CC number (0-127)
                self.settings.custom_cc_number = (self.settings.custom_cc_number + 1) % 128
            elif self.current_setting == self.CUSTOM_CC_SMOOTHING:
                # Cycle to next smoothing level
                self.settings.next_custom_cc_smoothing()

        # Auto-save settings after change
        self.settings.save()

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

        elif self.current_category == self.CATEGORY_TRANSLATION:
            if self.current_setting == self.TRANSLATION_ROUTING_MODE:
                # Toggle routing mode (THRU/TRANSLATION)
                self.settings.previous_routing_mode()
            elif self.current_setting == self.TRANSLATION_INPUT_SOURCE:
                # Cycle input source (MIDI IN/USB/CV IN/GATE IN)
                self.settings.previous_input_source()
            elif self.current_setting == self.TRANSLATION_CLOCK_ENABLED:
                # Toggle clock transformation layer (enabled/disabled)
                self.settings.clock_enabled = not self.settings.clock_enabled

        elif self.current_category == self.CATEGORY_CLOCK:
            if self.current_setting == self.CLOCK_SOURCE:
                # Cycle to previous clock source
                self.settings.previous_clock_source()
            elif self.current_setting == self.CLOCK_BPM:
                # Decrease BPM by 1
                self.settings.internal_bpm = max(30, self.settings.internal_bpm - 1)
            elif self.current_setting == self.CLOCK_RATE:
                # Cycle unified clock rate backwards: /8 <- /4 <- /2 <- 1x <- 2x <- 4x <- 8x <- /8
                self.settings.clock_rate = (self.settings.clock_rate - 1) % 7
            elif self.current_setting == self.TIMING_FEEL:
                # Decrease timing feel (50-100%)
                self.settings.timing_feel = max(50, self.settings.timing_feel - 1)

        elif self.current_category == self.CATEGORY_TRIGGERS:
            if self.current_setting == self.TRIGGER_POLARITY:
                # Cycle to previous trigger polarity
                self.settings.previous_trigger_polarity()

        elif self.current_category == self.CATEGORY_CV:
            if self.current_setting == self.CV_SCALE:
                # Cycle to previous CV scale
                self.settings.previous_cv_scale()

        elif self.current_category == self.CATEGORY_CUSTOM_CC:
            if self.current_setting == self.CUSTOM_CC_SOURCE:
                # Cycle to previous Custom CC source
                self.settings.previous_custom_cc_source()
            elif self.current_setting == self.CUSTOM_CC_NUMBER:
                # Decrease CC number (0-127)
                self.settings.custom_cc_number = (self.settings.custom_cc_number - 1) % 128
            elif self.current_setting == self.CUSTOM_CC_SMOOTHING:
                # Cycle to previous smoothing level
                self.settings.previous_custom_cc_smoothing()

        # Auto-save settings after change
        self.settings.save()

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
            # Show TWO categories: current (selected) and next
            # Helper function to get category display text with preview
            def get_category_text(cat_index):
                cat_name = self.category_names[cat_index]
                if cat_index == self.CATEGORY_ARP:
                    preview = f"{self.settings.get_pattern_name()}/{self.settings.octave_range}oct"
                    return f"{cat_name} ({preview})"
                elif cat_index == self.CATEGORY_SCALE:
                    preview = f"{self.settings.get_root_note_name()} {self.settings.get_scale_name()}"
                    return f"{cat_name} ({preview})"
                elif cat_index == self.CATEGORY_TRANSLATION:
                    preview = f"{self.settings.get_routing_mode_name()}"
                    return f"{cat_name} ({preview})"
                elif cat_index == self.CATEGORY_CLOCK:
                    preview = f"{self.settings.get_clock_source_name()}/{self.settings.internal_bpm}"
                    return f"{cat_name} ({preview})"
                elif cat_index == self.CATEGORY_TRIGGERS:
                    preview = f"{self.settings.get_trigger_polarity_name()}"
                    return f"{cat_name} ({preview})"
                elif cat_index == self.CATEGORY_CV:
                    preview = f"{self.settings.get_cv_scale_name()}"
                    return f"{cat_name} ({preview})"
                elif cat_index == self.CATEGORY_CUSTOM_CC:
                    preview = f"{self.settings.get_custom_cc_source_name()}"
                    return f"{cat_name} ({preview})"
                elif cat_index == self.CATEGORY_FIRMWARE:
                    from arp.utils.config import FIRMWARE_VERSION
                    preview = f"v{FIRMWARE_VERSION}"
                    return f"{cat_name} ({preview})"
                else:
                    return cat_name

            # Current category (selected)
            current_text = get_category_text(self.current_category)

            # Next category (preview)
            next_category = (self.current_category + 1) % 8  # 8 categories now
            next_text = get_category_text(next_category)

            return (
                "Settings:",
                f"> {current_text}",
                f"  {next_text}"
            )

        elif self.current_level == self.LEVEL_SETTING:
            # Show TWO settings: current (selected) and next within category
            category_name = self.category_names[self.current_category]

            # Helper to get setting name by index (with current value preview)
            def get_setting_name(idx):
                if self.current_category == self.CATEGORY_ARP:
                    return self.arp_setting_names.get(idx, "")
                elif self.current_category == self.CATEGORY_SCALE:
                    return self.scale_setting_names.get(idx, "")
                elif self.current_category == self.CATEGORY_TRANSLATION:
                    return self.translation_setting_names.get(idx, "")
                elif self.current_category == self.CATEGORY_CLOCK:
                    # Add current value preview for Clock settings (v3 unified controls)
                    setting_name = self.clock_setting_names.get(idx, "")
                    if idx == self.CLOCK_SOURCE:
                        return f"{setting_name} ({self.settings.get_clock_source_name()})"
                    elif idx == self.CLOCK_BPM:
                        return f"{setting_name} ({self.settings.internal_bpm})"
                    elif idx == self.CLOCK_RATE:
                        # Show unified clock rate
                        rate_name = self.settings.get_clock_rate_name()
                        return f"{setting_name} ({rate_name})"
                    elif idx == self.TIMING_FEEL:
                        # Show timing feel percentage
                        return f"{setting_name} ({self.settings.timing_feel}%)"
                    return setting_name
                elif self.current_category == self.CATEGORY_TRIGGERS:
                    return self.trigger_setting_names.get(idx, "")
                elif self.current_category == self.CATEGORY_CV:
                    return self.cv_setting_names.get(idx, "")
                elif self.current_category == self.CATEGORY_CUSTOM_CC:
                    return self.custom_cc_setting_names.get(idx, "")
                elif self.current_category == self.CATEGORY_FIRMWARE:
                    return self.firmware_setting_names.get(idx, "")
                else:
                    return "Unknown"

            # Get number of settings in this category
            if self.current_category == self.CATEGORY_ARP:
                num_settings = 2
            elif self.current_category == self.CATEGORY_SCALE:
                num_settings = 2
            elif self.current_category == self.CATEGORY_TRANSLATION:
                num_settings = 3  # Mode, Input, Clock
            elif self.current_category == self.CATEGORY_CLOCK:
                num_settings = 4  # Source, BPM, Rate, Feel (v3 unified)
            elif self.current_category == self.CATEGORY_CUSTOM_CC:
                num_settings = 3  # Source, CC Number, Smoothing
            elif self.current_category == self.CATEGORY_FIRMWARE:
                num_settings = 2
            else:
                num_settings = 1  # Triggers, CV only have 1 setting

            # Current setting
            current_setting_name = get_setting_name(self.current_setting)

            # Next setting (if exists)
            if num_settings > 1:
                next_setting = (self.current_setting + 1) % num_settings
                next_setting_name = get_setting_name(next_setting)
            else:
                next_setting_name = ""

            return (
                f"{category_name}:",
                f"> {current_setting_name}",
                f"  {next_setting_name}" if next_setting_name else ""
            )

        elif self.current_level == self.LEVEL_VALUE:
            # Show value adjustment
            if self.current_category == self.CATEGORY_ARP:
                if self.current_setting == self.ARP_PATTERN:
                    value = self.settings.get_pattern_name()
                    return (
                        "Arp Pattern:",
                        f"> {value} <",
                        ""
                    )
                elif self.current_setting == self.ARP_OCTAVES:
                    value = self.settings.octave_range
                    return (
                        "Octave Range:",
                        f"> {value} <",
                        ""
                    )

            elif self.current_category == self.CATEGORY_SCALE:
                if self.current_setting == self.SCALE_TYPE:
                    value = self.settings.get_scale_name()
                    return (
                        "Scale Type:",
                        f"> {value} <",
                        ""
                    )
                elif self.current_setting == self.SCALE_ROOT:
                    value = self.settings.get_root_note_name()
                    return (
                        "Root Note:",
                        f"> {value} <",
                        ""
                    )

            elif self.current_category == self.CATEGORY_TRANSLATION:
                if self.current_setting == self.TRANSLATION_ROUTING_MODE:
                    # Show both options with current selected
                    if self.settings.routing_mode == self.settings.ROUTING_THRU:
                        return (
                            "Routing Mode:",
                            "> THRU",
                            "  TRANSLATION"
                        )
                    else:
                        return (
                            "Routing Mode:",
                            "  THRU",
                            "> TRANSLATION"
                        )
                elif self.current_setting == self.TRANSLATION_INPUT_SOURCE:
                    value = self.settings.get_input_source_name()
                    return (
                        "Input Source:",
                        f"> {value} <",
                        ""
                    )
                elif self.current_setting == self.TRANSLATION_CLOCK_ENABLED:
                    # Show both options with current selected
                    if self.settings.clock_enabled:
                        return (
                            "Clock Layer:",
                            "> Enabled",
                            "  Disabled"
                        )
                    else:
                        return (
                            "Clock Layer:",
                            "  Enabled",
                            "> Disabled"
                        )

            elif self.current_category == self.CATEGORY_CLOCK:
                if self.current_setting == self.CLOCK_SOURCE:
                    # Show both options with current selected
                    if self.settings.clock_source == self.settings.CLOCK_INTERNAL:
                        return (
                            "Clock Source:",
                            "> Internal",
                            "  External"
                        )
                    else:
                        return (
                            "Clock Source:",
                            "  Internal",
                            "> External"
                        )
                elif self.current_setting == self.CLOCK_BPM:
                    return (
                        "BPM (Internal):",
                        f"> {self.settings.internal_bpm} <",
                        ""
                    )
                elif self.current_setting == self.CLOCK_RATE:
                    # Show unified clock rate name
                    rate_name = self.settings.get_clock_rate_name()
                    return (
                        "Clock Rate:",
                        f"> {rate_name} <",
                        "/8 /4 /2 1x 2x 4x 8x"
                    )
                elif self.current_setting == self.TIMING_FEEL:
                    # Show timing feel with descriptive text
                    feel_text = ""
                    if self.settings.timing_feel == 50:
                        feel_text = " (Robot)"
                    elif self.settings.timing_feel <= 66:
                        feel_text = " (Swing)"
                    else:
                        feel_text = " (Humanize)"
                    return (
                        "Timing Feel:",
                        f"> {self.settings.timing_feel}%{feel_text} <",
                        "50=Robot 66=Swing 85=Humanize"
                    )

            elif self.current_category == self.CATEGORY_TRIGGERS:
                if self.current_setting == self.TRIGGER_POLARITY:
                    # Show both options with current selected
                    if self.settings.trigger_polarity == self.settings.TRIGGER_VTRIG:
                        return (
                            "Trigger Polarity:",
                            "> V-trig",
                            "  S-trig"
                        )
                    else:
                        return (
                            "Trigger Polarity:",
                            "  V-trig",
                            "> S-trig"
                        )

            elif self.current_category == self.CATEGORY_CV:
                if self.current_setting == self.CV_SCALE:
                    # Show both options with current selected
                    if self.settings.cv_scale == self.settings.CV_SCALE_STANDARD:
                        return (
                            "CV Scale:",
                            "> 1V/octave",
                            "  Moog (1.035V)"
                        )
                    else:
                        return (
                            "CV Scale:",
                            "  1V/octave",
                            "> Moog (1.035V)"
                        )

            elif self.current_category == self.CATEGORY_CUSTOM_CC:
                if self.current_setting == self.CUSTOM_CC_SOURCE:
                    value = self.settings.get_custom_cc_source_name()
                    return (
                        "Custom CC Source:",
                        f"> {value} <",
                        ""
                    )
                elif self.current_setting == self.CUSTOM_CC_NUMBER:
                    # Show CC number with name (if source is CC)
                    if self.settings.custom_cc_source == self.settings.CC_SOURCE_CC:
                        try:
                            from arp.data.midi_cc_names import get_cc_short_name
                            cc_name = get_cc_short_name(self.settings.custom_cc_number)
                            return (
                                "CC Number:",
                                f"> {cc_name} <",
                                ""
                            )
                        except:
                            # Fallback if midi_cc_names not found
                            return (
                                "CC Number:",
                                f"> CC {self.settings.custom_cc_number} <",
                                ""
                            )
                    else:
                        # Not in CC mode - show disabled message
                        return (
                            "CC Number:",
                            "(N/A - not in CC mode)",
                            ""
                        )
                elif self.current_setting == self.CUSTOM_CC_SMOOTHING:
                    value = self.settings.get_custom_cc_smoothing_name()
                    return (
                        "Smoothing:",
                        f"> {value} <",
                        ""
                    )

            elif self.current_category == self.CATEGORY_FIRMWARE:
                if self.current_setting == self.FIRMWARE_INFO:
                    from arp.utils.config import FIRMWARE_VERSION, FIRMWARE_DATE
                    return (
                        f"v{FIRMWARE_VERSION}",
                        f"{FIRMWARE_DATE}",
                        ""
                    )
                elif self.current_setting == self.FIRMWARE_UPDATE:
                    return (
                        "Update Firmware:",
                        "Connect to PC",
                        ""
                    )

        return ("Settings", "Error", "")

    def get_current_category_name(self):
        """Get name of current category"""
        return self.category_names.get(self.current_category, "Unknown")

    def is_at_top_level(self):
        """Check if we're at the top level (category selection)"""
        return self.current_level == self.LEVEL_CATEGORY
