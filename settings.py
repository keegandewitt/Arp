"""
Global settings for the MIDI Arpeggiator
Manages configuration for arpeggiation patterns, timing, and behavior
"""

class Settings:
    """Global settings container for the arpeggiator"""

    # Arpeggiator pattern types
    ARP_UP = 0
    ARP_DOWN = 1
    ARP_UP_DOWN = 2
    ARP_DOWN_UP = 3
    ARP_RANDOM = 4
    ARP_AS_PLAYED = 5

    # Clock source types
    CLOCK_INTERNAL = 0
    CLOCK_EXTERNAL = 1

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

    def get_pattern_name(self):
        """Return human-readable pattern name"""
        patterns = {
            self.ARP_UP: "Up",
            self.ARP_DOWN: "Down",
            self.ARP_UP_DOWN: "Up-Down",
            self.ARP_DOWN_UP: "Down-Up",
            self.ARP_RANDOM: "Random",
            self.ARP_AS_PLAYED: "As Played"
        }
        return patterns.get(self.pattern, "Unknown")

    def next_pattern(self):
        """Cycle to next pattern"""
        self.pattern = (self.pattern + 1) % 6

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


# Global settings instance
settings = Settings()
