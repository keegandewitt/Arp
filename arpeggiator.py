"""
Arpeggiator Engine
Core logic for generating arpeggiated note sequences
"""

import random
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff


class Arpeggiator:
    """Main arpeggiator engine"""

    def __init__(self, settings, midi_io):
        """
        Initialize the arpeggiator

        Args:
            settings: Global settings object
            midi_io: MidiIO object for sending notes
        """
        self.settings = settings
        self.midi_io = midi_io

        # Note buffer - stores currently held notes
        self.note_buffer = []  # List of (note, velocity) tuples
        self.note_order = []  # Order notes were received (for as-played mode)

        # Arpeggiator state
        self.current_step = 0
        self.current_note = None  # Currently playing note
        self.step_sequence = []  # Generated sequence of notes to play

    def add_note(self, note, velocity):
        """
        Add a note to the arpeggiator buffer

        Args:
            note: MIDI note number
            velocity: Note velocity
        """
        # Add to buffer if not already present
        if not any(n[0] == note for n in self.note_buffer):
            self.note_buffer.append((note, velocity))
            self.note_order.append(note)

            # Regenerate sequence
            self._generate_sequence()

            # If this is the first note, reset step counter
            if len(self.note_buffer) == 1:
                self.current_step = 0

    def remove_note(self, note):
        """
        Remove a note from the arpeggiator buffer

        Args:
            note: MIDI note number
        """
        # Remove from buffer
        self.note_buffer = [(n, v) for n, v in self.note_buffer if n != note]

        # Remove from order tracking
        if note in self.note_order:
            self.note_order.remove(note)

        # If we were playing this note, send note off
        if self.current_note == note:
            self.midi_io.send_note_off(note, self.settings.midi_channel)
            self.current_note = None

        # Regenerate sequence
        self._generate_sequence()

        # Reset step if buffer is empty
        if not self.note_buffer:
            self.current_step = 0
            self.step_sequence = []

    def clear_notes(self):
        """Clear all notes from the buffer"""
        # Send note off for currently playing note
        if self.current_note is not None:
            self.midi_io.send_note_off(self.current_note, self.settings.midi_channel)
            self.current_note = None

        self.note_buffer = []
        self.note_order = []
        self.step_sequence = []
        self.current_step = 0

    def _generate_sequence(self):
        """Generate the note sequence based on current pattern and settings"""
        if not self.note_buffer:
            self.step_sequence = []
            return

        # Sort notes by pitch
        sorted_notes = sorted(self.note_buffer, key=lambda x: x[0])

        # Expand notes across octaves if needed
        expanded_notes = []
        for octave in range(self.settings.octave_range):
            for note, velocity in sorted_notes:
                transposed_note = note + (octave * 12)
                if transposed_note <= 127:  # Stay within MIDI range
                    expanded_notes.append((transposed_note, velocity))

        # Generate sequence based on pattern
        if self.settings.pattern == self.settings.ARP_UP:
            self.step_sequence = expanded_notes

        elif self.settings.pattern == self.settings.ARP_DOWN:
            self.step_sequence = list(reversed(expanded_notes))

        elif self.settings.pattern == self.settings.ARP_UP_DOWN:
            # Up then down, don't repeat top/bottom notes
            if len(expanded_notes) > 1:
                self.step_sequence = expanded_notes + list(reversed(expanded_notes[1:-1]))
            else:
                self.step_sequence = expanded_notes

        elif self.settings.pattern == self.settings.ARP_DOWN_UP:
            # Down then up, don't repeat top/bottom notes
            if len(expanded_notes) > 1:
                reversed_notes = list(reversed(expanded_notes))
                self.step_sequence = reversed_notes + expanded_notes[1:-1]
            else:
                self.step_sequence = list(reversed(expanded_notes))

        elif self.settings.pattern == self.settings.ARP_RANDOM:
            # Random order (will randomize on each step)
            self.step_sequence = expanded_notes

        elif self.settings.pattern == self.settings.ARP_AS_PLAYED:
            # Use the order notes were received
            as_played = []
            for note_num in self.note_order:
                # Find the note in buffer
                for note, velocity in self.note_buffer:
                    if note == note_num:
                        # Add across octaves
                        for octave in range(self.settings.octave_range):
                            transposed_note = note + (octave * 12)
                            if transposed_note <= 127:
                                as_played.append((transposed_note, velocity))
                        break
            self.step_sequence = as_played

        # Wrap step position if needed
        if self.step_sequence and self.current_step >= len(self.step_sequence):
            self.current_step = 0

    def step(self):
        """
        Advance the arpeggiator by one step
        Called by the clock handler on each timing division
        """
        # Do nothing if arp is disabled or no notes to play
        if not self.settings.enabled or not self.step_sequence:
            return

        # Turn off previous note if still playing
        if self.current_note is not None:
            self.midi_io.send_note_off(self.current_note, self.settings.midi_channel)

        # For random mode, pick a random note each time
        if self.settings.pattern == self.settings.ARP_RANDOM:
            note, velocity = random.choice(self.step_sequence)
        else:
            # Get next note in sequence
            note, velocity = self.step_sequence[self.current_step]

        # Use fixed or original velocity
        if not self.settings.velocity_passthrough:
            velocity = self.settings.fixed_velocity

        # Play the note
        self.midi_io.send_note_on(note, velocity, self.settings.midi_channel)
        self.current_note = note

        # Advance step counter
        self.current_step = (self.current_step + 1) % len(self.step_sequence)

    def process_midi_message(self, msg):
        """
        Process an incoming MIDI message

        Args:
            msg: MIDI message object
        """
        # Only process messages on the configured channel
        # Note: Some MIDI messages don't have a channel attribute
        if hasattr(msg, 'channel') and msg.channel != self.settings.midi_channel:
            return

        if isinstance(msg, NoteOn):
            if msg.velocity > 0:
                self.add_note(msg.note, msg.velocity)
            else:
                # Velocity 0 is note off
                if not self.settings.latch:
                    self.remove_note(msg.note)

        elif isinstance(msg, NoteOff):
            if not self.settings.latch:
                self.remove_note(msg.note)

    def panic(self):
        """Stop all notes immediately"""
        if self.current_note is not None:
            self.midi_io.send_note_off(self.current_note, self.settings.midi_channel)
            self.current_note = None

    def get_status(self):
        """
        Get current arpeggiator status

        Returns:
            Dictionary with status information
        """
        return {
            'enabled': self.settings.enabled,
            'pattern': self.settings.get_pattern_name(),
            'notes_held': len(self.note_buffer),
            'sequence_length': len(self.step_sequence),
            'current_step': self.current_step,
            'latch': self.settings.latch
        }
