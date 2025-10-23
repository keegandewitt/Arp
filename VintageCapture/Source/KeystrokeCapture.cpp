/*
  ==============================================================================

    KeystrokeCapture.cpp

    Implementation of MIDI keystroke recording.

  ==============================================================================
*/

#include "KeystrokeCapture.h"
#include <algorithm>
#include <map>

namespace VintageCapture {

KeystrokeBuffer::KeystrokeBuffer()
    : recording(false), captureStartTime(0.0), captureEndTime(0.0) {
}

void KeystrokeBuffer::startCapture() {
    events.clear();
    recording = true;
    captureStartTime = 0.0;
    captureEndTime = 0.0;
}

void KeystrokeBuffer::stopCapture() {
    recording = false;
    calculateNoteDurations();
}

void KeystrokeBuffer::recordEvent(uint8_t note, uint8_t velocity, bool isNoteOn, double timestamp) {
    if (!recording) {
        return;
    }

    // First event sets start time
    if (events.empty()) {
        captureStartTime = timestamp;
    }

    KeystrokeEvent event;
    event.timestamp = timestamp - captureStartTime; // Relative to capture start
    event.note = note;
    event.velocity = velocity;
    event.isNoteOn = isNoteOn;
    event.noteDuration = 0.0;

    events.push_back(event);
    captureEndTime = event.timestamp;
}

double KeystrokeBuffer::getDuration() const {
    if (events.empty()) {
        return 0.0;
    }
    return captureEndTime;
}

void KeystrokeBuffer::clear() {
    events.clear();
    recording = false;
    captureStartTime = 0.0;
    captureEndTime = 0.0;
}

void KeystrokeBuffer::calculateNoteDurations() {
    // Map of active notes (note number -> Note On event index)
    std::map<uint8_t, size_t> activeNotes;

    for (size_t i = 0; i < events.size(); ++i) {
        auto& event = events[i];

        if (event.isNoteOn && event.velocity > 0) {
            // Note On - add to active notes
            activeNotes[event.note] = i;
        } else {
            // Note Off (or Note On with velocity 0)
            auto it = activeNotes.find(event.note);
            if (it != activeNotes.end()) {
                // Found matching Note On
                size_t noteOnIndex = it->second;
                auto& noteOnEvent = events[noteOnIndex];

                // Calculate duration
                double duration = event.timestamp - noteOnEvent.timestamp;
                event.noteDuration = duration;

                // Remove from active notes
                activeNotes.erase(it);
            }
        }
    }
}

int KeystrokeBuffer::getNoteCount() const {
    int count = 0;
    for (const auto& event : events) {
        if (event.isNoteOn && event.velocity > 0) {
            count++;
        }
    }
    return count;
}

} // namespace VintageCapture
