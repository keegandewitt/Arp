"""
Hardware Test Suite for MIDI Arpeggiator
=========================================

Simple tests to verify individual hardware components are connected and working.
Run each test independently by uncommenting the desired test in the main section.

Requirements:
- CircuitPython installed on M4 Feather CAN
- Required libraries in /lib folder:
  - adafruit_displayio_ssd1306
  - adafruit_display_text
  - adafruit_midi
  - adafruit_mcp4728
  - adafruit_bus_device

Usage:
1. Copy this file to CIRCUITPY drive as code.py (or import from REPL)
2. Uncomment ONE test function at a time in the main section
3. Save and watch serial console for results
4. Power cycle between tests for clean state
"""

import board
import busio
import time
import digitalio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306


# =============================================================================
# TEST 1: I2C Bus Scan
# =============================================================================
def test_i2c_scan():
    """
    Test I2C bus and scan for connected devices.
    Expected devices:
    - 0x3C: OLED FeatherWing
    - 0x60: MCP4728 DAC (if connected)
    """
    print("\n" + "="*50)
    print("TEST 1: I2C Bus Scan")
    print("="*50)

    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        print("✓ I2C bus initialized successfully")
        print("  SCL: board.SCL")
        print("  SDA: board.SDA")

        # Lock bus to scan
        while not i2c.try_lock():
            pass

        print("\nScanning I2C bus...")
        devices = i2c.scan()
        i2c.unlock()

        print(f"\nFound {len(devices)} device(s):")
        for device in devices:
            device_name = "Unknown"
            if device == 0x3C:
                device_name = "OLED Display (FeatherWing)"
            elif device == 0x60:
                device_name = "MCP4728 DAC"
            print(f"  0x{device:02X} - {device_name}")

        # Check for expected devices
        print("\nExpected Device Check:")
        if 0x3C in devices:
            print("  ✓ OLED Display found at 0x3C")
        else:
            print("  ✗ OLED Display NOT found (expected at 0x3C)")

        if 0x60 in devices:
            print("  ✓ MCP4728 DAC found at 0x60")
        else:
            print("  ⚠ MCP4728 DAC NOT found (expected at 0x60 - may not be connected yet)")

        print("\n" + "="*50)
        print("I2C Scan Complete")
        print("="*50 + "\n")

        i2c.deinit()
        return len(devices) > 0

    except Exception as e:
        print(f"✗ I2C scan FAILED: {e}")
        return False


# =============================================================================
# TEST 2: OLED Display
# =============================================================================
def test_oled_display():
    """
    Test OLED FeatherWing display.
    Should display test pattern and cycle through messages.
    Watch the physical display for visual confirmation.
    """
    print("\n" + "="*50)
    print("TEST 2: OLED Display")
    print("="*50)

    try:
        # Initialize I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        print("✓ I2C initialized")

        # Release any existing displays
        displayio.release_displays()

        # Create display bus
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
        print("✓ Display bus created (address 0x3C)")

        # Create display object (128x32 OLED)
        display = adafruit_displayio_ssd1306.SSD1306(
            display_bus,
            width=128,
            height=32
        )
        display.brightness = 0.5
        print("✓ Display object created (128x32)")

        # Create display group
        group = displayio.Group()

        # Test 1: Simple text
        print("\nDisplaying test pattern 1: 'OLED Test OK'")
        text_label = label.Label(
            terminalio.FONT,
            text="OLED Test OK",
            color=0xFFFFFF,
            x=0,
            y=4
        )
        group.append(text_label)
        display.root_group = group
        time.sleep(2)

        # Test 2: Multi-line text
        print("Displaying test pattern 2: Multi-line")
        group = displayio.Group()

        line1 = label.Label(terminalio.FONT, text="Line 1: BPM 120", color=0xFFFFFF, x=0, y=4)
        line2 = label.Label(terminalio.FONT, text="Line 2: Pattern", color=0xFFFFFF, x=0, y=14)
        line3 = label.Label(terminalio.FONT, text="Line 3: Status", color=0xFFFFFF, x=0, y=24)

        group.append(line1)
        group.append(line2)
        group.append(line3)
        display.root_group = group
        time.sleep(2)

        # Test 3: Brightness levels
        print("Testing brightness levels...")
        for brightness in [1.0, 0.5, 0.2, 0.5, 1.0]:
            display.brightness = brightness
            print(f"  Brightness: {brightness}")
            time.sleep(0.5)

        # Test 4: Update speed test
        print("Testing display update speed (10 updates)...")
        start_time = time.monotonic()
        for i in range(10):
            line1.text = f"Update: {i+1}/10"
            time.sleep(0.1)
        elapsed = time.monotonic() - start_time
        print(f"  10 updates in {elapsed:.2f}s ({elapsed/10*1000:.1f}ms per update)")

        # Final message
        group = displayio.Group()
        final_label = label.Label(
            terminalio.FONT,
            text="Test Complete!",
            color=0xFFFFFF,
            x=10,
            y=12
        )
        group.append(final_label)
        display.root_group = group

        print("\n" + "="*50)
        print("✓ OLED Display Test PASSED")
        print("  Check physical display for 'Test Complete!' message")
        print("="*50 + "\n")

        return True

    except Exception as e:
        print(f"✗ OLED test FAILED: {e}")
        return False


