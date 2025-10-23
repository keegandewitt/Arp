/*
  ==============================================================================

    PluginEditor.h

    GUI for VintageCapture VST Plugin.
    Provides buttons for calibration, recording, and playback.

  ==============================================================================
*/

#pragma once

#include "PluginProcessor.h"
// When building with JUCE: #include <JuceHeader.h>

namespace VintageCapture {

/**
 * Main GUI for VintageCapture
 *
 * Layout:
 * ┌─────────────────────────────────────────────────────────┐
 * │            VINTAGE CAPTURE - "PRESS C3"                 │
 * ├─────────────────────────────────────────────────────────┤
 * │                                                         │
 * │  [STAGE 1: CALIBRATION]                                │
 * │  ┌────────────────────────────────────────────┐        │
 * │  │  Status: Ready / Recording / Complete      │        │
 * │  │  Duration: 0.00s                            │        │
 * │  │                                             │        │
 * │  │  Attack:  ---    Release: ---              │        │
 * │  │                                             │        │
 * │  │  [●REC C3] [■STOP]                         │        │
 * │  └────────────────────────────────────────────┘        │
 * │                                                         │
 * │  [STAGE 2: KEYSTROKE CAPTURE]                          │
 * │  ┌────────────────────────────────────────────┐        │
 * │  │  Status: Ready / Recording                 │        │
 * │  │  Notes Captured: 0                         │        │
 * │  │  Duration: 0.00s                            │        │
 * │  │                                             │        │
 * │  │  □ Enable Monitoring (zero-latency)        │        │
 * │  │  [●REC] [■STOP]                            │        │
 * │  └────────────────────────────────────────────┘        │
 * │                                                         │
 * │  [STAGE 3: PLAYBACK]                                    │
 * │  ┌────────────────────────────────────────────┐        │
 * │  │  Status: Ready / Playing                   │        │
 * │  │  Position: 0.00s / 16.00s                  │        │
 * │  │                                             │        │
 * │  │  [▶PLAY] [■STOP]                           │        │
 * │  └────────────────────────────────────────────┘        │
 * │                                                         │
 * └─────────────────────────────────────────────────────────┘
 *
 * This will be implemented as a juce::Component when JUCE is available.
 */
class VintageCaptureEditor {
public:
    VintageCaptureEditor(VintageCaptureProcessor& processor);
    ~VintageCaptureEditor();

    // ========================================================================
    // Button Callbacks
    // ========================================================================

    void onCalibrationRecordClicked();
    void onCalibrationStopClicked();

    void onKeystrokeRecordClicked();
    void onKeystrokeStopClicked();
    void onMonitoringToggled(bool enabled);

    void onPlaybackStartClicked();
    void onPlaybackStopClicked();

    // ========================================================================
    // UI Updates (call from timer)
    // ========================================================================

    void updateUI();

private:
    VintageCaptureProcessor& processor;

    // UI state strings
    std::string calibrationStatus;
    std::string keystrokeStatus;
    std::string playbackStatus;

    float calibrationDuration;
    int notesCaptured;
    float keystrokeDuration;
    float playbackPosition;

    bool monitoringEnabled;

    void updateCalibrationDisplay();
    void updateKeystrokeDisplay();
    void updatePlaybackDisplay();
};

} // namespace VintageCapture
