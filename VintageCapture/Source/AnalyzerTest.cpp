/*
  ==============================================================================

    AnalyzerTest.cpp

    Standalone test program for DurationAnalyzer.
    Generates test signals and validates analysis.

  ==============================================================================
*/

#include "DurationAnalyzer.h"
#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace VintageCapture;

// Generate a synthetic ADSR envelope for testing
std::vector<float> generateTestSignal(double sampleRate,
                                     float attackTime,
                                     float decayTime,
                                     float sustainLevel,
                                     float releaseTime,
                                     float holdTime) {
    int attackSamples = static_cast<int>(attackTime * sampleRate);
    int decaySamples = static_cast<int>(decayTime * sampleRate);
    int holdSamples = static_cast<int>(holdTime * sampleRate);
    int releaseSamples = static_cast<int>(releaseTime * sampleRate);

    int totalSamples = attackSamples + decaySamples + holdSamples + releaseSamples;
    std::vector<float> signal(totalSamples);

    int pos = 0;

    // Attack phase (0 -> 1.0)
    for (int i = 0; i < attackSamples; ++i, ++pos) {
        float phase = static_cast<float>(i) / static_cast<float>(attackSamples);
        float envelope = phase;

        // Add some frequency content (440 Hz tone)
        float tone = std::sin(2.0f * M_PI * 440.0f * static_cast<float>(pos) / static_cast<float>(sampleRate));
        signal[pos] = envelope * tone;
    }

    // Decay phase (1.0 -> sustainLevel)
    for (int i = 0; i < decaySamples; ++i, ++pos) {
        float phase = static_cast<float>(i) / static_cast<float>(decaySamples);
        float envelope = 1.0f - (phase * (1.0f - sustainLevel));

        float tone = std::sin(2.0f * M_PI * 440.0f * static_cast<float>(pos) / static_cast<float>(sampleRate));
        signal[pos] = envelope * tone;
    }

    // Hold/Sustain phase (constant sustainLevel)
    for (int i = 0; i < holdSamples; ++i, ++pos) {
        float envelope = sustainLevel;

        float tone = std::sin(2.0f * M_PI * 440.0f * static_cast<float>(pos) / static_cast<float>(sampleRate));
        signal[pos] = envelope * tone;
    }

    // Release phase (sustainLevel -> 0)
    for (int i = 0; i < releaseSamples; ++i, ++pos) {
        float phase = static_cast<float>(i) / static_cast<float>(releaseSamples);
        float envelope = sustainLevel * (1.0f - phase);

        float tone = std::sin(2.0f * M_PI * 440.0f * static_cast<float>(pos) / static_cast<float>(sampleRate));
        signal[pos] = envelope * tone;
    }

    return signal;
}

void runTest(const std::string& testName,
            float expectedAttack,
            float expectedRelease,
            float attackTime,
            float decayTime,
            float sustainLevel,
            float releaseTime,
            float holdTime) {
    const double sampleRate = 44100.0;

    std::cout << "\n=== " << testName << " ===" << std::endl;
    std::cout << "Generating test signal..." << std::endl;
    std::cout << "  Expected attack:  " << std::fixed << std::setprecision(3) << expectedAttack << "s" << std::endl;
    std::cout << "  Expected release: " << expectedRelease << "s" << std::endl;

    // Generate test signal
    auto signal = generateTestSignal(sampleRate, attackTime, decayTime, sustainLevel, releaseTime, holdTime);

    // Calculate note-off sample (after attack + decay + hold)
    int noteOffSample = static_cast<int>((attackTime + decayTime + holdTime) * sampleRate);

    // Analyze
    DurationAnalyzer analyzer;
    TimingProfile profile = analyzer.analyze(signal.data(), signal.size(), sampleRate, noteOffSample);

    // Display results
    std::cout << "\nAnalysis Results:" << std::endl;
    std::cout << "  Detected attack:  " << profile.attackTime << "s" << std::endl;
    std::cout << "  Detected release: " << profile.releaseTime << "s" << std::endl;
    std::cout << "  Peak level:       " << profile.peakLevel << std::endl;

    // Validate
    float attackError = std::abs(profile.attackTime - expectedAttack);
    float releaseError = std::abs(profile.releaseTime - expectedRelease);

    // Tolerance: 50ms for attack (usually fast), 15% for release (can be long)
    const float attackTolerance = 0.05f; // 50ms
    const float releaseTolerance = std::max(0.05f, expectedRelease * 0.15f); // 50ms or 15%, whichever is larger

    bool attackPass = attackError < attackTolerance;
    bool releasePass = releaseError < releaseTolerance;

    std::cout << "\nValidation:" << std::endl;
    std::cout << "  Attack:  " << (attackPass ? "PASS" : "FAIL") << " (error: " << (attackError * 1000.0f) << "ms)" << std::endl;
    std::cout << "  Release: " << (releasePass ? "PASS" : "FAIL") << " (error: " << (releaseError * 1000.0f) << "ms)" << std::endl;

    if (attackPass && releasePass) {
        std::cout << "\n✓ Test PASSED" << std::endl;
    } else {
        std::cout << "\n✗ Test FAILED" << std::endl;
    }
}

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "  VintageCapture Duration Analyzer Test" << std::endl;
    std::cout << "========================================" << std::endl;

    // Test 1: Fast attack, long release (typical synth pad)
    runTest("Synth Pad (Fast Attack, Long Release)",
            0.1f,   // Expected attack
            0.8f,   // Expected release
            0.1f,   // Attack time
            0.2f,   // Decay time
            0.7f,   // Sustain level
            0.8f,   // Release time
            1.0f);  // Hold time

    // Test 2: Slow attack, fast release (typical synth string)
    runTest("Synth String (Slow Attack, Fast Release)",
            0.3f,   // Expected attack
            0.3f,   // Expected release
            0.3f,   // Attack time
            0.4f,   // Decay time
            0.8f,   // Sustain level
            0.3f,   // Release time
            1.5f);  // Hold time

    // Test 3: Medium attack, medium release (typical brass)
    runTest("Synth Brass (Medium Attack, Medium Release)",
            0.2f,   // Expected attack
            0.4f,   // Expected release
            0.2f,   // Attack time
            0.3f,   // Decay time
            0.75f,  // Sustain level
            0.4f,   // Release time
            1.2f);  // Hold time

    // Note: We don't test pluck sounds (sustain=0) because our calibration
    // workflow asks users to "press and hold C3", which implies sustained notes.

    std::cout << "\n========================================" << std::endl;
    std::cout << "  All tests complete!" << std::endl;
    std::cout << "========================================" << std::endl;

    return 0;
}
