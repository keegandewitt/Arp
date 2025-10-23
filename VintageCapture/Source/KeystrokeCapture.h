/*
  ==============================================================================

    KeystrokeCapture.h

    Records MIDI performance data (notes, velocity, timing).
    Stage 1 of the VintageCapture workflow.

  ==============================================================================
*/

#pragma once

#include <vector>
#include <cstdint>

namespace VintageCapture {

/**
 * A single MIDI note event with timing
 */
struct KeystrokeEvent {
    double timestamp;       // Seconds from capture start
    uint8_t note;          // MIDI note number (0-127)
    uint8_t velocity;      // Note velocity (0-127)
    bool isNoteOn;         // true = Note On, false = Note Off

    // Derived data (calculated after capture)
    double noteDuration;   // For Note Off events: how long the note was held
};

/**
 * Buffer of recorded keystrokes
 */
class KeystrokeBuffer {
public:
    KeystrokeBuffer();

    /**
     * Start recording keystrokes
     */
    void startCapture();

    /**
     * Stop recording keystrokes
     */
    void stopCapture();

    /**
     * Check if currently recording
     */
    bool isRecording() const { return recording; }

    /**
     * Record a MIDI event
     * @param note MIDI note number
     * @param velocity Note velocity
     * @param isNoteOn true for Note On, false for Note Off
     * @param timestamp Current time in seconds (from host)
     */
    void recordEvent(uint8_t note, uint8_t velocity, bool isNoteOn, double timestamp);

    /**
     * Get all recorded events
     */
    const std::vector<KeystrokeEvent>& getEvents() const { return events; }

    /**
     * Get number of events recorded
     */
    size_t getEventCount() const { return events.size(); }

    /**
     * Get total duration of recording (in seconds)
     */
    double getDuration() const;

    /**
     * Clear all recorded events
     */
    void clear();

    /**
     * Calculate note durations (pairs Note On/Off events)
     * Call this after stopping capture
     */
    void calculateNoteDurations();

    /**
     * Get count of notes played (Note On events)
     */
    int getNoteCount() const;

private:
    std::vector<KeystrokeEvent> events;
    bool recording;
    double captureStartTime;
    double captureEndTime;
};

} // namespace VintageCapture
