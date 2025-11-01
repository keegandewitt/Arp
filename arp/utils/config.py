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
NVM_SETTINGS_MAGIC = b'ARP2'  # Magic bytes to identify valid settings (v2 = struct format)
NVM_SETTINGS_START = 0  # Start offset in NVM

# Struct format for compact binary storage
# B = unsigned byte (0-255), H = unsigned short (0-65535), f = float
# Total: 4 (magic) + 31 bytes = 35 bytes (13.7% of 256 byte limit)
# Pattern, enabled, clock_source, internal_bpm, clock_division, octave_range,
# midi_channel, velocity_passthrough, fixed_velocity, latch, cv_enabled,
# cv_scale, trigger_polarity, scale_type, scale_root, gate_length,
# custom_cc_source, custom_cc_number, custom_cc_smoothing (19 values)
# + Translation Hub: routing_mode, input_source, layer_order, scale_enabled,
#   arp_enabled, clock_multiply, clock_divide, swing_percent (8 values)
SETTINGS_STRUCT_FORMAT = 'BBBHBBBBBBBBBBBfBBBBBBBBBBB'  # 27 values total (19 + 8)

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

    # Translation Hub - Layer ordering
    LAYER_ORDER_SCALE_FIRST = 0  # Scale → Arp
    LAYER_ORDER_ARP_FIRST = 1    # Arp → Scale

    # Translation Hub - Clock transformations
    CLOCK_MULTIPLY_1X = 1
    CLOCK_MULTIPLY_2X = 2
    CLOCK_MULTIPLY_4X = 4

    CLOCK_DIVIDE_1 = 1
    CLOCK_DIVIDE_2 = 2
    CLOCK_DIVIDE_4 = 4
    CLOCK_DIVIDE_8 = 8

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
        self.routing_mode = self.ROUTING_TRANSLATION  # Default to translation mode
        self.input_source = self.INPUT_SOURCE_MIDI_IN  # Default to MIDI IN
        self.layer_order = self.LAYER_ORDER_SCALE_FIRST  # Default to Scale → Arp
        self.scale_enabled = True  # Scale quantization layer enabled
        self.arp_enabled = True    # Arpeggiator layer enabled
        self.clock_multiply = self.CLOCK_MULTIPLY_1X  # Default to 1x (no multiply)
        self.clock_divide = self.CLOCK_DIVIDE_1      # Default to 1 (no divide)
        self.swing_percent = 50    # Default to 50% (no swing)

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

    def next_layer_order(self):
        """Cycle to next layer order (wraps around)"""
        self.layer_order = (self.layer_order + 1) % 2  # 2 options: Scale First, Arp First

    def previous_layer_order(self):
        """Cycle to previous layer order (wraps around)"""
        self.layer_order = (self.layer_order - 1) % 2

    def get_layer_order_name(self):
        """Return human-readable layer order name"""
        if self.layer_order == self.LAYER_ORDER_SCALE_FIRST:
            return "Scale First"
        else:
            return "Arp First"

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
        Save current settings to NVM (non-volatile memory) using compact binary format

        Returns:
            True if successful, False otherwise
        """
        try:
            # Pack settings into compact binary format
            # Order must match SETTINGS_STRUCT_FORMAT
            packed_data = struct.pack(
                SETTINGS_STRUCT_FORMAT,
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
                int(self.cv_enabled),      # B (byte as bool)
                self.cv_scale,             # B (byte)
                self.trigger_polarity,     # B (byte)
                self.scale_type,           # B (byte)
                self.scale_root,           # B (byte)
                self.gate_length,          # f (float)
                self.custom_cc_source,     # B (byte)
                self.custom_cc_number,     # B (byte)
                self.custom_cc_smoothing,  # B (byte)
                # Translation Hub settings (8 new bytes)
                self.routing_mode,         # B (byte)
                self.input_source,         # B (byte)
                self.layer_order,          # B (byte)
                int(self.scale_enabled),   # B (byte as bool)
                int(self.arp_enabled),     # B (byte as bool)
                self.clock_multiply,       # B (byte)
                self.clock_divide,         # B (byte)
                self.swing_percent         # B (byte)
            )

            # Prepend magic bytes
            nvm_data = NVM_SETTINGS_MAGIC + packed_data

            # Write to NVM
            microcontroller.nvm[NVM_SETTINGS_START:NVM_SETTINGS_START + len(nvm_data)] = nvm_data

            print(f"Settings saved to NVM ({len(packed_data)} bytes)")
            return True

        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False

    def load(self):
        """
        Load settings from NVM (non-volatile memory) using compact binary format

        Returns:
            True if successful, False otherwise
        """
        try:
            # Calculate how many bytes we need to read
            struct_size = struct.calcsize(SETTINGS_STRUCT_FORMAT)
            total_size = len(NVM_SETTINGS_MAGIC) + struct_size

            # Read from NVM
            nvm_data = bytes(microcontroller.nvm[NVM_SETTINGS_START:NVM_SETTINGS_START + total_size])

            # Check magic bytes
            if not nvm_data.startswith(NVM_SETTINGS_MAGIC):
                print("No saved settings found in NVM, using defaults")
                return False

            # Extract binary data (skip magic bytes)
            packed_data = nvm_data[len(NVM_SETTINGS_MAGIC):]

            # Unpack settings from binary format
            # Order must match SETTINGS_STRUCT_FORMAT and save() method
            unpacked = struct.unpack(SETTINGS_STRUCT_FORMAT, packed_data)

            # Assign to settings (order must match pack() in save())
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
            self.cv_enabled = bool(unpacked[10])
            self.cv_scale = unpacked[11]
            self.trigger_polarity = unpacked[12]
            self.scale_type = unpacked[13]
            self.scale_root = unpacked[14]
            self.gate_length = unpacked[15]
            self.custom_cc_source = unpacked[16]
            self.custom_cc_number = unpacked[17]
            self.custom_cc_smoothing = unpacked[18]
            # Translation Hub settings (8 new values)
            self.routing_mode = unpacked[19]
            self.input_source = unpacked[20]
            self.layer_order = unpacked[21]
            self.scale_enabled = bool(unpacked[22])
            self.arp_enabled = bool(unpacked[23])
            self.clock_multiply = unpacked[24]
            self.clock_divide = unpacked[25]
            self.swing_percent = unpacked[26]

            print(f"Settings loaded from NVM ({struct_size} bytes)")
            return True

        except Exception as e:
            print(f"Failed to load settings from NVM: {e}")
            print("Using default settings")
            return False


# Global settings instance
settings = Settings()
