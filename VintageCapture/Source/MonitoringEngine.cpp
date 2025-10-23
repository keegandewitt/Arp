/*
  ==============================================================================

    MonitoringEngine.cpp

    Implementation of zero-latency sample playback for monitoring.

  ==============================================================================
*/

#include "MonitoringEngine.h"
#include <algorithm>
#include <cmath>

namespace VintageCapture {

// ============================================================================
// MonitorVoice Implementation
// ============================================================================

MonitorVoice::MonitorVoice()
    : active(false), currentNote(0), velocityGain(1.0f),
      playbackPosition(0.0), pitchRatio(1.0), released(false), releaseGain(1.0f) {
}

void MonitorVoice::trigger(uint8_t note, uint8_t velocity,
                          const std::vector<float>& sample, double sampleRate) {
    currentNote = note;
    velocityGain = velocity / 127.0f;
    playbackPosition = 0.0;
    sampleData = sample;
    active = true;
    released = false;
    releaseGain = 1.0f;

    // Calculate pitch ratio (semitones from C3 = 60)
    int semitoneOffset = note - 60;  // C3 = MIDI note 60
    pitchRatio = std::pow(2.0, semitoneOffset / 12.0);  // 2^(semitones/12)
}

void MonitorVoice::release() {
    released = true;
}

float MonitorVoice::process(double sampleRate) {
    if (!active || sampleData.empty()) {
        return 0.0f;
    }

    // Linear interpolation for pitch shifting
    int index0 = static_cast<int>(playbackPosition);
    int index1 = index0 + 1;

    if (index1 >= static_cast<int>(sampleData.size())) {
        // End of sample
        active = false;
        return 0.0f;
    }

    float frac = static_cast<float>(playbackPosition - index0);
    float sample = sampleData[index0] * (1.0f - frac) + sampleData[index1] * frac;

    // Apply velocity
    sample *= velocityGain;

    // Apply release envelope if released
    if (released) {
        sample *= releaseGain;

        // Decay release gain
        float releaseDecay = 1.0f - (1.0f / (RELEASE_TIME * sampleRate));
        releaseGain *= releaseDecay;

        if (releaseGain < 0.001f) {
            active = false;
        }
    }

    // Advance playback position
    playbackPosition += pitchRatio;

    return sample;
}

// ============================================================================
// MonitoringEngine Implementation
// ============================================================================

MonitoringEngine::MonitoringEngine()
    : referenceSampleRate(44100.0), enabled(true) {
}

void MonitoringEngine::setReferenceSample(const std::vector<float>& sample, double sampleRate) {
    referenceSample = sample;
    referenceSampleRate = sampleRate;
}

void MonitoringEngine::noteOn(uint8_t note, uint8_t velocity) {
    if (!enabled || referenceSample.empty()) {
        return;
    }

    // Allocate a voice
    MonitorVoice* voice = allocateVoice();
    if (voice) {
        voice->trigger(note, velocity, referenceSample, referenceSampleRate);
    }
}

void MonitoringEngine::noteOff(uint8_t note) {
    if (!enabled) {
        return;
    }

    // Find and release the voice
    MonitorVoice* voice = findVoice(note);
    if (voice) {
        voice->release();
    }
}

void MonitoringEngine::allNotesOff() {
    for (int i = 0; i < MAX_VOICES; ++i) {
        voices[i].release();
    }
}

void MonitoringEngine::process(float* outputBuffer, int numSamples, double sampleRate) {
    if (!enabled) {
        // Fill with silence
        for (int i = 0; i < numSamples * 2; ++i) {
            outputBuffer[i] = 0.0f;
        }
        return;
    }

    // Process all voices and mix
    for (int sample = 0; sample < numSamples; ++sample) {
        float mixL = 0.0f;
        float mixR = 0.0f;

        // Sum all active voices
        for (int v = 0; v < MAX_VOICES; ++v) {
            if (voices[v].isActive()) {
                float voiceSample = voices[v].process(sampleRate);
                mixL += voiceSample;
                mixR += voiceSample;  // Mono for now
            }
        }

        // Write to stereo output (interleaved)
        outputBuffer[sample * 2] = mixL;
        outputBuffer[sample * 2 + 1] = mixR;
    }
}

MonitorVoice* MonitoringEngine::allocateVoice() {
    // First, try to find an inactive voice
    for (int i = 0; i < MAX_VOICES; ++i) {
        if (!voices[i].isActive()) {
            return &voices[i];
        }
    }

    // All voices active - steal the first one (simple voice stealing)
    return &voices[0];
}

MonitorVoice* MonitoringEngine::findVoice(uint8_t note) {
    for (int i = 0; i < MAX_VOICES; ++i) {
        if (voices[i].isActive() && voices[i].getNote() == note) {
            return &voices[i];
        }
    }
    return nullptr;
}

double MonitoringEngine::calculatePitchRatio(uint8_t note) {
    int semitoneOffset = note - 60;  // C3 = MIDI note 60
    return std::pow(2.0, semitoneOffset / 12.0);
}

} // namespace VintageCapture
