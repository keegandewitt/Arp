/*
  ==============================================================================

    PluginProcessor.h

    Main VST3/AU processor for VintageCapture.
    Coordinates calibration, keystroke capture, and playback.

  ==============================================================================
*/

#pragma once

// Note: This will require JUCE to build, but we're creating the structure now
// #include <JuceHeader.h>

#include "DurationAnalyzer.h"
#include "KeystrokeCapture.h"
#include "MonitoringEngine.h"
#include <vector>
#include <atomic>

namespace VintageCapture {

/**
 * Plugin state machine
 */
enum class PluginState {
    Idle,               // Ready for calibration or recording
    Calibrating,        // Recording C3 for analysis
    RecordingPerformance, // Capturing keystrokes (Stage 1)
    PlayingBack         // Sending to Arp hardware (Stage 2)
};

/**
 * Main VST3/AU processor
 *
 * When JUCE is available, this will inherit from juce::AudioProcessor
 * For now, we're building the core logic.
 */
class VintageCaptureProcessor {
public:
    VintageCaptureProcessor();
    ~VintageCaptureProcessor();

    // ========================================================================
    // Calibration (Press C3)
    // ========================================================================

    /**
     * Start calibration recording
     */
    void startCalibration();

    /**
     * Stop calibration and analyze
     */
    void stopCalibration();

    /**
     * Get calibration results
     */
    const TimingProfile& getTimingProfile() const { return timingProfile; }

    /**
     * Check if calibration is complete
     */
    bool isCalibrated() const { return timingProfile.isValid(); }

    // ========================================================================
    // Keystroke Recording (Stage 1)
    // ========================================================================

    /**
     * Start keystroke recording
     */
    void startKeystrokeRecording();

    /**
     * Stop keystroke recording
     */
    void stopKeystrokeRecording();

    /**
     * Get recorded keystrokes
     */
    const KeystrokeBuffer& getKeystrokeBuffer() const { return keystrokeBuffer; }

    // ========================================================================
    // Playback (Stage 2)
    // ========================================================================

    /**
     * Start timeline-locked playback
     */
    void startPlayback();

    /**
     * Stop playback
     */
    void stopPlayback();

    // ========================================================================
    // State
    // ========================================================================

    /**
     * Get current plugin state
     */
    PluginState getState() const { return currentState.load(); }

    // ========================================================================
    // Audio/MIDI Processing (called by JUCE)
    // ========================================================================

    /**
     * Process audio block
     * @param buffer Audio buffer (stereo)
     * @param numSamples Number of samples
     * @param sampleRate Current sample rate
     * @param midiMessages MIDI messages for this block
     */
    void processBlock(float** buffer, int numSamples, double sampleRate,
                     const std::vector<uint8_t>& midiMessages);

    /**
     * Process MIDI message
     * @param message Raw MIDI bytes
     * @param timestamp Time in seconds
     */
    void processMIDIMessage(const uint8_t* message, int size, double timestamp);

    // ========================================================================
    // Monitoring Control
    // ========================================================================

    /**
     * Enable/disable zero-latency monitoring
     */
    void setMonitoringEnabled(bool enabled);

    /**
     * Check if monitoring is enabled
     */
    bool isMonitoringEnabled() const;

private:
    // State
    std::atomic<PluginState> currentState;

    // Calibration
    std::vector<float> calibrationBuffer;
    double calibrationSampleRate;
    DurationAnalyzer analyzer;
    TimingProfile timingProfile;

    // Keystroke Capture
    KeystrokeBuffer keystrokeBuffer;

    // Monitoring
    MonitoringEngine monitoringEngine;

    // Playback
    size_t playbackIndex;
    double playbackTime;

    /**
     * Handle MIDI Note On
     */
    void handleNoteOn(uint8_t note, uint8_t velocity, double timestamp);

    /**
     * Handle MIDI Note Off
     */
    void handleNoteOff(uint8_t note, double timestamp);

    /**
     * Process audio during calibration
     */
    void processCalibrationAudio(float** buffer, int numSamples, double sampleRate);

    /**
     * Send MIDI to Arp hardware (placeholder for now)
     */
    void sendToArpHardware(uint8_t note, uint8_t velocity, bool isNoteOn);
};

} // namespace VintageCapture
