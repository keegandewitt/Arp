# VintageCapture VST Plugin - JUCE CMake Build
cmake_minimum_required(VERSION 3.22)

project(VintageCapture VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================================================================
# JUCE Setup
# ============================================================================

# Find JUCE (install via: git clone https://github.com/juce-framework/JUCE.git)
# Or set JUCE_DIR to your JUCE installation
find_package(JUCE CONFIG REQUIRED)

# ============================================================================
# Plugin Target
# ============================================================================

juce_add_plugin(VintageCapture
    COMPANY_NAME "VintageCapture"
    PLUGIN_MANUFACTURER_CODE Vntg
    PLUGIN_CODE Vcpt
    FORMATS VST3 AU Standalone
    PRODUCT_NAME "VintageCapture"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT TRUE
    NEEDS_MIDI_OUTPUT TRUE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE
    PLUGIN_MANUFACTURER_EMAIL "support@vintagecapture.com"
    PLUGIN_CODE_NAME "VintageCapture"
    BUNDLE_ID "com.vintagecapture.vst"
)

# ============================================================================
# Source Files
# ============================================================================

target_sources(VintageCapture
    PRIVATE
        Source/PluginProcessor.cpp
        Source/PluginProcessor.h
        Source/PluginEditor.cpp
        Source/PluginEditor.h
        Source/DurationAnalyzer.cpp
        Source/DurationAnalyzer.h
        Source/KeystrokeCapture.cpp
        Source/KeystrokeCapture.h
        Source/MonitoringEngine.cpp
        Source/MonitoringEngine.h
)

# ============================================================================
# Compile Definitions
# ============================================================================

target_compile_definitions(VintageCapture
    PUBLIC
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        JUCE_VST3_CAN_REPLACE_VST2=0
        JUCE_DISPLAY_SPLASH_SCREEN=0
        JUCE_REPORT_APP_USAGE=0
)

# ============================================================================
# Link JUCE Modules
# ============================================================================

target_link_libraries(VintageCapture
    PRIVATE
        juce::juce_audio_basics
        juce::juce_audio_devices
        juce::juce_audio_formats
        juce::juce_audio_plugin_client
        juce::juce_audio_processors
        juce::juce_audio_utils
        juce::juce_core
        juce::juce_data_structures
        juce::juce_events
        juce::juce_graphics
        juce::juce_gui_basics
        juce::juce_gui_extra
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags
)

# ============================================================================
# Installation
# ============================================================================

install(TARGETS VintageCapture
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

message(STATUS "VintageCapture VST Plugin Configuration:")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
