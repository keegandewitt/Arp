# Custom CC Implementation - Final Questions
**Date:** 2025-11-01
**After Reading:** `main.py`, all core modules

---

## ❓ CRITICAL QUESTIONS (Must Answer Before Implementation)

### 1. CV Output Not Initialized! (BLOCKER)

**Observation:** `main.py` does NOT initialize `CVOutput` anywhere!

**Evidence:**
- Line 82-86: Imports don't include `from arp.drivers.cv_gate import CVOutput`
- Lines 104-137: Initialization section has NO CV output setup
- `cv_gate.py` exists and works, but it's never instantiated in main.py

**Questions:**
1. Is CV output supposed to be initialized?
2. If yes, where should I add it? (After line 137 in initialization section?)
3. If no, why does `cv_gate.py` exist?

**Impact:** If CV isn't initialized, Custom CC won't work at all!

---

### 2. Where to Instantiate CustomCCHandler?

**Current Initialization Order (lines 104-137):**
```python
[1/3] MIDI
[2/3] Display
[3/3] Buttons
[4/5] Settings
[5/5] Clock
```

**Question:** Where should I add CustomCCHandler?

**Options:**
- **Option A:** Add as `[6/6]` after Clock (line 137)
  ```python
  print("[6/6] Initializing Custom CC...")
  custom_cc = CustomCCHandler(cv_output, settings)
  ```

- **Option B:** Add inside CV initialization (if we add it)
  ```python
  print("[X/X] Initializing CV Output...")
  cv_output = CVOutput(i2c, settings)
  custom_cc = CustomCCHandler(cv_output, settings)
  ```

- **Option C:** Don't initialize - create on-demand when menu entered
  ```python
  # In menu handling code
  if not hasattr(self, 'custom_cc'):
      self.custom_cc = CustomCCHandler(...)
  ```

**Which do you prefer?**

---

### 3. Where to Call custom_cc.process_messages()?

**MIDI Processing Loop (lines 260-336):**
```python
msg = midi.receive()
if msg is not None:
    if isinstance(msg, NoteOn):
        # ... arpeggiator logic ...
    elif isinstance(msg, NoteOff):
        # ... arpeggiator logic ...
    else:
        # Pass-through (lines 287-336)
        # Already handles CC, PitchBend, ChannelPressure! ✓
        midi.send(msg)
```

**Question:** Where should I call `custom_cc.process_messages()`?

**Options:**
- **Option A:** Before pass-through (line 287)
  ```python
  else:
      # Process for Custom CC output FIRST
      custom_cc.process_messages([msg])
      # Then pass through to MIDI OUT
      midi.send(msg)
  ```

- **Option B:** After pass-through (line 336)
  ```python
  else:
      midi.send(msg)  # Pass through first
      custom_cc.process_messages([msg])  # Then process for CV
  ```

- **Option C:** Batch processing after msg loop
  ```python
  messages = []
  msg = midi.receive()
  while msg is not None:
      messages.append(msg)
      msg = midi.receive()
  custom_cc.process_messages(messages)  # Process batch
  ```

**Which has lowest latency?**

---

### 4. Button B Long Press - Conflict Check

**Current Button B Usage:**
- **Line 347:** `button_b` captured
- **Line 356:** Used in menu for "select"
- **Line 430:** Used in main mode for "Demo arpeggio"
- **Line 347:** `b_long` is captured but **NEVER USED!** ✓

**Question:** Is button B long press (`b_long`) safe to use for Learn Mode?

**My Analysis:** YES - `b_long` flag exists but is completely unused!
- Not checked in menu mode (lines 349-390)
- Not checked in main mode (lines 405-450)
- Perfect for Learn Mode!

**Confirmation:** Can I use `b_long` for Learn Mode without conflicts?

---

### 5. RAM Constraints - Memory Budget

**Current Memory Tracking (lines 98-102):**
```python
DEBUG_MEMORY = False
if DEBUG_MEMORY:
    print(f"[DEBUG] Startup memory: {gc.mem_free()} bytes free")
```

**Questions:**
1. How much RAM does M4 have total?
2. What's typical `gc.mem_free()` after initialization?
3. Is there a minimum free RAM threshold to maintain?
4. Will adding `CustomCCHandler` + smoothing state (1 float) cause issues?

**My Estimate:**
- `CustomCCHandler` object: ~500 bytes
- Smoothing state (1 float): 4 bytes
- MIDI message buffer: minimal (reusing existing)
- **Total impact: < 1KB**

**Confirmation:** Is 1KB of additional RAM acceptable?

---

### 6. Display Update Rate - MIDI Feedback Concern

**Current Display Update (lines 455-463):**
```python
display_update_interval = 0.1  # Update every 100ms

if not menu.menu_active and (current_time - last_display_update >= display_update_interval):
    display.update_display(...)
```

**Question:** If I show real-time MIDI messages in Custom CC menu, will updating display at 100ms rate cause lag?

**My Analysis:**
- MIDI messages arrive at ~1000 Hz (1ms intervals)
- Display updates at 10 Hz (100ms intervals)
- Worst case: 100 MIDI messages before display updates
- **Should be fine** - just show last received message

**Confirmation:** Is 100ms display update acceptable for MIDI monitoring?

---

### 7. Error Handling Pattern

