# UI Architecture & Button Standards

**Project:** Arp - CircuitPython MIDI Arpeggiator
**Last Updated:** 2025-10-22

---

## OLED FeatherWing Button Configuration

### Hardware
- **Display:** Adafruit OLED FeatherWing 128x64 (Product #4650, SH1107 driver)
- **Buttons:** 3 tactile buttons (A, B, C) + Reset button
- **Button Logic:** Active LOW (False = pressed, True = released)

### Button Pin Assignments

| Button | GPIO Pin | CircuitPython | Notes |
|--------|----------|---------------|-------|
| A | D9 | `board.D9` | Shares battery voltage divider |
| B | D6 | `board.D6` | Has 100K pull-up |
| C | D5 | `board.D5` | Standard GPIO |

**Pull-up Configuration:**
```python
button = digitalio.DigitalInOut(board.D9)  # or D6, D5
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
```

---

## Button Interaction Standards

### Universal Long Press Threshold

**STANDARD: 0.5 seconds**

This is the project-wide definition of a "long press":
- **Short press:** < 0.5 seconds
- **Long press:** ≥ 0.5 seconds

All UI code should use this constant:
```python
LONG_PRESS_THRESHOLD = 0.5  # seconds
```

**Rationale:**
- Fast enough for responsive UI
- Slow enough to prevent accidental triggers
- Comfortable for deliberate long press actions

### Button Combinations

Supported multi-button combinations:
- **A + B**: Two-button combo
- **B + C**: Two-button combo
- **A + C**: Two-button combo
- **A + B + C**: Three-button combo (if needed)

### Detection Logic

```python
# Example: Detect button state
is_pressed = not button.value  # Inverted: False = pressed

# Example: Detect long press
if is_pressed and (time.monotonic() - press_start_time) >= 0.5:
    # Long press detected
    pass
```

---

## UI Interaction Patterns

### Pattern 1: Mode Selection (Short Press)
- **Button A:** Cycle through arpeggio patterns
- **Button B:** Adjust tempo (or enter tempo adjustment mode)
- **Button C:** Enter settings menu

### Pattern 2: Long Press Actions
- **Button A (long):** Toggle pattern selection mode
- **Button B (long):** Toggle clock source (Internal/External)
- **Button C (long):** Toggle display sleep/wake

### Pattern 3: Combination Actions
- **A + B:** Quick save settings
- **B + C:** Reset to defaults (with confirmation)
- **A + C:** Reserved for future use

---

## Button Debouncing

**Method:** Software debouncing using state tracking and time thresholds

**Polling Rate:** 50ms (0.05 seconds)
- Fast enough for responsive UI
- Slow enough to filter bounce noise

```python
while True:
    current_state = button.value
    # Process state changes
    time.sleep(0.05)  # 50ms polling
```

---

## Display Feedback

### Button Press Feedback
- Visual indicator on OLED when button pressed
- Status message for long press actions
- Confirmation message for combinations

### Example Feedback Messages
- Short press: Update display immediately
- Long press: Show "HOLD..." indicator during press
- Long press completed: Show action confirmation
- Combination: Show "A+B" indicator

---

## Code Standards

### Button Handler Module
All button logic should be centralized in `button_handler.py`

### Required Features
1. **Debouncing:** Prevent false triggers from button bounce
2. **Long Press Detection:** Track press duration
3. **Combination Detection:** Detect multiple simultaneous presses
4. **State Management:** Track button states and transitions

### Example Structure
```python
class ButtonHandler:
    LONG_PRESS_THRESHOLD = 0.5  # Standard threshold

    def __init__(self, button_a_pin, button_b_pin, button_c_pin):
        # Initialize buttons with pull-ups
        pass

    def update(self):
        # Poll buttons, detect presses, long presses, combos
        pass

    def is_pressed(self, button_name):
        # Check if button currently pressed
        pass

    def get_long_press(self):
        # Return button name if long press detected
        pass

    def get_combination(self):
        # Return combination if detected (e.g., "A+B")
        pass
```

---

## Testing

### Button Test Script
Located at: `tests/button_clean_test.py`

**Features:**
- Static line display (no scrolling)
- Real-time button state monitoring
- Long press detection (0.5s threshold)
- Combination detection
- Press duration display

**Usage:**
```bash
cp tests/button_clean_test.py /Volumes/CIRCUITPY/code.py
```

Monitor serial output to see button states.

---

## Future Enhancements

### Potential Additions
1. **Double-tap detection:** Quick double press for advanced actions
2. **Haptic feedback:** If vibration motor added
3. **Button lock:** Prevent accidental presses during performance
4. **Configurable thresholds:** User-adjustable long press duration

---

## Version History

**v1.0 (2025-10-22)**
- Initial UI architecture document
- Established 0.5s long press standard
- Documented button pin assignments
- Defined interaction patterns
