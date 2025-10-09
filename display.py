"""
OLED Display Handler for Adafruit FeatherWing OLED
Manages display output and user interface
"""

import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306


class Display:
    """Handles OLED display and UI rendering"""

    def __init__(self, i2c):
        """
        Initialize the OLED display

        Args:
            i2c: I2C bus object
        """
        # Release any existing displays
        displayio.release_displays()

        # Create display bus
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

        # Create display (128x32 for FeatherWing OLED)
        self.display = adafruit_displayio_ssd1306.SSD1306(
            display_bus,
            width=128,
            height=32
        )

        # Set optimal brightness for readability and power efficiency
        # Range: 0.0 (off) to 1.0 (max brightness)
        # 0.5 = good balance: readable in most conditions, saves ~25% power vs full brightness
        # Lower values save more power but reduce readability in bright environments
        self.display.brightness = 0.5

        # Create display group
        self.group = displayio.Group()

        # MIDI activity indicators (top corners)
        # Top left: MIDI IN indicator (downward arrow)
        self.midi_in_label = label.Label(
            terminalio.FONT,
            text=" ",  # Space when inactive, "v" when active
            color=0xFFFFFF,
            x=0,
            y=0
        )

        # Top right: MIDI OUT indicator (upward arrow)
        self.midi_out_label = label.Label(
            terminalio.FONT,
            text=" ",  # Space when inactive, "^" when active
            color=0xFFFFFF,
            x=122,  # Right side of 128px display
            y=0
        )

        # Create text labels
        # Line 1: BPM
        self.bpm_label = label.Label(
            terminalio.FONT,
            text="BPM: ---",
            color=0xFFFFFF,
            x=0,
            y=10  # Moved down to make room for indicators
        )

        # Line 2: Pattern (current)
        self.pattern_label = label.Label(
            terminalio.FONT,
            text="Pattern: Up",
            color=0xFFFFFF,
            x=0,
            y=20  # Moved down
        )

        # Line 3: Status/Selection indicator
        self.status_label = label.Label(
            terminalio.FONT,
            text="",
            color=0xFFFFFF,
            x=0,
            y=30  # Moved down
        )

        # Add labels to group
        self.group.append(self.midi_in_label)
        self.group.append(self.midi_out_label)
        self.group.append(self.bpm_label)
        self.group.append(self.pattern_label)
        self.group.append(self.status_label)

        # Show the group
        self.display.root_group = self.group

        # UI state
        self.selection_mode = False
        self.clock_source_selection_mode = False
        self.selected_pattern = None

        # Sleep state
        self.is_sleeping = False
        self.sleep_timeout = 15.0  # seconds
        self.last_activity_time = None

        # MIDI activity indicators
        self.midi_in_active = False
        self.midi_out_active = False

        # Brightness control
        self.brightness_level = 0.5  # Default brightness (0.0-1.0)

    def update_bpm(self, bpm, clock_source_short=""):
        """
        Update the BPM display

        Args:
            bpm: Current BPM value (float or int)
            clock_source_short: Short indicator like "(Int)" or "(Ext)"
        """
        if self.is_sleeping:
            return
        if bpm is None or bpm <= 0:
            self.bpm_label.text = f"BPM: --- {clock_source_short}"
        else:
            self.bpm_label.text = f"BPM: {int(bpm)} {clock_source_short}"

    def update_pattern(self, pattern_name):
        """
        Update the current pattern display

        Args:
            pattern_name: Name of the current pattern
        """
        if self.is_sleeping:
            return
        if self.selection_mode:
            # In selection mode, show the selected pattern differently
            self.pattern_label.text = f"> {pattern_name} <"
        else:
            self.pattern_label.text = f"Pattern: {pattern_name}"

    def enter_selection_mode(self, pattern_name):
        """
        Enter pattern selection mode (wakes display)

        Args:
            pattern_name: Initial pattern name
        """
        if self.is_sleeping:
            self.wake()
        self.selection_mode = True
        self.selected_pattern = pattern_name
        self.update_pattern(pattern_name)
        self.status_label.text = "A/C:Chg B:Confirm"

    def exit_selection_mode(self, confirmed=False):
        """
        Exit pattern selection mode

        Args:
            confirmed: True if selection was confirmed, False if cancelled
        """
        if self.is_sleeping:
            return
        self.selection_mode = False
        if confirmed:
            self.show_message("Pattern Set!", duration=1.0)
        self.status_label.text = ""

    def show_message(self, message, duration=2.0):
        """
        Show a temporary message on the status line

        Args:
            message: Message to display
            duration: How long to show (not implemented - would need timer)
        """
        if self.is_sleeping:
            return
        self.status_label.text = message

    def clear_status(self):
        """Clear the status line"""
        if self.is_sleeping or self.selection_mode:
            return
        self.status_label.text = ""

    def show_startup(self):
        """Show startup screen"""
        if self.is_sleeping:
            return
        self.bpm_label.text = "MIDI"
        self.pattern_label.text = "Arpeggiator"
        self.status_label.text = "Ready!"

    def enter_clock_source_selection(self, clock_source_name):
        """
        Enter clock source selection mode (wakes display)

        Args:
            clock_source_name: "Internal" or "External"
        """
        if self.is_sleeping:
            self.wake()
        self.clock_source_selection_mode = True
        self.bpm_label.text = "Clock Source:"
        self.pattern_label.text = f"> {clock_source_name} <"
        self.status_label.text = "A/C:Chg B:Confirm"

    def update_clock_source_selection(self, clock_source_name):
        """
        Update the clock source selection display

        Args:
            clock_source_name: "Internal" or "External"
        """
        if self.is_sleeping:
            return
        if self.clock_source_selection_mode:
            self.pattern_label.text = f"> {clock_source_name} <"

    def exit_clock_source_selection(self, confirmed=False):
        """
        Exit clock source selection mode

        Args:
            confirmed: True if selection was confirmed
        """
        if self.is_sleeping:
            return
        self.clock_source_selection_mode = False
        if confirmed:
            self.show_message("Clock Set!", duration=1.0)

    def sleep(self):
        """Put display to sleep (turns off display)"""
        if not self.is_sleeping:
            self.display.sleep = True
            self.is_sleeping = True

    def wake(self):
        """Wake display from sleep"""
        if self.is_sleeping:
            self.display.sleep = False
            self.is_sleeping = False

    def record_activity(self, current_time):
        """
        Record user activity timestamp

        Args:
            current_time: Current monotonic time
        """
        self.last_activity_time = current_time
        # Wake display on any activity
        if self.is_sleeping:
            self.wake()

    def check_sleep(self, current_time):
        """
        Check if display should sleep due to inactivity

        Args:
            current_time: Current monotonic time

        Returns:
            True if display went to sleep, False otherwise
        """
        # Don't sleep if in selection mode
        if self.selection_mode or self.clock_source_selection_mode:
            return False

        # Initialize on first check
        if self.last_activity_time is None:
            self.last_activity_time = current_time
            return False

        # Check timeout
        if not self.is_sleeping:
            elapsed = current_time - self.last_activity_time
            if elapsed >= self.sleep_timeout:
                self.sleep()
                return True

        return False

    def set_midi_in_active(self, active):
        """
        Set MIDI IN indicator state

        Args:
            active: True to show activity, False to hide
        """
        if self.is_sleeping:
            return
        self.midi_in_active = active
        self.midi_in_label.text = "v" if active else " "

    def set_midi_out_active(self, active):
        """
        Set MIDI OUT indicator state

        Args:
            active: True to show activity, False to hide
        """
        if self.is_sleeping:
            return
        self.midi_out_active = active
        self.midi_out_label.text = "^" if active else " "

    def update_midi_indicators(self, has_midi_in, has_midi_out):
        """
        Update MIDI activity indicators

        Args:
            has_midi_in: True if MIDI IN activity detected
            has_midi_out: True if MIDI OUT activity detected
        """
        if self.is_sleeping:
            return
        self.set_midi_in_active(has_midi_in)
        self.set_midi_out_active(has_midi_out)

    def set_brightness(self, brightness):
        """
        Set display brightness level

        Args:
            brightness: Brightness level (0.0 to 1.0)
                       0.0 = minimum (off), 1.0 = maximum
                       0.3 = low (max power saving, ~50% power reduction)
                       0.5 = medium (good balance, ~25% power reduction) - DEFAULT
                       0.7 = high (bright, ~10% power reduction)
                       1.0 = maximum (full brightness, no power saving)
        """
        self.brightness_level = max(0.0, min(1.0, brightness))
        self.display.brightness = self.brightness_level

    def get_brightness(self):
        """
        Get current brightness level

        Returns:
            Current brightness (0.0 to 1.0)
        """
        return self.brightness_level

    def update_display(self, bpm, pattern_name, clock_running, clock_source_short=""):
        """
        Update the entire display (only if awake)

        Args:
            bpm: Current BPM
            pattern_name: Current pattern name
            clock_running: Whether clock is running
            clock_source_short: Short indicator like "(Int)" or "(Ext)"
        """
        # Skip updates if display is sleeping
        if self.is_sleeping:
            return

        if not self.selection_mode and not self.clock_source_selection_mode:
            self.update_bpm(bpm, clock_source_short)
            self.update_pattern(pattern_name)

            # Show clock status if not running (external only)
            if not clock_running and self.status_label.text == "":
                self.status_label.text = "No Clock"
            elif clock_running and self.status_label.text == "No Clock":
                self.status_label.text = ""