# =============================================================================
# TEST 3: OLED Buttons
# =============================================================================
def test_oled_buttons():
    """
    Test the three buttons on OLED FeatherWing.
    Press each button to verify it's working.
    Press all three simultaneously to exit test.
    """
    print("\n" + "="*50)
    print("TEST 3: OLED FeatherWing Buttons")
    print("="*50)

    try:
        # Initialize buttons (D9=A, D6=B, D5=C)
        button_a = digitalio.DigitalInOut(board.D9)
        button_a.direction = digitalio.Direction.INPUT
        button_a.pull = digitalio.Pull.UP

        button_b = digitalio.DigitalInOut(board.D6)
        button_b.direction = digitalio.Direction.INPUT
        button_b.pull = digitalio.Pull.UP

        button_c = digitalio.DigitalInOut(board.D5)
        button_c.direction = digitalio.Direction.INPUT
        button_c.pull = digitalio.Pull.UP

        print("✓ Buttons initialized")
        print("  Button A: D9")
        print("  Button B: D6")
        print("  Button C: D5")

        print("\nButton Test Instructions:")
        print("  - Press Button A (left)")
        print("  - Press Button B (center)")
        print("  - Press Button C (right)")
        print("  - Press all three buttons together to exit")
        print("\nWaiting for button presses...\n")

        button_a_tested = False
        button_b_tested = False
        button_c_tested = False

        while True:
            # Read button states (active low - pressed = False)
            a_pressed = not button_a.value
            b_pressed = not button_b.value
            c_pressed = not button_c.value

            # Check for exit condition (all three pressed)
            if a_pressed and b_pressed and c_pressed:
                print("\n✓ All three buttons pressed - exiting test")
                break

            # Individual button presses
            if a_pressed and not button_a_tested:
                print("  ✓ Button A pressed!")
                button_a_tested = True
                time.sleep(0.3)  # Debounce

            if b_pressed and not button_b_tested:
                print("  ✓ Button B pressed!")
                button_b_tested = True
                time.sleep(0.3)

            if c_pressed and not button_c_tested:
                print("  ✓ Button C pressed!")
                button_c_tested = True
                time.sleep(0.3)

            # Check if all buttons tested
            if button_a_tested and button_b_tested and button_c_tested:
                print("\n✓ All buttons tested successfully!")
                print("  Press all three buttons together to exit...\n")

            time.sleep(0.05)  # Small delay to prevent CPU hogging

        # Cleanup
        button_a.deinit()
        button_b.deinit()
        button_c.deinit()

        print("\n" + "="*50)
        print("✓ Button Test PASSED")
        print("="*50 + "\n")

        return True

    except Exception as e:
        print(f"✗ Button test FAILED: {e}")
        return False


