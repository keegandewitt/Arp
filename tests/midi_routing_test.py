"""
MIDI Routing Test - Simple Pass-Through + Basic Arpeggiator
Tests MIDI FeatherWing routing without complex module dependencies
Follows CircuitPython crash prevention patterns from mastery guide
"""

import board
import busio
import time
import gc
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend

print("\n" + "="*60)
print("MIDI ROUTING TEST")
print("="*60)
print("\nMode: Pass-through with note echo")
print("- Note ON/OFF → Echoed back immediately")
print("- CC, Pitch Bend, etc. → Passed through")
print("\nSetup: MIDI Keyboard → MIDI IN, MIDI OUT → Synth")
print("="*60 + "\n")

# Initialize UART MIDI
print("[1/2] Initializing MIDI...")
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
midi = MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)
print("      ✓ MIDI ready\n")

# Pre-allocate note buffer (NO allocations in loop!)
note_buffer = []  # Will hold (note, velocity) tuples
MAX_NOTES = 16  # Prevent unbounded growth

# Performance counters
notes_received = 0
notes_sent = 0
messages_passed = 0

# Memory monitoring
gc.collect()
initial_mem = gc.mem_free()
print(f"[2/2] Memory: {initial_mem} bytes free")
print("="*60)
print("\nListening for MIDI... (Ctrl+C to stop)\n")

# Main loop - following crash prevention patterns
loop_count = 0
gc_interval = 100  # GC every 100 loops

try:
    while True:
        loop_count += 1

        # Process MIDI input
        msg = midi.receive()

        if msg is not None:
            # Note ON
            if isinstance(msg, NoteOn) and msg.velocity > 0:
                notes_received += 1

                # Add to buffer (with bounds check!)
                if len(note_buffer) < MAX_NOTES:
                    if not any(n == msg.note for n, v in note_buffer):
                        note_buffer.append((msg.note, msg.velocity))

                # Echo note back immediately
                midi.send(NoteOn(msg.note, msg.velocity))
                notes_sent += 1
                print(f"Note ON:  {msg.note:3d} vel {msg.velocity:3d} | Buffer: {[n for n,v in note_buffer]}")

            # Note OFF
            elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
                # Remove from buffer (safe removal)
                note_buffer = [(n, v) for n, v in note_buffer if n != msg.note]

                # Echo note off
                midi.send(NoteOff(msg.note, 0))
                notes_sent += 1
                print(f"Note OFF: {msg.note:3d}         | Buffer: {[n for n,v in note_buffer]}")

            # Pass through other messages
            else:
                try:
                    midi.send(msg)
                    messages_passed += 1

                    # Log important messages only (not chatty ones)
                    if isinstance(msg, ControlChange):
                        print(f"CC#{msg.control:3d} = {msg.value:3d}")
                    elif isinstance(msg, PitchBend):
                        print(f"PitchBend: {msg.pitch_bend}")
                except Exception as e:
                    print(f"⚠️  Pass-through failed: {type(msg).__name__}: {e}")

        # Periodic garbage collection (following mastery guide)
        if loop_count % gc_interval == 0:
            gc.collect()

        # Small delay to prevent CPU spinning
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\n\n" + "="*60)
    print("ROUTING TEST STOPPED")
    print("="*60)
    print(f"Notes received:     {notes_received}")
    print(f"Notes sent:         {notes_sent}")
    print(f"Messages passed:    {messages_passed}")
    print(f"Final buffer size:  {len(note_buffer)}")

    # Memory report
    gc.collect()
    final_mem = gc.mem_free()
    mem_used = initial_mem - final_mem
    print(f"\nMemory: {final_mem} bytes free ({mem_used} bytes used)")
    print("="*60 + "\n")
