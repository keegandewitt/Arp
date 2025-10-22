"""
MIDI I/O Handler for the first MIDI FeatherWing
Manages MIDI input and output for note data
"""

import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange


class MidiIO:
    """Handles MIDI input and output on the first FeatherWing"""

    def __init__(self, uart_in, uart_out):
        """
        Initialize MIDI I/O

        Args:
            uart_in: UART object for MIDI input
            uart_out: UART object for MIDI output
        """
        self.midi_in = adafruit_midi.MIDI(
            midi_in=uart_in,
            in_channel=0  # Listen to all channels, filter in code
        )

        self.midi_out = adafruit_midi.MIDI(
            midi_out=uart_out,
            out_channel=0  # Default channel, can be changed per message
        )

        # Track currently held notes (for passthrough when arp is off)
        self.held_notes = set()

        # MIDI activity tracking
        self.has_received_midi = False
        self.has_sent_midi = False

    def read_messages(self):
        """
        Read and return all available MIDI messages

        Returns:
            List of MIDI message objects
        """
        messages = []
        msg = self.midi_in.receive()

        while msg is not None:
            messages.append(msg)
            self.has_received_midi = True  # Flag that we received MIDI
            msg = self.midi_in.receive()

        return messages

    def get_and_clear_midi_activity(self):
        """
        Get MIDI activity status and reset flags

        Returns:
            Tuple of (has_received, has_sent)
        """
        received = self.has_received_midi
        sent = self.has_sent_midi

        # Clear flags
        self.has_received_midi = False
        self.has_sent_midi = False

        return (received, sent)

    def send_note_on(self, note, velocity, channel=0):
        """
        Send a Note On message

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)
            channel: MIDI channel (0-15)
        """
        self.midi_out.send(NoteOn(note, velocity), channel=channel)
        self.has_sent_midi = True  # Flag that we sent MIDI

    def send_note_off(self, note, channel=0):
        """
        Send a Note Off message

        Args:
            note: MIDI note number (0-127)
            channel: MIDI channel (0-15)
        """
        self.midi_out.send(NoteOff(note, 0), channel=channel)
        self.has_sent_midi = True  # Flag that we sent MIDI

    def send_cc(self, control, value, channel=0):
        """
        Send a Control Change message

        Args:
            control: CC number (0-127)
            value: CC value (0-127)
            channel: MIDI channel (0-15)
        """
        self.midi_out.send(ControlChange(control, value), channel=channel)
        self.has_sent_midi = True  # Flag that we sent MIDI

    def stop_all_notes(self, channel=0):
        """
        Send Note Off for all possible notes (panic function)

        Args:
            channel: MIDI channel (0-15)
        """
        for note in range(128):
            self.send_note_off(note, channel)

        self.held_notes.clear()

    def process_passthrough(self, messages, channel=0):
        """
        Pass MIDI messages through unchanged (for when arp is disabled)

        Args:
            messages: List of MIDI messages to pass through
            channel: MIDI channel to output on (0-15)
        """
        for msg in messages:
            if isinstance(msg, NoteOn):
                if msg.velocity > 0:
                    self.held_notes.add(msg.note)
                    self.send_note_on(msg.note, msg.velocity, channel)
                else:
                    # Velocity 0 is equivalent to Note Off
                    if msg.note in self.held_notes:
                        self.held_notes.remove(msg.note)
                    self.send_note_off(msg.note, channel)

            elif isinstance(msg, NoteOff):
                if msg.note in self.held_notes:
                    self.held_notes.remove(msg.note)
                self.send_note_off(msg.note, channel)