# =============================================================================
# TEST 4: MIDI FeatherWing
# =============================================================================
def test_midi_featherwing():
    """
    Test MIDI FeatherWing input and output.
    Requires:
    - MIDI device connected to MIDI IN (keyboard, controller, etc.)
    - Optional: MIDI device connected to MIDI OUT to hear echo

    This test will echo any received MIDI messages back to MIDI OUT.
    """
    print("\n" + "="*50)
    print("TEST 4: MIDI FeatherWing")
    print("="*50)

    try:
        import adafruit_midi
        from adafruit_midi.note_on import NoteOn
        from adafruit_midi.note_off import NoteOff
        from adafruit_midi.control_change import ControlChange

        # Initialize UART for MIDI (TX=board.TX, RX=board.RX)
        uart = busio.UART(
            board.TX, board.RX,
            baudrate=31250,
            timeout=0
        )
        print("✓ UART initialized (31250 baud)")
        print("  TX: board.TX")
        print("  RX: board.RX")

        # Create MIDI interface
        midi = adafruit_midi.MIDI(
            midi_in=uart,
            midi_out=uart,
            in_channel=0,
            out_channel=0
        )
        print("✓ MIDI interface created")

        print("\nMIDI Test Instructions:")
        print("  1. Connect MIDI keyboard/controller to MIDI IN")
        print("  2. Optionally connect MIDI OUT to synth (will echo messages)")
        print("  3. Play some notes or move controls")
        print("  4. Wait 30 seconds or press Ctrl+C to exit")
        print("\nListening for MIDI messages...\n")

        message_count = 0
        start_time = time.monotonic()
        timeout = 30  # 30 second test

        while (time.monotonic() - start_time) < timeout:
            msg = midi.receive()

            if msg is not None:
                message_count += 1

                # Print message details
                if isinstance(msg, NoteOn):
                    print(f"  [{message_count}] Note ON:  Note={msg.note} Vel={msg.velocity} Ch={msg.channel+1}")
                    # Echo back
                    midi.send(msg)

                elif isinstance(msg, NoteOff):
                    print(f"  [{message_count}] Note OFF: Note={msg.note} Vel={msg.velocity} Ch={msg.channel+1}")
                    # Echo back
                    midi.send(msg)

                elif isinstance(msg, ControlChange):
                    print(f"  [{message_count}] CC: Controller={msg.control} Value={msg.value} Ch={msg.channel+1}")
                    # Echo back
                    midi.send(msg)

                else:
                    print(f"  [{message_count}] Other: {type(msg).__name__}")
                    # Echo back
                    midi.send(msg)

            time.sleep(0.001)  # 1ms delay for responsiveness

        print(f"\n✓ Test complete - received {message_count} MIDI messages")

        if message_count == 0:
            print("\n⚠ WARNING: No MIDI messages received")
            print("  Check:")
            print("    - MIDI device is connected to MIDI IN")
            print("    - MIDI device is powered on and sending data")
            print("    - MIDI cable is working")
            print("    - TX/RX pins are correct (board.TX, board.RX)")

        print("\n" + "="*50)
        if message_count > 0:
            print("✓ MIDI FeatherWing Test PASSED")
        else:
            print("⚠ MIDI FeatherWing Test INCOMPLETE (no messages)")
        print("="*50 + "\n")

        uart.deinit()
        return message_count > 0

    except KeyboardInterrupt:
        print(f"\n\n✓ Test interrupted - received {message_count} MIDI messages")
        print("="*50 + "\n")
        return message_count > 0

    except Exception as e:
        print(f"✗ MIDI test FAILED: {e}")
        return False


