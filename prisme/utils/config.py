"""
Global settings for the MIDI Arpeggiator
Manages configuration for arpeggiation patterns, timing, and behavior
"""

import struct
import microcontroller

# Firmware version
FIRMWARE_VERSION = "1.0.0"
FIRMWARE_DATE = "2025-01-15"

# Settings storage using NVM (non-volatile memory)
# NVM is always writable, even when USB is connected
# CircuitPython provides 256 bytes of NVM on most boards
NVM_SETTINGS_MAGIC = b'ARP2'  # Magic bytes for v2 format (for migration)
NVM_SETTINGS_MAGIC_V3 = b'ARP3'  # Magic bytes for v3 format (unified controls)
NVM_SETTINGS_START = 0  # Start offset in NVM

# Struct format for compact binary storage
# B = unsigned byte (0-255), H = unsigned short (0-65535), f = float

# V2 format (for migration): 4 (magic) + 31 bytes = 35 bytes total
# 27 values: 19 core + 8 Translation Hub
SETTINGS_STRUCT_FORMAT = 'BBBHBBBBBBBBBBBfBBBBBBBBBBB'  # v2 (migration only)

# V3 format (unified controls): 4 (magic) + 31 bytes = 35 bytes total (13.7% of 256 byte limit)
# 29 values: 18 core + 2 Translation basics + 8 v3 unified controls + 1 display
# Removed (7): cv_enabled, scale_enabled, arp_enabled, clock_multiply, clock_divide, swing_percent, clock_enabled
# Added (9): clock_rate, timing_feel, midi_filter, likelihood, strum_speed, strum_octaves, strum_repeat, strum_direction, display_rotation
SETTINGS_STRUCT_FORMAT_V3 = 'BBBHBBBBBBBBBBfBBBBBBBBBBBBBH'  # v3 (29 values + display_rotation)

