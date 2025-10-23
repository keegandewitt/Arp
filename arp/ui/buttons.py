"""
Button Handler for Adafruit FeatherWing OLED
Manages button input and debouncing for A, B, C buttons
"""

import time
import digitalio


class ButtonHandler:
    """Handles button input with debouncing"""

    def __init__(self, button_a_pin, button_b_pin, button_c_pin):
        """
        Initialize button handler

        Args:
            button_a_pin: Pin for button A
            button_b_pin: Pin for button B
            button_c_pin: Pin for button C
        """
        # Configure button A
        self.button_a = digitalio.DigitalInOut(button_a_pin)
        self.button_a.direction = digitalio.Direction.INPUT
        self.button_a.pull = digitalio.Pull.UP

        # Configure button B
        self.button_b = digitalio.DigitalInOut(button_b_pin)
        self.button_b.direction = digitalio.Direction.INPUT
        self.button_b.pull = digitalio.Pull.UP

        # Configure button C
        self.button_c = digitalio.DigitalInOut(button_c_pin)
        self.button_c.direction = digitalio.Direction.INPUT
        self.button_c.pull = digitalio.Pull.UP

        # Button state tracking
        self.last_a_state = True  # Pull-up means True when not pressed
        self.last_b_state = True
        self.last_c_state = True

        self.last_a_press_time = 0
        self.last_b_press_time = 0
        self.last_c_press_time = 0

        self.debounce_time = 0.05  # 50ms debounce
        self.long_press_time = 0.8  # 800ms for long press

        # Long press tracking
        self.a_press_start_time = None
        self.b_press_start_time = None
        self.a_long_press_triggered = False
        self.b_long_press_triggered = False

        # A+C combo long press tracking (for settings menu)
        self.ac_long_press_start_time = None
        self.ac_long_press_triggered = False

    def check_buttons(self):
        """
        Check button states and return which buttons were pressed

        Returns:
            Tuple of (a_pressed, b_pressed, c_pressed, ac_combo, a_long_press, b_long_press, ac_long_press) as booleans
            ac_combo is True if A and C are pressed simultaneously (short press)
            a_long_press is True if A is held for long press duration
            b_long_press is True if B is held for long press duration
            ac_long_press is True if A and C are held together for long press duration (for settings menu)
        """
        current_time = time.monotonic()
        a_pressed = False
        b_pressed = False
        c_pressed = False
        ac_combo = False
        a_long_press = False
        b_long_press = False
        ac_long_press = False

        # Read current states
        current_a = self.button_a.value
        current_b = self.button_b.value
        current_c = self.button_c.value

        # Check for A+C combo (both pressed) - this has two modes:
        # 1. Short press = ac_combo (existing behavior)
        # 2. Long press = ac_long_press (NEW - for settings menu)
        ac_combo_active = not current_a and not current_c

        if ac_combo_active:  # Both A and C are pressed
            # Track for long press detection
            if self.ac_long_press_start_time is None:
                # Just started pressing both
                self.ac_long_press_start_time = current_time
                self.ac_long_press_triggered = False
            elif not self.ac_long_press_triggered:
                # Check if held long enough for settings menu
                if current_time - self.ac_long_press_start_time >= self.long_press_time:
                    ac_long_press = True
                    self.ac_long_press_triggered = True

            # When A+C are both pressed, reset individual trackers to prevent conflicts
            self.a_press_start_time = None
            self.c_press_start_time = None
            self.a_long_press_triggered = False
        else:
            # A+C combo released
            self.ac_long_press_start_time = None
            self.ac_long_press_triggered = False

        # Track button A press start for long press detection (only if not in A+C combo)
        if not current_a and not ac_combo_active:  # Button A pressed alone
            if self.a_press_start_time is None:
                # Just started pressing
                self.a_press_start_time = current_time
                self.a_long_press_triggered = False
            elif not self.a_long_press_triggered:
                # Check if held long enough
                if current_time - self.a_press_start_time >= self.long_press_time:
                    a_long_press = True
                    self.a_long_press_triggered = True
        elif current_a or ac_combo_active:
            # Button A released or in combo
            self.a_press_start_time = None
            self.a_long_press_triggered = False

        # Track button B press start for long press detection
        if not current_b:  # Button B is pressed
            if self.b_press_start_time is None:
                # Just started pressing
                self.b_press_start_time = current_time
                self.b_long_press_triggered = False
            elif not self.b_long_press_triggered:
                # Check if held long enough
                if current_time - self.b_press_start_time >= self.long_press_time:
                    b_long_press = True
                    self.b_long_press_triggered = True
        else:
            # Button B released
            self.b_press_start_time = None
            self.b_long_press_triggered = False

        # Check for A+C short combo (both pressed simultaneously - existing behavior)
        # This is different from ac_long_press which is for settings menu
        if ac_combo_active:
            # Both buttons are currently pressed
            if self.last_a_state and self.last_c_state:
                # Both were released before, this is a new SHORT press (not long press)
                if current_time - max(self.last_a_press_time, self.last_c_press_time) > self.debounce_time:
                    if not ac_long_press:  # Only trigger short combo if long press hasn't fired
                        ac_combo = True
                        self.last_a_press_time = current_time
                        self.last_c_press_time = current_time

        # Check individual buttons only if not part of combo and not long press
        if not ac_combo and not a_long_press and not b_long_press and not ac_long_press:
            # Check button A (active low - pressed = False)
            if not current_a and self.last_a_state:  # Button just pressed
                if current_time - self.last_a_press_time > self.debounce_time:
                    a_pressed = True
                    self.last_a_press_time = current_time

            # Check button B
            if not current_b and self.last_b_state:  # Button just pressed
                if current_time - self.last_b_press_time > self.debounce_time:
                    b_pressed = True
                    self.last_b_press_time = current_time

            # Check button C
            if not current_c and self.last_c_state:  # Button just pressed
                if current_time - self.last_c_press_time > self.debounce_time:
                    c_pressed = True
                    self.last_c_press_time = current_time

        # Update last states
        self.last_a_state = current_a
        self.last_b_state = current_b
        self.last_c_state = current_c

        return (a_pressed, b_pressed, c_pressed, ac_combo, a_long_press, b_long_press, ac_long_press)

    def wait_for_release(self, button='all'):
        """
        Wait for button(s) to be released

        Args:
            button: 'a', 'b', 'c', or 'all' to wait for all buttons
        """
        if button == 'all':
            while not (self.button_a.value and self.button_b.value and self.button_c.value):
                time.sleep(0.01)
        elif button == 'a':
            while not self.button_a.value:
                time.sleep(0.01)
        elif button == 'b':
            while not self.button_b.value:
                time.sleep(0.01)
        elif button == 'c':
            while not self.button_c.value:
                time.sleep(0.01)