# =============================================================================
# TEST 5: MCP4728 DAC
# =============================================================================
def test_mcp4728_dac():
    """
    Test MCP4728 Quad DAC (4-channel, 12-bit, I2C).
    Generates test voltages on all 4 channels.
    Use a multimeter to verify output voltages on CV 1-4.

    Expected outputs (with 5V VCC):
    - Channel A (CV1): 0V → 1.25V → 2.5V → 3.75V → 5V
    - Channel B (CV2): 5V → 3.75V → 2.5V → 1.25V → 0V
    - Channel C (CV3): 2.5V (constant)
    - Channel D (CV4): Triangle wave (0V → 5V → 0V)
    """
    print("\n" + "="*50)
    print("TEST 5: MCP4728 Quad DAC")
    print("="*50)

    try:
        import adafruit_mcp4728

        # Initialize I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        print("✓ I2C initialized")

        # Create DAC object (default address 0x60)
        dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)
        print("✓ MCP4728 found at address 0x60")

        # Check if powered by 5V
        print("\n⚠ IMPORTANT: Ensure MCP4728 is powered by 5V from Teyleten boost module")
        print("  If powered by 3.3V, maximum output will be 3.3V instead of 5V")

        print("\nDAC Test Pattern:")
        print("  Channel A (CV1): 0V → 1.25V → 2.5V → 3.75V → 5V")
        print("  Channel B (CV2): 5V → 3.75V → 2.5V → 1.25V → 0V")
        print("  Channel C (CV3): 2.5V (constant)")
        print("  Channel D (CV4): Triangle wave (0V → 5V → 0V)")
        print("\nUse a multimeter to verify voltages on CV outputs")
        print("Starting test in 3 seconds...\n")
        time.sleep(3)

        # Helper function to convert voltage to DAC value
        def voltage_to_dac(volts, max_voltage=5.0):
            """Convert voltage (0-5V) to 16-bit DAC value (0-65535)"""
            dac_value = int((volts / max_voltage) * 65535)
            return max(0, min(65535, dac_value))

        # Test sequence
        test_voltages = [0.0, 1.25, 2.5, 3.75, 5.0]

        for step, v_a in enumerate(test_voltages):
            v_b = test_voltages[-(step+1)]  # Reverse for channel B
            v_c = 2.5  # Constant
            v_d = abs(2.5 - v_a)  # Triangle wave

            # Set DAC values
            dac.channel_a.value = voltage_to_dac(v_a)
            dac.channel_b.value = voltage_to_dac(v_b)
            dac.channel_c.value = voltage_to_dac(v_c)
            dac.channel_d.value = voltage_to_dac(v_d)

            print(f"Step {step+1}/5:")
            print(f"  CV1 (Ch A): {v_a:.2f}V  (DAC: {dac.channel_a.value})")
            print(f"  CV2 (Ch B): {v_b:.2f}V  (DAC: {dac.channel_b.value})")
            print(f"  CV3 (Ch C): {v_c:.2f}V  (DAC: {dac.channel_c.value})")
            print(f"  CV4 (Ch D): {v_d:.2f}V  (DAC: {dac.channel_d.value})")
            print()

            time.sleep(3)  # Hold each voltage for 3 seconds

        # Test MIDI note to CV conversion (1V/octave)
        print("\nTesting MIDI Note to CV conversion (1V/octave):")
        print("  C1 (MIDI 36) = 1.0V")
        print("  C2 (MIDI 48) = 2.0V")
        print("  C3 (MIDI 60) = 3.0V")
        print("  C4 (MIDI 72) = 4.0V")
        print("  C5 (MIDI 84) = 5.0V")
        print()

        def midi_note_to_cv(midi_note, base_note=36):
            """Convert MIDI note to 1V/octave CV (C1=36=1V)"""
            volts = (midi_note - base_note) / 12.0 + 1.0
            return volts

        test_notes = [
            (36, "C1"),
            (48, "C2"),
            (60, "C3"),
            (72, "C4"),
            (84, "C5")
        ]

        for midi_note, note_name in test_notes:
            cv_voltage = midi_note_to_cv(midi_note)
            dac.channel_a.value = voltage_to_dac(cv_voltage)
            print(f"  {note_name} (MIDI {midi_note}): {cv_voltage:.2f}V")
            time.sleep(2)

        # Reset to 0V
        print("\nResetting all channels to 0V...")
        dac.channel_a.value = 0
        dac.channel_b.value = 0
        dac.channel_c.value = 0
        dac.channel_d.value = 0

        print("\n" + "="*50)
        print("✓ MCP4728 DAC Test PASSED")
        print("  Verify voltages matched expected values on multimeter")
        print("="*50 + "\n")

        i2c.deinit()
        return True

    except Exception as e:
        print(f"✗ DAC test FAILED: {e}")
        print("\nTroubleshooting:")
        print("  - Check MCP4728 is connected to I2C (SCL/SDA)")
        print("  - Verify MCP4728 address is 0x60 (run I2C scan test)")
        print("  - Ensure MCP4728 VCC is connected to 5V boost output")
        print("  - Check adafruit_mcp4728 library is installed")
        return False


