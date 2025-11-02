"""
OLED Display Handler for Adafruit FeatherWing OLED
Manages display output and user interface

Required CircuitPython Libraries:
- adafruit_displayio_sh1107 (install via: circup install adafruit_displayio_sh1107)
- adafruit_display_text (install via: circup install adafruit_display_text)

Built-in Dependencies:
- displayio, terminalio, i2cdisplaybus (CircuitPython 10.x+)

IMPORTANT: OLED FeatherWing 128x64 (Product #4650) uses SH1107 driver, NOT SSD1306!
The older 128x32 FeatherWing uses SSD1306, but the 128x64 uses a different chip.
"""

import displayio
import terminalio
import i2cdisplaybus  # New in CircuitPython 10.x
from adafruit_display_text import label
import adafruit_displayio_sh1107


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

        # Create display bus using CircuitPython 10.x API
        # NOTE: CP 10.x uses i2cdisplaybus.I2CDisplayBus (NOT displayio.I2CDisplay)
        display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

        # Create display (128x64 for Adafruit OLED FeatherWing #4650)
        # Hardware: Adafruit OLED FeatherWing 128x64 (Product ID: 4650)
        # CRITICAL: This uses SH1107 driver, NOT SSD1306!
        self.display = adafruit_displayio_sh1107.SH1107(
            display_bus,
            width=128,
            height=64
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

        # Create text labels for new 3-line Translation Hub display
        # Line 1: MODE and INPUT SOURCE
        self.line1_label = label.Label(
            terminalio.FONT,
            text="MODE: XLAT  IN: MIDI",
            color=0xFFFFFF,
            x=0,
            y=20
        )

        # Line 2: CLOCK SOURCE, BPM, and modifiers
        self.line2_label = label.Label(
            terminalio.FONT,
            text="CLK SRC: Int  BPM: 120",
            color=0xFFFFFF,
            x=0,
            y=35
        )

        # Line 3: TRANSLATION active layers
        self.line3_label = label.Label(
            terminalio.FONT,
            text="XLAT: Scale -> Arp - Clock",
            color=0xFFFFFF,
            x=0,
            y=50
        )

        # Legacy labels (for backward compatibility with old display methods)
        self.bpm_label = self.line2_label  # Alias for old code
        self.pattern_label = self.line3_label  # Alias for old code
        self.status_label = self.line3_label  # Alias for old code

        # Add labels to group
        self.group.append(self.midi_in_label)
        self.group.append(self.midi_out_label)
        self.group.append(self.line1_label)
        self.group.append(self.line2_label)
        self.group.append(self.line3_label)

        # Show the group
        self.display.root_group = self.group

        # UI state
        self.selection_mode = False
        self.clock_source_selection_mode = False
        self.settings_menu_mode = False
        self.selected_pattern = None

        # Sleep state
        self.is_sleeping = False
        self.sleep_timeout = 15.0  # seconds
        self.last_activity_time = None

        # Status message timing
        self.status_message = None
        self.status_end_time = None

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

    def show_startup(self, version="0.95.0"):
        """
        Show startup screen with version info

        Args:
            version: Firmware version string
        """
        if self.is_sleeping:
            return
        self.bpm_label.text = "MIDI Arpeggiator"
        self.pattern_label.text = f"v{version}"
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

    def enter_settings_menu(self, line1, line2, line3):
        """
        Enter settings menu mode (wakes display)

        Args:
            line1, line2, line3: Text for each display line
        """
        if self.is_sleeping:
            self.wake()
        self.settings_menu_mode = True
        self.bpm_label.text = line1
        self.pattern_label.text = line2
        self.status_label.text = line3

    def update_settings_menu(self, line1, line2, line3):
        """
        Update settings menu display

        Args:
            line1, line2, line3: Text for each display line
        """
        if self.is_sleeping:
            return
        if self.settings_menu_mode:
            self.bpm_label.text = line1
            self.pattern_label.text = line2
            self.status_label.text = line3

    def exit_settings_menu(self):
        """Exit settings menu mode"""
        if self.is_sleeping:
            return
        self.settings_menu_mode = False
        self.status_label.text = ""

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
        # Don't sleep if in any menu mode
        if self.selection_mode or self.clock_source_selection_mode or self.settings_menu_mode:
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

        # Skip updates if in any menu mode
        if not self.selection_mode and not self.clock_source_selection_mode and not self.settings_menu_mode:
            self.update_bpm(bpm, clock_source_short)
            self.update_pattern(pattern_name)

            # Check for timed status message
            import time
            current_time = time.monotonic()
            if self.status_end_time and current_time >= self.status_end_time:
                # Status message expired, clear it
                self.status_label.text = ""
                self.status_message = None
                self.status_end_time = None

            # Show status message if active
            if self.status_message:
                self.status_label.text = self.status_message
            # Otherwise show clock status if not running (external only)
            elif not clock_running:
                self.status_label.text = "No Clock"
            elif clock_running and self.status_label.text == "No Clock":
                self.status_label.text = ""

    def show_status(self, message, duration_seconds=2.0):
        """
        Show a temporary status message on line 3

        Args:
            message: The message to show
            duration_seconds: How long to show it (default 2 seconds)
        """
        import time
        self.status_message = message
        self.status_end_time = time.monotonic() + duration_seconds
        self.status_label.text = message

    def update_translation_display(self, settings, clock_running=True):
        """
        Update the main display with Translation Hub info (ASCII icon-based)

        New compact format (v3):
        Line 1: *120 P:Up S:Maj  >MIDI
        Line 2: x2 ~66 .80%  [XLAT]

        Icons: * = clock running, o = stopped
               > = input arrow
               x = multiply
               ~ = timing feel (tilde suggests variation)
               . = likelihood dot

        Args:
            settings: Settings object with all current values
            clock_running: Whether clock is currently running (default True)
        """
        # Skip updates if display is sleeping or in menu
        if self.is_sleeping or self.settings_menu_mode:
            return

        # Line 1: Clock status + BPM + Pattern + Scale + Input
        # Format: *120 P:Up S:Maj  >MIDI
        clock_icon = "*" if clock_running else "o"

        # BPM
        if settings.clock_source == settings.CLOCK_INTERNAL:
            bpm_text = str(settings.internal_bpm)
        else:
            bpm_text = "---"

        # Pattern (only if arp enabled)
        if settings.is_arp_enabled():
            pattern_short = self._get_pattern_short_name(settings.pattern)
            pattern_text = f" P:{pattern_short}"
        else:
            pattern_text = ""

        # Scale (only if enabled, skip if Chromatic)
        if settings.is_scale_enabled():
            scale_short = self._get_scale_short_name(settings.scale_type)
            scale_text = f" S:{scale_short}"
        else:
            scale_text = ""

        # Input source with arrow
        input_short = self._format_input_source(settings.input_source)
        input_text = f" >{input_short}"

        self.line1_label.text = f"{clock_icon}{bpm_text}{pattern_text}{scale_text} {input_text}"

        # Line 2: Clock rate + Timing Feel + Likelihood + Mode badge
        # Format: x2 ~66 .80%  [XLAT]
        parts = []

        # Clock rate (only if not 1x)
        clock_rate_text = self._format_clock_rate(settings)
        if clock_rate_text:
            parts.append(clock_rate_text)

        # Timing Feel (only if not 50% = robot)
        timing_text = self._format_timing_feel(settings)
        if timing_text:
            parts.append(timing_text)

        # Likelihood (only if not 100% = all notes)
        if hasattr(settings, 'likelihood') and settings.likelihood < 100:
            parts.append(f".{settings.likelihood}%")

        # Mode badge
        mode_badge = "[THRU]" if settings.routing_mode == settings.ROUTING_THRU else "[XLAT]"

        # Combine parts
        if parts:
            self.line2_label.text = f"{' '.join(parts)}  {mode_badge}"
        else:
            self.line2_label.text = mode_badge

        # Line 3: Translation layer flow (simplified)
        if settings.routing_mode == settings.ROUTING_TRANSLATION:
            flow_text = self._format_layer_flow(settings)
            self.line3_label.text = flow_text
        else:
            # THRU mode: simple indicator
            self.line3_label.text = "Pass-through mode"

    def _format_clock_rate(self, settings):
        """Format clock rate for compact display

        Returns empty string if 1x (no transformation)
        Examples: x2, x4, /2, /4
        """
        # Use new unified clock_rate if available
        if hasattr(settings, 'clock_rate'):
            rate_map = {
                0: "/8",   # CLOCK_RATE_DIV_8
                1: "/4",   # CLOCK_RATE_DIV_4
                2: "/2",   # CLOCK_RATE_DIV_2
                3: "",     # CLOCK_RATE_1X (no display)
                4: "x2",   # CLOCK_RATE_2X
                5: "x4",   # CLOCK_RATE_4X
                6: "x8",   # CLOCK_RATE_8X
            }
            return rate_map.get(settings.clock_rate, "")

        # Fallback to old multiply/divide settings
        if settings.clock_multiply > 1:
            return f"x{settings.clock_multiply}"
        elif settings.clock_divide > 1:
            return f"/{settings.clock_divide}"
        return ""

    def _format_timing_feel(self, settings):
        """Format timing feel for compact display

        Returns empty string if 50% (robot mode)
        Examples: ~66 (swing), ~85 (humanize)
        """
        # Use new unified timing_feel if available
        if hasattr(settings, 'timing_feel'):
            if settings.timing_feel != 50:
                return f"~{settings.timing_feel}"
            return ""

        # Fallback to old swing_percent
        if hasattr(settings, 'swing_percent') and settings.swing_percent != 50:
            return f"~{settings.swing_percent}"
        return ""

    def _format_layer_flow(self, settings):
        """Format layer processing flow for line 3 (simplified)

        Shows active layers with arrows: MIDI>Scale>Arp>CV
        Only shows enabled layers
        """
        flow = ["MIDI"]

        # Add Scale if enabled
        if settings.is_scale_enabled():
            flow.append("Scale")

        # Add Arp if enabled
        if settings.is_arp_enabled():
            flow.append("Arp")

        # Output (CV or MIDI based on routing)
        flow.append("CV")

        return ">".join(flow)

    def _format_input_source(self, input_source):
        """Format input source for display (short)"""
        if input_source == 0:  # INPUT_SOURCE_MIDI_IN
            return "MIDI"
        elif input_source == 1:  # INPUT_SOURCE_USB
            return "USB"
        elif input_source == 2:  # INPUT_SOURCE_CV_IN
            return "CV"
        elif input_source == 3:  # INPUT_SOURCE_GATE_IN
            return "GATE"
        return "?"

    def _format_clock_modifiers(self, settings):
        """Format clock modifiers for display (compact)"""
        modifiers = []

        # Only show modifiers if clock transformations are enabled
        if not settings.clock_enabled:
            return ""

        # Swing (only if not 50%)
        if settings.swing_percent != 50:
            modifiers.append(f"sw:{settings.swing_percent}%")

        # Multiply (only if not 1x)
        if settings.clock_multiply != 1:
            modifiers.append(f"x{settings.clock_multiply}")

        # Divide (only if not /1)
        if settings.clock_divide != 1:
            modifiers.append(f"/{settings.clock_divide}")

        if modifiers:
            return " (" + " ".join(modifiers) + ")"
        return ""

    def _format_active_layers(self, settings):
        """Format active translation layers with values

        Format: Scale(Maj) -> Arp(Up) - Clk(Int)
        Only shows enabled layers
        """
        layers = []

        # Scale layer (if enabled)
        if settings.scale_enabled:
            scale_short = self._get_scale_short_name(settings.scale_type)
            layers.append(f"Scale({scale_short})")

        # Arp layer (if enabled)
        if settings.arp_enabled:
            pattern_short = self._get_pattern_short_name(settings.pattern)
            layers.append(f"Arp({pattern_short})")

        # Clock layer (if enabled) - always last with dash
        if settings.clock_enabled and layers:
            clk_src = "Int" if settings.clock_source == settings.CLOCK_INTERNAL else "Ext"
            return " -> ".join(layers) + f" - Clk({clk_src})"
        elif settings.clock_enabled:
            # Only clock enabled
            clk_src = "Int" if settings.clock_source == settings.CLOCK_INTERNAL else "Ext"
            return f"Clk({clk_src})"
        elif layers:
            # No clock, but other layers
            return " -> ".join(layers)
        else:
            # No layers enabled!
            return "No layers active"

    def _get_scale_short_name(self, scale_type):
        """Get short scale name for display"""
        scale_names = {
            0: "Chr",   # Chromatic
            1: "Maj",   # Major
            2: "Min",   # Minor
            3: "Dor",   # Dorian
            4: "Phr",   # Phrygian
            5: "Lyd",   # Lydian
            6: "Mix",   # Mixolydian
            7: "Aeo",   # Aeolian
            8: "Loc",   # Locrian
            9: "Blu",   # Blues
            10: "Pnt",  # Pentatonic Major
            11: "PnM"   # Pentatonic Minor
        }
        return scale_names.get(scale_type, "?")

    def _get_pattern_short_name(self, pattern):
        """Get short pattern name for display"""
        pattern_names = {
            0: "Up",
            1: "Dn",
            2: "UpDn",
            3: "DnUp",
            4: "Rnd",
            5: "Play",
            6: "UpI",   # Up-Down Inclusive
            7: "DnI",   # Down-Up Inclusive
            8: "Up2",   # Up 2x
            9: "Dn2",   # Down 2x
            10: "Conv", # Converge
            11: "Div",  # Diverge
            12: "Pnky", # Pinky Up
            13: "Thmb", # Thumb Up
            14: "Oct",  # Octave Up
            15: "Chrd"  # Chord Repeat
        }
        return pattern_names.get(pattern, "?")
