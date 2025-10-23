"""
MIDI Clock Handler
Manages timing from both external MIDI clock and internal clock sources
"""

import time
import adafruit_midi
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.midi_continue import Continue


class ClockHandler:
    """Handles clock synchronization from external MIDI or internal generator"""

    # Clock source constants
    CLOCK_INTERNAL = 0
    CLOCK_EXTERNAL = 1

    def __init__(self, midi_in_port=None):
        """
        Initialize clock handler

        Args:
            midi_in_port: MIDI input port for clock messages (UART or usb_midi.ports[])
                         If None, external clock will not be available (internal only)
        """
        self.midi_clock = None
        if midi_in_port is not None:
            self.midi_clock = adafruit_midi.MIDI(
                midi_in=midi_in_port,
                in_channel=0  # Clock messages are channel-independent
            )

        # Clock state
        self.running = False
        self.tick_count = 0
        self.ticks_per_step = 6  # Default to 16th notes (24 PPQN / 4)

        # Callback for when a step should trigger
        self.on_step_callback = None

        # BPM calculation (for external clock)
        self.bpm = None
        self.displayed_bpm = None  # Last BPM shown to user (for stability)
        self.last_tick_time = None
        self.tick_intervals = []  # Store recent intervals for averaging
        self.max_intervals = 96  # Average over 96 ticks (4 beats at 24 PPQN) for stability
        self.bpm_update_threshold = 5  # Only update displayed BPM if change is >= 5 BPM

        # Internal clock
        self.clock_source = self.CLOCK_INTERNAL  # Default to internal
        self.internal_bpm = 120  # Default internal BPM
        self.last_internal_tick = None
        self.internal_tick_interval = self._calculate_tick_interval(self.internal_bpm)

    def _calculate_tick_interval(self, bpm):
        """
        Calculate the time interval between clock ticks for a given BPM

        Args:
            bpm: Beats per minute

        Returns:
            Interval in seconds between ticks (24 PPQN)
        """
        # 24 ticks per quarter note, 60 seconds per minute
        return 60.0 / (bpm * 24)

    def set_clock_division(self, division):
        """
        Set the clock division

        Args:
            division: Number of MIDI clock ticks per arp step
                     6 = 16th notes, 12 = 8th notes, 24 = quarter notes
        """
        self.ticks_per_step = division

    def set_step_callback(self, callback):
        """
        Set the callback function to call on each arp step

        Args:
            callback: Function to call with no arguments
        """
        self.on_step_callback = callback

    def set_clock_source(self, source):
        """
        Set the clock source

        Args:
            source: CLOCK_INTERNAL or CLOCK_EXTERNAL
        """
        self.clock_source = source
        if source == self.CLOCK_INTERNAL:
            # Start internal clock automatically
            self.running = True
            self.last_internal_tick = time.monotonic()
            self.tick_count = 0
            print("Switched to internal clock")
        else:
            # External clock requires Start message
            self.running = False
            self.tick_count = 0
            print("Switched to external clock")

    def set_internal_bpm(self, bpm):
        """
        Set the internal clock BPM

        Args:
            bpm: Beats per minute (typically 40-240)
        """
        self.internal_bpm = max(40, min(240, bpm))  # Clamp to reasonable range
        self.internal_tick_interval = self._calculate_tick_interval(self.internal_bpm)

    def get_clock_source(self):
        """Get the current clock source"""
        return self.clock_source

    def get_clock_source_name(self):
        """Get human-readable clock source name"""
        return "Internal" if self.clock_source == self.CLOCK_INTERNAL else "External"

    def process_clock_messages(self):
        """
        Process clock - either from internal generator or external MIDI
        Calls step callback when appropriate
        """
        if self.clock_source == self.CLOCK_INTERNAL:
            # Internal clock generation
            self._process_internal_clock()
        else:
            # External MIDI clock
            self._process_external_clock()

    def _process_internal_clock(self):
        """Generate internal clock ticks based on BPM with drift compensation"""
        if not self.running:
            return

        current_time = time.monotonic()

        # Initialize timing on first run
        if self.last_internal_tick is None:
            self.last_internal_tick = current_time
            return

        # Check if it's time for next tick
        elapsed = current_time - self.last_internal_tick
        if elapsed >= self.internal_tick_interval:
            # Compensate for timing drift by adding the exact interval
            # rather than resetting to current_time
            self.last_internal_tick += self.internal_tick_interval
            self.tick_count += 1

            # Check if we should trigger a step
            if self.tick_count >= self.ticks_per_step:
                self.tick_count = 0

                # Trigger step callback
                if self.on_step_callback:
                    self.on_step_callback()

    def _process_external_clock(self):
        """Process incoming MIDI clock messages"""
        if self.midi_clock is None:
            # No external clock source available
            return

        msg = self.midi_clock.receive()

        while msg is not None:
            if isinstance(msg, Start):
                # Start message received
                self.running = True
                self.tick_count = 0
                print("MIDI Clock: Start")

            elif isinstance(msg, Stop):
                # Stop message received
                self.running = False
                self.tick_count = 0
                print("MIDI Clock: Stop")

            elif isinstance(msg, Continue):
                # Continue message received
                self.running = True
                print("MIDI Clock: Continue")

            elif isinstance(msg, TimingClock):
                # Clock tick received
                if self.running:
                    # Calculate BPM
                    current_time = time.monotonic()
                    if self.last_tick_time is not None:
                        interval = current_time - self.last_tick_time

                        # Detect tempo change: if interval is very different from average, clear buffer
                        if len(self.tick_intervals) >= 12:
                            avg_interval = sum(self.tick_intervals) / len(self.tick_intervals)
                            # If new interval differs by more than 15% from average, tempo changed
                            if abs(interval - avg_interval) > (avg_interval * 0.15):
                                print(f"Tempo change detected - clearing buffer (interval: {interval:.4f}s, avg: {avg_interval:.4f}s)")
                                self.tick_intervals = []
                                self.displayed_bpm = None

                        self.tick_intervals.append(interval)

                        # Keep only recent intervals
                        if len(self.tick_intervals) > self.max_intervals:
                            self.tick_intervals.pop(0)

                        # Debug: print buffer status every 24 ticks
                        if len(self.tick_intervals) % 24 == 0:
                            print(f"Buffer: {len(self.tick_intervals)} samples")

                        # Calculate average interval and BPM
                        if len(self.tick_intervals) >= 12:  # Need at least half a beat of samples
                            avg_interval = sum(self.tick_intervals) / len(self.tick_intervals)
                            # BPM = 60 / (avg_interval * 24) since 24 PPQN
                            calculated_bpm = 60.0 / (avg_interval * 24)

                            # Round to nearest integer for stability
                            rounded_bpm = round(calculated_bpm)

                            # Only update displayed BPM if change is significant (hysteresis)
                            if self.displayed_bpm is None:
                                self.displayed_bpm = rounded_bpm
                                self.bpm = rounded_bpm
                                print(f"External BPM: {self.bpm}")
                            elif abs(rounded_bpm - self.displayed_bpm) >= self.bpm_update_threshold:
                                self.displayed_bpm = rounded_bpm
                                self.bpm = rounded_bpm
                                print(f"External BPM: {self.bpm}")
                            else:
                                # Keep the stable displayed value
                                self.bpm = self.displayed_bpm

                    self.last_tick_time = current_time

                    self.tick_count += 1

                    # Check if we should trigger a step
                    if self.tick_count >= self.ticks_per_step:
                        self.tick_count = 0

                        # Trigger step callback
                        if self.on_step_callback:
                            self.on_step_callback()

            # Get next message
            msg = self.midi_clock.receive()

    def reset(self):
        """Reset clock state"""
        self.running = False
        self.tick_count = 0
        self.bpm = None
        self.displayed_bpm = None
        self.last_tick_time = None
        self.tick_intervals = []
        self.last_internal_tick = None

    def is_running(self):
        """Check if clock is currently running"""
        return self.running

    def get_bpm(self):
        """
        Get the current BPM (internal or calculated from external)

        Returns:
            BPM as float, or None if not yet calculated (external only)
        """
        if self.clock_source == self.CLOCK_INTERNAL:
            return self.internal_bpm
        else:
            return self.bpm

    def start(self):
        """Start the clock (mainly for internal clock)"""
        self.running = True
        if self.clock_source == self.CLOCK_INTERNAL:
            self.last_internal_tick = time.monotonic()
            self.tick_count = 0

    def stop(self):
        """Stop the clock (mainly for internal clock)"""
        self.running = False
        self.tick_count = 0