# =============================================================================
# TEST 6: Full System Integration
# =============================================================================
def test_full_system():
    """
    Test all components together:
    - OLED display shows MIDI activity
    - MIDI input triggers CV output
    - Buttons control which CV channel receives note data

    This simulates basic operation of the complete system.
    """
    print("\n" + "="*50)
    print("TEST 6: Full System Integration")
    print("="*50)

    try:
        import adafruit_midi
        from adafruit_midi.note_on import NoteOn
        from adafruit_midi.note_off import NoteOff
        import adafruit_mcp4728

        # Initialize I2C
        i2c = busio.I2C(board.SCL, board.SDA)

        # Initialize OLED
        displayio.release_displays()
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
        display.brightness = 0.5

        # Create display labels
        group = displayio.Group()
        line1 = label.Label(terminalio.FONT, text="System Test", color=0xFFFFFF, x=0, y=4)
        line2 = label.Label(terminalio.FONT, text="MIDI: ---", color=0xFFFFFF, x=0, y=14)
        line3 = label.Label(terminalio.FONT, text="CV: Ready", color=0xFFFFFF, x=0, y=24)
        group.append(line1)
        group.append(line2)
        group.append(line3)
        display.root_group = group

        # Initialize UART for MIDI
        uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0)
        midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart, in_channel=0, out_channel=0)

        # Initialize DAC
        dac = adafruit_mcp4728.MCP4728(i2c, address=0x60)

        # Initialize buttons
        button_a = digitalio.DigitalInOut(board.D9)
        button_a.direction = digitalio.Direction.INPUT
        button_a.pull = digitalio.Pull.UP

        print("✓ All components initialized")
        print("\nFull System Test:")
        print("  - Play MIDI notes (will appear on display)")
        print("  - CV1 will output 1V/octave for each note")
        print("  - Button A cycles CV output channel")
        print("  - Test runs for 30 seconds")
        print("\nStarting test...\n")

        current_channel = 0  # 0=A, 1=B, 2=C, 3=D
        channel_names = ["CV1 (A)", "CV2 (B)", "CV3 (C)", "CV4 (D)"]
        last_note = None
        start_time = time.monotonic()
        last_button_time = 0

        def midi_note_to_cv(midi_note):
            volts = (midi_note - 36) / 12.0 + 1.0
            return int((volts / 5.0) * 65535)

        while (time.monotonic() - start_time) < 30:
            # Check button A for channel switching
            if not button_a.value:  # Button pressed
                current_time = time.monotonic()
                if (current_time - last_button_time) > 0.3:  # Debounce
                    current_channel = (current_channel + 1) % 4
                    line3.text = f"Out: {channel_names[current_channel]}"
                    print(f"  Switched to {channel_names[current_channel]}")
                    last_button_time = current_time

            # Process MIDI
            msg = midi.receive()
            if msg is not None:
                if isinstance(msg, NoteOn) and msg.velocity > 0:
                    last_note = msg.note
                    cv_value = midi_note_to_cv(msg.note)

                    # Send to selected channel
                    if current_channel == 0:
                        dac.channel_a.value = cv_value
                    elif current_channel == 1:
                        dac.channel_b.value = cv_value
                    elif current_channel == 2:
                        dac.channel_c.value = cv_value
                    elif current_channel == 3:
                        dac.channel_d.value = cv_value

                    line2.text = f"Note: {msg.note} V={msg.velocity}"
                    print(f"  Note ON: {msg.note} → CV={cv_value}")

                elif isinstance(msg, NoteOff) or (isinstance(msg, NoteOn) and msg.velocity == 0):
                    # Reset to 0V on note off
                    if current_channel == 0:
                        dac.channel_a.value = 0
                    elif current_channel == 1:
                        dac.channel_b.value = 0
                    elif current_channel == 2:
                        dac.channel_c.value = 0
                    elif current_channel == 3:
                        dac.channel_d.value = 0

                    line2.text = "Note: OFF"
                    print(f"  Note OFF")

            time.sleep(0.001)

        # Cleanup
        dac.channel_a.value = 0
        dac.channel_b.value = 0
        dac.channel_c.value = 0
        dac.channel_d.value = 0

        line1.text = "Test Complete"
        line2.text = ""
        line3.text = ""

        print("\n" + "="*50)
        print("✓ Full System Integration Test COMPLETE")
        print("="*50 + "\n")

        return True

    except Exception as e:
        print(f"✗ Full system test FAILED: {e}")
        return False


# =============================================================================
# MAIN - Uncomment ONE test at a time
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("    MIDI ARPEGGIATOR - HARDWARE TEST SUITE")
    print("="*60)
    print("\nInstructions:")
    print("  1. Uncomment ONE test function below")
    print("  2. Save this file")
    print("  3. Watch serial console for results")
    print("  4. Power cycle between tests for clean state")
    print("\n" + "="*60 + "\n")

    # Uncomment ONE test at a time:

    # test_i2c_scan()              # Test 1: Scan I2C bus for devices
    # test_oled_display()          # Test 2: OLED display functionality
    # test_oled_buttons()          # Test 3: OLED FeatherWing buttons
    # test_midi_featherwing()      # Test 4: MIDI In/Out
    # test_mcp4728_dac()           # Test 5: MCP4728 DAC CV output
    # test_full_system()           # Test 6: All components together

    print("No test selected. Uncomment a test function above and save.")
