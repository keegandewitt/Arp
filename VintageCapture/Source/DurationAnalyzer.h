/*
  ==============================================================================

    DurationAnalyzer.h

    Analyzes a recorded C3 note to detect attack and release times.
    This tells us the sonic duration characteristics of the vintage synth.

  ==============================================================================
*/

#pragma once

#include <vector>
#include <algorithm>
#include <cmath>

namespace VintageCapture {

/**
 * Result of analyzing a C3 calibration recording
 */
struct TimingProfile {
    float attackTime;      // Seconds from note-on to 90% peak
    float releaseTime;     // Seconds from note-off to 10% peak
    float peakLevel;       // Peak RMS level (for reference)

    /**
     * Calculate total sonic duration for a MIDI note
     * @param midiDuration How long the key was held (in seconds)
     * @return Total time the note will sound (including release tail)
     */
    float calculateSonicDuration(float midiDuration) const {
        return midiDuration + releaseTime;
    }

    /**
     * Check if analysis was successful
     */
    bool isValid() const {
        return attackTime > 0.0f && releaseTime > 0.0f && peakLevel > 0.0f;
    }
};

/**
 * Analyzes audio recordings to extract timing characteristics
 */
class DurationAnalyzer {
public:
    DurationAnalyzer() = default;

    /**
     * Analyze a C3 calibration recording to detect attack/release times
     *
     * @param samples Mono audio buffer containing C3 note
     * @param numSamples Length of buffer
     * @param sampleRate Sample rate of the recording
     * @param noteOffSample Sample index where key was released (if known, -1 otherwise)
     * @return TimingProfile with detected characteristics
     */
    TimingProfile analyze(const float* samples,
                         int numSamples,
                         double sampleRate,
                         int noteOffSample = -1);

    /**
     * Get the last calculated RMS envelope for visualization
     */
    const std::vector<float>& getLastEnvelope() const { return lastEnvelope; }

    /**
     * Get envelope sample rate (may be downsampled from audio rate)
     */
    double getEnvelopeSampleRate() const { return envelopeSampleRate; }

private:
    // Configuration
    static constexpr float ENVELOPE_WINDOW_MS = 10.0f;  // 10ms RMS window
    static constexpr float ATTACK_THRESHOLD = 0.9f;     // 90% of peak
    static constexpr float RELEASE_THRESHOLD = 0.1f;    // 10% of peak
    static constexpr float SILENCE_THRESHOLD = 0.001f;  // -60dB

    // Results from last analysis (for visualization)
    std::vector<float> lastEnvelope;
    double envelopeSampleRate;

    /**
     * Calculate RMS envelope of audio with sliding window
     */
    std::vector<float> calculateRMSEnvelope(const float* samples,
                                           int numSamples,
                                           double sampleRate);

    /**
     * Find sample index where envelope first crosses threshold
     */
    int findFirstAbove(const std::vector<float>& envelope, float threshold, int startIndex = 0);

    /**
     * Find sample index where envelope first drops below threshold (searching forward)
     */
    int findFirstBelow(const std::vector<float>& envelope, float threshold, int startIndex = 0);

    /**
     * Find the peak value in envelope
     */
    float findPeak(const std::vector<float>& envelope);

    /**
     * Detect where the note-off occurred (if not provided)
     * Looks for the start of the decay/release portion
     */
    int detectNoteOffPoint(const std::vector<float>& envelope, float peakLevel);
};

} // namespace VintageCapture
