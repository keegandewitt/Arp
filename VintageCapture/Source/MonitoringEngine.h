/*
  ==============================================================================

    MonitoringEngine.h

    Zero-latency sample-based monitoring for vintage synth performance.
    Plays back pitched C3 samples when MIDI notes are received.

  ==============================================================================
*/

#pragma once

#include <vector>
#include <map>
#include <cstdint>
#include <cmath>

namespace VintageCapture {

/**
 * Voice for sample playback (one voice per active note)
 */
class MonitorVoice {
public:
    MonitorVoice();

    /**
     * Trigger this voice with a note
     */
    void trigger(uint8_t note, uint8_t velocity, const std::vector<float>& sample, double sampleRate);

    /**
     * Release this voice
     */
    void release();

    /**
     * Check if voice is active
     */
    bool isActive() const { return active; }

    /**
     * Process one sample and return output
     */
    float process(double sampleRate);

    /**
     * Get the note this voice is playing
     */
    uint8_t getNote() const { return currentNote; }

private:
    bool active;
    uint8_t currentNote;
    float velocityGain;
    double playbackPosition;  // Sample position (can be fractional)
    double pitchRatio;        // Playback speed for pitch shifting
    std::vector<float> sampleData;
    bool released;
    float releaseGain;  // Envelope for release

    static constexpr float RELEASE_TIME = 0.05f;  // 50ms release
};

/**
 * Polyphonic monitoring playback engine
 */
class MonitoringEngine {
public:
    MonitoringEngine();

    /**
     * Set the reference C3 sample
     */
    void setReferenceSample(const std::vector<float>& sample, double sampleRate);

    /**
     * Trigger a note (Note On)
     */
    void noteOn(uint8_t note, uint8_t velocity);

    /**
     * Release a note (Note Off)
     */
    void noteOff(uint8_t note);

    /**
     * All notes off (panic)
     */
    void allNotesOff();

    /**
     * Process audio and fill output buffer
     * @param outputBuffer Stereo output buffer (interleaved L/R)
     * @param numSamples Number of sample frames
     * @param sampleRate Current sample rate
     */
    void process(float* outputBuffer, int numSamples, double sampleRate);

    /**
     * Check if monitoring is enabled
     */
    bool isEnabled() const { return enabled; }

    /**
     * Enable/disable monitoring
     */
    void setEnabled(bool shouldBeEnabled) { enabled = shouldBeEnabled; }

private:
    static constexpr int MAX_VOICES = 16;

    std::vector<float> referenceSample;
    double referenceSampleRate;
    bool enabled;
    MonitorVoice voices[MAX_VOICES];

    /**
     * Find a free voice or steal the oldest
     */
    MonitorVoice* allocateVoice();

    /**
     * Find voice playing a specific note
     */
    MonitorVoice* findVoice(uint8_t note);

    /**
     * Calculate pitch ratio for a MIDI note (relative to C3 = 60)
     */
    double calculatePitchRatio(uint8_t note);
};

} // namespace VintageCapture