class Settings:
    """Global settings container for the arpeggiator"""

    # Arpeggiator pattern types
    ARP_UP = 0
    ARP_DOWN = 1
    ARP_UP_DOWN = 2
    ARP_DOWN_UP = 3
    ARP_RANDOM = 4
    ARP_AS_PLAYED = 5
    ARP_UP_DOWN_INC = 6      # Up-down with top note repeated (inclusive)
    ARP_DOWN_UP_INC = 7      # Down-up with bottom note repeated (inclusive)
    ARP_UP_2X = 8            # Each note twice going up
    ARP_DOWN_2X = 9          # Each note twice going down
    ARP_CONVERGE = 10        # Alternate between lowest and highest, moving inward
    ARP_DIVERGE = 11         # Alternate from middle out
    ARP_PINKY_UP = 12        # Pinky pattern: 1-2-3-highest, repeat
    ARP_THUMB_UP = 13        # Thumb pattern: lowest-2-3-4, repeat
    ARP_OCTAVE_UP = 14       # Play root then jump octaves up
    ARP_CHORD_REPEAT = 15    # Repeat all notes as a chord, then arpeggio
    ARP_STRUM = 16           # Guitar-like strum with configurable speed/direction

    # Strum direction types
    STRUM_UP = 0             # Strum from low to high
    STRUM_DOWN = 1           # Strum from high to low
    STRUM_UP_DOWN = 2        # Strum up then down

    # Clock source types
    CLOCK_INTERNAL = 0
    CLOCK_EXTERNAL = 1

    # CV scaling types
    CV_SCALE_STANDARD = 0  # 1V/octave (standard modular)
    CV_SCALE_MOOG = 1      # 1.035V/octave (Moog Source)

    # Trigger polarity
    TRIGGER_VTRIG = 0      # V-trig: 0V=off, 5V=on (standard)
    TRIGGER_STRIG = 1      # S-trig: 5V=off, 0V=on (Moog Source inverted)

    # Custom CC source types
    CC_SOURCE_DISABLED = 0   # Custom CC output disabled
    CC_SOURCE_CC = 1         # MIDI CC (Control Change)
    CC_SOURCE_AFTERTOUCH = 2 # Channel Pressure (Aftertouch)
    CC_SOURCE_PITCHBEND = 3  # Pitch Bend
    CC_SOURCE_VELOCITY = 4   # Note Velocity

    # Custom CC smoothing levels
    CC_SMOOTH_OFF = 0   # No smoothing (alpha = 1.0)
    CC_SMOOTH_LOW = 1   # Light smoothing (alpha = 0.9)
    CC_SMOOTH_MID = 2   # Medium smoothing (alpha = 0.7)
    CC_SMOOTH_HIGH = 3  # Heavy smoothing (alpha = 0.5)

    # Translation Hub - Routing modes
    ROUTING_THRU = 0        # Pass-through mode (zero latency)
    ROUTING_TRANSLATION = 1  # Translation layer processing

    # Translation Hub - Input source selection
    INPUT_SOURCE_MIDI_IN = 0  # MIDI IN (DIN-5 UART)
    INPUT_SOURCE_USB = 1       # USB MIDI
    INPUT_SOURCE_CV_IN = 2     # CV IN (future)
    INPUT_SOURCE_GATE_IN = 3   # Gate IN (future)

    # Display rotation (for handedness preference)
    DISPLAY_ROTATION_0 = 0     # Normal (USB-C on left for right-handed)
    DISPLAY_ROTATION_180 = 180 # Rotated 180° (USB-C on right for left-handed)

    # Translation Hub - Clock transformations
    CLOCK_MULTIPLY_1X = 1
    CLOCK_MULTIPLY_2X = 2
    CLOCK_MULTIPLY_4X = 4

    CLOCK_DIVIDE_1 = 1
    CLOCK_DIVIDE_2 = 2
    CLOCK_DIVIDE_4 = 4
    CLOCK_DIVIDE_8 = 8

    # Clock Rate (unified multiply/divide) - NEW in v3
    CLOCK_RATE_DIV_8 = 0
    CLOCK_RATE_DIV_4 = 1
    CLOCK_RATE_DIV_2 = 2
    CLOCK_RATE_1X = 3      # Default - no transformation
    CLOCK_RATE_2X = 4
    CLOCK_RATE_4X = 5
    CLOCK_RATE_8X = 6

    # MIDI Filter presets - NEW in v3
    MIDI_FILTER_OFF = 0      # Pass everything
    MIDI_FILTER_VINTAGE = 1  # Safe for vintage synths
    MIDI_FILTER_MINIMAL = 2  # Only Note + Clock (future)
    MIDI_FILTER_CUSTOM = 3   # User-defined (future)

    # Scale types (chromatic intervals from root note)
    SCALE_CHROMATIC = 0    # All notes (no quantization)
    SCALE_MAJOR = 1        # Major scale
    SCALE_MINOR = 2        # Natural minor
    SCALE_DORIAN = 3       # Dorian mode
    SCALE_PHRYGIAN = 4     # Phrygian mode
    SCALE_LYDIAN = 5       # Lydian mode
    SCALE_MIXOLYDIAN = 6   # Mixolydian mode
    SCALE_MINOR_PENT = 7   # Minor pentatonic
    SCALE_MAJOR_PENT = 8   # Major pentatonic
    SCALE_BLUES = 9        # Blues scale
    SCALE_HARMONIC_MIN = 10  # Harmonic minor
    SCALE_MELODIC_MIN = 11   # Melodic minor

    # Scale interval patterns (semitones from root)
    SCALE_INTERVALS = {
        SCALE_CHROMATIC: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  # All notes
        SCALE_MAJOR: [0, 2, 4, 5, 7, 9, 11],  # W-W-H-W-W-W-H
        SCALE_MINOR: [0, 2, 3, 5, 7, 8, 10],  # W-H-W-W-H-W-W
        SCALE_DORIAN: [0, 2, 3, 5, 7, 9, 10],  # W-H-W-W-W-H-W
        SCALE_PHRYGIAN: [0, 1, 3, 5, 7, 8, 10],  # H-W-W-W-H-W-W
        SCALE_LYDIAN: [0, 2, 4, 6, 7, 9, 11],  # W-W-W-H-W-W-H
        SCALE_MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],  # W-W-H-W-W-H-W
        SCALE_MINOR_PENT: [0, 3, 5, 7, 10],  # Minor pentatonic
        SCALE_MAJOR_PENT: [0, 2, 4, 7, 9],  # Major pentatonic
        SCALE_BLUES: [0, 3, 5, 6, 7, 10],  # Blues scale
        SCALE_HARMONIC_MIN: [0, 2, 3, 5, 7, 8, 11],  # Harmonic minor
        SCALE_MELODIC_MIN: [0, 2, 3, 5, 7, 9, 11],  # Melodic minor
    }

    def __init__(self):
        # Arpeggiator settings
        self.pattern = self.ARP_UP  # Default pattern
        self.enabled = True  # Arpeggiator on/off

        # Clock settings
        self.clock_source = self.CLOCK_INTERNAL  # Default to internal clock
        self.internal_bpm = 120  # Internal clock BPM

        # Clock division (how many clock ticks per arp step)
        # 24 PPQN (pulses per quarter note) is MIDI standard
        # 6 = 16th notes, 12 = 8th notes, 24 = quarter notes
        self.clock_division = 6  # Default to 16th notes

        # Note settings
        self.octave_range = 1  # How many octaves to span (1-4)
        self.gate_length = 0.8  # Note length as fraction of step (0.1-1.0)

        # MIDI settings
        self.midi_channel = 0  # 0-15, channel to monitor/output
        self.velocity_passthrough = True  # Use incoming velocity or fixed
        self.fixed_velocity = 100  # Used if velocity_passthrough is False

        # Latch mode
        self.latch = False  # If True, notes continue even after key release

        # CV/Trigger settings
        self.cv_enabled = True  # Enable CV output
        self.cv_scale = self.CV_SCALE_STANDARD  # 1V/octave by default
        self.trigger_polarity = self.TRIGGER_VTRIG  # V-trig by default

        # Scale quantization settings
        self.scale_type = self.SCALE_CHROMATIC  # Default to chromatic (no quantization)
        self.scale_root = 0  # Root note (0=C, 1=C#, 2=D, etc.)

        # Custom CC settings
        self.custom_cc_source = self.CC_SOURCE_DISABLED  # Default to disabled
        self.custom_cc_number = 74  # Default to CC 74 (Filter Cutoff)
        self.custom_cc_smoothing = self.CC_SMOOTH_LOW  # Default to light smoothing

        # Translation Hub settings (8 new bytes)
        # ============================================================================
        # TRANSLATION LAYERS ARCHITECTURE:
        # prisme has THREE translation layers in FIXED ORDER:
        #   1. Scale (pitch quantization)
        #   2. Arp (sequence generation)
        #   3. Clock (timing transformation)
        #
        # WHY this order is fixed:
        #   - Scale corrects pitch BEFORE musical processing (not an effect)
        #   - Arp generates sequences from corrected notes
        #   - Clock transforms timing globally
        #
        # IMPORTANT: Clock is architecturally separate from Scale/Arp:
        #   - Scale/Arp: Data-driven (note in → note out) via TranslationPipeline
        #   - Clock: Event-driven (callback-based timing engine) via ClockHandler
        #
        # WHY Clock is separate:
        #   - Global timing: Affects all output, not just individual notes
        #   - Source independence: Can be internal OR external MIDI clock
        #   - Callback model: Triggers arpeggiator steps, not note transformation
        #
        # However, Clock IS a translation layer from the user's perspective:
        #   - When enabled: Applies swing/multiply/divide timing transformations
        #   - When disabled: 1:1 timing (multiply=1, divide=1, swing=50%)
        #   - Only affects output in TRANSLATION mode (not THRU)
        #
        # Display format: "Scale → Arp - Clock" (dash indicates Clock is always last)
        # V3 Philosophy: Value determines behavior (no redundant enable/disable toggles)
        # ============================================================================
        self.routing_mode = self.ROUTING_TRANSLATION  # Default to translation mode
        self.input_source = self.INPUT_SOURCE_MIDI_IN  # Default to MIDI IN

        # ============================================================================
        # UNIFIED CONTROLS (v3) - Intuitive, self-explanatory settings
        # ============================================================================
        self.clock_rate = self.CLOCK_RATE_1X  # Unified multiply/divide: /8 to 8x (1x = disabled)
        self.timing_feel = 50  # Unified swing/humanize: 50-100% (50=robot/disabled, 51-75=swing, 76-100=humanize)
        self.midi_filter = self.MIDI_FILTER_OFF  # MIDI filter preset: Off/Vintage/Minimal
        self.likelihood = 100  # Note probability: 0-100% (100=all notes, disabled)

        # Strum arpeggiator settings (for future feature)
        self.strum_speed = 1  # Clock division: 0=/64, 1=/32, 2=/16, 3=/8, 4=/4, 5=/2
        self.strum_octaves = 1  # Octave range: 1-4
        self.strum_repeat = False  # One-shot or loop
        self.strum_direction = 0  # 0=Up, 1=Down, 2=UpDown

        # Display settings
        self.display_rotation = self.DISPLAY_ROTATION_0  # 0 (normal) or 180 (flipped for left-handed)

    def get_pattern_name(self):
        """Return human-readable pattern name"""
        patterns = {
            self.ARP_UP: "Up",
            self.ARP_DOWN: "Down",
            self.ARP_UP_DOWN: "Up-Down",
            self.ARP_DOWN_UP: "Down-Up",
            self.ARP_RANDOM: "Random",
            self.ARP_AS_PLAYED: "As Played",
            self.ARP_UP_DOWN_INC: "Up-Dn Inc",
            self.ARP_DOWN_UP_INC: "Dn-Up Inc",
            self.ARP_UP_2X: "Up 2x",
            self.ARP_DOWN_2X: "Down 2x",
            self.ARP_CONVERGE: "Converge",
            self.ARP_DIVERGE: "Diverge",
            self.ARP_PINKY_UP: "Pinky Up",
            self.ARP_THUMB_UP: "Thumb Up",
            self.ARP_OCTAVE_UP: "Oct Up",
            self.ARP_CHORD_REPEAT: "Chord Rpt",
            self.ARP_STRUM: "Strum"
        }
        return patterns.get(self.pattern, "Unknown")

    def next_pattern(self):
        """Cycle to next pattern"""
        self.pattern = (self.pattern + 1) % 17  # 17 patterns (0-16)

    def set_clock_division_16th(self):
        """Set to 16th notes"""
        self.clock_division = 6

    def set_clock_division_8th(self):
        """Set to 8th notes"""
        self.clock_division = 12

    def set_clock_division_quarter(self):
        """Set to quarter notes"""
        self.clock_division = 24

    def set_clock_division_half(self):
        """Set to half notes"""
        self.clock_division = 48

    def toggle_enabled(self):
        """Toggle arpeggiator on/off"""
        self.enabled = not self.enabled

    def toggle_latch(self):
        """Toggle latch mode"""
        self.latch = not self.latch

    def get_clock_source_name(self):
        """Return human-readable clock source name"""
        return "Internal" if self.clock_source == self.CLOCK_INTERNAL else "External"

    def get_clock_source_short(self):
        """Return short clock source indicator for display"""
        return "(Int)" if self.clock_source == self.CLOCK_INTERNAL else "(Ext)"

    def next_clock_source(self):
        """Cycle to next clock source (wraps around)"""
        self.clock_source = (self.clock_source + 1) % 2  # 2 options: Internal, External
        print(f"[DEBUG] Clock source: {self.get_clock_source_name()}")

    def previous_clock_source(self):
        """Cycle to previous clock source (wraps around)"""
        self.clock_source = (self.clock_source - 1) % 2
        print(f"[DEBUG] Clock source: {self.get_clock_source_name()}")

    def get_cv_scale_name(self):
        """Return human-readable CV scale name"""
        if self.cv_scale == self.CV_SCALE_STANDARD:
            return "1V/octave"
        else:
            return "Moog (1.035V)"

    def get_routing_mode_name(self):
        """Return human-readable routing mode name"""
        if self.routing_mode == self.ROUTING_THRU:
            return "THRU"
        else:
            return "TRANSLATION"

    def next_cv_scale(self):
        """Cycle to next CV scale"""
        self.cv_scale = (self.cv_scale + 1) % 2  # 2 options: Standard, Moog

    def previous_cv_scale(self):
        """Cycle to previous CV scale"""
        self.cv_scale = (self.cv_scale - 1) % 2

    def get_trigger_polarity_name(self):
        """Return human-readable trigger polarity name"""
        return "V-trig" if self.trigger_polarity == self.TRIGGER_VTRIG else "S-trig"

    def next_trigger_polarity(self):
        """Cycle to next trigger polarity"""
        self.trigger_polarity = (self.trigger_polarity + 1) % 2  # 2 options: V-trig, S-trig

    def previous_trigger_polarity(self):
        """Cycle to previous trigger polarity"""
        self.trigger_polarity = (self.trigger_polarity - 1) % 2

    def get_scale_name(self):
        """Return human-readable scale name"""
        scale_names = {
            self.SCALE_CHROMATIC: "Chromatic",
            self.SCALE_MAJOR: "Major",
            self.SCALE_MINOR: "Minor",
            self.SCALE_DORIAN: "Dorian",
            self.SCALE_PHRYGIAN: "Phrygian",
            self.SCALE_LYDIAN: "Lydian",
            self.SCALE_MIXOLYDIAN: "Mixolydian",
            self.SCALE_MINOR_PENT: "Min Pent",
            self.SCALE_MAJOR_PENT: "Maj Pent",
            self.SCALE_BLUES: "Blues",
            self.SCALE_HARMONIC_MIN: "Harm Min",
            self.SCALE_MELODIC_MIN: "Mel Min",
        }
        return scale_names.get(self.scale_type, "Unknown")

    def next_scale(self):
        """Cycle to next scale"""
        self.scale_type = (self.scale_type + 1) % 12

    def previous_scale(self):
        """Cycle to previous scale"""
        self.scale_type = (self.scale_type - 1) % 12

    def get_root_note_name(self):
        """Return human-readable root note name"""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        return note_names[self.scale_root % 12]

    def next_root_note(self):
        """Cycle to next root note"""
        self.scale_root = (self.scale_root + 1) % 12

    def previous_root_note(self):
        """Cycle to previous root note"""
        self.scale_root = (self.scale_root - 1) % 12

    def get_custom_cc_source_name(self):
        """Return human-readable Custom CC source name"""
        source_names = {
            self.CC_SOURCE_DISABLED: "Disabled",
            self.CC_SOURCE_CC: "CC",
            self.CC_SOURCE_AFTERTOUCH: "Aftertouch",
            self.CC_SOURCE_PITCHBEND: "Pitch Bend",
            self.CC_SOURCE_VELOCITY: "Velocity"
        }
        return source_names.get(self.custom_cc_source, "Unknown")

    def next_custom_cc_source(self):
        """Cycle to next Custom CC source"""
        self.custom_cc_source = (self.custom_cc_source + 1) % 5  # 5 options

    def previous_custom_cc_source(self):
        """Cycle to previous Custom CC source"""
        self.custom_cc_source = (self.custom_cc_source - 1) % 5

    def get_custom_cc_smoothing_name(self):
        """Return human-readable Custom CC smoothing name"""
        smoothing_names = {
            self.CC_SMOOTH_OFF: "Off",
            self.CC_SMOOTH_LOW: "Low",
            self.CC_SMOOTH_MID: "Mid",
            self.CC_SMOOTH_HIGH: "High"
        }
        return smoothing_names.get(self.custom_cc_smoothing, "Unknown")

    def next_custom_cc_smoothing(self):
        """Cycle to next Custom CC smoothing level"""
        self.custom_cc_smoothing = (self.custom_cc_smoothing + 1) % 4  # 4 options

    def previous_custom_cc_smoothing(self):
        """Cycle to previous Custom CC smoothing level"""
        self.custom_cc_smoothing = (self.custom_cc_smoothing - 1) % 4

    def next_routing_mode(self):
        """Cycle to next routing mode (wraps around)"""
        self.routing_mode = (self.routing_mode + 1) % 2  # 2 options: THRU, TRANSLATION

    def previous_routing_mode(self):
        """Cycle to previous routing mode (wraps around)"""
        self.routing_mode = (self.routing_mode - 1) % 2

    def next_input_source(self):
        """Cycle to next input source"""
        self.input_source = (self.input_source + 1) % 4  # 4 options: MIDI IN, USB, CV IN, Gate IN

    def previous_input_source(self):
        """Cycle to previous input source"""
        self.input_source = (self.input_source - 1) % 4

    def get_input_source_name(self):
        """Return human-readable input source name"""
        source_names = {
            self.INPUT_SOURCE_MIDI_IN: "MIDI IN",
            self.INPUT_SOURCE_USB: "USB",
            self.INPUT_SOURCE_CV_IN: "CV IN",
            self.INPUT_SOURCE_GATE_IN: "Gate IN"
        }
        return source_names.get(self.input_source, "Unknown")

    # ============================================================================
    # NEW UNIFIED CONTROLS HELPERS (v3)
    # ============================================================================

    def get_clock_multiply_divide(self):
        """Convert clock_rate to multiply/divide values for clock engine

        Returns:
            tuple: (multiply, divide) for backward compatibility with clock engine
        """
        rates = [
            (1, 8),  # CLOCK_RATE_DIV_8
            (1, 4),  # CLOCK_RATE_DIV_4
            (1, 2),  # CLOCK_RATE_DIV_2
            (1, 1),  # CLOCK_RATE_1X
            (2, 1),  # CLOCK_RATE_2X
            (4, 1),  # CLOCK_RATE_4X
            (8, 1),  # CLOCK_RATE_8X
        ]
        return rates[self.clock_rate]

    def get_clock_rate_name(self):
        """Return human-readable clock rate name"""
        rate_names = {
            self.CLOCK_RATE_DIV_8: "/8",
            self.CLOCK_RATE_DIV_4: "/4",
            self.CLOCK_RATE_DIV_2: "/2",
            self.CLOCK_RATE_1X: "1x",
            self.CLOCK_RATE_2X: "2x",
            self.CLOCK_RATE_4X: "4x",
            self.CLOCK_RATE_8X: "8x",
        }
        return rate_names.get(self.clock_rate, "1x")

    def next_clock_rate(self):
        """Cycle to next clock rate"""
        self.clock_rate = (self.clock_rate + 1) % 7  # 7 options: /8 to 8x

    def previous_clock_rate(self):
        """Cycle to previous clock rate"""
        self.clock_rate = (self.clock_rate - 1) % 7

    def is_clock_active(self):
        """Check if clock transformations are active

        Returns:
            bool: True if clock rate != 1x OR timing feel != 50%
        """
        return self.clock_rate != self.CLOCK_RATE_1X or self.timing_feel != 50

    def is_scale_enabled(self):
        """Check if scale quantization is active

        Chromatic scale = all notes allowed = effectively disabled

        Returns:
            bool: True if scale type is not Chromatic
        """
        return self.scale_type != self.SCALE_CHROMATIC

    def is_arp_enabled(self):
        """Check if arpeggiator is active

        Zero octaves = no arpeggio = disabled

        Returns:
            bool: True if octave range > 0
        """
        return self.octave_range > 0

    def get_midi_filter_name(self):
        """Return human-readable MIDI filter name"""
        filter_names = {
            self.MIDI_FILTER_OFF: "Off",
            self.MIDI_FILTER_VINTAGE: "Vintage",
            self.MIDI_FILTER_MINIMAL: "Minimal",
            self.MIDI_FILTER_CUSTOM: "Custom",
        }
        return filter_names.get(self.midi_filter, "Off")

    def next_midi_filter(self):
        """Cycle to next MIDI filter preset"""
        self.midi_filter = (self.midi_filter + 1) % 4  # 4 options for now

    def previous_midi_filter(self):
        """Cycle to previous MIDI filter preset"""
        self.midi_filter = (self.midi_filter - 1) % 4

    # Strum helper methods
    def get_strum_speed_name(self):
        """Return human-readable strum speed name"""
        speed_names = {
            0: "/64",
            1: "/32",
            2: "/16",
            3: "/8",
            4: "/4",
            5: "/2"
        }
        return speed_names.get(self.strum_speed, "/32")

    def next_strum_speed(self):
        """Cycle to next strum speed"""
        self.strum_speed = (self.strum_speed + 1) % 6  # 6 speeds (0-5)

    def previous_strum_speed(self):
        """Cycle to previous strum speed"""
        self.strum_speed = (self.strum_speed - 1) % 6

    def get_strum_speed_division(self):
        """Convert strum_speed to clock division (PPQN)

        Returns:
            Clock division in PPQN (24 = quarter note)
        """
        # Map strum speed index to clock division
        divisions = {
            0: 1,   # /64 = 24/64 = 0.375 PPQN
            1: 2,   # /32 = 24/32 = 0.75 PPQN
            2: 6,   # /16 = 24/16 = 1.5 PPQN (16th note)
            3: 12,  # /8 = 24/8 = 3 PPQN (8th note)
            4: 24,  # /4 = quarter note
            5: 48   # /2 = half note
        }
        return divisions.get(self.strum_speed, 2)

    def next_strum_octaves(self):
        """Increment strum octaves (1-4)"""
        self.strum_octaves = min(4, self.strum_octaves + 1)

    def previous_strum_octaves(self):
        """Decrement strum octaves (1-4)"""
        self.strum_octaves = max(1, self.strum_octaves - 1)

    def toggle_strum_repeat(self):
        """Toggle strum repeat mode"""
        self.strum_repeat = not self.strum_repeat

    def get_strum_direction_name(self):
        """Return human-readable strum direction name"""
        direction_names = {
            self.STRUM_UP: "Up",
            self.STRUM_DOWN: "Down",
            self.STRUM_UP_DOWN: "Up-Down"
        }
        return direction_names.get(self.strum_direction, "Up")

    def next_strum_direction(self):
        """Cycle to next strum direction"""
        self.strum_direction = (self.strum_direction + 1) % 3  # 3 directions (0-2)

    def previous_strum_direction(self):
        """Cycle to previous strum direction"""
        self.strum_direction = (self.strum_direction - 1) % 3

    def should_filter_message(self, msg):
        """Check if MIDI message should be filtered based on current preset

        Args:
            msg: MIDI message object

        Returns:
            bool: True if message should be filtered (blocked)
        """
        if self.midi_filter == self.MIDI_FILTER_OFF:
            return False  # Pass everything

        if self.midi_filter == self.MIDI_FILTER_VINTAGE:
            # Filter problematic messages for vintage synths
            # Import here to avoid circular dependencies
            try:
                from adafruit_midi.active_sensing import ActiveSensing
                from adafruit_midi.channel_pressure import ChannelPressure
                from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure
                from adafruit_midi.program_change import ProgramChange

                return isinstance(msg, (ActiveSensing, ChannelPressure,
                                        PolyphonicKeyPressure, ProgramChange))
            except ImportError:
                # Running in test environment without adafruit_midi
                return False

        # Future: MIDI_FILTER_MINIMAL (only Note + Clock)
        # Future: MIDI_FILTER_CUSTOM (user-defined)
        return False

    def quantize_to_scale(self, midi_note):
        """
        Quantize a MIDI note to the current scale

        Args:
            midi_note: Input MIDI note number (0-127)

        Returns:
            Quantized MIDI note number
        """
        # If chromatic, no quantization needed
        if self.scale_type == self.SCALE_CHROMATIC:
            return midi_note

        # Get the scale intervals
        intervals = self.SCALE_INTERVALS[self.scale_type]

        # Find the octave and note within octave
        octave = midi_note // 12
        note_in_octave = midi_note % 12

        # Adjust for root note
        note_relative_to_root = (note_in_octave - self.scale_root) % 12

        # Find nearest note in scale
        min_distance = 12
        nearest_interval = 0

        for interval in intervals:
            distance = abs(note_relative_to_root - interval)
            # Also check wrap-around distance
            wrap_distance = 12 - distance

            if distance < min_distance:
                min_distance = distance
                nearest_interval = interval
            if wrap_distance < min_distance:
                min_distance = wrap_distance
                nearest_interval = interval

        # Calculate quantized note
        quantized_note_in_octave = (self.scale_root + nearest_interval) % 12
        quantized_note = (octave * 12) + quantized_note_in_octave

        # Make sure we stay in MIDI range
        return max(0, min(127, quantized_note))

    def save(self):
        """
        Save current settings to NVM (non-volatile memory) using v3 format

        Returns:
            True if successful, False otherwise
        """
        try:
            # Pack settings into compact binary format (v3)
            # Order must match SETTINGS_STRUCT_FORMAT_V3
            packed_data = struct.pack(
                SETTINGS_STRUCT_FORMAT_V3,
                self.pattern,              # B (byte)
                int(self.enabled),         # B (byte as bool)
                self.clock_source,         # B (byte)
                self.internal_bpm,         # H (unsigned short)
                self.clock_division,       # B (byte)
                self.octave_range,         # B (byte)
                self.midi_channel,         # B (byte)
                int(self.velocity_passthrough),  # B (byte as bool)
                self.fixed_velocity,       # B (byte)
                int(self.latch),           # B (byte as bool)
                # cv_enabled removed (v3)
                self.cv_scale,             # B (byte)
                self.trigger_polarity,     # B (byte)
                self.scale_type,           # B (byte)
                self.scale_root,           # B (byte)
                self.gate_length,          # f (float)
                self.custom_cc_source,     # B (byte)
                self.custom_cc_number,     # B (byte)
                self.custom_cc_smoothing,  # B (byte)
                # Translation Hub v3 settings
                self.routing_mode,         # B (byte)
                self.input_source,         # B (byte)
                # Unified controls (v3) - replaced 7 old settings
                self.clock_rate,           # B (byte)
                self.timing_feel,          # B (byte)
                self.midi_filter,          # B (byte)
                self.likelihood,           # B (byte)
                self.strum_speed,          # B (byte)
                self.strum_octaves,        # B (byte)
                int(self.strum_repeat),    # B (byte as bool)
                self.strum_direction,      # B (byte)
                self.display_rotation      # H (unsigned short: 0 or 180)
            )

            # Prepend v3 magic bytes
            nvm_data = NVM_SETTINGS_MAGIC_V3 + packed_data

            # Write to NVM
            microcontroller.nvm[NVM_SETTINGS_START:NVM_SETTINGS_START + len(nvm_data)] = nvm_data

            print(f"Settings saved to NVM (v3 format, {len(packed_data)} bytes)")
            return True

        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False

    def load(self):
        """
        Load settings from NVM with format migration (v2 → v3)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Try v3 format first (current)
            struct_size_v3 = struct.calcsize(SETTINGS_STRUCT_FORMAT_V3)
            total_size_v3 = len(NVM_SETTINGS_MAGIC_V3) + struct_size_v3
            nvm_data = bytes(microcontroller.nvm[NVM_SETTINGS_START:NVM_SETTINGS_START + total_size_v3])

            if nvm_data.startswith(NVM_SETTINGS_MAGIC_V3):
                # V3 format detected
                packed_data = nvm_data[len(NVM_SETTINGS_MAGIC_V3):]
                unpacked = struct.unpack(SETTINGS_STRUCT_FORMAT_V3, packed_data)
                self._load_v3(unpacked)
                print(f"Settings loaded (v3 format, {struct_size_v3} bytes)")
                return True

            # Try v2 format (migration needed)
            struct_size_v2 = struct.calcsize(SETTINGS_STRUCT_FORMAT)
            total_size_v2 = len(NVM_SETTINGS_MAGIC) + struct_size_v2
            nvm_data = bytes(microcontroller.nvm[NVM_SETTINGS_START:NVM_SETTINGS_START + total_size_v2])

            if nvm_data.startswith(NVM_SETTINGS_MAGIC):
                # V2 format detected - migrate to v3
                print("Migrating settings from v2 to v3 format...")
                packed_data = nvm_data[len(NVM_SETTINGS_MAGIC):]
                unpacked = struct.unpack(SETTINGS_STRUCT_FORMAT, packed_data)
                self._load_v2_and_migrate(unpacked)
                self.save()  # Save in new v3 format
                print("Settings migrated to v3 format")
                return True

            # No valid settings found
            print("No saved settings found in NVM, using defaults")
            return False

        except Exception as e:
            print(f"Failed to load settings from NVM: {e}")
            print("Using default settings")
            return False

    def _load_v3(self, unpacked):
        """Load v3 format settings

        Args:
            unpacked: Tuple of unpacked values from struct.unpack
        """
        self.pattern = unpacked[0]
        self.enabled = bool(unpacked[1])
        self.clock_source = unpacked[2]
        self.internal_bpm = unpacked[3]
        self.clock_division = unpacked[4]
        self.octave_range = unpacked[5]
        self.midi_channel = unpacked[6]
        self.velocity_passthrough = bool(unpacked[7])
        self.fixed_velocity = unpacked[8]
        self.latch = bool(unpacked[9])
        # cv_enabled removed in v3
        self.cv_scale = unpacked[10]
        self.trigger_polarity = unpacked[11]
        self.scale_type = unpacked[12]
        self.scale_root = unpacked[13]
        self.gate_length = unpacked[14]
        self.custom_cc_source = unpacked[15]
        self.custom_cc_number = unpacked[16]
        self.custom_cc_smoothing = unpacked[17]
        # Translation Hub v3
        self.routing_mode = unpacked[18]
        self.input_source = unpacked[19]
        # Unified controls (v3)
        self.clock_rate = unpacked[20]
        self.timing_feel = unpacked[21]
        self.midi_filter = unpacked[22]
        self.likelihood = unpacked[23]
        self.strum_speed = unpacked[24]
        self.strum_octaves = unpacked[25]
        self.strum_repeat = bool(unpacked[26])
        self.strum_direction = unpacked[27]
        self.display_rotation = unpacked[28]

    def _load_v2_and_migrate(self, unpacked):
        """Load v2 format and migrate to v3

        Args:
            unpacked: Tuple of unpacked values from v2 struct.unpack
        """
        # Load core settings (unchanged)
        self.pattern = unpacked[0]
        self.enabled = bool(unpacked[1])
        self.clock_source = unpacked[2]
        self.internal_bpm = unpacked[3]
        self.clock_division = unpacked[4]
        self.octave_range = unpacked[5]
        self.midi_channel = unpacked[6]
        self.velocity_passthrough = bool(unpacked[7])
        self.fixed_velocity = unpacked[8]
        self.latch = bool(unpacked[9])
        # Skip cv_enabled (unpacked[10]) - removed in v3
        self.cv_scale = unpacked[11]
        self.trigger_polarity = unpacked[12]
        self.scale_type = unpacked[13]
        self.scale_root = unpacked[14]
        self.gate_length = unpacked[15]
        self.custom_cc_source = unpacked[16]
        self.custom_cc_number = unpacked[17]
        self.custom_cc_smoothing = unpacked[18]
        # Translation Hub basics
        self.routing_mode = unpacked[19]
        self.input_source = unpacked[20]
        # Skip scale_enabled, arp_enabled (unpacked[21-22]) - removed in v3

        # Migrate clock settings (v2 → v3)
        clock_multiply = unpacked[23]
        clock_divide = unpacked[24]
        swing_percent = unpacked[25]
        # clock_enabled = unpacked[26]  # Ignored (auto-detected in v3)

        # Convert multiply/divide to unified clock_rate
        if clock_divide == 8:
            self.clock_rate = self.CLOCK_RATE_DIV_8
        elif clock_divide == 4:
            self.clock_rate = self.CLOCK_RATE_DIV_4
        elif clock_divide == 2:
            self.clock_rate = self.CLOCK_RATE_DIV_2
        elif clock_multiply == 2:
            self.clock_rate = self.CLOCK_RATE_2X
        elif clock_multiply == 4:
            self.clock_rate = self.CLOCK_RATE_4X
        elif clock_multiply == 8:
            self.clock_rate = self.CLOCK_RATE_8X
        else:
            self.clock_rate = self.CLOCK_RATE_1X  # Default

        # Convert swing to timing_feel
        self.timing_feel = max(50, swing_percent)

        # Default new v3 settings
        self.midi_filter = self.MIDI_FILTER_OFF
        self.likelihood = 100  # All notes (disabled)
        self.strum_speed = 1  # /32
        self.strum_octaves = 1
        self.strum_repeat = False
        self.strum_direction = 0  # Up
        self.display_rotation = self.DISPLAY_ROTATION_0  # Normal orientation


# Global settings instance
settings = Settings()