class PatternSelector:
    """Handles pattern selection UI logic"""

    def __init__(self, settings):
        """
        Initialize pattern selector

        Args:
            settings: Global settings object
        """
        self.settings = settings
        self.selection_active = False
        self.selected_pattern = self.settings.pattern

        # Pattern names for display
        self.pattern_names = {
            settings.ARP_UP: "Up",
            settings.ARP_DOWN: "Down",
            settings.ARP_UP_DOWN: "Up-Down",
            settings.ARP_DOWN_UP: "Down-Up",
            settings.ARP_RANDOM: "Random",
            settings.ARP_AS_PLAYED: "As Played"
        }

    def start_selection(self):
        """Start pattern selection mode"""
        self.selection_active = True
        self.selected_pattern = self.settings.pattern

    def next_pattern(self):
        """Move to next pattern in selection"""
        self.selected_pattern = (self.selected_pattern + 1) % 6

    def previous_pattern(self):
        """Move to previous pattern in selection"""
        self.selected_pattern = (self.selected_pattern - 1) % 6

    def confirm_selection(self):
        """Confirm and apply the selected pattern"""
        self.settings.pattern = self.selected_pattern
        self.selection_active = False

    def cancel_selection(self):
        """Cancel selection and revert"""
        self.selected_pattern = self.settings.pattern
        self.selection_active = False

    def get_selected_pattern_name(self):
        """Get the name of the currently selected pattern"""
        return self.pattern_names.get(self.selected_pattern, "Unknown")

    def get_current_pattern_name(self):
        """Get the name of the actual current pattern"""
        return self.pattern_names.get(self.settings.pattern, "Unknown")


class ClockSourceSelector:
    """Handles clock source selection UI logic"""

    def __init__(self, settings):
        """
        Initialize clock source selector

        Args:
            settings: Global settings object
        """
        self.settings = settings
        self.selection_active = False
        self.selected_source = self.settings.clock_source

    def start_selection(self):
        """Start clock source selection mode"""
        self.selection_active = True
        self.selected_source = self.settings.clock_source

    def toggle_source(self):
        """Toggle between internal and external"""
        if self.selected_source == self.settings.CLOCK_INTERNAL:
            self.selected_source = self.settings.CLOCK_EXTERNAL
        else:
            self.selected_source = self.settings.CLOCK_INTERNAL

    def confirm_selection(self):
        """Confirm and apply the selected clock source"""
        self.settings.clock_source = self.selected_source
        self.selection_active = False

    def cancel_selection(self):
        """Cancel selection and revert"""
        self.selected_source = self.settings.clock_source
        self.selection_active = False

    def get_selected_source_name(self):
        """Get the name of the currently selected source"""
        return "Internal" if self.selected_source == self.settings.CLOCK_INTERNAL else "External"

    def get_current_source_name(self):
        """Get the name of the actual current source"""
        return "Internal" if self.settings.clock_source == self.settings.CLOCK_INTERNAL else "External"
