/*
  ==============================================================================

    PluginProcessor.cpp

    Implementation of VintageCapture VST processor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include <algorithm>

namespace VintageCapture {

VintageCaptureProcessor::VintageCaptureProcessor()
    : currentState(PluginState::Idle),
      calibrationSampleRate(44100.0),
      playbackIndex(0),
      playbackTime(0.0) {
}

VintageCaptureProcessor::~VintageCaptureProcessor() {
}

// ============================================================================
// Calibration
// ============================================================================

void VintageCaptureProcessor::startCalibration() {
    currentState.store(PluginState::Calibrating);
    calibrationBuffer.clear();
}

void VintageCaptureProcessor::stopCalibration() {
    if (currentState.load() != PluginState::Calibrating) {
        return;
    }

    // Analyze the recorded C3
    timingProfile = analyzer.analyze(calibrationBuffer.data(),
                                     static_cast<int>(calibrationBuffer.size()),
                                     calibrationSampleRate);

    // Store the sample for monitoring
    if (timingProfile.isValid()) {
        monitoringEngine.setReferenceSample(calibrationBuffer, calibrationSampleRate);
    }

    currentState.store(PluginState::Idle);
}

// ============================================================================
// Keystroke Recording
// ============================================================================

void VintageCaptureProcessor::startKeystrokeRecording() {
    currentState.store(PluginState::RecordingPerformance);
    keystrokeBuffer.startCapture();
    monitoringEngine.setEnabled(true);
}

void VintageCaptureProcessor::stopKeystrokeRecording() {
    if (currentState.load() != PluginState::RecordingPerformance) {
        return;
    }

    keystrokeBuffer.stopCapture();
    monitoringEngine.setEnabled(false);
    currentState.store(PluginState::Idle);
}

// ============================================================================
// Playback
// ============================================================================

void VintageCaptureProcessor::startPlayback() {
    currentState.store(PluginState::PlayingBack);
    playbackIndex = 0;
    playbackTime = 0.0;
}

void VintageCaptureProcessor::stopPlayback() {
    currentState.store(PluginState::Idle);
    monitoringEngine.allNotesOff();
}

// ============================================================================
// Audio/MIDI Processing
// ============================================================================

void VintageCaptureProcessor::processBlock(float** buffer, int numSamples,
                                          double sampleRate,
                                          const std::vector<uint8_t>& midiMessages) {
    PluginState state = currentState.load();

    // Process audio based on current state
    switch (state) {
        case PluginState::Calibrating:
            processCalibrationAudio(buffer, numSamples, sampleRate);
            break;

        case PluginState::RecordingPerformance:
            // Fill output with monitoring engine
            monitoringEngine.process(buffer[0], numSamples, sampleRate);
            break;

        case PluginState::PlayingBack:
            // TODO: Send keystroke buffer to Arp hardware
            // For now, fill with silence
            for (int ch = 0; ch < 2; ++ch) {
                for (int i = 0; i < numSamples; ++i) {
                    buffer[ch][i] = 0.0f;
                }
            }
            break;

        case PluginState::Idle:
        default:
            // Fill with silence
            for (int ch = 0; ch < 2; ++ch) {
                for (int i = 0; i < numSamples; ++i) {
                    buffer[ch][i] = 0.0f;
                }
            }
            break;
    }
}

void VintageCaptureProcessor::processMIDIMessage(const uint8_t* message,
                                                int size,
                                                double timestamp) {
    if (size < 3) {
        return;  // Invalid MIDI message
    }

    uint8_t status = message[0] & 0xF0;
    uint8_t note = message[1] & 0x7F;
    uint8_t velocity = message[2] & 0x7F;

    if (status == 0x90 && velocity > 0) {
        // Note On
        handleNoteOn(note, velocity, timestamp);
    } else if (status == 0x80 || (status == 0x90 && velocity == 0)) {
        // Note Off
        handleNoteOff(note, timestamp);
    }
}

void VintageCaptureProcessor::handleNoteOn(uint8_t note, uint8_t velocity, double timestamp) {
    PluginState state = currentState.load();

    if (state == PluginState::RecordingPerformance) {
        // Record the keystroke
        keystrokeBuffer.recordEvent(note, velocity, true, timestamp);

        // Trigger monitoring
        monitoringEngine.noteOn(note, velocity);
    }
}

void VintageCaptureProcessor::handleNoteOff(uint8_t note, double timestamp) {
    PluginState state = currentState.load();

    if (state == PluginState::RecordingPerformance) {
        // Record the keystroke
        keystrokeBuffer.recordEvent(note, 0, false, timestamp);

        // Release monitoring
        monitoringEngine.noteOff(note);
    }
}

void VintageCaptureProcessor::processCalibrationAudio(float** buffer,
                                                     int numSamples,
                                                     double sampleRate) {
    // Record audio from input channel 0 (mono)
    calibrationSampleRate = sampleRate;

    for (int i = 0; i < numSamples; ++i) {
        calibrationBuffer.push_back(buffer[0][i]);
    }

    // Pass through to output (user can hear what they're playing)
    for (int ch = 0; ch < 2; ++ch) {
        for (int i = 0; i < numSamples; ++i) {
            buffer[ch][i] = buffer[0][i];  // Mono to stereo
        }
    }
}

void VintageCaptureProcessor::sendToArpHardware(uint8_t note, uint8_t velocity, bool isNoteOn) {
    // TODO: Implement USB MIDI to Arp hardware
    // For now, this is a placeholder
    (void)note;
    (void)velocity;
    (void)isNoteOn;
}

// ============================================================================
// Monitoring Control
// ============================================================================

void VintageCaptureProcessor::setMonitoringEnabled(bool enabled) {
    monitoringEngine.setEnabled(enabled);
}

bool VintageCaptureProcessor::isMonitoringEnabled() const {
    return monitoringEngine.isEnabled();
}

} // namespace VintageCapture
