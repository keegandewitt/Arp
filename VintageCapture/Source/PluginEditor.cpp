/*
  ==============================================================================

    PluginEditor.cpp

    Implementation of VintageCapture GUI logic.

  ==============================================================================
*/

#include "PluginEditor.h"
#include <sstream>
#include <iomanip>

namespace VintageCapture {

VintageCaptureEditor::VintageCaptureEditor(VintageCaptureProcessor& proc)
    : processor(proc),
      calibrationDuration(0.0f),
      notesCaptured(0),
      keystrokeDuration(0.0f),
      playbackPosition(0.0f),
      monitoringEnabled(true) {

    calibrationStatus = "Ready";
    keystrokeStatus = "Ready";
    playbackStatus = "Ready";
}

VintageCaptureEditor::~VintageCaptureEditor() {
}

// ============================================================================
// Button Callbacks
// ============================================================================

void VintageCaptureEditor::onCalibrationRecordClicked() {
    processor.startCalibration();
    calibrationStatus = "Recording C3...";
}

void VintageCaptureEditor::onCalibrationStopClicked() {
    processor.stopCalibration();

    if (processor.isCalibrated()) {
        calibrationStatus = "Complete";
    } else {
        calibrationStatus = "Failed - Try Again";
    }
}

void VintageCaptureEditor::onKeystrokeRecordClicked() {
    if (!processor.isCalibrated()) {
        keystrokeStatus = "Error: Calibrate first!";
        return;
    }

    processor.startKeystrokeRecording();
    keystrokeStatus = "Recording Performance...";
}

void VintageCaptureEditor::onKeystrokeStopClicked() {
    processor.stopKeystrokeRecording();
    keystrokeStatus = "Recording Complete";
}

void VintageCaptureEditor::onMonitoringToggled(bool enabled) {
    monitoringEnabled = enabled;
    processor.setMonitoringEnabled(enabled);
}

void VintageCaptureEditor::onPlaybackStartClicked() {
    const auto& buffer = processor.getKeystrokeBuffer();
    if (buffer.getEventCount() == 0) {
        playbackStatus = "Error: No performance recorded!";
        return;
    }

    processor.startPlayback();
    playbackStatus = "Playing Back...";
}

void VintageCaptureEditor::onPlaybackStopClicked() {
    processor.stopPlayback();
    playbackStatus = "Stopped";
}

// ============================================================================
// UI Updates
// ============================================================================

void VintageCaptureEditor::updateUI() {
    updateCalibrationDisplay();
    updateKeystrokeDisplay();
    updatePlaybackDisplay();
}

void VintageCaptureEditor::updateCalibrationDisplay() {
    const auto& profile = processor.getTimingProfile();

    if (processor.getState() == PluginState::Calibrating) {
        calibrationStatus = "Recording C3...";
    } else if (profile.isValid()) {
        std::ostringstream oss;
        oss << "Attack: " << std::fixed << std::setprecision(3) << profile.attackTime << "s  "
            << "Release: " << profile.releaseTime << "s";
        calibrationStatus = oss.str();
    }
}

void VintageCaptureEditor::updateKeystrokeDisplay() {
    const auto& buffer = processor.getKeystrokeBuffer();

    notesCaptured = buffer.getNoteCount();
    keystrokeDuration = static_cast<float>(buffer.getDuration());

    if (processor.getState() == PluginState::RecordingPerformance) {
        std::ostringstream oss;
        oss << "Recording: " << notesCaptured << " notes, "
            << std::fixed << std::setprecision(2) << keystrokeDuration << "s";
        keystrokeStatus = oss.str();
    }
}

void VintageCaptureEditor::updatePlaybackDisplay() {
    if (processor.getState() == PluginState::PlayingBack) {
        playbackStatus = "Playing Back via Arp...";
    }
}

} // namespace VintageCapture
