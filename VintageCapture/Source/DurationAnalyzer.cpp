/*
  ==============================================================================

    DurationAnalyzer.cpp

    Implementation of attack/release time detection from audio analysis.

  ==============================================================================
*/

#include "DurationAnalyzer.h"
#include <cmath>
#include <algorithm>
#include <numeric>

namespace VintageCapture {

TimingProfile DurationAnalyzer::analyze(const float* samples,
                                       int numSamples,
                                       double sampleRate,
                                       int noteOffSample) {
    TimingProfile profile;
    profile.attackTime = 0.0f;
    profile.releaseTime = 0.0f;
    profile.peakLevel = 0.0f;

    if (numSamples <= 0 || sampleRate <= 0.0) {
        return profile; // Invalid input
    }

    // Calculate RMS envelope
    lastEnvelope = calculateRMSEnvelope(samples, numSamples, sampleRate);

    if (lastEnvelope.empty()) {
        return profile; // Failed to calculate envelope
    }

    // Find peak level
    profile.peakLevel = findPeak(lastEnvelope);

    if (profile.peakLevel < SILENCE_THRESHOLD) {
        return profile; // Signal too quiet
    }

    // Calculate attack time (0 to 90% of peak)
    float attackThreshold = profile.peakLevel * ATTACK_THRESHOLD;
    int attackEndIndex = findFirstAbove(lastEnvelope, attackThreshold);

    if (attackEndIndex >= 0) {
        profile.attackTime = static_cast<float>(attackEndIndex) / static_cast<float>(envelopeSampleRate);
    }

    // Detect or use provided note-off point
    int noteOffIndex = noteOffSample;
    if (noteOffIndex < 0) {
        noteOffIndex = detectNoteOffPoint(lastEnvelope, profile.peakLevel);
    } else {
        // Convert from audio sample index to envelope index
        int windowSize = static_cast<int>(sampleRate * ENVELOPE_WINDOW_MS / 1000.0f);
        int hopSize = windowSize / 2;
        noteOffIndex = noteOffIndex / hopSize;
    }

    // Calculate release time (note-off to 10% of peak)
    if (noteOffIndex >= 0 && noteOffIndex < static_cast<int>(lastEnvelope.size())) {
        float releaseThreshold = profile.peakLevel * RELEASE_THRESHOLD;
        int releaseEndIndex = findFirstBelow(lastEnvelope, releaseThreshold, noteOffIndex);

        if (releaseEndIndex >= 0) {
            int releaseDuration = releaseEndIndex - noteOffIndex;
            profile.releaseTime = static_cast<float>(releaseDuration) / static_cast<float>(envelopeSampleRate);
        } else {
            // Release didn't reach threshold before end of recording
            // Use remaining duration as estimate
            int releaseDuration = static_cast<int>(lastEnvelope.size()) - noteOffIndex;
            profile.releaseTime = static_cast<float>(releaseDuration) / static_cast<float>(envelopeSampleRate);
        }
    }

    return profile;
}

std::vector<float> DurationAnalyzer::calculateRMSEnvelope(const float* samples,
                                                         int numSamples,
                                                         double sampleRate) {
    std::vector<float> envelope;

    // Window size in samples (e.g., 10ms at 44.1kHz = 441 samples)
    int windowSize = static_cast<int>(sampleRate * ENVELOPE_WINDOW_MS / 1000.0f);
    int hopSize = windowSize / 2; // 50% overlap

    if (windowSize <= 0 || numSamples < windowSize) {
        return envelope;
    }

    // Calculate envelope sample rate
    envelopeSampleRate = sampleRate / static_cast<double>(hopSize);

    // Reserve space for efficiency
    envelope.reserve(numSamples / hopSize);

    // Sliding window RMS calculation
    for (int i = 0; i + windowSize <= numSamples; i += hopSize) {
        float sumSquares = 0.0f;

        // Calculate sum of squares in window
        for (int j = 0; j < windowSize; ++j) {
            float sample = samples[i + j];
            sumSquares += sample * sample;
        }

        // RMS = sqrt(mean(squares))
        float rms = std::sqrt(sumSquares / static_cast<float>(windowSize));
        envelope.push_back(rms);
    }

    return envelope;
}

int DurationAnalyzer::findFirstAbove(const std::vector<float>& envelope,
                                    float threshold,
                                    int startIndex) {
    for (int i = startIndex; i < static_cast<int>(envelope.size()); ++i) {
        if (envelope[i] >= threshold) {
            return i;
        }
    }
    return -1; // Not found
}

int DurationAnalyzer::findFirstBelow(const std::vector<float>& envelope,
                                    float threshold,
                                    int startIndex) {
    for (int i = startIndex; i < static_cast<int>(envelope.size()); ++i) {
        if (envelope[i] <= threshold) {
            return i;
        }
    }
    return -1; // Not found
}

float DurationAnalyzer::findPeak(const std::vector<float>& envelope) {
    if (envelope.empty()) {
        return 0.0f;
    }

    return *std::max_element(envelope.begin(), envelope.end());
}

int DurationAnalyzer::detectNoteOffPoint(const std::vector<float>& envelope,
                                        float peakLevel) {
    if (envelope.empty()) {
        return -1;
    }

    // Find the peak index
    auto peakIt = std::max_element(envelope.begin(), envelope.end());
    int peakIndex = static_cast<int>(std::distance(envelope.begin(), peakIt));

    // Strategy: Find the longest "stable" region after the peak
    // This is likely the sustain portion. Release starts after that.

    const int windowSize = 10; // Look at 10-sample windows
    const float stabilityThreshold = 0.05f; // Max 5% variation in stable region

    int longestStableStart = peakIndex;
    int longestStableLength = 0;
    int currentStableStart = peakIndex;
    int currentStableLength = 0;

    for (int i = peakIndex; i + windowSize < static_cast<int>(envelope.size()); ++i) {
        // Calculate variation in this window
        float minVal = *std::min_element(envelope.begin() + i, envelope.begin() + i + windowSize);
        float maxVal = *std::max_element(envelope.begin() + i, envelope.begin() + i + windowSize);
        float variation = (maxVal - minVal) / peakLevel;

        if (variation < stabilityThreshold) {
            // Stable region
            currentStableLength++;
            if (currentStableLength > longestStableLength) {
                longestStableLength = currentStableLength;
                longestStableStart = currentStableStart;
            }
        } else {
            // Unstable region - reset counter
            currentStableStart = i + 1;
            currentStableLength = 0;
        }
    }

    // Note-off point is at the end of the longest stable region
    int noteOffPoint = longestStableStart + longestStableLength;

    // Sanity check: Make sure we're not too close to the end
    if (noteOffPoint >= static_cast<int>(envelope.size()) - 10) {
        // Use 60% through as fallback (user likely held note most of the time)
        noteOffPoint = static_cast<int>(envelope.size() * 0.6f);
    }

    return noteOffPoint;
}

} // namespace VintageCapture
