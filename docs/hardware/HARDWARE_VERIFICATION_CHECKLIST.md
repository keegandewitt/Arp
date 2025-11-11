# Hardware Verification Checklist

**Purpose:** Prevent assumptions about hardware specifications. ALWAYS verify before coding.

**Created:** 2025-10-22
**Reason:** Incorrectly assumed 128x32 display when hardware was 128x64

---

## Before Writing ANY Hardware-Specific Code

### Step 1: Check Documentation
- [ ] Read PROJECT_STATUS.md hardware configuration section
- [ ] Read HARDWARE_PINOUT.md for pin assignments
- [ ] Read BOM.md for part numbers and specifications
- [ ] Check README.md for hardware descriptions

### Step 2: Verify for Inconsistencies
- [ ] Cross-reference all documentation sources
- [ ] Note any conflicting information
- [ ] Check part numbers against manufacturer specs

### Step 3: Ask User for Clarification
**If documentation is:**
- **Ambiguous:** "128x32 or 128x64" → ASK which one
- **Inconsistent:** Different docs say different things → ASK which is correct
- **Missing:** No spec found → ASK for specification
- **Unclear:** Any doubt whatsoever → ASK

### Step 4: Physical Verification (when possible)
- [ ] Ask user to confirm physical hardware present
- [ ] Ask for part numbers from physical labels
- [ ] Ask for photos if specifications unclear
- [ ] Verify dimensions, pinouts, addresses

### Step 5: Document the Answer
- [ ] Update documentation with verified specification
- [ ] Add hardware notes to code comments
- [ ] Update PROJECT_STATUS.md if needed
- [ ] Fix any inconsistencies found

---

## Hardware Specification Questions to ALWAYS Ask

### Displays
- [ ] Exact dimensions (128x32 vs 128x64, etc.)
- [ ] I2C address (0x3C vs 0x3D)
- [ ] Part number / model
- [ ] Manufacturer

### Microcontrollers
- [ ] Exact model (Feather M4 CAN vs Feather M4 Express)
- [ ] Pin assignments being used
- [ ] CircuitPython version installed
- [ ] RAM/Flash capacity

### Buttons/Controls
- [ ] How many buttons
- [ ] Which pins
- [ ] Pull-up or pull-down configuration

### Communication Buses
- [ ] Which I2C pins (if multiple I2C buses available)
- [ ] SPI vs UART vs I2C
- [ ] Baud rates for UART

### Power
- [ ] Voltage levels (3.3V vs 5V)
- [ ] Battery type if applicable
- [ ] Current requirements

---

## NEVER ASSUME

### ❌ Don't Assume:
- Display dimensions
- I2C addresses
- Pin assignments
- Voltage levels
- Part numbers
- Configurations

### ✅ Always Verify:
- Check documentation
- Ask user
- Cross-reference specs
- Test on hardware
- Document findings

---

## Example Verification Dialog

**Bad (Assumption):**
```
the assistant: "I'll configure the display for 128x32..."
[Writes code without asking]
```

**Good (Verification):**
```
the assistant: "I see the documentation mentions both 128x32 and 128x64 displays.
        Which OLED FeatherWing do you have installed?"

User: "128x64"

the assistant: "Thank you! I'll configure for 128x64.
        I'll also update the documentation to be consistent."
```

---

## Lesson Learned (2025-10-22)

**Mistake Made:**
- Assumed 128x32 display based on incomplete documentation check
- Did not ask user for clarification when "128x32 or 128x64" was ambiguous
- Coded and tested without verifying actual hardware

**Correct Approach:**
1. Check all documentation sources
2. Notice ambiguity: "128x32 or 128x64"
3. **ASK USER:** "Which display do you have: 128x32 or 128x64?"
4. Get answer: "128x64"
5. Code for 128x64
6. Update all documentation to remove ambiguity

**Impact:**
- Wasted time debugging
- Code didn't work on actual hardware
- Lost user confidence
- Had to rewrite and retest

---

## Checklist Template for New Hardware

When adding new hardware to the project:

```markdown
## [Hardware Component Name]

**Verified:** [Date]
**Verified By:** [User name]
**Documentation Updated:** [Y/N]

### Specifications
- **Manufacturer:** [Name]
- **Part Number:** [Number]
- **Model:** [Model]
- **Key Specs:** [Dimensions, voltage, pins, etc.]

### Physical Verification
- [ ] Component physically present
- [ ] Part number confirmed from label
- [ ] Connections verified
- [ ] Compatible with existing hardware

### Documentation
- [ ] Added to BOM.md
- [ ] Added to HARDWARE_PINOUT.md
- [ ] Added to PROJECT_STATUS.md
- [ ] Added to README.md if user-facing

### Testing
- [ ] Hardware test written
- [ ] Test passed on actual hardware
- [ ] Results documented
```

---

## Integration into Workflow

**This checklist is now REQUIRED before:**
- Writing display code
- Configuring I2C/SPI/UART
- Setting pin assignments
- Configuring DACs/ADCs
- Any hardware-specific code

**Add to METHODOLOGY.md:**
- Reference this checklist in hardware development section
- Require verification before hardware coding
- Make "Ask user for clarity" a core principle

---

## Notes

- This checklist exists because assumptions break hardware projects
- **Asking > Assuming**, always
- 5 minutes of verification saves hours of debugging
- User knows their hardware better than documentation
- When in doubt, ASK

