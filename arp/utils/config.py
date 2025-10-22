"""
Global settings for the MIDI Arpeggiator
Manages configuration for arpeggiation patterns, timing, and behavior
"""

# Firmware version
FIRMWARE_VERSION = "1.0.0"
FIRMWARE_DATE = "2025-01-15"

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

    # Clock source types
    CLOCK_INTERNAL = 0
    CLOCK_EXTERNAL = 1

    # CV scaling types
    CV_SCALE_STANDARD = 0  # 1V/octave (standard modular)
    CV_SCALE_MOOG = 1      # 1.035V/octave (Moog Source)

    # Trigger polarity
    TRIGGER_VTRIG = 0      # V-trig: 0V=off, 5V=on (standard)
    TRIGGER_STRIG = 1      # S-trig: 5V=off, 0V=on (Moog Source inverted)

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
            self.ARP_CHORD_REPEAT: "Chord Rpt"
        }
        return patterns.get(self.pattern, "Unknown")

    def next_pattern(self):
        """Cycle to next pattern"""
        self.pattern = (self.pattern + 1) % 16

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

    def toggle_clock_source(self):
        """Toggle between internal and external clock"""
        if self.clock_source == self.CLOCK_INTERNAL:
            self.clock_source = self.CLOCK_EXTERNAL
        else:
            self.clock_source = self.CLOCK_INTERNAL

    def get_cv_scale_name(self):
        """Return human-readable CV scale name"""
        if self.cv_scale == self.CV_SCALE_STANDARD:
            return "1V/octave"
        else:
            return "Moog (1.035V)"

    def toggle_cv_scale(self):
        """Toggle between standard and Moog CV scaling"""
        if self.cv_scale == self.CV_SCALE_STANDARD:
            self.cv_scale = self.CV_SCALE_MOOG
        else:
            self.cv_scale = self.CV_SCALE_STANDARD

    def get_trigger_polarity_name(self):
        """Return human-readable trigger polarity name"""
        return "V-trig" if self.trigger_polarity == self.TRIGGER_VTRIG else "S-trig"

    def toggle_trigger_polarity(self):
        """Toggle between V-trig and S-trig"""
        if self.trigger_polarity == self.TRIGGER_VTRIG:
            self.trigger_polarity = self.TRIGGER_STRIG
        else:
            self.trigger_polarity = self.TRIGGER_VTRIG

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


# Global settings instance
settings = Settings()