**Current Error Handling Examples:**
```python
# Line 296-308: Try/except for MIDI send
try:
    midi.send(msg)
except Exception as e:
    print(f"⚠️  Failed real-time pass: {type(msg).__name__}: {e}")

# cv_gate.py line 124: Try/except for DAC write
try:
    dac.channel_a.value = dac_value
except Exception as e:
    print(f"Error setting pitch CV: {e}")
```

**Question:** Should I wrap CustomCC processing in try/except?

**Options:**
- **Option A:** Wrap entire `process_messages()`
  ```python
  try:
      custom_cc.process_messages(messages)
  except Exception as e:
      print(f"Custom CC error: {e}")
  ```

- **Option B:** Wrap only DAC writes (inside CustomCCHandler)
  ```python
  try:
      self.cv_output.set_custom_cc(voltage)
  except Exception as e:
      print(f"Custom CC DAC error: {e}")
  ```

**Which pattern matches your codebase style?**

---

### 8. Import Structure - Where to Add?

**Current Imports (lines 82-86):**
```python
from arp.ui.display import Display
from arp.ui.buttons import ButtonHandler
from arp.core.clock import ClockHandler
from arp.ui.menu import SettingsMenu
from arp.utils.config import Settings
```

**Questions:**
1. Should I add `from arp.drivers.cv_gate import CVOutput`?
2. Should I add `from arp.drivers.midi_custom_cc import CustomCCHandler`?
3. Or should these be conditional imports (only if hardware detected)?

**Pattern Matching:** All current imports are unconditional, so I assume unconditional is correct.

---

### 9. Settings Auto-Save Timing

**Current Auto-Save Pattern (from menu.py line 264):**
```python
def _increase_value(self):
    # ... change value ...
    self.settings.save()  # Save immediately after each change
```

**Question:** Should Custom CC settings auto-save?

**Options:**
- **Option A:** Auto-save immediately (matches existing pattern)
  - Every CC number change → save
  - Every smoothing change → save
  - Pro: Never lose settings
  - Con: Wear on NVM flash

- **Option B:** Save only on menu exit
  - Batch save all changes
  - Pro: Fewer NVM writes
  - Con: Lose changes if power loss

**Which do you prefer?**

---

### 10. CV Output and Arpeggiator Coexistence

**Observation:** If CV output is added to main.py:
- Arpeggiator uses `midi.send()` to send notes (line 210, 218)
- CV output would need to mirror these notes
- Custom CC uses same CV output object

**Question:** Should arpeggiator notes also output to CV pitch (Channel A)?

**Options:**
- **Option A:** Arpeggiator drives both MIDI and CV pitch simultaneously
  ```python
  midi.send(NoteOn(note, velocity))
  cv_output.note_on(note)  # Also send to CV
  ```

- **Option B:** Arpeggiator only drives MIDI (current behavior)
  - Custom CC uses Channel D only
  - CV pitch (Channel A) remains unused

- **Option C:** User-selectable (settings toggle)
  - `settings.cv_output_enabled = True/False`
  - If enabled, arpegg drives CV

**What's your vision for CV integration?**

---

## 📊 Summary of Questions

| # | Question | Severity | Can Proceed Without? |
|---|----------|----------|---------------------|
| 1 | CV Output initialization | CRITICAL | ❌ No - blocks Custom CC |
| 2 | CustomCCHandler instantiation location | HIGH | ✅ Yes - can guess |
| 3 | process_messages() call location | HIGH | ✅ Yes - can guess |
| 4 | Button B long press conflict | MEDIUM | ✅ Yes - seems safe |
| 5 | RAM budget | MEDIUM | ✅ Yes - likely fine |
| 6 | Display update rate | LOW | ✅ Yes - 100ms ok |
| 7 | Error handling pattern | LOW | ✅ Yes - can match style |
| 8 | Import structure | LOW | ✅ Yes - unconditional |
| 9 | Settings auto-save timing | LOW | ✅ Yes - match existing |
| 10 | CV + Arpeggiator coexistence | MEDIUM | ✅ Yes - can defer |

---

## 🎯 Must-Answer Questions (Blockers):

### Question 1: CV Output Initialization
**Status:** CRITICAL BLOCKER
**Why:** Custom CC requires CVOutput object, but it's not initialized in main.py

**Answer Needed:**
- Should I add CVOutput initialization to main.py?
- If yes, where? (After line 137?)
- If no, how does Custom CC get access to DAC?

---

## ✅ Can-Guess Questions (Non-Blockers):

**Questions 2-10:** I can make reasonable guesses based on existing code patterns, but I'd prefer confirmation to avoid rework.

**My Best Guesses:**
- Q2: Initialize as `[6/6]` after Clock
- Q3: Call before pass-through (Option A)
- Q4: `b_long` is safe - unused currently
- Q5: 1KB RAM impact is acceptable
- Q6: 100ms display update is fine
- Q7: Wrap DAC writes (Option B)
- Q8: Unconditional imports
- Q9: Auto-save immediately (match existing)
- Q10: Defer to Phase 2

---

## 🚀 Recommendation:

**Option A: Answer Question 1, I'll implement with best guesses**
- You tell me if/how to initialize CV output
- I proceed with guesses for Questions 2-10
- We iterate if guesses are wrong

**Option B: Answer all 10 questions**
- Takes more time now
- Zero rework later
- Highest confidence (95%+)

**Option C: You show me existing CV test code**
- If CV is used elsewhere, I can see the pattern
- Faster than answering 10 questions

**Which option do you prefer?**
